---
name: "bounded-loops"
description: "À utiliser avant de lancer toute boucle qui peut relancer, poller, itérer ou appeler une API externe — boucles d'agent, boucles de réparation, planificateurs, watchers. Déclare des plafonds de budget, pose un checkpoint à l'épuisement, et rend le martèlement structurellement impossible. Trigger words: bounded loop, budget, ceiling, retry, backoff, rate limit, throttle, kill-switch, checkpoint, runaway, infinite loop, spin, budget exhaustion, boucle bornée, plafond, budget épuisé, boucle infinie, relance, martèlement, emballement."
license: "MIT"
---

# Boucles bornées
**Effort:** free — des plafonds et des checkpoints déclarés avant que la boucle démarre ; réduit le coût tout court. Élimine : la dépense des boucles en fuite — le quota brûlé, les routes bloquées à coups de 429, et le progrès qu'un crash efface.

Une boucle sans borne est le bug le plus cher qu'un agent puisse livrer. Elle brûle le
budget, martèle les fournisseurs jusqu'à ce qu'ils te bloquent, et cache son propre
échec dans son tourbillon. Chaque boucle reçoit un plafond, un checkpoint et une façon
bruyante de mourir — avant de démarrer.

## Quand l'utiliser

Avant de démarrer toute boucle : une boucle de réparation, un wrapper de retry, un
poller, un scheduler, un run autonome multi-étapes, tout ce qui peut réémettre un appel
ou retenter une étape.

## Les étapes

1. **Déclare le budget d'abord.** Tokens, coût, temps réel et tentatives max — posés
   par écrit avant la première itération. Une boucle sans budget déclaré est sans
   borne par définition et ne démarre pas.
2. **Plafonne les tours internes.** Un épisode interne (un cycle LLM/outil sur un
   problème) reçoit un petit plafond de tours fixe (environ 4). Le plafond borne
   l'épisode, pas la mission — le travail inachevé remonte, il ne s'acharne pas.
3. **Checkpoint à chaque itération.** Un état durable sur disque — manifeste du run,
   journal de preuves, étape courante — jamais la mémoire du chat. N'importe qui (y
   compris une session toute neuve) peut reprendre depuis le dernier checkpoint.
4. **À l'épuisement : checkpoint, puis escalade.** Remets le checkpoint à la boucle
   du dessus ou à ton humain, avec ce qui est fait, ce qui reste, et le blocage. Ne
   continue jamais en silence au-delà d'un budget. Ne t'arrête jamais en silence non
   plus — l'épuisement se dit fort.
5. **Respecte chaque API externe.** Avant le premier appel, apprends la rate limit
   (la limite d'appels) et le quota du fournisseur ; quand c'est inconnu, traite-le
   comme strict — un appel, large espacement — jusqu'à mesure. Ralentis chaque appel,
   mets en cache et réutilise les réponses, et tiens un plafond dur par fenêtre.
6. **Recule exponentiellement quand ça repousse.** Un 429 ou un 503 veut dire :
   attends, puis attends plus longtemps. Zéro retry instantané sur le même endpoint.
   Un retry serré contre un seul endpoint, c'est comme ça qu'une route qui marchait
   meurt : ça brûle le quota et ça peut faire bloquer toute ton adresse de sortie.
7. **Porte un kill-switch bruyant et borné.** Toute boucle qui peut réémettre un appel
   a un nombre max de tentatives ; quand il est atteint, la boucle s'arrête FORT avec
   les preuves — jamais un tourbillon infini ou silencieux.
8. **Stop et mise en file aux points sûrs seulement.** Stop veut dire
   checkpoint-puis-annulation. Le nouveau travail attend le prochain point sûr (une
   frontière d'état entre deux étapes) — jamais injecté en pleine étape. Une seule
   instance de boucle, un seul écrivain, des écritures d'état atomiques.

## Règles dures (ce qui fait rater ce skill)

- Une boucle qui démarre sans budget déclaré de tokens / coût / temps / tentatives.
- Continuer au-delà d'un budget épuisé, en silence ou pas, sans escalader.
- Un retry instantané contre le même endpoint, ou tout chemin de retry sans backoff.
- Une boucle de retry sans plafond de tentatives, ou un plafond qui échoue en douce
  quand il est atteint.
- Un état d'avancement gardé seulement dans la mémoire de conversation — un crash
  efface le run.
- Deux instances de boucle qui écrivent le même état, ou des écritures d'état non
  atomiques.
- S'évader de la boucle en affaiblissant ses propres contrôles de sortie — un vert
  obtenu en baissant la barre, en supprimant des données ou en avalant des erreurs
  est un faux vert, pas une sortie.

## Marche bien avec

- [optimus](../optimus/SKILL.md) — charge le plancher avant que toute boucle démarre.
- [repair-loop](../repair-loop/SKILL.md) — le principal consommateur de ces plafonds.
- [fleet-ladder](../fleet-ladder/SKILL.md) — un repli borné entre modèles, pas le martèlement d'un seul.
- [session-handoff](../session-handoff/SKILL.md) — ce en quoi un checkpoint escalade.
