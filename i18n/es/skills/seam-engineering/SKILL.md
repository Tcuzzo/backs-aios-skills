---
name: "seam-engineering"
description: "Úsala al reparar un bug o al cerrar una auditoría o cacería de bugs. Arregla la clase del defecto una sola vez en su primitiva compartida, barre a cada hermano, aterriza una guarda que atrapa la próxima instancia y cierra cada hallazgo sacado a la luz — sin aplazamientos silenciosos. Trigger words: seam, class fix, whole-seam closure, point patch, structural guard, do it right the first time, costura, arreglo de clase, cierre de seam completo, parche puntual, guarda estructural, hazlo bien a la primera."
license: "MIT"
---

# Seam Engineering
**Effort:** free — pura disciplina de reparación: un solo arreglo de clase en la primitiva compartida en vez de N parches puntuales. Elimina: el mismo bug reparado otra vez en cada sitio hermano, y el hallazgo medio aplazado que se vuelve el bug misterioso que nadie encuentra en seis meses.

Un seam (la costura del sistema donde vive el defecto) se cierra correcta y
completamente, o no está cerrado. Un parche rápido hoy es el bug que nadie puede
encontrar en seis meses. Esta skill convierte un reporte de bug en una clase de
bugs cerrada.

## Cuándo correrla

Cualquier reparación: un bug reportado, un test fallido, una lista de hallazgos
de una auditoría o cacería de bugs. Sobre todo cuando sientes el tirón de
"parchearlo aquí nomás".

## Pasos

1. **Causa raíz con evidencia.** Arregla la causa, no el síntoma. Antes de
   escribir el fix, muestra la prueba: una reproducción que falla, una línea de
   log, un trace que apunta al seam real. Un fix sin evidencia es una suposición.
2. **Nombra la CLASE del defecto.** Pregunta: ¿qué familia de error es esta, y en
   qué otro lugar podría vivir el mismo error? Escribe la clase en una frase.
3. **Arregla en vertical — una vez, en la primitiva compartida.** La primitiva
   compartida es la función o módulo por donde fluye cada ocurrencia. Arréglala
   ahí. Nunca N parches puntuales. Nunca marcar-el-caso-malo-y-compensar.
4. **Barre en horizontal.** Busca cada ocurrencia hermana de la clase y
   arréglalas en el mismo cambio, no "después".
5. **Aterriza una guarda estructural.** Un test o chequeo automatizado que falla
   con la PRÓXIMA instancia de la clase. La clase se queda cerrada porque algo la
   vigila, no porque todos se acuerden.
6. **Cierra el seam completo.** Lista cada hallazgo que la cacería sacó a la luz.
   Antes de aterrizar, cada uno está arreglado y en verde, o carga un veredicto
   explícito y registrado de "no es un bug" con evidencia. Nunca un aplazamiento
   silencioso. Nunca "estacionado en un doc".

## Reglas duras

- **Una reparación que agrega una nueva condición de fallo es en sí misma un
  bug.** Un helper de rollback que puede reventar, una limpieza que deja estado
  huérfano, un test editado para bendecir el defecto que debía atrapar — todos
  bugs. Rediseña el cambio como una unidad atómica, o como una máquina de
  estados explícita y a prueba de caídas. Nunca lo tapes de pasada.
- **"Arreglé los de severidad alta; el resto son seguimientos" reprueba la
  skill.** Ese es el hábito exacto que esta skill existe para matar. Un bug medio
  aplazado es el futuro bug misterioso. Cada hallazgo del seam cuenta igual.
- **"Suficientemente bueno para aterrizar" no es un estado.** Si el seam no está
  bien, sigue iterando — quita el bloqueo, escala a un modelo o revisor más
  fuerte, reintenta — hasta que lo esté.
- **Un parche puntual junto a una primitiva compartida existente reprueba la
  skill.** Si una primitiva ya posee el seam, el fix la monta; un fix que la
  esquiva recrea la clase.
- **Un "no es un bug" adjudicado necesita evidencia,** no un voto. Registra qué
  se revisó y por qué el hallazgo no se sostiene.

## Combina bien con

- [root-cause-first](../root-cause-first/SKILL.md) — la disciplina de
  investigación detrás del paso 1.
- [red-first](../red-first/SKILL.md) — el test que falla y prueba el fix, y el
  patrón de guarda estructural para el paso 5.
- [sniper-testing](../sniper-testing/SKILL.md) — tests acotados mientras
  iteras; una pasada completa al aterrizar.
- [repair-loop](../repair-loop/SKILL.md) — el loop de punta a punta dentro del
  que corre esta disciplina.
- [incident-closure](../incident-closure/SKILL.md) — "arréglalo" significa un
  cierre completo, nunca un menú de opciones.
