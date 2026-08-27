---
name: clean-code-gauntlet
description: Úsala al endurecer o aterrizar cualquier build — un agente, un servicio, una librería — cuando quieres una barra de calidad determinista en vez de una revisión línea por línea. Corre tests francotirador, el puntaje CRAP (complejidad x cobertura) y mutation testing acotado, y luego una revisión ligera de gusto. Trigger words: clean code, gauntlet, unc, uncle bob, crap score, crap, mutation testing, harden, complexity, coverage, quality bar. Disparadores: código limpio, guantelete, puntaje crap, pruebas de mutación, endurecer, complejidad, cobertura, barra de calidad.
license: MIT
---

# Clean Code Gauntlet
**Effort:** heavy — cómputo real: corridas de cobertura y complejidad más una pasada de mutación acotada, y luego un solo modelo de gusto; gástalo en cambios que van a entregarse. Elimina: la revisión humana línea por línea de diffs enteros, y los tests de verde falso tras los que se esconde una regresión.

## Por qué existe

El código desordenado hace que los agentes den bandazos, y las reglas enterradas
en un prompt largo se desvanecen a mitad de contexto — los chequeos deterministas
nunca se desvanecen. Así que corre Clean Code como un **guantelete que el código
debe pasar**, no como prosa que el modelo debe recordar.

**Mide, no revises.** Pon la puerta sobre números que una herramienta calcula:
cobertura, complejidad ciclomática (un conteo de caminos independientes a través
de una función), tamaño de módulo, mutantes muertos. Humanos y modelos auditan
muestras — nunca diffs completos.

## La cadena (corre en orden; cada etapa se detiene con ruido al fallar)

1. **Tests francotirador en verde.** Corre solo los archivos de test que cubren lo
   que el diff tocó — mira [sniper-testing](../sniper-testing/SKILL.md). Una línea
   base en rojo significa parar y arreglar; nunca mutes ni califiques sobre rojo.
2. **CRAP bajo el umbral** con datos de cobertura reales (mira la puerta abajo).
   ¿Se rompe? → refactoriza la función hacia abajo, o cúbrela por completo. Nunca
   bajes la barra.
3. **Mutation testing: cero sobrevivientes dentro del alcance.** Un sobreviviente
   condena a los TESTS, no al código — refuerza el test que debió atraparlo.
4. **Revisión ligera de gusto** — un modelo juzga solo lo que los números no pueden.

## Herramientas que lo calculan

| Stack | Herramientas |
| --- | --- |
| Python | coverage.py + radon + mutmut |
| JS/TS | c8 (o istanbul) + Stryker |
| Go | go test -cover + gocyclo + go-mutesting |
| Rust | cargo-tarpaulin + cargo-mutants |
| Java | JaCoCo + PIT |
| Otro | cualquier % de cobertura + cualquier contador de complejidad ciclomática |

Una forma de comando por etapa:
- Cobertura: `coverage run -m pytest <sniper files> && coverage report` (JS/TS: `npx c8 vitest run <files>`)
- Complejidad: `radon cc -s <changed files>`
- Mutación: `mutmut run --paths-to-mutate <changed files>` (JS/TS: `npx stryker run --mutate "<glob>"`)

## La puerta CRAP

```
CRAP(m) = comp(m)^2 * (1 - cov(m)/100)^3 + comp(m)
```

- Con 100% de cobertura el puntaje colapsa a la complejidad misma.
- 30 es la línea clásica de "crappy" (complejidad 5 con cero cobertura la alcanza).
- Los humanos sostienen más o menos 4–5 de complejidad por función. Un agente
  puede cargar 6–8 SOLO con cobertura casi al 100% — la cobertura paga esa
  holgura.
- Una función con CRAP alto tiene exactamente dos salidas: refactorizarla hacia
  abajo, o cubrirla por completo. **Nunca bajes el umbral para pasar.**

## De quién es la deuda — AUTHORED / WORSENED / UNCHANGED

Un puntaje absoluto esconde de quién es la deuda. Divide cada delta de
complejidad y de CRAP contra la línea base previa al cambio:

