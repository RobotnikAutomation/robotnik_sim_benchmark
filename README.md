# Robotnik simulation benchmark

Main repository for running and comparing the Gazebo Harmonic, Webots, Isaac
Sim, MuJoCo, O3DE, and Unity benchmarks. Each simulator keeps an independent
workspace, and its dependencies are pinned as Git submodules.

## 1. Requirements

The workflow is validated on Ubuntu with ROS 2 Jazzy. Install at least:

```bash
sudo apt update
sudo apt install git git-lfs build-essential cmake ninja-build python3-pip
sudo apt install ros-jazzy-desktop python3-colcon-common-extensions
git lfs install
```

Each simulator may have additional requirements. Isaac Sim requires its own
installation and runtime environment; MuJoCo requires its dependencies and
license/configuration where applicable; O3DE requires a compatible O3DE
installation; and Unity requires a Linux host compatible with the included
Players.

## 2. Clone and prepare the workspace

Clone the reproducible branch and initialise all direct submodules:

```bash
git clone -b review/jazzy-2026 \
  https://github.com/RobotnikAutomation/robotnik_sim_benchmark.git
cd robotnik_sim_benchmark
./scripts/setup_workspace.sh
```

To also download assets managed by Git LFS:

```bash
./scripts/setup_workspace.sh --pull-lfs
```

The resulting layout is:

```text
robotnik_sim_benchmark/
├── benchmarks/                         # Local results, not versioned
├── config/                             # Matrix and canonical sensor profile
├── scripts/                            # Setup, build, and execution tools
├── robotnik_benchmark_gazebo_ws/src/robotnik/
├── robotnik_benchmark_webots_ws/src/
├── robotnik_benchmark_isaac_ws/src/
├── robotnik_benchmark_mujoco_ws/src/
├── robotnik_benchmark_o3de_ws/src/
└── robotnik_benchmark_unity_ws/src/
```

The source repository and exact pinned commit for every submodule are listed in
[`docs/repositories.md`](docs/repositories.md). Commits are pinned so that two
clones produce the same environment; the branch shown there only records the
source used to select each commit.

The Isaac repository contains an additional nested submodule named
`robotnik_isaac_ros2_control`. It is not required by this benchmark, so the
bootstrap script initialises only the direct submodules declared by this
repository.

## 3. Build the workspaces

The build script keeps one isolated workspace per simulator:

```bash
./scripts/build_workspace.sh gazebo_harmonic
./scripts/build_workspace.sh webots
./scripts/build_workspace.sh isaac_sim
./scripts/build_workspace.sh mujoco
./scripts/build_workspace.sh o3de
./scripts/build_workspace.sh unity
```

To build every simulator workspace:

```bash
./scripts/build_workspace.sh all
```

Each invocation loads only `/opt/ros/${ROS_DISTRO:-jazzy}/setup.bash` and runs
`colcon build --symlink-install` inside its own workspace. Do not reuse
`build`, `install`, or `log` directories between simulators.

## 4. O3DE: generate the project locally

O3DE binaries and generated project directories are not stored in Git. They are
generated locally from `robotnik_o3de` and `o3de-extras`.

Set the required paths:

```bash
export O3DE_HOME=/opt/O3DE/26.05
export O3DE_EXTRAS_HOME=$PWD/robotnik_benchmark_o3de_ws/src/o3de-extras
export PROJECT_PATH=$PWD/robotnik_benchmark_o3de_ws/src/robotnik_o3de/project/robotnik_roscon25
```

Download the assets and register the gems and templates:

```bash
git -C "$O3DE_EXTRAS_HOME" lfs pull

$O3DE_HOME/scripts/o3de.sh register \
  --all-gems-path "$O3DE_EXTRAS_HOME/Gems"
$O3DE_HOME/scripts/o3de.sh register \
  --all-templates-path "$O3DE_EXTRAS_HOME/Templates"
```

Generate and build the project:

