---
name: live-research
description: तब लगाओ जब किसी codebase, API या system पर reasoning हो रही हो और उसकी असल शक्ल मायने रखती हो। एक parallel research agent चलाता है जो live सच पढ़ता है — project के अपने READMEs, section docs, असली source — ताकि नतीजे उस पर टिकें जो सच में वहाँ है, model की याददाश्त पर नहीं। Trigger words: live research, ground the reasoning, read the real source, check what is actually there, primary sources, background research, verify against the repo, what do the docs say, असली source पढ़ो, repo से मिलाओ, docs क्या कहते हैं, ज़मीनी सच.
license: MIT
---

# Live Research

Model की याददाश्त एक अंदाज़ा है कि training के वक़्त project कैसा दिखता था।
Live सच वह है जो अभी disk पर और official docs में बैठा है। यह skill दोनों
lanes एक साथ चलाती है: main lane target पर reasoning करती है, और उसी वक़्त
एक research agent असली चीज़ पढ़ता है — और उसकी findings किसी भी नतीजे से
**पहले** reasoning में मिल जाती हैं।

## कब चलाएँ

- तुम किसी project के structure, किसी API के contract, या किसी library के
  behavior पर reasoning करने वाले हो — और मौजूदा source पढ़ा नहीं है।
- कोई design, fix या दावा ऐसे facts पर टिका है जो तुम्हारे training data के
  बाद बदल चुके हो सकते हैं।
- किसी सवाल को असल दुनिया के ऐसे facts चाहिए जो working context अकेले नहीं
  दे सकता।

## क़दम

1. **Researcher को parallel में छोड़ो।** जिस पल target पर reasoning शुरू हो,
   उसी target पर एक background research agent dispatch करो। Main lane काम
   करती रहती है; researcher पढ़ता है। जो भाग-दौड़ एक agent अकेला कर सकता है,
   उस पर काम को कभी मत रोको।
2. **Live सच पढ़ो, सबसे नज़दीक से शुरू करके।** पहले project का अपना README,
   फिर target के सबसे पास के section docs, फिर असली source structure — असली
   directory listing, असली file contents, असली signatures। Project के बाहर
   के facts के लिए: official docs, source code, specs, first-party APIs। जो
   blog docs का सार सुनाता है, वह primary source नहीं है।
3. **नतीजों से पहले findings वापस stream करो।** Findings आते ही main lane
   में पहुँचती हैं, और reasoning उन्हें समेटकर रास्ता ठीक करती है। जिस बिंदु
   पर researcher ने report नहीं दी, उस पर पहले निकाला नतीजा एक अंदाज़ा है —
   उसे अंदाज़ा ही कहो, जब तक live सच उसे पक्का या ख़त्म न कर दे।
4. **हर दावे को उसके मालिक source से बाँधो।** हर finding अपना source साथ
   रखती है: एक file path, एक quoted line, एक link, एक commit। जो दावा बाँधा
   नहीं जा सकता, वह unverified marked होता है — ज़ोर से; उसे fact का लिबास
   कभी नहीं पहनाया जाता।
5. **एक cited file लिखो।** Findings एक ही Markdown file में उतरती हैं, हर
   दावा अपने source के साथ। उसे वहीं रखो जहाँ project ऐसे notes पहले से रखता
   है; कोई रिवाज़ न हो तो समझदारी की जगह चुनो और बता दो कहाँ रखी, ताकि अगला
   agent उसे पा सके।
6. **दोबारा पढ़ने से पहले याद करो।** पहले पिछले sessions के notes देखो — वही
   source शायद पहले से खिंचा हुआ है। Cached finding दोबारा इस्तेमाल करो और
   वही source cite करो। मिनटों की recall घंटों की दोबारा खोज से बेहतर है।

## Hard rules

- **Merge से पहले कोई नतीजा नहीं।** जिस बिंदु पर researcher ने report नहीं
  दी, main lane उसे तय हुआ नहीं कह सकती।
- **सिर्फ़ primary sources।** हर दावे को उसके मालिक source तक वापस ले जाओ।
  Secondary write-up एक pointer है, proof नहीं।
- **Headless, कभी watched नहीं।** Background research headless fetch रास्ते
  से चलती है — कभी उस live browser से नहीं जिसे कोई इंसान देख रहा हो; वह
  अलग lane है।
- **Verify नहीं हो सकता, तो कह दो।** जिस finding का कोई primary source नहीं,
  वह flag होकर ship होती है — बाक़ी में चुपचाप घुलकर कभी नहीं।
- **इंसान पर zero friction।** यह skill कोई approval step और कोई gate नहीं
  जोड़ती। यह method की discipline है, checkpoint नहीं।

## वापस क्या आता है

एक grounded, cited Markdown file — और साथ में एक reasoning lane जो नतीजा
ship होने के बाद नहीं, बीच उड़ान में ठीक हुई। Main lane file पढ़ती है और आगे
बढ़ती है।

## इनके साथ अच्छा चलता है

- [wayfinder](../wayfinder/SKILL.md) — research tickets वही agent-alone क़िस्म हैं जो यह skill हल करती है।
- [root-cause-first](../root-cause-first/SKILL.md) — वही source-first discipline, bugs पर तानी हुई।

> Scaffold credit: Matt Pocock, research (mattpocock/skills, MIT). यहाँ का
> composition और hard rules BACKS AIOS के हैं।
