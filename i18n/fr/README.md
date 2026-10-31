> Version canonique en anglais : [README.md](../../README.md) — l'anglais fait foi ; cette traduction peut avoir un temps de retard.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../../assets/reflex-seam-dark.svg">
  <img alt="La couture réflexe. À gauche, un runtime déterministe possède l'état, les fichiers, les règles et les tests. À droite, un noyau de jugement du modèle possède l'inférence, la politique, la réversibilité et la priorité. Entre les deux court une couture dentelée. Les signaux de décision passent du modèle au runtime, et les mises à jour d'état repassent en sens inverse. Un changement d'état non autorisé est refusé à voix haute." src="../../assets/reflex-seam-light.svg">
</picture>

# BACKS AIOS Skills

**Lire ceci en :** [English](../../README.md) · [Español](../es/README.md) · [Português (BR)](../pt-BR/README.md) · [Deutsch](../de/README.md) · [हिन्दी](../hi/README.md) · [简体中文](../zh-CN/README.md)

**Le modèle décide. Le runtime possède l'état, les fichiers et les règles — et si le
modèle cherche un état qui ne lui appartient pas, le système échoue à voix haute au lieu
de deviner.**

Cette ligne, c'est le **Reflex Seam**, installé sur un agent que vous utilisez déjà.
Le hook de contexte livre avant le travail les vrais textes d'Optimus, Yoke et
Build Flow. Il recharge le contexte manquant sans bloquer les outils ni retirer
l'ancrage acquis. L'agent travaille avec les règles lues et des preuves vérifiables.

Deux règles l'accompagnent. **Pas de théâtre de mocks :** un test qui passe alors que la
chose est cassée est un mensonge, donc les tests vérifient des effets réels. **Celui qui
construit ne note pas :** le test qui échoue s'écrit en premier, et quelque chose qui n'a
pas écrit le code doit le valider.

Un harnais avec **62 dossiers de skills** : **54 dossiers hors commandes**
(alias de compatibilité compris), **8 entrées de plays** et **15 adaptateurs de commandes**.
Les 8 plays nommés et leurs méthodes sont tirés
d'une plateforme d'agents en production et reconstruits en markdown brut que
n'importe quel agent peut charger.

