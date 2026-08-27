---
name: bounded-loops
description: Úsala antes de arrancar cualquier loop que pueda reintentar, hacer polling, iterar o llamar a una API externa — loops de agente, loops de reparación, schedulers, watchers. Declara techos de presupuesto, hace checkpoint al agotarse, y vuelve estructuralmente imposible martillar a un proveedor. Trigger words: bounded loop, budget, ceiling, retry, backoff, rate limit, throttle, kill-switch, checkpoint, runaway, infinite loop, spin, budget exhaustion. Disparadores: loop acotado, presupuesto, techo, reintento, límite de tasa, loop infinito, desbocado, agotamiento de presupuesto.
license: MIT
---

# Bounded Loops

Un loop sin límites es el bug más caro que un agente puede publicar. Quema
presupuesto, martilla a los proveedores hasta que te bloquean, y esconde su propio
fracaso dentro del giro. Cada loop recibe un techo, un checkpoint y una forma
ruidosa de morir — antes de arrancar.

## Cuándo ejecutarla

Antes de arrancar cualquier loop: un loop de reparación, un envoltorio de
reintentos, un poller, un scheduler, una corrida autónoma de varios pasos,
cualquier cosa que pueda re-emitir una llamada o reintentar un paso.

## Los pasos

1. **Declara el presupuesto primero.** Tokens, costo, tiempo de reloj y máximo de
   intentos — por escrito antes de la primera iteración. Un loop sin presupuesto
   declarado es ilimitado por definición y no arranca.
2. **Ponle tope a las rondas internas.** Un episodio interno (un ciclo LLM/
   herramienta sobre un problema) recibe un techo fijo y chico de rondas
   (alrededor de 4). El techo acota el episodio, no la misión — el trabajo sin
   terminar sube de nivel, no se queda moliendo.
3. **Checkpoint en cada iteración.** Estado durable en disco — manifiesto de la
   corrida, log de evidencia, paso actual — nunca la memoria del chat. Cualquiera
   (incluida una sesión fresca) puede retomar desde el último checkpoint.
4. **Al agotarse: checkpoint, y luego escala.** Entrega el checkpoint al loop
   externo o a tu humano con lo que se hizo, lo que falta y el bloqueo. Nunca
   sigas en silencio pasado un presupuesto. Tampoco te detengas en silencio — el
   agotamiento es ruidoso.
5. **Respeta cada API externa.** Antes de la primera llamada, aprende el límite de
   tasa y la cuota del proveedor; cuando no se conocen, trátalos como estrictos —
   una llamada, espaciado amplio — hasta medirlos. Ponle throttle a cada llamada,
   cachea y reutiliza respuestas, y sostén un techo duro por ventana.
6. **Retrocede exponencialmente ante el rechazo.** Un 429 o un 503 significa
   espera, y luego espera más. Cero reintentos instantáneos contra el mismo
   endpoint. Un reintento apretado contra un endpoint es como muere una ruta que
   funcionaba: quema cuota y puede hacer que bloqueen toda tu dirección de salida.
7. **Lleva un kill-switch ruidoso y acotado.** Todo loop que pueda re-emitir una
   llamada tiene un conteo máximo de intentos; cuando lo alcanza, el loop se
   detiene CON RUIDO y con la evidencia — nunca un giro infinito o silencioso.
8. **Detente y encola solo en puntos seguros.** Detenerse significa checkpoint y
   luego cancelar. El trabajo nuevo se encola para el siguiente punto seguro (una
   frontera de estado entre pasos) — nunca inyectado a mitad de un paso. Una sola
   instancia del loop, un solo escritor, escrituras de estado atómicas.

## Reglas duras (lo que reprueba esta skill)

- Un loop que arranca sin presupuesto declarado de tokens / costo / tiempo / intentos.
- Seguir pasado un presupuesto agotado, en silencio o no, sin escalar.
- Un reintento instantáneo contra el mismo endpoint, o cualquier ruta de reintento sin backoff.
- Un loop de reintentos sin tope de intentos, o un tope que falla calladito al alcanzarse.
- Estado de progreso guardado solo en la memoria de la conversación — un crash borra la corrida.
- Dos instancias del loop escribiendo el mismo estado, o escrituras de estado no atómicas.
- Escapar del loop debilitando sus propios chequeos de salida — un verde producido
  bajando la barra, borrando datos o tragándose errores es un verde falso, no una
  salida.

## Combina bien con

- [optimus](../optimus/SKILL.md) — carga el piso antes de que arranque cualquier loop.
- [repair-loop](../repair-loop/SKILL.md) — el consumidor principal de estos techos.
- [fleet-ladder](../fleet-ladder/SKILL.md) — fallback acotado entre modelos, no martillar a uno.
- [session-handoff](../session-handoff/SKILL.md) — aquello en lo que un checkpoint se convierte al escalar.
