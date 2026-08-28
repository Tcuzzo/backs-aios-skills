#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
TARGET="all"
MODE="link"
LOCALE="en"

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

install_skills() {
  local label="$1" destination="$2" source target
  mkdir -p "$destination"
  for source in "$SKILLS"/*; do
    [[ -f "$source/SKILL.md" ]] || continue
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
  done
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
    (cd "$ROOT" && tar --exclude='./.git' -cf - .) | tar -xf - -C "$target"
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
    install_skills codex "$HOME/.codex/skills"
    install_cursor_plugin
    install_skills opencode "$HOME/.config/opencode/skills"
    install_skills claude "$HOME/.claude/skills"
    install_skills portable "$HOME/.agents/skills"
    ;;
  codex) install_skills codex "$HOME/.codex/skills" ;;
  cursor) install_cursor_plugin ;;
  opencode) install_skills opencode "$HOME/.config/opencode/skills" ;;
  claude) install_skills claude "$HOME/.claude/skills" ;;
  portable) install_skills portable "$HOME/.agents/skills" ;;
esac

if ((conflicts)); then
  echo "$conflicts conflict(s) left untouched. Move or rename them, then rerun." >&2
  exit 1
fi

echo "BACKS AIOS registered. Start a new agent session and invoke optimus."
