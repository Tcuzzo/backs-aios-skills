# Elite Build — le play maître

Le play par défaut pour toute demande « construis X », « répare X » ou « fais
monter X d'un cran ». L'humain énonce le but une seule fois ; ce play assemble
tout l'environnement pour qu'il n'ait jamais à ré-expliquer la base. Lis
l'intention, charge l'humain, verrouille le plan, prouve le rouge, construis,
teste serré, mesure, note à l'aveugle, atterris.

## Quand le lancer

Tout build, correctif ou uplift avec de vrais enjeux. Une retouche triviale
d'une ligne peut filer droit vers
[sniper-testing](../skills/sniper-testing/SKILL.md) et atterrir.

## La chaîne

0. [optimus](../skills/optimus/SKILL.md) — démarre le harnais avant la moindre
   édition. Le socle se charge en premier, chaque session, chaque fois.
1. [intent-compiler](../skills/intent-compiler/SKILL.md) — lis la demande comme
   la spec, en entier. Déduis l'intention avant de faire remonter la moindre
   décision de livraison ou d'option. Ne présente jamais un menu d'options quand
   une solution claire existe — résous-la.
2. [human-calibration](../skills/human-calibration/SKILL.md) — charge le profil
   validé de l'humain et applique-le. Ne ré-interroge jamais un humain que tu
   connais déjà.
3. [understanding-gates](../skills/understanding-gates/SKILL.md) — Design →
   Plan → Build → Test → Ship, chaque étape verrouillée. Avant tout design : lis
   ce qui existe via [live-research](../skills/live-research/SKILL.md),
   réutilise ce qui est écrit, cartographie toute la topologie. La réponse est
   presque toujours déjà écrite quelque part.
4. [wayfinder](../skills/wayfinder/SKILL.md) — perdu à une étape ? Trace la
   route à partir des preuves. Ne pose jamais à l'humain une question à laquelle
   les preuves peuvent répondre.
5. [red-first](../skills/red-first/SKILL.md) — écris le test de contrat qui
   échoue et commite-le AVANT de lancer le moindre builder. Le builder n'a pas
   le droit de toucher ce test.
6. Construis. Déploie des lanes parallèles par défaut — ne sérialise jamais ce
   qui peut tourner en même temps. Chaque lane reçoit sa propre branche de
   travail ou son propre worktree. Solo, une seule session ? Une lane EST le
   déploiement — construis sur une branche de travail et continue. (Un worktree
   est un second checkout du même dépôt dans un autre dossier, pour que deux
   builders ne touchent jamais les mêmes fichiers.) Résous les builders via
   [fleet-ladder](../skills/fleet-ladder/SKILL.md) ; combine les brouillons avec
   [model-fusion](../skills/model-fusion/SKILL.md). Pour un bug, déroule le
   [repair-loop](../skills/repair-loop/SKILL.md) et ferme la CLASSE à la couture
   partagée selon [seam-engineering](../skills/seam-engineering/SKILL.md).
7. [sniper-testing](../skills/sniper-testing/SKILL.md) — des runs ciblés
   uniquement pendant l'itération ; l'unique passe complète des modules touchés
   attend l'atterrissage (étape 10).
8. [clean-code-gauntlet](../skills/clean-code-gauntlet/SKILL.md) — mesure avant
   d'atterrir : suite sniper, score de risque complexité-fois-couverture sous
   ton plafond, puis tests de mutation jusqu'à zéro survivant. Mesure le code ;
   ne le juge jamais à l'œil.
9. [blind-eval](../skills/blind-eval/SKILL.md), puis
   [blind-tribunal](../skills/blind-tribunal/SKILL.md) — une enveloppe dont
   l'auteur est masqué part vers des graders d'une autre famille de modèles que
   le builder. Le builder ne note jamais son propre travail. Chaque trouvaille
   d'un juré devient un nouveau test rouge ; on reconvoque jusqu'à ce que chaque
   juré passe. Config solo ? Dégrade selon la règle « Solo rig » de
   blind-tribunal — et nomme la barrière affaiblie dans le rapport
   d'atterrissage.
10. Atterris — merge proprement, fais tourner UNE passe complète sur les suites
    des modules touchés, redémarre le vrai service, et prouve le comportement
    sur la propre surface de l'humain (la page qu'il charge, la commande qu'il
    lance) — jamais une sonde par procuration. Puis rends compte.

## Barrières dures (une seule au rouge bloque l'atterrissage)

- Le test qui échoue a été commité avant le build et n'a pas bougé — le grader
  vérifie que le diff du fichier de test est vide.
- Le builder n'est jamais le grader, et le grader vient d'une autre famille de
  modèles.
- Chaque trouvaille remontée est fermée, ou tranchée « pas un bug » avec des
  preuves enregistrées. Jamais reportée en silence. Fermeture de la couture
  entière — la couture, c'est l'endroit partagé du code où vit cette classe de
  bug — ou pas d'atterrissage.
- Preuve en direct sur la vraie surface de l'humain. Des tests verts avec une
  capacité cassée, c'est un échec, pas un succès.
- Rends compte en deux mots — PROVEN ou STILL-BUILDING — dans
  [human-voice](../skills/human-voice/SKILL.md). Proven veut dire atterri, plus
  noté indépendamment, plus démontré en direct.
- Ne commite que les fichiers de ce changement — jamais le travail en cours
  d'une autre session.

## Marche bien avec

- [optimus](../skills/optimus/SKILL.md) — recharger le socle après une compaction ou un redémarrage
- [invariant-floor](../skills/invariant-floor/SKILL.md) — le socle verrouillé que chaque atterrissage doit respecter
- [decision-bar](../skills/decision-bar/SKILL.md) — ce qui remonte à l'humain vs. ce qui s'exécute
- [bounded-loops](../skills/bounded-loops/SKILL.md) — budgets et kill-switchs sur les longues sessions
- [session-handoff](../skills/session-handoff/SKILL.md) — sceller l'état avant de s'arrêter
