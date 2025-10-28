#!/usr/bin/env bash
# run_webots_benchmark.sh
set -Eeuo pipefail

show_help() {
	cat <<EOF
Usage: $0 [OPTIONS] 
Options:
	-s, --simulator NAME   Simulator to use (default: webots)
	-h, --help             Show this help message and exit

Example:
	$0 -s webots -- 
EOF
}

SIMULATOR="webots"
ITERATION_TIME=60
ITERATIONS=1

# Parse options
while [[ $# -gt 0 ]]; do
	case "$1" in
		-s|--simulator)
			if [[ -n "${2:-}" && ! "$2" =~ ^- ]]; then
				SIMULATOR="$2"; shift 2
			else
				echo "Error: Missing argument for -s|--simulator"; show_help; exit 1
			fi
			;;
		-h|--help)
			show_help; exit 0;;
		*)
			shift
			;;
	esac
done

if [[ "$SIMULATOR" == "webots" || "$SIMULATOR" == "gazebo_harmonic" || "$SIMULATOR" == "isaac_sim" || "$SIMULATOR" == "unity"  || "$SIMULATOR" == "o3de" ]]; then
	for CATEGORY in {1..24}; do
		echo -e "\n\n\n------------------------------------------------------------------------------------------------------------------------------------------"
		# Print the current test in color with command verbosity
		echo -e "\033[1;34mRunning benchmark for CATEGORY $CATEGORY with simulator $SIMULATOR (iterations: $ITERATIONS, iteration_time: $ITERATION_TIME)\033[0m"
		echo -e "------------------------------------------------------------------------------------------------------------------------------------------n\n\n"

		python3 "$(dirname "$0")/benchmark_simulator.py" --category "$CATEGORY" --iterations "$ITERATIONS" --iteration_time "$ITERATION_TIME" "$SIMULATOR"
		# Ensure all child processes are terminated before continuing
		pkill -f benchmark_simulator.py || true
		
		echo -e "Waiting 10 seconds before the next benchmark..."
		sleep 10
	done
else
	echo "Unknown simulator: $SIMULATOR"
	exit 1
fi


echo "All benchmarks completed. Thank you for using the benchmarking script!"