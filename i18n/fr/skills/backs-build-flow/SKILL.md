---
name: backs-build-flow
description: "Pour construire, corriger, examiner, reprendre ou livrer un travail qui exige de coordonner contexte, skills et vérification sans perdre le rythme d'exécution."
license: MIT
---

# BACKS Build Flow

Un responsable de l'intégration mène la demande du contexte à la livraison
vérifiée. Les spécialistes lui rendent des preuves ; ils ne relancent pas le
workflow. Pour une réponse simple sans build ni enquête, applique seulement les étapes pertinentes.

## Établir assez de contexte pour agir

1. Préserve l'objectif, les contraintes, l'autorisation déjà accordée et le résultat
   demandé. Choisis un mode : **build/correction**, **revue en lecture seule**,
   **enquête** ou **reprise/livraison**. Une revue n'autorise ni modification,
   ni installation, ni déploiement.
2. Réutilise le dossier de tâche actuel. Sinon, fais vérifier par
   [context-engineer](../context-engineer/SKILL.md) la cible, les instructions
   applicables, le chemin appelant/consommateur touché, le travail existant et le
   contrôle d'acceptation. [building-with-backs](../building-with-backs/SKILL.md)
   résout le checkout et la promotion. Épingle le `base_sha` d'avant modification ;
   actualise `candidate_sha` quand le travail est commité.
3. Applique [operator-essence](../operator-essence/SKILL.md) à l'opérateur actuel :
   charge l'extrait de contexte pertinent ou lance une fois son initialisation
   par insights si le profil manque. Observations qualitatives et preuves
   quantitatives guident communication et vérification ; elles n'accordent pas
   d'autorité et ne figent pas de personnalité. Signale les preuves limitées comme
   provisoires et poursuis le travail utile autorisé. Utilise
   [intent-compiler](../intent-compiler/SKILL.md) seulement si l'intention est ambiguë ;
   [operator-intent-deduction](../operator-intent-deduction/SKILL.md) décide si un
   choix important non résolu exige vraiment l'opérateur.
4. **Commence l'exécution dès que tu peux nommer la cible, la prochaine action
   concrète, les contraintes et un contrôle d'acceptation observable.** Toute
   lecture supplémentaire doit résoudre une question nommée pouvant modifier
   cette action. Ne cartographie pas tout le dépôt à répétition.

## Orienter les skills une fois, avec résultat et sortie

Charge les textes réels des skills pertinents ; un nom ou un reçu seul ne vaut
pas application. Réutilise les textes et preuves encore présents et actuels dans
le contexte. Après compaction, recharge seulement ce qu'exige la prochaine action.
Pour chaque spécialiste, précise but, preuve attendue et condition de sortie ;
consulte les références approfondies à la demande. Un dossier actuel suit
responsabilité, état et prochaine action ([format du dossier et de la relève](references/task-packet.md)).
Évite les registres en double.

Pour une adoption, [absorb](../absorb/SKILL.md) possède la carte des capacités et
l'intégration native. [rea-investigation](../rea-investigation/SKILL.md) apporte
les preuves de découverte ou de vérification pertinentes et retourne à son
appelant sans relancer Absorb récursivement. Le travail ordinaire sur les sources
utilise directement code et tests.

## Exécuter la boucle bornée RED → GREEN

Lie [bounded-loops](../bounded-loops/SKILL.md) avant toute répétition : une
`mission_id`, une échéance, un quota d'essais/tours et un budget de ressources
restant. Sous-agents, changements de modèle, constats de réparation et tours de
revue consomment ce même quota.

1. **RED :** [red-first](../red-first/SKILL.md) établit un vrai contrôle de comportement
   en échec avant la correction. Préserve son fichier scellé et son identité de
   référence. Pour une revue ou une recherche, utilise son contrat de preuve sans fabriquer de modifications.
2. **Build :** réalise le plus petit changement complet à la frontière responsable ;
   actualise consommateurs et surfaces de compatibilité concernés. Préserve le travail sans rapport.
3. **Lint et tests :** [sniper-testing](../sniper-testing/SKILL.md) déduit le périmètre
   de `base_sha` jusqu'au candidat actuel, travail en attente pertinent compris.
   Exécute les commandes applicables du dépôt : lint, contrôle de format, typage
   et tests de comportement. Consigne commandes exactes, révision, résultats et
   contrôles indisponibles ou inapplicables. Un arbre propre n'efface pas le périmètre déjà commité.
4. **Qualité :** [clean-code-gauntlet](../clean-code-gauntlet/SKILL.md) utilise les
   mêmes périmètre et budget pour qualité mesurée, mutation isolée bornée et
   revue indépendante. Ajoute des tests supplémentaires pour les nouvelles
   lacunes sans réécrire le RED scellé.
5. **Réagir aux preuves :** corrige un constat établi et relance seulement les
   contrôles touchés. Des échecs identiques répétés exigent une autre hypothèse
   ou tactique. Aux limites épuisées, sauvegarde le travail non résolu ; ne
   réinitialise jamais le budget et n'abaisse jamais les contrôles.

Exécute les contrôles agrégés obligatoires du dépôt une fois le candidat stabilisé.
Rapporte les capacités réelles de cet hôte ; n'invente ni outil, ni test, ni revue.

## Achever le résultat demandé

Poursuis paquetage, commit, publication et vérification autorisés lorsqu'ils font
partie de la demande. Si une approbation externe est vraiment nécessaire, prépare
d'abord le résultat complet et examinable. Informe l'utilisateur des constats,
de l'action actuelle, des preuves et de l'endroit où voir le travail en cours ; respecte sa cadence.

Distingue **tâche demandée livrée** du statut de capacité **PROVEN** du socle
invariant. Un patch local terminé ou une revue en lecture seule n'implique pas un
déploiement réel. Les contrôles obligatoires en échec ou indisponibles restent
visibles : sauvegarde **STILL-BUILDING** avec le blocage exact, le quota restant
et la prochaine action. En lecture seule, rends le dossier dans la réponse ou
un registre externe déjà autorisé ; ne crée pas implicitement de registre dans
le dépôt ni de fichier essence.
