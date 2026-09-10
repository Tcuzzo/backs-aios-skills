#!/usr/bin/env python3
"""BACKS Claude Code provider control plane.

Switches Claude Code between the user's existing Anthropic/OAuth path and an
Ollama-compatible provider. Ollama models are resolved from the live catalog
against ordered role preferences; credentials never live in this repository.
"""
from __future__ import annotations

import fcntl
import json
import os
import subprocess
import sys
import tempfile
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

HOME = Path.home()
CLAUDE_SETTINGS = HOME / ".claude" / "settings.json"
STATE_DIR = HOME / ".config" / "backs-aios"
STATE_FILE = STATE_DIR / "provider-state.json"
LOCK_FILE = STATE_DIR / "provider.lock"
KEY_FILE = Path(os.environ.get("BACKS_OLLAMA_KEY_FILE", STATE_DIR / "secrets" / "ollama-api-key"))
PROFILE_FILE = Path(__file__).resolve().parent / "profiles" / "ollama.json"
KEY_HELPER = HOME / ".local" / "bin" / "backs-ollama-key"

MANAGED_ENV_KEYS = (
    "ANTHROPIC_BASE_URL",
    "ANTHROPIC_AUTH_TOKEN",
    "ANTHROPIC_API_KEY",
    "ANTHROPIC_MODEL",
    "ANTHROPIC_DEFAULT_OPUS_MODEL",
    "ANTHROPIC_DEFAULT_SONNET_MODEL",
    "ANTHROPIC_DEFAULT_HAIKU_MODEL",
    "CLAUDE_CODE_ENABLE_GATEWAY_MODEL_DISCOVERY",
    "CLAUDE_CODE_SUBAGENT_MODEL",
)
MANAGED_TOP_KEYS = ("apiKeyHelper",)
ROLE_ENV = {
    "default": "ANTHROPIC_MODEL",
    "opus": "ANTHROPIC_DEFAULT_OPUS_MODEL",
    "sonnet": "ANTHROPIC_DEFAULT_SONNET_MODEL",
    "haiku": "ANTHROPIC_DEFAULT_HAIKU_MODEL",
}


def load_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"ERROR: invalid JSON in {path}: {exc}") from exc


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
        dir_fd = os.open(path.parent, os.O_DIRECTORY)
        try:
            os.fsync(dir_fd)
        finally:
            os.close(dir_fd)
    finally:
        tmp.unlink(missing_ok=True)


def snapshot(settings: dict[str, Any]) -> dict[str, Any]:
    env = settings.get("env", {})
    if not isinstance(env, dict):
        raise SystemExit(f"ERROR: settings.env in {CLAUDE_SETTINGS} is not an object")
    return {
        "env": {
            key: {"present": key in env, "value": env.get(key)}
            for key in MANAGED_ENV_KEYS
        },
        "top": {
            key: {"present": key in settings, "value": settings.get(key)}
            for key in MANAGED_TOP_KEYS
        },
    }


def restore_snapshot(settings: dict[str, Any], baseline: dict[str, Any]) -> dict[str, Any]:
    env = settings.get("env", {})
    if not isinstance(env, dict):
        raise SystemExit(f"ERROR: settings.env in {CLAUDE_SETTINGS} is not an object")

    env_baseline = baseline.get("env", {}) if isinstance(baseline, dict) else {}
    for key in MANAGED_ENV_KEYS:
        prior = env_baseline.get(key)
        if isinstance(prior, dict) and prior.get("present"):
            env[key] = prior.get("value")
        else:
            env.pop(key, None)

    if env:
        settings["env"] = env
    else:
        settings.pop("env", None)

    top_baseline = baseline.get("top", {}) if isinstance(baseline, dict) else {}
    for key in MANAGED_TOP_KEYS:
        prior = top_baseline.get(key)
        if isinstance(prior, dict) and prior.get("present"):
            settings[key] = prior.get("value")
        else:
            settings.pop(key, None)

    return settings


def read_api_key() -> str:
    value = os.environ.get("OLLAMA_API_KEY", "").strip()
    if value:
        return value
    if KEY_FILE.is_file():
        value = KEY_FILE.read_text(encoding="utf-8").strip()
        if value:
            return value
    raise SystemExit(
        "ERROR: Ollama API key not found. Export OLLAMA_API_KEY before installing "
        "or provide BACKS_OLLAMA_KEY_FILE pointing to a local 0600 key file."
    )


