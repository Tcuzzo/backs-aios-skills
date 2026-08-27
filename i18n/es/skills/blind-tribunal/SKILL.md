---
name: blind-tribunal
description: Úsala cuando un cambio autónomo necesita una calificación independiente antes de aterrizar y no hay humano en el circuito. Convoca jurados ciegos de familias distintas — una lente cada uno — sobre un sobre con archivos completos y autoría borrada; cada hallazgo se vuelve un nuevo test que falla; se repite hasta que todos los jurados aprueban. Trigger words: blind tribunal, grill tribunal, tribunal, jurors, cross-family grade, convene, blind grade, independent grade, grade before landing. Disparadores: tribunal ciego, jurados, calificación entre familias, convocar, calificar a ciegas, calificación independiente, calificar antes de aterrizar.
license: MIT
---

# Blind Tribunal
**Effort:** heavy — tres modelos jurados de familias distintas, reconvocados con sobres frescos en cada ronda hasta la unanimidad; gástalo en cambios autónomos que aterrizan sin revisión humana. Elimina: aterrizajes rebeldes sin más puerta que la palabra del propio constructor.

El loop de calificación que deja al humano irse sin que el agente se descarrile.
Un panel de jurados revisa el cambio a ciegas, con la autoría borrada. Cada
hallazgo se convierte en un nuevo test que falla. El loop se repite hasta que
todos los jurados aprueban. Nada aterriza solo con la palabra del constructor.

## Cuándo ejecutarla

- Antes de aterrizar cualquier cambio autónomo que ningún humano va a revisar.
- Cualquier cambio de alto radio de impacto: con forma de seguridad, que toca datos, cercano a la autoridad.
- Cuando un solo evaluador no basta y quieres lentes independientes sobre el mismo artefacto.

## Los asientos

Tres jurados. Cada uno es un modelo de una familia DISTINTA a la del constructor.
Cada uno sostiene exactamente UNA lente — un jurado al que le piden revisar todo
no revisa nada bien.

| Jurado | Lente | La pregunta que hace |
| --- | --- | --- |
| Defecto | caza de defectos | ¿Qué se rompe de verdad? Escapes, casos borde, contratos rotos. |
| Proporción | tamaño justo | ¿Es este el tamaño correcto? ¿Sobreconstruido, o un parche sobre un síntoma? |
| Consecuencia | impacto humano | Si esto está mal, ¿qué le pasa a la persona que depende de ello? |

**Equipo solo.** Cuando solo hay una familia de modelos disponible, degrada
EXPLÍCITAMENTE: un contexto o sesión fresca que nunca vio la conversación del
autor actúa como evaluador ciego, o el humano revisa el sobre con la autoría
borrada. El reporte debe nombrar la puerta debilitada — "calificado a ciegas
misma-familia, no entre familias" — nunca fingir en silencio que la puerta entre
familias se sostuvo.

## El sobre

Los jurados nunca ven el repo, al constructor ni la conversación. Ven un solo sobre:

- **Archivos actuales completos** de cada archivo que el cambio tocó, más sus
  archivos de test. Nunca fragmentos de diff sueltos — un fragmento esconde el
  contrato que lo rodea e induce hallazgos falsos.
- **El contrato de revisión**: la intención del cambio en una línea, y los
  criterios para aprobar.
- **Cero autoría.** Sin nombres, sin ids de modelos, sin autores de commits, sin
  historial de chat. Si la identidad se filtra, el armado del sobre falla con
  ruido — nunca se califica sin la venda.
- **Nada de prosa sobre el comportamiento viejo.** Describir lo que el código
  "hacía antes" siembra defectos fantasma. Los archivos hablan solos.

## El veredicto

JSON estricto y parseable por máquina, un solo objeto, sin prosa:

```json
{"verdict": "pass" | "refuse",
 "findings": [{"severity": "blocker|major|minor|info",
               "claim": "...", "evidence": "..."}]}
```

