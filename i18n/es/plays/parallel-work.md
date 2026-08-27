# Jugada: Parallel Work

Cómo repartir trabajo entre agentes sin que se pisen entre ellos. La regla que paga
todo lo demás: una sola espina de escritura, muchos lectores.

## Cuándo ejecutarla

- Una tarea se parte en investigación, escaneo, testing o calificación que pueden
  correr a la vez.
- Más de un agente va a tocar el mismo repositorio en la misma ventana.
- Te tienta dejar que dos agentes escriban código en paralelo. Lee esto primero.

## La cadena

1. [leap-protocol](../skills/leap-protocol/SKILL.md) — descompone el trabajo en
   bolas con objetivos, specs y alcances duros de archivos ANTES de lanzar cualquier
   agente.
2. Lanza lectores, no escritores — despliega subagentes SOLO para trabajo de mucha
   lectura con pocas dependencias cruzadas: investigación, correr tests, escaneos de
   seguridad, calificación. Nunca para autoría de código interdependiente.
3. Aísla cada carril — cada agente paralelo recibe su PROPIO worktree (un checkout
   separado del mismo repo). Los conflictos entonces afloran en el merge como
   conflictos de merge reales, nunca como sobrescrituras silenciosas que pierden
   datos sin aviso.
4. [clean-code-gauntlet](../skills/clean-code-gauntlet/SKILL.md) — cada carril corre
   su propio gauntlet de calidad dentro de su propio worktree antes de pedir
   aterrizar. Primero en seco (dry-run), para que el carril conozca su propio costo.
   Ningún carril aterriza sobre el verde de otro carril.
5. [blind-tribunal](../skills/blind-tribunal/SKILL.md) — el agente revisor recibe un
   contexto LIMPIO, nunca el del autor. El contexto compartido se pudre y se da la
   razón a sí mismo.
6. Mergea un carril a la vez, en un espacio de merge dedicado, con puerta de tests
   por código de salida.

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
