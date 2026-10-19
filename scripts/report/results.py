"""Persistence of benchmark iteration results and session metadata."""
from __future__ import annotations
import csv
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any

ITERATION_HEADER = [
    "simulator", "timestamp", "iteration", "first_frame_seconds",
    "startup_time", "cpu_mean_percent", "cpu_core_peak_mean_percent",
    "cpu_core_saturated_mean_count", "ram_mean_mb", "gpu_mean_percent",
    "gpu_memory_util_mean_percent", "gpu_temperature_mean_c", "gpu_power_mean_w",
    "gpu_clock_mean_mhz", "gpu_mem_mean_mb", "real_time_factor_mean",
    "real_time_factor_global", "real_time_factor_sample_count",
    "rtf_clock_message_count", "rtf_clock_reset_count", "rtf_clock_max_gap_seconds",
    "iteration_total_time", "monitor_ros", "image_topic_rate_mean_hz",
    "image_topic_rate_min_hz", "image_payload_total_mib_s", "image_max_gap_seconds",
    "image_message_count_total", "render_fps_cap", "render_fps_mean",
]
ROS_TOPIC_HEADER = [
    "simulator", "category", "timestamp", "iteration", "topic", "topic_type",
    "publisher_count", "message_count", "rate_hz", "payload_mib_s",
    "max_gap_seconds",
]

class PerformanceResultsWriter:
    """Write benchmark performance rows and session metadata."""

    def __init__(self, csv_path: Path):
        self.csv_path = Path(csv_path)

    @staticmethod
    def _append_row(path: Path, header: list[str], row: list[Any]) -> None:
        if len(row) != len(header):
            raise ValueError(f"CSV row has {len(row)} fields but the current schema requires {len(header)}")
        path.parent.mkdir(parents=True, exist_ok=True)
        exists = path.is_file()
        if exists:
            with path.open(newline="") as stream:
                if next(csv.reader(stream), []) != header:
                    raise ValueError(f"CSV schema mismatch in {path}; choose a new output path")
        with path.open("a", newline="") as stream:
            writer = csv.writer(stream)
            if not exists:
                writer.writerow(header)
            writer.writerow(row)

    def write_iteration(self, row: list[Any]) -> None:
        self._append_row(self.csv_path, ITERATION_HEADER, row)


    def write_metadata(self, context: dict[str, Any]) -> Path:
        metadata_path = self.csv_path.with_name(f"{self.csv_path.stem}.metadata.json")
        session = {
            "started_at": datetime.now().isoformat(),
            **{key: context.get(key) for key in (
                "simulator", "category", "launch_commands", "image_topics",
                "iterations", "iteration_time_seconds", "startup_timeout_seconds",
                "warmup_time_seconds", "rtf_window_seconds",
                "rtf_clock_source_contract", "rtf_clock_nominal_hz", "monitor_ros",
                "ros_topic_csv_file", "external_process_monitor", "rtf_policy",
                "render_fps_cap", "render_fps_source",
            )},
            "environment": context.get("environment", {}),
        }
        semantics = context.get("measurement_semantics", {})
        document = {
            "schema_version": 3,
            "csv_file": self.csv_path.name,
            "measurement_semantics": semantics,
            "sessions": [],
        }
        if metadata_path.exists():
            try:
                document = json.loads(metadata_path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError) as exc:
                raise ValueError(f"Cannot read existing metadata file {metadata_path}: {exc}") from exc
            if not isinstance(document, dict) or not isinstance(document.get("sessions"), list):
                raise ValueError(f"Invalid metadata document: {metadata_path}")
        document["sessions"].append(session)
        temporary = metadata_path.with_suffix(metadata_path.suffix + ".tmp")
        temporary.write_text(json.dumps(document, indent=2) + "\n", encoding="utf-8")
        os.replace(temporary, metadata_path)
        return metadata_path


class RosResultsWriter:
    """Write optional ROS transport results independently from performance data."""

    def __init__(self, csv_path: Path):
        self.csv_path = Path(csv_path)

    def write_ros_topics(self, simulator: str, category: str, iteration: int,
                         timestamp: str, rows: list[dict[str, Any]]) -> None:
        self.csv_path.parent.mkdir(parents=True, exist_ok=True)
        exists = self.csv_path.is_file()
        if exists:
            with self.csv_path.open(newline="") as stream:
                if next(csv.reader(stream), []) != ROS_TOPIC_HEADER:
                    raise ValueError(f"ROS topic CSV schema mismatch in {self.csv_path}")
        with self.csv_path.open("a", newline="") as stream:
            writer = csv.writer(stream)
            if not exists:
                writer.writerow(ROS_TOPIC_HEADER)
            for row in rows:
                writer.writerow([
                    simulator, category, timestamp, iteration, row["topic"],
                    row["topic_type"], row.get("publisher_count"),
                    row["message_count"], row["rate_hz"], row.get("payload_mib_s"),
                    row["max_gap_seconds"],
                ])
