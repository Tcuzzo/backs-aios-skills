# Play : Grading & Verification

Le play de la notation adversariale. Sa seule conviction : un résultat vert est
une affirmation, pas une preuve. Le grader (l'évaluateur) attaque, et le socle
est construit pour qu'on ne puisse pas le truquer.

## Quand le lancer

- Un changement construit demande à atterrir — du code, de la config, des docs,
  la sortie d'un agent.
- Une suite se dit verte et personne ne l'a vue échouer d'abord.
- Un modèle a construit le travail et il te faut un verdict honnête dessus.

La notation, en un coup d'œil :

```
+--------------------------------------------+
| 1 red-first  confirm the suite failed --   |<--------------------------+
|   non-zero exit -- BEFORE the fix existed  |  each finding -> a new    |
+--------------------------------------------+  red test -> fix ->       |
| 2 sniper-testing  scoped runs verified;    |  re-convene               |
|   no mock theater on the changed seam      |                           |
+--------------------------------------------+   +---------------------+ |
| 3 cross-family grade -- a model from a     |   |  LORD OF THE LOOP   |-+
|   DIFFERENT family than the builder        |   | one hand drives the |
+--------------------------------------------+   | loop: dispatch,     |
| 4 blind-tribunal  jurors judge an          |-->| judge, loop back    |
|   author-redacted envelope                 |   | until the gate is   |
+--------------------------------------------+   | green. a lane never |
| 5 clean-code-gauntlet  the grader re-runs  |   | lands its own work. |
|   it -- never trust the builder's numbers  |   +---------------------+
+--------------------------------------------+
          |
          | all jurors pass
          v
+--------------------------------------------+
| LANDING GATE -- the two-sided proof:       |
| fail-to-pass AND pass-to-pass, run         |
| hermetically . no fake-green tell .        |
| builder + grader families differ . the     |
| grader re-ran the checks itself            |
+--------------------------------------------+
```

*Dans le schéma : LORD OF THE LOOP = le maître de la boucle, la seule main qui pilote l'itération — dispatch, jugement, rebouclage — jusqu'à ce que la barrière d'atterrissage soit verte ; LANDING GATE = la barrière d'atterrissage — tout au vert, ou pas d'atterrissage.*

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
