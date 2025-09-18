import os
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument, GroupAction, ExecuteProcess
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution, LaunchConfiguration
from launch_ros.substitutions import FindPackageShare
from launch.conditions import IfCondition
from launch_ros.actions import Node


def generate_launch_description():


    declared_arguments = []

    declared_arguments.append(
        DeclareLaunchArgument(
            "run_rviz",
            default_value="true",
            description="Launch RViz2 with predefined config"
        )
    )

    world_path = PathJoinSubstitution([
        FindPackageShare('isaac_sim'),
        'worlds/rbwacther_sim.world'
    ])

    autorun_script = PathJoinSubstitution([
        FindPackageShare('isaac_sim'),
        'utils/load_usd_and_run.py'
    ])


    # run isaac
    isaac_sim = ExecuteProcess(
        cmd=[
            os.path.expanduser("~/isaac_sim/isaac-sim.sh"),
            "--exec", autorun_script
        ],
        output="screen"
    )

    # run rviz
    rviz_config = PathJoinSubstitution([
        FindPackageShare("isaac_sim"), 
        "config",
        "rviz_config.rviz"
    ])

    rviz = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        arguments=["-d", rviz_config],
        output="screen",
        condition=IfCondition(LaunchConfiguration("run_rviz"))
    )


    group = GroupAction([
        isaac_sim,
        rviz
    ])

    return LaunchDescription(declared_arguments + [group])


