# Play : Grading & Verification

Le play de la notation adversariale. Sa seule conviction : un résultat vert est
une affirmation, pas une preuve. Le grader (l'évaluateur) attaque, et le socle
est construit pour qu'on ne puisse pas le truquer.

## Quand le lancer

- Un changement construit demande à atterrir — du code, de la config, des docs,
  la sortie d'un agent.
- Une suite se dit verte et personne ne l'a vue échouer d'abord.
- Un modèle a construit le travail et il te faut un verdict honnête dessus.

## La chaîne

1. [red-first](../skills/red-first/SKILL.md) — confirme que la suite a échoué
   avec un code de sortie non nul AVANT que le correctif existe. Une suite qui
   n'a jamais été rouge ne prouve rien.
2. [sniper-testing](../skills/sniper-testing/SKILL.md) — vérifie que le builder
   a utilisé des tests ciblés pendant l'itération et n'a fait aucun théâtre de
   mocks sur la couture qu'il a changée.
3. Notation inter-famille — confie le travail à un modèle d'une famille
   DIFFÉRENTE de celle du builder. La notation intra-famille gonfle les taux de
   victoire de façon mesurable — les graders favorisent les leurs ; une autre
   instance de la même famille ne suffit pas.
4. [blind-tribunal](../skills/blind-tribunal/SKILL.md) — pour les changements à
   conséquences, convoque des jurés sur une enveloppe dont l'auteur est masqué.
   Chaque trouvaille devient un nouveau test rouge, et le tribunal se reconvoque
   jusqu'à ce que tous les jurés le fassent passer.
5. [clean-code-gauntlet](../skills/clean-code-gauntlet/SKILL.md) — le grader
   refait tourner le gauntlet lui-même (couverture-contre-complexité, tests de
   mutation bornés). Ne fais jamais confiance au rapport du builder sur ses
   propres chiffres.

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

- Le builder et le grader partagent une famille de modèles.
- La suite ne peut pas être montrée rouge avant le correctif.
- Le fail-to-pass ou le pass-to-pass manque au run noté.
- Un des aveux de faux vert ci-dessus est présent.
- Le grader a cru le rapport du builder au lieu de refaire tourner les
  vérifications lui-même.

**Weight:** des vérifications red et sniper free en amont ; la dépense heavy, c'est le tribunal plus le grader qui relance lui-même le gauntlet — elle se rentabilise sur tout changement qui demande à atterrir, parce qu'un seul faux vert coûte plus cher que toutes les notes réunies.
