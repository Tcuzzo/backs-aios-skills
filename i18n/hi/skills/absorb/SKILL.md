---
name: "absorb"
description: "जब जरूरी capability किसी open-source project में पहले से हो सकती हो, या operator absorb, adopt, port, re-engineer, ingest a repo, prior art evaluation या existing capability को native बनाने को कहे, तब उपयोग करें।"
license: "MIT"
---

# Absorb — पहले से बना हुआ अपनाओ, दोबारा मत बनाओ
**Effort:** light — एक repo ingest (metadata probe + shallow clone) और port की एक independent, capability-resolved grade। हटाता है: उस capability को दोबारा गढ़ना जिसे prior art पहले ही हल कर चुका है — वह from-scratch डुप्लिकेट जिसके हर bug का बोझ आप पर होता।

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

Current [BACKS Build Flow](../backs-build-flow/SKILL.md) task packet और integration
owner लें। Direct invocation packet एक बार बनाता है; nested call adoption evidence
caller को लौटाता है। Valid context, operator essence और loaded skill bodies reuse करें।
[bounded-loops](../bounded-loops/SKILL.md) mission deadline और remaining attempt/round
allowances का owner है; discovery, builds, mutation, reviews, model changes और handoffs
सब इसी budget से खर्च होते हैं। नया phase या worker budget reset नहीं करता। Packet का
`task_mode` मानें: review या diagnosis native edits या delivery की अनुमति नहीं देता।

1. **पहले prior art की तलाश करो।** बनाने से पहले खोजो। खुद गढ़ा हुआ डुप्लिकेट, अपनाए हुए
   scaffold से बदतर है: field testing शून्य मिलती है और सारे bugs आपके सिर।
2. **README से आगे discovery।** Platform API से metadata (license, activity,
   language) लें। Scratch directory में shallow-clone करें और code/tests पढ़ें। Shipped
   artifact या requested runtime behavior का उत्तर source से न मिले तो exact target
   और bounded question के साथ [rea-investigation](../rea-investigation/SKILL.md) लें।
   REA evidence इसी caller को लौटाता है, Absorb फिर शुरू नहीं करता। Adoption चुनने से
   पहले upstream identity, observations, limits और unknowns लिखें। Static findings
   runtime behavior सिद्ध नहीं करते।
3. **Trust gates चलाओ।**
   - *License:* permissive (MIT / Apache / BSD / MPL) = re-engineer करना सुरक्षित।
     Copyleft (GPL / AGPL) = सिर्फ technique — idea को re-engineer करो, code कभी
     copy मत करो। कोई license नहीं = all-rights-reserved मानो, सिर्फ technique।
     Non-commercial शर्तें = blocker; अपने human के पास ले जाओ।
   - *Shady scan:* cloak / spam / fake-review / scam patterns के लिए `rg` करो। ज़ोर से flag करो।
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
6. **Native integration।** [red-first](../red-first/SKILL.md) अपनाएँ: owning seam के
   minimal fix से पहले real failure देखें और contract seal करें। Original test file
   न बदलें। [sniper-testing](../sniper-testing/SKILL.md) से pinned `base_sha` और current
   `candidate_sha`, तथा applicable owned pending paths के आधार पर repo की वास्तविक
   lint, type-check और test commands scope करें। Unavailable/inapplicable checks
   स्पष्ट लिखें; arbitrary checker install या passing result न गढ़ें। Quality और
   mutation evidence के लिए [clean-code-gauntlet](../clean-code-gauntlet/SKILL.md)
   inline चलाएँ। Test gap के लिए separate supplemental regression जोड़ें; sealed
   original न बदलें। सारा काम साझा budget में रहे।
7. **अपनाई capability का verification।** Native result capability map और user के actual
   surface पर exercise करें। Discovery evidence reuse करें; specific unresolved
   comparison हो तभी REA observation लें, उसकी existing provider/execution boundaries
   में। Configured rung matrix से capable grader चुनें; exact aggregate candidate की
   fresh author-disjoint review में authoring execution record और exclude करें। Builder
   अपना काम grade नहीं करता। Required affected-suite landing pass चलाएँ और project की
   authorized delivery procedure अपनाएँ। Static upstream evidence या local GREEN
   अकेले native live delivery सिद्ध नहीं करता।
8. **Credit और record।** जहाँ capability रहती है वहाँ author, project, license,
   borrowed scaffold और अपनी re-engineering का credit लिखें। Credit न गढ़ें, न हटाएँ।
   Capability map, exact candidate, check results, attribution और unresolved gaps
   integration owner को लौटाएँ। Budget खत्म हो या required gate न चल सके तो remaining
   work और next action के साथ **STILL-BUILDING** checkpoint करें; exhausted allowance
   खर्च किए बिना उपयोगी authorized work जारी रखें। **PROVEN** न गढ़ें और pass पाने को
   capability चुपचाप न हटाएँ।

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
- [blind-tribunal](../blind-tribunal/SKILL.md) — port की independent non-author grading।
- [decision-bar](../decision-bar/SKILL.md) — license के blockers और taste के फ़ैसले आपके human तक जाते हैं; बाक़ी सब execute होता है।
