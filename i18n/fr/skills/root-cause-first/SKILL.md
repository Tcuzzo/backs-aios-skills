---
name: root-cause-first
description: À utiliser face à un bug coriace, un échec silencieux, une chasse à la régression, ou un changement risqué qui pourrait casser en douce un consommateur en aval. Pas de fix sans enquête — lire l'erreur, la reproduire à la demande, vérifier les changements récents, instrumenter les frontières de composants, remonter le flux de données jusqu'à la source. Trigger words: debug, root cause, why is this failing, silent failure, regression, works in tests but fails live, systematic debugging, cause racine, pourquoi ça échoue, échec silencieux, régression, ça passe en test mais casse en live, débogage systématique.
license: MIT
---

# Root Cause First

Pas de fix sans enquête. Un patch fait avant de comprendre l'échec corrige la
mauvaise chose, cache le vrai bug, et casse quelque chose en aval. Ton produit
n'est pas un patch — c'est une cause racine prouvée par une sonde décisive, et
un fix prouvé sans régression.

Deux lois gouvernent tout ce qui suit :

1. **Aucune supposition — le code, les données et le système live sont la
   vérité ; les notes ne sont que des indices.** Un commentaire, un souvenir,
   une conclusion passée, même ta propre dernière phrase est une hypothèse tant
   qu'une sonde ne l'a pas confirmée. Les mots « tous / chaque / aucun »
   déclenchent une vérification en trois points : l'environnement, une
   recherche sur tout le repo, et un scan de chaque appelant.
2. **Un contre-exemple vérifié tue la conclusion précédente immédiatement.**
   Quand une sonde contredit ce que tu croyais, dis simplement « je me suis
   trompé — en fait c'est X », puis repars du fait nouveau. Ne maquille jamais.

## La boucle (dans l'ordre ; ne saute rien)

1. **Lis l'erreur.** Énonce le symptôme en une phrase précise. Lis le vrai
   message, pas ce que tu t'attends à y lire. Nomme le rayon d'impact : qu'est-ce
   qui dépend de la chose que tu soupçonnes ?
2. **Reproduis.** Fais survenir l'échec à la demande — en live, ou dans un test
   en échec. **Chronomètre-le.** Un « échec » qui revient en millisecondes quand
   le vrai travail prend des secondes, c'est une exception avalée tôt, pas du
   vrai travail qui échoue. L'écart de timing est lui-même un indice.
3. **Vérifie les changements récents.** Diffe ce qui a changé depuis que ça
   marchait — code, config, environnement, dépendances. Si l'historique est
   long, bissecte-le.
4. **Cartographie les consommateurs.** Pour un bug dans une surface partagée,
   liste chaque appelant et comment chacun l'utilise (comparaison de chaîne
   exacte ? booléen ? liste ?). La vraie régression se cache d'habitude dans
   une comparaison exacte en aval, pas dans le bouton que tu tournes.
5. **Instrumente les frontières.** Logge ou sonde à chaque couture de
   composant — ce qui entre, ce qui sort. Remonte la mauvaise donnée en
   arrière, frontière par frontière, jusqu'à atteindre la source. Fixe la
   source, jamais le symptôme.
6. **Cause racine par hypothèse.** Formule une hypothèse falsifiable. Trouve LA
   sonde décisive qui la sépare des alternatives, et lance uniquement
   celle-là. Ne tire pas tout le pipeline « pour voir ce que ça donne ».
7. **Fixe chirurgicalement, à la bonne couture.** Le plus petit changement qui
   résout la cause racine. Préfère la source partagée unique (un normaliseur,
   un runner) à l'édition de N points d'appel. Quand c'est possible, rends le
   fix inerte sur le chemin qui marche — il n'y change prouvablement rien et ne
   s'active que sur le chemin cassé. Aucun refactor voisin embarqué.
8. **Prouve-le.** Écris le test en échec qui reproduit le bug ; regarde-le
   passer au rouge ; fixe ; regarde-le passer au vert. Puis lance les tests de
   chaque chemin consommateur cartographié à l'étape 4 — le vert là-bas est ton
   plancher de zéro régression. Une suite qui mocke la couture exacte qui a
   échoué ne prouve rien.
9. **Vérifie en live.** Pilote le vrai système — vraies requêtes, vraie base de
   données, vrais logs. Jamais un script sidecar qui importe le code dans ton
   propre process. Capture les preuves avant/après.
10. **Apprends.** Note le symptôme, la sonde décisive, la cause racine, et
    l'anti-patron qui l'a cachée, pour que le prochain bug de cette forme coûte
    moins cher.

## Construis la boucle de reproduction AVANT de théoriser

Si tu te surprends à lire du code pour bâtir une théorie avant qu'une commande
capable de virer au rouge existe — stop. Pas de commande capable de rouge, pas
de théorie. Un signal serré passe/échoue qui vire au rouge sur CE bug est le
plus gros levier de débogage qui soit. Investis un effort disproportionné ici.

Façons d'en construire une, en gros dans l'ordre : un test en échec ; un script
HTTP contre un serveur de dev ; un run CLI avec une entrée fixture, diffé
contre un instantané connu bon ; un script de navigateur headless ; une vraie
charge utile capturée, rejouée dans le chemin de code en isolation ; un harnais
jetable qui appelle une seule fonction ; une boucle de fuzz sur des entrées
aléatoires ; un harnais de bissection pour que le bisect automatisé marche ;
une boucle différentielle (même entrée dans l'ancienne et la nouvelle version,
diff des sorties).

Puis resserre-la : plus rapide (cache le setup, réduis la portée), plus
tranchante (asserte le symptôme précis, pas « ça n'a pas crashé »),
déterministe (fige le temps, seede le RNG, gèle le réseau). Une boucle
déterministe de deux secondes est un super-pouvoir.

Pour les bugs intermittents, vise un taux de reproduction plus haut, pas une
repro propre : boucle le déclencheur 100 fois, ajoute du stress, resserre les
fenêtres de timing. Un flake à 50 % se débogue ; un flake à 1 %, non.

Si tu ne peux vraiment pas construire de boucle, arrête-toi et dis-le. Liste ce
que tu as essayé et demande à ton humain un accès, un artefact capturé, ou une
instrumentation temporaire. Ne théorise pas sans boucle. Et si aucune couture
n'existe qui puisse répliquer le vrai schéma d'appel, cette absence EST un
constat — signale le trou d'architecture après l'atterrissage du fix.

## Anti-patrons (comment les bugs coriaces restent en vie)

- Conclure d'une note ou d'un commentaire sans sonde.
- Fixer avant de reproduire.
- Croire une suite verte qui mocke la couture exacte qui échoue en live.
- Vérification sidecar — importer le code au lieu de piloter le système live.
- Changer un bouton de config sans cartographier les consommateurs à
  comparaison exacte qu'il alimente.
- Des refactors larges embarqués avec un fix.
- Dire « tous / chaque / aucun » sans la vérification en trois points.

## Fonctionne bien avec

- [red-first](../red-first/SKILL.md) — committer le test en échec avant le fix.
- [sniper-testing](../sniper-testing/SKILL.md) — tests ciblés pendant l'itération.
- [seam-engineering](../seam-engineering/SKILL.md) — fixer la classe, pas l'instance.
- [repair-loop](../repair-loop/SKILL.md) — le cycle complet fixer-et-atterrir.

> Crédit d'échafaudage : Matt Pocock, diagnosing-bugs (mattpocock/skills). La composition et les règles dures ici sont BACKS AIOS.
