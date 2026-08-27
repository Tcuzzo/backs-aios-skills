---
name: sniper-testing
description: À utiliser pendant toute boucle de fix ou de build, et avant de croire n'importe quel test vert. Ne lance que les tests qui couvrent ce que tu as touché, et tue le théâtre de mocks — les tests qui passent pendant que la capacité est cassée. Trigger words: sniper testing, scoped tests, test scope, mock theater, fake green, full suite, test bloat, tests ciblés, périmètre de test, théâtre de mocks, faux vert, suite complète, tests au sniper.
license: MIT
---

# Sniper Testing

## Pourquoi ce skill existe

Deux modes d'échec brûlent l'essentiel du temps de test. Le gonflement de
tests : lancer toute la suite pour un changement minuscule. Le théâtre de
mocks : des tests qui passent pendant que la vraie capacité est physiquement
cassée. Ce skill tue les deux.

## Règle 1 — le diff définit le périmètre, pas l'optimisme

Pendant la boucle d'itération fix/build, tu as interdiction de lancer la suite
de tests entière.

1. Lance `git diff --name-only HEAD` pour voir exactement quels fichiers tu as
   touchés.
2. Associe chaque fichier touché aux fichiers de test qui le couvrent
   directement (ex. `src/payments/refund.py` → `tests/test_refund.py`).
3. Annonce ta cible de test précise, puis lance UNIQUEMENT ces fichiers
   (ex. `pytest tests/test_refund.py`).
4. Un test déjà passé ne se relance pas, sauf si ton changement suivant touche
   du code qu'il exerce. Le diff définit le périmètre — pas l'optimisme, pas
   la peur.
5. À l'atterrissage — la porte du commit — lance UNE passe complète sur la
   suite de chaque module touché. Cette unique passe attrape les couplages
   indirects exactement une fois. La vitesse d'itération et un atterrissage
   sain font tous deux partie du job.

## Règle 2 — tue le théâtre de mocks

Un test de capacité doit asserter un effet de bord réel et physique :

- « produit une vidéo » → un vrai fichier existe sur le disque avec une taille
  > 0 octet.
- « stocke un souvenir » → la ligne se relit depuis une vraie base de données
  locale.
- « affiche le widget » → un vrai élément DOM existe sur la page.

Ne mocke pas la base de données. Ne mocke pas le système de fichiers. Ne mocke
pas les sockets réseau locales.

Le seul mock légal est la feuille de transport externe payante — l'appel HTTP
vers une API tierce facturée. Même là, le test doit traverser toute la vraie
logique autour : construction de la requête, routage, parsing de la réponse.
Mocke le fil, jamais le cerveau.

## Audite avant de faire confiance

Avant de t'appuyer sur un test, lis-le. Si c'est du théâtre de mocks — vert
grâce aux mocks, sans assertion physique — supprime le mock et réécris le test
pour asserter un vrai effet de bord. Un test qui ne peut pas échouer est pire
que pas de test : il certifie un mensonge, et tu construiras sur ce mensonge.

## Règles dures (une seule enfreinte fait échouer le skill)

- Aucun run de suite complète pendant l'itération.
- Aucune déclaration de vert sans assertion d'effet de bord réel.
- Aucun mock au-delà de la feuille de transport externe payante dans un test
  de capacité.
- Aucun atterrissage sans l'unique passe complète sur les modules touchés.

## Fonctionne bien avec

- [clean-code-gauntlet](../clean-code-gauntlet/SKILL.md) — le périmètre sniper alimente sa première porte
- [red-first](../red-first/SKILL.md) — écrire le test en échec avant le fix
- [seam-engineering](../seam-engineering/SKILL.md) — fixer la classe, puis balayer avec des tests ciblés
