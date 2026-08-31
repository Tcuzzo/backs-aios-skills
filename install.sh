#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
TARGET="all"
MODE="link"
LOCALE="en"
RUNTIME="$HOME/.local/share/backs-aios/current"
MANAGED_COMMAND_MARKER="backs-aios-managed-command"
MANAGED_ROOT_MARKER_FILE="backs-aios-managed"
MANAGED_ROOT_MARKER_CONTENT="backs-aios-managed 0.7.5"
LAST_HOLDER=""
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

is_managed_root() {
  local path="$1"
  [[ -d "$path" ]] || return 1
  [[ -f "$path/$MANAGED_ROOT_MARKER_FILE" ]] || return 1
  local content
  content="$(head -n 1 "$path/$MANAGED_ROOT_MARKER_FILE" 2>/dev/null || true)"
  content="${content%$'\r'}"
  [[ "$content" =~ ^backs-aios-managed\ [0-9]+\.[0-9]+\.[0-9]+$ ]]
}

write_root_marker() {
  local path="$1"
  printf '%s\n' "$MANAGED_ROOT_MARKER_CONTENT" > "$path/$MANAGED_ROOT_MARKER_FILE"
}

refresh_managed_marker() {
  local marker="$1" tmp
  tmp=$(mktemp "$marker.tmp.XXXXXX") || return 1
  if printf '%s\n' "$MANAGED_ROOT_MARKER_CONTENT" > "$tmp"; then
    chmod 644 "$tmp"
    if mv "$tmp" "$marker"; then
      return 0
    else
      rm -f "$tmp"
      return 1
    fi
  else
    rm -f "$tmp"
    return 1
  fi
}

roots_equal() {
  diff -r -q -x "$MANAGED_ROOT_MARKER_FILE" "$1" "$2" >/dev/null 2>&1
}

swap_or_create_directory() {
  local staging="$2" destination="$3"
  local holder backup
  LAST_HOLDER=""
  if [[ -e "$destination" ]]; then
    holder=$(mktemp -d "$destination.backs-aios-holder.XXXXXX") || return 1
    LAST_HOLDER="$holder"
    backup="$holder/backup"
    if mv "$destination" "$backup"; then
      if mv "$staging" "$destination"; then
        rm -rf "$holder"
        LAST_HOLDER=""
        return 0
      else
        if mv "$backup" "$destination"; then
          if [[ -e "$destination" ]]; then
            rm -rf "$staging" "$holder"
            LAST_HOLDER=""
            return 2
          else
            return 3
          fi
        else
          return 3
        fi
      fi
    else
      rm -rf "$staging" "$holder"
      LAST_HOLDER=""
      return 1
    fi
  else
    if mv "$staging" "$destination"; then
      return 0
    else
      rm -rf "$staging"
      return 1
    fi
  fi
}

install_directory_copy() {
  local label="$1" source="$2" destination="$3"
  local staging existed=0
  if [[ -L "$destination" ]]; then
    printf 'CONFLICT %-10s %s is a symlink\n' "$label" "$destination" >&2
    conflicts=$((conflicts + 1))
    return
  fi
  if [[ -e "$destination" ]]; then
    existed=1
    if ! is_managed_root "$destination"; then
      printf 'CONFLICT %-10s %s already exists (not managed)\n' "$label" "$destination" >&2
      conflicts=$((conflicts + 1))
      return
    fi
  fi
  staging=$(mktemp -d "$destination.backs-aios-staging.XXXXXX") || {
    printf 'ERROR    %-10s %s cannot create staging\n' "$label" "$destination" >&2
    conflicts=$((conflicts + 1))
    return
  }
  chmod 755 "$staging"
  if ! cp -R "$source/." "$staging/"; then
    rm -rf "$staging"
    printf 'ERROR    %-10s %s copy failed\n' "$label" "$destination" >&2
    conflicts=$((conflicts + 1))
    return
  fi
  write_root_marker "$staging"
  if ((existed)); then
    if roots_equal "$staging" "$destination"; then
      rm -rf "$staging"
      if refresh_managed_marker "$destination/$MANAGED_ROOT_MARKER_FILE"; then
        printf 'OK       %-10s %s\n' "$label" "$destination"
      else
        printf 'ERROR    %-10s %s marker refresh failed\n' "$label" "$destination" >&2
        conflicts=$((conflicts + 1))
      fi
      return
    fi
  fi
  if swap_or_create_directory "$label" "$staging" "$destination"; then rc=0; else rc=$?; fi
  case $rc in
    0)
      if ((existed)); then
        printf 'UPDATED  %-10s %s\n' "$label" "$destination"
      else
        printf 'CREATED  %-10s %s\n' "$label" "$destination"
      fi ;;
    1)
      conflicts=$((conflicts + 1))
      if ((existed)); then
        printf 'ERROR    %-10s %s backup failed\n' "$label" "$destination" >&2
      else
        printf 'ERROR    %-10s %s create failed\n' "$label" "$destination" >&2
      fi ;;
    2)
      conflicts=$((conflicts + 1))
      printf 'ERROR    %-10s %s swap failed; restored original\n' "$label" "$destination" >&2 ;;
    3)
      conflicts=$((conflicts + 1))
      printf 'ERROR    %-10s %s recovery failure: original retained in holder %s\n' "$label" "$destination" "$LAST_HOLDER" >&2 ;;
  esac
}

