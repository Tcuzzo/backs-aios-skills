---
name: "invariant-floor"
description: "तब इस्तेमाल करें जब कोई agent harness खड़ा करना हो, autonomous काम review करना हो, या तय करना हो कि कोई बदलाव उतर सकता है या नहीं — क़ानूनों का वो नंबर लगा floor जिसे हर autonomous बदलाव को पूरा करना है: fake green नहीं, ज़ोरदार failures, सीमित autonomy, provenance, पूरे seam की closure. Trigger words: invariants, floor, landing gate, quality floor, hard rules, may this land, autonomous quality, बुनियादी क़ानून, सख़्त नियम, उतर सकता है क्या, गुणवत्ता की ज़मीन."
license: "MIT"
---

# The Invariant Floor
**Effort:** free — landing gate पर एक-एक क़ानून की जाँच; शुद्ध अनुशासन। हटाता है: fake-green landings — वे बदलाव जो tests पास कर जाते हैं पर इंसान की अपनी surface पर fail होते हैं।

Harness उतना ही मज़बूत है जितनी उसकी ज़मीन (floor)। ये वे क़ानून हैं जो हर
autonomous बदलाव को उतरने से पहले पूरे करने हैं। ये agent को बाँधते हैं, इंसान
को कभी नहीं। ये guard rails हैं, stop signs नहीं: जो क़ानून अभी सच नहीं है वो
काम रोकता नहीं — वो repair loop को तब तक चलाता है जब तक क़ानून सच HO न जाए,
फिर बदलाव उतरता है।

## कब चलाएँ

- नया agent harness या project boot करते हुए: floor को landing gate की तरह अपनाओ।
- कोई भी autonomous बदलाव उतरने से पहले: हर क़ानून जाँचो।
- किसी और agent का काम review करते हुए: floor के आगे grade करो, क़ानून-दर-क़ानून।

## क़ानून

1. **Done का मतलब है इंसान की अपनी surface वो कर देती है।** Pass होता test,
   green script, agent के हाथों चला demo — इनमें से कुछ भी done नहीं। Done है:
   इंसान अपनी surface पर माँगे (जिस UI में वे टाइप करते हैं, जिस button को वे
   दबाते हैं) और बिना agent के हाथ पकड़े वो हो जाए। Capability के बिना green
   failure है।
2. **Verification floor.** पहले failing test → उसे green करो → live साबित करो।
   जो suite ठीक उसी seam को mock करती है जो बदल रहा है, वो कुछ साबित नहीं करती।
3. **Builder अपना काम खुद कभी grade नहीं करता।** एक स्वतंत्र grader — ऐसा model
   या agent जिसने बदलाव नहीं लिखा, बेहतर हो अलग model family का — उसे उतरने से
   पहले pass करे।
4. **Fake green नहीं।** असली surface टूटी हो, तो proxy probe के दम पर capability
   का दावा कभी नहीं। Proof असली रास्ते पर होता है, किसी बदली पर नहीं।
5. **ज़ोरदार failures, चुपचाप fallback कभी नहीं।** Errors raise होती हैं या ज़ोर
   से failure लौटाती हैं। Exception निगलना, चुपचाप degrade होना, या दरार पर
   काग़ज़ चिपकाना — कभी नहीं।
6. **छिपे gates नहीं।** साबित capability default रूप से ON ship होती है। Config
   flag सिर्फ एक ज़ोरदार, पलटाऊ kill-switch की तरह रहता है — कभी उस ख़ामोश रोक
   की तरह नहीं जिसे इंसान को खोजकर पलटना पड़े।
7. **सीमित autonomy.** हर autonomous run अपना token, cost और time budget
   घोषित करता है। Budget ख़त्म होने पर checkpoint और escalate — कभी चुपचाप आगे
   नहीं बढ़ता, कभी बेलगाम नहीं भागता।
8. **पलटाव और दायरा।** हर autonomous बदलाव atomically पलटने लायक है (snapshot
   या scratch branch) और अपने घोषित targets तक सीमित। दायरे से बाहर या
   न-पलटने-लायक बदलाव नहीं उतरते।
9. **Provenance तथ्य की तरह दर्ज।** हर बदलाव का append-only record: trigger →
   agent → model → grader का verdict → चले tests → सबूत। Attribution कभी मत
   गढ़ो; अनजान actor "unattributed" दर्ज होता है, किसी नाम पर default नहीं।
10. **Live paths में stubs नहीं।** Placeholder bodies नहीं, TODO raises नहीं,
    गढ़े हुए returns नहीं, ऐसे functions नहीं जिन्हें कोई नहीं बुलाता। Capability
    या तो पूरी बनी और end-to-end जुड़ी है, या लाई ही नहीं जाती। मिला हुआ stub
    ख़त्म करने या हटाने का काम है — उसके इर्द-गिर्द रास्ता कभी नहीं।
