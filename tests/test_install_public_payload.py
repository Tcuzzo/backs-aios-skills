"""The host plugin/runtime copy must exclude provider and private scaffolding."""

from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]


def test_windows_pack_copy_is_public_skills_and_hooks_only() -> None:
    installer = (ROOT / "install.ps1").read_text(encoding="utf-8")
    block = re.search(r"\$PackEntries\s*=\s*@\((.*?)\)", installer, re.S)
    assert block is not None
    names = set(re.findall(r'"([^"]+)"', block.group(1)))
    assert {"skills", "hooks", "plays", "command-adapters"}.issubset(names)
    assert not names.intersection({
        "provider", "claude-skills", "config", "scripts", "docs",
        "install-provider.sh", "bin",
    })
