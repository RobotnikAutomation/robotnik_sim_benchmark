import csv
import json
import sys
from pathlib import Path

import pytest

SCRIPT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPT_ROOT))

from report.results import (  # noqa: E402
    ITERATION_HEADER,
    ROS_TOPIC_HEADER,
    PerformanceResultsWriter,
    RosResultsWriter,
)


def _iteration_row():
    return ["webots", "2026-01-01T00:00:00", 1, 1.0, 2.0] + [None] * (len(ITERATION_HEADER) - 5)


def test_iteration_csv_preserves_schema_and_null_values(tmp_path):
    writer = PerformanceResultsWriter(tmp_path / "results.csv")
    writer.write_iteration(_iteration_row())
    with (tmp_path / "results.csv").open(newline="") as stream:
        rows = list(csv.reader(stream))
    assert rows[0] == ITERATION_HEADER
    assert rows[1][0:5] == ["webots", "2026-01-01T00:00:00", "1", "1.0", "2.0"]
    assert rows[1][-1] == ""


def test_iteration_csv_rejects_wrong_schema_length(tmp_path):
    writer = PerformanceResultsWriter(tmp_path / "results.csv")
    with pytest.raises(ValueError, match="current schema requires"):
        writer.write_iteration(["too short"])


def test_ros_topic_csv_and_metadata_are_written(tmp_path):
    ros_writer = RosResultsWriter(tmp_path / "ros.csv")
    ros_writer.write_ros_topics(
        "webots", "one_robot_empty_world", 1, "now",
        [{"topic": "/camera", "topic_type": "sensor_msgs/msg/Image", "publisher_count": 1,
          "message_count": 2, "rate_hz": 2.0, "payload_mib_s": None, "max_gap_seconds": 0.5}],
    )
    metadata = PerformanceResultsWriter(tmp_path / "results.csv").write_metadata(
        {"simulator": "webots", "category": "one_robot_empty_world"}
    )
    assert metadata.exists()
    assert json.loads(metadata.read_text())["schema_version"] == 3
    with (tmp_path / "ros.csv").open(newline="") as stream:
        assert next(csv.reader(stream)) == ROS_TOPIC_HEADER
