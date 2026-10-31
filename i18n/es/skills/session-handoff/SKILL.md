---
name: "session-handoff"
description: "Úsala al terminar una sesión, antes de compactar contexto, al agotar un cupo de misión o cuando trabajo pendiente deba continuar en otro agente o harness."
license: "MIT"
---

# Session Handoff
**Effort:** free — un solo archivo plano escrito antes de que el contexto muera; sin llamadas a modelos, y recorta el costo neto directamente al arrancar la siguiente sesión. Elimina: que el agente fresco re-derive el estado, que re-pague trampas ya pagadas, y decisiones perdidas en una ventana de contexto muerta.

Una ventana de contexto muere; el trabajo no debe morir con ella. Antes de que
una sesión termine o se compacte, escribe un archivo plano que un agente recién
llegado pueda leer en frío y continuar — qué se estaba haciendo, dónde vive, qué
está a medias y el próximo comando exacto. El traspaso debe sobrevivir al contexto.
Usa el registro existente de [BACKS Build Flow](../backs-build-flow/SKILL.md):
transfiere la tarea sin crear otro responsable, pasada de contexto ni misión.

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

Respeta `task_mode` y permisos de escritura de la tarea. Para revisión de solo
lectura o congelada, devuelve el traspaso en la respuesta o registro externo ya
autorizado; nunca escribas una bitácora en el repo protegido para cumplir esta skill.

## Verifica el trabajo concurrente primero (antes de escribir una palabra)

Comprueba que el trabajo de OTRAS sesiones está preservado. Corre `git status`,
`git log` y `git worktree list`. Anota con honestidad los archivos sucios y las
ramas sin fusionar. Nunca alteres el trabajo sin commitear de otra sesión para
que el relevo se vea limpio — ese es el defecto de pérdida de datos. Un relevo
que describe un estado limpio mientras otra sesión tiene trabajo en vuelo es una
afirmación falsa.

## Qué lleva — una sección corta por punto

1. **Meta.** Trabajo en una frase y definición de terminado. Conserva `mission_id`,
   `task_mode`, responsable de integración, resultado solicitado y acciones de
   entrega ya autorizadas.
2. **Estado.** Integrado (ids de commit), en construcción, en cola. Referencia
   specs, planes, issues y diffs por ruta o URL sin duplicarlos. Incluye `base_sha`
   fijado, `candidate_sha` actual, rutas/commit/hashes del RED sellado, comandos
   y resultados, y candidato exacto cubierto por cada recibo.
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
9. **Skills sugeridas.** Qué cargar primero y por qué. Nombra cuerpos/evidencia
   ya disponibles, qué actualizar y fuente de esencia del operador; no copies un
   segundo perfil.
10. **Presupuesto restante.** Conserva plazo original y total/consumido/restante
    de intentos, rondas y otros límites de [bounded-loops](../bounded-loops/SKILL.md),
    llamadas pendientes y última hipótesis/fallo. Lo desconocido sigue desconocido.
    Nunca reinicies presupuesto al traspasar, compactar, cambiar trabajador o modelo.

## Reglas duras

- **Censura.** Nada de claves de API, contraseñas, tokens ni datos personales.
  Nada de hostnames reales, IPs internas ni rutas de home — solo marcadores de
  posición; apunta a los valores reales por nombre de variable de entorno. El
  relevo es el archivo con más chances de salir de la máquina; un secreto que se
  fuga por él ES el bug.
- **Las afirmaciones de ausencia se pudren más rápido.** Antes de escribir "X no
  existe" o "X no aterrizó", vuelve a verificarlo en el commit actual — el
  trabajo paralelo aterriza mientras escribes.
- **Estado respaldado por evidencia por ítem.** La entrega de capacidades usa
  PROVEN solo con revisión requerida y prueba real de superficie; en otro caso,
  STILL-BUILDING nombra evidencia faltante. Una revisión o parche local terminado
  puede satisfacer el pedido sin presentarse como capacidad desplegada.
- **Que se lea en dos minutos** (unas 120 líneas). Cuando crezca más allá de
  eso, archiva los bloques más viejos moviéndolos a una sección de historia —
  nunca borrándolos.

## Retomar (la otra mitad)

Una sesión que arranca desde un relevo lo lee PRIMERO, y luego verifica las dos
o tres afirmaciones principales contra `git log` y el árbol vivo antes de actuar
sobre ellas. El relevo es un mapa, no la verdad — confíale el DÓNDE mirar;
verifica el QUÉ dice.

Retoma con el mismo paquete y cupos restantes. Revisa el plazo antes de despachar;
otra sesión no es otro presupuesto. Si un cupo se agotó, conserva STILL-BUILDING
y completa solo trabajo útil autorizado que no lo consuma. Mantén sello RED y
base fijada; actualiza identidad del candidato solo al cambiar los bytes reales.

## Combina bien con

- [root-cause-first](../root-cause-first/SKILL.md) — la investigación que la próxima sesión continúa.
- [repair-loop](../repair-loop/SKILL.md) — pasar el relevo a mitad del loop sin perder el seam.
- [decision-bar](../decision-bar/SKILL.md) — cómo llegan las decisiones abiertas a tu humano.

> Crédito de andamiaje: Matt Pocock, handoff (mattpocock/skills). La composición y las reglas duras de aquí son de BACKS AIOS.
