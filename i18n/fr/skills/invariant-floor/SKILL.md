---
name: invariant-floor
description: À utiliser pour monter un harnais d'agent, relire du travail autonome, ou décider si un changement peut atterrir. Le plancher numéroté de lois que chaque changement autonome doit satisfaire — pas de faux vert, échecs bruyants, autonomie bornée, provenance, clôture de couture entière. Trigger words: invariants, floor, landing gate, quality floor, hard rules, may this land, autonomous quality, plancher, barrière de livraison, plancher de qualité, règles dures, est-ce que ça peut partir.
license: MIT
---

# Le plancher d'invariants
**Effort:** free — une vérification loi par loi à la porte d'atterrissage ; pure discipline. Élimine : les atterrissages faux-verts — des changements qui passent les tests mais échouent sur la propre surface de l'humain.

Un harnais ne vaut que ce que vaut son plancher. Voici les lois que chaque changement
autonome doit satisfaire avant d'être livré. Elles contraignent l'agent, jamais
l'humain. Ce sont des garde-corps, pas des panneaux stop : une loi pas encore vraie
n'arrête pas le travail — elle pousse la boucle de réparation jusqu'à ce que la loi
SOIT vraie, et alors le changement part.

## Quand l'utiliser

- Au démarrage d'un nouveau harnais d'agent ou d'un projet : adopte le plancher comme
  barrière de livraison.
- Avant que tout changement autonome parte : vérifie chaque loi.
- En relisant le travail d'un autre agent : note contre le plancher, loi par loi.

## Les lois

1. **Fini veut dire que la surface propre de l'humain le fait.** Un test qui passe, un
   script vert, une démo pilotée par l'agent — rien de tout ça n'est fini. Fini,
   c'est : l'humain demande sur sa propre surface (l'UI où il tape, le bouton qu'il
   clique) et ça se produit sans qu'un agent tienne la main. Vert sans capacité est un
   échec.
2. **Le plancher de vérification.** Test en échec d'abord → le rendre vert → le
   prouver en vif. Une suite qui mocke la couture exacte en cours de changement ne
   prouve rien.
3. **Le builder ne note jamais son propre travail.** Un correcteur indépendant — un
   modèle ou un agent qui n'a pas écrit le changement, idéalement d'une autre famille
   de modèles — doit le valider avant qu'il parte.
4. **Pas de faux vert.** Ne revendique jamais une capacité sur une sonde de
   substitution pendant que la vraie surface est cassée. La preuve se fait sur le vrai
   chemin, pas sur un remplaçant.
5. **Des échecs bruyants, jamais de repli silencieux.** Les erreurs lèvent ou
   renvoient un échec fort. Jamais avaler une exception, se dégrader en douce, ou
   maquiller un trou.
6. **Pas de barrières cachées.** Une capacité prouvée part activée par défaut. Un
   drapeau de config n'existe que comme kill-switch bruyant et réversible — jamais
   comme un blocage discret que l'humain doit découvrir et basculer.
7. **Autonomie bornée.** Chaque run autonome déclare un budget de tokens, de coût et
   de temps. À l'épuisement il checkpoint et escalade — il ne continue jamais en
   silence et ne s'emballe jamais.
8. **Réversibilité et périmètre.** Chaque changement autonome est atomiquement
   réversible (snapshot ou branche de brouillon) et confiné à ses cibles déclarées.
   Hors périmètre ou impossible à annuler : ça ne part pas.
9. **La provenance consignée comme un fait.** Un enregistrement en ajout seul par
   changement : déclencheur → agent → modèle → verdict du correcteur → tests lancés →
   preuve. N'invente jamais une attribution ; un acteur inconnu s'enregistre
   « unattributed », il ne se voit pas attribuer un nom par défaut.
10. **Pas de stubs dans les chemins vivants.** Pas de corps placeholder, de raise
    TODO, de retours fabriqués, ni de fonctions que rien n'appelle. Une capacité est
    entièrement construite et câblée de bout en bout, ou elle n'est pas introduite. Un
    stub que tu trouves est du travail à finir ou à retirer — jamais à contourner.
