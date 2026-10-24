---
name: building-with-backs
description: Build or repair a BACKS project at the operator's intended repository and path, with a checked source revision, one write spine, tests, and proof on the actual surface. Use for build with BACKS, wrong-folder friction, and IDE-to-runtime promotion.
license: MIT
---

# Building with BACKS

This skill closes a recurring failure: a good patch in the wrong checkout or a
green test that never reaches the operator's app. The destination is the human's
requested product and path. Discover the target before writing.

1. **Resolve the destination.** Use the exact path named by the human. If none was
   named, inspect the active workspace, recent project references, and repository
   map. Do not substitute a nearby clone merely because it has a matching name.
   Run `scripts/resolve_target.py --repo <path> --target <file-or-directory>`;
   add `--expected-root <path>` when the human named the checkout. The command
   returns nonzero for a missing target root, a path outside that root, or a
   checkout mismatch or missing Git revision. A new target file may not exist
   yet; its parent must. For a specifically named non-Git project, add
   `--allow-non-git` and record that no revision is available.
2. **Pin the starting truth.** Record the resolved root, branch or detached HEAD,
   commit, worktree status, requested target, app/service entry point, and tests.
   Preserve unrelated edits. If another checkout is newer, compare revisions and
   actual working trees before choosing; "newest" is a measured claim.
3. **Map the route.** Trace user action to entry point, implementation, data,
   outputs, and deployment seam. Name the existing owner of the behavior and
   any dependent consumers. Use `repo-map`, `architecture-engineer`, and
   `root-cause-first` when those seams are uncertain.
4. **Build in the resolved place.** Give parallel readers distinct questions and
   writers non-overlapping files or isolated worktrees. Keep one integration
   owner. Write the smallest change that closes the failure class; use
   `repair-loop` for defects and `elite-build` for new capability.
5. **Prove the path.** Run focused tests, then the affected suite. Inspect the
   actual app/CLI surface and runtime logs. A staged file, mock, or green test
   is not live proof. Record the exact source revision/hash deployed and the
   observed behavior; name anything that could not be exercised.
6. **Promote through the project's own route.** Read its deployment instructions
   and approval rules from that repository. Never transplant a deployment
   command from another project. Re-run the target check before installation
   and verify the running process uses the installed code afterward.

If the destination remains ambiguous, keep read-only investigation moving and
ask for the missing path only after checking available evidence. Never claim a
cross-host installation merely because files were copied; verify discovery in
each host or mark it unverified.
