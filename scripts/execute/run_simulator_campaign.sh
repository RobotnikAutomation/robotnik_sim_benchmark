#!/usr/bin/env bash
set -Eeuo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
REPOSITORY_ROOT="$(cd -- "${SCRIPT_DIR}/../.." && pwd)"

show_help() {
  cat <<EOF
Usage: $(basename "$0") [OPTIONS]

Options:
  -s, --simulator NAME       Simulator (default: webots)
  -n, --iterations COUNT     Iterations per category (default: 1)
  -t, --iteration-time SEC   Measurement time after startup (default: 60)
      --gui                  Run only GUI categories
      --headless              Run only headless categories
      --rviz                 Add RViz to the selected GUI/headless modes
      --list-only            Print selected categories without launching them
      --startup-timeout SEC  Readiness timeout for configured image topics (default: 120)
      --warmup-time SEC      Stabilization time after readiness (default: 0)
      --max-retries COUNT    Retries after a failed iteration (default: 3)
      --retry-cooldown SEC   Pause between retries (default: 5)
      --iteration-cooldown SEC Pause between iterations (default: 5)
      --sigint-timeout SEC   Cleanup grace after SIGINT (default: 10; Isaac: 30)
      --sigterm-timeout SEC  Cleanup grace after SIGTERM (default: 5)
      --final-cleanup-timeout SEC Extra SIGKILL/reap time before retrying (default: 30)
      --cooldown SEC         Pause between categories (default: 10)
      --process-monitor      Open the external live process tree
      --monitor-ros          Enable external ROS transport monitoring (disabled by default)
      --render-fps FPS       GUI render cap: 1..1000 (default: 60; use 500 for a high cap)
  -h, --help                 Show this help
EOF
}

SIMULATOR="webots"
ITERATIONS=1
ITERATION_TIME=60
STARTUP_TIMEOUT=120
WARMUP_TIME=0
MAX_RETRIES=3
RETRY_COOLDOWN=5
ITERATION_COOLDOWN=5
SIGINT_TIMEOUT=10
SIGTERM_TIMEOUT=5
FINAL_CLEANUP_TIMEOUT=30
COOLDOWN_SECONDS=10
SIGINT_TIMEOUT_SET=false
GUI_ONLY=false
HEADLESS_ONLY=false
RVIZ=false
LIST_ONLY=false
PROCESS_MONITOR=false
MONITOR_ROS=false
RENDER_FPS=60

if [[ -t 1 && "${NO_COLOR:-}" != "1" ]]; then
  COLOR_RESET=$'\033[0m'
  COLOR_TITLE=$'\033[1;36m'
  COLOR_ACCENT=$'\033[1;33m'
  COLOR_MUTED=$'\033[2m'
else
  COLOR_RESET=""
  COLOR_TITLE=""
  COLOR_ACCENT=""
  COLOR_MUTED=""
fi

print_run_header() {
  local category_number="$1"
  local category_name="$2"
  printf '\n%s\n' '================================================================================'
  printf '%s BENCHMARK %d/%d %s\n' \
    "${COLOR_TITLE}" "${category_number}" "${CATEGORY_COUNT}" "${COLOR_RESET}"
  printf '  Simulator : %s\n' "${SIMULATOR}"
  printf '  Category  : %s\n' "${category_name}"
  printf '  Iterations: %s    Measurement: %ss    Startup timeout: %ss\n' \
    "${ITERATIONS}" "${ITERATION_TIME}" "${STARTUP_TIMEOUT}"
  printf '  Shutdown  : SIGINT %ss + SIGTERM %ss    Cooldown: %ss\n' \
    "${SIGINT_TIMEOUT}" "${SIGTERM_TIMEOUT}" "${COOLDOWN_SECONDS}"
  printf '  RViz      : %s\n' \
    "$([[ "${RVIZ}" == true ]] && printf 'filtered to RViz categories' || printf 'configured per category')"
  printf '  ROS monitor: %s\n' \
    "$( [[ "${MONITOR_ROS}" == true ]] && printf 'enabled' || printf 'disabled' )"
  printf '  Render FPS: %s (GUI only)\n' "${RENDER_FPS}"
  printf '%s\n' '--------------------------------------------------------------------------------'
}

