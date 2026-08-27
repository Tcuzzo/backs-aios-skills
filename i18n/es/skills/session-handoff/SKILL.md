---
name: session-handoff
description: Úsala cuando una sesión está terminando, la ventana de contexto está por compactarse, o el trabajo debe continuar en otro agente u otro harness. Compacta la sesión en un archivo plano que un agente recién llegado puede leer en frío y continuar — estado, trabajo a medias, el próximo comando exacto, decisiones abiertas — con secretos censurados y el trabajo concurrente verificado como preservado. Trigger words: handoff, hand off, compact, save state, continue in another session, portable handoff, before restart, relevo, traspaso, compactar, guardar estado, continuar en otra sesión, relevo portátil, antes de reiniciar.
license: MIT
---

# Session Handoff

Una ventana de contexto muere; el trabajo no debe morir con ella. Antes de que
una sesión termine o se compacte, escribe un archivo plano que un agente recién
llegado pueda leer en frío y continuar — qué se estaba haciendo, dónde vive, qué
está a medias y el próximo comando exacto. Un relevo (handoff) estacionado solo
en la prosa del chat o en la memoria no existe.

## Cuándo escribir uno

- Antes de que la ventana de contexto se compacte o se limpie.
- Al terminar una sesión con trabajo todavía abierto.
- Justo después de aterrizar algo grande (registra el id del commit mientras
  está fresco).
- En el momento en que una decisión real sube a tu humano (registra qué significa
  cada opción).

## Dónde va

Un lugar conocido donde el próximo agente mirará PRIMERO. Si el próximo agente
comparte tu proyecto, usa un archivo de bitácora estable en el repo y commitea la
actualización, para que sobreviva un reinicio de máquina y no solo una limpieza
de contexto. Si el próximo agente es otro harness o un login fresco, escribe un
archivo plano portátil en el directorio temporal — es andamiaje, no un artefacto
rastreado.

## Verifica el trabajo concurrente primero (antes de escribir una palabra)

Comprueba que el trabajo de OTRAS sesiones está preservado. Corre `git status`,
`git log` y `git worktree list`. Anota con honestidad los archivos sucios y las
ramas sin fusionar. Nunca alteres el trabajo sin commitear de otra sesión para
que el relevo se vea limpio — ese es el defecto de pérdida de datos. Un relevo
que describe un estado limpio mientras otra sesión tiene trabajo en vuelo es una
afirmación falsa.

## Qué lleva — una sección corta por punto

1. **Meta.** El trabajo en una frase. El próximo agente no debe adivinar qué
   significa "terminado".
2. **Estado.** Aterrizado (ids de commit), en construcción, en cola. Referencia
   specs, planes, issues y diffs por ruta o URL — nunca dupliques su contenido.
3. **Dónde vive el trabajo.** Ramas, worktrees, archivos sucios. Nombra los
   archivos exactos que el próximo agente debe leer primero.
4. **El rastro de veredictos.** Quién o qué calificó cada pieza y cuáles fueron
   los hallazgos reales. Un veredicto reprobado con defectos nombrados vale MÁS
   que un verde — escribe los defectos textuales.
5. **Trabajo a medias y el próximo comando exacto.** Qué está en pleno vuelo, y
   el comando literal que lo continúa.
6. **Decisiones abiertas.** Todo lo que espera a tu humano, y qué significa cada
   opción. Una decisión jamás debe existir solo en una ventana de contexto muerta.
7. **Contratos sin cumplir.** Tests todavía en rojo, pruebas todavía faltantes,
   promesas hechas y aún no cumplidas.
8. **Trampas.** Una línea cada una. Una trampa que ya pagaste vale más que un
   verde — escríbela para que la próxima sesión no la pague otra vez.
9. **Skills sugeridas.** Qué skills debería cargar primero el próximo agente, y
   una línea del porqué. Esto es lo que hace al doc portátil entre harnesses.

## Reglas duras

- **Censura.** Nada de claves de API, contraseñas, tokens ni datos personales.
  Nada de hostnames reales, IPs internas ni rutas de home — solo marcadores de
  posición; apunta a los valores reales por nombre de variable de entorno. El
  relevo es el archivo con más chances de salir de la máquina; un secreto que se
  fuga por él ES el bug.
- **Las afirmaciones de ausencia se pudren más rápido.** Antes de escribir "X no
  existe" o "X no aterrizó", vuelve a verificarlo en el commit actual — el
  trabajo paralelo aterriza mientras escribes.
- **Estado de dos palabras por ítem: PROVEN o STILL-BUILDING.** Tests verdes sin
  prueba viva es STILL-BUILDING, y el relevo dice exactamente qué prueba falta.
- **Que se lea en dos minutos** (unas 120 líneas). Cuando crezca más allá de
  eso, archiva los bloques más viejos moviéndolos a una sección de historia —
  nunca borrándolos.

## Retomar (la otra mitad)

Una sesión que arranca desde un relevo lo lee PRIMERO, y luego verifica las dos
o tres afirmaciones principales contra `git log` y el árbol vivo antes de actuar
sobre ellas. El relevo es un mapa, no la verdad — confíale el DÓNDE mirar;
verifica el QUÉ dice.

## Combina bien con

- [root-cause-first](../root-cause-first/SKILL.md) — la investigación que la próxima sesión continúa.
- [repair-loop](../repair-loop/SKILL.md) — pasar el relevo a mitad del loop sin perder el seam.
- [decision-bar](../decision-bar/SKILL.md) — cómo llegan las decisiones abiertas a tu humano.

> Crédito de andamiaje: Matt Pocock, handoff (mattpocock/skills). La composición y las reglas duras de aquí son de BACKS AIOS.
