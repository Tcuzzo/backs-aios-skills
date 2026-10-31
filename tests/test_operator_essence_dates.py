"""A partial evidence window must not present future observations as history."""

import json
from test_operator_essence import profile, run, write_profile


def test_future_start_with_unknown_end_is_rejected(tmp_path):
    path = tmp_path / "OPERATOR_ESSENCE.md"
    data = profile()
    data["evidence_window"] = {"start": "2027-01-01", "end": None}
    write_profile(path, data)
    before = path.read_bytes()

    process = run(path)

    assert process.returncode == 1
    assert "future" in json.loads(process.stdout)["error"]
    assert path.read_bytes() == before
