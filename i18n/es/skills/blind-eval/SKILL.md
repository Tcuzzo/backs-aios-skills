---
name: blind-eval
description: Úsala antes de aterrizar cualquier cambio donde la pregunta es de gusto o de calidad y un test no puede decidirla. Juzga el cambio por sus méritos con la autoría oculta, y luego lo conserva o lo revierte — un empate revierte; solo aterriza la mejora probada. Trigger words: blind eval, karpathy, keep or revert, quality gate, taste call, blind judge, A/B judge, prove uplift. Disparadores: evaluación ciega, conservar o revertir, puerta de calidad, juicio a ciegas, juez A/B, probar la mejora.
license: MIT
---

# Blind Eval

Una puerta de calidad de conservar-o-revertir para decisiones que un test no puede
tomar — la calidad de una prosa, el copy de una UI, la legibilidad de un refactor,
la salida de un prompt, la sensación de un diseño. Juzga el cambio por sus méritos
con la autoría oculta, y luego CONSÉRVALO o REVIÉRTELO. Un empate revierte. Solo
aterriza la mejora probada.

## Cuándo ejecutarla

- Antes de aterrizar cualquier cambio donde "¿es mejor?" es una pregunta de gusto o calidad.
- Como la puerta dentro de un loop de mejora: proponer → probar → medir → conservar o descartar.
- Cada vez que el autor sienta la tentación de declarar su propio trabajo una mejora.

## El método

1. **Escribe qué significa "mejor" ANTES de mirar.** Una meta en lenguaje llano.
   Una medida primaria o un eje de rúbrica con una barra dura — un nivel que
   superar, no un número que empujar. Ejes secundarios en orden de prioridad
   (costo, longitud, latencia).
2. **Congela ambas versiones.** La base y la candidata, como artefactos reales —
   nunca una descripción de ellos.
3. **Quita la autoría.** Etiquétalas A y B, baraja el orden, elimina cada nombre,
   id de modelo y el razonamiento del autor. El juez ve solo los artefactos y la
   rúbrica.
4. **Sienta un juez que no escribió ninguna de las dos** — un modelo de otra
   familia, o un humano. El autor nunca califica su propio trabajo.
5. **Juzga por méritos.** Puntúa cada eje de la rúbrica. Cita evidencia del
   artefacto para cada puntaje — un veredicto sin evidencia es una corazonada.
6. **CONSERVA solo si la candidata supera la barra Y le gana estrictamente a la
   base.** Un empate no es mejora — revierte.
7. **Revierte limpio.** Restaura el árbol byte a byte idéntico al estado previo al
   cambio (una rama de trabajo o un stash lo dejan en un solo comando). Registra el
   veredicto en ambos casos.

## Reglas que frenan las trampas

- **La barra se revisa primero, y los ejes se ordenan por prioridad.** Una
  regresión en un eje de mayor prioridad es fatal aunque todos los ejes menores
  mejoren. Y superar la barra con margen extra no compra nada — no puedes
  sobrepasar el eje primario para "pagar" una regresión de costo.
- **Nunca bajes la barra después de ver el resultado.** Arreglar el puntaje
  debilitando la evaluación está prohibido. Mantén la rúbrica y la evaluación
  fuera de los archivos que el cambio tiene permitido tocar.
- **Nada de autocalificarse.** El juez nunca ve la justificación del autor — un
  juez que lee el discurso de venta califica el discurso, no el trabajo.
- **Quítale el ruido a un juez estocástico.** Las lecturas ciegas varían de
  corrida en corrida, y los jueces prefieren la primera opción que ven. Corre cada
  comparación varias veces con el orden barajado y toma el voto de la mayoría — el
  barajado mata el sesgo de posición y las repeticiones matan el ruido, en un solo
  movimiento. Si la mejora real es más chica que la oscilación del juez entre
  corridas, la puerta no distingue señal de suerte — agrega lecturas o elige una
  medida más estable.
- **¿Equipo solo?** ¿No hay una segunda familia de modelos disponible? Una sesión
  ciega fresca que nunca vio la conversación del autor juzga — y el reporte nombra
  la puerta debilitada ("juzgado a ciegas misma-familia, no entre familias").
- **¿Sin barra confiable? Usa dominancia.** Cuando el nivel de la base es
  desconocido o ruidoso, suelta la barra absoluta y conserva solo lo que le gana
  estrictamente al campeón actual. Una regresión nunca puede dominar, así que no
  hace falta piso.
- **Nunca puntúes un eje de costo sobre fracasos.** "Menos pasos" calculado sobre
  intentos fallidos premia rendirse rápido. Calcula costo y esfuerzo solo sobre
  los éxitos.

## Quítale el sesgo al juez

El piso de mecánica del juez. Estas reglas viven aquí y en ningún otro lado:

- **Suite reservada.** Califica sobre una suite que queda FUERA del alcance de
  escritura del constructor — el constructor nunca ve los tests que califican, así
  que no puede programar a la medida de ellos.
- **Limpieza a commit fresco.** Deja el workspace en un solo commit fresco y
  bloquea el egreso de red antes de una corrida calificada, para que un pase sea
  DERIVADO — no recuperado del historial de git ni del arreglo de otro.
- **Normaliza por longitud.** Los jueces prefieren con fuerza la respuesta más
  larga — corrige por longitud antes de comparar puntajes.
- **Criterios reservados rotados.** Usa una rúbrica de ejes nombrados con
  respuestas sí/no y criterios ocultos que rotan entre corridas. Un puntaje
  holístico visible se termina jugando con teatro de citas.
- **Califica el estado final.** Califica el trabajo de varios pasos sobre el
  estado FINAL, no sobre cada paso intermedio.
- **Calibra al juez.** Calibra al juez con un set chico etiquetado por humanos —
  reporta sus tasas de verdaderos positivos y verdaderos negativos — antes de
  confiarle tu dominio.

El barajado del orden es parte de la regla de quitar ruido de arriba — una ley,
dicha una sola vez.

## La variante en loop

La misma puerta alimenta un loop de mejora autónomo: proponer un cambio chico →
correr un experimento corto → medir a ciegas → conservar si es mejor, revertir si
no → repetir, con un presupuesto fijo de rondas. Aliméntale al proponente las
trazas de fracaso de la ronda anterior, no solo la meta — un proponente que no ve
por qué falla edita a ciegas. Incluso un loop que no conserva nada paga su costo:
las trazas que junta apuntan a bugs concretos y arreglables que ningún puntaje
agregado revela.

## Combina bien con

- [blind-tribunal](../blind-tribunal/SKILL.md) — el panel de jurados más pesado cuando la pregunta son defectos, no gusto.
- [red-first](../red-first/SKILL.md) — cuando un test SÍ puede decidirlo, escribe el test.
- [clean-code-gauntlet](../clean-code-gauntlet/SKILL.md) — puertas medidas de calidad de código para acompañar la decisión de gusto.

> Crédito del nombre: Andrej Karpathy. Inspiración del nombre; la disciplina de
> conservar-o-revertir tiene un paralelo independiente en el autoresearch de
> Karpathy (2026, github.com/karpathy/autoresearch, MIT). El aspecto ciego
> (autoría oculta) y la composición y reglas duras de aquí son de BACKS AIOS.
