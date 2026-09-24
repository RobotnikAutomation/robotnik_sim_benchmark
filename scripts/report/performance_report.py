"""Generate a compact Markdown report from performance benchmark CSV files."""
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
    """Read performance CSVs recursively, ignoring metadata and malformed headers."""
    rows: list[dict[str, str]] = []
    for path in sorted(benchmarks_dir.rglob("ros2_launch_timings_*.csv")):
        with path.open(newline="", encoding="utf-8-sig") as stream:
            reader = csv.DictReader(stream)
            if reader.fieldnames and "simulator" in reader.fieldnames:
                for row in reader:
                    # The iteration CSV schema predates the category column.
                    # The result directory is the authoritative category.
                    row["category"] = row.get("category") or path.parent.name
                    row["_source_file"] = str(path)
                    rows.append(row)
    return rows


def _category_dimensions(category: str) -> tuple[str, str, str]:
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


def _mean(group: list[dict[str, str]], field: str) -> str:
    values = [_number(row, field) for row in group]
    values = [value for value in values if value is not None]
    return f"{sum(values) / len(values):.2f}" if values else "n/a"


def _fps_label(row: dict[str, str]) -> str:
    return row.get("render_fps_cap") or "n/a"


def render_report(rows: list[dict[str, str]]) -> str:
    groups: dict[tuple[str, str, str], list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        key = (row.get("simulator", ""), row.get("category", ""), row.get("render_fps_cap", ""))
        groups[key].append(row)

    lines = ["# Performance benchmark report", ""]
    if not groups:
        return "\n".join(lines + ["No performance results were found.", ""])
    simulators: dict[str, list[tuple[str, str, str, list[dict[str, str]]]]] = defaultdict(list)
    for (simulator, category, fps_cap), group in sorted(groups.items()):
        simulators[simulator].append((category, fps_cap, simulator, group))

    for simulator, simulator_groups in sorted(simulators.items()):
        lines.extend([
            f"## {simulator or 'Unknown simulator'}",
            "### Summary",
            "",
            "| Robots | World | Modes | Measurements | Startup mean (s) | RTF mean | FPS mean | CPU mean (%) | GPU mean (%) |",
            "|---:|---|---|---:|---:|---:|---:|---:|---:|",
        ])
        summary_groups: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
        summary_modes: dict[tuple[str, str], set[str]] = defaultdict(set)
        for category, fps_cap, _simulator, group in simulator_groups:
            robots, world, mode = _category_dimensions(category)
            summary_groups[(robots, world)].extend(group)
            summary_modes[(robots, world)].add(f"{mode}@{fps_cap or 'n/a'}")
        for (robots, world), group in sorted(summary_groups.items()):
            lines.append(
                f"| {robots} | {world} | {', '.join(sorted(summary_modes[(robots, world)]))} "
                f"| {len(group)} | {_mean(group, 'startup_time')} | {_mean(group, 'real_time_factor_mean')} "
                f"| {_mean(group, 'render_fps_mean')} | {_mean(group, 'cpu_mean_percent')} "
                f"| {_mean(group, 'gpu_mean_percent')} |"
            )

        lines.extend([
            "",
            "<details>",
            f"<summary>{simulator or 'Unknown simulator'} details</summary>",
            "",
            "| Category | FPS cap | Measurements | Startup mean (s) | RTF mean | FPS mean | CPU mean (%) | GPU mean (%) |",
            "|---|---:|---:|---:|---:|---:|---:|---:|",
        ])
        for category, fps_cap, _simulator, group in simulator_groups:
            lines.append(
                f"| {category or 'n/a'} | {_fps_label(group[0])} | {len(group)} "
                f"| {_mean(group, 'startup_time')} | {_mean(group, 'real_time_factor_mean')} "
                f"| {_mean(group, 'render_fps_mean')} | {_mean(group, 'cpu_mean_percent')} "
                f"| {_mean(group, 'gpu_mean_percent')} |"
            )
        lines.extend(["", "</details>", ""])
    return "\n".join(lines + [""])


def main() -> int:
    repository_root = Path(__file__).resolve().parents[2]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--benchmarks-dir", type=Path, default=repository_root / "benchmarks")
    parser.add_argument(
        "--output", type=Path,
        default=repository_root / "benchmarks" / "summary" / "performance_report.md",
    )
    args = parser.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(render_report(collect_rows(args.benchmarks_dir)), encoding="utf-8")
    print(f"Performance report generated: {args.output.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
