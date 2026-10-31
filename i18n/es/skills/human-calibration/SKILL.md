---
name: human-calibration
description: "Úsala cuando una decisión de construcción, diseño, comunicación o UX importante necesite conocer las preferencias expresadas y el contexto de trabajo del operador."
license: MIT
---

# Conoce a tu humano

Aplica el pedido y las correcciones actuales del operador. Usa evidencia sobre
sus preferencias de trabajo para elegir explicaciones útiles, actualizaciones
de progreso y decisiones de diseño. Este conocimiento es contexto revisable,
nunca una personalidad fija ni un permiso.

## Una sola pasada de perfil

[operator-essence](../operator-essence/SKILL.md) controla el archivo privado de
contexto y su evidencia. Reutiliza su fragmento vigente de
[Build Flow](../backs-build-flow/SKILL.md). Si falta, ejecuta una sola vez el flujo
de insights disponible de esa skill, evalúa el informe/historial facilitado y
crea contexto provisional cuando la evidencia sea escasa. No reinicies la recogida
de insights desde cada skill posterior.

Un perfil existente designado por el operador puede aportar evidencia: conserva
fuente, fecha, estado de confirmación e incertidumbre al conciliarlo en la esencia.
No explores perfiles ajenos ni infieras quién es dueño de un archivo por un nombre
visible. Mantén los datos personales fuera del código público del plugin. Una tarea
de solo lectura puede pasar un fragmento en memoria sin escribir ningún perfil.

## Aplica lo conocido

- Las preferencias y correcciones explícitas actuales prevalecen sobre observaciones
  históricas. Los hechos del proyecto y las comprobaciones de aceptación siguen
  necesitando verificación.
- Distingue elecciones observadas de tendencias inferidas. Un diseño rechazado o
  pedidos repetidos de progreso respaldan una adaptación específica; no establecen
  personalidad, identidad, competencia ni tolerancia general al riesgo.
- Usa el fragmento relevante más pequeño: preferencia u observación, evidencia,
  adaptación propuesta e incertidumbre. Muestra al operador de dónde proviene.
- Conserva ambos lados de una tensión real, como profundidad de contexto y rapidez
  de ejecución. Resuélvela con una condición concreta de preparación y evidencia,
  sin reducir el objetivo.
- Una pregunta opcional puede resolver una incógnita material de gusto o comunicación.
  Haz primero trabajo útil autorizado. No exijas cuestionarios ni reconfirmes
  preferencias ya dadas solo porque empezó otra sesión.
- Captura correcciones y contraejemplos cuando esté autorizada la escritura del
  perfil. Una corrección actualiza el contexto; nunca reescribe silenciosamente la
  tarea ni concede autoridad para acciones ajenas.

## Salida

Devuelve un fragmento conciso al responsable existente de tarea. El usuario puede
inspeccionarlo y corregirlo. Adapta cómo comunica el agente y reúne evidencia;
mantén los mismos estándares de hechos, calidad y autorización para cada operador.

## Combina bien con

- [operator-essence](../operator-essence/SKILL.md) — evidencia privada e inicio de insights.
- [human-voice](../human-voice/SKILL.md) — comunicación clara en el registro solicitado.
- [intent-compiler](../intent-compiler/SKILL.md) — lenguaje ambiguo convertido en contrato de acción.
- [operator-intent-deduction](../operator-intent-deduction/SKILL.md) — decisiones a partir de la intención actual.
