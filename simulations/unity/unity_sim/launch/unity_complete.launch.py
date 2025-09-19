#!/usr/bin/env python3
#
# Launches:
#  - RViz2 with sim time and package rviz config
#  - Unity simulation bootstrap script (utils/load_usd_and_run.py)
#  - ROS-TCP-Endpoint (delayed start)
#  - Optional spawning of N robots via std_srvs/Trigger services: robot[/_N]/on
#
# Args:
#   run_rviz         (bool)  : launch RViz2 (default: true)
#   robot_count      (int)   : number of robots to spawn [1..5] (default: 1)
#   world            (str)   : name of the world to load (default: empty_world)
#   bridge_delay_sec (float) : delay before starting ROS-TCP-Endpoint (default: 4.0)

import os
from launch import LaunchDescription
from launch.actions import (
    DeclareLaunchArgument,
    GroupAction,
    ExecuteProcess,
    TimerAction,
    OpaqueFunction,
)
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch.conditions import IfCondition
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    # -------------------------
    # Launch arguments
    # -------------------------
    run_rviz_arg = DeclareLaunchArgument(
        "run_rviz",
        default_value="true",
        description="Launch RViz2 with the provided config",
    )

    robot_count_arg = DeclareLaunchArgument(
        "robot_count",
        default_value="1",
        description="Number of robots to spawn via services [1..5]",
    )

    world_arg = DeclareLaunchArgument(
        "world",
        default_value="empty_world",
        choices=["empty_world", "simple_world"],
        description="Name of the world to load",
    )

    bridge_delay_arg = DeclareLaunchArgument(
        "bridge_delay_sec",
        default_value="4.0",
        description="Delay (seconds) before starting ROS-TCP-Endpoint",
    )

    # -------------------------
    # Launch Unity with selected world (executes immediately)
    # -------------------------
    def launch_unity_with_world(context, *args, **kwargs):
        world_to_filename_map = {
            "empty_world": "unity_simulation_only.tar.gz",
            "simple_world": "unity_simulation.tar.gz",
        }
        selected_world_name = LaunchConfiguration("world").perform(context)
        world_filename = world_to_filename_map[selected_world_name]

        print(
            f"[INFO] Selected world: '{selected_world_name}' -> using file: '{world_filename}'"
        )

        pkg_share_path = get_package_share_directory("unity_sim")
        autorun_script_path = os.path.join(pkg_share_path, "utils", "load_usd_and_run.py")

        unity_bootstrap = ExecuteProcess(
            cmd=["python3", autorun_script_path, world_filename],
            name="unity_sim_bootstrap",
            output="screen",
        )
        return [unity_bootstrap]

    # -------------------------
    # ROS–TCP–Endpoint (listens on 0.0.0.0) — delayed start
    # -------------------------
    ros_tcp_endpoint_node = Node(
        package="ros_tcp_endpoint",
        executable="default_server_endpoint",
        name="ros_tcp_endpoint",
        output="screen",
        parameters=[{"ROS_IP": "0.0.0.0"}],
    )

    ros_tcp_endpoint_delayed = TimerAction(
        period=LaunchConfiguration("bridge_delay_sec"),
        actions=[ros_tcp_endpoint_node],
    )

    # -------------------------
    # RViz2 (use_sim_time enabled)
    # -------------------------
    pkg_share = FindPackageShare("unity_sim")
    rviz_config = PathJoinSubstitution([pkg_share, "rviz", "robot.rviz"])

    rviz = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        arguments=["-d", rviz_config],
        output="screen",
        parameters=[{"use_sim_time": True}],
        condition=IfCondition(LaunchConfiguration("run_rviz")),
    )

    # -------------------------
    # Helper to build spawn calls
    # -------------------------
    def build_spawn_calls(context, *args, **kwargs):
        try:
            count = int(LaunchConfiguration("robot_count").perform(context))
        except (TypeError, ValueError):
            count = 1
        count = max(1, min(5, count))

        processes = []
        spawn_delay_sec = 5.0  # spawns happen after bridge delay; total ~9s if default

        for idx in range(1, count + 1):
            name = "robot" if idx == 1 else f"robot_{idx}"
            srv_name = f"/{name}/on"
            call = ExecuteProcess(
                cmd=["ros2", "service", "call", srv_name, "std_srvs/srv/Trigger", "{}"],
                name=f"spawn_{name}",
                output="screen",
            )
            processes.append(call)

        return [TimerAction(period=spawn_delay_sec, actions=processes)]

    spawn_group = OpaqueFunction(function=build_spawn_calls)

    # -------------------------
    # Group and LD
    # -------------------------
    group = GroupAction(
        [
            # 1) Unity bootstrap immediately
            OpaqueFunction(function=launch_unity_with_world),
            # 2) RViz (optional)
            rviz,
            # 3) Delayed ROS–TCP–Endpoint
            ros_tcp_endpoint_delayed,
            # 4) Spawns (already delayed 5s)
            spawn_group,
        ]
    )

    return LaunchDescription(
        [
            run_rviz_arg,
            robot_count_arg,
            world_arg,
            bridge_delay_arg,
            group,
        ]
    )

