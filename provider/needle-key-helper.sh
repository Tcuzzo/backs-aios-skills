#!/usr/bin/env bash
# backs-needle-key: IDE credential helper for the Automatic gateway slot.
# Does NOT read or emit MiniMax keys. BACKS local gateway (/v1) uses empty bearer
# or optional BACKS_ANTHROPIC_GATEWAY_TOKEN, emitted only as helper protocol output.
set -euo pipefail
if [[ -n "${BACKS_ANTHROPIC_GATEWAY_TOKEN:-}" ]]; then
  printf '%s' "$BACKS_ANTHROPIC_GATEWAY_TOKEN"
  exit 0
fi
# Empty token is intentional for localhost BACKS Anthropic-format gateway.
printf '%s' ""
