---
name: "seam-engineering"
description: "तब लगाओ जब कोई bug ठीक करना हो या किसी audit या bug hunt को बंद करना हो। Flaw की class को एक बार, उसके shared primitive पर ठीक करता है, हर sibling को sweep करता है, अगली instance पकड़ने वाला guard लगाता है, और सामने आई हर finding बंद करता है — कोई चुपचाप टालना नहीं। Trigger words: seam, class fix, whole-seam closure, point patch, structural guard, do it right the first time, पूरी class ठीक करो, जड़ से बंद करो, पहली बार में सही, पूरा seam बंद करो."
license: "MIT"
---

# Seam Engineering
**Effort:** free — शुद्ध मरम्मत का अनुशासन: N point patches की जगह shared primitive पर एक class fix। हटाता है: वही bug हर sibling site पर दोबारा सुधारना, और वह टाली हुई medium finding जो छह महीने में वह रहस्यमय bug बन जाती है जिसे कोई ढूँढ नहीं पाता।

Seam या तो सही और पूरा बंद होता है, या बंद होता ही नहीं।
आज का जल्दबाज़ patch वही bug है जो छह महीने बाद किसी को नहीं मिलता।
यह skill एक bug report को bugs की एक बंद class में बदल देती है।

## कब चलाएँ

कोई भी repair: reported bug, fail हुआ test, किसी audit या bug hunt की
findings की list। ख़ासकर तब, जब "बस यहीं patch कर दें" वाली खिंचावट महसूस हो।

## क़दम

1. **सबूत के साथ root cause।** वजह ठीक करो, symptom नहीं। Fix लिखने से पहले
   proof दिखाओ: एक failing repro, एक log line, एक trace जो असली seam की तरफ़
   इशारा करे। बिना सबूत का fix अंदाज़ा है।
2. **Flaw की CLASS का नाम लो।** पूछो: यह किस परिवार की ग़लती है, और वही
   ग़लती और कहाँ-कहाँ रह सकती है? Class को एक वाक्य में लिख डालो।
3. **Vertically ठीक करो — एक बार, shared primitive पर।** Shared primitive वह
   एक function या module है जिससे हर occurrence गुज़रती है। वहीं ठीक करो।
   कभी N point patches नहीं। कभी "ख़राब case mark करके compensate" नहीं।
4. **Horizontally sweep करो।** Class की हर sibling occurrence ढूँढ निकालो और
   उसी बदलाव में ठीक करो — "बाद में" नहीं।
5. **Structural guard लगाओ।** ऐसा test या automated check जो class की अगली
   instance पर fail हो। Class इसलिए बंद रहती है कि कोई चीज़ उस पर नज़र रखती
   है — इसलिए नहीं कि सबको याद है।
6. **पूरा seam बंद करो।** Hunt ने जो भी finding उठाई, सबकी list बनाओ। Landing
   से पहले हर एक या तो ठीक और green है, या उस पर सबूत के साथ खुला, दर्ज
   "not a bug" verdict है। चुपचाप टालना कभी नहीं। "किसी doc में park" कभी
   नहीं।

## Hard rules

- **जो repair नई failure condition जोड़े, वह ख़ुद bug है।** Crash कर सकने
  वाला rollback helper, state अधर में छोड़ने वाला cleanup, वह test जो जिस
  defect को पकड़ने के लिए था उसी को आशीर्वाद देने के लिए edit हुआ — सब bugs।
  बदलाव को एक atomic unit, या एक खुली crash-safe state machine की तरह दोबारा
  design करो। लीपापोती कभी नहीं।
- **"High-severity वाले ठीक कर दिए; बाक़ी follow-ups हैं" skill fail करता
  है।** यही वह आदत है जिसे मारने के लिए यह skill बनी है। टाला हुआ medium bug
  ही भविष्य का रहस्यमयी bug है। Seam की हर finding बराबर गिनी जाती है।
- **"Land करने लायक़ अच्छा" कोई status नहीं है।** Seam सही नहीं है तो iterate
  करते रहो — blocker हटाओ, ज़्यादा ताक़तवर model या reviewer तक escalate
  करो, retry करो — जब तक सही न हो जाए।
- **मौजूद shared primitive के बग़ल में point patch skill fail करता है।** अगर
  कोई primitive पहले से seam का मालिक है, तो fix उसी पर सवार होता है; bypass
  fix उसी class को दोबारा जन्म देता है।
- **Adjudicate हुए "not a bug" को सबूत चाहिए,** vote नहीं। दर्ज करो क्या
  जाँचा गया और finding क्यों नहीं टिकती।

## इनके साथ अच्छा चलता है

- [root-cause-first](../root-cause-first/SKILL.md) — step 1 के पीछे की जाँच
  वाली discipline।
- [red-first](../red-first/SKILL.md) — fix साबित करने वाला failing test, और
  step 5 के structural guard का pattern।
- [sniper-testing](../sniper-testing/SKILL.md) — iterate करते हुए scoped
  tests; landing पर एक full pass।
- [repair-loop](../repair-loop/SKILL.md) — वह end-to-end loop जिसके अंदर यह
  discipline चलती है।
- [incident-closure](../incident-closure/SKILL.md) — "fix it" का मतलब पूरा
  close है, option menu कभी नहीं।
