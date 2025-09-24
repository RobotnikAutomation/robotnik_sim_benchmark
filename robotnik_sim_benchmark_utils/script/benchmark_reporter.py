#!/usr/bin/env python3
"""
Monitor a PID and its children: CPU% (0–100), RAM MB, total NVIDIA GPU util% and GPU MB, and this PID's GPU MB.
No ROS. Works on Linux with psutil and nvidia-smi.
"""

import argparse
import time
import psutil
import subprocess as sp
from datetime import datetime
import csv
import os
import math
from typing import List, Optional, Tuple

MI_B = 1024 * 1024


def get_children(proc: psutil.Process) -> List[psutil.Process]:
    procs = []
    try:
        if proc.is_running():
            procs.append(proc)
            procs.extend(proc.children(recursive=True))
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        pass
    alive = []
    for p in procs:
        try:
            if p.is_running():
                alive.append(p)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return alive


class CpuAggregator:
    """Tree CPU% using cpu_times() deltas across PID + children. Normalized by logical CPUs."""
    def __init__(self):
        self.prev = {}          # pid -> cpu_seconds (user+system)
        self.last_wall = None
        self.ncpu = psutil.cpu_count(logical=True) or 1

    def sample(self, procs: List[psutil.Process]) -> Tuple[float, float]:
        """Return (cpu_total_percent_0_100, ram_mb_total)."""
        now = time.time()
        cur = {}
        rss_sum = 0
        for p in procs:
            try:
                t = p.cpu_times()
                cur[p.pid] = (t.user + t.system)
                rss_sum += p.memory_info().rss
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        cpu_pct = 0.0
        if self.last_wall is not None:
            dt = now - self.last_wall
            if dt > 0:
                dproc = 0.0
                for pid, v in cur.items():
                    pv = self.prev.get(pid)
                    if pv is not None:
                        d = v - pv
                        if d > 0:
                            dproc += d
                cpu_pct = 100.0 * dproc / (dt * self.ncpu)

        self.prev = cur
        self.last_wall = now
        return cpu_pct, rss_sum / MI_B


def nvidia_totals() -> Tuple[Optional[float], Optional[float]]:
    """Return (gpu_util_percent_total, gpu_mem_used_mib_total) or (None, None)."""
    try:
        out = sp.run(
            ['nvidia-smi',
             '--query-gpu=utilization.gpu,memory.used',
             '--format=csv,noheader,nounits'],
            capture_output=True, text=True, check=True, timeout=2.0
        ).stdout.strip()
        if not out:
            return None, None
        util_t = 0.0
        mem_t = 0.0
        for line in out.splitlines():
            util, mem = [x.strip() for x in line.split(',')]
            util_t += float(util)
            mem_t += float(mem)
        return util_t, mem_t
    except Exception:
        return None, None


def nvidia_pid_mem_mib(pid: int) -> Optional[float]:
    """Total GPU memory MiB used by this PID across GPUs, if NVIDIA. Else None."""
    try:
        out = sp.run(
            ['nvidia-smi',
             '--query-compute-apps=pid,used_memory',
             '--format=csv,noheader,nounits'],
            capture_output=True, text=True, check=True, timeout=2.0
        ).stdout.strip()
        if not out:
            return None
        total = 0.0
        for line in out.splitlines():
            parts = [x.strip() for x in line.split(',')]
            if len(parts) != 2:
                continue
            apid, mem = parts
            if apid.isdigit() and int(apid) == pid:
                total += float(mem)
        # If present but zero, return 0.0; if not present return None
        return total if total > 0.0 else 0.0
    except Exception:
        return None


