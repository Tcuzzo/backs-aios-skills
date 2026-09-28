---
name: "seam-engineering"
description: "À utiliser pour réparer un bug ou clôturer un audit ou une chasse aux bugs. Fixe la classe de défaut une fois à sa primitive partagée, balaie chaque occurrence sœur, pose un garde qui attrape la prochaine instance, et clôt chaque constat remonté — aucun report silencieux. Trigger words: seam, class fix, whole-seam closure, point patch, structural guard, do it right the first time, couture, fix de classe, clôture de couture entière, patch ponctuel, garde structurel, bien faire du premier coup."
license: "MIT"
---

# Seam Engineering
**Effort:** free — pure discipline de réparation : un correctif de classe à la primitive partagée au lieu de N rustines ponctuelles. Élimine : le même bug réparé encore et encore à chaque site frère, et la trouvaille moyenne remise à plus tard qui devient le bug mystère que personne ne trouve dans six mois.

Une couture est fermée correctement et complètement, ou elle n'est pas fermée.
Un patch rapide aujourd'hui, c'est le bug que personne ne retrouvera dans six
mois. Ce skill transforme un rapport de bug en une classe de bugs fermée.

## Quand le lancer

Toute réparation : un bug signalé, un test qui échoue, une liste de constats
d'un audit ou d'une chasse aux bugs. Surtout quand tu sens l'envie de
« juste patcher ici ».

## Les étapes

1. **Cause racine avec preuve.** Fixe la cause, pas le symptôme. Avant
   d'écrire le fix, montre la preuve : une repro en échec, une ligne de log,
   une trace qui pointe la vraie couture. Un fix sans preuve est une
   supposition.
2. **Nomme la CLASSE du défaut.** Demande : quelle famille d'erreur est-ce, et
   où ailleurs la même erreur peut-elle vivre ? Écris la classe en une phrase.
3. **Fixe verticalement — une fois, à la primitive partagée.** La primitive
   partagée est la fonction ou le module unique par lequel chaque occurrence
   passe. Fixe-la là. Jamais N patchs ponctuels. Jamais
   marquer-le-mauvais-cas-et-compenser.
4. **Balaie horizontalement.** Débusque chaque occurrence sœur de la classe et
   fixe-les dans le même changement, pas « plus tard ».
5. **Pose un garde structurel.** Un test ou un check automatisé qui échoue sur
   la PROCHAINE instance de la classe. La classe reste fermée parce que
   quelque chose la surveille, pas parce que tout le monde s'en souvient.
6. **Ferme la couture entière.** Liste chaque constat que la chasse a fait
   remonter. Avant d'atterrir, chacun est soit fixé et vert, soit porteur d'un
   verdict « pas un bug » explicite, enregistré, avec preuve. Jamais de report
   silencieux. Jamais de « garé dans un doc ».

## Règles dures

- **Une réparation qui ajoute une nouvelle condition d'échec est elle-même un
  bug.** Un helper de rollback qui peut crasher, un nettoyage qui abandonne de
  l'état en rade, un test édité pour bénir le défaut qu'il devait attraper —
  tous des bugs. Reconçois le changement comme une unité atomique, ou comme
  une machine à états explicite et sûre au crash. Ne maquille jamais.
- **« Fixé les critiques ; le reste en follow-up » fait échouer le skill.**
  C'est exactement l'habitude que ce skill existe pour tuer. Un bug moyen
  reporté est le futur bug mystère. Chaque constat sur la couture compte
  pareil.
- **« Assez bien pour atterrir » n'est pas un statut.** Si la couture n'est
  pas juste, continue d'itérer — lève le blocage, escalade vers un modèle ou
  un relecteur plus fort, réessaie — jusqu'à ce qu'elle le soit.
- **Un patch ponctuel à côté d'une primitive partagée existante fait échouer
  le skill.** Si une primitive possède déjà la couture, le fix passe par
  elle ; un fix de contournement recrée la classe.
- **Un « pas un bug » adjugé exige une preuve,** pas un vote. Enregistre ce
  qui a été vérifié et pourquoi le constat ne tient pas.

## Fonctionne bien avec

- [root-cause-first](../root-cause-first/SKILL.md) — la discipline d'enquête
  derrière l'étape 1.
- [red-first](../red-first/SKILL.md) — le test en échec qui prouve le fix, et
  le patron de garde structurel de l'étape 5.
- [sniper-testing](../sniper-testing/SKILL.md) — tests ciblés pendant
  l'itération ; une passe complète à l'atterrissage.
- [repair-loop](../repair-loop/SKILL.md) — la boucle de bout en bout dans
  laquelle cette discipline tourne.
- [incident-closure](../incident-closure/SKILL.md) — « répare » veut dire une
  clôture complète, jamais un menu d'options.
