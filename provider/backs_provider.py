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
import re
import shlex
import subprocess
import sys
import tempfile
import time
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
MINIMAX_PROFILE_FILE = Path(__file__).resolve().parent / "profiles" / "minimax.json"
MINIMAX_KEY_HELPER = HOME / ".local" / "bin" / "backs-minimax-key"
API_PROVIDERS = ("ollama", "minimax")
MANAGED_ENV_KEYS = (
    "ANTHROPIC_BASE_URL", "ANTHROPIC_AUTH_TOKEN", "ANTHROPIC_API_KEY",
    "ANTHROPIC_MODEL", "ANTHROPIC_DEFAULT_OPUS_MODEL",
    "ANTHROPIC_DEFAULT_SONNET_MODEL", "ANTHROPIC_DEFAULT_HAIKU_MODEL",
    "CLAUDE_CODE_ENABLE_GATEWAY_MODEL_DISCOVERY", "CLAUDE_CODE_SUBAGENT_MODEL",
    "CLAUDE_CODE_OAUTH_TOKEN", "CLAUDE_CODE_AUTO_COMPACT_WINDOW",
)
MANAGED_TOP_KEYS = ("apiKeyHelper", "model")
ROLE_ENV = {
    "default": "ANTHROPIC_MODEL", "opus": "ANTHROPIC_DEFAULT_OPUS_MODEL",
    "sonnet": "ANTHROPIC_DEFAULT_SONNET_MODEL", "haiku": "ANTHROPIC_DEFAULT_HAIKU_MODEL",
}
# This controller targets ollama.com. A local daemon/proxy credential must
# never be selected or sent to the cloud. Prefer explicit cloud names.
OLLAMA_KEY_ALIASES = ("OLLAMA_CLOUD_API_KEY", "OLLAMA_API_KEY")


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


def read_api_key(provider: str = "ollama") -> str:
    root = find_backs_project_root()
    backend = str(root / "backend")
    sys.path.insert(0, backend)
    try:
        # A backend import/warning must not contaminate apiKeyHelper stdout.
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            from core.env_loader import load_runtime_env
            from core.env_utils import env_secret_text
            load_runtime_env(repo_root=root, override=False)
            if provider == "ollama":
                value = env_secret_text(
                    "CLOUD_OLLAMA_API_KEY", aliases=OLLAMA_KEY_ALIASES,
                    file_aliases=("OLLAMA_API_KEY_FILE",),
                    credential_names=("cloud_ollama_api_key", "ollama_api_key"),
                ).strip()
            elif provider == "minimax":
                value = env_secret_text(
                    "MINIMAX_API_KEY", file_aliases=("MINIMAX_API_KEY_FILE",),
                    credential_names=("minimax_api_key",),
                ).strip()
            else:
                raise ProviderError("Unknown credential provider.")
    except BaseException:
        raise ProviderError("BACKS credential loader failed. Reinstall from the working BACKS Python environment; details withheld.") from None
    finally:
        sys.path.pop(0)
    if not value or any(char.isspace() or ord(char) < 32 for char in value):
        raise ProviderError("BACKS did not resolve a valid provider credential; check its API key in the existing BACKS environment. No values displayed.")
    return value


def helper_key(provider: str = "ollama") -> str:
    """Use exactly the installed helper Claude invokes, without shell activation."""
    helper = credential_helper(provider)
    if not helper.is_file():
        raise ProviderError("Installed credential helper is missing; run install-provider.sh.")
    try:
        # Retain environment semantics but force the same active project. The saved
        # Python interpreter in the launcher makes shell/IDE activation irrelevant.
        env = dict(os.environ, BACKS_PROJECT_ROOT=str(find_backs_project_root()))
        result = subprocess.run([str(helper)], env=env, cwd=HOME,
                                capture_output=True, timeout=30, check=False)
        value = result.stdout.decode("utf-8").strip()
    except (OSError, ValueError, subprocess.TimeoutExpired):
        raise ProviderError("Credential helper failed to execute; output withheld.") from None
    if result.returncode or not value or any(char.isspace() or ord(char) < 32 for char in value):
        raise ProviderError("Credential helper failed or returned malformed output; output withheld.")
    return value


def credential_helper(provider: str = "ollama") -> Path:
    if provider == "ollama":
        return KEY_HELPER
    if provider == "minimax":
        return MINIMAX_KEY_HELPER
    raise ProviderError("Unknown credential provider.")


