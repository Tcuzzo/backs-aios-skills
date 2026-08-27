---
name: root-cause-first
description: Úsala frente a un bug difícil, un fallo silencioso, una cacería de regresiones o un cambio riesgoso que podría romper calladamente a un consumidor aguas abajo. Sin fixes antes de investigar — lee el error, reprodúcelo a demanda, revisa los cambios recientes, instrumenta las fronteras entre componentes, rastrea el flujo de datos hacia atrás hasta la fuente. Trigger words: debug, root cause, why is this failing, silent failure, regression, works in tests but fails live, systematic debugging, causa raíz, por qué falla esto, fallo silencioso, regresión, pasa en tests pero falla en vivo, depuración sistemática.
license: MIT
---

# Root Cause First

Sin fixes antes de investigar. Un parche hecho antes de entender el fallo arregla
la cosa equivocada, esconde el bug real y rompe algo aguas abajo. Tu producto no
es un parche — es una causa raíz probada con una sonda decisiva, y un fix probado
de no regresar nada.

Dos leyes gobiernan todo lo de abajo:

1. **Sin suposiciones — el código, los datos y el sistema vivo son la verdad;
   las notas son solo pistas.** Un comentario, un recuerdo, una conclusión
   previa, incluso tu propia última frase, es una hipótesis hasta que una sonda
   la confirme. Las palabras "todo / cada / ninguno" disparan un chequeo de tres
   puntos: el entorno, una búsqueda en todo el repo y un barrido de cada caller.
2. **Un contraejemplo verificado mata la conclusión anterior de inmediato.**
   Cuando una sonda contradice lo que creías, di en claro "me equivoqué — en
   realidad es X", y continúa desde el hecho nuevo. Nunca lo tapes.

## El loop (corre en orden; no te saltes pasos)

1. **Lee el error.** Enuncia el síntoma en una frase precisa. Lee el mensaje
   real, no lo que esperas que diga. Nombra el radio de impacto: ¿qué depende de
   la cosa que sospechas?
2. **Reproduce.** Haz que el fallo ocurra a demanda — en vivo, o en un test que
   falla. **Tómale el tiempo.** Un "fallo" que vuelve en milisegundos cuando el
   trabajo real toma segundos es una excepción tragada temprano, no trabajo real
   fallando. La brecha de tiempos es en sí misma una pista.
3. **Revisa los cambios recientes.** Haz diff de lo que cambió desde la última
   vez que funcionó — código, config, entorno, dependencias. Si la historia es
   larga, biséctala.
4. **Mapea a los consumidores.** Para un bug en una superficie compartida, lista
   cada caller y cómo la usa cada uno (¿comparación exacta de strings? ¿booleano?
   ¿lista?). La regresión real suele esconderse en una comparación exacta aguas
   abajo, no en la perilla que estás girando.
5. **Instrumenta las fronteras.** Loguea o sondea en cada costura entre
   componentes — qué entra, qué sale. Rastrea el dato malo hacia atrás, frontera
   por frontera, hasta llegar a la fuente. Arregla la fuente, nunca el síntoma.
6. **Causa raíz por hipótesis.** Forma una hipótesis falsable. Encuentra LA sonda
   decisiva que la separa de las alternativas, y corre solo esa. No dispares el
   pipeline entero "a ver qué pasa".
7. **Arregla con cirugía, en el seam correcto.** El cambio más pequeño que
   resuelve la causa raíz. Prefiere la única fuente compartida (un normalizador,
   un runner) antes que editar N puntos de llamada. Donde se pueda, haz el fix
   inerte en la ruta que funciona — que demuestre no cambiar nada ahí y solo se
   active en la rota. Sin refactors vecinos colándose.
8. **Pruébalo.** Escribe el test que falla reproduciendo el bug; míralo ponerse
   rojo; arregla; míralo ponerse verde. Luego corre los tests de cada ruta de
   consumidor que mapeaste en el paso 4 — el verde ahí es tu piso de cero
   regresiones. Una suite que mockea el seam exacto que falló no prueba nada.
9. **Verifica en vivo.** Maneja el sistema real — peticiones reales, base de
   datos real, logs reales. Nunca un script de acompañamiento que importa el
   código a tu propio proceso. Captura evidencia de antes y después.
10. **Aprende.** Anota el síntoma, la sonda decisiva, la causa raíz y el
    anti-patrón que la escondió, para que el próximo bug de esta forma salga más
    barato.

## Construye el loop de reproducción ANTES de teorizar

Si te sorprendes leyendo código para armar una teoría antes de que exista un
comando capaz de ponerse rojo — para. Sin comando capaz de rojo, no hay teoría.
Una señal apretada de pasa/falla que se pone roja con ESTE bug es la mayor
palanca de depuración que existe. Gasta un esfuerzo desproporcionado aquí.

Formas de construir uno, más o menos en orden: un test que falla; un script HTTP
contra un servidor de dev; una corrida de CLI con una entrada de fixture,
comparada con un snapshot bueno conocido; un script de navegador headless; un
payload real capturado y reproducido por la ruta de código en aislamiento; un
arnés desechable que llama a una sola función; un loop de fuzzing sobre entradas
aleatorias; un arnés de bisección para que el bisect automático funcione; un loop
diferencial (la misma entrada por la versión vieja y la nueva, diff de salidas).

Luego apriétalo: más rápido (cachea el setup, estrecha el alcance), más filoso
(afirma el síntoma específico, no "no se cayó"), determinista (fija el tiempo,
siembra el RNG, congela la red). Un loop determinista de dos segundos es un
superpoder.

Para bugs intermitentes, persigue una tasa de reproducción más alta, no una
reproducción limpia: repite el disparador 100 veces, agrega estrés, estrecha las
ventanas de tiempo. Un fallo intermitente al 50% se puede depurar; uno al 1%, no.

Si de verdad no puedes construir un loop, para y dilo. Lista lo que intentaste y
pídele a tu humano acceso, un artefacto capturado o instrumentación temporal. No
teorices sin loop. Y si no existe ningún seam que pueda replicar el patrón real
de llamada, esa ausencia ES un hallazgo — marca la brecha de arquitectura después
de que el fix aterrice.

## Anti-patrones (cómo los bugs difíciles siguen vivos)

- Concluir desde una nota o comentario sin una sonda.
- Arreglar antes de reproducir.
- Confiar en una suite verde que mockea el seam exacto que falla en vivo.
- Verificación de acompañamiento — importar el código en vez de manejar el
  sistema vivo.
- Cambiar una perilla de config sin mapear los consumidores de comparación
  exacta que alimenta.
- Refactors amplios colándose con un fix.
- Decir "todo / cada / ninguno" sin el chequeo de tres puntos.

## Combina bien con

- [red-first](../red-first/SKILL.md) — commitea el test que falla antes del fix.
- [sniper-testing](../sniper-testing/SKILL.md) — tests acotados mientras iteras.
- [seam-engineering](../seam-engineering/SKILL.md) — arregla la clase, no la instancia.
- [repair-loop](../repair-loop/SKILL.md) — el ciclo completo de arreglar y aterrizar.

> Crédito de andamiaje: Matt Pocock, diagnosing-bugs (mattpocock/skills). La composición y las reglas duras de aquí son de BACKS AIOS.
