---
name: wayfinder
description: तब लगाओ जब रास्ता खो गया हो, आगे का क़दम धुँधला हो, या तय करना हो कि अगला काम क्या हो। सवाल इंसान पर टिकाने की जगह मंज़िल तक का decision map बनाता है। Trigger words: wayfinder, the path, chart the route, map the work, what next, lost, fog of war, decision map, frontier, रास्ता बनाओ, नक्शा बनाओ, अब आगे क्या, रास्ता खो गया.
license: MIT
---

# Wayfinder
**Effort:** free — शुद्ध नक़्शा-खींचने का अनुशासन: disk पर पहले से मौजूद सबूतों से बना एक decision map, कोई अतिरिक्त model call नहीं। हटाता है: इंसान पर park किए वे सवाल जिनका जवाब सबूत दे सकते थे, और वह build काम जो उससे आगे के फ़ैसले होने से पहले ही शुरू कर दिया गया।

रास्ता पता न हो, तो सस्ती चाल है रुककर इंसान से वही सवाल पूछ लेना जिसका जवाब
देने के लिए उन्होंने तुम्हें रखा है। Wayfinder उसकी जगह रास्ता chart करता है:
एक decision map बनाओ, unknowns को सबूत से सुलझाओ, और ऊपर सिर्फ़ वे फ़ैसले
भेजो जो सच में इंसान के हैं।

## कब चलाएँ

- रास्ता खो गया है, या अगला क़दम धुँधला है।
- कोई बड़ी मुहिम बनने से पहले टुकड़ों में बँटनी है।
- "आप क्या करवाना चाहते हैं?" पूछने की खिंचावट महसूस हो रही है।

## क़दम

1. **मंज़िल का नाम लो।** Tracker में एक named goal, साथ में एक close
   predicate: कैसे पता चलेगा कि हो गया। मंज़िल ही scope को जड़ देती है।
2. **जो दिखता है, chart करो।** Frontier पर tickets बनाओ — वे फ़ैसले जो अभी
   सुलझ सकते हैं। हर ticket एक **decision** सुलझाता है, build के काम का
   टुकड़ा नहीं।
3. **बाक़ी को धुंध (fog) में रहने दो।** जो फ़ैसले आते महसूस होते हैं पर अभी
   पकड़ में नहीं आते, वे **Not yet specified** section में जाते हैं: शक वाला
   सवाल, दोबारा देखने की जगह। धुंध को पहले से ticket-size टुकड़ों में मत
   काटो — वह ticket से मोटी होती है, और एक टुकड़ा कई tickets बन सकता है, या
   एक भी नहीं।
4. **बाहर का काम बोलकर बाहर करो।** मंज़िल के पार का काम धुंध नहीं है — वह
   **Out of scope** section में जाता है और कभी graduate नहीं होता। कोई चालू
   ticket मंज़िल के पार निकले, तो उसे बंद करो और Out of scope में एक line
   छोड़ो।
5. **हर ticket को type दो** (नीचे Ticket types देखो)।
6. **एक decision सबूत से सुलझाओ।** Code पढ़ो, docs पढ़ो, record पढ़ो —
   deterministic सबूत ticket को बिना अंदाज़े के बंद करता है। Ticket सुलझते ही
   उसके आगे की धुंध छँटती है: जो अब specify हो सकता है, उसे नए tickets में
   graduate करो, एक-एक करके।
7. **रास्ता साफ़ हो तो सौंप दो।** नक्शा तब पूरा है जब कोई फ़ैसला बचा नहीं —
   बस कोई जाकर काम कर दे। "ख़ुद ही कर डालूँ" वाली खिंचावट इस बात का signal
   है कि तुम नक्शे के किनारे पहुँच गए हो।

## धुंध या ticket?

कसौटी यह है कि क्या तुम सवाल को अभी **ठीक-ठीक** बोल सकते हो — यह नहीं कि
जवाब अभी दे सकते हो। सवाल पैना है तो ticket, चाहे blocked ही हो। उतना पैना
बोल नहीं सकते, तो not-yet-specified।

## Ticket types

हर ticket या तो **human-in-loop** है (इंसान के साथ live होता है) या
**agent-alone**। Human-in-loop ticket सिर्फ़ live आदान-प्रदान से सुलझता है —
agent इंसान की तरफ़ से कभी नहीं बोलता। जो agent अपने ही grilling सवालों के
जवाब ख़ुद दे रहा है, उसने यह तोड़ दिया।

- **Research** (agent-alone) — background research agent इसे सुलझाता है;
  findings एक scratch branch पर उतरती हैं, ticket से pointer के साथ। देखो
  [live-research](../live-research/SKILL.md)।
- **Prototype** (human-in-loop) — एक सस्ते, कच्चे artifact से fidelity
  बढ़ाओ जिस पर इंसान react कर सके।
- **Grilling** (human-in-loop) — वह बातचीत जो फ़ैसला बाहर खींचती है। Default
  type।
- **Task** (कोई भी) — वह हाथ का काम जो फ़ैसले से पहले होना ही है: किसी
  service पर sign up, access provision, data move। अकेला type जो फ़ैसला
  नहीं, *काम* करता है; अपनी जगह इसलिए कमाता है कि किसी decision को unblock
  करता है।

## Hard rules

- **इंसान पर कभी ऐसा सवाल मत टिकाओ** जिसका जवाब सबूत, code या standing rules
  दे सकते हैं। ऊपर सिर्फ़ पसंद, vision और destructive-risk के फ़ैसले जाते
  हैं — देखो [decision-bar](../decision-bar/SKILL.md)।
- **काम का हवाला नाम से दो, नंगी id से कभी नहीं।** #42, #43, #44 की दीवार
  पढ़ी नहीं जाती; नाम एक नज़र में पढ़ जाते हैं। Id या link नाम के अंदर सवार
  रहता है — उसकी जगह कभी नहीं लेता।
- **एक session, एक decision।** हर session में ज़्यादा से ज़्यादा एक ticket
  सुलझाओ, research tickets छोड़कर। Charting अपने आप में एक session का काम
  है; वह हाथ से कुछ नहीं सुलझाती।
- **Plan करो, करो मत।** नक्शा decisions पैदा करता है, deliverables नहीं।
- **जब माँग ही धुंध हो** — मंज़िल इसलिए धुँधली है कि request गद्य या metaphor
  बनकर आई — तो पहले request को [intent-compiler](../intent-compiler/SKILL.md)
  से पढ़ो, फिर उससे chart करो जो वह असल में कहती है।

## इनके साथ अच्छा चलता है

- [live-research](../live-research/SKILL.md) — agent-alone research tickets इसी से सुलझते हैं।
- [decision-bar](../decision-bar/SKILL.md) — कौन-से फ़ैसले सच में इंसान तक पहुँचते हैं।
- [human-voice](../human-voice/SKILL.md) — नक्शा इंसान को कैसा पढ़ता है।

> Scaffold credit: Matt Pocock, wayfinder (mattpocock/skills, MIT). यहाँ का
> composition और hard rules BACKS AIOS के हैं।
