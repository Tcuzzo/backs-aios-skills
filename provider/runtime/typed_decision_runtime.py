"""Demand-loaded, owned CPU child. Stdlib-only so the plugin uses the same bytes.

No request queue: an occupied child returns busy immediately. A request that
expires is settled by reaping its own child; it never executes later as backlog.
"""
from __future__ import annotations

import concurrent.futures
import json
import os
import signal
from pathlib import Path
import subprocess
import threading
import time
import uuid


class DecisionUnavailable(RuntimeError):
    def __init__(self, reason, status=503):
        super().__init__(reason)
        self.status = status


class TypedDecisionRuntime:
    def __init__(self, config, *, worker=None):
        self.config = dict(config)
        self.worker = Path(worker or Path(__file__).with_name("typed_decision_worker.py"))
        self._lock = threading.RLock()
        self._process = None
        self._pending = None
        self._runtime = None
        self._state = "cold"
        self._last_use = 0.
        self._closed = False

    def status(self):
        with self._lock:
            return {"status": self._state, "runtime": self._runtime,
                    "pid": self._process.pid if self._process else None,
                    "busy": self._pending is not None}

    def _start(self):
        config = self.config
        python = Path(config["python"]).expanduser()
        if not python.is_file() or not self.worker.is_file():
            raise DecisionUnavailable("isolated_runtime_missing")
        if not config.get("checkpoint"):
            raise DecisionUnavailable("checkpoint_not_configured")
        env = dict(os.environ)
        env.update(OMP_NUM_THREADS=str(config.get("cpu_threads", 2)),
                   MKL_NUM_THREADS=str(config.get("cpu_threads", 2)),
                   OPENBLAS_NUM_THREADS=str(config.get("cpu_threads", 2)), KEV_BACKEND="torch",
                   KEV_DTYPE=str(config.get("dtype", "fp32")))
        if config.get("hf_home"):
            env["HF_HOME"] = str(Path(config["hf_home"]).expanduser())
        # Serving never performs an implicit model download on a task request.
        env.update(HF_HUB_OFFLINE="1", TRANSFORMERS_OFFLINE="1")
        log_path = Path(config["log_path"])
        log_path.parent.mkdir(parents=True, exist_ok=True)
        env["BACKS_OWNED_WORKER_CONFIG"] = json.dumps(config)
        with log_path.open("ab") as log:
            process = subprocess.Popen([str(python), "-u", str(self.worker), "--run", config["checkpoint"],
                "--max-input-bytes", str(config["max_input_bytes"])], stdin=subprocess.PIPE,
                stdout=subprocess.PIPE, stderr=log, env=env, start_new_session=(os.name == "posix"))
        self._process, self._state = process, "warming"
        self._last_use = time.monotonic()
        threading.Thread(target=self._read, args=(process,), daemon=True).start()
        threading.Thread(target=self._watch, args=(process,), daemon=True).start()

    def _read(self, process):
        try:
            while True:
                raw = process.stdout.readline(self.config["max_response_bytes"] + 4097)
                if not raw:
                    raise DecisionUnavailable("worker_exited")
                if len(raw) > self.config["max_response_bytes"] + 4096 or not raw.endswith(b"\n"):
                    raise DecisionUnavailable("worker_response_budget_exceeded")
                message = json.loads(raw)
                with self._lock:
                    if self._process is not process:
                        return
                    if self._state == "warming":
                        runtime = message.get("runtime", {})
                        if (message.get("status") != "ready" or runtime.get("device") != "cpu"
                                or runtime.get("run") != self.config["checkpoint"]):
                            raise DecisionUnavailable("worker_identity_mismatch")
                        self._runtime, self._state = runtime, "ready"
                        self._last_use = time.monotonic()
                    elif self._pending:
                        request_id, future = self._pending
                        if message.get("id") != request_id:
                            raise DecisionUnavailable("worker_request_mismatch")
                        self._pending = None
                        self._last_use = time.monotonic()
                        if message.get("status") == "ready":
                            future.set_result((message["result"], request_id))
                        else:
                            future.set_exception(DecisionUnavailable(message.get("status", "worker_failure"), 422))
        except Exception as exc:
            self._stop(process, str(exc) if isinstance(exc, DecisionUnavailable) else "worker_protocol_failure")
        finally:
            if process.stdout:
                process.stdout.close()

    def _watch(self, process):
        started = time.monotonic()
        while True:
            time.sleep(.2)
            with self._lock:
                if self._process is not process:
                    return
                now = time.monotonic()
                warming_expired = self._state == "warming" and now - started > self.config.get("startup_timeout_s", 180)
                idle = self._state == "ready" and self._pending is None and now - self._last_use > self.config.get("idle_timeout_s", 120)
            if warming_expired or idle:
                self._stop(process, "startup_timeout" if warming_expired else "cold")
                return

    def _stop(self, process, reason):
        with self._lock:
            if self._process is not process:
                return
            self._state = reason
            self._runtime = None
            pending, self._pending = self._pending, None
            # The child is ours, identified by its Popen object, never a scanned PID.
            # The unreaped retained leader pins this owned process-group identity.
            # TERM lets the SDK parent reap its own child; KILL bounds settlement.
            if os.name == "posix":
                try:
                    os.killpg(process.pid, signal.SIGTERM)
                except ProcessLookupError:
                    pass
                # Do not reap the leader before killing any remaining descendants:
                # its unreaped PID prevents another process inheriting this PGID.
                time.sleep(.2)
                try:
                    os.killpg(process.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
                process.wait(timeout=.8)
            else:
                process.kill()
                process.wait(timeout=1)
            self._process = None
            if process.stdin:
                process.stdin.close()
            if pending and not pending[1].done():
                pending[1].set_exception(DecisionUnavailable(reason))

    def decide(self, payload, *, request_id=None, timeout_s=None, cancelled=None):
        data = json.dumps(payload, allow_nan=False).encode()
        if len(data) > self.config["max_input_bytes"]:
            raise DecisionUnavailable("input_budget_exceeded", 413)
        budget = min(float(timeout_s or self.config["timeout_s"]), self.config["timeout_s"])
        with self._lock:
            if cancelled is not None and cancelled.is_set():
                raise DecisionUnavailable("request_cancelled", 499)
            if self._closed:
                raise DecisionUnavailable("runtime_closed")
            if self._process is None:
                self._start()
            if cancelled is not None and cancelled.is_set():
                self._stop(self._process, "request_cancelled")
                raise DecisionUnavailable("request_cancelled", 499)
            if self._state != "ready":
                raise DecisionUnavailable("warming")
            if self._pending is not None:
                raise DecisionUnavailable("worker_busy", 429)
            process = self._process
            request_id = request_id or uuid.uuid4().hex
            future = concurrent.futures.Future()
            self._pending = (request_id, future)
            # Execution receives the full configured phase budget. Physical
            # settlement is separately bounded by _stop; never skip reaping.
            work_budget = budget
            envelope = {"id": request_id, "deadline": time.time() + work_budget, "request": payload}
            try:
                process.stdin.write((json.dumps(envelope, allow_nan=False) + "\n").encode())
                process.stdin.flush()
            except (OSError, ValueError):
                self._stop(process, "worker_pipe_failure")
                raise DecisionUnavailable("worker_pipe_failure") from None
        try:
            return future.result(timeout=work_budget)
        except concurrent.futures.TimeoutError:
            self._stop(process, "decision_timeout")
            raise DecisionUnavailable("decision_timeout", 504) from None

    def cancel(self, request_id):
        """Settle only the exact in-flight request owned by this caller."""
        with self._lock:
            if not self._pending or self._pending[0] != request_id or self._process is None:
                return False
            self._stop(self._process, "request_cancelled")
            return True

    def close(self):
        with self._lock:
            self._closed = True
            if self._process:
                self._stop(self._process, "closed")