Pour apprendre visuellement, consulte le [guide des skills et des boucles](../../docs/FLOWCHARTS.md).

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
commandes de play deviennent disponibles, et le hook de contexte activé livre
les textes sans bloquer d'outils (kill-switch : `AIOS_GATE=off`).

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
- **Les plays** combinent méthodes et contrôles métier dans le dossier Build Flow
  existant. Un responsable conduit l'itération bornée ; tous les contrôles requis
  restent nécessaires avant atterrissage. Un fichier chacun : `plays/<name>.md`.
  Le rôle est décrit dans [NAMING.md](NAMING.md#lord-of-the-loop).
- **Les commandes** sont les entrées slash que le plugin installe — chacune
  charge un play ou un skill et l'exécute. Un fichier chacune dans `command-adapters/`.
- **La convention de nommage** — pourquoi les skills sont des groupes nominaux,
  les commandes des verbes, et le socle une loi — est dans
  [NAMING.md](NAMING.md).
- **Les tampons d'effort** — l'affirmation de coût en une ligne de chaque skill
  (free / light / heavy) et la ligne Weight qui clôt chaque play sont décodées
  dans [NAMING.md](NAMING.md#tampons-deffort).

## Build Flow et Operator Essence

[Build Flow](skills/backs-build-flow/SKILL.md) conserve une tâche, un responsable
et un budget restant partagé. Il commence dès que le contexte permet d'agir et
exécute RED → GREEN borné, les vraies commandes lint/typage/tests du projet et
Clean Code Gauntlet. Les fichiers RED scellés restent intacts ; les nouvelles
lacunes reçoivent des tests distincts.

[Operator Essence](skills/operator-essence/SKILL.md) fournit un contexte privé
étayé. Si le fichier manque ou vieillit, le workflow d'insights disponible est
recherché et tenté une fois ; sans invocation disponible, l'historique pertinent
autorisé sert de recours explicitement signalé. Observations qualitatives et
comptes quantitatifs gardent sources, dénominateurs, incertitudes et contre-exemples.
Demande et corrections actuelles priment. Les spécialistes réutilisent cet extrait
et reviennent au même responsable de tâche.

Ce miroir contient les **54 dossiers hors commandes** et **8 plays**. Les
**15 adaptateurs** restent dans `command-adapters/` à la racine ; l'installation
ajoute les huit entrées de commande en skills et fusionne scripts et références
canoniques avec les textes traduits.

## Les skills

| Skill | Ce qu'il fait |
| --- | --- |
| [absorb](skills/absorb/SKILL.md) | Adopter une capacité open source existante et la ré-ingénierer en skill natif, au lieu d'en construire un doublon. |
| [blind-eval](skills/blind-eval/SKILL.md) | Juger un changement sur ses mérites, auteur masqué, puis garder ou annuler. Seul un gain prouvé atterrit. |
| [blind-tribunal](skills/blind-tribunal/SKILL.md) | Des jurés examinent dans des sessions fraîches disjointes de l'auteur. Les constats étayés reçoivent RED distinct et réparation dans le budget restant ; tous les jurés requis doivent valider avant atterrissage. |
| [bounded-loops](skills/bounded-loops/SKILL.md) | Transmettre une échéance et des quotas communs à travers réessais, agents, modèles, revues et relèves ; sauvegarder honnêtement à épuisement. |
| [clean-code-gauntlet](skills/clean-code-gauntlet/SKILL.md) | Lint/typage/tests ciblés, complexité et couverture mesurées, mutation isolée bornée et revue de design indépendante sur le même candidat. |
| [decision-bar](skills/decision-bar/SKILL.md) | Une seule barre pour chaque décision : seuls le goût, la vision ou le risque destructeur remontent à l'humain. Tout le reste s'exécute. |
| [design-taste](skills/design-taste/SKILL.md) | Livrer du visuel qui a l'air conçu, pas généré : les design tokens d'abord, la critique sur capture d'écran, une barrière d'accessibilité dure. |
| [fleet-ladder](skills/fleet-ladder/SKILL.md) | Résoudre l'échelle de modèles en direct : sonder ce qui est debout, redescendre dans l'ordre, échouer bruyamment quand l'échelle est épuisée. |
| [gpu-dispatch](skills/gpu-dispatch/SKILL.md) | Un modèle par GPU, aucun débordement vers la RAM système, la carte reste chaude pendant la boucle, déchargement en fin de boucle. |
| [guided-steps](skills/guided-steps/SKILL.md) | Scripter les étapes que seul un humain peut faire — dashboards, credentials, secrets — étape par étape, en capturant chaque valeur. |
| [human-calibration](skills/human-calibration/SKILL.md) | Appliquer préférences confirmées pertinentes et observations étayées d'Operator Essence ; les corrections actuelles priment. |
| [incident-closure](skills/incident-closure/SKILL.md) | « Répare-le » veut dire une fermeture complète — cause racine avec preuves, test qui échoue, vert, preuve en direct — jamais un menu d'options renvoyé à l'humain. |
| [intent-compiler](skills/intent-compiler/SKILL.md) | Traduire une fois une demande actuelle ambiguë en contrat d'action fondé, sans inventer personnalité, tolérance au risque ou autorité supplémentaire. |
| [invariant-floor](skills/invariant-floor/SKILL.md) | Les lois numérotées que chaque changement autonome doit satisfaire avant d'atterrir. Le socle sur lequel tout le pack tient debout. |
| [leap-protocol](skills/leap-protocol/SKILL.md) | Découper le gros travail en balls indépendamment possédables, les répartir sur des builders parallèles dans des worktrees isolés, réconcilier par une seule colonne d'écriture. |
| [live-research](skills/live-research/SKILL.md) | Un agent de recherche parallèle lit la source vivante — READMEs, docs, le vrai code — pour que le raisonnement s'ancre dans ce qui est vraiment là, pas dans la mémoire. |
| [model-fusion](skills/model-fusion/SKILL.md) | Un panel de modèles rédige en parallèle, un juge indépendant choisit, le gagnant est validé contre l'intention d'origine. |
| [optimus](skills/optimus/SKILL.md) | Charger socle, Optimus, Yoke et Build Flow comme textes réels ; le hook déterministe recharge le contexte sans bloquer les outils. |
| [human-voice](skills/human-voice/SKILL.md) | La barre sans-diplôme : si la lecture exige un diplôme, réécris. Garde l'idée entière en enlevant les tics de machine. |
| [red-first](skills/red-first/SKILL.md) | Commiter un test dont l'échec est prouvé avant que le build commence. Le builder n'a pas le droit d'y toucher. Un grader vérifie qu'il n'a jamais bougé. |
| [repair-loop](skills/repair-loop/SKILL.md) | Mener la même réparation bornée depuis RED réel jusqu'à l'aboutissement demandé via correction de frontière, lint/typage/tests, gauntlet et revue indépendante. |
| [repo-map](skills/repo-map/SKILL.md) | Cartographie d’abord la structure réelle du dépôt, ses points d’entrée, sa configuration et ses chemins d’exécution avant toute modification. |
| [root-cause-first](skills/root-cause-first/SKILL.md) | Pas de correctif sans enquête. Reproduire à la demande, instrumenter les frontières, remonter la donnée jusqu'à la source. |
| [seam-engineering](skills/seam-engineering/SKILL.md) | Corriger la classe de faille une fois, à sa primitive partagée, balayer chaque occurrence sœur, poser un garde qui attrape le prochain contrevenant. |
| [session-handoff](skills/session-handoff/SKILL.md) | Transmettre le même dossier avec base/candidat, sceaux RED, preuves, échéance et budget restant, en respectant la lecture seule. |
| [sniper-testing](skills/sniper-testing/SKILL.md) | Choisir lint, typage, tests de comportement et intégration depuis le diff complet base-candidat ; vérifier effets réels et sceaux RED intacts. |
| [understanding-gates](skills/understanding-gates/SKILL.md) | Verrouiller Design, Plan, Build, Test et Ship avec des verdicts approuver/réviser/rejeter, pour que le build colle toujours à la demande. |
| [wayfinder](skills/wayfinder/SKILL.md) | Perdu ? Tracer une carte de décision jusqu'à la destination, au lieu de poser la question à l'humain. |
| [architecture-engineer](skills/architecture-engineer/SKILL.md) | Examiner frontières architecturales, directions de dépendances et dérive structurelle ; consigner les décisions durables en ADR. |
| [backs-build-flow](skills/backs-build-flow/SKILL.md) | Mener la demande du contexte suffisant à l'aboutissement demandé avec un responsable, un dossier et un budget, via RED/GREEN, lint/typage/tests et gauntlet. |
| [backs-pack-sync](skills/backs-pack-sync/SKILL.md) | Comparer la couverture privée au pack public et n'adopter que des ponts publics rédigés et revus séparément. |
| [backs-session-rollover](skills/backs-session-rollover/SKILL.md) | Passer la main avec un état vérifié et reprendre la même tâche après changement de contexte. |
| [building-with-backs](skills/building-with-backs/SKILL.md) | Vérifier dépôt, checkout et chemin demandés ; prouver le transfert autorisé jusqu'au vrai runtime. |
| [cam-iot-inventory](skills/cam-iot-inventory/SKILL.md) | Examiner inventaires caméra, IoT et Wi-Fi avec identité stable et distinction honnête entre inventaire et image. |
| [co-health](skills/co-health/SKILL.md) | Vérifier santé et preuves des watchdogs à la cadence de l'opérateur. |
| [conscientious-objector](skills/conscientious-objector/SKILL.md) | Observer l'usage vérifiable du harnais, les preuves de qualité et les écarts entre affirmations et code. |
| [context-compiler](skills/context-compiler/SKILL.md) | Alias de compatibilité de context-engineer ; même dossier étayé et même méthode. |
| [context-engineer](skills/context-engineer/SKILL.md) | Reconstruire seulement le contexte manquant utile à l'action ; transmettre base, candidat, autorisation, contexte opérateur et budget restant. |
| [context_engineer](skills/context_engineer/SKILL.md) | Alias de compatibilité de context-engineer avec texte de skill identique octet pour octet. |
| [debugging-engineer](skills/debugging-engineer/SKILL.md) | Enquêter sur régressions difficiles, échecs silencieux et courses concurrentes avec des hypothèses réfutables avant modification. |
| [design-critique](skills/design-critique/SKILL.md) | Évaluer les surfaces produit selon tâche réelle, hiérarchie des preuves, affordances, mouvement, accessibilité et cohérence. |
| [fix-shit](skills/fix-shit/SKILL.md) | Reproduire, sceller et réparer un défaut signalé dans la même tâche bornée, puis rendre les vraies preuves de livraison. |
| [fleet-dispatch](skills/fleet-dispatch/SKILL.md) | Exécuter les routes configurées et rendre les reçus réels du fournisseur, modèle et run. |
| [harness-optimizer](skills/harness-optimizer/SKILL.md) | Mesurer les améliorations du harnais par comparaison bornée référence/candidat, holdouts et preuves durables. |
| [karpathy](skills/karpathy/SKILL.md) | Mener des expériences bornées et mesurées dans un clone jetable en gardant seulement les améliorations prouvées. |
| [operator-essence](skills/operator-essence/SKILL.md) | Établir un contexte privé depuis les preuves qualitatives et quantitatives ; tenter les insights manquants une fois, garder l'incertitude et donner priorité aux instructions actuelles. |
| [operator-intent-deduction](skills/operator-intent-deduction/SKILL.md) | Résoudre les décisions ouvertes depuis demande actuelle, faits vérifiés et contexte étayé, sans figer de règles personnelles. |
| [operator_intent_deduction](skills/operator_intent_deduction/SKILL.md) | Alias de compatibilité de operator-intent-deduction avec texte de skill identique octet pour octet. |
| [osha-bot](skills/osha-bot/SKILL.md) | Observer les watchdogs eux-mêmes pour repérer dérive des règles, défauts de qualité et restrictions cachées. |
| [rea-investigation](skills/rea-investigation/SKILL.md) | Produire des preuves de découverte ou vérification avec REA déjà disponible et revenir au responsable actuel. |
| [reload-vsc-and-verify](skills/reload-vsc-and-verify/SKILL.md) | Identifier l'installation des nouveaux skills, effectuer le rechargement autorisé et vérifier leur découverte réelle. |
| [scrub-plugin-pack-literals](skills/scrub-plugin-pack-literals/SKILL.md) | Détecter et nettoyer les littéraux privés à la frontière partagée de nettoyage avant publication. |
| [truth-audit](skills/truth-audit/SKILL.md) | Examiner en lecture seule runtime réel et défauts pour livrer une spécification de réparation étayée. |
| [turn-and-burn](skills/turn-and-burn/SKILL.md) | Examiner plan de mission, capacités des modèles, skills manquants et leçons existantes avant exécution. |

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

Note du miroir : LICENSE, NOTICE.md, CITATION.cff, `command-adapters/`, `hooks/` et
`.claude-plugin/` restent volontairement en anglais (texte légal, citations
factuelles, câblage exécutable) et ne sont pas dupliqués ici.
