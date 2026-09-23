#!/usr/bin/env bash
set -Eeuo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"

ROS_SOURCE="${ROS_SOURCE:-/opt/ros/jazzy/setup.bash}"
WORKSPACE_ROOT="${WORKSPACE_ROOT:-${SCRIPT_DIR}/../../../..}"
BENCHMARK_SOURCE="${BENCHMARK_SOURCE:-${WORKSPACE_ROOT}/benchmark_ws/install/setup.bash}"
GAZEBO_SOURCE="${GAZEBO_SOURCE:-${WORKSPACE_ROOT}/robotnik_benchmark_gazebo_ws/install/setup.bash}"
WEBOTS_SOURCE="${WEBOTS_SOURCE:-${WORKSPACE_ROOT}/robotnik_benchmark_webots_ws/install/setup.bash}"
UNITY_SOURCE="${UNITY_SOURCE:-${WORKSPACE_ROOT}/unity_ws/install/setup.bash}"
O3DE_SOURCE="${O3DE_SOURCE:-${WORKSPACE_ROOT}/o3de_ws/install/setup.bash}"
MUJOCO_SOURCE="${MUJOCO_SOURCE:-${WORKSPACE_ROOT}/mujoco_ws/install/setup.bash}"

SIMULATOR_COOLDOWN=60
BENCHMARK_ARGS=()
SHOW_HELP=false
while (($#)); do
  case "$1" in
    --simulator-cooldown)
      [[ "${2:-}" =~ ^[0-9]+([.][0-9]+)?$ ]] || {
        echo "Invalid simulator cooldown" >&2
        exit 2
      }
      SIMULATOR_COOLDOWN="$2"
      shift 2
      ;;
    -h|--help)
      SHOW_HELP=true
      shift
      ;;
    *)
      BENCHMARK_ARGS+=("$1")
      shift
      ;;
  esac
done

if [[ "${SHOW_HELP}" == true ]]; then
  "${SCRIPT_DIR}/run_simulator_campaign.sh" --help
  printf '      --simulator-cooldown SEC  Pause between simulators (default: 60)\n'
  exit 0
fi

