# Elite Build — el play maestro

Usa este play completo cuando se solicite expresamente o cuando construir,
reparar o mejorar necesite sus etapas compuestas de diseño, construcción,
calidad y revisión. El humano indica el objetivo una vez. Un cambio acotado
puede usar los métodos pertinentes de BACKS Build Flow sin iniciar todo este
play; seleccionarlo conserva todas las puertas aplicables de abajo.

## Una tarea, un responsable de integración

[BACKS Build Flow](../skills/backs-build-flow/SKILL.md) controla paquete de tarea,
`task_mode`, esencia del operador y resultado. Reutiliza contexto vigente,
cuerpos reales cargados y evidencia; actualiza una etapa solo si cambian entradas
o candidato. Conserva `base_sha` fijado, `candidate_sha` actual y un responsable
entre todos los carriles. Llamar a un especialista no inicia otro ciclo de vida.

[bounded-loops](../skills/bounded-loops/SKILL.md) controla plazo original y cupos
restantes. Investigación, constructores, lint/tipos/tests, mutación, revisiones,
modelos alternativos y traspasos gastan los mismos límites. Nunca los reinicies
en un play anidado. Al agotarlos, guarda **STILL-BUILDING** con candidato, evidencia,
puertas pendientes y siguiente acción; completa trabajo útil autorizado que no
consuma el cupo agotado. Un límite de presupuesto no dispensa una puerta.

## La cadena

0. [optimus](../skills/optimus/SKILL.md) — establece piso y Build Flow una vez
   por sesión. Reutiliza los cuerpos reales que siguen presentes en contexto y sus
   recibos de origen; un recibo solo no sustituye un cuerpo ausente. Una llamada
   anidada no reinicia el ciclo ni afirma una invocación que no ocurrió.
1. Usa intención y esencia establecidas por Build Flow. Lee el pedido completo y
   correcciones actuales; deduce la directiva antes de presentar decisiones de
   entrega u opciones. Resuelve directamente lo que pueda resolverse con evidencia.
2. [human-calibration](../skills/human-calibration/SKILL.md) — aplica el perfil
   validado ya presente en el paquete. Carga solo contexto aplicable faltante;
   nunca reinterrogues al humano ni reconstruyas el mismo perfil en cada etapa.
3. [turn-and-burn](../skills/turn-and-burn/SKILL.md) — conserva requisitos de
   plantilla de misión y revisión de plan. Consulta esencia de cada modelo
   (know-thyself), `docs/BACKS_LESSONS_LEARNED.md` y `memory/MEMORY.md` cuando
   existan. Son registros de capacidades y lecciones distintos de la esencia del
   operador. Reutiliza evidencia vigente del burn; cualquier Absorb necesario
   comparte la misión y devuelve resultado al responsable de integración.
4. [understanding-gates](../skills/understanding-gates/SKILL.md) — conserva puertas
   Diseño → Plan → Construcción → Tests → Entrega. Usa
   [live-research](../skills/live-research/SKILL.md) para inspeccionar ruta afectada,
   responsables, consumidores y costura de entrega. Sigue dependencias adicionales
   cuando la evidencia indique que pueden cambiar el resultado; no repitas un
   sondeo de todo el sistema antes de cada edición. Empieza el siguiente paso
   ejecutable al cumplir la condición de contexto suficiente de Build Flow.
5. [architecture-engineer](../skills/architecture-engineer/SKILL.md) — si el diff
   toca límites de módulo, dirección de dependencias o costura compartida, aplica
   revisión estructural y clasificación de superficies de autoridad. Cita regla
   local o fallo concreto detrás de cada infracción; usa un ADR para decisiones duraderas.
6. [wayfinder](../skills/wayfinder/SKILL.md) — traza desde evidencia una ruta
   realmente pendiente. No vuelvas a planificar si la ruta ya se conoce.
7. [red-first](../skills/red-first/SKILL.md) — observa y confirma el contrato real
   fallido antes de ejecutar su constructor. Registra sello y conserva el archivo
   original byte a byte. Hallazgos posteriores reciben tests suplementarios
   separados; no pueden reescribir RED original.
