#!/usr/bin/env python3

import argparse
import csv
import glob
import os
import re
import subprocess
import subprocess as sp
import sys
import time
from datetime import datetime

import psutil

# ---------------- GPU helpers ----------------
def get_gpu_usage():
    """Return total GPU utilization (%) and memory (MiB) if NVIDIA GPU is present, else (None, None)."""
    try:
        result = sp.run(
            ['nvidia-smi', '--query-gpu=utilization.gpu,memory.used', '--format=csv,noheader,nounits'],
            capture_output=True, text=True, check=True
        )
        lines = result.stdout.strip().split('\n')
        total_util, total_mem = 0.0, 0.0
        for line in lines:
            util, mem = line.split(',')
            total_util += float(util.strip())
            total_mem += float(mem.strip())
        return total_util, total_mem
    except Exception:
        return None, None

# ---------------- Launch configs ----------------
LAUNCH_CONFIGS = {
    "gazebo_harmonic": {
        "LAUNCH_SIMULATOR_CMD": ["ros2", "launch", "robotnik_gazebo_ignition", "spawn_world.launch.py"],
        "LAUNCH_ROBOT_CMD": ["ros2", "launch", "robotnik_gazebo_ignition", "spawn_robot.launch.py",
                             "robot:=rbwatcher", "robot_model:=rbwatcher"],
        "NODES_TO_KILL": ["parameter_bridge", "rviz2", "gz", "robot_state_publisher"],
    },
    "isaac_sim": {
        "LAUNCH_SIMULATOR_CMD": ["ros2", "launch", "isaac_sim", "isaac_sim_complete.launch.py"],
        "LAUNCH_ROBOT_CMD": ["ros2", "launch", "robotnik_gazebo_ignition", "spawn_robot.launch.py",
                             "robot:=rbwatcher", "robot_model:=rbwatcher"],
        "NODES_TO_KILL": ["rviz2", "isaac"],
    },
    "webots": {
        "LAUNCH_SIMULATOR_CMD": ["ros2", "launch", "robotnik_webots", "spawn_world.launch.py"],
        "LAUNCH_ROBOT_CMD": ["ros2", "launch", "robotnik_webots", "spawn_robot.launch.py",
                             "robot:=rbwatcher", "robot_id:=robot", "x:=2.0", "y:=2.0", "z:=0.0"],
        "NODES_TO_KILL": ["rviz2", "robot_state_publisher", "webots", "Ros2Supervisor", "static_transform_publisher"],
    },
    "unity": {
        "LAUNCH_SIMULATOR_CMD": ["ros2", "launch", "unity_sim", "unity_complete.launch.py"],
        "LAUNCH_ROBOT_CMD": ["ros2", "launch", "robotnik_unity", "spawn_robot.launch.py",
                             "robot:=rbwatcher", "robot_id:=robot", "x:=2.0", "y:=2.0", "z:=0.0"],
        "NODES_TO_KILL": ["rviz2", "ros_tcp_endpoint", "PI_simulation_Unity_Robotnik.x86_64"],
    },
}

CATEGORY = [
    "",
    "one_robot_emtpy_world",
    "two_robot_emtpy_world",
    "three_robot_emtpy_world",
    "one_robot_simple_world",
    "two_robot_simple_world",
    "three_robot_simple_world",
    "one_robot_emtpy_world_rviz",
    "two_robot_emtpy_world_rviz",
    "three_robot_emtpy_world_rviz",
    "one_robot_simple_world_rviz",
    "two_robot_simple_world_rviz",
    "three_robot_simple_world_rviz",
]

# ---------------- Args ----------------
parser = argparse.ArgumentParser(description="Benchmark simulator script using robotnik_sim_benchmark_utils/benchmark_node")
parser.add_argument("simulator", help="Simulator name (gazebo_harmonic, isaac_sim, webots, unity)")
parser.add_argument("--image_topic", default="/robot/front_rgbd_camera/color/image_raw", help="Image topic to wait for")
parser.add_argument("--topics", nargs="*", default=["/tf", "/robot/front_rgbd_camera/color/image_raw"],
                    help="Topics to pass to benchmark_node")
