---
name: "fleet-dispatch"
description: "Use quando um par do pack enviar \"invoke skill fleet-dispatch\" ou quando este agente precisar despachar seu próprio degrau da frota para o próprio trabalho. Chama o resolvedor local da frota, lê o FLEET_RECEIPT e devolve a resposta com a procedência. Agnóstico de modelo: a escada decide a ordem. Trigger words: fleet-dispatch, fleet rung, dispatch, role agent, role bot, invoke skill, fleet ladder. Gatilhos: despacho da frota, degrau da frota, invocar skill."
license: "MIT"
---

# Despacho da frota

Carregue e execute o guia canônico completo. Analise o papel e a especificação, chame o resolvedor local da frota e devolva juntos a resposta e o FLEET_RECEIPT. Nunca fixe um nome de modelo nem pule o resolvedor; tudo segue exatamente o original em inglês.

[Canonical skill](../../../../skills/fleet-dispatch/SKILL.md)
