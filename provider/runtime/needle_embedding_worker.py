"""Pinned Needle SDK/CPU engine inside an owned process group, JSON-lines protocol."""
from __future__ import annotations
import argparse
import contextlib
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import signal
import sys
import time

from typed_routing_policy import score_embeddings


def emit(value):
    sys.__stdout__.write(json.dumps(value, allow_nan=False)+'\n')
    sys.__stdout__.flush()


def terminate(_signal, _frame):
    # Unwind SDK's request lock, then its supported close reaps its own child.
    raise SystemExit(0)


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--run', required=True)
    parser.add_argument('--max-input-bytes', type=int, required=True)
    args=parser.parse_args()
    config=json.loads(os.environ['BACKS_OWNED_WORKER_CONFIG'])
    weights=Path(config['weights_path']).expanduser().resolve()
    library=Path(config['library_path']).expanduser().resolve()
    if not weights.is_file() or not library.is_file():
        raise RuntimeError('Needle isolated weights/CPU engine missing')
    os.environ.update(NEEDLE3_LIB_PATH=str(library), NEEDLE_TELEMETRY='0', DO_NOT_TRACK='1')
    signal.signal(signal.SIGTERM, terminate)
    # Constrain only this owned worker and its SDK child to the requested CPU budget.
    if hasattr(os, 'sched_getaffinity'):
        cpus=sorted(os.sched_getaffinity(0))[:max(1,int(config.get('cpu_threads',2)))]
        os.sched_setaffinity(0,cpus)
    model=None
    try:
        with contextlib.redirect_stdout(sys.stderr):
            import needle
            model=needle.Needle(weights=str(weights))
            vector=model.embed('')
            initial=config.get('criteria')
            vectors={role:model.embed(initial[role]) for role in ('plan','build','work')} if initial else {}
            criteria_key=json.dumps(initial,sort_keys=True) if initial else None
        runtime={'run':args.run, 'device':'cpu', 'backend':'needle3_c_native',
                 'package_version':importlib.metadata.version('cactus-needle'),
                 'library_sha256':hashlib.file_digest(library.open('rb'),'sha256').hexdigest(),
                 'weights_sha256':hashlib.file_digest(weights.open('rb'),'sha256').hexdigest(),
                 'dimensions':len(vector), 'cpu_affinity':sorted(os.sched_getaffinity(0)) if hasattr(os,'sched_getaffinity') else None}
        emit({'status':'ready','runtime':runtime})
        while True:
            raw=sys.stdin.buffer.readline(args.max_input_bytes+4097)
            if not raw:break
            if len(raw)>args.max_input_bytes+4096 or not raw.endswith(b'\n'):
                raise ValueError('worker input envelope exceeds bound')
            envelope=json.loads(raw);request_id=envelope['id']
            if time.time()>=envelope['deadline']:
                emit({'id':request_id,'status':'expired'});continue
            try:
                request=envelope['request'];criteria=request['criteria']
                key=json.dumps(criteria,sort_keys=True)
                with contextlib.redirect_stdout(sys.stderr):
                    if key!=criteria_key:
                        vectors={role:model.embed(criteria[role]) for role in ('plan','build','work')}
                        criteria_key=key
                    query=model.embed(request['task'])
                result={'status':'ready','provider':'cactus_needle_local','dimensions':len(query),
                        **score_embeddings(query,vectors),'runtime':runtime}
                emit({'id':request_id,'status':'ready','result':result})
            except Exception as exc:
                emit({'id':request_id,'status':'invalid_request','reason':type(exc).__name__})
    finally:
        if model is not None:
            with contextlib.redirect_stdout(sys.stderr):model.close()


if __name__=='__main__':main()
