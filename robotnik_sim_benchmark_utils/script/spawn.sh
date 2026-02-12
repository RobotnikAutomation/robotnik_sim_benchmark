#!/usr/bin/env bash
# gpu-mon-nvidia.sh <parent-pid> [gpu_index] [interval_sec]
set -euo pipefail
PPID_IN="${1:?usage: $0 <parent-pid> [gpu_index] [interval_sec]}"
GPU="${2:-0}"
INTERVAL="${3:-1}"
TMP="$(mktemp)"; trap 'rm -f "$TMP"' EXIT

descendants() {  # prints all living descendants of a PID
  local p="$1" c
  echo "$p"
  for c in $(pgrep -P "$p" || true); do descendants "$c"; done
}

any_alive() {
  for p in "$@"; do kill -0 "$p" 2>/dev/null && return 0; done
  return 1
}

echo "Monitoring GPU $GPU for processes descended from PID $PPID_IN (interval ${INTERVAL}s)"
echo "Output file: $TMP"
echo "Press Ctrl-C to stop monitoring and show summary."
echo "timestamp,pid,sm_pct,mem_pct" > "$TMP"

while :; do
  mapfile -t D < <(descendants "$PPID_IN" | sort -u)
  any_alive "${D[@]}" || break

  # one-sample process monitor; fields: gpu pid type sm mem enc dec cmd
  OUT="$(nvidia-smi pmon -i "$GPU" -c 1 2>/dev/null || true)"
  [[ -z "$OUT" ]] && sleep "$INTERVAL" && continue

  PIDS="$(printf '%s ' "${D[@]}")"
  awk -v pids="$PIDS" -v ts="$(date +%s)" '
    BEGIN{ split(pids,a," "); for(i in a) if(a[i]!="") h[a[i]]=1 }
    $1 ~ /^[0-9]+$/ && $2 ~ /^[0-9]+$/ {
      pid=$2; sm=$4; mem=$5;
      if (pid in h) printf "%s,%s,%s,%s\n", ts, pid, sm, mem;
    }
  ' <<<"$OUT" >> "$TMP"

  sleep "$INTERVAL"
done

# Summaries
awk -F, 'NR>1{ c[$2]++; sm[$2]+=$3; mem[$2]+=$4 }
END{
  printf "%-8s %-8s %-10s %-10s\n","PID","SAMPLES","AVG_SM%","AVG_MEM%"
  for (p in c) printf "%-8s %-8d %-10.1f %-10.1f\n", p, c[p], sm[p]/c[p], mem[p]/c[p]
}' "$TMP"
