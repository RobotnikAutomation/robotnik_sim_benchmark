"""Generate a compact Markdown report from performance benchmark CSV files."""
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
    """Read performance CSVs recursively, ignoring metadata and malformed headers."""
    rows: list[dict[str, str]] = []
    for path in sorted(benchmarks_dir.rglob("ros2_launch_timings_*.csv")):
        with path.open(newline="", encoding="utf-8-sig") as stream:
            reader = csv.DictReader(stream)
            if reader.fieldnames and "simulator" in reader.fieldnames:
                rows.extend(reader)
    return rows


def render_report(rows: list[dict[str, str]]) -> str:
    groups: dict[tuple[str, str, str], list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        key = (row.get("simulator", ""), row.get("category", ""), row.get("render_fps_cap", ""))
        groups[key].append(row)

    lines = ["# Performance benchmark report", ""]
    if not groups:
        return "\n".join(lines + ["No performance results were found.", ""])
    lines.append("| Simulator | Category | FPS cap | Iterations | Startup mean (s) | RTF mean | FPS mean | CPU mean (%) | GPU mean (%) |")
    lines.append("|---|---|---:|---:|---:|---:|---:|---:|---:|")
    for (simulator, category, fps_cap), group in sorted(groups.items()):
        def mean(field: str) -> str:
            values = [_number(row, field) for row in group]
            values = [value for value in values if value is not None]
            return f"{sum(values) / len(values):.2f}" if values else "n/a"

        lines.append(
            f"| {simulator or 'n/a'} | {category or 'n/a'} | {fps_cap or 'n/a'} "
            f"| {len(group)} | {mean('startup_time')} | {mean('real_time_factor_mean')} "
            f"| {mean('render_fps_mean')} | {mean('cpu_mean_percent')} | {mean('gpu_mean_percent')} |"
        )
    return "\n".join(lines + [""])


def main() -> int:
    repository_root = Path(__file__).resolve().parents[2]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--benchmarks-dir", type=Path, default=repository_root / "benchmarks")
    parser.add_argument("--output", type=Path, default=repository_root / "performance_report.md")
    args = parser.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(render_report(collect_rows(args.benchmarks_dir)), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
