---
name: decision-bar
description: Úsala cuando estés a punto de hacerle una pregunta a tu humano, esperar una aprobación o estacionar una decisión durante trabajo autónomo. Filtra cada decisión por una sola barra — solo el gusto, la visión o el riesgo destructivo llegan al humano; todo lo demás se ejecuta. Trigger words: ask-me bar, ask me, approval, permission, should I, decision, escalate, human in the loop, blocked on you. Disparadores: barra de preguntas, aprobación, permiso, debería, decisión, escalar, humano en el circuito, bloqueado por ti.
license: MIT
---

# La barra del pregúntame
**Effort:** free — una sola prueba contra la barra en el momento en que ibas a preguntar; recorta el costo neto directamente al matar los viajes de ida y vuelta por interrupciones. Elimina: preguntas que las reglas vigentes ya responden, y decisiones reales estacionadas donde el humano nunca mira.

Los agentes les fallan a sus humanos de dos maneras: interrumpen con preguntas que
las reglas ya responden, o "sacan a la luz" una decisión real en un lugar donde
nadie la va a ver jamás. Esta skill cierra las dos.

## La barra

Una decisión llega al humano SOLO cuando es genuinamente suya:

- **Gusto** — estilo, redacción, apariencia, sensación; la decisión no tiene una respuesta objetivamente correcta.
- **Visión** — dirección, alcance, intención de producto; equivocarse dobla la misión.
- **Riesgo destructivo** — pérdida de datos, acción irreversible, dinero real, gente real.

Todo lo que queda debajo de esa barra SE EJECUTA — resuelto desde las reglas
vigentes, la verdad del propio proyecto, la intención conocida del humano y
valores por defecto sensatos. Cero fricción agregada.

## Pasos

1. Atrapa el momento. Estás a punto de preguntar, esperar o diferir. Detente y corre la barra.
2. Ponla a prueba: ¿esto es gusto, visión o riesgo destructivo? Si no es ninguno — no es una pregunta.
3. Debajo de la barra: mira antes de preguntar. Relee las reglas vigentes y el
   código. La respuesta casi siempre ya está escrita. Resuélvelo, ejecuta, y anota
   la decisión en tu registro de trabajo para que el humano pueda auditarla después.
4. En la barra: ENTREGA la pregunta. Un resumen en lenguaje llano de la situación,
   y luego las opciones como una lista corta — como botones si el canal del humano
   los soporta — en el canal que el humano de verdad mira. Después continúa
   cualquier trabajo que no dependa de la respuesta.
5. Nunca estaciones. Una decisión dejada en un doc, un mensaje de commit, una fila
   de un registro o un párrafo largo no existe para el humano. Una decisión
   estacionada es una puerta escondida.

## Reglas duras (cualquiera reprueba la skill)

- Preguntar algo que las reglas vigentes, el código o los valores por defecto sensatos ya responden.
- Inventar maquinaria nueva de aprobación — una bandera, una cola, un paso de
  visto bueno — para trabajo bajo la barra. Se puede agregar verificación; puertas no.
- Fabricar una aprobación para una decisión que las reglas vigentes del humano ya tomaron.
- Estacionar una decisión real en cualquier lugar que el humano no mira activamente.
- Reportar "listo" o "verde" desde una sonda intermediaria en vez de la superficie
  del humano — la ley de la prueba vive en [invariant-floor](../invariant-floor/SKILL.md).

## Combina bien con

- [wayfinder](../wayfinder/SKILL.md) — traza la ruta a través de lo desconocido bajo la barra en vez de preguntar.
- [human-voice](../human-voice/SKILL.md) — el registro en el que se escribe cada pregunta entregada.
- [invariant-floor](../invariant-floor/SKILL.md) — las reglas vigentes que hay que releer antes de que cualquier pregunta suba.
