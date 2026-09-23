# Robotnik simulation benchmark

Runner and reporting tools shared by the Robotnik simulator benchmarks.  Simulator
implementations are deliberately kept in independent workspaces; this repository
contains no simulator package, game project, world asset, or compatibility wrapper.

## Layout

```text
repos_structure/
├── robotnik_sim_benchmark/             # this repository
├── robotnik_benchmark_gazebo_ws/
├── robotnik_benchmark_webots_ws/
├── robotnik_benchmark_isaac_ws/
├── robotnik_benchmark_mujoco_ws/
├── robotnik_benchmark_o3de_ws/
└── robotnik_benchmark_unity_ws/
```

Each simulator is selected by sourcing only its own workspace before running a
benchmark.  The compact configuration in `config/benchmark_config.yaml` expands
the common matrix of 1/2/3 robots, empty/simple worlds, GUI/headless and RViz into
the 24 stable public category names.

## Build the simulator workspaces

Build the workspace for the simulator under test using its documented dependency
setup.  The benchmark runner expects these package names:

| Simulator | Workspace | Launch packages |
| --- | --- | --- |
| Gazebo Harmonic | `robotnik_benchmark_gazebo_ws` | `robotnik_gazebo_ignition` |
| Webots | `robotnik_benchmark_webots_ws` | `robotnik_webots` |
| Isaac Sim | `robotnik_benchmark_isaac_ws` | `isaac_sim` |
| MuJoCo | `robotnik_benchmark_mujoco_ws` | `robotnik_mujoco` |
| O3DE | `robotnik_benchmark_o3de_ws` | `robotnik_o3de` |
| Unity | `robotnik_benchmark_unity_ws` | `unity_sim` |

Gazebo, Webots and O3DE use their installed `scripts/multiple.sh` to launch
robot instances.  The benchmark runner starts that process directly together with
the backend's `spawn_world.launch.py`; there are no wrappers under
`simulations/`.

## Run a benchmark

Example for Gazebo:

```bash
cd ~/jlgalan_dev/repos_structure/robotnik_sim_benchmark
source /opt/ros/jazzy/setup.bash
source ../robotnik_benchmark_gazebo_ws/install/setup.bash

python3 scripts/execute/run_benchmark.py gazebo_harmonic \
  --category one_robot_empty_world_headless \
  --iterations 1 --iteration_time 10 --warmup-time 5 \
  --startup_timeout 120 --max_retries 0 --monitor-ros
```

Replace `gazebo_harmonic` and the sourced workspace with the selected simulator.
Use `--list-categories` to inspect the public category names:

```bash
python3 scripts/validate/validate_config.py --list-categories
```

Results are written below `benchmarks/<simulator>/` and are ignored by Git.

## Validation

No real simulator is launched by the unit suite.

```bash
python3 scripts/validate/validate_config.py --category-count
python3 -m pytest -q scripts/tests
python3 -m compileall -q scripts
```

The category count must be `24`; all tests must pass.
