#!/usr/bin/env python3
"""BACKS provider control; credentials are read in memory from the BACKS runtime.

Catalog selection is not an inference or request-time-failover guarantee.
Switching uses a real credential-helper + Messages API check before activation.
"""
from __future__ import annotations

import contextlib
import copy
import fcntl
import io
import json
import os
import shlex
import subprocess
import sys
import tempfile
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

HOME = Path.home()
CLAUDE_SETTINGS = Path(os.environ.get("CLAUDE_CONFIG_DIR", HOME / ".claude")) / "settings.json"
STATE_DIR = HOME / ".config" / "backs-aios"
STATE_FILE = STATE_DIR / "provider-state.json"
LOCK_FILE = STATE_DIR / "provider.lock"
PROJECT_FILE = STATE_DIR / "provider-control" / "project-root"
PROFILE_FILE = Path(__file__).resolve().parent / "profiles" / "ollama.json"
KEY_HELPER = HOME / ".local" / "bin" / "backs-ollama-key"
MANAGED_ENV_KEYS = (
    "ANTHROPIC_BASE_URL", "ANTHROPIC_AUTH_TOKEN", "ANTHROPIC_API_KEY",
    "ANTHROPIC_MODEL", "ANTHROPIC_DEFAULT_OPUS_MODEL",
    "ANTHROPIC_DEFAULT_SONNET_MODEL", "ANTHROPIC_DEFAULT_HAIKU_MODEL",
    "CLAUDE_CODE_ENABLE_GATEWAY_MODEL_DISCOVERY", "CLAUDE_CODE_SUBAGENT_MODEL",
    "CLAUDE_CODE_OAUTH_TOKEN",
)
MANAGED_TOP_KEYS = ("apiKeyHelper",)
ROLE_ENV = {
    "default": "ANTHROPIC_MODEL", "opus": "ANTHROPIC_DEFAULT_OPUS_MODEL",
    "sonnet": "ANTHROPIC_DEFAULT_SONNET_MODEL", "haiku": "ANTHROPIC_DEFAULT_HAIKU_MODEL",
}
OLLAMA_KEY_ALIASES = ("OLLAMA_API_KEY", "LOCAL_OLLAMA_API_KEY", "OLLAMA_CLOUD_API_KEY")


class ProviderError(Exception):
    """Messages in this class must be static and contain no secret or response body."""


def load_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return copy.deepcopy(default)
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        raise ProviderError("Cannot read provider configuration JSON; no values displayed.") from None


def atomic_json_write(path: Path, payload: Any, mode: int = 0o600) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    tmp = Path(tmp_name)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(payload, handle, indent=2, sort_keys=True)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.chmod(tmp, mode)
        os.replace(tmp, path)
        directory = os.open(path.parent, os.O_DIRECTORY)
        try:
            os.fsync(directory)
        finally:
            os.close(directory)
    finally:
        tmp.unlink(missing_ok=True)


def snapshot(settings: dict[str, Any]) -> dict[str, Any]:
    env = settings.get("env", {})
    if not isinstance(env, dict):
        raise ProviderError("settings.env must be an object.")
    return {
        "env": {key: {"present": key in env, "value": env.get(key)} for key in MANAGED_ENV_KEYS},
        "top": {key: {"present": key in settings, "value": settings.get(key)} for key in MANAGED_TOP_KEYS},
    }


def restore_snapshot(settings: dict[str, Any], baseline: dict[str, Any]) -> dict[str, Any]:
    env = settings.get("env", {})
    if not isinstance(env, dict):
        raise ProviderError("settings.env must be an object.")
    for key in MANAGED_ENV_KEYS:
        # Older snapshots did not own newer keys. Do not delete someone else's value.
        if key not in baseline.get("env", {}):
            continue
        prior = baseline["env"][key]
        if prior.get("present"):
            env[key] = prior.get("value")
        else:
            env.pop(key, None)
    if env:
        settings["env"] = env
    else:
        settings.pop("env", None)
    for key in MANAGED_TOP_KEYS:
        if key not in baseline.get("top", {}):
            continue
        prior = baseline["top"][key]
        if prior.get("present"):
            settings[key] = prior.get("value")
        else:
            settings.pop(key, None)
    return settings


