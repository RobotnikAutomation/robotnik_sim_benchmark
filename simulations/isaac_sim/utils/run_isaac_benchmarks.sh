#bin/bash

pushd "$(dirname "${BASH_SOURCE[0]}")/../../.." > /dev/null
ROOT_DIR="$(pwd)"

print_info() {
    local message="$@"
    local width=$(tput cols)
    local border=$(printf '=%.0s' $(seq 1 $width))
    
    # Centrar mensaje
    local padding=$(( (width - ${#message}) / 2 ))
    printf "\n\e[34m%s\e[0m\n" "$border"
    printf "\e[34m%*s%s%*s\e[0m\n" $padding "" "$message" $padding ""
    printf "\e[34m%s\e[0m\n\n" "$border"
}

isaac_benchmark() {
    local category num_robots world_file run_rviz

    for arg in "$@"; do
        case $arg in
            category=*) category="${arg#*=}" ;;
            num_robots=*) num_robots="${arg#*=}" ;;
            world_file=*) world_file="${arg#*=}" ;;
            run_rviz=*) run_rviz="${arg#*=}" ;;
            *) echo "Argumento desconocido: $arg"; exit 1 ;;
        esac
    done

    sleep 0.5

    python3 scripts/benchmark_simulator.py isaac_sim \
        --category "$category" \
        --iterations 1 \
        --image_topic front_rgbd_camera/color/image_raw \
        --ros_args "num_robots:=$num_robots" "world_file:=$world_file" "run_rviz:=$run_rviz"
}

print_info "one_robot_emtpy_world"
isaac_benchmark category=1 num_robots=1 world_file="empty_world.usd" run_rviz="false"

print_info "two_robot_emtpy_world"
isaac_benchmark category=2 num_robots=2 world_file="empty_world.usd" run_rviz="false"

print_info "three_robot_emtpy_world"
isaac_benchmark category=3 num_robots=3 world_file="empty_world.usd" run_rviz="false"

print_info "one_robot_simple_world"
isaac_benchmark category=4 num_robots=1 world_file="simple_world.usd" run_rviz="false"

print_info "two_robot_simple_world"
isaac_benchmark category=5 num_robots=2 world_file="simple_world.usd" run_rviz="false"

print_info "three_robot_simple_world"
isaac_benchmark category=6 num_robots=3 world_file="simple_world.usd" run_rviz="false"


print_info "one_robot_emtpy_world_rviz"
isaac_benchmark category=7 num_robots=1 world_file="empty_world.usd" run_rviz="true"

print_info "two_robot_emtpy_world_rviz"
isaac_benchmark category=8 num_robots=2 world_file="empty_world.usd" run_rviz="true"

print_info "three_robot_emtpy_world_rviz"
isaac_benchmark category=9 num_robots=3 world_file="empty_world.usd" run_rviz="true"

print_info "one_robot_simple_world_rviz"
isaac_benchmark category=10 num_robots=1 world_file="simple_world.usd" run_rviz="true"

print_info "two_robot_simple_world_rviz"
isaac_benchmark category=11 num_robots=2 world_file="simple_world.usd" run_rviz="true"

print_info "three_robot_simple_world_rviz"
isaac_benchmark category=12 num_robots=3 world_file="simple_world.usd" run_rviz="true"


popd > /dev/null

