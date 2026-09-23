"""Generate a Markdown report from optional ROS topic result CSV files."""
from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from pathlib import Path


def _number(row: dict[str, str], field: str) -> float | None:
    value = (row.get(field) or "").strip()
    try:
        return float(value) if value else None
    except ValueError:
        return None


def collect_rows(benchmarks_dir: Path) -> list[dict[str, str]]:
    """Read optional ROS topic CSVs recursively."""
    rows: list[dict[str, str]] = []
    for path in sorted(benchmarks_dir.rglob("ros_topic_stats_*.csv")):
        with path.open(newline="", encoding="utf-8-sig") as stream:
            reader = csv.DictReader(stream)
            if reader.fieldnames and {"topic", "topic_type"}.issubset(reader.fieldnames):
                rows.extend(reader)
    return rows


def render_report(rows: list[dict[str, str]]) -> str:
    groups: dict[tuple[str, str, str, str], list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        key = (row.get("simulator", ""), row.get("category", ""), row.get("topic", ""), row.get("topic_type", ""))
        groups[key].append(row)

    lines = ["# ROS benchmark report", ""]
    if not groups:
        return "\n".join(lines + ["No ROS results were found. ROS monitoring may be disabled.", ""])
    lines.extend([
        "| Simulator | Category | Topic | Type | Samples | Mean rate (Hz) | Mean payload (MiB/s) |",
        "|---|---|---|---|---:|---:|---:|",
    ])
    for (simulator, category, topic, topic_type), group in sorted(groups.items()):
        rates = [_number(row, "rate_hz") for row in group]
        rates = [value for value in rates if value is not None]
        payloads = [_number(row, "payload_mib_s") for row in group]
        payloads = [value for value in payloads if value is not None]
        rate = f"{sum(rates) / len(rates):.2f}" if rates else "n/a"
        payload = f"{sum(payloads) / len(payloads):.2f}" if payloads else "n/a"
        lines.append(f"| {simulator or 'n/a'} | {category or 'n/a'} | `{topic or 'n/a'}` | `{topic_type or 'n/a'}` | {len(group)} | {rate} | {payload} |")
    return "\n".join(lines + [""])


def main() -> int:
    repository_root = Path(__file__).resolve().parents[2]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--benchmarks-dir", type=Path, default=repository_root / "benchmarks")
    parser.add_argument("--output", type=Path, default=repository_root / "ros_report.md")
    args = parser.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(render_report(collect_rows(args.benchmarks_dir)), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
