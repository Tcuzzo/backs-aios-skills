#!/usr/bin/env python3
"""Build one offline Bash installer from the current public BACKS worktree."""
from __future__ import annotations

import argparse
import base64
import gzip
import hashlib
import io
import json
import os
from pathlib import Path
import stat
import subprocess
import tarfile
import tempfile


SOURCE_ROOT = Path(__file__).resolve().parents[2]
PROGRAM_FILES = ("rollout.py", "installer.py")
SKIP_PARTS = frozenset({".git", "__pycache__", ".pytest_cache", ".mypy_cache",
                        ".ruff_cache", ".cache", "node_modules", ".venv", "venv"})
MAX_TAR_BYTES = 256 * 1024 * 1024
BEGIN = "# __BACKS_ROLLOVER_PAYLOAD_BEGIN__"
END = "# __BACKS_ROLLOVER_PAYLOAD_END__"

SHELL_HEADER = r'''#!/usr/bin/env bash
# Offline BACKS rollover installer. Inspect with --help or --dry-run.
# The embedded SHA256 detects payload corruption; it is not a publisher signature.
set -euo pipefail
umask 077
if ! command -v python3 >/dev/null 2>&1; then
  echo "Python 3.11 or newer is required. Install it, then rerun this file." >&2
  exit 2
fi
python3 -c 'import sys; sys.exit(0 if sys.version_info >= (3, 11) else "Python 3.11 or newer is required.")'
rollover_unpack_dir=$(mktemp -d "${TMPDIR:-/tmp}/backs-rollover.XXXXXXXX")
trap 'rm -rf -- "$rollover_unpack_dir"' EXIT
trap 'exit 130' INT
trap 'exit 143' TERM
python3 - "$0" "$rollover_unpack_dir" "$@" <<'BACKS_ROLLOVER_PYTHON'
'''

BOOTSTRAP = r'''import base64
import gzip
import hashlib
import io
import os
from pathlib import Path, PurePosixPath, PureWindowsPath
import stat
import subprocess
import sys
import tarfile

EXPECTED_SHA256 = "@PAYLOAD_SHA256@"
MAX_TAR_BYTES = 268435456


def fail(message):
    raise ValueError(message)


def extract_payload(encoded_script, destination):
    start = b"\n# __BACKS_ROLLOVER_PAYLOAD_BEGIN__\n"
    end = b"\n# __BACKS_ROLLOVER_PAYLOAD_END__\n"
    if encoded_script.count(start) != 1 or encoded_script.count(end) != 1:
        fail("missing or ambiguous embedded payload")
    body, trailing = encoded_script.split(start, 1)[1].split(end, 1)
    if trailing.strip():
        fail("unexpected content after the payload")
    lines = body.splitlines()
    if not lines or any(not line.startswith(b"# ") for line in lines):
        fail("invalid embedded payload encoding")
    compressed = base64.b64decode(b"".join(line[2:] for line in lines), validate=True)
    if hashlib.sha256(compressed).hexdigest() != EXPECTED_SHA256:
        fail("embedded payload checksum mismatch")
    with gzip.GzipFile(fileobj=io.BytesIO(compressed), mode="rb") as zipped:
        archive_bytes = zipped.read(MAX_TAR_BYTES + 1)
    if len(archive_bytes) > MAX_TAR_BYTES:
        fail("embedded archive exceeds the extraction limit")
    root = destination.resolve(strict=True)
    if not root.is_dir() or root.stat().st_mode & 0o077:
        fail("extraction directory must be private")
    seen = set()
    with tarfile.open(fileobj=io.BytesIO(archive_bytes), mode="r:") as archive:
        for member in archive:
            name = member.name
            parts = name.split("/")
            if (not member.isfile() or member.issparse() or "\\" in name or "\0" in name
                    or PurePosixPath(name).is_absolute() or PureWindowsPath(name).drive
                    or any(part in ("", ".", "..") for part in parts)
                    or parts[0] not in ("pack", "program") or len(parts) < 2
                    or name in seen or ".git" in parts):
                fail("unsafe or duplicate archive member")
            if parts[0] == "program" and name not in ("program/rollout.py", "program/installer.py"):
                fail("unexpected installer program")
            if member.size < 0 or member.size > MAX_TAR_BYTES:
                fail("invalid archive member size")
            seen.add(name)
            if len(seen) > 20000:
                fail("too many archive members")
            target = root.joinpath(*parts)
            target.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
            if not target.resolve().is_relative_to(root):
                fail("archive member escapes the extraction directory")
            for parent in target.parents:
                if parent == root:
                    break
                if parent.is_symlink():
                    fail("symlink parent in extraction directory")
            mode = 0o700 if member.mode & 0o111 else 0o600
            flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0)
            source = archive.extractfile(member)
            if source is None:
                fail("archive member has no data")
            with source, os.fdopen(os.open(target, flags, mode), "wb") as output:
                remaining = member.size
                while remaining:
                    chunk = source.read(min(1024 * 1024, remaining))
                    if not chunk:
                        fail("truncated archive member")
                    output.write(chunk)
                    remaining -= len(chunk)
    required = {"program/rollout.py", "program/installer.py",
                "pack/skills/backs-session-rollover/SKILL.md"}
    if not required.issubset(seen):
        fail("embedded installer is incomplete")


def main():
    arguments = sys.argv[3:]
    help_requested = any(arg in ("--help", "-h") for arg in arguments)
    safe_dry_run = "--dry-run" in arguments and not any(
        arg in ("rollback", "disable-boot") for arg in arguments)
    if hasattr(os, "geteuid") and os.geteuid() == 0 and not (help_requested or safe_dry_run):
        fail("Run this installer from your normal user account, without sudo. "
             "Root may inspect --help or --dry-run; root installation is refused.")
    options = [arg.split("=", 1)[0] for arg in arguments if arg.startswith("--") and len(arg) > 2]
    if any("--payload-root".startswith(option) for option in options):
        fail("--payload-root is reserved for this embedded installer")
    destination = Path(sys.argv[2])
    extract_payload(Path(sys.argv[1]).read_bytes(), destination)
    result = subprocess.run([sys.executable, str(destination / "program/rollout.py"),
                             "--payload-root", str(destination), *arguments], check=False)
    return result.returncode if result.returncode >= 0 else 128 - result.returncode


try:
    raise SystemExit(main())
except (ValueError, OSError, EOFError, tarfile.TarError) as error:
    print("Rollover installer stopped: " + str(error), file=sys.stderr)
    raise SystemExit(2)
'''


