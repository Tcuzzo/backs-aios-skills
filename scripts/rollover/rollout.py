#!/usr/bin/env python3
"""Install the local rollover policy without claiming an unbound runtime is live."""
from __future__ import annotations

import argparse
import fcntl
import hashlib
import json
import os
from pathlib import Path
import platform
import plistlib
import shlex
import shutil
import subprocess
import sys
import tempfile
import time

from installer import Conflict, Transaction, discover, merge_claude, merge_codex, read_config, rollback

BEGIN = "# >>> backs-session-rollover managed >>>"
END = "# <<< backs-session-rollover managed <<<"
MD_BEGIN = "<!-- backs-session-rollover:begin -->"
MD_END = "<!-- backs-session-rollover:end -->"
CRON_BEGIN = "# BEGIN backs-session-rollover"
CRON_END = "# END backs-session-rollover"
UNIT = "backs-session-rollover"
LABEL = "local.backs.session-rollover"
OWNED = "backs-session-rollover:managed"
THRESHOLD = 125000
GLOBAL_SKILLS = (".claude/skills", ".codex/skills", ".agents/skills", ".cursor/skills", ".config/opencode/skills")
PROJECT_SKILLS = (".claude/skills", ".codex/skills", ".agents/skills", ".cursor/skills", ".opencode/skills")
SKIP_DIRS = {".git", ".hg", ".svn", "node_modules", "vendor", ".venv", "venv", "dist", "build", "Library", ".cache", ".local", ".Trash"}
SCAN_NAMES = ("Projects", "projects", "code", "src", "dev", "repos", "workspace", "workspaces", "BACKS", "backs")
CONFIG_ENV_KEYS = ("CODEX_HOME", "CLAUDE_CONFIG_DIR", "XDG_CONFIG_HOME", "BACKS_DEPLOY_ROOT", "BACKS_AI_ROOT")


def block(raw: bytes, body: str, start: str = MD_BEGIN, end: str = MD_END) -> bytes:
    text = raw.decode("utf-8")
    if text.count(start) != text.count(end) or text.count(start) > 1:
        raise Conflict("ambiguous managed block; preserve the file and review it")
    addition = start + "\n" + body.rstrip() + "\n" + end
    if start in text:
        left, tail = text.split(start, 1)
        _, right = tail.split(end, 1)
        return (left + addition + right).encode("utf-8")
    separator = "" if not text else "\n" if text.endswith("\n") else "\n\n"
    return (text + separator + addition + "\n").encode("utf-8")


def run(args: list[str], *, stdin: str | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(args, input=stdin, text=True, capture_output=True, timeout=15, check=False)


def write_report(path: Path, value: dict) -> None:
    check_dir(path.parent)
    descriptor, temporary = tempfile.mkstemp(prefix=".report-", dir=path.parent)
    try:
        with os.fdopen(descriptor, "w") as stream:
            json.dump(value, stream, indent=2)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        Path(temporary).replace(path)
    finally:
        if Path(temporary).exists():
            Path(temporary).unlink()


def scan_projects(home: Path, roots: list[Path], explicit: list[Path], enabled: bool = True) -> tuple[list[Path], list[str]]:
    found = {p.expanduser().resolve() for p in explicit}
    warnings = []
    for p in found:
        if not p.is_dir():
            raise Conflict(f"project directory is missing: {p}")
    if not enabled:
        return sorted(found), warnings
    candidates = [home / name for name in SCAN_NAMES] + roots
    candidates.extend(Path(os.environ[key]).expanduser() for key in ("BACKS_DEPLOY_ROOT", "BACKS_AI_ROOT") if os.environ.get(key))
    # Running the installer from a checkout explicitly locates that worktree.
    caller = Path.cwd().resolve()
    for ancestor in (caller, *caller.parents):
        if ancestor == home or ancestor == ancestor.parent:
            break
        if (ancestor / ".git").exists():
            found.add(ancestor)
            break
    if any((home / n).exists() for n in (".git", ".claude/settings.json", ".codex/config.toml")):
        # Home is not recursively treated as a project tree.
        candidates.extend(p for p in home.iterdir() if p.is_dir() and not p.is_symlink() and not p.name.startswith(".") and (p / ".git").exists())
    visited = 0
    for root in dict.fromkeys(p.expanduser().resolve() for p in candidates if p.exists()):
        for current, dirs, files in os.walk(root, followlinks=False):
            current_path = Path(current)
            depth = len(current_path.relative_to(root).parts)
            visited += 1
            if visited > 20000:
                warnings.append("Project scan stopped after 20000 directories; add missed projects with --project.")
                return sorted(found), warnings
            dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS and not (current_path / d).is_symlink() and (not d.startswith(".") or d in {".claude", ".codex", ".agents", ".cursor", ".opencode"})) if depth < 5 else []
            if (current_path / ".git").exists() or any((current_path / p).exists() for p in PROJECT_SKILLS) or any((current_path / p).exists() for p in (".claude/settings.json", ".claude/settings.local.json", ".codex/config.toml")):
                if current_path != home:
                    found.add(current_path)
    return sorted(found), warnings


