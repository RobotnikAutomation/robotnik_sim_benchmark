#!/usr/bin/env python3

"""Orchestrate one complete simulator benchmark execution.

This module coordinates configuration, simulator and auxiliary process launch,
readiness detection, warmup, measurement, result writing, and cleanup.  The
actual process lifecycle, monitoring, RViz management, and report serialization
remain delegated to their respective modules.
"""

import argparse
import os
import shutil
import signal
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

import psutil
import rclpy

SCRIPT_ROOT = Path(__file__).resolve().parents[1]
if str(SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPT_ROOT))

from validate.validate_config import (
    DEFAULT_CONFIG_PATH,
    REPOSITORY_ROOT,
    ConfigurationError,
    load_config,
    resolve_category,
    resolve_command,
)
from execute.process_supervisor import ProcessGroupSupervisor
from monitor.monitor import (
    BenchmarkMonitor,
    MangoHudSession,
)
from common.sensor_profile import expected_nonimage_sensor_topics, physics_clock_rate_hz
from report.results import PerformanceResultsWriter, RosResultsWriter
from simulators import SimulatorLaunchContext, get_adapter


_shutdown_requested = False
PERFORMANCE_WRITER = None
ROS_RESULTS_WRITER = None
LAST_ROS_TOPIC_STATISTICS = []
LAUNCH_ENVIRONMENT = {}

# This is deliberately a contract, not a guess from a received Clock message.
# A wall-clock publisher also yields an RTF close to one, so each integration
# has to use a source tied to its simulation timeline.
RTF_CLOCK_SOURCES = {
    "gazebo_harmonic": "Gazebo simulation clock through ros_gz_bridge",
    "webots": "Webots Supervisor robot.getTime()",
    "isaac_sim": "Isaac Sim ROS2_Clock OmniGraph on the first robot",
    "mujoco": "MuJoCo physics clock from mujoco_ros2_control",
    "unity": "Unity completed physics steps (Time.fixedTimeAsDouble)",
    "o3de": "O3DE Physics Scene simulation clock",
}

# A literal 100 % threshold hides cores that are effectively fully occupied
# once scheduler overhead and the sampling interval are accounted for.
CORE_SATURATION_THRESHOLD_PERCENT = 90.0




