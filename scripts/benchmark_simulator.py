import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
import subprocess
import time
import csv
import os
from datetime import datetime
import psutil
import sys
from rclpy.qos import QoSProfile
from rclpy.qos import qos_profile_sensor_data

import threading
import subprocess as sp
from rosgraph_msgs.msg import Clock
import argparse
import json
import random
import yaml

def get_gpu_usage(simulator):
    """Return total GPU utilization (%) and memory (MiB) if GPU is present, else (None, None)."""
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

    def query_nvidia(nombre_simulador):
        SIMULADORES_GPU = {
            "gazebo_harmonic": ("gazebo", "ign", "gz", "world",),
            "webots": ("webots",),
            "o3de": ("Editor", "GameLauncher", "robotnik_roscon", "AssetProcessor",),
            "isaac_sim": ("kit", "omni", "isaac", "exe", "python3",),
            "unity": ("Unity","PI_simulation_U",)
        }

        if nombre_simulador not in SIMULADORES_GPU:
            return None

        keywords = SIMULADORES_GPU[nombre_simulador]


        try:
            res_gpu = sp.run(
                ['nvidia-smi', '--query-gpu=utilization.gpu', '--format=csv,noheader,nounits'],
                capture_output=True, text=True, check=True
            )
            gpu_util_global = float(res_gpu.stdout.strip())

            res_apps = sp.run(
              'nvidia-smi pmon -c 1 -s m | grep -vE "^#|idx" | awk \'{print $6 "," $4 }\'',
              shell=True, capture_output=True, text=True, check=True
              )
        except Exception:
            return None

        memoria_simulador = 0.0
        encontrado = False

        for line in res_apps.stdout.strip().splitlines():
            if ',' not in line: continue
            nombre_proc, mem = line.split(',')
            nombre_proc = nombre_proc.lower().strip()
            
            if any(key.lower() in nombre_proc for key in keywords):
                memoria_simulador += float(mem.strip())
                encontrado = True

        if not encontrado:
            print("no encontrado proceso")
            return 0.0, 0.0

        return gpu_util_global, memoria_simulador


    def query_amd():
        try:
            util_proc = sp.run(
                ['rocm-smi', '--showuse', '--json'],
                capture_output=True,
                text=True,
                check=True
            )
            mem_proc = sp.run(
                ['rocm-smi', '--showmeminfo', 'vram', '--json'],
                capture_output=True,
                text=True,
                check=True
            )
        except Exception:
            return None

        util_json = _extract_json(util_proc.stdout) or _extract_json(util_proc.stderr)
        mem_json = _extract_json(mem_proc.stdout) or _extract_json(mem_proc.stderr)
        if not util_json:
            return None

        card_items = [(k, v) for k, v in util_json.items() if k.startswith('card')]
        if not card_items:
            return None

        total_util = 0.0
        total_mem_mib = 0.0

        for card_key, card_data in card_items:
            util_val = (
                _try_float(card_data.get('GPU use (%)')) or
                _try_float(card_data.get('GPU (%)')) or
                _try_float(card_data.get('GPU Utilization (%)'))
            )
            if util_val is not None:
                total_util += util_val

            mem_used_mib = None
            card_mem = mem_json.get(card_key, {}) if mem_json else {}

            for key in (
                'VRAM Used Memory (B)', 'GPU Memory Used (B)', 'VRAM Usage (B)',
                'VRAM Used Memory (MB)', 'GPU Memory Used (MB)', 'VRAM Usage (MB)'
            ):
                if key in card_mem:
                    val = _try_float(card_mem[key])
                    if val is None:
                        continue
                    if key.endswith('(B)'):
                        mem_used_mib = val / (1024 * 1024)
                    else:
                        mem_used_mib = val
                    break

            if mem_used_mib is None:
                percent = _try_float(card_data.get('VRAM use (%)'))
                total_bytes = None
                for key in (
                    'VRAM Total Memory (B)', 'Total VRAM Memory (B)',
                    'GPU Memory Total (B)'
                ):
                    if key in card_mem:
                        val = _try_float(card_mem[key])
                        if val is not None:
                            total_bytes = val
                            break
                if percent is not None and total_bytes is not None:
                    mem_used_mib = (percent / 100.0) * (total_bytes / (1024 * 1024))

            if mem_used_mib is not None:
                total_mem_mib += mem_used_mib

        if total_util == 0.0 and total_mem_mib == 0.0:
            return None
        return total_util, total_mem_mib if total_mem_mib > 0 else None

    nvidia = query_nvidia(simulator)
    if nvidia:
        return nvidia
    else:
        amd = query_amd()
        if amd:
            return amd
    return None, None


