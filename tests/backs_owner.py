"""Locate the deployed BACKS owner that the native Stop contracts run against.

The Stop adapter persists continuation state through the deployed BACKS run
store (``backend/core/durable_runs.py``). These contracts exercise that real
store, so they need a BACKS deployment. A host without one configured, such as
public CI, skips the whole module with a visible reason; a configured deployment
without the run store fails loudly.
"""
from __future__ import annotations

import os
from pathlib import Path

import pytest


def deployed_owner() -> Path:
    configured = os.environ.get("BACKS_DEPLOY_ROOT", "")
    if not configured:
        pytest.skip("BACKS deployment not configured: set BACKS_DEPLOY_ROOT to run the "
                    "native Stop contracts against its run store", allow_module_level=True)
    root = Path(configured)
    if not (root / "backend" / "core" / "durable_runs.py").is_file():
        # A configured deployment that cannot serve the contracts is a broken host, not an absent one.
        pytest.fail(f"BACKS_DEPLOY_ROOT={configured} has no backend/core/durable_runs.py",
                    pytrace=False)
    return root