class Terminal:
    """Small, dependency-free formatter for readable benchmark progress."""

    enabled = sys.stdout.isatty() and os.environ.get("NO_COLOR") is None
    reset = "\033[0m" if enabled else ""
    title = "\033[1;36m" if enabled else ""
    success = "\033[1;32m" if enabled else ""
    warning = "\033[1;33m" if enabled else ""
    muted = "\033[2m" if enabled else ""
    cyan = "\033[1;36m" if enabled else ""
    green = "\033[1;32m" if enabled else ""
    yellow = "\033[1;33m" if enabled else ""
    red = "\033[1;31m" if enabled else ""
    blue = "\033[1;34m" if enabled else ""
    magenta = "\033[1;35m" if enabled else ""
    white = "\033[1;37m" if enabled else ""
    _status_colors = {
        "STARTUP": cyan,
        "READY": green,
        "WARMUP": yellow,
        "MONITORING": blue,
        "PROCESS": cyan,
        "MONITOR": magenta,
        "RESULT": green,
        "SUMMARY": yellow,
        "ERROR": red,
        "WARNING": yellow,
    }
    _progress_active = False
    _progress_rows = None
    _spinner_active = False
    _spinner_index = 0

    @classmethod
    def section(cls, title):
        print(f"\n{'=' * 80}\n{cls.title}{title}{cls.reset}\n{'-' * 80}", flush=True)

    @classmethod
    def status(cls, label, message):
        if label == "PROCESS" and cls._progress_active:
            cls.process_status(message)
            return
        if cls._progress_active:
            cls.finish_progress()
        color = cls._status_colors.get(label, cls.white)
        print(f"{color}[{label}]{cls.reset} {message}", flush=True)

    @classmethod
    @classmethod
    def process_status(cls, message):
        """Render process cleanup messages in the fixed bottom status line."""
        if not sys.stdout.isatty():
            print(f"[PROCESS] {message}", flush=True)
            return
        cls._write_status_line(
            f"[PROCESS] {message}",
            cls._progress_rows or shutil.get_terminal_size(fallback=(120, 24)).lines,
            cls._status_colors["PROCESS"],
        )

    @classmethod
    def progress(cls, label, elapsed, total=None, current=None, maximum=None):
        """Show a live phase indicator without affecting benchmark timing."""
        if not sys.stdout.isatty():
            return
        terminal_rows = shutil.get_terminal_size(fallback=(120, 24)).lines
        if terminal_rows < 3:
            return
        if total is not None:
            percent = min(100.0, max(0.0, elapsed / max(total, 1e-9) * 100.0))
            bar_width = 24
            filled = int(bar_width * percent / 100.0)
            bar = "=" * filled + ">" + " " * max(0, bar_width - filled - 1)
            suffix = f"[{bar}] {percent:5.1f}%"
        else:
            suffix = "[running]"
        if current is not None and maximum is not None:
            suffix += f" topics={current}/{maximum}"
        message = f"[{label}] {suffix} elapsed={elapsed:.1f}s"
        cls._write_status_line(message, terminal_rows, cls._status_colors.get(label, cls.white))

    @classmethod
    def _write_status_line(cls, message, terminal_rows, color=""):
        """Render one status line while preserving the log cursor position."""
        if not cls._progress_active:
            cls._progress_rows = terminal_rows
            cls._progress_active = True
            # DECSTBM resets the cursor and the previous cursor may have
            # been on the physical last row.  That row becomes the status
            # bar, so explicitly place simulator output on the last row of
            # the scrolling region before saving its position.
            log_row = terminal_rows - 1
            prefix = f"\033[1;{log_row}r\033[{log_row};1H\0337"
        else:
            prefix = "\0337"
        row = cls._progress_rows or terminal_rows
        width = max(1, shutil.get_terminal_size().columns - 1)
        visible_message = message[:width]
        rendered_message = f"{color}{visible_message:<{width}}{cls.reset}"
        sys.stdout.write(
            f"{prefix}\033[{row};1H\033[2K{rendered_message}\0338"
        )
        sys.stdout.flush()

    @classmethod
    def spinner(cls, label, elapsed, current=None, maximum=None):
        """Show startup activity in the same fixed status line as other phases."""
        if not sys.stdout.isatty():
            return
        frames = ("|", "/", "-", "\\")
        frame = frames[cls._spinner_index % len(frames)]
        cls._spinner_index += 1
        suffix = f" topics={current}/{maximum}" if current is not None and maximum is not None else ""
        message = f"[{label}] {frame} waiting for simulator readiness; elapsed={elapsed:.1f}s{suffix}"
        cls._spinner_active = True
        cls._write_status_line(
            message,
            shutil.get_terminal_size(fallback=(120, 24)).lines,
            cls._status_colors.get(label, cls.white),
        )

    @classmethod
    def finish_progress(cls):
        if cls._spinner_active and sys.stdout.isatty():
            cls._spinner_active = False
        cls._spinner_active = False
        if cls._progress_active and sys.stdout.isatty():
            row = cls._progress_rows or shutil.get_terminal_size(fallback=(120, 24)).lines
            sys.stdout.write(f"\0337\033[{row};1H\033[2K\033[r\0338\n")
            sys.stdout.flush()
        cls._progress_active = False
        cls._progress_rows = None


