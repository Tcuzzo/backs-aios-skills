---
name: red-first
description: Úsala al despachar cualquier constructor — un agente, un modelo o tú mismo — para hacer un cambio que un test debería probar. Commitea un test de contrato probado-en-rojo antes de que arranque el build, le prohíbe al constructor tocarlo, y un evaluador independiente verifica que el test nunca fue editado. Trigger words: red first, failing test first, contract test, red baseline, tamper-proof test, test before build, rojo primero, test en rojo primero, test de contrato, línea base roja, test a prueba de manipulación, test antes del build.
license: MIT
---

# Rojo Primero, a Prueba de Manipulación
**Effort:** free — pura disciplina de orden: el test que igual ibas a escribir se escribe primero, se prueba en rojo y se sella con un commit; el chequeo de manipulación es un solo git diff. Elimina: tests moldeados después del arreglo para pasar, y veredictos verdes que un constructor dobló editando el test.

Un test escrito después del fix no prueba nada — fue moldeado para pasar.
Un test que el constructor puede editar prueba menos — se puede doblar para pasar.
Así que el test va primero, se sella, y se califica intacto.

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
3. **Commitea el test rojo ANTES de despachar al constructor.** Registra el id
   del commit. Ese commit es la línea base roja — el sello anti-manipulación.
4. **Despacha al constructor con un solo trabajo: ponerlo en verde.** El
   constructor tiene prohibido tocar el archivo del test. Dilo en el despacho.
5. **Califica de forma independiente.** Un evaluador que no escribió el cambio
   revisa dos cosas:
   - el test ahora pasa;
   - el archivo del test es byte a byte idéntico a la línea base roja —
     `git diff <red-sha> HEAD -- tests/test_contract.py` no imprime nada.
   Cualquier diff sobre el archivo del test reprueba la calificación. Sin
   excepciones, ni siquiera "solo corregí un typo".
6. **Prefiere una guarda estructural sobre tests puntuales regados.** Una guarda
   estructural es un chequeo (un barrido con grep, un escaneo de AST, una regla
   de lint) que falla con el PRÓXIMO infractor, no solo con esta instancia. Una
   guarda gana a diez tests puntuales que fijan un caso cada uno.

## Reglas duras

- **El rojo se prueba en rojo.** Córrelo, míralo fallar, antes de que cuente.
- **El constructor nunca edita el test.** El diff vacío del archivo de test
  desde la línea base roja es parte de la compuerta de aterrizaje, no un chequeo
  de cortesía.
- **El constructor nunca es el evaluador.** Usa otra persona, otro agente, o un
  modelo de una familia distinta a la del constructor.
- **El verde solo no es prueba.** Verde + test intacto + calificación
  independiente es prueba.
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