- **AUTHORED** — funciones que este cambio creó. Aplica la barra completa.
- **WORSENED** — funciones preexistentes que este cambio empeoró. El delta se le
  cobra a este cambio; debe volver a la línea base o mejor.
- **UNCHANGED** — deuda preexistente que el cambio nunca tocó. Repórtala,
  archívala, nunca se la cobres a este cambio — y nunca la uses de excusa para
  saltarte el guantelete.

## Reglas de mutación (acotada, nunca imprudente)

- **Nunca sobre el árbol de trabajo compartido.** Muta en un checkout temporal
  cortado desde el HEAD commiteado. ¿Archivos objetivo o de test sucios? =
  rechaza; commit primero.
- **El costo se mide, nunca se asume.** Cronometra la suite acotada una vez,
  reporta ETA = línea base x cantidad de mutantes ANTES de gastar nada. Ofrece
  una corrida en seco.
- **Acotada y reanudable.** Ponle tope a los mutantes y a los minutos. Una parada
  por presupuesto es una pausa con checkpoint, no un fracaso — reanuda para
  terminar.
- **Cobertura primero.** Muta solo líneas cubiertas; una línea sin cubrir es un
  hueco de cobertura que la puerta CRAP ya atrapó.
- **Solo dentro del alcance.** Muta lo que el diff tocó, nunca el repo entero.
- Un mutante genuinamente equivalente puede refutarse en vez de matarse — con la
  refutación por escrito, nunca saltada en silencio.
- **¿No existe herramienta de mutación para tu stack?** Déjalo registrado en el
  reporte de aterrizaje y apóyate en la puerta CRAP — nunca lo saltes en silencio.

## La revisión de gusto (al final, y ligera)

Las puertas deterministas van primero; gasta un modelo solo donde razonar es la
única herramienta. El revisor es un modelo de una familia distinta a la del
constructor — el que construye nunca califica su propio trabajo. Juzga solo diseño
y gusto: nombres, responsabilidades mezcladas, ancho de interfaz, y los seis
olores — rigidez, fragilidad, inmovilidad, complejidad innecesaria, repetición
innecesaria, opacidad. La aritmética ya la resolvieron las puertas.

El piso de oficio que la revisión sostiene: funciones pequeñas, que hacen una sola
cosa, con pocos argumentos, sin argumentos bandera, con nombres honestos; módulos
profundos — una interfaz pequeña que esconde lógica real; tests rápidos,
independientes, repetibles, con un solo comportamiento verificado cada uno.

## Reglas duras (romper cualquiera reprueba la skill)

- Nunca bajes un umbral ni debilites el set de mutantes para forzar un pase.
- Nunca mutes el árbol de trabajo compartido; nunca corras sin límites.
- Nunca le cobres deuda UNCHANGED al cambio actual.
- Un test que no puede fallar es teatro — el mutation testing es cómo pruebas
  qué tests son reales.
- Di el costo real — el tiempo de máquina es barato, las regresiones no. Nunca
  finjas un verde para ahorrarte la hora.

## Combina bien con

- [sniper-testing](../sniper-testing/SKILL.md) — elige el alcance de tests para la etapa 1
- [red-first](../red-first/SKILL.md) — el contrato que falla y precede a cualquier build
- [blind-eval](../blind-eval/SKILL.md) — conservar-o-revertir cuando la pregunta es de gusto
- [blind-tribunal](../blind-tribunal/SKILL.md) — un veredicto calificado más completo antes de aterrizar

> Crédito de andamiaje: Robert C. Martin, *Clean Code* (2008); Alberto Savoia &
> Bob Evans, la métrica CRAP (2007); John Ousterhout, módulos profundos
> (*A Philosophy of Software Design*, 2018); Pocock, M., & Martin, R. C.
> (2026, Aug 19). LIVE: Uncle Bob on Software Fundamentals in the Age of AI
> [Video]. YouTube. https://www.youtube.com/watch?v=zcLPGC-tvgk — fuente de la
> banda CRAP para agentes y de la mutación cobertura-primero. La composición y
> las reglas duras de aquí son de BACKS AIOS.
