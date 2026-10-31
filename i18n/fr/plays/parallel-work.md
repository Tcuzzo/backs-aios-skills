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

## Tâche et limites communes

Applique ce play dans le dossier [BACKS Build Flow](../skills/backs-build-flow/SKILL.md)
actuel. Garde un responsable de l'intégration, le `task_mode` demandé, les
révisions base et candidat épinglées, l'essence opérateur et les preuves actuelles.
Réutilise les textes chargés pertinents ; ce play ajoute ses contrôles métier
sans relancer la tâche.

[bounded-loops](../skills/bounded-loops/SKILL.md) possède échéance initiale et quotas
restants à travers réessais, agents, modèles, revues et relèves. Ne les
réinitialise jamais pour un play imbriqué. À épuisement, sauvegarde
**STILL-BUILDING** avec candidat, preuves, barrières non satisfaites et prochaine
action. Le travail utile autorisé reste dans son quota disponible ; aucun
contrôle absent ne devient une réussite.

## La chaîne

1. [leap-protocol](../skills/leap-protocol/SKILL.md) — décompose en balls avec
   objectifs, specs et périmètres stricts AVANT tout lancement d'agent. Chaque lane
   reçoit dossier actuel, base/candidat épinglés, sceaux RED et quota restant
   alloué. Sa limite ne peut prolonger échéance ou totaux de la mission parente.

2. Spawne des lecteurs, pas des écrivains — ne déploie des sous-agents QUE pour
   du travail surtout en lecture, avec peu de dépendances croisées : recherche,
   exécution de tests, scans de sécurité, notation. Jamais pour écrire du code
   interdépendant.
3. Isole chaque lane — chaque agent parallèle reçoit son PROPRE worktree (un
   checkout séparé du même dépôt). Les conflits remontent alors au merge comme
   de vrais conflits de merge, jamais comme des écrasements silencieux qui
   perdent des données sans prévenir.
4. [clean-code-gauntlet](../skills/clean-code-gauntlet/SKILL.md) — chaque lane
   exécute son gauntlet dans le worktree ou l'isolation permis avant atterrissage.
   Utilise d'abord [sniper-testing](../skills/sniper-testing/SKILL.md) pour vraies
   commandes lint/typage/tests du diff agrégé épinglé ; nomme contrôles absents ou
   N/A. Réutilise un reçu valide seulement pour le même candidat et périmètre de
   contrôle, jamais le vert d'une autre lane pour des octets différents. Une lacune
   de couverture reçoit un fichier supplémentaire distinct, originaux scellés préservés.

5. [blind-tribunal](../skills/blind-tribunal/SKILL.md) — l'agent qui relit
   reçoit un contexte PROPRE, jamais celui de l'auteur. Un contexte partagé
   pourrit et s'auto-approuve.
6. Merge une lane à la fois dans un espace dédié, contrôlé par le code de sortie
   des tests. Le responsable vérifie candidat combiné, consommateurs affectés et
   passe complète obligatoire des suites touchées ; les succès séparés ne prouvent
   pas leur composition. Les affirmations de livraison exigent des preuves sur la cible réelle.

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
