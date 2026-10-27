---
name: "fleet-dispatch"
description: "Úsalo cuando un par del pack envía \"invoke skill fleet-dispatch\" o cuando este agente necesita despachar su propio peldaño de la flota para su propio trabajo. Llama al resolvedor local de la flota, lee FLEET_RECEIPT y devuelve la respuesta con su procedencia. Agnóstico de modelo: la escalera decide el orden. Trigger words: fleet-dispatch, fleet rung, dispatch, role agent, role bot, invoke skill, fleet ladder. Disparadores: despacho de flota, peldaño de flota, invocar skill."
license: "MIT"
---

# Despacho de flota

Carga y ejecuta la guía canónica completa. Analiza el rol y la especificación, llama al resolvedor local de la flota y devuelve juntos la respuesta y el FLEET_RECEIPT. Nunca fijes un nombre de modelo ni te saltes el resolvedor; todo sigue exactamente el original en inglés.

[Canonical skill](../../../../skills/fleet-dispatch/SKILL.md)
