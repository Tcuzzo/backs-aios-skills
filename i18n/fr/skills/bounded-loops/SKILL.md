---
name: bounded-loops
description: "Avant tout travail susceptible de réessayer, sonder, itérer, distribuer des agents ou répéter des appels externes, notamment les boucles autonomes de build, correction, revue et adoption."
license: MIT
---

# Boucles bornées

Une mission a un seul quota restant. Réessai, agent, repli de modèle, tour de
revue, remise à zéro du contexte ou skill imbriqué le consomment ; ils ne le
reconstituent jamais. [Build Flow](../backs-build-flow/SKILL.md) possède les
transitions de tâche. Cette méthode possède la comptabilité du budget, les
réessais, l'annulation et les points de sauvegarde.

## Déclarer et transmettre le contrat

Avant la première action répétée, note dans le dossier de tâche existant :

- `mission_id`, responsable de l'intégration, objectif et acceptation mesurable.
- Échéance ou durée maximale, maximum d'essais/tours et plafonds de ressources/appels.
- Quota consommé et restant, limite inférieure de tours de l'épisode actuel,
  signature d'échec et prochaine action. Fixe un petit plafond interne explicite,
  souvent trois essais ; choisis-le pour cette tâche sans ériger l'exemple en règle universelle.
- Coût/tokens/appels mesurés quand disponibles. Les compteurs indisponibles restent
  inconnus ; n'invente ni zéro, ni allocation illimitée, ni budget fournisseur.
  Fixe des bornes de temps et d'essais applicables avec les compteurs exposés par l'hôte.

Hérite des limites plus strictes de l'utilisateur ou du projet. Si une tâche
ordinaire autorisée n'en fournit pas, choisis et annonce des bornes proportionnées,
puis agis sans nouvelle autorisation. Demande seulement si l'engagement réel de
ressources exige une autorisation. Une extension de budget demande une décision
explicite du responsable de mission et les autorisations opérateur nécessaires ;
changer d'agent ou de tactique ne constitue pas une extension.

## L'itération

1. Vérifie le quota restant avant de distribuer du travail. Alloue les plafonds
   enfants à l'intérieur, y compris en parallèle : réserve centralement leur
   maximum pour que le cumul ne dépasse pas le parent. Chaque enfant rend le
   quota consommé et inutilisé.
2. Exécute une action guidée par une hypothèse. En build/correction, préserve un
   vrai RED, applique la plus petite correction complète, exécute lint/typage/tests
   ciblés et rends les preuves de qualité via [sniper-testing](../sniper-testing/SKILL.md)
   et [clean-code-gauntlet](../clean-code-gauntlet/SKILL.md).
3. Sauvegarde résultats et quota restant aux frontières sûres. Un rédacteur
   actualise atomiquement l'état autorisé ; les agents lui rendent leurs preuves.
   Pour une revue strictement en lecture seule, utilise un registre externe déjà
   autorisé ou la réponse. La lecture seule n'autorise pas un registre dans le dépôt.
4. Un échec identique sans preuve nouvelle appelle une autre hypothèse ou tactique,
   pas un nouvel essai aveugle. Ferme l'épisode interne épuisé. Un autre épisode
   peut utiliser le reste du parent, en le comptabilisant explicitement.
5. À épuisement, annulation ou blocage d'un contrôle obligatoire : sauvegarde,
   explique le blocage et arrête de répéter. Poursuis du travail indépendant utile
   seulement si périmètre et allocation restante le permettent. Une capacité
   inachevée reste **STILL-BUILDING** ; un délai dépassé ou un contrôle sauté
   ne vaut jamais GREEN ou PROVEN.

## Appels externes et annulation

Respecte les limites publiées et Retry-After. Réutilise les résultats en cache ;
si les limites sont inconnues, commence prudemment et mesure. Emploie un recul
exponentiel borné face aux refus transitoires, avec durée et essais maximaux.
Ne traite pas les erreurs permanentes d'autorisation ou d'entrée comme transitoires.
Attente, recul et repli consomment la même échéance de mission.

Arrête à une frontière d'état sûre : consigne le travail en cours, sauvegarde,
annule. Ne lance pas un second rédacteur et ne laisse pas de boucle en arrière-plan
après annulation. Les nouvelles demandes orientent la mission actuelle à cette
frontière ; comptabilise explicitement le changement de périmètre sans remplacer
silencieusement l'objectif initial.

## Relève et sortie

Le destinataire reçoit la même identité de mission, les révisions base/candidat,
l'identité des tests scellés, le quota consommé et restant, les preuves et la
prochaine action. Il vérifie cet état avant de reprendre. Un nouveau contexte
n'est pas un nouveau budget.

Le succès exige les contrôles d'acceptation initiaux et la livraison demandée.
L'épuisement exige une sauvegarde honnête : ni tests affaiblis, erreurs avalées,
suppression de données, réussite inventée, ni boucle externe automatique à compteur rechargé.

Voir [session-handoff](../session-handoff/SKILL.md) pour continuer et
[fleet-ladder](../fleet-ladder/SKILL.md) avant un véritable dispatch de modèle configuré.
