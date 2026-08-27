---
name: model-fusion
description: तब लगाओ जब एक model का जवाब भरोसे लायक़ न हो — कोई कड़ा build, fix या design जहाँ तुम चाहते हो कि कई models मुक़ाबला करें और एक independent judge चुने। Panel parallel में drafts बनाता है, judge जीतने वाला merge करता है, नतीजा original intent से मिलाकर validate होता है। Trigger words: fusion, panel, judge, multi-model, ensemble, draft and merge, builder not grader, कई models से बनवाओ, panel बैठाओ, judge चुने, मुक़ाबला कराओ.
license: MIT
---

# Model Fusion
**Effort:** heavy — parallel में draft करता पूरा panel, साथ में एक स्वतंत्र judge (और वैकल्पिक writer); इसे कठिन builds और ship होने वाले fixes पर खर्च करें, one-line बदलावों पर कभी नहीं। हटाता है: पूरा बदलाव एक अकेले model के draft पर दाँव लगाना, और वह rework जब वही draft ग़लत निकलता है।

कई आज़ाद आवाज़ें एक आवाज़ से बेहतर होती हैं। Models का एक panel वही task
parallel में draft करता है। एक judge — ऐसा model जिसने कोई draft नहीं लिखा —
सबसे अच्छा चुनता या merge करता है। फिर जीतने वाले को उससे मिलाया जाता है जो
असल में माँगा गया था।

## कब चलाएँ

- कोई भी बड़ा build, fix या uplift जहाँ रफ़्तार से ज़्यादा quality मायने रखे।
- जब तुम्हें independent graders की एक तय जोड़ी चाहिए, एक model पर अंधा
  भरोसा नहीं।
- मामूली one-line बदलावों के लिए नहीं। सीधा बदलाव करो और verify करो।

## तीन stages

### 1. Panel — parallel में drafts

1. वही task, वही context, हर panel model को एक साथ भेजो।
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
     टकराव), फिर एक अलग writer model उस छानबीन से आख़िरी जवाब गढ़ता है।
     Writer और judge अलग roles हैं; हो सके तो अलग models रखो।
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

- Fusion की rung की शक्ल: नीचे सस्ते models का चौड़ा panel, ऊपर चढ़ते हुए
  कसे panels और कसे output budgets — ग़लत configure हुई rung load होते ही
  ज़ोर से fail होती है।
- Config का format, roles-not-names, और live-probe resolution — सब
  [fleet-ladder](../fleet-ladder/SKILL.md) के हैं।

## Hard rules — एक भी तोड़ा तो skill fail

- **Builder कभी judge नहीं।** Judge ने कोई candidate नहीं लिखा। आख़िरी
  grader उससे अलग model है (बेहतर हो तो अलग family) जिसने जीतने वाला बनाया।
- **किसी call site पर hardcoded model names नहीं।** Code में roles, config
  में models।
- **कोई silent degradation नहीं।** Drop हुए drafters, judge का fallback, gate
  की failures, और exhaustion — सब ज़ोर से। जो नतीजा grade नहीं हो सकता, वह
  default से कभी pass नहीं होता।
- **Bounded repair।** Panel के reruns की सख़्त cap है। Exhaustion एक ज़ोरदार
  failure है, infinite loop नहीं।
- **अकेले green tests का मतलब done नहीं।** जीतने वाला live behavior पर साबित
  होता है।

## इनके साथ अच्छा चलता है

- [fleet-ladder](../fleet-ladder/SKILL.md) — panel चलने से पहले पता करो कौन-से models ज़िंदा हैं।
- [blind-tribunal](../blind-tribunal/SKILL.md) — primary grader मर जाए तो fail-closed grading अदालत।
- [red-first](../red-first/SKILL.md) — वह failing test जिसे जीतने वाले draft को green करना है।
- [blind-eval](../blind-eval/SKILL.md) — जब कोई test फ़ैसला न कर सके, keep-or-revert taste gate।
