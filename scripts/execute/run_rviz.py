#!/usr/bin/env python3

"""Launch the single multi-robot RViz instance used by a benchmark iteration."""

from __future__ import annotations

import argparse
import json
import math
import os
import signal
import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPT_ROOT = Path(__file__).resolve().parents[1]
if str(SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPT_ROOT))

from common.sensor_profile import SIMULATORS, robot_name, rviz_streams



def _topic(value: str) -> dict[str, object]:
    return {
        "Depth": 5,
        "Durability Policy": "Volatile",
        "History Policy": "Keep Last",
        "Reliability Policy": "Best Effort",
        "Value": value,
    }


def _display(display_class: str, name: str, topic: str) -> dict[str, object]:
    return {
        "Class": display_class,
        "Enabled": True,
        "Name": name,
        "Topic": _topic(topic),
    }


def _robot_names(simulator: str, robot_count: int) -> list[str]:
    return [robot_name(simulator, index) for index in range(1, robot_count + 1)]


def _sensor_topics(simulator: str, robot_name: str) -> list[tuple[str, str, str]]:
    """Return RViz display class, label suffix, and topic for one robot.

    These are the camera and LiDAR streams enabled in the benchmark robot
    descriptions.  RViz subscriptions are created for every active robot even
    before its simulator has advertised the corresponding topic.
    """
    names = _robot_names(simulator, 3)
    try:
        index = names.index(robot_name) + 1
    except ValueError as exc:
        raise ValueError(f"Unknown {simulator} robot name: {robot_name}") from exc
    return rviz_streams(simulator, index)


def _fixed_frame(simulator: str) -> str:
    """Return a frame that exists and connects every displayed robot."""
    if simulator in {"webots", "isaac_sim", "mujoco"}:
        return "world"
    return "benchmark_world"


def _static_transform_specs(
    simulator: str,
    robot_names: list[str],
) -> list[tuple[str, float, float, float]]:
    """Describe missing common-world to per-robot odom transforms.

    Webots and Isaac publish a world-rooted tree themselves. Gazebo and O3DE
    spawn at the benchmark wrapper's one-metre X/Y increments. Unity odometry
    already contains each initial world pose, so its odom roots are connected
    with identity transforms.
    """
    if simulator in {"webots", "isaac_sim", "mujoco"}:
        return []
    specs = []
    for index, robot_name in enumerate(robot_names):
        if simulator == "gazebo_harmonic":
            child_frame = f"{robot_name}_odom"
            x = y = float(index)
        elif simulator == "o3de":
            child_frame = f"{robot_name}/odom"
            x = y = float(index)
        else:
            child_frame = f"{robot_name}_odom"
            x = y = 0.0
        specs.append((child_frame, x, y, 0.0))
    return specs


def build_config(simulator: str, robot_count: int) -> dict[str, object]:
    """Build a compact, valid RViz configuration for all benchmark sensors."""
    robot_names = _robot_names(simulator, robot_count)
    displays: list[dict[str, object]] = [
        {
            "Class": "rviz_default_plugins/Grid",
            "Enabled": True,
            "Name": "Grid",
            "Reference Frame": "<Fixed Frame>",
        },
        {
            "Class": "rviz_default_plugins/TF",
            "Enabled": True,
            "Name": "TF",
            "Show Arrows": True,
            "Show Axes": False,
            "Show Names": False,
        },
    ]
    for robot_name in robot_names:
        for display_class, label, topic in _sensor_topics(simulator, robot_name):
            displays.append(_display(display_class, f"{robot_name} {label}", topic))

    return {
        "Panels": [{"Class": "rviz_common/Displays", "Name": "Displays"}],
        "Visualization Manager": {
            "Class": "",
            "Displays": displays,
            "Enabled": True,
            "Global Options": {
                "Background Color": "48; 48; 48",
                "Fixed Frame": _fixed_frame(simulator),
                "Frame Rate": 30,
            },
            "Name": "root",
        },
    }


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Launch one RViz instance subscribed to every benchmark robot sensor"
    )
    parser.add_argument("simulator", choices=SIMULATORS)
    parser.add_argument("robot_count", type=int, choices=(1, 2, 3))
    return parser.parse_args()


def main() -> int:
    args = parse_arguments()
    with tempfile.NamedTemporaryFile(
        mode="w", encoding="utf-8", suffix=".rviz", prefix="benchmark_rviz_", delete=False
    ) as config_file:
        json.dump(build_config(args.simulator, args.robot_count), config_file, indent=2)
        config_path = Path(config_file.name)

    child: subprocess.Popen[str] | None = None
    static_node = None
    static_broadcaster = None
    rclpy_initialized = False

    transform_specs = _static_transform_specs(
        args.simulator,
        _robot_names(args.simulator, args.robot_count),
    )
    if transform_specs:
        import rclpy
        from geometry_msgs.msg import TransformStamped
        from rclpy.node import Node
        from rclpy.signals import SignalHandlerOptions
        from tf2_ros.static_transform_broadcaster import StaticTransformBroadcaster

        rclpy.init(signal_handler_options=SignalHandlerOptions.NO)
        rclpy_initialized = True
        static_node = Node(f"benchmark_static_frames_{os.getpid()}")
        static_broadcaster = StaticTransformBroadcaster(static_node)
        transforms = []
        for child_frame, x, y, yaw in transform_specs:
            transform = TransformStamped()
            transform.header.stamp = static_node.get_clock().now().to_msg()
            transform.header.frame_id = "benchmark_world"
            transform.child_frame_id = child_frame
            transform.transform.translation.x = x
            transform.transform.translation.y = y
            transform.transform.rotation.z = math.sin(yaw / 2.0)
            transform.transform.rotation.w = math.cos(yaw / 2.0)
            transforms.append(transform)
        static_broadcaster.sendTransform(transforms)

    def forward_signal(signum: int, _frame: object) -> None:
        if child is not None and child.poll() is None:
            child.send_signal(signum)

    for handled_signal in (signal.SIGINT, signal.SIGTERM, signal.SIGHUP):
        signal.signal(handled_signal, forward_signal)

    try:
        child = subprocess.Popen(
            [
                "rviz2",
                "-d",
                str(config_path),
                "--ros-args",
                "-p",
                "use_sim_time:=true",
            ]
        )
        return child.wait()
    finally:
        if static_node is not None:
            static_node.destroy_node()
        if rclpy_initialized:
            import rclpy
            if rclpy.ok():
                rclpy.shutdown()
        try:
            config_path.unlink(missing_ok=True)
        except OSError:
            pass


if __name__ == "__main__":
    raise SystemExit(main())
