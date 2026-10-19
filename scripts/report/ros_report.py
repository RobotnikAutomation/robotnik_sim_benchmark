"""Generate a Markdown report from optional ROS topic result CSV files."""
from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from pathlib import Path


ROBOT_COUNTS = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
}


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
                for row in reader:
                    row["category"] = row.get("category") or path.parent.name
                    row["_source_file"] = str(path)
                    rows.append(row)
    return rows


def _category_dimensions(category: str) -> tuple[str, str, str]:
    """Return robot count, world name, and execution mode for a category."""
    parts = category.split("_")
    if len(parts) >= 3 and parts[1] == "robot":
        robots = ROBOT_COUNTS.get(parts[0], parts[0])
        parts = parts[2:]
    else:
        robots = "n/a"

    modes = []
    while parts and parts[-1] in {"rviz", "headless"}:
        modes.insert(0, parts.pop())
    world = "_".join(parts) or "n/a"
    mode = "+".join(modes) if modes else "default"
    return robots, world, mode


def _iterations(group: list[dict[str, str]]) -> set[tuple[str, str]]:
    return {
        (row.get("_source_file", ""), row.get("iteration", ""))
        for row in group
    }


def _mean(group: list[dict[str, str]], field: str, decimals: int = 2) -> str:
    values = [_number(row, field) for row in group]
    values = [value for value in values if value is not None]
    return f"{sum(values) / len(values):.{decimals}f}" if values else "n/a"


def render_report(rows: list[dict[str, str]]) -> str:
    groups: dict[tuple[str, str, str, str], list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        key = (row.get("simulator", ""), row.get("category", ""), row.get("topic", ""), row.get("topic_type", ""))
        groups[key].append(row)

    lines = ["# ROS benchmark report", ""]
    if not groups:
        return "\n".join(lines + ["No ROS results were found. ROS monitoring may be disabled.", ""])
    simulators: dict[str, list[tuple[str, str, str, str, list[dict[str, str]]]]] = defaultdict(list)
    for (simulator, category, topic, topic_type), group in sorted(groups.items()):
        simulators[simulator].append((category, topic, topic_type, simulator, group))

    for simulator, simulator_groups in sorted(simulators.items()):
        lines.extend([
            f"## {simulator or 'Unknown simulator'}",
            "### Summary",
            "",
            "| Robots | World | Modes | Iterations | Topics | Messages | Mean rate (Hz) | Mean payload (MiB/s) |",
            "|---:|---|---|---:|---:|---:|---:|---:|",
        ])

        summary_groups: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
        summary_modes: dict[tuple[str, str], set[str]] = defaultdict(set)
        for category, _topic, _topic_type, _simulator, group in simulator_groups:
            robots, world, mode = _category_dimensions(category)
            summary_groups[(robots, world)].extend(group)
            summary_modes[(robots, world)].add(mode)
        for (robots, world), group in sorted(summary_groups.items()):
            topics = {row.get("topic", "") for row in group}
            messages = [
                value for value in (_number(row, "message_count") for row in group)
                if value is not None
            ]
            lines.append(
                f"| {robots} | {world} | {', '.join(sorted(summary_modes[(robots, world)]))} "
                f"| {len(_iterations(group))} "
                f"| {len(topics)} | {int(sum(messages)) if messages else 'n/a'} "
                f"| {_mean(group, 'rate_hz')} | {_mean(group, 'payload_mib_s')} |"
            )

        lines.extend([
            "",
            "<details>",
            f"<summary>{simulator or 'Unknown simulator'} details</summary>",
            "",
            "### Categories",
            "",
        ])
        current_category = None
        for category, topic, topic_type, _simulator, group in simulator_groups:
            if category != current_category:
                if current_category is not None:
                    lines.extend(["", "</details>", ""])
                lines.extend([
                    "<details>",
                    f"<summary>{category or 'Unknown category'}</summary>",
                    "",
                    "| Topic | Type | Iterations | Messages | Mean rate (Hz) | Mean payload (MiB/s) | Max gap (s) |",
                    "|---|---|---:|---:|---:|---:|---:|",
                ])
                current_category = category
            gaps = [
                value for value in (_number(row, "max_gap_seconds") for row in group)
                if value is not None
            ]
            messages = [
                value for value in (_number(row, "message_count") for row in group)
                if value is not None
            ]
            max_gap = f"{max(gaps):.3f}" if gaps else "n/a"
            lines.append(
                f"| `{topic or 'n/a'}` | `{topic_type or 'n/a'}` | {len(_iterations(group))} "
                f"| {int(sum(messages)) if messages else 'n/a'} | {_mean(group, 'rate_hz')} "
                f"| {_mean(group, 'payload_mib_s')} | {max_gap} |"
            )
        if current_category is not None:
            lines.extend(["", "</details>"])
        lines.extend(["", "</details>", ""])
    return "\n".join(lines + [""])


def main() -> int:
    repository_root = Path(__file__).resolve().parents[2]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--benchmarks-dir", type=Path, default=repository_root / "benchmarks")
    parser.add_argument(
        "--output", type=Path,
        default=repository_root / "benchmarks" / "summary" / "ros_report.md",
    )
    args = parser.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(render_report(collect_rows(args.benchmarks_dir)), encoding="utf-8")
    print(f"ROS report generated: {args.output.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
