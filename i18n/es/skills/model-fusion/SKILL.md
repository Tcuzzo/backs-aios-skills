---
name: "model-fusion"
description: "Úsala cuando comparar enfoques elaborados de forma independiente ayude a la tarea y quepa en el presupuesto restante, o cuando el operador pida un panel. Borradores, selección o síntesis y verificación independientes del modelo; un mismo modelo configurado puede cubrir roles separados en sesiones aisladas."
license: "MIT"
---

# Model Fusion
**Effort:** heavy — borradores independientes, un evaluador y un escritor opcional; usa el panel cuando su utilidad para la tarea justifique el costo dentro del presupuesto restante.

El panel es opcional. Ejecuciones separadas elaboran la misma tarea; un evaluador
que no participó en esas ejecuciones selecciona o combina candidatos. El resultado
se verifica contra la petición original. El mismo modelo configurado y capaz puede
redactar, evaluar y escribir mediante sesiones separadas y aisladas. No hace falta
cambiar de modelo ni proveedor. El evaluador no hereda la conversación ni el
contexto de trabajo de los autores.

## Cuándo correrla

- Cuando comparar enfoques pueda resolver una incertidumbre concreta y su
  evaluación quepa en el presupuesto restante de la misión.
- Cuando el operador pida un panel; declara roles disponibles y límites.
  Una tarea grande por sí sola no exige un panel.
- Para cambios sencillos, aplica el cambio directo y la verificación pertinente.

Vincula [bounded-loops](../bounded-loops/SKILL.md). Borradores, juez, escritor y
rondas de reparación comparten plazo, intentos restantes y recursos de la misión
actual. Nuevos roles o sesiones no reinician esos límites. Ejecuta los borradores
independientes en paralelo si el host lo permite; si no, de forma secuencial dentro
de los mismos límites. No inventes aislamiento de sesiones que el host no ofrece.

## Las tres etapas

### 1. Panel — borradores independientes

1. Da la misma tarea y el mismo paquete de contexto a cada sesión aislada de redacción.
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
     conflictos), y luego una ejecución de escritura separada compone la
     respuesta final a partir de ese análisis. Conserva roles y sesiones separados;
     el mismo modelo configurado y capaz puede cubrir ambos.
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

- Elige tamaño del panel y roles según capacidades necesarias, disponibilidad
  real, configuración vigente y presupuesto restante. No fijes modelos, preferencias
  de proveedor ni diversidad obligatoria. Declara huecos de configuración.
- El formato de config, los roles-no-nombres y la resolución por sondeo vivo
  pertenecen a [fleet-ladder](../fleet-ladder/SKILL.md).

## Reglas duras — rompes una y la skill falló

- **El que construye nunca juzga.** La ejecución evaluadora no redactó candidatos
  ni heredó la conversación o el contexto de trabajo de sus autores. El evaluador
  final trabaja en una sesión nueva y disjunta del autor.
- **Nada de nombres de modelos en duro** en ningún punto de llamada. Roles en el
  código, modelos en la config.
- **Nada de degradación silenciosa.** Redactores descartados, el fallback del
  juez, fallos de compuerta y agotamiento suenan todos en voz alta. Un resultado
  imposible de calificar nunca pasa por defecto.
- **Reparación acotada.** Las repeticiones tienen tope duro y consumen el
  presupuesto restante de la misión; se respeta el límite que se alcance primero.
  El agotamiento deja un checkpoint visible, nunca un loop infinito.
- **Tests en verde por sí solos no es terminado.** El ganador se prueba en
  comportamiento vivo.

## Combina bien con

- [fleet-ladder](../fleet-ladder/SKILL.md) — resuelve qué modelos están arriba antes de disparar el panel.
- [blind-tribunal](../blind-tribunal/SKILL.md) — la corte de calificación que falla-cerrado cuando el evaluador primario muere.
- [red-first](../red-first/SKILL.md) — el test en rojo que el borrador ganador debe poner en verde.
- [blind-eval](../blind-eval/SKILL.md) — la compuerta de gusto conservar-o-revertir cuando ningún test puede decidir.
