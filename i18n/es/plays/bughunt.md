# Jugada: Bughunt

Una cacería de bugs acotada y en paralelo. Traza la cacería como un mapa, despliega
buscadores sobre él, verifica cada hallazgo de forma adversarial y cierra costuras
completas — nunca síntomas sueltos.

## Cuándo ejecutarla

- Una auditoría, un barrido o una cacería sobre muchas costuras — no un solo bug
  reportado (para eso está el repair loop).
- Un backlog de hallazgos que hay que atacar en paralelo sin deriva y sin pisarse.

## Tarea y límites compartidos

Aplica este play dentro del paquete actual de
[BACKS Build Flow](../skills/backs-build-flow/SKILL.md). Mantén un responsable
de integración, `task_mode` solicitado, revisiones base y candidata fijadas,
esencia del operador y evidencia vigente. Reutiliza cuerpos pertinentes ya cargados;
este play añade puertas de su dominio sin reiniciar la tarea.

[bounded-loops](../skills/bounded-loops/SKILL.md) controla plazo original y cupos
restantes entre reintentos, trabajadores, modelos, revisiones y traspasos.
Nunca los reinicies para un play anidado. Al agotarlos, guarda **STILL-BUILDING**
con candidato, evidencia, puertas pendientes y siguiente acción. Continúa trabajo
útil autorizado solo dentro de su cupo restante; una puerta ausente no se vuelve aprobada.

## La cadena

1. [wayfinder](../skills/wayfinder/SKILL.md) — traza la cacería PRIMERO como un solo
   mapa, con un nodo por costura o hallazgo. Los buscadores reclaman nodos de forma
   atómica desde la frontera; cerrar un nodo escribe la pregunta del siguiente. No
   inventes nada fuera del mapa.
2. [leap-protocol](../skills/leap-protocol/SKILL.md) — cada nodo es una bola:
   objetivo, spec, alcance duro de archivos, rondas acotadas, resultado tri-estado.
   Las bolas relacionadas viajan en una sola tajada ordenada por dependencias, con
   exactamente UN escritor.
3. [root-cause-first](../skills/root-cause-first/SKILL.md) — reproduce el bug y
   revisa la evidencia de causa raíz ANTES de cualquier cambio de código. Ninguna
   mutación sobre una corazonada.
4. [repair-loop](../skills/repair-loop/SKILL.md) — disciplina interna de cada
   bola: [red-first](../skills/red-first/SKILL.md) confirmado fallando antes del
   arreglo; [sniper-testing](../skills/sniper-testing/SKILL.md) para comandos reales
   acotados de lint/tipos/tests desde el diff agregado fijado, y pasada completa de
   módulos tocados al integrar. Conserva RED original; cada hallazgo nuevo recibe
   test suplementario separado. Devuelve evidencia al responsable de cacería sin
   reiniciar un play.

5. [blind-tribunal](../skills/blind-tribunal/SKILL.md) — cada hallazgo se ataca de
   forma adversarial: un evaluador que no lo escribió ataca con rechazo por
   defecto, y los jurados juzgan un sobre con el autor tachado. El que construye
   nunca califica su propio trabajo.
6. [seam-engineering](../skills/seam-engineering/SKILL.md) — cierra la CLASE en la
   costura compartida, nunca el síntoma suelto.
7. [clean-code-gauntlet](../skills/clean-code-gauntlet/SKILL.md) — prueba de cierre:
   la rama arreglada debe MORIR bajo mutación. Un cierre cuyo mutante sobrevive no
   está probado, y el hallazgo sigue abierto.

## Una bola se cierra

Una bola se cierra solo a través de la puerta Score de
[leap-protocol](../skills/leap-protocol/SKILL.md) — verdad de la fuente,
conservar-o-revertir, revisión ciega, prueba en vivo, procedencia; la evidencia que
falta nunca cuenta como aprobada por defecto. Estados terminales propios de la
cacería: cada hallazgo termina ARREGLADO o REFUTADO-CON-EVIDENCIA.

Un cupo agotado deja el hallazgo abierto con checkpoint STILL-BUILDING; no es
un estado terminal ARREGLADO ni REFUTADO-CON-EVIDENCIA. Conserva historial de
intentos y límites restantes antes de reclamar otro nodo permitido.

## Reglas de la cacería

- Baja tu confianza. Vuelve a aterrizarte desde la bitácora y el historial de
  intentos del nodo, nunca desde tu propia memoria. Relanzar significa volver a
  reclamar desde la frontera; el traspaso va por
  [session-handoff](../skills/session-handoff/SKILL.md).
- Transmite el avance con voz humana mientras trabajas. Lo desconocido se queda
  desconocido — nunca se convierte en "aprobado".
- Una vez congelados los bytes candidatos, los comandos, los tests y el veredicto,
  aterrizar es una repetición determinista. Ninguna llamada a un modelo re-decide un
  comando ya decidido.
- Respeta la caja: mide los recursos antes de lanzar procesos, acota la
  concurrencia, recoge los carriles muertos, para EN VOZ ALTA tras una segunda
  muerte en el mismo nodo, y regula cada llamada externa. El kill-switch frena
  reclamos nuevos — nunca una mutación en pleno vuelo.
- Nombra el desperdicio de cada tajada y mide antes/después. Toma una ganancia de
  eficiencia solo cuando un comparador prueba cero pérdida de capacidad; el
  sobre-engorde también es un defecto.
- Reporta en dos palabras: PROVEN o STILL-BUILDING.

## Puertas duras — cualquiera hace fallar la jugada

- Una mutación hecha antes de revisar la evidencia reproducida de causa raíz.
- Un constructor calificando su propio hallazgo.
- Un hallazgo cerrado mientras un mutante sobrevive en la rama arreglada.
- Una corrida de la suite completa a mitad de cacería — francotirador solo sobre la
  costura del propio hallazgo.
- Teatro de mocks en un test de cierre: reabre el bug en silencio mientras la
  bitácora afirma que está cerrado.
- Un hallazgo estacionado en vez de arreglado o refutado con evidencia.

**Weight:** disciplina de cacería free en el núcleo; el gasto heavy es triple — el reparto leap, el tribunal adversarial y la prueba de cierre por mutación — se paga cuando un backlog entero se cierra en paralelo con cada cierre probado bajo mutación.
