#bin/bash

source /opt/ros/humble/setup.bash

cd "$HOME/isaacsim"
./python.sh "/home/robotnik/workspaces/PI_simulation_ws/src/robotnik_sim_benchmark/simulations/isaac_sim/utils/isaac_sim_launcher_headless.py"
