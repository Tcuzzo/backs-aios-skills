---
name: fleet-ladder
description: Úsala antes de entregarle trabajo a un modelo — construir, calificar o un trabajo acotado de worker — o cuando un proveedor está caído y necesitas el orden de fallback. Resuelve la escalera VIVA de modelos: sondea lo que de verdad está arriba, elige el mejor disponible según un orden de fallback explícito, y falla con ruido cuando la escalera se agota. Trigger words: fleet, ladder, dispatch, fallback, model down, provider down, which model, availability. Disparadores: flota, escalera, despacho, respaldo, modelo caído, proveedor caído, qué modelo, disponibilidad.
license: MIT
---

# Fleet Ladder

Nunca armes a mano una llamada a un proveedor, y nunca claves un nombre de modelo
en un punto de llamada. Un solo resolutor es dueño de la pregunta "¿qué modelo
hace este trabajo ahora mismo?" — y responde desde la verdad viva, no desde la
opinión de un archivo de config.

## Cuándo ejecutarla

- Antes de CUALQUIER despacho a un modelo: construir, calificar, revisar o un trabajo acotado de worker.
- Cuando un proveedor está caído y necesitas saber qué cae hacia qué.
- En el momento en que te sorprendas tecleando un nombre de modelo en código o en una plantilla de prompt.

## Los pasos

1. **Declara el rol, no el modelo.** Cada trabajo pide un rol — `builder`,
   `grader` o `worker`. La escalera mapea roles a candidatos ordenados.
   - `builder`: implementa y repara.
   - `grader`: revisión independiente — estructuralmente nunca el mismo modelo que construyó.
   - `worker`: trabajos acotados y bien especificados. Aquí los peldaños baratos están bien.
2. **Lee la escalera desde la config.** Un archivo lista, por rol, los candidatos
   en orden de fallback explícito: el más fuerte primero, bajando hasta tu cola
   local de supervivencia (lo que puedas correr en tu propio hardware cuando todos
   los proveedores de nube están a oscuras). Para cambiar o agregar un modelo,
   edita ese archivo — nunca el código. Forma inicial:
   [ladder.example.yaml](ladder.example.yaml) — cópialo y cambia los marcadores.
3. **Sondea en vivo antes de confiar.** Un listado en la config es una afirmación,
   no la verdad. Una entrada vieja lista modelos que están muertos; también omite
   modelos que están vivos. Sondea al proveedor antes de despachar a un peldaño —
   una llamada al endpoint de modelos o una petición de un token, p. ej.:
   `curl -s "$PROVIDER_BASE_URL/v1/models" -H "Authorization: Bearer $API_KEY"`
   (o la misma forma contra el endpoint de chat con `"max_tokens": 1`).
   Cachea el resultado del sondeo por una ventana sensata — no martilles a los
   proveedores re-sondeando en cada llamada. Refresca la caché solo cuando de
   verdad necesites verdad fresca.
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

- **Ningún nombre de modelo en un punto de llamada.** El código pide un rol; la
  escalera responde con un modelo. Haz grep de tu código buscando literales de
  nombres de modelo — cada uno es un bug.
- **El sondeo vivo le gana a la config.** Si el humano dice que un modelo existe y
  la config lo niega, sondéalo. Comprobado-y-responde queda zanjado; una lista
  vieja no.
- **Builder y grader nunca se resuelven al mismo modelo** para el mismo cambio.
  Si la escalera los colapsaría en un solo modelo, el grader toma el siguiente
  peldaño independiente — o el trabajo falla con ruido.
- **Sondeo acotado.** Los sondeos son baratos, van a caché y respetan el backoff.
  Un loop apretado de reintentos contra un proveedor muerto está prohibido.
- **Sin fallback silencioso.** Cada paso hacia abajo en la escalera es visible en
  el log y en el reporte. Degradar calladito es como una ruta rota muere sin que
  nadie lo note.

## Combina bien con

- [model-fusion](../model-fusion/SKILL.md) — el panel y el juez resuelven sus modelos a través de esta escalera.
- [blind-tribunal](../blind-tribunal/SKILL.md) — los jurados vienen de familias distintas; la escalera elige los que están vivos.
- [bounded-loops](../bounded-loops/SKILL.md) — cadencia de sondeo, backoff y kill-switches.
