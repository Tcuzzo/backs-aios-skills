---
name: "model-fusion"
description: "Úsala cuando la respuesta de un solo modelo no da suficiente confianza — un build, fix o diseño difícil donde quieres que varios modelos compitan y un juez independiente elija. Un panel redacta en paralelo, un juez fusiona al ganador, y el resultado se valida contra la intención original. Trigger words: fusion, panel, judge, multi-model, ensemble, draft and merge, builder not grader, fusión, panel de modelos, juez, multimodelo, borradores en paralelo, el que construye no califica."
license: "MIT"
---

# Model Fusion
**Effort:** heavy — un panel completo redactando en paralelo más un juez independiente (y un escritor opcional); gástalo en builds y arreglos difíciles que van a entregarse, nunca en cambios de una línea. Elimina: apostar el cambio al borrador de un solo modelo, y el retrabajo cuando ese único borrador está mal.

Muchas voces independientes ganan a una sola. Un panel de modelos redacta la
misma tarea en paralelo. Un juez — un modelo que no escribió ninguno de los
borradores — elige o fusiona al mejor. Al ganador después se le compara con lo
que de verdad se pidió.

## Cuándo correrla

- Cualquier build, fix o mejora sustancial donde la calidad importa más que la velocidad.
- Cuando quieres un par concreto de evaluadores independientes, no fe ciega en un modelo.
- NO para cambios triviales de una línea. Haz el cambio directo y verifícalo.

## Las tres etapas

### 1. Panel — borradores en paralelo

1. Manda la misma tarea, con el mismo contexto, a todos los modelos del panel a la vez.
2. Cada redactor trabaja solo. Ningún redactor ve el trabajo de otro.
3. Un redactor que falla, se queda sin tiempo o devuelve vacío se registra y se
   descarta. Nunca mata la ronda. Registra el descarte en voz alta — jamás lo
   tragues en silencio.
4. Recoge todos los candidatos no vacíos.

### 2. Juez — un externo elige y fusiona

1. Antes de juzgar, corre una compuerta mecánica barata sobre cada candidato:
   ¿aplica limpio? ¿parsea? Corre la prueba sobre una copia desechable, nunca
   sobre el árbol vivo. Los candidatos que fallan la compuerta quedan fuera antes
   de que el juez los vea.
2. Dos formas de juez — elige una por config:
   - **Síntesis:** el juez analiza cada candidato (fortalezas, defectos,
     conflictos), y luego un modelo escritor aparte compone la respuesta final a
     partir de ese análisis. Escritor y juez son roles distintos; mantenlos en
     modelos distintos cuando puedas.
   - **Selección:** el juez elige el mejor candidato único que pasó la compuerta.
     Más barato. Úsalo cuando fusionar no aporta nada.
3. Si el juez o el escritor no está disponible, degrada EN VOZ ALTA a selección
   sobre los mismos candidatos. Nunca desperdicies el panel en silencio; nunca
   finjas que hubo síntesis.
4. Si ningún candidato sobrevive la compuerta, añade el mejor error al prompt y
   vuelve a correr el panel — acotado, máximo 2 rondas de reparación. Al
   agotarse, devuelve fallo con la lista completa de errores. Nunca devuelvas un
   resultado vacío o sin efecto como éxito.

### 3. Validar — comparar al ganador con la intención

1. Relee la petición original. ¿El ganador hace lo que se pidió — todo, y nada
   que no se le pidió hacer?
2. Revisa la corrección semántica, el encaje de estilo con el código de alrededor,
   y que siga aplicando limpio.
3. La confianza baja se muestra como bandera de escalado, no se esconde. Luego
   pruébalo por la vía normal: test en rojo primero, verde, comportamiento vivo.
   Un borrador fusionado que nunca corrió es una suposición.

## La escalera

- La forma de peldaños de la fusión: un panel amplio de modelos baratos abajo,
  paneles más apretados y presupuestos de salida más cortos subiendo — un peldaño
  mal configurado falla en voz alta al cargarse.
- El formato de config, los roles-no-nombres y la resolución por sondeo vivo
  pertenecen a [fleet-ladder](../fleet-ladder/SKILL.md).

## Reglas duras — rompes una y la skill falló

- **El que construye nunca juzga.** El juez no escribió ningún candidato. El
  evaluador final es un modelo distinto (idealmente de otra familia) del que
  construyó al ganador.
- **Nada de nombres de modelos en duro** en ningún punto de llamada. Roles en el
  código, modelos en la config.
- **Nada de degradación silenciosa.** Redactores descartados, el fallback del
  juez, fallos de compuerta y agotamiento suenan todos en voz alta. Un resultado
  imposible de calificar nunca pasa por defecto.
- **Reparación acotada.** Las repeticiones del panel tienen tope duro. El
  agotamiento es un fallo en voz alta, no un loop infinito.
- **Tests en verde por sí solos no es terminado.** El ganador se prueba en
  comportamiento vivo.

## Combina bien con

- [fleet-ladder](../fleet-ladder/SKILL.md) — resuelve qué modelos están arriba antes de disparar el panel.
- [blind-tribunal](../blind-tribunal/SKILL.md) — la corte de calificación que falla-cerrado cuando el evaluador primario muere.
- [red-first](../red-first/SKILL.md) — el test en rojo que el borrador ganador debe poner en verde.
- [blind-eval](../blind-eval/SKILL.md) — la compuerta de gusto conservar-o-revertir cuando ningún test puede decidir.
