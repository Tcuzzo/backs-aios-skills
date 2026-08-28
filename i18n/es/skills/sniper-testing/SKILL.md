---
name: "sniper-testing"
description: "Úsala durante cualquier loop de fix o build, y antes de confiar en cualquier test en verde. Corre solo los tests que cubren lo que tocaste, y mata el teatro de mocks — tests que pasan mientras la capacidad está rota. Trigger words: sniper testing, scoped tests, test scope, mock theater, fake green, full suite, test bloat, tests de francotirador, tests acotados, alcance de tests, teatro de mocks, verde falso, suite completa, inflación de tests."
license: "MIT"
---

# Sniper Testing
**Effort:** free — pura disciplina, sin corridas extra; recorta el costo neto directamente al borrar las re-corridas de la suite completa durante la iteración. Elimina: la inflación de tests (corridas de la suite entera por un diff chiquito) y los verdes de teatro de mocks sobre los que construirías encima.

## Por qué existe

Dos modos de fallo queman la mayor parte del tiempo de testing. Inflación de
tests: correr la suite completa por un cambio chiquito. Teatro de mocks: tests
que pasan mientras la capacidad real está físicamente rota. Esta skill mata
ambos.

## Regla 1 — el diff define el alcance, no el optimismo

Durante el loop de iteración de fix/build, tienes prohibido correr la suite de
tests completa.

1. Corre `git diff --name-only HEAD` para ver exactamente qué archivos tocaste.
2. Mapea cada archivo tocado a los archivos de test que lo cubren directamente
   (p. ej. `src/payments/refund.py` → `tests/test_refund.py`).
3. Declara tu objetivo de test específico, y corre SOLO esos archivos
   (Python: `pytest tests/test_refund.py`;
   JS: `npx vitest run tests/refund.test.js`;
   Go: `go test ./payments/ -run TestRefund`).
4. Un test que ya pasó no se vuelve a correr, a menos que tu próximo cambio
   toque código que ese test ejercita. El diff define el alcance — no el
   optimismo, no el miedo.
5. Al aterrizar — la compuerta del commit — corre UNA pasada completa sobre la
   suite de cada módulo tocado. Esa pasada única atrapa los acoplamientos
   indirectos exactamente una vez. La velocidad de iteración y un aterrizaje
   sano son las dos partes del trabajo.

## Regla 2 — mata el teatro de mocks

Un test de capacidad debe afirmar un efecto secundario real y físico:

- "produce un video" → existe un archivo real en disco con tamaño > 0 bytes.
- "guarda memoria" → la fila se vuelve a leer desde una base de datos local real.
- "renderiza el widget" → existe un elemento DOM real en la página.

No mockees la base de datos. No mockees el sistema de archivos. No mockees los
sockets de red locales.

El único mock legal es la hoja de transporte externo pagado — la llamada HTTP a
una API de terceros con medidor. Incluso ahí, el test debe atravesar toda la
lógica real de alrededor: armar la petición, el ruteo, parsear la respuesta.
Mockea el cable, nunca el cerebro.

## Audita antes de confiar

Antes de apoyarte en cualquier test, léelo. Si es teatro de mocks — verde por
los mocks, sin ninguna afirmación física — borra el mock y reescribe el test
para que afirme un efecto secundario real. Un test que no puede fallar es peor
que ningún test: certifica una mentira, y vas a construir sobre esa mentira.

## Reglas duras (romper una sola reprueba la skill)

- Nada de correr la suite completa durante la iteración.
- Nada de declarar verde sin una afirmación de efecto secundario real.
- Ningún mock más allá de la hoja de transporte externo pagado en un test de
  capacidad.
- Nada de aterrizar sin la pasada completa única sobre los módulos tocados.

## Combina bien con

- [clean-code-gauntlet](../clean-code-gauntlet/SKILL.md) — el alcance de francotirador alimenta su primera compuerta
- [red-first](../red-first/SKILL.md) — escribe el test que falla antes del fix
- [seam-engineering](../seam-engineering/SKILL.md) — arregla la clase, luego barre con tests acotados
