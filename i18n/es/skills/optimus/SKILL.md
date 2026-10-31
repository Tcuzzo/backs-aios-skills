---
name: "optimus"
description: "Úsala al iniciar o retomar una sesión, trabajo o ciclo autónomo que necesite el harness BACKS y las skills pertinentes."
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

Al iniciar una sesión o trabajo nuevo; revalida después de un reinicio de contexto
o traspaso. Un reintento interno reutiliza el anclaje vigente y el mismo paquete
de tarea. Recarga cuerpos ausentes o cambiados; no reinicies el ciclo de vida en
cada iteración.

## La secuencia de arranque

1. **Carga el piso de invariantes.** Lee [invariant-floor](../invariant-floor/SKILL.md)
   antes de tocar nada. Es el piso de toda la sesión.
2. **Aplica [Build Flow](../backs-build-flow/SKILL.md).** Controla modo de tarea,
   preparación para actuar, selección de skills, RED/GREEN acotado con lint y
   tests focalizados, evidencia del gauntlet y entrega. Reutiliza un paquete
   verificado; recoge solo hechos faltantes para la siguiente acción concreta.
   Los especialistas regresan a un único responsable.
3. **Aplica contexto humano** ([human-calibration](../human-calibration/SKILL.md))
   cuando corresponda. [operator-essence](../operator-essence/SKILL.md) controla
   el archivo de conocimiento respaldado y la pasada de insights cuando falta;
   no ejecutes un segundo ciclo de perfil.
4. **Carga la sesión.** El hook entrega los cuerpos reales de Optimus, Yoke y
   Build Flow, más el harness nativo probado cuando exista. La compactación los
   recarga sin revocar el anclaje adquirido. Un marcador ausente ante una
   herramienta mutante dispara la carga, nunca el rechazo de la herramienta.
   Los hosts sin hook de contexto pueden usar:
   ```bash
   node "$HOME/.local/share/backs-aios/current/hooks/aios_gate.js" --load backs-aios:optimus
   ```
   En un shell Codex, pasa el `CODEX_SESSION_ID` activo como argumento final.
   La variante Python está en `aios_gate.py`. Skills desconocidas devuelven
   código distinto de cero sin inventar recibos.
5. **Aplica las skills que necesita la siguiente acción.** Nombra propósito,
   resultado y condición de salida. Una skill nombrada pero no invocada no ocurrió.
   Reutiliza cuerpos reales todavía presentes en el contexto; un resumen de
   memoria o hash de archivo no los reemplaza.
6. Solo entonces escribe código, ejecuta comandos mutantes o cambia algo.

## Anclaje automático

El hook existente lee los archivos fundamentales y entrega sus cuerpos por el
contexto del host. Registra hashes de fuente solo después de la entrega. Los
recibos de carga de contexto son distintos de evidencia real de eventos Skill;
cargar un puntero o calcular un hash no invoca esa skill.

- Inicio de sesión y compactación recargan el piso sin quitar herramientas.
- Un marcador de sesión ausente dispara carga automática en la siguiente herramienta coincidente.
- Cuerpos ausentes o ilegibles producen un diagnóstico visible y ningún recibo
  falso; el operador y los agentes conservan sus herramientas.
- `--rearm <session_id>` solicita otra carga. Nunca bloquea la sesión.
- `AIOS_GATE=off` sigue siendo el interruptor reversible existente del operador.
- Los hooks son locales y deterministas. No se añade llamada a modelo ni dependencia de red.

## Reglas duras (qué reprueba esta skill)

- Cualquier mutación antes de cargar el harness.
- Una skill nombrada en un reporte que nunca fue invocada en la sesión.
- Anclarse en memoria de sesión, conocimientos previos del LLM o «lo recuerdo» en
  vez del harness BACKS. BACKS es independiente de modelo y contexto y tiene
  canales robustos de memoria: el harness (archivos de memoria, plays, registros,
  YAML de escalera) conserva el conocimiento, no la cabeza del modelo
  (decisión del operador 2026-09-26).
- Un hook que rechace herramientas, revoque anclaje adquirido o informe cargas inexistentes.
- Una segunda puerta o fricción nueva para el humano. El interruptor sigue siendo suyo.

## Combina bien con

- [invariant-floor](../invariant-floor/SKILL.md) — el piso que se carga primero.
- [human-calibration](../human-calibration/SKILL.md) — contexto humano del arranque.
- [repair-loop](../repair-loop/SKILL.md) — reparación después del arranque.
- [bounded-loops](../bounded-loops/SKILL.md) — presupuestos para cada ciclo.
- [wayfinder](../wayfinder/SKILL.md) — cuando falta conocer la ruta.

## Política de peldaños de la flota (referencia breve)

Antes de despachar modelos o elevar diseño/razonamiento a frontera, invoca
[fleet-ladder](../fleet-ladder/SKILL.md). Exige **leer**
`config/fleet_ladder.yaml` y `config/gpu_nodes.yaml` (rutas del despliegue),
respetar el puesto constructor activo y exigir investigación actual (web, GitHub,
Reddit y papers) cuando el peldaño marque frontera / `research_seams`.
No fijes IDs de modelos; Patch controla el YAML.
Referencia: `observe/SECURITY_OPERATOR_BUILDER_SEAT_ORDER_20260926.md`.

Respeta [fleet-ladder](../fleet-ladder/SKILL.md): razonamiento de nivel medio o
superior cuando esté soportado, investigación antes de tareas pesadas y contexto
sin truncar.
