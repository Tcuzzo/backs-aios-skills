---
name: "repair-loop"
description: "Bug fix, reported issue बंद करने या seam को end to end uplift करने में current task के भीतर bounded reproduction, repair और verification loop चलाने के लिए उपयोग करें।"
license: "MIT"
---

# Repair Loop
**Effort:** light — loop खुद अनुशासन है, साथ में एक स्वतंत्र grading pass; यह जो भारी कदम जोड़ता है (gauntlet, tribunal) वे अपने stamps खुद रखते हैं और सिर्फ़ ship होने वाले बदलावों पर चलते हैं। हटाता है: green-मगर-टूटी landings, और दोबारा खुले bug का वह rework जो वे महँगा पड़वाती हैं।

किसी भी fix, bug close या uplift का default loop। यह एक behavior है, approval
की मशीनरी नहीं: इंसान पर zero gates और zero friction। यह agent को ऐसी
discipline से बाँधता है जो "green पर टूटा हुआ" ship करना structurally मुश्किल
बना देती है।

## Current task में जुड़ें

Task packet, operator essence और एक integration owner के लिए
[BACKS Build Flow](../backs-build-flow/SKILL.md) लें। Caller के applicable rules,
context, loaded skill bodies और evidence reuse करें; केवल changed facts refresh करें।
Direct invocation missing context एक बार बनाता है। Invariant floor और required
understanding gates उपलब्ध न हों तो load करें; unresolved route पर ही wayfinder लें।
Repair finding के लिए outer build play फिर शुरू न करें।

[bounded-loops](../bounded-loops/SKILL.md) shared deadline और remaining attempt/round
allowances का owner है। `mission_id`, `task_mode`, pinned `base_sha` और current
`candidate_sha` को reproduction, edits, tools, models, reviews और handoffs में बचाएँ।
Nested call budget reset नहीं करता। Review/diagnosis बिना edits/promotion evidence
लौटाते हैं; build actions के लिए वही task scope चाहिए।

## Loop

1. **Affected path ground करें।** Rules, project के current source, caller contracts
   और existing checks देखें। Whole-repo audit दोहराने की जगह current relevant evidence
   reuse करें।
2. **Live सच पर reproduce करो।** Failure ख़ुद देखो, उसी असली रास्ते पर जो
   इंसान इस्तेमाल करता है — कोई proxy probe नहीं, bug report की बात पर भरोसा
   नहीं। Reproduction नहीं, तो fix नहीं।
3. **Red contract test।** Defect पकड़ने वाला failing test लिखो, और fix से
   पहले commit करो। साबित करो कि वह सच में red है। Fix उसे green करता है;
   fix test को कभी edit नहीं करता। देखो [red-first](../red-first/SKILL.md)।
4. **Seam पर CLASS ठीक करो** — हर symptom पर एक point patch नहीं। पूरा
   formula [seam-engineering](../seam-engineering/SKILL.md) में है।
5. **Scoped checks चलाएँ।** [sniper-testing](../sniper-testing/SKILL.md) से pinned
   `base_sha` से `candidate_sha` aggregate diff और owned pending paths का scope लें।
   Repo की actual lint/type-check/test commands चलाएँ। Command, result और revision
   लिखें। Inapplicable check reason सहित **N/A** है; missing required tool gap है।
   Arbitrary tools install या pass न गढ़ें। Sealed test byte-identical रहता है।
6. **Inline measure करें।** Candidate quality और bounded mutation evidence के लिए
   [clean-code-gauntlet](../clean-code-gauntlet/SKILL.md) चलाएँ। Surviving mutant जाँचें;
   test gap मिले तो original RED बचाकर separate supplemental file जोड़ें। Owning seam
   ठीक करें और same remaining budget में affected checks rerun करें; GREEN के लिए
   gate कमजोर न करें।
7. **Independent grade।** Configured rung matrix से capability और availability के
   अनुसार live चुना non-author grader fresh author-disjoint session में pass करे।
   Authoring execution provenance में दर्ज और disqualified हो; builder का context
   inherit करने वाला reviewer भी eligible नहीं। Builder अपना काम कभी grade नहीं करता।
   देखें [blind-tribunal](../blind-tribunal/SKILL.md)।
8. **साथ चल रहा काम देखो।** Shared state बदलने से पहले verify करो कि किसी
   दूसरे session का in-flight काम बचा हुआ है (किसी branch या commit पर)। जो
   काम तुम्हारा नहीं, उसे कभी commit या साफ़ मत करो।
9. **Scope में verify और land करें।** Landing पर touched modules की suites का full
   pass और required project checks करें, फिर authorized delivery procedure अपनाएँ।
   Human के actual surface (उनकी UI या command) पर behavior जाँचें और exact candidate/
   installed revision लिखें। Local tests और upstream static evidence live delivery
   सिद्ध नहीं करते। Seam पर हर surfaced finding बंद करें या evidence सहित explicit
   “not a bug” verdict दें। “बड़ा वाला ठीक, बाकी बाद में” land नहीं होता।

## Mission budget में iterate करें

Failed check अगली bounded hypothesis देता है। Retry या configured capable route केवल
remaining allowance में लें; model बदलना fresh mission नहीं। Bounded-loops के stagnation
और exhaustion rules मानें। Limit पर current candidate, sealed tests, failure evidence,
unmet gates और exact next action के साथ **STILL-BUILDING** checkpoint करें। Useful
 authorized work exhausted allowance खर्च किए बिना करें। Open finding landing रोकती
है; progress मिटाती या invented **PROVEN** नहीं बनती।

## Hard rules — इनमें से कोई एक भी skill fail कर देता है

- Live सच पर reproduction के बिना fix ship हुआ।
- Test fix के बाद लिखा गया, या fix ने उसे edit किया।
- Symptom पर patch लगा और class seam पर खुली रह गई।
- इंसान का अपना रास्ता टूटा हुआ है और proxy पर capability green बताई गई।
- Builder ने अपना ही बदलाव grade किया।
- कोई उठी हुई finding landing पर चुपचाप टाल दी गई।
- Loop reset हुआ, चुपचाप छोड़ा गया, या unmet gate के साथ green बताया गया।

## Report

दो शब्द — **PROVEN** या **STILL-BUILDING** — साथ में सादी भाषा में intent, और
इंसान के सामने खड़ा अकेला फ़ैसला, अगर कोई हो। इंसान तक सवाल सिर्फ़ पसंद,
vision या destructive risk के लिए जाते हैं; देखो
[decision-bar](../decision-bar/SKILL.md)।

## इनके साथ अच्छा चलता है

- [incident-closure](../incident-closure/SKILL.md) — इंसान टूट-फूट report करे, तो यह loop पूरे close के अंदर चलता है।
- [red-first](../red-first/SKILL.md) · [seam-engineering](../seam-engineering/SKILL.md) · [sniper-testing](../sniper-testing/SKILL.md)
- [blind-tribunal](../blind-tribunal/SKILL.md) · [clean-code-gauntlet](../clean-code-gauntlet/SKILL.md)