parser.add_argument("--bench_csv_dir", default="/tmp/topic_stats", help="Directory where benchmark_node will write CSVs")
parser.add_argument("--best_effort", type=lambda x: str(x).lower() in ["1","true","yes","y"], default=True,
                    help="Set benchmark_node best_effort param")
parser.add_argument("--window_seconds", type=float, default=2.0, help="benchmark_node window_seconds param")
parser.add_argument("--csv_file", default="", help="Output summary CSV path (defaults under benchmarks/...)")
parser.add_argument("--iterations", default=1, help="Number of iterations")
parser.add_argument("--category", default=0, help="Category index from predefined CATEGORY list")
parser.add_argument("--ros_args", nargs="*", default=[], help="Extra ROS 2 args to pass to the simulator/robot launch")
if "--help" in sys.argv or "-h" in sys.argv or len(sys.argv) < 2:
    parser.print_help()
    sys.exit(0)
args = parser.parse_args()

SELECTED_SIMULATOR = args.simulator
if SELECTED_SIMULATOR not in LAUNCH_CONFIGS:
    print(f"Simulator '{SELECTED_SIMULATOR}' not found in LAUNCH_CONFIGS.")
    sys.exit(1)
LAUNCH_SIMULATOR_CMD = LAUNCH_CONFIGS[SELECTED_SIMULATOR]["LAUNCH_SIMULATOR_CMD"] + args.ros_args
LAUNCH_ROBOT_CMD = LAUNCH_CONFIGS[SELECTED_SIMULATOR]["LAUNCH_ROBOT_CMD"] + args.ros_args
NODES_TO_KILL = LAUNCH_CONFIGS[SELECTED_SIMULATOR]["NODES_TO_KILL"] + ["benchmark_node", "robotnik_sim_benchmark_utils"]

IMAGE_TOPIC = args.image_topic
TOPICS = args.topics
BENCH_CSV_DIR = args.bench_csv_dir
BEST_EFFORT = args.best_effort
WINDOW_SECONDS = args.window_seconds

SELECTED_CATEGORY = CATEGORY[int(args.category)]
if args.csv_file == "":
    timestamp = int(time.time())
    os.makedirs(f"benchmarks/{SELECTED_SIMULATOR}/{SELECTED_CATEGORY}", exist_ok=True)
    CSV_PATH = f"benchmarks/{SELECTED_SIMULATOR}/{SELECTED_CATEGORY}/ros2_launch_timings_{timestamp}.csv"
else:
    CSV_PATH = args.csv_file

ITERATIONS = int(args.iterations)

# ---------------- Helpers ----------------
def kill_processes_by_name(names):
    parent_pid = os.getpid()
    for proc in psutil.process_iter(['pid', 'cmdline']):
        if proc.pid == parent_pid:
            continue
        cmdline = proc.info.get('cmdline', [])
        if not isinstance(cmdline, list):
            continue
        cmdline_str = ' '.join(cmdline)
        if any(name in cmdline_str for name in names):
            try:
                proc.kill()
            except Exception:
                pass

def write_csv_row(filename, row):
    file_exists = os.path.isfile(filename)
    with open(filename, 'a', newline='') as f:
        w = csv.writer(f)
        if not file_exists:
            w.writerow([
                'simulator', 'timestamp', 'iteration', 'elapsed_seconds',
                'cpu_mean_percent', 'ram_mean_mb', 'gpu_mean_percent', 'gpu_mem_mean_mb',
                'real_time_factor_mean', 'iteration_total_time'
            ])
        w.writerow(row)

def sanitise_topic_for_match(topic: str) -> str:
    return re.sub(r'[^a-zA-Z0-9_]', '_', topic)

