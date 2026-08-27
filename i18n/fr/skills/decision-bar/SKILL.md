---
name: decision-bar
description: À utiliser quand tu t'apprêtes à poser une question à ton humain, attendre une approbation, ou garer une décision pendant un travail autonome. Filtre chaque décision par une seule barre — seuls le goût, la vision ou le risque destructif remontent à l'humain ; tout le reste s'exécute. Trigger words: ask-me bar, ask me, approval, permission, should I, decision, escalate, human in the loop, blocked on you, la barre du demande-moi, demander la permission, approbation, est-ce que je dois, décision, escalader, bloqué sur toi.
license: MIT
---

# La barre du « demande-moi »
**Effort:** free — un test de barre au moment où tu poserais la question ; réduit le coût tout court en tuant les allers-retours d'interruption. Élimine : les questions auxquelles les règles en vigueur répondent déjà, et les vraies décisions garées là où l'humain ne regarde jamais.

Les agents trahissent leurs humains de deux façons : ils interrompent avec des
questions que les règles ont déjà tranchées, ou ils « font remonter » une vraie
décision quelque part où personne ne la verra jamais. Ce skill ferme les deux.

## La barre

Une décision n'atteint l'humain QUE si elle est réellement la sienne :

- **Le goût** — le style, la formulation, l'apparence, le ressenti ; le choix n'a pas
  de réponse objectivement juste.
- **La vision** — la direction, le périmètre, l'intention produit ; se tromper tord la
  mission.
- **Le risque destructeur** — perte de données, action irréversible, argent réel,
  personnes réelles.

Tout ce qui est sous cette barre S'EXÉCUTE — résolu depuis les règles en vigueur, la
vérité du projet lui-même, l'intention connue de l'humain, et des défauts raisonnables.
Zéro friction ajoutée.

## Les étapes

1. Attrape l'instant. Tu t'apprêtes à demander, attendre ou reporter. Stop, passe la
   barre.
2. Teste : est-ce du goût, de la vision, ou un risque destructeur ? Si rien de tout
   ça — ce n'est pas une question à poser.
3. Sous la barre : cherche avant de demander. Relis les règles en vigueur et le code.
   La réponse est presque toujours déjà écrite. Tranche, exécute, et note la décision
   dans ton journal de travail pour que l'humain puisse l'auditer plus tard.
4. À la barre : LIVRE la question. Un résumé de la situation en langage clair, puis
   les choix en liste courte — en boutons si le canal de l'humain les permet — sur le
   canal que l'humain regarde vraiment. Puis continue tout le travail qui ne dépend
   pas de la réponse.
5. Ne gare jamais rien. Une décision laissée dans un doc, un message de commit, une
   ligne de registre ou un long paragraphe n'existe pas pour l'humain. Une décision
   garée est une barrière cachée.

## Règles dures (une seule fait rater le skill)

- Demander quoi que ce soit que les règles en vigueur, le code ou des défauts
  raisonnables savent trancher.
- Inventer une nouvelle machinerie d'approbation — un drapeau, une file, une étape de
  visa — pour du travail sous la barre. La vérification peut s'ajouter ; les
  barrières, jamais.
- Fabriquer une approbation pour une décision que les règles en vigueur de l'humain
  ont déjà prise.
- Garer une vraie décision là où l'humain ne regarde pas activement.
- Annoncer « fait » ou « vert » depuis une sonde de substitution au lieu de la surface
  de l'humain — la loi de la preuve vit dans
  [invariant-floor](../invariant-floor/SKILL.md).

## Marche bien avec

- [wayfinder](../wayfinder/SKILL.md) — tracer la route à travers les inconnues sous la barre au lieu de demander.
- [human-voice](../human-voice/SKILL.md) — le registre dans lequel toute question livrée s'écrit.
- [invariant-floor](../invariant-floor/SKILL.md) — les règles en vigueur à relire avant qu'une question ne monte.