def write_csv_header(path: str) -> None:
    if os.path.isfile(path):
        return
    os.makedirs(os.path.dirname(path) or '.', exist_ok=True)
    with open(path, 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow([
            'timestamp_iso', 'pid', 'proc_name',
            'cpu_percent_total', 'ram_mb_total',
            'gpu_util_percent_total', 'gpu_mem_mb_total',
            'pid_gpu_mem_mb'
        ])


def write_csv_row(path: str, row: list) -> None:
    with open(path, 'a', newline='') as f:
        csv.writer(f).writerow(row)


def mean(xs: List[float]) -> Optional[float]:
    return sum(xs) / len(xs) if xs else None


def main():
    ap = argparse.ArgumentParser(description="Monitor a PID and its children. No ROS.")
    ap.add_argument('--pid', type=int, required=True, help='Root process ID to monitor')
    ap.add_argument('--interval', type=float, default=0.5, help='Sampling interval seconds')
    ap.add_argument('--duration', type=float, default=60, help='Total seconds to monitor')
    ap.add_argument('--csv', type=str, default='', help='Optional CSV output path')
    ap.add_argument('--quiet', action='store_true', help='Suppress per-sample prints')
    args = ap.parse_args()

    try:
        root = psutil.Process(args.pid)
        name = root.name()
    except psutil.NoSuchProcess:
        print(f"PID {args.pid} not found")
        return

    if args.csv:
        write_csv_header(args.csv)

    tracker = CpuAggregator()

    # Prime
    procs = get_children(root)
    tracker.sample(procs)

    t0 = time.time()
    next_t = t0 + args.interval

    cpu_vals = []
    ram_vals = []
    gpu_util_vals = []
    gpu_mem_vals = []
    pid_gpu_mem_vals = []

    # align to interval
    while time.time() < next_t:
        time.sleep(0.01)

    while True:
        if time.time() - t0 >= args.duration:
            break
        try:
            if not root.is_running():
                break
        except psutil.NoSuchProcess:
            break

        procs = get_children(root)

        # keep steady interval
        now = time.time()
        delay = max(0.0, next_t - now)
        if delay > 0:
            time.sleep(delay)
        next_t += args.interval

        cpu_percent, ram_mb = tracker.sample(procs)
        g_util, g_mem = nvidia_totals()
        pid_gmem = nvidia_pid_mem_mib(args.pid)

        cpu_vals.append(cpu_percent)
        ram_vals.append(ram_mb)
        if g_util is not None:
            gpu_util_vals.append(g_util)
        if g_mem is not None:
            gpu_mem_vals.append(g_mem)
        if pid_gmem is not None:
            pid_gpu_mem_vals.append(pid_gmem)

        ts = datetime.utcnow().isoformat()
        if args.csv:
            write_csv_row(args.csv, [
                ts, args.pid, name,
                f"{cpu_percent:.2f}", f"{ram_mb:.2f}",
                f"{g_util:.2f}" if g_util is not None else '',
                f"{g_mem:.2f}" if g_mem is not None else '',
                f"{pid_gmem:.2f}" if pid_gmem is not None else ''
            ])

        if not args.quiet:
            print(
                f"{ts} pid={args.pid} {name} | "
                f"CPU%={cpu_percent:.2f} RAM_MB={ram_mb:.2f} | "
                f"GPU_UTIL%_TOTAL={(g_util if g_util is not None else math.nan):.2f} "
                f"GPU_MEM_MB_TOTAL={(g_mem if g_mem is not None else math.nan):.2f} "
                f"PID_GPU_MEM_MB={(pid_gmem if pid_gmem is not None else math.nan):.2f}"
            )

    summary = {
        'pid': args.pid,
        'name': name,
        'samples': len(cpu_vals),
        'cpu_percent_mean': mean(cpu_vals),
        'ram_mb_mean': mean(ram_vals),
        'gpu_util_percent_total_mean': mean(gpu_util_vals),
        'gpu_mem_mb_total_mean': mean(gpu_mem_vals),
        'pid_gpu_mem_mb_mean': mean(pid_gpu_mem_vals),
        'duration_s': round(time.time() - t0, 3)
    }

    print("\nSummary:")
    for k, v in summary.items():
        if isinstance(v, float) and v is not None:
            print(f"{k}: {v:.2f}")
        else:
            print(f"{k}: {v}")


if __name__ == "__main__":
    main()
