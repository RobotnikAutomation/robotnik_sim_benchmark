# Robotnik Simulation Benchmark

## 1. Introduction

`robotnik_sim_benchmark` is the reproducible integration repository for
comparing the same Robotnik robot workload in six simulation backends:
Gazebo Harmonic, Webots, NVIDIA Isaac Sim, MuJoCo, Open 3D Engine (O3DE), and
Unity.

The objective is not to declare a universally best simulator. It is to make
the trade-offs measurable and repeatable: the same robot model, worlds,
sensor profile, ROS 2 interfaces, scenario combinations, measurement periods,
and result format are used wherever the backend supports them. This makes the
repository useful for capacity planning, simulator selection, regression
tracking, and identifying differences between rendering, physics, and ROS 2
integration.

Simulation is important because it allows robotics teams to test many robots,
sensor configurations, environments, and failure cases before using physical
hardware. It also makes repeatable performance measurements possible and
reduces the cost and risk of validating changes.

Official simulator information:

| Simulator | Official information |
|---|---|
| Gazebo Harmonic | [Gazebo Harmonic documentation](https://gazebosim.org/docs/harmonic/) |
| Webots | [Cyberbotics Webots](https://cyberbotics.com/) |
| NVIDIA Isaac Sim | [Isaac Sim documentation](https://docs.isaacsim.omniverse.nvidia.com/latest/) |
| MuJoCo | [MuJoCo documentation](https://mujoco.readthedocs.io/) |
| O3DE | [O3DE documentation](https://docs.o3de.org/docs/) |
| Unity | [Unity for robotics](https://unity.com/solutions/robotics) |

The integration branch is `review/jazzy-2026`. This project is published by
updating that branch directly; it does not require Pull Requests.

## 2. Benchmark approach

The benchmark defines one canonical workload and adapts only the launch
mechanism required by each backend. The comparison is based on:

- the `rbwatcher` robot model;
- one, two, or three robot instances;
- an empty world and a simple world;
- GUI and headless execution;
- RViz disabled or enabled;
- the same canonical sensor intent: two RGB/RGB-D cameras, a 16-channel
  3D lidar, and an IMU;
- ROS 2 topic and message-rate monitoring when enabled;
- independent simulator workspaces and isolated build environments.

The adapters map equivalent concepts to backend-specific names. For example,
Isaac Sim uses USD world files, O3DE uses levels, and Unity uses scene names,
but all of them represent the same `empty` and `simple` benchmark cases.
Backend-specific limitations or unavailable sensors must be recorded with the
result rather than silently changing the common workload.

The source of truth is [`config/benchmark_config.yaml`](config/benchmark_config.yaml)
and the sensor contract is [`config/canonical_sensor_profile.yaml`](config/canonical_sensor_profile.yaml).

## 3. Scenario matrix

The current configuration contains 24 categories:

| Dimension | Values | Count |
|---|---|---:|
| World | `empty`, `simple` | 2 |
| Robot count | 1, 2, 3 | 3 |
| RViz | disabled, enabled | 2 |
| Execution mode | GUI, headless | 2 |
| **Total** | 2 × 3 × 2 × 2 | **24** |

World names are translated per simulator as follows:

| Common case | Gazebo | Webots | Isaac Sim | Unity | O3DE | MuJoCo |
|---|---|---|---|---|---|---|
| Empty | `empty` | `empty` | `empty_world.usd` | `empty_world` | `EmptyLevel` | `empty` |
| Simple | `demo` | `demo` | `simple_world.usd` | `simple_world` | `BasicLevel` | `simple` |

Category names are generated from these dimensions. List them at any time with:

```bash
python3 scripts/validate/validate_config.py --category-names
```

## 4. Configuration parameters and observations

### Parameters

| Parameter | Current values/default | Meaning |
|---|---|---|
| `robot_model` | `rbwatcher` | Robot description used by the workload |
| `robot_counts` | `1`, `2`, `3` | Number of simultaneous robot instances |
| `worlds` | `empty`, `simple` | Canonical environments and backend mappings |
| `modes.gui.headless` | `false` | Rendered execution |
| `modes.headless.headless` | `true` | Headless execution |
| `rviz` | `false`, `true` | Whether RViz is included |
| Physics clock | `50 Hz` | Target simulation clock in the sensor profile |
| Camera A | `1920×1080`, RGB, `25 Hz` | Main colour camera |
| Camera B | `1280×720`, RGB-D, `25 Hz`, `32FC1` depth | Depth camera |
| 3D lidar | `16` channels, `1800` samples/channel, `10 Hz` | `28,800` points per scan |
| IMU | `100 Hz` | Inertial sensor rate |
| QoS | best effort, volatile, keep last, depth 5 | Canonical ROS 2 transport profile |
| Measurement time | `60 s` by default | Time measured after readiness |
| Iterations | `1` by default | Repetitions per category; use more for statistics |
| Warm-up | `0 s` by default | Stabilisation time before measurement |
| Startup timeout | `120 s` by default | Maximum readiness wait |
| Retries | `3` by default | Retries after a failed iteration |
| Retry/iteration cooldown | `5 s` / `5 s` | Cleanup and inter-iteration pauses |
| Category cooldown | `10 s` in campaigns | Pause between categories |
| Render FPS cap | `60` by default | GUI render cap; not measured for headless runs |
| ROS monitoring | disabled by default | Enables per-topic transport statistics |

### Observable results

Performance CSV files record simulator, timestamp, iteration, first-frame and
startup time, total iteration time, CPU mean usage, CPU core peak and
saturation, RAM, GPU utilisation, GPU memory utilisation, GPU temperature,
GPU power, GPU and memory clocks, real-time factor statistics, clock message
count, clock resets, clock gaps, image-topic rate, image payload rate, image
gaps, image message count, render FPS cap, and measured render FPS.

Optional ROS CSV files record simulator, category, timestamp, iteration, topic,
message type, publisher count, message count, topic rate, payload MiB/s, and
maximum message gap. These measurements help distinguish simulator workload
limitations from ROS 2 transport or bridge limitations.

## 5. Basic installation

The reference environment is Ubuntu with ROS 2 Jazzy. Install the common
tools first:

```bash
sudo apt update
sudo apt install git git-lfs build-essential cmake ninja-build python3-pip
sudo apt install ros-jazzy-desktop python3-colcon-common-extensions
git lfs install
```

Each backend has additional requirements. Install the simulator version and
GPU drivers required by its official documentation before building its
workspace. In particular, Isaac Sim requires a compatible NVIDIA GPU and
installation; O3DE requires a compatible engine checkout; and Unity requires
a host capable of running the distributed Player archives.

Clone the integration branch and initialise its pinned submodules:

```bash
git clone -b review/jazzy-2026 \
  https://github.com/RobotnikAutomation/robotnik_sim_benchmark.git
cd robotnik_sim_benchmark
./scripts/setup_workspace.sh
```

Download Git LFS assets when required by Unity or O3DE:

```bash
./scripts/setup_workspace.sh --pull-lfs
```

The repository contains one workspace per backend:

```text
robotnik_sim_benchmark/
├── benchmarks/                         # Local results; ignored by Git
├── config/                             # Matrix and sensor contract
├── scripts/                            # Setup, build, execution, validation, reports
├── robotnik_benchmark_gazebo_ws/src/robotnik/
├── robotnik_benchmark_webots_ws/src/
├── robotnik_benchmark_isaac_ws/src/
├── robotnik_benchmark_mujoco_ws/src/
├── robotnik_benchmark_o3de_ws/src/
└── robotnik_benchmark_unity_ws/src/
```

All direct dependencies are declared in [`.gitmodules`](.gitmodules) and are
fixed to commits. The nested `robotnik_isaac_ros2_control` submodule is not
needed for this benchmark and is intentionally not part of the bootstrap
operation.

## 6. Building the workspaces

Build only the backend you need:

```bash
./scripts/build_workspace.sh gazebo_harmonic
./scripts/build_workspace.sh webots
./scripts/build_workspace.sh isaac_sim
./scripts/build_workspace.sh mujoco
./scripts/build_workspace.sh o3de
./scripts/build_workspace.sh unity
```

Build all backends in dependency order with:

```bash
./scripts/build_workspace.sh all
```

The script sources ROS 2 and builds each workspace independently. It does not
share `build/`, `install/`, or `log/` directories between simulators.

### O3DE-specific preparation

O3DE generates its project locally; generated binaries are not stored in this
repository.

```bash
export O3DE_HOME=/opt/O3DE/26.05
export O3DE_EXTRAS_HOME=$PWD/robotnik_benchmark_o3de_ws/src/o3de-extras
export PROJECT_PATH=$PWD/robotnik_benchmark_o3de_ws/src/robotnik_o3de/project/robotnik_roscon25

git -C "$O3DE_EXTRAS_HOME" lfs pull
"$O3DE_HOME/scripts/o3de.sh" register --all-gems-path "$O3DE_EXTRAS_HOME/Gems"
"$O3DE_HOME/scripts/o3de.sh" register --all-templates-path "$O3DE_EXTRAS_HOME/Templates"

cd "$PROJECT_PATH"
cmake -B build/linux -G "Ninja Multi-Config" \
  -DLY_DISABLE_TEST_MODULES=ON \
  -DCMAKE_EXPORT_COMPILE_COMMANDS=ON \
  -DLY_STRIP_DEBUG_SYMBOLS=ON
cmake --build build/linux --config profile \
  --target robotnik_roscon25 Editor robotnik_roscon25.Assets robotnik_roscon25.GameLauncher
```

The remaining ROS 2 wrapper is built by `build_workspace.sh o3de`. Run the
engine directly or through the configured ROS 2 launch file, then run the
benchmark from the repository root.

### Unity-specific preparation

The Unity integration has two distinct parts:

- `ROS-TCP-Endpoint` and `unity_sim` are ROS 2 packages and are built with
  `colcon`.
- Unity Players are distributed as compressed archives in `robotnik_unity`;
  the complete Unity source project is not currently available as a submodule.

After initialising LFS assets, verify and build the ROS packages:

```bash
UNITY_REPO=robotnik_benchmark_unity_ws/src/robotnik_unity
git -C "$UNITY_REPO" lfs pull
python3 "$UNITY_REPO/utils/verify_unity_archives.py" \
  "$UNITY_REPO/worlds/unity_simulation.tar.gz" \
  "$UNITY_REPO/worlds/unity_simulation_only.tar.gz"
./scripts/build_workspace.sh unity
source robotnik_benchmark_unity_ws/install/setup.bash
```

Launch Unity with the existing ROS 2 launch integration. If the Unity source
project is published later, it should be added as a separate submodule with
its Unity Editor version and Player-generation procedure documented here.

## 7. Running each simulator

The normal entry point is the common campaign script. It selects the same
categories for every backend and applies the backend-specific launch adapter.

### Gazebo Harmonic

```bash
source robotnik_benchmark_gazebo_ws/install/setup.bash
./scripts/execute/run_simulator_campaign.sh --simulator gazebo_harmonic \
  --iterations 3 --iteration-time 60 --monitor-ros
```

Gazebo uses `robotnik_gazebo_ignition` and the configured world/spawn launch
files. Use `--headless` for the headless categories only or `--gui` for GUI
categories only.

### Webots

```bash
source robotnik_benchmark_webots_ws/install/setup.bash
./scripts/execute/run_simulator_campaign.sh --simulator webots \
  --iterations 3 --iteration-time 60 --monitor-ros
```

Webots uses its world files and `robotnik_webots` launch integration. Ensure
the Webots runtime is installed and discoverable before launching.

### NVIDIA Isaac Sim

```bash
source robotnik_benchmark_isaac_ws/install/setup.bash
./scripts/execute/run_simulator_campaign.sh --simulator isaac_sim \
  --headless --iterations 3 --iteration-time 60 --monitor-ros
```

Isaac Sim must be installed separately and its environment must be available
before the ROS 2 wrapper is launched. Isaac receives USD world files and has
a longer shutdown grace period automatically configured by the campaign
script.

### MuJoCo

```bash
source robotnik_benchmark_mujoco_ws/install/setup.bash
./scripts/execute/run_simulator_campaign.sh --simulator mujoco \
  --iterations 3 --iteration-time 60 --monitor-ros
```

MuJoCo uses `rbwatcher_benchmark.launch.py` and receives the common world,
robot-count, GUI, RViz, and render-FPS parameters through the ROS 2 launch
file.

### O3DE

Complete the O3DE preparation above, then run:

```bash
source robotnik_benchmark_o3de_ws/install/setup.bash
./scripts/execute/run_simulator_campaign.sh --simulator o3de \
  --iterations 3 --iteration-time 60 --monitor-ros
```

O3DE requires the generated Editor, asset, and GameLauncher targets before
the ROS wrapper can start. Its level names are mapped from the common world
names by `benchmark_config.yaml`.

### Unity

Complete the Unity archive verification above, then run:

```bash
source robotnik_benchmark_unity_ws/install/setup.bash
./scripts/execute/run_simulator_campaign.sh --simulator unity \
  --iterations 3 --iteration-time 60 --monitor-ros
```

Unity launches a distributed Player through the existing ROS 2 integration.
The archive and transport checks are therefore part of setup, not a second
source build of a Unity project.

### One category or all simulators

To inspect the selected categories without launching a simulator:

```bash
./scripts/execute/run_simulator_campaign.sh --simulator gazebo_harmonic --list-only
```

To run one exact category directly:

```bash
source /opt/ros/jazzy/setup.bash
source robotnik_benchmark_gazebo_ws/install/setup.bash
python3 scripts/execute/run_benchmark.py gazebo_harmonic \
  --category one_robot_empty_world_headless \
  --iterations 1 --iteration_time 10 --warmup-time 5 --monitor-ros
```

To run the complete cross-simulator campaign:

```bash
./scripts/execute/run_all_simulators.sh --iterations 3 --iteration-time 60
```

## 8. Reports and validation

Each run writes performance CSV files, metadata JSON, and optional ROS topic
CSV files below `benchmarks/`. Generate Markdown summaries with:

```bash
python3 scripts/report/performance_report.py \
  --benchmarks-dir benchmarks --output performance_report.md
python3 scripts/report/ros_report.py \
  --benchmarks-dir benchmarks --output ros_report.md
```

The generated reports contain grouped summaries by simulator, category, and
render-FPS cap. Keep raw CSV and JSON data with the report when results need
to be audited. Benchmark outputs, generated simulator projects, and all
`build/`, `install/`, and `log/` directories are ignored by Git.

Validate the repository before sharing results:

```bash
./scripts/validate_workspace.sh
python3 -m pytest -q scripts/tests
```

The validation checks submodule commits, expected packages, the 24-category
configuration, and repository hygiene. It does not replace a real simulator
run; each backend should be smoke-tested on the target machine.

## 9. Updating pinned dependencies

Submodules are pinned for reproducibility. To update one dependency, check
out the intended branch inside that submodule, test the complete affected
workspace, record the new commit in the superproject, and update this README
if the setup or compatibility requirements changed:

```bash
git -C robotnik_benchmark_gazebo_ws/src/robotnik/robotnik_description \
  fetch origin benchmarking-compatibility
git -C robotnik_benchmark_gazebo_ws/src/robotnik/robotnik_description \
  checkout <tested-commit>
git add robotnik_benchmark_gazebo_ws/src/robotnik/robotnik_description
git commit -m "Update pinned robotnik_description dependency"
git push origin review/jazzy-2026
```

Do not replace a pinned commit with a floating branch reference. The branch is
useful for selecting future updates; the commit is what makes a checkout
reproducible.

## 10. Conclusion and contribution

This repository provides a common, inspectable basis for comparing robotics
simulators through ROS 2. Its value grows when scenarios, sensor mappings,
launch adapters, and measurements are kept aligned across backends.

Contributions are welcome: improve a simulator adapter, add a validated
scenario, clarify a limitation, improve the report, or contribute hardware
and reproducibility notes. Please include the exact host, simulator version,
submodule commits, configuration, and generated report data needed to repeat
the result. Small, documented improvements help keep the benchmark useful to
the whole robotics community.