- Un jurado que RESPONDIÓ mal — basura, texto que no es JSON, texto de rechazo —
  cuenta como **refuse**; un jurado que NUNCA respondió (falla de transporte,
  inalcanzable) es una **espera**: vuelve a sentarlo vía
  [fleet-ladder](../fleet-ladder/SKILL.md), nunca un pase silencioso. Un solo
  disparo por jurado que responde por ronda — sin reintentos.
- Un pase pelado con cero hallazgos y sin evidencia es un **voto de poca
  información**. Cuenta, pero nunca como la única prueba — dos pases pelados no
  le ganan a un refuse detallado. Un pase fuerte nombra lo que revisó.

## El loop

1. Rojo primero: haz commit del test de contrato que falla ANTES de construir el
   arreglo, y registra ese commit. El constructor no puede tocar el test
   ([red-first](../red-first/SKILL.md)).
2. Construye hasta el verde.
3. Arma el sobre con los archivos ACTUALES.
4. Sienta a los tres jurados — de familias distintas a la del constructor
   ([fleet-ladder](../fleet-ladder/SKILL.md) resuelve cuáles están vivos).
5. Cada jurado además verifica, no solo lee: los tests nuevos pasan; la suite de
   regresión no está peor que la línea base; y un chequeo de verde falso — un test
   que DEBERÍA fallar (el bug reintroducido) de verdad falla. Un verde falso es un
   refuse.
6. Ante cualquier refuse: CADA hallazgo — blocker, major y minor — se convierte en
   un NUEVO test que falla por la razón real del hallazgo. Arréglalo. Rearma el
   sobre con los archivos revisados. Vuelve a convocar a TODOS los jurados. Un
   veredicto sobre archivos viejos no es veredicto.
7. Aterriza solo con pase unánime. Los hallazgos minor levantados en la ronda
   final también se cierran, nunca se difieren — "arreglé los blockers, los minor
   después" es exactamente la fuga que esta skill existe para frenar. Un hallazgo
   termina ARREGLADO o refutado con evidencia registrada, nunca estacionado.

## Reglas duras — romper una anula la calificación

- El constructor nunca califica su propio trabajo: ni la misma instancia, ni la misma familia.
- **Un refuse de jurado vale lo que vale el sobre.** Antes de escribir un test a
  partir de un hallazgo, verifica el hallazgo contra los archivos reales. Un
  hallazgo sobre código que el sobre nunca llevó significa arreglar el sobre, no
  el código.
- Mide la convergencia sobre los hallazgos NUEVOS por ronda, no sobre el total
  bruto. Hallazgos nuevos planos o creciendo dos rondas seguidas: detente y
  escala al humano. Nunca muelas en vano.
- Nunca debilites ni edites los tests que fallan para alcanzar un pase. Los
  jurados verifican que los archivos de test siguen sin cambios desde el commit
  rojo.
- Un pase unánime abre la puerta; no es la meta. Aterriza, y luego prueba la
  capacidad en vivo sobre la superficie real. Verde sin prueba en vivo no es
  estar terminado.

## Combina bien con

- [red-first](../red-first/SKILL.md) — el contrato que falla, commiteado antes de que corra el constructor.
- [sniper-testing](../sniper-testing/SKILL.md) — efectos reales, corridas acotadas, sin teatro de mocks.
- [seam-engineering](../seam-engineering/SKILL.md) — arregla la clase, barre a los hermanos, aterriza una guarda.
- [repair-loop](../repair-loop/SKILL.md) — el loop de construcción que este tribunal califica.
- [blind-eval](../blind-eval/SKILL.md) — la puerta más ligera de conservar-o-revertir cuando la pregunta es de gusto, no de defectos.

> Crédito de andamiaje: Matt Pocock, grill-me / grilling (mattpocock/skills, MIT).
> El diseño del tribunal adversarial ciego entre familias es de BACKS AIOS.
