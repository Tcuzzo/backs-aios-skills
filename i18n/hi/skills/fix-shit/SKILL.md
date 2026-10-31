---
name: fix-shit
description: "जब operator broken behavior report करे, fix shit या stop swallowing errors कहे, या stubborn bug पूरा ठीक करने को कहे, तब उपयोग करें।"
license: MIT
---

# Fix Shit

Current [BACKS Build Flow](../backs-build-flow/SKILL.md) task में `root-cause-first`
और `repair-loop` का fast entry point लें। वही integration owner, operator essence,
`task_mode`, candidate identity और evidence रखें; valid packet reload या दूसरा
lifecycle न शुरू करें। Direct invocation packet एक बार बनाता है।
[bounded-loops](../bounded-loops/SKILL.md) का caller budget/deadline हर reproduction,
fix, model fallback और review पर लागू है; यह skill उसे reset या failure signal छुपाती नहीं।

1. User का broken behavior और वह exact surface बताएँ जहाँ वह दिखता है।
2. Real path से repeatable red signal बनाएँ। Input और हर boundary trace करें कि actual
   behavior expected behavior से कहाँ अलग होता है। Builder seam बदले उससे पहले
   [red-first](../red-first/SKILL.md) से original failing contract seal करें। Diagnostic
   task यह evidence लौटाता है।
3. Root cause और broken seam के सभी callers पहचानें। Original error logs या operator
   state में रखें; fallback app बचा सकता है, failure को false success नहीं बनाता।
4. Authorized fix में [repair-loop](../repair-loop/SKILL.md) inline लें: smallest
   class-level repair, pinned aggregate candidate diff से scoped real lint/type/tests,
   फिर clean-code-gauntlet quality/mutation checks। Sealed original बचाएँ; नया gap
   separate supplemental test पाता है। Already verified stages reuse करें।
5. Requested delivery के लिए required author-disjoint review, affected-suite landing
   gate और actual app-path checks पूरे करें। Desired result और explicit failure state
   दोनों सत्यापित करें। Missing reviewer capability runtime gap है; खुद दिया independent
   pass नहीं।
6. Candidate और evidence integration owner को लौटाएँ। Required review और real delivery
   evidence होने पर ही PROVEN कहें; अन्यथा exact remaining red bar और next action के
   साथ STILL-BUILDING checkpoint करें। Budget exhaustion work और limits बचाता है;
   useful unblocked work remaining allowance में ही करें।

If the error is intermittent, capture timing and a bounded reproduction rate;
do not infer a cause from one green rerun. For code-location ambiguity, start
with `building-with-backs` and its target check.


## साक्ष्य और स्वतंत्र समीक्षा

प्रकाशित executables, packages या अनुरोधित runtime व्यवहार के लिए [rea-investigation](../rea-investigation/SKILL.md) और अलग से स्थापित `reverse-engineer-anything` skill का उपयोग करें जब उसका विश्लेषण उपयोगी हो; समर्थित native लक्ष्य पर मौजूदा Ghidra provider लें। Static साक्ष्य live व्यवहार का प्रमाण नहीं है; अनुपस्थित provider चुपचाप स्थापित न करें। Open-source क्षमता अपनाने के लिए [absorb](../absorb/SKILL.md) चलाएं। [fleet-ladder](../fleet-ladder/SKILL.md) से role और capability पर चयन करें, model नाम hardcode न करें। Tribunal आवश्यक हो तो [blind-tribunal](../blind-tribunal/SKILL.md) अपनाएं: नई, लेखक से अलग execution लेखक की जानकारी हटाए frozen packet की समीक्षा करे। गायब resolver, reviewer या साक्ष्य को runtime gap बताएं।
