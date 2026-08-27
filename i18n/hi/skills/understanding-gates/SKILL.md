---
name: understanding-gates
description: तब लगाओ जब कोई build, fix या uplift intent से delivery की तरफ़ बढ़ रहा हो और तुम्हें proof चाहिए कि वह अब भी original माँग से मेल खाता है। Design, Plan, Build, Test और Ship से जिरह करता है — approve/revise/reject verdicts, नामी failures बतौर repair targets, और हर repair के बाद rerun। Trigger words: understanding, stage gates, validate build, spec match, verdict, green but wrong, echo check, done means done, समझ की जाँच, माँग से मिलाओ, हर stage पर परखो, green पर भी ग़लत.
license: MIT
---

# Understanding Gates

Builds के लिए एक validation discipline। यह काम से पाँच stages पर जिरह करती है
— Design, Plan, Build, Test, Ship — हमेशा ORIGINAL माँग के ख़िलाफ़, काम की
अपनी दोहराई हुई भाषा के ख़िलाफ़ कभी नहीं। हर gate सबूत लौटाता है: scores, एक
verdict, नामी failures, और repair actions। यह agent को बाँधती है, इंसान को
नहीं: कोई नया approval step नहीं, पूछने वाले पर कोई friction नहीं।

## कब चलाएँ

- कोई भी build, fix या uplift जो किसी असली जगह land होगा।
- जब भी "done" कहने ही वाले हो और अकेला proof एक green test हो।
- हर repair के बाद, उसी stage पर जो fail हुई थी।

## Stage 0 — intent को लंगर बनाओ

कुछ भी score करने से पहले comparison का लंगर पक्का करो: इंसान के ORIGINAL
शब्द, साथ में एक-line का translated directive (देखो
[intent-compiler](../intent-compiler/SKILL.md))। हर gate उसी लंगर के ख़िलाफ़
score करता है। अपने paraphrase के ख़िलाफ़ कभी score मत करो — paraphrase बहकता
है, और फिर हर gate चुपचाप माँग की जगह उस बहकाव को validate करता है।

## पाँच gates

हर gate original intent के ख़िलाफ़ एक सवाल पूछता है:

| Stage | सवाल |
| --- | --- |
| Design | क्या spec साफ़ है और original माँग के प्रति वफ़ादार? |
| Plan | क्या plan intent का जवाब देता है और उस सतह पर बैठता है जहाँ यह ship होगा? |
| Build | क्या code बिना बहके spec को पूरा करता है? |
| Test | क्या tests असली behavior को exercise करते हैं, उसके किसी stand-in को नहीं? |
| Ship | क्या यह साफ़ apply होता है, ज़ोर से fail होता है, और delivery का दावा fact check से बचता है? |

HAR gate को उन्हीं पाँच lenses पर score करो, हर एक 0–4: spec match,
architectural fit, type safety, testability, security — stage के हिसाब से
ढाले हुए (Design पर "testability" पूछती है spec जाँचने लायक़ है या नहीं;
Ship पर, delivery का दावा)। Roll-up: पाँचों lenses जोड़ो (0–20), 5 से गुणा
करो — वही gate का 0–100 verdict score है। हर lens दर्ज करो, सिर्फ़ total
नहीं — total छिपा देता है कौन-सी lens fail हुई।

## Verdicts

Lenses को 0–100 score में जोड़ो और band दो:

- **Approve** (80+): मज़बूत सबूत। फिर भी done का proof नहीं — दूसरा क़ानून
  देखो।
- **Revise** (60–79): नामी failures मौजूद हैं। हर एक repair target है।
- **Reject** (60 से नीचे): काम intent से चूकता है। एक stage पीछे जाओ।

जिस verdict के पीछे कोई नामी failure नहीं, वह low-information verdict है।
List माँगो।

## Repair की discipline

1. हर rerun के लिए original intent ही लंगर रहे।
2. Per-lens scores दर्ज करो, सिर्फ़ ऊपर वाला नंबर नहीं।
3. हर नामी failure एक repair target है। कोई failure सजावट नहीं।
4. Repair करो, फिर WAHI GATE दोबारा चलाओ। Rerun के बिना repair सिर्फ़ एक
   दावा है।
5. Confidence को readiness में कभी मत बदलो। फ़ैसला tests और असली सतह करते
   हैं।

## दो क़ानून

**1. Echo का क़ानून।** जो check सिर्फ़ हाँ में हाँ मिला सकता है, वह echo है,
validator नहीं। ईमानदारी का proof refutation है: उसे एक ऐसा दावा खिलाओ जिसे
तुम झूठा जानते हो, और देखो वह उसे fail करता है। झूठ को pass कर दे, तो check
theater है। Mocking पर corollary: सिर्फ़ अस्थिर external पत्ती mock करो —
कोई paid API, कोई flaky network। उस organ को कभी mock मत करो जिसका behavior
ही proof है; उसकी scoring, claim निकालना, और pass/fail logic असल में चलने
चाहिए।

**2. ज़रूरी, पर काफ़ी नहीं।** Pass होता test ज़रूरी है, काफ़ी कभी नहीं। Done
का मतलब: असली सतह — जो इंसान सच में इस्तेमाल करता है — काम ख़ुद कर देती है।
उस सतह का नाम लो, असली रास्ता trigger करो, और सही नतीजा आते देखो। Unit-test
की receipt को live-capability के दावे में कभी मत बदलो।

## Hard rules (क्या इस skill को fail करता है)

- Original माँग की जगह paraphrase के ख़िलाफ़ scoring।
- Revise या reject verdict जिसके साथ कोई नामी failure नहीं।
- Fail हुए gate को rerun किए बिना repair।
- Validator को ही mock करना, या ठीक उसी seam को जो बदल रहा है।
- Green test से done का दावा, असली सतह के proof के बिना।

## Build का record रखो

हर stage के लिए रखो: intent, exact input artifact, scores, नामी failures,
किया गया repair, rerun का नतीजा, और असली सतह का सबूत। जो record reproducible
सबूत की तरफ़ इशारा नहीं करता, वह banner है, record नहीं।

## इनके साथ अच्छा चलता है

- [intent-compiler](../intent-compiler/SKILL.md) — score करने से पहले माँग को translate करो।
- [red-first](../red-first/SKILL.md) — Test gate का contract: failing test पहले commit।
- [sniper-testing](../sniper-testing/SKILL.md) — असली side-effects, कोई mock theater नहीं।
- [blind-tribunal](../blind-tribunal/SKILL.md) — इन gates के ऊपर independent graders।
- [repair-loop](../repair-loop/SKILL.md) — वह loop जो revise verdicts को green तक ले जाता है।
