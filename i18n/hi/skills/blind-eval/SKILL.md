---
name: blind-eval
description: तब इस्तेमाल करें जब taste या output quality सवाल हो और कोई test फ़ैसला न कर सके — authorship छिपाकर बदलाव को उसके गुणों पर परखता है, फिर keep या revert; tie पर revert, सिर्फ साबित हुआ सुधार ही उतरता है। Trigger words: blind eval, karpathy, keep or revert, quality gate, taste call, blind judge, A/B judge, prove uplift, अंधी परख, रखें या पलटें, गुणवत्ता द्वार, सुधार साबित करो.
license: MIT
---

# Blind Eval
**Effort:** light — एक blind judge run: frozen जोड़ी की कई shuffled पढ़ाइयाँ, उस model से जिसने दोनों में से कोई नहीं लिखा। हटाता है: खुद को grade देकर "यह बेहतर है" वाली landings — वे taste regressions जिन्हें लेखक खुद हाथ के इशारे से पास कर देता।

एक keep-or-revert quality gate उन फ़ैसलों के लिए जो कोई test तय नहीं कर सकता —
लिखावट की quality, UI copy, किसी refactor की पठनीयता, किसी prompt का output, किसी
design का एहसास। बदलाव को authorship छिपाकर उसके गुणों पर परखो, फिर KEEP करो या
REVERT करो। Tie का मतलब revert। सिर्फ साबित हुआ सुधार ही उतरता है।

## कब चलाएँ

- ऐसा कोई भी बदलाव उतारने से पहले जहाँ "बेहतर है क्या?" taste या quality का सवाल हो।
- किसी improvement loop के अंदर gate की तरह: propose → try → measure → keep या discard.
- जब भी author अपने ही काम को improvement घोषित करने के मूड में हो।

## तरीक़ा

1. **देखने से PEHLE "बेहतर" लिखकर तय करो।** सादी भाषा में एक goal। एक primary
   measure या rubric axis जिस पर एक सख़्त bar हो — एक level जो पार करना है, कोई
   ऐसा नंबर नहीं जिसे बस बढ़ाते जाना है। Secondary axes priority क्रम में (cost,
   length, latency)।
2. **दोनों versions freeze करो।** Baseline और candidate, असली artifacts के रूप में —
   उनके बारे में कोई description कभी नहीं।
3. **Authorship हटाओ।** उन्हें A और B नाम दो, क्रम फेंटो (shuffle), हर नाम, model id
   और author की दलील हटा दो। Judge को सिर्फ artifacts और rubric दिखते हैं।
4. **ऐसा judge बिठाओ जिसने दोनों में से कुछ नहीं लिखा** — किसी दूसरी family का
   model, या एक इंसान। Author अपना काम खुद कभी grade नहीं करता।
5. **गुणों पर परखो।** हर rubric axis पर score दो। हर score के लिए artifact से सबूत
   cite करो — बिना सबूत का verdict एक अंदाज़ा है।
6. **KEEP सिर्फ तब जब candidate bar पार करे AND baseline को साफ़-साफ़ हराए।**
   Tie कोई सुधार नहीं — revert.
7. **साफ़ revert करो।** Tree को बदलाव से पहले वाली हालत में byte-identical बहाल करो
   (एक scratch branch या stash इसे एक command बना देता है)। Verdict दोनों सूरतों में
   log करो।

## वो नियम जो gaming रोकते हैं

- **पहले bar जाँची जाती है, और axes क्रम से गिनते हैं।** ऊँची priority वाले axis पर
  regression जानलेवा है, भले ही हर नीचे वाला axis सुधरे। और bar को extra margin से
  पार करने का कोई फ़ायदा नहीं — primary में बढ़त से cost का regression "चुकाया"
  नहीं जा सकता।
- **नतीजा देखने के बाद bar कभी नीचे मत करो।** Eval को कमज़ोर करके score ठीक करना
  मना है। Rubric और eval उन files के बाहर रखो जिन्हें बदलाव छू सकता है।
- **Self-grading नहीं।** Judge को author की दलील कभी नहीं दिखती — जो judge sales
  pitch पढ़ता है वो pitch को grade करता है, काम को नहीं।
