#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
PROVIDER_ROOT="${BACKS_AIOS_PROVIDER_ROOT:-$HOME/.local/share/backs-aios/provider-control}"
PROVIDER_RUNTIME="$PROVIDER_ROOT/current"
CLAUDE_SKILLS="$HOME/.claude/skills"
PROVIDER_SKILL="$CLAUDE_SKILLS/provider"
BIN_DIR="$HOME/.local/bin"

mkdir -p "$PROVIDER_ROOT" "$CLAUDE_SKILLS" "$BIN_DIR"

# Provider control is an additive layer. It deliberately does not touch
# ~/.local/share/backs-aios/current or any existing Codex/Cursor/OpenCode/Claude
# skill installation owned by another BACKS deployment mechanism.
if [[ -e "$PROVIDER_RUNTIME" && ! -L "$PROVIDER_RUNTIME" ]]; then
  printf 'ERROR: provider runtime path exists and is not a symlink: %s\n' "$PROVIDER_RUNTIME" >&2
  exit 1
fi
ln -sfn "$ROOT" "$PROVIDER_RUNTIME"

expected_skill="$PROVIDER_RUNTIME/claude-skills/provider"
if [[ -L "$PROVIDER_SKILL" ]]; then
  current="$(readlink "$PROVIDER_SKILL")"
  case "$current" in
    "$expected_skill"|*/claude-skills/provider)
      ln -sfn "$expected_skill" "$PROVIDER_SKILL"
      ;;
    *)
      printf 'ERROR: existing /provider skill is not BACKS provider-managed; refusing to overwrite.\n' >&2
      exit 1
      ;;
  esac
elif [[ -e "$PROVIDER_SKILL" ]]; then
  printf 'ERROR: existing /provider skill is user-owned; refusing to overwrite.\n' >&2
  exit 1
else
  ln -s "$expected_skill" "$PROVIDER_SKILL"
fi

ln -sfn "$PROVIDER_RUNTIME/provider/ollama-key-helper.sh" "$BIN_DIR/backs-ollama-key"
ln -sfn "$PROVIDER_RUNTIME/bin/backs-aios-update" "$BIN_DIR/backs-aios-update"
chmod +x "$ROOT/provider/backs_provider.py" "$ROOT/provider/ollama-key-helper.sh" "$ROOT/bin/backs-aios-update" 2>/dev/null || true

printf '\nBACKS provider control installed.\n'
printf 'Source  : %s\n' "$ROOT"
printf 'Runtime : %s\n' "$PROVIDER_RUNTIME"
printf 'Command : /provider [claude|ollama|status|models|update]\n'
printf 'Updater : backs-aios-update\n'
printf 'Ollama  : uses the active BACKS runtime env/secret resolver; no duplicate key store\n'
printf '\nExisting BACKS runtime and host skill links were left untouched.\n'
printf 'Start a fresh Claude Code session once so /provider is discovered.\n'
