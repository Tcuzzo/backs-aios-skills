# Nommage — comment ce pack nomme les choses, et pourquoi

Dans ce pack, les noms portent du poids. Un agent choisit un skill en matchant
la tâche contre le nom et la description, donc un nom qui dit la mauvaise chose
route le travail vers la mauvaise discipline. La convention ci-dessous garde le
routage honnête.

## Les trois sortes de noms

- **Les skills sont des disciplines en groupe nominal.** Un skill, c'est le
  contexte qu'un agent charge pour raisonner avec — un corps de règles, pas une
  action. Il est donc nommé comme une discipline : `red-first`,
  `seam-engineering`, `sniper-testing`. On charge une discipline ; on ne la
  « lance » pas.
- **Les commandes sont des impératifs.** Une commande est une action avec un
  début et une fin, donc son nom est un verbe, ou le nom du play ou du skill
  qu'elle déclenche : boot, build, hunt, grade, tribunal.
- **Le socle d'invariants est une loi.** `invariant-floor` est le seul skill
  dont tous les autres héritent. Il est nommé pour ce qu'il est — le socle —
  parce que chaque règle dure du pack tient dessus, et qu'aucun skill n'a le
  droit de faire atterrir un changement en dessous.

## Les commandes livrées

| Commande | Déclenche |
| --- | --- |
| `/agent-build` | `plays/agent-builds.md` |
| `/bughunt` | `plays/bughunt.md` |
| `/design-taste` | `plays/design-taste.md` |
| `/elite-build` | `plays/elite-build.md` |
| `/grade` | `plays/grading-verification.md` |
| `/optimus` | `skills/optimus/SKILL.md` |
| `/parallel-work` | `plays/parallel-work.md` |
| `/secure-delivery` | `plays/security-delivery.md` |
| `/tribunal` | `skills/blind-tribunal/SKILL.md` |
| `/web-build` | `plays/web-app-builds.md` |

Que `design-taste` existe à la fois comme skill, play et commande est voulu —
une discipline, trois portes d'entrée : le skill est le contexte, le play est
la recette, la commande est le déclencheur. Sans ambiguïté, parce que la
commande déclenche le play, et le play lie le skill.

## Où vit chaque type d'information

Chaque couche répond à une question différente, et rien n'est dupliqué :

- **Le nom dit le mécanisme.** `blind-tribunal` te dit comment ça marche avant
  même d'ouvrir le fichier : des jurés, aveugles à l'auteur.
- **La description porte les mots déclencheurs.** Le runtime matche tes mots
  contre les descriptions, donc la description contient chaque phrase qu'un
  humain dirait quand il a besoin du skill — y compris les anciens noms (voir
  plus bas).
- **Le corps porte les règles.** Les étapes, les règles dures qui font échouer
  le skill, et les skills qui vont avec. Le corps est la discipline ; le nom et
  la description ne sont que son adresse.

## Un renommage ne casse jamais rien

Quand un skill est renommé, son ancien nom part dans la description comme mot
déclencheur, pour que chaque habitude et chaque doc qui utilisait l'ancien nom
route encore correctement :

- **optimus** garde son nom tel quel — c'est la marque du démarrage, le seul
  nom propre du pack, et la commande que tu tapes en premier (`/optimus`).
- **« yoke »** survit comme mot déclencheur sur `human-calibration` — dis l'un
  ou l'autre, et la même discipline se charge.

Un renommage qui casse un déclencheur existant est une régression, pas un
nettoyage.

## La raison de chaque nom

| Nom | Pourquoi ce nom |
| --- | --- |
| absorb | La discipline de prendre une capacité externe et de la ré-ingénierer en natif, au lieu de la dupliquer. |
| blind-eval | Une évaluation à auteur masqué — l'aveuglement est le mécanisme. |
| blind-tribunal | Un panel de jurés, aveugles à l'auteur, de familles de modèles différentes. Tribunal = panel plus verdict. |
| bounded-loops | La propriété imposée : chaque boucle porte une borne — budget, checkpoint, kill-switch. |
| clean-code-gauntlet | Un gauntlet est une série d'épreuves dures ; le code propre est ce qui y survit. |
| decision-bar | Une seule barre contre laquelle chaque décision est mesurée avant d'avoir le droit d'atteindre l'humain. |
| design-taste | La discipline du goût dans le travail visuel — verrouillée et vérifiée, pas laissée au feeling. |
| fleet-ladder | La flotte de modèles résolue comme une échelle de repli, gravie dans l'ordre. |
| gpu-dispatch | La loi de dispatch du travail GPU : un modèle par carte, chaude pendant toute la boucle. |
| guided-steps | Les étapes que seul un humain peut faire, guidées une par une. |
| human-calibration | Calibrer le build sur l'humain qu'il sert. (S'appelait « yoke » — l'ancien nom survit comme mot déclencheur.) |
| incident-closure | Un incident se ferme complètement — de la cause racine à la preuve en direct — jamais retrié vers l'humain. |
| intent-compiler | Compile le langage naturel en directive exécutable. La prose est le source ; la directive est la sortie. |
| invariant-floor | Le socle des lois numérotées que chaque changement doit franchir. Une loi, pas un conseil. |
| leap-protocol | Le protocole pour propulser le gros travail sur des builders parallèles et le faire atterrir par une seule colonne. |
| live-research | La recherche sur sources vivantes — les docs et le code tels qu'ils sont maintenant — pas la mémoire du modèle. |
| model-fusion | Plusieurs modèles rédigent, un juge indépendant choisit — une fusion de sorties, pas un vote. |
| optimus | La marque du démarrage, gardée comme nom propre. Il démarre le socle ; chaque session commence ici. |
| human-voice | Nommé pour ce qu'il impose : l'agent écrit comme une personne parle, et les idées dures arrivent quand même entières. |
| red-first | Le test qui échoue (rouge) vient en premier, commité avant que le build commence. |
| repair-loop | La boucle de correction complète, nommée pour sa forme : s'ancrer, reproduire, corriger, vérifier, atterrir. |
| root-cause-first | L'ordre des opérations est la règle : la cause avant le correctif, toujours. |
| seam-engineering | Les correctifs atterrissent à la couture — la primitive partagée — jamais en rustines éparpillées. |
| session-handoff | Nommé pour son artefact : un seul fichier de passation qu'une session à froid peut continuer. |
| sniper-testing | Un tir, une cible : ne lancer que les tests qui couvrent ce que tu as touché. |
| understanding-gates | Des portes à chaque étape du build qui vérifient la compréhension, pas seulement la syntaxe. |
| wayfinder | Trouve le chemin quand on est perdu, au lieu de poser la question à l'humain. |