def load_launch_configs(yaml_path):
    with open(yaml_path, "r") as f:
        return yaml.safe_load(f)

# Default path for the YAML config file
DEFAULT_LAUNCH_CONFIGS_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "../config", "benchmark_config.yaml"
)

# Load LAUNCH_CONFIGS from YAML file
LAUNCH_CONFIGS = load_launch_configs(
    os.environ.get("LAUNCH_CONFIGS_PATH", DEFAULT_LAUNCH_CONFIGS_PATH)
)

CATEGORY = [
    "",
    "one_robot_empty_world",
    "two_robot_empty_world",
    "three_robot_empty_world",
    "one_robot_simple_world",
    "two_robot_simple_world",
    "three_robot_simple_world",
    "one_robot_empty_world_headless",
    "two_robot_empty_world_headless",
    "three_robot_empty_world_headless",
    "one_robot_simple_world_headless",
    "two_robot_simple_world_headless",
    "three_robot_simple_world_headless",
]

parser = argparse.ArgumentParser(description="Benchmark simulator script")
parser.add_argument("simulator", help="Simulator name (gazebo_harmonic, isaac_sim, webots)")
parser.add_argument("--image_topic", default="", help="Image topic to subscribe to")
parser.add_argument("--csv_file", default="", help="CSV file to store results")
parser.add_argument("--iterations", default=1, help="Number of interations")
parser.add_argument("--category", default=0, help="Category name for an specific set of benchmarks")
parser.add_argument("--ros_args", nargs="*", default=[], help="Additional ROS 2 args to pass to the launch files")
parser.add_argument("--iteration_time", default=60, help="Time for each iteration in seconds (time to wait after receiving the first image)")
if "--help" in sys.argv or "-h" in sys.argv or len(sys.argv) < 2:
    parser.print_help()
    sys.exit(0)
args = parser.parse_args()

try:
    SELECTED_CATEGORY = CATEGORY[int(args.category)]
except (IndexError, ValueError):
    print(f"Error: category index {args.category} is invalid. Please select a valid category index.")
    print("Available categories:")
    for idx, cat in enumerate(CATEGORY):
        print(f"{idx}: {cat}")
    sys.exit(1)

SELECTED_SIMULATOR = args.simulator
if SELECTED_SIMULATOR not in LAUNCH_CONFIGS:
    print(f"Simulator '{SELECTED_SIMULATOR}' not found in LAUNCH_CONFIGS.")
    sys.exit(1)
try:
    LAUNCH_SIMULATOR_CMD = LAUNCH_CONFIGS[SELECTED_SIMULATOR][SELECTED_CATEGORY]["LAUNCH_SIMULATOR_CMD"] + args.ros_args
    LAUNCH_ROBOT_CMD = LAUNCH_CONFIGS[SELECTED_SIMULATOR][SELECTED_CATEGORY]["LAUNCH_ROBOT_CMD"] + args.ros_args
except KeyError as e:
    print(f"Error: Could not find configuration for simulator '{SELECTED_SIMULATOR}' and category '{SELECTED_CATEGORY}'.")
    print(f"Missing key: {e}")
    sys.exit(1)

try:
    NODES_TO_KILL = LAUNCH_CONFIGS[SELECTED_SIMULATOR][SELECTED_CATEGORY]["NODES_TO_KILL"]
