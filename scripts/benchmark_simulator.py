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

def get_gpu_usage():
    """Return total GPU utilization (%) and memory (MiB) if NVIDIA GPU is present, else (None, None)."""
    try:
        result = sp.run([
            'nvidia-smi',
            '--query-gpu=utilization.gpu,memory.used',
            '--format=csv,noheader,nounits'
        ], capture_output=True, text=True, check=True)
        lines = result.stdout.strip().split('\n')
        total_util = 0
        total_mem = 0
        for line in lines:
            util, mem = line.split(',')
            total_util += float(util.strip())
            total_mem += float(mem.strip())
        return total_util, total_mem
    except Exception:
        return None, None

LAUNCH_CONFIGS = {
    "gazebo_harmonic": {
        "LAUNCH_SIMULATOR_CMD": [
            "ros2", "launch", "robotnik_gazebo_ignition", "spawn_world.launch.py"
        ],
        "LAUNCH_ROBOT_CMD": [
            "ros2", "launch", "robotnik_gazebo_ignition", "spawn_robot.launch.py",
            "robot:=rbwatcher", "robot_model:=rbwatcher"
        ],
        "NODES_TO_KILL": ["parameter_bridge", "rviz2", "gz", "robot_state_publisher"]
    },
    "isaac_sim": {
        "LAUNCH_SIMULATOR_CMD": [
            "ros2", "launch", "isaac_sim", "isaac_sim_complete.launch.py"
        ],
        "LAUNCH_ROBOT_CMD": [
            "ros2", "launch", "robotnik_gazebo_ignition", "spawn_robot.launch.py",
            "robot:=rbwatcher", "robot_model:=rbwatcher"
        ],
        "NODES_TO_KILL": ["rviz2", "isaac"]
    },
    "webots": {
        "LAUNCH_SIMULATOR_CMD": [
            "ros2", "launch", "webots_robotnik", "world_launch.py"
        ],
        "LAUNCH_ROBOT_CMD": [
            "ros2", "launch", "webots_robotnik", "robot_launch_alfa.py",
            "robot:=rbwatcher", "namespace:=robot", "x:=2.0", "y:=2.0", "z:=0.0"
        ],
        "NODES_TO_KILL": ["rviz2", "robot_state_publisher", "webots", "Ros2Supervisor", "static_transform_publisher"]
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
]

parser = argparse.ArgumentParser(description="Benchmark simulator script")
parser.add_argument("simulator", help="Simulator name (gazebo_harmonic, isaac_sim, webots)")
parser.add_argument("--image_topic", default="/robot/front_rgbd_camera/color/image_raw", help="Image topic to subscribe to")
parser.add_argument("--csv_file", default="", help="CSV file to store results")
parser.add_argument("--iterations", default=1, help="Number of interations")
parser.add_argument("--category", default=0, help="Category name for an specific set of benchmarks")
if "--help" in sys.argv or "-h" in sys.argv or len(sys.argv) < 2:
    parser.print_help()
    sys.exit(0)
args = parser.parse_args()

SELECTED_SIMULATOR = args.simulator
if SELECTED_SIMULATOR not in LAUNCH_CONFIGS:
    print(f"Simulator '{SELECTED_SIMULATOR}' not found in LAUNCH_CONFIGS.")
    sys.exit(1)
LAUNCH_SIMULATOR_CMD = LAUNCH_CONFIGS[SELECTED_SIMULATOR]["LAUNCH_SIMULATOR_CMD"]
LAUNCH_ROBOT_CMD = LAUNCH_CONFIGS[SELECTED_SIMULATOR]["LAUNCH_ROBOT_CMD"]
NODES_TO_KILL = LAUNCH_CONFIGS[SELECTED_SIMULATOR]["NODES_TO_KILL"]

SELECTED_SIMULATOR = args.simulator
IMAGE_TOPIC = args.image_topic
CSV_FILE = args.csv_file

SELECTED_CATEGORY = CATEGORY[int(args.category)]

if CSV_FILE == "":
    timestamp = int(time.time())
    os.makedirs(f"benchmarks/{SELECTED_SIMULATOR}/{SELECTED_CATEGORY}", exist_ok=True)
    CSV_PATH = f"benchmarks/{SELECTED_SIMULATOR}/{SELECTED_CATEGORY}/ros2_launch_timings_{timestamp}.csv"
else:
    CSV_PATH = "ros2_launch_timings.csv"

ITERATIONS = int(args.iterations)  # Cambia esto para más/menos iteraciones

class ImageListener(Node):
    def __init__(self):
        super().__init__('image_listener')
        self.image_received = False
        self.subscription = self.create_subscription(
            Image,
            IMAGE_TOPIC,
            self.image_callback,
            10
        )
        print(f"Subscribed to {IMAGE_TOPIC}")

    def image_callback(self, msg):
        self.image_received = True

class ClockListener(Node):
    def __init__(self):
        super().__init__('clock_listener')
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

        if self.last_clock_msg is not None:
            clock_diff = msg.clock.sec - self.last_clock_msg.clock.sec + (msg.clock.nanosec - self.last_clock_msg.clock.nanosec) * 1e-9
            time_diff = time.time() - self.last_received_time
            self.real_time_factor = clock_diff / time_diff if time_diff > 0 else 1.0
            self.real_time_factor_array.append(self.real_time_factor)
            
            #print(f"Clock diff: {clock_diff:.6f} s, Real time diff: {time_diff:.6f} s")
            #print(f"Real time factor: {self.real_time_factor:.6f}")
            #if len(self.real_time_factor_array) >= 10:
            #    moving_avg = sum(self.real_time_factor_array[-10:]) / 10
                #print(f"Real time factor (moving avg last 10): {moving_avg:.6f}")

        self.last_clock_msg = msg
        self.last_received_time = time.time()

    def get_last_msg(self):
        return self.last_clock_msg
    
    def get_real_time_factor_avg(self):
        moving_avg = None
        if len(self.real_time_factor_array) >= 100:
            moving_avg = sum(self.real_time_factor_array[-100:]) / 100
        return moving_avg

def run_iteration(iter_num):
    # Lanzar el launch file
    start_time = time.time()
    launch_simulator_process = subprocess.Popen(LAUNCH_SIMULATOR_CMD)
    launch_robot_process = subprocess.Popen(LAUNCH_ROBOT_CMD)
    print(f"[{iter_num}] Lanzando launch file...")
    #time.sleep(5)  # Espera para asegurar que ROS 2 inicia

    rclpy.init()
    node = ImageListener()
    clock_node = ClockListener()

    print(f"[{iter_num}] Esperando primer mensaje de imagen en {IMAGE_TOPIC}...")

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
            print("Monitoring resources for all children processes:", all_procs)
            try:

                # Initialize cpu_percent for each process if not already done
                for proc in all_procs:
                    proc.cpu_percent(interval=None)
                time.sleep(0.5)  # Give time for cpu_percent to measure

                for proc in all_procs:
                    print(f"Process: {proc}, CPU%: {proc.cpu_percent(interval=0.5)}, RAM MB: {proc.memory_info().rss / (1024*1024)}")
                cpu = sum([proc.cpu_percent(interval=0.5) for proc in all_procs]) / psutil.cpu_count()  # Normalizar por número de núcleos
                ram = sum([proc.memory_info().rss for proc in all_procs]) / (1024*1024)  # MB
                print(f"CPU: {cpu:.2f}%, RAM: {ram:.2f} MB")
                cpu_samples.append(cpu)
                ram_samples.append(ram)
                gpu_util, gpu_mem = get_gpu_usage()
                if gpu_util is not None:
                    gpu_util_samples.append(gpu_util)
                    gpu_mem_samples.append(gpu_mem)
                
                    
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

    monitor_thread = threading.Thread(target=monitor)
    monitor_thread.start()

    end_time = time.time() + 300  # Timeout de 5 minutos
    image_received = False
    try:
        while rclpy.ok() and time.time() < end_time:
            rclpy.spin_once(node, timeout_sec=0.1)
            rclpy.spin_once(clock_node, timeout_sec=0.1)
            if not image_received and node.image_received:
                image_received = True
                end_time = time.time()
                elapsed = end_time - start_time
                # Wait 60 seconds more after receiving the image
                extra_time = 60
                print(f"Imagen recibida, esperando {extra_time} segundos más para estabilizar...")
                end_time = time.time() + extra_time                
                print(f"[{iter_num}] Imagen recibida tras {elapsed:.3f} segundos.")
    finally:
        print(f"[{iter_num}] Finalizando procesos...")
        # No need for extra sleep here, as interval=0.1 already waits
        rtf_avg = clock_node.get_real_time_factor_avg()
        if rtf_avg is not None:
            real_time_factor_samples.append(rtf_avg)
        stop_monitor.set()
        monitor_thread.join()   
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
    
        print(f"[{iter_num}] Launch file terminado.")

    # Calcular medias
    cpu_mean = sum(cpu_samples)/len(cpu_samples) if cpu_samples else 0
    ram_mean = sum(ram_samples)/len(ram_samples) if ram_samples else 0
    gpu_util_mean = sum(gpu_util_samples)/len(gpu_util_samples) if gpu_util_samples else None
    gpu_mem_mean = sum(gpu_mem_samples)/len(gpu_mem_samples) if gpu_mem_samples else None
    real_time_factor_mean = sum(real_time_factor_samples)/len(real_time_factor_samples) if real_time_factor_samples else None
    iteration_total_time = time.time() - start_time

    return elapsed, cpu_mean, ram_mean, gpu_util_mean, gpu_mem_mean, real_time_factor_mean, iteration_total_time

def kill_processes_by_name(names):
    # Obtener y matar procesos por nombre usando NODES_TO_KILL, evitando matar el propio proceso padre
    parent_pid = os.getpid()
    for proc in psutil.process_iter(['pid', 'cmdline']):
        if proc.pid == parent_pid:
            continue
        cmdline = proc.info.get('cmdline', [])
        if not isinstance(cmdline, list):
            continue
        cmdline_str = ' '.join(cmdline)
        if any(node_name in cmdline_str for node_name in names):
            print(f"Matando proceso: {cmdline_str} (PID: {proc.pid})")
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
        print(f"[{i}] Iteración {i} completada y registrada.")

if __name__ == "__main__":
    main()