def open_process_monitor(supervisor_pid, session_id):
    """Open a terminal that displays the owned process session."""
    if os.environ.get("DISABLE_PROCESS_MONITOR") == "1":
        return None

    monitor_script = (
        f"while kill -0 {supervisor_pid} 2>/dev/null; do "
        f"clear; echo 'Benchmark process session (SID {session_id}, supervisor PID {supervisor_pid})'; "
        f"echo; ps -eo pid=,ppid=,pgid=,sid=,stat=,etime=,args= --forest | "
        f"awk -v sid={session_id} '$4 == sid'; sleep 1; done; "
        "clear; echo 'Supervisor finished; process session is closed.'; "
        "sleep 3"
    )
    executable = "gnome-terminal"
    terminal_path = shutil.which(executable)
    if terminal_path is None:
        Terminal.status("MONITOR", "gnome-terminal is not installed or is not on PATH")
        return None
    try:
        monitor_process = subprocess.Popen(
            [
                terminal_path,
                "--quiet",
                "--wait",
                "--",
                "bash",
                "-lc",
                monitor_script,
            ],
            start_new_session=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        time.sleep(0.25)
        if monitor_process.poll() is not None:
            Terminal.status(
                "MONITOR",
                f"gnome-terminal exited immediately with status {monitor_process.returncode}",
            )
            return None
        Terminal.status("MONITOR", f"opened process monitor for supervisor PID {supervisor_pid}")
        return monitor_process
    except OSError as exc:
        Terminal.status("MONITOR", f"could not open gnome-terminal: {exc}")
        return None

    return None


def render_fps_limit_method(simulator):
    """Select the limiter boundary that matches each render architecture."""
    # Kept for a direct MangoHud session. Benchmark MuJoCo uses its native
    # pacer instead (see render_fps_uses_mangohud_limiter).
    if simulator == "mujoco":
        return "late"
    # Unity owns its deterministic in-player pacer. Keep MangoHud's limiter at
    # the early boundary as a safety ceiling without adding another late sleep.
    return "early"


def render_fps_uses_mangohud_limiter(simulator):
    """Whether MangoHud, rather than the simulator, owns the FPS cap."""
    # MuJoCo has a native UI-loop pacer.  Enabling MangoHud's limiter too
    # creates two independent deadlines around glfwSwapBuffers(), which can
    # alternate and under-run the requested rate under multi-robot load.
    return simulator != "mujoco"


def category_uses_rviz(category):
    """RViz is selected by category, independently of ROS probe workload."""
    return "rviz" in category


def _launch_context(simulator, entry, render_fps, ros_args):
    """Build the adapter context from the normalized declarative entry."""
    return SimulatorLaunchContext(
        simulator=simulator,
        world=str(entry["world"]),
        robot_count=int(entry["robot_count"]),
        robot_model=str(entry["robot_model"]),
        headless=bool(entry["headless"]),
        use_rviz=bool(entry["use_rviz"]),
        render_fps=render_fps,
        ros_args=list(ros_args),
    )


def _format_metric(value, unit="", decimals=2):
    """Format optional numeric metrics consistently for terminal summaries."""
    return "n/a" if value is None else f"{value:.{decimals}f}{unit}"



def _print_iteration_summary(iteration, results):
    """Print concise timing and resource results after one owned iteration."""
    (
        first_frame,
        startup_time,
        cpu,
        cpu_core_peak,
        cpu_core_saturated,
        ram,
        gpu_util,
        _gpu_memory_util,
        _gpu_temperature,
        _gpu_power,
        _gpu_clock,
        gpu_memory,
        rtf_window_mean,
        rtf_global,
        rtf_sample_count,
        rtf_clock_messages,
        rtf_clock_resets,
        rtf_clock_max_gap,
        total,
        monitor_ros,
        image_rate_mean,
        image_rate_min,
        image_payload_total,
        image_max_gap,
        image_message_count,
        render_fps_cap,
        render_fps_mean,
    ) = results
    Terminal.section(f"ITERATION {iteration} COMPLETE")
    print(
        "  Timing    "
        f"first frame {_format_metric(first_frame, 's')}  |  "
        f"startup {_format_metric(startup_time, 's')}  |  "
        f"measurement {ITERATION_TIME}s  |  total {total:.2f}s"
    )
    print(
        "  Resources "
        f"CPU host {_format_metric(cpu, '%')}  |  "
        f"CPU core peak {_format_metric(cpu_core_peak, '%')}  |  "
        f"cores >= {CORE_SATURATION_THRESHOLD_PERCENT:g}% {_format_metric(cpu_core_saturated)}  |  "
        f"RAM {_format_metric(ram, ' MiB')}  |  "
        f"GPU {_format_metric(gpu_util, '%')}  |  VRAM {_format_metric(gpu_memory, ' MiB')}"
    )
    print(
        "  Simulation RTF "
        f"windows {_format_metric(rtf_window_mean, decimals=3)} "
        f"({rtf_sample_count} × {RTF_WINDOW_SECONDS:g}s)  |  "
        f"global {_format_metric(rtf_global, decimals=3)}  |  "
        f"clock {rtf_clock_messages} msg, {rtf_clock_resets} reset, "
        f"gap {_format_metric(rtf_clock_max_gap, 's', decimals=3)}"
    )
    print(
        f"  ROS monitor {'enabled' if monitor_ros else 'disabled'} "
        f"({RTF_CLOCK_SOURCES[SELECTED_SIMULATOR]})"
    )
    if render_fps_cap is not None:
        print(
            "  Render FPS "
            f"cap {render_fps_cap}  |  mean {_format_metric(render_fps_mean, ' FPS')}"
        )
    if monitor_ros:
        print(
            "  ROS images "
            f"mean {_format_metric(image_rate_mean, ' Hz')}  |  "
            f"slowest {_format_metric(image_rate_min, ' Hz')}  |  "
            f"payload {_format_metric(image_payload_total, ' MiB/s')}  |  "
            f"max gap {_format_metric(image_max_gap, 's', decimals=3)}  |  "
            f"messages {image_message_count}"
        )


def _request_shutdown(signum, _frame):
    """Turn terminal closure and service stop into normal iteration cleanup."""
    global _shutdown_requested
    signal_name = signal.Signals(signum).name
    if not _shutdown_requested:
        _shutdown_requested = True
        print(f"\nReceived {signal_name}; cleaning up the active iteration...", flush=True)
        raise KeyboardInterrupt
    print(f"\nCleanup already in progress after {signal_name}; please wait.", flush=True)


def _install_shutdown_handlers():
    for handled_signal in (signal.SIGINT, signal.SIGTERM, signal.SIGHUP):
        signal.signal(handled_signal, _request_shutdown)



def positive_int(value):
    """Argparse converter for strictly positive integers."""
    try:
        parsed = int(value)
    except (TypeError, ValueError) as exc:
        raise argparse.ArgumentTypeError(f"expected an integer, got {value!r}") from exc
    if parsed <= 0:
        raise argparse.ArgumentTypeError("value must be greater than zero")
    return parsed


def nonnegative_int(value):
    """Argparse converter for retry counts."""
    try:
        parsed = int(value)
    except (TypeError, ValueError) as exc:
        raise argparse.ArgumentTypeError(f"expected an integer, got {value!r}") from exc
    if parsed < 0:
        raise argparse.ArgumentTypeError("value must not be negative")
    return parsed


def nonnegative_float(value):
    """Argparse converter for cleanup grace periods."""
    try:
        parsed = float(value)
    except (TypeError, ValueError) as exc:
        raise argparse.ArgumentTypeError(f"expected a number, got {value!r}") from exc
    if parsed < 0:
        raise argparse.ArgumentTypeError("value must not be negative")
    return parsed


def positive_float(value):
    """Argparse converter for strictly positive durations."""
    try:
        parsed = float(value)
    except (TypeError, ValueError) as exc:
        raise argparse.ArgumentTypeError(f"expected a number, got {value!r}") from exc
    if parsed <= 0:
        raise argparse.ArgumentTypeError("value must be greater than zero")
    return parsed


def parse_arguments():
    parser = argparse.ArgumentParser(description="Benchmark a configured simulator")
    parser.add_argument(
        "simulator",
        choices=("gazebo_harmonic", "webots", "isaac_sim", "unity", "o3de", "mujoco"),
    )
    parser.add_argument("--csv_file", default="", help="CSV output path")
    parser.add_argument(
        "--ros-topic-csv-file", default="",
        help="Separate per-topic ROS statistics CSV output path",
    )
    parser.add_argument("--iterations", type=positive_int, default=1)
    parser.add_argument(
        "--category",
        default="1",
        help="One-based category number (1-24) or exact category name",
    )
    parser.add_argument(
        "--ros_args",
        nargs="*",
        default=[],
        help="Additional ROS 2 arguments appended to both configured commands",
    )
    parser.add_argument(
        "--iteration_time",
        type=positive_int,
        default=60,
        help="Measurement time after all image topics become ready",
    )
    parser.add_argument(
        "--startup_timeout",
        type=positive_int,
        default=120,
        help="Maximum seconds to wait for all configured image topics",
    )
    parser.add_argument(
        "--warmup-time",
        type=nonnegative_float,
        default=0.0,
        help="Seconds to stabilize after readiness before measurement (default: 0)",
    )
    parser.add_argument(
        "--max_retries",
        type=nonnegative_int,
        default=3,
        help="Retries after a failed iteration (default: 3)",
    )
    parser.add_argument(
        "--retry_cooldown",
        type=nonnegative_float,
        default=5.0,
        help="Seconds to wait after cleanup before retrying (default: 5)",
    )
    parser.add_argument(
        "--iteration_cooldown",
        type=nonnegative_float,
        default=5.0,
        help="Seconds to wait between iterations (default: 5)",
    )
    parser.add_argument(
        "--sigint_timeout",
        type=nonnegative_float,
        default=10.0,
        help="Grace period after SIGINT during cleanup",
    )
    parser.add_argument(
        "--sigterm_timeout",
        type=nonnegative_float,
        default=5.0,
        help="Grace period after SIGTERM during cleanup",
    )
    parser.add_argument(
        "--final-cleanup-timeout",
        type=nonnegative_float,
        default=30.0,
        help="Extra bounded SIGKILL/reap time before an iteration may be retried",
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=Path(os.environ.get("LAUNCH_CONFIGS_PATH", DEFAULT_CONFIG_PATH)),
        help="Benchmark YAML configuration path",
    )
    parser.add_argument(
        "--process-monitor",
        dest="process_monitor",
        action="store_true",
        default=False,
        help="Open the live process tree in another terminal.",
    )
    parser.add_argument(
        "--monitor-ros",
        action="store_true",
        help=(
            "Enable persistent external ROS transport monitoring after readiness "
            "(disabled by default)."
        ),
    )
    parser.add_argument(
        "--render-fps",
        type=int,
        default=60,
        help="GUI render FPS cap (1..1000; headless runs do not capture FPS)",
    )
    return parser.parse_args()


def configure(args):
    """Validate CLI/config and initialize immutable run settings."""
    global SELECTED_CATEGORY, SELECTED_SIMULATOR
    global LAUNCH_COMMANDS, LAUNCH_ENVIRONMENT, IMAGE_TOPICS
    global CSV_PATH, ROS_TOPIC_CSV_PATH, ITERATIONS, ITERATION_TIME, STARTUP_TIMEOUT, RTF_WINDOW_SECONDS
    global SIGINT_TIMEOUT, SIGTERM_TIMEOUT, FINAL_CLEANUP_TIMEOUT, MAX_RETRIES, RETRY_COOLDOWN
    global ITERATION_COOLDOWN, PROCESS_MONITOR, MONITOR_ROS, WARMUP_TIME
    global RENDER_FPS_CAP, RENDER_FPS_ENABLED
    global PERFORMANCE_WRITER, ROS_RESULTS_WRITER

    config = load_config(args.config)
    SELECTED_CATEGORY = resolve_category(args.category)
    SELECTED_SIMULATOR = args.simulator
    entry = config[SELECTED_SIMULATOR][SELECTED_CATEGORY]
    render_fps_cap = MangoHudSession.validate_render_fps(args.render_fps)
    MONITOR_ROS = args.monitor_ros
    # Monitoring is optional, but readiness always uses the configured image
    # topics, so startup retains the same definition in both modes.
    uses_rviz = category_uses_rviz(SELECTED_CATEGORY)
    launch_context = _launch_context(
        SELECTED_SIMULATOR,
        entry,
        render_fps_cap,
        args.ros_args,
    )
    adapter = get_adapter(SELECTED_SIMULATOR, entry, REPOSITORY_ROOT)
    launch_plan = adapter.build_launch_plan(launch_context)
    rviz_command = None
    if uses_rviz:
        robot_count = {"one": 1, "two": 2, "three": 3}[SELECTED_CATEGORY.split("_", 1)[0]]
        rviz_command = [
            sys.executable,
            str(REPOSITORY_ROOT / "scripts" / "execute" / "run_rviz.py"),
            SELECTED_SIMULATOR,
            str(robot_count),
        ]
    LAUNCH_COMMANDS = [resolve_command(command) for command in launch_plan.commands]
    LAUNCH_ENVIRONMENT = dict(launch_plan.environment)
    if sys.stdout.isatty() and os.environ.get("NO_COLOR") is None:
        # Keep ROS/Gazebo log severity readable in the interactive terminal;
        # redirected runs retain their plain, machine-friendly output.
        LAUNCH_ENVIRONMENT.setdefault("RCUTILS_COLORIZED_OUTPUT", "1")
        if os.environ.get("TERM") in (None, "", "dumb"):
            LAUNCH_ENVIRONMENT.setdefault("TERM", "xterm-256color")
    if rviz_command is not None:
        LAUNCH_COMMANDS.append(rviz_command)
    IMAGE_TOPICS = list(launch_plan.readiness_topics)
    ITERATIONS = args.iterations
    ITERATION_TIME = args.iteration_time
    RTF_WINDOW_SECONDS = 1.0
    STARTUP_TIMEOUT = args.startup_timeout
    WARMUP_TIME = args.warmup_time
    MAX_RETRIES = args.max_retries
    RETRY_COOLDOWN = args.retry_cooldown
    ITERATION_COOLDOWN = args.iteration_cooldown
    SIGINT_TIMEOUT = args.sigint_timeout
    SIGTERM_TIMEOUT = args.sigterm_timeout
    FINAL_CLEANUP_TIMEOUT = args.final_cleanup_timeout
    PROCESS_MONITOR = args.process_monitor
    RENDER_FPS_CAP = render_fps_cap
    RENDER_FPS_ENABLED = "headless" not in SELECTED_CATEGORY

    if args.csv_file:
        CSV_PATH = Path(args.csv_file).expanduser().resolve()
    else:
        output_dir = REPOSITORY_ROOT / "benchmarks" / SELECTED_SIMULATOR / SELECTED_CATEGORY
        CSV_PATH = output_dir / f"ros2_launch_timings_{int(time.time())}.csv"
    if args.ros_topic_csv_file:
        ROS_TOPIC_CSV_PATH = Path(args.ros_topic_csv_file).expanduser().resolve()
    else:
        ROS_TOPIC_CSV_PATH = CSV_PATH.with_name(f"ros_topic_stats_{CSV_PATH.stem.rsplit('_', 1)[-1]}.csv")
    CSV_PATH.parent.mkdir(parents=True, exist_ok=True)
    PERFORMANCE_WRITER = PerformanceResultsWriter(CSV_PATH)
    ROS_RESULTS_WRITER = (
        RosResultsWriter(ROS_TOPIC_CSV_PATH) if MONITOR_ROS else None
    )
    MangoHudSession(
        CSV_PATH.parent / "render_fps",
        RENDER_FPS_CAP,
        RENDER_FPS_ENABLED,
        # Unity's main-thread player needs the post-present boundary. O3DE can
        # queue frames from its render thread and therefore uses early pacing.
        fps_limit_method=render_fps_limit_method(SELECTED_SIMULATOR),
        apply_fps_limit=render_fps_uses_mangohud_limiter(SELECTED_SIMULATOR),
    ).validate_dependencies()


def run_iteration(iter_num, attempt=1):
    """Run one iteration through the prepare, launch, measure, and cleanup pipeline."""
    global LAST_ROS_TOPIC_STATISTICS
    Terminal.section(
        f"ITERATION {iter_num}/{ITERATIONS} · ATTEMPT {attempt}/{MAX_RETRIES + 1} · "
        f"{SELECTED_SIMULATOR} · {SELECTED_CATEGORY}"
    )
    iteration_started = time.monotonic()
    render_session = MangoHudSession(
        CSV_PATH.parent / "render_fps" / f"iteration_{iter_num}_attempt_{attempt}_{time.monotonic_ns()}",
        RENDER_FPS_CAP,
        RENDER_FPS_ENABLED,
        fps_limit_method=render_fps_limit_method(SELECTED_SIMULATOR),
        apply_fps_limit=render_fps_uses_mangohud_limiter(SELECTED_SIMULATOR),
    )
    launch_commands = list(LAUNCH_COMMANDS)
    launch_commands[0] = render_session.wrap_command(launch_commands[0])
    process_supervisor = ProcessGroupSupervisor(
        launch_commands,
        environment=LAUNCH_ENVIRONMENT,
        graceful_timeout=SIGINT_TIMEOUT,
        terminate_timeout=SIGTERM_TIMEOUT,
        final_cleanup_timeout=FINAL_CLEANUP_TIMEOUT,
        logger=lambda message: Terminal.status("PROCESS", message),
    )
    monitor = BenchmarkMonitor(
        context={
            "simulator": SELECTED_SIMULATOR,
            "category": SELECTED_CATEGORY,
            "iteration": iter_num,
            "rtf_window_seconds": RTF_WINDOW_SECONDS,
        },
        process_supervisor=process_supervisor,
        monitor_ros=MONITOR_ROS,
    )
    measurement_results = {}
    readiness_result = None
    measurement_ended = None

    try:
        _install_shutdown_handlers()
        monitor.prepare(
            IMAGE_TOPICS,
            expected_nonimage_sensor_topics(SELECTED_SIMULATOR, SELECTED_CATEGORY),
            render_monitor=render_session,
        )
        process_supervisor.start()
        if PROCESS_MONITOR:
            open_process_monitor(
                process_supervisor.supervisor_process.pid,
                process_supervisor.sid,
            )
        startup_started = process_supervisor.launch_started_monotonic
        if startup_started is None:
            raise RuntimeError("Process supervisor did not report a launch timestamp")
        monitor.mark_launch_started(startup_started)
        Terminal.status("STARTUP", "waiting for first frame and all configured image topics")
        try:
            readiness_result = monitor.wait_until_ready(
                STARTUP_TIMEOUT,
                progress_callback=lambda elapsed, total, current, maximum: Terminal.spinner(
                    "STARTUP", elapsed, current, maximum
                ),
            )
        finally:
            Terminal.finish_progress()
        Terminal.status(
            "READY",
            f"all image topics received after {readiness_result.startup_seconds:.2f}s; "
            "starting stabilization and measurement boundary",
        )
        if WARMUP_TIME > 0:
            Terminal.status("WARMUP", f"stabilizing for {WARMUP_TIME:g}s")
            warmup_started = time.monotonic()
            next_warmup_progress = warmup_started
            try:
                while True:
                    now = time.monotonic()
                    elapsed = now - warmup_started
                    if now >= next_warmup_progress:
                        Terminal.progress("WARMUP", elapsed, WARMUP_TIME)
                        next_warmup_progress = now + 1.0
                    if elapsed >= WARMUP_TIME:
                        break
                    time.sleep(min(0.05, WARMUP_TIME - elapsed))
                Terminal.progress("WARMUP", WARMUP_TIME, WARMUP_TIME)
            finally:
                Terminal.finish_progress()
        measurement_started = time.monotonic()
        monitor.start_measurement(measurement_started)
        measurement_deadline = measurement_started + ITERATION_TIME
        Terminal.status("MONITORING", f"collecting metrics for {ITERATION_TIME:g}s")
        next_measurement_progress = measurement_started
        measurement_completed = False
        try:
            while rclpy.ok() and time.monotonic() < measurement_deadline:
                if process_supervisor.command_failure is not None:
                    raise RuntimeError(process_supervisor.command_failure)
                if process_supervisor.returncode not in (None, 0):
                    raise RuntimeError(
                        f"Iteration launcher exited with status {process_supervisor.returncode}"
                    )
                now = time.monotonic()
                if now >= next_measurement_progress:
                    Terminal.progress(
                        "MONITORING",
                        now - measurement_started,
                        ITERATION_TIME,
                    )
                    next_measurement_progress = now + 1.0
                time.sleep(min(0.05, max(0.0, measurement_deadline - now)))
            measurement_completed = rclpy.ok()
        finally:
            if not measurement_completed:
                Terminal.finish_progress()
        if not rclpy.ok():
            raise RuntimeError("ROS context stopped before measurement completed")
        Terminal.progress("MONITORING", ITERATION_TIME, ITERATION_TIME)
        measurement_ended = time.monotonic()
        measurement_results = monitor.stop_measurement(ITERATION_TIME)
        ros_statistics = list(measurement_results.get("ros_topic_statistics", []))
        clock_statistics = measurement_results["rtf_clock_statistics"]
        if MONITOR_ROS:
            ros_statistics.append({
                "topic": "/clock",
                "topic_type": "rosgraph_msgs/msg/Clock",
                "publisher_count": None,
                "message_count": clock_statistics["message_count"],
                "rate_hz": clock_statistics["message_count"] / ITERATION_TIME,
                "payload_mib_s": None,
                "max_gap_seconds": clock_statistics["max_gap_seconds"],
            })
        image_statistics = [
            row for topic_name in IMAGE_TOPICS
            for row in ros_statistics
            if row["topic"] == topic_name
        ]
        image_rates = [row["rate_hz"] for row in image_statistics]
        image_rate_mean = sum(image_rates) / len(image_rates) if image_rates else None
        image_rate_min = min(image_rates) if image_rates else None
        image_payload_total = (
            sum(row["payload_mib_s"] for row in image_statistics)
            if image_statistics else None
        )
        image_max_gap = (
            max(row["max_gap_seconds"] for row in image_statistics)
            if image_statistics else None
        )
        image_message_count = sum(row["message_count"] for row in image_statistics)
        monitor.validate_rtf(ITERATION_TIME)
        LAST_ROS_TOPIC_STATISTICS = ros_statistics
        iteration_total_time = time.monotonic() - iteration_started
        resources = measurement_results
        return (
            readiness_result.first_frame_seconds,
            readiness_result.startup_seconds,
            resources["cpu_mean_percent"],
            resources["cpu_core_peak_mean_percent"],
            resources["cpu_core_saturated_mean_count"],
            resources["ram_mean_mb"],
            resources["gpu_mean_percent"],
            resources["gpu_memory_util_mean_percent"],
            resources["gpu_temperature_mean_c"],
            resources["gpu_power_mean_w"],
            resources["gpu_clock_mean_mhz"],
            resources["gpu_mem_mean_mb"],
            resources["real_time_factor_mean"],
            resources["real_time_factor_global"],
            resources["real_time_factor_sample_count"],
            clock_statistics["message_count"],
            clock_statistics["rewind_count"],
            clock_statistics["max_gap_seconds"],
            iteration_total_time,
            MONITOR_ROS,
            image_rate_mean,
            image_rate_min,
            image_payload_total,
            image_max_gap,
            image_message_count,
            RENDER_FPS_CAP if RENDER_FPS_ENABLED else None,
            resources["render_fps_mean"],
        )
    finally:
        Terminal.process_status("stopping iteration processes")
        try:
            monitor.close()
        finally:
            cleanup_report = process_supervisor.stop()
            Terminal.finish_progress()
        if cleanup_report.survivors:
            raise RuntimeError(
                "Iteration cleanup incomplete; refusing to save a contaminated "
                f"measurement (survivor PIDs: {list(cleanup_report.survivors)})"
            )

def run_iteration_with_retries(iter_num, run_once=run_iteration, sleep=time.sleep):
    """Run one logical iteration, discarding failed attempts after cleanup."""
    total_attempts = MAX_RETRIES + 1
    for attempt in range(1, total_attempts + 1):
        try:
            return run_once(iter_num, attempt)
        except Exception as exc:
            retries_left = total_attempts - attempt
            Terminal.status(
                "FAILED",
                f"iteration {iter_num}, attempt {attempt}/{total_attempts}: "
                f"{type(exc).__name__}: {exc}",
            )
            if retries_left == 0:
                Terminal.status(
                    "SKIP",
                    f"iteration {iter_num} discarded after {MAX_RETRIES} retries; "
                    "continuing with the next iteration",
                )
                return None
            Terminal.status(
                "RETRY",
                f"cleanup complete; retrying in {RETRY_COOLDOWN:g}s "
                f"({retries_left} {'retry' if retries_left == 1 else 'retries'} remaining)",
            )
            sleep(RETRY_COOLDOWN)
    return None


def main():
    try:
        configure(parse_arguments())
        metadata_path = PERFORMANCE_WRITER.write_metadata({
            "simulator": SELECTED_SIMULATOR,
            "category": SELECTED_CATEGORY,
            "launch_commands": LAUNCH_COMMANDS,
            "image_topics": IMAGE_TOPICS,
            "iterations": ITERATIONS,
            "iteration_time_seconds": ITERATION_TIME,
            "startup_timeout_seconds": STARTUP_TIMEOUT,
            "warmup_time_seconds": WARMUP_TIME,
            "rtf_window_seconds": RTF_WINDOW_SECONDS,
            "rtf_clock_source_contract": RTF_CLOCK_SOURCES[SELECTED_SIMULATOR],
            "rtf_clock_nominal_hz": physics_clock_rate_hz(SELECTED_SIMULATOR),
            "monitor_ros": MONITOR_ROS,
            "ros_topic_csv_file": ROS_TOPIC_CSV_PATH.name if MONITOR_ROS else None,
            "external_process_monitor": PROCESS_MONITOR,
            "rtf_policy": "cap_1",
            "render_fps_cap": RENDER_FPS_CAP if RENDER_FPS_ENABLED else None,
            "render_fps_source": "mangohud" if RENDER_FPS_ENABLED else None,
            "environment": {
                "ros_distro": os.environ.get("ROS_DISTRO"),
                "ros_domain_id": os.environ.get("ROS_DOMAIN_ID", "0"),
                "ros_localhost_only": os.environ.get("ROS_LOCALHOST_ONLY", "0"),
                "logical_cpu_count": psutil.cpu_count(),
            },
            "measurement_semantics": {
                "cpu_mean_percent": "mean CPU percentage attributed to iteration-owned processes",
                "ram_mean_mb": "mean RSS of iteration-owned processes",
                "gpu_mean_percent": "device-wide GPU utilization",
                "gpu_mem_mean_mb": "GPU memory attributed to iteration-owned process IDs",
                "rtf_clock_message_count": "Clock messages received during the measurement window",
                "render_fps_mean": "mean presented GUI FPS; null for headless runs",
            },
        })
    except ConfigurationError as exc:
        print(f"Configuration error: {exc}", file=sys.stderr)
        return 2

    _install_shutdown_handlers()
    Terminal.status("METADATA", f"saved run definition to {metadata_path}")
    skipped_iterations = []
    try:
        for i in range(1, ITERATIONS + 1):
            results = run_iteration_with_retries(i)
            if results is not None:
                timestamp = datetime.now().isoformat()
                PERFORMANCE_WRITER.write_iteration([
                    SELECTED_SIMULATOR,
                    timestamp,
                    i,
                    *results,
                ])
                if MONITOR_ROS:
                    ROS_RESULTS_WRITER.write_ros_topics(
                        SELECTED_SIMULATOR,
                        SELECTED_CATEGORY,
                        i,
                        timestamp,
                        LAST_ROS_TOPIC_STATISTICS,
                    )
                _print_iteration_summary(i, results)
                Terminal.status("RESULT", f"simulator data saved to {CSV_PATH}")
                if MONITOR_ROS:
                    Terminal.status("RESULT", f"ROS topic data saved to {ROS_TOPIC_CSV_PATH}")
            else:
                skipped_iterations.append(i)
            if i < ITERATIONS:
                cooldown = ITERATION_COOLDOWN
                Terminal.status(
                    "NEXT", f"waiting {cooldown:g} seconds before the next iteration"
                )
                time.sleep(cooldown)
    except KeyboardInterrupt:
        print("Benchmark interrupted; owned processes have been cleaned up.", flush=True)
        return 130
    if skipped_iterations:
        Terminal.status(
            "SUMMARY",
            f"discarded iterations: {', '.join(map(str, skipped_iterations))}; "
            "no CSV rows were written for them",
        )
        return 1
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
