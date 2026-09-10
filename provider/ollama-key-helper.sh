#!/bin/sh
set -eu

if [ -n "${OLLAMA_API_KEY:-}" ]; then
    printf '%s' "$OLLAMA_API_KEY"
    exit 0
fi

KEY_FILE="${BACKS_OLLAMA_KEY_FILE:-$HOME/.config/backs-aios/secrets/ollama-api-key}"

if [ ! -r "$KEY_FILE" ]; then
    printf '%s\n' "BACKS Ollama key helper: no API key available" >&2
    exit 1
fi

IFS= read -r key < "$KEY_FILE" || true
if [ -z "${key:-}" ]; then
    printf '%s\n' "BACKS Ollama key helper: key file is empty" >&2
    exit 1
fi

printf '%s' "$key"
