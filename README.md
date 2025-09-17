# robotnik_sim_benchmark

## 1. Simulators

Clone repository

```
mkdir -p ~/benchmark_ws/src
cd ~/benchmark_ws/src/
git clone https://github.com/RobotnikAutomation/robotnik_sim_benchmark.git
```


### Gazebo

install vcstool
```
sudo apt update
sudo apt install python3-vcstool
```

clone repositories
```
mkdir -p ~/benchmark_ws/src/gazebo && cd ~/benchmark_ws/src/gazebo
vcs import --input https://raw.githubusercontent.com/RobotnikAutomation/robotnik_simulation/refs/heads/jazzy-devel/robotnik_simulation.humble.repos
```

install controllers
```
cd robotnik/robotnik_simulation/debs/
sudo dpkg -i ros-humble-*.deb
```

Install dependencies

```
cd ~/benchmark_ws
rosdep update
rosdep install --from-paths src --ignore-src -r -y
```

compile:

```
colcon build
source install/setup.bash
```


```
ros2 run...
```

### Webots

```
ros2 run..
```

### Isaac Sim


Requirements: `isaac_sim.sh` located in `$HOME/isaac_sim`
```
ros2 launch isaac_sim isaac_sim_complete.launch.py
```

### Unity

```
./unity.sh...
```

## 2. Benchmark

```
.//robotnik_benchmark.sh...
```
