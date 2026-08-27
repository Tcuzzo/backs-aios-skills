# Play : Bughunt

Une chasse aux bugs bornée et parallèle. Trace la chasse comme une carte,
déploie des chercheurs dessus, vérifie chaque trouvaille de façon adversariale,
et ferme des coutures entières — jamais des symptômes isolés.

## Quand le lancer

- Un audit, un balayage ou une chasse à travers beaucoup de coutures — pas un
  bug signalé isolé (pour ça, prends la boucle de réparation, le repair loop).
- Un backlog de trouvailles à attaquer en parallèle, sans dérive et sans que
  les agents se marchent dessus.

La chasse, en un coup d'œil :

```
    +--------------------------------------------+
+-->| 1 wayfinder  chart the hunt as one map,    |
|   |   a node per seam; claim from the frontier |
|   +--------------------------------------------+
|   | 2 leap-protocol  one node = one ball:      |
|   |   goal, spec, hard file scope, ONE writer  |
|   +--------------------------------------------+
|   | 3 root-cause-first  reproduce + review     |
|   |   evidence BEFORE any code changes         |
|   +--------------------------------------------+
|   | 4 repair-loop  red-first test committed,   |<--------------------------+
|   |   sniper-testing while iterating           |  finding or survivor ->   |
|   +--------------------------------------------+   +---------------------+ |
|   | 5 blind-tribunal  a non-author grader      |-->|  LORD OF THE LOOP   |-+
|   |   attacks; jurors judge redacted work      |   | one hand drives the |
|   +--------------------------------------------+   | loop: dispatch,     |
|   | 6 seam-engineering  close the CLASS at     |   | judge, loop back    |
|   |   the shared seam, never the symptom       |   | until the gate is   |
|   +--------------------------------------------+   | green. a lane never |
|   | 7 clean-code-gauntlet  the fixed branch    |-->| lands its own work. |
|   |   must DIE under mutation, or stay open    |   +---------------------+
|   +--------------------------------------------+
|             |
|             | jurors pass + mutant dies
|             v
|   +--------------------------------------------+
|   | LANDING GATE -- leap-protocol Score gate:  |
|   | source truth . keep-or-revert . blind      |
|   | review . live proof . provenance -- each   |
|   | finding ends FIXED or REFUTED-W-EVIDENCE   |
+---| ball closed -> claim the next node         |
    +--------------------------------------------+
```

*Dans le schéma : LORD OF THE LOOP = le maître de la boucle, la seule main qui pilote l'itération — dispatch, jugement, rebouclage — jusqu'à ce que la barrière d'atterrissage soit verte ; LANDING GATE = la barrière d'atterrissage — tout au vert, ou pas d'atterrissage.*

## La chaîne

1. [wayfinder](../skills/wayfinder/SKILL.md) — trace la chasse D'ABORD, comme
   une seule carte, avec un nœud par couture ou par trouvaille. Les chercheurs
   réclament les nœuds de façon atomique depuis la frontière ; fermer un nœud
   écrit la question du nœud suivant. Rien ne s'invente hors carte.
2. [leap-protocol](../skills/leap-protocol/SKILL.md) — chaque nœud est un
   « ball » : objectif, spec, périmètre de fichiers strict, rounds bornés,
   résultat à trois états. Les balls liés voyagent sur une seule tranche
   ordonnée par dépendances, avec exactement UN écrivain.
3. [root-cause-first](../skills/root-cause-first/SKILL.md) — reproduis le bug et
   passe en revue les preuves de la cause racine AVANT de toucher au code.
   Aucune mutation sur une intuition.
4. [repair-loop](../skills/repair-loop/SKILL.md) — la discipline intérieure de
   chaque ball : un test qui échoue commité avant le correctif
   ([red-first](../skills/red-first/SKILL.md)), des runs ciblés pendant
   l'itération ([sniper-testing](../skills/sniper-testing/SKILL.md)), une seule
   passe complète des modules touchés à l'atterrissage.
5. [blind-tribunal](../skills/blind-tribunal/SKILL.md) — chaque trouvaille est
   attaquée de façon adversariale : un grader qui n'en est pas l'auteur attaque
   en mode refus-par-défaut, des jurés jugent une enveloppe dont l'auteur est
   masqué. Le builder ne note jamais son propre travail.
6. [seam-engineering](../skills/seam-engineering/SKILL.md) — ferme la CLASSE à
   la couture partagée, jamais le symptôme isolé.
7. [clean-code-gauntlet](../skills/clean-code-gauntlet/SKILL.md) — preuve de
   fermeture : la branche corrigée doit MOURIR sous mutation. Une fermeture dont
   le mutant survit n'est pas prouvée, et la trouvaille reste ouverte.

## Un ball se ferme

Un ball ne se ferme qu'à travers la porte Score de
[leap-protocol](../skills/leap-protocol/SKILL.md) — vérité source,
garder-ou-annuler, revue à l'aveugle, preuve en conditions réelles,
provenance ; une preuve manquante ne devient jamais un « pass » par défaut.
États terminaux propres à la chasse : chaque trouvaille finit CORRIGÉE ou
RÉFUTÉE-AVEC-PREUVES.

## Les règles de la chasse

- Baisse ta confiance. Réancre-toi dans le registre et l'historique des
  tentatives du nœud, jamais dans ta propre mémoire. Relancer = re-réclamer
  depuis la frontière ; passe le relais via
  [session-handoff](../skills/session-handoff/SKILL.md).
- Diffuse ta progression avec une voix humaine, au fil de l'eau. L'inconnu
  reste inconnu — il ne devient jamais un « pass ».
- Une fois les octets candidats, les commandes, les tests et le verdict gelés,
  l'atterrissage est un replay déterministe. Aucun appel de modèle ne re-décide
  une commande déjà décidée.
- Respecte la machine : mesure les ressources avant de spawner, borne la
  concurrence, récupère les lanes mortes, arrête-toi BRUYAMMENT après une
  deuxième mort sur le même nœud, ralentis chaque appel externe. Le kill-switch
  arrête les nouvelles réclamations — jamais une mutation en plein vol.
- Nomme le gâchis de chaque tranche et mesure avant/après. Ne prends un gain
  d'efficacité que si un comparateur prouve zéro perte de capacité ; le
  sur-engineering est un défaut aussi.
- Rends compte en deux mots : PROVEN (prouvé) ou STILL-BUILDING (encore en
  chantier).

## Barrières dures — une seule suffit à faire échouer le play

- Une mutation faite avant la revue des preuves d'une cause racine reproduite.
- Un builder qui note sa propre trouvaille.
- Une trouvaille fermée alors qu'un mutant survit sur la branche corrigée.
- Une passe de suite complète en pleine chasse — vise uniquement la couture de
  la trouvaille, au sniper.
- Du théâtre de mocks dans un test de fermeture : il rouvre le bug en silence
  pendant que le registre le dit fermé.
- Une trouvaille mise de côté au lieu d'être corrigée ou réfutée avec preuves.

**Weight:** une discipline de chasse free au cœur ; la dépense heavy est triple — l'éventail leap, le tribunal adversarial, et la preuve de clôture par mutation — elle se rentabilise quand tout un backlog se ferme en parallèle, chaque clôture prouvée sous mutation.
