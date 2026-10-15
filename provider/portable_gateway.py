"""Explicitly started Anthropic relay for hosts without a native BACKS backend.

The host's configured provider is the inference destination. Needle/Kev supply
routing evidence only; they never receive provider credentials or execute tools.
"""
from __future__ import annotations

import argparse
import asyncio
import json
import os
from pathlib import Path
import signal
import threading
import time
import uuid
from urllib.parse import urlsplit

from aiohttp import ClientSession, ClientTimeout, web

from runtime.needle_process_runtime import NeedleProcessRuntime
from runtime.typed_decision_runtime import DecisionUnavailable, TypedDecisionRuntime
from runtime.typed_routing_policy import (choose_policy, collect_evidence, decision_spec,
                                         task_text, validate_choice)

AUTO_MODEL = "backs/claude-auto"
HOP_HEADERS = {"connection", "keep-alive", "proxy-authenticate", "proxy-authorization",
               "te", "trailer", "transfer-encoding", "upgrade", "host", "content-length"}


def transport_headers(headers):
    excluded = HOP_HEADERS | {item.strip().lower() for item in headers.get("Connection", "").split(",")}
    return {key: value for key, value in headers.items() if key.lower() not in excluded}


def configured_host(config):
    """Read existing host settings; do not select, edit or persist a provider."""
    if config.get("upstream"):
        return dict(config["upstream"])
    home = Path.home()
    settings_path = Path(os.environ.get("CLAUDE_CONFIG_DIR", home / ".claude")) / "settings.json"
    settings = json.loads(settings_path.read_text()) if settings_path.is_file() else {}
    project = Path(config.get("project_root") or os.environ.get("BACKS_PROJECT_ROOT") or Path.cwd()).expanduser()
    for overlay_path in (project / ".claude/settings.json", project / ".claude/settings.local.json"):
        if overlay_path.is_file():
            overlay = json.loads(overlay_path.read_text())
            merged_env = {**settings.get("env", {}), **overlay.get("env", {})}
            settings.update(overlay)
            settings["env"] = merged_env
    env = {**settings.get("env", {}), **os.environ}
    model = env.get("ANTHROPIC_MODEL") or settings.get("model")
    endpoint = env.get("ANTHROPIC_BASE_URL")
    if not endpoint or not model or model == AUTO_MODEL:
        raise ValueError("Configure the existing upstream endpoint/model, or provide upstream in the serve config")
    result = {"endpoint": endpoint, "model": model, "provider": urlsplit(endpoint).hostname,
              "api_key_helper": settings.get("apiKeyHelper"), "credential_env": env}
    return result


