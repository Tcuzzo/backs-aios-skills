---
name: rea-investigation
description: जब shipped executable, package या requested runtime behavior में diagnosis, capability discovery या native adoption verification के लिए REA investigation चाहिए, तब उपयोग करें।
license: MIT
---

# REA artifact investigation

Shipped binaries, packages या requested runtime behavior की investigation में installed
REA engine और उसकी matching standalone skill लें। सामान्य source repos में source और
tests सीधे लें। यह bridge REA, Ghidra, provider या MCP server install नहीं करता और उनकी
availability का दावा नहीं करता।

Caller का [BACKS Build Flow](../backs-build-flow/SKILL.md) task packet, integration
owner और permitted `task_mode` लें। Direct investigation packet एक बार बनाती है।
[bounded-loops](../bounded-loops/SKILL.md) deadline और remaining allowances का owner
है; provider retries, model changes और handoffs वही लेते हैं। यह evidence देने वाला
specialist है, दूसरा adoption या repair owner नहीं।

1. Exact target, उसकी identity/hash, question और phase तय करें: upstream artifact की
   **discovery** या specific native result की **verification**। Host की agent skill
   directory से installed upstream `reverse-engineer-anything` skill और relevant
   references पढ़ें; यही bridge recursively न चुनें। वह उपलब्ध न हो तो बताएँ और मौजूदा
   budget में available tools से उपयोगी investigation करें।
2. Connected REA tools उपलब्ध हों तो लें, अन्यथा installed REA CLI। Native binary
   analysis के लिए जहाँ supported हो existing compatible Ghidra provider लें। Missing
   या unavailable provider बताएँ; result न गढ़ें और authorization बिना dependencies
   install न करें।
3. Read-only static inspection से शुरू करें। Target identity, evidence IDs, scope,
   limits और unknowns दर्ज करें। Static findings runtime behavior सिद्ध नहीं करते;
   live observation केवल user-requested scope और declared tool की execution तथा
   mutation boundaries में करें।
4. Caller को evidence packet लौटाएँ: target identity, phase, commands/tool receipts,
   evidence IDs, observations, static/runtime distinction, unknowns और remaining
   mission budget। Next step caller का है: Absorb अपने license/dependency gates और
   native integration चलाता है; repair owner root-cause-first और repair-loop अपनाता
   है। इस bridge से इनमें से कोई lifecycle recursively शुरू न करें। Verification defect
   पाए तो sealed RED और bounded fix/check loop के लिए observation लौटाएँ; repair हो
   जाने का दावा न करें।
5. Configured fleet-ladder से role/capability अनुसार dispatch तय करें; model IDs
   hardcode न करें। Independent assessment जरूरी हो तो blind-tribunal का fresh
   author-disjoint execution और author-redacted packet लें, केवल host runtime की
   वास्तविक capabilities के अनुसार। Missing provider या exhausted budget पर उपयोगी
   observations और exact next action के साथ **STILL-BUILDING** checkpoint दें; वह
   कभी fabricated runtime proof नहीं। Unblocked investigation remaining allowance
   में ही रखें।

Scaffold: morluto का REA, MIT license, https://github.com/morluto/rea।
Engine, upstream skill और providers अलग installations हैं।
