---
name: human-calibration
description: तब इस्तेमाल करें जब कोई build, design या नतीजों वाला UX फ़ैसला शुरू हो और पहले उस इंसान से मिलना ज़रूरी हो जिसके लिए वो है — यह इंसान कैसे सोचता, फ़ैसले करता और किस लहजे में बात चाहता है, उसका session profile load या तैयार करता है, फिर पूरा build उसी से चलाता है। Trigger words: yoke, know your human, human profile, session profile, grounding ladder, interaction model, intent, अपने इंसान को जानो, इंसानी प्रोफ़ाइल, इरादा समझो.
license: MIT
---

# Know Your Human

जो build अपने इंसान को ग़लत पढ़ता है, वो पहली line लिखने से पहले ही ग़लत है।
यह skill अंदाज़ों की जगह उस इंसान का चालू model रखती है जिसकी वो सेवा करती है:
सोचने का ढंग, taste, लहजा, और कहाँ उनकी बात पर सीधे भरोसा है। इंसान से वहीं
मिलो जहाँ वो है — उसे कभी system के स्तर तक चढ़ने पर मजबूर मत करो।

## कब चलाएँ

किसी भी build, design, uplift या नतीजों वाले UX फ़ैसले की शुरुआत में। Chat की सजावट नहीं।

## बहाव: profile या सवाल

1. **इंसान को पहचानो।** Project में `.agent/profiles/<human>.md` देखो, फिर
   agent की home config dir (जैसे `~/.claude/profiles/<human>.md`) में
   all-projects profile। वहाँ validated profile मिले, तो load करके लागू करो।
   जिसके पास पहले से profile है, उससे दोबारा सवाल-जवाब कभी नहीं।
2. **Profile नहीं? Question protocol चलाओ** (नीचे)। ज़्यादा से ज़्यादा 7 आराम के
   सवाल, और जहाँ किसी जवाब से कोई धागा खुले वहाँ अधिकतम 3 follow-ups। हमेशा
   optional — जो इंसान किसी सवाल को टाल दे, उसकी profile देखे गए बर्ताव से बनती
   है। काम पर कभी gate नहीं।
3. **Session profile synthesize करो** (template नीचे)। हर field के साथ एक
   `source` और एक `status`। जिस section का सबूत नहीं, वो ख़ाली रहता है: ख़ाली
   ईमानदार है, अंदाज़ा एक छिपा inference।
4. **Goal का मिलान करो।** Build का इरादा profile से छानकर, इंसान के अपने लहजे
   में दोबारा कहो — एक सादा paragraph, spec नहीं। वे confirm या correct करते
   हैं। उनका correction आख़िरी है।
5. **खुद को reprompt करो।** Execute करने से पहले अपना working prompt profile से
   फिर लिखो: उनका मतलब क्या था, किन बातों पर भरोसा करना है, किन्हें एक हल्की
   जाँच चाहिए, क्या उन्हें ज़िंदा लगेगा और क्या बेइज़्ज़ती जैसा।
6. **Profile को राह दिखाते हाथ की तरह लेकर बनाओ** — design, engineering, UX और
   taste के फ़ैसले सब उसी से मुड़ते हैं।
7. **सीखो।** देखे गए चुनाव, ठुकराव और corrections profile को update करते हैं —
   वापस `.agent/profiles/<human>.md` में सहेजे जाते हैं (या all-projects profile
   के लिए home config dir में)। Correction फ़ौरन जीतता है।

## Grounding ladder (priority क्रम, अटल)

```
HUMAN CORRECTION
  > OBSERVED REPEATED BEHAVIOR
  > DECLARED ARCHETYPE   (वे खुद को जो कहते हैं)
  > CULTURAL PATTERN     (वो घोषित archetype आम तौर पर जो जताता है)
  > MODEL GUESS
```

कोई नीचे का पायदान ऊपर वाले को कभी नहीं पलटता। Archetypes और cultural patterns
राह दिखाने का context हैं, डिब्बा कभी नहीं — देखा गया बर्ताव और correction उनसे
ऊपर हैं।

## Question protocol

Design के नियम: जवाब देने के लिए कोई डिग्री नहीं चाहिए। आराम के true/false और
either/or। एक बार में एक, goal की बातचीत में छिड़के हुए — कभी list की तरह दागे
नहीं, कभी score नहीं, कभी दोहराए नहीं। इंसान के अपने शब्द दर्ज करो; वे जवाब
जितने ही अहम हैं।

7 core सवाल (हर एक दो या ज़्यादा axes एक साथ पढ़ता है):
1. नया gadget: पहले पढ़ोगे कैसे चलता है, या सीधे बटन दबाने लगोगे?
   → processing style, risk से आराम।
