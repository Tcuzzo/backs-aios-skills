---
name: live-research
description: Úsala al razonar sobre un código, una API o un sistema cuya forma real importa. Lanza un agente de investigación en paralelo que lee la verdad viva — los README del proyecto, los docs de cada sección, el código fuente real — para que las conclusiones se anclen en lo que de verdad hay, no en la memoria del modelo. Trigger words: live research, ground the reasoning, read the real source, check what is actually there, primary sources, background research, verify against the repo, what do the docs say, investigación viva, ancla el razonamiento, lee la fuente real, revisa lo que hay de verdad, fuentes primarias, verifica contra el repo, qué dicen los docs.
license: MIT
---

# Live Research
**Effort:** light — un agente de investigación en segundo plano leyendo la fuente viva mientras el carril principal sigue trabajando. Elimina: conclusiones montadas sobre la memoria del modelo que el repo real luego refuta — el retrabajo de entregar una suposición.

La memoria del modelo es una suposición de cómo se veía un proyecto cuando lo
entrenaron. La verdad viva es lo que está en disco y en los docs oficiales ahora
mismo. Esta skill corre ambos carriles a la vez: mientras el carril principal
razona sobre un objetivo, un agente de investigación lee la cosa real, y sus
hallazgos se funden en el razonamiento **antes** de sacar cualquier conclusión.

## Cuándo correrla

- Estás por razonar sobre la estructura de un proyecto, el contrato de una API o
  el comportamiento de una librería — y no has leído el código fuente actual.
- Un diseño, un fix o una afirmación depende de hechos que pudieron cambiar desde
  tus datos de entrenamiento.
- Una pregunta necesita hechos del mundo real que el contexto de trabajo no puede
  responder solo.

## Los pasos

1. **Lanza al investigador en paralelo.** En el momento en que arranca el
   razonamiento sobre un objetivo, despacha un agente de investigación en segundo
   plano hacia ese mismo objetivo. El carril principal sigue trabajando; el
   investigador lee. Nunca frenes el trabajo por una vuelta que un agente puede
   dar solo.
2. **Lee la verdad viva, lo más cercano primero.** El README del propio proyecto,
   luego los docs de la sección más cercana al objetivo, luego la estructura real
   del código: listado real de directorios, contenido real de archivos, firmas
   reales. Para hechos fuera del proyecto: docs oficiales, código fuente, specs,
   APIs de primera mano. Un blog que resume los docs no es fuente primaria.
3. **Devuelve hallazgos antes de las conclusiones.** Los hallazgos fluyen al
   carril principal según van cayendo, y el razonamiento los incorpora y corrige
   el rumbo. Una conclusión sacada antes de que el investigador reporte sobre ese
   punto es una suposición — márcala como tal hasta que la verdad viva la
   confirme o la mate.
4. **Ancla cada afirmación a la fuente que la posee.** Cada hallazgo lleva su
   fuente en línea: una ruta de archivo, una línea citada, un enlace, un commit.
   Una afirmación que no se puede anclar se marca como no verificada, en voz
   alta — nunca disfrazada de hecho.
5. **Escribe un solo archivo con citas.** Los hallazgos aterrizan en un único
   archivo Markdown, cada afirmación con su fuente. Guárdalo donde el proyecto ya
   guarda notas así; si no hay convención, elige un lugar sensato y di cuál, para
   que el próximo agente lo encuentre.
6. **Recuerda antes de releer.** Revisa primero las notas de sesiones anteriores
   — puede que la misma fuente ya esté consultada. Reutiliza el hallazgo en caché
   y cita la misma fuente. Minutos de memoria ganan a horas de redescubrimiento.

## Reglas duras

- **Ninguna conclusión antes de la fusión.** Si el investigador no ha reportado
  sobre un punto, el carril principal no puede darlo por cerrado.
- **Solo fuentes primarias.** Sigue cada afirmación hasta la fuente que la posee.
  Un resumen de segunda mano es un puntero, no una prueba.
- **Sin cabeza, nunca observado.** La investigación de fondo usa una ruta de
  descarga headless (sin navegador visible) — jamás un navegador en vivo que un
  humano esté mirando; ese es otro carril.
- **Lo no verificable se dice.** Un hallazgo sin fuente primaria sale marcado,
  nunca mezclado en silencio con el resto.
- **Cero fricción humana.** Esta skill no agrega ningún paso de aprobación ni
  ninguna compuerta. Es disciplina de método, no un punto de control.

## Qué vuelve

Un archivo Markdown anclado y con citas — más un carril de razonamiento corregido
en pleno vuelo, en vez de después de que la conclusión ya salió. El carril
principal lee el archivo y avanza.

## Combina bien con

- [wayfinder](../wayfinder/SKILL.md) — los tickets de investigación son el tipo agente-solo que esta skill resuelve.
- [root-cause-first](../root-cause-first/SKILL.md) — la misma disciplina de fuente-primero, apuntada a bugs.

> Crédito de andamiaje: Matt Pocock, research (mattpocock/skills, MIT). La composición y las reglas duras de aquí son de BACKS AIOS.
