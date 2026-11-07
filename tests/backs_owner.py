"""Locate the deployed BACKS owner that the native Stop contracts run against.

The Stop adapter persists continuation state through the deployed BACKS run
store (``backend/core/durable_runs.py``). These contracts exercise that real
store, so they need a BACKS deployment. A host without one, such as public CI,
skips the whole module with a visible reason instead of failing at import.
"""
from __future__ import annotations

import os
from pathlib import Path

import pytest


def deployed_owner() -> Path:
    configured = os.environ.get("BACKS_DEPLOY_ROOT", "")
    root = Path(configured) if configured else None
    if root is None or not (root / "backend" / "core" / "durable_runs.py").is_file():
        pytest.skip("BACKS deployment not available: set BACKS_DEPLOY_ROOT to a deploy "
                    "that provides backend/core/durable_runs.py to run the native Stop contracts",
                    allow_module_level=True)
    return root
