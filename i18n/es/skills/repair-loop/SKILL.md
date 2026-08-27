---
name: repair-loop
description: Úsala al arreglar un bug, cerrar un issue reportado o mejorar un seam de punta a punta. Corre el loop de reparación completo — anclarse en el piso, reproducir sobre la verdad viva, test de contrato en rojo, arreglar la clase en el seam, verificar en la ruta real, calificación independiente, aterrizar — e itera hasta que sea verdad. Trigger words: repair loop, dev mode, fix this, uplift, close the seam, dev build, loop de reparación, modo dev, arregla esto, arréglalo, mejora, cierra el seam.
license: MIT
---

# Repair Loop
**Effort:** light — el bucle en sí es disciplina más una pasada de calificación independiente; los pasos más pesados que encadena (gauntlet, tribunal) llevan su propio sello y solo se disparan en cambios que van a entregarse. Elimina: aterrizajes verdes-pero-rotos, y el retrabajo de bug reabierto que cuestan.

El loop por defecto para cualquier fix, cierre de bug o mejora. Es un
comportamiento, no maquinaria de aprobaciones: agrega cero compuertas y cero
fricción para el humano. Ata al agente a una disciplina que hace que "verde pero
roto" sea estructuralmente difícil de entregar.

## Carga primero, antes de cualquier diseño o edición

1. [invariant-floor](../invariant-floor/SKILL.md) — lee tu reglamento antes de trabajar.
2. [human-calibration](../human-calibration/SKILL.md) — aplica el perfil del humano; nunca lo vuelvas a interrogar.
3. [understanding-gates](../understanding-gates/SKILL.md) — el planificador diagnóstico: Diseño → Plan → Build → Test → Entrega.
4. [wayfinder](../wayfinder/SKILL.md) — cuando estés perdido, traza la ruta; nunca estaciones una pregunta sobre el humano.
5. Si la petición llega como prosa o metáfora, corre [intent-compiler](../intent-compiler/SKILL.md) primero e itera sobre la directiva deducida.

## El loop

1. **Ánclate en el piso.** Carga las reglas y la verdad propia del proyecto
   (docs, código fuente, tracker) antes de tocar código. El trabajo hecho de
   memoria de las reglas no cuenta.
2. **Reproduce sobre la verdad viva.** Ve el fallo tú mismo, en la ruta real que
   el humano usa — no una sonda proxy, no la palabra del reporte de bug. Sin
   reproducción no hay fix.
3. **Test de contrato en rojo.** Escribe un test que falle capturando el defecto,
   y commitéalo antes del fix. Prueba que de verdad está en rojo. El fix lo pone
   en verde; el fix jamás edita el test. Ver [red-first](../red-first/SKILL.md).
4. **Arregla la CLASE en el seam** (la costura donde vive el defecto) — no un
   parche puntual por síntoma. La fórmula completa vive en
   [seam-engineering](../seam-engineering/SKILL.md).
5. **Verifica en la ruta real.** Confía pero verifica. La capacidad se prueba en
   la propia superficie del humano — la UI donde escribe, el comando que corre —
   nunca en un test verde sobre un seam con mocks. Contrasta cada afirmación ("la
   otra rama ya lo aterrizó", "ese servicio está caído") con la verdad viva antes
   de actuar sobre ella.
6. **Mide el fix.** A mitad del loop, corre solo los tests que cubren el seam que
   tocaste — ver [sniper-testing](../sniper-testing/SKILL.md). Luego corre el
   [clean-code-gauntlet](../clean-code-gauntlet/SKILL.md) sobre el código
   cambiado: tests acotados, puntaje de complejidad-contra-cobertura, mutation
   testing acotado. Un mutante que sobrevive a tu fix significa que el test nunca
   llegó a la rama que cambiaste — verde falso; sigue iterando.
7. **Calificación independiente.** Un evaluador que no escribió el cambio —
   idealmente un modelo de una familia distinta a la del constructor — debe darle
   el pase. El constructor nunca califica su propio trabajo. Ver
   [blind-tribunal](../blind-tribunal/SKILL.md).
8. **Revisa el trabajo concurrente.** Antes de alterar estado compartido,
   verifica que el trabajo en vuelo de cualquier otra sesión está preservado (en
   una rama o commit). Nunca commitees ni limpies trabajo que no es tuyo.
9. **Aterriza.** Una pasada completa sobre las suites de los módulos tocados al
   aterrizar, y entonces commit. Cierra cada hallazgo que el loop sacó a la luz
   en este seam — o registra un veredicto explícito de "no es un bug" con
   evidencia por hallazgo. "Arreglé el grande y aplacé el resto" nunca aterriza.

## Itera hasta que sea verdad

Una regla que aún no se cumple no detiene el loop — lo impulsa. Escala el modelo
o el nivel, arregla el bloqueo, reintenta, hasta que cada paso de arriba sea
verdad y el cambio aterrice. "Suficientemente bueno" no es un estado. Si te
atoras de verdad dos veces en el mismo seam, registra la evidencia exacta del
bloqueo y pasa a la siguiente pieza desbloqueada — nunca muelas en silencio.

## Reglas duras — cualquiera de estas reprueba la skill

- Fix entregado sin reproducción sobre la verdad viva.
- Test escrito después del fix, o editado por el fix.
- Síntoma parchado mientras la clase sigue abierta en el seam.
- Capacidad declarada en verde desde un proxy mientras la propia ruta del humano
  sigue rota.
- El constructor calificó su propio cambio.
- Un hallazgo sacado a la luz, aplazado en silencio al aterrizar.
- Loop abandonado en "suficientemente bueno" en vez de escalado.

## Reporte

Dos palabras — **PROVEN** (probado) o **STILL-BUILDING** (aún en construcción) —
más la intención en lenguaje claro y la única decisión frente al humano, si la
hay. Las preguntas van al humano solo por gusto, visión o riesgo destructivo;
ver [decision-bar](../decision-bar/SKILL.md).

## Combina bien con

- [incident-closure](../incident-closure/SKILL.md) — cuando el humano reporta una rotura, este loop corre dentro de un cierre completo.
- [red-first](../red-first/SKILL.md) · [seam-engineering](../seam-engineering/SKILL.md) · [sniper-testing](../sniper-testing/SKILL.md)
- [blind-tribunal](../blind-tribunal/SKILL.md) · [clean-code-gauntlet](../clean-code-gauntlet/SKILL.md)