def valid_project(root: Path) -> bool:
    return all((root / "backend" / "core" / file).is_file()
               for file in ("env_loader.py", "env_utils.py"))


def find_backs_project_root() -> Path:
    explicit = os.environ.get("BACKS_PROJECT_ROOT", "").strip()
    if explicit:
        root = Path(explicit).expanduser().resolve()
        if not valid_project(root):
            raise ProviderError("BACKS_PROJECT_ROOT is not a valid BACKS runtime project.")
        return root
    cwd = Path.cwd().resolve()
    for root in (cwd, *cwd.parents):
        if valid_project(root):
            return root
    if PROJECT_FILE.is_file():
        root = Path(PROJECT_FILE.read_text(encoding="utf-8").strip()).expanduser().resolve()
        if valid_project(root):
            return root
    raise ProviderError("BACKS project not found. Run install-provider.sh with the workspace root.")


def read_api_key() -> str:
    root = find_backs_project_root()
    backend = str(root / "backend")
    sys.path.insert(0, backend)
    try:
        # A backend import/warning must not contaminate apiKeyHelper stdout.
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            from core.env_loader import load_runtime_env
            from core.env_utils import env_secret_text
            load_runtime_env(repo_root=root, override=False)
            value = env_secret_text(
                "CLOUD_OLLAMA_API_KEY", aliases=OLLAMA_KEY_ALIASES,
                file_aliases=("OLLAMA_API_KEY_FILE",),
                credential_names=("cloud_ollama_api_key", "ollama_api_key"),
            ).strip()
    except BaseException:
        raise ProviderError("BACKS credential loader failed. Reinstall from the working BACKS Python environment; details withheld.") from None
    finally:
        sys.path.pop(0)
    if not value or any(char.isspace() or ord(char) < 32 for char in value):
        raise ProviderError("BACKS did not resolve a valid Ollama credential; no values displayed.")
    return value


def helper_key() -> str:
    """Use exactly the installed helper Claude invokes, without shell activation."""
    if not KEY_HELPER.is_file():
        raise ProviderError("Installed credential helper is missing; run install-provider.sh.")
    try:
        # Retain environment semantics but force the same active project. The saved
        # Python interpreter in the launcher makes shell/IDE activation irrelevant.
        env = dict(os.environ, BACKS_PROJECT_ROOT=str(find_backs_project_root()))
        result = subprocess.run([str(KEY_HELPER)], env=env, cwd=HOME,
                                capture_output=True, timeout=30, check=False)
        value = result.stdout.decode("utf-8").strip()
    except (OSError, ValueError, subprocess.TimeoutExpired):
        raise ProviderError("Credential helper failed to execute; output withheld.") from None
    if result.returncode or not value or any(char.isspace() or ord(char) < 32 for char in value):
        raise ProviderError("Credential helper failed or returned malformed output; output withheld.")
    return value


def load_profile() -> dict[str, Any]:
    profile = load_json(PROFILE_FILE, {})
    if not isinstance(profile, dict) or not isinstance(profile.get("endpoint"), str) or not isinstance(profile.get("roles"), dict):
        raise ProviderError("Incomplete Ollama profile.")
    return profile


