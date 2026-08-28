#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
TARGET="all"
MODE="link"
LOCALE="en"
RUNTIME="$HOME/.local/share/backs-aios/current"
MANAGED_COMMAND_MARKER="backs-aios-managed-command"
PACK_ENTRIES=(
  .claude-plugin .codex-plugin .cursor-plugin .gitignore
  command-adapters docs hooks i18n plays skills
  CITATION.cff INSTALL.md LICENSE NAMING.md NOTICE.md README.md
  install.sh install.ps1
)

usage() {
  cat <<'EOF'
Usage: ./install.sh [--target all|codex|cursor|opencode|claude|portable]
                    [--copy] [--locale en|de|es|fr|hi|pt-BR|zh-CN]

The default creates update-friendly symlinks. --copy makes pinned copies.
Existing non-matching files are never overwritten.
EOF
}

while (($#)); do
  case "$1" in
    --target) TARGET="${2:?--target needs a value}"; shift 2 ;;
    --locale) LOCALE="${2:?--locale needs a value}"; shift 2 ;;
    --copy) MODE="copy"; shift ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown argument: $1" >&2; usage >&2; exit 2 ;;
  esac
done

case "$TARGET" in all|codex|cursor|opencode|claude|portable) ;; *) echo "Unknown target: $TARGET" >&2; exit 2 ;; esac
case "$LOCALE" in
  en) SKILLS="$ROOT/skills" ;;
  de|es|fr|hi|pt-BR|zh-CN) SKILLS="$ROOT/i18n/$LOCALE/skills" ;;
  *) echo "Unknown locale: $LOCALE" >&2; exit 2 ;;
esac

conflicts=0

copy_pack() {
  local destination="$1"
  (cd "$ROOT" && tar \
    --exclude='.pytest_cache' \
    --exclude='*/.pytest_cache' \
    --exclude='__pycache__' \
    --exclude='*/__pycache__' \
    --exclude='*.pyc' \
    -cf - "${PACK_ENTRIES[@]}") | tar -xf - -C "$destination"
}

install_skill() {
  local label="$1" destination="$2" source="$3" target
  [[ -f "$source/SKILL.md" ]] || return 0
  target="$destination/$(basename "$source")"
  if [[ -L "$target" ]]; then
    if [[ "$(readlink "$target")" == "$source" ]]; then
      printf 'OK       %-10s %s\n' "$label" "$target"
    else
      printf 'CONFLICT %-10s %s -> %s\n' "$label" "$target" "$(readlink "$target")" >&2
      conflicts=$((conflicts + 1))
    fi
  elif [[ -e "$target" ]]; then
    printf 'CONFLICT %-10s %s already exists\n' "$label" "$target" >&2
    conflicts=$((conflicts + 1))
  elif [[ "$MODE" == "copy" ]]; then
    cp -R "$source" "$target"
    printf 'COPIED   %-10s %s\n' "$label" "$target"
  else
    ln -s "$source" "$target"
    printf 'LINKED   %-10s %s\n' "$label" "$target"
  fi
}