- **Stochastic judge का शोर निकालो।** Blind readings हर run में बदलती हैं, और
  judges पहले दिखे option को पसंद करते हैं। हर तुलना कई बार चलाओ, क्रम फेंटकर,
  और majority vote लो — shuffle position bias मारता है और repeats शोर मारते हैं,
  एक ही चाल में। अगर असली सुधार judge के run-दर-run झूले से छोटा है, तो gate
  signal और तुक़्क़े में फ़र्क़ नहीं कर सकता — readings बढ़ाओ या कोई स्थिर measure चुनो।
- **Solo rig.** दूसरी model family नहीं है? एक ताज़ा blind session जो author की
  बातचीत ने कभी नहीं देखी, judge बनता है — और report कमज़ोर हुए gate का नाम लेती
  है ("judged same-family-blind, not cross-family")।
- **भरोसेमंद bar नहीं? Dominance इस्तेमाल करो।** जब baseline का level अनजान या
  शोर-भरा हो, absolute bar छोड़ो और सिर्फ वही रखो जो मौजूदा champion को साफ़ हराए।
  Regression कभी dominate नहीं कर सकता, इसलिए किसी floor की ज़रूरत नहीं।
- **Cost वाला axis कभी failures पर मत नापो।** Fail हुई कोशिशों पर गिना "कम steps"
  जल्दी हार मानने को इनाम देता है। Cost और effort सिर्फ successes पर गिनो।

## Judge का bias निकालो

Judge-mechanics का floor। ये यहीं रहते हैं, और कहीं नहीं:

- **Held-out suite.** Builder की write पहुँच के BAHAR रखे suite पर grade करो —
  builder graded tests कभी नहीं देखता, इसलिए उन पर hardcode नहीं कर सकता।
- **Fresh-commit strip.** Graded run से पहले workspace को एक ताज़ा commit तक
  छाँटो और network egress रोको, ताकि pass DERIVED हो — git history या किसी और के
  fix से उठाया हुआ नहीं।
- **Length-normalize.** Judges लंबे जवाब को ज़ोर से तरजीह देते हैं — scores की
  तुलना से पहले length की भरपाई करो।
- **घुमाए हुए holdout criteria.** नामित-axis, yes/no rubric इस्तेमाल करो जिसमें
  छिपे holdout criteria runs के बीच घुमाए जाते हैं। दिखता हुआ holistic score
  citation theater में game हो जाता है।
- **Final-state grading.** कई-step के काम को FINAL end-state पर grade करो, हर
  बीच वाले step पर नहीं।
- **Judge calibration.** Judge को एक छोटे human-labeled set पर calibrate करो —
  उसकी true-positive और true-negative दरें report करो — अपने domain पर उस पर
  भरोसा करने से पहले।

क्रम फेंटना ऊपर वाले denoise नियम का हिस्सा है — एक क़ानून, एक बार कहा गया।

## Loop वाला रूप

यही gate एक autonomous improvement loop भी चलाता है: छोटा बदलाव propose करो →
छोटा experiment चलाओ → blind नापो → बेहतर तो keep, वरना revert → दोहराओ, एक तय
round budget पर। Proposer को पिछले round के failure traces दो, सिर्फ goal नहीं —
जो proposer देख ही नहीं सकता कि वो क्यों fail हो रहा है, वो अंधा edit करता है।
जो loop कुछ भी keep नहीं करता वो भी अपनी क़ीमत कमा लेता है: उसके जुटाए traces
ठोस, ठीक करने लायक bugs की तरफ़ इशारा करते हैं जो कोई aggregate score नहीं दिखाता।

## इनके साथ अच्छा चलता है

- [blind-tribunal](../blind-tribunal/SKILL.md) — जब सवाल taste नहीं बल्कि defects हों, तब का भारी juror panel.
- [red-first](../red-first/SKILL.md) — जब कोई test फ़ैसला कर SAKTA हो, तो test ही लिखो।
- [clean-code-gauntlet](../clean-code-gauntlet/SKILL.md) — taste के फ़ैसले के साथ जोड़ने लायक नापे हुए code-quality gates.

> Namesake credit: Andrej Karpathy. Namesake inspiration; the keep-or-revert
> discipline is independently paralleled in Karpathy's autoresearch (2026,
> github.com/karpathy/autoresearch, MIT). The blind (author-hidden) aspect and
> the composition and hard rules here are BACKS AIOS.
