# Design Taste

ऐसा UI बनाने का play जो designed दिखे, generated नहीं। generic UI एक WORKFLOW bug
है, model का bug नहीं: taste तय करने को implementation से अलग करें, सबसे पहले exact
design tokens रखें, agent को आँखें दें, और accessibility पर gate लगाएँ।

## कब चलाएँ

कोई भी screen, page, component, dashboard, या ऐसा visual deliverable जिसे कोई
इंसान देखेगा। पहली screen बाद की हर screen का स्तर तय कर देती है — उससे पहले यह
play चलाएँ।

## चेन

1. [intent-compiler](../skills/intent-compiler/SKILL.md) — इंसान के अपने शब्दों से
   यह निकालें कि वे कौन-सी taste माँग रहे हैं, और लिखने से पहले अपनी समझ एक
   पंक्ति में बताएँ।
2. [human-calibration](../skills/human-calibration/SKILL.md) — उस समझ को इंसान के
   record और सचमुच पढ़े गए references में बाँधें, कभी demographic अंदाज़े में नहीं।
3. किसी भी component से पहले, सबसे पहले तीन-स्तरीय design-token file निकालें —
   पूरा token spec और banned-defaults की सूची
   [design-taste](../skills/design-taste/SKILL.md) में है।
4. components को token file के साथ एक सख़्त constraint की तरह बनाएँ। किसी
   component के अंदर कभी कच्चा hex, pixel value, या font family hardcode न करें।
5. screenshot → critic loop चलाएँ, जैसा
   [design-taste](../skills/design-taste/SKILL.md) कहता है; critic model को
   [fleet-ladder](../skills/fleet-ladder/SKILL.md) से live resolve करें।
6. 8-axis taste rubric का score करें, [design-taste](../skills/design-taste/SKILL.md)
   के हिसाब से।
7. WCAG 2.2 accessibility का HARD gate लागू करें, जैसा
   [design-taste](../skills/design-taste/SKILL.md) में लिखा है।
8. [clean-code-gauntlet](../skills/clean-code-gauntlet/SKILL.md) — सिर्फ़ pixels के
   पीछे वाले code पर: token resolvers, theme switches, contrast calculators, और
   state reducers zero surviving mutants के साथ पास हों। contrast check में उलटी
   हुई एक comparison एक सुंदर मगर inaccessible screen ship कर देती है। gauntlet
   कभी taste का score नहीं करता — visual फ़ैसले rubric और accessibility gate के
   ही रहते हैं। tests में असली DOM render करें; mocked render उस चीज़ के बारे में
   कुछ साबित नहीं करता जो इंसान असल में देखता है।

## Hard gates (इस play के अपने — skill के अपने hard rules इनके ऊपर लागू रहते हैं)

- critic builder से एक ALAG model family का हो, और fleet ladder से live resolve
  हो — कभी pinned model id नहीं (एक retire हो चुका pin पूरे critic को चुपचाप मार
  देता है)।

## इनके साथ अच्छा चलता है

- [blind-tribunal](../skills/blind-tribunal/SKILL.md) — पूरे deliverable का grade
- [sniper-testing](../skills/sniper-testing/SKILL.md) — component tests का दायरा तय करने के लिए
