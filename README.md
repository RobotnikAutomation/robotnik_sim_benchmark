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

### 1.4 Unity

```
TO DO
```
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
python3 scripts/benchmark_simulator.py isaac_sim --category 4 --iterations 1 --image_topic front_rgbd_camera/color/image_raw
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