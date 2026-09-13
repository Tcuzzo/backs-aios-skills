#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
PROVIDER_ROOT="${BACKS_AIOS_PROVIDER_ROOT:-$HOME/.local/share/backs-aios/provider-control}"
RUNTIME="$PROVIDER_ROOT/current"
CONFIG="$HOME/.config/backs-aios/provider-control"
BIN="$HOME/.local/bin"
PROJECT_ROOT="${BACKS_PROJECT_ROOT:-${1:-}}"
PYTHON="${BACKS_PROVIDER_PYTHON:-}"

if [[ -z "$PROJECT_ROOT" && -r "$CONFIG/project-root" ]]; then
    IFS= read -r PROJECT_ROOT < "$CONFIG/project-root" || true
fi
if [[ -z "$PROJECT_ROOT" || ! -d "$PROJECT_ROOT" ]]; then
    printf '%s\n' 'ERROR: pass the existing BACKS workspace to install-provider.sh.' >&2
    exit 1
fi
PROJECT_ROOT="$(cd "$PROJECT_ROOT" && pwd -P)"
for module in env_loader.py env_utils.py; do
    [[ -f "$PROJECT_ROOT/backend/core/$module" ]] || {
        printf '%s\n' 'ERROR: workspace does not contain the BACKS environment resolver.' >&2
        exit 1
    }
done
if [[ -z "$PYTHON" && -n "${VIRTUAL_ENV:-}" && -x "$VIRTUAL_ENV/bin/python3" ]]; then
    PYTHON="$VIRTUAL_ENV/bin/python3"
fi
if [[ -z "$PYTHON" ]]; then
    for candidate in "$PROJECT_ROOT/.venv/bin/python3" "$PROJECT_ROOT/venv/bin/python3"; do
        if [[ -x "$candidate" ]]; then PYTHON="$candidate"; break; fi
    done
fi
if [[ -z "$PYTHON" && -r "$CONFIG/python-executable" ]]; then
    IFS= read -r PYTHON < "$CONFIG/python-executable" || true
fi
PYTHON="${PYTHON:-$(command -v python3)}"
[[ -x "$PYTHON" ]] || { echo 'ERROR: Python interpreter is unavailable.' >&2; exit 1; }
# Keep the virtual-environment executable path; resolving its symlink would lose
# the virtual environment. This command reads no credential or .env.
PYTHON="$("$PYTHON" -c 'import sys; print(sys.executable)')"

mkdir -p "$CONFIG" "$PROVIDER_ROOT" "$BIN"
chmod 700 "$CONFIG"
EXPECTED="$RUNTIME/claude-skills/provider"
CLAUDE_HOME="${CLAUDE_CONFIG_DIR:-$HOME/.claude}"
GLOBAL_SKILL="$CLAUDE_HOME/skills/provider"
LOCAL_SKILL="$PROJECT_ROOT/.claude/skills/provider"

# Preflight every destination before changing the runtime pointer.
if [[ -e "$RUNTIME" && ! -L "$RUNTIME" ]]; then
    echo 'ERROR: provider runtime is a user-owned directory; not changed.' >&2; exit 1
fi
for target in "$GLOBAL_SKILL" "$LOCAL_SKILL"; do
    if [[ -L "$target" ]]; then
        case "$(readlink "$target")" in
            "$EXPECTED"|*/claude-skills/provider) ;;
            *) echo 'ERROR: conflicting provider skill; not changed.' >&2; exit 1 ;;
        esac
    elif [[ -e "$target" ]]; then
        echo 'ERROR: user-owned provider skill; not changed.' >&2; exit 1
    fi
done
for pair in 'backs-provider:bin/backs-provider' 'backs-ollama-key:provider/ollama-key-helper.sh' 'backs-aios-update:bin/backs-aios-update'; do
    name="${pair%%:*}"
    source="$ROOT/${pair#*:}"
    [[ -f "$source" ]] || { echo 'ERROR: incomplete provider package.' >&2; exit 1; }
    if [[ -e "$BIN/$name" || -L "$BIN/$name" ]]; then
        if [[ ! -f "$BIN/$name" ]] || ! grep -Eq 'BACKS|backs-aios|provider-control' "$BIN/$name"; then
            echo 'ERROR: conflicting command at install destination; not changed.' >&2; exit 1
        fi
    fi
done

# Local paths only, not secret copies. Do not print these paths into diagnostics.
umask 077
printf '%s\n' "$PROJECT_ROOT" > "$CONFIG/project-root"
printf '%s\n' "$PYTHON" > "$CONFIG/python-executable"
ln -sfn "$ROOT" "$RUNTIME"
for target in "$GLOBAL_SKILL" "$LOCAL_SKILL"; do
    mkdir -p "$(dirname "$target")"
    ln -sfn "$EXPECTED" "$target"
done
for pair in 'backs-provider:bin/backs-provider' 'backs-ollama-key:provider/ollama-key-helper.sh' 'backs-aios-update:bin/backs-aios-update'; do
    name="${pair%%:*}"
    tmp="$(mktemp "$BIN/.backs-install.XXXXXX")"
    install -m 0755 "$ROOT/${pair#*:}" "$tmp"
    mv -f "$tmp" "$BIN/$name"
done
printf '\n%s\n' 'BACKS provider installed: shared project and Python context for CLI + IDE credential helper.'
printf '%s\n' 'Existing BACKS runtime, .env, and OAuth credential store were not changed.'
printf '%s\n' 'Run backs-provider ollama to validate real Messages requests and activate the profile.'
printf '%s\n' 'Then reload the IDE window and open a NEW LOCAL Claude Code chat.'
