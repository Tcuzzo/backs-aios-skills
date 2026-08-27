---
name: bounded-loops
description: तब इस्तेमाल करें जब कोई भी ऐसा loop शुरू होने वाला हो जो retry, poll, iterate या external API call कर सकता है — agent loops, repair loops, schedulers, watchers; पहले budget की छतें घोषित करता है, budget ख़त्म होने पर checkpoint करता है, और hammering को ढाँचे से ही नामुमकिन बनाता है। Trigger words: bounded loop, budget, ceiling, retry, backoff, rate limit, throttle, kill-switch, checkpoint, runaway, infinite loop, spin, budget exhaustion, सीमित loop, बजट, छत, अनंत loop, बेलगाम.
license: MIT
---

# Bounded Loops
**Effort:** free — loop शुरू होने से पहले घोषित छतें (ceilings) और checkpoints; लागत सीधे घटाता है। हटाता है: बेलगाम loop का खर्च — जला हुआ quota, 429 से block हुए routes, और वह progress जिसे crash मिटा देता है।

बेलगाम loop सबसे महँगा bug है जो कोई agent ship कर सकता है। वो budget जलाता है,
providers को तब तक ठोकता है जब तक वे आपको block न कर दें, और अपनी नाकामी अपने ही
चक्कर में छिपा लेता है। हर loop को एक छत, एक checkpoint, और ज़ोर से मरने का एक
रास्ता मिलता है — शुरू होने से पहले।

## कब चलाएँ

कोई भी loop शुरू करने से पहले: repair loop, retry wrapper, poller, scheduler,
कई-step का autonomous run — कुछ भी जो कोई call दोबारा भेज सकता है या कोई step
दोबारा आज़मा सकता है।

## कदम

1. **पहले budget घोषित करो।** Tokens, cost, wall time, और max attempts — पहली
   iteration से पहले लिखकर। जिस loop का budget घोषित नहीं, वो परिभाषा से ही
   unbounded है और शुरू ही नहीं होता।
2. **अंदरूनी rounds पर सीमा लगाओ।** एक inner episode (एक समस्या पर एक LLM/tool
   चक्र) को एक छोटी, तय round-छत मिलती है (क़रीब 4)। छत episode को बाँधती है,
   mission को नहीं — अधूरा काम ऊपर जाता है, घिसता नहीं।
3. **हर iteration पर checkpoint करो।** टिकाऊ state disk पर — run manifest,
   evidence log, मौजूदा step — chat memory कभी नहीं। कोई भी (एक ताज़ा session भी)
   आख़िरी checkpoint से resume कर सके।
4. **Budget ख़त्म: checkpoint, फिर escalate।** Checkpoint बाहरी loop या अपने
   human को सौंपो — क्या हुआ, क्या बचा, और blocker क्या है। Budget के पार चुपचाप
   कभी मत बढ़ो। चुपचाप रुको भी मत — budget का ख़त्म होना ज़ोर से होता है।
5. **हर external API की इज़्ज़त करो।** पहली call से पहले provider की rate limit
   और quota जानो; अनजान हो तो उसे सख़्त मानो — एक call, लंबा फ़ासला — जब तक नाप
   न लो। हर call throttle करो, responses cache करके reuse करो, और per-window की
   एक सख़्त छत रखो।
6. **धक्के पर exponential backoff.** 429 या 503 का मतलब है रुको, फिर और देर रुको।
   एक ही endpoint पर फ़ौरन retry शून्य। एक endpoint पर कसी हुई retry ऐसे ही किसी
   चालू रास्ते की मौत बनती है: वो quota जलाती है और आपका पूरा egress address
   block करवा सकती है।
7. **एक ज़ोरदार, सीमित kill-switch साथ रखो।** जो भी loop call दोबारा भेज सकता है,
   उसके पास max attempt count है; वो लगते ही loop सबूत के साथ ZOR से रुकता है —
   कभी अनंत या ख़ामोश चक्कर नहीं।
8. **रुकना और queue करना सिर्फ safe points पर।** Stop का मतलब checkpoint-फिर-cancel।
   नया काम अगले safe point (steps के बीच की state सीमा) के लिए queue होता है —
   step के बीच में कभी नहीं घुसाया जाता। एक loop instance, एक writer, atomic
   state writes.

## सख़्त नियम (क्या इस skill को fail करता है)

- ऐसा loop जो बिना घोषित token / cost / time / attempt budget के शुरू हो।
- ख़त्म हो चुके budget के पार बढ़ना — चुपचाप या खुलेआम — बिना escalate किए।
- उसी endpoint पर फ़ौरन retry, या backoff के बिना कोई भी retry रास्ता।
- बिना attempt cap का retry loop, या ऐसी cap जो लगने पर चुपचाप fail हो।
- Progress की state सिर्फ conversation memory में — एक crash पूरा run मिटा देता है।
- दो loop instances एक ही state लिख रहे हों, या non-atomic state writes.
- Loop से निकलने के लिए उसके अपने exit checks को कमज़ोर करना — bar गिराकर, data
  मिटाकर या errors निगलकर बना green एक fake green है, exit नहीं।

## इनके साथ अच्छा चलता है

- [optimus](../optimus/SKILL.md) — किसी भी loop के शुरू होने से पहले floor load करो।
- [repair-loop](../repair-loop/SKILL.md) — इन छतों का सबसे बड़ा उपभोक्ता।
- [fleet-ladder](../fleet-ladder/SKILL.md) — models के बीच सीमित fallback, एक को ठोकना नहीं।
- [session-handoff](../session-handoff/SKILL.md) — checkpoint escalate होकर जिसमें बदलता है।
