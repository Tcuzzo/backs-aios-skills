---
name: "repair-loop"
description: "तब लगाओ जब कोई bug fix करना हो, reported issue बंद करना हो, या किसी seam को end to end uplift करना हो। पूरा repair loop चलाता है — floor में grounding, live सच पर reproduce, red contract test, seam पर class का fix, असली रास्ते पर verify, independent grade, land — और तब तक iterate करता है जब तक सब सच न हो जाए। Trigger words: repair loop, dev mode, fix this, uplift, close the seam, dev build, इसे ठीक करो, bug बंद करो, seam बंद करो, पूरा loop चलाओ."
license: "MIT"
---

# Repair Loop
**Effort:** light — loop खुद अनुशासन है, साथ में एक स्वतंत्र grading pass; यह जो भारी कदम जोड़ता है (gauntlet, tribunal) वे अपने stamps खुद रखते हैं और सिर्फ़ ship होने वाले बदलावों पर चलते हैं। हटाता है: green-मगर-टूटी landings, और दोबारा खुले bug का वह rework जो वे महँगा पड़वाती हैं।

किसी भी fix, bug close या uplift का default loop। यह एक behavior है, approval
की मशीनरी नहीं: इंसान पर zero gates और zero friction। यह agent को ऐसी
discipline से बाँधता है जो "green पर टूटा हुआ" ship करना structurally मुश्किल
बना देती है।

## पहले load करो — किसी design या edit से पहले

1. [invariant-floor](../invariant-floor/SKILL.md) — काम से पहले अपनी rulebook पढ़ो।
2. [human-calibration](../human-calibration/SKILL.md) — इंसान का profile लगाओ; उससे दोबारा पूछताछ कभी नहीं।
3. [understanding-gates](../understanding-gates/SKILL.md) — diagnostic planner: Design → Plan → Build → Test → Ship।
4. [wayfinder](../wayfinder/SKILL.md) — रास्ता न सूझे तो chart करो; सवाल इंसान पर कभी मत टिकाओ।
5. माँग गद्य या metaphor बनकर आई हो, तो पहले [intent-compiler](../intent-compiler/SKILL.md) चलाओ और निकाले हुए directive पर loop करो।

## Loop

1. **Floor में ground हो।** Code छूने से पहले नियम और project का अपना सच
   (docs, source, tracker) load करो। नियमों की याद से किया काम गिनती में
   नहीं आता।
2. **Live सच पर reproduce करो।** Failure ख़ुद देखो, उसी असली रास्ते पर जो
   इंसान इस्तेमाल करता है — कोई proxy probe नहीं, bug report की बात पर भरोसा
   नहीं। Reproduction नहीं, तो fix नहीं।
3. **Red contract test।** Defect पकड़ने वाला failing test लिखो, और fix से
   पहले commit करो। साबित करो कि वह सच में red है। Fix उसे green करता है;
   fix test को कभी edit नहीं करता। देखो [red-first](../red-first/SKILL.md)।
4. **Seam पर CLASS ठीक करो** — हर symptom पर एक point patch नहीं। पूरा
   formula [seam-engineering](../seam-engineering/SKILL.md) में है।
5. **असली रास्ते पर verify करो।** Trust but verify। Capability इंसान की अपनी
   सतह पर साबित होती है — वह UI जिसमें वे type करते हैं, वह command जो वे
   चलाते हैं — mocked seam पर green test से कभी नहीं। हर दावे को ("दूसरी
   branch ने land कर दिया", "वह service down है") उस पर चलने से पहले live सच
   से मिलाओ।
6. **Fix को नापो।** Loop के बीच सिर्फ़ वे tests चलाओ जो छुए हुए seam को
   cover करते हैं — देखो [sniper-testing](../sniper-testing/SKILL.md)। फिर
   बदले हुए code पर [clean-code-gauntlet](../clean-code-gauntlet/SKILL.md)
   चलाओ: scoped tests, complexity-बनाम-coverage score, bounded mutation
   testing। तुम्हारे fix से बच निकला mutant मतलब test उस branch तक पहुँचा ही
   नहीं जो तुमने बदली — fake green; iterate करते रहो।
7. **Independent grade।** ऐसा grader जिसने बदलाव नहीं लिखा — बेहतर हो तो
   builder से अलग family का model — उसे pass करे। Builder अपना काम कभी grade
   नहीं करता। देखो [blind-tribunal](../blind-tribunal/SKILL.md)।
8. **साथ चल रहा काम देखो।** Shared state बदलने से पहले verify करो कि किसी
   दूसरे session का in-flight काम बचा हुआ है (किसी branch या commit पर)। जो
   काम तुम्हारा नहीं, उसे कभी commit या साफ़ मत करो।
9. **Land करो।** Landing पर छुए modules की suites का एक full pass, फिर
   commit। इस seam पर loop ने जो भी finding उठाई, हर एक बंद करो — या हर
   finding पर सबूत के साथ खुला "not a bug" verdict दर्ज करो। "बड़ा वाला ठीक
   किया, बाक़ी बाद में" कभी land नहीं होता।

## सच होने तक iterate करो

जो नियम अभी पूरा नहीं हुआ, वह loop रोकता नहीं — उसे चलाता है। Model या tier
escalate करो, blocker हटाओ, retry करो — जब तक ऊपर का हर step सच न हो और
बदलाव land न हो जाए। "काफ़ी अच्छा" कोई status नहीं है। एक ही seam पर सच में
दो बार अटको, तो blocker का ठीक-ठीक सबूत log करो और अगले खुले टुकड़े पर बढ़ो —
चुपचाप पिसते कभी मत रहो।

## Hard rules — इनमें से कोई एक भी skill fail कर देता है

- Live सच पर reproduction के बिना fix ship हुआ।
- Test fix के बाद लिखा गया, या fix ने उसे edit किया।
- Symptom पर patch लगा और class seam पर खुली रह गई।
- इंसान का अपना रास्ता टूटा हुआ है और proxy पर capability green बताई गई।
- Builder ने अपना ही बदलाव grade किया।
- कोई उठी हुई finding landing पर चुपचाप टाल दी गई।
- Loop "काफ़ी अच्छा" पर छोड़ा गया, escalate करने की जगह।

## Report

दो शब्द — **PROVEN** या **STILL-BUILDING** — साथ में सादी भाषा में intent, और
इंसान के सामने खड़ा अकेला फ़ैसला, अगर कोई हो। इंसान तक सवाल सिर्फ़ पसंद,
vision या destructive risk के लिए जाते हैं; देखो
[decision-bar](../decision-bar/SKILL.md)।

## इनके साथ अच्छा चलता है

- [incident-closure](../incident-closure/SKILL.md) — इंसान टूट-फूट report करे, तो यह loop पूरे close के अंदर चलता है।
- [red-first](../red-first/SKILL.md) · [seam-engineering](../seam-engineering/SKILL.md) · [sniper-testing](../sniper-testing/SKILL.md)
- [blind-tribunal](../blind-tribunal/SKILL.md) · [clean-code-gauntlet](../clean-code-gauntlet/SKILL.md)
