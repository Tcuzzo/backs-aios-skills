# Play : Parallel Work

Comment répartir le travail entre agents sans qu'ils se marchent dessus. La
règle qui paie tout le reste : une seule colonne d'écriture, beaucoup de
lecteurs.

## Quand le lancer

- Une tâche se découpe en recherche, scans, tests ou notation qui peuvent
  tourner en même temps.
- Plus d'un agent va toucher le même dépôt dans la même fenêtre.
- Tu es tenté de laisser deux agents écrire du code en parallèle. Lis ceci
  d'abord.

## La chaîne

1. [leap-protocol](../skills/leap-protocol/SKILL.md) — décompose le travail en
   balls avec objectifs, specs et périmètres de fichiers stricts AVANT de
   spawner le moindre agent.
2. Spawne des lecteurs, pas des écrivains — ne déploie des sous-agents QUE pour
   du travail surtout en lecture, avec peu de dépendances croisées : recherche,
   exécution de tests, scans de sécurité, notation. Jamais pour écrire du code
   interdépendant.
3. Isole chaque lane — chaque agent parallèle reçoit son PROPRE worktree (un
   checkout séparé du même dépôt). Les conflits remontent alors au merge comme
   de vrais conflits de merge, jamais comme des écrasements silencieux qui
   perdent des données sans prévenir.
4. [clean-code-gauntlet](../skills/clean-code-gauntlet/SKILL.md) — chaque lane
   fait tourner son propre gauntlet de qualité dans son propre worktree avant de
   demander à atterrir. Dry-run d'abord, pour que la lane connaisse son propre
   coût. Aucune lane n'atterrit sur le vert d'une autre.
5. [blind-tribunal](../skills/blind-tribunal/SKILL.md) — l'agent qui relit
   reçoit un contexte PROPRE, jamais celui de l'auteur. Un contexte partagé
   pourrit et s'auto-approuve.
6. Merge une lane à la fois, dans un espace de merge dédié, verrouillé par le
   code de sortie des tests.

## Règles de coordination

- UN agent écrit du code par espace de travail, dans un seul contexte cohérent.
  Des écrivains parallèles prennent des décisions implicites contradictoires
  qu'aucun merge ne peut réconcilier.
- Déclare la propriété des fichiers par agent dès le départ. Chaque agent
  n'édite QUE ses fichiers nommés.
- Coordonne via un tracker (issues, tickets) — jamais via un fichier checklist
  partagé dans l'arbre de travail. Ce fichier est lui-même une surface de
  conflit de merge, et il pousse deux agents à prendre la même tâche.
- Chaque sous-agent renvoie un résumé distillé — les faits clés, les décisions,
  les points ouverts, une page ou deux — jamais sa transcription complète.
- Persiste le plan, la spec et les décisions sur disque, et relis-les. Les
  longues sessions compactent le contexte et perdent des instructions en
  silence ; les règles qui doivent toujours s'appliquer vivent dans le fichier
  toujours chargé, nulle part ailleurs.

## Discipline de merge

- Verrouille CHAQUE merge sur le code de sortie des tests avant qu'il atterrisse.
  Une suite rouge bloque le merge. Ça seul élimine la plus grande part de la
  casse causée par les agents.
- Merge dans un espace de merge dédié, puis vérifie le résultat aux stats :
  nombre de fichiers, diffstat, les fichiers nommés de chaque lane bien
  présents. Un merge qui perd en silence les fichiers d'une lane est LE mauvais
  merge par excellence — vérifie-le à chaque fois.

## Barrières dures — une seule suffit à faire échouer le play

- Deux agents qui écrivent du code dans le même espace de travail en même temps.
- Une lane qui édite hors de son périmètre de fichiers déclaré.
- Un merge atterri sans code de sortie vert, ou sans vérification aux stats.
- Un relecteur qui a partagé son contexte avec l'auteur.
- Une lane qui atterrit sur les résultats de tests d'une autre, ou qui mocke la
  couture qu'elle a changée.

**Weight:** heavy par conception — la décomposition leap, un gauntlet par voie, et un tribunal au contexte propre — la dépense ne se rentabilise que quand le travail est assez gros pour être découpé, et c'est le seul moment où lancer ce play.
