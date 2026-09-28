---
name: "blind-tribunal"
description: "तब इस्तेमाल करें जब किसी autonomous बदलाव को उतरने से पहले स्वतंत्र grade चाहिए और loop में कोई इंसान नहीं है — author-redacted envelope में पूरी files पर blind, cross-family jurors बैठते हैं, एक-एक lens; हर finding नया failing test बनती है; हर juror pass होने तक loop चलता है। Trigger words: blind tribunal, grill tribunal, tribunal, jurors, cross-family grade, convene, blind grade, independent grade, grade before landing, अंधी अदालत, जूरी, स्वतंत्र जाँच, उतरने से पहले परख."
license: "MIT"
---

# Blind Tribunal
**Effort:** heavy — आठ jurors, एक-एक lens, tier के हिसाब से सबसे सस्ती काफ़ी model family पर routed, हर round ताज़े envelopes पर दोबारा बैठते हैं जब तक फ़ैसला एकमत न हो; इसे उन autonomous बदलावों पर खर्च करें जो बिना इंसानी review के land होते हैं। हटाता है: वे rogue landings जिन पर builder की अपनी बात के सिवा कोई पहरा नहीं।

वो grading loop जिसकी बदौलत इंसान उठकर जा सकता है और agent बेलगाम नहीं होता।
Jurors का panel बदलाव को blind देखता है, authorship हटाकर। हर finding एक नया
failing test बनती है। Loop तब तक दोहराता है जब तक हर juror pass न कर दे।
सिर्फ builder की ज़बान पर कुछ नहीं उतरता।

## कब चलाएँ

- ऐसा कोई autonomous बदलाव उतारने से पहले जिसे कोई इंसान review नहीं करेगा।
- कोई भी बड़े blast-radius वाला बदलाव: security जैसा, data छूने वाला, authority के क़रीब।
- जब एक grader काफ़ी नहीं और आपको एक ही artifact पर स्वतंत्र नज़रें (lenses) चाहिएँ।

## कुर्सियाँ

आठ jurors, एक-एक lens। हर एक builder से ALAG family का model (एक ही vendor = एक ही family)।
जिस juror से सब कुछ जाँचने को कहा जाए, वो कुछ भी ठीक से नहीं जाँचता।

| Juror | Lens id | Tier | वो कौन सा सवाल पूछता है |
| --- | --- | --- | --- |
| Defect | `defect` | generalist | असल में टूटता क्या है? Logic की ग़लतियाँ, syntax errors, नए defects. |
| Proportion | `proportion` | generalist | क्या size सही है? ज़रूरत से ज़्यादा बना, या intent के नाप का? |
| Consequence | `operator_consequence` | operator safety | कोई इंसान operator इसे चलाए तो क्या destructive, unsafe या नुक़सानदेह है? |
| Reversibility | `reversibility` | deep state | क्या irreversible असर छोड़ता है? बीच में मरे तो system साफ़ rollback कर पाएगा? |
| Continuity | `state_continuity` | deep state | Variables orphan, global state clobber, या आगे के nodes का ज़रूरी context drop? |
| Economy | `resource_economy` | fast structural | Un-optimized loops, बेकार network/API calls, memory bloat? |
| Boundary | `boundary_condition` | fast structural | Null, empty, ग़लत type या malformed input पर — क्या gracefully fail होता है? |
| Telemetry | `telemetry` | operator safety | यहाँ की failure logs और error handling से पकड़ी जा सकती है? |

