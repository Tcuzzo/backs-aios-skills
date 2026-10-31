---
name: bounded-loops
description: "Úsala antes de trabajo que pueda reintentar, sondear, iterar, despachar trabajadores o repetir llamadas externas, incluidos ciclos autónomos de construcción, reparación, revisión y adopción."
license: MIT
---

# Ciclos acotados

Una misión tiene un único cupo restante. Un reintento, trabajador, modelo alternativo,
ronda de revisión, reinicio de contexto o skill anidada consume ese cupo; nunca lo
repone. [Build Flow](../backs-build-flow/SKILL.md) controla las transiciones de tarea.
Este método controla contabilidad del presupuesto, reintentos, cancelación y checkpoints.

## Declara y conserva el contrato

Antes de la primera acción repetitiva, registra en el paquete existente:

- `mission_id`, responsable de integración, objetivo y aceptación medible.
- Plazo o duración máxima, máximo de intentos/rondas y topes de recursos/llamadas.
- Cupo consumido y restante, límite menor de rondas del episodio actual, firma
  del fallo y siguiente acción. Usa un tope interno pequeño y explícito, a menudo
  tres intentos; elígelo para esta tarea, sin convertir el ejemplo en regla universal.
- Costos/tokens/llamadas medidos cuando existan. Marca desconocidos los contadores
  no disponibles; no inventes un cero, una asignación ilimitada ni un presupuesto
  del proveedor. Fija límites exigibles de tiempo e intentos con los contadores
  que este entorno realmente expone.

Hereda los límites más estrictos del usuario/proyecto. Si una tarea ordinaria
autorizada no trae límites, elige y declara límites proporcionales, y actúa sin
otra ronda de permisos. Pregunta solo si el compromiso real de recursos requiere
autorización. Una ampliación propuesta exige decisión explícita del responsable
de misión y la autorización del operador que corresponda; cambiar trabajadores
o tácticas no es ampliar el presupuesto.

## La iteración

1. Comprueba el cupo restante antes de despachar trabajo. Asigna techos hijos
   dentro de él, también para hijos paralelos: reserva sus máximos centralmente
   para que la suma no exceda al padre. Cada hijo devuelve consumo y cupo no usado.
2. Ejecuta una acción basada en una hipótesis. Para construir/reparar, conserva
   RED real, aplica la corrección completa más pequeña, ejecuta comprobaciones
   acotadas de lint/tipos/comportamiento y devuelve evidencia de calidad mediante
   [sniper-testing](../sniper-testing/SKILL.md) y
   [clean-code-gauntlet](../clean-code-gauntlet/SKILL.md).
3. Guarda resultados y cupo restante en puntos seguros. Un único escritor
   actualiza atómicamente el estado autorizado; los trabajadores le devuelven
   evidencia. Para una revisión estrictamente de solo lectura, usa un registro
   externo ya autorizado o la respuesta. Solo lectura no autoriza un registro en el repo.
4. Un fallo idéntico sin evidencia nueva exige cambiar hipótesis o táctica, no
   otra ejecución ciega. Cierra un episodio interno agotado. Otro episodio puede
   usar el cupo restante de la misión con contabilidad explícita.
5. Al agotar la misión, cancelarla o bloquearse una puerta obligatoria: guarda
   checkpoint, explica el bloqueo y deja de repetir. Continúa trabajo independiente
   útil solo si su alcance y cupo restante lo permiten. Informa la capacidad
   pendiente como **STILL-BUILDING**; un timeout o una puerta omitida nunca es
   GREEN ni PROVEN.

## Llamadas externas y cancelación

Respeta los límites publicados del proveedor y las señales Retry-After. Reutiliza
cachés; si los límites son desconocidos, empieza conservadoramente y mide. Usa
espera exponencial acotada ante rechazo transitorio, con tiempo máximo e intentos
máximos. No reintentes errores permanentes de autorización/entrada como si fueran
transitorios. Esperas, backoff y alternativas cuentan contra el mismo plazo.

Detente en un punto seguro del estado: registra trabajo en curso, guarda checkpoint
y cancela. No inicies un segundo escritor ni dejes un ciclo de fondo tras cancelar.
Los nuevos pedidos orientan la misión actual en ese punto; registra explícitamente
el cambio de alcance sin sustituir silenciosamente el objetivo original.

## Traspaso y salida

Quien recibe obtiene la misma identidad de misión, revisiones base/candidata,
identidad de tests sellados, cupo consumido/restante, evidencia y siguiente acción.
Verifica ese estado antes de retomar. Contexto nuevo no significa presupuesto nuevo.

El éxito exige las comprobaciones de aceptación originales y la entrega solicitada.
El agotamiento exige un checkpoint honesto, nunca tests debilitados, errores
ocultos, datos borrados, pases inventados ni otro ciclo externo con contador repuesto.

Consulta [session-handoff](../session-handoff/SKILL.md) para continuar y
[fleet-ladder](../fleet-ladder/SKILL.md) antes de despachar modelos realmente configurados.
