> Esta es la traducción al español. La versión canónica, en inglés, vive en [README (English)](../../README.md).

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../../assets/reflex-seam-dark.svg">
  <img alt="El Reflex Seam. A la izquierda, un runtime determinista es dueño del estado, los archivos, las reglas y los tests. A la derecha, un kernel de juicio del modelo es dueño de la inferencia, la política, la reversibilidad y la prioridad. Entre ellos corre una costura dentada. Las señales de decisión cruzan del modelo al runtime, y las actualizaciones de estado cruzan de vuelta. Un cambio de estado sin permiso se rechaza en voz alta." src="../../assets/reflex-seam-light.svg">
</picture>

# BACKS AIOS Skills

**Léelo en:** [English](../../README.md) · [Português (BR)](../pt-BR/README.md) · [Français](../fr/README.md) · [Deutsch](../de/README.md) · [हिन्दी](../hi/README.md) · [简体中文](../zh-CN/README.md)

**El modelo decide. El runtime es dueño del estado, los archivos y las reglas — y si el
modelo busca un estado que no le pertenece, el sistema falla en voz alta en lugar de
adivinar.**

Esa línea es el **Reflex Seam**, y este pack la lleva a un agente que ya usas.
El hook entrega los cuerpos reales del piso, Optimus, Yoke y Build Flow al contexto
del host. Si falta contexto, lo carga y comunica cualquier diagnóstico; no rechaza
herramientas ni revoca anclaje adquirido. Los recibos de carga no se presentan como
invocaciones de skills que nunca ocurrieron.

Dos reglas viajan con él. **Sin teatro de mocks:** un test que pasa mientras la cosa
está rota es una mentira, así que los tests afirman efectos reales. **Quien construye no
califica:** el test que falla se escribe primero, y algo que no escribió el código tiene
que aprobarlo.

El pack contiene **62 carpetas de skills**: **54 métodos y alias traducidos** y
8 entradas de comando, además de **8 plays y 15 adaptadores de comando**. Los
métodos portátiles se distribuyen como Markdown que el agente puede cargar.

Para aprender con imágenes, consulta el [mapa visual de skills y bucles](../../docs/FLOWCHARTS.md).

## Misión

Este pack existe para la gente que, por precio, quedaría fuera de los resultados de
agentes de élite — coders, diseñadores y constructores que no son ingenieros de
plataforma. El harness y las skills son el igualador: cargan con los humanos que no
pueden pagar los modelos más grandes, y hacen que el nivel del modelo importe menos.
Esa es la apuesta de este pack: un modelo chico dentro de un harness fuerte puede
ganarle a un modelo grande corriendo suelto. No necesitas saber cómo se construyó el
harness para usarlo — dices las palabras gatillo, y la disciplina se dispara.

## Filosofía

Tres convicciones cruzan cada archivo de este pack.

**Programado, no prompteado.** El agente detrás de este pack se comunica claro y
rechaza las malas jugadas porque esas propiedades están construidas dentro del
harness como reglas estructurales — hooks, puertas, tests — no sugeridas en un
prompt. Una regla que un agente debe recordar falla justo cuando el agente está más
ocupado. Por eso las reglas que importan se imponen donde olvidar es imposible: en el
harness, no en la memoria del modelo.

**Las máquinas no piensan — destilan.** Dale a un modelo nada real de dónde partir y
comprime aire — una respuesta equivocada dicha con confianza. Dale al mismo modelo el
contexto correcto y acierta. Lo que llamamos razonamiento es destilación sobre
contexto: el modelo comprime lo que le dieron hasta volverlo una respuesta. Razonar
sin investigar es alucinar. Para eso existen las skills. Una skill es el contexto CON
el que un agente razona mientras razona SOBRE una cosa — lleva al agente desde el
entendimiento de alto nivel hasta la profundidad de la materia, para que la
destilación tenga algo real que destilar.

**Razona solo donde razonar es la única herramienta que funciona.** Todo lo
determinista pertenece al harness — puertas, tests, hooks, presupuestos. El
razonamiento del modelo se gasta solo donde paga su costo: juicio, diseño, leer la
intención. Esa división es lo que hace al pack igualador de modelos: el harness hace
el trabajo pesado, y el nivel del modelo deja de decidir el resultado.

