---
name: fix-shit
description: Diagnose and close a reported failure end to end with a reproducer, root cause, class-level repair, consumer tests, and real-path proof. Use when the operator says fix shit, stop swallowing errors, or finish a stubborn bug.
license: MIT
---

# Fix Shit

Use this as the fast entry point into `root-cause-first` and `repair-loop`.
It is a repair skill, not a permission to hide a failing signal.

1. Name the user's broken behavior and the exact surface where it appears.
2. Build a repeatable red signal from the real path. Trace the input and each
   boundary to find where actual behavior diverges from expected behavior.
3. Identify the root cause and all callers of the broken seam. Preserve the
   original error in logs or the operator-facing state; a fallback may protect
   the app, but it must not turn failure into false success.
4. Make the smallest change that closes the failure class. Add a test that fails
   on the old behavior and covers the seam that failed.
5. Run focused tests, the affected consumers, and the actual app path. Verify
   both the desired result and the explicit failure state. Ask an author-disjoint
   reviewer to inspect the change when available.
6. Report PROVEN or STILL-BUILDING, with the evidence and any remaining red bar.

If the error is intermittent, capture timing and a bounded reproduction rate;
do not infer a cause from one green rerun. For code-location ambiguity, start
with `building-with-backs` and its target check.


## साक्ष्य और स्वतंत्र समीक्षा

प्रकाशित executables, packages या अनुरोधित runtime व्यवहार के लिए [rea-investigation](../rea-investigation/SKILL.md) और अलग से स्थापित `reverse-engineer-anything` skill का उपयोग करें जब उसका विश्लेषण उपयोगी हो; समर्थित native लक्ष्य पर मौजूदा Ghidra provider लें। Static साक्ष्य live व्यवहार का प्रमाण नहीं है; अनुपस्थित provider चुपचाप स्थापित न करें। Open-source क्षमता अपनाने के लिए [absorb](../absorb/SKILL.md) चलाएं। [fleet-ladder](../fleet-ladder/SKILL.md) से role और capability पर चयन करें, model नाम hardcode न करें। Tribunal आवश्यक हो तो [blind-tribunal](../blind-tribunal/SKILL.md) अपनाएं: नई, लेखक से अलग execution लेखक की जानकारी हटाए frozen packet की समीक्षा करे; model family session isolation का प्रमाण नहीं है। गायब resolver, reviewer या साक्ष्य को runtime gap बताएं।
