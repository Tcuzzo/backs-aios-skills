"""Deadline evaluation accepts an explicit instant for exact boundary proof."""
from datetime import datetime, timedelta, timezone

from test_codex_stop_direct import helper


def test_deadline_is_exhausted_at_the_exact_instant(helper):
    deadline = datetime(2030, 1, 1, tzinfo=timezone.utc)
    assert helper._expired(deadline.isoformat(), now=deadline)
    assert not helper._expired(deadline.isoformat(), now=deadline - timedelta(microseconds=1))
    assert helper._expired(deadline.isoformat(), now=deadline + timedelta(microseconds=1))
