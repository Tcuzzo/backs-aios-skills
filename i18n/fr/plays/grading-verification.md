# Play : Grading & Verification

Le play de la notation adversariale. Sa seule conviction : un résultat vert est
une affirmation, pas une preuve. Le grader (l'évaluateur) attaque, et le socle
est construit pour qu'on ne puisse pas le truquer.

## Quand le lancer

- Un changement construit demande à atterrir — du code, de la config, des docs,
  la sortie d'un agent.
- Une suite se dit verte et personne ne l'a vue échouer d'abord.
- Un modèle a construit le travail et il te faut un verdict honnête dessus.

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

1. [red-first](../skills/red-first/SKILL.md) — confirme que la suite a échoué
   avec un code de sortie non nul AVANT que le correctif existe. Une suite qui
   n'a jamais été rouge ne prouve rien.
   Le test en échec est commité avant correction et le builder ne peut y toucher ;
   les octets exacts de son fichier sont le contrat.
2. [sniper-testing](../skills/sniper-testing/SKILL.md) — vérifie les vraies
   commandes lint/typage/tests du dépôt ciblées sur le diff agrégé épinglé, sans
   théâtre de mocks sur la frontière modifiée. Vérifie raisons N/A explicites
   et contrôles manquants. Fige l'identité du candidat pour cette revue.

3. Notation disjointe de l'auteur — confie le travail à un correcteur dont
   l'exécution autrice n'a pas construit le changement, choisi en direct par
   capacité et disponibilité depuis la matrice de barreaux configurée ; la revue utilise une session vierge et disjointe de l'auteur. L'auto-signature de la note par l'exécution qui a construit est
   disqualifiée à la racine.
4. [blind-tribunal](../skills/blind-tribunal/SKILL.md) — pour les changements
   importants, convoque des jurés sur un dossier expurgé de l'auteur dans une
   session fraîche sans conversation héritée. Rends les constats étayés au
   responsable pour RED supplémentaire distinct et réparation bornée ; le RED
   initial reste scellé. Reconvoque sur le candidat révisé figé dans le même
   budget restant. Tous les jurés requis doivent valider avant atterrissage.

5. [clean-code-gauntlet](../skills/clean-code-gauntlet/SKILL.md) — le grader
   refait tourner le gauntlet lui-même (couverture-contre-complexité, tests de
   mutation bornés). Ne fais jamais confiance au rapport du builder sur ses
   propres chiffres.

Respecte la cible immuable du mode revue. Les contrôles qui créent des caches,
modifient le code ou exercent des services ne tournent qu'en isolation permise ;
la mutation ne réécrit jamais les sources figées. Isolation ou support runtime
absents sont des lacunes de preuve, pas une permission de corriger pendant la
revue. Garde la passe complète des suites touchées à l'atterrissage et distingue
contrôles locaux et preuves de surface ou de livraison réelles.

## La preuve à deux faces (les deux, ou pas de pass)

- **Fail-to-pass :** les tests qui étaient rouges sont maintenant verts — le
  correctif est prouvé.
- **Pass-to-pass :** tout ce qui était vert est toujours vert — aucune
  régression.
- Un run qui ne fait qu'AJOUTER des tests qui passent ne satisfait ni l'un ni
  l'autre. Fais tourner les deux de façon hermétique.

## Les gardes anti-faux-vert (un seul suffit à trahir)

- Une trappe sur le code de sortie — un harnais qui sort propre quoi qu'il
  arrive.
- Des sorties codées en dur ou mémorisées à la place de sorties calculées.
- Des tests supprimés, sautés ou affaiblis.
- Tout grader, timer ou scoreur modifié. Un harnais modifié qui passe au vert
  EST l'aveu.
- Un mutant survivant sous une suite verte. Le mutant prouve que les assertions
  n'ont jamais atteint cette branche — du faux vert par définition.

## Dé-biaiser le juge

Le socle mécanique du juge vit dans la section « Débiaiser le juge » de
[blind-eval](../skills/blind-eval/SKILL.md) — applique-la en entier.

## Barrières dures — une seule suffit à faire échouer le play

- L'exécution autrice qui a construit le changement signe elle-même la
  note.
- La suite ne peut pas être montrée rouge avant le correctif.
- Le fail-to-pass ou le pass-to-pass manque au run noté.
- Un des aveux de faux vert ci-dessus est présent.
- Le grader a cru le rapport du builder au lieu de refaire tourner les
  vérifications lui-même.

**Weight:** des vérifications red et sniper free en amont ; la dépense heavy, c'est le tribunal plus le grader qui relance lui-même le gauntlet — elle se rentabilise sur tout changement qui demande à atterrir, parce qu'un seul faux vert coûte plus cher que toutes les notes réunies.
