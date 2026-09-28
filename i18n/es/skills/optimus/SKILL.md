---
name: "optimus"
description: "Úsala al arrancar cualquier sesión, trabajo o loop de agente — antes de escribir una sola línea de código. Arranque harness-primero: carga el piso de invariantes y las skills que el trabajo necesita, para que el agente lea las reglas antes de trabajar; incluye el patrón de hook de compuerta de anclaje que bloquea las herramientas mutantes hasta que el harness esté cargado. Trigger words: optimus, harness-boot, harness first, load the harness, boot the floor, grounding gate, read the floor, no code without harness, session start, boot sequence, harness primero, carga el harness, arranca el piso, compuerta de anclaje, lee el piso, sin harness no hay código, arranque de sesión."
license: "MIT"
---

# Harness Boot
**Effort:** light — una sola pasada de arranque por sesión para cargar el piso y las skills del trabajo, más un hook determinista que no cuesta nada correr. Elimina: ediciones sin fundamento — mutaciones hechas antes de leer las reglas, y el rehacer que viene después, una vez leídas.

Una regla: **ni código ni trabajo hasta que el harness esté cargado.** El harness
(el arnés: las reglas y herramientas que sujetan al agente) es el piso de
invariantes del pack más las skills que cubren este trabajo. Cada sesión, cada
runtime, cada vez. El porqué: una regla que el agente debe recordar falla justo
cuando el agente está más ocupado — así que cargar las reglas es el primer acto,
y un hook lo vuelve estructural en vez de consultivo.

## Cuándo correrla

Al inicio de cada sesión, trabajo, misión y loop. Otra vez después de un reinicio
de contexto o de un relevo. Cargar el harness una vez y vivir de eso una semana
no es cargar el harness.

## La secuencia de arranque

1. **Carga el piso de invariantes.** Lee [invariant-floor](../invariant-floor/SKILL.md)
   antes de tocar nada. Este es el piso sobre el que se para toda la sesión.
2. **Carga el mapa de este trabajo.** Nombra qué archivos, qué reglas y qué
   skills del pack gobiernan este trabajo concreto. Si no puedes nombrarlos, no
   estás listo para editar.
3. **Carga el perfil humano** ([human-calibration](../human-calibration/SKILL.md))
   cuando el trabajo toca el gusto, la superficie o el flujo de un humano.
4. **Invoca las skills que el trabajo necesita — en tiempo real, en esta sesión.**
   Una skill nombrada pero no invocada no ocurrió. Trabajar "de memoria de una
   skill" no es invocarla.
5. Solo entonces: escribe código, corre comandos mutantes o cambia cualquier cosa.

## El patrón de compuerta de anclaje (grounding gate)

Vuelve el paso 4 estructural con un **hook pre-herramienta** determinista — un
script pequeño que tu runtime de agente llama antes de cada uso de herramienta:

- Cada sesión arranca en **RED** (rojo).
- En RED, las herramientas de solo lectura (read, grep, search, fetch) siempre
  pasan. El agente se ancla con libertad.
- En RED, el hook **bloquea las herramientas mutantes** (edit, write, delete) y
  los verbos mutantes primarios de shell (commit, push, rm, install, reinicio de
  servicios, ediciones in-place).
- Invocar cualquier skill del harness **pone la sesión en GREEN** (verde; lo
  captura un hook post-herramienta). Entonces el agente puede actuar.
- **Rearme:** el estado vuelve a RED en cada arranque de sesión. En sesiones
  largas, rearma por trabajo o por acción, para que un GREEN viejo nunca se
  cuele en trabajo sin anclar.

Reglas de diseño para el hook mismo:

- **Determinista y gratis.** Sin llamada a modelo, sin red, sin dependencias. El
  estado es un archivo pequeño por sesión, escrito de forma atómica.
- **Fuerza el anclaje, no es un sandbox.** Empareja solo los verbos mutantes
  primarios; deja en paz los envoltorios de doble uso y las herramientas de
  copia, para que los comandos de anclaje no queden atrapados.
- **Falla abierto, pero en voz alta.** Un hook caído jamás debe romper la sesión
  — y jamás debe permitir en silencio. Imprime el error donde el humano lo vea.
- **Nunca atrapes una sesión.** Identidad de sesión desconocida: permite, con una
  línea de advertencia en voz alta. Una sesión que nunca puede pasar a GREEN
  jamás debe quedar bloqueada en RED.
- **Un solo interruptor de apagado en manos del humano** (una variable de
  entorno), encendido por defecto, que avisa en voz alta cuando está apagado. La
  compuerta ata a los agentes, nunca al humano. Nunca agregues una segunda
  compuerta.

Hook genérico (pseudocódigo, ~25 líneas):

```python
HARNESS_SKILLS = {"optimus", "repair-loop", "invariant-floor"}  # el set de tu pack
MUTATING_TOOLS = {"Edit", "Write", "Delete"}
MUTATING_SHELL = r"^\s*(sudo\s+)?(git (commit|push|reset|checkout)|rm|pip install|" \
                 r"npm install|systemctl (restart|stop)|sed .*-i)"

def handle(event, session_id, tool, args):
    if kill_switch_off():                    # env var del humano, p. ej. HARNESS_GATE=off
        return ALLOW                         # apagado en voz alta, nunca en silencio
    if not session_id:
        warn("sin id de sesión — se permite; la compuerta nunca atrapa una sesión")
        return ALLOW
    if event == "SessionStart":
        set_state(session_id, "RED")         # cada sesión rearma a RED
        return ALLOW
    if event == "PostToolUse":
        if tool == "Skill" and args.get("skill") in HARNESS_SKILLS:
            set_state(session_id, "GREEN")   # harness invocado -> el agente puede actuar
        return ALLOW
    if event == "PreToolUse":
        mutating = tool in MUTATING_TOOLS or (
            tool == "Bash" and matches(MUTATING_SHELL, args.get("command", "")))
        if not mutating or get_state(session_id) == "GREEN":
            return ALLOW                     # lo de solo lectura siempre pasa
        return BLOCK("RED: invoca una skill del harness primero, luego actúa")
    return ALLOW
```

## Reglas duras (qué reprueba esta skill)

- Cualquier mutación antes de cargar el harness.
- Una skill nombrada en un reporte que nunca fue invocada en la sesión.
- Un hook que bloquea herramientas de solo lectura, atrapa una sesión en RED o
  falla en silencio.
- Una segunda compuerta, o cualquier fricción nueva puesta sobre el humano. El
  interruptor de apagado sigue siendo suyo.

## Combina bien con

- [invariant-floor](../invariant-floor/SKILL.md) — el piso que el arranque carga primero.
- [human-calibration](../human-calibration/SKILL.md) — el paso de perfil del arranque.
- [repair-loop](../repair-loop/SKILL.md) — lo que un trabajo de fix corre después del arranque.
- [bounded-loops](../bounded-loops/SKILL.md) — presupuestos para cada loop que el arranque inicia.
- [wayfinder](../wayfinder/SKILL.md) — cuando el arranque muestra que no conoces la ruta.