```bash
cd "$PROJECT_PATH"
cmake -B build/linux \
  -G "Ninja Multi-Config" \
  -DLY_DISABLE_TEST_MODULES=ON \
  -DCMAKE_EXPORT_COMPILE_COMMANDS=ON \
  -DLY_STRIP_DEBUG_SYMBOLS=ON

cmake --build build/linux \
  --config profile \
  --target robotnik_roscon25 Editor \
  robotnik_roscon25.Assets robotnik_roscon25.GameLauncher
```

Build the ROS 2 wrapper with:

```bash
./scripts/build_workspace.sh o3de
source robotnik_benchmark_o3de_ws/install/setup.bash
ros2 launch robotnik_o3de spawn_world.launch.py
```

The generated launcher can also be run directly from
`build/linux/bin/profile`. CMake and O3DE-generated directories must not be
added to the repository.

## 5. Unity: build the wrapper and use the Players

The `robotnik_unity` submodule contains the Unity Players as compressed
archives and the ROS 2 `unity_sim` package. The complete Unity Editor source
project is not currently published, so this repository does not regenerate the
Player.

Download and validate the LFS archives:

```bash
git -C robotnik_benchmark_unity_ws/src/robotnik_unity lfs pull
python3 robotnik_benchmark_unity_ws/src/robotnik_unity/utils/verify_unity_archives.py \
  robotnik_benchmark_unity_ws/src/robotnik_unity/worlds/unity_simulation.tar.gz \
  robotnik_benchmark_unity_ws/src/robotnik_unity/worlds/unity_simulation_only.tar.gz
```

Build the ROS endpoint and Unity wrapper:

```bash
./scripts/build_workspace.sh unity
source robotnik_benchmark_unity_ws/install/setup.bash
```

The launch files select the Player for `empty_world` or `simple_world` and
support GUI/headless execution, robot count, RViz, and an FPS limit. If the
Unity source project is published in the future, it will be added as a separate
submodule together with its exact Unity Editor version.

## 6. Run benchmarks

List the available benchmark categories first:

```bash
python3 scripts/validate/validate_config.py --list-categories
```

Example using Gazebo:

```bash
source /opt/ros/jazzy/setup.bash
source robotnik_benchmark_gazebo_ws/install/setup.bash

python3 scripts/execute/run_benchmark.py gazebo_harmonic \
  --category one_robot_empty_world_headless \
  --iterations 1 --iteration_time 10 --warmup-time 5 \
  --startup_timeout 120 --max_retries 0 --monitor-ros
```

Replace `gazebo_harmonic` and the sourced `setup.bash` with the selected
simulator. To run a complete campaign for one simulator:

```bash
source /opt/ros/jazzy/setup.bash
source robotnik_benchmark_<simulator>_ws/install/setup.bash
./scripts/execute/run_simulator_campaign.sh --simulator <simulator>
```

Results are written to `benchmarks/<simulator>/` and are not versioned.

## 7. Validation

```bash
./scripts/validate_workspace.sh
python3 -m pytest -q scripts/tests
python3 -m compileall -q scripts
```

Validation must confirm 24 categories, direct submodules initialised at their
pinned commits, and all workspace directories present. The unit tests do not
launch real simulators; complete acceptance also requires one minimal run on
each backend.

## 8. Update a dependency

Submodules do not automatically follow a remote branch. To update one:

```bash
cd robotnik_benchmark_webots_ws/src/robotnik_webots
git fetch personal benchmarking-compatibility
git checkout benchmarking-compatibility
git pull --ff-only personal benchmarking-compatibility
cd ../../../../
git add robotnik_benchmark_webots_ws/src/robotnik_webots
```

After testing the workspace, update the commit and the table in
`docs/repositories.md` in the same change to the main repository.

## 9. Publish changes

The integration branch is `review/jazzy-2026`; it includes the
`benchmarking-compatibility` base. Changes to the main repository are published
directly to that branch; no Pull Request is required to reproduce or run the
benchmarks.