except KeyError:
    print(f"Warning: 'NODES_TO_KILL' not found for simulator '{SELECTED_SIMULATOR}' and category '{SELECTED_CATEGORY}'. Using empty list.")
    NODES_TO_KILL = []

ITERATION_TIME = int(args.iteration_time)
if ITERATION_TIME <= 0:
    print("Warning: --iteration_time must be greater than 0. Setting default value of 60 seconds.")
    ITERATION_TIME = 60


# Set IMAGE_TOPICS from --image_topic if provided, otherwise use the dictionary
if args.image_topic and args.image_topic != "":
    IMAGE_TOPICS = [args.image_topic]
else:
    try:
        IMAGE_TOPICS = LAUNCH_CONFIGS[SELECTED_SIMULATOR][SELECTED_CATEGORY]["TOPICS_TO_LISTEN"]
    except KeyError:
        print(f"Error: 'TOPICS_TO_LISTEN' not found for simulator '{SELECTED_SIMULATOR}' and category '{SELECTED_CATEGORY}'.")
        sys.exit(1)

CSV_FILE = args.csv_file


if CSV_FILE == "":
    timestamp = int(time.time())
    os.makedirs(f"benchmarks/{SELECTED_SIMULATOR}/{SELECTED_CATEGORY}", exist_ok=True)
    CSV_PATH = f"benchmarks/{SELECTED_SIMULATOR}/{SELECTED_CATEGORY}/ros2_launch_timings_{timestamp}.csv"
else:
    CSV_PATH = "ros2_launch_timings.csv"

ITERATIONS = int(args.iterations)  # Cambia esto para más/menos iteraciones
if ITERATIONS <= 0:
    print("Warning: --iterations must be greater than 0. Setting default value of 1 iteration.")
    ITERATIONS = 1

class ImageListener(Node):
    def __init__(self, namespace="image_listener"):
        super().__init__(f"image_listener_{random.randint(1000, 9999)}")
        self.image_received = False
        self.namespace = namespace
        self.subscription = self.create_subscription(
            Image,
            namespace,
            self.image_callback,
            10
        )
        print(f"Subscribed to {self.namespace}")

    def image_callback(self, msg):
        self.image_received = True
        self.destroy_subscription(self.subscription)

class ClockListener(Node):
    def __init__(self):
        super().__init__('clock_listener')
        self.first_clock_msg = None
        self.first_received_time = None
        self.last_clock_msg = None
        self.last_received_time = None
        self.real_time_factor = 1.0
        self.real_time_factor_array = []
        self.subscription = self.create_subscription(
            Clock,
            '/clock',
            self.clock_callback,
            qos_profile=qos_profile_sensor_data
        )

    def clock_callback(self, msg):
        """
        Callback for processing simulator clock updates, tracking the real-time factor.
        Args:
            msg: ROS 2 Clock message containing the current simulation time.
        Notes:
            - On the first received message, initializes the reference simulation time
              and the wall-clock timestamp for later comparisons.
            - For subsequent messages, computes the ratio between the simulated time
              elapsed and the real time elapsed (real-time factor) and appends it to
              ``real_time_factor_array``.
            - Updates internal timestamps and the last received clock message for
              continuous monitoring.
        """
        if self.first_clock_msg is None:
            self.first_clock_msg = msg
            self.first_received_time = time.time()

        self.last_clock_msg = msg
        self.last_received_time = time.time()
        
        if self.first_clock_msg is not None:
            clock_diff = msg.clock.sec - self.first_clock_msg.clock.sec + (msg.clock.nanosec - self.first_clock_msg.clock.nanosec) * 1e-9
            time_diff = time.time() - self.first_received_time
            self.real_time_factor = clock_diff / time_diff if time_diff > 0 else 1.0
            self.real_time_factor_array.append(self.real_time_factor)

        self.first_clock_msg = msg
        self.first_received_time = time.time()

    def get_first_msg(self):
        return self.first_clock_msg
    
    def get_real_time_factor_avg(self):
        moving_avg = None
        if len(self.real_time_factor_array) >= 100:
            moving_avg = sum(self.real_time_factor_array[-100:]) / 100
        return moving_avg
    
    def get_real_time_factor(self):
        return self.real_time_factor

