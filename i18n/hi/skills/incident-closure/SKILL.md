---
name: incident-closure
description: तब इस्तेमाल करें जब इंसान टूट-फूट report करे या "fix it" कहे — ख़ासकर जब सामान्य control plane (API, CLI, service) मरा पड़ा हो और आपको उसके नीचे उतरना पड़े; जवाब है एक पूरा understanding-first close — सबूत के साथ root cause, पहले failing test, green, इंसान के अपने रास्ते पर live proof, commit — कभी विकल्पों का menu वापस उनके मुँह पर नहीं। Trigger words: fix it, fix shit, full close, broken, wiped, down, it stopped working, recover, restore, ठीक करो, टूट गया, बंद पड़ा है, चलना बंद, बहाल करो, वापस लाओ.
license: MIT
---

# Full Close

जब इंसान टूट-फूट report करे या "fix it" कहे, तो ठीक एक ही सही जवाब है: एक
पूरा, understanding-first close। सबूत के साथ root cause, पहले एक failing test,
green, इंसान के अपने रास्ते पर live proof, फिर commit। कभी विकल्पों का menu
वापस उनके मुँह पर नहीं, और हर step पर confirmation का prompt भी नहीं — वे
fix it कह चुके हैं।

जहाँ भाई-बहन skills विनाशकारी कामों के लिए explicit हाँ माँगती हैं, वहाँ यह
नियम सिर्फ पलटाऊ आधे पर जीतता है: इंसान का "fix it" ही उन reversible recovery
writes के लिए standing हाँ है जो backup का निशान छोड़ती हैं; जो भी अपरिवर्तनीय
है — data का विनाश, ख़र्च, बाहर भेजना — वो अब भी
[decision-bar](../decision-bar/SKILL.md) से गुज़रता है, और bar जीतती है।

इंसान से कुछ तभी माँगो जब वो हर और जगह साबित तौर पर खो चुका हो और सिर्फ वही उसे
दे सकते हों। बाक़ी हर input, आप जाकर खुद ढूँढते हो।

## तरीक़ा

1. **सामान्य surface को probe करो — फिर उस पर भरोसा बंद।** API या CLI को एक
   बार call करो। सामान्य जवाब आए, तो यह incident-closure वाली सूरत नहीं है; आगे
   सौंप दो। 401/403 आए, connection refused, जहाँ data होना चाहिए वहाँ ख़ाली
   नतीजे, या बासी data — तो उस surface को आधिकारिक मानना बंद करो।
2. **ज़मीनी सच disk से बनाओ, API से नहीं।** टूटी service पर कभी भरोसा मत करो कि
   वो अपनी हालत खुद बताए। Data files, directory listings और modification times
   खुद पढ़ो, और API के दावों से मिलाओ। फ़र्क़ ही diagnostic संकेत है।
3. **Blast radius खँगालो।** हर top-level data directory में वे files खोजो जो
   failure window के अंदर छुई गईं (जैसे `find /data/volumes -newermt "<start>"
   ! -newermt "<end>"`)। निशाना: "क्या छुआ गया, क्या नहीं" का एक-screen जवाब।
   सँकरा radius (एक volume, एक table) यहीं सँभल जाता है। चौड़ा radius (कई
   volumes, पूरी data dir) disaster recovery है — escalate करो, जुगाड़ मत करो।
4. **बचे बनाम गए की सूची बनाओ।** हर प्रभावित asset को बाँटो:
   - disk पर सलामत — जस का तस recover करो
   - repo से दोबारा बनने लायक — git में checked-in configs और backups
   - env या credential files से दोबारा बनने लायक — tokens, passwords
   - हमेशा के लिए गया — खोई key से encrypted, सिर्फ-runtime वाली state
   सिर्फ आख़िरी टोकरी इंसान से पूछने लायक है। बाक़ी सब आप दोबारा बनाते हो।
