#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ROS_DISTRO="${ROS_DISTRO:-jazzy}"
ROS_SETUP="/opt/ros/${ROS_DISTRO}/setup.bash"
EXPECTED_O3DE_DISPLAY_VERSION="26.05"
EXPECTED_O3DE_ENGINE_VERSION="2.6.0"

usage() {
  cat <<'EOF'
Usage: scripts/build_workspace.sh {gazebo_harmonic|webots|isaac_sim|mujoco|o3de|unity|all}

Build one simulator workspace, or all ROS workspaces in dependency order.
O3DE additionally requires O3DE 26.05, O3DE_HOME, and PROJECT_PATH; see README.md.
Unity Player archives are validated against Unity Editor 6000.1.14f1.

The individual 'o3de' target builds the O3DE project and its ROS 2 wrapper.
The 'all' target only builds the O3DE ROS 2 wrapper; build the O3DE project
first with the individual target.
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
  [[ -n "${O3DE_HOME:-}" ]] || { echo "O3DE_HOME is required." >&2; exit 1; }
  local project_path="${PROJECT_PATH:-${ROOT_DIR}/robotnik_benchmark_o3de_ws/src/robotnik_o3de/project/robotnik_roscon25}"
  local extras_path="${O3DE_EXTRAS_HOME:-${ROOT_DIR}/robotnik_benchmark_o3de_ws/src/o3de-extras}"
  [[ -x "${O3DE_HOME}/scripts/o3de.sh" ]] || { echo "Missing ${O3DE_HOME}/scripts/o3de.sh" >&2; exit 1; }
  [[ -r "${O3DE_HOME}/engine.json" ]] || {
    echo "Missing ${O3DE_HOME}/engine.json; install O3DE ${EXPECTED_O3DE_DISPLAY_VERSION}." >&2
    exit 1
  }
  local o3de_versions
  o3de_versions="$(python3 - "${O3DE_HOME}/engine.json" <<'PY'
import json
import sys

with open(sys.argv[1], encoding="utf-8") as stream:
    metadata = json.load(stream)
print(metadata.get("display_version", ""), metadata.get("version", ""))
PY
)"
  [[ "${o3de_versions}" == "${EXPECTED_O3DE_DISPLAY_VERSION} ${EXPECTED_O3DE_ENGINE_VERSION}" ]] || {
    echo "O3DE ${EXPECTED_O3DE_DISPLAY_VERSION} (${EXPECTED_O3DE_ENGINE_VERSION}) is required; found: ${o3de_versions:-unknown}." >&2
    exit 1
  }
  echo "Using O3DE ${EXPECTED_O3DE_DISPLAY_VERSION} (${EXPECTED_O3DE_ENGINE_VERSION})"
  git -C "${extras_path}" lfs pull
  (
    cd "${O3DE_HOME}"
    "${O3DE_HOME}/scripts/o3de.sh" register --this-engine
  )
  "${O3DE_HOME}/scripts/o3de.sh" register --all-gems-path "${extras_path}/Gems"
  "${O3DE_HOME}/scripts/o3de.sh" register --all-templates-path "${extras_path}/Templates"
  (
    cd "${project_path}"
    cmake -B build/linux -G "Ninja Multi-Config" \
      -DLY_DISABLE_TEST_MODULES=ON \
      -DCMAKE_EXPORT_COMPILE_COMMANDS=ON \
      -DLY_STRIP_DEBUG_SYMBOLS=ON
    cmake --build build/linux --config profile \
      --target robotnik_roscon25 Editor robotnik_roscon25.Assets robotnik_roscon25.GameLauncher
  )
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
  build_o3de_ros_workspace
  build_one unity
else
  build_one "${simulator}"
fi
