---
name: gpu-dispatch
description: Úsala al despachar modelos locales a GPUs — programar trabajo de inferencia, elegir una tarjeta o gestionar la residencia de modelos. Un modelo por GPU, sin desborde a la RAM del sistema, mantén el calor durante el loop, descarga al final del loop, admite por verdad medida. Trigger words: gpu, vram, gpu dispatch, model loading, keep alive, resident model, local inference, spill, warm. Disparadores: gpu, vram, despacho de gpu, carga de modelo, modelo residente, inferencia local, desborde, tarjeta caliente.
license: MIT
---

# La ley del despacho de GPU

Cuatro reglas para correr modelos locales en GPUs. Existen porque los dos modos de
fallo comunes son opuestos e igual de caros: reventar las tarjetas con cargas y
desbordes, y sobre-cercar el hardware hasta dejarlo ocioso. Ambos son capacidad
perdida. Impón estas reglas en el despachador como código — nunca como una regla
que un modelo deba recordar.

## Cuándo ejecutarla

- Antes de despachar cualquier trabajo de inferencia a una GPU local.
- Al diseñar o revisar un despachador, un scheduler o un enrutador de modelos.
- Cuando una corrida local está misteriosamente lenta, o una tarjeta está misteriosamente "no disponible".

## Las cuatro reglas

1. **Un modelo residente por tarjeta, a la vez.** Antes de cualquier despacho, lee
   el estado vivo de modelos cargados del nodo desde la propia API del runtime. Si
   hay otro modelo residente, úsalo o descárgalo primero. Nunca cargues un segundo
   modelo a su lado.
2. **Sin desborde a la RAM del sistema — aborta, no corras lento.** Verifica que
   el modelo cabe entero en la VRAM libre de la tarjeta antes del despacho, y
   asegura que se mantiene por completo en VRAM durante el trabajo. Cualquier
   desborde hacia la RAM del sistema es un ABORTO, no una corrida degradada — un
   modelo desbordado es calladamente 10 veces más lento y envenena cada trabajo
   que viene detrás. Un modelo que no cabe por encima del piso reservado de la
   tarjeta no se despacha a esa tarjeta; elige un modelo más chico u otra tarjeta.
3. **Mantén la tarjeta caliente durante todo el loop de trabajo.** Sostén el
   modelo residente con un keep-alive acotado — un piso y un techo que tú
   configuras, nunca ilimitado — y refréscalo mientras el loop corre. Nada de
   arranques en frío entre trabajos del mismo loop.
4. **Descarga solo cuando el loop termina.** Liberación explícita al final del
   loop — no después de cada trabajo. Descargar por trabajo es arranque en frío
   repetido; no descargar nunca es una fuga. La liberación al final del loop es
   la costura.

## Admisión por verdad medida

Si una tarjeta puede tomar trabajo se decide por medición viva, nunca por suposición:

- Un **sondeo real** del nodo — no una nota vieja de "inalcanzable" en una config.
- **VRAM libre real** por encima del piso reservado de la tarjeta — el piso es el
  único límite vigente; todo lo que está encima es libre de usar.
- Un **chequeo real de procesos corriendo** para cargas interactivas. Un juego en
  vivo, un stream o una sesión de edición sobre la tarjeta gana al instante —
  pero su presencia se mide, nunca se asume desde un archivo marcador ni desde
  una lista "fría" clavada en el código.

Los defaults que fallan cerrado, las negaciones por "propósito desconocido" y los
archivos marcadores cuya ausencia significa "cerca puesta" son todos el mismo bug:
el runtime negándole al humano el hardware que le pertenece. Sobre-cercar hardware
propio es capacidad perdida, y la capacidad perdida es un defecto. Solo la palabra
viva del humano pone o levanta una cerca.

## Reglas duras (lo que reprueba esta skill)

- Cargar un segundo modelo en una tarjeta que ya tiene uno residente.
- Continuar una corrida después de detectar desborde de VRAM en vez de abortar.
- Un keep-alive sin límite, o descargar entre trabajos dentro de un mismo loop.
- Negar una tarjeta por una nota de config, un archivo marcador o una suposición
  en vez de un sondeo vivo.
- Imponer cualquiera de estas reglas por prompt en vez de en el código del despachador.

## Combina bien con

- [invariant-floor](../invariant-floor/SKILL.md) — la verdad medida y las fallas
  ruidosas son leyes del piso; esta skill las aplica a las GPUs.
- [fleet-ladder](../fleet-ladder/SKILL.md) — resuelve qué modelo despachar antes
  de decidir dónde corre.
- [bounded-loops](../bounded-loops/SKILL.md) — el loop de trabajo al que el
  keep-alive y la liberación de final de loop están atados.