def endpoint(profile: dict[str, Any]) -> str:
    value = os.environ.get("BACKS_OLLAMA_BASE_URL", profile["endpoint"]).rstrip("/")
    parsed = urllib.parse.urlsplit(value)
    if parsed.username or parsed.password or parsed.query or parsed.fragment:
        raise ProviderError("Provider endpoint must not contain credentials, query, or fragment.")
    # Avoid sending a real credential to an arbitrary endpoint from stale config.
    if parsed.scheme != "https" or parsed.hostname != "ollama.com" or parsed.port not in (None, 443) or parsed.path:
        raise ProviderError("This cloud credential path requires the official HTTPS Ollama origin.")
    return value


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def request_json(url: str, key: str, body: dict[str, Any] | None = None) -> dict[str, Any]:
    headers = {"Authorization": f"Bearer {key}", "Accept": "application/json"}
    if body is not None:
        headers.update({"x-api-key": key, "anthropic-version": "2023-06-01", "Content-Type": "application/json"})
    req = urllib.request.Request(url, data=None if body is None else json.dumps(body).encode(),
                                 headers=headers, method="GET" if body is None else "POST")
    try:
        with urllib.request.build_opener(NoRedirect).open(req, timeout=90) as response:
            payload = json.loads(response.read(2_000_000).decode("utf-8"))
    except urllib.error.HTTPError as exc:
        code = exc.code
        exc.close()
        if code in (401, 403):
            raise ProviderError(f"Ollama Messages/catalog authentication rejected (HTTP {code}). Check the current credential in BACKS .env; configuration was not activated.") from None
        raise ProviderError(f"Ollama request failed (HTTP {code}); response body withheld.") from None
    except (OSError, ValueError, urllib.error.URLError):
        raise ProviderError("Ollama request failed or returned invalid data; details withheld.") from None
    if not isinstance(payload, dict):
        raise ProviderError("Ollama response was not a JSON object.")
    return payload


def fetch_catalog(profile: dict[str, Any], key: str | None = None) -> list[str]:
    # A fixture may exercise catalog selection, never bypass the inference preflight.
    fixture = os.environ.get("BACKS_OLLAMA_CATALOG_FILE")
    if fixture:
        payload = load_json(Path(fixture), {})
    else:
        payload = request_json(endpoint(profile) + "/api/tags", key or helper_key())
    names = []
    for item in payload.get("models", []):
        name = (item.get("model") or item.get("name")) if isinstance(item, dict) else item
        if isinstance(name, str) and name.strip() and not any(ord(c) < 32 for c in name):
            names.append(name.strip())
    if not names:
        raise ProviderError("Ollama catalog returned no models.")
    return sorted(set(names))


def family_match(model: str, family: str) -> bool:
    model, family = model.lower(), family.lower()
    return model == family or model.startswith(family + ":") or model.startswith(family + "-cloud")


def role_candidates(available: list[str], preferences: list[str]) -> list[str]:
    return list(dict.fromkeys(model for family in preferences
                             for model in sorted(available, key=lambda m: (len(m), m))
                             if family_match(model, family)))


def resolve_lineup(profile: dict[str, Any], available: list[str]) -> tuple[dict[str, str], dict[str, list[str]]]:
    selected, fallbacks, used = {}, {}, set()
    for role in ROLE_ENV:
        prefs = profile.get("roles", {}).get(role)
        if not isinstance(prefs, list) or not all(isinstance(p, str) for p in prefs):
            raise ProviderError("Invalid role preference list.")
        candidates = role_candidates(available, prefs)
        if not candidates:
            raise ProviderError("No available Ollama model satisfies a configured role.")
        choice = next((m for m in candidates if m not in used), candidates[0])
        selected[role] = choice
        used.add(choice)
        fallbacks[role] = [m for m in candidates if m != choice]
    return selected, fallbacks


def verify_messages(profile: dict[str, Any], selected: dict[str, str], key: str) -> None:
    """Minimal real inference request, once per distinct selected model."""
    for model in dict.fromkeys(selected.values()):
        payload = request_json(endpoint(profile) + "/v1/messages", key, {
            "model": model, "max_tokens": 64, "stream": False,
            "messages": [{"role": "user", "content": "Reply with OK."}],
        })
        if payload.get("type") != "message" or payload.get("role") != "assistant" or not payload.get("content"):
            raise ProviderError("Messages API did not return an assistant message; configuration was not activated.")