**Routing tiers (पहले सबसे सस्ता जो काफ़ी हो):** deep state → सबसे बड़ा context और
सबसे गहरा reasoning, बेहतर हो तो ऐसे harness से जो repo को READ करे (कभी write नहीं);
fast structural → पहले free local GPU, जो एक सस्ते cloud verifier के साथ FUSED है — दोनों
वही prompt जाँचते हैं, lens तभी pass जब दोनों pass; cloud पूरी तरह down हो तो local verdict
रहता है पर UNVERIFIED मार्क होकर, कभी चुपचाप "verified" नहीं; और local model को पूरा artifact
दिखना चाहिए (`num_ctx` को prompt के हिसाब से set करो — Ollama का default 4096 चुपचाप काट
देता है — जो नहीं समाता उसे भेजने से पहले ही refuse करो); verifier कभी primary seat की family से नहीं होता, और UNVERIFIED seat एक hold है (कभी unanimity नहीं); harness jurors read-only चलते हैं, और हर convene एक `run_id` रखता है और summary सबसे आख़िर में लिखता है; फिर low-latency cloud models;
operator safety → safety grounding वाला आपका सबसे मज़बूत coder; generalist → एक
बड़ा भरोसेमंद generalist। हर ladder एक local survival rung पर ख़त्म होती है।

**Solo rig.** जब सिर्फ एक model family उपलब्ध हो, तो SAAF-SAAF degrade करो: एक
ताज़ा context या session जो author की बातचीत ने कभी नहीं देखी, blind grader बनता
है, या इंसान redacted envelope को review करता है। Report को कमज़ोर हुए gate का
नाम लेना ही होगा — "graded same-family-blind, not cross-family" — कभी चुपचाप यह
नाटक नहीं कि cross-family gate क़ायम रहा।

## builder घोषित होता है, और बहिष्कार संरचनात्मक है

"builder से अलग परिवार" एक नियम था जिसे jurors को याद रखना था। tribunal के अपने ही परीक्षण में operator-safety
सीट का नेतृत्व उसी model ने किया जिसने candidate बनाया था, और किसी ने उसे दर्ज या बाहर नहीं किया: लेखक ने दो
round तक अपना ही काम grade किया। इसलिए:

- **builder का नाम लेकर convene करें** (`--builder <model-या-परिवार>`)। run record में `builder_family` रहता है।
  उस परिवार की हर rung हर ladder पर, dispatch से पहले, ज़ोर से अस्वीकार होती है। बिना rung वाला lens HOLD पर जाता है — कभी builder पर नहीं लौटता।
- **एक ही vendor = एक ही परिवार।** एक घोषणा पूरे vendor को बाहर करती है।
- **इसे live ladder पर साबित करें, test में नहीं:** routing table दिखाए कि उसकी सीटें दूसरे परिवार को चली गईं। वरना बहिष्कार सजावट है।

## Envelope

Jurors को repo, builder या बातचीत कभी नहीं दिखती। उन्हें एक envelope दिखता है:

- **पूरी current files** — हर उस file की जिसे बदलाव ने छुआ, साथ में उसकी test files।
  नंगे diff hunks कभी नहीं — hunk आस-पास का contract छिपाता है और झूठी findings पैदा करता है।
- **Review contract**: बदलाव का इरादा एक line में, और pass की कसौटियाँ।
- **Authorship शून्य।** कोई नाम नहीं, model ids नहीं, commit authors नहीं, chat history नहीं।
  अगर पहचान रिसती है, तो envelope बनाना ज़ोर से fail होता है — बिना blind grade कभी नहीं।
- **पुराने behavior के बारे में कोई गद्य नहीं।** "यह code पहले क्या करता था" बताना
  भूतिया defects बोता है। Files खुद बोलती हैं।

## Verdict

सख़्त machine-parseable JSON, एक object, कोई गद्य नहीं:

```json
{"verdict": "pass" | "refuse",
 "findings": [{"severity": "blocker|major|minor|info",
               "claim": "...", "evidence": "..."}]}
```

