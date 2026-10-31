---
name: "optimus"
description: "Agent session, job या autonomous loop शुरू या resume करते समय BACKS harness और relevant task skills की जरूरत हो तो उपयोग करें।"
license: "MIT"
---

# Harness Boot
**Effort:** light — हर session में एक boot pass जो floor और इस काम की skills load करता है, साथ में एक deterministic hook जिसे चलाने की कोई लागत नहीं। हटाता है: बिना ज़मीन पकड़े edits — नियम पढ़ने से पहले किए गए बदलाव, और नियम पढ़ते ही आने वाला उनका redo।

एक नियम: **harness load होने तक न कोई code, न कोई job।** Harness = pack का
invariant floor + वे skills जो इस job को cover करती हैं। हर session, हर
runtime, हर बार। क्यों: जो नियम agent को याद रखना पड़े, वह ठीक तब fail होता
है जब agent सबसे ज़्यादा busy हो — इसलिए नियम load करना पहला काम है, और एक
hook उसे सलाह की जगह structural बना देता है।

## कब चलाएँ

Session या नए job की शुरुआत पर; context reset या handoff के बाद revalidate करें।
Inner retry current grounding और वही task packet reuse करता है। Missing या changed
bodies reload करें; हर iteration में पूरा lifecycle reboot न करें।

## Boot sequence

1. **Invariant floor load करें।** कुछ छूने से पहले
   [invariant-floor](../invariant-floor/SKILL.md) पढ़ें; पूरा session इसी floor पर है।
2. **[Build Flow](../backs-build-flow/SKILL.md) अपनाएँ।** Task mode, readiness to act,
   skill selection, scoped lint/tests सहित bounded RED/GREEN, gauntlet evidence और
   delivery उसका काम है। Verified packet reuse करें; next concrete action के लिए केवल
   missing facts जुटाएँ। Specialists एक ही owner को लौटते हैं।
3. **Human context अपनाएँ** ([human-calibration](../human-calibration/SKILL.md)) जहाँ
   relevant हो। [operator-essence](../operator-essence/SKILL.md) evidence आधारित awareness
   file और missing-file insight pass का owner है; दूसरी profile cycle न चलाएँ।
4. **Session load करें।** Session hook actual Optimus, Yoke और Build Flow bodies, और
   उपलब्ध हो तो proven native harness देता है। Compaction earned grounding हटाए बिना
   उन bodies को reload करता है। Mutating tool पर missing marker loading trigger करता
   है, tool refusal कभी नहीं। Context hook बिना hosts उपयोग कर सकते हैं:
   ```bash
   node "$HOME/.local/share/backs-aios/current/hooks/aios_gate.js" --load backs-aios:optimus
   ```
   Codex shell में active `CODEX_SESSION_ID` अंतिम argument दें। Matching
   `aios_gate.py` loader से Python भी उपलब्ध है। Unknown skills nonzero लौटाती हैं;
   receipt गढ़ी नहीं जाती।
5. **अगली action की जरूरी skills अपनाएँ।** हर एक का purpose, output और exit बताएँ।
   नाम लिया लेकिन invoke नहीं किया तो skill हुई नहीं। Current context में उपलब्ध
   actual bodies reuse करें; याद किया summary या file hash उनका विकल्प नहीं।
6. तभी code लिखें, mutating commands चलाएँ या कुछ बदलें।

## Automatic grounding

Existing hook foundation files पढ़कर उनकी bodies host context में देता है। Delivery
के बाद ही source hashes record करता है। Context-loading receipts और actual Skill-event
 evidence अलग हैं; pointer load या file hash करना उस skill का invocation नहीं।

- Session start और compaction tools छीने बिना floor reload करते हैं।
- Missing session marker अगले matched tool पर automatic loading करता है।
- Missing/unreadable bodies visible diagnostic देती हैं, false receipt नहीं; operator
  और agents के tools उपलब्ध रहते हैं।
- `--rearm <session_id>` एक और load माँगता है; session lock कभी नहीं करता।
- `AIOS_GATE=off` operator का existing reversible kill switch है।
- Hooks local और deterministic हैं; model call या network dependency नहीं जुड़ती।

## Hard rules (क्या इस skill को fail करता है)

- Harness load होने से पहले कोई mutation।
- Report में ऐसी skill का नाम जो session में invoke नहीं हुई।
- BACKS harness की जगह session memory, LLM priors या “मुझे याद है” से grounding।
  BACKS model/context agnostic है और मजबूत memory lanes रखता है; ज्ञान harness के
  memory files, playbooks, ledgers और ladder YAML में है, model के दिमाग में नहीं
  (operator ruling 2026-09-26)।
- ऐसा hook जो कोई tool refuse करे, earned grounding हटाए या बिना हुए loading का दावा करे।
- दूसरा gate या human पर नई friction; kill switch उन्हीं का है।

## इनके साथ अच्छा चलता है

- [invariant-floor](../invariant-floor/SKILL.md) — वह floor जो boot सबसे पहले load करता है।
- [human-calibration](../human-calibration/SKILL.md) — boot का profile वाला step।
- [repair-loop](../repair-loop/SKILL.md) — boot के बाद fix job जो चलाता है।
- [bounded-loops](../bounded-loops/SKILL.md) — boot से शुरू हर loop के budgets।
- [wayfinder](../wayfinder/SKILL.md) — जब boot दिखाए कि रास्ता पता नहीं।


## Fleet ladder rung policy — संक्षिप्त pointer

Model dispatch या frontier design/reason lift से पहले
[fleet-ladder](../fleet-ladder/SKILL.md) invoke करें। वह `config/fleet_ladder.yaml`
और `config/gpu_nodes.yaml` (deploy paths) पढ़वाता है, live builder seat मानता है और rung
में frontier / `research_seams` होने पर realtime research seams (web + GitHub + Reddit
+ papers) अनिवार्य करता है। Model IDs hardcode न करें; Patch YAML का owner है।
संदर्भ: `observe/SECURITY_OPERATOR_BUILDER_SEAT_ORDER_20260926.md`।

जहाँ supported हो medium-or-higher reasoning baseline, heavy lifts से पहले research,
और पूरा context रखने के लिए [fleet-ladder](../fleet-ladder/SKILL.md) मानें।
