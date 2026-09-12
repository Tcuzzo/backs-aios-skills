#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
PROVIDER_ROOT="${BACKS_AIOS_PROVIDER_ROOT:-$HOME/.local/share/backs-aios/provider-control}"
PROVIDER_RUNTIME="$PROVIDER_ROOT/current"
GLOBAL_CLAUDE_SKILLS="$HOME/.claude/skills"
GLOBAL_PROVIDER_SKILL="$GLOBAL_CLAUDE_SKILLS/provider"
BIN_DIR="$HOME/.local/bin"
CONFIG_DIR="$HOME/.config/backs-aios/provider-control"
PROJECT_FILE="$CONFIG_DIR/project-root"
PROJECT_ROOT="${BACKS_PROJECT_ROOT:-${1:-}}"

mkdir -p "$PROVIDER_ROOT" "$GLOBAL_CLAUDE_SKILLS" "$BIN_DIR" "$CONFIG_DIR"
chmod 700 "$CONFIG_DIR"

# Provider control is additive and does not replace the primary BACKS runtime.
if [[ -e "$PROVIDER_RUNTIME" && ! -L "$PROVIDER_RUNTIME" ]]; then
  printf 'ERROR: provider runtime path exists and is not a symlink: %s\n' "$PROVIDER_RUNTIME" >&2
  exit 1
fi
ln -sfn "$ROOT" "$PROVIDER_RUNTIME"

expected_skill="$PROVIDER_RUNTIME/claude-skills/provider"

link_provider_skill() {
  local target="$1" current
  mkdir -p "$(dirname "$target")"
  if [[ -L "$target" ]]; then
    current="$(readlink "$target")"
    case "$current" in
      "$expected_skill"|*/claude-skills/provider)
        ln -sfn "$expected_skill" "$target"
        ;;
      *)
        printf 'ERROR: existing provider skill is not BACKS-managed: %s\n' "$target" >&2
        exit 1
        ;;
    esac
  elif [[ -e "$target" ]]; then
    printf 'ERROR: existing provider skill is user-owned: %s\n' "$target" >&2
    exit 1
  else
    ln -s "$expected_skill" "$target"
  fi
}

# Global registration for terminal Claude Code and hosts that honor user skills.
link_provider_skill "$GLOBAL_PROVIDER_SKILL"

# Optional project-local registration for IDE/extension discovery.
# Pass the workspace root as arg 1 or BACKS_PROJECT_ROOT; never hard-coded here.
if [[ -n "$PROJECT_ROOT" ]]; then
  PROJECT_ROOT="$(cd "$PROJECT_ROOT" && pwd -P)"
  link_provider_skill "$PROJECT_ROOT/.claude/skills/provider"
  umask 077
  printf '%s\n' "$PROJECT_ROOT" > "$PROJECT_FILE"
elif [[ -r "$PROJECT_FILE" ]]; then
  IFS= read -r PROJECT_ROOT < "$PROJECT_FILE" || true
fi

# Install executable copies into ~/.local/bin instead of chmod'ing files in the
# Git checkout. This keeps the provider source clean so /provider update can
# fast-forward safely.
install -m 0755 "$PROVIDER_RUNTIME/provider/ollama-key-helper.sh" "$BIN_DIR/backs-ollama-key"
install -m 0755 "$PROVIDER_RUNTIME/bin/backs-aios-update" "$BIN_DIR/backs-aios-update"
install -m 0755 "$PROVIDER_RUNTIME/bin/backs-provider" "$BIN_DIR/backs-provider"

printf '\nBACKS provider control installed.\n'
printf 'Source  : %s\n' "$ROOT"
printf 'Runtime : %s\n' "$PROVIDER_RUNTIME"
printf 'Global  : %s\n' "$GLOBAL_PROVIDER_SKILL"
if [[ -n "$PROJECT_ROOT" ]]; then
  printf 'Project : %s\n' "$PROJECT_ROOT/.claude/skills/provider"
  printf 'Default : %s\n' "$PROJECT_ROOT"
fi
printf 'Command : /provider [claude|ollama|status|models|update]\n'
printf 'CLI     : backs-provider [claude|ollama|status|models|update]\n'
printf 'Updater : backs-aios-update\n'
printf 'Ollama  : uses the active BACKS runtime env/secret resolver; no duplicate key store\n'
printf '\nExisting BACKS runtime and host skill links were left untouched.\n'
printf 'Reload the IDE window and start a new Claude Code agent chat once.\n'
