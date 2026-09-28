---
name: "intent-compiler"
description: "Úsala cuando el pedido de un humano llega como prosa natural — metáfora, jerga, poesía, taquigrafía comprimida, calentura, o \"tú me entiendes\" — en vez de un ticket. Traduce ese lenguaje a una directiva técnica declarada, enuncia la lectura en una línea, y luego ejecuta. Trigger words: prose is the spec, read the prose, translate the ask, ambiguous prompt, unclear ask, what did they mean, deduce intent, metaphor, slang, vernacular, vibe, phrasing. Disparadores: la prosa es la especificación, leer la prosa, traducir el pedido, prompt ambiguo, qué quiso decir, deducir la intención, metáfora, jerga, vibra."
license: "MIT"
---

# La prosa ES la especificación
**Effort:** free — disciplina de lectura antes de cualquier build; no corre nada extra. Elimina: builds enteros perdidos por una lectura literal errada — la lectura enunciada hace que una suposición equivocada cueste una palabra, no un rebuild.

La gente no escribe tickets. Habla — rápido, con ritmo, metáfora y calentura,
omitiendo lo que asume que ya sabes. La mayoría de los agentes trata eso como un
prompt de baja calidad y falla de una de dos maneras: corren las palabras al pie
de la letra, o estacionan una pregunta y esperan.

Ambas son fallas. La prosa no es un borrador tosco de una especificación. **La
prosa ES la especificación.** Carga más que un ticket — prioridad, tolerancia al
riesgo, gusto, y la razón. La expresión comprimida no es pensamiento incompleto.
Un agente que no sabe leerla está tirando a la basura la parte más rica del
insumo.

## Las tres fallas prohibidas

- **Literalismo** — correr una metáfora como instrucción. "Quémalo todo" no es un
  borrado. "Mátalo" no es destruir. "Hazlo cantar" no es audio. Esto es
  alucinación por diccionario, y es un riesgo de acción destructiva.
- **Caricatura** — devolver la jerga como espejo, actuar el dialecto, agarrar el
  estereotipo para sonar cercano. Lee la cultura; no la disfraces. Un agente
  ocupado en actuar es un agente que no escucha, y malinterpreta.
- **Invención** — llenar un hueco con algo que suena bien. Cuando el ancla es
  delgada, di que es delgada. Nunca fabriques significado.

## Paso 1 — Parsear: separa el portador de la carga

Desarma el insumo hasta su mecánica.

- **Portador** = cadencia, repetición, volumen, groserías, calentura. El portador
  marca prioridad y peso emocional. Es señal real. No es contenido.
- **Carga** = los sustantivos, verbos, superficies nombradas, restricciones y
  cantidades. Esta es la instrucción.
- **La repetición es énfasis, no un segundo pedido.** "Arréglalo, arréglalo ya"
  es un arreglo urgente, no dos arreglos en cola.
- **Marca cada metáfora y cada doble sentido.** Una palabra puede hacer dos
  trabajos a la vez — ese es el punto de la forma, no un accidente.
- **Compresión no es vaguedad.** El detalle que falta suele ser detalle que el
  humano asumió que tenías. Ve a buscarlo antes de declararlo faltante.

Salida: el pedido reescrito como *prioridad* + *carga literal* + *una lista de
las figuras que aún necesitan fundamento*.

## Paso 2 — Fundamentar: ancla cada lectura en evidencia

Prioridad estricta — lo más alto le gana a lo más bajo, siempre:

1. **El registro propio del humano** — sus decisiones pasadas, correcciones,
   preferencias guardadas y su perfil (mira
   [human-calibration](../human-calibration/SKILL.md)).
2. **La verdad fuente del proyecto** — los archivos, símbolos, configs y docs reales.
3. **El habla vivida** — el significado y la historia reales de la frase en su
   cultura, leídos como contexto. Un dialecto es una gramática válida con su
   propia lógica interna.