def apply_ollama(settings: dict[str, Any], selected: dict[str, str], base: str) -> None:
    env = settings.setdefault("env", {})
    if not isinstance(env, dict):
        raise ProviderError("settings.env must be an object.")
    # Removing keys from one file does not neutralize inherited higher-priority auth.
    # Empty overrides avoid storing the Ollama credential in any settings file.
    env.update({"ANTHROPIC_AUTH_TOKEN": "", "ANTHROPIC_API_KEY": "", "CLAUDE_CODE_OAUTH_TOKEN": "",
                "ANTHROPIC_BASE_URL": base, "CLAUDE_CODE_ENABLE_GATEWAY_MODEL_DISCOVERY": "1",
                "CLAUDE_CODE_SUBAGENT_MODEL": selected["default"]})
    for role, key in ROLE_ENV.items():
        env[key] = selected[role]
    settings["apiKeyHelper"] = shlex.quote(str(KEY_HELPER))


def commit_changes(changes: dict[Path, dict[str, Any]]) -> None:
    """Per-file atomic replacement with rollback for ordinary write failures.

    This is not a cross-file crash-atomic transaction. Baselines are written first
    so an interrupted activation can be recovered without losing original values.
    """
    before = {p: (p.read_bytes() if p.exists() else None) for p in changes}
    written = []
    try:
        for path, payload in changes.items():
            atomic_json_write(path, payload)
            written.append(path)
    except BaseException:
        for path in reversed(written):
            if before[path] is None:
                path.unlink(missing_ok=True)
            else:
                atomic_json_write(path, json.loads(before[path]))
        raise


def check_policy(root: Path) -> None:
    # Never bypass administrator policy. Report it rather than overwriting it.
    managed = Path("/etc/claude-code/managed-settings.json")
    if managed.is_file():
        data = load_json(managed, {})
        if any(k in data for k in ("forceLoginMethod", "forceLoginOrgUUID", "forceLoginGatewayUrl", "apiKeyHelper")) or any(
            k in data.get("env", {}) for k in MANAGED_ENV_KEYS):
            raise ProviderError("Managed Claude authentication policy is present; administrator review is required.")
    cloud_modes = ("CLAUDE_CODE_USE_BEDROCK", "CLAUDE_CODE_USE_VERTEX", "CLAUDE_CODE_USE_FOUNDRY")
    if any(os.environ.get(k, "").lower() in ("1", "true") for k in cloud_modes):
        raise ProviderError("Another cloud-provider mode is active in the process environment; not changed automatically.")
    for path in (CLAUDE_SETTINGS, root / ".claude/settings.json", root / ".claude/settings.local.json"):
        data = load_json(path, {})
        if not isinstance(data, dict):
            raise ProviderError("Claude settings root must be an object.")
        if not isinstance(data.get("env", {}), dict):
            raise ProviderError("settings.env must be an object.")
        if any(k in data for k in ("forceLoginMethod", "forceLoginOrgUUID", "forceLoginGatewayUrl")):
            raise ProviderError("Explicit Claude login policy is configured; not changed automatically.")
        if any(data.get("env", {}).get(k) in (True, "1", "true") for k in
               ("CLAUDE_CODE_USE_BEDROCK", "CLAUDE_CODE_USE_VERTEX", "CLAUDE_CODE_USE_FOUNDRY")):
            raise ProviderError("Another cloud-provider mode is configured; not changed automatically.")


def activate_ollama(settings: dict[str, Any], state: dict[str, Any]) -> None:
    root = find_backs_project_root()
    check_policy(root)
    profile = load_profile()
    key = helper_key()
    available = fetch_catalog(profile, key)
    selected, fallbacks = resolve_lineup(profile, available)
    verify_messages(profile, selected, key)
    del key
    # Use project-local precedence to override the earlier project's stale routing,
    # without modifying the shared .claude/settings.json file or OAuth store.
    local_path = root / ".claude/settings.local.json"
    local = load_json(local_path, {})
    previous_project = state.get("project_overlay")
    if previous_project and previous_project.get("path") != str(local_path):
        raise ProviderError("A different project's overlay is active. Restore Claude before changing the bound project.")
    if not isinstance(state.get("baseline"), dict) or state.get("provider") != "ollama":
        state["baseline"] = snapshot(settings)
    else:
        # Extend old baseline only for newly owned keys before applying overrides.
        original = snapshot(settings)
        for group in ("env", "top"):
            for k, v in original[group].items():
                state["baseline"].setdefault(group, {}).setdefault(k, v)
    if not previous_project:
        state["project_overlay"] = {"path": str(local_path), "baseline": snapshot(local), "existed": local_path.exists()}
    apply_ollama(settings, selected, endpoint(profile))
    apply_ollama(local, selected, endpoint(profile))
    state.update({"provider": "ollama", "profile": "ollama", "selected": selected, "fallbacks": fallbacks,
                  "messages_preflight": "passed", "catalog_size": len(available)})
    commit_changes({STATE_FILE: state, CLAUDE_SETTINGS: settings, local_path: local})


