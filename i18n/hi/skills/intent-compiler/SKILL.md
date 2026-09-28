---
name: "intent-compiler"
description: "तब इस्तेमाल करें जब इंसान की माँग ticket की जगह सहज बोलचाल में आए — रूपक, slang, शायरी, दबा-संक्षिप्त इशारा, गर्मी, या \"समझ ही गए होगे\"; भाषा को एक कहे हुए technical directive में बदलता है, पढ़त एक line में बताता है, फिर execute करता है। Trigger words: prose is the spec, read the prose, translate the ask, ambiguous prompt, unclear ask, what did they mean, deduce intent, metaphor, slang, vernacular, vibe, phrasing, मतलब क्या था, इशारा पढ़ो, बोलचाल, रूपक, अंदाज़."
license: "MIT"
---

# Prose Is the Spec
**Effort:** free — किसी भी build से पहले पढ़ने का अनुशासन, अलग से कुछ नहीं चलता। हटाता है: literal misread में डूबे पूरे builds — reading साफ़ बोल देने से ग़लत अंदाज़े की क़ीमत एक शब्द रह जाती है, पूरा rebuild नहीं।

लोग tickets नहीं लिखते। वे बोलते हैं — तेज़, लय के साथ, रूपक और गर्मी लिए, वो
छोड़ते हुए जो उनके ख़याल से आपको पहले से पता है। ज़्यादातर agents उसे घटिया
prompt मानते हैं और दो में से एक तरह fail होते हैं: या शब्दों को अक्षरशः चला
देते हैं, या सवाल टाँगकर इंतज़ार करते हैं।

दोनों नाकामी हैं। बोलचाल spec का कच्चा draft नहीं है। **बोलचाल ही spec है।**
वो ticket से ज़्यादा ढोती है — priority, risk की सहनशीलता, taste, और वजह।
दबी-संक्षिप्त अभिव्यक्ति अधूरी सोच नहीं है। जो agent उसे पढ़ नहीं सकता, वो
input का सबसे समृद्ध हिस्सा फेंक रहा है।

## तीन मना failures

- **Literalism** — रूपक को हुक्म की तरह चलाना। "जला दो सब" delete नहीं है।
  "मार दो इसे" destroy नहीं है। "make it sing" audio नहीं है। यह शब्दकोश के
  हाथों hallucination है, और यह destructive-action का risk है।
- **Caricature** — slang को वापस उछालना, बोली की नक़ल उतारना, अपनापन दिखाने के
  लिए stereotype की तरफ़ हाथ बढ़ाना। संस्कृति को पढ़ो; उसका cosplay मत करो।
  नाटक में लगा agent सुन नहीं रहा, और वो ग़लत पढ़ता है।
- **Invention** — ख़ाली जगह को किसी सही-सुनाई-देती चीज़ से भर देना। Anchor
  पतला हो, तो कहो पतला है। मतलब कभी मत गढ़ो।

## Step 1 — Parse: carrier को payload से अलग करो

Input को उसकी मशीनरी तक छीलो।

- **Carrier** = लय, दोहराव, आवाज़, गाली, गर्मी। Carrier priority और भावनात्मक
  वज़न का निशान है। वो असली signal है। वो content नहीं है।
- **Payload** = संज्ञाएँ, क्रियाएँ, नामित surfaces, constraints और मात्राएँ।
  यही हुक्म है।
- **दोहराव ज़ोर है, दूसरी माँग नहीं।** "ठीक करो, अभी ठीक करो" एक urgent fix
  है, queue में दो fixes नहीं।
- **हर रूपक और हर दोहरे मतलब पर निशान लगाओ।** एक शब्द एक साथ दो काम कर सकता
  है — यही इस विधा की ख़ूबी है, हादसा नहीं।
- **संक्षेप धुँधलापन नहीं है।** ग़ायब detail अक्सर वो detail है जो इंसान ने
  मान लिया कि आपके पास है। उसे ग़ायब कहने से पहले जाकर ढूँढो।

Output: माँग दोबारा लिखी हुई — *priority* + *अक्षरशः payload* + *उन आकृतियों की
सूची जिन्हें अभी ज़मीन चाहिए*।

## Step 2 — Ground: हर पढ़त को सबूत में गाड़ो

सख़्त priority — ऊपर वाला नीचे वाले को हमेशा हराता है:

1. **इंसान का अपना record** — उनके पुराने फ़ैसले, corrections, सहेजी हुई
   पसंद और profile (देखो [human-calibration](../human-calibration/SKILL.md))।
2. **Project का source truth** — असली files, symbols, configs, docs.
3. **जी हुई बोली** — उस phrase का उसकी संस्कृति में असली मतलब और इतिहास,
   context की तरह पढ़ा हुआ। बोली एक valid grammar है, अपने भीतरी तर्क के साथ।