def load_profile(provider: str = "ollama") -> dict[str, Any]:
    if provider not in API_PROVIDERS:
        raise ProviderError("Unknown provider profile.")
    path = PROFILE_FILE if provider == "ollama" else Path(
        os.environ.get("BACKS_MINIMAX_PROFILE", str(MINIMAX_PROFILE_FILE))).expanduser()
    profile = load_json(path, {})
    if not isinstance(profile, dict) or not isinstance(profile.get("endpoint"), str) or not isinstance(profile.get("roles"), dict):
        raise ProviderError("Incomplete provider profile.")
    if profile.get("provider", provider) != provider:
        raise ProviderError("Profile belongs to a different provider.")
    profile["provider"] = provider
    return profile


def endpoint(profile: dict[str, Any]) -> str:
    provider = profile.get("provider", "ollama")
    if provider not in API_PROVIDERS:
        raise ProviderError("Unknown provider endpoint.")
    value = os.environ.get("BACKS_" + provider.upper() + "_BASE_URL", profile["endpoint"]).rstrip("/")
    try:
        parsed = urllib.parse.urlsplit(value)
        port = parsed.port
    except ValueError:
        raise ProviderError("Invalid provider endpoint; value withheld.") from None
    if parsed.username or parsed.password or parsed.query or parsed.fragment:
        raise ProviderError("Provider endpoint must not contain credentials, query, or fragment.")
    hosts, path = (("ollama.com",), "") if provider == "ollama" else (
        ("api.minimax.io", "api.minimax.cn"), "/anthropic")
    if parsed.scheme != "https" or parsed.hostname not in hosts or port not in (None, 443) or parsed.path != path:
        raise ProviderError("This credential path requires the official HTTPS provider endpoint.")
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
            raise ProviderError(f"Provider Messages/catalog authentication rejected (HTTP {code}). Check the current credential in BACKS .env; configuration was not activated.") from None
        raise ProviderError(f"Provider request failed (HTTP {code}); response body withheld.") from None
    except (OSError, ValueError, urllib.error.URLError):
        raise ProviderError("Provider request failed or returned invalid data; details withheld.") from None
    if not isinstance(payload, dict):
        raise ProviderError("Provider response was not a JSON object.")
    return payload


def fetch_catalog(profile: dict[str, Any], key: str | None = None) -> list[str]:
    if profile.get("provider") == "minimax":
        # MiniMax's published compatibility list is NOT an entitlement/catalog API.
        # Activation must still prove each selected model with real inference.
        names = profile.get("models")
        if not isinstance(names, list) or not names or not all(
            isinstance(name, str) and re.fullmatch(r"MiniMax-[A-Za-z0-9][A-Za-z0-9._-]{0,100}", name)
            for name in names
        ):
            raise ProviderError("Invalid MiniMax documented model list.")
        return sorted(set(names))
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
            raise ProviderError("No listed model satisfies a configured role.")
        choice = candidates[0] if profile.get("provider") == "minimax" else next((m for m in candidates if m not in used), candidates[0])
        selected[role] = choice
        used.add(choice)
        fallbacks[role] = [m for m in candidates if m != choice]
    return selected, fallbacks


def verify_messages(profile: dict[str, Any], selected: dict[str, str], key: str) -> None:
    """Real inference preflight; MiniMax additionally requires streaming/tool use."""
    if profile.get("provider") == "minimax":
        verify_minimax(profile, selected, key)
        return
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
    settings["model"] = selected["default"]


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


def extend_baseline(baseline: dict[str, Any], settings: dict[str, Any]) -> None:
    original = snapshot(settings)
    for group in ("env", "top"):
        for key, value in original[group].items():
            baseline.setdefault(group, {}).setdefault(key, value)