8. Construye el cambio completo más pequeño en la costura responsable. Paraleliza
   preguntas y trabajo independientes con propiedad explícita de archivos o
   worktrees aislados; conserva un responsable y las reglas de concurrencia del
   proyecto. Resuelve constructores por [fleet-ladder](../skills/fleet-ladder/SKILL.md),
   usando [model-fusion](../skills/model-fusion/SKILL.md) cuando la misión lo requiera.
   Para defectos, aplica [repair-loop](../skills/repair-loop/SKILL.md) dentro del
   flujo y cierra la clase en la costura compartida con
   [seam-engineering](../skills/seam-engineering/SKILL.md). Devuelve hallazgos a
   esta tarea sin reiniciar el play recursivamente.
9. [sniper-testing](../skills/sniper-testing/SKILL.md) — deriva alcance del diff
   agregado de base a candidato más rutas pendientes propias. Ejecuta comandos
   reales de lint, tipos y tests focalizados del repo. Registra N/A con razón y
   herramientas obligatorias ausentes como huecos; no instales comprobadores
   arbitrarios ni inventes pases. Mantén pruebas acotadas durante la iteración.
10. [clean-code-gauntlet](../skills/clean-code-gauntlet/SKILL.md) — aplica calidad,
    complejidad/cobertura y mutación acotada en el mismo flujo y candidato.
    Sobreviviente significativo o hallazgo retorna a RED suplementario y arreglo
    mínimo dentro del presupuesto restante. Reutiliza evidencia válida, nunca
    veredictos obsoletos de bytes distintos; no lances otro ciclo completo.
11. [blind-eval](../skills/blind-eval/SKILL.md), después
    [blind-tribunal](../skills/blind-tribunal/SKILL.md) — entrega paquete congelado
    de evidencia sin autoría a revisores elegidos en vivo por capacidad y
    disponibilidad. Revisión en ejecuciones nuevas separadas del autor, sin
    conversación heredada del constructor. Registra ejecución autora como
    procedencia y exclúyela. Cada hallazgo fundamentado recibe RED separado,
    arreglo y nueva revisión dentro del mismo cupo. Todos los jurados requeridos
    deben aprobar. Sigue la regla Solo rig del tribunal cuando aplique; registra
    configuración real y brechas del runtime sin debilitar independencia.
12. Completa el resultado solicitado. Revisa identidad del candidato, ejecuta una
    pasada completa de suites de módulos tocados más chequeos requeridos,
    conserva trabajo concurrente y sigue integración autorizada del proyecto.
    Para despliegue, verifica código instalado/en ejecución y superficie real
    del humano. Reinicia servicios solo si entrega y procedimiento lo requieren.
    Un parche local o revisión no adquiere alcance de publicación silenciosamente.

## Puertas duras

- RED original observado fallando antes del arreglo y todavía byte a byte intacto;
  contratos suplementarios tienen evidencia y sellos propios.
- Puertas requeridas de calidad, lint/tipos/tests y mutación aprobadas sobre el
  candidato exacto, con N/A justificados y huecos reales informados honestamente.
- Revisión requerida en ejecución nueva separada del autor; el constructor nunca
  evalúa su trabajo ni dicta al revisor la conclusión deseada.
- Cada hallazgo de la costura propia se corrige o juzga con evidencia. Un hallazgo
  abierto se registra explícitamente y bloquea integrar; nunca se oculta.
- Requisitos aplicables de burn, esencia, lecciones y revisión del plan satisfechos
  con evidencia actual. Reutilizar evidencia no autoriza omitir puertas requeridas.
- Capacidad **PROVEN** significa integrada, evaluada independientemente y
  demostrada en la superficie real del humano. De lo contrario informa
  **STILL-BUILDING** y prueba exacta faltante con
  [human-voice](../skills/human-voice/SKILL.md). Declara finalización de revisión o
  parche solicitado por separado de una capacidad en vivo.
- Confirma solo archivos de esta tarea. Conserva trabajo de otras sesiones.

## Política de escalera de la flota

Usa [fleet-ladder](../skills/fleet-ladder/SKILL.md) para despachos reales, rutas
configuradas, sondeos, alternativas e independencia de revisión. Lee
`config/fleet_ladder.yaml` y `config/gpu_nodes.yaml` del despliegue cuando estén
disponibles; el pack no crea un resolutor. Conserva requisitos de investigación
previa para peldaños frontera y sus fuentes permitidas de web, GitHub, Reddit y
papers. Respeta nivel de razonamiento y política de eficiencia de tokens
configurados; no fijes IDs de modelos ni truncues evidencia para fabricar cumplimiento.

Usa [session-handoff](../skills/session-handoff/SKILL.md) para conservar candidato,
sellos, evidencia, plazo y cupos restantes antes de una interrupción.
