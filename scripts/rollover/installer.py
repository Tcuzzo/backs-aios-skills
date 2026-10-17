"""Reversible installer support; Python 3.11+, standard library only.

This module merges configuration and manages selected files. It never launches,
stops, or claims control over coder sessions. Reports contain hashes and paths,
never configuration contents. Backups and the journal are private local files.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import tempfile
import tomllib
import uuid

THRESHOLD = 125000
CLAUDE_KEY = "CLAUDE_CODE_AUTO_COMPACT_WINDOW"
CODEX_KEY = "model_auto_compact_token_limit"
_UNSET = object()


class InstallerError(ValueError):
    pass


class Conflict(InstallerError):
    pass


@dataclass(frozen=True)
class MergeResult:
    data: bytes
    changed: bool
    warnings: list[str]
    thresholds: dict[str, int]


def _require(condition, message):
    if not condition:
        raise InstallerError(message)


def _digest(data):
    return hashlib.sha256(data).hexdigest()


def _json_pairs(pairs):
    result = {}
    for key, value in pairs:
        _require(key not in result, "duplicate JSON key; merge refused")
        result[key] = value
    return result


def _json_load(raw):
    try:
        return json.loads(raw, object_pairs_hook=_json_pairs,
                          parse_constant=lambda _: (_ for _ in ()).throw(InstallerError("non-finite JSON number")))
    except (UnicodeError, json.JSONDecodeError) as error:
        raise InstallerError("invalid JSON; merge refused") from error


def _threshold(value):
    _require(type(value) is int and value > 0, "threshold must be a positive integer")
    return value


def merge_claude(raw: bytes, threshold=THRESHOLD) -> MergeResult:
    """Merge only env.CLAUDE_CODE_AUTO_COMPACT_WINDOW, preserving stricter caps."""
    _threshold(threshold)
    _require(100000 <= threshold <= 1000000, "Claude window must be between 100000 and 1000000")
    document = _json_load(raw) if raw.strip() else {}
    _require(isinstance(document, dict), "Claude settings must be an object")
    env = document.get("env", {})
    _require(isinstance(env, dict), "Claude env is not an object; merge refused")
    warnings = []
    for key in env:
        if "COMPACT" in key and ("PCT" in key or "PERCENT" in key):
            warnings.append("Retained compaction percentage override: " + key)
    for key in ("DISABLE_AUTO_COMPACT", "DISABLE_COMPACT"):
        if str(env.get(key, "")).lower() in ("1", "true", "yes", "on"):
            warnings.append(key + " remains enabled; native compaction may be disabled")
    previous = env.get(CLAUDE_KEY)
    valid = (type(previous) is int and 100000 <= previous <= 1000000) or (
        isinstance(previous, str) and re.fullmatch(r"[0-9]+", previous) and 100000 <= int(previous) <= 1000000)
    selected = min(int(previous), threshold) if valid else threshold
    if previous is not None and not valid:
        warnings.append("Repaired an invalid " + CLAUDE_KEY + " value")
    if previous == str(selected):
        return MergeResult(raw, False, warnings, {CLAUDE_KEY: selected})
    document["env"] = {**env, CLAUDE_KEY: str(selected)}
    text = raw.decode("utf-8") if raw else ""
    indentation = re.search(r"\n([ \t]+)\"", text)
    indent = indentation.group(1) if indentation else "  "
    newline = "\r\n" if "\r\n" in text else "\n"
    data = (json.dumps(document, indent=indent, ensure_ascii=False, allow_nan=False) + "\n")
    if newline != "\n":
        data = data.replace("\n", newline)
    return MergeResult(data.encode("utf-8"), True, warnings, {CLAUDE_KEY: selected})


def _quoted_end(text, start):
    quote = text[start]
    triple = text.startswith(quote * 3, start)
    cursor = start + (3 if triple else 1)
    while cursor < len(text):
        if quote == '"' and text[cursor] == "\\":
            cursor += 2
        elif triple and text.startswith(quote * 3, cursor):
            end = cursor + 3
            while end < len(text) and end < cursor + 5 and text[end] == quote:
                end += 1
            return end
        elif not triple and text[cursor] == quote:
            return cursor + 1
        else:
            cursor += 1
    raise InstallerError("unterminated TOML string")


def _skip(text, cursor):
    while cursor < len(text):
        if text[cursor].isspace():
            cursor += 1
        elif text[cursor] == "#":
            end = text.find("\n", cursor)
            cursor = len(text) if end < 0 else end + 1
        else:
            break
    return cursor


def _equals(text, cursor):
    while cursor < len(text):
        if text[cursor] in ("'", '"'):
            cursor = _quoted_end(text, cursor)
        elif text[cursor] == "=":
            return cursor
        else:
            cursor += 1
    raise InstallerError("TOML assignment has no equals sign")


def _key_path(raw):
    value = tomllib.loads(raw.strip() + " = 0")
    path = []
    while isinstance(value, dict):
        _require(len(value) == 1, "ambiguous TOML key")
        key, value = next(iter(value.items()))
        path.append(key)
    return tuple(path)


def _value_end(text, start):
    if text[start] in ("'", '"'):
        return _quoted_end(text, start)
    if text[start] in "[{":
        stack, cursor = [], start
        while cursor < len(text):
            char = text[cursor]
            if char in ("'", '"'):
                cursor = _quoted_end(text, cursor)
                continue
            if char == "#":
                cursor = text.find("\n", cursor)
                _require(cursor >= 0, "unterminated TOML collection")
            elif char in "[{":
                stack.append(char)
            elif char in "]}":
                stack.pop()
                if not stack:
                    return cursor + 1
            cursor += 1
        raise InstallerError("unterminated TOML collection")
    cursor = start
    while cursor < len(text) and text[cursor] not in "#\r\n,]}":
        cursor += 1
    while cursor > start and text[cursor - 1].isspace():
        cursor -= 1
    return cursor


def _inline_locations(text, start, end, prefix, locations):
    cursor = start + 1
    while cursor < end - 1:
        cursor = _skip(text, cursor)
        if text[cursor] == "}":
            return
        equals = _equals(text, cursor)
        path = prefix + _key_path(text[cursor:equals])
        value = _skip(text, equals + 1)
        stop = _value_end(text, value)
        locations[path] = (value, stop)
        if text[value] == "{":
            _inline_locations(text, value, stop, path, locations)
        cursor = _skip(text, stop)
        if text[cursor] == ",":
            cursor += 1


def _toml_locations(text):
    """Locate scalar source spans after tomllib validates the whole document."""
    locations, table, cursor = {}, (), 0
    while (cursor := _skip(text, cursor)) < len(text):
        if text[cursor] == "[":
            array = text.startswith("[[", cursor)
            start = cursor + (2 if array else 1)
            end = start
            while end < len(text) and text[end] != "]":
                end = _quoted_end(text, end) if text[end] in ("'", '"') else end + 1
            table = _key_path(text[start:end])
            cursor = end + (2 if array else 1)
        else:
            equals = _equals(text, cursor)
            path = table + _key_path(text[cursor:equals])
            value = _skip(text, equals + 1)
            stop = _value_end(text, value)
            locations[path] = (value, stop)
            if text[value] == "{":
                _inline_locations(text, value, stop, path, locations)
            cursor = stop
    return locations


def merge_codex(raw: bytes, threshold=THRESHOLD) -> MergeResult:
    """Edit the top-level cap and existing per-profile caps; retain other bytes."""
    _threshold(threshold)
    try:
        text = raw.decode("utf-8")
        parsed = tomllib.loads(text)
    except (UnicodeError, tomllib.TOMLDecodeError) as error:
        raise InstallerError("invalid TOML; merge refused") from error
    desired = {(CODEX_KEY,): parsed.get(CODEX_KEY)}
    profiles = parsed.get("profiles", {})
    if isinstance(profiles, dict):
        for name, profile in profiles.items():
            if isinstance(profile, dict) and CODEX_KEY in profile:
                desired[("profiles", name, CODEX_KEY)] = profile[CODEX_KEY]
    locations = _toml_locations(text)
    warnings, thresholds, edits = [], {}, []
    for path, previous in desired.items():
        selected = min(previous, threshold) if type(previous) is int and previous > 0 else threshold
        label = ".".join(path)
        thresholds[label] = selected
        if previous is not None and (type(previous) is not int or previous <= 0):
            warnings.append("Repaired an invalid " + label + " value")
        if type(previous) is int and previous == selected:
            continue
        if path == (CODEX_KEY,) and CODEX_KEY not in parsed:
            newline = "\r\n" if "\r\n" in text else "\n"
            edits.append((0, 0, CODEX_KEY + " = " + str(selected) + newline))
        else:
            _require(path in locations, "unsupported TOML representation for " + label)
            edits.append((*locations[path], str(selected)))
    for start, stop, value in sorted(edits, reverse=True):
        text = text[:start] + value + text[stop:]
    # Validate the edited document too, including quoted/dotted/inline profiles.
    tomllib.loads(text)
    data = text.encode("utf-8")
    return MergeResult(data, data != raw, warnings, thresholds)


def _absolute(path):
    path = Path(path).expanduser()
    _require(path.is_absolute(), "an absolute path is required")
    _require(".." not in path.parts, "parent traversal is refused")
    return path


def _check_path(path, allow_final_link=False):
    path = _absolute(path)
    for item in (*reversed(path.parents), path):
        if item.is_symlink() and not (allow_final_link and item == path):
            raise Conflict("symlink path refused: " + str(item))
    return path


def read_config(path) -> bytes:
    path = _check_path(path)
    if not path.exists():
        return b""
    if not path.is_file():
        raise Conflict("configuration is not a regular file: " + str(path))
    return path.read_bytes()


def discover(home, projects=()):
    """Return default/override global configs and existing explicit-project configs."""
    home = _absolute(home).resolve()
    candidates = [("claude", home / ".claude/settings.json", "global"),
                  ("codex", home / ".codex/config.toml", "global")]
    for variable, kind, suffix in (("CLAUDE_CONFIG_DIR", "claude", "settings.json"),
                                    ("CODEX_HOME", "codex", "config.toml")):
        if os.environ.get(variable):
            directory = Path(os.environ[variable]).expanduser().absolute()
            candidates.append((kind, directory / suffix, "environment:" + variable))
    for project in projects:
        project = _absolute(project).resolve()
        for kind, suffix in (("claude", ".claude/settings.json"), ("claude", ".claude/settings.local.json"),
                              ("codex", ".codex/config.toml")):
            path = project / suffix
            if os.path.lexists(path):
                candidates.append((kind, path, "project"))
    configs, warnings, seen = [], [], set()
    for kind, path, scope in candidates:
        if str(path) in seen:
            continue
        seen.add(str(path))
        unsafe = False
        try:
            _check_path(path)
        except Conflict as error:
            unsafe = True
            warnings.append(str(error))
        configs.append({"kind": kind, "path": str(path), "scope": scope,
                        "exists": os.path.lexists(path), "symlink": unsafe})
    return {"configs": configs, "warnings": warnings}


def _mkdir_private(path):
    path = _check_path(path)
    missing = []
    cursor = path
    while not cursor.exists():
        missing.append(cursor)
        cursor = cursor.parent
    _require(cursor.is_dir(), "parent path is not a directory")
    for directory in reversed(missing):
        directory.mkdir(mode=0o700)


def _fsync_directory(path):
    if os.name != "nt":
        descriptor = os.open(path, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0))
        try:
            os.fsync(descriptor)
        finally:
            os.close(descriptor)


def _atomic_write(path, data, mode):
    path = _check_path(path)
    _mkdir_private(path.parent)
    descriptor, name = tempfile.mkstemp(prefix=".rollover-", dir=path.parent)
    temporary = Path(name)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            os.fchmod(stream.fileno(), mode)
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        _check_path(path)
        os.replace(temporary, path)
        _fsync_directory(path.parent)
    finally:
        if temporary.exists():
            temporary.unlink()


def _file_state(path):
    path = _check_path(path)
    if not path.exists():
        return None
    if not path.is_file():
        raise Conflict("target is not a regular file: " + str(path))
    return {"sha256": _digest(path.read_bytes()), "mode": stat.S_IMODE(path.stat().st_mode)}


def _replace_link(path, target, expected):
    """Atomically retarget a link only after checking the caller's prior target."""
    path = _check_path(path, allow_final_link=True)
    if not path.is_symlink() or os.readlink(path) != expected:
        raise Conflict("registration changed during installation: " + str(path))
    temporary = path.parent / (".rollover-link-" + uuid.uuid4().hex)
    try:
        temporary.symlink_to(target, target_is_directory=Path(target).is_dir())
        _check_path(path, allow_final_link=True)
        if not path.is_symlink() or os.readlink(path) != expected:
            raise Conflict("registration changed during installation: " + str(path))
        os.replace(temporary, path)
        _fsync_directory(path.parent)
    finally:
        if os.path.lexists(temporary):
            temporary.unlink()