def activate_provider(settings: dict[str, Any], state: dict[str, Any], provider: str) -> None:
    root = find_backs_project_root()
    check_policy(root)
    local_path = root / ".claude/settings.local.json"
    local = load_json(local_path, {})
    previous_project = state.get("project_overlay")
    if previous_project and previous_project.get("path") != str(local_path):
        raise ProviderError("A different project's overlay is active. Restore Claude before changing the bound project.")
    profile = load_profile() if provider == "ollama" else load_profile(provider)
    base = endpoint(profile)  # Validate before resolving any credential.
    key = helper_key() if provider == "ollama" else helper_key(provider)
    available = fetch_catalog(profile, key)
    selected, fallbacks = resolve_lineup(profile, available)
    verify_messages(profile, selected, key)
    del key
    # Preserve the native baseline across ANY sequence of third-party switches.
    if not isinstance(state.get("baseline"), dict) or state.get("provider") not in API_PROVIDERS:
        state["baseline"] = snapshot(settings)
    else:
        extend_baseline(state["baseline"], settings)
    if not previous_project:
        state["project_overlay"] = {"path": str(local_path), "baseline": snapshot(local), "existed": local_path.exists()}
    else:
        extend_baseline(previous_project["baseline"], local)
    # Clear the previous provider's owned settings, including context limits,
    # before applying the next profile. Unrelated hooks/MCP/preferences survive.
    restore_snapshot(settings, state["baseline"])
    restore_snapshot(local, state["project_overlay"]["baseline"])
    for target in (settings, local):
        if provider == "ollama":
            apply_ollama(target, selected, base)
        else:
            apply_minimax(target, selected, base, profile)
    state.update({"provider": provider, "profile": provider, "selected": selected, "fallbacks": fallbacks,
                  "messages_preflight": "passed", "catalog_size": len(available)})
    commit_changes({STATE_FILE: state, CLAUDE_SETTINGS: settings, local_path: local})


def activate_ollama(settings: dict[str, Any], state: dict[str, Any]) -> None:
    activate_provider(settings, state, "ollama")


def activate_minimax(settings: dict[str, Any], state: dict[str, Any]) -> None:
    activate_provider(settings, state, "minimax")


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
    for key in ("baseline", "profile", "selected", "fallbacks", "catalog_size", "project_overlay", "messages_preflight"):
        state.pop(key, None)
    changes[STATE_FILE] = state
    commit_changes(changes)


def status(settings: dict[str, Any], state: dict[str, Any]) -> int:
    provider = state.get("provider", "unmanaged")
    print("provider:", provider)
    if provider in API_PROVIDERS:
        print("endpoint:", "official MiniMax Anthropic API" if provider == "minimax" else "official Ollama cloud")
        for role, model in state.get("selected", {}).items():
            print(f"{role:7}: {model}")
        print("saved preflight:", state.get("messages_preflight", "not performed by this version"))
        print("Saved configuration only; this does not inspect the running IDE transport.")
        print("Alternatives are catalog-selection fallbacks, not live request retry.")
    else:
        print("transport: prior Claude settings; OAuth authentication is not verified here")
    return 0



