---
name: bounded-loops
description: "ऐसे काम से पहले उपयोग करें जो retry, poll, iterate, workers dispatch या external calls दोहरा सकता हो; इसमें autonomous build, repair, review और adoption loops शामिल हैं।"
license: MIT
---

# सीमाबद्ध Loops

एक mission की एक ही remaining allowance होती है। Retry, worker, model fallback,
review round, context reset या nested skill उसी को खर्च करता है; उसे फिर भरता नहीं।
[Build Flow](../backs-build-flow/SKILL.md) task transitions का owner है। यह method
budget accounting, retries, cancellation और checkpoints का owner है।

## Contract घोषित करें और साथ रखें

पहली दोहराई जा सकने वाली कार्रवाई से पहले मौजूदा task packet में दर्ज करें:

- `mission_id`, integration owner, objective और measurable acceptance condition।
- Deadline या maximum elapsed time, maximum attempts/rounds और resource/call caps।
- Consumed तथा remaining allowance, current episode की छोटी round limit,
  failure signature और next action। स्पष्ट छोटा inner cap लें, अक्सर तीन attempts;
  उसे task के लिए चुनें, उदाहरण को सार्वभौम नियम न बनाएँ।
- जहाँ उपलब्ध हों measured cost/token/call data। अनुपलब्ध counters को unknown लिखें;
  zero, unlimited allocation या provider budget न गढ़ें। Host वास्तव में जो counters
  देता है उनसे लागू हो सकने वाली time और attempt bounds बनाएँ।

User/project की अधिक सख्त limits अपनाएँ। सामान्य अधिकृत task में limits न दी गई हों तो
अनुपातिक bounds चुनें, बताएँ और नई permission round के बिना काम करें। पूछें तभी जब असली
resource commitment के लिए authorization जरूरी हो। Budget extension के लिए mission
owner का स्पष्ट निर्णय और आवश्यक operator authorization चाहिए; worker या tactic बदलना
extension नहीं है।

## Iteration

1. काम देने से पहले शेष allowance जाँचें। Parallel children सहित सभी child ceilings
   उसी के भीतर रखें: उनके अधिकतम allocation centrally reserve करें ताकि कुल खर्च
   parent से अधिक न हो। Child used/unused allowance लौटाता है।
2. एक hypothesis आधारित action चलाएँ। Build/fix में वास्तविक RED सुरक्षित रखें,
   सबसे छोटा पूर्ण fix करें, scoped lint/type/behavior checks चलाएँ, और
   [sniper-testing](../sniper-testing/SKILL.md) तथा
   [clean-code-gauntlet](../clean-code-gauntlet/SKILL.md) से quality evidence लौटाएँ।
3. सुरक्षित boundaries पर results और remaining allowance checkpoint करें। एक writer
   अधिकृत task state को atomically अपडेट करता है; workers उसे evidence लौटाते हैं।
   Strict read-only review में पहले से अधिकृत external task record या response लें।
   Read-only scope repo ledger लिखने की अनुमति नहीं बनता।
4. नए evidence के बिना वही failure आए तो hypothesis या tactic बदलें; blind run फिर न
   करें। Exhausted inner episode बंद करें। अलग episode parent की बची allowance ले सकता
   है, लेकिन उसका स्पष्ट हिसाब रखें।
5. Mission exhaustion, cancellation या required gate के blocked होने पर checkpoint
   करें, blocker बताएँ और दोहराव रोकें। स्वतंत्र उपयोगी काम केवल तभी जारी रहे जब scope
   और बचा allocation अनुमति दें। अधूरी capability **STILL-BUILDING** है; timeout या
   skipped gate कभी GREEN या PROVEN नहीं।

## External calls और cancellation

Published provider limits और Retry-After मानें। Cached results उपयोग करें; limits
अज्ञात हों तो सावधानी से शुरू करें और मापें। Transient pushback पर maximum elapsed time
और attempt count सहित bounded exponential backoff करें। Permanent authorization/input
failures को transient मानकर retry न करें। Waiting, backoff और fallback उसी mission
deadline में गिने जाते हैं।

सुरक्षित state boundary पर रुकें: जारी काम दर्ज करें, checkpoint करें और cancel करें।
दूसरा writer शुरू न करें; cancellation के बाद background loop चलता न छोड़ें। नए requests
उसी boundary पर current mission को दिशा देते हैं; scope परिवर्तन स्पष्ट हिसाब में लें,
मूल उद्देश्य चुपचाप न बदलें।

## Handoff और exit

Receiver को वही mission identity, base/candidate revisions, sealed test identity,
used/remaining allowance, evidence और next action दें। वह resume से पहले state सत्यापित
करता है। Fresh context fresh budget नहीं है।

Success के लिए मूल acceptance checks और माँगी गई delivery जरूरी हैं। Budget exhaustion
पर ईमानदार checkpoint चाहिए; कमजोर tests, swallowed errors, data deletion, गढ़ा pass या
भरे हुए counter वाला automatic outer loop नहीं।

Continuation के लिए [session-handoff](../session-handoff/SKILL.md), और वास्तव में
configured model dispatch से पहले [fleet-ladder](../fleet-ladder/SKILL.md) देखें।
