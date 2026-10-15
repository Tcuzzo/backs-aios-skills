"""CPU-only System One worker for an isolated Kev environment.

Standard JSON lines are the owned-parent protocol; model diagnostics go to stderr.
This file has no BACKS backend imports and is shipped unchanged to the plugin.
"""
from __future__ import annotations

import argparse
import contextlib
import json
import os
import sys
import time


def emit(value):
    sys.__stdout__.write(json.dumps(value, allow_nan=False) + "\n")
    sys.__stdout__.flush()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--run", required=True)
    parser.add_argument("--max-input-bytes", required=True, type=int)
    args = parser.parse_args()
    with contextlib.redirect_stdout(sys.stderr):
        import torch
        threads = max(1, int(os.environ.get("OMP_NUM_THREADS", "2")))
        torch.set_num_threads(threads)
        torch.set_num_interop_threads(threads)
        from kev.checkpoint import Checkpoint, LoadOptions
        from kev.device import select
        from kev.serve import Server
        from kev.api import SystemOneRequest

        device = select("cpu")
        checkpoint = Checkpoint(args.run)
        tokenizer, model = checkpoint.load(device, LoadOptions.from_env())
        server = Server(checkpoint, tokenizer, model, device)
    runtime = {"run": checkpoint.requested, "base": checkpoint.meta.base,
               "base_revision": checkpoint.meta.base_revision, "device": device,
               "backend": model.backend, "dtype": model.dtype,
               "cpu_threads":torch.get_num_threads(), "interop_threads":torch.get_num_interop_threads()}
    emit({"status": "ready", "runtime": runtime})
    try:
        while True:
            raw = sys.stdin.buffer.readline(args.max_input_bytes + 4097)
            if not raw:
                break
            if len(raw) > args.max_input_bytes + 4096 or not raw.endswith(b"\n"):
                raise ValueError("worker input envelope exceeds bound")
            envelope = json.loads(raw)
            request_id = envelope["id"]
            if time.time() >= envelope["deadline"]:
                emit({"id": request_id, "status": "expired"})
                continue
            try:
                with contextlib.redirect_stdout(sys.stderr):
                    result = server.answer(SystemOneRequest.model_validate(envelope["request"]))
                result["runtime"] = runtime
                emit({"id": request_id, "status": "ready", "result": result})
            except Exception as exc:
                emit({"id": request_id, "status": "invalid_request", "reason": type(exc).__name__})
    finally:
        with contextlib.redirect_stdout(sys.stderr):
            server.close()


if __name__ == "__main__":
    main()
