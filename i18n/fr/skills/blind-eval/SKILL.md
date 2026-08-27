---
name: blind-eval
description: À utiliser avant de livrer quoi que ce soit où le goût ou la qualité du rendu est la question et qu'un test ne peut pas trancher. Juge un changement sur ses mérites, auteur masqué, puis garde ou annule — une égalité annule, seul un gain prouvé atterrit. Trigger words: blind eval, karpathy, keep or revert, quality gate, taste call, blind judge, A/B judge, prove uplift, éval à l'aveugle, garder ou annuler, barrière de qualité, question de goût, juge aveugle, gain prouvé.
license: MIT
---

# Blind Eval — l'éval à l'aveugle

Une barrière de qualité garder-ou-annuler (keep or revert) pour les décisions qu'un
test ne peut pas trancher — la qualité d'une prose, un texte d'interface, la lisibilité
d'un refactor, la sortie d'un prompt, le rendu d'un design. Juge le changement sur ses
mérites, auteur masqué, puis GARDE-le ou ANNULE-le. Une égalité s'annule. Seul un gain
prouvé est conservé.

## Quand la lancer

- Avant de livrer tout changement où « est-ce mieux ? » est une question de goût ou de
  qualité.
- Comme barrière au cœur d'une boucle d'amélioration : proposer → essayer → mesurer →
  garder ou jeter.
- Chaque fois que l'auteur est tenté de déclarer lui-même son travail « une
  amélioration ».

## La méthode

1. **Écris « mieux » AVANT de regarder.** Un objectif en langage clair. Une mesure
   principale ou un axe de grille qui porte une barre dure — un niveau à franchir, pas
   un chiffre à pousser. Les axes secondaires en ordre de priorité (coût, longueur,
   latence).
2. **Fige les deux versions.** La base et le candidat, comme artefacts réels — jamais
   une description de ceux-ci.
3. **Efface l'auteur.** Étiquette-les A et B, mélange l'ordre, retire chaque nom,
   chaque id de modèle et le raisonnement de l'auteur. Le juge ne voit que les
   artefacts et la grille.
4. **Assieds un juge qui n'a écrit ni l'un ni l'autre** — un modèle d'une autre
   famille, ou un humain. L'auteur ne note jamais son propre travail.
5. **Juge sur les mérites.** Note chaque axe de la grille. Cite une preuve tirée de
   l'artefact pour chaque note — un verdict sans preuve est une supposition.
6. **GARDE seulement si le candidat franchit la barre ET bat strictement la base.**
   Une égalité n'est pas un gain — annule.
7. **Annule proprement.** Restaure l'arbre à l'identique, octet pour octet, à l'état
   d'avant le changement (une branche de brouillon ou un stash le fait en une seule
   commande). Consigne le verdict dans les deux cas.

## Les règles qui coupent la triche

- **La barre se vérifie en premier, et les axes comptent dans l'ordre.** Une
  régression sur un axe plus prioritaire est fatale, même si tous les axes du dessous
  s'améliorent. Et franchir la barre avec de la marge n'achète rien — tu ne peux pas
  sur-réussir le principal pour « payer » une régression de coût.
- **Ne baisse jamais la barre après avoir vu le résultat.** Réparer la note en
  affaiblissant l'éval est interdit. Garde la grille et l'éval hors des fichiers que
  le changement a le droit de toucher.
- **Pas d'auto-notation.** Le juge ne voit jamais l'argumentaire de l'auteur — un juge
  qui lit le pitch note le pitch, pas le travail.
- **Débruite un juge stochastique.** Les lectures à l'aveugle varient d'un run à
  l'autre, et les juges préfèrent la première option qu'ils voient. Lance chaque
  comparaison plusieurs fois, ordre mélangé, et prends le vote majoritaire — le
  mélange tue le biais de position et les répétitions tuent le bruit, en un seul
  geste. Si le vrai gain est plus petit que la variation du juge d'un run à l'autre,
  la barrière ne distingue pas le signal de la chance — ajoute des lectures ou choisis
  une mesure plus stable.
- **Montage solo.** Pas de seconde famille de modèles sous la main ? Une session
  vierge qui n'a jamais vu la conversation de l'auteur juge — et le rapport nomme la
  barrière affaiblie (« jugé même-famille-à-l'aveugle, pas inter-familles »).
- **Pas de barre fiable ? Utilise la dominance.** Quand le niveau de la base est
  inconnu ou bruité, abandonne la barre absolue et ne garde que ce qui bat strictement
  le champion en titre. Une régression ne peut jamais dominer, donc aucun plancher
  n'est nécessaire.
- **Ne note jamais un axe de coût sur des échecs.** « Moins d'étapes » calculé sur des
  tentatives ratées récompense l'abandon rapide. Calcule le coût et l'effort sur les
  réussites seulement.

## Débiaiser le juge

Le socle de la mécanique du juge. Il vit ici et nulle part ailleurs :

- **Suite tenue à l'écart.** Note sur une suite gardée HORS de portée d'écriture du
  builder — le builder ne voit jamais les tests notés, donc il ne peut pas coder en
  dur pour eux.
- **Repartir d'un commit frais.** Réduis l'espace de travail à un commit frais et
  coupe le réseau sortant avant un run noté, pour qu'un pass soit DÉRIVÉ — pas
  récupéré dans l'historique git ou dans le correctif de quelqu'un d'autre.
- **Normalise la longueur.** Les juges préfèrent nettement la réponse la plus longue —
  corrige la longueur avant de comparer les notes.
- **Critères cachés tournants.** Utilise une grille oui/non à axes nommés, avec des
  critères cachés qui tournent entre les runs. Une note holistique visible finit
  gamée en théâtre de citations.
- **Notation sur l'état final.** Note un travail multi-étapes sur l'état FINAL, pas
  sur chaque étape intermédiaire.
- **Calibration du juge.** Calibre le juge sur un petit jeu étiqueté par des humains —
  rapporte ses taux de vrais positifs et de vrais négatifs — avant de lui faire
  confiance sur ton domaine.

Le mélange d'ordre fait partie de la règle de débruitage ci-dessus — une seule loi,
énoncée une seule fois.

## La variante en boucle

La même barrière alimente une boucle d'amélioration autonome : proposer un petit
changement → lancer une courte expérience → mesurer à l'aveugle → garder si mieux,
annuler sinon → répéter, sur un budget de tours fixé. Donne au proposeur les traces
d'échec du tour précédent, pas seulement l'objectif — un proposeur qui ne voit pas
pourquoi il échoue édite à l'aveugle. Même une boucle qui ne garde rien rembourse son
coût : les traces qu'elle collecte pointent des bugs concrets et réparables qu'aucun
score agrégé ne révèle.

## Marche bien avec

- [blind-tribunal](../blind-tribunal/SKILL.md) — le panel de jurés, plus lourd, quand la question porte sur les défauts, pas le goût.
- [red-first](../red-first/SKILL.md) — quand un test PEUT trancher, écris le test à la place.
- [clean-code-gauntlet](../clean-code-gauntlet/SKILL.md) — des barrières de qualité de code mesurées, à marier au jugement de goût.

> Crédit du nom : Andrej Karpathy. Inspiration éponyme ; la discipline
> garder-ou-annuler trouve un parallèle indépendant dans autoresearch de Karpathy
> (2026, github.com/karpathy/autoresearch, MIT). L'aspect aveugle (auteur masqué), la
> composition et les règles dures d'ici sont BACKS AIOS.
