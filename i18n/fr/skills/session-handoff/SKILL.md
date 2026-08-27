---
name: session-handoff
description: À utiliser quand une session se termine, que la fenêtre de contexte va se compacter, ou que le travail doit continuer dans un autre agent ou harnais. Compacte la session en un fichier plat qu'un agent tout neuf peut lire à froid et reprendre — état, travail à moitié fait, commande suivante exacte, décisions ouvertes — secrets expurgés et travail concurrent vérifié préservé. Trigger words: handoff, hand off, compact, save state, continue in another session, portable handoff, before restart, passation, passer la main, compacter, sauver l'état, continuer dans une autre session, passation portable, avant redémarrage.
license: MIT
---

# Session Handoff

Une fenêtre de contexte meurt ; le travail ne doit pas mourir avec. Avant
qu'une session se termine ou se compacte, écris un fichier plat qu'un agent
tout neuf peut lire à froid et reprendre — ce qui était en cours, où ça vit,
ce qui est à moitié fait, et la commande suivante exacte. Une passation garée
dans la prose du chat ou dans la seule mémoire n'existe pas.

## Quand en écrire une

- Avant que la fenêtre de contexte se compacte ou soit vidée.
- Quand tu termines une session avec du travail encore ouvert.
- Juste après avoir atterri quelque chose de gros (note l'id du commit tant
  que c'est frais).
- À l'instant où une vraie décision part vers ton humain (note ce que chaque
  choix implique).

## Où elle va

Un endroit connu que l'agent suivant regardera EN PREMIER. Si l'agent suivant
partage ton projet, utilise un fichier registre stable dans le repo et committe
la mise à jour pour qu'elle survive à un redémarrage machine, pas seulement à
un vidage de contexte. Si l'agent suivant est un autre harnais ou un login
neuf, écris un fichier plat portable dans le répertoire temporaire — c'est de
l'échafaudage, pas un artefact suivi.

## Vérifie d'abord le travail concurrent (avant d'écrire un mot)

Vérifie que le travail des AUTRES sessions est préservé. Lance `git status`,
`git log` et `git worktree list`. Note honnêtement les fichiers modifiés et les
branches non fusionnées dans le doc. Ne modifie jamais le travail non committé
d'une autre session pour que la passation ait l'air propre — c'est le défaut de
perte de données. Une passation qui décrit un état propre pendant qu'une autre
session a du travail en vol est une affirmation fausse.

## Ce qui va dedans — une section courte chacun

1. **Objectif.** Le travail en une phrase. L'agent suivant ne doit pas avoir à
   deviner ce que « fini » veut dire.
2. **État.** Atterri (ids de commit), en construction, en file. Référence les
   specs, plans, issues et diffs par chemin ou URL — ne duplique jamais leur
   contenu.
3. **Où vit le travail.** Branches, worktrees, fichiers modifiés. Nomme les
   fichiers exacts que l'agent suivant doit lire en premier.
4. **La piste des verdicts.** Qui ou quoi a noté chaque morceau et quelles
   étaient les vraies prises. Un verdict échoué avec des défauts nommés vaut
   PLUS qu'un vert — écris les défauts mot pour mot.
5. **Le travail à moitié fait et la commande suivante exacte.** Ce qui est en
   vol, et la commande littérale qui le reprend.
6. **Décisions ouvertes.** Tout ce qui attend ton humain, et ce que chaque
   choix implique. Une décision ne doit jamais exister uniquement dans une
   fenêtre de contexte morte.
7. **Contrats non tenus.** Tests encore rouges, preuves encore manquantes,
   promesses faites mais pas encore tenues.
8. **Pièges.** Une ligne chacun. Un piège que tu as déjà payé vaut plus qu'un
   vert — écris-le pour que la session suivante ne paie pas deux fois.
9. **Skills suggérés.** Quels skills l'agent suivant devrait charger en
   premier, et une ligne pour dire pourquoi. C'est ce qui rend le doc portable
   entre harnais.

## Règles dures

- **Expurge.** Aucune clé API, aucun mot de passe, aucun token, aucune donnée
  personnelle. Aucun vrai hostname, aucune IP interne, aucun chemin
  personnel — placeholders uniquement ; pointe les vraies valeurs par nom de
  variable d'env. Une passation est le fichier le plus susceptible de quitter
  la machine ; un secret qui fuit par elle EST le bug.
- **Les affirmations d'absence pourrissent le plus vite.** Avant d'écrire « X
  n'existe pas » ou « X n'est pas atterri », re-vérifie au commit courant — du
  travail parallèle atterrit pendant que tu écris.
- **Statut en deux mots par élément : PROVEN ou STILL-BUILDING.** Des tests
  verts sans preuve live, c'est STILL-BUILDING, et la passation dit exactement
  quelle preuve manque.
- **Reste lisible en deux minutes** (environ 120 lignes). Quand ça dépasse,
  archive les blocs les plus anciens en les déplaçant dans une section
  historique — jamais en les supprimant.

## La reprise (l'autre moitié)

Une session qui démarre d'une passation la lit EN PREMIER, puis vérifie les
deux ou trois affirmations du haut contre `git log` et l'arbre live avant
d'agir dessus. La passation est une carte, pas la vérité — fais-lui confiance
pour OÙ regarder ; vérifie CE qu'elle dit.

## Fonctionne bien avec

- [root-cause-first](../root-cause-first/SKILL.md) — l'enquête que la session suivante continue.
- [repair-loop](../repair-loop/SKILL.md) — passer la main en pleine boucle sans perdre la couture.
- [decision-bar](../decision-bar/SKILL.md) — comment les décisions ouvertes atteignent ton humain.

> Crédit d'échafaudage : Matt Pocock, handoff (mattpocock/skills). La composition et les règles dures ici sont BACKS AIOS.