while (($#)); do
  case "$1" in
    -s|--simulator)
      [[ -n "${2:-}" ]] || { echo "Missing simulator name" >&2; exit 2; }
      SIMULATOR="$2"
      shift 2
      ;;
    -n|--iterations)
      [[ "${2:-}" =~ ^[1-9][0-9]*$ ]] || { echo "Invalid iteration count" >&2; exit 2; }
      ITERATIONS="$2"
      shift 2
      ;;
    -t|--iteration-time)
      [[ "${2:-}" =~ ^[1-9][0-9]*$ ]] || { echo "Invalid iteration time" >&2; exit 2; }
      ITERATION_TIME="$2"
      shift 2
      ;;
    --gui)
      GUI_ONLY=true
      shift
      ;;
    --headless)
      HEADLESS_ONLY=true
      shift
      ;;
    --rviz)
      RVIZ=true
      shift
      ;;
    --list-only)
      LIST_ONLY=true
      shift
      ;;
    --startup-timeout)
      [[ "${2:-}" =~ ^[1-9][0-9]*$ ]] || { echo "Invalid startup timeout" >&2; exit 2; }
      STARTUP_TIMEOUT="$2"
      shift 2
      ;;
    --warmup-time)
      [[ "${2:-}" =~ ^[0-9]+([.][0-9]+)?$ ]] || { echo "Invalid warmup time" >&2; exit 2; }
      WARMUP_TIME="$2"
      shift 2
      ;;
    --max-retries)
      [[ "${2:-}" =~ ^[0-9]+$ ]] || { echo "Invalid retry count" >&2; exit 2; }
      MAX_RETRIES="$2"
      shift 2
      ;;
    --retry-cooldown)
      [[ "${2:-}" =~ ^[0-9]+([.][0-9]+)?$ ]] || { echo "Invalid retry cooldown" >&2; exit 2; }
      RETRY_COOLDOWN="$2"
      shift 2
      ;;
    --iteration-cooldown)
      [[ "${2:-}" =~ ^[0-9]+([.][0-9]+)?$ ]] || { echo "Invalid iteration cooldown" >&2; exit 2; }
      ITERATION_COOLDOWN="$2"
      shift 2
      ;;
    --sigint-timeout)
      [[ "${2:-}" =~ ^[0-9]+([.][0-9]+)?$ ]] || { echo "Invalid SIGINT timeout" >&2; exit 2; }
      SIGINT_TIMEOUT="$2"
      SIGINT_TIMEOUT_SET=true
      shift 2
      ;;
    --sigterm-timeout)
      [[ "${2:-}" =~ ^[0-9]+([.][0-9]+)?$ ]] || { echo "Invalid SIGTERM timeout" >&2; exit 2; }
      SIGTERM_TIMEOUT="$2"
      shift 2
      ;;
    --final-cleanup-timeout)
      [[ "${2:-}" =~ ^[0-9]+([.][0-9]+)?$ ]] || { echo "Invalid final cleanup timeout" >&2; exit 2; }
      FINAL_CLEANUP_TIMEOUT="$2"
      shift 2
      ;;
    --cooldown)
      [[ "${2:-}" =~ ^[0-9]+([.][0-9]+)?$ ]] || { echo "Invalid cooldown" >&2; exit 2; }
      COOLDOWN_SECONDS="$2"
      shift 2
      ;;
    --process-monitor)
      PROCESS_MONITOR=true
      shift
      ;;
    --monitor-ros)
      MONITOR_ROS=true
      shift
      ;;
    --render-fps)
      [[ "${2:-}" =~ ^[1-9][0-9]{0,2}$ && "${2}" -le 1000 ]] || {
        echo "--render-fps must be an integer between 1 and 1000" >&2; exit 2;
      }
      RENDER_FPS="$2"
      shift 2
      ;;
    -h|--help)
      show_help
      exit 0
      ;;
    *)
      echo "Unknown option: $1" >&2
      show_help >&2
      exit 2
      ;;
  esac
