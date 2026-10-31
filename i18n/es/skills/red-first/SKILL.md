---
name: "red-first"
description: "Úsala antes de despachar un constructor para un cambio de comportamiento demostrable, o cuando un hallazgo de revisión o hueco de mutación necesite un contrato de regresión."
license: "MIT"
---

# Rojo Primero, a Prueba de Manipulación
**Effort:** free — pura disciplina de orden: el test que igual ibas a escribir se escribe primero, se prueba en rojo y se sella con un commit; el chequeo de manipulación es un solo git diff. Elimina: tests moldeados después del arreglo para pasar, y veredictos verdes que un constructor dobló editando el test.

Un resultado verde observado solo después del fix no demuestra el fallo original
ni que el test pueda detectarlo. Demuestra y sella el RED original antes del fix;
el constructor deja ese archivo intacto. Una regresión suplementaria separada
puede demostrar después un fallo frente a un mutante controlado y un pase frente
al candidato sin mutación, como se describe más abajo.

Usa el paquete actual de [BACKS Build Flow](../backs-build-flow/SKILL.md). Esta
skill controla el sello RED; no crea otro responsable ni ciclo de construcción.
Conserva `base_sha` fijado, `candidate_sha` actual e identidad de misión. Plazo
e intentos restantes de [bounded-loops](../bounded-loops/SKILL.md) cubren reproducción,
constructores, tests suplementarios y revisiones. Reutiliza un recibo RED válido
en vez de fabricar un fallo nuevo.

## Cuándo correrla

Antes de despachar cualquier build o fix donde un test pueda enunciar el
comportamiento deseado. Este es el default tanto para arreglos de bugs como para
capacidades nuevas.

## Pasos

1. **Escribe el test de contrato en rojo.** Enuncia el comportamiento que
   quieres, en la forma más pequeña que detectaría su ausencia. Debe fallar
   ahora mismo.
2. **Pruébalo en rojo.** Corre el test y míralo fallar — por la razón correcta.
   Un test que revienta en el import, o que pasa calladito, no está en rojo. Un
   test rojo que nadie corrió es una suposición, no una línea base.
3. **Confirma el test RED ANTES de despachar al constructor.** Registra id del
   commit, rutas y bytes exactos, comando/salida fallidos y razón. Ese commit es
   la línea base RED y sello contra manipulación; no sustituye el `base_sha`
   fijado de misión que delimita el cambio agregado.
4. **Despacha al constructor con un solo trabajo: ponerlo en verde.** El
   constructor tiene prohibido tocar el archivo del test. Dilo en el despacho.
5. **Califica de forma independiente.** Un evaluador que no escribió el cambio
   revisa dos cosas:
   - el test ahora pasa;
   - el archivo del test es byte a byte idéntico a la línea base roja —
     `git diff <red-sha> <candidate_sha> -- tests/test_contract.py` no imprime nada.
     Si se prueba trabajo pendiente, compara también los bytes reales con el
     sello; un diff confirmado limpio no excusa una edición preparada o sin preparar.
   Cualquier diff sobre el archivo del test reprueba la calificación. Sin
   excepciones, ni siquiera "solo corregí un typo".
6. **Prefiere una guarda estructural sobre tests puntuales regados.** Una guarda
   estructural es un chequeo (un barrido con grep, un escaneo de AST, una regla
   de lint) que falla con el PRÓXIMO infractor, no solo con esta instancia. Una
   guarda gana a diez tests puntuales que fijan un caso cada uno.

## Un hallazgo nuevo después del sello original

Un sobreviviente de mutación o hallazgo de revisión puede revelar una aserción
faltante. Conserva byte a byte el archivo RED original y añade un **archivo
suplementario separado**. Observa que falla por el nuevo defecto antes del
arreglo; para huecos de mutación demuestra fallo ante el mutante controlado
pertinente en aislamiento y pase ante el candidato sin mutar. Registra y sella
esa evidencia antes de que el siguiente constructor cambie la costura. No
afirmes que era la línea base original. El evaluador comprueba ambos sellos y
el candidato agregado exacto. Añadir un test no autoriza debilitar, renombrar
ni reemplazar el contrato original.

Si se agota el presupuesto compartido o no puede establecerse RED, guarda
**STILL-BUILDING** con el hueco y la siguiente acción exacta. No fabriques RED
ni reinicies la misión para forzar verde.

## Reglas duras

- **El rojo se prueba en rojo.** Córrelo, míralo fallar, antes de que cuente.
- **El constructor nunca edita el test.** El diff vacío del archivo de test
  desde la línea base roja es parte de la compuerta de aterrizaje, no un chequeo
  de cortesía.
- **El constructor nunca es el evaluador.** Usa un evaluador que no sea del
  constructor, elegido en vivo por capacidad y disponibilidad desde la matriz
  de peldaños configurada; la ejecución autora que construyó queda descalificada,
  igual que cualquier sesión que haya heredado la conversación o el contexto del
  constructor. El evaluador trabaja en una sesión fresca y disjunta del autor.
- **El verde solo no es prueba.** Verde + test intacto + calificación
  independiente prueba este contrato; una capacidad en vivo todavía necesita
  evidencia de superficie real y entrega del flujo de tarea.
- **Cuando hay una clase entera de defecto en juego, guarda la clase.** Los
  tests puntuales frenan este bug; una guarda estructural frena el siguiente.

## Combina bien con

- [sniper-testing](../sniper-testing/SKILL.md) — corre solo los tests que el
  cambio toca mientras iteras; una pasada completa al aterrizar.
- [seam-engineering](../seam-engineering/SKILL.md) — la disciplina de arreglar
  la clase, a la que pertenece la guarda estructural.
- [blind-tribunal](../blind-tribunal/SKILL.md) — evaluadores independientes que
  nunca vieron al autor.
- [repair-loop](../repair-loop/SKILL.md) — el loop que lleva rojo → verde →
  probado de punta a punta.
