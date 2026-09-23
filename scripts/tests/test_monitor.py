import csv
import sys
from pathlib import Path

import pytest

pytest.importorskip("rclpy")

SCRIPT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPT_ROOT))

from monitor.monitor import (  # noqa: E402
    BenchmarkMonitor,
    ClockListener,
    MangoHudSession,
    RealTimeFactorSampler,
    RosMonitor,
)


def test_render_fps_validation_and_headless_session(tmp_path):
    assert MangoHudSession.validate_render_fps(60) == 60
    with pytest.raises(ValueError):
        MangoHudSession.validate_render_fps(0)
    session = MangoHudSession(tmp_path, 60, enabled=False)
    assert session.wrap_command(["ros2", "launch"]) == ["ros2", "launch"]
    assert session.finish_measurement() is None


def test_mangohud_csv_processing_is_internal_to_the_session(tmp_path):
    path = tmp_path / "frames.csv"
    path.write_text("os,cpu\nUbuntu,CPU\nfps,frametime,elapsed\n60,16,1\n59,17,2\n")
    assert MangoHudSession._max_elapsed_from_csv(path) == 2
    assert MangoHudSession._mean_fps_from_csv(path, minimum_elapsed=1) == pytest.approx(59)


def test_mangohud_summary_csv_uses_average_fps(tmp_path):
    path = tmp_path / "frames_summary.csv"
    with path.open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=["Average FPS", "GPU Load"])
        writer.writeheader()
        writer.writerow({"Average FPS": "59.8", "GPU Load": "10"})
    assert MangoHudSession._mean_fps_from_csv(path) == pytest.approx(59.8)


def test_rtf_windows_and_global_ratio_are_distinct():
    sampler = RealTimeFactorSampler(window_seconds=1.0)
    sampler.add_clock(0.0, 0.0)
    sampler.add_clock(1.0, 1.0)
    sampler.add_clock(1.4, 2.5)
    assert len(sampler.window_samples) == 2
    assert sampler.window_mean() == pytest.approx((1.0 + 0.4 / 1.5) / 2)
    assert sampler.global_ratio() == pytest.approx(1.4 / 2.5)
    assert sampler.required_window_samples(5) == 3


def test_rtf_rewind_resets_the_current_span():
    sampler = RealTimeFactorSampler(window_seconds=1.0)
    sampler.add_clock(10.0, 0.0)
    sampler.add_clock(11.0, 1.0)
    sampler.add_clock(0.0, 2.0)
    sampler.add_clock(0.5, 3.0)
    assert sampler.rewind_count == 1
    assert sampler.global_ratio() == pytest.approx(0.5)


def test_clock_listener_rejects_incomplete_measurements():
    listener = ClockListener.__new__(ClockListener)
    listener.rtf_lock = __import__("threading").Lock()
    listener.message_count = 1
    listener.rtf_sampler = RealTimeFactorSampler(1.0)
    with pytest.raises(RuntimeError, match="fewer than two"):
        listener.validate_measurement(10)


def test_readiness_result_is_grouped_inside_benchmark_monitor():
    assert hasattr(BenchmarkMonitor, "ReadinessResult")
    result = BenchmarkMonitor.ReadinessResult(True, 1.0, 2.0)
    assert result.ready is True
    assert result.startup_seconds == 2.0


def test_ros_monitor_keeps_rclpy_subscription_storage_separate():
    monitor = RosMonitor.__new__(RosMonitor)
    monitor.excluded_topics = set()
    monitor._records = {}
    monitor._topic_subscriptions = {}
    monitor._lock = __import__("threading").Lock()
    monitor.discovery_errors = []
    monitor.get_publishers_info_by_topic = lambda _topic: [object(), object()]
    monitor.create_subscription = lambda *_args, **_kwargs: "subscription"
    monkeypatch = pytest.MonkeyPatch()
    monkeypatch.setattr("monitor.monitor.get_message", lambda _name: bytes)
    try:
        assert monitor.subscribe("/camera", "sensor_msgs/msg/Image")
        assert monitor._topic_subscriptions == {"/camera": "subscription"}
    finally:
        monkeypatch.undo()
