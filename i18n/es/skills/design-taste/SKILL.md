---
name: design-taste
description: Úsala antes de construir cualquier cosa visual — un sitio, una app, un dashboard, una consola o una presentación — para que salga con gusto de verdad en vez de los defaults genéricos de la IA. Trigger words: design, UI, taste, design tokens, design system, accessibility, WCAG, screenshot critique, dark mode, restyle. Disparadores: diseño, interfaz, gusto, tokens de diseño, sistema de diseño, accesibilidad, crítica de captura, modo oscuro, rediseñar.
license: MIT
---

# Design Taste — Tokens primero, ojos puestos, accesibilidad dura
**Effort:** light — un archivo de tokens antes de cualquier componente, más una pasada captura de pantalla → crítico de visión por cada superficie renderizada. Elimina: volver a entregar los defaults genéricos de la IA — el retrabajo de reestilizar y el parche de accesibilidad después del envío.

La UI genérica es un bug de flujo de trabajo, no un bug del modelo. Arréglalo de
forma estructural: lee el brief como una especificación, fija tokens de diseño
exactos antes de cualquier componente, prohíbe los defaults por su nombre, dale
ojos al constructor con un loop de capturas de pantalla, y pon una puerta de
accesibilidad — dura.

## Cuándo ejecutarla

- Cualquier pedido de "constrúyeme un / diséñame un…" que renderice píxeles.
- Antes de armar el esqueleto de un frontend o un entregable de cara al cliente.
- Cuando una superficie existente se ve genérica y necesita una dirección específica y defendible.

## Pasos

1. **Lee el brief como especificación.** Una metáfora, una cadencia, una época, un
   artista o un lugar nombrado en las palabras del humano es una restricción de
   diseño concreta, no decoración. La disciplina completa de leer el brief:
   [intent-compiler](../intent-compiler/SKILL.md).
2. **Elige una dirección con fundamento.** Escoge una referencia *líder* (un
   sistema de diseño o librería real que fija la base estructural) y una
   referencia de *acento* (una que estampa su firma encima). Ambas deben ser
   reales y actuales, con una firma de gusto verificable. Una vibra inventada
   reprueba la puerta, cerrada.
3. **Emite los tokens PRIMERO.** Antes de cualquier componente, escribe un archivo
   de tokens de diseño legible por máquina, de tres niveles (primitivo → semántico
   → componente; formato de tokens del W3C, `$value` + `$type`). Fija de entrada:
   una rampa de color perceptualmente pareja (Oklch — un espacio de color donde
   pasos iguales se ven iguales), una escala tipográfica real sobre una tipografía
   que no sea la de siempre, un solo incremento de espaciado (base 4px →
   4/8/12/16/24/32/48/64), una escala de radios, una escala de elevación, y
   tokens de movimiento con nombre (duración + easing por entrada / scroll /
   cambio de estado; respeta `prefers-reduced-motion`). Oscuro y claro son de
   primera clase y ambos se resuelven desde los MISMOS tokens semánticos.
4. **Prohíbe los defaults genéricos por su nombre.** Las prohibiciones le ganan a
   los adjetivos: nada de tipografía por reflejo (Inter/Roboto), nada de
   degradados morados, nada de hero centrado, nada de fila de tres tarjetas
   iguales, nada de bloque gris sobre blanco. Agrega tu propia lista prohibida
   por proyecto.
5. **Construye bajo restricción.** Los componentes consumen tokens y nada más. Un
   hex, un px o una familia tipográfica en crudo dentro de un componente es un
   defecto.
6. **Cierra el loop captura → crítico con visión.** Para todo lo renderizado:
   renderízalo en un navegador headless en anchos móvil y escritorio, toma
   capturas, y haz que un modelo con visión lo puntúe — luego arregla, en pasadas
   separadas (crítica → arreglo estructural → auditoría → pulido), nunca de un
   solo tiro. El crítico es un evaluador: usa un modelo de una familia distinta a
   la del constructor, puntuando ejes con nombre, nunca un puntaje holístico
   único. Resuelve el modelo crítico desde la config al momento de llamar — un id
   de modelo clavado se retira algún día y se lleva el loop entero con él.
7. **Puntúa la rúbrica de gusto de 8 ejes.** 0–3 por eje, y cada eje debe puntuar
   ≥ 2: adhesión a tokens · layout/jerarquía · tipografía · color/contraste ·
   movimiento · paridad oscuro-claro · accesibilidad · el chequeo visceral
   diseñado-vs-promedio ("¿esto se ve diseñado, o como el promedio de todo?").
   Un eje bajo 2 = no está listo.
8. **Aplica la puerta DURA de accesibilidad (WCAG 2.2).** Objetivos de puntero
   ≥ 24×24 px CSS. Indicador de foco visible de ≥ 2px de perímetro con contraste
   ≥ 3:1. Contraste de texto ≥ 4.5:1 en texto normal, ≥ 3:1 en texto grande y
   componentes de UI. Navegable por completo con teclado. Contraste verificado en
   AMBOS temas. Esto es una puerta, no una sugerencia: falla = no se publica.
9. **Prueba el código detrás de los píxeles.** Los resolutores de tokens, los
   cambios de tema, los calculadores de contraste y los reductores de estado
   reciben tests reales sobre DOM renderizado de verdad — una comparación
   invertida en un chequeo de contraste publica una pantalla hermosa que es
   silenciosamente inaccesible. Los tests juzgan el código; la rúbrica y la
   puerta WCAG juzgan el gusto.

## Reglas duras — cualquiera de estas reprueba la skill

- Un componente escrito antes de que exista el archivo de tokens.
- Un hex / px / familia tipográfica en crudo dentro de un componente.
- Cualquier ítem de la lista de defaults prohibidos apareciendo en el resultado.
- Saltarse el loop captura → crítico para algo renderizado.
- El constructor calificando sus propios visuales, o un solo puntaje holístico en vez de ejes.
- Cualquier eje de la rúbrica bajo 2, o cualquier chequeo WCAG 2.2 fallando, al momento de publicar.
- Una dirección de gusto que no puede fundamentarse en una referencia real y verificable.

## Combina bien con

- [intent-compiler](../intent-compiler/SKILL.md) — la disciplina completa de leer el brief.
- [blind-eval](../blind-eval/SKILL.md) — conservar-o-revertir cuando la pregunta es de gusto.
- [clean-code-gauntlet](../clean-code-gauntlet/SKILL.md) — endurecer el código detrás de los píxeles.
- [blind-tribunal](../blind-tribunal/SKILL.md) — calificación entre familias antes de aterrizar.

> Crédito de andamiaje: W3C Design Tokens Community Group (formato de tokens);
> WCAG 2.2, W3C (puerta de accesibilidad); UICrit, UIST 2024 (crítica de UI
> puntuada por ejes); AI Jason, & JackJack. (2025). superdesign: AI design agent
> [Computer software]. GitHub. https://github.com/superdesigndev/superdesign
> (AGPL-3.0; dual-licensed with a commercial enterprise license) — la idea de
> prohibir los defaults. La composición y las reglas duras de aquí son de BACKS
> AIOS.
