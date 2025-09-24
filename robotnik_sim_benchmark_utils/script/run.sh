#!/bin/bash
set -euo pipefail

# Function to run a command in a detached screen session
run_screen() {
  echo "Starting screen session: $1"
  screen -dmS "$1" bash -c "$2"
}

# Send stop signal to all screens
stop_screens() {
  # List of screen sessions to stop
  local active_screens=$(screen -ls | grep -oP '\d+\.\w+' || true)
  if [ -z "$active_screens" ]; then
    echo "No active screen sessions found."
    return
  fi
  for session in "$@"; do
    if ! echo "$active_screens" | grep -q "^$session$"; then
      echo "Screen session $session not found. Skipping."
      continue
    fi
    echo "Stopping screen session: $session"
    screen -S "$session" -p 0 -X stuff "exit$(printf \\r)"
  done
}

# Kill gz processes
kill_gz_processes() {
  local gz_pids=$(pgrep -f gzserver || true)
  if [ -n "$gz_pids" ]; then
    kill -9 $gz_pids
  fi
}

stop_screens "stats" "world" "robot"
sleep 2
kill_gz_processes
sleep 1

run_screen "stats" "ros2 run robotnik_sim_benchmark_utils benchmark_node --ros-args -p topics:="[/tf,/robot/front_rgbd_camera/color/image_raw]" -p best_effort:=true -p window_size:=512 -p csv_dir:=/tmp/stats -p run_tag:=test"
run_screen "world" "ros2 launch robotnik_gazebo_ignition spawn_world.launch.py world:=lightweight_scene"
run_screen "robot" "ros2 launch robotnik_gazebo_ignition spawn_robot.launch.py robot:=rbwatcher"
