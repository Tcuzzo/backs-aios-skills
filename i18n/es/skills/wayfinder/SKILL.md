---
name: "wayfinder"
description: "Úsala cuando estás perdido, el camino adelante no está claro, o debes decidir en qué trabajar después. Traza un mapa de decisiones hacia el destino en vez de estacionar una pregunta sobre el humano. Trigger words: wayfinder, the path, chart the route, map the work, what next, lost, fog of war, decision map, frontier, el camino, traza la ruta, mapea el trabajo, qué sigue, perdido, niebla de guerra, mapa de decisiones, frontera."
license: "MIT"
---

# Wayfinder
**Effort:** free — pura disciplina de trazado: un mapa de decisiones construido con evidencia que ya está en disco, sin llamadas extra a modelos. Elimina: preguntas estacionadas en el humano que la evidencia podía responder, y trabajo de build arrancado antes de tomar las decisiones que van delante de él.

Cuando no conoces el camino, la salida barata es parar y hacerle al humano una
pregunta que te contrató para responder. El wayfinder traza la ruta en su lugar:
arma un mapa de decisiones, resuelve incógnitas con evidencia, y sube solo las
llamadas que son genuinamente del humano.

## Cuándo correrla

- Estás perdido, o el próximo paso no está claro.
- Un esfuerzo grande necesita descomponerse antes de que alguien construya.
- Sientes el tirón de preguntar "¿qué quieres que haga?".

## Los pasos

1. **Nombra el destino.** Una meta con nombre en tu tracker, más un predicado de
   cierre: cómo sabrás que está terminado. El destino fija el alcance.
2. **Traza lo que puedes ver.** Crea tickets en la frontera — las decisiones
   listas para resolverse ahora. Cada ticket resuelve una **decisión**, no una
   tajada de trabajo de construcción.
3. **Deja el resto en la niebla.** Las decisiones que puedes sentir venir pero
   aún no puedes precisar van a una sección de **Aún sin especificar**: la
   pregunta sospechada, el área a revisitar. No rebanes la niebla por adelantado
   en piezas tamaño ticket — es más gruesa que un ticket, y un parche puede
   graduarse en varios tickets, o en ninguno.
4. **Descarta trabajo en voz alta.** El trabajo más allá del destino no es
   niebla — va a una sección de **Fuera de alcance** y nunca se gradúa. Si un
   ticket vivo resulta estar más allá del destino, ciérralo y deja una línea en
   Fuera de alcance.
5. **Tipa cada ticket** (ver Tipos de ticket abajo).
6. **Resuelve una decisión con evidencia.** Lee el código, los docs, el registro
   — la evidencia determinista cierra un ticket sin adivinar. Resolver un ticket
   despeja la niebla que tenía delante: gradúa lo que ahora sí se puede
   especificar en tickets frescos, de a uno.
7. **Pasa la mano cuando el camino esté claro.** El mapa está terminado cuando
   no queda nada por decidir antes de que alguien vaya y haga la cosa. El tirón
   de simplemente hacer el trabajo es la señal de que llegaste al borde del mapa.

## ¿Niebla o ticket?

La prueba es si puedes enunciar la pregunta **con precisión** ahora — no si
puedes responderla ahora. Ticket cuando la pregunta está afilada, aunque esté
bloqueada. Aún-sin-especificar cuando todavía no puedes formularla así de filosa.

## Tipos de ticket

Cada ticket es **humano-en-el-loop** (se trabaja en vivo con un humano) o
**agente-solo**. Un ticket humano-en-el-loop solo se resuelve mediante
intercambio en vivo — el agente nunca suple el lado del humano. Un agente que
responde sus propias preguntas de parrilla ya rompió esto.

- **Investigación** (agente-solo) — un agente de investigación de fondo lo
  resuelve; los hallazgos aterrizan en una rama de borrador con un puntero desde
  el ticket. Ver [live-research](../live-research/SKILL.md).
- **Prototipo** (humano-en-el-loop) — sube la fidelidad con un artefacto burdo y
  barato al que el humano pueda reaccionar.
- **Parrilla** (humano-en-el-loop) — conversación que saca la decisión afuera.
  El tipo por defecto.
- **Tarea** (cualquiera de los dos) — trabajo manual que debe pasar antes de que
  una decisión pueda tomarse: registrarse en un servicio, aprovisionar acceso,
  mover datos. El único tipo que *hace* en vez de decidir; se gana su lugar
  desbloqueando una decisión.

## Reglas duras

- **Nunca estaciones sobre el humano una pregunta** que la evidencia, el código
  o las reglas vigentes pueden responder. Solo suben las llamadas de gusto,
  visión y riesgo destructivo — ver [decision-bar](../decision-bar/SKILL.md).
- **Refiérete al trabajo por nombre, nunca por un id pelado.** Una pared de #42,
  #43, #44 es ilegible; los nombres se leen de un vistazo. El id o el enlace
  viaja dentro del nombre — nunca lo reemplaza.
- **Una decisión por sesión.** Resuelve como máximo un ticket por sesión, salvo
  los tickets de investigación. Trazar el mapa es el trabajo de una sesión; no
  resuelve nada a mano.
- **Planea, no hagas.** El mapa produce decisiones, no entregables.
- **Cuando la petición misma es la niebla** — el destino no está claro porque la
  petición llegó como prosa o metáfora — primero lee la petición con
  [intent-compiler](../intent-compiler/SKILL.md), y luego traza desde lo que de
  verdad dice.

## Combina bien con

- [live-research](../live-research/SKILL.md) — resuelve los tickets de investigación agente-solo.
- [decision-bar](../decision-bar/SKILL.md) — qué decisiones llegan de verdad al humano.
- [human-voice](../human-voice/SKILL.md) — cómo se lee el mapa para un humano.

> Crédito de andamiaje: Matt Pocock, wayfinder (mattpocock/skills, MIT). La composición y las reglas duras de aquí son de BACKS AIOS.
