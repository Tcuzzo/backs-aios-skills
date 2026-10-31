---
name: fix-shit
description: "Quand l'opérateur signale un comportement cassé, dit fix shit ou stop swallowing errors, ou demande de terminer un bug tenace."
license: MIT
---

# Fix Shit

Utilise cette entrée rapide dans `root-cause-first` et `repair-loop` au sein
de la tâche [BACKS Build Flow](../backs-build-flow/SKILL.md) actuelle. Garde son
unique responsable, son essence opérateur, son `task_mode`, l'identité du candidat
et les preuves ; ne recharge pas un dossier valide et ne lance pas un second cycle.
Un appel direct établit le dossier une fois. Budget restant et échéance de
[bounded-loops](../bounded-loops/SKILL.md) couvrent chaque reproduction, correction,
repli de modèle et revue. Ce skill ne les réinitialise jamais et ne masque pas un signal d'échec.

1. Name the user's broken behavior and the exact surface where it appears.
2. Produis un signal rouge répétable depuis le vrai chemin. Suis l'entrée et
   chaque frontière jusqu'à l'écart entre comportement réel et attendu. Scelle le
   contrat d'échec initial avec [red-first](../red-first/SKILL.md) avant qu'un
   builder modifie la frontière responsable. Une tâche de diagnostic rend ces preuves.
3. Identify the root cause and all callers of the broken seam. Preserve the
   original error in logs or the operator-facing state; a fallback may protect
   the app, but it must not turn failure into false success.
4. Pour une correction autorisée, applique [repair-loop](../repair-loop/SKILL.md)
   dans le workflow : plus petite correction de classe, vraies commandes lint/
   typage/tests ciblées sur le diff agrégé épinglé, puis contrôles de qualité et
   mutation clean-code-gauntlet. Préserve l'original scellé ; une nouvelle lacune
   reçoit un test supplémentaire distinct. Réutilise les étapes déjà vérifiées.
5. Achève revue disjointe de l'auteur (author-disjoint), contrôle des suites affectées à
   l'atterrissage et vérifications du vrai chemin applicatif pour la livraison
   demandée. Vérifie résultat voulu et état d'échec explicite. Un relecteur absent
   est une lacune du runtime, jamais un succès indépendant que l'on s'accorde soi-même.
6. Rends candidat et preuves au responsable de l'intégration. Rapporte PROVEN
   seulement avec revue requise et vraie preuve de livraison ; sinon sauvegarde
   STILL-BUILDING avec échec restant exact et prochaine action. L'épuisement
   préserve travail et limites ; poursuis le travail utile non bloqué seulement
   dans son quota restant.

If the error is intermittent, capture timing and a bounded reproduction rate;
do not infer a cause from one green rerun. For code-location ambiguity, start
with `building-with-backs` and its target check.


## Preuves et revue indépendante

Pour les exécutables distribués, paquets ou comportements demandés à l’exécution, utilise [rea-investigation](../rea-investigation/SKILL.md) et le skill `reverse-engineer-anything` installé séparément lorsque son analyse est utile ; utilise un fournisseur Ghidra existant pour les cibles natives prises en charge. Une preuve statique ne démontre pas le comportement en direct ; n’installe pas silencieusement un fournisseur manquant. Pour adopter une capacité open source, utilise [absorb](../absorb/SKILL.md). Choisis par rôle et capacité avec [fleet-ladder](../fleet-ladder/SKILL.md), sans nom de modèle codé en dur. Si un tribunal est requis, suis [blind-tribunal](../blind-tribunal/SKILL.md) : une nouvelle exécution séparée de l’auteur examine un paquet figé expurgé des données de l’auteur. Signale tout résolveur, relecteur ou preuve manquant comme une lacune du runtime.