def load_profile() -> dict[str, Any]:
    profile = load_json(PROFILE_FILE, {})
    if not isinstance(profile, dict):
        raise SystemExit(f"ERROR: invalid Ollama profile: {PROFILE_FILE}")
    if not isinstance(profile.get("endpoint"), str) or not isinstance(profile.get("roles"), dict):
        raise SystemExit(f"ERROR: incomplete Ollama profile: {PROFILE_FILE}")
    return profile


def fetch_catalog(profile: dict[str, Any]) -> list[str]:
    fixture = os.environ.get("BACKS_OLLAMA_CATALOG_FILE")
    if fixture:
        payload = load_json(Path(fixture), {})
    else:
        key = read_api_key()
        endpoint = os.environ.get("BACKS_OLLAMA_BASE_URL", profile["endpoint"]).rstrip("/")
        path = str(profile.get("catalog_path", "/api/tags"))
        url = endpoint + (path if path.startswith("/") else "/" + path)
        request = urllib.request.Request(
            url,
            headers={
                "Authorization": f"Bearer {key}",
                "Accept": "application/json",
                "User-Agent": "backs-aios-provider/1",
            },
            method="GET",
        )
        try:
            with urllib.request.urlopen(request, timeout=12) as response:
                payload = json.loads(response.read().decode("utf-8"))
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
            raise SystemExit(f"ERROR: unable to read Ollama model catalog: {exc}") from exc

    models = payload.get("models", []) if isinstance(payload, dict) else []
    names: list[str] = []
    for item in models:
        if isinstance(item, dict):
            name = item.get("model") or item.get("name")
        elif isinstance(item, str):
            name = item
        else:
            name = None
        if isinstance(name, str) and name.strip():
            names.append(name.strip())
    if not names:
        raise SystemExit("ERROR: Ollama catalog returned no models.")
    return sorted(set(names))


def family_match(model: str, family: str) -> bool:
    model_l = model.lower()
    family_l = family.lower()
    return (
        model_l == family_l
        or model_l.startswith(family_l + ":")
        or model_l.startswith(family_l + "-cloud")
    )


def role_candidates(available: list[str], preferences: list[str]) -> list[str]:
    ordered: list[str] = []
    for family in preferences:
        matches = sorted((m for m in available if family_match(m, family)), key=len)
        for model in matches:
            if model not in ordered:
                ordered.append(model)
    return ordered


def resolve_lineup(profile: dict[str, Any], available: list[str]) -> tuple[dict[str, str], dict[str, list[str]]]:
    roles = profile.get("roles", {})
    selected: dict[str, str] = {}
    fallbacks: dict[str, list[str]] = {}
    used: set[str] = set()

    for role in ("default", "opus", "sonnet", "haiku"):
        prefs = roles.get(role)
        if not isinstance(prefs, list) or not all(isinstance(x, str) for x in prefs):
            raise SystemExit(f"ERROR: Ollama profile role {role!r} has no valid preference list.")
        candidates = role_candidates(available, prefs)
        if not candidates:
            raise SystemExit(f"ERROR: no available Ollama model satisfies role {role!r}.")
        choice = next((model for model in candidates if model not in used), candidates[0])
        selected[role] = choice
        used.add(choice)
        fallbacks[role] = [model for model in candidates if model != choice]
    return selected, fallbacks


def switch_ollama(
    settings: dict[str, Any], state: dict[str, Any]
) -> tuple[dict[str, Any], dict[str, Any]]:
    profile = load_profile()
    available = fetch_catalog(profile)
    selected, fallbacks = resolve_lineup(profile, available)

    if state.get("provider") != "ollama":
        state["baseline"] = snapshot(settings)

    env = settings.setdefault("env", {})
    if not isinstance(env, dict):
        raise SystemExit(f"ERROR: settings.env in {CLAUDE_SETTINGS} is not an object")

    env.pop("ANTHROPIC_AUTH_TOKEN", None)
    env.pop("ANTHROPIC_API_KEY", None)

    endpoint = os.environ.get("BACKS_OLLAMA_BASE_URL", profile["endpoint"]).rstrip("/")
    env["ANTHROPIC_BASE_URL"] = endpoint
    for role, env_key in ROLE_ENV.items():
        env[env_key] = selected[role]
    env["CLAUDE_CODE_ENABLE_GATEWAY_MODEL_DISCOVERY"] = "1"
    env["CLAUDE_CODE_SUBAGENT_MODEL"] = "inherit"
    settings["apiKeyHelper"] = str(KEY_HELPER)

    state.update(
        {
            "provider": "ollama",
            "profile": "ollama",
            "selected": selected,
            "fallbacks": fallbacks,
            "catalog_size": len(available),
        }
    )
    return settings, state


