---
name: intent-compiler
description: जब request संक्षिप्त prose, metaphor, slang, shorthand या अस्पष्ट references में आए और agent को evidence आधारित technical directive चाहिए, तब उपयोग करें। Correction intended capability या requested finish बदले तब भी उपयोग करें।
license: MIT
---

# वर्तमान अनुरोध Compile करें

Operator के शब्दों को actionable contract में बदलें, अपना अर्थ संक्षेप में बताएँ और काम
जारी रखें। संक्षिप्त अभिव्यक्ति में पूरी spec हो सकती है। Operator को उसे engineering
 ticket में दोबारा लिखना जरूरी नहीं।

## वर्तमान task का एक parse

Current packet में directive मौजूद हो और कोई नया instruction उसे न बदले, तो उसे reuse
करें। यह skill भाषा interpretation की owner है;
[operator-intent-deduction](../operator-intent-deduction/SKILL.md) उसी directive में
अनसुलझे निर्णय का owner है। कोई भी दूसरे का पूरा workflow फिर शुरू नहीं करता।

### 1. वास्तविक शब्दों को parse करें

Requested capability, action, named surfaces, quantities, constraints और observable
finish निकालें। Unresolved references और metaphors चिह्नित करें। Repetition जोर बता
सकती है; उससे नया task नहीं बनता। Tone urgency दिखा सकता है, permission, risk tolerance,
competence या identity नहीं।

Figurative language को वास्तविक task context में समझें। “जला दो” किसी approach के लिए
हो सकता है; अकेले उससे data delete करने की authorization नहीं मिलती। Dialect की नकल
या persona गढ़े बिना साफ भाषा में उत्तर दें।

### 2. केवल कार्रवाई बदलने वाली uncertainties की grounding करें

Governing instructions के भीतर यह क्रम अपनाएँ:

1. Operator का current explicit request और corrections।
2. इस conversation में स्थापित scope और authorization।
3. Verified project facts, targets, contracts और current state।
4. [operator-essence](../operator-essence/SKILL.md) की relevant confirmed preferences
   और evidence आधारित observations।
5. Evidence कम हो तो स्पष्ट label वाला provisional inference।

Essence गायब या पुराना हो तो उसका owner एक supported insights pass करता है और
provisional या current slice लौटाता है। Nested skills वही result reuse करें; history
बार-बार न लें। Historical preferences नए instruction से ऊपर नहीं हैं। Source facts
route सीमित कर सकते हैं; goal छोटा नहीं करते।

गुणात्मक evidence preference का अर्थ और context दिखाता है। मात्रात्मक evidence अपनी
बताई population में repeated outcomes का वर्णन कर सकता है। Counts अकेले operator का
मतलब तय नहीं करते, और report की inferred tendency operator-confirmed instruction नहीं।

### 3. Directive तैयार करें

दूसरा plan बनाए बिना existing task packet में ये fields रखें:

| Field | आवश्यक content |
| --- | --- |
| Intended capability | Operator क्या अस्तित्व में चाहता है या क्या जानना चाहता है। |
| Current boundary | Verified state और उपलब्ध capabilities आज क्या करने देती हैं। |
| Route now | मौजूदा authorization में अगली उपयोगी कार्रवाई। |
| Route later | पूरी intended capability के लिए शेष dependencies। |
| Task contract | Mode, target, boundaries, requested finish और acceptance evidence। |
| Uncertainty | महत्वपूर्ण unknowns और उन्हें सुलझा सकने वाला evidence। |

External dependency current route सीमित करे तो पूरी intended capability सामने रखें।
Review findings देता है; वह चुपचाप repair नहीं बन जाता।

## अर्थ बताएँ, फिर काम करें

Interpretation मायने रखे तो एक सीधा वाक्य दें:

> अर्थ: मौजूदा integration अपडेट करना है, उसका public interface बचाना है और release से पहले actual consumer सत्यापित करना है।

जरूरत पर कमजोर inference label करें। Evidence से उचित reversible work जारी रखें।
Factual uncertainty inspection या focused experiment से सुलझाएँ। जरूरी authorization
गायब हो या operator का असली चुनाव अनसुलझा हो, तो उपलब्ध तैयारी के बाद एक concrete
recommendation और question दें; [decision-bar](../decision-bar/SKILL.md) देखें। पुरानी
preference किसी नई consequential action की missing permission नहीं भर सकती।

Directive [Build Flow](../backs-build-flow/SKILL.md) को लौटाएँ। वास्तव में कोई निर्णय
बचा हो तभी intent deduction लें। बाद की correction existing packet और संबंधित essence
 evidence अपडेट करती है; goal चुपचाप नहीं बदलती और remaining mission budget reset नहीं करती।
