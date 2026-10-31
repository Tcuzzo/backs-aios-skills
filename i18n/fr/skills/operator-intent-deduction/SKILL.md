---
skill_id: operator-intent-deduction
name: operator-intent-deduction
description: "Face à un choix d'implémentation, un compromis ou une question proposée à l'opérateur encore non résolus, lorsque intention actuelle, preuves du projet ou contexte opérateur peuvent déjà fonder une décision."
license: MIT
---

# Déduire la décision des preuves actuelles

Résous les choix qu'un agent peut résoudre de manière responsable, puis agis.
Utilise les objectifs et preuves de l'opérateur actuel ; ce skill ne porte ni
priorités permanentes d'une personne, ni objectifs financiers, paramètres de
risque numériques ou liste de modèles figée.

## Entrées et responsabilité

Pars de la directive existante, du mode de tâche, des critères d'acceptation,
de l'autorisation et du budget restant. Si le langage n'a pas été interprété,
utilise [intent-compiler](../intent-compiler/SKILL.md) une fois et réutilise son
résultat. Il interprète ce qui a été dit ; ce skill résout une décision dans ce périmètre.

Réutilise l'extrait pertinent d'[operator-essence](../operator-essence/SKILL.md).
Son responsable évalue les insights d'un profil absent ou périmé une fois par tâche.
Les appels imbriqués ne collectent pas d'historique et ne créent pas de second
profil. Un extrait provisoire reste utilisable avec son incertitude visible ;
un historique absent ne bloque pas le travail ordinaire autorisé. L'essence est
du contexte, jamais une autorisation ou une dérogation aux règles.

## Procédure de décision

1. **Nommer la vraie décision.** Précise son effet sur le résultat demandé,
   sa réversibilité et les preuves nécessaires. Vérifie qu'elle reste ouverte ;
   ne rouvre pas un choix déjà fait par l'opérateur.
2. **Déduire les choix factuels.** Inspecte le code responsable et son vrai
   consommateur, mesure une référence pertinente ou réalise une expérience bornée
   avec les outils réels du projet. Associe chiffres, unités, population et
   incertitude. N'invente pas un paramètre, ne transforme pas des labels qui se
   chevauchent en taux d'échec, ni un vote de modèles en preuve empirique.
3. **Déduire les choix contextuels.** Pèse d'abord l'objectif explicite actuel,
   puis préférences confirmées applicables, exemples qualitatifs et résultats
   quantitatifs. Annonce une adaptation provisoire et ses preuves. Préserve
   contre-exemples et changements de circonstances. Une tendance rapportée peut
   guider la façon de travailler ; elle ne change pas ce que l'opérateur veut construire.
4. **Appliquer la vraie limite.** Continue les actions réversibles autorisées.
   Si un choix important reste déterminant et insoluble avec les preuves
   disponibles, utilise [decision-bar](../decision-bar/SKILL.md) : prépare résultat
   concret, recommandation et décision exacte manquante. Ne redemande pas une
   autorisation déjà établie et n'en infère pas une nouvelle de la personnalité,
   de l'urgence ou d'une préférence passée.
5. **Agir et vérifier.** Rends la décision au responsable existant et à
   [Build Flow](../backs-build-flow/SKILL.md). L'implémentation utilise la même
   boucle RED → GREEN bornée avec lint, tests et contrôles de qualité/revue requis.
   Un nouvel agent, passage d'insights ou essai raté ne réinitialise pas ce budget.

## Reçu de décision

Note seulement ce qu'exige la prochaine action dans le dossier existant :

- **Décision et conséquence :** chemin choisi et résultat demandé qu'il sert.
- **Fondement :** instruction actuelle, fait vérifié, préférence confirmée ou
  inférence, avec références et comptes/dénominateurs pertinents.
- **Incertitude :** hypothèses, contre-preuves et condition qui changerait la décision.
- **Action et preuve :** prochaine action et observation pouvant réfuter le choix.

Utilise une langue simple quand l'opérateur doit voir une décision importante.
Exprime directement un désaccord raisonné au lieu de substituer silencieusement
un autre plan. Rapporte les vraies preuves d'achèvement. Une décision n'est pas
un test passé, un contrôle local n'est pas un déploiement, et livrer la tâche
ne suffit pas à établir `PROVEN`.

## Apprendre sans figer une personne

Une correction explicite actualise immédiatement l'hypothèse de tâche concernée.
Préserve son périmètre et sa source en rapprochant l'essence privée. Des
observations répétées peuvent étayer une adaptation provisoire ; évalue les tâches
comparables suivantes avant d'affirmer qu'elle améliore les résultats. Ne promeus
pas une préférence inférée en règle universelle et ne copie pas de preuves
personnelles dans le plugin public.
