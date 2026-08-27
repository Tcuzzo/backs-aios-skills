---
name: human-calibration
description: Úsala cuando arranca un build, un diseño o una decisión de UX con consecuencias y primero debes conocer al humano al que sirve. Carga o construye un perfil de sesión de cómo piensa, decide y quiere que le hablen este humano, y luego conduce todo el build a través de él. Trigger words: yoke, know your human, human profile, session profile, grounding ladder, interaction model, intent. Disparadores: conoce a tu humano, perfil humano, perfil de sesión, escalera de fundamento, modelo de interacción, intención.
license: MIT
---

# Conoce a tu humano
**Effort:** light — una sola pasada de perfil: carga el perfil guardado, o constrúyelo con a lo sumo 7 preguntas casuales. Elimina: re-interrogar a un humano que ya respondió, y el retrabajo de builds que malinterpretaron su gusto.

Un build que malinterpreta a su humano está mal antes de escribir la primera
línea. Esta skill reemplaza la adivinanza con un modelo funcional del humano al
que sirve: patrón de pensamiento, gusto, registro, y dónde su palabra se confía
sin más. Encuentra al humano donde está — nunca lo obligues a subir al nivel del
sistema.

## Cuándo ejecutarla

Al arranque de cualquier build, diseño, mejora o decisión de UX con
consecuencias. No es decoración de chat.

## El flujo: perfil o entrevista

1. **Identifica al humano.** Revisa `.agent/profiles/<human>.md` en el proyecto,
   y luego el directorio de config del agente en el home (p. ej.
   `~/.claude/profiles/<human>.md`) para un perfil de todos-los-proyectos. Si ahí
   existe un perfil validado, cárgalo y aplícalo. Nunca vuelvas a entrevistar a
   un humano que ya tiene uno.
2. **¿Sin perfil? Corre el protocolo de preguntas** (abajo). Hasta 7 preguntas
   casuales, más como máximo 3 repreguntas donde una respuesta abra un hilo.
   Siempre opcionales — a un humano que esquiva una se le perfila desde el
   comportamiento observado. Nunca una puerta sobre el trabajo.
3. **Sintetiza un perfil de sesión** (plantilla abajo). Cada campo lleva un
   `source` y un `status`. Una sección sin evidencia queda vacía: vacío es
   honesto, adivinado es una inferencia escondida.
4. **Reconcilia la meta.** Reformula la intención del build a través del perfil,
   en el propio registro del humano — un párrafo llano, no una especificación. Él
   confirma o corrige. Su corrección es final.
5. **Re-promptéate.** Antes de ejecutar, reescribe tu prompt de trabajo a través
   del perfil: qué quiso decir, qué afirmaciones confiar, cuáles necesitan un
   chequeo sutil, qué le va a sentir vivo y qué le va a sentir una falta de
   respeto.
6. **Construye con el perfil como mano que guía** — las decisiones de diseño,
   ingeniería, UX y gusto se conducen todas a través de él.
7. **Aprende.** Las elecciones, rechazos y correcciones observadas actualizan el
   perfil — guardado de vuelta en `.agent/profiles/<human>.md` (o el directorio
   de config del home para un perfil de todos-los-proyectos). La corrección gana,
   al instante.

## La escalera de fundamento (orden de prioridad, absoluto)

```
CORRECCIÓN DEL HUMANO
  > COMPORTAMIENTO REPETIDO OBSERVADO
  > ARQUETIPO DECLARADO   (lo que dice que es)
  > PATRÓN CULTURAL       (lo que ese arquetipo declarado suele implicar)
  > CONJETURA DEL MODELO
```

Ningún peldaño inferior anula jamás a uno superior. Los arquetipos y patrones
culturales son contexto para conducir, nunca una caja — el comportamiento
observado y la corrección los superan.

## El protocolo de preguntas

Reglas de diseño: no hace falta ningún título para responder. Verdadero/falso
casual y esto-o-aquello. De una en una, esparcidas por la conversación sobre la
meta — nunca disparadas como lista, nunca puntuadas, nunca repetidas. Captura la
fraseología propia del humano; importa tanto como la respuesta.

Las 7 preguntas centrales (cada una lee dos o más ejes a la vez):
1. Aparato nuevo: ¿lees primero cómo funciona, o te pones a apretar botones?
   → estilo de procesamiento, comodidad con el riesgo.
