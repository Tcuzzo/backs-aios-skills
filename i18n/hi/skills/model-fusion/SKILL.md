---
name: "model-fusion"
description: "जब स्वतंत्र रूप से बनाए गए approaches की तुलना task में मदद करे और शेष budget में संभव हो, या operator panel माँगे, तब उपयोग करें। Model-agnostic drafts, selection या synthesis और verification; वही configured model अलग isolated sessions में कई roles संभाल सकता है।"
license: "MIT"
---

# Model Fusion
**Effort:** heavy — स्वतंत्र drafts, एक evaluator और वैकल्पिक writer; panel तभी लें जब task में उसका लाभ शेष budget के भीतर खर्च को उचित ठहराए।

Panel वैकल्पिक है। अलग executions एक ही task के drafts बनाती हैं; इन executions
में शामिल न रहा evaluator candidates चुनता या मिलाता है। परिणाम original request
से verify होता है। वही सक्षम configured model अलग, isolated sessions में drafter,
judge और writer बन सकता है। Model या provider बदलना आवश्यक नहीं है। Evaluator
authors की बातचीत या working context inherit नहीं करता।

## कब चलाएँ

- जब approaches की तुलना कोई स्पष्ट uncertainty दूर कर सके और उनकी जाँच
  mission के शेष budget में हो सके।
- जब operator panel माँगे; उपलब्ध roles और सीमाएँ बताएँ। केवल बड़ा task होने
  से panel अनिवार्य नहीं हो जाता।
- साधारण बदलावों में सीधा implementation और उचित verification करें।

[bounded-loops](../bounded-loops/SKILL.md) लागू करें। Drafts, judge, writer और
repair rounds मौजूदा mission की deadline, शेष attempts और resources साझा करते
हैं। नए roles या sessions इन सीमाओं को reset नहीं करते। Host समर्थन दे तो स्वतंत्र
drafts parallel चलाएँ, अन्यथा उन्हीं सीमाओं में क्रम से चलाएँ। Host में न मिलने
वाली session isolation का दावा न करें।

## तीन stages

### 1. Panel — स्वतंत्र drafts

1. वही task और वही context packet हर isolated drafting session को दो।
2. हर drafter अकेला काम करता है। कोई drafter दूसरे का काम नहीं देखता।
3. जो drafter error दे, time out हो, या ख़ाली लौटे — वह log होकर drop होता
   है। वह round को कभी नहीं मारता। Drop को ज़ोर से log करो — कभी निगलो मत।
4. हर non-empty candidate इकट्ठा करो।

### 2. Judge — बाहर वाला चुनता और merge करता है

1. Judge से पहले हर candidate पर एक सस्ता mechanical gate चलाओ: क्या यह साफ़
   apply होता है? Parse होता है? Probe किसी throwaway copy पर चलाओ, live
   tree पर कभी नहीं। जो candidates gate fail करें, वे judge के देखने से पहले
   बाहर।
2. Judge की दो शक्लें — config के हिसाब से एक चुनो:
   - **Synthesis:** judge हर candidate की छानबीन करता है (ताक़तें, defects,
     टकराव), फिर अलग writing execution उस विश्लेषण से अंतिम उत्तर बनाती है।
     Roles और sessions अलग रखें; वही सक्षम configured model दोनों संभाल सकता है।
   - **Selection:** judge gate पार करने वालों में से अकेला सबसे अच्छा
     candidate चुनता है। सस्ता। तब लो जब merge से कुछ नहीं जुड़ता।
3. Judge या writer उपलब्ध न हो, तो उन्हीं candidates पर selection पर उतरो —
   पर ज़ोर से (LOUDLY)। Panel को चुपचाप कभी बर्बाद मत करो; synthesis होने का
   नाटक कभी मत करो।
4. कोई candidate gate से न बचे, तो सबसे अच्छा error prompt में जोड़कर panel
   दोबारा चलाओ — bounded, ज़्यादा से ज़्यादा 2 repair rounds। ख़त्म होने पर
   पूरी error list के साथ failure लौटाओ। ख़ाली या no-op नतीजे को success
   बनाकर कभी मत लौटाओ।

### 3. Validate — जीतने वाले को intent से मिलाओ

1. Original माँग दोबारा पढ़ो। क्या जीतने वाला वही करता है जो माँगा गया —
   पूरा का पूरा, और कुछ भी ऐसा नहीं जो माँगा नहीं गया?
2. Semantic सहीपन देखो, आस-पास के code से style का मेल देखो, और यह कि वह अब
   भी साफ़ apply होता है।
3. कम confidence एक escalation flag बनकर सतह पर आता है, छिपता नहीं। फिर उसे
   आम तरीक़े से साबित करो: पहले failing test, फिर green, फिर live behavior।
   जो merged draft कभी चला ही नहीं, वह अंदाज़ा है।

## Ladder

- Panel का आकार और roles आवश्यक capability, वास्तविक availability, मौजूदा
  config और शेष budget से चुनें। Fixed models, provider preference या अनिवार्य
  model diversity नहीं। Config की कमी स्पष्ट दर्ज करें।
- Config का format, roles-not-names, और live-probe resolution — सब
  [fleet-ladder](../fleet-ladder/SKILL.md) के हैं।

## Hard rules — एक भी तोड़ा तो skill fail

- **Builder कभी judge नहीं।** Evaluating execution ने कोई candidate नहीं
  लिखा और authors की बातचीत या working context inherit नहीं किया। आख़िरी
  grader एक fresh, author-disjoint session में काम करता है।
- **किसी call site पर hardcoded model names नहीं।** Code में roles, config
  में models।
- **कोई silent degradation नहीं।** Drop हुए drafters, judge का fallback, gate
  की failures, और exhaustion — सब ज़ोर से। जो नतीजा grade नहीं हो सकता, वह
  default से कभी pass नहीं होता।
- **Bounded repair।** Reruns की सख़्त cap है और वे mission का शेष budget
  खर्च करते हैं; जो सीमा पहले पहुँचे, वहीं रुकें। Exhaustion पर स्पष्ट checkpoint
  दें, infinite loop नहीं।
- **अकेले green tests का मतलब done नहीं।** जीतने वाला live behavior पर साबित
  होता है।

## इनके साथ अच्छा चलता है

- [fleet-ladder](../fleet-ladder/SKILL.md) — panel चलने से पहले पता करो कौन-से models ज़िंदा हैं।
- [blind-tribunal](../blind-tribunal/SKILL.md) — primary grader मर जाए तो fail-closed grading अदालत।
- [red-first](../red-first/SKILL.md) — वह failing test जिसे जीतने वाले draft को green करना है।
- [blind-eval](../blind-eval/SKILL.md) — जब कोई test फ़ैसला न कर सके, keep-or-revert taste gate।
