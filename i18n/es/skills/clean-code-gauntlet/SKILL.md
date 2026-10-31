---
name: "clean-code-gauntlet"
description: "Úsala al endurecer o integrar cambios ejecutables que necesiten medidas de complejidad, cobertura, fuerza de regresión y revisión de diseño independiente."
license: "MIT"
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

Vincula `base_sha`, `candidate_sha`, responsable de integración y cupo restante
de [bounded-loops](../bounded-loops/SKILL.md) del paquete existente de
[Build Flow](../backs-build-flow/SKILL.md). Reutiliza evidencia aún válida;
rondas de revisión y campañas de mutación no reinician el presupuesto.

1. **Lint, tipos y comportamiento acotados en verde.** Ejecuta comandos aplicables
   del repo; consulta [sniper-testing](../sniper-testing/SKILL.md). Registra
   comprobaciones no disponibles o no aplicables sin llamarlas aprobadas. Una
   línea base roja exige parar y reparar; no mutes ni evalúes sobre rojo.
2. **CRAP bajo el umbral** con cobertura real (puerta de abajo). Si falla,
   refactoriza la función o cúbrela por completo. Nunca rebajes la barra.
3. **Mutación: ningún sobreviviente sin explicar dentro del alcance.** Uno no
   equivalente revela hueco de regresión. Añade un archivo suplementario separado;
   conserva byte a byte el contrato original sellado de [red-first](../red-first/SKILL.md).
   Refuta mutantes equivalentes con evidencia. Error de herramienta o timeout es
   inconcluso, nunca un mutante muerto.
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

Estos comandos son ejemplos, no instrucciones de instalación ni garantías de
CLI estable. Usa herramientas fijadas y flags soportados del repo. Para cambios
solo de documentación, valida enlaces, estructura, distribución y escenarios de
comportamiento; complejidad y mutación pueden no aplicar. Registra la razón sin
inventar métricas.

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
complejidad y de CRAP contra el `base_sha` fijado previo a la tarea,
con cobertura real comparable:

- **AUTHORED** — funciones que este cambio creó. Aplica la barra completa.
- **WORSENED** — funciones preexistentes que este cambio empeoró. El delta se le
  cobra a este cambio; debe volver a la línea base o mejor.
- **UNCHANGED** — deuda preexistente que el cambio nunca tocó. Repórtala,
  archívala, nunca se la cobres a este cambio — y nunca la uses de excusa para
  saltarte el guantelete.

## Reglas de mutación (acotada, nunca imprudente)

- **Nunca sobre el árbol compartido.** Muta en un checkout temporal del
  `candidate_sha` confirmado exacto. Si hay objetivos o tests sucios, guarda
  checkpoint y termina primero el candidato. Conserva trabajo ajeno en el original.
- **El costo se mide, no se supone.** Cronometra una vez la suite acotada y declara
  ETA = línea base x cantidad de mutantes ANTES del gasto. Ofrece ejecución en seco.
- **Acotada y reanudable.** Limita mutantes y minutos dentro del cupo restante.
  Una parada por presupuesto registra mutantes sin verificar y deja la puerta
  incompleta. Retoma solo con cupo restante o ampliado explícitamente.
- **Cobertura primero.** Muta solo líneas cubiertas; las no cubiertas son huecos
  que ya detectó la puerta CRAP.
- **Solo en alcance.** Muta el diff, nunca el repo completo.
- Un mutante realmente equivalente puede refutarse por escrito con evidencia,
  nunca omitirse silenciosamente.
- **¿No hay herramienta de mutación para el stack?** Registra limitación y evidencia
  sustitutiva real. Aplica la política de aceptación del repo; una puerta requerida
  sigue incompleta hasta que su responsable acepte una alternativa documentada.

## La revisión de gusto (al final, y ligera)

Las puertas deterministas van primero; gasta un modelo solo donde razonar es la
única herramienta. El revisor es un evaluador que no sea del constructor,
elegido en vivo por capacidad y disponibilidad desde la matriz de peldaños
configurada; la ejecución autora que construyó queda descalificada, igual que
cualquier sesión que haya heredado la conversación o el contexto del
constructor. El revisor trabaja en una sesión fresca y disjunta del autor
— el que construye nunca califica su propio trabajo. Juzga solo diseño
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
