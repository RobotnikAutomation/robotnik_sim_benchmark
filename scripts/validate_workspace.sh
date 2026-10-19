#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${ROOT_DIR}"

failures=0
check_path() {
  if [[ ! -d "$1" ]]; then
    echo "Missing submodule: $1" >&2
    failures=$((failures + 1))
  fi
}

git submodule sync >/dev/null
git submodule status
if git submodule status | grep -E '^[+-U]' >/dev/null; then
  echo "Submodules are not fully initialised or do not match their pinned commits." >&2
  failures=$((failures + 1))
fi

while IFS= read -r path; do
  [[ -n "${path}" ]] && check_path "${path}"
done < <(git config --file .gitmodules --get-regexp '^submodule\..*\.path$' | awk '{print $2}')

if command -v python3 >/dev/null; then
  python3 scripts/validate/validate_config.py --category-count
else
  echo "python3 is required for benchmark configuration validation." >&2
  failures=$((failures + 1))
fi

for workspace in \
  robotnik_benchmark_gazebo_ws \
  robotnik_benchmark_webots_ws \
  robotnik_benchmark_isaac_ws \
  robotnik_benchmark_mujoco_ws \
  robotnik_benchmark_o3de_ws \
  robotnik_benchmark_unity_ws; do
  [[ -d "${workspace}/src" ]] || {
    echo "Missing workspace source directory: ${workspace}/src" >&2
    failures=$((failures + 1))
  }
done

if (( failures != 0 )); then
  echo "Workspace validation failed with ${failures} issue(s)." >&2
  exit 1
fi

echo "Workspace validation passed."