run_simulator() {
  local simulator="$1"
  shift

  local -a workspace_setups=()
  while [[ "${1:-}" != "--" ]]; do
    [[ -n "${1:-}" ]] || {
      echo "Missing -- separator before benchmark options for ${simulator}" >&2
      return 2
    }
    workspace_setups+=("$1")
    shift
  done
  shift

  printf '\n%s\n' '================================================================================'
  printf 'Starting simulator: %s\n' "${simulator}"
  printf '%s\n' '================================================================================'

  [[ -r "${ROS_SOURCE}" ]] || { echo "ROS setup not readable: ${ROS_SOURCE}" >&2; return 1; }
  local workspace_setup
  for workspace_setup in "${workspace_setups[@]}"; do
    [[ -r "${workspace_setup}" ]] || {
      echo "Workspace setup not readable for ${simulator}: ${workspace_setup}" >&2
      return 1
    }
  done

  printf 'Environment: clean base + %s\n' "${workspace_setups[*]}"

  # A subshell alone is insufficient: it inherits any ROS overlays, Python
  # paths and shared-library paths from the terminal that invoked this script.
  # Start a new Bash with an allow-list instead.  The ROS environment is then
  # built solely from the setup files declared for this simulator.
  #
  # Display/session variables are retained so GUI benchmark categories can use
  # the caller's desktop. ROS domain settings are explicit user settings, not
  # workspace overlays, so they are retained as well.
  local -a clean_environment=(
    "HOME=${HOME:?HOME must be set to run benchmarks}"
    "USER=${USER:-}"
    "LOGNAME=${LOGNAME:-}"
    "LANG=${LANG:-C.UTF-8}"
    "TERM=${TERM:-dumb}"
  )
  local environment_variable
  for environment_variable in \
    DISPLAY WAYLAND_DISPLAY XAUTHORITY XDG_RUNTIME_DIR \
    DBUS_SESSION_BUS_ADDRESS XDG_CURRENT_DESKTOP XDG_SESSION_TYPE \
    XDG_DATA_DIRS XDG_DATA_HOME \
    ROS_DOMAIN_ID ROS_LOCALHOST_ONLY ROS_LOG_DIR ROS_HOME \
    CUDA_VISIBLE_DEVICES NVIDIA_VISIBLE_DEVICES \
    ISAAC_SIM_ROOT ISAAC_BENCHMARK_GPU \
    ROS2_WEBOTS_HOME WEBOTS_HOME \
    __NV_PRIME_RENDER_OFFLOAD __GLX_VENDOR_LIBRARY_NAME; do
    if [[ -v "${environment_variable}" ]]; then
      clean_environment+=("${environment_variable}=${!environment_variable}")
    fi
  done

  /usr/bin/env -i \
    "${clean_environment[@]}" \
    "PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin" \
    /usr/bin/bash --noprofile --norc -c '
      set -Eeuo pipefail

      ros_source="$1"
      simulator="$2"
      runner="$3"
      shift 3

      # Colcon-generated setup files may reference unset optional variables.
      set +u
      # shellcheck disable=SC1090
      source "${ros_source}"
      while [[ "$1" != "--" ]]; do
        # shellcheck disable=SC1090
        source "$1"
        shift
      done
      set -u
      shift

      # Verify the packages that identify this simulator after the complete
      # source chain is in place.
      case "${simulator}" in
        gazebo_harmonic) required_packages=(robotnik_gazebo_ignition) ;;
        webots) required_packages=(robotnik_webots) ;;
        isaac_sim) required_packages=(isaac_sim) ;;
        unity) required_packages=(robotnik_gazebo_ignition unity_sim) ;;
        o3de) required_packages=(robotnik_gazebo_ignition robotnik_o3de) ;;
        mujoco) required_packages=(robotnik_mujoco mujoco_ros2_control) ;;
      esac
      for required_package in "${required_packages[@]}"; do
        ros2 pkg prefix "${required_package}" >/dev/null
      done
      printf "Environment verified: packages=%s\\n" "${required_packages[*]}"

      exec "${runner}" --simulator "${simulator}" "$@"
    ' bash \
    "${ROS_SOURCE}" "${simulator}" "${SCRIPT_DIR}/run_simulator_campaign.sh" \
    "${workspace_setups[@]}" -- "$@"

  printf 'Finished simulator: %s\n' "${simulator}"
  if [[ "${simulator}" != "mujoco" && "${SIMULATOR_COOLDOWN}" != "0" ]]; then
    printf 'Next simulator in %s seconds...\n' "${SIMULATOR_COOLDOWN}"
    sleep "${SIMULATOR_COOLDOWN}"
  fi
}

run_simulator gazebo_harmonic \
  "${BENCHMARK_SOURCE}" "${GAZEBO_SOURCE}" -- "${BENCHMARK_ARGS[@]}"
run_simulator webots \
  "${BENCHMARK_SOURCE}" "${WEBOTS_SOURCE}" -- "${BENCHMARK_ARGS[@]}"
run_simulator isaac_sim \
  "${BENCHMARK_SOURCE}" -- "${BENCHMARK_ARGS[@]}"
run_simulator unity \
  "${BENCHMARK_SOURCE}" "${GAZEBO_SOURCE}" "${UNITY_SOURCE}" -- "${BENCHMARK_ARGS[@]}"
run_simulator o3de \
  "${BENCHMARK_SOURCE}" "${GAZEBO_SOURCE}" "${O3DE_SOURCE}" -- "${BENCHMARK_ARGS[@]}"
run_simulator mujoco \
  "${MUJOCO_SOURCE}" "${BENCHMARK_SOURCE}" -- "${BENCHMARK_ARGS[@]}"
