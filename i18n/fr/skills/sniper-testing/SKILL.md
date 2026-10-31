---
name: sniper-testing
description: "Pendant une boucle de build ou de réparation, ou avant de croire un résultat vert, quand la vérification doit couvrir le vrai candidat sans relancer inutilement toute la suite."
license: MIT
---

# Sniper Testing

Vérifie le comportement modifié par son vrai consommateur. Choisis les contrôles
à partir du diff complet de la tâche, puis ne relance que ceux touchés par la
modification suivante. Hérite du même quota de mission depuis
[bounded-loops](../bounded-loops/SKILL.md).

## 1. Épingler le vrai périmètre

Conserve le `base_sha` vérifié d'avant la tâche et le `candidate_sha` commité
actuel dans le dossier [Build Flow](../backs-build-flow/SKILL.md). Un arbre propre
après les commits RED et correction possède toujours un diff de tâche.
`git diff HEAD` seul le perd.

Utilise l'outil de périmètre en lecture seule depuis le répertoire résolu du skill :

```bash
python scripts/changed_files.py --repo <verified-repo> --base <base-sha> --candidate <candidate-sha>
```

Pendant l'itération, ajoute `--include-worktree` seulement si le candidat est HEAD.
L'outil distingue chemins commités, indexés, non indexés et non suivis, en
préservant les noms inhabituels. Le périmètre agrégé comprend suppressions et deux
côtés des renommages. Signale le travail sans rapport en attente comme préservé ;
ne revendique pas chaque chemin retourné. Une base absente ou une révision invalide
est une erreur à résoudre, jamais un périmètre vide justifiant de sauter les
contrôles. L'outil ne récupère ni ne modifie l'historique.

## 2. Choisir et exécuter de vrais contrôles

Associe fichiers modifiés et appelants/consommateurs affectés aux tests de
comportement, puis lis scripts, CI et configuration réels du dépôt pour les commandes applicables.

| Contrôle | Périmètre et preuve |
| --- | --- |
| Lint et contrôle de format | Fichiers modifiés pris en charge avec la configuration existante ; mode contrôle avant de décider de reformater. |
| Typage ou compilateur | Frontière de paquet/projet concernée ; les dépendances de types peuvent exiger une cible plus large. |
| Tests de comportement | Vrai chemin modifié et régression qui échoue quand la capacité casse. |
| Tests de contrat/intégration | Consommateurs, alias, paquetage, préservation des réglages ou frontières runtime touchés. |
| Contrôles d'atterrissage obligatoires | Suites exigées par le dépôt une fois le candidat stabilisé. |

Précise chaque commande, le risque couvert, révision/état en attente, résultat
exécuté et échecs restants. Un linter ou vérificateur de types absent est
**indisponible** ou **inapplicable**, avec une raison ; n'invente pas une réussite.
N'installe pas un nouvel outil parce qu'un exemple le nomme. Un lint vert ne remplace pas des tests de comportement.

Pendant l'itération, choisis la plus petite cible utile. Un contrôle déjà réussi
n'a pas à être relancé si aucun code exercé, entrée ou environnement pertinent
n'a changé. Un couplage concret non résolu ou un contrôle projet obligatoire
justifie des tests plus larges ; note pourquoi. À l'atterrissage, exécute une fois
les contrôles agrégés requis sur le candidat final. Les changements suivants
invalident seulement les preuves affectées et les contrôles de commit obligatoires.

## 3. Faire détecter de vraies pannes aux tests

Affirme un effet observable : artefact existant et valide, données relues dans une
vraie base locale, octets réels de contexte reçus par l'hôte, ou élément d'UI rendu.
Exerce fichiers locaux, bases et sockets au lieu de les simuler. Une feuille de
transport externe facturée peut être remplacée par une fixture déterministe,
pendant que construction de requête, routage, analyse et consommateur local restent
réels. Ne prétends jamais que la fixture prouve l'exécution du service externe.

Préserve octet pour octet le fichier RED scellé de [red-first](../red-first/SKILL.md).
Pour une nouvelle lacune, ajoute un fichier de régression supplémentaire distinct
en suivant les règles de preuve et de scellement de ce skill. N'affaiblis, ne
renomme, ne remplace et ne modifie jamais le fichier scellé initial.

## Sortie

Rends périmètre du candidat, résultats lint/typage/tests exécutés, effets réels
observés et contrôles non résolus au même responsable.
[clean-code-gauntlet](../clean-code-gauntlet/SKILL.md) utilise ces preuves comme
première étape, sans répéter les contrôles inchangés.
