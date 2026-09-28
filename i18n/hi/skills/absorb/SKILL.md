---
name: "absorb"
description: "तब इस्तेमाल करें जब कोई capability किसी open-source project में पहले से मौजूद हो — डुप्लिकेट बनाने की बजाय उसे अपनाएँ और अपने harness के हिसाब से re-engineer करके native skill बनाएँ। Trigger words: absorb, adopt, port, re-engineer, ingest a repo, prior art, capability port, make this native, अपनाओ, समाहित करो, पोर्ट करो, दोबारा मत बनाओ, पहले से बना हुआ."
license: "MIT"
---

# Absorb — पहले से बना हुआ अपनाओ, दोबारा मत बनाओ
**Effort:** light — एक repo ingest (metadata probe + shallow clone) और port की एक cross-family grade। हटाता है: उस capability को दोबारा गढ़ना जिसे prior art पहले ही हल कर चुका है — वह from-scratch डुप्लिकेट जिसके हर bug का बोझ आप पर होता।

**Capability ही राजा है।** Repo तो बस capability को ढोने वाली गाड़ी है। जब आपको कुछ ऐसा
चाहिए जो कोई मौजूदा project पहले से करता है, तो न शून्य से डुप्लिकेट बनाओ, न
clone करके code चिपकाओ। सबसे अच्छा prior art (पहले से बना काम) ढूँढो, उसकी capability
निकालो, अपने harness में फिट होने लायक re-engineer करो, और scaffold को credit दो।
Citation एक तथ्य है, सजावट नहीं।

## कब चलाएँ

- आपसे कोई capability जोड़ने को कहा गया है (tool, skill, agent, pipeline) जो open source
  में शायद पहले से हल हो चुकी है।
- आप `git clone` करके code जस का तस copy करने वाले हैं — रुकिए; उसकी जगह यही रास्ता है।
- एक अकेले snippet, किसी config value, या किसी fact की खोज के लिए इसे छोड़ दें। वो बस पढ़ लें।

## कदम

1. **पहले prior art की तलाश करो।** बनाने से पहले खोजो। खुद गढ़ा हुआ डुप्लिकेट, अपनाए हुए
   scaffold से बदतर है: field testing शून्य मिलती है और सारे bugs आपके सिर।
2. **README से आगे जाकर पढ़ो।** Platform API से project का metadata (license, activity,
   language) निकालो। एक scratch directory में shallow-clone करो। Code और tests पढ़ो।
   README marketing है; code ही सच है।
3. **Trust gates चलाओ।**
   - *License:* permissive (MIT / Apache / BSD / MPL) = re-engineer करना सुरक्षित।
     Copyleft (GPL / AGPL) = सिर्फ technique — idea को re-engineer करो, code कभी
     copy मत करो। कोई license नहीं = all-rights-reserved मानो, सिर्फ technique।
     Non-commercial शर्तें = blocker; अपने human के पास ले जाओ।
   - *Shady scan:* cloak / spam / fake-review / scam patterns के लिए grep करो। ज़ोर से flag करो।
   - *बेलगाम install नहीं:* बिना जाँचे dependency का `pip install` / `npm install` कभी
     नहीं (typo-squatting असली supply-chain हमला है)। उसकी जगह अपने ही primitives के
     ऊपर पतला code लिखकर re-engineer करो।
   - *Capability असली है भी?* दावों को स्वतंत्र सबूत से जाँचो। बेचने वाले का blog दावा
     है, सबूत नहीं। फ़ैसला: real / hype / scam / unverifiable.
   - *Bounded egress:* अपनाया हुआ version जो भी fetch करे, वो throttled, cached और
     बंद करने लायक (killable) होना चाहिए।
4. **Capability map में तोड़ो।** Project की हर ability के लिए दर्ज करो: क्या करती है,
   कैसे, उसके load-bearing seams, उसका bloat या risk, अपने stack से क्या reuse हो सकता
   है, और वो native उतरेगी या किसी पतले adapter के पीछे। हर capability **या तो सबूत के
   साथ बचाई जाती है या सबूत के साथ खारिज होती है**। चुपचाप गिरा दी गई capability एक defect है।
5. **Re-engineering spec लिखो।** कौन से seams बनने हैं, कौन सा bloat गिराया जा रहा है
   (ज़ोर से दर्ज, कभी चुपचाप नहीं), और हर capability के लिए एक failing contract test जो
   असली side-effect जाँचे — एक file, database की row, असली output। सिर्फ paid external
   API का transport mock करो, logic कभी नहीं।
6. **Red-first दोबारा बनाओ।** Failing tests commit करो, फिर पूरे seam पर green होने तक
   बनाओ। नतीजे को builder से अलग family का model grade करता है — builder अपना काम
   खुद कभी grade नहीं करता।
7. **Credit दो और दर्ज करो।** जहाँ capability अब रहती है वहीं scaffold credit लिखो:
   author, project, license, क्या उधार लिया (scaffold) और क्या आपका है
   (re-engineering)। Credit कभी गढ़ो मत। कभी हटाओ मत।

## सख़्त नियम — इनमें से कोई एक भी टूटा तो skill fail

- Capability को re-engineer करने की बजाय code जस का तस copy करना।
- Prior art खोजे बिना ही डुप्लिकेट बना डालना।
- Code की बजाय README या marketing page पर भरोसा करना।
- Technique को re-engineer करने की बजाय बेलगाम dependency install कर लेना।
- Copyleft या बिना-license वाला code copy करना (हमेशा सिर्फ technique)।
- बिना लिखित खंडन के कोई capability गिरा देना।
- Capability test में mock theater — test को असली side-effect छूना ही होगा।
- Scaffold citation के बिना ship करना।

## इनके साथ अच्छा चलता है

- [red-first](../red-first/SKILL.md) — हर capability की रखवाली करने वाले contract tests.
- [sniper-testing](../sniper-testing/SKILL.md) — असली side-effects, mock theater नहीं।
- [blind-tribunal](../blind-tribunal/SKILL.md) — port की cross-family grading.
- [decision-bar](../decision-bar/SKILL.md) — license के blockers और taste के फ़ैसले आपके human तक जाते हैं; बाक़ी सब execute होता है।