def run_iteration(iter_num):
    """
    Execute a single simulation benchmark iteration and collect system performance metrics.
    Args:
        iter_num (int): Sequential identifier of the benchmark iteration, used for logging.
    Returns:
        tuple:
            elapsed (float): Seconds elapsed between launching the simulator and receiving the first image.
            cpu_mean (float): Average normalized CPU utilization (%) across simulator and robot processes.
            ram_mean (float): Average RAM usage (MB) across simulator and robot processes.
            gpu_util_mean (Optional[float]): Average GPU utilization (%) if a GPU is available, otherwise None.
            gpu_mem_mean (Optional[float]): Average GPU memory usage (MB) if a GPU is available, otherwise None.
            real_time_factor_mean (Optional[float]): Average real-time factor reported by the clock listener, or None when unavailable.
            iteration_total_time (float): Total wall-clock time (seconds) spent on the iteration, including post-image wait time.
    """
    # Lanzar el launch file
    start_time = time.time()
    launch_simulator_process = subprocess.Popen(LAUNCH_SIMULATOR_CMD)
    launch_robot_process = subprocess.Popen(LAUNCH_ROBOT_CMD)
    elapsed = 0
    print(f"[{iter_num}] Launching launch file...")

    rclpy.init()
    node_listeners = [ImageListener(topic) for topic in IMAGE_TOPICS]
    clock_node = ClockListener()

    print(f"[{iter_num}] Waiting for the first image message on {IMAGE_TOPICS}...")

    # Monitor resources in a background thread
    cpu_samples = []
    ram_samples = []
    gpu_util_samples = []
    gpu_mem_samples = []
    real_time_factor_samples = []
    stop_monitor = threading.Event()

    def monitor():
        procs = [psutil.Process(launch_simulator_process.pid), psutil.Process(launch_robot_process.pid)]
        print("Monitoring resources for processes:", procs)
        while not stop_monitor.is_set():
            all_procs = []
            for p in procs:
                try:
                    all_procs.append(p)
                    all_procs.extend(p.children(recursive=True))
                except Exception:
                    pass
            #print("Monitoring resources for all children processes:", all_procs)
            try:

                # Initialize cpu_percent for each process if not already done
                for proc in all_procs:
                    proc.cpu_percent(interval=None)
                time.sleep(0.5)  # Give time for cpu_percent to measure

                #for proc in all_procs:
                #    print(f"Process: {proc}, CPU%: {proc.cpu_percent(interval=0.5)}, RAM MB: {proc.memory_info().rss / (1024*1024)}")
                cpu = sum([proc.cpu_percent(interval=0.5) for proc in all_procs]) / psutil.cpu_count()  # Normalizar por número de núcleos
                ram = sum([proc.memory_info().rss for proc in all_procs]) / (1024*1024)  # MB
                #print(f"CPU: {cpu:.2f}%, RAM: {ram:.2f} MB")
                cpu_samples.append(cpu)
                ram_samples.append(ram)
                gpu_util, gpu_mem = get_gpu_usage(SELECTED_SIMULATOR)
                if gpu_util is not None:
                    gpu_util_samples.append(gpu_util)
                    if gpu_mem is not None:
                        gpu_mem_samples.append(gpu_mem)

            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

    monitor_thread = threading.Thread(target=monitor)
    monitor_thread.start()

    end_time = time.time() + 120  # Timeout of 2 minutes
    image_received = False
    try:
        while rclpy.ok() and time.time() < end_time:
            elapsed_time = time.time() - start_time
            print(f"Monitoring for {elapsed_time:.2f} seconds... {end_time - time.time():.2f} seconds to finalize")
            all_nodes_received = all(node.image_received for node in node_listeners)
            for node in node_listeners:
                rclpy.spin_once(node, timeout_sec=0.1)
            rclpy.spin_once(clock_node, timeout_sec=0.1)
            if not image_received and all_nodes_received:
                image_received = True
                end_time = time.time()
                elapsed = time.time() - start_time
                # Wait ITERATION_TIME seconds more after receiving the image
                extra_time = ITERATION_TIME
                print(f"Image received, waiting {extra_time} more seconds to stabilize...")
                end_time = time.time() + extra_time                
                print(f"[{iter_num}] Image received after {elapsed:.3f} seconds.")
            elif not image_received:
                print(f"[{iter_num}] Still waiting for topics images to set the startup time... ({elapsed_time:.2f}s elapsed)")
    finally:
        print(f"[{iter_num}] Finalizing processes...")
        # No need for extra sleep here, as interval=0.1 already waits
        rtf_avg = clock_node.get_real_time_factor()
        if rtf_avg is not None:
            real_time_factor_samples.append(rtf_avg)
        stop_monitor.set()
        monitor_thread.join()
        for node in node_listeners:
            node.destroy_node()
        clock_node.destroy_node()
        rclpy.shutdown()
        launch_simulator_process.send_signal(subprocess.signal.SIGINT)
        launch_simulator_process.terminate()
        launch_simulator_process.wait()
        launch_robot_process.terminate()
        launch_robot_process.send_signal(subprocess.signal.SIGINT)
        launch_robot_process.wait()
        
        kill_processes_by_name(NODES_TO_KILL)
    
        print(f"[{iter_num}] All processes finalized.")

    # Calcular medias
    cpu_mean = sum(cpu_samples)/len(cpu_samples) if cpu_samples else 0
    ram_mean = sum(ram_samples)/len(ram_samples) if ram_samples else 0
    gpu_util_mean = sum(gpu_util_samples)/len(gpu_util_samples) if gpu_util_samples else None
    gpu_mem_mean = sum(gpu_mem_samples)/len(gpu_mem_samples) if gpu_mem_samples else None
    real_time_factor_mean = sum(real_time_factor_samples)/len(real_time_factor_samples) if real_time_factor_samples else None
    iteration_total_time = time.time() - start_time

    return elapsed, cpu_mean, ram_mean, gpu_util_mean, gpu_mem_mean, real_time_factor_mean, iteration_total_time

