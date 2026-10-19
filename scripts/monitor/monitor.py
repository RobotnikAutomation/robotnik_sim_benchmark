"""Unified benchmark monitoring for resources, ROS, simulation time, FPS, and readiness."""

from __future__ import annotations

import json
import csv
import os
import random
import signal
import shutil
import socket
import subprocess
import threading
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import psutil
import rclpy
from rclpy.executors import SingleThreadedExecutor
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from rosgraph_msgs.msg import Clock
from sensor_msgs.msg import Image

from rosidl_runtime_py.utilities import get_message


class RosMonitor(Node):
    """Discover published topics and measure their received ROS transport."""

    def __init__(self, excluded_topics=()):
        super().__init__("benchmark_topic_monitor")
        self.excluded_topics = set(excluded_topics)
        self._records = {}
        # ``Node`` owns ``_subscriptions`` internally and expects it to be a
        # list.  Keep the monitor's topic lookup separate; replacing the Node
        # attribute makes every create_subscription() fail at runtime.
        self._topic_subscriptions = {}
        self._lock = threading.Lock()
        self.discovery_errors = []

    def discover(self):
        """Subscribe once to every currently published, supported topic."""
        discovered = {
            topic_name: type_names[0]
            for topic_name, type_names in self.get_topic_names_and_types()
            if type_names
        }
        for topic_name, type_name in discovered.items():
            self._subscribe(topic_name, type_name)
        return len(self._topic_subscriptions)

    def subscribe(self, topic_name, type_name):
        """Subscribe to a known topic even before its publisher is visible.

        Some simulator bridges only advertise their sensor publisher after a
        ROS subscriber exists.  Keeping this separate from graph discovery
        avoids a publisher/subscriber discovery deadlock for those streams.
        """
        self._subscribe(topic_name, type_name)
        return topic_name in self._topic_subscriptions

    def _subscribe(self, topic_name, type_name):
        if topic_name in self.excluded_topics or topic_name in self._topic_subscriptions:
            return
        try:
            message_type = get_message(type_name)
            subscription = self.create_subscription(
                message_type,
                topic_name,
                lambda message, name=topic_name: self._callback(name, message),
                qos_profile_sensor_data,
                raw=True,
            )
        except (ImportError, AttributeError, RuntimeError, TypeError, ValueError) as exc:
            self.discovery_errors.append(f"{topic_name} [{type_name}]: {exc}")
            return
        self._topic_subscriptions[topic_name] = subscription
        publisher_count = len(self.get_publishers_info_by_topic(topic_name))
        self._records[topic_name] = {
            "topic": topic_name,
            "topic_type": type_name,
            "publisher_count": publisher_count,
            "message_count": 0,
            "payload_bytes": 0,
            "first_message_monotonic": None,
            "last_message_monotonic": None,
            "maximum_gap_seconds": 0.0,
        }

    def _callback(self, topic_name, serialized_message):
        now = time.monotonic()
        payload_size = len(serialized_message) if isinstance(serialized_message, (bytes, bytearray)) else 0
        with self._lock:
            record = self._records[topic_name]
            previous = record["last_message_monotonic"]
            if previous is not None:
                record["maximum_gap_seconds"] = max(
                    record["maximum_gap_seconds"], now - previous
                )
            record["first_message_monotonic"] = record["first_message_monotonic"] or now
            record["last_message_monotonic"] = now
            record["message_count"] += 1
            record["payload_bytes"] += payload_size

    def start_measurement(self):
        with self._lock:
            for record in self._records.values():
                record.update(
                    message_count=0,
                    payload_bytes=0,
                    first_message_monotonic=None,
                    last_message_monotonic=None,
                    maximum_gap_seconds=0.0,
                )

    def statistics(self, ended_monotonic, duration):
        """Return stable, CSV-friendly statistics for every discovered topic."""
        with self._lock:
            rows = []
            for record in self._records.values():
                record["publisher_count"] = len(
                    self.get_publishers_info_by_topic(record["topic"])
                )
                last = record["last_message_monotonic"]
                final_gap = duration if last is None else ended_monotonic - last
                rows.append({
                    "topic": record["topic"],
                    "topic_type": record["topic_type"],
                    "publisher_count": record["publisher_count"],
                    "message_count": record["message_count"],
                    "rate_hz": record["message_count"] / duration,
                    "payload_mib_s": record["payload_bytes"] / (1024 * 1024) / duration,
                    "max_gap_seconds": max(record["maximum_gap_seconds"], final_gap),
                })
            return rows



