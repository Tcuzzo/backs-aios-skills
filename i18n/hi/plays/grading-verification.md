# Play: Grading & Verification

Adversarial grading का play। इसका एक ही विश्वास है: green नतीजा एक दावा है, सबूत
नहीं। grader हमला करता है, और floor ऐसा बना होता है कि उसे game करना नामुमकिन हो।

## कब चलाएँ

- कोई भी बना हुआ बदलाव land होना चाहता है — code, config, docs, किसी agent का
  output।
- कोई suite green होने का दावा करती है और किसी ने उसे पहले fail होते नहीं देखा।
- काम एक model ने बनाया है और आपको उस पर एक ईमानदार verdict चाहिए।

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

1. [red-first](../skills/red-first/SKILL.md) — पक्का करें कि fix के आने से पहले
   suite non-zero exit के साथ fail हुई थी। जो suite कभी red थी ही नहीं, वह कुछ
   साबित नहीं करती।
2. [sniper-testing](../skills/sniper-testing/SKILL.md) — सत्यापित करें builder ने
   pinned aggregate candidate diff के scoped actual repo lint/type/test commands लिए
   और changed seam पर mock theater नहीं किया। Explicit N/A reasons और missing checks
   जाँचें। इस review के लिए candidate identity freeze करें।

3. Independent grade — configured rung matrix से capability और availability के
   अनुसार live reviewer चुनें (task → capability → rung → live probe)। Builder की
   authoring execution को supported provenance में दर्ज और exclude करें। fresh, author-disjoint session किसी भी capable configured route से review कर सकता है। Builder
   conversation या inherited context देखने वाले session की grade निषिद्ध है। Model
   identity provenance है, authority नहीं।

4. [blind-tribunal](../skills/blind-tribunal/SKILL.md) — consequential changes के लिए
   author-redacted envelope पर fresh session में jurors बैठें, inherited conversation
   बिना। Proven findings separate supplemental RED और bounded repair के लिए integration
   owner को लौटाएँ; original RED sealed रहे। Revised frozen candidate पर same remaining
   budget में re-convene करें। Landing से पहले हर required juror pass करे।

5. [clean-code-gauntlet](../skills/clean-code-gauntlet/SKILL.md) — grader खुद
   gauntlet दोबारा चलाता है (coverage-बनाम-complexity, सीमित mutation testing)।
   builder की अपने ही आँकड़ों की रिपोर्ट पर कभी भरोसा न करें।

Review mode का immutable target मानें। Cache बनाने, code mutate करने या services
exercise करने वाले checks केवल permitted isolation में चलाएँ; mutation testing frozen
source कभी न बदले। Missing isolation/runtime support evidence gap है, review में patch
करने की permission नहीं। Required full affected-suite landing evidence रखें और local
checks को real-surface/delivery proof से अलग बताएँ।

## दो-तरफ़ा सबूत (दोनों चाहिए, वरना pass नहीं)

- **Fail-to-pass:** जो tests red थे वे अब green हैं — fix साबित हुआ।
- **Pass-to-pass:** जो कुछ green था वह अब भी green है — कोई regression नहीं।
- जो run सिर्फ़ नए passing tests जोड़ता है, वह दोनों में से कोई शर्त पूरी नहीं
  करता। दोनों को hermetically चलाएँ।

## Fake-green के पहरेदार (इनमें से कोई एक भी दिखा, तो वही सुराग़ है)

- exit-code का escape hatch — ऐसा harness जो कुछ भी हो जाए, साफ़ exit करता है।
- computed नतीजों की जगह hardcoded या रटे हुए outputs।
- delete किए गए, skip किए गए, या कमज़ोर किए गए tests।
- कोई भी edit किया हुआ grader, timer, या scorer। edit हुआ harness जो green हो
  जाए — वही सुराग़ है।
- green suite के नीचे ज़िंदा बचा mutant। mutant इस बात का सबूत है कि assertions
  उस branch तक पहुँचे ही नहीं — परिभाषा से fake green।

## Judge का bias हटाएँ

Judge-mechanics का floor [blind-eval](../skills/blind-eval/SKILL.md) के "De-bias
the judge" section में है — उसे पूरा लागू करें।

## Hard gates — कोई एक भी टूटा तो play fail

- Grader authoring session में है, author का context विरासत में मिला है, या author ने अपना ही काम grade किया है।
- fix से पहले suite को red दिखाया नहीं जा सकता।
- graded run में fail-to-pass या pass-to-pass गायब है।
- ऊपर वाला कोई भी fake-green सुराग़ मौजूद है।
- grader ने checks खुद दोबारा चलाने की जगह builder की अपनी रिपोर्ट पर भरोसा कर लिया।

**Weight:** शुरुआत में free red और sniper जाँचें; heavy खर्च tribunal और grader का खुद gauntlet दोबारा चलाना है — यह land होने की माँग करने वाले हर बदलाव पर वसूल होता है, क्योंकि एक fake green सारी grades की मिली-जुली लागत से ज़्यादा महँगा पड़ता है।
