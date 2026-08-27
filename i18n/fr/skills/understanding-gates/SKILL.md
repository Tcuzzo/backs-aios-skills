---
name: understanding-gates
description: À utiliser quand un build, un fix ou un uplift avance de l'intention vers la livraison et qu'il te faut la preuve qu'il colle toujours à la demande d'origine. Interroge Design, Plan, Build, Test et Ship avec des verdicts approuver/réviser/rejeter, des échecs nommés comme cibles de réparation, et une re-exécution après chaque réparation. Trigger words: understanding, stage gates, validate build, spec match, verdict, green but wrong, echo check, done means done, portes d'étape, valider le build, conformité à la spec, vert mais faux, test d'écho, fini veut dire fini.
license: MIT
---

# Understanding Gates

Une discipline de validation pour les builds. Elle interroge le travail à cinq
étapes — Design, Plan, Build, Test, Ship — toujours contre la demande
D'ORIGINE, jamais contre la reformulation que le travail en fait. Chaque porte
renvoie des preuves : des scores, un verdict, des échecs nommés, et des actions
de réparation. Elle lie l'agent, pas l'humain : aucune nouvelle étape
d'approbation, aucune friction sur la personne qui a demandé.

## Quand la lancer

- Tout build, fix ou uplift qui va atterrir quelque part de réel.
- Chaque fois que tu t'apprêtes à dire « fini » et que la seule preuve est un
  test vert.
- Après chaque réparation, sur la même étape qui a échoué.

## Étape 0 — ancrer l'intention

Avant de scorer quoi que ce soit, fixe l'ancre de comparaison : les mots
D'ORIGINE de l'humain, plus une directive traduite en une ligne (voir
[intent-compiler](../intent-compiler/SKILL.md)). Chaque porte score contre
cette ancre. Ne score jamais contre ta propre paraphrase — une paraphrase
dérive, et alors chaque porte valide tranquillement la dérive au lieu de la
demande.

## Les cinq portes

Chaque porte pose une question contre l'intention d'origine :

| Étape | Question |
| --- | --- |
| Design | La spec est-elle claire et fidèle à la demande d'origine ? |
| Plan | Le plan répond-il à l'intention et convient-il à la surface où il part ? |
| Build | Le code satisfait-il la spec sans dérive ? |
| Test | Les tests exercent-ils le vrai comportement, pas un substitut ? |
| Ship | Ça s'applique proprement, ça échoue bruyamment, et l'affirmation de livraison survit-elle à une vérification des faits ? |

Score CHAQUE porte sur les mêmes cinq lentilles, chacune de 0 à 4 : conformité
à la spec, cohérence architecturale, sûreté des types, testabilité, sécurité —
formulées pour l'étape (au Design, « testabilité » demande si la spec est
vérifiable ; au Ship, si l'affirmation de livraison l'est). Agrégation :
additionne les cinq lentilles (0–20), multiplie par 5 — c'est le score de
verdict 0–100 de la porte. Enregistre chaque lentille, pas seulement le total —
le total cache quelle lentille a échoué.

## Verdicts

Agrège les lentilles en un score 0–100 et classe-le :

- **Approuver** (80+) : preuve solide. Toujours pas une preuve de fini — voir
  la deuxième loi.
- **Réviser** (60–79) : des échecs nommés existent. Chacun est une cible de
  réparation.
- **Rejeter** (moins de 60) : le travail rate l'intention. Recule d'une étape.

Un verdict sans échecs nommés derrière est un verdict pauvre en information.
Exige la liste.

## Discipline de réparation

1. Garde l'intention d'origine comme ancre de chaque re-exécution.
2. Enregistre les scores par lentille, pas seulement le chiffre global.
3. Traite chaque échec nommé comme une cible de réparation. Aucun échec n'est
   de la décoration.
4. Répare, puis RELANCE LA MÊME PORTE. Une réparation sans re-exécution n'est
   qu'une affirmation.
5. Ne promeus jamais la confiance en état de préparation. Les tests et la
   vraie surface décident.

## Les deux lois

**1. La loi de l'écho.** Un check qui ne peut qu'acquiescer est un écho, pas
un validateur. La preuve d'honnêteté, c'est la réfutation : donne-lui une
affirmation que tu sais fausse et regarde-le la recaler. S'il laisse passer le
mensonge, le check est du théâtre. Corollaire sur le mock : ne mocke que la
feuille externe instable — une API payante, un réseau capricieux. Ne mocke
jamais l'organe dont le comportement EST la preuve ; son scoring, son
extraction d'affirmations et sa logique passe/échoue doivent tourner pour de
vrai.

**2. Nécessaire, pas suffisant.** Un test qui passe est nécessaire, jamais
suffisant. Fini veut dire que la vraie surface — celle que l'humain utilise
vraiment — fait le travail toute seule. Nomme cette surface, déclenche le vrai
chemin, et regarde le bon résultat arriver. Ne promeus jamais un reçu de test
unitaire en affirmation de capacité live.

## Règles dures (ce qui fait échouer ce skill)

- Scorer contre une paraphrase au lieu de la demande d'origine.
- Un verdict réviser ou rejeter sans échecs nommés attachés.
- Réparer sans relancer la porte qui a échoué.
- Mocker le validateur lui-même, ou la couture exacte en cours de changement.
- Déclarer fini depuis un test vert sans preuve sur la vraie surface.

## Tiens un dossier de build

Pour chaque étape, garde : l'intention, l'artefact d'entrée exact, les scores,
les échecs nommés, la réparation effectuée, le résultat de la re-exécution, et
la preuve sur la vraie surface. Un dossier qui ne pointe pas vers des preuves
reproductibles est une banderole, pas un dossier.

## Fonctionne bien avec

- [intent-compiler](../intent-compiler/SKILL.md) — traduire la demande avant de la scorer.
- [red-first](../red-first/SKILL.md) — le contrat de la porte Test : test en échec committé d'abord.
- [sniper-testing](../sniper-testing/SKILL.md) — de vrais effets de bord, pas de théâtre de mocks.
- [blind-tribunal](../blind-tribunal/SKILL.md) — des correcteurs indépendants par-dessus ces portes.
- [repair-loop](../repair-loop/SKILL.md) — la boucle qui pousse les verdicts réviser jusqu'au vert.