install_pack_copy() {
  local label="$1" destination="$2"
  local staging existed=0
  if [[ -L "$destination" ]]; then
    printf 'CONFLICT %-10s %s is a symlink\n' "$label" "$destination" >&2
    conflicts=$((conflicts + 1))
    return
  fi
  if [[ -e "$destination" ]]; then
    existed=1
    if ! is_managed_root "$destination"; then
      printf 'CONFLICT %-10s %s already exists (not managed)\n' "$label" "$destination" >&2
      conflicts=$((conflicts + 1))
      return
    fi
  fi
  staging=$(mktemp -d "$destination.backs-aios-staging.XXXXXX") || {
    printf 'ERROR    %-10s %s cannot create staging\n' "$label" "$destination" >&2
    conflicts=$((conflicts + 1))
    return
  }
  chmod 755 "$staging"
  if ! copy_pack "$staging"; then
    rm -rf "$staging"
    printf 'ERROR    %-10s %s copy failed\n' "$label" "$destination" >&2
    conflicts=$((conflicts + 1))
    return
  fi
  write_root_marker "$staging"
  if ((existed)); then
    if roots_equal "$staging" "$destination"; then
      rm -rf "$staging"
      if refresh_managed_marker "$destination/$MANAGED_ROOT_MARKER_FILE"; then
        printf 'OK       %-10s %s\n' "$label" "$destination"
      else
        printf 'ERROR    %-10s %s marker refresh failed\n' "$label" "$destination" >&2
        conflicts=$((conflicts + 1))
      fi
      return
    fi
  fi
  if swap_or_create_directory "$label" "$staging" "$destination"; then rc=0; else rc=$?; fi
  case $rc in
    0)
      if ((existed)); then
        printf 'UPDATED  %-10s %s\n' "$label" "$destination"
      else
        printf 'CREATED  %-10s %s\n' "$label" "$destination"
      fi ;;
    1)
      conflicts=$((conflicts + 1))
      if ((existed)); then
        printf 'ERROR    %-10s %s backup failed\n' "$label" "$destination" >&2
      else
        printf 'ERROR    %-10s %s create failed\n' "$label" "$destination" >&2
      fi ;;
    2)
      conflicts=$((conflicts + 1))
      printf 'ERROR    %-10s %s swap failed; restored original\n' "$label" "$destination" >&2 ;;
    3)
      conflicts=$((conflicts + 1))
      printf 'ERROR    %-10s %s recovery failure: original retained in holder %s\n' "$label" "$destination" "$LAST_HOLDER" >&2 ;;
  esac
}

install_skill() {
  local label="$1" destination="$2" source="$3" target
  [[ -f "$source/SKILL.md" ]] || return 0
  target="$destination/$(basename "$source")"
  if [[ "$MODE" == "link" ]]; then
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
    else
      ln -s "$source" "$target"
      printf 'LINKED   %-10s %s\n' "$label" "$target"
    fi
  else
    install_directory_copy "$label" "$source" "$target"
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
  if [[ "$MODE" == "link" ]]; then
    if [[ -L "$target" ]]; then
      if [[ "$(readlink "$target")" == "$ROOT" ]]; then
        printf 'OK       %-10s %s\n' "runtime" "$target"
      else
        printf 'CONFLICT %-10s %s -> %s\n' "runtime" "$target" "$(readlink "$target")" >&2
        conflicts=$((conflicts + 1))
      fi
    elif [[ -e "$target" ]]; then
      printf 'CONFLICT %-10s %s already exists\n' "runtime" "$target" >&2
      conflicts=$((conflicts + 1))
    else
      ln -s "$ROOT" "$target"
      printf 'LINKED   %-10s %s\n' "runtime" "$target"
    fi
  else
    install_pack_copy "runtime" "$target"
  fi
}

