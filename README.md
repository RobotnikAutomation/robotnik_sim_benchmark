# robotnik_sim_benchmark

## 1. Simulators

Clone repository

```
mkdir -p ~/benchmark_ws/src
cd ~/benchmark_ws/src/
git clone https://github.com/RobotnikAutomation/robotnik_sim_benchmark.git
```

Install `vcstool`.
```
sudo apt update
sudo apt install python3-vcstool
```

### 1.1 Gazebo


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

### 1.2 Webots

```
ros2 run..
```

### 1.3 Isaac Sim


Requirements: `isaac_sim.sh` located in `$HOME/isaac_sim`
```
ros2 launch isaac_sim isaac_sim_complete.launch.py
```

### 1.4 Unity

```
./unity.sh...
```

## 2. Benchmark

Go to benchmark repository:

```
cd ~/benchmark_ws/src/robotnik_sim_benchmark/scripts
```

### 2.1 Gazebo
Run `gazebo_harmonic` benchmark:

```
python3 benchmark_simulator.py gazebo_harmonic
```

### 2.3 Isaac Sim

Run `isaac_sim` benchmark 

```
python3 benchmark_simulator.py isaac_sim
```