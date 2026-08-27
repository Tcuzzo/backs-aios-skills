# Elite Build — la jugada maestra

La jugada por defecto para cualquier pedido de "construye X", "arregla X" o "mejora
X". El humano dice la meta una vez; esta jugada arma el entorno completo para que
nunca tenga que re-explicar la base. Lee la intención, carga al humano, ponle
puertas al plan, pruébalo en rojo, construye, testea acotado, mide, califica a
ciegas, aterriza.

## Cuándo ejecutarla

Cualquier construcción, arreglo o mejora con algo real en juego. Una edición trivial
de una línea puede saltar directo a
[sniper-testing](../skills/sniper-testing/SKILL.md) y aterrizar.

## La cadena

0. [optimus](../skills/optimus/SKILL.md) — arranca el harness antes de que nada
   edite. El piso se carga primero, cada sesión, cada vez.
1. [intent-compiler](../skills/intent-compiler/SKILL.md) — lee el pedido como la
   spec, completo. Deduce la intención antes de subir cualquier decisión de entrega
   u opciones. Nunca presentes un menú de opciones cuando existe una solución clara
   — resuélvela.
2. [human-calibration](../skills/human-calibration/SKILL.md) — carga el perfil
   validado del humano y aplícalo. Nunca re-interrogues a un humano que ya conoces.
3. [understanding-gates](../skills/understanding-gates/SKILL.md) — Diseño → Plan →
   Construcción → Test → Entrega, cada etapa con su puerta. Antes de cualquier
   diseño: lee lo que existe vía [live-research](../skills/live-research/SKILL.md),
   reutiliza lo que ya está escrito, mapea la topología completa. La respuesta casi
   siempre ya está escrita.
4. [wayfinder](../skills/wayfinder/SKILL.md) — cuando te pierdas en cualquier paso,
   traza la ruta desde la evidencia. Nunca estaciones sobre el humano una pregunta
   que la evidencia puede responder.
5. [red-first](../skills/red-first/SKILL.md) — escribe el test de contrato que falla
   y haz commit ANTES de que corra cualquier constructor. El constructor no puede
   tocar ese test.
6. Construye. Despliega carriles paralelos por defecto — nunca serialices lo que
   puede correr a la vez. Cada carril recibe su propia rama de trabajo o worktree.
   ¿Solo, con una sesión? Un carril ES el despliegue — construye en una rama de
   trabajo y sigue. (Un worktree es un segundo checkout del mismo repo en otra
   carpeta, para que dos constructores nunca toquen los mismos archivos.) Resuelve
   los constructores por [fleet-ladder](../skills/fleet-ladder/SKILL.md); combina
   borradores con [model-fusion](../skills/model-fusion/SKILL.md). Para un bug,
   corre el [repair-loop](../skills/repair-loop/SKILL.md) y cierra la CLASE en la
   costura compartida según [seam-engineering](../skills/seam-engineering/SKILL.md).
7. [sniper-testing](../skills/sniper-testing/SKILL.md) — solo corridas acotadas
   mientras iteras; la única pasada completa de los módulos tocados espera al
   aterrizaje (paso 10).
8. [clean-code-gauntlet](../skills/clean-code-gauntlet/SKILL.md) — mide antes de
   aterrizar: suite francotiradora, puntaje de riesgo complejidad-por-cobertura
   debajo de tu techo, luego testing de mutación hasta cero sobrevivientes. Mide el
   código; nunca lo evalúes a ojo.
9. [blind-eval](../skills/blind-eval/SKILL.md), luego
   [blind-tribunal](../skills/blind-tribunal/SKILL.md) — un sobre con el autor
   tachado va a evaluadores de una familia de modelos distinta a la del
   constructor. El constructor nunca califica su propio trabajo. Cada hallazgo de un
   jurado se vuelve un nuevo test rojo; vuelve a convocar hasta que todos los
   jurados aprueben. ¿Equipo de una sola máquina? Degrada según la regla "Solo rig"
   de blind-tribunal — y nombra la puerta debilitada en el reporte de aterrizaje.
10. Aterriza — mergea limpio, corre UNA pasada completa sobre las suites de los
    módulos tocados, reinicia el servicio real y prueba el comportamiento en la
    superficie propia del humano (la página que carga, el comando que corre) —
    nunca una sonda proxy. Después reporta.

## Puertas duras (con una sola en rojo, el aterrizaje se bloquea)

- El test que falla fue commiteado antes de la construcción y está intacto — el
  evaluador verifica que el diff del archivo de test esté vacío.
- El constructor nunca es el evaluador, y el evaluador es de otra familia de
  modelos.
- Cada hallazgo sacado a la luz queda cerrado, o adjudicado como "no es un bug" con
  evidencia registrada. Nunca aplazado en silencio. Cierre de costura completa — la
  costura es el punto compartido del código donde vive esta clase de bug — o no hay
  aterrizaje.
- Prueba en vivo en la superficie real del humano. Tests verdes con la capacidad
  rota es fracaso, no éxito.
- Reporta en dos palabras — PROVEN o STILL-BUILDING — en
  [human-voice](../skills/human-voice/SKILL.md). Proven significa aterrizado, más
  calificado de forma independiente, más demostrado en vivo.
- Haz commit solo de los archivos propios de este cambio — nunca del trabajo en
  vuelo de otra sesión.

## Combina bien con

- [optimus](../skills/optimus/SKILL.md) — re-arranca el piso tras una compactación o un reinicio
- [invariant-floor](../skills/invariant-floor/SKILL.md) — el piso fijado que todo aterrizaje debe cumplir
- [decision-bar](../skills/decision-bar/SKILL.md) — qué llega al humano y qué se ejecuta
- [bounded-loops](../skills/bounded-loops/SKILL.md) — presupuestos y kill-switches en corridas largas
- [session-handoff](../skills/session-handoff/SKILL.md) — sella el estado antes de parar