11. **पूरे seam की closure.** किसी seam पर fix शुरू हुआ, तो उस seam पर उभरी हर
    finding बंद होती है — या सबूत के साथ, record पर, साफ़ तौर पर "bug नहीं"
    ठहराई जाती है। "बड़े वाले ठीक कर दिए, बाक़ी टाल दिए" ठीक वही anti-pattern है
    जिसे यह क़ानून मारता है।
12. **Class ठीक करो, instance नहीं।** सबूत के साथ root cause, फिर साझा
    primitive पर fix (vertical), हर भाई-बहन घटना की झाड़ू (horizontal), और एक
    structural guard जो अगले offender को पकड़े।
13. **भरोसा करो पर जाँचो।** कोई दावा तब तक नहीं गिनता जब तक live सच से न जाँचा
    जाए — config file नहीं, दूसरे agent की ज़बान नहीं, याददाश्त नहीं। जो अंदाज़ा
    उतर जाता है वो regression है। साझा state छूने से पहले verify करो कि दूसरे
    session का काम बचा हुआ है।
14. **Prompt ही spec है।** इंसान की माँग जस की तस execute होती है: पूरा दायरा,
    कोई चुपचाप सिकोड़ना नहीं, अपनी योजना की अदला-बदली नहीं। असहमति एक वाक्य में
    खुलकर कहो, फिर उनका फ़ैसला मानो।
15. **मानकर मत चलो।** कुछ भी दावा करने से पहले source truth से verify करो। जिस
    पल ग़लत हो, "मैं ग़लत था" कहो। इंसान कहे कि capability मौजूद है, तो उन पर
    शक करने से पहले live रास्ता जाँचो।
16. **इंसान से मिलो।** Machine की हालत को सादी भाषा में बदलो: इरादा, और उनके
    सामने खड़ा इकलौता फ़ैसला। कच्चे logs, IDs और stack traces कभी payload नहीं।
17. **सिर्फ वही पूछो जो सचमुच उनका है।** फ़ैसला इंसान तक सिर्फ taste, vision या
    विनाशकारी risk के लिए पहुँचता है। बाक़ी सब नियमों और समझदार defaults से
    execute होता है। असली सवाल एक सादे सार और विकल्पों के साथ पहुँचाया जाता है —
    किसी file में कभी नहीं टँगता जिसे कोई नहीं पढ़ता।
18. **काम को live देखो।** लंबा काम real time में progress stream करता है। सब
    कुछ एक आख़िरी verdict में दबा देना अपारदर्शिता है, और अपारदर्शिता एक छिपा
    gate है।
19. **बाहरी services की इज़्ज़त करो।** Call से पहले rate limit जानो। Throttle
    करो, errors पर back off करो, responses cache करो, और हर retry loop को एक
    सख़्त छत से बाँधो। किसी endpoint को ठोकना मना है।
20. **Commits में secrets या असली topology नहीं।** Hostnames, IPs, keys, निजी
    data एक ignored env file में रहते हैं; tracked files में placeholders।
    Commit के वक़्त एक guard scan करता है और ज़ोर से fail होता है।
21. **नियम ढाँचे में हैं, याददाश्त में नहीं।** जो नियम agent को याद रखना पड़े,
    वो ठीक तब fail होता है जब agent सबसे व्यस्त है। Floor को hooks, guards और
    tests से लागू करो — prompts और उम्मीद से नहीं।

## सख़्त नियम (क्या इस skill को fail करता है)

- कोई क़ानून अधूरा और कोई दर्ज अधिनिर्णय (adjudication) नहीं — फिर भी बदलाव उतारना।
- बदलाव उतारने के लिए किसी क़ानून को कमज़ोर करना ("good enough" कोई status नहीं)।
- Floor के नाम पर इंसान पर friction डालना — ये क़ानून agents को बाँधते हैं।

## इनके साथ अच्छा चलता है

- [repair-loop](../repair-loop/SKILL.md) — वो loop जो क़ानूनों को सच तक ले जाता है।
- [red-first](../red-first/SKILL.md) — क़ानून 2 एक build method की तरह।
- [blind-tribunal](../blind-tribunal/SKILL.md) — क़ानून 3, ढाँचे में ढला।
- [seam-engineering](../seam-engineering/SKILL.md) — क़ानून 11–12 गहराई में।
- [sniper-testing](../sniper-testing/SKILL.md) — क़ानून 4 के लिए ईमानदार tests.
- [decision-bar](../decision-bar/SKILL.md) — क़ानून 17 गहराई में।
- [human-voice](../human-voice/SKILL.md) — क़ानून 16 का register.
