---
name: fleet-ladder
description: À utiliser avant de confier n'importe quel travail à un modèle — build, notation, ou job de worker borné — ou quand un fournisseur est en panne et qu'il te faut l'ordre de repli. Résout l'échelle de modèles LIVE : sonde ce qui répond vraiment, choisit le meilleur disponible selon un ordre de repli explicite, échoue bruyamment quand l'échelle est épuisée. Trigger words: fleet, ladder, dispatch, fallback, model down, provider down, which model, availability, échelle de modèles, repli, modèle en panne, fournisseur à terre, quel modèle, disponibilité.
license: MIT
---

# Fleet Ladder — l'échelle de la flotte
**Effort:** light — une sonde en direct, mise en cache, du barreau avant tout dispatch. Élimine : les dispatches vers des providers morts, et les noms de modèles codés en dur aux points d'appel, qui cassent le jour où le modèle part à la retraite.

Ne bricole jamais un appel fournisseur à la main, et ne code jamais un nom de modèle en
dur sur un site d'appel. Un seul résolveur possède la question « quel modèle fait ce
travail, là, maintenant ? » — et il répond depuis la vérité vivante, pas depuis
l'opinion d'un fichier de config.

## Quand la dérouler

- Avant TOUT envoi de travail à un modèle : build, notation, revue, ou job de worker
  borné.
- Quand un fournisseur est à terre et que tu dois savoir ce qui se replie sur quoi.
- À l'instant où tu te surprends à taper un nom de modèle dans du code ou un template
  de prompt.

## Les étapes

1. **Déclare le rôle, pas le modèle.** Chaque job demande un rôle — `builder`,
   `grader` ou `worker`. L'échelle associe les rôles à des candidats ordonnés.
   - `builder` : implémente et répare.
   - `grader` : la revue indépendante — structurellement jamais le même modèle que
     celui qui a construit.
   - `worker` : des jobs bornés et bien spécifiés. Les barreaux moins chers suffisent
     ici.
2. **Lis l'échelle depuis la config.** Un fichier liste, par rôle, les candidats en
   ordre de repli explicite : le plus fort d'abord, jusqu'à ta queue de survie locale
   (ce que tu peux faire tourner sur ton propre matériel quand tous les fournisseurs
   cloud sont éteints). Pour changer ou ajouter un modèle, édite ce fichier — jamais
   le code. Forme de départ : [ladder.example.yaml](ladder.example.yaml) — copie-le,
   remplace les valeurs d'exemple.
3. **Sonde le vif avant de croire.** Une entrée de config est une affirmation, pas la
   vérité. Une liste périmée cite des modèles morts ; elle omet aussi des modèles
   vivants. Sonde le fournisseur avant d'envoyer vers un barreau — un appel à
   l'endpoint des modèles ou une requête à un token, par ex. :
   `curl -s "$PROVIDER_BASE_URL/v1/models" -H "Authorization: Bearer $API_KEY"`
   (ou la même forme sur l'endpoint de chat avec `"max_tokens": 1`).
   Mets le résultat de la sonde en cache pour une fenêtre raisonnable — ne martèle pas
   les fournisseurs en re-sondant à chaque appel. Ne rafraîchis le cache que quand il
   te faut vraiment de la vérité fraîche.
4. **Descends, à voix haute.** Envoie au meilleur barreau DISPONIBLE. Sur une panne de
   transport, signale l'échec fort, puis tente le barreau suivant. Ne saute jamais en
   silence — le registre doit montrer quels barreaux ont échoué et pourquoi.
5. **L'épuisement échoue fort.** Si tous les barreaux sont à terre, lève une erreur
   claire qui nomme ce qui a été tenté. Un job impossible à envoyer ne réussit jamais
   en silence, n'attend jamais pour toujours, et ne se dégrade jamais en réponse
   inventée.
6. **Journalise la provenance.** Ajoute chaque envoi à un journal : rôle, modèle
   choisi, barreaux sautés et pourquoi. Plus tard, tu dois pouvoir répondre à « qui a
   réellement fait ce travail ? »

## Règles dures — une seule cassée et le skill a échoué

- **Aucun nom de modèle sur un site d'appel.** Le code demande un rôle ; l'échelle
  répond un modèle. Greppe ta base de code pour les littéraux de noms de modèles —
  chacun est un bug.
- **La sonde vivante bat la config.** Si l'humain dit qu'un modèle existe et que la
  config n'est pas d'accord, sonde-le. Vérifié-et-ça-répond, c'est réglé ; une liste
  périmée, non.
- **Builder et grader ne se résolvent jamais sur le même modèle** pour le même
  changement. Si l'échelle devait les écraser sur un seul modèle, le grader prend le
  barreau indépendant suivant — ou le job échoue fort.
- **Sondage borné.** Les sondes sont bon marché, en cache, et respectent le backoff.
  Une boucle de retry serrée contre un fournisseur mort est interdite.
- **Pas de repli silencieux.** Chaque marche descendue est visible dans le journal et
  dans le rapport. Se dégrader en douce, c'est comme ça qu'une route cassée meurt sans
  que personne ne le remarque.

## Marche bien avec

- [model-fusion](../model-fusion/SKILL.md) — le panel et le juge résolvent leurs modèles par cette échelle.
- [blind-tribunal](../blind-tribunal/SKILL.md) — les jurés viennent de familles différentes ; l'échelle en choisit des vivants.
- [bounded-loops](../bounded-loops/SKILL.md) — la cadence de sonde, le backoff et les kill-switchs.
