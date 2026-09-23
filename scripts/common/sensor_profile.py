#!/usr/bin/env python3
"""Single source of truth for the benchmark sensor workload and ROS names."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml


PROFILE_PATH = Path(__file__).resolve().parents[2] / "config" / "canonical_sensor_profile.yaml"
SIMULATORS = ("gazebo_harmonic", "webots", "isaac_sim", "unity", "o3de", "mujoco")


@lru_cache(maxsize=1)
def load_profile() -> dict[str, Any]:
    with PROFILE_PATH.open(encoding="utf-8") as stream:
        profile = yaml.safe_load(stream)
    if profile.get("schema_version") != 1:
        raise ValueError(f"Unsupported sensor profile schema in {PROFILE_PATH}")
    lidar = profile["canonical"]["lidar_3d"]
    calculated = int(lidar["channels"]) * int(lidar["horizontal_samples"])
    if calculated != int(lidar["points_per_scan"]):
        raise ValueError(f"LiDAR profile is inconsistent: {calculated} != {lidar['points_per_scan']}")
    if set(profile["simulators"]) != set(SIMULATORS):
        raise ValueError("Sensor profile must describe exactly the benchmark backends")
    for camera_name in ("camera_a", "camera_b"):
        if not isinstance(profile["canonical"][camera_name].get("depth_enabled"), bool):
            raise ValueError(f"{camera_name}.depth_enabled must be boolean")
    if float(profile["canonical"]["physics_clock_hz"]) <= 0:
        raise ValueError("canonical.physics_clock_hz must be positive")
    for simulator in SIMULATORS:
        rate = profile["simulators"][simulator].get("physics_clock_hz")
        if rate is not None and float(rate) <= 0:
            raise ValueError(f"{simulator}.physics_clock_hz must be positive")
    return profile


def physics_clock_rate_hz(simulator: str) -> float:
    """Return the nominal simulation-clock rate for a backend."""
    if simulator not in SIMULATORS:
        raise ValueError(f"Invalid simulator: {simulator}")
    profile = load_profile()
    return float(profile["simulators"][simulator].get(
        "physics_clock_hz", profile["canonical"]["physics_clock_hz"]
    ))


def robot_name(simulator: str, index: int) -> str:
    if simulator not in SIMULATORS or index not in (1, 2, 3):
        raise ValueError(f"Invalid simulator/robot index: {simulator}/{index}")
    simulator_profile = load_profile()["simulators"][simulator]
    if index == 1 and "first_robot_name" in simulator_profile:
        return str(simulator_profile["first_robot_name"])
    return str(simulator_profile["robot_name_template"]).format(index=index)


def namespace(simulator: str, index: int) -> str:
    simulator_profile = load_profile()["simulators"][simulator]
    name = robot_name(simulator, index)
    template = simulator_profile.get("namespace_template", name)
    return "/" + str(template).format(index=index, robot_name=name).strip("/")


def topic(simulator: str, index: int, sensor: str, field: str = "topic") -> str:
    simulator_profile = load_profile()["simulators"][simulator]
    name = robot_name(simulator, index)
    relative = str(simulator_profile[sensor][field]).format(index=index, robot_name=name)
    if relative.startswith("/"):
        return relative
    return f"{namespace(simulator, index)}/{relative.lstrip('/')}"


def expected_nonimage_sensor_topics(simulator: str, category: str):
    """Return canonical LiDAR and IMU topics required by ROS monitoring."""
    robot_count = {"one": 1, "two": 2, "three": 3}[category.split("_", 1)[0]]
    return [
        (topic(simulator, index, sensor), message_type)
        for index in range(1, robot_count + 1)
        for sensor, message_type in (
            ("lidar_3d", "sensor_msgs/msg/PointCloud2"),
            ("imu", "sensor_msgs/msg/Imu"),
        )
    ]


def camera_stream_fields(camera_name: str) -> tuple[str, ...]:
    """Return only the image streams enabled by the canonical camera profile."""
    if camera_name not in ("camera_a", "camera_b"):
        raise ValueError(f"Invalid camera: {camera_name}")
    fields = ["color_topic"]
    if load_profile()["canonical"][camera_name]["depth_enabled"]:
        fields.append("depth_topic")
    return tuple(fields)


def rviz_streams(simulator: str, index: int) -> list[tuple[str, str, str]]:
    labels = {
        ("camera_a", "color_topic"): "front RGB",
        ("camera_a", "depth_topic"): "front depth",
        ("camera_b", "color_topic"): "top RGB",
        ("camera_b", "depth_topic"): "top depth",
    }
    images = [
        ("rviz_default_plugins/Image", labels[(camera, field)], topic(simulator, index, camera, field))
        for camera in ("camera_a", "camera_b")
        for field in camera_stream_fields(camera)
    ]
    return images + [
        ("rviz_default_plugins/PointCloud2", "3D lidar", topic(simulator, index, "lidar_3d")),
    ]
