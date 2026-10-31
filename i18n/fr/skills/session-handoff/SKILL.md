---
name: "session-handoff"
description: "Quand une session se termine, que le contexte va être compacté, qu'un quota de mission est épuisé ou que le travail inachevé doit continuer avec un autre agent ou harnais. Trigger words: handoff, compact, save state, before restart, relève."
license: "MIT"
---

# Session Handoff
**Effort:** free — un seul fichier plat écrit avant que le contexte meure ; aucun appel de modèle, et il réduit le coût tout court au démarrage de la session suivante. Élimine : l'agent tout neuf qui redérive l'état, repaie des pièges déjà payés, et les décisions perdues dans une fenêtre de contexte morte.

Une fenêtre de contexte meurt ; le travail ne doit pas mourir avec. Avant
qu'une session se termine ou se compacte, écris un fichier plat qu'un agent
tout neuf peut lire à froid et reprendre — ce qui était en cours, où ça vit,
ce qui est à moitié fait, et la commande suivante exacte. La relève d'un build
doit survivre au contexte. Utilise le registre [BACKS Build Flow](../backs-build-flow/SKILL.md)
existant ; ce skill transfère la tâche sans créer de second responsable,
passage de contexte ou mission.

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

Respecte `task_mode` et les permissions d'écriture. Pour une revue en lecture
seule ou figée, rends la relève dans la réponse ou un registre externe déjà
autorisé ; n'écris pas de registre dans le dépôt protégé pour satisfaire ce skill.

## Vérifie d'abord le travail concurrent (avant d'écrire un mot)

Vérifie que le travail des AUTRES sessions est préservé. Lance `git status`,
`git log` et `git worktree list`. Note honnêtement les fichiers modifiés et les
branches non fusionnées dans le doc. Ne modifie jamais le travail non committé
d'une autre session pour que la passation ait l'air propre — c'est le défaut de
perte de données. Une passation qui décrit un état propre pendant qu'une autre
session a du travail en vol est une affirmation fausse.

## Ce qui va dedans — une section courte chacun

1. **Objectif.** Le travail en une phrase. Le prochain agent ne doit pas deviner
   ce que « fini » signifie. Transmets `mission_id`, `task_mode`, responsable de
   l'intégration, aboutissement demandé et actions de livraison déjà autorisées.

2. **État.** Livré (identifiants de commits), en construction, en attente.
   Référence specs, plans, issues et diffs par chemin ou URL sans dupliquer le
   contenu. Inclus `base_sha` épinglé, `candidate_sha` actuel, chemins/commit/hashes
   des RED scellés, commandes/résultats et candidat exact couvert par chaque reçu.

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
9. **Skills suggérés.** Quels skills charger d'abord et pourquoi. Nomme les
   textes/preuves réellement disponibles, ce qui doit être rafraîchi et la source
   de l'essence opérateur ; ne copie pas un second profil.
10. **Budget restant.** Transmets échéance initiale et totaux/consommés/restants des
    essais, tours et autres limites de [bounded-loops](../bounded-loops/SKILL.md),
    plus appels en attente et dernière hypothèse/échec. L'inconnu reste inconnu.
    Ne réinitialise jamais le budget en passant la main, compactant le contexte,
    remplaçant un agent ou changeant de modèle.

## Règles dures

- **Expurge.** Aucune clé API, aucun mot de passe, aucun token, aucune donnée
  personnelle. Aucun vrai hostname, aucune IP interne, aucun chemin
  personnel — placeholders uniquement ; pointe les vraies valeurs par nom de
  variable d'env. Une passation est le fichier le plus susceptible de quitter
  la machine ; un secret qui fuit par elle EST le bug.
- **Les affirmations d'absence pourrissent le plus vite.** Avant d'écrire « X
  n'existe pas » ou « X n'est pas atterri », re-vérifie au commit courant — du
  travail parallèle atterrit pendant que tu écris.
- **Statut étayé par élément.** Une capacité livrée devient PROVEN seulement avec
  revue requise et preuve sur la vraie surface ; sinon STILL-BUILDING nomme les
  preuves manquantes. Une revue terminée ou un patch local peut satisfaire son
  aboutissement demandé sans être rebaptisé capacité déployée.
- **Reste lisible en deux minutes** (environ 120 lignes). Quand ça dépasse,
  archive les blocs les plus anciens en les déplaçant dans une section
  historique — jamais en les supprimant.

## La reprise (l'autre moitié)

Une session qui démarre d'une passation la lit EN PREMIER, puis vérifie les
deux ou trois affirmations du haut contre `git log` et l'arbre live avant
d'agir dessus. La passation est une carte, pas la vérité — fais-lui confiance
pour OÙ regarder ; vérifie CE qu'elle dit.

Reprends avec le même dossier et les mêmes quotas restants. Revérifie l'échéance
avant de distribuer du travail ; une session neuve ne recharge pas le budget.
Si un quota est épuisé, conserve la sauvegarde STILL-BUILDING et termine seulement
le travail utile autorisé qui ne le consomme pas. Garde sceau RED initial et base
épinglée ; actualise l'identité du candidat seulement si les octets changent réellement.

## Fonctionne bien avec

- [root-cause-first](../root-cause-first/SKILL.md) — l'enquête que la session suivante continue.
- [repair-loop](../repair-loop/SKILL.md) — passer la main en pleine boucle sans perdre la couture.
- [decision-bar](../decision-bar/SKILL.md) — comment les décisions ouvertes atteignent ton humain.

> Crédit d'échafaudage : Matt Pocock, handoff (mattpocock/skills). La composition et les règles dures ici sont BACKS AIOS.
