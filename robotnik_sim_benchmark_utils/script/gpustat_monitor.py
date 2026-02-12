#!/usr/bin/env python3
import re, subprocess, psutil
from collections import defaultdict
import pynvml as nv

def have_nvml_proc_util():
    return hasattr(nv, "nvmlDeviceGetProcessUtilization")

def pmon_snapshot():
    # returns {(gpu, pid): {"sm":%, "mem":%}}
    out = subprocess.check_output(["nvidia-smi", "pmon", "-c", "1", "-s", "um"], text=True)
    data = {}
    cur_gpu = None
    for line in out.splitlines():
        if line.startswith("# gpu"):
            cur_gpu = None
            continue
        m = re.match(r"^\s*(\d+)\s+(\d+)\s+([gr])\s+(\S+)\s+(\d+)\s+(\d+)\s+(\d+)", line)
        if m:
            gpu, pid, _type, _name, sm, mem, enc = m.groups()
            cur_gpu = int(gpu)
            pid = int(pid)
            data[(cur_gpu, pid)] = {"sm": float(sm), "mem": float(mem)}
    return data

def mem_bytes_snapshot():
    # returns {(gpu, pid): MiB}
    nv.nvmlInit()
    try:
        res = {}
        for gi in range(nv.nvmlDeviceGetCount()):
            h = nv.nvmlDeviceGetHandleByIndex(gi)
            for getter in (nv.nvmlDeviceGetComputeRunningProcesses,
                           nv.nvmlDeviceGetGraphicsRunningProcesses):
                try:
                    for p in getter(h):
                        used = getattr(p, "usedGpuMemory", 0) or 0
                        res[(gi, p.pid)] = max(res.get((gi, p.pid), 0), used / (1024*1024))
                except nv.NVMLError:
                    pass
        return res
    finally:
        nv.nvmlShutdown()

def root_in_set(pid, pidset):
    try:
        p = psutil.Process(pid)
    except Exception:
        return pid
    r = p
    while True:
        try:
            par = r.parent()
        except Exception:
            break
        if not par or par.pid not in pidset:
            break
        r = par
    return r.pid

def main():
    # Try NVML per-PID %; if missing, use pmon
    try:
        nv.nvmlInit()
        nvml_ok = have_nvml_proc_util()
    finally:
        try: nv.nvmlShutdown()
        except: pass

    if nvml_ok:
        # If you do upgrade, you can reuse the original util path.
        print("Your NVML now supports per-PID utilization; use the earlier script.")
        return

    util = pmon_snapshot()                 # {(gpu,pid): {"sm":%, "mem":%}}
    mem  = mem_bytes_snapshot()            # {(gpu,pid): MiB}
    pids = {pid for (_, pid) in set(util)|set(mem)}

    # group by root
    groups = defaultdict(lambda: {"sm":0.0,"mem%":0.0,"MiB":0.0,"name":""})
    names  = {}
    for (gi, pid), u in util.items():
        names[pid] = (psutil.Process(pid).name() if psutil.pid_exists(pid) else "unknown")
    for (gi, pid), mib in mem.items():
        names.setdefault(pid, (psutil.Process(pid).name() if psutil.pid_exists(pid) else "unknown"))

    roots = {}
    for pid in pids:
        roots[pid] = root_in_set(pid, pids)

    # aggregate per GPU per root
    agg = defaultdict(lambda: defaultdict(lambda: {"sm":0.0,"mem%":0.0,"MiB":0.0,"rname":""}))
    for (gi, pid), u in util.items():
        r = roots[pid]
        agg[gi][r]["sm"]   += u.get("sm", 0.0)
        agg[gi][r]["mem%"] += u.get("mem", 0.0)
        agg[gi][r]["rname"] = names.get(r, "unknown")
    for (gi, pid), mib in mem.items():
        r = roots[pid]
        agg[gi][r]["MiB"] += mib
        agg[gi][r]["rname"] = names.get(r, "unknown")

    print("\n=== Aggregated by parent per GPU ===")
    for gi in sorted(agg):
        print(f"\nGPU {gi}")
        print(f"{'ROOT_PID':>8}  {'ROOT_PROC':<25}  {'SM%_SUM':>8}  {'MEM%_SUM':>9}  {'MiB_SUM':>9}")
        for rpid, a in sorted(agg[gi].items()):
            print(f"{rpid:8d}  {a['rname']:<25}  {a['sm']:8.1f}  {a['mem%']:9.1f}  {a['MiB']:9.1f}")

    print("\n=== Per-process ===")
    print(f"{'GPU':>3} {'PID':>7}  {'PROC':<25} {'ROOT':>7} {'RPROC':<25} {'SM%':>6} {'MEM%':>6} {'MiB':>9}")
    for (gi, pid) in sorted(set(util)|set(mem)):
        sm  = util.get((gi, pid), {}).get("sm", 0.0)
        mmu = util.get((gi, pid), {}).get("mem", 0.0)
        mib = mem.get((gi, pid), 0.0)
        r   = roots[pid]
        print(f"{gi:>3} {pid:>7}  {names.get(pid,'unknown'):<25} {r:>7} {names.get(r,'unknown'):<25} "
              f"{sm:>6.1f} {mmu:>6.1f} {mib:>9.1f}")

if __name__ == "__main__":
    main()
