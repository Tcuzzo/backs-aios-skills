"""Localized grading plays retain independent-session review without identity rules."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_localized_grading_plays_have_no_retired_model_identity_claims():
    forbidden = {
        'hi': 'builder + grader families differ',
        'de': 'Eigen-Bevorzugung zwischen\n   Ausführungen derselben Familie',
        'es': 'auto-preferencia entre\n   ejecuciones de la misma familia',
        'fr': "auto-préférence mesurable entre exécutions\n   d'une même famille",
        'zh-CN': '同一模型家族内不同执行之间的自\n   偏袒',
    }
    for locale, stale in forbidden.items():
        path = ROOT / 'i18n' / locale / 'plays' / 'grading-verification.md'
        assert stale not in path.read_text(encoding='utf-8'), locale


def test_localized_grading_plays_require_fresh_author_disjoint_review():
    import re
    required = {
        'de': 'frischen, autor-disjunkten Session',
        'es': 'sesión fresca y disjunta del autor',
        'fr': "session vierge et disjointe de l'auteur",
        'hi': 'fresh, author-disjoint session',
        'pt-BR': 'sessão nova e disjunta',
        'zh-CN': '全新且与作者无关的会话',
    }
    forbidden = re.compile(r'famil(?:y|ies|ia|ie|le|íli)|家族|परिवार', re.I)
    for locale, expected in required.items():
        source = (ROOT / 'i18n' / locale / 'plays' / 'grading-verification.md').read_text(encoding='utf-8')
        assert expected in source, locale
        assert not forbidden.search(source), locale


def test_hindi_grade_checks_author_session_not_reviewer_seat():
    source = (ROOT / 'i18n/hi/plays/grading-verification.md').read_text(encoding='utf-8')
    assert 'एक ही seat / context' not in source
    assert 'जिस seat ने build किया' not in source
    assert 'authoring session' in source
    assert 'fresh, author-disjoint session' in source
