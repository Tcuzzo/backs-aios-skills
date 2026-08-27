---
name: live-research
description: À utiliser quand tu raisonnes sur un codebase, une API ou un système dont la forme réelle compte. Lance un agent de recherche en parallèle qui lit la vérité vivante — les READMEs du projet, les docs de section, le vrai source — pour ancrer les conclusions dans ce qui existe vraiment, pas dans la mémoire du modèle. Trigger words: live research, ground the reasoning, read the real source, check what is actually there, primary sources, background research, verify against the repo, what do the docs say, recherche live, ancrer le raisonnement, lire le vrai source, vérifier ce qui existe, sources primaires, vérifier contre le repo, que disent les docs.
license: MIT
---

# Live Research
**Effort:** light — un agent de recherche en arrière-plan qui lit la source vivante pendant que la voie principale continue de travailler. Élimine : les conclusions bâties sur la mémoire du modèle que le vrai repo réfute ensuite — le rework d'avoir livré une supposition.

La mémoire du modèle est une supposition sur l'état d'un projet au moment de
l'entraînement. La vérité vivante, c'est ce qui est sur le disque et dans les
docs officielles maintenant. Ce skill fait tourner les deux voies en même
temps : pendant que la voie principale raisonne sur une cible, un agent de
recherche lit la vraie chose, et ses trouvailles fusionnent dans le
raisonnement **avant** toute conclusion.

## Quand le lancer

- Tu t'apprêtes à raisonner sur la structure d'un projet, le contrat d'une API
  ou le comportement d'une librairie — et tu n'as pas lu le source actuel.
- Un design, un fix ou une affirmation dépend de faits qui ont pu dériver
  depuis tes données d'entraînement.
- Une question exige des faits du monde réel que le contexte de travail seul
  ne peut pas fournir.

## Les étapes

1. **Lance le chercheur en parallèle.** Dès que le raisonnement sur une cible
   démarre, envoie un agent de recherche en arrière-plan sur la même cible. La
   voie principale continue de travailler ; le chercheur lit. Ne bloque jamais
   le travail sur du défrichage qu'un agent peut faire seul.
2. **Lis la vérité vivante, au plus près d'abord.** Le README du projet, puis
   les docs de section les plus proches de la cible, puis la vraie structure du
   source — vrai listing de répertoires, vrais contenus de fichiers, vraies
   signatures. Pour les faits hors du projet : docs officielles, code source,
   specs, APIs de première main. Un blog qui résume les docs n'est pas une
   source primaire.
3. **Fais remonter les trouvailles avant les conclusions.** Les trouvailles
   affluent vers la voie principale au fil de l'eau, et le raisonnement les
   intègre et corrige le cap. Une conclusion tirée avant que le chercheur ait
   rendu compte sur ce point est une supposition — marque-la comme telle
   jusqu'à ce que la vérité vivante la confirme ou la tue.
4. **Épingle chaque affirmation à la source qui la possède.** Chaque trouvaille
   porte sa source en ligne : un chemin de fichier, une ligne citée, un lien,
   un commit. Une affirmation qui ne peut pas être épinglée est marquée non
   vérifiée, bien fort — jamais déguisée en fait.
5. **Écris un seul fichier cité.** Les trouvailles atterrissent dans un unique
   fichier Markdown, chaque affirmation avec sa source. Range-le là où le
   projet garde déjà ce genre de notes ; sans convention, choisis un endroit
   sensé et dis où, pour que l'agent suivant le trouve.
6. **Rappelle-toi avant de relire.** Vérifie d'abord les notes des sessions
   précédentes — la même source a peut-être déjà été tirée. Réutilise la
   trouvaille en cache et cite la même source. Des minutes de rappel battent
   des heures de redécouverte.

## Règles dures

- **Aucune conclusion avant la fusion.** Si le chercheur n'a pas rendu compte
  sur un point, la voie principale ne peut pas énoncer ce point comme acquis.
- **Sources primaires uniquement.** Remonte chaque affirmation jusqu'à la
  source qui la possède. Un résumé de seconde main est un pointeur, pas une
  preuve.
- **Headless, jamais regardé.** La recherche en arrière-plan passe par un
  chemin de récupération headless — jamais un navigateur live qu'un humain
  regarde ; ça, c'est une autre voie.
- **Invérifiable, ça se dit.** Une trouvaille sans source primaire part
  signalée, jamais fondue en silence dans le reste.
- **Zéro friction humaine.** Ce skill n'ajoute aucune étape d'approbation et
  aucune barrière. C'est une discipline de méthode, pas un checkpoint.

## Ce qui revient

Un seul fichier Markdown, ancré et cité — plus une voie de raisonnement
corrigée en vol au lieu d'après la conclusion. La voie principale lit le
fichier et avance.

## Fonctionne bien avec

- [wayfinder](../wayfinder/SKILL.md) — les tickets de recherche sont le type agent-seul que ce skill résout.
- [root-cause-first](../root-cause-first/SKILL.md) — la même discipline source-d'abord, pointée sur les bugs.

> Crédit d'échafaudage : Matt Pocock, research (mattpocock/skills, MIT). La composition et les règles dures ici sont BACKS AIOS.