def source_paths(root: Path, output: Path) -> list[Path]:
    """Only tracked public paths plus explicitly staged rollover source modules."""
    result = subprocess.run(["git", "-C", str(root), "ls-files", "--cached", "-z"],
                            check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    paths = {Path(os.fsdecode(name)) for name in result.stdout.split(b"\0") if name}
    paths.update(p.relative_to(root) for p in (root / "scripts/rollover").glob("*.py"))
    selected = []
    for relative in sorted(paths):
        if (relative.is_absolute() or any(part in ("", ".", "..") for part in relative.parts)):
            raise ValueError("invalid source path")
        if SKIP_PARTS.intersection(relative.parts) or relative.suffix in {".pyc", ".pyo"}:
            continue
        source = root / relative
        if source.absolute() == output.absolute():
            continue
        for ancestor in (source, *source.parents):
            if ancestor == root:
                break
            if ancestor.is_symlink():
                raise ValueError(f"symlink source is not allowed: {relative}")
        if not stat.S_ISREG(source.lstat().st_mode):
            raise ValueError(f"source is not a regular file: {relative}")
        selected.append(relative)
    for filename in PROGRAM_FILES:
        if Path("scripts/rollover", filename) not in selected:
            raise ValueError(f"required installer module is missing: {filename}")
    return selected


def make_payload(root: Path, output: Path) -> tuple[bytes, int]:
    entries = {}
    for relative in source_paths(root, output):
        source = root / relative
        before = source.stat()
        data = source.read_bytes()
        after = source.stat()
        if (before.st_ino, before.st_size, before.st_mtime_ns) != (
                after.st_ino, after.st_size, after.st_mtime_ns):
            raise ValueError(f"source changed during packaging: {relative}")
        entries["pack/" + relative.as_posix()] = (data, 0o755 if before.st_mode & 0o111 else 0o644)
    for filename in PROGRAM_FILES:
        entries["program/" + filename] = entries["pack/scripts/rollover/" + filename]
    raw = io.BytesIO()
    with tarfile.open(fileobj=raw, mode="w", format=tarfile.PAX_FORMAT) as archive:
        for name, (data, mode) in sorted(entries.items()):
            member = tarfile.TarInfo(name)
            member.size, member.mode, member.mtime = len(data), mode, 0
            archive.addfile(member, io.BytesIO(data))
    if raw.tell() > MAX_TAR_BYTES:
        raise ValueError("source snapshot exceeds the extraction limit")
    compressed = io.BytesIO()
    with gzip.GzipFile(filename="", fileobj=compressed, mode="wb", mtime=0, compresslevel=9) as zipped:
        zipped.write(raw.getvalue())
    return compressed.getvalue(), len(entries)


def render_installer(payload: bytes) -> bytes:
    digest = hashlib.sha256(payload).hexdigest()
    bootstrap = BOOTSTRAP.replace("@PAYLOAD_SHA256@", digest)
    encoded = base64.b64encode(payload).decode("ascii")
    lines = "\n".join("# " + encoded[i:i + 76] for i in range(0, len(encoded), 76))
    return (SHELL_HEADER + bootstrap + "BACKS_ROLLOVER_PYTHON\nexit 0\n" +
            BEGIN + "\n" + lines + "\n" + END + "\n").encode("utf-8")


def build(root: Path, output: Path) -> dict:
    root, output = root.resolve(), output.expanduser().absolute()
    if output.is_symlink():
        raise ValueError("refusing to replace a symlink output")
    payload, count = make_payload(root, output)
    script = render_installer(payload)
    output.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(prefix=".rollover-installer-", dir=output.parent)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(script)
            stream.flush()
            os.fsync(stream.fileno())
        os.chmod(temporary, 0o755)
        os.replace(temporary, output)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)
    return {"output": str(output), "files": count, "bytes": len(script),
            "payload_sha256": hashlib.sha256(payload).hexdigest(),
            "installer_sha256": hashlib.sha256(script).hexdigest()}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path, help="standalone .sh artifact to write")
    args = parser.parse_args()
    try:
        print(json.dumps(build(SOURCE_ROOT, args.output), indent=2))
    except (ValueError, OSError, subprocess.CalledProcessError) as error:
        parser.exit(2, f"Installer build stopped: {error}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
