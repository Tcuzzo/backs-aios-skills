---
name: "repair-loop"
description: "Pour corriger un bug, fermer un problème signalé, améliorer une frontière partagée ou reprendre une réparation bornée inachevée. Trigger words: repair loop, dev mode, fix this, uplift, close the seam, dev build, boucle de réparation."
license: "MIT"
---

# Repair Loop
**Effort:** light — la boucle elle-même est de la discipline plus une passe de notation indépendante ; les étapes plus lourdes qu'elle enchaîne (gauntlet, tribunal) portent leurs propres tampons et ne se déclenchent que sur les changements qui livrent. Élimine : les atterrissages verts-mais-cassés, et le rework de bug rouvert qu'ils coûtent.

La boucle par défaut pour tout fix, clôture de bug ou uplift. C'est un
comportement, pas une machinerie d'approbation : elle n'ajoute aucune barrière
et aucune friction pour l'humain. Elle lie l'agent à une discipline qui rend
« vert mais cassé » structurellement difficile à livrer.

## Rejoindre la tâche actuelle

Utilise [BACKS Build Flow](../backs-build-flow/SKILL.md) pour le dossier,
l'essence opérateur et un responsable unique. Réutilise règles applicables,
contexte, textes chargés et preuves déjà établis par l'appelant ; actualise
seulement ce qui a changé. Un appel direct établit le contexte manquant une fois.
Charge socle invariant et understanding-gates requis s'ils ne sont pas disponibles ;
utilise wayfinder seulement pour une route ouverte. Ne relance pas le play de
build extérieur pour un constat de réparation.

[bounded-loops](../bounded-loops/SKILL.md) possède échéance partagée et essais/tours
restants. Préserve `mission_id`, `task_mode`, `base_sha` épinglé et `candidate_sha`
actuel à travers reproduction, éditions, outils, modèles, revues et relèves.
Un appel imbriqué ne recharge jamais le budget. Revue et diagnostic rendent des
preuves sans édition ni promotion ; construire exige ce périmètre autorisé.

## La boucle

1. **Ancrer le chemin touché.** Vérifie règles, sources actuelles du projet,
   contrats appelants et contrôles existants. Réutilise les preuves actuelles
   pertinentes au lieu de répéter l'audit du dépôt entier.
2. **Reproduis sur la vérité live.** Vois l'échec toi-même, sur le vrai chemin
   que l'humain utilise — pas une sonde proxy, pas la parole du rapport de bug.
   Pas de reproduction, pas de fix.
3. **Test de contrat rouge.** Écris un test en échec qui capture le défaut, et
   committe-le avant le fix. Prouve qu'il est vraiment rouge. Le fix le fait
   passer au vert ; le fix n'édite jamais le test. Voir
   [red-first](../red-first/SKILL.md).
4. **Fixe la CLASSE à la couture** — pas un patch ponctuel par symptôme. La
   formule complète vit dans [seam-engineering](../seam-engineering/SKILL.md).
5. **Exécuter les contrôles ciblés.** Avec [sniper-testing](../sniper-testing/SKILL.md),
   déduis le périmètre du diff agrégé entre `base_sha` épinglé et `candidate_sha`,
   plus les chemins en attente possédés. Exécute les vraies commandes lint,
   typage et tests du dépôt pour ce périmètre. Consigne commande, résultat et
   révision. Marque un contrôle inapplicable **N/A** avec sa raison ; un outil
   requis absent est une lacune. N'installe pas d'outils arbitraires et n'invente
   pas de contrôle réussi. Un test scellé reste identique octet pour octet.
6. **Mesurer dans le workflow.** Exécute [clean-code-gauntlet](../clean-code-gauntlet/SKILL.md)
   pour qualité et mutation bornée du candidat. Examine un mutant survivant ;
   s'il révèle une lacune, ajoute un test dans un fichier distinct en préservant
   le RED initial. Corrige la frontière responsable et relance les contrôles
   affectés dans le même budget restant ; n'affaiblis jamais une barrière pour GREEN.
7. **Note indépendante.** Un correcteur qui n'a pas écrit le changement —
   dans une session vierge et disjointe de l'auteur — doit le valider.
   Le builder ne note jamais son propre travail. Voir
   [blind-tribunal](../blind-tribunal/SKILL.md).
8. **Vérifie le travail concurrent.** Avant de modifier un état partagé,
   vérifie que le travail en vol des autres sessions est préservé (sur une
   branche ou un commit). Ne committe et ne nettoie jamais du travail qui n'est
   pas le tien.
9. **Vérifier et atterrir dans le périmètre.** Une passe complète des suites
   touchées à l'atterrissage, plus les contrôles projet requis, puis la procédure
   de livraison autorisée. Vérifie sur l'UI ou la commande réellement utilisée et
   note la révision exacte du candidat/installée. Tests locaux et preuves
   statiques amont n'établissent pas une livraison réelle. Ferme chaque constat
   de cette frontière ou consigne un verdict explicite et étayé « pas un bug ».
   « Corrigé le gros, reporté le reste » n'atterrit jamais.

## Itérer dans le budget de mission

Un contrôle en échec fournit l'hypothèse bornée suivante. Réessaie ou choisis une
route configurée capable seulement dans le quota restant ; changer de modèle ne
crée pas une nouvelle mission. Applique les règles de stagnation et d'épuisement
de bounded-loops. À une limite, sauvegarde **STILL-BUILDING** avec candidat,
tests scellés, preuves d'échec, contrôles non satisfaits et prochaine action
exacte. Termine le travail utile autorisé qui ne consomme pas un quota épuisé.
Un constat ouvert bloque l'atterrissage sans effacer le progrès ni devenir un
verdict **PROVEN** inventé.

## Règles dures — une seule suffit à faire échouer le skill

- Fix livré sans reproduction sur la vérité live.
- Test écrit après le fix, ou édité par le fix.
- Symptôme rafistolé pendant que la classe reste ouverte à la couture.
- Capacité déclarée verte sur un proxy pendant que le chemin propre de l'humain
  est cassé.
- Builder qui a noté son propre changement.
- Un constat remonté puis reporté en silence à l'atterrissage.
- Boucle réinitialisée, abandonnée en silence ou déclarée verte avec une barrière non satisfaite.

## Rapport

Deux mots — **PROVEN** ou **STILL-BUILDING** — plus l'intention en langage
simple et l'unique décision posée devant l'humain, s'il y en a une. Les
questions ne vont à l'humain que pour le goût, la vision, ou le risque
destructeur ; voir [decision-bar](../decision-bar/SKILL.md).

## Fonctionne bien avec

- [incident-closure](../incident-closure/SKILL.md) — quand l'humain signale une casse, cette boucle tourne dans une clôture complète.
- [red-first](../red-first/SKILL.md) · [seam-engineering](../seam-engineering/SKILL.md) · [sniper-testing](../sniper-testing/SKILL.md)
- [blind-tribunal](../blind-tribunal/SKILL.md) · [clean-code-gauntlet](../clean-code-gauntlet/SKILL.md)
