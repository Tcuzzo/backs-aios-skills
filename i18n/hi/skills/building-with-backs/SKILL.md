---
name: building-with-backs
description: "BACKS project build/repair, wrong-folder या checkout ambiguity सुलझाने, या authorized change IDE से actual runtime तक ले जाने में उपयोग करें।"
license: MIT
---

# Building with BACKS

This skill closes a recurring failure: a good patch in the wrong checkout or a
green test that never reaches the operator's app. The destination is the human's
requested product and path. Discover the target before writing.

Existing [BACKS Build Flow](../backs-build-flow/SKILL.md) task packet में जुड़ें; direct
invocation उसे एक बार बनाता है। एक integration owner रखें और established operator
essence/context reuse करें। `task_mode` मानें और [bounded-loops](../bounded-loops/SKILL.md)
की deadline तथा remaining allowances workers, models और handoffs में साथ रखें। नया path
तय करने से budget restart या deployment authorization नहीं मिलती।

1. **Resolve the destination.** Use the exact path named by the human. If none was
   named, inspect the active workspace, recent project references, and repository
   map. Do not substitute a nearby clone merely because it has a matching name.
   इस skill की directory से
   `python scripts/resolve_target.py --repo <path> --target <file-or-directory>` चलाएँ;
   add `--expected-root <path>` when the human named the checkout. The command
   returns nonzero for a missing target root, a path outside that root, or a
   checkout mismatch or missing Git revision. A new target file may not exist
   yet; its parent must. For a specifically named non-Git project, add
   `--allow-non-git` and record that no revision is available.
2. **Pin the starting truth.** Record the resolved root, branch or detached HEAD,
   `base_sha`, current `candidate_sha`, worktree status, requested target,
   app/service entry point और checks दर्ज करें। Commits होने पर original base pinned
   रखें; candidate identity स्पष्ट अपडेट करें और pending paths फिर जाँचें।
   Preserve unrelated edits. If another checkout is newer, compare revisions and
   actual working trees before choosing; "newest" is a measured claim.
3. **Map the route.** Trace user action to entry point, implementation, data,
   outputs, and deployment seam. Name the existing owner of the behavior and
   any dependent consumers. Use `repo-map`, `architecture-engineer`, and
   `root-cause-first` when those seams are uncertain.
4. **Build in the resolved place.** Give parallel readers distinct questions and
   writers non-overlapping files or isolated worktrees. Keep one integration
   owner. Failure class बंद करने वाला smallest change करें; defect में current
   workflow के अंदर `repair-loop` लें। चुना या explicit request हो तो full `elite-build`
   play अपनाएँ, valid stages reuse करते हुए, फिर boot किए बिना। Review/diagnosis edits
   के बिना findings लौटाता है।
5. **Path साबित करें।** Current sealed RED → minimal fix → sniper lint/type/test
   checks → clean-code-gauntlet loop अपनाएँ। Pinned aggregate candidate diff से scope
   लें; repo की real commands चलाएँ और missing/N/A checks ईमानदारी से बताएँ। Author-
   disjoint review और required full affected-suite landing pass बनाए रखें। Requested
   scope में actual app/CLI surface और runtime logs देखें। Deployed source का exact
   revision/hash और observed behavior लिखें; जो exercise न हो सका वह बताएँ।
6. **Promote through the project's own route.** Read its deployment instructions
   and approval rules from that repository. Never transplant a deployment
   command from another project. Re-run the target check before installation
   and verify the running process uses the installed code afterward.

If the destination remains ambiguous, keep read-only investigation moving and
ask for the missing path only after checking available evidence. Never claim a
cross-host installation merely because files were copied; verify discovery in
each host or mark it unverified.

Allowance समाप्त हो तो verified target, candidate, unresolved evidence और exact next
 action के साथ **STILL-BUILDING** checkpoint करें। Original mission limits बचाएँ;
exhausted allowance खर्च किए बिना उपयोगी authorized work पूरा करें। Local check माँगी
गई delivery evidence की जगह नहीं लेता।
