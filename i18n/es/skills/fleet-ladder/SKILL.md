---
name: "fleet-ladder"
description: "Guía de selección por rol y capacidad antes del despacho; el paquete público no incluye resolutor ni ejecutable Fleet. Trigger words: fleet, ladder, dispatch, fallback, model down, provider down, which model, availability. Disparadores: flota, escalera, despacho, respaldo, modelo caído, proveedor caído, qué modelo, disponibilidad."
license: "MIT"
---

# Fleet Ladder
**Effort:** light — un solo sondeo vivo, cacheado, del peldaño antes de cualquier despacho. Elimina: despachos a proveedores muertos, y nombres de modelo clavados en los puntos de llamada que se rompen el día que el modelo se retira.

Esta skill describe la selección, pero no resuelve modelos por sí misma. El paquete público no incluye resolutor ni ejecutable Fleet; informa cualquier función ausente como una brecha de ejecución. No fijes identificadores de modelos en skills, prompts ni puntos de llamada.

## Cuándo ejecutarla

- Antes de CUALQUIER despacho a un modelo: construir, calificar, revisar o un trabajo acotado de worker.
- Cuando un proveedor está caído y necesitas saber qué cae hacia qué.
- En el momento en que te sorprendas tecleando un nombre de modelo en código o en una plantilla de prompt.

## Los pasos

1. **Declara rol y capacidades.** Lee la escalera configurada y su orden; elige un candidato apto según tarea, capacidad y disponibilidad. La configuración de ejemplo es solo una plantilla. Esta skill no clasifica ni filtra candidatos.
2. **Comprueba la independencia.** La revisión usa una ejecución nueva y separada del autor, con un paquete congelado sin contexto del autor. Elige un revisor capaz mediante la escalera configurada. Informa las restricciones adicionales como brechas del entorno.
Cualquier revisor capaz puede realizar la revisión en una sesión nueva y separada del autor; el modelo y el proveedor no son restricciones.
3. **Prueba inferencia real.** Una lista de modelos no demuestra inferencia, capacidad ni cuota. Ejecuta una inferencia real y acotada en el candidato; guarda el resultado en caché por un plazo razonable y respeta el backoff. Comprueba de nuevo la capacidad al cambiar de candidato.
4. **Baja la escalera, con ruido.** Despacha al mejor peldaño DISPONIBLE. Ante una
   falla de transporte, reporta la falla con ruido, y luego prueba el siguiente
   peldaño. Nunca saltes en silencio — el registro debe mostrar qué peldaños
   fallaron y por qué.
5. **El agotamiento falla con ruido.** Si todos los peldaños están caídos, levanta
   un error claro nombrando lo que se intentó. Un trabajo que no puede despacharse
   nunca triunfa en silencio, ni espera para siempre, ni degrada a una respuesta
   inventada.
6. **Registra la procedencia.** Añade cada despacho a un log: rol, modelo elegido,
   peldaños saltados y por qué. Después tienes que poder responder "¿quién hizo
   este trabajo en realidad?"

## Reglas duras — rompe una y la skill fracasó

- No fijes identificadores de modelos en skills, prompts ni llamadas; usa el rol y las capacidades de la configuración activa.
- Una prueba de inferencia real y acotada es necesaria; un catálogo por sí solo no basta.
- La revisión requiere una ejecución nueva separada del autor y un paquete congelado sin contexto del autor.
- Registra fallos y alternativas; informa los resolutores o mecanismos de aislamiento ausentes como brechas del entorno.


## Combina bien con

- [blind-tribunal](../blind-tribunal/SKILL.md)
- [bounded-loops](../bounded-loops/SKILL.md)
- [model-fusion](../model-fusion/SKILL.md)
