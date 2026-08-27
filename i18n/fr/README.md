> Version canonique en anglais : [README.md](../../README.md) — l'anglais fait foi ; cette traduction peut avoir un temps de retard.

# BACKS AIOS Skills

**Lire ceci en :** [English](../../README.md) · [Español](../es/README.md) · [Português (BR)](../pt-BR/README.md) · [Deutsch](../de/README.md) · [हिन्दी](../hi/README.md) · [简体中文](../zh-CN/README.md)

Un harnais d'agent distillé en 27 skills portables et 8 plays nommés, tirés
d'une plateforme d'agents en production et reconstruits en markdown brut que
n'importe quel agent peut charger.

## Mission

Ce pack existe pour celles et ceux qui, sans lui, seraient exclus des résultats
d'agents d'élite par le prix — les codeurs, les designers, les bâtisseurs qui ne
sont pas ingénieurs plateforme. Le harnais et les skills sont l'égalisateur :
ils portent les humains qui ne peuvent pas se payer les plus gros modèles, et
ils font que le niveau du modèle compte moins. C'est le pari de ce pack : un
petit modèle dans un harnais solide peut battre un gros modèle lâché sans
cadre. Pas besoin de savoir comment le harnais a été construit pour t'en
servir — tu dis les mots déclencheurs, et la discipline se déclenche.

## Philosophie

Trois convictions traversent chaque fichier de ce pack.

**Programmé, pas prompté.** L'agent derrière ce pack parle simplement et refuse
les mauvais coups parce que ces propriétés sont gravées dans le harnais comme
des règles structurelles — hooks, portes, tests — pas suggérées dans un prompt.
Une règle qu'un agent doit se rappeler échoue exactement quand l'agent est le
plus occupé. Alors les règles qui comptent sont imposées là où l'oubli est
impossible : dans le harnais, pas dans la mémoire du modèle.

**Les machines ne pensent pas — elles distillent.** Donne à un modèle rien de
réel à travailler, et il compresse du vide — une réponse fausse dite avec
aplomb. Donne au même modèle le bon contexte, et il tombe juste. Ce qu'on
appelle raisonner, c'est distiller du contexte : le modèle compresse ce qu'on
lui a donné en une réponse. Raisonner sans recherche, c'est halluciner. C'est
pour ça que les skills existent. Un skill, c'est le contexte AVEC lequel un
agent raisonne pendant qu'il raisonne SUR une chose — il porte l'agent de la
compréhension de haut niveau jusqu'à la profondeur du sujet, pour que la
distillation ait du réel à distiller.

**Ne raisonner que là où le raisonnement est le seul outil qui marche.** Tout
ce qui est déterministe appartient au harnais — portes, tests, hooks, budgets.
Le raisonnement du modèle n'est dépensé que là où il gagne son coût : le
jugement, le design, la lecture de l'intention. C'est cette séparation qui rend
le pack égalisateur de modèles : le harnais fait le gros du travail, et le
niveau du modèle cesse de décider du résultat.

## Démarrage rapide

### Option 1 — plugin Claude Code

    /plugin marketplace add Tcuzzo/backs-aios-skills
    /plugin install backs-aios

Puis tape `/optimus` pour démarrer le socle. Les skills se chargent, les
commandes de play deviennent disponibles, et le hook d'ancrage arrive activé
(kill-switch : `AIOS_GATE=off`).

### Option 2 — manuel

Dépose les dossiers de `skills/` dans le répertoire de skills de ton agent et
dis les mots déclencheurs. Les chemins par agent — Claude Code, tout runtime
Agent Skills, OpenClaw, Hermes, une boucle API nue — sont dans
[INSTALL.md](INSTALL.md).

| Quand tu veux… | Dis… |
| --- | --- |
| Un truc a cassé | « repair loop » (ou « boucle de réparation ») |
| Construire une fonctionnalité | `/elite-build` (plugin) ou lis `plays/elite-build.md` (manuel) |
| C'est assez bon pour livrer ? | « clean code gauntlet » |
| Vérifie mon travail, à l'aveugle | « blind tribunal » (ou « tribunal à l'aveugle ») |
| Je suis perdu — et maintenant ? | « wayfinder » |
| La demande est de la prose floue | « prose is the spec » (ou « la prose est la spec ») |

Les déclencheurs anglais marchent toujours ; les équivalents français sont
ajoutés dans les descriptions des skills de ce miroir.

## Comment ça marche

- **Les skills** sont des disciplines unitaires. Chacun porte ses mots
  déclencheurs dans sa description, des étapes numérotées, des règles dures qui
  font échouer le skill, et des liens vers les skills qui vont avec. Un fichier
  chacun : `skills/<name>/SKILL.md`.