def request_stream(url: str, key: str, body: dict[str, Any]) -> dict[str, Any]:
    """Read a bounded Anthropic SSE response, preserving complete content blocks."""
    headers = {"Authorization": f"Bearer {key}", "x-api-key": key,
               "anthropic-version": "2023-06-01", "Content-Type": "application/json",
               "Accept": "text/event-stream"}
    req = urllib.request.Request(url, data=json.dumps(body).encode(), headers=headers, method="POST")
    message, blocks, partial, opened, closed = None, {}, {}, set(), set()
    total, event_lines, stopped = 0, [], False
    deadline = time.monotonic() + 90
    try:
        with urllib.request.build_opener(NoRedirect).open(req, timeout=90) as response:
            if "text/event-stream" not in response.headers.get("Content-Type", ""):
                raise ProviderError("MiniMax did not return a streaming response.")
            while True:
                raw = response.readline(65537)
                total += len(raw)
                if total > 2_000_000 or len(raw) > 65536 or time.monotonic() > deadline:
                    raise ProviderError("MiniMax stream exceeded the preflight budget.")
                if not raw:
                    break
                line = raw.decode("utf-8").rstrip("\r\n")
                if line:
                    if line.startswith("data:"):
                        event_lines.append(line[5:].lstrip())
                    continue
                if not event_lines:
                    continue
                event = json.loads("\n".join(event_lines))
                event_lines = []
                kind = event.get("type")
                if kind == "error":
                    raise ProviderError("MiniMax returned a streaming error; details withheld.")
                if kind == "message_start":
                    if message is not None:
                        raise ProviderError("MiniMax returned duplicate message starts.")
                    message = event["message"]
                    if not isinstance(message, dict) or message.get("type") != "message" or message.get("role") != "assistant":
                        raise ProviderError("MiniMax stream did not start an assistant message.")
                elif kind == "content_block_start":
                    index, block = event["index"], event["content_block"]
                    if message is None or type(index) is not int or index != len(blocks) or not isinstance(block, dict):
                        raise ProviderError("MiniMax stream returned an invalid content block.")
                    blocks[index] = copy.deepcopy(block)
                    opened.add(index)
                elif kind == "content_block_delta":
                    index, delta = event["index"], event["delta"]
                    if index not in opened or index in closed:
                        raise ProviderError("MiniMax stream returned an out-of-order delta.")
                    dtype = delta.get("type")
                    if dtype == "input_json_delta":
                        partial[index] = partial.get(index, "") + delta["partial_json"]
                    else:
                        field = {"text_delta": "text", "thinking_delta": "thinking", "signature_delta": "signature"}.get(dtype)
                        if field is None:
                            raise ProviderError("MiniMax stream returned an unsupported delta.")
                        blocks[index][field] = blocks[index].get(field, "") + delta[field]
                elif kind == "content_block_stop":
                    index = event["index"]
                    if index not in opened or index in closed:
                        raise ProviderError("MiniMax stream returned an invalid block stop.")
                    if index in partial:
                        blocks[index]["input"] = json.loads(partial[index])
                        if not isinstance(blocks[index]["input"], dict):
                            raise ProviderError("MiniMax tool input was not an object.")
                    closed.add(index)
                elif kind == "message_delta":
                    if message is None:
                        raise ProviderError("MiniMax stream returned an out-of-order message delta.")
                    message.update(event.get("delta", {}))
                elif kind == "message_stop":
                    stopped = True
                    break
                elif kind != "ping":
                    raise ProviderError("MiniMax stream returned an unsupported event.")
    except urllib.error.HTTPError as exc:
        code = exc.code
        exc.close()
        raise ProviderError(f"MiniMax stream request failed (HTTP {code}); details withheld.") from None
    except (OSError, ValueError, TypeError, KeyError, AttributeError, urllib.error.URLError):
        raise ProviderError("MiniMax stream failed or returned malformed data; details withheld.") from None
    if not stopped or message is None or not blocks or opened != closed:
        raise ProviderError("MiniMax stream ended before a complete assistant message.")
    message["content"] = [blocks[i] for i in range(len(blocks))]
    return message


def verify_minimax(profile: dict[str, Any], selected: dict[str, str], key: str) -> None:
    """Two requests per distinct model; the local echo tool has no side effects."""
    if set(selected) != set(ROLE_ENV) or not all(isinstance(v, str) and v in fetch_catalog(profile) for v in selected.values()):
        raise ProviderError("MiniMax selected roles are incomplete or not in the documented model list.")
    url = endpoint(profile) + "/v1/messages"
    tool = {"name": "backs_provider_probe", "description": "Echo a fixed provider connectivity check.",
            "input_schema": {"type": "object", "properties": {"echo": {"type": "string", "enum": ["BACKS_OK"]}},
                             "required": ["echo"], "additionalProperties": False}}
    for model in dict.fromkeys(selected.values()):
        messages = [{"role": "user", "content": "Call backs_provider_probe with echo BACKS_OK. After its result, reply with BACKS_OK only."}]
        body = {"model": model, "max_tokens": 1024, "stream": True, "messages": messages,
                "tools": [tool], "tool_choice": {"type": "tool", "name": "backs_provider_probe"}}
        if model == "MiniMax-M3":
            body["thinking"] = {"type": "disabled"}
        first = request_stream(url, key, body)
        calls = [b for b in first["content"] if b.get("type") == "tool_use"]
        if (first.get("model") != model or first.get("stop_reason") != "tool_use" or len(calls) != 1
                or calls[0].get("name") != tool["name"] or calls[0].get("input") != {"echo": "BACKS_OK"}
                or not isinstance(calls[0].get("id"), str) or not calls[0]["id"]):
            raise ProviderError("MiniMax did not complete the expected streaming tool call.")
        # Preserve thinking, signature, text and tool_use exactly as the API sent them.
        messages = messages + [{"role": "assistant", "content": first["content"]},
                               {"role": "user", "content": [{"type": "tool_result", "tool_use_id": calls[0]["id"], "content": "BACKS_OK"}]}]
        followup = dict(body, stream=False, messages=messages)
        followup.pop("tool_choice", None)
        result = request_json(url, key, followup)
        content = result.get("content", [])
        if not isinstance(content, list) or not all(isinstance(block, dict) for block in content):
            raise ProviderError("MiniMax returned invalid tool-result content.")
        texts = [b.get("text", "") for b in content if b.get("type") == "text"]
        if (result.get("type") != "message" or result.get("role") != "assistant" or result.get("model") != model
                or result.get("stop_reason") != "end_turn" or not all(isinstance(t, str) for t in texts)
                or "BACKS_OK" not in "".join(texts)):
            raise ProviderError("MiniMax did not complete the tool-result round trip.")


