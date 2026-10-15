"""Portable owned Needle CPU supervisor; no SDK imports in the host process."""
from pathlib import Path
try:
    from .typed_decision_runtime import TypedDecisionRuntime
except ImportError:
    from typed_decision_runtime import TypedDecisionRuntime


class NeedleProcessRuntime(TypedDecisionRuntime):
    def __init__(self, config):
        super().__init__(config, worker=Path(__file__).with_name('needle_embedding_worker.py'))