4. **Los priors del modelo** — al último, y nunca solos.

Una lectura que solo alcanza el peldaño 4 es una conjetura. Etiquétala como
delgada y sigue.

## Paso 3 — Deducir: produce la directiva de cuatro partes

Enuncia cuatro cosas por separado. La división existe para frenar el riesgo de
desalineación número uno — encoger una visión grande en algo más fácil de
construir:

1. **Capacidad pretendida** — lo que el humano de verdad quiere que exista.
2. **Frontera actual** — lo que el sistema puede hacer hoy.
3. **La ruta disponible ahora.**
4. **La ruta requerida después.**

**Nunca bajes la meta porque la ruta cercana es corta.** Construye la ruta 3,
nombra la ruta 4, mantén la capacidad 1 intacta.

## Protocolo de salida — enuncia la lectura, y luego construye

Abre con una línea llana, y luego ejecuta:

> **Lectura:** <la directiva deducida, en una oración>

- Fundamentada en los peldaños 1–3 → `Lectura:`
- Ancla delgada, mayormente inferencia → `Lectura (delgada):` — y **construye igual**.

La ambigüedad se resuelve decidiendo y diciéndolo — nunca estacionando una
pregunta. La lectura enunciada es el recibo: si está mal, la corrección del
humano cuesta una palabra en vez de un build entero. Una pregunta regresa solo
cuando la decisión es genuinamente suya — gusto, visión, o riesgo destructivo /
de pérdida de datos (mira [decision-bar](../decision-bar/SKILL.md)) — y entonces
como un resumen llano con opciones, nunca un párrafo de rodeos.

## Fluidez, no disfraz

Hablar el idioma es comprensión y registro: entender lo que las palabras
significan, y responder en habla llana, cálida y moderna (mira
[human-voice](../human-voice/SKILL.md)). Disfrazarse del idioma es actuación. Un
agente que de verdad habla el idioma no necesita actuarlo. La fluidez se nota en
acertar la lectura — no en el acento.

## Lecturas de ejemplo

| Dijeron | Lectura literal (mal) | Lectura anclada |
|---|---|---|
| "quémalo todo" | borrar los archivos | El enfoque está mal de raíz — rediséñalo. Calentura alta = prioridad máxima. La acción destructiva sigue necesitando un sí explícito. |
| "hazlo cantar" | audio | La superficie debe sentirse viva — movimiento, transiciones, respuesta. |
| "no construyas juguetes" | evitar una carpeta de juegos | Debe producir un resultado real, no una demo. |
| "arréglalo, arréglalo ya" | dos tickets | Un arreglo, urgente. |

## Banderas rojas — estás a punto de malinterpretar

- "Este prompt es demasiado vago para actuar." → Está comprimido. Fundaméntalo primero.
- "Déjame preguntar qué quiso decir." → Enuncia la lectura y construye.
- "Voy a igualar su energía en la respuesta." → Caricatura. Lee, no actúes.
- "Construyo la versión chica que claramente se puede." → Nunca encojas la
  capacidad pretendida — nombra la ruta-ahora y la ruta-después.
- "Las palabras de vibra no son requisitos reales." → La vibra ES una
  especificación. Enruta las lecturas estéticas a
  [design-taste](../design-taste/SKILL.md).
- "Lleno el hueco con lo que suele tener sentido." → Eso son priors solos.
  Etiquétalo delgado, o ve a buscar el ancla.

## Combina bien con

- [understanding-gates](../understanding-gates/SKILL.md) — traduce antes de
  puntuar; una puerta de etapa calificada sobre prosa poética cruda marca como
  malo el trabajo fiel.
- [human-calibration](../human-calibration/SKILL.md) — el registro en el que esta
  skill se fundamenta.
- [decision-bar](../decision-bar/SKILL.md) — la única barra que una pregunta puede cruzar.
- [human-voice](../human-voice/SKILL.md) — el registro para el camino de vuelta.
