---
name: "red-first"
description: "Test से साबित हो सकने वाले behavior change के लिए builder dispatch से पहले, या नए review finding/mutation gap को regression contract चाहिए तब उपयोग करें।"
license: "MIT"
---

# Red-First, Tamper-Proof
**Effort:** free — शुद्ध क्रम का अनुशासन: जो test आप वैसे भी लिखते वह पहले लिखा जाता है, red साबित होता है, और एक commit से seal हो जाता है; tamper check बस एक git diff है। हटाता है: fix के बाद pass होने की शक्ल में ढाले गए tests, और वे green फ़ैसले जिन्हें builder ने test बदलकर मोड़ लिया।

केवल fix के बाद देखा गया green result न original failure साबित करता है, न उसे
पकड़ने की test की क्षमता। Fix से पहले original RED साबित करके seal करें; builder
उस file को अपरिवर्तित रखे। अलग supplemental regression बाद में controlled mutant
पर failure और unmutated candidate पर pass दिखा सकता है, जैसा नीचे बताया गया है।

Current [BACKS Build Flow](../backs-build-flow/SKILL.md) task packet लें। यह skill
RED seal की owner है; नया build owner या lifecycle नहीं बनाती। Pinned `base_sha`,
current `candidate_sha` और mission identity बचाएँ।
[bounded-loops](../bounded-loops/SKILL.md) deadline तथा remaining attempts reproduction,
builders, supplemental tests और independent reviews सभी पर लागू हैं। Valid existing RED
receipt reuse करें; नया failure गढ़ें नहीं।

## कब चलाएँ

कोई भी build या fix dispatch करने से पहले, जहाँ कोई test चाहा हुआ behavior
बयान कर सके। Bug fixes और नई capabilities — दोनों के लिए यही default है।

## क़दम

1. **Failing contract test लिखो।** वह चाहा हुआ behavior बताता है, उस सबसे
   छोटी शक्ल में जो उसकी ग़ैरमौजूदगी पकड़ ले। उसे अभी fail होना ही चाहिए।
2. **Red साबित करो।** Test चलाओ और उसे fail होते देखो — सही वजह से। जो test
   import पर error दे, या चुपचाप pass हो जाए, वह red नहीं है। जिसे किसी ने
   चलाया ही नहीं, वह red test अंदाज़ा है, baseline नहीं।
3. **Builder dispatch से पहले RED commit करें।** Commit ID, exact test paths/bytes,
   failing command/output और reason दर्ज करें। यह commit red baseline और tamper seal
   है; aggregate change scope का mission `base_sha` इससे replace नहीं होता।
4. **Builder को एक ही काम देकर भेजो: इसे green करो।** Builder को test file
   छूने की मनाही है। Dispatch में यह साफ़ लिखो।
5. **Independent grade कराओ।** ऐसा grader जिसने बदलाव नहीं लिखा, दो चीज़ें
   जाँचता है:
   - test अब pass होता है;
   - test file, red baseline से byte-दर-byte वही है —
     `git diff <red-sha> <candidate_sha> -- tests/test_contract.py` कुछ नहीं छापता।
     Pending work जाँचने पर actual tested bytes भी seal से मिलाएँ; clean committed
     diff staged या unstaged edit को सही नहीं ठहराता।
   Test file पर कोई भी diff grade fail करता है। कोई रियायत नहीं, "बस एक typo
   ठीक किया" भी नहीं।
6. **बिखरे point tests से एक structural guard बेहतर।** Structural guard वह
   check है (एक grep sweep, एक AST scan, एक lint rule) जो अगले offender पर
   fail होता है, सिर्फ़ इसी instance पर नहीं। एक guard उन दस point tests से
   बेहतर है जो एक-एक case पिन करते हैं।

## Original seal के बाद नया finding

Mutation survivor या review finding missing assertion दिखा सकता है। Original RED
file byte-identical रखें और **अलग supplemental test file** जोड़ें। नए defect के fix से
पहले test failing देखें; mutation gap में relevant controlled mutant पर isolated
failure और unmutated candidate पर pass दिखाएँ। अगला builder seam बदले उससे पहले
supplemental evidence record और seal करें। इसे original baseline न कहें। Grader दोनों
seals और exact aggregate candidate जाँचता है। Test जोड़ना original contract कमजोर करने,
rename करने या replace करने की अनुमति नहीं देता।

Shared budget समाप्त हो या RED स्थापित न हो सके तो gap और exact next action सहित
**STILL-BUILDING** checkpoint दें। RED न गढ़ें; green पाने को mission reset न करें।

## Hard rules

- **Red को red साबित करना ज़रूरी है।** चलाओ, fail होते देखो — तभी गिनती में
  आएगा।
- **Builder कभी test edit नहीं करता।** Red baseline के बाद से test file का
  ख़ाली diff landing gate का हिस्सा है, शिष्टाचार की जाँच नहीं।
- **Builder कभी grader नहीं।** Configured rung matrix से capability/availability
  के अनुसार non-builder reviewer चुनें। Authoring execution provenance में record और
  disqualify करें; review fresh author-disjoint session में हो।
- **अकेला green proof नहीं है।** Green + untouched test + independent grade इस
  contract को सिद्ध करते हैं; live capability claim को task workflow का real-surface
  और delivery evidence भी चाहिए।
- **जब defect की पूरी class खेल में हो, class को guard करो।** Point tests
  यह bug रोकते हैं; structural guard अगला रोकता है।

## इनके साथ अच्छा चलता है

- [sniper-testing](../sniper-testing/SKILL.md) — iterate करते हुए सिर्फ़ वही
  tests चलाओ जिन्हें बदलाव छूता है; landing पर एक full pass।
- [seam-engineering](../seam-engineering/SKILL.md) — वह class-fix discipline
  जिसकी structural guard हिस्सा है।
- [blind-tribunal](../blind-tribunal/SKILL.md) — independent graders जिन्होंने
  author को कभी देखा नहीं।
- [repair-loop](../repair-loop/SKILL.md) — वह loop जो red → green → proven को
  end to end ले जाता है।
