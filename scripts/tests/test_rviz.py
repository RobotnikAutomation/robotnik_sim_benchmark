import sys
from pathlib import Path

SCRIPT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPT_ROOT))

from execute import run_rviz  # noqa: E402


def _topics(config):
    return {
        display["Topic"]["Value"]
        for display in config["Visualization Manager"]["Displays"]
        if "Topic" in display
    }


def test_config_contains_exactly_the_requested_robot_topics():
    topics = _topics(run_rviz.build_config("unity", 3))
    assert "/robot/front_rgbd_camera/color/image_raw" in topics
    assert "/robot_2/top_rgbd_camera/depth/image_raw" in topics
    assert "/robot_3/points" in topics
    assert "/robot_4/front_rgbd_camera/color/image_raw" not in topics


def test_backend_specific_topics_and_frames_are_preserved():
    config = run_rviz.build_config("webots", 2)
    topics = _topics(config)
    assert "/rbwatcher1/rbwatcher1/front_rgbd_camera_color/image_color" in topics
    assert "/rbwatcher2/rbwatcher2/rbwatcher2_top_3d_laser_link/point_cloud" in topics
    assert run_rviz._fixed_frame("webots") == "world"
    assert run_rviz._fixed_frame("gazebo_harmonic") == "benchmark_world"


def test_multirobot_static_transforms_are_deterministic():
    specs = run_rviz._static_transform_specs("gazebo_harmonic", ["rbwatcher_1", "rbwatcher_2"])
    assert specs == [("rbwatcher_1_odom", 0.0, 0.0, 0.0), ("rbwatcher_2_odom", 1.0, 1.0, 0.0)]