def activate_claude(settings: dict[str, Any], state: dict[str, Any]) -> None:
    changes = {}
    if isinstance(state.get("baseline"), dict):
        restore_snapshot(settings, state["baseline"])
        changes[CLAUDE_SETTINGS] = settings
    overlay = state.get("project_overlay")
    if overlay:
        path = Path(overlay["path"])
        local = load_json(path, {})
        restore_snapshot(local, overlay["baseline"])
        changes[path] = local
    state["provider"] = "claude"
    for key in ("profile", "selected", "fallbacks", "catalog_size", "project_overlay", "messages_preflight"):
        state.pop(key, None)
    changes[STATE_FILE] = state
    commit_changes(changes)


def status(settings: dict[str, Any], state: dict[str, Any]) -> int:
    print("provider:", state.get("provider", "unmanaged"))
    if state.get("provider") == "ollama":
        print("endpoint: official Ollama cloud")
        for role, model in state.get("selected", {}).items():
            print(f"{role:7}: {model}")
        print("verification:", state.get("messages_preflight", "not performed by this version"))
        print("Alternatives are catalog-selection fallbacks, not live request retry.")
    else:
        print("transport: prior Claude settings; OAuth authentication is not verified here")
    return 0


def main() -> int:
    action = (sys.argv[1] if len(sys.argv) > 1 else "status").strip().lower()
    if len(sys.argv) > 2 or action not in {"__key", "claude", "ollama", "status", "models", "doctor", "update"}:
        print("usage: backs-provider [claude|ollama|status|models|doctor|update]", file=sys.stderr)
        return 2
    try:
        if action == "__key":
            sys.stdout.write(read_api_key())
            return 0
        if action == "update":
            return subprocess.run([str(HOME / ".local/bin/backs-aios-update")], check=False).returncode
        if action in ("doctor", "models"):
            profile = load_profile()
            key = helper_key()
            available = fetch_catalog(profile, key)
            selected, fallbacks = resolve_lineup(profile, available)
            if action == "doctor":
                verify_messages(profile, selected, key)
                print("PASS: installed helper and Messages API accepted all selected roles.")
                print("No Claude settings were changed. IDE session remains to be tested.")
            else:
                print(f"discovered: {len(available)} Ollama model(s)")
                for role in ROLE_ENV:
                    print(role + ":\n  selected: " + selected[role])
                    for model in fallbacks[role]:
                        print("  fallback: " + model)
            return 0
        STATE_DIR.mkdir(parents=True, exist_ok=True)
        LOCK_FILE.touch(mode=0o600, exist_ok=True)
        with LOCK_FILE.open("r+") as lock:
            fcntl.flock(lock, fcntl.LOCK_EX)
            settings = load_json(CLAUDE_SETTINGS, {})
            state = load_json(STATE_FILE, {})
            if not isinstance(settings, dict) or not isinstance(state, dict):
                raise ProviderError("Invalid settings/state root.")
            if action == "status":
                return status(settings, state)
            if action == "ollama":
                activate_ollama(settings, state)
                print("PASS: installed credential helper and real Messages API preflight.")
            else:
                activate_claude(settings, state)
            status(settings, state)
            print("Configuration saved. Start a NEW local Claude Code IDE session; an existing process is not hot-switched.")
        return 0
    except ProviderError as exc:
        print("ERROR:", exc, file=sys.stderr)
        return 1
    except (OSError, ValueError, TypeError, KeyError):
        print("ERROR: provider operation failed; details withheld to protect credentials.", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
