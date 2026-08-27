---
name: guided-steps
description: तब इस्तेमाल करें जब किसी setup में ऐसे steps हों जो सिर्फ इंसान कर सकता है — third-party dashboards, credentials, CI secrets, provisioning, one-off migrations, cutovers; एक stage-by-stage interactive script लिखता है जो हर URL खोलती है, बताती है क्या click और copy करना है, values पकड़ती है और उन्हें सही जगह लिखती है। Trigger words: wizard, human-only steps, provision, credentials, dashboard setup, CI secrets, cutover, विज़ार्ड, इंसानी कदम, सेटअप गाइड, क्रेडेंशियल.
license: MIT
---

# Human Steps Wizard
**Effort:** free — लिखने का अनुशासन और एक static syntax check; कोई model call नहीं। हटाता है: वही human-only clickpath हर run पर दोबारा समझाना, और रास्ते में tracked files में चिपके secrets।

कुछ steps सिर्फ इंसान कर सकता है: third-party dashboard में click करना,
credentials बनाना, provisioning screen को approve करना। हाथ से करने में ये
उबाऊ हैं और हर बार दोबारा समझाने में भी। Wizard उन्हें एक guided run बना देता
है: एक stage-by-stage interactive shell script जो हर URL खोलती है, ठीक-ठीक
बताती है क्या click और copy करना है, values पकड़ती है, और उन्हें वहीं लिखती है
जहाँ उन्हें होना चाहिए।

## कब इस्तेमाल करें

- Setup में इंसान को ऐसा UI चलाना है जहाँ कोई API नहीं पहुँचता — dashboards,
  consoles, credential screens, CI secret pages, one-off migrations, cutovers.
- रास्ता इतना लंबा है कि हर बार दोबारा समझाना खलता है।

कब NAHIN इस्तेमाल करें: API वो step कर सकता है (उसे automate करो — wizard आख़िरी
सहारा है), या procedure एक-दो steps की है (इंसान को बस सादे शब्दों में बता दो)।

## आकार

एक script, दो हिस्से:

- **ऊपर एक helper library** — हर wizard में एक जैसी, कभी हाथ से edit नहीं होती।
  वो देती है: progress के साथ stage headers ("stage 3 of 7"), human-voice
  narration, cross-platform URL खोलना, secrets के लिए छिपी entry, idempotent
  `.env` upserts (key हो तो update, न हो तो append), आपके CI provider के secret
  store में writes, एक confirm/pause step, और अंत में जो कुछ पकड़ा गया उसका सार।
- **Marker के नीचे stages** — बस यही हिस्सा आप लिखते हैं। हर इंसानी step की एक
  stage: URL खोलो, बताओ क्या click और क्या copy करना है, value पकड़ो, उसकी मंज़िल
  पर लिखो। Stages की कुल गिनती सेट करो ताकि progress display ईमानदार रहे।

## Process

1. **Scope.** Env example file, README, deploy config और CI workflows पढ़ो। वे
   जिस भी secret या variable का ज़िक्र करते हैं, वो value wizard को पैदा करनी
   है। इंसान को क्रमबद्ध stages और values पहले ही दिखाओ — लिखने से पहले plan
   confirm करो।
2. **हर stage का सफ़र map करो।** हर stage की एक line: URL → action → value →
   destination. इंसान शुरू करने से पहले पूरा रास्ता देख लेता है।
3. **लिखो।** Template copy करो। सिर्फ stages लिखो; library को कभी मत छुओ।
   Narration सादे शब्दों में रखो — इसे चलाने वाला इंसान engineer न भी हो।
4. **Statically verify करो।** Script का syntax जाँचो (`bash -n`, shellcheck),
   उसे executable बनाओ, फिर हर stage हाथ से टटोलो: हर URL सही है, हर हिदायत
   साफ़ है, हर write target ठीक है? इसे end-to-end मत चलाओ — यह browsers खोलती
   है और इंसानी input पर अटकती है।

## सख़्त नियम

- **Secrets tracked files को कभी नहीं छूते।** पकड़ी गई values gitignored `.env`
  या CI secret store में उतरती हैं। Script खुद सिर्फ placeholders रखती है; असली
  values इंसान run के वक़्त paste करता है। लिखी हुई script में असली key,
  hostname या निजी ब्योरा — यही bug है।
- **हर remote write single-shot और सीमित है।** Secret-store write एक API call
  है: कोई retry loops नहीं, कोई hammering नहीं। ज़ोर से fail करो और इंसान को
  stage दोबारा चलाने दो।
- **Default रूप से ephemeral.** Wizard एक run के लिए बनता है और बाद में delete
  होता है। Commit तभी करो जब इंसान दोहराने लायक setup path माँगे — और committed
  wizard में भी सिर्फ placeholders ही रहते हैं।
- **Confirm step इंसान का अपना pause button है, gate नहीं।** वो इसलिए है कि वे
  अपना काम जाँच सकें — उन पर approval का friction डालने के लिए कभी नहीं।

## इनके साथ अच्छा चलता है

- [session-handoff](../session-handoff/SKILL.md) — run बँट जाए तो दर्ज करो कौन सी stages चलीं।
- [human-voice](../human-voice/SKILL.md) — हर stage जिस register में बोलती है।
- [bounded-loops](../bounded-loops/SKILL.md) — remote writes के पीछे का no-hammering नियम।

> Scaffold credit: Matt Pocock, wizard (mattpocock/skills). The composition and hard rules here are BACKS AIOS.