- **`[blocker]` या `[major]` finding सूचीबद्ध करने वाला pass, pass नहीं है।** आत्म-विरोधी; severity का नाम लेकर refuse पर fail-closed।
- **बैठाए गए lens से अलग lens का verdict** अस्वीकृत rung है, verdict नहीं: दोनों lens दर्ज, walk अगली rung पर; सब गलत जवाब दें तभी lens HOLD। कभी pass नहीं।
- **output directory पहले अपनाई जाती है, फिर साफ़ होती है।** organ अपनी directory पर मुहर (stamp) लगाता है; उन file-आकारों वाली पर बिना मुहर के अस्वीकार — files और उपाय का नाम, कुछ delete नहीं। केवल पराई files वाली directory कभी ख़तरे में नहीं थी, रोकी नहीं जाती।
- **एक lens के फटने से चुकाए गए verdict कभी नहीं खोते।** हर seat failure lens-वार दर्ज; verdict और summary error से पहले लिखे जाते हैं।
- **mutation evidence दोबारा लिखी गई file का नाम लेती है** (`changed_paths`)।
- **organ जो भी लिखता है वह केवल owner-पठनीय है (0600)।**
- **छलका हुआ local model केवल आख़िरी holder ही unload करता है।** दो lens एक card साझा कर सकते हैं; पहले ख़त्म होने वाला दूसरे के बीच-call में model नहीं छीनता।
- **जिस rung में artifact नहीं समाता वह call से पहले छोड़ दी जाती है**, कारण दर्ज; capacity refusal एक TYPE है और walk जारी रहता है — कभी halt नहीं।
- जिस juror ने BURA जवाब दिया — कचरा, non-JSON, इनकार का text — वो **refuse**
  गिना जाता है; जिस juror ने जवाब ही NAHIN दिया (transport failure, unreachable)
  वो **hold** है: उसे [fleet-ladder](../fleet-ladder/SKILL.md) से दोबारा बिठाओ,
  चुपचाप pass कभी नहीं। हर जवाब देने वाले juror को हर round में एक ही मौक़ा — retries नहीं।
- शून्य findings और बिना सबूत का नंगा pass एक **low-information vote** है।
  वो गिनता है, पर अकेले सबूत के तौर पर कभी नहीं — दो नंगे pass एक तफ़सीली refuse
  से ऊपर नहीं। मज़बूत pass बताता है कि उसने क्या-क्या जाँचा।

## Loop

1. Red first: fix बनने से PEHLE failing contract test commit करो, और वो commit दर्ज
   करो। Builder test को छू नहीं सकता ([red-first](../red-first/SKILL.md))।
2. Green होने तक बनाओ।
3. CURRENT files से envelope बनाओ।
4. आठों jurors tier के हिसाब से बिठाओ — builder से अलग families
   ([fleet-ladder](../fleet-ladder/SKILL.md) बताता है कौन live है)।
5. हर juror सिर्फ पढ़ता नहीं, verify भी करता है: नए tests pass होते हैं; regression
   suite baseline से बदतर नहीं; और एक fake-green जाँच — जिस test को fail होना
   CHAHIYE (bug वापस डालकर) वो fail होता भी है। Fake green यानी refuse.
6. किसी भी refuse पर: HAR finding — blocker, major और minor — एक NAYA failing
   test बनती है जो उस finding की असली वजह से fail होता है। उसे ठीक करो। सुधरी
   files पर envelope दोबारा बनाओ। SAB jurors दोबारा बिठाओ। बासी files पर verdict
   कोई verdict नहीं।
7. सिर्फ सर्वसम्मत pass पर उतारो। आख़िरी round में उठीं minor findings भी बंद होती
   हैं, टाली नहीं जातीं — "blockers ठीक कर दिए, minors बाद में" ठीक वही रिसाव है
   जिसे रोकने के लिए यह skill बनी है। Finding का अंत FIXED होता है या दर्ज सबूत के
   साथ खंडित — कभी parked नहीं।

## Footer lens का नाम लेता है, rejected rung अपने शब्द रखता है, और floor तीन rung गहरा है

Round 4 में zero refusal के साथ दो lens hold पर रह गए, और हर कड़ी record पर थी। उससे तीन नियम निकले:

