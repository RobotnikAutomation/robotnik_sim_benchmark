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
ros2 launch isaac_sim isaac_sim_complete.launch.py num_robots:=1 world_file:=simple_world.usd run_rviz:=false
```

</details>

<details>
<summary style="font-size:1.25em; font-weight:bold;">O3DE</summary>

## 1. Prerequisites
```
TO DO
```

## 2. Recommended: Run with Launch File

```
TO DO
```
</details>

<details>
<summary style="font-size:1.25em; font-weight:bold;">1.4 Unity</summary>

Install and run the Unity simulation with ROS 2 Humble (also tested on ROS 2 Jazzy):

## 1. Prerequisites

- ROS 2 Humble installed and sourced. *(Also works on Humble or Jazzy.)*
- ROS–Unity bridge: [ROS-TCP-Endpoint](https://github.com/Unity-Technologies/ROS-TCP-Endpoint). Add to your workspace:
  ```bash
  cd ~/workspace/src
  git clone  --branch=main-ros2 https://github.com/Unity-Technologies/ROS-TCP-Endpoint.git
  ```
- The Unity simulation archive placed at:
  `unity_sim/worlds/unity_simulation.tar.gz`
  *(The launch auto-extracts it on first run.)*

## 2. Recommended: Run with Launch File

This launch:
- Starts **ROS-TCP-Endpoint** listening on **0.0.0.0**.
- Starts **RViz2** with **use_sim_time:=true** and config `rviz/robot.rviz`.
- Runs the bootstrap script `utils/load_usd_and_run.py` which **extracts** the tar (if needed) and starts the Unity binary.
- Optionally **spawns N robots** via `/robot[/_N]/on` services.

Run:
```bash
# 1 robot (default)
ros2 launch unity_sim unity_complete.launch.py

# 1 robot in simple_world
ros2 launch unity_sim unity_complete.launch.py world:=simple_world

# 3 robots and RViz on
ros2 launch unity_sim unity_complete.launch.py robot_count:=3 run_rviz:=true

# 2 robots, no RViz, in simple_world
ros2 launch unity_sim unity_complete.launch.py robot_count:=2 run_rviz:=false world:=simple_world

