# Repositories and pinned revisions

The benchmark repository pins every simulator dependency to a commit. The
branch column records the branch from which that commit was selected; it is
metadata for future updates and is not used to make a checkout floating.

| Workspace path | Repository | Source | Branch | Pinned commit |
| --- | --- | --- | --- | --- |
| `robotnik_benchmark_gazebo_ws/src/robotnik/robotnik_common` | `robotnik_common` | Robotnik | detached source commit | `0153704` |
| `robotnik_benchmark_gazebo_ws/src/robotnik/robotnik_description` | `robotnik_description` | Robotnik | `benchmarking-compatibility` | `4bc7342` |
| `robotnik_benchmark_gazebo_ws/src/robotnik/robotnik_interfaces` | `robotnik_interfaces` | Robotnik | default source revision | `ee903ab` |
| `robotnik_benchmark_gazebo_ws/src/robotnik/robotnik_moveit_configs` | `robotnik_moveit_configs` | Robotnik | default source revision | `45bc509` |
| `robotnik_benchmark_gazebo_ws/src/robotnik/robotnik_sensors` | `robotnik_sensors` | `jlgalanRB` fork | `benchmarking-compatibility` | `9170657` |
| `robotnik_benchmark_gazebo_ws/src/robotnik/robotnik_simulation` | `robotnik_simulation` | `jlgalanRB` fork | `benchmarking-compatibility` | `df3ef1e` |
| `robotnik_benchmark_gazebo_ws/src/robotnik/robotnik_teleop_panel` | `teleop_panel` | Robotnik | default source revision | `21d3e53` |
| `robotnik_benchmark_webots_ws/src/robotnik_common` | `robotnik_common` | Robotnik | `jazzy-devel` | `0153704` |
| `robotnik_benchmark_webots_ws/src/robotnik_webots` | `robotnik_webots` | `jlgalanRB` fork | `benchmarking-compatibility` | `c40ee27` |
| `robotnik_benchmark_isaac_ws/src/robotnik_isaac` | `robotnik_isaac` | `jlgalanRB` fork | `benchmarking-compatibility` | `62ee1c3` |
| `robotnik_benchmark_mujoco_ws/src/mujoco_ros2_control` | `mujoco_ros2_control` | `jlgalanRB` fork | `benchmarking-compatibility` | `55a8626` |
| `robotnik_benchmark_mujoco_ws/src/robotnik_mujoco` | `robotnik_mujoco` | `jlgalanRB` fork | `benchmarking-compatibility` | `7a4b534` |
| `robotnik_benchmark_o3de_ws/src/o3de-extras` | `o3de-extras` | `jlgalanRB` fork | `benchmarking-compatibility` | `f1eadf6` |
| `robotnik_benchmark_o3de_ws/src/robotnik_common` | `robotnik_common` | Robotnik | `jazzy-devel` | `0153704` |
| `robotnik_benchmark_o3de_ws/src/robotnik_o3de` | `robotnik_o3de` | `jlgalanRB` fork | `benchmarking-compatibility` | `3084d85` |
| `robotnik_benchmark_unity_ws/src/ROS-TCP-Endpoint` | `ROS-TCP-Endpoint` | Unity Technologies | `main-ros2` | `54c1a64` |
| `robotnik_benchmark_unity_ws/src/robotnik_unity` | `robotnik_unity` | `jlgalanRB` fork | `benchmarking-compatibility` | `b1e7fd9` |

Robotnik repositories use `https://github.com/RobotnikAutomation/<repo>.git`.
Personal forks use `https://github.com/jlgalanRB/<repo>.git`. The Unity
endpoint uses its official Unity Technologies repository.

To update a dependency, checkout and test the intended branch in the
submodule, then record the new gitlink in the parent repository and update this
table in the same change.
