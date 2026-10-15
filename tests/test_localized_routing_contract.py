"""Regression checks for concrete identity restrictions missed in locale copies.

These checks cover known clauses, not semantic completeness; independent review
still evaluates the whole instruction contract in each language.
"""
from pathlib import Path
import re

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]
LOCALES = ('de', 'es', 'fr', 'hi', 'pt-BR', 'zh-CN')
FAMILY_REQUIREMENTS = {
    'de': 'ein modell aus einer anderen familie',
    'es': 'un modelo de otra familia',
    'fr': "un modèle d'une autre famille",
    'hi': 'किसी दूसरी family का model',
    'pt-BR': 'um modelo de outra família',
    'zh-CN': '不同家族的模型',
}


@pytest.mark.parametrize('locale', LOCALES)
def test_localized_blind_eval_does_not_require_another_family(locale):
    path = ROOT / 'i18n' / locale / 'skills/blind-eval/SKILL.md'
    text = re.sub(r'\s+', ' ', path.read_text().lower())
    assert FAMILY_REQUIREMENTS[locale] not in text, str(path.relative_to(ROOT))


@pytest.mark.parametrize('locale', ('en', *LOCALES))
def test_copied_ladder_example_has_no_identity_exclusion(locale):
    prefix = ROOT if locale == 'en' else ROOT / 'i18n' / locale
    path = prefix / 'skills/fleet-ladder/ladder.example.yaml'
    body = path.read_text()
    config = yaml.safe_load(body)
    assert isinstance(config, dict)
    assert all(isinstance(config[role], list) and config[role]
               for role in ('builder', 'grader', 'worker'))
    text = re.sub(r'\s+', ' ', body.lower())
    for obsolete in (
        'never the model that built',
        'a different family from the builder',
        'must not resolve to the same model',
        'never resolve to the same model',
        'ending in a local survival',
    ):
        assert obsolete not in text, f'{path.relative_to(ROOT)}: {obsolete}'