```

**Arguments**
- `robot_count` (int, 1..5, default: 1) — spawns `robot`, `robot_2`, … `robot_5`.
- `run_rviz` (bool, default: true) — toggles RViz2.
- `world` (string, default: `empty_world`) — choose the world to load. Available worlds:
  - `empty_world` — empty plane.
  - `simple_world` — simple scene with some objects.

> If the launch prints an error like
> `Archive not found: .../unity_sim/worlds/unity_simulation.tar.gz`,
> make sure the archive exists at that exact path (or the extracted binary is already present somewhere under `unity_sim/worlds/`).

## 3. (Optional) Manual Download/Update of the Archive

If you need to refresh the Unity build:

**A) Using `gdown`**
```bash
pip install gdown
gdown https://drive.google.com/uc?id=1NDRtJ9zw5TGTveNKsOdgXoxGDFOHcktZ
mv unity_simulation.tar.gz unity_sim/worlds/
```

**B) Using a web browser**
- Open: [Unity Simulation Binary](https://drive.google.com/file/d/1NDRtJ9zw5TGTveNKsOdgXoxGDFOHcktZ/view?usp=drive_link)
- Download `unity_simulation.tar.gz` and place it in `unity_sim/worlds/`.

## 4. (Optional) Manual Run Without Launch

1) Extract and run the Unity simulation:
```bash
cd unity_sim/worlds
tar -xvzf unity_simulation.tar.gz
chmod +x UnitySimulation.x86_64  # or your binary name (e.g., PI_simulation_Unity_Robotnik.x86_64)
./UnitySimulation.x86_64         # replace with your actual filename if different
```

2) Start the ROS–Unity bridge on 0.0.0.0:
```bash
ros2 run ros_tcp_endpoint default_server_endpoint --ros-args -p ROS_IP:=0.0.0.0
```

## 5. Notes

- **RViz time**: RViz launches with `use_sim_time:=true` because the simulator publishes `/clock`.
- **Keyboard shortcuts in the simulator**:
  - `F1`: show performance stats.
  - `F2`: respawn/destroy robots.
  - Navigation: arrow keys to move, mouse wheel to zoom; to follow a robot, pick it from the bottom-right dropdown.
- **Robot services** (provided by the simulation):
  - Spawn: `robot_{id}/on`   (e.g., `/robot/on`, `/robot_2/on`, …)
  - Delete: `robot_{id}/off` (e.g., `/robot/off`, `/robot_2/off`, …)

</details>

<details>
<summary style="font-size:1.25em; font-weight:bold;">1.5 Webots</summary>

1. Download required repositories:
```
mkdir -p ~/robotnik_benchmark_webots_ws/src
cd ~/robotnik_benchmark_webots_ws/src
git clone https://github.com/RobotnikAutomation/robotnik_webots.git
git clone https://github.com/RobotnikAutomation/robotnik_common.git
```
2. Install missing dependencies:
Follow the guide to install webots from via apt: https://cyberbotics.com/doc/guide/installation-procedure#installation-on-linux
```
sudo apt-get install ros-humble-webots-ros2
cd ~/robotnik_benchmark_webots_ws
rosdep update --rosdistro humble
rosdep install --from-paths src --ignore-src -r -y 
```

3. Build workspace:
```
source /opt/ros/humble/setup.bash
cd ~/robotnik_benchmark_webots_ws
colcon build --symlink-install
```

Run Webots simulation:

1. Spawn world:
```
source ~/robotnik_benchmark_webots_ws/install/setup.bash
ros2 launch robotnik_webots spawn_world.launch.py
```

2. Spawn a robot instance (e.g., `robot_a`):
```
ros2 launch robotnik_webots spawn_robot.launch.py robot_id:=robot_a robot:=rbwatcher
```
</details>


## 2. Benchmarks

### 2.1 Specifications

This is the sensor configuration for 1 robot:

| Sensor        | Frequency |
|---------------|------------|
| Front camera  | 1920x1080@30fps |
| Lidar 3D      | 10 Hz      | 
| IMU           | 200 Hz     |
| Top camera    | 1920x1080@30fps     |


### 2.1 Benchmarking

Go to benchmark repository:

```
cd ~/benchmark_ws/src/robotnik_sim_benchmark
```

The benchmark iterations is set by `--iteration`: 

| Simulator        | Iterations |
|---------------|------------|
| Any  |   1 (default)     |



The benchmark results are saved under the category folder specified by the `--category` argument.  

> Changing the conditions of the simulation (e.g., number of robots or world type) must be done manually for each simulation.

By default, this repository launches **one robot in a simple world**, which corresponds to **category 4**.

| Category  | Name                            | Description 
|----|------| --------------------------------| 
| 0  |         No category                    | No folder
| 1  |         one_robot_emtpy_world    | One robot without scene results
| 2  |         two_robot_emtpy_world    | Two robot without scene results
| 3  |         three_robot_emtpy_world  | Three robot without scene results
| 4  |         one_robot_simple_world   | One robot in a lightweight scene results
| 5  |         two_robot_simple_world   | Two robot in a lightweight scene results
| 6  |         three_robot_simple_world | Three robot in a lightweight scene results

Run `gazebo_harmonic` benchmark:

```
TO DO
```

Run `isaac_sim` benchmark 

```
python3 scripts/benchmark_simulator.py isaac_sim --category 4 --iterations 1 --image_topic front_rgbd_camera/color/image_raw --ros_args num_robots:=1 world_file:=simple_world.usd
```

Run `o3de` benchmark:

```
TO DO
```

Run `unity` benchmark:

```
python3 scripts/benchmark_simulator.py unity --image_topic /robot/top_rgbd_camera/image_raw --iterations 1 --category 5 --ros_args robot_count:=2 world:=simple_world
```

Run `webots` benchmark:

```
python3 ./scripts/benchmark_simulator.py --image_topic /robot/robot/front_rgbd_camera_color/image_color --category 4 --iterations 1 webots
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
