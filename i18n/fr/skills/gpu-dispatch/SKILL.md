---
name: gpu-dispatch
description: À utiliser pour dispatcher des modèles locaux sur les GPU — planifier l'inférence, choisir une carte, ou gérer la résidence des modèles. Un modèle par GPU, aucun débordement vers la RAM système, garder chaud pendant toute la boucle, décharger en fin de boucle, admettre sur vérité mesurée. Trigger words: gpu, vram, gpu dispatch, model loading, keep alive, resident model, local inference, spill, warm, carte graphique, chargement de modèle, modèle résident, inférence locale, débordement, garder chaud.
license: MIT
---

# La loi du dispatch GPU

Quatre règles pour faire tourner des modèles locaux sur GPU. Elles existent parce que
les deux pannes classiques sont opposées et coûtent aussi cher l'une que l'autre :
essorer les cartes à coups de chargements et de débordements, et sur-clôturer le
matériel pour qu'il reste à dormir. Les deux sont de la capacité perdue. Applique-les
dans le dispatcher, en code — jamais comme une règle qu'un modèle devrait retenir.

## Quand l'utiliser

- Avant d'envoyer tout job d'inférence vers un GPU local.
- En concevant ou en relisant un dispatcher, un scheduler ou un routeur de modèles.
- Quand un run local est mystérieusement lent, ou une carte mystérieusement
  « indisponible ».

## Les quatre règles

1. **Un seul modèle résident par carte, à la fois.** Avant tout envoi, lis l'état
   vivant des modèles chargés du nœud via l'API du runtime lui-même. Si un autre
   modèle est résident, utilise-le ou décharge-le d'abord. Ne charge jamais un second
   modèle à côté.
2. **Pas de débordement vers la RAM système — on abandonne, on ne ralentit pas.**
   Vérifie que le modèle tient entièrement dans la VRAM libre de la carte avant
   l'envoi, et vérifie qu'il reste entièrement en VRAM pendant le travail. Tout
   débordement vers la RAM système est un ABANDON, pas un run dégradé — un modèle qui
   a débordé est discrètement 10x plus lent et empoisonne chaque job derrière lui. Un
   modèle qui ne tient pas au-dessus du plancher réservé de la carte n'est pas envoyé
   sur cette carte ; prends un modèle plus petit ou une autre carte.
3. **Garde la carte chaude pour toute la boucle de travail.** Tiens le modèle résident
   avec un keep-alive borné — un plancher et un plafond que tu configures, jamais
   illimité — et rafraîchis-le tant que la boucle tourne. Pas de valse de démarrages à
   froid entre les jobs d'une même boucle.
4. **Ne décharge qu'à la fin de la boucle.** Une libération explicite en fin de
   boucle — pas après chaque job. Décharger par job, c'est la valse du démarrage à
   froid ; ne jamais décharger, c'est une fuite. La libération en fin de boucle est la
   couture.

## Admission par vérité mesurée

Qu'une carte puisse prendre du travail se décide par mesure vivante, jamais par
supposition :

- Une **vraie sonde** du nœud — pas une note « injoignable » périmée dans une config.
- De la **vraie VRAM libre** au-dessus du plancher réservé de la carte — le plancher
  est la seule limite en vigueur ; tout ce qui est au-dessus est libre d'usage.
- Un **vrai contrôle de processus en cours** pour les charges interactives. Un jeu, un
  stream ou une session de montage en vif sur la carte gagne instantanément — mais sa
  présence se mesure, elle ne se suppose jamais depuis un fichier marqueur ou une
  liste « froide » codée en dur.

Les défauts fermés-par-défaut, les refus pour « usage inconnu » et les fichiers
marqueurs dont l'absence veut dire « clôture activée » sont tous le même bug : le
runtime qui refuse du matériel que l'humain possède. Sur-clôturer du matériel possédé
est de la capacité perdue, et la capacité perdue est un défaut. Seule la parole vivante
de l'humain ajoute ou lève une clôture.

## Règles dures (ce qui fait rater ce skill)

- Charger un second modèle sur une carte qui en a déjà un résident.
- Continuer un run après avoir détecté un débordement de VRAM au lieu d'abandonner.
- Un keep-alive sans borne, ou décharger entre les jobs d'une même boucle.
- Refuser une carte sur la foi d'une note de config, d'un fichier marqueur ou d'une
  supposition au lieu d'une sonde vivante.
- Appliquer tout ça par prompt au lieu du code du dispatcher.

## Marche bien avec

- [invariant-floor](../invariant-floor/SKILL.md) — la vérité mesurée et les échecs
  bruyants sont des lois du plancher ; ce skill les applique aux GPU.
- [fleet-ladder](../fleet-ladder/SKILL.md) — résoudre quel modèle envoyer avant de
  décider où il tourne.
- [bounded-loops](../bounded-loops/SKILL.md) — la boucle de travail à laquelle le
  keep-alive et la libération de fin de boucle sont attachés.
