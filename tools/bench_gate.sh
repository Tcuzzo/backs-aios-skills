#!/usr/bin/env bash
# bench_gate — measure what the grounding gate actually costs on YOUR machine.
#
# The README quotes per-call numbers from one Linux box. Spawn cost varies a lot
# by machine, so do not take those digits on faith. Run this and read your own.
#
#   bash tools/bench_gate.sh [iterations]     # default 40
#
# It feeds the gate a real PreToolUse payload on stdin, the same way a host
# runtime does, and reports the median wall time per call. It writes nothing
# outside a temporary directory and it changes no repo state.

set -euo pipefail

ITERS="${1:-40}"
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
GATE="$HERE/hooks/aios_gate.js"

if ! command -v node >/dev/null 2>&1; then
  echo "bench_gate: node is not installed — nothing to measure." >&2
  exit 1
fi
if [ ! -f "$GATE" ]; then
  echo "bench_gate: cannot find $GATE" >&2
  exit 1
fi

WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT
export HOME="$WORK"

payload_for() {
  printf '{"hook_event_name":"PreToolUse","tool_name":"%s","session_id":"bench","tool_input":{"command":"ls -la"}}' "$1"
}

median_ms() {
  sort -n | awk '{a[NR]=$1} END {print (NR%2) ? a[(NR+1)/2] : int((a[NR/2]+a[NR/2+1])/2)}'
}

run_case() {
  local label="$1" tool="$2" gate_env="$3"
  local payload t0 t1
  payload="$(payload_for "$tool")"
  # one warm-up, so we time steady state rather than first-touch disk
  printf '%s' "$payload" | AIOS_GATE="$gate_env" node "$GATE" >/dev/null 2>&1 || true
  : > "$WORK/times"
  for _ in $(seq "$ITERS"); do
    t0=$(date +%s%N)
    printf '%s' "$payload" | AIOS_GATE="$gate_env" node "$GATE" >/dev/null 2>&1 || true
    t1=$(date +%s%N)
    echo $(( (t1 - t0) / 1000000 )) >> "$WORK/times"
  done
  printf '  %-36s %4s ms (median of %s)\n' "$label" "$(median_ms < "$WORK/times")" "$ITERS"
}

echo "gate benchmark — node $(node --version), $ITERS iterations per case"
echo
run_case "armed, file-edit tool (Write)"   "Write" "on"
run_case "armed, read-only shell (Bash)"   "Bash"  "on"
run_case "kill-switch off (AIOS_GATE=off)" "Write" "off"
echo
echo "Most of that number is process spawn, which is why the kill-switch is not free."
echo "True zero overhead means removing the hook from your host config, not the env var."
