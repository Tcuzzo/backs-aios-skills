# Design Taste

La jugada para construir cualquier UI que se vea diseñada, no generada. La UI
genérica es un bug de FLUJO DE TRABAJO, no del modelo: separa la creación del gusto
de la implementación, fija primero tokens de diseño exactos, dale ojos al agente y
pon una puerta de accesibilidad.

## Cuándo ejecutarla

Cualquier pantalla, página, componente, dashboard o entregable visual que un humano
vaya a mirar. La primera pantalla fija el estándar de todas las que siguen —
ejecuta esta jugada antes de esa primera pantalla.

## La cadena

1. [intent-compiler](../skills/intent-compiler/SKILL.md) — deduce QUÉ gusto piden
   las propias palabras del humano, y declara tu lectura en una línea antes de
   escribir nada.
2. [human-calibration](../skills/human-calibration/SKILL.md) — ancla esa lectura en
   el historial del humano y en referencias reales estudiadas, nunca en una
   suposición demográfica.
3. Emite PRIMERO el archivo de tokens de diseño de tres niveles, antes de cualquier
   componente — la spec completa de tokens y la lista de valores por defecto
   prohibidos están en [design-taste](../skills/design-taste/SKILL.md).
4. Construye los componentes con el archivo de tokens inyectado como restricción
   dura. Nunca metas a mano un hex crudo, un valor en píxeles o una familia
   tipográfica dentro de un componente.
5. Corre el bucle captura de pantalla → crítico según
   [design-taste](../skills/design-taste/SKILL.md), resolviendo el modelo crítico en
   vivo a través de [fleet-ladder](../skills/fleet-ladder/SKILL.md).
6. Puntúa la rúbrica de gusto de 8 ejes según
   [design-taste](../skills/design-taste/SKILL.md).
7. Aplica la puerta DURA de accesibilidad WCAG 2.2 según
   [design-taste](../skills/design-taste/SKILL.md).
8. [clean-code-gauntlet](../skills/clean-code-gauntlet/SKILL.md) — solo sobre el
   código DETRÁS de los píxeles: los resolvedores de tokens, los cambios de tema,
   los calculadores de contraste y los reducers de estado pasan con cero mutantes
   sobrevivientes. Una comparación invertida en un chequeo de contraste entrega una
   pantalla hermosa e inaccesible. El gauntlet nunca puntúa el gusto — la rúbrica y
   la puerta de accesibilidad siguen siendo los jueces visuales. Renderiza DOM real
   en los tests; un render mockeado no prueba nada sobre lo que el humano ve.

## Puertas duras (propias de la jugada — las reglas duras de la skill aplican encima)

- El crítico es una familia de modelos DISTINTA a la del constructor, resuelta en
  vivo a través de la escalera de flota — nunca un id de modelo fijado (un pin
  retirado mata en silencio al crítico entero).

## Combina bien con

- [blind-tribunal](../skills/blind-tribunal/SKILL.md) — califica el entregable completo
- [sniper-testing](../skills/sniper-testing/SKILL.md) — acota los tests de componentes