def find_new_csv_files(base_dir: str, since_ts: float):
    files = []
    for path in glob.glob(os.path.join(base_dir, "**", "*.csv"), recursive=True):
        try:
            if os.path.getmtime(path) >= since_ts - 0.5:
                files.append(path)
        except FileNotFoundError:
            pass
    return files

def csv_has_data(path: str) -> bool:
    try:
        with open(path, 'r', newline='') as f:
            return sum(1 for _ in f) > 1
    except Exception:
        return False

def extract_rtf_mean_from_dir(base_dir: str) -> float | None:
    rtf_vals = []
    for path in glob.glob(os.path.join(base_dir, "**", "*.csv"), recursive=True):
        try:
            with open(path, 'r', newline='') as f:
                reader = csv.DictReader(f)
                # Find likely RTF column
                rtf_col = None
                for name in reader.fieldnames or []:
                    if name is None:
                        continue
                    low = name.strip().lower()
                    if low in ("rtf", "real_time_factor", "real-time factor", "realtime_factor"):
                        rtf_col = name
                        break
                if rtf_col is None:
                    # fallback: any column containing rtf
                    for name in reader.fieldnames or []:
                        if name and "rtf" in name.lower():
                            rtf_col = name
                            break
                if rtf_col is None:
                    continue
                for row in reader:
                    v = row.get(rtf_col, "").strip()
                    if v:
                        try:
                            rtf_vals.append(float(v))
                        except ValueError:
                            pass
        except Exception:
            continue
    if not rtf_vals:
        return None
    return sum(rtf_vals) / len(rtf_vals)

def start_benchmark_node():
    os.makedirs(BENCH_CSV_DIR, exist_ok=True)
    topics_param = f"topics:=[{','.join(TOPICS)}]"
    csv_dir_param = f"csv_dir:={BENCH_CSV_DIR}"
    best_effort_param = f"best_effort:={'true' if BEST_EFFORT else 'false'}"
    win_param = f"window_seconds:={WINDOW_SECONDS}"
    cmd = [
        "ros2", "run", "robotnik_sim_benchmark_utils", "benchmark_node",
        "--ros-args",
        "-p", topics_param,
        "-p", csv_dir_param,
        "-p", best_effort_param,
        "-p", win_param,
    ]
    return subprocess.Popen(cmd)

def wait_for_first_image_csv(bench_start_ts: float, timeout_s: float = 300.0):
    """Wait until a CSV with data appears for the image topic. Return elapsed seconds since bench start."""
    deadline = time.time() + timeout_s
    image_hint = sanitise_topic_for_match(IMAGE_TOPIC)
    image_received = False
    while time.time() < deadline and not image_received:
        files = find_new_csv_files(BENCH_CSV_DIR, bench_start_ts)
        # Prefer files that look like the image topic
        preferred = [p for p in files if image_hint in os.path.basename(p) or "image" in os.path.basename(p).lower()]
        candidates = preferred if preferred else files
        for path in candidates:
            if csv_has_data(path):
                image_received = True
                break
        if not image_received:
            time.sleep(0.2)
    if not image_received:
        return None
    return time.time() - bench_start_ts

