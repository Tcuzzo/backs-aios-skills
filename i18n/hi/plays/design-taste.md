# Design Taste

ऐसा UI बनाने का play जो designed दिखे, generated नहीं। generic UI एक WORKFLOW bug
है, model का bug नहीं: taste तय करने को implementation से अलग करें, सबसे पहले exact
design tokens रखें, agent को आँखें दें, और accessibility पर gate लगाएँ।

## कब चलाएँ

कोई भी screen, page, component, dashboard, या ऐसा visual deliverable जिसे कोई
इंसान देखेगा। पहली screen बाद की हर screen का स्तर तय कर देती है — उससे पहले यह
play चलाएँ।

## साझा task और limits

यह play current [BACKS Build Flow](../skills/backs-build-flow/SKILL.md) task packet
के भीतर चलाएँ। एक integration owner, requested `task_mode`, pinned `base_sha`, current
`candidate_sha`, operator essence और current evidence रखें। Applicable loaded skill
bodies reuse करें; यह play अपने domain gates जोड़ता है, task फिर शुरू नहीं करता।

[bounded-loops](../skills/bounded-loops/SKILL.md) original deadline और remaining
allowances को retries, workers, models, reviews और handoffs में संभालता है। Nested play
के लिए उन्हें reset न करें। Exhaustion पर candidate, evidence, unmet gates और next action
सहित **STILL-BUILDING** checkpoint करें। Useful authorized work remaining allowance में
ही करें; missing gate कभी pass नहीं बनता।

## चेन

1. Build Flow के established intent और operator essence से तय करें कि human के
   शब्द किस taste की माँग करते हैं। लिखने से पहले समझ एक बार बताएँ।

2. [human-calibration](../skills/human-calibration/SKILL.md) — उस समझ को इंसान के
   record और सचमुच पढ़े गए references में बाँधें, कभी demographic अंदाज़े में नहीं।
3. किसी भी component से पहले, सबसे पहले तीन-स्तरीय design-token file निकालें —
   पूरा token spec और banned-defaults की सूची
   [design-taste](../skills/design-taste/SKILL.md) में है।
4. components को token file के साथ एक सख़्त constraint की तरह बनाएँ। किसी
   component के अंदर कभी कच्चा hex, pixel value, या font family hardcode न करें।
5. [design-taste](../skills/design-taste/SKILL.md) का screenshot → critic loop चलाएँ;
   [fleet-ladder](../skills/fleet-ladder/SKILL.md) से critic live resolve करें। हर critique
   और re-render same remaining budget खर्च करता है; findings current owner को लौटाएँ।

6. 8-axis taste rubric का score करें, [design-taste](../skills/design-taste/SKILL.md)
   के हिसाब से।
7. WCAG 2.2 accessibility का HARD gate लागू करें, जैसा
   [design-taste](../skills/design-taste/SKILL.md) में लिखा है।
8. [clean-code-gauntlet](../skills/clean-code-gauntlet/SKILL.md) — pixels के पीछे code
   पर: token resolvers, theme switches, contrast calculators और state reducers zero
   surviving mutants के साथ pass हों। Contrast check में flipped comparison सुंदर
   लेकिन inaccessible screen ship करती है। Gauntlet taste score नहीं करता; rubric
   और accessibility gate visual judges हैं। Gauntlet से पहले
   [sniper-testing](../skills/sniper-testing/SKILL.md) से pinned aggregate candidate
   diff के real repo lint/type/test commands चलाएँ। N/A और missing checks ईमानदारी से
   बताएँ। Tests real DOM render करें; mocked render user की view सिद्ध नहीं करता।
   Sealed RED बचाएँ, नए gaps के लिए separate supplemental tests जोड़ें, required
   independent review, full affected-suite landing check और real rendered proof रखें।

## Hard gates (इस play के अपने — skill के अपने hard rules इनके ऊपर लागू रहते हैं)

- critic एक fresh, author-disjoint session में हो और fleet ladder से live resolve
  हो; कभी pinned model id नहीं (एक retire हो चुका pin पूरे critic को चुपचाप मार
  देता है)।

## इनके साथ अच्छा चलता है

- [blind-tribunal](../skills/blind-tribunal/SKILL.md) — पूरे deliverable का grade
- [sniper-testing](../skills/sniper-testing/SKILL.md) — component tests का दायरा तय करने के लिए

**Weight:** पूरे loop में light — calibration और screenshot-critic pass, दोनों की क़ीमत एक-एक अतिरिक्त run है; heavy कदम pixels के पीछे के code पर gauntlet है — यह हर उस screen पर वसूल होता है जिसे कोई इंसान सचमुच देखेगा।
