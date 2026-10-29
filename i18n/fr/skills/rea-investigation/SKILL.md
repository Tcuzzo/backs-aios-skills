---
name: rea-investigation
description: Utilise REA pour examiner un exécutable distribué, un paquet ou un comportement observé à l’exécution lorsque cela aide à diagnostiquer ou réparer une panne.
license: MIT
---

# Investigation d’artefacts avec REA

Utilise le moteur REA installé et son skill autonome pour les binaires distribués, les paquets ou le comportement demandé à l’exécution. Pour les dépôts de code ordinaires, utilise directement le code et les tests. Ce pont n’installe ni REA, ni Ghidra, ni fournisseur, ni serveur MCP et ne prétend pas qu’ils sont disponibles.

1. Identifie la cible exacte et la question. Lis le skill REA original installé et ses références pertinentes dans le répertoire de skills de l’hôte, sans sélectionner récursivement ce pont. S’il manque, signale-le et poursuis avec les outils disponibles.
2. Utilise les outils REA connectés lorsqu’ils sont disponibles, ou la CLI REA installée. Pour les binaires natifs pris en charge, utilise un fournisseur Ghidra compatible déjà présent ; signale son absence ou son indisponibilité sans inventer de résultat ni installer de dépendances sans autorisation.
3. Commence par une inspection statique en lecture seule. Consigne l’identité de la cible, les identifiants de preuve, le périmètre, les limites et les inconnues. Les résultats statiques ne prouvent pas le comportement à l’exécution ; observe en direct seulement dans le cadre demandé et les limites déclarées d’exécution et de modification de l’outil.
4. Transmets les résultats à root-cause-first et repair-loop. Pour adopter une capacité open source, utilise absorb et ses contrôles de licence et de dépendances. Sélectionne par rôle et capacité via le fleet-ladder configuré, sans coder d’identifiant de modèle en dur. Pour une évaluation indépendante, utilise une nouvelle exécution de blind-tribunal séparée de l’auteur et un paquet figé expurgé des données de l’auteur, selon les capacités réelles du runtime.

Scaffold: REA by morluto, MIT license, https://github.com/morluto/rea.
Le moteur, le skill original et les fournisseurs sont installés séparément.
