# Nombres — cómo nombra las cosas este pack, y por qué

Los nombres de este pack cargan peso. Un agente elige una skill comparando la tarea
contra el nombre y la descripción, así que un nombre que dice lo equivocado enruta
el trabajo a la disciplina equivocada. La convención de abajo mantiene honesto el
enrutado.

## Los tres tipos de nombres

- **Las skills son disciplinas en frase nominal.** Una skill es el contexto que un
  agente carga para razonar — un cuerpo de reglas, no una acción. Por eso se nombra
  como una disciplina: `red-first`, `seam-engineering`, `sniper-testing`. Una
  disciplina se carga; no se "ejecuta".
- **Los comandos son imperativos.** Un comando es una acción con principio y fin,
  así que su nombre es un verbo, o el nombre de la jugada o de la skill que dispara:
  boot, build, hunt, grade, tribunal.
- **El piso de invariantes es ley.** `invariant-floor` es la única skill que todas
  las demás heredan. Se llama por lo que es — el piso — porque cada regla dura del
  pack se para sobre él, y ninguna skill puede aterrizar un cambio por debajo de él.

## Los comandos incluidos

| Comando | Dispara |
| --- | --- |
| `/agent-build` | `plays/agent-builds.md` |
| `/bughunt` | `plays/bughunt.md` |
| `/design-taste` | `plays/design-taste.md` |
| `/elite-build` | `plays/elite-build.md` |
| `/grade` | `plays/grading-verification.md` |
| `/optimus` | `skills/optimus/SKILL.md` |
| `/parallel-work` | `plays/parallel-work.md` |
| `/secure-delivery` | `plays/security-delivery.md` |
| `/tribunal` | `skills/blind-tribunal/SKILL.md` |
| `/web-build` | `plays/web-app-builds.md` |

Que `design-taste` exista como skill, jugada y comando es deliberado — una
disciplina, tres formas de entrada: la skill es el contexto, la jugada es la receta,
el comando es el gatillo. No hay ambigüedad porque el comando dispara la jugada; la
jugada enlaza la skill.

## Dónde vive cada tipo de información

Cada capa responde una pregunta distinta, y nada se duplica:

- **El nombre dice el mecanismo.** `blind-tribunal` te dice cómo funciona antes de
  abrir el archivo: jurados, ciegos al autor.
- **La descripción lleva las palabras gatillo.** El runtime compara tus palabras
  contra las descripciones, así que la descripción guarda cada frase que un humano
  diría cuando necesita la skill — incluidos los nombres viejos (mira abajo).
- **El cuerpo lleva las reglas.** Pasos, reglas duras que hacen fallar la skill, y
  las skills con las que se combina. El cuerpo es la disciplina; el nombre y la
  descripción son solo su dirección.

## Los renombres nunca rompen

Cuando una skill se renombra, su nombre viejo pasa a la descripción como palabra
gatillo, para que cada hábito y cada doc que usaba el nombre viejo siga enrutando
bien:

- **optimus** conserva su nombre tal cual — es la marca de arranque, el único nombre
  propio del pack, y el comando que escribes primero (`/optimus`).
- **"yoke"** sobrevive como palabra gatillo en `human-calibration` — di cualquiera
  de los dos, y carga la misma disciplina.

Un renombre que rompe un gatillo existente es una regresión, no una limpieza.

## Sellos de esfuerzo

Cada skill lleva una línea **Effort:** bajo su título, que responde dos preguntas:
¿qué GASTA correrla, y qué esfuerzo desperdiciado ELIMINA? Tres niveles:

- **free** — disciplina pura: sin llamadas extra a modelos, sin corridas extra de
  herramientas. Algunas skills free recortan el costo neto directamente, y sus
  sellos lo dicen.
- **light** — una pasada extra: un subagente, una corrida de validador, un sondeo,
  una escritura con el test primero.
- **heavy** — varios modelos o agentes, o cómputo real (corridas de mutación,
  paneles de jurados). Un sello heavy además debe decir CUÁNDO se paga el gasto.

Ley de honestidad: el sello es una afirmación que el cuerpo de la skill debe
respaldar — un tribunal sellado como free es una mentira. La cláusula "Elimina:"
nombra el desperdicio específico que la skill borra (retrabajo matado, aterrizajes
rebeldes matados, re-corridas de la suite completa matadas), nunca un genérico
"ahorra tiempo". Cada jugada termina con una línea **Weight:** que suma su cadena
de la misma manera.

## Justificación por skill

| Nombre | Por qué este nombre |
| --- | --- |
| absorb | La disciplina de tomar una capacidad externa y re-ingenierarla como nativa, en vez de duplicarla. |
| blind-eval | Evaluación con la autoría oculta — la ceguera es el mecanismo. |
| blind-tribunal | Un panel de jurados, ciegos al autor, de distintas familias de modelos. Tribunal = panel más veredicto. |
| bounded-loops | La propiedad que impone: cada bucle lleva un límite — presupuesto, checkpoint, kill-switch. |
| clean-code-gauntlet | Un gauntlet es una serie de chequeos duros; el código limpio es lo que sobrevive. |
| decision-bar | Una sola vara contra la que se mide cada decisión antes de poder llegar al humano. |
| design-taste | La disciplina del gusto en el trabajo visual — con puertas y chequeos, no dejada a la intuición. |
| fleet-ladder | La flota de modelos resuelta como una escalera de respaldo, que se sube en orden. |
| gpu-dispatch | La ley de despacho para trabajo en GPU: un modelo por tarjeta, caliente durante el bucle. |
| guided-steps | Pasos que solo un humano puede hacer, guiados una etapa a la vez. |
| human-calibration | Calibrar la construcción al humano al que sirve. (Era "yoke" — el nombre viejo sobrevive como palabra gatillo.) |
| incident-closure | Un incidente se cierra completo — de la causa raíz a la prueba en vivo — nunca se triaja de vuelta al humano. |
| intent-compiler | Compila lenguaje natural en una directiva ejecutable. La prosa es la fuente; la directiva es la salida. |
| invariant-floor | El piso de leyes numeradas que todo cambio debe superar. Ley, no guía. |
| leap-protocol | El protocolo para saltar trabajo grande entre constructores paralelos y aterrizarlo por una sola espina. |
| live-research | Investigación contra fuentes vivas — docs y código tal como están ahora — no la memoria del modelo. |
| model-fusion | Muchos modelos borradorean, un juez independiente elige — fusión de salidas, no una votación. |
| optimus | La marca de arranque, conservada como nombre propio. Arranca el piso; cada sesión empieza aquí. |
| human-voice | Nombrado por lo que impone: el agente escribe como habla una persona, y las ideas difíciles igual llegan completas. |
| red-first | El test que falla (rojo) va primero, commiteado antes de que empiece la construcción. |
| repair-loop | El bucle de arreglo completo, nombrado por su forma: anclar, reproducir, arreglar, verificar, aterrizar. |
| root-cause-first | El orden de operaciones es la regla: la causa antes que el arreglo, siempre. |
| seam-engineering | Los arreglos aterrizan en la costura — la primitiva compartida — nunca como parches sueltos regados. |
| session-handoff | Nombrado por su artefacto: un archivo de traspaso desde el que una sesión en frío puede continuar. |
| sniper-testing | Un tiro, un blanco: corre solo los tests que cubren lo que tocaste. |
| understanding-gates | Puertas en cada etapa de la construcción que chequean el entendimiento, no solo la sintaxis. |
| wayfinder | Encuentra el camino cuando se pierde, en vez de estacionar una pregunta sobre el humano. |
