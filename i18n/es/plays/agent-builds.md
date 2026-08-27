# Agent Builds

Cómo construir un agente o servicio que actúa por su cuenta. La idea central: las
primitivas deterministas hacen el trabajo pesado; el modelo razona solo donde razonar
es lo único que funciona. Un diseño que es puro LLM, con cero primitivas, es inválido.

## Cuándo ejecutarla

Al construir cualquier agente, bot, worker o servicio de larga duración — cualquier
cosa que tenga herramientas, llame a la red o actúe sin un humano mirando cada paso.

La construcción, de un vistazo:

```
    +--------------------------------------------+
    | 1 intent-compiler  mission + limits from   |
    |   the human's own words                    |
    +--------------------------------------------+
+-->| 2 understanding-gates  DOMAIN PRIMITIVES   |
|   |   first; LLM slot for genuine reasoning    |
|   +--------------------------------------------+
|   | 3 red-first  a failing contract test per   |<--------------------------+
|   |   typed IO boundary, committed first       |  finding -> a new red     |
|   +--------------------------------------------+  test -> fix ->           |
|   | 4 build to the doctrine -- every loop      |  re-convene               |
|   |   inside bounded-loops                     |   +---------------------+ |
|   +--------------------------------------------+   |  LORD OF THE LOOP   |-+
|   | 5 sniper-testing  mock transport only      |   | one hand drives the |
|   +--------------------------------------------+   | loop: dispatch,     |
|   | 6 clean-code-gauntlet  mutate decision     |   | judge, loop back    |
|   |   paths to zero survivors                  |   | until the gate is   |
|   +--------------------------------------------+   | green. a lane never |
|   | 7 blind-tribunal  cross-family graders     |-->| lands its own work. |
|   +--------------------------------------------+   +---------------------+
|             |
|             | every juror passes
|             v
|   +--------------------------------------------+
|   | LANDING GATE -- all green or no ship:      |
|   | no fail-open boundary, silent fallback,    |
|   | or swallowed error . zero mutation         |
|   | survivors in decision paths . cross-       |
|   | family pass; the builder never grades .    |
+---| zero primitives = invalid -> redesign      |
    +--------------------------------------------+
```

En el diagrama: **Lord of the Loop** = el dueño del bucle, la mano que conduce la iteración — despacha, juzga y vuelve a iterar — hasta que la puerta de aterrizaje está en verde; **LAND / LANDING GATE** = aterrizar — integrar el cambio solo cuando todo está en verde.

## La cadena

1. [intent-compiler](../skills/intent-compiler/SKILL.md) — lee el pedido completo;
   la misión y sus límites salen de las palabras del propio humano.
2. [understanding-gates](../skills/understanding-gates/SKILL.md) — en la etapa de
   diseño, nombra primero las PRIMITIVAS DE DOMINIO: cada capacidad central es una
   función determinista, offline y que falla cerrada. Reserva el hueco del LLM solo
   para razonamiento genuino.
3. [red-first](../skills/red-first/SKILL.md) — haz commit de tests de contrato que
   fallen para cada frontera de IO tipada, antes de construirla.
4. Construye según la doctrina de abajo. Mantén cada bucle dentro de
   [bounded-loops](../skills/bounded-loops/SKILL.md): presupuestos, checkpoints,
   backoff y un kill-switch ruidoso — nunca un reintento que martilla.
5. [sniper-testing](../skills/sniper-testing/SKILL.md) — solo el transporte de salida
   se puede mockear — nunca el enrutado, el armado del prompt ni el parseo.
6. [clean-code-gauntlet](../skills/clean-code-gauntlet/SKILL.md) — los manejadores de
   herramientas y las funciones de decisión del agente pasan el gauntlet: puntaje de
   riesgo por debajo de tu techo, y luego mutación sobre las rutas de decisión hasta
   cero sobrevivientes. Una lógica de ramas que sobrevive a una comparación invertida
   nunca estuvo probada de verdad.
7. [blind-tribunal](../skills/blind-tribunal/SKILL.md) — evaluadores de otra
   familia de modelos aprueban el agente antes de la entrega. El que construye nunca
   califica su propio trabajo.

## La doctrina (lo que la construcción debe cumplir)

- Cada frontera de IO declara un contrato tipado (entradas → salidas) y FALLA
  CERRADA — lanza un error o deniega ante una entrada mala. Nunca falla abierta,
  nunca se traga un error.
- Cada costura de red se puede probar con casetes: envuelve las llamadas salientes
  tras una costura de grabar/reproducir, para que la suite corra offline contra
  fixtures.
- Todo el egreso pasa por una allowlist explícita de hostnames que deniega por
  defecto. Un host desconocido lanza un error; nunca conecta en silencio.
- Modela el agente como un flujo de eventos tipado / máquina de estados con estados
  de visto-bueno deterministas (draft → review → ready → done) que el agente calcula
  por sí mismo — una primitiva, no fricción humana. Ninguna acción puede saltarse su
  estado.
- Confirma SOLO las acciones genuinamente destructivas o irreversibles (gastar,
  borrar, un envío externo que no se puede deshacer) contra el estado ya commiteado,
  antes de disparar. Nunca le pongas puerta a una acción benigna o de solo lectura,
  y nunca al humano — mira [decision-bar](../skills/decision-bar/SKILL.md).
- Persiste el estado durable (objetivos, decisiones, bitácora) en disco, FUERA de la
  ventana de contexto, y vuélvelo a leer. Nunca confíes en la memoria en-contexto a
  lo largo de una corrida larga.
- Incluye un documento operativo que el agente carga antes de cada tarea — gana el
  archivo más cercano, con tope de tamaño — con las reglas que siempre deben aplicar.
- Los fallos de herramientas devuelven un error estructurado al hueco de
  razonamiento, para auto-corrección. Un error de herramienta tragado es un bug.
- Privilegio mínimo: el agente lleva exactamente las herramientas que su misión
  necesita — nada de autoridad ambiental sobre el sistema de archivos o la red.

## Puertas duras

- Cero primitivas = diseño inválido; vuelve al paso 2.
- Cualquier frontera que falla abierta, fallback silencioso o error tragado bloquea
  la entrega.
- Mutantes sobrevivientes en las rutas de decisión bloquean la entrega.
- La calificación entre familias debe pasar; el que construye nunca es el que
  califica.

## Combina bien con

- [root-cause-first](../skills/root-cause-first/SKILL.md) — cuando el agente se porta mal
- [session-handoff](../skills/session-handoff/SKILL.md) — el estado durable bien hecho

**Weight:** mayormente disciplina free más una puerta de diseño light; el gasto heavy son las corridas de mutación del gauntlet y el tribunal cross-family — se paga en cualquier agente que va a actuar sin nadie mirando.