- **Les plays** sont des combos nommés. Un play déclenche des skills dans un
  ordre fixé et liste les barrières dures qui bloquent un atterrissage. Un
  fichier chacun : `plays/<name>.md`. Le wireframe de chaque play marque un
  **Lord of the Loop** — le maître de la boucle qui pilote l'itération jusqu'à
  ce que la barrière d'atterrissage soit verte ; le rôle est défini dans
  [NAMING.md](NAMING.md#lord-of-the-loop).
- **Les commandes** sont les entrées slash que le plugin installe — chacune
  charge un play ou un skill et l'exécute. Un fichier chacune dans `commands/`.
- **La convention de nommage** — pourquoi les skills sont des groupes nominaux,
  les commandes des verbes, et le socle une loi — est dans
  [NAMING.md](NAMING.md).
- **Les tampons d'effort** — l'affirmation de coût en une ligne de chaque skill
  (free / light / heavy) et la ligne Weight qui clôt chaque play sont décodées
  dans [NAMING.md](NAMING.md#tampons-deffort).

## Les skills

| Skill | Ce qu'il fait |
| --- | --- |
| [absorb](skills/absorb/SKILL.md) | Adopter une capacité open source existante et la ré-ingénierer en skill natif, au lieu d'en construire un doublon. |
| [blind-eval](skills/blind-eval/SKILL.md) | Juger un changement sur ses mérites, auteur masqué, puis garder ou annuler. Seul un gain prouvé atterrit. |
| [blind-tribunal](skills/blind-tribunal/SKILL.md) | Des jurés à l'aveugle, de familles de modèles différentes, notent le changement, une grille de lecture chacun. Chaque trouvaille devient un test qui échoue. Boucle jusqu'à ce que tous passent. |
| [bounded-loops](skills/bounded-loops/SKILL.md) | Plafonds de budget, checkpoints et kill-switchs sur chaque boucle. Rend le martelage d'une API structurellement impossible. |
| [clean-code-gauntlet](skills/clean-code-gauntlet/SKILL.md) | Une barre de qualité déterministe : tests sniper, le score CRAP (complexité x couverture), tests de mutation bornés, puis une légère revue de goût. |
| [decision-bar](skills/decision-bar/SKILL.md) | Une seule barre pour chaque décision : seuls le goût, la vision ou le risque destructeur remontent à l'humain. Tout le reste s'exécute. |
| [design-taste](skills/design-taste/SKILL.md) | Livrer du visuel qui a l'air conçu, pas généré : les design tokens d'abord, la critique sur capture d'écran, une barrière d'accessibilité dure. |
| [fleet-ladder](skills/fleet-ladder/SKILL.md) | Résoudre l'échelle de modèles en direct : sonder ce qui est debout, redescendre dans l'ordre, échouer bruyamment quand l'échelle est épuisée. |
| [gpu-dispatch](skills/gpu-dispatch/SKILL.md) | Un modèle par GPU, aucun débordement vers la RAM système, la carte reste chaude pendant la boucle, déchargement en fin de boucle. |
| [guided-steps](skills/guided-steps/SKILL.md) | Scripter les étapes que seul un humain peut faire — dashboards, credentials, secrets — étape par étape, en capturant chaque valeur. |
| [human-calibration](skills/human-calibration/SKILL.md) | Construire un profil de comment cet humain pense, décide et veut qu'on lui parle, puis piloter tout le build à travers. |
| [incident-closure](skills/incident-closure/SKILL.md) | « Répare-le » veut dire une fermeture complète — cause racine avec preuves, test qui échoue, vert, preuve en direct — jamais un menu d'options renvoyé à l'humain. |
| [intent-compiler](skills/intent-compiler/SKILL.md) | Lire le langage naturel d'un humain — dialecte, métaphore, raccourcis — comme une spec complète, puis l'exécuter en entier. Chaque dialecte est une grammaire valide ; le skill lit la culture comme un contexte avec sa logique interne propre, jamais comme un stéréotype. |
| [invariant-floor](skills/invariant-floor/SKILL.md) | Les lois numérotées que chaque changement autonome doit satisfaire avant d'atterrir. Le socle sur lequel tout le pack tient debout. |
| [leap-protocol](skills/leap-protocol/SKILL.md) | Découper le gros travail en balls indépendamment possédables, les répartir sur des builders parallèles dans des worktrees isolés, réconcilier par une seule colonne d'écriture. |
| [live-research](skills/live-research/SKILL.md) | Un agent de recherche parallèle lit la source vivante — READMEs, docs, le vrai code — pour que le raisonnement s'ancre dans ce qui est vraiment là, pas dans la mémoire. |
| [model-fusion](skills/model-fusion/SKILL.md) | Un panel de modèles rédige en parallèle, un juge indépendant choisit, le gagnant est validé contre l'intention d'origine. |
| [optimus](skills/optimus/SKILL.md) | Pas de code tant que le harnais n'est pas chargé. Un hook déterministe bloque les outils qui modifient tant que l'agent n'a pas lu les règles. |
| [human-voice](skills/human-voice/SKILL.md) | La barre sans-diplôme : si la lecture exige un diplôme, réécris. Garde l'idée entière en enlevant les tics de machine. |
| [red-first](skills/red-first/SKILL.md) | Commiter un test dont l'échec est prouvé avant que le build commence. Le builder n'a pas le droit d'y toucher. Un grader vérifie qu'il n'a jamais bougé. |
| [repair-loop](skills/repair-loop/SKILL.md) | La boucle de correction complète : s'ancrer dans le socle, reproduire, test rouge, corriger la classe, vérifier sur le vrai chemin, notation indépendante, atterrir. |
| [root-cause-first](skills/root-cause-first/SKILL.md) | Pas de correctif sans enquête. Reproduire à la demande, instrumenter les frontières, remonter la donnée jusqu'à la source. |
| [seam-engineering](skills/seam-engineering/SKILL.md) | Corriger la classe de faille une fois, à sa primitive partagée, balayer chaque occurrence sœur, poser un garde qui attrape le prochain contrevenant. |
| [session-handoff](skills/session-handoff/SKILL.md) | Compacter une session en un seul fichier plat qu'un agent tout neuf peut lire à froid et continuer. Secrets caviardés. |
| [sniper-testing](skills/sniper-testing/SKILL.md) | Ne lancer que les tests qui couvrent ce que tu as touché. Tuer le théâtre de mocks — les tests qui passent pendant que la capacité est cassée. |
| [understanding-gates](skills/understanding-gates/SKILL.md) | Verrouiller Design, Plan, Build, Test et Ship avec des verdicts approuver/réviser/rejeter, pour que le build colle toujours à la demande. |
| [wayfinder](skills/wayfinder/SKILL.md) | Perdu ? Tracer une carte de décision jusqu'à la destination, au lieu de poser la question à l'humain. |

## Les plays

| Play | Ce qu'il déroule |
| --- | --- |
| [elite-build](plays/elite-build.md) | Le play maître pour tout build, correctif ou uplift : lire l'intention, verrouiller le plan, prouver le rouge, construire, tester serré, noter à l'aveugle, atterrir prouvé en direct. |
| [agent-builds](plays/agent-builds.md) | Construire des agents et des services : les primitives déterministes font le gros du travail ; le modèle ne raisonne que là où le raisonnement est le seul outil qui marche. |
| [web-app-builds](plays/web-app-builds.md) | Des apps et des sites web à la structure propre et à la chaîne d'approvisionnement défendue — l'hygiène des dépendances est le play, pas une réflexion d'après-coup. |
| [design-taste](plays/design-taste.md) | Une UI qui a l'air conçue, pas générée : séparer la fabrique du goût de l'implémentation, fixer les tokens d'abord, donner des yeux à l'agent, verrouiller sur l'accessibilité. |
| [grading-verification](plays/grading-verification.md) | La notation adversariale : un résultat vert est une affirmation, pas une preuve. Le grader attaque, et le socle ne peut pas être truqué. |
| [parallel-work](plays/parallel-work.md) | Répartir le travail entre agents sans qu'ils se marchent dessus : une seule colonne d'écriture, beaucoup de lecteurs. |
| [security-delivery](plays/security-delivery.md) | La porte de livraison pour tout ce qu'un client ou une autre machine va exécuter. Sûr par construction, pas par mémoire. |
| [bughunt](plays/bughunt.md) | Une chasse aux bugs bornée et parallèle : tracer la carte, déployer les chercheurs, vérifier chaque trouvaille de façon adversariale, fermer des coutures entières. |

## Marche au mieux avec

Ces skills sont la couche portable de **BACKS AIOS**, une plateforme d'agents
construite par [Tcuzzo](https://github.com/Tcuzzo) — un système indexé en
graphe, imposé par des portes, où c'est le harnais, pas le modèle, qui tient la
discipline. Le système complet — son design mémoire, ses profils de
comportement de modèles, son graphe de code — n'est pas dans ce pack. Les
skills tiennent quand même debout seuls sur n'importe quel agent : Claude Code,
OpenClaw, Hermes, Codex, Cursor, ou une boucle API nue. Plus ton agent a
d'autonomie, plus le socle se rentabilise.

## Crédit

Composition et conversion par [Tcuzzo](https://github.com/Tcuzzo). Certains
skills portent des crédits de charpente pour les travaux publiés qu'ils
greffent ; ils sont notés en ligne et rassemblés dans [NOTICE.md](../../NOTICE.md).
Sous licence [MIT](../../LICENSE). Les contributions sont les bienvenues — garde les
crédits intacts.

Note du miroir : LICENSE, NOTICE.md, CITATION.cff, `commands/`, `hooks/` et
`.claude-plugin/` restent volontairement en anglais (texte légal, citations
factuelles, câblage exécutable) et ne sont pas dupliqués ici.
