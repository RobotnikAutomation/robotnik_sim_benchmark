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
            'num_robots',
            default_value='1',
            description='Número de robots a spawnear'
        )
    )

    declared_arguments.append(
        DeclareLaunchArgument(
            'world_file',
            default_value='empty_world.usd',
            description='Nombre del USD del mundo'
        )
    )

    declared_arguments.append(
        DeclareLaunchArgument(
            "run_rviz",
            default_value="true",
            description="Launch RViz2 with predefined config"
        )
    )

    num_robots = LaunchConfiguration('num_robots')
    world_file = LaunchConfiguration('world_file')
    run_rviz = LaunchConfiguration("run_rviz")

    world_path = PathJoinSubstitution([
        FindPackageShare('isaac_sim'),
        'worlds/rbwacther_sim.world'
    ])

    autorun_script = PathJoinSubstitution([
        FindPackageShare('isaac_sim'),
        'utils/isaac_sim_launcher.py'
    ])

    isaac_sim = ExecuteProcess(
        cmd=[
            os.path.expanduser("~/isaac_sim/isaac-sim.sh"),
            "--exec", autorun_script
        ],
        output="screen",
        additional_env={
            'NUM_ROBOTS': num_robots,
            'WORLD_FILE': world_file
        }
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
        condition=IfCondition(run_rviz)
    )


    group = GroupAction([
        isaac_sim,
        rviz
    ])

    return LaunchDescription(declared_arguments + [group])


