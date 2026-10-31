# Design Taste

La jugada para construir cualquier UI que se vea diseñada, no generada. La UI
genérica es un bug de FLUJO DE TRABAJO, no del modelo: separa la creación del gusto
de la implementación, fija primero tokens de diseño exactos, dale ojos al agente y
pon una puerta de accesibilidad.

## Cuándo ejecutarla

Cualquier pantalla, página, componente, dashboard o entregable visual que un humano
vaya a mirar. La primera pantalla fija el estándar de todas las que siguen —
ejecuta esta jugada antes de esa primera pantalla.

## Tarea y límites compartidos

Aplica este play dentro del paquete actual de
[BACKS Build Flow](../skills/backs-build-flow/SKILL.md). Mantén un responsable
de integración, `task_mode` solicitado, revisiones base y candidata fijadas,
esencia del operador y evidencia vigente. Reutiliza cuerpos pertinentes ya cargados;
este play añade puertas de su dominio sin reiniciar la tarea.

[bounded-loops](../skills/bounded-loops/SKILL.md) controla plazo original y cupos
restantes entre reintentos, trabajadores, modelos, revisiones y traspasos.
Nunca los reinicies para un play anidado. Al agotarlos, guarda **STILL-BUILDING**
con candidato, evidencia, puertas pendientes y siguiente acción. Continúa trabajo
útil autorizado solo dentro de su cupo restante; una puerta ausente no se vuelve aprobada.

## La cadena

1. Usa intención y esencia establecidas por Build Flow para deducir el gusto
   pedido por las palabras del humano. Expresa la interpretación una vez antes de escribir.

2. [human-calibration](../skills/human-calibration/SKILL.md) — ancla esa lectura en
   el historial del humano y en referencias reales estudiadas, nunca en una
   suposición demográfica.
3. Emite PRIMERO el archivo de tokens de diseño de tres niveles, antes de cualquier
   componente — la spec completa de tokens y la lista de valores por defecto
   prohibidos están en [design-taste](../skills/design-taste/SKILL.md).
4. Construye los componentes con el archivo de tokens inyectado como restricción
   dura. Nunca metas a mano un hex crudo, un valor en píxeles o una familia
   tipográfica dentro de un componente.
5. Ejecuta el ciclo captura → crítico de [design-taste](../skills/design-taste/SKILL.md),
   resolviendo el modelo crítico en vivo por [fleet-ladder](../skills/fleet-ladder/SKILL.md).
   Cada crítica y render consume el mismo presupuesto restante; devuelve hallazgos
   al responsable actual.

6. Puntúa la rúbrica de gusto de 8 ejes según
   [design-taste](../skills/design-taste/SKILL.md).
7. Aplica la puerta DURA de accesibilidad WCAG 2.2 según
   [design-taste](../skills/design-taste/SKILL.md).
8. [clean-code-gauntlet](../skills/clean-code-gauntlet/SKILL.md) — solo código
   DETRÁS de los píxeles: resolvedores de tokens, cambios de tema, calculadores de
   contraste y reducers de estado pasan sin mutantes sobrevivientes. Una comparación
   invertida de contraste puede entregar una pantalla hermosa e inaccesible.
   El gauntlet no puntúa gusto; rúbrica y accesibilidad conservan ese papel.
   Antes del gauntlet usa [sniper-testing](../skills/sniper-testing/SKILL.md) para
   comandos reales de lint/tipos/tests según el diff agregado fijado. Declara N/A
   o ausencias honestamente. Renderiza DOM real; un render mockeado no prueba lo
   que ve el humano. Conserva RED sellado, añade tests suplementarios separados
   para nuevos huecos y mantén revisión independiente, pasada completa requerida
   de suites afectadas y prueba real del render.

## Puertas duras (propias de la jugada — las reglas duras de la skill aplican encima)

- El crítico trabaja en una sesión nueva y disjunta del autor; su modelo se resuelve en
  vivo a través de la escalera de flota; nunca un id de modelo fijado (un pin
  retirado mata en silencio al crítico entero).

## Combina bien con

- [blind-tribunal](../skills/blind-tribunal/SKILL.md) — califica el entregable completo
- [sniper-testing](../skills/sniper-testing/SKILL.md) — acota los tests de componentes

**Weight:** light a lo largo del bucle — la calibración y la pasada de captura → crítico cuestan una corrida extra cada una; el paso heavy es el gauntlet sobre el código detrás de los píxeles — se paga en cualquier pantalla que un humano de verdad va a mirar.
