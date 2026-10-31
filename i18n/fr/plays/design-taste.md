# Design Taste

Le play pour construire une UI qui a l'air conçue, pas générée. Une UI générique
est un bug de WORKFLOW, pas un bug de modèle : sépare la fabrique du goût de
l'implémentation, fixe d'abord des design tokens exacts, donne des yeux à
l'agent, et verrouille sur l'accessibilité.

## Quand le lancer

Tout écran, page, composant, dashboard ou livrable visuel qu'un humain va
regarder. Le premier écran fixe le niveau de tous les suivants — lance ce play
avant lui.

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

1. Utilise intention et essence opérateur établies par Build Flow pour déduire
   le goût demandé par les mots de l'humain. Énonce cette lecture une fois avant d'écrire.

2. [human-calibration](../skills/human-calibration/SKILL.md) — ancre cette
   lecture dans l'historique de l'humain et dans de vraies références étudiées,
   jamais dans une supposition démographique.
3. Émets le fichier de design tokens à trois niveaux EN PREMIER, avant tout
   composant — la spec complète des tokens et la liste des valeurs par défaut
   interdites sont dans [design-taste](../skills/design-taste/SKILL.md).
4. Construis les composants avec le fichier de tokens injecté comme contrainte
   dure. Jamais de hex brut, de valeur en pixels ou de famille de polices codée
   en dur dans un composant.
5. Exécute la boucle capture d'écran → critique selon
   [design-taste](../skills/design-taste/SKILL.md), avec le critique résolu en
   direct via [fleet-ladder](../skills/fleet-ladder/SKILL.md). Chaque critique et
   nouveau rendu consomment le même budget restant ; rends les constats au responsable actuel.

6. Note la grille de goût à 8 axes selon
   [design-taste](../skills/design-taste/SKILL.md).
7. Applique la barrière DURE d'accessibilité WCAG 2.2 selon
   [design-taste](../skills/design-taste/SKILL.md).
8. [clean-code-gauntlet](../skills/clean-code-gauntlet/SKILL.md) — sur le code
   DERRIÈRE les pixels uniquement : résolveurs de tokens, bascules de thème,
   calculateurs de contraste et réducteurs d'état passent avec zéro mutant
   survivant. Une comparaison inversée dans un check de contraste livre un écran
   magnifique et inaccessible. Le gauntlet ne note jamais le goût — grille et
   barrière d'accessibilité restent juges du visuel. Utilise auparavant
   [sniper-testing](../skills/sniper-testing/SKILL.md) pour les vraies commandes
   lint/typage/tests ciblées sur le diff agrégé épinglé. Déclare N/A ou contrôles
   absents honnêtement. Rends du vrai DOM ; un mock ne prouve pas ce que l'humain
   voit. Préserve RED scellés, ajoute des tests distincts pour les lacunes et garde
   revue indépendante, passe complète des suites touchées et preuve du rendu réel.

## Barrières dures (propres au play — les règles dures du skill s'appliquent en plus)

- Le critique travaille dans une session vierge et disjointe de l'auteur ; son modèle est
  résolu en direct via l'échelle de la flotte ; jamais un id de modèle épinglé
  (un pin retiré du service tue tout le critique, en silence).

## Marche bien avec

- [blind-tribunal](../skills/blind-tribunal/SKILL.md) — noter le livrable entier
- [sniper-testing](../skills/sniper-testing/SKILL.md) — cibler les tests de composants

**Weight:** light tout au long de la boucle — la calibration et la passe de critique sur capture d'écran coûtent chacune un run de plus ; l'étape heavy est le gauntlet sur le code derrière les pixels — elle se rentabilise sur tout écran qu'un humain va vraiment regarder.
