---
name: sniper-testing
description: किसी भी fix या build loop के दौरान लगाओ, और किसी भी green test पर भरोसा करने से पहले। सिर्फ़ वे tests चलाता है जो तुम्हारे छुए हुए code को cover करते हैं, और mock theater को मारता है — वे tests जो pass होते हैं जबकि capability टूटी पड़ी है। Trigger words: sniper testing, scoped tests, test scope, mock theater, fake green, full suite, test bloat, सिर्फ़ ज़रूरी tests, नक़ली green, पूरी suite मत चलाओ, test का दायरा.
license: MIT
---

# Sniper Testing
**Effort:** free — शुद्ध अनुशासन, कोई अतिरिक्त run नहीं; iteration के दौरान full-suite reruns मिटाकर net लागत सीधे घटाता है। हटाता है: test bloat (नन्हे-से diff पर पूरी suite के runs) और वे mock-theater greens जिन पर आप वरना आगे का काम खड़ा करते।

## यह क्यों है

Test का ज़्यादातर वक़्त दो failure modes खा जाते हैं। Test bloat: ज़रा-से
बदलाव पर पूरी suite चलाना। Mock theater: tests जो pass होते हैं जबकि असली
capability physically टूटी है। यह skill दोनों को मारती है।

## Rule 1 — scope diff तय करता है, optimism नहीं

Fix/build के iteration loop के दौरान पूरी test suite चलाना तुम्हारे लिए मना
है।

1. `git diff --name-only HEAD` चलाओ, ठीक-ठीक देखो कौन-सी files छुई हैं।
2. हर छुई file को उन test files से map करो जो उसे सीधे cover करती हैं
   (जैसे `src/payments/refund.py` → `tests/test_refund.py`)।
3. अपना specific test target बोलकर बताओ, फिर सिर्फ़ वही files चलाओ
   (Python: `pytest tests/test_refund.py`;
   JS: `npx vitest run tests/refund.test.js`;
   Go: `go test ./payments/ -run TestRefund`)।
4. जो test पहले pass हो चुका, वह दोबारा नहीं चलता — जब तक तुम्हारा अगला
   बदलाव उस code को न छुए जिसे वह exercise करता है। Scope diff तय करता है —
   न optimism, न डर।
5. Landing के वक़्त — commit gate पर — हर छुए module की suite पर EK full
   pass चलाओ। वही अकेला pass indirect couplings ठीक एक बार पकड़ता है।
   Iteration की रफ़्तार और पक्की landing — दोनों काम का हिस्सा हैं।

## Rule 2 — mock theater को मारो

Capability test को एक असली, physical side-effect assert करना ही होगा:

- "video बनाता है" → disk पर असली file मौजूद है, size > 0 bytes।
- "memory store करता है" → row असली local database से वापस पढ़ी जाती है।
- "widget render करता है" → page पर असली DOM element मौजूद है।

Database mock मत करो। File system mock मत करो। Local network sockets mock
मत करो।

एक ही mock जायज़ है: paid external transport की पत्ती — metered third-party
API वाली HTTP call। तब भी test को उसके इर्द-गिर्द की सारी असली logic से
गुज़रना होगा: request बनाना, routing, response parse करना। Wire को mock करो,
दिमाग़ को कभी नहीं।

## भरोसे से पहले audit

किसी भी test पर टिकने से पहले उसे पढ़ो। वह mock theater है — mocks की वजह से
green, कोई physical assertion नहीं — तो mock हटाओ और test को दोबारा लिखो
ताकि वह असली side-effect assert करे। जो test fail हो ही नहीं सकता, वह test न
होने से बदतर है: वह झूठ को certify करता है, और तुम उसी झूठ पर आगे बनाओगे।

## Hard rules (कोई एक भी टूटा तो skill fail)

- Iteration के दौरान कोई full-suite run नहीं।
- असली side-effect assertion के बिना कोई green का दावा नहीं।
- Capability test में paid external transport की पत्ती से आगे कोई mock नहीं।
- छुए modules पर उस अकेले full pass के बिना कोई landing नहीं।

## इनके साथ अच्छा चलता है

- [clean-code-gauntlet](../clean-code-gauntlet/SKILL.md) — sniper scope उसके पहले gate की ख़ुराक है
- [red-first](../red-first/SKILL.md) — fix से पहले failing test लिखो
- [seam-engineering](../seam-engineering/SKILL.md) — class ठीक करो, फिर scoped tests से sweep करो
