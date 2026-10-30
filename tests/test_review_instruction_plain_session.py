"""Runtime skill instructions state session isolation without old routing labels."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]


def test_installed_skill_sources_use_plain_review_isolation():
    paths = [ROOT / 'skills/fleet-ladder/SKILL.md', *[ROOT / 'skills' / name / 'SKILL.md' for name in ('context-compiler', 'context-engineer', 'context_engineer')]]
    stale = re.compile(r'cross[-_ ]family|family[-_ ]disjoint|same[-_ ]family', re.I)
    for path in paths:
        text = re.sub(r'\s+', ' ', path.read_text())
        assert not stale.search(text), str(path)


def test_public_runtime_instructions_do_not_restate_retired_review_rule():
    roots = [ROOT / 'skills', ROOT / 'i18n', ROOT / 'plays']
    paths = [p for root in roots for p in root.rglob('*') if p.is_file() and p.suffix in ('.md', '.yaml')]
    paths.extend([ROOT / 'NAMING.md', ROOT / 'NOTICE.md'])
    stale = re.compile(r'cross[-_ ]family|family[-_ ]disjoint|same[-_ ]family|different\s+(?:model\s+)?famil(?:y|ies)|disjoint[-_ ]family', re.I)
    localized = re.compile(r'verschiedenen Modellfamilien|distintas familias de modelos|familles de modèles différentes|famílias de modelos diferentes|来自不同模型家族|与构建者不同家族|builder से अलग परिवार|Distinta familia que el constructor|Andere Familie als der Builder|Famille différente du constructeur|Família diferente do construtor|tribunal adversarial ciego entre familias', re.I)
    hits = [str(path.relative_to(ROOT)) for path in paths if stale.search(path.read_text(encoding='utf-8')) or localized.search(path.read_text(encoding='utf-8'))]
    assert not hits, '\n'.join(hits)


def test_localized_tribunals_require_fresh_isolated_review_sessions():
    checks = {
        "de": ("frischen, autor-disjunkten Session", "Autors nie gesehen"),
        "es": ("sesión fresca y disjunta del autor", "nunca vio"),
        "fr": ("session vierge et disjointe de l'auteur", "jamais vu"),
        "hi": ("author-disjoint", "नहीं देखी"),
        "pt-BR": ("sessão nova e disjunta do autor", "nunca viu"),
        "zh-CN": ("全新的、与作者无关", "从未见过作者的对话"),
    }
    for locale, required in checks.items():
        text = (ROOT / "i18n" / locale / "skills/blind-tribunal/SKILL.md").read_text(encoding="utf-8")
        for phrase in required:
            assert phrase in text, f"{locale}: missing {phrase}"


def test_localized_tribunals_do_not_restate_model_comparisons():
    phrases = {
        "de": ("gleicher Familie", "Familien- oder Anbieter-Gate"),
        "es": ("peldaño o familia", "peldaño, familia o proveedor"),
        "fr": ("même famille", "barreau, famille ou fournisseur"),
        "hi": ("या family का reviewer", "family-only identity filter", "model/rung/family/vendor"),
        "pt-BR": ("ou família em uma", "família ou fornecedor"),
        "zh-CN": ("同一家族的评审者", "家族或厂商", "家族过滤身份"),
    }
    for locale, forbidden in phrases.items():
        text = (ROOT / "i18n" / locale / "skills/blind-tribunal/SKILL.md").read_text(encoding="utf-8")
        for phrase in forbidden:
            assert phrase not in text, f"{locale}: obsolete wording {phrase}"


def test_localized_tribunals_disqualify_inherited_author_context():
    requirements = {
        'de': 'die die Konversation oder den Kontext des Builders geerbt hat, werden laut abgelehnt',
        'es': 'heredado la conversación o el contexto del constructor quedan descalificadas',
        'fr': 'session qui a hérité de la conversation ou du contexte du builder, sont disqualifiées',
        'hi': 'जिस session ने builder की बातचीत या context inherit किया, वो हर ladder पर, dispatch से पहले, ज़ोर से disqualify',
        'pt-BR': 'tenha herdado a conversa ou o contexto do builder, são desqualificadas',
        'zh-CN': '任何继承了构建者对话或上下文的会话，在每一架梯子、每次派发之前都被大声 拒绝',
    }
    for locale, requirement in requirements.items():
        text = (ROOT / 'i18n' / locale / 'skills/blind-tribunal/SKILL.md').read_text(encoding='utf-8')
        assert requirement in re.sub(r'\s+', ' ', text), locale


def test_localized_blind_eval_requires_fresh_noninheriting_sessions():
    required = {
        'de': ('frische, autor-disjunkte Prüfsession', 'Konversation oder den Kontext des Autors geerbt'),
        'es': ('sesión de revisión fresca y disjunta del autor', 'heredó la conversación o el contexto del autor'),
        'fr': ('session de revue vierge et disjointe de l’auteur', 'hérité de la conversation ou du contexte de l’auteur'),
        'hi': ('ताज़ी, author-disjoint review session', 'author की बातचीत या context inherit'),
        'pt-BR': ('sessão de revisão nova e disjunta do autor', 'herdou a conversa ou o contexto do autor'),
        'zh-CN': ('全新的、与作者无关的评审会话', '继承作者对话或上下文'),
    }
    # This is the judge-selection section. Model-group comparisons here are
    # unnecessary: selection is by capability and session isolation.
    comparisons = {
        'de': r'familie|(?:gleich|ander|verschieden)\w*\s+(?:modell|sprosse)',
        'es': r'familia|(?:mismo|distinto|diferente)\s+(?:modelo|peldaño)',
        'fr': r'famille|(?:même|autre|différent)\s+(?:modèle|barreau)',
        'hi': r'family|परिवार|same\s+(?:model|rung)|अलग\s+(?:model|rung)',
        'pt-BR': r'família|(?:mesmo|diferente)\s+(?:modelo|degrau)',
        'zh-CN': r'家族|同一模型|不同模型|同一梯级|不同梯级',
    }
    for locale, phrases in required.items():
        text = (ROOT / 'i18n' / locale / 'skills/blind-eval/SKILL.md').read_text(encoding='utf-8')
        section = text[text.index('4. **'):text.index('\n5. **')]
        normalized = re.sub(r'\s+', ' ', section)
        for phrase in phrases:
            assert phrase in normalized, locale
        assert not re.search(comparisons[locale], normalized, re.I), locale


def test_review_workflows_use_session_requirements_without_model_comparisons():
    paths = [ROOT / 'skills' / name / 'SKILL.md' for name in (
        'fix-shit', 'invariant-floor', 'model-fusion', 'absorb', 'red-first',
        'repair-loop', 'design-taste', 'clean-code-gauntlet',
    )]
    paths += [ROOT / 'plays' / name for name in ('agent-builds.md', 'web-app-builds.md')]
    comparison = re.compile(r'(?:same\s+)?model,\s*rung,\s*or\s*family|model\s+family\s+is\s+not', re.I)
    hits = [str(path.relative_to(ROOT)) for path in paths if comparison.search(re.sub(r'\s+', ' ', path.read_text(encoding='utf-8')))]
    assert not hits, '\n'.join(hits)


def test_core_review_workflows_use_execution_provenance_only():
    paths = [ROOT / 'skills/blind-tribunal/SKILL.md', ROOT / 'skills/fleet-ladder/SKILL.md', ROOT / 'plays/elite-build.md', ROOT / 'plays/grading-verification.md']
    comparisons = re.compile(r'\bfamil(?:y|ies)\b|builder_family|author-family', re.I)
    hits = [str(path.relative_to(ROOT)) for path in paths if comparisons.search(path.read_text(encoding='utf-8'))]
    assert not hits, '\n'.join(hits)


def test_hindi_review_instructions_do_not_compare_model_groups():
    names = ('absorb', 'blind-tribunal', 'clean-code-gauntlet', 'design-taste', 'fleet-ladder', 'invariant-floor', 'model-fusion', 'red-first', 'repair-loop')
    stale = re.compile(r'(?<!font )\bfamily\b|builder_family', re.I)
    hits = []
    for name in names:
        path = ROOT / 'i18n/hi/skills' / name / 'SKILL.md'
        if stale.search(path.read_text(encoding='utf-8')):
            hits.append(name)
    assert not hits, ', '.join(hits)


def test_chinese_review_instructions_do_not_compare_model_groups():
    names = ('absorb', 'blind-tribunal', 'clean-code-gauntlet', 'design-taste', 'fleet-ladder', 'invariant-floor', 'leap-protocol', 'model-fusion', 'red-first', 'repair-loop')
    hits = []
    for name in names:
        path = ROOT / 'i18n/zh-CN/skills' / name / 'SKILL.md'
        text = path.read_text(encoding='utf-8')
        if '家族' in text or 'builder_family' in text:
            hits.append(name)
    assert not hits, ', '.join(hits)


def test_portuguese_review_instructions_do_not_compare_model_groups():
    names = ('absorb', 'blind-tribunal', 'clean-code-gauntlet', 'design-taste', 'fleet-ladder', 'invariant-floor', 'leap-protocol', 'model-fusion', 'red-first', 'repair-loop')
    hits = []
    for name in names:
        path = ROOT / 'i18n/pt-BR/skills' / name / 'SKILL.md'
        for line in path.read_text(encoding='utf-8').splitlines():
            if ('família' in line.lower() and 'família de fonte' not in line.lower()) or 'builder_family' in line:
                hits.append(name)
    assert not hits, ', '.join(hits)


def test_german_review_instructions_do_not_compare_model_groups():
    names = ('absorb', 'blind-tribunal', 'clean-code-gauntlet', 'design-taste', 'fleet-ladder', 'invariant-floor', 'leap-protocol', 'model-fusion', 'red-first', 'repair-loop')
    hits = []
    for name in names:
        path = ROOT / 'i18n/de/skills' / name / 'SKILL.md'
        for line in path.read_text(encoding='utf-8').splitlines():
            if (re.search(r'familie|familien', line, re.I) and 'font-family' not in line.lower()) or 'builder_family' in line:
                hits.append(name)
    assert not hits, ', '.join(hits)


def test_spanish_review_instructions_do_not_compare_model_groups():
    names = ('absorb', 'blind-tribunal', 'clean-code-gauntlet', 'design-taste', 'fleet-ladder', 'invariant-floor', 'leap-protocol', 'model-fusion', 'red-first', 'repair-loop')
    hits = []
    for name in names:
        path = ROOT / 'i18n/es/skills' / name / 'SKILL.md'
        for line in path.read_text(encoding='utf-8').splitlines():
            if ('familia' in line.lower() and 'familia tipográfica' not in line.lower()) or 'builder_family' in line:
                hits.append(name)
    assert not hits, ', '.join(hits)


def test_french_review_instructions_do_not_compare_model_groups():
    names = ('absorb', 'blind-tribunal', 'clean-code-gauntlet', 'design-taste', 'fleet-ladder', 'invariant-floor', 'leap-protocol', 'model-fusion', 'red-first', 'repair-loop')
    hits = []
    for name in names:
        path = ROOT / 'i18n/fr/skills' / name / 'SKILL.md'
        for line in path.read_text(encoding='utf-8').splitlines():
            if ('famille' in line.lower() and 'famille de polices' not in line.lower()) or 'builder_family' in line:
                hits.append(name)
    assert not hits, ', '.join(hits)


def test_localized_review_plays_do_not_restate_identity_comparisons():
    stale = {
        'de': ('die Modellfamilie beweist keine Sitzungsisolierung', 'dieselbe Modellfamilie ist zulässig', 'gleicher Familie'),
        'es': ('la familia del modelo no demuestra aislamiento', 'se permite la misma familia de modelos', 'mismo modelo, peldaño o familia'),
        'fr': ('la famille du modèle ne prouve pas', 'la même famille de modèles est permise', 'correcteur de même modèle, même barreau ou même famille'),
        'hi': ('model family session isolation', 'same model family की अनुमति', 'model family होना'),
        'pt-BR': ('família de modelo não comprova', 'a mesma família de modelos é permitida', 'o mesmo modelo, degrau ou família'),
        'zh-CN': ('模型家族不能证明', '同一模型家族也可胜任', '同一模型、同一梯级或同一家族'),
    }
    hits = []
    for locale, phrases in stale.items():
        for rel, phrase in zip(('skills/fix-shit/SKILL.md', 'plays/design-taste.md', 'plays/grading-verification.md'), phrases):
            path = ROOT / 'i18n' / locale / rel
            if phrase in re.sub(r'\s+', ' ', path.read_text(encoding='utf-8')):
                hits.append(f'{locale}/{rel}')
    assert not hits, '\n'.join(hits)


def test_ladder_examples_do_not_restate_review_identity_comparisons():
    paths = [ROOT / 'skills/fleet-ladder/ladder.example.yaml'] + list((ROOT / 'i18n').glob('*/skills/fleet-ladder/ladder.example.yaml'))
    stale = re.compile(r'family|familia', re.I)
    hits = [str(path.relative_to(ROOT)) for path in paths if stale.search(path.read_text(encoding='utf-8'))]
    assert not hits, '\n'.join(hits)


def test_context_aliases_preserve_author_session_separation():
    paths = [ROOT / 'skills' / name / 'SKILL.md' for name in ('context-compiler', 'context-engineer', 'context_engineer')]
    paths += [ROOT / 'i18n' / locale / 'skills' / name / 'SKILL.md'
              for locale in ('de', 'es', 'fr', 'hi', 'pt-BR', 'zh-CN')
              for name in ('context-compiler', 'context-engineer', 'context_engineer')]
    hits = [str(path.relative_to(ROOT)) for path in paths if 'identity-based landing defaults' in path.read_text(encoding='utf-8')]
    assert not hits, '\n'.join(hits)