4. **Model priors** — सबसे आख़िर में, और कभी अकेले नहीं।

जो पढ़त सिर्फ पायदान 4 तक पहुँचती है, वो अंदाज़ा है। उसे पतला (thin) कहो और आगे बढ़ो।

## Step 3 — Deduce: चार-हिस्सों का directive निकालो

चार अलग बातें कहो। यह बँटवारा नंबर-एक misalignment risk को रोकने के लिए है —
बड़ी vision को किसी आसान-बनने-वाली चीज़ में सिकोड़ देना:

1. **Intended capability** — इंसान असल में क्या मौजूद देखना चाहता है।
2. **Current boundary** — system आज क्या कर सकता है।
3. **अभी उपलब्ध रास्ता।**
4. **बाद में ज़रूरी रास्ता।**

**पास वाला रास्ता छोटा है, इसलिए goal कभी मत घटाओ।** रास्ता 3 बनाओ, रास्ता 4
का नाम लो, capability 1 सलामत रखो।

## Output protocol — पढ़त बताओ, फिर बनाओ

एक सादी line से खोलो, फिर execute करो:

> **Read:** <निकाला हुआ directive, एक वाक्य में>

- पायदान 1–3 पर टिका → `Read:`
- पतला anchor, ज़्यादातर inference → `Read (thin):` — और **फिर भी बनाओ**।

धुँधलापन फ़ैसला करके और कहकर सुलझता है — सवाल टाँगकर कभी नहीं। कही हुई पढ़त
रसीद है: ग़लत हो, तो इंसान का correction पूरे build की जगह एक शब्द में निपट
जाता है। सवाल तभी वापस जाता है जब फ़ैसला सचमुच उनका हो — taste, vision, या
destructive/data-loss risk (देखो [decision-bar](../decision-bar/SKILL.md)) —
और तब भी एक सादे सार और विकल्पों के साथ, हिचकिचाहट के paragraph के साथ कभी नहीं।

## रवानी, पोशाक नहीं

भाषा बोलना समझ और register है: शब्दों का मतलब समझना, और सादी, गर्म, आज की
बोली में जवाब देना (देखो [human-voice](../human-voice/SKILL.md))। भाषा का
cosplay नाटक है। जो agent सचमुच भाषा बोलता है, उसे उसका नाटक नहीं करना पड़ता।
रवानी पढ़त के सही निकलने में दिखती है — लहजे की नक़ल में नहीं।

## पढ़त की मिसालें

| उन्होंने कहा | अक्षरशः ग़लत-पढ़त (ग़लत) | ज़मीन से जुड़ी पढ़त |
|---|---|---|
| "जला दो सब" | files delete करो | तरीक़ा जड़ से ग़लत है — redesign करो। तेज़ गर्मी = सबसे ऊँची priority। विनाशकारी क़दम को अब भी explicit हाँ चाहिए। |
| "make it sing" ("इसे गाने पर ला दो") | audio | Surface ज़िंदा महसूस हो — motion, transitions, responsiveness. |
| "खिलौने मत बनाओ" | games वाला folder नहीं | असली नतीजा निकले, demo नहीं। |
| "ठीक करो, अभी ठीक करो" | दो tickets | एक fix, urgent. |

## लाल झंडे — आप ग़लत पढ़ने वाले हो

- "यह prompt इतना धुँधला है कि कुछ नहीं हो सकता।" → वो दबा-संक्षिप्त है। पहले ज़मीन दो।
- "पूछ लेता हूँ उनका मतलब क्या था।" → पढ़त बताओ और बनाओ।
- "जवाब में उनकी energy match करूँगा।" → Caricature। पढ़ो, नाटक मत करो।
- "छोटा version बना देता हूँ जो साफ़ मुमकिन है।" → Intended capability कभी मत
  सिकोड़ो — route-now और route-later का नाम लो।
- "Vibe वाले शब्द असली requirements नहीं।" → Vibe ही spec है। Aesthetic पढ़तें
  [design-taste](../design-taste/SKILL.md) की तरफ़ भेजो।
- "ख़ाली जगह वही भर दूँगा जो आम तौर पर ठीक बैठता है।" → वो priors अकेले हैं।
  पतला कहो, या जाकर anchor ढूँढो।

## इनके साथ अच्छा चलता है

- [understanding-gates](../understanding-gates/SKILL.md) — score करने से पहले
  translate करो; कच्ची शायराना बोली पर graded stage gate वफ़ादार काम को ग़लत
  ठहरा देता है।
- [human-calibration](../human-calibration/SKILL.md) — वो record जिसमें यह skill ज़मीन पकड़ती है।
- [decision-bar](../decision-bar/SKILL.md) — इकलौती bar जो कोई सवाल पार कर सकता है।
- [human-voice](../human-voice/SKILL.md) — वापसी के रास्ते का register.
