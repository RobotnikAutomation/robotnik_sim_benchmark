#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${ROOT_DIR}"

usage() {
  cat <<'EOF'
Usage: scripts/setup_workspace.sh [--pull-lfs]

Initialise all pinned Git submodules. Use --pull-lfs to download simulator
assets after the repositories have been initialised.
EOF
}

pull_lfs=false
case "${1:-}" in
  '') ;;
  --pull-lfs) pull_lfs=true ;;
  -h|--help) usage; exit 0 ;;
  *) echo "Unknown option: $1" >&2; usage >&2; exit 2 ;;
esac

for command in git; do
  command -v "${command}" >/dev/null || {
    echo "Required command not found: ${command}" >&2
    exit 1
  }
done

if ! command -v git-lfs >/dev/null; then
  echo "Git LFS is required. Install it before initialising simulator assets." >&2
  exit 1
fi

if [[ -n "${ROS_DISTRO:-}" ]]; then
  ros_setup="/opt/ros/${ROS_DISTRO}/setup.bash"
  [[ -r "${ros_setup}" ]] || {
    echo "ROS_DISTRO=${ROS_DISTRO}, but ${ros_setup} is not readable." >&2
    exit 1
  }
elif [[ -r /opt/ros/jazzy/setup.bash ]]; then
  ros_setup=/opt/ros/jazzy/setup.bash
  ROS_DISTRO=jazzy
else
  echo "ROS 2 Jazzy was not found under /opt/ros/jazzy." >&2
  exit 1
fi

git lfs install --local
git submodule sync
git submodule update --init

if ${pull_lfs}; then
  git submodule foreach --recursive 'git lfs pull'
fi

if git submodule status | grep -E '^[+-U]' >/dev/null; then
  echo "One or more submodules are not at the pinned commit:" >&2
  git submodule status >&2
  exit 1
fi

echo "Workspace initialised successfully."
echo "ROS setup: ${ros_setup}"
echo "ROS_DISTRO: ${ROS_DISTRO}"
echo "For O3DE: export O3DE_HOME=/opt/O3DE/26.05"
echo "For O3DE: export O3DE_EXTRAS_HOME=${ROOT_DIR}/robotnik_benchmark_o3de_ws/src/o3de-extras"
echo "For O3DE: export PROJECT_PATH=${ROOT_DIR}/robotnik_benchmark_o3de_ws/src/robotnik_o3de/project/robotnik_roscon25"
if ! ${pull_lfs}; then
  echo "Run '$0 --pull-lfs' before building O3DE or Unity assets."
fi
