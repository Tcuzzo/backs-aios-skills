---
name: blind-tribunal
description: तब इस्तेमाल करें जब किसी autonomous बदलाव को उतरने से पहले स्वतंत्र grade चाहिए और loop में कोई इंसान नहीं है — author-redacted envelope में पूरी files पर blind, cross-family jurors बैठते हैं, एक-एक lens; हर finding नया failing test बनती है; हर juror pass होने तक loop चलता है। Trigger words: blind tribunal, grill tribunal, tribunal, jurors, cross-family grade, convene, blind grade, independent grade, grade before landing, अंधी अदालत, जूरी, स्वतंत्र जाँच, उतरने से पहले परख.
license: MIT
---

# Blind Tribunal

वो grading loop जिसकी बदौलत इंसान उठकर जा सकता है और agent बेलगाम नहीं होता।
Jurors का panel बदलाव को blind देखता है, authorship हटाकर। हर finding एक नया
failing test बनती है। Loop तब तक दोहराता है जब तक हर juror pass न कर दे।
सिर्फ builder की ज़बान पर कुछ नहीं उतरता।

## कब चलाएँ

- ऐसा कोई autonomous बदलाव उतारने से पहले जिसे कोई इंसान review नहीं करेगा।
- कोई भी बड़े blast-radius वाला बदलाव: security जैसा, data छूने वाला, authority के क़रीब।
- जब एक grader काफ़ी नहीं और आपको एक ही artifact पर स्वतंत्र नज़रें (lenses) चाहिएँ।

## कुर्सियाँ

तीन jurors। हर एक builder से ALAG family का model।
हर एक के पास ठीक EK lens — जिस juror से सब कुछ जाँचने को कहा जाए, वो कुछ भी ठीक से नहीं जाँचता।

| Juror | Lens | वो कौन सा सवाल पूछता है |
| --- | --- | --- |
| Defect | defect का शिकार | असल में टूटता क्या है? Escapes, edge cases, टूटे contracts. |
| Proportion | सही नाप | क्या यह सही size है? ज़रूरत से ज़्यादा बना, या symptom पर band-aid? |
| Consequence | इंसानी असर | यह ग़लत निकला तो उस इंसान का क्या होगा जो इस पर टिका है? |

**Solo rig.** जब सिर्फ एक model family उपलब्ध हो, तो SAAF-SAAF degrade करो: एक
ताज़ा context या session जो author की बातचीत ने कभी नहीं देखी, blind grader बनता
है, या इंसान redacted envelope को review करता है। Report को कमज़ोर हुए gate का
नाम लेना ही होगा — "graded same-family-blind, not cross-family" — कभी चुपचाप यह
नाटक नहीं कि cross-family gate क़ायम रहा।

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
4. तीनों jurors बिठाओ — builder से अलग families
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

## सख़्त नियम — कोई एक टूटा तो grade रद्द

- Builder अपना काम खुद कभी grade नहीं करता: न वही instance, न वही family।
- **Juror का refuse उतना ही अच्छा है जितना envelope।** किसी finding से test लिखने
  से पहले, finding को असली files के आगे जाँचो। ऐसे code की finding जो envelope में
  था ही नहीं, मतलब envelope ठीक करो, code नहीं।
- Convergence हर round की NAYI findings पर नापो, कुल जोड़ पर नहीं। नई findings दो
  round लगातार जस की तस या बढ़ती हुई: रुको और इंसान तक escalate करो। कभी घिसते मत रहो।
- Pass तक पहुँचने के लिए failing tests को कमज़ोर या edit कभी मत करो। Jurors जाँचते
  हैं कि red commit के बाद से test files बदली नहीं।
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
