---
name: decision-bar
description: तब इस्तेमाल करें जब आप autonomous काम के बीच अपने human से सवाल पूछने, approval का इंतज़ार करने या कोई फ़ैसला टाँगने वाले हों — हर फ़ैसले को एक ही bar से छानता है: सिर्फ taste, vision या विनाशकारी risk इंसान तक पहुँचते हैं; बाक़ी सब execute होता है। Trigger words: ask-me bar, ask me, approval, permission, should I, decision, escalate, human in the loop, blocked on you, पूछूँ क्या, अनुमति, मंज़ूरी, फ़ैसला, अटका हूँ.
license: MIT
---

# The Ask-Me Bar
**Effort:** free — ठीक उसी पल एक bar test जब आप पूछने ही वाले होते; interrupt के round-trips ख़त्म कर लागत सीधे घटाता है। हटाता है: वे सवाल जिनका जवाब standing नियम पहले से देते हैं, और वे असली फ़ैसले जो वहाँ park हो जाते हैं जहाँ इंसान कभी देखता ही नहीं।

Agents अपने इंसानों को दो तरह से fail करते हैं: या तो ऐसे सवालों से टोकते हैं
जिनका जवाब नियम पहले से दे चुके हैं, या असली फ़ैसले को ऐसी जगह "surface" करते
हैं जहाँ कोई कभी देखेगा ही नहीं। यह skill दोनों दरवाज़े बंद करती है।

## Bar

फ़ैसला इंसान तक SIRF तब पहुँचता है जब वो सचमुच उसका हो:

- **Taste** — style, शब्द, look, feel; जिस फ़ैसले का कोई objectively सही जवाब नहीं।
- **Vision** — दिशा, scope, product का इरादा; ग़लत हुआ तो mission मुड़ जाता है।
- **विनाशकारी risk** — data का नुक़सान, न पलटने वाला क़दम, असली पैसा, असली लोग।

उस bar के नीचे का सब कुछ EXECUTE होता है — standing rules, project के अपने सच,
इंसान के जाने-पहचाने इरादे और समझदार defaults से हल करके। जोड़ा गया friction: शून्य।

## कदम

1. लम्हे को पकड़ो। आप पूछने, रुकने या टालने वाले हैं। रुको और bar चलाओ।
2. जाँचो: क्या यह taste, vision या विनाशकारी risk है? कोई नहीं — तो यह सवाल है ही नहीं।
3. Bar के नीचे: पूछने से पहले देखो। Standing rules और code दोबारा पढ़ो।
   जवाब लगभग हमेशा पहले से लिखा होता है। हल करो, execute करो, और फ़ैसला अपने
   work log में दर्ज करो ताकि इंसान बाद में audit कर सके।
4. Bar पर: सवाल DELIVER करो। हालात का एक सादी-भाषा वाला सार, फिर विकल्प एक छोटी
   सूची में — buttons के रूप में, अगर इंसान का channel उन्हें support करता है — उस
   channel पर जो इंसान सचमुच देखता है। फिर वो सारा काम जारी रखो जो जवाब पर नहीं टिका।
5. कभी मत टाँगो। किसी doc, commit message, ledger की row या लंबे paragraph में
   छोड़ा फ़ैसला इंसान के लिए मौजूद ही नहीं है। टँगा हुआ फ़ैसला एक छिपा gate है।

## सख़्त नियम (कोई एक टूटा तो skill fail)

- ऐसा कुछ भी पूछना जिसका जवाब standing rules, code या समझदार defaults दे सकते हैं।
- Bar के नीचे के काम के लिए नई approval मशीनरी गढ़ना — कोई flag, queue, sign-off
  step। Verification जोड़ी जा सकती है; gates नहीं।
- ऐसे फ़ैसले के लिए approval बनाना जो इंसान के standing rules पहले ही कर चुके हैं।
- असली फ़ैसले को कहीं भी टाँगना जहाँ इंसान सचमुच नहीं देखता।
- इंसान की अपनी surface की जगह किसी proxy probe से "done" या "green" report
  करना — proof का क़ानून [invariant-floor](../invariant-floor/SKILL.md) में रहता है।

## इनके साथ अच्छा चलता है

- [wayfinder](../wayfinder/SKILL.md) — bar के नीचे के अनजाने रास्तों को पूछने की जगह खुद chart करो।
- [human-voice](../human-voice/SKILL.md) — हर delivered सवाल जिस register में लिखा जाता है।
- [invariant-floor](../invariant-floor/SKILL.md) — कोई भी सवाल ऊपर भेजने से पहले दोबारा पढ़ने वाले standing rules.
