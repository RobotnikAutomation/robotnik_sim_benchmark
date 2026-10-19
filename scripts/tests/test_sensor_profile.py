import sys
from pathlib import Path

import pytest

SCRIPT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPT_ROOT))

from common.sensor_profile import (  # noqa: E402
    SIMULATORS,
    camera_stream_fields,
    expected_nonimage_sensor_topics,
    load_profile,
    namespace,
    physics_clock_rate_hz,
    robot_name,
    rviz_streams,
    topic,
)
from validate.validate_config import CATEGORIES, load_config  # noqa: E402


def test_profile_is_complete_and_consistent():
    profile = load_profile()
    assert tuple(profile["simulators"]) == SIMULATORS
    lidar = profile["canonical"]["lidar_3d"]
    assert int(lidar["channels"]) * int(lidar["horizontal_samples"]) == int(lidar["points_per_scan"])
    assert profile["canonical"]["camera_a"]["depth_enabled"] is False
    assert profile["canonical"]["camera_b"]["depth_enabled"] is True


@pytest.mark.parametrize("simulator", SIMULATORS)
def test_each_backend_exposes_the_canonical_rviz_workload(simulator):
    streams = rviz_streams(simulator, 1)
    assert [stream[0] for stream in streams].count("rviz_default_plugins/Image") == 3
    assert [stream[0] for stream in streams].count("rviz_default_plugins/PointCloud2") == 1


def test_namespaces_and_topics_are_backend_specific_and_stable():
    assert namespace("gazebo_harmonic", 2) == "/rbwatcher_2"
    assert namespace("webots", 2) == "/rbwatcher2/rbwatcher2"
    assert namespace("unity", 1) == "/robot"
    assert robot_name("unity", 2) == "robot_2"
    assert topic("webots", 1, "imu") == "/rbwatcher1/imu/data"
    assert camera_stream_fields("camera_a") == ("color_topic",)
    assert camera_stream_fields("camera_b") == ("color_topic", "depth_topic")


def test_nonimage_topics_cover_each_robot():
    assert expected_nonimage_sensor_topics("gazebo_harmonic", "two_robot_empty_world_rviz") == [
        ("/rbwatcher_1/top_laser/points", "sensor_msgs/msg/PointCloud2"),
        ("/rbwatcher_1/imu/data", "sensor_msgs/msg/Imu"),
        ("/rbwatcher_2/top_laser/points", "sensor_msgs/msg/PointCloud2"),
        ("/rbwatcher_2/imu/data", "sensor_msgs/msg/Imu"),
    ]


def test_configured_readiness_topics_match_the_profile():
    config = load_config()
    counts = {"one": 1, "two": 2, "three": 3}
    for simulator in SIMULATORS:
        for category in CATEGORIES:
            count = counts[category.split("_", 1)[0]]
            expected = [
                topic(simulator, index, camera, stream)
                for index in range(1, count + 1)
                for camera in ("camera_a", "camera_b")
                for stream in camera_stream_fields(camera)
            ]
            assert config[simulator][category]["TOPICS_TO_LISTEN"] == expected
