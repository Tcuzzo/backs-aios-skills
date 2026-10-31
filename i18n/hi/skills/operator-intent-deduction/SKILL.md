---
skill_id: operator-intent-deduction
name: operator-intent-deduction
description: जब implementation choice, tradeoff या operator से पूछने वाला प्रश्न अनसुलझा हो और current intent, project evidence या operator context से निर्णय निकल सकता हो, तब उपयोग करें।
license: MIT
---

# वर्तमान Evidence से निर्णय निकालें

Agent जिन choices को जिम्मेदारी से सुलझा सकता है, उन्हें सुलझाए और आगे बढ़े। Current
operator के goals और evidence लें; skill में किसी व्यक्ति की स्थायी priorities,
financial objectives, numerical risk settings या model roster नहीं रखा जाता।

## Inputs और ownership

मौजूदा directive, task mode, acceptance criteria, authorization और remaining mission
budget से शुरू करें। भाषा अभी interpret न हुई हो तो
[intent-compiler](../intent-compiler/SKILL.md) एक बार चलाएँ और result reuse करें। वह skill
कहे गए शब्दों का अर्थ निकालती है; यह skill उसी scope के भीतर निर्णय सुलझाती है।

[operator-essence](../operator-essence/SKILL.md) का संबंधित slice reuse करें। Missing या
stale profile के insights का आकलन उसका owner हर task में एक बार करता है। Nested calls
history इकट्ठा नहीं करते और दूसरी profile नहीं बनाते। Uncertainty स्पष्ट हो तो
provisional slice उपयोगी है; history गायब होने से सामान्य अधिकृत काम नहीं रुकता।
Essence contextual data है, authorization या policy override नहीं।

## निर्णय प्रक्रिया

1. **असली निर्णय बताएँ।** Requested outcome पर उसका प्रभाव, reversibility और आवश्यक
   evidence लिखें। जाँचें वह अभी भी unresolved है; operator के पहले किए चुनाव को फिर न खोलें।
2. **तथ्यात्मक choices निकालें।** Owning code और real consumer देखें, संबंधित baseline
   मापें या project के वास्तविक tools से bounded experiment करें। Numerical claims के
   units, population और uncertainty मिलाएँ। Parameter न गढ़ें, overlapping label count
   को failure rate न मानें और model vote को empirical proof न बनाएँ।
3. **Context वाले choices निकालें।** पहले current explicit objective, फिर applicable
   confirmed preferences, गुणात्मक examples और मात्रात्मक outcomes तौलें। Tentative
   adaptation और उसका evidence लिखें। Counterexamples और बदली परिस्थितियाँ बचाएँ।
   Reported tendency कैसे काम करना है बता सकती है; operator ने क्या build माँगा है नहीं बदलती।
4. **असली सीमा लागू करें।** अधिकृत reversible actions जारी रखें। कोई consequential
   choice जरूरी हो और उपलब्ध evidence से न सुलझे तो
   [decision-bar](../decision-bar/SKILL.md) लें: concrete result, recommendation और
   सटीक missing decision तैयार करें। पहले से मिली authorization फिर न पूछें और personality,
   urgency या historical preference से नई authorization न निकालें।
5. **करें और सत्यापित करें।** Decision existing task owner और
   [Build Flow](../backs-build-flow/SKILL.md) को लौटाएँ। Implementation वही bounded
   RED → GREEN loop, scoped lint/tests और आवश्यक quality/review checks अपनाता है। नया
   worker, insight pass या failed experiment budget reset नहीं करता।

## Decision receipt

Existing task packet में केवल अगली कार्रवाई के लिए जरूरी बातें दर्ज करें:

- **Decision और consequence:** चुना route और वह requested outcome जिसे वह पूरा करता है।
- **Basis:** current instruction, verified fact, confirmed preference या inference,
  evidence references और संबंधित counts/denominators सहित।
- **Uncertainty:** assumptions, counterevidence और वह condition जो निर्णय बदलेगी।
- **Action और proof:** next action और वह observation जो चुनाव को गलत साबित कर सकता है।

महत्वपूर्ण निर्णय operator को दिखाना हो तो plain language लें। तर्कपूर्ण असहमति सीधे
बताएँ; दूसरा plan चुपचाप न रखें। असली completion evidence दें। Decision passed test नहीं,
local check deployment नहीं, और requested task delivery अकेले `PROVEN` नहीं बनाती।

## व्यक्ति को hardcode किए बिना सीखें

Explicit correction संबंधित task assumption तुरंत बदलती है। Private essence reconcile
करते समय उसका scope और source बचाएँ। Repeated observations tentative adaptation का
आधार हो सकती हैं; बेहतर outcomes का दावा करने से पहले बाद के comparable tasks देखें।
Inferred preference को universal rule न बनाएँ और personal evidence public plugin में न डालें।