class MangoHudSession:
    """Own one iteration's hidden MangoHud limiter and CSV capture."""

    class Error(RuntimeError):
        """Raised when a requested GUI FPS measurement cannot be collected."""

    @staticmethod
    def validate_render_fps(value: int) -> int:
        """Validate the FPS contract shared by MangoHud and the launcher."""
        if not 1 <= value <= 1000:
            raise ValueError("render FPS must be an integer between 1 and 1000")
        return value

    def __init__(
        self,
        output_dir: Path,
        fps_cap: int,
        enabled: bool,
        fps_limit_method: str = "early",
        apply_fps_limit: bool = True,
    ) -> None:
        self.output_dir = output_dir
        self.fps_cap = self.validate_render_fps(fps_cap)
        self.enabled = enabled
        if fps_limit_method not in {"early", "late"}:
            raise ValueError("FPS limit method must be one of: early, late")
        self.fps_limit_method = fps_limit_method
        self.apply_fps_limit = apply_fps_limit
        # MangoHud 0.6.x exposes an *abstract* Unix socket.  Keeping the
        # protocol here avoids relying on a distro-specific control client
        # (Ubuntu calls it ``mangohudctl``, but that controls MangoApp rather
        # than injected MangoHud instances).
        self.socket_name = f"robotnik-fps-{os.getpid()}-{time.monotonic_ns()}"
        self._control_socket: socket.socket | None = None
        self._started = False
        self._measurement_elapsed_floor: dict[Path, float] = {}

    def validate_dependencies(self) -> None:
        if not self.enabled:
            return
        missing = [name for name in ("mangohud",) if shutil.which(name) is None]
        if missing:
            raise self.Error(
                "GUI FPS benchmarking requires " + ", ".join(missing)
            )

    def wrap_command(self, command: list[str]) -> list[str]:
        """Return a command whose graphical descendants inherit MangoHud."""
        if not self.enabled:
            return command
        self.output_dir.mkdir(parents=True, exist_ok=True)
        # MangoHud configuration entries are comma-separated. A '+' only has
        # a special meaning within selected *values* (for example a list of
        # FPS limits), and MangoHud 0.6.x treats it as part of the key name.
        config_entries = ["no_display"]
        if self.apply_fps_limit:
            config_entries.extend(
                (
                    f"fps_limit={self.fps_cap}",
                    # O3DE submits rendering from a dedicated thread. MangoHud's
                    # default late limiter sleeps after present, which lets that
                    # thread queue additional frames and exceed a low cap. Limit
                    # before present so the configured cap is a hard boundary.
                    f"fps_limit_method={self.fps_limit_method}",
                )
            )
        config_entries.extend(
            (
                # Keep MangoHud from adding VSync pacing; a simulator with a
                # native pacer remains the sole owner of its present deadline.
                "vsync=1",  # MangoHud: Vulkan VSync off
                "gl_vsync=0",
                f"output_folder={self.output_dir}",
                f"control={self.socket_name}",
                "log_interval=100",
                "benchmark_percentiles=AVG",
            )
        )
        config = ",".join(config_entries)
        return [
            "env",
            "MANGOHUD=1",
            f"ROBOTNIK_RENDER_FPS={self.fps_cap}",
            f"MANGOHUD_CONFIG={config}",
            "mangohud",
            "--dlsym",
            *command,
        ]

    def _control(self, action: str, required: bool) -> None:
        if not self.enabled:
            return
        if action == "start-logging":
            self._connect_control_socket(required)
            if self._control_socket is not None:
                self._control_socket.sendall(b":logging=1;")
            return

        if action != "stop-logging" or self._control_socket is None:
            if required:
                raise self.Error("MangoHud render control socket is unavailable")
            return
        try:
            self._control_socket.sendall(b":logging=0;")
            deadline = time.monotonic() + 5.0
            response = b""
            while time.monotonic() < deadline:
                try:
                    response += self._control_socket.recv(4096)
                except socket.timeout:
                    continue
                if b"LoggingFinished" in response:
                    return
                if not response:
                    break
            if required:
                raise self.Error("MangoHud did not confirm that FPS logging stopped")
        finally:
            self._close_control_socket()

    def _connect_control_socket(self, required: bool) -> None:
        deadline = time.monotonic() + 10.0
        last_error: OSError | None = None
        while time.monotonic() < deadline:
            connection = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            connection.settimeout(0.5)
            try:
                connection.connect("\0" + self.socket_name)
            except OSError as error:
                last_error = error
                connection.close()
                time.sleep(0.1)
                continue
            self._control_socket = connection
            return
        if required:
            detail = f": {last_error}" if last_error else ""
            raise self.Error("MangoHud did not create a render control socket" + detail)

    def _close_control_socket(self) -> None:
        if self._control_socket is not None:
            self._control_socket.close()
            self._control_socket = None

    def start_measurement(self) -> None:
        self._control("start-logging", required=True)
        # The CSV may retain startup rows even when logging is toggled via the
        # control socket. Record its process-relative watermark so the final
        # result begins at the monitoring boundary.
        self._measurement_elapsed_floor = {
            path: self._max_elapsed_from_csv(path)
            for path in self.output_dir.glob("*.csv")
            if not path.name.endswith("_summary.csv")
        }
        self._started = True

    def finish_measurement(self) -> float | None:
        if not self.enabled:
            return None
        if not self._started:
            raise self.Error("MangoHud measurement never started")
        self._control("stop-logging", required=True)
        deadline = time.monotonic() + 5.0
        files = []
        while not files and time.monotonic() < deadline:
            files = sorted(self.output_dir.glob("*.csv"))
            if not files:
                time.sleep(0.1)
        if not files:
            raise self.Error("MangoHud did not write an FPS CSV")
        # MangoHud writes a raw log and then a derived ``*_summary.csv`` for
        # the same graphical process.  They are two representations of one
        # stream, not two injected applications.  Prefer the raw time-series
        # samples so the steady-state window is measured directly.
        raw_files = [path for path in files if not path.name.endswith("_summary.csv")]
        if raw_files:
            files = raw_files
        # MuJoCo owns the cap in its visible GLFW window. MangoHud is injected
        # into the whole ROS process, so its process-wide CSV can also contain
        # startup/hidden-context swaps which are not presentations from that
        # window. They can be thousands of FPS and must not pollute its GUI
        # metric. Keep normal jitter but reject samples impossible under the
        # native cap.
        maximum_fps = self.fps_cap * 1.2 if not self.apply_fps_limit else None
        means = [
            self._mean_fps_from_csv(
                path,
                maximum_fps=maximum_fps,
                minimum_elapsed=self._measurement_elapsed_floor.get(path),
            )
            for path in files
        ]
        values = [value for value in means if value is not None]
        if len(values) != 1:
            raise self.Error(
                "expected exactly one graphical MangoHud log, found "
                f"{len(values)} usable logs"
            )
        return values[0]

    @staticmethod
    def _csv_rows(path: Path) -> list[dict[str, str]]:
        """Read a MangoHud raw or summary CSV while tolerating its preamble."""
        with path.open(encoding="utf-8-sig") as stream:
            lines = stream.readlines()

        header_index = next(
            (
                index
                for index, line in enumerate(lines)
                if {
                    column.strip().lower().replace(" ", "")
                    for column in next(csv.reader([line]), [])
                }
                >= {"fps", "frametime"}
            ),
            0,
        )
        return list(csv.DictReader(lines[header_index:]))

    @staticmethod
    def _max_elapsed_from_csv(path: Path) -> float:
        """Return the latest MangoHud process-relative elapsed timestamp."""
        elapsed_values = []
        for row in MangoHudSession._csv_rows(path):
            try:
                elapsed_values.append(float((row.get("elapsed") or "").strip()))
            except ValueError:
                continue
        return max(elapsed_values, default=0.0)

    @staticmethod
    def _mean_fps_from_csv(
        path: Path,
        maximum_fps: float | None = None,
        minimum_elapsed: float | None = None,
    ) -> float | None:
        """Return the mean presented FPS from a MangoHud raw or summary CSV."""
        fps_values: list[float] = []
        for row in MangoHudSession._csv_rows(path):
            if minimum_elapsed is not None:
                try:
                    if float((row.get("elapsed") or "").strip()) <= minimum_elapsed:
                        continue
                except ValueError:
                    # Summary CSVs have no elapsed column and remain a fallback.
                    pass
            for key, raw in row.items():
                normalized = (key or "").strip().lower().replace(" ", "")
                if normalized not in {"fps", "averagefps", "avgfps"}:
                    continue
                try:
                    value = float((raw or "").strip())
                except ValueError:
                    continue
                if value > 0 and (maximum_fps is None or value <= maximum_fps):
                    fps_values.append(value)
                break

        return sum(fps_values) / len(fps_values) if fps_values else None



