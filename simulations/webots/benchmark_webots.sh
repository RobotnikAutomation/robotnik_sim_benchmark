#!/usr/bin/env bash
# bringup_multiple_harmonic.sh
set -Eeuo pipefail

print_usage() {
    echo "Usage: $0 [<world>] [num_robots] [robot_model] [run_rviz]"
    echo ""
    echo "Arguments:"
    echo "  [world]        : Name of the Gazebo world to launch (default: empty)"
    echo "  [num_robots]   : Number of robots to spawn (default: 1)"
    echo "  [robot_model]  : Robot model to use (default: rbwatcher)"
    echo "  [run_rviz]     : true/false to launch RViz (default: true)"
    echo ""
    echo "Example:"
    echo "  $0 harmonic 5 rbwatcher true    "
}

if [[ $# -eq 1 ]] && ([[ "$1" == "-h" ]] || [[ "$1" == "--help" ]]); then
    print_usage
    exit 0
fi

WORLD_NAME="${1:-empty}"
NUM_ROBOTS="${2:-1}"
ROBOT_MODEL="${3:-rbwatcher}"
RUN_RVIZ="${4:-true}"

echo "Launching Webots world: $WORLD_NAME"

ros2 launch robotnik_webots spawn_world.launch.py world:="$WORLD_NAME" &
world_pid=$!

# Wait for the world to be up (adjust as needed)

# Launch multiple robots using the provided script
SCRIPT_DIR="$(dirname "$0")"
MULTIPLE_SH="$(ros2 pkg prefix robotnik_webots)/share/robotnik_webots/scripts/multiple.sh"

if [ ! -x "$MULTIPLE_SH" ]; then
  echo "Error: $MULTIPLE_SH not found or not executable."
  kill $world_pid
  exit 1
fi

echo "Spawning multiple robots..."
# You can adjust the arguments as needed, here using defaults (3 rbwatcher robots)

"$MULTIPLE_SH" "$NUM_ROBOTS" "$ROBOT_MODEL" 1.0 1.0 0.0 0.0 0.05 0.0 -- run_rviz:="$RUN_RVIZ" &
robots_pid=$!

# Wait for both processes
wait $world_pid
wait $robots_pid