def apply_minimax(settings: dict[str, Any], selected: dict[str, str], base: str, profile: dict[str, Any]) -> None:
    context = profile.get("context_windows", {})
    windows = [context.get(model) for model in selected.values()]
    if not all(type(window) is int and 4096 <= window <= 2_000_000 for window in windows):
        raise ProviderError("MiniMax profile needs a valid context window for every selected model.")
    lineup = {role: model + ("[1m]" if context[model] >= 1_000_000 else "") for role, model in selected.items()}
    # Reuse the auth neutralization and complete role mapping; replace only the
    # provider-specific helper and discovery/context settings.
    apply_ollama(settings, lineup, base)
    settings["apiKeyHelper"] = shlex.quote(str(MINIMAX_KEY_HELPER))
    settings["env"]["CLAUDE_CODE_ENABLE_GATEWAY_MODEL_DISCOVERY"] = "0"
    settings["env"]["CLAUDE_CODE_AUTO_COMPACT_WINDOW"] = str(min(windows))


def main() -> int:
    args = sys.argv[1:]
    action = args[0].strip().lower() if args else "status"
    target = args[1] if len(args) == 2 else None
    actions = {"__key", "__minimax_key", "claude", "ollama", "minimax", "status", "models", "doctor", "update"}
    if len(args) > 2 or action not in actions or (target is not None and (action not in ("models", "doctor") or target not in API_PROVIDERS)):
        print("usage: backs-provider [claude|ollama|minimax|status|models [ollama|minimax]|doctor [ollama|minimax]|update]", file=sys.stderr)
        return 2
    try:
        if action in ("__key", "__minimax_key"):
            sys.stdout.write(read_api_key() if action == "__key" else read_api_key("minimax"))
            return 0
        if action == "update":
            return subprocess.run([str(HOME / ".local/bin/backs-aios-update")], check=False).returncode
        if action in ("doctor", "models"):
            state = load_json(STATE_FILE, {})
            if not isinstance(state, dict):
                raise ProviderError("Invalid provider state root.")
            provider = target or (state.get("provider") if state.get("provider") in API_PROVIDERS else "ollama")
            profile = load_profile() if provider == "ollama" else load_profile(provider)
            # The documented MiniMax list needs no credential or invented catalog API.
            key = None if action == "models" and provider == "minimax" else helper_key(provider)
            available = fetch_catalog(profile, key)
            selected, fallbacks = resolve_lineup(profile, available)
            if action == "doctor":
                if state.get("provider") == provider and isinstance(state.get("selected"), dict):
                    selected = state["selected"]
                verify_messages(profile, selected, key)
                print("PASS: installed helper and Messages API accepted all selected roles.")
                if provider == "minimax":
                    print("PASS: streaming tool call and tool-result round trip.")
                print("No Claude settings were changed. IDE session remains to be tested.")
            else:
                label = "documented (not account discovery)" if provider == "minimax" else "discovered"
                print(f"{label}: {len(available)} {provider} model(s)")
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
            if action in API_PROVIDERS:
                activate_provider(settings, state, action)
                print("PASS: installed credential helper and real Messages API preflight.")
                if action == "minimax":
                    print("PASS: streaming tool call and tool-result round trip.")
            else:
                activate_claude(settings, state)
            status(settings, state)
            print("Configuration saved. Start a NEW local Claude Code IDE session; an existing process is not hot-switched.")
            if any(os.environ.get(k) for k in ("ANTHROPIC_AUTH_TOKEN", "ANTHROPIC_API_KEY", "ANTHROPIC_BASE_URL", "CLAUDE_CODE_OAUTH_TOKEN")):
                print("NOTE: inherited Anthropic routing/auth variables detected. Restart from a clean shell; settings cannot change a parent process.")
        return 0
    except ProviderError as exc:
        print("ERROR:", exc, file=sys.stderr)
        return 1
    except (OSError, ValueError, TypeError, KeyError, AttributeError):
        print("ERROR: provider operation failed; details withheld to protect credentials.", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