## Arranque rápido

### Opción 1 — plugin de Claude Code

    /plugin marketplace add Tcuzzo/backs-aios-skills
    /plugin install backs-aios

Después escribe `/optimus` para arrancar el piso. Las skills se cargan, los comandos
de jugada quedan disponibles, y el hook de grounding viene activado (kill-switch:
`AIOS_GATE=off`).

### Opción 2 — manual

Suelta las carpetas de `skills/` en el directorio de skills de tu agente y di las
palabras gatillo. Las rutas por agente — Claude Code, cualquier runtime de Agent
Skills, OpenClaw, Hermes, un bucle de API pelado — están en [INSTALL.md](INSTALL.md).

Los gatillos en inglés son el contrato de invocación y siempre funcionan; los
equivalentes en español también disparan la misma disciplina.

| Cuando quieras... | Di... |
| --- | --- |
| Algo se rompió | "repair loop" (o "bucle de reparación") |
| Construir una funcionalidad | `/elite-build` (plugin) o lee `plays/elite-build.md` (manual) |
| ¿Esto alcanza para entregarse? | "clean code gauntlet" (o "gauntlet de código limpio") |
| Revisa mi trabajo, a ciegas | "blind tribunal" (o "tribunal ciego") |
| Estoy perdido — ¿qué sigue? | "wayfinder" (o "traza la ruta") |
| El pedido es prosa vaga | "prose is the spec" (o "la prosa es la spec") |

## Cómo funciona

- **Las skills** son disciplinas individuales. Cada una lleva palabras gatillo en su
  descripción, pasos numerados, reglas duras que hacen fallar la skill, y enlaces a
  las skills con las que se combina. Un archivo cada una: `skills/<name>/SKILL.md`.
- **Las jugadas** (plays) combinan métodos y puertas de dominio dentro del paquete
  vigente de Build Flow. Un responsable de integración conduce el trabajo con
  presupuesto compartido; cada especialista devuelve evidencia sin reiniciar la tarea.
  Un archivo por play: `plays/<name>.md`.
- **Los comandos** son las entradas slash que instala el plugin — cada uno carga una
  jugada o una skill y la ejecuta. Un archivo cada uno en `command-adapters/`.
- **La convención de nombres** — por qué las skills son frases nominales, los
  comandos son verbos y el piso es ley — está en [NAMING.md](NAMING.md).
