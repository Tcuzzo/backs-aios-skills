---
name: backs-build-flow
description: "Úsala al construir, reparar, revisar, retomar o entregar trabajo que exige coordinar contexto, skills y verificación sin perder el impulso de ejecución."
license: MIT
---

# BACKS Build Flow

Un único responsable de integración lleva el pedido desde el contexto hasta la
entrega verificada. Las skills especialistas devuelven evidencia a ese responsable;
no reinician el flujo. Para una respuesta sencilla sin construcción ni
investigación, usa solo los pasos pertinentes.

## Reúne suficiente contexto para actuar

1. Conserva el objetivo, las restricciones, la autorización existente y el resultado
   solicitado. Elige un modo: **construir/reparar**, **revisión de solo lectura**,
   **investigar** o **retomar/entregar**. Una revisión no autoriza cambios,
   instalaciones ni despliegues.
2. Reutiliza el paquete de tarea vigente. Si falta, usa
   [context-engineer](../context-engineer/SKILL.md) para verificar el destino,
   las instrucciones rectoras, la ruta afectada de llamadas y consumidores,
   el trabajo existente y la comprobación de aceptación.
   [building-with-backs](../building-with-backs/SKILL.md) resuelve el checkout y
   la promoción. Fija el `base_sha` anterior al cambio y actualiza `candidate_sha`
   a medida que se confirman cambios.
3. Aplica [operator-essence](../operator-essence/SKILL.md) al operador actual:
   carga el fragmento pertinente de contexto personal o ejecuta una sola vez su
   arranque de insights para perfiles ausentes. Las observaciones cualitativas y
   la evidencia cuantitativa orientan la comunicación y la verificación; no
   otorgan autoridad ni fijan una personalidad. Marca como provisional la
   evidencia escasa y continúa el trabajo útil autorizado. Usa
   [intent-compiler](../intent-compiler/SKILL.md) solo para intención ambigua;
   [operator-intent-deduction](../operator-intent-deduction/SKILL.md) decide si una
   elección material pendiente realmente necesita al operador.
4. **Empieza a ejecutar cuando puedas nombrar el destino, la siguiente acción
   concreta, las restricciones y una comprobación observable de aceptación.**
   Leer más debe resolver una pregunta concreta que pueda cambiar esa acción.
   No vuelvas a mapear todo el repositorio repetidamente.

## Enruta las skills una vez, con una salida y un cierre

Carga los cuerpos reales de las skills pertinentes; un nombre o recibo no demuestra
su aplicación. Reutiliza cuerpos y evidencia que sigan presentes y vigentes en el
contexto. Tras una compactación, recarga solo lo necesario para la siguiente acción.
Para cada especialista, indica su propósito, la evidencia esperada y su condición
de salida; consulta referencias más profundas cuando hagan falta. Un único paquete
vigente registra responsable, estado y siguiente acción
([formato de paquete y traspaso](references/task-packet.md)). Evita registros duplicados.

Para adoptar capacidades, [absorb](../absorb/SKILL.md) se ocupa del mapa de
capacidades y la integración nativa. [rea-investigation](../rea-investigation/SKILL.md)
aporta evidencia de descubrimiento o verificación cuando corresponda y regresa a
quien la llamó sin iniciar Absorb recursivamente. Para código fuente ordinario,
usa directamente el código y sus tests.

## Ejecuta el ciclo acotado RED → GREEN

Vincula [bounded-loops](../bounded-loops/SKILL.md) antes de reintentar: un
`mission_id`, plazo, cupo de intentos/rondas y presupuesto de recursos restante.
Los trabajadores hijos, cambios de modelo, hallazgos y rondas de revisión consumen
ese mismo cupo.

1. **RED:** [red-first](../red-first/SKILL.md) establece una comprobación real de
   comportamiento que falla antes de la reparación. Conserva su archivo sellado
   y la identidad de su línea base. Para revisión o investigación, usa su contrato
   de evidencia sin fabricar cambios.
2. **Construcción:** implementa el cambio completo más pequeño en la costura
   responsable; actualiza consumidores afectados y superficies de compatibilidad.
   Conserva el trabajo ajeno.
3. **Lint y tests:** [sniper-testing](../sniper-testing/SKILL.md) deriva el alcance
   desde `base_sha` hasta el candidato actual, incluyendo trabajo pendiente
   pertinente. Ejecuta lint, comprobación de formato, tipos y tests de comportamiento
   aplicables del repositorio. Registra comandos exactos, revisión, resultados y
   comprobaciones no disponibles o no aplicables. Un árbol limpio no borra el
   alcance de los cambios confirmados.
4. **Calidad:** [clean-code-gauntlet](../clean-code-gauntlet/SKILL.md) usa ese mismo
   alcance y presupuesto para calidad medida, mutación aislada y acotada, y revisión
   independiente. Añade tests suplementarios para nuevos huecos sin reescribir el
   RED sellado.
5. **Responde a la evidencia:** corrige hallazgos demostrados y repite solo las
   comprobaciones afectadas. Fallos idénticos repetidos exigen cambiar la hipótesis
   o táctica. Al agotar límites, guarda un checkpoint del trabajo pendiente;
   nunca reinicies el presupuesto ni rebajes las comprobaciones.

Cuando el candidato se estabilice, usa las puertas agregadas de integración que
exige el repositorio. Informa las capacidades reales del entorno; no inventes
herramientas, tests ni revisiones.

## Completa el resultado solicitado

Continúa con empaquetado, commit, publicación y verificación autorizados cuando
formen parte del pedido. Si realmente se necesita aprobación externa, prepara
primero el resultado completo y revisable. Informa de hallazgos, acción actual,
evidencia y dónde inspeccionar el trabajo en curso; sigue la cadencia del usuario.

Distingue **tarea solicitada entregada** del estado de capacidad **PROVEN** del
piso de invariantes. Un parche local o una revisión terminados no implican un
despliegue en vivo. Las puertas obligatorias fallidas o ausentes siguen visibles:
guarda **STILL-BUILDING** con bloqueo exacto, cupo restante y siguiente acción.
En modo de solo lectura devuelve el paquete en la respuesta o en un registro
externo ya autorizado; no crees implícitamente un registro del repositorio ni un
archivo de esencia.