def kill_processes_by_name(names):
    # Get and kill processes by name using NODES_TO_KILL, avoiding killing the parent process itself
    parent_pid = os.getpid()
    for proc in psutil.process_iter(['pid', 'cmdline']):
        if proc.pid == parent_pid:
            continue
        cmdline = proc.info.get('cmdline', [])
        if not isinstance(cmdline, list):
            continue
        cmdline_str = ' '.join(cmdline)
        if any(node_name in cmdline_str for node_name in names):
            print(f"Killing process: {cmdline_str} (PID: {proc.pid})")
            try:
                proc.kill()
            except Exception:
                pass

def write_csv_row(filename, row):
    file_exists = os.path.isfile(filename)
    with open(filename, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        if not file_exists:
            writer.writerow([
                'simulator', 'timestamp', 'iteration', 'elapsed_seconds',
                'cpu_mean_percent', 'ram_mean_mb', 'gpu_mean_percent', 'gpu_mem_mean_mb', 'real_time_factor_mean', 'iteration_total_time'
            ])
        writer.writerow(row)

def main():
    kill_processes_by_name(NODES_TO_KILL)
    
    for i in range(1, ITERATIONS + 1):
        elapsed, cpu_mean, ram_mean, gpu_util_mean, gpu_mem_mean, real_time_factor_mean, iteration_total_time = run_iteration(i)
        timestamp = datetime.now().isoformat()
        write_csv_row(CSV_PATH, [SELECTED_SIMULATOR, timestamp, i, elapsed, cpu_mean, ram_mean, gpu_util_mean, gpu_mem_mean, real_time_factor_mean, iteration_total_time])
        time.sleep(5)  # Espera entre iteraciones
        print(f"[{i}] Iteration {i} completed and recorded.")

if __name__ == "__main__":
    main()


