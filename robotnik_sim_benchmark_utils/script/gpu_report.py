#!/usr/bin/env python3
import argparse
import csv
import json
import shutil
import subprocess
import sys
import time
from typing import List, Dict

def _check_nvidia_smi() -> None:
    if not shutil.which("nvidia-smi"):
        sys.stderr.write("nvidia-smi not found in PATH.\n")
        sys.exit(1)

def _run(cmd: List[str]) -> str:
    try:
        out = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
        return out.decode("utf-8", errors="replace").strip()
    except subprocess.CalledProcessError as e:
        sys.stderr.write(e.output.decode("utf-8", errors="replace"))
        sys.exit(e.returncode)

def _query(target: str, fields: List[str]) -> List[Dict[str, str]]:
    """
    target: 'gpu' or 'compute-apps'
    fields: nvidia-smi --query-<target> fields
    """
    base = ["nvidia-smi", f"--query-{target}", ",".join(fields),
            "--format=csv,noheader,nounits"]
    raw = _run(base)
    if not raw:
        return []

    # Parse CSV robustly
    rows = []
    reader = csv.reader(raw.splitlines())
    for row in reader:
        # pad if short
        if len(row) < len(fields):
            row += [""] * (len(fields) - len(row))
        rows.append({fields[i]: row[i].strip() for i in range(len(fields))})
    return rows

def collect_once() -> Dict:
    # GPU-level stats
    gpu_fields = [
        "index",
        "uuid",
        "name",
        "driver_version",
        "temperature.gpu",
        "utilization.gpu",
        "utilization.memory",
        "memory.total",
        "memory.used",
        "memory.free",
        "power.draw",
        "power.limit",
        "pstate",
        "fan.speed",
        "clocks.sm",
        "clocks.mem",
        "pcie.link.gen.current",
        "pcie.link.width.current",
    ]
    gpus = _query("gpu", gpu_fields)

    # Process-level stats (may be empty)
    proc_fields = [
        "gpu_uuid",
        "pid",
        "process_name",
        "used_memory",
    ]
    procs = _query("compute-apps", proc_fields)

    # Map processes to GPUs by uuid
    by_uuid = {}
    for g in gpus:
        g_copy = dict(g)
        g_copy["processes"] = []
        by_uuid[g["uuid"]] = g_copy

    for p in procs:
        u = p.get("gpu_uuid")
        if u in by_uuid:
            by_uuid[u]["processes"].append({
                "pid": p.get("pid"),
                "name": p.get("process_name"),
                "vram_used": p.get("used_memory")  # MiB, nounits
            })

    # Convert strings that are numeric into numbers where sensible
    def to_num(s):
        try:
            if s is None or s == "":
                return None
            if "." in s:
                return float(s)
            return int(s)
        except Exception:
            return s

    # Normalize fields
    out = []
    for gpu in by_uuid.values():
        norm = {
            "index": to_num(gpu.get("index")),
            "uuid": gpu.get("uuid"),
            "name": gpu.get("name"),
            "driver_version": gpu.get("driver_version"),
            "temperature_c": to_num(gpu.get("temperature.gpu")),
            "util_gpu_pct": to_num(gpu.get("utilization.gpu")),
            "util_mem_pct": to_num(gpu.get("utilization.memory")),
            "mem_total_mib": to_num(gpu.get("memory.total")),
            "mem_used_mib": to_num(gpu.get("memory.used")),
            "mem_free_mib": to_num(gpu.get("memory.free")),
            "power_draw_w": to_num(gpu.get("power.draw")),
            "power_limit_w": to_num(gpu.get("power.limit")),
            "pstate": gpu.get("pstate"),
            "fan_speed_pct": to_num(gpu.get("fan.speed")),
            "clock_sm_mhz": to_num(gpu.get("clocks.sm")),
            "clock_mem_mhz": to_num(gpu.get("clocks.mem")),
            "pcie_gen": to_num(gpu.get("pcie.link.gen.current")),
            "pcie_width": to_num(gpu.get("pcie.link.width.current")),
            "processes": gpu.get("processes", []),
        }
        out.append(norm)

    return {"gpus": sorted(out, key=lambda x: x["index"] if x["index"] is not None else 1e9)}

def main():
    parser = argparse.ArgumentParser(
        description="Report GPU usage and processes via nvidia-smi")
    parser.add_argument("--watch", type=float, help="Refresh interval in seconds")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON")
    parser.add_argument("--once", action="store_true", help="Collect once and exit")
    args = parser.parse_args()

    _check_nvidia_smi()

    def emit():
        data = collect_once()
        if args.pretty:
            print(json.dumps(data, indent=2, sort_keys=False))
        else:
            print(json.dumps(data, separators=(",", ":"), sort_keys=False))

    if args.watch:
        try:
            while True:
                emit()
                sys.stdout.flush()
                time.sleep(args.watch)
        except KeyboardInterrupt:
            pass
    else:
        emit()

if __name__ == "__main__":
    main()
