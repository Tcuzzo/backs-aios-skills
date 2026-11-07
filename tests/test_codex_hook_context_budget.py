"""The installed Codex registry must retain the measured BACKS context budget.

The native 0.164 host reduced the 16,325-token startup payload to a 2,500-token
preview. Query its actual plugin registry, without starting a model or trusting
any hook. The explicit positive ceiling keeps future output bounded.
"""
import importlib.util
import json
import os
from pathlib import Path
import queue
import shutil
import subprocess
import threading
import time

import pytest


ROOT = Path(__file__).resolve().parents[1]


def toml_value(value):
    if isinstance(value, dict):
        return "{" + ", ".join(json.dumps(k) + " = " + toml_value(v) for k, v in value.items()) + "}"
    if isinstance(value, list):
        return "[" + ", ".join(toml_value(v) for v in value) + "]"
    return json.dumps(value)


def test_native_registry_preserves_complete_bounded_foundation_context(tmp_path):
    codex = os.environ.get("CODEX_BIN") or shutil.which("codex")
    if not codex:
        pytest.skip("native Codex host not installed; set CODEX_BIN to run this registry contract")
    spec = importlib.util.spec_from_file_location("context_packager", ROOT / "tools/refresh_codex_local.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    stage = module.stage_bundle(ROOT, tmp_path / "packages", "context-budget-contract")
    configuration = json.loads((stage / "hooks/hooks.json").read_text())
    # Feed the packaged definitions to the real parser as transient session
    # flags. No installed plugin, trust record or operator configuration changes.
    overrides = []
    for event, handlers in configuration["hooks"].items():
        overrides += ["-c", "hooks." + event + "=" + toml_value(handlers)]
    incoming = queue.Queue()
    with (tmp_path / "native.stderr").open("w") as errors:
        process = subprocess.Popen([codex, *overrides, "app-server", "--listen", "stdio://"],
                                   stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=errors,
                                   text=True, bufsize=1)

        def read_output():
            for line in process.stdout:
                incoming.put(json.loads(line))

        reader = threading.Thread(target=read_output, daemon=True)
        reader.start()

        def request(identifier, method, params):
            process.stdin.write(json.dumps({"id": identifier, "method": method, "params": params}) + "\n")
            process.stdin.flush()
            deadline = time.monotonic() + 20
            while time.monotonic() < deadline:
                response = incoming.get(timeout=max(0.01, deadline - time.monotonic()))
                if response.get("id") == identifier:
                    assert "error" not in response, response
                    return response["result"]
            raise AssertionError("Native registry never returned the requested response")

        try:
            request(1, "initialize", {"clientInfo": {"name": "backs_context_contract", "version": "1"},
                                      "capabilities": {"experimentalApi": True}})
            process.stdin.write('{"method":"initialized","params":{}}\n')
            process.stdin.flush()
            result = request(2, "hooks/list", {"cwds": [str(stage)]})
            hooks = [h for row in result["data"] for h in row["hooks"] if h["source"] == "sessionFlags"]
            assert len(hooks) == 6
            context_hooks = [h for h in hooks if h["eventName"] in ("sessionStart", "preToolUse")]
            assert len(context_hooks) == 3
            stop_hooks = [h for h in hooks if h["eventName"] == "stop"]
            assert len(stop_hooks) == 1
            for hook in context_hooks:
                limit = hook.get("additionalContextLimit")
                assert isinstance(limit, int) and 16325 <= limit <= 32768, (
                    "Native host still replaces the measured full BACKS payload with a preview", hook)
            (tmp_path / "native-context-registry.json").write_text(json.dumps(result))
            assert (tmp_path / "native-context-registry.json").stat().st_size > 0
        finally:
            process.stdin.close()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.terminate()
                process.wait(timeout=5)
            reader.join(timeout=1)