class ImageListener(Node):
    def __init__(self, namespace="image_listener", probe_mode="startup"):
        super().__init__(f"image_listener_{random.randint(1000, 9999)}")
        self.image_received = False
        self.received_monotonic = None
        self.namespace = namespace
        self.probe_mode = probe_mode
        self.measurement_started = None
        self.measurement_active = False
        self.statistics_lock = threading.Lock()
        self.message_count = 0
        self.payload_bytes = 0
        self.previous_message_monotonic = None
        self.maximum_gap_seconds = 0.0
        self.subscription = self.create_subscription(
            Image,
            namespace,
            self.image_callback,
            qos_profile_sensor_data,
            raw=True,
        )
        print(f"Subscribed to {self.namespace}")

    def image_callback(self, serialized_msg):
        received = time.monotonic()
        with self.statistics_lock:
            if not self.image_received:
                self.received_monotonic = received
                self.image_received = True
                if self.probe_mode == "startup":
                    self.destroy_subscription(self.subscription)
            if self.measurement_active:
                if self.previous_message_monotonic is not None:
                    self.maximum_gap_seconds = max(
                        self.maximum_gap_seconds,
                        received - self.previous_message_monotonic,
                    )
                else:
                    self.maximum_gap_seconds = received - self.measurement_started
                self.previous_message_monotonic = received
                self.message_count += 1
                self.payload_bytes += len(serialized_msg)

    def start_measurement(self, started_monotonic):
        """Reset and enable the low-overhead raw transport probe."""
        if self.probe_mode != "continuous":
            return
        with self.statistics_lock:
            self.measurement_started = started_monotonic
            self.measurement_active = True
            self.message_count = 0
            self.payload_bytes = 0
            self.previous_message_monotonic = None
            self.maximum_gap_seconds = 0.0

    def finish_measurement(self):
        """Atomically stop counting messages at the measurement boundary."""
        with self.statistics_lock:
            self.measurement_active = False

    def transport_statistics(self, ended_monotonic):
        """Return delivery rate, serialized payload rate, gap and count."""
        with self.statistics_lock:
            if self.measurement_started is None:
                return None
            duration = max(ended_monotonic - self.measurement_started, 1e-9)
            final_gap = (
                duration
                if self.previous_message_monotonic is None
                else ended_monotonic - self.previous_message_monotonic
            )
            return {
                "rate_hz": self.message_count / duration,
                "payload_mib_s": self.payload_bytes / (1024 * 1024) / duration,
                "max_gap_seconds": max(self.maximum_gap_seconds, final_gap),
                "message_count": self.message_count,
            }


