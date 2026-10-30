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


## Preuves et revue indépendante

Pour les exécutables distribués, paquets ou comportements demandés à l’exécution, utilise [rea-investigation](../rea-investigation/SKILL.md) et le skill `reverse-engineer-anything` installé séparément lorsque son analyse est utile ; utilise un fournisseur Ghidra existant pour les cibles natives prises en charge. Une preuve statique ne démontre pas le comportement en direct ; n’installe pas silencieusement un fournisseur manquant. Pour adopter une capacité open source, utilise [absorb](../absorb/SKILL.md). Choisis par rôle et capacité avec [fleet-ladder](../fleet-ladder/SKILL.md), sans nom de modèle codé en dur. Si un tribunal est requis, suis [blind-tribunal](../blind-tribunal/SKILL.md) : une nouvelle exécution séparée de l’auteur examine un paquet figé expurgé des données de l’auteur. Signale tout résolveur, relecteur ou preuve manquant comme une lacune du runtime.
