---
name: "repair-loop"
description: "Úsala al reparar un bug, cerrar un problema reportado o mejorar una costura de punta a punta mediante reproducción, RED sellado, arreglo de la clase, comprobaciones acotadas y entrega verificada dentro del presupuesto de misión."
license: "MIT"
---

# Repair Loop
**Effort:** light — el bucle en sí es disciplina más una pasada de calificación independiente; los pasos más pesados que encadena (gauntlet, tribunal) llevan su propio sello y solo se disparan en cambios que van a entregarse. Elimina: aterrizajes verdes-pero-rotos, y el retrabajo de bug reabierto que cuestan.

El loop por defecto para cualquier fix, cierre de bug o mejora. Es un
comportamiento, no maquinaria de aprobaciones: agrega cero compuertas y cero
fricción para el humano. Ata al agente a una disciplina que hace que "verde pero
roto" sea estructuralmente difícil de entregar.

## Carga primero, antes de cualquier diseño o edición

Usa [BACKS Build Flow](../backs-build-flow/SKILL.md) para paquete de tarea, esencia
del operador y un responsable de integración. Reutiliza reglas aplicables,
contexto, cuerpos cargados y evidencia ya establecidos; actualiza solo lo que
cambió. Una invocación directa establece contexto faltante una vez. Carga el piso
de invariantes y puertas de comprensión requeridas si faltan; usa wayfinder solo
para una ruta sin resolver. Un hallazgo de reparación no reinicia el play externo.

[bounded-loops](../bounded-loops/SKILL.md) controla plazo compartido y cupos restantes
de intentos/rondas. Conserva `mission_id`, `task_mode`, `base_sha` fijado y
`candidate_sha` actual durante reproducciones, ediciones, herramientas, modelos,
revisiones y traspasos. Una llamada anidada no reinicia presupuesto. Revisar y
diagnosticar devuelve evidencia sin editar ni promover; construir requiere ese alcance.

## El loop

1. **Fundamenta la ruta afectada.** Comprueba reglas, código actual del proyecto,
   contratos de llamadas y comprobaciones existentes. Reutiliza evidencia vigente
   y pertinente sin repetir una auditoría de todo el repo.
2. **Reproduce sobre la verdad viva.** Ve el fallo tú mismo, en la ruta real que
   el humano usa — no una sonda proxy, no la palabra del reporte de bug. Sin
   reproducción no hay fix.
3. **Test de contrato en rojo.** Escribe un test que falle capturando el defecto,
   y commitéalo antes del fix. Prueba que de verdad está en rojo. El fix lo pone
   en verde; el fix jamás edita el test. Ver [red-first](../red-first/SKILL.md).
4. **Arregla la CLASE en el seam** (la costura donde vive el defecto) — no un
   parche puntual por síntoma. La fórmula completa vive en
   [seam-engineering](../seam-engineering/SKILL.md).
5. **Ejecuta comprobaciones acotadas.** Usa [sniper-testing](../sniper-testing/SKILL.md)
   para derivar alcance del diff agregado de `base_sha` a `candidate_sha` y rutas
   propias pendientes. Ejecuta comandos reales de lint, tipos y tests del repo.
   Registra comando, resultado y revisión. Marca **N/A** con razón lo no aplicable;
   herramienta obligatoria ausente es un hueco. No instales herramientas arbitrarias
   ni inventes pases. El test sellado sigue idéntico byte a byte.
6. **Mide dentro del flujo.** Aplica [clean-code-gauntlet](../clean-code-gauntlet/SKILL.md)
   para calidad y mutación acotada del candidato. Investiga sobrevivientes; si
   revelan huecos de test, añade un archivo suplementario separado conservando RED
   original. Corrige la costura responsable y repite comprobaciones afectadas
   dentro del mismo cupo restante; nunca rebajes puertas para lograr GREEN.
7. **Calificación independiente.** Un evaluador que no escribió el cambio —
   elegido en vivo por capacidad y disponibilidad desde la matriz de peldaños
   configurada; la ejecución autora que construyó queda descalificada, igual que
   cualquier sesión que haya heredado la conversación o el contexto del
   constructor. Un evaluador en una sesión fresca y disjunta del autor debe
   darle el pase. El constructor nunca califica su propio trabajo. Ver
   [blind-tribunal](../blind-tribunal/SKILL.md).
8. **Revisa el trabajo concurrente.** Antes de alterar estado compartido,
   verifica que el trabajo en vuelo de cualquier otra sesión está preservado (en
   una rama o commit). Nunca commitees ni limpies trabajo que no es tuyo.
9. **Verifica e integra dentro del alcance.** Una pasada completa por suites
   de módulos tocados al integrar, más chequeos obligatorios del proyecto; sigue
   la entrega autorizada. Comprueba comportamiento en la superficie real del humano
   (su UI o comando) y registra revisión exacta candidata/instalada. Tests locales
   y evidencia estática original no establecen entrega en vivo. Cierra cada hallazgo
   en esta costura o registra «no es un bug» con evidencia. «Arreglé el grande y
   aplacé el resto» nunca aterriza.

## Itera dentro del presupuesto de misión

Un chequeo fallido aporta la siguiente hipótesis acotada. Reintenta o elige una
ruta capaz configurada solo dentro del cupo restante; cambiar modelo no crea
misión nueva. Aplica reglas de estancamiento y agotamiento de bounded-loops.
Al alcanzar un límite guarda **STILL-BUILDING** con candidato, tests sellados,
evidencia de fallo, puertas pendientes y siguiente acción exacta. Completa trabajo
útil autorizado que no consuma cupo agotado. Un hallazgo abierto bloquea integrar
pero no borra progreso ni se vuelve un veredicto **PROVEN** inventado.

## Reglas duras — cualquiera de estas reprueba la skill

- Fix entregado sin reproducción sobre la verdad viva.
- Test escrito después del fix, o editado por el fix.
- Síntoma parchado mientras la clase sigue abierta en el seam.
- Capacidad declarada en verde desde un proxy mientras la propia ruta del humano
  sigue rota.
- El constructor calificó su propio cambio.
- Un hallazgo sacado a la luz, aplazado en silencio al aterrizar.
- Ciclo reiniciado, abandonado en silencio o declarado verde con una puerta pendiente.

## Reporte

Dos palabras — **PROVEN** (probado) o **STILL-BUILDING** (aún en construcción) —
más la intención en lenguaje claro y la única decisión frente al humano, si la
hay. Las preguntas van al humano solo por gusto, visión o riesgo destructivo;
ver [decision-bar](../decision-bar/SKILL.md).

## Combina bien con

- [incident-closure](../incident-closure/SKILL.md) — cuando el humano reporta una rotura, este loop corre dentro de un cierre completo.
- [red-first](../red-first/SKILL.md) · [seam-engineering](../seam-engineering/SKILL.md) · [sniper-testing](../sniper-testing/SKILL.md)
- [blind-tribunal](../blind-tribunal/SKILL.md) · [clean-code-gauntlet](../clean-code-gauntlet/SKILL.md)