- **Los sellos de esfuerzo** — la afirmación de costo de una línea de cada skill
  (free / light / heavy) y la línea **Weight:** con la que cierra cada jugada — se
  decodifican en [NAMING.md](NAMING.md#sellos-de-esfuerzo).

## Integración de Build Flow y esencia del operador

[backs-build-flow](skills/backs-build-flow/SKILL.md) mantiene una tarea y un responsable:
contexto suficiente → RED sellado → arreglo mínimo → lint, tipos y tests reales →
[clean-code-gauntlet](skills/clean-code-gauntlet/SKILL.md) → revisión y entrega
autorizada. El alcance va del `base_sha` fijado al candidato actual, incluso tras
commits, y todos los trabajadores y reintentos consumen el mismo presupuesto.
Un hueco nuevo recibe un test separado; el RED original permanece intacto.

[operator-essence](skills/operator-essence/SKILL.md) aporta un fragmento privado
basado en evidencia cualitativa y cuantitativa. Si falta el archivo, usa una vez
los insights admitidos del host o declara la alternativa disponible. Los datos
escasos quedan provisionales; no bloquean trabajo autorizado. El pedido y las
correcciones actuales prevalecen sobre tendencias históricas. La esencia no es
personalidad fija, política financiera/de riesgo ni autorización.

## Las skills

| Skill | Qué hace |
| --- | --- |
| [absorb](skills/absorb/SKILL.md) | Adopta una capacidad open-source existente y re-ingeniérala como skill nativa, en vez de construir un duplicado. |
| [architecture-engineer](skills/architecture-engineer/SKILL.md) | Revisa límites, dependencias y responsabilidades contra las reglas del proyecto, y registra decisiones de arquitectura. |
| [backs-build-flow](skills/backs-build-flow/SKILL.md) | Un responsable coordina contexto suficiente, esencia del operador, RED/GREEN acotado, lint/tipos/tests, gauntlet y entrega verificada. |
| [backs-pack-sync](skills/backs-pack-sync/SKILL.md) | Compara cobertura privada y pública sin revelar datos privados; añade capacidades solo mediante puentes públicos revisados. |
| [backs-session-rollover](skills/backs-session-rollover/SKILL.md) | Conserva objetivo, correcciones, evidencia y paso pendiente al compactar contexto y continuar en una sesión nueva. |
| [blind-eval](skills/blind-eval/SKILL.md) | Juzga un cambio por sus méritos con la autoría oculta, y luego conserva o revierte. Solo aterriza la mejora probada. |
| [blind-tribunal](skills/blind-tribunal/SKILL.md) | Jurados en sesiones nuevas sin contexto del autor revisan un paquete sin autoría; los hallazgos vuelven a RED suplementario y revisión dentro del presupuesto. |
| [bounded-loops](skills/bounded-loops/SKILL.md) | Un único presupuesto restante de misión limita reintentos, trabajadores, modelos y revisiones; su agotamiento conserva un checkpoint honesto. |
| [building-with-backs](skills/building-with-backs/SKILL.md) | Resuelve checkout y ruta exactos y lleva el cambio autorizado hasta la superficie real con evidencia de revisión y entrega. |
| [cam-iot-inventory](skills/cam-iot-inventory/SKILL.md) | Inventaría cámaras, IoT y Wi-Fi con identidad estable y evidencia honesta; distingue inventario de imagen disponible. |
| [clean-code-gauntlet](skills/clean-code-gauntlet/SKILL.md) | Una vara de calidad determinista: tests francotirador, el puntaje CRAP (complejidad x cobertura), testing de mutación acotado, y al final una revisión ligera de gusto. |
| [co-health](skills/co-health/SKILL.md) | Observa evidencia del harness y watchdog y comunica hallazgos preservando herramientas y código. |
| [conscientious-objector](skills/conscientious-objector/SKILL.md) | Observa evidencia del harness y watchdog sin retirar herramientas ni alterar código del operador. |
| [context-compiler](skills/context-compiler/SKILL.md) | Alias compatible de context-engineer; conserva el mismo método y paquete de ejecución. |
| [context-engineer](skills/context-engineer/SKILL.md) | Reconstruye solo contexto faltante, verifica destino y siguiente acción y conserva presupuesto, evidencia y esencia pertinente. |
| [context_engineer](skills/context_engineer/SKILL.md) | Alias compatible de context-engineer con contenido idéntico. |
| [debugging-engineer](skills/debugging-engineer/SKILL.md) | Investiga regresiones difíciles, fallos silenciosos y carreras con hipótesis refutables y sondas decisivas antes de editar. |
| [decision-bar](skills/decision-bar/SKILL.md) | Una sola vara para cada decisión: solo el gusto, la visión o el riesgo destructivo llegan al humano. Todo lo demás se ejecuta. |
| [design-critique](skills/design-critique/SKILL.md) | Critica la superficie real según tarea del usuario, jerarquía, accesibilidad, movimiento y coherencia visual. |
| [design-taste](skills/design-taste/SKILL.md) | Entrega trabajo visual que se ve diseñado, no generado: tokens de diseño primero, crítica por captura de pantalla, una puerta dura de accesibilidad. |
| [fix-shit](skills/fix-shit/SKILL.md) | Entrada directa al diagnóstico y reparación acotada de la clase de fallo, con RED sellado y prueba real de entrega. |
| [fleet-dispatch](skills/fleet-dispatch/SKILL.md) | Despacha por rol mediante la escalera configurada y devuelve resultados con procedencia real. |
| [fleet-ladder](skills/fleet-ladder/SKILL.md) | Resuelve la escalera de modelos en vivo: sondea qué está arriba, cae en orden, falla con ruido cuando la escalera se agota. |
| [gpu-dispatch](skills/gpu-dispatch/SKILL.md) | Un modelo por GPU, sin derrame a la RAM del sistema, la tarjeta caliente durante todo el bucle, descarga al terminar el bucle. |
| [guided-steps](skills/guided-steps/SKILL.md) | Guiona los pasos que solo un humano puede hacer — dashboards, credenciales, secretos — etapa por etapa, capturando cada valor. |
| [harness-optimizer](skills/harness-optimizer/SKILL.md) | Compara línea base y candidato con experimentos acotados, datos reservados y comprobaciones de fuga y sobreajuste. |
| [human-calibration](skills/human-calibration/SKILL.md) | Aplica preferencias expresadas y corregidas del operador mediante la esencia existente, sin cuestionarios duplicados ni personalidad fija. |
| [human-voice](skills/human-voice/SKILL.md) | La vara sin-título-universitario: si leerlo exige un título, reescríbelo. Conserva la idea completa mientras quita los tics de máquina. |
| [incident-closure](skills/incident-closure/SKILL.md) | "Arréglalo" significa un cierre completo — causa raíz con evidencia, test que falla, verde, prueba en vivo — nunca un menú de opciones de vuelta al humano. |
| [intent-compiler](skills/intent-compiler/SKILL.md) | Interpreta el pedido actual en un contrato ejecutable; distingue hechos, preferencias e inferencias y reutiliza la directiva vigente. |
| [invariant-floor](skills/invariant-floor/SKILL.md) | Las leyes numeradas que todo cambio autónomo debe cumplir antes de aterrizar. El piso sobre el que se para todo el pack. |
| [karpathy](skills/karpathy/SKILL.md) | Experimenta en un clon desechable con meta, métricas, archivos permitidos y presupuesto explícitos; conserva mejoras probadas. |
| [leap-protocol](skills/leap-protocol/SKILL.md) | Parte el trabajo grande en bolas con dueño independiente, repártelas a constructores paralelos en worktrees aislados, reconcilia por una sola espina de escritura. |
| [live-research](skills/live-research/SKILL.md) | Un agente de investigación paralelo lee la fuente viva — READMEs, docs, código real — para que el razonamiento se ancle en lo que de verdad hay, no en la memoria. |
| [model-fusion](skills/model-fusion/SKILL.md) | Un panel de modelos borradorea en paralelo, un juez independiente elige, y el ganador se valida contra la intención original. |
| [operator-essence](skills/operator-essence/SKILL.md) | Aporta contexto privado cualitativo y cuantitativo con fuentes, límites e incertidumbre; usa insights o alternativa disponible una sola vez. |
| [operator-intent-deduction](skills/operator-intent-deduction/SKILL.md) | Resuelve decisiones pendientes desde el pedido actual, hechos verificados y contexto respaldado, sin fijar identidad ni política de riesgo. |
| [operator_intent_deduction](skills/operator_intent_deduction/SKILL.md) | Alias compatible de operator-intent-deduction con contenido idéntico. |
| [optimus](skills/optimus/SKILL.md) | Carga los cuerpos reales del piso, Yoke y Build Flow en el contexto; el hook no rechaza herramientas ni reinicia la tarea. |
| [osha-bot](skills/osha-bot/SKILL.md) | Observa evidencia del harness y watchdog y conserva herramientas, código y control del operador. |
| [rea-investigation](skills/rea-investigation/SKILL.md) | Devuelve evidencia REA de descubrimiento o verificación al responsable actual sin reiniciar adopción o reparación. |
| [red-first](skills/red-first/SKILL.md) | Haz commit de un test probado-en-rojo antes de que empiece la construcción. El constructor no puede tocarlo. Un evaluador verifica que nunca se movió. |
| [reload-vsc-and-verify](skills/reload-vsc-and-verify/SKILL.md) | Detecta la instalación local, conecta skills ausentes y recarga VS Code con verificación de descubrimiento. |
| [repair-loop](skills/repair-loop/SKILL.md) | El bucle de arreglo completo: anclarse en el piso, reproducir, test rojo, arreglar la clase, verificar en la ruta real, calificación independiente, aterrizar. |
| [repo-map](skills/repo-map/SKILL.md) | Mapea primero la estructura real del repositorio, puntos de entrada, configuración y rutas de ejecución antes de cambiar código. |
| [root-cause-first](skills/root-cause-first/SKILL.md) | Sin arreglos sin investigación. Reproduce a demanda, instrumenta las fronteras, rastrea los datos hacia atrás hasta la fuente. |
| [scrub-plugin-pack-literals](skills/scrub-plugin-pack-literals/SKILL.md) | Detecta y elimina literales privados del pack público sin debilitar la higiene de publicación. |
| [seam-engineering](skills/seam-engineering/SKILL.md) | Arregla la clase de la falla una sola vez en su primitiva compartida, barre cada hermano, y deja una guarda que atrape al siguiente infractor. |
| [session-handoff](skills/session-handoff/SKILL.md) | Transfiere el mismo paquete, candidato, sellos RED, evidencia, plazo y presupuesto restante respetando el modo de solo lectura. |
| [sniper-testing](skills/sniper-testing/SKILL.md) | Deriva lint, tipos y tests reales del diff completo entre base fijada y candidato, incluyendo pendientes pertinentes. |
| [truth-audit](skills/truth-audit/SKILL.md) | Verifica en solo lectura qué se ejecuta realmente y convierte hallazgos comprobados en una especificación de reparación. |
| [turn-and-burn](skills/turn-and-burn/SKILL.md) | Coordina preparación de misión, revisión de plan y capacidades faltantes mediante investigación y adopción. |
| [understanding-gates](skills/understanding-gates/SKILL.md) | Puertas en Diseño, Plan, Construcción, Test y Entrega con veredictos aprobar/revisar/rechazar, para que la construcción siga calzando con el pedido. |
| [wayfinder](skills/wayfinder/SKILL.md) | Cuando estés perdido, traza un mapa de decisiones hasta el destino, en vez de estacionar una pregunta sobre el humano. |

## Las jugadas

| Jugada | Qué ejecuta |
| --- | --- |
| [elite-build](plays/elite-build.md) | La jugada maestra para cualquier construcción, arreglo o mejora: lee la intención, ponle puertas al plan, pruébalo en rojo, construye, testea acotado, califica a ciegas, aterriza probado en vivo. |
| [agent-builds](plays/agent-builds.md) | Construcción de agentes y servicios: las primitivas deterministas hacen el trabajo pesado; el modelo razona solo donde razonar es lo único que funciona. |
| [web-app-builds](plays/web-app-builds.md) | Apps y sitios web con estructura limpia y una cadena de suministro defendida — la higiene de dependencias es la jugada, no una idea de último minuto. |
| [design-taste](plays/design-taste.md) | UI que se ve diseñada, no generada: separa la creación del gusto de la implementación, fija tokens primero, dale ojos al agente, pon puerta de accesibilidad. |
| [grading-verification](plays/grading-verification.md) | Calificación adversarial: un resultado verde es una afirmación, no una prueba. El evaluador ataca, y al piso no se le puede hacer trampa. |
| [parallel-work](plays/parallel-work.md) | Reparte trabajo entre agentes sin que se pisen entre ellos: una sola espina de escritura, muchos lectores. |
| [security-delivery](plays/security-delivery.md) | La puerta de salida para cualquier cosa que un cliente u otra máquina vaya a correr. Segura por construcción, no de memoria. |
| [bughunt](plays/bughunt.md) | Una cacería de bugs acotada y en paralelo: traza el mapa, despliega buscadores, verifica cada hallazgo de forma adversarial, cierra costuras completas. |

## Funciona mejor con

Estas skills son la capa portable de **BACKS AIOS**, una plataforma de agentes
construida por [Tcuzzo](https://github.com/Tcuzzo) — un sistema indexado por grafos
y forzado por puertas donde el harness, no el modelo, sostiene la disciplina. El
sistema completo — su diseño de memoria, sus perfiles de comportamiento de modelos,
su grafo de código — no está en este pack. Aun así, las skills se sostienen solas en
cualquier agente: Claude Code, OpenClaw, Hermes, Codex, Cursor o un bucle de API
pelado. Cuanta más autonomía tenga tu agente, más se paga solo el piso.

## Crédito

Composición y conversión por [Tcuzzo](https://github.com/Tcuzzo). Algunas skills
llevan créditos de andamiaje por el trabajo publicado que injertan; están anotados en
el propio archivo y recopilados en [NOTICE.md](../../NOTICE.md) (en inglés — las
citas son hechos y se quedan tal cual). Licencia [MIT](../../LICENSE). Las
contribuciones son bienvenidas — mantén los créditos intactos.