5. **सबूत के साथ root cause, फिर red test.** क्यों टूटा, यह disk के proof के साथ
   नाम दो — अंदाज़ा नहीं। जहाँ defect code में है, fix से पहले वो failing test
   लिखो जो उसे पकड़े, और उसे green करो। देखो [red-first](../red-first/SKILL.md)
   और [root-cause-first](../root-cause-first/SKILL.md)।
6. **परतों में नीचे उतरो — इंसान की तरफ़ ऊपर कभी नहीं।** पसंदीदा रास्ता टूटा हो,
   तो एक परत नीचे उतरकर फिर आज़माओ:
   API / SDK → container के अंदर CLI → सीधे DB writes → filesystem की surgery।
   जब तक उतरने के रास्ते बचे हैं, इंसान को prompt मत करो। नीचे का हर पायदान
   पूछने से सस्ता है।
7. **मानो dependencies भी टूटी हैं।** Recovery code HTTP और JSON के लिए सिर्फ
   आपकी language की standard library इस्तेमाल करता है — third-party clients
   खुद उसी मौत का हिस्सा हो सकते हैं।
8. **Idempotent लिखो, backup के निशान के साथ।** हर disk write target के बग़ल में
   एक timestamped `.bak` copy छोड़ती है। पढ़ो, sanity-check करो, copy करो, लिखो,
   फिर जाँचो — कभी अंधा overwrite नहीं। नई key बनाने के लिए credential
   temp-swap करो, तो पहले original का backup लो और लौटने से पहले बहाल करो:
   इंसान का अपना login अनछुआ बचता है।
9. **इंसान के अपने रास्ते पर live calls से verify करो।** Step-1 वाली probe फिर
   चलाओ और पक्का करो कि आँकड़े incident-से-पहले की सूची या repo backups से मिलते
   हैं। Green DB state proof नहीं है; इंसान जिस surface को इस्तेमाल करता है उसका
   फिर चल पड़ना proof है।
10. **Commit करो और report दो।** सिर्फ fix की अपनी files commit करो। Report:
    क्या probe हुआ, blast radius, क्रम में उठाए क़दम, कितने बहाल हुए, क्या हमेशा
    के लिए गया (कुछ नहीं तो ख़ाली), और कोई step जो non-fatally fail हुआ।

## लाल झंडे — रुको और दोबारा probe करो

- "इंसान से पूछ लूँ क्यों टूटा" — नहीं; पहले disk से पता करो।
- "API कहता है यहाँ कुछ नहीं है" — टूटे API की खुद के बारे में राय सच नहीं है।
- "साफ़ reinstall कर देता हूँ" — आप recover होने लायक state फेंक रहे हो।
- "Key चली गई तो credentials बेकार हैं" — plaintext values अक्सर अब भी env या
  credential files में पड़ी होती हैं; credential दोबारा बनाओ।
- "हर step से पहले confirm करूँ?" — इंसान ने fix it कहा था; cascade चलाओ, अंत
  में report दो।

## सख़्त नियम — इनमें से कोई एक भी टूटा तो skill fail

- साफ़ हल मौजूद होते हुए इंसान के आगे विकल्प परोसना।
- बिना `.bak` निशान की विनाशकारी write।
- Cascade और सूची सूखने से पहले ही इंसान से कुछ माँग लेना।
- कोई retired subsystem "मदद में" बहाल कर देना — बंद की गई service का बंद रहना
  ही मनचाही हालत है, और उसे दोबारा चालू करना इंसान का सोचा-समझा फ़ैसला है।
- Recovery को उनके रास्ते की live probe की जगह अंदरूनी state से done बताना।
- Fix बिना commit छोड़ना (जब तक इंसान ने साफ़ न कहा हो कि commit नहीं)।

## इनके साथ अच्छा चलता है

- [repair-loop](../repair-loop/SKILL.md) — defect code में हो तो यह close जो code-fix loop चलाता है।
- [root-cause-first](../root-cause-first/SKILL.md) · [red-first](../red-first/SKILL.md)
- [decision-bar](../decision-bar/SKILL.md) — इंसान तक क्या पहुँच सकता है, और कैसे।