2. Verdadero/falso: los bugs feos te molestan más que los lentos. → prioridad de
   gusto (estético vs mecánico).
3. Un amigo llega tarde: ¿texto rápido, o una llamada con la historia completa?
   → registro (comprimido vs narrativo).
4. Construyendo una casa del árbol: ¿te imaginas la cosa terminada, o la primera
   tabla? → pensamiento de cuadro completo vs por pasos.
5. Verdadero/falso: las reglas sin sentido igual deben seguirse. → aceptación vs
   desafío del marco.
6. ¿Tres buenas opciones, o una recomendación fuerte que puedes vetar?
   → preferencia de autoridad — fija directamente cómo presentas decisiones.
7. Critican su trabajo: ¿defiende, arregla, o pregunta qué harían ellos?
   → estilo de corrección — fija cómo entregas hallazgos duros.

Repreguntas (máximo 3, solo donde una respuesta central abra un hilo): el
instinto confiado en todo o solo donde son buenos (mapa de confianza); "¿lo
suficientemente bueno es suficiente?" (sesgo de publicación); libertad de
cambiarlo-después vs certeza de funciona-hoy (gusto por la reversibilidad);
¿sigue siendo suyo después de que otro lo edita? (propiedad); "¿qué malinterpreta
la gente de tu forma de trabajar?" (ancla de identidad, en sus palabras).

## La regla de confianza

El perfil mapea dónde el juicio de este humano es fuerte y dónde es débil.
- **Área fuerte + afirmación confiada → confía.** Sin re-derivar, sin dudar, sin
  explicarle lo básico de vuelta.
- **Área débil + afirmación vaga → un chequeo sutil.** Haz una pregunta casual
  que resuelva la ambigüedad, u ofrece tu interpretación para una confirmación de
  una palabra. Nunca lo desafíes de frente; nunca sustituyas en silencio tu
  propio plan.
- **Nunca uses el perfil para limitar lo que el humano puede intentar.** Afina
  CÓMO escuchas, nunca SI obedeces.

## Plantilla del perfil de sesión (compacta)

```markdown
# PERFIL DE SESIÓN — <human>
## Anclas de identidad  # valor + source (declared|observed|cultural|guess) + status (confirmed|working|needs-validation|rejected)
## Patrón de trabajo    # un párrafo: cómo se combinan las anclas para ESTE humano
## Rasgos de conducción # "tiende a: <comportamiento>" → "así que yo: <regla concreta del agente>"
## Mapa de confianza    # áreas fuertes (confiar sin más) / áreas débiles (un chequeo sutil)
## Tensión central      # necesidades ambas-a-la-vez que parecen contradictorias pero son requisitos
## Riesgo de desalineación # la malinterpretación más probable, dicha como prohibición
## Registro             # fecha, peldaño de la escalera, cambio, evidencia
```

Un perfil de sesión vive en su sesión: en una sesión nueva es dato, no verdad,
hasta que el humano lo re-confirma o el comportamiento lo vuelve a ganar. El
perfil es propiedad del humano: muéstralo si lo pide, corrígelo en el momento en
que diga que está mal, y nunca actúes sobre una inferencia que él no puede ver —
eso es una puerta escondida.

## Reglas duras (cualquiera de estas reprueba la skill)

- Volver a entrevistar a un humano que ya tiene un perfil validado.
- Hacer que las preguntas se sientan como un examen, o hacerlas obligatorias.
- Un campo adivinado disfrazado de confirmado.
- Un peldaño inferior de la escalera anulando a uno superior.
- Usar el perfil para limitar lo que el humano tiene permitido intentar.
- Bajar la meta porque una ruta está incompleta. Separa: capacidad pretendida →
  frontera actual → ruta disponible ahora → ruta necesaria después.

## Combina bien con

- [human-voice](../human-voice/SKILL.md) — el registro en que responder una vez que el perfil dice cómo escucha.
- [decision-bar](../decision-bar/SKILL.md) — qué decisiones llegan al humano; el perfil moldea cómo llegan.
- [intent-compiler](../intent-compiler/SKILL.md) — el prompt del humano es la especificación; el perfil te dice qué quiso decir.
- [model-fusion](../model-fusion/SKILL.md) — síntesis del perfil por panel-y-compresión.