async def credentials(upstream):
    env = upstream.get("credential_env", {})
    if upstream.get("api_key_env"):
        key = env.get(upstream["api_key_env"]) or os.environ.get(upstream["api_key_env"], "")
        return {"x-api-key": key} if key else {}
    if upstream.get("auth_token_env"):
        token = env.get(upstream["auth_token_env"]) or os.environ.get(upstream["auth_token_env"], "")
        return {"Authorization": f"Bearer {token}"} if token else {}
    if env.get("ANTHROPIC_AUTH_TOKEN"):
        return {"Authorization": f"Bearer {env['ANTHROPIC_AUTH_TOKEN']}"}
    if env.get("ANTHROPIC_API_KEY"):
        return {"x-api-key": env["ANTHROPIC_API_KEY"]}
    if upstream.get("api_key_helper"):
        # This is the existing operator-configured host helper, never request data.
        process = await asyncio.create_subprocess_shell(
            upstream["api_key_helper"], env={**os.environ, **env}, stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.DEVNULL, start_new_session=True)
        try:
            output, _ = await asyncio.wait_for(process.communicate(), timeout=30)
        finally:
            if process.returncode is None:
                # Only the helper group created by this exact request is ours.
                try:
                    os.killpg(process.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
                await process.wait()
        if process.returncode or not output.strip():
            raise RuntimeError("configured_credential_helper_failed")
        return {"x-api-key": output.decode().strip()}
    return {}


class Selector:
    def __init__(self, config):
        config = dict(config)
        for section in ("needle", "typed_decision"):
            if config.get(section):
                config[section] = dict(config[section])
                for key in ("python", "hf_home", "log_path", "weights_path", "library_path"):
                    if config[section].get(key):
                        config[section][key] = str(Path(config[section][key]).expanduser())
        self.config = config
        self.policy = json.loads(Path(__file__).with_name("routing-policy.json").read_text())
        self.policy.update(config.get("policy", {}))
        self.upstream = configured_host(config)
        self.routes = config.get("routes") or {name: self.upstream for name in ("plan", "build", "work")}
        self.lock = threading.Lock()
        if config.get("needle"):
            config["needle"]["criteria"] = self.policy["criteria"]
        self.needle = NeedleProcessRuntime(config["needle"]) if config.get("needle") else None
        self.typed = TypedDecisionRuntime(config["typed_decision"]) if config.get("typed_decision") else None

    def select(self, body, request_id, cancelled):
        selected = body.get("model", AUTO_MODEL)
        if selected != AUTO_MODEL:
            return {**self.upstream, "model": selected}, {"source": "explicit", "fallback_reason": None}
        started = time.monotonic()
        human_text = task_text(body)
        eligible = [name for name in self.routes if name in self.policy["criteria"] and name != "none"]
        needle = {"status": "unconfigured"}
        typed = {"status": "unconfigured", "transport": "systemone"}
        if self.lock.acquire(blocking=False):
            try:
                text = human_text[:self.policy.get("max_task_chars", 4000)]

                def needle_call(phase_timeout):
                    if not self.needle:
                        return {"status": "unconfigured"}
                    try:
                        result, needle_id = self.needle.decide(
                            {"task": text, "criteria": self.policy["criteria"]},
                            request_id=request_id, cancelled=cancelled, timeout_s=phase_timeout)
                        return {**result, "request_id": needle_id}
                    except DecisionUnavailable as error:
                        return {"status": str(error)}
                    except Exception:
                        return {"status": "invalid_response", "reason": "needle_inference_failed"}

                def decision_call(needle_evidence, phase_timeout):
                    if not self.typed:
                        return {"status": "unconfigured", "transport": "systemone"}
                    try:
                        payload = json.loads(decision_spec(
                            text, needle_evidence, eligible, self.policy))
                        payload["model"] = self.config["typed_decision"]["model"]
                        answer, typed_id = self.typed.decide(
                            payload, request_id=request_id, cancelled=cancelled, timeout_s=phase_timeout)
                        if answer.get("model") != payload["model"]:
                            raise ValueError("typed_model_mismatch")
                        return {"status": "ready", "transport": "systemone", "request_id": typed_id,
                                "answer": validate_choice(answer["answers"]["routing"], self.policy["criteria"]),
                                "model": answer["model"], "usage": answer["usage"],
                                "runtime": self.typed.status()["runtime"]}
                    except DecisionUnavailable as error:
                        return {"status": str(error), "transport": "systemone"}
                    except Exception:
                        return {"status": "invalid_response", "transport": "systemone"}

                needle, typed = collect_evidence(
                    needle_call, decision_call,
                    needle_timeout_s=float(self.config.get("needle", {}).get("timeout_s", 8)),
                    decision_timeout_s=float(self.config.get("typed_decision", {}).get("timeout_s", 8)))
            finally:
                self.lock.release()
        else:
            needle = {"status": "busy"}
            typed = {"status": "busy", "transport": "systemone"}
        if cancelled.is_set():
            raise asyncio.CancelledError()
        tier, source, reason = choose_policy(needle, typed, eligible, self.policy)
        if tier not in self.routes:
            raise ValueError("No configured eligible capability route")
        override = self.routes[tier]
        route = dict(self.upstream)
        credential_fields = {"credential_env", "api_key_env", "auth_token_env", "api_key_helper"}
        destination_changed = override.get("endpoint", route["endpoint"]).rstrip("/") != route["endpoint"].rstrip("/")
        if destination_changed or credential_fields.intersection(override):
            # Credentials belong to the configured destination. A route with
            # its own auth binding must not inherit another provider's helper.
            for key in credential_fields:
                route.pop(key, None)
        route.update(override)
        return route, {"source": source, "tier": tier, "fallback_reason": reason,
                                   "needle": needle, "typed": typed,
                                   "task_chars": len(human_text),
                                   "task_truncated": len(human_text) > self.policy.get("max_task_chars", 4000),
                                   "decision_elapsed_s": time.monotonic() - started}

    def cancel(self, request_id):
        if self.needle:
            self.needle.cancel(request_id)
        if self.typed:
            self.typed.cancel(request_id)

    def close(self):
        if self.needle:
            self.needle.close()
        if self.typed:
            self.typed.close()


class Gateway:
    def __init__(self, config):
        self.config = config
        self.selector = Selector(config)
        self.client = None
        self.receipt_lock = asyncio.Lock()
        self.receipt_failures = 0
        self.last_receipt_error = None

    async def receipt(self, record):
        path = self.config.get("receipt_path")
        if path:
            async with self.receipt_lock:
                def append():
                    target = Path(path).expanduser()
                    target.parent.mkdir(parents=True, exist_ok=True)
                    with target.open("a") as handle:
                        handle.write(json.dumps(record, allow_nan=False) + "\n")
                try:
                    await asyncio.to_thread(append)
                    self.last_receipt_error = None
                except OSError as error:
                    self.receipt_failures += 1
                    self.last_receipt_error = type(error).__name__

    async def health(self, request):
        return web.json_response({"status": "ok", "backend_required": False,
                                  "receipt_failures": self.receipt_failures, "last_receipt_error": self.last_receipt_error,
                                  "needle": self.selector.needle.status() if self.selector.needle else {"status": "unconfigured"},
                                  "typed_decision": self.selector.typed.status() if self.selector.typed else {"status": "unconfigured"}})

    async def models(self, request):
        models = [AUTO_MODEL, self.selector.upstream["model"]]
        return web.json_response({"data": [{"id": name, "type": "model", "display_name": name} for name in dict.fromkeys(models)],
                                  "has_more": False, "first_id": models[0], "last_id": models[-1]})

    async def catalog(self, request):
        route = self.selector.upstream
        return web.json_response({"ok": True, "picker_model": AUTO_MODEL, "source": "portable_configured_host",
                                  "selected": {"available": True, "model": route["model"], "provider": route.get("provider"),
                                               "identity": "configured_host", "role": "builder", "transport": "anthropic_http"}})

    async def relay(self, request):
        request_id = uuid.uuid4().hex
        cancelled = threading.Event()
        response = None
        record = {"request_id": request_id, "transport": "anthropic_http", "status": "started"}
        try:
            body = await request.json()
            if not isinstance(body, dict):
                raise ValueError("Request body must be a JSON object")
            route, proof = await asyncio.to_thread(self.selector.select, body, request_id, cancelled)
            endpoint = route["endpoint"].rstrip("/")
            forwarded = {**body, "model": route["model"]}
            headers = transport_headers(request.headers)
            auth = await credentials(route)
            destination_changed = endpoint != self.selector.upstream["endpoint"].rstrip("/")
            has_auth_binding = any(route.get(key) for key in
                                    ("credential_env", "api_key_env", "auth_token_env", "api_key_helper"))
            for key in tuple(headers):
                if key.lower() == "content-encoding" or ((auth or destination_changed or has_auth_binding)
                                                        and key.lower() in {"authorization", "x-api-key"}):
                    headers.pop(key)
            headers.update(auth)
            headers["Content-Type"] = "application/json"
            # Endpoint may include the provider's /anthropic prefix. Preserve
            # query flags and the full tool/thinking/message payload unchanged.
            url = endpoint + request.rel_url.raw_path
            if request.rel_url.query_string:
                url += "?" + request.rel_url.query_string
            record.update(proof, model=route["model"], provider=route.get("provider") or urlsplit(endpoint).hostname,
                          host=urlsplit(endpoint).hostname)
            async with self.client.post(url, json=forwarded, headers=headers) as remote:
                record.update(status="response", http_status=remote.status)
                response = web.StreamResponse(status=remote.status, headers=transport_headers(remote.headers))
                await response.prepare(request)
                async for chunk in remote.content.iter_any():
                    await response.write(chunk)
                await response.write_eof()
                record["status"] = "complete"
                return response
        except asyncio.CancelledError:
            cancelled.set()
            await asyncio.to_thread(self.selector.cancel, request_id)
            record["status"] = "cancelled"
            raise
        except (ConnectionError, BrokenPipeError):
            cancelled.set()
            await asyncio.to_thread(self.selector.cancel, request_id)
            record["status"] = "disconnected"
            raise
        except Exception as error:
            record.update(status="error", error_type=type(error).__name__)
            if response and response.prepared:
                raise
            return web.json_response({"type": "error", "error": {"type": "api_error", "message": "Portable provider request failed; see the routing receipt."}}, status=502)
        finally:
            await asyncio.shield(self.receipt(record))

    async def lifetime(self, app):
        self.client = ClientSession(timeout=ClientTimeout(total=self.config.get("request_timeout_s", 180)),
                                    auto_decompress=False, trust_env=True)
        yield
        await asyncio.to_thread(self.selector.close)
        await self.client.close()


def create_app(config):
    gateway = Gateway(config)
    app = web.Application(client_max_size=0)
    app.cleanup_ctx.append(gateway.lifetime)
    app.router.add_get("/health", gateway.health)
    app.router.add_get("/v1/models", gateway.models)
    app.router.add_get("/api/system/needle_engineer_rungs", gateway.catalog)
    app.router.add_post("/v1/messages", gateway.relay)
    app.router.add_post("/v1/messages/count_tokens", gateway.relay)
    return app


async def serve(config, host, port, ready_file=None):
    runner = web.AppRunner(create_app(config), handler_cancellation=True, access_log=None,
                           shutdown_timeout=config.get("shutdown_timeout_s", 10))
    await runner.setup()
    site = web.TCPSite(runner, host, port)
    await site.start()
    actual_port = site._server.sockets[0].getsockname()[1]
    receipt = {"host": host, "port": actual_port, "pid": os.getpid(), "model": AUTO_MODEL}
    if ready_file:
        Path(ready_file).write_text(json.dumps(receipt) + "\n")
    print(json.dumps(receipt), flush=True)
    stopped = asyncio.Event()
    loop = asyncio.get_running_loop()
    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, stopped.set)
    try:
        await stopped.wait()
    finally:
        await runner.cleanup()


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=Path(__file__).with_name("portable.example.json"))
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=0)
    parser.add_argument("--ready-file", type=Path)
    args = parser.parse_args(argv)
    config = json.loads(args.config.read_text())
    asyncio.run(serve(config, args.host, args.port, args.ready_file))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