2. True/false: बदसूरत bugs धीमे करने से ज़्यादा चुभते हैं। → taste priority (aesthetic बनाम mechanical)।
3. दोस्त लेट है: छोटा text, या पूरे क़िस्से वाली call? → लहजा (compressed बनाम narrative)।
4. Treehouse बना रहे हो: बना-बनाया घर दिखता है, या पहला तख़्ता? → whole-picture बनाम step सोच।
5. True/false: बेतुके नियम भी माने जाने चाहिएँ। → frame स्वीकारना बनाम चुनौती देना।
6. तीन अच्छे विकल्प, या एक मज़बूत सिफ़ारिश जिसे veto कर सको?
   → authority की पसंद — सीधे तय करता है फ़ैसले कैसे पेश होंगे।
7. उनके काम की आलोचना होती है: बचाव, सुधार, या पूछते हो तुम क्या करते?
   → correction style — तय करता है कड़वी findings कैसे दी जाएँगी।

Follow-ups (अधिकतम 3, सिर्फ जहाँ core जवाब धागा खोले): gut पर हर जगह भरोसा या
सिर्फ जहाँ वे कमाल हैं (trust map); "good enough काफ़ी है?" (shipping का
झुकाव); बाद-में-बदलने की आज़ादी बनाम आज-चलता-है का यक़ीन (reversibility taste);
किसी और के edit के बाद भी उनका ही है क्या (ownership); "लोग तुम्हारे काम करने के
तरीक़े में क्या ग़लत समझते हैं?" (identity anchor, उनके शब्द)।

## Trust का नियम

Profile नक्शा है कि इस इंसान की परख कहाँ मज़बूत है और कहाँ कमज़ोर।
- **मज़बूत इलाक़ा + यक़ीन से कही बात → भरोसा करो।** दोबारा साबित करना नहीं,
  शक नहीं, उन्हें basics वापस समझाना नहीं।
- **कमज़ोर इलाक़ा + धुँधली बात → एक हल्की जाँच।** एक आराम का सवाल जो धुँध साफ़
  करे, या अपनी पढ़त एक-शब्द की confirm के लिए रख दो। मुँह पर चुनौती कभी नहीं;
  चुपचाप अपना plan बदलकर रखना भी कभी नहीं।
- **Profile से कभी वो सीमा मत खींचो जो इंसान आज़मा सकता है।** वो tune करती है
  आप KAISE सुनते हो, कभी यह नहीं कि आप मानोगे या नहीं।

## Session profile template (compact)

```markdown
# SESSION PROFILE — <human>
## Identity anchors   # value + source (declared|observed|cultural|guess) + status (confirmed|working|needs-validation|rejected)
## Working pattern    # एक paragraph: ये anchors IS इंसान में कैसे जुड़ते हैं
## Steering traits    # "likely to: <behavior>" → "so I: <concrete agent rule>"
## Trust map          # मज़बूत इलाक़े (सीधा भरोसा) / कमज़ोर इलाक़े (एक हल्की जाँच)
## Core tension       # both/and ज़रूरतें जो विरोधाभासी दिखती हैं पर requirements हैं
## Misalignment risk  # सबसे संभावित ग़लत-पढ़त, मनाही के रूप में लिखी
## Ledger             # date, ladder rung, change, evidence
```

Session profile session तक सीमित है: नए session में वो data है, सच नहीं, जब तक
इंसान उसे फिर से confirm न करे या बर्ताव उसे दोबारा कमा न ले। Profile इंसान की
संपत्ति है: माँगने पर दिखाओ, जिस पल वे ग़लत कहें उसी पल सुधारो, और किसी ऐसे
inference पर कभी मत चलो जो वे देख नहीं सकते — वो एक छिपा gate है।

## सख़्त नियम (कोई एक टूटा तो skill fail)

- जिस इंसान के पास validated profile है, उससे दोबारा सवाल-जवाब।
- सवालों को test जैसा महसूस कराना, या उन्हें अनिवार्य बनाना।
- अंदाज़े वाली field को confirmed की पोशाक पहनाना।
- नीचे का ladder-पायदान ऊपर वाले को पलटना।
- Profile से यह सीमित करना कि इंसान को क्या आज़माने की इजाज़त है।
- एक रास्ता अधूरा है इसलिए goal घटा देना। अलग-अलग रखो: intended capability →
  current boundary → अभी उपलब्ध रास्ता → बाद में चाहिए रास्ता।

## इनके साथ अच्छा चलता है

- [human-voice](../human-voice/SKILL.md) — profile बता दे वे कैसे सुनते हैं, तो जवाब देने का register.
- [decision-bar](../decision-bar/SKILL.md) — कौन से फ़ैसले इंसान तक पहुँचते हैं; profile तय करती है वे कैसे पहुँचें।
- [intent-compiler](../intent-compiler/SKILL.md) — इंसान का prompt ही spec है; profile बताती है उनका मतलब क्या था।
- [model-fusion](../model-fusion/SKILL.md) — profile का panel-फिर-compress संश्लेषण।
