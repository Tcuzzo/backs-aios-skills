"""Active instructions must not reintroduce identity-based reviewer bans."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]


def test_active_review_instructions_do_not_require_family_or_cloud_identity():
    paths = [*ROOT.glob("plays/*.md"), *ROOT.glob("command-adapters/*.md"),
             *ROOT.glob("skills/*/SKILL.md"), *ROOT.glob("i18n/*/skills/*/SKILL.md")]
    forbidden = (
        r"(?:model|reviewers?|jurors?|graders?)\s+from\s+(?:a\s+)?different\s+(?:model\s+)?famil",
        r"(?:blind\s+)?cross-family\s+(?:graders?|jurors?|reviewers?|review|grade|verdict|independence)",
        r"(?:must|never|requires?|refused|excludes?).{0,60}(?:same|different|builder.s)\s+(?:model\s+)?family",
        r"(?:fused\s+with\s+a\s+cheap\s+cloud\s+verifier|verifier\s+never\s+comes\s+from\s+the\s+primary.s\s+family)",
        r"4090\s+NEVER\s+grades",
    )
    failures = []
    for path in paths:
        # Historical attribution is not an active instruction.
        body = path.read_text().split("> Scaffold credit:", 1)[0]
        flat = re.sub(r"\s+", " ", body)
        for pattern in forbidden:
            match = re.search(pattern, flat, re.I)
            if match:
                failures.append(f"{path.relative_to(ROOT)}: {match.group()}")
    assert not failures, "Active review identity rules remain:\n" + "\n".join(failures)