def instruction_text(data: Path) -> str:
    return """## Automatic context and memory continuity

Load the installed `backs-session-rollover` skill at session startup and after
compaction, alongside the existing BACKS grounding and current operator rules.
Prepare a durable checkpoint at 110000 active-context tokens and request a
fresh provider session at 125000, or earlier for bounded pending input or a
smaller verified model window. Keep the original task and corrections exact;
carry verified work, failed attempts, receipts, next action and remaining
budgets through the existing task journal and memory authority.

Use the existing host controller to quiesce, verify, start an empty session,
hydrate and transfer one writer before continuing the saved step. A summary,
fork or resume of the old conversation does not establish a fresh session.
Run `backs-rollover status` for installation coverage, or read the report under
`$BACKS_ROLLOVER_HOME` (default `$HOME/.local/share/backs-rollover`). A runtime marked
UNBOUND still needs its provider/store/write-boundary integration. Preserve
operator controls, existing hooks, model choice and permission scope. Never
claim this installer is evidence that a real provider handoff ran.
"""


def inside(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def check_dir(path: Path) -> None:
    if any(character in str(path) for character in ("\n", "\r", "\0")):
        raise Conflict("paths with control characters are not supported")
    for part in [path, *path.parents]:
        if part.is_symlink():
            raise Conflict(f"refusing an unverified symlink directory: {part}")


def install_release(payload: Path, data: Path) -> Path:
    """A complete pinned source snapshot keeps relative skill references valid."""
    files = sorted(p for p in payload.rglob("*") if p.is_file())
    digest = hashlib.sha256()
    for p in files:
        if p.is_symlink():
            raise Conflict("release payload may not contain symlinks")
        digest.update(str(p.relative_to(payload)).encode() + b"\0")
        digest.update(p.read_bytes())
    release = data / "releases" / digest.hexdigest()[:24]
    check_dir(release)
    if release.is_dir():
        # Detect changes to an installed release before linking to it again.
        for p in files:
            target = release / p.relative_to(payload)
            check_dir(target.parent)
            if not target.is_file() or target.is_symlink() or target.read_bytes() != p.read_bytes():
                raise Conflict("installed release differs from its pinned source; preserved for inspection")
        return release
    check_dir(data)
    data.mkdir(parents=True, exist_ok=True, mode=0o700)
    os.chmod(data, 0o700)
    release.parent.mkdir(exist_ok=True, mode=0o700)
    stage = Path(tempfile.mkdtemp(prefix=".stage-", dir=release.parent))
    try:
        for p in files:
            target = stage / p.relative_to(payload)
            target.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
            target.write_bytes(p.read_bytes())
            target.chmod(0o700 if p.stat().st_mode & 0o111 else 0o600)
        stage.rename(release)
    finally:
        if stage.exists():
            shutil.rmtree(stage)
    return release


def add_file(plan: list[tuple], path: Path, content: bytes, mode: int | None = None, *, before: bytes | None = None) -> None:
    current = read_config(path) if before is None else before
    wrong_mode = mode is not None and path.exists() and path.stat().st_mode & 0o777 != mode
    if content != current or not path.exists() or wrong_mode:
        plan.append(("write", path, content, mode, current))


def managed_before(path: Path) -> bytes:
    raw = read_config(path)
    if raw and OWNED.encode() not in raw:
        raise Conflict(f"existing file has no rollover ownership marker: {path}")
    return raw


def add_managed_file(plan: list[tuple], report: dict, path: Path, content: bytes, mode: int = 0o600) -> None:
    try:
        before = managed_before(path)
        add_file(plan, path, content, mode, before=before)
    except (Conflict, ValueError, OSError) as exc:
        report["warnings"].append(str(exc))
        report.setdefault("managed_file_conflicts", []).append(str(path))


def make_plan(home: Path, data: Path, release: Path, projects: list[Path]) -> tuple[list[tuple], dict]:
    plan: list[tuple] = []
    report: dict = {"schema_version": 1, "threshold": THRESHOLD, "checkpoint_threshold": 110000,
                    "generated_at": time.time(), "projects": [str(p) for p in projects],
                    "native_configs": [], "skill_surfaces": [], "startup_files": [], "warnings": [],
                    "fresh_session_handoff": {"status": "UNBOUND", "reason": "The local installer cannot prove or install an unknown host provider/store/writer adapter. Bind the bundled controller at the actual BACKS launcher and run its live acceptance checks."},
                    "remote_surfaces": "Run this installer separately on each remote, container or cloud-worker image you control."}
    config_discovery = discover(home, projects)
    report["warnings"].extend(config_discovery["warnings"])
    for config in config_discovery["configs"]:
        path = Path(config["path"])
        try:
            before = read_config(path)
            result = (merge_claude if config["kind"] == "claude" else merge_codex)(before, THRESHOLD)
            add_file(plan, path, result.data, before=before)
            blocked = any("remains enabled; native compaction may be disabled" in warning for warning in result.warnings)
            if config["kind"] == "claude":
                for key in ("DISABLE_AUTO_COMPACT", "DISABLE_COMPACT"):
                    if str(os.environ.get(key, "")).lower() in ("1", "true", "yes", "on"):
                        blocked = True
                        report["warnings"].append(f"Inherited {key} disables compaction; verify the effective Claude configuration before assuming the native cap is active.")
            entry = {"path": str(path), "provider": config["kind"], "status": "CONFLICT" if blocked else "configured", "thresholds": result.thresholds}
            if blocked:
                entry["reason"] = "An existing Claude disable control remains active; the window value alone is not enabled auto-compaction."
            report["native_configs"].append(entry)
            report["warnings"].extend(f"{path}: {w}" for w in result.warnings)
        except (Conflict, ValueError, OSError) as exc:
            report["native_configs"].append({"path": str(path), "provider": config["kind"], "status": "CONFLICT", "reason": str(exc)})
    roots = [home / p for p in GLOBAL_SKILLS]
    for name in ("CODEX_HOME", "CLAUDE_CONFIG_DIR"):
        if os.environ.get(name):
            roots.append(Path(os.environ[name]).expanduser().absolute() / "skills")
    if os.environ.get("XDG_CONFIG_HOME"):
        roots.append(Path(os.environ["XDG_CONFIG_HOME"]).expanduser().absolute() / "opencode/skills")
    source_skills = release / "pack/skills"
    for root in dict.fromkeys(roots):
        entries = {"root": str(root), "new": 0, "preserved": 0, "conflicts": []}
        try:
            check_dir(root)
            for source in sorted(source_skills.iterdir()):
                if not source.is_dir() or not (source / "SKILL.md").is_file():
                    continue
                destination = root / source.name
                if destination.is_symlink():
                    current = destination.resolve()
                    if current == source:
                        entries["preserved"] += 1
                    elif inside(current, data / "releases"):
                        # Only links owned by this installer may be retargeted.
                        plan.append(("replace_link", destination, str(source), os.readlink(destination), None))
                        entries["new"] += 1
                    else:
                        entries["preserved"] += 1
                        if source.name == "backs-session-rollover":
                            entries["conflicts"].append("existing rollover skill is controlled by another installation")
                elif destination.exists():
                    entries["preserved"] += 1
                    if source.name == "backs-session-rollover":
                        entries["conflicts"].append("existing rollover skill is not owned by this installer")
                else:
                    plan.append(("link", destination, str(source), None, None))
                    entries["new"] += 1
        except (Conflict, OSError) as exc:
            entries["conflicts"].append(str(exc))
        report["skill_surfaces"].append(entries)
    # Project loaders contain no machine-specific absolute symlink targets that
    # could leak into a later source commit. Global registrations supply the pack.
    loader = b'''---
name: backs-session-rollover
description: Load the installed BACKS policy for 125000-token session rollover and durable task continuity.
---
<!-- backs-session-rollover:project-loader -->

Read the installation record at $BACKS_ROLLOVER_HOME/installation.json.
When that variable is unset, use $XDG_DATA_HOME/backs-rollover/installation.json
or the default $HOME/.local/share/backs-rollover/installation.json. Take the
verified `release` directory from that record and read
pack/skills/backs-session-rollover/SKILL.md there. Apply its complete procedure
alongside the existing native BACKS floor and operator instructions.

This portable loader does not establish a running rollover controller. Check
`backs-rollover status` and the real host acceptance trace before claiming that
automatic fresh-session handoff is active.
'''
    for project in projects:
        for relative in PROJECT_SKILLS:
            root = project / relative
            if not root.exists():
                continue
            target = root / "backs-session-rollover/SKILL.md"
            entry = {"root": str(root), "new": 0, "preserved": 0, "conflicts": []}
            try:
                raw = read_config(target)
                if raw and b"<!-- backs-session-rollover:project-loader -->" not in raw:
                    raise Conflict("project rollover skill is controlled by another installation")
                add_file(plan, target, loader, before=raw)
                entry["new"] = int(raw != loader)
                entry["preserved"] = int(raw == loader)
            except (Conflict, ValueError, OSError) as exc:
                entry["conflicts"].append(str(exc))
            report["skill_surfaces"].append(entry)
    body = instruction_text(data)
    claude_dirs = [home / ".claude"]
    codex_dirs = [home / ".codex"]
    if os.environ.get("CLAUDE_CONFIG_DIR"):
        claude_dirs.append(Path(os.environ["CLAUDE_CONFIG_DIR"]).expanduser().absolute())
    if os.environ.get("CODEX_HOME"):
        codex_dirs.append(Path(os.environ["CODEX_HOME"]).expanduser().absolute())
    instruction_paths = [p / "CLAUDE.md" for p in claude_dirs]
    instruction_paths += [p / ("AGENTS.override.md" if (p / "AGENTS.override.md").exists() else "AGENTS.md") for p in codex_dirs]
    opencode = Path(os.environ.get("XDG_CONFIG_HOME", str(home / ".config"))) / "opencode/AGENTS.md"
    if opencode.exists():
        instruction_paths.append(opencode)
    for project in projects:
        for name in ("AGENTS.override.md", "AGENTS.md", "CLAUDE.md"):
            if (project / name).is_file():
                instruction_paths.append(project / name)
        cursor_rule = project / ".cursor/rules/backs-session-rollover.mdc"
        if (project / ".cursor").exists():
            try:
                raw = read_config(cursor_rule)
                if raw and MD_BEGIN not in raw.decode("utf-8"):
                    raise Conflict("existing Cursor rule has no installer marker")
                content = block(raw, body) if raw else ("---\ndescription: Preserve task state across context rollover\nalwaysApply: true\n---\n\n" + block(b"", body).decode()).encode()
                add_file(plan, cursor_rule, content, before=raw)
                report["startup_files"].append(str(cursor_rule))
            except (Conflict, ValueError, OSError) as exc:
                report["warnings"].append(f"{cursor_rule}: {exc}")
    for path in dict.fromkeys(instruction_paths):
        try:
            before = read_config(path)
            add_file(plan, path, block(before, body), before=before)
            report["startup_files"].append(str(path))
        except (Conflict, ValueError, OSError) as exc:
            report["warnings"].append(f"{path}: {exc}")
    python = str(Path(sys.executable).resolve())
    program = str(release / "program/rollout.py")
    command = f"{shlex.quote(python)} {shlex.quote(program)} --data-dir {shlex.quote(str(data))}"
    launcher = f'#!/usr/bin/env bash\n# {OWNED}\nset -euo pipefail\nexec {command} "$@"\n'.encode()
    add_managed_file(plan, report, home / ".local/bin/backs-rollover", launcher, 0o700)
    for provider in ("claude", "codex"):
        wrapper = f'#!/usr/bin/env bash\n# {OWNED}\nset -euo pipefail\nif ! {command} reconcile --quiet; then\n  printf "%s\\n" "Rollover configuration has conflicts; inspect backs-rollover status." >&2\nfi\n'
        # Native merged configuration preserves stricter existing caps. Do not
        # override those with a larger forced CLI flag or environment value.
        wrapper += f'exec {provider} "$@"\n'
        add_managed_file(plan, report, home / f".local/bin/backs-{provider}", wrapper.encode(), 0o700)
    env_path = data / "env.sh"
    env = f'# {OWNED}\nexport BACKS_ROLLOVER_HOME={shlex.quote(str(data))}\n' + f'case ":${{PATH-}}:" in *:{shlex.quote(str(home / ".local/bin"))}:*) ;; *) export PATH={shlex.quote(str(home / ".local/bin"))}:"${{PATH-}}" ;; esac\n'
    add_managed_file(plan, report, env_path, env.encode(), 0o600)
    for name in (".profile", ".bashrc", ".bash_profile", ".bash_login", ".zshrc", ".zprofile"):
        path = home / name
        if path.exists() or name == ".profile":
            try:
                source = f"[ ! -r {shlex.quote(str(env_path))} ] || . {shlex.quote(str(env_path))}"
                before = read_config(path)
                add_file(plan, path, block(before, source, BEGIN, END), before=before)
            except (Conflict, ValueError, OSError) as exc:
                report["warnings"].append(f"{path}: {exc}")
    report["command"] = command
    return plan, report


def configure_boot(tx: Transaction, report: dict, home: Path, data: Path, choice: str, enable_linger: bool) -> None:
    if choice == "none":
        # Remove only this installer's named startup jobs, preserving other jobs.
        if (data / "installation.json").exists():
            stopped = stop_boot(home)
        else:
            stopped = {"success": True, "operations": []}
        report["boot"] = {"status": "disabled" if stopped["success"] else "stop_incomplete", "scope": "none", "stop_result": stopped}
        return
    command = report["command"] + " reconcile --quiet --from-boot"
    system = platform.system()
    if system == "Darwin" and choice in ("auto", "launchd"):
        path = home / "Library/LaunchAgents" / f"{LABEL}.plist"
        value = {"Label": LABEL, "ProgramArguments": shlex.split(command), "RunAtLoad": True, "StartInterval": 900,
                 "StandardOutPath": str(data / "boot.log"), "StandardErrorPath": str(data / "boot.log"),
                 "EnvironmentVariables": {k: os.environ[k] for k in CONFIG_ENV_KEYS if k in os.environ}}
        before = managed_before(path)
        xml = plistlib.dumps(value).replace(b"\n", f"\n<!-- {OWNED} -->\n".encode(), 1)
        tx.write(path, xml, 0o600, expected_before=before)
        domain = f"gui/{os.getuid()}"
        run(["launchctl", "bootout", f"{domain}/{LABEL}"])
        outcome = run(["launchctl", "bootstrap", domain, str(path)])
        report["boot"] = {"status": "enabled" if outcome.returncode == 0 else "written_not_loaded", "mechanism": "launchd", "scope": "user login and every 15 minutes", "path": str(path)}
        return
    if system == "Linux" and choice in ("auto", "systemd") and shutil.which("systemctl"):
        probe = run(["systemctl", "--user", "show-environment"])
        if probe.returncode == 0:
            units = home / ".config/systemd/user"
            # systemd does not execute these fields through a shell.
            argv = shlex.split(command)
            quoted = " ".join('"' + a.replace("\\", "\\\\").replace('"', '\\"').replace("%", "%%").replace("$", "$$") + '"' for a in argv)
            service_path, timer_path = units / f"{UNIT}.service", units / f"{UNIT}.timer"
            service_before, timer_before = managed_before(service_path), managed_before(timer_path)
            tx.write(service_path, (f"# {OWNED}\n[Unit]\nDescription=Reconcile the BACKS context rollover installation\n\n[Service]\nType=oneshot\nExecStart={quoted}\nUMask=0077\n").encode(), 0o600, expected_before=service_before)
            tx.write(timer_path, (f"# {OWNED}\n[Unit]\nDescription=Load BACKS rollover policy at startup\n\n[Timer]\nOnStartupSec=30s\nOnUnitActiveSec=15min\nUnit={UNIT}.service\n\n[Install]\nWantedBy=timers.target\n").encode(), 0o600, expected_before=timer_before)
            linger = False
            if shutil.which("loginctl"):
                if enable_linger:
                    run(["loginctl", "enable-linger", str(os.getuid())])
                result = run(["loginctl", "show-user", str(os.getuid()), "-p", "Linger", "--value"])
                linger = result.returncode == 0 and result.stdout.strip() == "yes"
            reloaded = run(["systemctl", "--user", "daemon-reload"])
            if reloaded.returncode != 0:
                report["boot"] = {"status": "written_not_loaded", "mechanism": "systemd-user", "reason": "systemctl --user daemon-reload failed", "exit_code": reloaded.returncode}
                return
            outcome = run(["systemctl", "--user", "enable", "--now", f"{UNIT}.timer"])
            report["boot"] = {"status": "enabled" if outcome.returncode == 0 else "written_not_loaded", "mechanism": "systemd-user", "scope": "boot and every 15 minutes" if linger else "user login and every 15 minutes", "linger": linger}
            if not linger:
                report["warnings"].append("User systemd starts at login on this host. Use --enable-linger if you want this user service before login; it may require administrator authorization.")
            return
    if choice in ("auto", "cron") and shutil.which("crontab"):
        previous = run(["crontab", "-l"])
        if previous.returncode != 0 and "no crontab" not in (previous.stderr + previous.stdout).lower():
            report["boot"] = {"status": "CONFLICT", "reason": "Could not read the existing crontab; it was preserved."}
            return
        log = shlex.quote(str(data / "boot.log"))
        cron_command = (command + f" >>{log} 2>&1").replace("%", "\\%")
        updated = block(previous.stdout.encode() if previous.returncode == 0 else b"", f"@reboot {cron_command}\n*/15 * * * * {cron_command}", CRON_BEGIN, CRON_END).decode()
        if updated != previous.stdout:
            tx.write(data / "crontab-before.txt", previous.stdout.encode(), 0o600)
            outcome = run(["crontab", "-"], stdin=updated)
        else:
            outcome = previous
        report["boot"] = {"status": "enabled" if outcome.returncode == 0 else "written_not_loaded", "mechanism": "cron", "scope": "boot and every 15 minutes when the cron daemon is running"}
        return
    report["boot"] = {"status": "UNAVAILABLE", "reason": "No supported user scheduler was available. Shell startup loading is installed."}


def processes() -> list[dict]:
    if not shutil.which("ps"):
        return []
    result = run(["ps", "-u", str(os.getuid()), "-o", "pid=,comm="])
    matches = []
    for line in result.stdout.splitlines():
        parts = line.strip().split(None, 1)
        if len(parts) == 2 and any(p in Path(parts[1]).name.lower() for p in ("claude", "codex", "opencode", "cursor", "hydra")):
            matches.append({"pid": int(parts[0]), "program": Path(parts[1]).name, "status": "not restarted; existing task state preserved"})
    return matches


def print_report(report: dict) -> None:
    print(f"Native context target: {report['threshold']:,}; checkpoint target: {report['checkpoint_threshold']:,}.")
    for entry in report["native_configs"]:
        print(f"  {entry['provider']}: {entry['status']} — {entry['path']}")
    print(f"Skill locations: {len(report['skill_surfaces'])}; discovered/registered projects: {len(report['projects'])}.")
    print("Startup: " + json.dumps(report.get("boot", {}), ensure_ascii=False))
    print("Fresh-session handoff: " + report["fresh_session_handoff"]["status"])
    print("The provider adapter, durable store, and enforced writer transfer still need live BACKS integration.")
    if report.get("active_processes"):
        print(f"Existing coder processes found: {len(report['active_processes'])}. None were interrupted.")
    conflicts = [p for p in report["native_configs"] if p["status"] == "CONFLICT"]
    conflicts += [p for p in report["skill_surfaces"] if p["conflicts"]]
    if conflicts:
        print(f"Unresolved installation conflicts: {len(conflicts)}; inspect the report before assuming coverage.")
    for warning in report["warnings"]:
        print("NOTE: " + warning)
    print("Report: " + report["report_path"])
    if report.get("transaction_manifest"):
        print("Rollback receipt: " + report["transaction_manifest"])


def stop_boot(home: Path) -> dict:
    notes = []
    timer = home / ".config/systemd/user" / f"{UNIT}.timer"
    if shutil.which("systemctl") and timer.exists() and OWNED.encode() in read_config(timer):
        result = run(["systemctl", "--user", "disable", "--now", f"{UNIT}.timer"])
        notes.append({"operation": "stop systemd timer", "exit_code": result.returncode})
        service_result = run(["systemctl", "--user", "stop", f"{UNIT}.service"])
        notes.append({"operation": "stop systemd reconciliation service", "exit_code": service_result.returncode})
    plist = home / "Library/LaunchAgents" / f"{LABEL}.plist"
    if platform.system() == "Darwin" and shutil.which("launchctl") and plist.exists() and OWNED.encode() in read_config(plist):
        result = run(["launchctl", "bootout", f"gui/{os.getuid()}/{LABEL}"])
        # A previously unloaded label is already stopped. Confirm independently.
        remaining = run(["launchctl", "print", f"gui/{os.getuid()}/{LABEL}"])
        notes.append({"operation": "stop launchd agent", "exit_code": 0 if remaining.returncode != 0 else result.returncode or 1})
    if shutil.which("crontab"):
        result = run(["crontab", "-l"])
        if result.returncode == 0 and CRON_BEGIN in result.stdout:
            raw = result.stdout
            if raw.count(CRON_BEGIN) != 1 or raw.count(CRON_END) != 1:
                raise Conflict("ambiguous managed crontab block")
            left, tail = raw.split(CRON_BEGIN, 1)
            _, right = tail.split(CRON_END, 1)
            outcome = run(["crontab", "-"], stdin=left + right.lstrip("\n"))
            notes.append({"operation": "remove managed cron block", "exit_code": outcome.returncode})
    return {"success": all(item["exit_code"] == 0 for item in notes), "operations": notes}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", nargs="?", choices=("install", "reconcile", "status", "rollback", "disable-boot"), default="install")
    parser.add_argument("--payload-root", type=Path)
    parser.add_argument("--data-dir", type=Path)
    parser.add_argument("--project", action="append", type=Path, default=[])
    parser.add_argument("--scan-root", action="append", type=Path, default=[])
    parser.add_argument("--all", action="store_true", help="discover standard local project roots (the default)")
    parser.add_argument("--no-scan", action="store_true")
    parser.add_argument("--boot", choices=("auto", "systemd", "launchd", "cron", "none"), default="auto")
    parser.add_argument("--enable-linger", action="store_true", help="ask loginctl to keep the user scheduler running before login")
    parser.add_argument("--manifest", type=Path, help="specific transaction receipt for rollback")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--quiet", action="store_true")
    parser.add_argument("--from-boot", action="store_true", help=argparse.SUPPRESS)
    args = parser.parse_args(argv)
    caller_config_environment = {k: os.environ[k] for k in CONFIG_ENV_KEYS if k in os.environ}
    home = Path.home().resolve()
    data = (args.data_dir or Path(os.environ.get("BACKS_ROLLOVER_HOME", str(Path(os.environ.get("XDG_DATA_HOME", str(home / ".local/share"))) / "backs-rollover")))).expanduser().absolute()
    check_dir(data)
    report_path = data / "report.json"
    settings_path = data / "installation.json"
    if args.action == "status":
        if not report_path.exists():
            print("No installation report exists. Run the installer first.")
            return 2
        print_report(json.loads(read_config(report_path)))
        print("This is the last reconciliation report; run reconcile to check the files again.")
        return 0
    if args.action == "disable-boot":
        stopped = stop_boot(home)
        tx = Transaction(data / "transactions", label="disable-boot")
        if settings_path.exists():
            before = read_config(settings_path)
            state = json.loads(before)
            state["boot_disabled"] = True
            tx.write(settings_path, (json.dumps(state, indent=2) + "\n").encode(), 0o600, expected_before=before)
        tx.finish()
        if report_path.exists():
            report = json.loads(read_config(report_path))
            report["boot"] = {"status": "disabled" if stopped["success"] else "stop_incomplete", "stop_result": stopped}
            write_report(report_path, report)
        print(json.dumps(stopped, indent=2))
        print("Boot reconciliation is disabled in the local registry. Native settings remain until their transaction is rolled back.")
        return 0 if stopped["success"] else 1
    if args.action == "rollback":
        if not args.manifest:
            parser.error("rollback requires --manifest from the installation report")
        stopped = stop_boot(home)
        outcome = rollback(args.manifest)
        if report_path.exists():
            report = json.loads(read_config(report_path))
            report["installation_state"] = outcome["status"]
            report["boot"] = {"status": "disabled" if stopped["success"] else "stop_incomplete", "stop_result": stopped}
            for config in report["native_configs"]:
                config["status"] = "ROLLBACK_REVIEW"
            write_report(report_path, report)
        print(json.dumps({"boot": stopped, "rollback": outcome}, indent=2))
        return 0 if stopped["success"] and not outcome["conflicts"] else 1
    prior = json.loads(read_config(settings_path)) if settings_path.exists() else {}
    requested_projects = list(args.project)
    requested_roots = list(args.scan_root)
    if args.action == "reconcile":
        if not prior:
            raise Conflict("no prior installation to reconcile")
        if prior.get("disabled") or (args.from_boot and prior.get("boot_disabled")):
            return 0
        args.project = [Path(p) for p in prior.get("projects", [])] + args.project
        args.scan_root = [Path(p) for p in prior.get("scan_roots", [])] + args.scan_root
        args.no_scan = prior.get("no_scan", False)
        release = Path(prior["release"])
    elif args.payload_root:
        release = args.payload_root if args.dry_run else install_release(args.payload_root, data)
    elif prior:
        release = Path(prior["release"])
    else:
        raise Conflict("install requires an embedded release payload")
    if args.dry_run:
        for key, value in prior.get("config_environment", {}).items():
            os.environ.setdefault(key, value)
        projects, warnings = scan_projects(home, args.scan_root, args.project, not args.no_scan)
        plan, report = make_plan(home, data, release, projects)
        report["warnings"].extend(warnings)
        report["report_path"] = str(report_path)
        print(json.dumps({"dry_run": True, "actions": [{"operation": p[0], "path": str(p[1])} for p in plan], "report": report}, indent=2))
        return 0
    check_dir(data)
    data.mkdir(parents=True, exist_ok=True, mode=0o700)
    with (data / "install.lock").open("a") as lock:
        os.chmod(data / "install.lock", 0o600)
        fcntl.flock(lock, fcntl.LOCK_EX)
        # The persisted release and project registry must also be read under the
        # lock. A boot reconciler waiting behind an upgrade may not restore its
        # old release or drop newly registered project scopes.
        prior = json.loads(read_config(settings_path)) if settings_path.exists() else {}
        if args.action == "reconcile":
            if not prior:
                raise Conflict("installation was removed while reconciliation waited")
            if prior.get("disabled") or (args.from_boot and prior.get("boot_disabled")):
                return 0
            release = Path(prior["release"])
        args.project = list(dict.fromkeys([Path(p) for p in prior.get("projects", [])] + requested_projects))
        args.scan_root = list(dict.fromkeys([Path(p) for p in prior.get("scan_roots", [])] + requested_roots))
        args.no_scan = False if args.all else args.no_scan or prior.get("no_scan", False)
        for key in CONFIG_ENV_KEYS:
            if key in caller_config_environment and not args.from_boot:
                os.environ[key] = caller_config_environment[key]
            elif key in prior.get("config_environment", {}):
                os.environ[key] = prior["config_environment"][key]
            else:
                os.environ.pop(key, None)
        if not inside(release, data / "releases"):
            raise Conflict("installed release is outside the owned releases directory")
        projects, warnings = scan_projects(home, args.scan_root, args.project, not args.no_scan)
        plan, report = make_plan(home, data, release, projects)
        report["warnings"].extend(warnings)
        report["report_path"] = str(report_path)
        tx = Transaction(data / "transactions", label=args.action)
        for kind, path, value, mode, before in plan:
            try:
                if kind == "write":
                    tx.write(path, value, mode, expected_before=before)
                elif kind == "link":
                    tx.symlink(path, value)
                elif kind == "replace_link":
                    # Foreign links are never rewritten by make_plan. Record both
                    # targets in the transaction so rollback can restore ownership.
                    if not hasattr(tx, "replace_symlink"):
                        report["warnings"].append(f"Owned old release link needs explicit upgrade: {path}")
                    else:
                        tx.replace_symlink(path, value, expected=mode)
            except (Conflict, OSError) as exc:
                report["warnings"].append(f"Failed to apply {path}: {exc}")
                report.setdefault("apply_failures", []).append(str(path))
                for config in report["native_configs"]:
                    if config["path"] == str(path):
                        config["status"] = "APPLY_FAILED"
        settings = {"schema_version": 1, "release": str(release), "projects": [str(p) for p in projects], "scan_roots": [str(p.expanduser().resolve()) for p in args.scan_root], "no_scan": args.no_scan,
                    "boot_disabled": args.boot == "none" if args.action == "install" else prior.get("boot_disabled", False),
                    "config_environment": {k: os.environ[k] for k in CONFIG_ENV_KEYS if k in os.environ}}
        tx.write(settings_path, (json.dumps(settings, indent=2) + "\n").encode(), 0o600)
        if args.action == "install":
            try:
                configure_boot(tx, report, home, data, args.boot, args.enable_linger)
            except (Conflict, OSError, subprocess.TimeoutExpired) as exc:
                report["boot"] = {"status": "CONFLICT", "reason": str(exc)}
        else:
            old_report = json.loads(read_config(report_path)) if report_path.exists() else {}
            report["boot"] = old_report.get("boot", {"status": "unknown"})
        report["active_processes"] = processes()
        receipt = tx.finish()
        manifest = receipt.get("manifest_path") or receipt.get("manifest")
        if manifest:
            report["transaction_manifest"] = str(manifest)
        elif report_path.exists():
            report["transaction_manifest"] = json.loads(read_config(report_path)).get("transaction_manifest")
        write_report(report_path, report)
    if not args.quiet:
        print_report(report)
    conflicts = any(c["status"] in ("CONFLICT", "APPLY_FAILED") for c in report["native_configs"])
    conflicts = conflicts or any(s["conflicts"] for s in report["skill_surfaces"])
    conflicts = conflicts or bool(report.get("managed_file_conflicts")) or bool(report.get("apply_failures"))
    return 1 if conflicts else 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (Conflict, ValueError, OSError, subprocess.TimeoutExpired) as exc:
        print(f"Rollover installation stopped: {exc}", file=sys.stderr)
        raise SystemExit(2)
