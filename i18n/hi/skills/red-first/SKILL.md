---
name: red-first
description: तब लगाओ जब कोई भी builder — agent, model, या ख़ुद तुम — ऐसा बदलाव करने भेजा जाए जिसे कोई test साबित कर सके। Build शुरू होने से पहले साबित-failing contract test commit करता है, builder को उसे छूने से रोकता है, और एक independent grader से verify कराता है कि test कभी edit नहीं हुआ। Trigger words: red first, failing test first, contract test, red baseline, tamper-proof test, test before build, पहले failing test, पहले test लिखो, test को लॉक करो, build से पहले test.
license: MIT
---

# Red-First, Tamper-Proof
**Effort:** free — शुद्ध क्रम का अनुशासन: जो test आप वैसे भी लिखते वह पहले लिखा जाता है, red साबित होता है, और एक commit से seal हो जाता है; tamper check बस एक git diff है। हटाता है: fix के बाद pass होने की शक्ल में ढाले गए tests, और वे green फ़ैसले जिन्हें builder ने test बदलकर मोड़ लिया।

Fix के बाद लिखा test कुछ साबित नहीं करता — वह pass होने के लिए ही गढ़ा गया
था। जो test builder edit कर सकता है, वह और भी कम साबित करता है — उसे मोड़कर
pass कराया जा सकता है। इसलिए test पहले आता है, lock होता है, और अनछुआ grade
होता है।

## कब चलाएँ

कोई भी build या fix dispatch करने से पहले, जहाँ कोई test चाहा हुआ behavior
बयान कर सके। Bug fixes और नई capabilities — दोनों के लिए यही default है।

## क़दम

1. **Failing contract test लिखो।** वह चाहा हुआ behavior बताता है, उस सबसे
   छोटी शक्ल में जो उसकी ग़ैरमौजूदगी पकड़ ले। उसे अभी fail होना ही चाहिए।
2. **Red साबित करो।** Test चलाओ और उसे fail होते देखो — सही वजह से। जो test
   import पर error दे, या चुपचाप pass हो जाए, वह red नहीं है। जिसे किसी ने
   चलाया ही नहीं, वह red test अंदाज़ा है, baseline नहीं।
3. **Builder dispatch करने से PEHLE red test commit करो।** Commit id दर्ज
   करो। वही commit red baseline है — tamper seal।
4. **Builder को एक ही काम देकर भेजो: इसे green करो।** Builder को test file
   छूने की मनाही है। Dispatch में यह साफ़ लिखो।
5. **Independent grade कराओ।** ऐसा grader जिसने बदलाव नहीं लिखा, दो चीज़ें
   जाँचता है:
   - test अब pass होता है;
   - test file, red baseline से byte-दर-byte वही है —
     `git diff <red-sha> HEAD -- tests/test_contract.py` कुछ नहीं छापता।
   Test file पर कोई भी diff grade fail करता है। कोई रियायत नहीं, "बस एक typo
   ठीक किया" भी नहीं।
6. **बिखरे point tests से एक structural guard बेहतर।** Structural guard वह
   check है (एक grep sweep, एक AST scan, एक lint rule) जो अगले offender पर
   fail होता है, सिर्फ़ इसी instance पर नहीं। एक guard उन दस point tests से
   बेहतर है जो एक-एक case पिन करते हैं।

## Hard rules

- **Red को red साबित करना ज़रूरी है।** चलाओ, fail होते देखो — तभी गिनती में
  आएगा।
- **Builder कभी test edit नहीं करता।** Red baseline के बाद से test file का
  ख़ाली diff landing gate का हिस्सा है, शिष्टाचार की जाँच नहीं।
- **Builder कभी grader नहीं।** अलग इंसान, अलग agent, या builder से अलग
  family का model लो।
- **अकेला green proof नहीं है।** Green + अनछुआ test + independent grade —
  यह proof है।
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