class Transaction:
    """Lazy private journal, exact backups, atomic writes, and guarded rollback.

    Use write for selected raw files, including merged configs and generated boot
    units. symlink creates registrations only; existing foreign paths are refused.
    A failure leaves a recoverable journal. finish records the completed receipt.
    """
    def __init__(self, state_dir, label="install"):
        self.state_dir = _check_path(state_dir)
        self.label = str(label)
        self.manifest_path = None
        self.document = {"version": 1, "transaction_id": None, "label": self.label,
                         "status": "open", "entries": []}

    def _start(self):
        if self.manifest_path is not None:
            return
        _mkdir_private(self.state_dir)
        self.state_dir.chmod(0o700)
        identity = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ-") + uuid.uuid4().hex[:12]
        folder = self.state_dir / "transactions" / identity
        _mkdir_private(folder / "backups")
        self.manifest_path = folder / "manifest.json"
        self.document.update(transaction_id=identity, status="applying")
        self._persist()

    def _persist(self):
        if self.manifest_path is not None:
            _atomic_write(self.manifest_path, (json.dumps(self.document, indent=2) + "\n").encode(), 0o600)

    def _prepare(self, entry, old_bytes=None):
        _require(self.document["status"] in ("open", "applying"), "transaction is already closed")
        _require(not any(item["path"] == entry["path"] for item in self.document["entries"]),
                 "target already changed in this transaction")
        self._start()
        if old_bytes is not None:
            backup = "backups/%06d.bin" % len(self.document["entries"])
            _atomic_write(self.manifest_path.parent / backup, old_bytes, 0o600)
            entry["backup"] = backup
        entry["status"] = "prepared"
        self.document["entries"].append(entry)
        self._persist()

    def _failure(self):
        self.document["status"] = "failed"
        self._persist()

    def write(self, path, data: bytes, mode=None, *, expected_before=_UNSET) -> bool:
        path = _check_path(path)
        _require(isinstance(data, bytes), "write data must be bytes")
        before = _file_state(path)
        selected_mode = mode if mode is not None else (before["mode"] if before else 0o600)
        _require(type(selected_mode) is int and 0 <= selected_mode <= 0o7777, "invalid file mode")
        after = {"sha256": _digest(data), "mode": selected_mode}
        if before == after:
            return False
        old_bytes = path.read_bytes() if before is not None else None
        if old_bytes is not None and _digest(old_bytes) != before["sha256"]:
            raise Conflict("target changed before backup: " + str(path))
        if expected_before is not _UNSET:
            _require(isinstance(expected_before, bytes), "expected_before must be the original bytes")
            if (old_bytes if old_bytes is not None else b"") != expected_before:
                raise Conflict("configuration changed since it was merged: " + str(path))
        entry = {"kind": "file", "path": str(path), "before": before, "after": after}
        self._prepare(entry, old_bytes)
        try:
            if _file_state(path) != before:
                raise Conflict("target changed during installation: " + str(path))
            _atomic_write(path, data, selected_mode)
            entry["status"] = "applied"
            self._persist()
        except Exception:
            self._failure()
            raise
        return True

    def symlink(self, path, target) -> bool:
        path = _check_path(path, allow_final_link=True)
        target = _absolute(target)
        if path.is_symlink():
            if os.readlink(path) == str(target):
                return False
            raise Conflict("foreign symlink retained: " + str(path))
        if os.path.lexists(path):
            raise Conflict("existing registration retained: " + str(path))
        _require(target.exists(), "registration target does not exist")
        entry = {"kind": "symlink", "path": str(path), "before": None, "after": {"target": str(target)}}
        self._prepare(entry)
        try:
            _mkdir_private(path.parent)
            path.symlink_to(target, target_is_directory=target.is_dir())
            _fsync_directory(path.parent)
            entry["status"] = "applied"
            self._persist()
        except Exception:
            self._failure()
            raise
        return True

    def replace_symlink(self, path, target, *, expected) -> bool:
        """Upgrade a caller-verified owned link, retaining its old rollback target."""
        path = _check_path(path, allow_final_link=True)
        target = _absolute(target)
        _require(isinstance(expected, str) and expected, "expected link target is required")
        if not path.is_symlink():
            raise Conflict("expected registration is no longer a symlink: " + str(path))
        current = os.readlink(path)
        if current == str(target):
            return False
        if current != expected:
            raise Conflict("registration changed since planning: " + str(path))
        _require(target.exists(), "registration target does not exist")
        entry = {"kind": "symlink", "path": str(path), "before": {"target": expected},
                 "after": {"target": str(target)}}
        self._prepare(entry)
        try:
            _replace_link(path, str(target), expected)
            entry["status"] = "applied"
            self._persist()
        except Exception:
            self._failure()
            raise
        return True

    def finish(self) -> dict:
        if self.document["status"] in ("open", "applying"):
            self.document["status"] = "complete"
            self._persist()
        return self.report()

    def report(self) -> dict:
        return {"transaction_id": self.document["transaction_id"],
                "manifest_path": str(self.manifest_path) if self.manifest_path else None,
                "status": self.document["status"],
                "changed": sum(entry["status"] == "applied" for entry in self.document["entries"]),
                "entries": json.loads(json.dumps(self.document["entries"]))}