def switch_claude(
    settings: dict[str, Any], state: dict[str, Any]
) -> tuple[dict[str, Any], dict[str, Any]]:
    settings = restore_snapshot(settings, state.get("baseline", {}))
    state["provider"] = "claude"
    for key in ("profile", "selected", "fallbacks", "catalog_size"):
        state.pop(key, None)
    return settings, state


def display_endpoint(value: str | None) -> str:
    if not value:
        return "<unset>"
    try:
        parsed = urllib.parse.urlparse(value)
        host = (parsed.hostname or "").lower()
    except ValueError:
        return "<custom endpoint>"
    if host in {"ollama.com", "localhost", "127.0.0.1", "::1"}:
        return value
    return "<custom endpoint>"


def status(settings: dict[str, Any], state: dict[str, Any]) -> int:
    provider = state.get("provider", "claude")
    print(f"provider: {provider}")
    if provider == "ollama":
        env = settings.get("env", {}) if isinstance(settings.get("env", {}), dict) else {}
        print(f"endpoint: {display_endpoint(env.get('ANTHROPIC_BASE_URL'))}")
        selected = state.get("selected", {})
        fallbacks = state.get("fallbacks", {})
        for role in ("default", "opus", "sonnet", "haiku"):
            model = selected.get(role, "<missing>") if isinstance(selected, dict) else "<missing>"
            count = len(fallbacks.get(role, [])) if isinstance(fallbacks, dict) else 0
            print(f"{role:7}: {model}  (+{count} fallback{'s' if count != 1 else ''})")
        print(f"catalog : {state.get('catalog_size', '<unknown>')} model(s) discovered")
    else:
        print("transport: Anthropic native / existing Claude OAuth")
    return 0


def list_models() -> int:
    profile = load_profile()
    available = fetch_catalog(profile)
    selected, fallbacks = resolve_lineup(profile, available)
    print(f"discovered: {len(available)} Ollama model(s)")
    for role in ("default", "opus", "sonnet", "haiku"):
        print(f"{role}:")
        print(f"  selected: {selected[role]}")
        for model in fallbacks[role]:
            print(f"  fallback: {model}")
    return 0


def main() -> int:
    action = (sys.argv[1] if len(sys.argv) > 1 else "status").strip().lower()
    if action not in {"claude", "ollama", "status", "models", "update"}:
        print("usage: /provider [claude|ollama|status|models|update]", file=sys.stderr)
        return 2

    if action == "models":
        return list_models()

    if action == "update":
        updater = HOME / ".local" / "bin" / "backs-aios-update"
        if not updater.is_file():
            print("ERROR: backs-aios-update is not installed.", file=sys.stderr)
            return 1
        return subprocess.run([str(updater)], check=False).returncode

    STATE_DIR.mkdir(parents=True, exist_ok=True)
    LOCK_FILE.touch(mode=0o600, exist_ok=True)

    with LOCK_FILE.open("r+") as lock:
        fcntl.flock(lock.fileno(), fcntl.LOCK_EX)
        settings = load_json(CLAUDE_SETTINGS, {})
        state = load_json(STATE_FILE, {"provider": "claude"})
        if not isinstance(settings, dict) or not isinstance(state, dict):
            raise SystemExit("ERROR: provider state/settings root must be a JSON object")

        if action == "status":
            return status(settings, state)

        before_settings = json.loads(json.dumps(settings))
        before_state = json.loads(json.dumps(state))
        try:
            if action == "ollama":
                settings, state = switch_ollama(settings, state)
            else:
                settings, state = switch_claude(settings, state)
            atomic_json_write(CLAUDE_SETTINGS, settings, 0o600)
            atomic_json_write(STATE_FILE, state, 0o600)
        except BaseException:
            if before_settings != settings:
                atomic_json_write(CLAUDE_SETTINGS, before_settings, 0o600)
            if before_state != state:
                atomic_json_write(STATE_FILE, before_state, 0o600)
            raise

        status(settings, state)
        print(
            "switched: Claude Code provider profile -> "
            + ("Ollama" if action == "ollama" else "native Claude OAuth")
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
