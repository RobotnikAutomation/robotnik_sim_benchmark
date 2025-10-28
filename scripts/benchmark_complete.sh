#bin/bash

pushd "$(dirname "${BASH_SOURCE[0]}")/.." > /dev/null
ROOT_DIR="$(pwd)"
echo $ROOT_DIR

ROS_SOURCE="/opt/ros/humble/setup.bash"
GAZEBO_SOURCE="~/workspaces/robotnik_gazebo_harmonic_ws/install/setup.bash"
WEBOTS_SOURCE="~/workspaces/robotnik_webots_ws/install/setup.bash"
ISAAC_SIM_SOURCE="~/workspaces/robotnik_isaac_ws/install/setup.bash"
UNITY_SOURCE="~/workspaces/robotnik_unity_ws/install/setup.bash"
O3DE_SOURCE="4/workspaces/robotnik_o3de_ws/install/setup.bash"

source $ROS_SOURCE
source $GAZEBO_SOURCE
./scripts/run_all_benchmarks.sh -s gazebo_harmonic

sleep 10

source $ROS_SOURCE
source $WEBOTS_SOURCE
./scripts/run_all_benchmarks.sh -s webots

sleep 10

source $ROS_SOURCE
source $ISAAC_SIM_SOURCE
./scripts/run_all_benchmarks.sh -s isaac_sim

sleep 10

source $ROS_SOURCE
source $UNITY_SOURCE
./scripts/run_all_benchmarks.sh -s unity

sleep 10

source $ROS_SOURCE
source $O3DE_SOURCE
./scripts/run_all_benchmarks.sh -s o3de