done

if [[ "${GUI_ONLY}" == true && "${HEADLESS_ONLY}" == true ]]; then
  echo "--gui and --headless cannot be used together" >&2
  exit 2
fi
case "${SIMULATOR}" in
  gazebo_harmonic|webots|isaac_sim|unity|o3de|mujoco) ;;
  *) echo "Unknown simulator: ${SIMULATOR}" >&2; exit 2 ;;
esac

# Kit needs more time than the lighter simulators to unload its plugins.
if [[ "${SIMULATOR}" == "isaac_sim" ]]; then
  [[ "${SIGINT_TIMEOUT_SET}" == true ]] || SIGINT_TIMEOUT=30
fi

# This validates the configuration before the first benchmark and keeps the
# selected categories tied to the canonical definition in Python.
CATEGORY_FILTER_ARGS=(--category-names)
[[ "${GUI_ONLY}" == true ]] && CATEGORY_FILTER_ARGS+=(--gui)
[[ "${HEADLESS_ONLY}" == true ]] && CATEGORY_FILTER_ARGS+=(--headless)
[[ "${RVIZ}" == true ]] && CATEGORY_FILTER_ARGS+=(--rviz)
CATEGORY_OUTPUT="$(python3 "${REPOSITORY_ROOT}/scripts/validate/validate_config.py" "${CATEGORY_FILTER_ARGS[@]}")"
mapfile -t CATEGORIES <<< "${CATEGORY_OUTPUT}"
CATEGORY_COUNT="${#CATEGORIES[@]}"
if [[ "${LIST_ONLY}" == true ]]; then
  printf '%s\n' "${CATEGORIES[@]}"
  exit 0
fi
cd "${REPOSITORY_ROOT}"

BENCHMARK_EXTRA_ARGS=()
[[ "${PROCESS_MONITOR}" == true ]] && BENCHMARK_EXTRA_ARGS+=(--process-monitor)
if [[ "${MONITOR_ROS}" == true ]]; then
  BENCHMARK_EXTRA_ARGS+=(--monitor-ros)
fi

for category_index in "${!CATEGORIES[@]}"; do
  category_number=$((category_index + 1))
  print_run_header "${category_number}" "${CATEGORIES[category_index]}"
  python3 "${SCRIPT_DIR}/run_benchmark.py" \
    --category "${CATEGORIES[category_index]}" \
    --iterations "${ITERATIONS}" \
    --iteration_time "${ITERATION_TIME}" \
    --startup_timeout "${STARTUP_TIMEOUT}" \
    --warmup-time "${WARMUP_TIME}" \
    --max_retries "${MAX_RETRIES}" \
    --retry_cooldown "${RETRY_COOLDOWN}" \
    --iteration_cooldown "${ITERATION_COOLDOWN}" \
    --sigint_timeout "${SIGINT_TIMEOUT}" \
    --sigterm_timeout "${SIGTERM_TIMEOUT}" \
    --final-cleanup-timeout "${FINAL_CLEANUP_TIMEOUT}" \
    --render-fps "${RENDER_FPS}" \
    "${BENCHMARK_EXTRA_ARGS[@]}" \
    "${SIMULATOR}"

  if ((category_number < CATEGORY_COUNT)); then
    printf '%sNext benchmark in %s seconds...%s\n' \
      "${COLOR_MUTED}" "${COOLDOWN_SECONDS}" "${COLOR_RESET}"
    sleep "${COOLDOWN_SECONDS}"
  fi
done

echo "All benchmarks completed."