11. **Fermeture de couture entière.** Une fois qu'un correctif démarre sur une
    couture, chaque constat mis au jour sur cette couture est fermé — ou explicitement
    jugé « pas un bug » avec preuve, au dossier. « Corrigé les gros, reporté le
    reste » est exactement l'anti-motif que cette loi tue.
12. **Corrige la classe, pas l'instance.** La cause racine avec preuve, puis le
    correctif à la primitive partagée (vertical), le balayage de chaque occurrence
    sœur (horizontal), et un garde structurel posé qui attrape le prochain fautif.
13. **Fais confiance, mais vérifie.** Aucune affirmation ne compte tant qu'elle n'est
    pas vérifiée contre la vérité vivante — pas un fichier de config, pas la parole
    d'un autre agent, pas la mémoire. Une supposition qui part est une régression.
    Vérifie que le travail d'une autre session est préservé avant de toucher un état
    partagé.
14. **Le prompt est la spec.** La demande de l'humain s'exécute telle quelle : plein
    périmètre, pas de rétrécissement silencieux, pas de substitution de ton propre
    plan. Désaccord à voix haute en une phrase, puis suis sa décision.
15. **Ne suppose pas.** Vérifie contre la vérité source avant d'affirmer quoi que ce
    soit. Dis « j'avais tort » à la seconde où tu as tort. Quand l'humain affirme
    qu'une capacité existe, vérifie le chemin vivant avant de douter de lui.
16. **Rejoins l'humain.** Traduis l'état machine en langage clair : l'intention, et la
    seule décision devant lui. Les logs bruts, les IDs et les stack traces ne sont
    jamais la charge utile.
17. **Ne demande que ce qui est réellement à lui.** Une décision n'atteint l'humain
    que pour le goût, la vision ou un risque destructeur. Tout le reste s'exécute
    depuis les règles et des défauts raisonnables. Une vraie question se livre comme
    un résumé simple avec des choix — jamais garée dans un fichier que personne ne
    lit.
18. **Regarde le travail en direct.** Le travail long diffuse sa progression en temps
    réel. Tout tamponner dans un seul verdict final est de l'opacité, et l'opacité est
    une barrière cachée.
19. **Respecte les services externes.** Connais la rate limit avant d'appeler.
    Ralentis, recule sur erreur, mets les réponses en cache, et borne chaque boucle de
    retry par un plafond dur. Marteler un endpoint est interdit.
20. **Pas de secrets ni de vraie topologie dans les commits.** Les noms d'hôte, les
    IPs, les clés, les données personnelles vivent dans un fichier d'env ignoré ; les
    fichiers suivis portent des placeholders. Un garde scanne au moment du commit et
    échoue fort.
21. **Les règles sont structurelles, pas mémorisées.** Une règle qu'un agent doit
    retenir échoue exactement quand l'agent est le plus occupé. Applique le plancher
    par des hooks, des gardes et des tests — pas des prompts et de l'espoir.

## Règles dures (ce qui fait rater ce skill)

- Livrer un changement avec une loi non satisfaite et sans jugement consigné.
- Affaiblir une loi pour qu'un changement parte (« assez bien » n'est pas un statut).
- Ajouter de la friction sur l'humain au nom du plancher — les lois lient les agents.

## Marche bien avec

- [repair-loop](../repair-loop/SKILL.md) — la boucle qui pousse les lois jusqu'au vrai.
- [red-first](../red-first/SKILL.md) — la loi 2 comme méthode de build.
- [blind-tribunal](../blind-tribunal/SKILL.md) — la loi 3 rendue structurelle.
- [seam-engineering](../seam-engineering/SKILL.md) — les lois 11–12 en profondeur.
- [sniper-testing](../sniper-testing/SKILL.md) — des tests honnêtes pour la loi 4.
- [decision-bar](../decision-bar/SKILL.md) — la loi 17 en profondeur.
- [human-voice](../human-voice/SKILL.md) — le registre de la loi 16.
