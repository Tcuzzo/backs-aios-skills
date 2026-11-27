#!/usr/bin/env python3
"""Freeze, verify, and isolation-check an allowlisted blind-review packet."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
from pathlib import Path

MANIFEST = "manifest.json"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def canonical_bytes(payload: object) -> bytes:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def safe_relative(value: str) -> Path:
    path = Path(value)
    if path.is_absolute() or not path.parts or any(part in ("", ".", "..") for part in path.parts):
        raise ValueError(f"path is not a clean relative allowlist entry: {value!r}")
    return path


def candidate_files(source: Path) -> list[Path]:
    candidates = [source] if source.is_file() else sorted(source.rglob("*"))
    if any(candidate.is_symlink() for candidate in candidates):
        raise ValueError(f"symlink is not freezeable below: {source}")
    return [candidate for candidate in candidates if candidate.is_file()]


def files_for(root: Path, allowlist: list[str]) -> list[tuple[Path, Path]]:
    selected: dict[str, tuple[Path, Path]] = {}
    for value in allowlist:
        relative = safe_relative(value)
        source = root / relative
        if source.is_symlink() or not source.exists() or not is_within(source, root):
            raise ValueError(f"allowlisted path is missing or a symlink: {value}")
        for candidate in candidate_files(source):
            child = candidate.relative_to(root)
            selected[child.as_posix()] = (candidate, child)
    if not selected:
        raise ValueError("allowlist contains no regular files")
    return [selected[name] for name in sorted(selected)]


def freeze(root: Path, output: Path, allowlist: list[str]) -> dict[str, object]:
    root = root.resolve(strict=True)
    if output.exists():
        raise ValueError("output packet already exists")
    files = files_for(root, allowlist)
    entries = []
    for source, relative in files:
        destination = output / "files" / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)
        entries.append({"path": relative.as_posix(), "sha256": sha256_file(destination), "size": destination.stat().st_size})
    manifest = {"version": 1, "files": entries}
    encoded = canonical_bytes(manifest)
    (output / MANIFEST).write_bytes(encoded)
    return {"verdict": 1, "reason": "satisfied", "manifest_digest": hashlib.sha256(encoded).hexdigest(), "file_count": len(entries)}


def manifest_payload(packet: Path, retained_digest: str) -> tuple[dict, str]:
    encoded = (packet / MANIFEST).read_bytes()
    payload = json.loads(encoded)
    if canonical_bytes(payload) != encoded:
        raise ValueError("manifest is not canonical JSON")
    actual = hashlib.sha256(encoded).hexdigest()
    if actual != retained_digest:
        raise ValueError("externally retained manifest digest does not match")
    if not isinstance(payload, dict) or payload.get("version") != 1 or not isinstance(payload.get("files"), list):
        raise ValueError("manifest shape is invalid")
    return payload, actual


def verify_entry(packet: Path, entry: dict) -> str:
    relative = safe_relative(entry["path"])
    path = packet / "files" / relative
    if not path.is_file() or path.is_symlink():
        raise ValueError(f"packet file missing or unsafe: {relative}")
    if path.stat().st_size != entry["size"] or sha256_file(path) != entry["sha256"]:
        raise ValueError(f"packet file integrity failed: {relative}")
    return relative.as_posix()


def reject_packet_links(packet: Path, files_root: Path) -> None:
    links = (packet, packet / MANIFEST, files_root)
    if any(path.is_symlink() for path in links):
        raise ValueError("packet symlink detected")


def packet_tree(files_root: Path) -> tuple[set[str], set[str]]:
    root = files_root.resolve(strict=True)
    observed: set[str] = set()
    directories: set[str] = set()
    for current, dirnames, filenames in os.walk(files_root, followlinks=False):
        for name in (*dirnames, *filenames):
            path = Path(current) / name
            if path.is_symlink() or not is_within(path, root):
                raise ValueError("packet symlink or escape detected")
            relative = path.relative_to(files_root).as_posix()
            target = directories if path.is_dir() else observed
            target.add(relative)
    return observed, directories


def manifest_directories(expected: set[str]) -> set[str]:
    return {
        parent.as_posix() for name in expected for parent in Path(name).parents
        if parent != Path(".")
    }


def verify(packet: Path, retained_digest: str) -> dict[str, object]:
    files_root = packet / "files"
    reject_packet_links(packet, files_root)
    payload, actual = manifest_payload(packet, retained_digest)
    observed, directories = packet_tree(files_root)
    expected = {verify_entry(packet, entry) for entry in payload["files"]}
    if directories != manifest_directories(expected):
        raise ValueError("packet contains directories outside the manifest")
    if observed != expected:
        raise ValueError("packet contains files outside the manifest")
    return {"verdict": 1, "reason": "satisfied", "manifest_digest": actual, "file_count": len(expected)}


def can_read(path: Path) -> bool:
    try:
        with path.open("rb") as handle:
            handle.read(1)
        return True
    except OSError:
        return False


def can_mutate_and_restore(path: Path) -> bool:
    mutated = False
    try:
        original = path.read_bytes()
        with path.open("r+b") as handle:
            handle.seek(0, os.SEEK_END)
            mutated = True
            handle.write(b"\x00blind-spot-canary")
            handle.flush()
            os.fsync(handle.fileno())
            handle.seek(0)
            handle.write(original)
            handle.truncate(len(original))
            handle.flush()
            os.fsync(handle.fileno())
        return path.read_bytes() == original
    except OSError:
        return mutated


def is_within(path: Path, parent: Path) -> bool:
    try:
        path.resolve(strict=True).relative_to(parent.resolve(strict=True))
        return True
    except (OSError, ValueError):
        return False


def canary(packet: Path, outside_path: Path, input_path: Path) -> dict[str, object]:
    if is_within(outside_path, packet) or not is_within(input_path, packet / "files"):
        raise ValueError("canary paths do not represent outside-read and packet-input checks")
    outside_read = can_read(outside_path)
    input_write = can_mutate_and_restore(input_path)
    unisolated = outside_read or input_write
    return {"verdict": -1 if unisolated else 1, "reason": "unisolated" if unisolated else "isolated", "outside_read": outside_read, "input_write": input_write}


def parser() -> argparse.ArgumentParser:
    command = argparse.ArgumentParser(description=__doc__)
    subs = command.add_subparsers(dest="operation", required=True)
    freezing = subs.add_parser("freeze", help="Freeze allowlisted files into a packet")
    freezing.add_argument("--root", required=True, type=Path)
    freezing.add_argument("--output", required=True, type=Path)
    freezing.add_argument("--path", required=True, action="append")
    verifying = subs.add_parser("verify", help="Verify packet bytes against an external digest")
    verifying.add_argument("--packet", required=True, type=Path)
    verifying.add_argument("--digest", required=True)
    checking = subs.add_parser("canary", help="Check outside-read and input-write isolation")
    checking.add_argument("--packet", required=True, type=Path)
    checking.add_argument("--outside-path", required=True, type=Path)
    checking.add_argument("--input-path", required=True, type=Path)
    return command


def execute(args: argparse.Namespace) -> dict[str, object]:
    if args.operation == "freeze":
        return freeze(args.root, args.output, args.path)
    if args.operation == "verify":
        return verify(args.packet, args.digest)
    return canary(args.packet, args.outside_path, args.input_path)


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        result = execute(args)
    except (OSError, TypeError, ValueError, KeyError, json.JSONDecodeError) as exc:
        result = {"verdict": -1, "reason": "failure", "error": f"{type(exc).__name__}: {exc}"}
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))
    return 0 if result["verdict"] == 1 else 1


if __name__ == "__main__":
    raise SystemExit(main())
