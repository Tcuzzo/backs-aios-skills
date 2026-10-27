---
name: "fleet-dispatch"
description: "À utiliser quand un pair du pack envoie \"invoke skill fleet-dispatch\" ou quand cet agent doit lancer son propre échelon de flotte pour son propre travail. Appelle le résolveur de flotte local, lit FLEET_RECEIPT et renvoie la réponse avec sa provenance. Indépendant du modèle : l'échelle décide de l'ordre. Trigger words: fleet-dispatch, fleet rung, dispatch, role agent, role bot, invoke skill, fleet ladder. Déclencheurs : dispatch de flotte, échelon de flotte, invoquer un skill."
license: "MIT"
---

# Dispatch de flotte

Charge et exécute le guide canonique complet. Analyse le rôle et la spécification, appelle le résolveur de flotte local et renvoie ensemble la réponse et le FLEET_RECEIPT. Ne fige jamais un nom de modèle et ne contourne jamais le résolveur ; tout suit exactement l'original anglais.

[Canonical skill](../../../../skills/fleet-dispatch/SKILL.md)