install_commands() {
  local label="$1" destination="$2" source target rendered
  mkdir -p "$destination"
  for source in "$ROOT"/command-adapters/*.md; do
    [[ -f "$source" ]] || continue
    target="$destination/$(basename "$source")"
    rendered=$(mktemp "$target.tmp.XXXXXX") || {
      printf 'ERROR    %-10s %s cannot stage\n' "$label" "$target" >&2
      conflicts=$((conflicts + 1))
      continue
    }
    {
      while IFS= read -r line || [[ -n "$line" ]]; do
        line="${line//'${CLAUDE_PLUGIN_ROOT}'/$RUNTIME}"
        line="${line//'${CURSOR_PLUGIN_ROOT}'/$RUNTIME}"
        printf '%s\n' "$line"
      done < "$source"
      printf '\n<!-- %s -->\n' "$MANAGED_COMMAND_MARKER"
    } > "$rendered"
    chmod 644 "$rendered"
    if [[ -e "$target" || -L "$target" ]]; then
      if [[ ! -f "$target" ]] || ! grep -Fq "$MANAGED_COMMAND_MARKER" "$target"; then
        printf 'CONFLICT %-10s %s already exists\n' "$label" "$target" >&2
        conflicts=$((conflicts + 1))
        rm -f "$rendered"
      elif cmp -s "$rendered" "$target"; then
        rm -f "$rendered"
        printf 'OK       %-10s %s\n' "$label" "$target"
      else
        if mv "$rendered" "$target"; then
          printf 'UPDATED  %-10s %s\n' "$label" "$target"
        else
          rm -f "$rendered"
          printf 'ERROR    %-10s %s update failed\n' "$label" "$target" >&2
          conflicts=$((conflicts + 1))
        fi
      fi
    else
      if mv "$rendered" "$target"; then
        printf 'CREATED  %-10s %s\n' "$label" "$target"
      else
        rm -f "$rendered"
        printf 'ERROR    %-10s %s create failed\n' "$label" "$target" >&2
        conflicts=$((conflicts + 1))
      fi
    fi
  done
}

install_opencode_plugin() {
  local source="$RUNTIME/hooks/opencode-plugin.js"
  local dest="$HOME/.config/opencode/plugins/backs-aios.js"
  local marker="$dest.backs-aios-managed"
  local tmp_dest backup
  mkdir -p "$HOME/.config/opencode/plugins"
  if [[ ! -f "$source" ]]; then
    printf 'ERROR    %-10s source missing: %s\n' "opencode-plugin" "$source" >&2
    conflicts=$((conflicts + 1))
    return
  fi
  if [[ "$MODE" == "link" ]]; then
    if [[ -L "$dest" ]]; then
      if [[ "$(readlink "$dest")" == "$source" ]]; then
        printf 'OK       %-10s %s\n' "opencode-plugin" "$dest"
      else
        printf 'CONFLICT %-10s %s -> %s\n' "opencode-plugin" "$dest" "$(readlink "$dest")" >&2
        conflicts=$((conflicts + 1))
      fi
    elif [[ -e "$dest" ]]; then
      printf 'CONFLICT %-10s %s already exists\n' "opencode-plugin" "$dest" >&2
      conflicts=$((conflicts + 1))
    else
      ln -s "$source" "$dest"
      printf 'LINKED   %-10s %s\n' "opencode-plugin" "$dest"
    fi
    return
  fi
  if [[ -L "$dest" ]]; then
    printf 'CONFLICT %-10s %s is a symlink\n' "opencode-plugin" "$dest" >&2
    conflicts=$((conflicts + 1))
    return
  fi
  if [[ -e "$dest" || -e "$marker" ]]; then
    if [[ ! -f "$marker" ]]; then
      printf 'CONFLICT %-10s %s already exists (not managed)\n' "opencode-plugin" "$dest" >&2
      conflicts=$((conflicts + 1))
      return
    fi
    local marker_content
    marker_content="$(head -n 1 "$marker" 2>/dev/null || true)"
    marker_content="${marker_content%$'\r'}"
    if [[ ! "$marker_content" =~ ^backs-aios-managed\ [0-9]+\.[0-9]+\.[0-9]+$ ]]; then
      printf 'CONFLICT %-10s %s already exists (not managed)\n' "opencode-plugin" "$dest" >&2
      conflicts=$((conflicts + 1))
      return
    fi
  fi
  tmp_dest=$(mktemp "$dest.tmp.XXXXXX") || {
    printf 'ERROR    %-10s %s cannot stage adapter\n' "opencode-plugin" "$dest" >&2
    conflicts=$((conflicts + 1))
    return
  }
  if ! cp "$source" "$tmp_dest"; then
    rm -f "$tmp_dest"
    printf 'ERROR    %-10s %s copy failed\n' "opencode-plugin" "$dest" >&2
    conflicts=$((conflicts + 1))
    return
  fi
  if [[ -e "$dest" ]]; then
    if cmp -s "$tmp_dest" "$dest"; then
      rm -f "$tmp_dest"
      if refresh_managed_marker "$marker"; then
        printf 'OK       %-10s %s\n' "opencode-plugin" "$dest"
      else
        printf 'ERROR    %-10s %s marker refresh failed\n' "opencode-plugin" "$dest" >&2
        conflicts=$((conflicts + 1))
      fi
      return
    fi
    backup=$(mktemp "$dest.backs-aios-backup.XXXXXX") || {
      rm -f "$tmp_dest"
      printf 'ERROR    %-10s %s cannot create backup\n' "opencode-plugin" "$dest" >&2
      conflicts=$((conflicts + 1))
      return
    }
    if ! cp -p "$dest" "$backup"; then
      rm -f "$backup" "$tmp_dest"
      printf 'ERROR    %-10s %s backup copy failed\n' "opencode-plugin" "$dest" >&2
      conflicts=$((conflicts + 1))
      return
    fi
    if ! mv "$tmp_dest" "$dest"; then
      rm -f "$backup"
      printf 'ERROR    %-10s %s adapter replace failed\n' "opencode-plugin" "$dest" >&2
      conflicts=$((conflicts + 1))
      return
    fi
    if refresh_managed_marker "$marker"; then
      rm -f "$backup"
      printf 'UPDATED  %-10s %s\n' "opencode-plugin" "$dest"
    else
      if mv "$backup" "$dest"; then
        if [[ -e "$dest" ]]; then
          printf 'ERROR    %-10s %s marker replace failed; restored adapter\n' "opencode-plugin" "$dest" >&2
        else
          printf 'ERROR    %-10s %s recovery failure: adapter backup retained at %s\n' "opencode-plugin" "$dest" "$backup" >&2
        fi
      else
        printf 'ERROR    %-10s %s recovery failure: adapter backup retained at %s\n' "opencode-plugin" "$dest" "$backup" >&2
      fi
      conflicts=$((conflicts + 1))
    fi
  else
    if ! mv "$tmp_dest" "$dest"; then
      rm -f "$tmp_dest"
      printf 'ERROR    %-10s %s adapter create failed\n' "opencode-plugin" "$dest" >&2
      conflicts=$((conflicts + 1))
      return
    fi
    if refresh_managed_marker "$marker"; then
      printf 'CREATED  %-10s %s\n' "opencode-plugin" "$dest"
    else
      rm -f "$dest"
      printf 'ERROR    %-10s %s marker create failed; removed adapter\n' "opencode-plugin" "$dest" >&2
      conflicts=$((conflicts + 1))
    fi
  fi
}

install_codex() {
  install_skills codex "$HOME/.codex/skills"
  [[ "$LOCALE" == "en" ]] || install_command_skills codex-cmd "$HOME/.codex/skills"
}

install_opencode() {
  install_skills opencode "$HOME/.config/opencode/skills"
  install_commands opencode "$HOME/.config/opencode/commands"
  install_opencode_plugin
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
  if [[ "$MODE" == "link" ]]; then
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
    else
      ln -s "$ROOT" "$target"
      printf 'LINKED   %-10s %s\n' "cursor" "$target"
    fi
  else
    install_pack_copy "cursor" "$target"
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
