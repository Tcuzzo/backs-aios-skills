---
name: fleet-ladder
description: तब इस्तेमाल करें जब किसी model को कोई काम सौंपना हो — building, grading या bounded worker job — या कोई provider down हो और fallback क्रम चाहिए; LIVE model ladder resolve करता है: probe करो कि सचमुच क्या चालू है, explicit fallback क्रम से सबसे अच्छा available चुनो, ladder ख़त्म हो तो ज़ोर से fail करो। Trigger words: fleet, ladder, dispatch, fallback, model down, provider down, which model, availability, कौन सा model, सीढ़ी, विकल्प क्रम, उपलब्धता.
license: MIT
---

# Fleet Ladder
**Effort:** light — किसी भी dispatch से पहले rung की एक cached live probe। हटाता है: मरे हुए providers को गए dispatches, और call sites पर hardcode हुए model नाम जो model के retire होते ही टूट जाते हैं।

Provider call कभी हाथ से मत गढ़ो, और call site पर model का नाम कभी hardcode मत
करो। "अभी यह काम कौन सा model करेगा?" — इस सवाल का मालिक एक resolver है — और
वो live सच से जवाब देता है, किसी config file की राय से नहीं।

## कब चलाएँ

- किसी model को KOI भी dispatch करने से पहले: build, grade, review या bounded worker job.
- जब कोई provider down हो और जानना हो कि क्या किस पर गिरता है।
- जिस पल आप code या prompt template में model का नाम टाइप करते खुद को पकड़ें।

## कदम

1. **Role घोषित करो, model नहीं।** हर job एक role माँगता है — `builder`,
   `grader`, या `worker`। Ladder roles को क्रमबद्ध model उम्मीदवारों से जोड़ता है।
   - `builder`: implement और repair करता है।
   - `grader`: स्वतंत्र review — ढाँचे से ही कभी वही model नहीं जिसने बनाया।
   - `worker`: सीमित, अच्छी तरह लिखे jobs। यहाँ सस्ते पायदान ठीक हैं।
2. **Ladder को config से पढ़ो।** एक file हर role के लिए उम्मीदवारों को explicit
   fallback क्रम में रखती है: सबसे मज़बूत पहले, नीचे आपकी local survival tail तक
   (जो भी आप अपने hardware पर चला सकें जब हर cloud provider अँधेरे में हो)।
   Model बदलना या जोड़ना हो, वो file edit करो — code कभी नहीं। शुरुआती आकार:
   [ladder.example.yaml](../../../../skills/fleet-ladder/ladder.example.yaml) — copy करो, placeholders बदलो।
3. **भरोसे से पहले live probe करो।** Config की सूची एक दावा है, सच नहीं। बासी
   entry मरे हुए models दिखाती है; ज़िंदा models छोड़ भी देती है। किसी पायदान को
   dispatch से पहले provider को probe करो — models-endpoint call या एक-token
   request, जैसे:
   `curl -s "$PROVIDER_BASE_URL/v1/models" -H "Authorization: Bearer $API_KEY"`
   (या chat endpoint पर वही आकार `"max_tokens": 1` के साथ)।
   Probe का नतीजा एक समझदार window के लिए cache करो — हर call पर re-probe करके
   providers को मत ठोको। Cache तभी refresh करो जब सचमुच ताज़ा सच चाहिए।
4. **नीचे उतरो, ज़ोर से।** सबसे अच्छे AVAILABLE पायदान पर dispatch करो। Transport
   failure पर failure को ज़ोर से report करो, फिर अगला पायदान आज़माओ। चुपचाप skip
   कभी नहीं — record में दिखना चाहिए कौन से पायदान fail हुए और क्यों।
5. **ख़ात्मा ज़ोर से fail होता है।** हर पायदान down है, तो एक साफ़ error उठाओ जो
   बताए क्या-क्या आज़माया गया। जो job dispatch नहीं हो सकता वो कभी चुपचाप कामयाब
   नहीं होता, हमेशा के लिए इंतज़ार नहीं करता, न ही किसी गढ़े हुए जवाब पर उतरता है।
6. **Provenance log करो।** हर dispatch एक log में जोड़ो: role, चुना गया model,
   छोड़े गए पायदान और वजह। बाद में आपको जवाब देना आना चाहिए: "यह काम असल में
   किसने किया?"

## सख़्त नियम — एक भी टूटा तो skill fail

- **Call site पर model का नाम नहीं।** Code role माँगता है; ladder model से जवाब
  देता है। अपने codebase में model-name literals के लिए grep करो — हर एक bug है।
- **Live probe config से ऊपर है।** इंसान कहे कि model मौजूद है और config इनकार
  करे, तो probe करो। जाँचा-और-जवाब-आया = तय; बासी सूची कुछ नहीं।
- **एक ही बदलाव के लिए builder और grader कभी एक ही model पर नहीं उतरते।**
  Ladder उन्हें एक model पर गिरा रहा हो, तो grader अगला स्वतंत्र पायदान लेता है —
  या job ज़ोर से fail होता है।
- **सीमित probing.** Probes सस्ते, cached और backoff-वाले हैं। मरे provider पर
  कसा retry loop मना है।
- **चुपचाप fallback नहीं।** Ladder का हर नीचे-क़दम log और report में दिखता है।
  ख़ामोशी से degrade होना ही वो तरीक़ा है जिससे टूटा रास्ता बिना किसी की नज़र में
  आए मर जाता है।

## इनके साथ अच्छा चलता है

- [model-fusion](../model-fusion/SKILL.md) — panel और judge अपने models इसी ladder से resolve करते हैं।
- [blind-tribunal](../blind-tribunal/SKILL.md) — jurors अलग families से आते हैं; ladder ज़िंदा वाले चुनता है।
- [bounded-loops](../bounded-loops/SKILL.md) — probe की रफ़्तार, backoff और kill-switches.
