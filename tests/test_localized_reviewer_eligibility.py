from pathlib import Path


def test_capable_reviewers_remain_eligible_in_all_ladder_translations():
    root = Path(__file__).resolve().parents[1] / 'i18n'
    eligibility = {
        'de': ('geeignete', 'Modell', 'Anbieter'),
        'es': ('cualquier revisor capaz', 'modelo', 'proveedor'),
        'fr': ('tout évaluateur compétent', 'modèle', 'fournisseur'),
        'hi': ('कोई भी सक्षम reviewer', 'model', 'provider'),
        'pt-BR': ('qualquer revisor capaz', 'modelo', 'fornecedor'),
        'zh-CN': ('任何具备相应能力的评审者', '模型', '提供商'),
    }
    for locale, words in eligibility.items():
        text = (root / locale / 'skills/fleet-ladder/SKILL.md').read_text().casefold()
        assert any(all(word.casefold() in line for word in words)
                   for line in text.splitlines()), locale
