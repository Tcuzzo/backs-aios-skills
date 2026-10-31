---
name: rea-investigation
description: "Quand un exécutable distribué, paquet ou comportement runtime demandé exige REA pour diagnostic, découverte de capacités ou vérification d'une adoption native."
license: MIT
---

# Investigation d’artefacts avec REA

Utilise le moteur REA installé et son skill autonome pour les binaires distribués, les paquets ou le comportement demandé à l’exécution. Pour les dépôts de code ordinaires, utilise directement le code et les tests. Ce pont n’installe ni REA, ni Ghidra, ni fournisseur, ni serveur MCP et ne prétend pas qu’ils sont disponibles.

Utilise le dossier [BACKS Build Flow](../backs-build-flow/SKILL.md), le responsable
et le `task_mode` permis de l'appelant. Une enquête directe établit ce dossier une
fois. [bounded-loops](../bounded-loops/SKILL.md) possède échéance et quotas restants ;
réessais fournisseur, changements de modèle et relèves en héritent. Ce spécialiste
produit des preuves, il ne possède pas un second cycle d'adoption ou de réparation.

1. Résous cible exacte, identité/hash, question et phase : **découverte** de
   l'artefact amont ou **vérification** d'un résultat natif précis. Lis le skill
   original `reverse-engineer-anything` installé et ses références pertinentes
   dans le répertoire de skills hôte, sans sélectionner récursivement ce pont.
   S'il manque, signale-le et poursuis l'enquête utile avec les outils disponibles dans le budget existant.
2. Utilise les outils REA connectés lorsqu’ils sont disponibles, ou la CLI REA installée. Pour les binaires natifs pris en charge, utilise un fournisseur Ghidra compatible déjà présent ; signale son absence ou son indisponibilité sans inventer de résultat ni installer de dépendances sans autorisation.
3. Commence par une inspection statique en lecture seule. Consigne l’identité de la cible, les identifiants de preuve, le périmètre, les limites et les inconnues. Les résultats statiques ne prouvent pas le comportement à l’exécution ; observe en direct seulement dans le cadre demandé et les limites déclarées d’exécution et de modification de l’outil.
4. Rends un dossier de preuves à l'appelant : identité cible, phase, reçus de
   commandes/outils, identifiants de preuve, observations, distinction statique/
   runtime, inconnues et budget restant. L'appelant possède la suite : Absorb
   applique contrôles de licence/dépendances et intégration native ; le responsable
   de réparation applique root-cause-first et repair-loop. Ne relance aucun de
   ces cycles récursivement depuis le pont. Si la vérification trouve un défaut,
   rends l'observation pour un RED scellé et une boucle correction/contrôles bornée ;
   ne prétends pas que la réparation a eu lieu.
5. Sélectionne par rôle et capacité via le fleet-ladder configuré, sans identifiant
   de modèle figé. Si une évaluation indépendante est requise, utilise l'exécution
   fraîche disjointe de l'auteur et le dossier expurgé de blind-tribunal, selon les
   capacités réelles de l'hôte. Fournisseur absent ou budget épuisé produit une
   sauvegarde **STILL-BUILDING** avec observations utiles et prochaine action
   précise, jamais une preuve runtime inventée. L'enquête non bloquée reste dans son quota disponible.

Scaffold: REA by morluto, MIT license, https://github.com/morluto/rea.
Le moteur, le skill original et les fournisseurs sont installés séparément.