# ---------------- Core iteration ----------------
def run_iteration(iter_num: int):
    start_time = time.time()
    print(f"[{iter_num}] Launching simulator and robot...")
    launch_simulator_process = subprocess.Popen(LAUNCH_SIMULATOR_CMD)
    launch_robot_process = subprocess.Popen(LAUNCH_ROBOT_CMD)

    # Start benchmark node
    bench_start_ts = time.time()
    bench_proc = start_benchmark_node()
    print(f"[{iter_num}] benchmark_node started. Writing CSVs at: {BENCH_CSV_DIR}")

    # Monitor resources
    cpu_samples, ram_samples, gpu_util_samples, gpu_mem_samples = [], [], [], []

    def sample_resources():
        procs = [psutil.Process(launch_simulator_process.pid),
                 psutil.Process(launch_robot_process.pid),
                 psutil.Process(bench_proc.pid)]
        all_procs = []
        for p in procs:
            try:
                all_procs.append(p)
                all_procs.extend(p.children(recursive=True))
            except Exception:
                pass

        # Initialize cpu_percent
        for proc in all_procs:
            try:
                proc.cpu_percent(interval=None)
            except Exception:
                pass

        # Collect a sample
        time.sleep(0.5)
        try:
            cpu = sum([proc.cpu_percent(interval=0.5) for proc in all_procs]) / max(1, psutil.cpu_count())
            ram = sum([proc.memory_info().rss for proc in all_procs]) / (1024 * 1024)
            gpu_util, gpu_mem = get_gpu_usage()
            cpu_samples.append(cpu)
            ram_samples.append(ram)
            if gpu_util is not None:
                gpu_util_samples.append(gpu_util)
            if gpu_mem is not None:
                gpu_mem_samples.append(gpu_mem)
        except Exception:
            pass

    # Wait for first image sample via CSV
    print(f"[{iter_num}] Waiting for first image sample on {IMAGE_TOPIC}...")
    elapsed = wait_for_first_image_csv(bench_start_ts, timeout_s=300.0)
    if elapsed is None:
        print(f"[{iter_num}] Timeout waiting for image samples.")
        elapsed = 0.0
        extra_wait = 30
    else:
        print(f"[{iter_num}] Image received after {elapsed:.3f} s. Stabilizing for 60 s...")
        extra_wait = 60

    # Stabilization window with resource sampling
    t_end = time.time() + extra_wait
    while time.time() < t_end:
        sample_resources()

    # Compute RTF mean from benchmark CSVs
    rtf_mean = extract_rtf_mean_from_dir(BENCH_CSV_DIR)

    # Teardown
    print(f"[{iter_num}] Shutting down processes...")
    try:
        bench_proc.send_signal(subprocess.signal.SIGINT)
        bench_proc.terminate()
        bench_proc.wait(timeout=10)
    except Exception:
        pass

    try:
        launch_simulator_process.send_signal(subprocess.signal.SIGINT)
        launch_simulator_process.terminate()
        launch_simulator_process.wait(timeout=20)
    except Exception:
        pass

    try:
        launch_robot_process.send_signal(subprocess.signal.SIGINT)
        launch_robot_process.terminate()
        launch_robot_process.wait(timeout=20)
    except Exception:
        pass

    kill_processes_by_name(NODES_TO_KILL)

    # Averages
    cpu_mean = sum(cpu_samples) / len(cpu_samples) if cpu_samples else 0.0
    ram_mean = sum(ram_samples) / len(ram_samples) if ram_samples else 0.0
    gpu_util_mean = sum(gpu_util_samples) / len(gpu_util_samples) if gpu_util_samples else None
    gpu_mem_mean = sum(gpu_mem_samples) / len(gpu_mem_samples) if gpu_mem_samples else None
    iteration_total_time = time.time() - start_time

    return elapsed, cpu_mean, ram_mean, gpu_util_mean, gpu_mem_mean, rtf_mean, iteration_total_time

# ---------------- Main ----------------
def main():
    kill_processes_by_name(NODES_TO_KILL)
    for i in range(1, ITERATIONS + 1):
        elapsed, cpu_mean, ram_mean, gpu_util_mean, gpu_mem_mean, rtf_mean, iteration_total_time = run_iteration(i)
        timestamp = datetime.now().isoformat()
        write_csv_row(CSV_PATH, [
            SELECTED_SIMULATOR, timestamp, i, elapsed,
            cpu_mean, ram_mean, gpu_util_mean, gpu_mem_mean, rtf_mean, iteration_total_time
        ])
        time.sleep(5)
        print(f"[{i}] Iteration {i} recorded.")

if __name__ == "__main__":
    main()