install_skills() {
  local label="$1" destination="$2" skills_root="${3:-$SKILLS}" source
  mkdir -p "$destination"
  for source in "$skills_root"/*; do
    install_skill "$label" "$destination" "$source"
  done
}

install_command_skills() {
  local label="$1" destination="$2" name
  mkdir -p "$destination"
  for name in agent-build bughunt elite-build grade parallel-work secure-delivery tribunal web-build; do
    install_skill "$label" "$destination" "$ROOT/skills/$name"
  done
}

install_runtime() {
  local destination="$HOME/.local/share/backs-aios" target="$RUNTIME"
  mkdir -p "$destination"
  if [[ -L "$target" ]]; then
    if [[ "$MODE" == "link" && "$(readlink "$target")" == "$ROOT" ]]; then
      printf 'OK       %-10s %s\n' "runtime" "$target"
    else
      printf 'CONFLICT %-10s %s -> %s\n' "runtime" "$target" "$(readlink "$target")" >&2
      conflicts=$((conflicts + 1))
    fi
  elif [[ -e "$target" ]]; then
    printf 'CONFLICT %-10s %s already exists\n' "runtime" "$target" >&2
    conflicts=$((conflicts + 1))
  elif [[ "$MODE" == "copy" ]]; then
    mkdir "$target"
    copy_pack "$target"
    printf 'COPIED   %-10s %s\n' "runtime" "$target"
  else
    ln -s "$ROOT" "$target"
    printf 'LINKED   %-10s %s\n' "runtime" "$target"
  fi
}

install_commands() {
  local label="$1" destination="$2" source target rendered
  mkdir -p "$destination"
  for source in "$ROOT"/command-adapters/*.md; do
    [[ -f "$source" ]] || continue
    target="$destination/$(basename "$source")"
    rendered="$target.tmp.$$"
    {
      while IFS= read -r line || [[ -n "$line" ]]; do
        line="${line//'${CLAUDE_PLUGIN_ROOT}'/$RUNTIME}"
        line="${line//'${CURSOR_PLUGIN_ROOT}'/$RUNTIME}"
        printf '%s\n' "$line"
      done < "$source"
      printf '\n<!-- %s -->\n' "$MANAGED_COMMAND_MARKER"
    } > "$rendered"
    if [[ -e "$target" || -L "$target" ]]; then
      if [[ ! -f "$target" ]] || ! grep -Fq "$MANAGED_COMMAND_MARKER" "$target"; then
        printf 'CONFLICT %-10s %s already exists\n' "$label" "$target" >&2
        conflicts=$((conflicts + 1))
        rm -f "$rendered"
      elif cmp -s "$rendered" "$target"; then
        rm -f "$rendered"
        printf 'OK       %-10s %s\n' "$label" "$target"
      else
        mv "$rendered" "$target"
        printf 'UPDATED  %-10s %s\n' "$label" "$target"
      fi
    else
      mv "$rendered" "$target"
      printf 'CREATED  %-10s %s\n' "$label" "$target"
    fi
  done
}

install_codex() {
  install_skills codex "$HOME/.codex/skills"
  [[ "$LOCALE" == "en" ]] || install_command_skills codex-cmd "$HOME/.codex/skills"
}

install_opencode() {
  install_skills opencode "$HOME/.config/opencode/skills"
  install_commands opencode "$HOME/.config/opencode/commands"
}

install_claude() {
  install_skills claude "$HOME/.claude/skills"
}

install_portable() {
  install_skills portable "$HOME/.agents/skills"
  [[ "$LOCALE" == "en" ]] || install_command_skills portable-cmd "$HOME/.agents/skills"
}

install_cursor_plugin() {
  local destination="$HOME/.cursor/plugins/local" target="$HOME/.cursor/plugins/local/backs-aios"
  mkdir -p "$destination"
  if [[ -L "$target" ]]; then
    if [[ "$(readlink "$target")" == "$ROOT" ]]; then
      printf 'OK       %-10s %s\n' "cursor" "$target"
    else
      printf 'CONFLICT %-10s %s -> %s\n' "cursor" "$target" "$(readlink "$target")" >&2
      conflicts=$((conflicts + 1))
    fi
  elif [[ -e "$target" ]]; then
    printf 'CONFLICT %-10s %s already exists\n' "cursor" "$target" >&2
    conflicts=$((conflicts + 1))
  elif [[ "$MODE" == "copy" ]]; then
    mkdir "$target"
    copy_pack "$target"
    printf 'COPIED   %-10s %s\n' "cursor" "$target"
  else
    ln -s "$ROOT" "$target"
    printf 'LINKED   %-10s %s\n' "cursor" "$target"
  fi
  if [[ "$LOCALE" != "en" ]]; then
    echo "NOTE: Cursor's full plugin stays English; locale $LOCALE was installed only to skill-only targets."
  fi
}

case "$TARGET" in
  all)
    install_runtime
    install_codex
    install_cursor_plugin
    install_opencode
    install_claude
    install_portable
    ;;
  codex) install_runtime; install_codex ;;
  cursor) install_cursor_plugin ;;
  opencode) install_runtime; install_opencode ;;
  claude) install_runtime; install_claude ;;
  portable) install_runtime; install_portable ;;
esac

if ((conflicts)); then
  echo "$conflicts conflict(s) left untouched. Move or rename them, then rerun." >&2
  exit 1
fi

echo "BACKS AIOS skills and host-native commands registered. Start a new agent session and invoke optimus."