def rollback(manifest_path) -> dict:
    """Restore only untouched installed states; later user edits become conflicts."""
    manifest_path = _check_path(manifest_path)
    document = _json_load(read_config(manifest_path))
    _require(isinstance(document, dict) and document.get("version") == 1 and
             isinstance(document.get("entries"), list), "invalid transaction journal")
    results, conflicts = [], []
    for entry in reversed(document["entries"]):
        try:
            path = _absolute(entry["path"])
            if entry["kind"] == "symlink":
                _check_path(path, allow_final_link=True)
                before_target = entry["before"]["target"] if entry["before"] is not None else None
                if not os.path.lexists(path) and before_target is None:
                    outcome = "already_restored"
                elif path.is_symlink() and os.readlink(path) == before_target:
                    outcome = "already_restored"
                elif path.is_symlink() and os.readlink(path) == entry["after"]["target"]:
                    if before_target is None:
                        path.unlink()
                        _fsync_directory(path.parent)
                    else:
                        _replace_link(path, before_target, entry["after"]["target"])
                    outcome = "restored"
                else:
                    raise Conflict("registration changed after installation")
            elif entry["kind"] == "file":
                current = _file_state(path)
                if current == entry["before"]:
                    outcome = "already_restored"
                elif current != entry["after"]:
                    raise Conflict("file changed after installation")
                elif entry["before"] is None:
                    path.unlink()
                    _fsync_directory(path.parent)
                    outcome = "restored"
                else:
                    relative = Path(entry["backup"])
                    _require(not relative.is_absolute() and ".." not in relative.parts, "unsafe backup path")
                    backup = read_config(manifest_path.parent / relative)
                    _require(_digest(backup) == entry["before"]["sha256"], "backup integrity mismatch")
                    _atomic_write(path, backup, entry["before"]["mode"])
                    outcome = "restored"
            else:
                raise InstallerError("unknown transaction entry type")
            entry["status"] = "rolled_back"
            results.append({"path": str(path), "outcome": outcome})
        except (InstallerError, OSError, KeyError, TypeError) as error:
            conflicts.append({"path": entry.get("path", ""), "reason": str(error)})
    document["status"] = "rollback_conflicts" if conflicts else "rolled_back"
    _atomic_write(manifest_path, (json.dumps(document, indent=2) + "\n").encode(), 0o600)
    return {"transaction_id": document.get("transaction_id"), "manifest_path": str(manifest_path),
            "status": document["status"], "restored": results, "conflicts": conflicts}
