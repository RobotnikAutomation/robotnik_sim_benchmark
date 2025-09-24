cmake_minimum_required(VERSION 3.5)
project(robotnik_sim_benchmark_utils)

find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(std_srvs REQUIRED)
find_package(sensor_msgs REQUIRED)


add_executable(
    benchmark_node
    src/benchmark_node.cpp
)
    
ament_target_dependencies(
    benchmark_node
    rclcpp
    std_srvs
    sensor_msgs
)

install(TARGETS
  benchmark_node
  DESTINATION lib/${PROJECT_NAME}
)

install(DIRECTORY launch script
  DESTINATION share/${PROJECT_NAME}
)

ament_package()
