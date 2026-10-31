---
name: building-with-backs
description: "Pour construire ou réparer un projet BACKS, résoudre un mauvais dossier ou un checkout ambigu, ou transférer une modification autorisée de l'IDE à son runtime réel."
license: MIT
---

# Building with BACKS

This skill closes a recurring failure: a good patch in the wrong checkout or a
green test that never reaches the operator's app. The destination is the human's
requested product and path. Discover the target before writing.

Rejoins le dossier [BACKS Build Flow](../backs-build-flow/SKILL.md) existant ;
un appel direct le crée une fois. Conserve un responsable de l'intégration et
réutilise l'essence opérateur et le contexte déjà établis. Respecte `task_mode` et
transmets échéance et quotas restants de [bounded-loops](../bounded-loops/SKILL.md)
entre agents, modèles et relèves. Résoudre un nouveau chemin ne recharge pas le
budget et n'autorise pas un déploiement.

1. **Resolve the destination.** Use the exact path named by the human. If none was
   named, inspect the active workspace, recent project references, and repository
   map. Do not substitute a nearby clone merely because it has a matching name.
   Run `python scripts/resolve_target.py --repo <path> --target <file-or-directory>`
   from this skill's directory;
   add `--expected-root <path>` when the human named the checkout. The command
   returns nonzero for a missing target root, a path outside that root, or a
   checkout mismatch or missing Git revision. A new target file may not exist
   yet; its parent must. For a specifically named non-Git project, add
   `--allow-non-git` and record that no revision is available.
2. **Pin the starting truth.** Record the resolved root, branch or detached HEAD,
   `base_sha`, `candidate_sha` actuel, état du worktree, cible demandée,
   point d'entrée app/service et contrôles. Garde la base initiale épinglée au fil
   des commits ; fais avancer explicitement l'identité du candidat et revérifie les chemins en attente.
   Preserve unrelated edits. If another checkout is newer, compare revisions and
   actual working trees before choosing; "newest" is a measured claim.
3. **Map the route.** Trace user action to entry point, implementation, data,
   outputs, and deployment seam. Name the existing owner of the behavior and
   any dependent consumers. Use `repo-map`, `architecture-engineer`, and
   `root-cause-first` when those seams are uncertain.
4. **Construire à l'endroit résolu.** Attribue des questions distinctes aux
   lecteurs parallèles et des fichiers séparés ou worktrees isolés aux rédacteurs.
   Garde un responsable de l'intégration. Réalise le plus petit changement qui
   ferme la classe de défaut ; applique `repair-loop` à un défaut dans le workflow
   actuel. Suis le play `elite-build` complet lorsqu'il est choisi ou explicitement
   demandé, en réutilisant les étapes valides sans redémarrer. Une revue ou un
   diagnostic rend des constats sans modifications.
5. **Prouver le chemin.** Suis la boucle actuelle RED scellé → correction minimale
   → lint/typage/tests sniper → clean-code-gauntlet. Déduis les contrôles du diff
   agrégé épinglé du candidat ; utilise les vraies commandes du dépôt et indique
   honnêtement les contrôles absents ou inapplicables. Préserve revue disjointe de
   l'auteur et passe complète obligatoire des suites touchées à l'atterrissage.
   Inspecte vraie surface app/CLI et journaux runtime dans le périmètre demandé.
   Note révision/hash exacts déployés et comportement observé ; nomme ce qui n'a pu être exercé.
6. **Promote through the project's own route.** Read its deployment instructions
   and approval rules from that repository. Never transplant a deployment
   command from another project. Re-run the target check before installation
   and verify the running process uses the installed code afterward.

If the destination remains ambiguous, keep read-only investigation moving and
ask for the missing path only after checking available evidence. Never claim a
cross-host installation merely because files were copied; verify discovery in
each host or mark it unverified.

À épuisement d'un quota, sauvegarde **STILL-BUILDING** avec cible vérifiée,
candidat, preuves non résolues et prochaine action exacte. Préserve les limites
initiales ; termine le travail utile autorisé qui ne consomme pas le quota épuisé.
Un contrôle local ne remplace jamais la preuve de livraison demandée.
