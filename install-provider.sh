#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
RUNTIME_ROOT="$HOME/.local/share/backs-aios"
RUNTIME="$RUNTIME_ROOT/current"
CLAUDE_SKILLS="$HOME/.claude/skills"
PROVIDER_SKILL="$CLAUDE_SKILLS/provider"
BIN_DIR="$HOME/.local/bin"
KEY_DIR="$HOME/.config/backs-aios/secrets"
KEY_FILE="$KEY_DIR/ollama-api-key"

mkdir -p "$RUNTIME_ROOT" "$CLAUDE_SKILLS" "$BIN_DIR" "$KEY_DIR"
chmod 700 "$KEY_DIR"

if [[ -L "$RUNTIME" ]]; then
  current="$(readlink "$RUNTIME")"
  if [[ "$current" != "$ROOT" ]]; then
    printf 'ERROR: BACKS runtime already points to another source checkout.\n' >&2
    printf 'Run that checkout'\''s install/update path instead of replacing it silently.\n' >&2
    exit 1
  fi
elif [[ -e "$RUNTIME" ]]; then
  printf 'ERROR: BACKS runtime exists as a pinned/non-symlink install.\n' >&2
  exit 1
else
  ln -s "$ROOT" "$RUNTIME"
fi

if [[ -L "$PROVIDER_SKILL" ]]; then
  current="$(readlink "$PROVIDER_SKILL")"
  if [[ "$current" != "$ROOT/claude-skills/provider" ]]; then
    printf 'ERROR: existing /provider skill is not BACKS-managed; refusing to overwrite.\n' >&2
    exit 1
  fi
elif [[ -e "$PROVIDER_SKILL" ]]; then
  printf 'ERROR: existing /provider skill is user-owned; refusing to overwrite.\n' >&2
  exit 1
else
  ln -s "$ROOT/claude-skills/provider" "$PROVIDER_SKILL"
fi

ln -sfn "$ROOT/provider/ollama-key-helper.sh" "$BIN_DIR/backs-ollama-key"
ln -sfn "$ROOT/bin/backs-aios-update" "$BIN_DIR/backs-aios-update"
chmod +x "$ROOT/provider/backs_provider.py" "$ROOT/provider/ollama-key-helper.sh" "$ROOT/bin/backs-aios-update" 2>/dev/null || true

if [[ -n "${OLLAMA_API_KEY:-}" ]]; then
  umask 077
  printf '%s' "$OLLAMA_API_KEY" > "$KEY_FILE"
  chmod 600 "$KEY_FILE"
fi

printf '\nBACKS provider control installed.\n'
printf 'Command : /provider [claude|ollama|status|models|update]\n'
printf 'Updater : backs-aios-update\n'
if [[ -f "$KEY_FILE" ]]; then
  printf 'Ollama  : API key helper ready (secret not displayed)\n'
else
  printf 'Ollama  : export OLLAMA_API_KEY once before /provider ollama\n'
fi
printf '\nStart a fresh Claude Code session once so /provider is discovered.\n'