class RealTimeFactorSampler:
    """Accumulate near-fixed wall-time RTF windows and the full observation."""

    def __init__(self, window_seconds):
        if window_seconds <= 0:
            raise ValueError("RTF window must be greater than zero")
        self.window_seconds = window_seconds
        self.reset()

    def reset(self):
        self.rewind_count = 0
        self._reset_span()

    def _reset_span(self):
        self.window_samples = []
        self._first_sim_time = None
        self._first_wall_time = None
        self._last_sim_time = None
        self._last_wall_time = None
        self._window_sim_time = None
        self._window_wall_time = None

    def add_clock(self, sim_time, wall_time):
        """Add one received clock value and close a due sample window.

        Window boundaries are the first received clock messages at or after
        the configured wall-time period. A dedicated executor keeps the
        resulting overshoot bounded by normal ROS callback latency.
        """
        if self._last_sim_time is not None and sim_time < self._last_sim_time:
            # A simulator reset invalidates elapsed-time ratios. Start a clean
            # measurement span instead of reporting a misleading negative RTF.
            self.rewind_count += 1
            self._reset_span()

        if self._first_sim_time is None:
            self._first_sim_time = sim_time
            self._first_wall_time = wall_time
            self._window_sim_time = sim_time
            self._window_wall_time = wall_time
        elif wall_time - self._window_wall_time >= self.window_seconds:
            sim_delta = sim_time - self._window_sim_time
            wall_delta = wall_time - self._window_wall_time
            if sim_delta >= 0 and wall_delta > 0:
                self.window_samples.append(sim_delta / wall_delta)
            self._window_sim_time = sim_time
            self._window_wall_time = wall_time

        self._last_sim_time = sim_time
        self._last_wall_time = wall_time

    def window_mean(self):
        if not self.window_samples:
            return None
        return sum(self.window_samples) / len(self.window_samples)

    def global_ratio(self):
        if self._first_sim_time is None or self._last_sim_time is None:
            return None
        sim_delta = self._last_sim_time - self._first_sim_time
        wall_delta = self._last_wall_time - self._first_wall_time
        if sim_delta < 0 or wall_delta <= 0:
            return None
        return sim_delta / wall_delta

    def required_window_samples(self, iteration_seconds):
        """Return the minimum complete windows required for this iteration."""
        expected = int(iteration_seconds // self.window_seconds)
        return 0 if expected < 2 else max(1, int(expected * 0.75))


class ClockListener(Node):
    def __init__(self, window_seconds=1.0):
        super().__init__('clock_listener')
        self.rtf_sampler = RealTimeFactorSampler(window_seconds)
        self.rtf_lock = threading.Lock()
        self.first_received_monotonic = None
        self.previous_received_monotonic = None
        self.message_count = 0
        self.maximum_gap_seconds = 0.0
        self.subscription = self.create_subscription(
            Clock,
            '/clock',
            self.clock_callback,
            qos_profile=qos_profile_sensor_data
        )

    def reset_samples(self):
        """Start an RTF measurement window from the next clock message."""
        with self.rtf_lock:
            self.rtf_sampler.reset()
            self.previous_received_monotonic = None
            self.message_count = 0
            self.maximum_gap_seconds = 0.0

    def clock_callback(self, msg):
        """
        Process simulator clock updates and record real-time-factor samples.

        Args:
            msg: ROS 2 Clock message containing the current simulation time.
        """
        received_time = time.monotonic()
        sim_time = msg.clock.sec + msg.clock.nanosec * 1e-9
        with self.rtf_lock:
            if self.first_received_monotonic is None:
                self.first_received_monotonic = received_time
            if self.previous_received_monotonic is not None:
                self.maximum_gap_seconds = max(
                    self.maximum_gap_seconds,
                    received_time - self.previous_received_monotonic,
                )
            self.previous_received_monotonic = received_time
            self.message_count += 1
            self.rtf_sampler.add_clock(sim_time, received_time)

    def get_real_time_factor_mean(self):
        """Return the mean of fixed wall-time RTF windows."""
        with self.rtf_lock:
            return self.rtf_sampler.window_mean()

    def get_real_time_factor_global(self):
        """Return simulation-time / wall-time across the full observation."""
        with self.rtf_lock:
            return self.rtf_sampler.global_ratio()

    def get_real_time_factor_sample_count(self):
        with self.rtf_lock:
            return len(self.rtf_sampler.window_samples)

    def get_integrity_statistics(self, ended_monotonic):
        """Return received-clock evidence for accepting an RTF result."""
        with self.rtf_lock:
            final_gap = (
                None
                if self.previous_received_monotonic is None
                else max(0.0, ended_monotonic - self.previous_received_monotonic)
            )
            return {
                "message_count": self.message_count,
                "rewind_count": self.rtf_sampler.rewind_count,
                "max_gap_seconds": max(
                    self.maximum_gap_seconds,
                    final_gap or 0.0,
                ),
            }

    def validate_measurement(self, iteration_seconds):
        """Reject incomplete or reset clock observations."""
        with self.rtf_lock:
            if self.message_count < 2:
                raise RuntimeError(
                    "RTF invalid: fewer than two /clock messages during measurement"
                )
            if self.rtf_sampler.rewind_count:
                raise RuntimeError("RTF invalid: /clock moved backwards during measurement")

            rtf_global = self.rtf_sampler.global_ratio()
            if rtf_global is None:
                raise RuntimeError(
                    "RTF invalid: /clock did not provide a positive wall-time span"
                )

            sample_count = len(self.rtf_sampler.window_samples)
            required_windows = self.rtf_sampler.required_window_samples(iteration_seconds)
            if sample_count < required_windows:
                raise RuntimeError(
                    "RTF invalid: only "
                    f"{sample_count} complete windows, expected at least {required_windows}"
                )
            if required_windows and self.rtf_sampler.window_mean() is None:
                raise RuntimeError("RTF invalid: complete /clock windows have no mean")


class ResourceSampler:
    """Sample host and iteration-owned CPU, RAM, and GPU resources."""

    @staticmethod
    def _get_gpu_usage(owned_pids):
        """Return global GPU metrics and VRAM attributed to iteration-owned PIDs.

        The tuple contains GPU utilization (%), memory-controller utilization (%),
        temperature (C), power (W), graphics clock (MHz), and owned VRAM (MiB).
        Device-wide metrics cannot be attributed per process. NVIDIA VRAM can be
        matched exactly by PID; AMD's command-line interface only exposes global
        VRAM here, so that final value is deliberately reported as unavailable.
        """
        owned_pids = set(owned_pids)

        def _try_float(value):
            try:
                return float(str(value).strip().split()[0])
            except (ValueError, AttributeError):
                return None

        def _extract_json(text):
            if not text:
                return None
            start = text.find('{')
            end = text.rfind('}')
            if start == -1 or end == -1 or end <= start:
                return None
            try:
                return json.loads(text[start:end + 1])
            except json.JSONDecodeError:
                return None

        def query_nvidia():
            try:
                import pynvml
            except ImportError:
                return None

            initialized = False
            try:
                pynvml.nvmlInit()
                initialized = True
                handle = pynvml.nvmlDeviceGetHandleByIndex(0)

                def safe_call(function):
                    try:
                        return function()
                    except (pynvml.NVMLError, AttributeError, TypeError, ValueError):
                        return None

                utilization = safe_call(lambda: pynvml.nvmlDeviceGetUtilizationRates(handle))
                temperature = safe_call(
                    lambda: pynvml.nvmlDeviceGetTemperature(handle, pynvml.NVML_TEMPERATURE_GPU)
                )
                power_mw = safe_call(lambda: pynvml.nvmlDeviceGetPowerUsage(handle))
                graphics_clock = safe_call(
                    lambda: pynvml.nvmlDeviceGetClockInfo(handle, pynvml.NVML_CLOCK_GRAPHICS)
                )

                process_by_pid = {}
                for process_type in ("compute", "graphics"):
                    base_name = f"nvmlDeviceGet{process_type.capitalize()}RunningProcesses"
                    process_api = None
                    for version in ("_v3", "_v2", "_v1", ""):
                        process_api = getattr(pynvml, base_name + version, None)
                        if process_api is not None:
                            break
                    if process_api is None:
                        continue

                    try:
                        processes = process_api(handle) or []
                    except pynvml.NVMLError:
                        continue

                    for process in processes:
                        pid = int(process.pid)
                        if pid not in owned_pids:
                            continue

                        memory_bytes = getattr(process, "usedGpuMemory", None)
                        if memory_bytes is not None and memory_bytes > 2**63:
                            memory_bytes = None
                        memory_mib = None if memory_bytes is None else memory_bytes / (1024 * 1024)

                        # A process can be reported by both the compute and graphics APIs.
                        # Keep one entry per PID and prefer the largest valid value.
                        previous = process_by_pid.get(pid)
                        if previous is None or (
                            memory_mib is not None
                            and (previous is None or previous < memory_mib)
                        ):
                            process_by_pid[pid] = memory_mib

                simulator_memory_mib = sum(
                    memory for memory in process_by_pid.values() if memory is not None
                )
                return (
                    None if utilization is None else utilization.gpu,
                    None if utilization is None else utilization.memory,
                    temperature,
                    None if power_mw is None else power_mw / 1000.0,
                    graphics_clock,
                    simulator_memory_mib if process_by_pid else None,
                )
            except (pynvml.NVMLError, AttributeError, TypeError, ValueError, OSError):
                return None
            finally:
                if initialized:
                    try:
                        pynvml.nvmlShutdown()
                    except pynvml.NVMLError:
                        pass


        def query_amd():
            try:
                util_proc = subprocess.run(
                    ['rocm-smi', '--showuse', '--json'],
                    capture_output=True,
                    text=True,
                    check=True,
                    timeout=5,
                )
            except (OSError, subprocess.SubprocessError):
                return None

            util_json = _extract_json(util_proc.stdout) or _extract_json(util_proc.stderr)
            if not util_json:
                return None

            card_items = [(k, v) for k, v in util_json.items() if k.startswith('card')]
            if not card_items:
                return None

            total_util = 0.0
            for _card_key, card_data in card_items:
                util_val = (
                    _try_float(card_data.get('GPU use (%)')) or
                    _try_float(card_data.get('GPU (%)')) or
                    _try_float(card_data.get('GPU Utilization (%)'))
                )
                if util_val is not None:
                    total_util += util_val

            # rocm-smi values are device-wide and cannot safely be assigned to this
            # iteration when another workload shares the GPU.
            return total_util, None, None, None, None, None

        nvidia = query_nvidia()
        if nvidia:
            return nvidia
        else:
            amd = query_amd()
            if amd:
                return amd
        return None, None, None, None, None, None

    def __init__(self, process_supervisor, interval: float = 0.5):
        self.process_supervisor = process_supervisor
        self.interval = interval
        self.cpu_samples: list[float] = []
        self.cpu_core_peak_samples: list[float] = []
        self.cpu_core_saturated_count_samples: list[float] = []
        self.ram_samples: list[float] = []
        self.gpu_util_samples: list[float] = []
        self.gpu_memory_util_samples: list[float] = []
        self.gpu_temperature_samples: list[float] = []
        self.gpu_power_samples: list[float] = []
        self.gpu_clock_samples: list[float] = []
        self.gpu_mem_samples: list[float] = []
        self.errors: list[str] = []
        self._stop = threading.Event()
        self._thread: threading.Thread | None = None


    def start(self):
        self._thread = threading.Thread(target=self._run, name="benchmark-resource-monitor")
        self._thread.start()

    def _run(self):
        while not self._stop.is_set():
            processes = self.process_supervisor.session_members()
            psutil.cpu_percent(interval=None, percpu=True)
            for process in processes:
                try:
                    process.cpu_percent(interval=None)
                except (psutil.Error, OSError):
                    pass
            if self._stop.wait(self.interval):
                break
            cpu = 0.0
            ram_bytes = 0
            live_pids = set()
            for process in processes:
                try:
                    if not process.is_running():
                        continue
                    live_pids.add(process.pid)
                    cpu += process.cpu_percent(interval=None)
                    ram_bytes += process.memory_info().rss
                except (psutil.Error, OSError):
                    continue
            cores = psutil.cpu_percent(interval=None, percpu=True)
            self.cpu_samples.append(cpu / (psutil.cpu_count() or 1))
            if cores:
                self.cpu_core_peak_samples.append(max(cores))
                self.cpu_core_saturated_count_samples.append(sum(value >= 90.0 for value in cores))
            self.ram_samples.append(ram_bytes / (1024 * 1024))
            try:
                values = self._get_gpu_usage(live_pids)
                for samples, value in zip((self.gpu_util_samples, self.gpu_memory_util_samples,
                    self.gpu_temperature_samples, self.gpu_power_samples,
                    self.gpu_clock_samples, self.gpu_mem_samples), values):
                    if value is not None:
                        samples.append(value)
            except Exception as exc:
                self.errors.append(str(exc))

    def stop(self):
        self._stop.set()
        if self._thread is not None:
            self._thread.join(timeout=7)

    @staticmethod
    def _mean(values):
        return sum(values) / len(values) if values else None

    def results(self) -> dict[str, Any]:
        return {
            "cpu_mean_percent": self._mean(self.cpu_samples) or 0,
            "cpu_core_peak_mean_percent": self._mean(self.cpu_core_peak_samples),
            "cpu_core_saturated_mean_count": self._mean(self.cpu_core_saturated_count_samples),
            "ram_mean_mb": self._mean(self.ram_samples) or 0,
            "gpu_mean_percent": self._mean(self.gpu_util_samples),
            "gpu_memory_util_mean_percent": self._mean(self.gpu_memory_util_samples),
            "gpu_temperature_mean_c": self._mean(self.gpu_temperature_samples),
            "gpu_power_mean_w": self._mean(self.gpu_power_samples),
            "gpu_clock_mean_mhz": self._mean(self.gpu_clock_samples),
            "gpu_mem_mean_mb": self._mean(self.gpu_mem_samples),
            "errors": list(self.errors),
        }


class BenchmarkMonitor:
    """Facade coordinating all monitors and the readiness boundary."""

    @dataclass(frozen=True)
    class ReadinessResult:
        ready: bool
        first_frame_seconds: float | None
        startup_seconds: float | None

    def __init__(self, context, process_supervisor, monitor_ros=False):
        self.context = context
        self.process_supervisor = process_supervisor
        self.monitor_ros = monitor_ros
        self.image_listeners = []
        self.ros_monitor = None
        self.clock_monitor = None
        self.resource_monitor = ResourceSampler(process_supervisor)
        self.render_monitor = None
        self.image_executor = None
        self.image_thread = None
        self.clock_executor = None
        self.clock_thread = None
        self.startup_started = None
        self.ready_result = None
        self.measurement_ended = None
        self.ros_statistics = []
        self._rclpy_initialized = False

    def prepare(self, image_topics, nonimage_topics=(), render_monitor=None):
        rclpy.init()
        self._rclpy_initialized = True
        self.image_listeners = [ImageListener(topic_name, "startup") for topic_name in image_topics]
        if self.monitor_ros:
            self.ros_monitor = RosMonitor(excluded_topics=["/clock"])
            for topic_name, type_name in nonimage_topics:
                self.ros_monitor.subscribe(topic_name, type_name)
        self.clock_monitor = ClockListener(
            float(self.context.get("rtf_window_seconds", 1.0))
        )
        self.render_monitor = render_monitor
        self.image_executor = SingleThreadedExecutor()
        for listener in self.image_listeners:
            self.image_executor.add_node(listener)
        if self.ros_monitor is not None:
            self.image_executor.add_node(self.ros_monitor)
        self.clock_executor = SingleThreadedExecutor()
        self.clock_executor.add_node(self.clock_monitor)
        self.image_thread = threading.Thread(target=self.image_executor.spin, name="image-monitor")
        self.clock_thread = threading.Thread(target=self.clock_executor.spin, name="clock-monitor")
        self.image_thread.start()
        self.clock_thread.start()

    def mark_launch_started(self, started_monotonic):
        self.startup_started = started_monotonic

    def wait_until_ready(
        self,
        timeout: float,
        poll_interval: float = 0.05,
        progress_callback=None,
        progress_interval: float = 1.0,
    ):
        if self.startup_started is None:
            raise RuntimeError("Launch start time is required before readiness")
        deadline = self.startup_started + timeout
        first_frame_seconds = None
        next_progress = self.startup_started
        while rclpy.ok():
            now = time.monotonic()
            received = [listener.received_monotonic for listener in self.image_listeners
                        if listener.image_received and listener.received_monotonic is not None]
            if received and first_frame_seconds is None:
                first_frame_seconds = min(received) - self.startup_started
            if self.image_listeners and len(received) == len(self.image_listeners):
                startup_seconds = max(received) - self.startup_started
                self.ready_result = self.ReadinessResult(
                    True, first_frame_seconds, startup_seconds
                )
                if progress_callback is not None:
                    progress_callback(
                        startup_seconds,
                        timeout,
                        len(received),
                        len(self.image_listeners),
                    )
                return self.ready_result
            if now >= deadline:
                raise TimeoutError(f"Simulator did not satisfy readiness within {timeout:g} seconds")
            if progress_callback is not None and now >= next_progress:
                progress_callback(
                    now - self.startup_started,
                    timeout,
                    len(received),
                    len(self.image_listeners),
                )
                next_progress = now + max(progress_interval, poll_interval)
            time.sleep(poll_interval)
        raise RuntimeError("ROS context stopped before readiness completed")

    def start_measurement(self, started_monotonic):
        if self.ros_monitor is not None:
            self.ros_monitor.discover()
            self.ros_monitor.start_measurement()
        self.clock_monitor.reset_samples()
        self.resource_monitor.start()
        if self.render_monitor is not None:
            self.render_monitor.start_measurement()

    def stop_measurement(self, duration: float):
        ended = time.monotonic()
        self.measurement_ended = ended
        self.resource_monitor.stop()
        if self.ros_monitor is not None:
            self.ros_statistics = self.ros_monitor.statistics(ended, duration)
        render_fps = self.render_monitor.finish_measurement() if self.render_monitor is not None else None
        clock_stats = self.clock_monitor.get_integrity_statistics(ended)
        self._results = {
            **self.resource_monitor.results(),
            "ros_topic_statistics": self.ros_statistics,
            "render_fps_mean": render_fps,
            "real_time_factor_mean": self.clock_monitor.get_real_time_factor_mean(),
            "real_time_factor_global": self.clock_monitor.get_real_time_factor_global(),
            "real_time_factor_sample_count": self.clock_monitor.get_real_time_factor_sample_count(),
            "rtf_clock_statistics": clock_stats,
        }
        return self._results

    def validate_rtf(self, iteration_seconds):
        """Validate the completed simulation-clock measurement."""
        self.clock_monitor.validate_measurement(iteration_seconds)

    def results(self):
        return getattr(self, "_results", {})

    def close(self):
        if self.image_executor is not None:
            self.image_executor.shutdown(timeout_sec=2)
        if self.clock_executor is not None:
            self.clock_executor.shutdown(timeout_sec=2)
        for thread in (self.image_thread, self.clock_thread):
            if thread is not None:
                thread.join(timeout=3)
        for node in (*self.image_listeners, self.ros_monitor, self.clock_monitor):
            if node is not None:
                try:
                    node.destroy_node()
                except Exception:
                    pass
        if self._rclpy_initialized and rclpy.ok():
            rclpy.shutdown()
