#!/usr/bin/env bash
# Launch an O3DE world and spawn multiple robots. Properly forwards SIGINT.

set -Eeuo pipefail
set -m  # enable job control so each background job gets its own process group

print_usage() {
    echo "Usage: $0 [<world>] [num_robots] [robot_model] [run_rviz] [run_headless]"
    echo ""
    echo "Arguments:"
    echo "  [world]        : Name of the O3DE world to launch (default: empty)"
    echo "  [num_robots]   : Number of robots to spawn (default: 1)"
    echo "  [robot_model]  : Robot model to use (default: rbwatcher)"
    echo "  [run_rviz]     : true/false to launch RViz (default: true)"
    echo "  [run_headless] : true/false to run O3DE in headless mode (default: false)"
    echo ""
    echo "Example:"
    echo "  $0 harmonic 5 rbwatcher true"
}

if [[ $# -eq 1 ]] && ([[ "$1" == "-h" ]] || [[ "$1" == "--help" ]]); then
    print_usage
    exit 0
fi

WORLD_NAME="${1:-empty}"
NUM_ROBOTS="${2:-1}"
ROBOT_MODEL="${3:-rbwatcher}"
RUN_RVIZ="${4:-true}"
RUN_HEADLESS="${5:-false}"

world_pid=""
robots_pid=""

forward_sigint() {
    # send SIGINT to each job's process group
    echo "Forwarding SIGINT to child processes..."
    [[ -n "${world_pid}"  ]]  && kill -INT "-${world_pid}"  2>/dev/null || true
    [[ -n "${robots_pid}" ]]  && kill -INT "-${robots_pid}" 2>/dev/null || true
}

cleanup() {
    # on TERM/EXIT, terminate children cleanly, then hard-kill if needed
    echo "Cleaning up..."
    [[ -n "${robots_pid}" ]] && kill -TERM "-${robots_pid}" 2>/dev/null || true
    [[ -n "${world_pid}"  ]] && kill -TERM "-${world_pid}"  2>/dev/null || true
    sleep 1
    [[ -n "${robots_pid}" ]] && kill -KILL "-${robots_pid}" 2>/dev/null || true
    [[ -n "${world_pid}"  ]] && kill -KILL "-${world_pid}"  2>/dev/null || true
}

trap forward_sigint INT
trap cleanup TERM EXIT

echo "Launching O3DE world: ${WORLD_NAME}"
ros2 launch robotnik_o3de spawn_world.launch.py \
  "world:=${WORLD_NAME}" \
  gui:=$([[ "${RUN_HEADLESS,,}" == "true" || "$RUN_HEADLESS" == "1" ]] && echo false || echo true) &
world_pid=$!

# Launch multiple robots
MULTIPLE_SH="$(ros2 pkg prefix robotnik_o3de)/share/robotnik_o3de/scripts/multiple.sh"
if [[ ! -x "${MULTIPLE_SH}" ]]; then
  echo "Error: ${MULTIPLE_SH} not found or not executable." >&2
  kill -TERM "-${world_pid}" 2>/dev/null || true
  exit 1
fi

echo "Spawning multiple robots..."
"${MULTIPLE_SH}" "${NUM_ROBOTS}" "${ROBOT_MODEL}" 1.0 1.0 0.0 0.0 0.05 0.0 -- "run_rviz:=${RUN_RVIZ}" &
robots_pid=$!

# Wait for both jobs and propagate failure
status=0
wait "${world_pid}"  || status=$?
wait "${robots_pid}" || status=$(( status != 0 ? status : $? ))
exit "${status}"
