# robotnik_sim_benchmark

## 1. Simulators

Clone repository

```
mkdir -p ~/benchmark_ws/src && cd ~/benchmark_ws/src/
git clone https://github.com/RobotnikAutomation/robotnik_sim_benchmark.git
cd ~/benchmark_ws
colcon build
source  install/setup.bash
```

Install `vcstool`.
```
sudo apt update
sudo apt install python3-vcstool
```

<details>
<summary style="font-size:1.25em; font-weight:bold;">1.1 Gazebo</summary>

Install Gazebo Harmonic with ROS 2 Humble:

1. Setup sources and keys.
```
sudo apt update
sudo apt-get install curl lsb-release gnupg
sudo curl https://packages.osrfoundation.org/gazebo.gpg --output /usr/share/keyrings/pkgs-osrf-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/pkgs-osrf-archive-keyring.gpg] http://packages.osrfoundation.org/gazebo/ubuntu-stable $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/gazebo-stable.list > /dev/null
```

2. Install Gazebo Harmonic.
```
sudo apt-get update
sudo apt-get install gz-harmonic
```

3. Install ROS 2 connectors for Gazebo Harmonic.

> **WARNING**: The package `ros-humble-ros-gzharmonic` conflicts with `ros-humble-ros-gz*`. Remove those packages before installing.
```
sudo apt-get update
sudo apt-get remove ros-humble-ros-gz*
sudo apt-get autoremove
sudo apt-get install ros-humble-ros-gzharmonic
```

Set up workspace and install dependencies:

1. Download required repositories:
```
mkdir -p ~/robotnik_benchmark_gazebo_ws/src
cd ~/robotnik_benchmark_gazebo_ws/src
vcs import --input https://raw.githubusercontent.com/RobotnikAutomation/robotnik_simulation/refs/heads/jazzy-devel/robotnik_simulation.humble.repos
```

2. Install closed-source packages:
```
source /opt/ros/humble/setup.bash
export GZ_VERSION=harmonic
cd ~/robotnik_benchmark_gazebo_ws/src/robotnik/robotnik_simulation/debs/
sudo apt-get install ./ros-${ROS_DISTRO}-*.deb
```

3. Install missing dependencies:
```
source /opt/ros/humble/setup.bash
export GZ_VERSION=harmonic
cd ~/robotnik_benchmark_gazebo_ws
rosdep update --rosdistro humble
rosdep install --from-paths src --ignore-src -r -y --skip-keys="gz-plugin2 gz-sim8"
```

4. Build workspace:
```
source /opt/ros/humble/setup.bash
export GZ_VERSION=harmonic
cd ~/robotnik_benchmark_gazebo_ws
colcon build --symlink-install
```

Run Gazebo Harmonic simulation:

1. Spawn world:
```
source ~/robotnik_benchmark_gazebo_ws/install/setup.bash
ros2 launch robotnik_gazebo_ignition spawn_world.launch.py
```

2. Spawn a robot instance (e.g., `robot_a`):
```
ros2 launch robotnik_gazebo_ignition spawn_robot.launch.py robot_id:=robot_a robot:=rbwatcher
```

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">1.2 Isaac Sim</summary>

Requirements: `isaac_sim.sh` located in `$HOME/isaac_sim`
```
ros2 launch isaac_sim isaac_sim_complete.launch.py
```

</details>

### 1.3 O3DE

```
TO DO
```

<details>
<summary style="font-size:1.25em; font-weight:bold;">1.4 Unity</summary>

Install and run the Unity simulation with ROS 2 Humble:

## 1. Prerequisites

- ROS 2 Humble installed and sourced.
- Unity binary (provided via download link).
- ROS–Unity bridge: [ROS-TCP-Endpoint](https://github.com/Unity-Technologies/ROS-TCP-Endpoint).

## 2. Download Unity Simulation

To download the unity simulation, choose one of the following methods:

1. Using `gdown` (command line)

    1.1. Install `gdown` (Google Drive downloader for command line):
    ```bash
    pip install gdown
    ```

    1.2. Download the precompiled Unity binary automatically:
    ```bash
    gdown https://drive.google.com/uc?id=1NDRtJ9zw5TGTveNKsOdgXoxGDFOHcktZ
    ```

   This will download the file `unity_simulation.tar.gz`.
2. Download from Google Drive using a web browser:
   2.1. Go to the following link:  

   [Unity Simulation Binary](https://drive.google.com/file/d/1NDRtJ9zw5TGTveNKsOdgXoxGDFOHcktZ/view?usp=drive_link)  
   
   2.2. Click on the download button to download the file `unity_simulation.tar.gz`.
3. Extract the package to your preferred directory, for example:
   ```bash
   mkdir -p ~/robotnik_benchmark_unity
   cd ~/robotnik_benchmark_unity
   tar -xvzf unity_simulation.tar.gz
   ```

## 3. Install Unity–ROS bridge

1. Clone the ROS–Unity bridge into your ROS 2 workspace:
   ```bash
   mkdir -p ~/robotnik_benchmark_unity_ws/src
   cd ~/robotnik_benchmark_unity_ws/src
   git clone https://github.com/Unity-Technologies/ROS-TCP-Endpoint.git
   ```

2. Build the workspace:
   ```bash
   source /opt/ros/humble/setup.bash
   cd ~/robotnik_benchmark_unity_ws
   colcon build --symlink-install
   ```

3. Source the workspace:
   ```bash
   source ~/robotnik_benchmark_unity_ws/install/setup.bash
   ```

## 4. Run Unity Simulation

1. Launch the Unity simulation binary:
   ```bash
   cd ~/robotnik_benchmark_unity
   ./PI_simulation_Unity_Robotnik.x86_64
   ```

2. Launch the ROS–Unity bridge:
   ```bash
   ros2 run ros_tcp_endpoint default_server_endpoint --ros-args -p ROS_IP:=0.0.0.0
   ```

## 5. Run Simulation with Launch File

> **TODO**: Integrate Unity simulation and ROS–Unity bridge into a single launch file.  
> Example (to be completed later):
> ```bash
> ros2 launch robotnik_unity_simulation simulation.launch.py
> ```

---

### Notes
- Ensure Unity binary has execution permission:
  ```bash
  chmod +x UnitySimulation.x86_64
  ```
- If Unity and ROS are running on different machines, configure network settings accordingly (ROS_DOMAIN_ID, IPs, etc.).

</details>

### 1.5 Webots

```
TO DO
```



## 2. Benchmarks

### 2.1 Specifications

This is the sensor configuration:

| Sensor        | Frequency |
|---------------|------------|
| Front camera  | 30 fps     |
| Lidar 3D      | 10 Hz      | 
| IMU           | 200 Hz     |
| Top camera    | 30 Hz      |

5 benchmarks

Go to benchmark repository:

```
cd ~/benchmark_ws/src/robotnik_sim_benchmark
```

### 2.1 Benchmarking

Run `gazebo_harmonic` benchmark:

```
TO DO
```

Run `isaac_sim` benchmark 

```
python3 scripts/benchmark_simulator.py isaac_sim --image_topic front_rgbd_camera/color/image_raw
```

Run `o3de` benchmark:

```
TO DO
```

Run `unity` benchmark:

```
TO DO
```

Run `webots` benchmark:

```
TO DO
```

## 3. Results

For the performance report, see [performance_report.md](benchmarks/performance_report.md)

Go to benchmark repository:

```
cd ~/benchmark_ws/src/robotnik_sim_benchmark
```

Generate report:

```
python3 scripts/benchmark_reporter.py
```

**Note**: Report file is created in `benchmark` folder