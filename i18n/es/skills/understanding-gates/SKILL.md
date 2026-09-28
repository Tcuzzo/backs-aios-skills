---
name: "understanding-gates"
description: "Úsala cuando un build, fix o mejora avanza de la intención hacia la entrega y necesitas prueba de que aún coincide con la petición original. Interroga Diseño, Plan, Build, Test y Entrega con veredictos de aprobar/revisar/rechazar, fallos nombrados como objetivos de reparación, y una recorrida después de cada reparación. Trigger words: understanding, stage gates, validate build, spec match, verdict, green but wrong, echo check, done means done, entendimiento, compuertas por etapa, validar el build, coincide con la spec, veredicto, verde pero mal, chequeo de eco, terminado es terminado."
license: "MIT"
---

# Understanding Gates
**Effort:** light — una pasada de validador por etapa, puntuada contra el pedido original y re-corrida después de cada reparación. Elimina: la deriva validada contra una paráfrasis — el build que aterriza en verde pero responde una pregunta que nadie hizo.

Una disciplina de validación para builds. Interroga el trabajo en cinco etapas —
Diseño, Plan, Build, Test, Entrega — siempre contra la petición ORIGINAL, nunca
contra la propia reformulación que el trabajo hizo de ella. Cada compuerta
devuelve evidencia: puntajes, un veredicto, fallos nombrados y acciones de
reparación. Ata al agente, no al humano: ningún paso de aprobación nuevo, cero
fricción para la persona que pidió.

## Cuándo correrla

- Cualquier build, fix o mejora que va a aterrizar en algún lugar real.
- Cada vez que estás por decir "terminado" y la única prueba es un test verde.
- Después de cada reparación, sobre la misma etapa que falló.

## Etapa 0 — anclar la intención

Antes de puntuar nada, fija el ancla de comparación: las palabras ORIGINALES del
humano, más una directiva traducida de una línea (ver
[intent-compiler](../intent-compiler/SKILL.md)). Cada compuerta puntúa contra
esa ancla. Nunca puntúes contra tu propia paráfrasis — una paráfrasis deriva, y
entonces cada compuerta valida en silencio la deriva en vez de la petición.

## Las cinco compuertas

Cada compuerta hace una pregunta contra la intención original:

| Etapa | Pregunta |
| --- | --- |
| Diseño | ¿La spec es clara y fiel a la petición original? |
| Plan | ¿El plan responde a la intención y encaja con la superficie donde se entrega? |
| Build | ¿El código satisface la spec sin deriva? |
| Test | ¿Los tests ejercitan el comportamiento real, no un sustituto? |
| Entrega | ¿Aplica limpio, falla en voz alta, y la afirmación de entrega sobrevive un chequeo de hechos? |

Puntúa CADA compuerta con los mismos cinco lentes, cada uno de 0–4: coincidencia
con la spec, encaje arquitectónico, seguridad de tipos, testeabilidad, seguridad
— formulados para la etapa (en Diseño, "testeabilidad" pregunta si la spec es
comprobable; en Entrega, si la afirmación de entrega lo es). Consolidado: suma
los cinco lentes (0–20), multiplica por 5 — ese es el puntaje de veredicto de la
compuerta, de 0–100. Registra cada lente, no solo el total — el total esconde
cuál lente falló.

## Veredictos

Consolida los lentes en un puntaje de 0–100 y ubícalo en su banda:

- **Aprobar** (80+): evidencia fuerte. Aun así no es prueba de terminado — ver
  la segunda ley.
- **Revisar** (60–79): existen fallos nombrados. Cada uno es un objetivo de
  reparación.
- **Rechazar** (menos de 60): el trabajo no da con la intención. Regresa una etapa.

Un veredicto sin fallos nombrados detrás es un veredicto de poca información.
Exige la lista.

## Disciplina de reparación

1. Mantén la intención original como ancla de cada recorrida.
2. Registra los puntajes por lente, no solo el número general.
3. Trata cada fallo nombrado como objetivo de reparación. Ningún fallo es decoración.
4. Repara, y luego VUELVE A CORRER LA MISMA COMPUERTA. Una reparación sin
   recorrida es solo una afirmación.
5. Nunca asciendas confianza a preparación. Deciden los tests y la superficie real.

## Las dos leyes

**1. La ley del eco.** Un chequeo que solo puede estar de acuerdo es un eco, no
un validador. La prueba de honestidad es la refutación: aliméntalo con una
afirmación que sabes falsa y míralo reprobarla. Si le pasa la mentira, el
chequeo es teatro. Corolario sobre mocks: mockea solo la hoja externa inestable
— una API de pago, una red intermitente. Nunca mockees el órgano cuyo
comportamiento ES la prueba; su puntuación, su extracción de afirmaciones y su
lógica de pasa/falla deben correr de verdad.

**2. Necesario, no suficiente.** Un test que pasa es necesario, nunca
suficiente. Terminado significa que la superficie real — la que el humano usa de
verdad — hace el trabajo por sí sola. Nombra esa superficie, dispara la ruta
real y mira llegar el resultado correcto. Nunca asciendas un recibo de test
unitario a una afirmación de capacidad viva.

## Reglas duras (qué reprueba esta skill)

- Puntuar contra una paráfrasis en vez de la petición original.
- Un veredicto de revisar o rechazar sin fallos nombrados adjuntos.
- Reparar sin volver a correr la compuerta que falló.
- Mockear al validador mismo, o el seam exacto bajo cambio.
- Declarar terminado desde un test verde sin prueba en la superficie real.

## Lleva un registro del build

Por cada etapa guarda: la intención, el artefacto de entrada exacto, los
puntajes, los fallos nombrados, la reparación hecha, el resultado de la
recorrida y la evidencia de superficie real. Un registro que no apunta a
evidencia reproducible es una pancarta, no un registro.

## Combina bien con

- [intent-compiler](../intent-compiler/SKILL.md) — traduce la petición antes de puntuarla.
- [red-first](../red-first/SKILL.md) — el contrato de la compuerta de Test: test en rojo commiteado primero.
- [sniper-testing](../sniper-testing/SKILL.md) — efectos secundarios reales, sin teatro de mocks.
- [blind-tribunal](../blind-tribunal/SKILL.md) — evaluadores independientes encima de estas compuertas.
- [repair-loop](../repair-loop/SKILL.md) — el loop que lleva los veredictos de revisar hasta el verde.
