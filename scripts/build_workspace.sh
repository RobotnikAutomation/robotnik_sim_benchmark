#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ROS_DISTRO="${ROS_DISTRO:-jazzy}"
ROS_SETUP="/opt/ros/${ROS_DISTRO}/setup.bash"

usage() {
  cat <<'EOF'
Usage: scripts/build_workspace.sh {gazebo_harmonic|webots|isaac_sim|mujoco|o3de|unity|all}

Build one simulator workspace, or all ROS workspaces in dependency order.
O3DE requires its project to be generated and built separately with CMake;
see README.md.
Unity Player archives are validated against Unity Editor 6000.1.14f1.

The 'o3de' target builds only the O3DE ROS 2 wrapper packages.
EOF
}

simulator="${1:-}"
case "${simulator}" in
  gazebo_harmonic|webots|isaac_sim|mujoco|o3de|unity|all) ;;
  -h|--help|'') usage; exit 0 ;;
  *) echo "Unknown simulator: ${simulator}" >&2; usage >&2; exit 2 ;;
esac

[[ -r "${ROS_SETUP}" ]] || {
  echo "ROS setup not found: ${ROS_SETUP}" >&2
  exit 1
}
# shellcheck source=/dev/null
# ROS 2 setup files may read optional variables before defining them. Keep
# nounset enabled for this script, but disable it while sourcing the setup.
set +u
source "${ROS_SETUP}"
set -u

require_command() {
  command -v "$1" >/dev/null || {
    echo "Required command not found: $1" >&2
    exit 1
  }
}
require_command colcon

build_ros_workspace() {
  (
    local workspace="$1"
    shift
    echo "==> Building ${workspace}"
    cd "${ROOT_DIR}/${workspace}"
    colcon build --symlink-install "$@"
  )
}

build_o3de_ros_workspace() {
  # o3de-extras also contains standalone sample projects and Gems. They are
  # built by the O3DE project, not as ROS packages. Restrict colcon to the
  # ROS 2 wrapper packages to avoid configuring unrelated O3DE projects.
  build_ros_workspace robotnik_benchmark_o3de_ws \
    --base-paths src/robotnik_common src/robotnik_o3de
}

build_o3de() {
  build_o3de_ros_workspace
}

build_unity() {
  local unity_repo="${ROOT_DIR}/robotnik_benchmark_unity_ws/src/robotnik_unity"
  local archive
  echo "Unity Player archives must be built with Unity Editor 6000.1.14f1"
  git -C "${unity_repo}" lfs pull
  for archive in \
    "${unity_repo}/worlds/unity_simulation.tar.gz" \
    "${unity_repo}/worlds/unity_simulation_only.tar.gz"; do
    [[ -f "${archive}" ]] || {
      echo "Missing Unity Player archive: ${archive}" >&2
      echo "The pinned robotnik_unity commit does not contain the Player archives." >&2
      echo "Recover the Unity source project and generate the Player with Unity 6000.1.14f1 first." >&2
      exit 1
    }
  done
  python3 "${unity_repo}/utils/verify_unity_archives.py" \
    "${unity_repo}/worlds/unity_simulation.tar.gz" \
    "${unity_repo}/worlds/unity_simulation_only.tar.gz"
  build_ros_workspace robotnik_benchmark_unity_ws
}

build_one() {
  case "$1" in
    gazebo_harmonic) build_ros_workspace robotnik_benchmark_gazebo_ws ;;
    webots) build_ros_workspace robotnik_benchmark_webots_ws ;;
    isaac_sim) build_ros_workspace robotnik_benchmark_isaac_ws ;;
    mujoco) build_ros_workspace robotnik_benchmark_mujoco_ws ;;
    o3de) build_o3de ;;
    unity) build_unity ;;
  esac
}

if [[ "${simulator}" == all ]]; then
  build_one gazebo_harmonic
  build_one webots
  build_one isaac_sim
  build_one mujoco
  build_o3de
  build_one unity
else
  build_one "${simulator}"
fi