- **जवाब का shape जवाब के बगल में लिखो।** Protocol footer में lens का literal नाम होता है (`"lens": "defect"`), कभी `<your lens>` placeholder नहीं। एक juror से 350 KB पहले बताया गया lens याद रखने को कहा गया, ऐसे artifact के अंदर जो आठों lens के नाम लेता है — उसने दो round में तीन बार गलत lens जवाब दिया। Placeholder render के समय भरो।
- **Rejected rung अपने शब्द record पर छोड़ता है।** गलत lens का जवाब या void हुआ verdict rejected entry पर एक bounded `raw_tail` रखता है, ताकि अगला round कारण पढ़े, अंदाज़ा न लगाए।
- **दो cloud rung floor नहीं हैं।** हर tier अपनी local tail से पहले कम से कम तीन ऐसे rung रखता है जिनमें `context_tokens` declared नहीं है (वे 120k-token artifact उठा सकते हैं)। एक गलत lens और एक void मिलकर कभी lens को hold पर न रखें।
- **Structured verdict कभी अपना budget सोचने के साथ नहीं बाँटता।** जिस reasoning model से सादा JSON verdict माँगा गया, उसने 131k-token artifact पर सोचने में पूरा 65536-token budget खर्च कर दिया और कुछ नहीं दिया (`finish_reason=length`); फिर role की time ceiling ने अगले rung को बीच रास्ते मार दिया। हर cloud rung जो JSON-object verdict माँगता है, reasoning channel बंद करके चलता है (`reasoning_effort: none`), और verifier ladder उसके पीछे plain-HTTP वाली तीसरी family रखती है।
- **Tribunal जब बैठा हो, उसके repo में और कोई कुछ न लिखे।** Checkout के अंदर एक साथ चल रहे grader की status file ने एक seat के नीचे bytes बदल दिए, और organ ने वह verdict ईमानदारी से void किया: वह बदलाव को किसी को attribute नहीं कर सकता। Writers को serialize करो, या उसी commit के अलग worktree पर बैठो।

## सख़्त नियम — कोई एक टूटा तो grade रद्द

- Builder अपना काम खुद कभी grade नहीं करता: न वही instance, न वही family।
- **Juror का refuse उतना ही अच्छा है जितना envelope।** किसी finding से test लिखने
  से पहले, finding को असली files के आगे जाँचो। ऐसे code की finding जो envelope में
  था ही नहीं, मतलब envelope ठीक करो, code नहीं।
- Convergence हर round की NAYI findings पर नापो, कुल जोड़ पर नहीं। नई findings दो
  round लगातार जस की तस या बढ़ती हुई: रुको और इंसान तक escalate करो। कभी घिसते मत रहो।
- Pass तक पहुँचने के लिए failing tests को कमज़ोर या edit कभी मत करो। Jurors जाँचते
  हैं कि red commit के बाद से test files बदली नहीं।
- **survivor एक दावा है; हरा proof एक दावा है।** हर बताए गए mutant survivor को अलग tree में, load से बचने वाली सीमा के साथ, हाथ से दोबारा चलाएँ। timeout survivor नहीं; collection error kill नहीं। proof harness का हर verdict path INVALID कह सके, और जिसकी बिना-mutation baseline साफ़ हरी न हो वह कोई verdict न दे।
- सर्वसम्मत pass gate खोलता है; वो अंत नहीं है। उतारो, फिर capability को असली
  surface पर live साबित करो। Live proof के बिना green, done नहीं है।

## इनके साथ अच्छा चलता है

- [red-first](../red-first/SKILL.md) — failing contract, builder चलने से पहले committed.
- [sniper-testing](../sniper-testing/SKILL.md) — असली side-effects, scoped runs, mock theater नहीं।
- [seam-engineering](../seam-engineering/SKILL.md) — class ठीक करो, siblings झाड़ो, guard उतारो।
- [repair-loop](../repair-loop/SKILL.md) — वो build loop जिसे यह tribunal grade करता है।
- [blind-eval](../blind-eval/SKILL.md) — जब सवाल defects नहीं taste हो, तब का हल्का keep-or-revert gate.

> Scaffold credit: Matt Pocock, grill-me / grilling (mattpocock/skills, MIT). The
> cross-family blind adversarial tribunal design is BACKS AIOS.
