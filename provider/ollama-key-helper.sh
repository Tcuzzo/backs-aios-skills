#!/bin/sh
set -eu

PROVIDER_RUNTIME="${BACKS_AIOS_PROVIDER_RUNTIME:-$HOME/.local/share/backs-aios/provider-control/current}"
CONTROLLER="$PROVIDER_RUNTIME/provider/backs_provider.py"

if [ ! -f "$CONTROLLER" ]; then
    printf '%s\n' "BACKS Ollama key helper: provider controller is not installed" >&2
    exit 1
fi

exec python3 "$CONTROLLER" __key
