# Jugada: Parallel Work

Cómo repartir trabajo entre agentes sin que se pisen entre ellos. La regla que paga
todo lo demás: una sola espina de escritura, muchos lectores.

## Cuándo ejecutarla

- Una tarea se parte en investigación, escaneo, testing o calificación que pueden
  correr a la vez.
- Más de un agente va a tocar el mismo repositorio en la misma ventana.
- Te tienta dejar que dos agentes escriban código en paralelo. Lee esto primero.

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

1. [leap-protocol](../skills/leap-protocol/SKILL.md) — divide el trabajo en bolas
   con objetivos, specs y alcance estricto de archivos ANTES de lanzar agentes.
   Entrega a cada carril paquete vigente, base/candidato fijados, sellos RED y cupo
   restante asignado. Su límite no puede ampliar plazo ni totales de la misión.

2. Lanza lectores, no escritores — despliega subagentes SOLO para trabajo de mucha
   lectura con pocas dependencias cruzadas: investigación, correr tests, escaneos de
   seguridad, calificación. Nunca para autoría de código interdependiente.
3. Aísla cada carril — cada agente paralelo recibe su PROPIO worktree (un checkout
   separado del mismo repo). Los conflictos entonces afloran en el merge como
   conflictos de merge reales, nunca como sobrescrituras silenciosas que pierden
   datos sin aviso.
4. [clean-code-gauntlet](../skills/clean-code-gauntlet/SKILL.md) — cada carril
   ejecuta su gauntlet en el aislamiento/worktree permitido antes de integrar.
   Usa primero [sniper-testing](../skills/sniper-testing/SKILL.md) para comandos
   reales de lint/tipos/tests del diff agregado fijado; declara ausencias o N/A.
   Reutiliza recibos válidos solo del mismo candidato y alcance; no apliques el
   verde de otro carril a bytes distintos. Cobertura faltante recibe archivo
   suplementario separado, conservando originales sellados.

5. [blind-tribunal](../skills/blind-tribunal/SKILL.md) — el agente revisor recibe un
   contexto LIMPIO, nunca el del autor. El contexto compartido se pudre y se da la
   razón a sí mismo.
6. Fusiona un carril por vez en un workspace dedicado, con puerta de tests
   por código de salida. El responsable de integración verifica candidato combinado,
   consumidores y pasada completa requerida de suites afectadas; pases independientes
   no prueban la composición. Afirmar entrega exige evidencia del destino real.

## Reglas de coordinación

- UN agente escribe código por espacio de trabajo, en un solo contexto coherente.
  Los escritores paralelos toman decisiones implícitas en conflicto que ningún merge
  puede reconciliar.
- Declara por adelantado la propiedad de archivos de cada agente. Cada agente edita
  SOLO sus archivos nombrados.
- Coordina a través de un tracker (issues, tickets) — nunca con un archivo de
  checklist compartido en el árbol de trabajo. Ese archivo es en sí mismo una
  superficie de conflictos de merge, y hace que dos agentes agarren la misma tarea.
- Cada subagente devuelve un resumen destilado — hechos clave, decisiones, temas
  abiertos, una página o dos — nunca su transcripción completa.
- Persiste el plan, la spec y las decisiones a disco y vuélvelas a leer. Las
  corridas largas compactan el contexto y sueltan instrucciones en silencio; las
  reglas que deben aplicar siempre viven en el archivo siempre-cargado, en ningún
  otro lado.

## Disciplina de merge

- Ponle puerta de tests a CADA merge por código de salida antes de aterrizar. Una
  suite roja bloquea el merge. Esto solo ya recorta la mayor parte de las roturas
  causadas por agentes.
- Mergea en un espacio de merge dedicado y luego verifica el resultado con stat:
  conteo de archivos, diffstat, los archivos nombrados de cada carril presentes. Un
  merge que suelta en silencio los archivos de un carril es el mal merge cardinal —
  chequéalo cada vez.

## Puertas duras — cualquiera hace fallar la jugada

- Dos agentes escribiendo código en el mismo espacio de trabajo a la vez.
- Un carril editando fuera de su alcance de archivos declarado.
- Un merge aterrizado sin código de salida verde, o sin la verificación por stat.
- Un revisor que compartió contexto con el autor.
- Un carril aterrizando sobre los resultados de tests de otro carril, o mockeando la
  costura que cambió.

**Weight:** heavy por diseño — descomposición leap, un gauntlet por carril y un tribunal de contexto limpio — el gasto se paga solo cuando el trabajo es lo bastante grande para partirlo, que es el único momento en que corre esta jugada.
