"""Keep directly invoked and translated review instructions consistent."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]


def test_direct_consumers_do_not_restore_the_old_review_contract():
    paths = [ROOT / 'README.md', ROOT / 'skills/fleet-ladder/ladder.example.yaml',
             *ROOT.glob('plays/*.md'), *ROOT.glob('command-adapters/*.md'),
             *ROOT.glob('skills/*/SKILL.md'), *ROOT.glob('i18n/*/README.md'),
             *ROOT.glob('i18n/*/plays/*.md'), *ROOT.glob('i18n/*/skills/*/SKILL.md')]
    obsolete = (
        "every candidate from the builder's identity is refused",
        'unverified seat is a hold',
        'refuse the builder’s identity',
        'never the model that built',
        'builder and grader still must not resolve to the same model',
        'jurors from different model families',
        'aus einer anderen familie als',
        'gleicher hersteller = gleiche familie',
        'gleicher anbieter = gleiche familie',
        "d'une famille différente de celle du",
        'même éditeur = même famille',
        'même fournisseur = même famille',
        'una familia distinta a la',
        'misma marca = misma familia',
        'mismo proveedor = misma familia',
        'uma família diferente da do',
        'mesmo fornecedor = mesma família',
        'उस परिवार की हर rung',
        'न वही instance, न वही family',
        '与构建者不同家族的模型',
        '同一供应商 = 同一家族',
        '不能是同一个实例，也不能是同一个家族',
    )
    found = []
    for path in paths:
        text = re.sub(r'\s+', ' ', path.read_text().lower())
        found.extend(f'{path.relative_to(ROOT)}: {clause}'
                     for clause in obsolete if clause in text)
    assert not found, 'Old consumer rules remain:\n' + '\n'.join(found)
