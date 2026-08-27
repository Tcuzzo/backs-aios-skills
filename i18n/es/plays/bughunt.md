# Jugada: Bughunt

Una cacería de bugs acotada y en paralelo. Traza la cacería como un mapa, despliega
buscadores sobre él, verifica cada hallazgo de forma adversarial y cierra costuras
completas — nunca síntomas sueltos.

## Cuándo ejecutarla

- Una auditoría, un barrido o una cacería sobre muchas costuras — no un solo bug
  reportado (para eso está el repair loop).
- Un backlog de hallazgos que hay que atacar en paralelo sin deriva y sin pisarse.

La cacería, de un vistazo:

```
    +--------------------------------------------+
+-->| 1 wayfinder  chart the hunt as one map,    |
|   |   a node per seam; claim from the frontier |
|   +--------------------------------------------+
|   | 2 leap-protocol  one node = one ball:      |
|   |   goal, spec, hard file scope, ONE writer  |
|   +--------------------------------------------+
|   | 3 root-cause-first  reproduce + review     |
|   |   evidence BEFORE any code changes         |
|   +--------------------------------------------+
|   | 4 repair-loop  red-first test committed,   |<--------------------------+
|   |   sniper-testing while iterating           |  finding or survivor ->   |
|   +--------------------------------------------+   +---------------------+ |
|   | 5 blind-tribunal  a non-author grader      |-->|  LORD OF THE LOOP   |-+
|   |   attacks; jurors judge redacted work      |   | one hand drives the |
|   +--------------------------------------------+   | loop: dispatch,     |
|   | 6 seam-engineering  close the CLASS at     |   | judge, loop back    |
|   |   the shared seam, never the symptom       |   | until the gate is   |
|   +--------------------------------------------+   | green. a lane never |
|   | 7 clean-code-gauntlet  the fixed branch    |-->| lands its own work. |
|   |   must DIE under mutation, or stay open    |   +---------------------+
|   +--------------------------------------------+
|             |
|             | jurors pass + mutant dies
|             v
|   +--------------------------------------------+
|   | LANDING GATE -- leap-protocol Score gate:  |
|   | source truth . keep-or-revert . blind      |
|   | review . live proof . provenance -- each   |
|   | finding ends FIXED or REFUTED-W-EVIDENCE   |
+---| ball closed -> claim the next node         |
    +--------------------------------------------+
```

En el diagrama: **Lord of the Loop** = el dueño del bucle, la mano que conduce la iteración — despacha, juzga y vuelve a iterar — hasta que la puerta de aterrizaje está en verde; **LAND / LANDING GATE** = aterrizar — integrar el cambio solo cuando todo está en verde.

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
4. [repair-loop](../skills/repair-loop/SKILL.md) — la disciplina interna de cada
   bola: [red-first](../skills/red-first/SKILL.md), el test que falla commiteado
   antes del arreglo; [sniper-testing](../skills/sniper-testing/SKILL.md), corridas
   acotadas durante la iteración; una pasada completa de los módulos tocados al
   aterrizar.
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
