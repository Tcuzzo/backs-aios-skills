---
name: "repo-map"
description: "Úsala en la primera sesión dentro de un repo frío sin índice y cada vez que el mapa quede viejo. Recorre el árbol una sola vez, escribe un CODE_MAP.md en la raíz y hace que toda sesión posterior lea primero el mapa — mapa primero, árbol crudo solo cuando el mapa no tenga la respuesta. Trigger words: repo map, code map, map first, map-first, index the repo, cold repo, stale map, refresh the map, mapa del repo, mapa de código, indexa el repo, actualiza el mapa."
license: "MIT"
---

# Repo Map
**Effort:** light — un recorrido la primera vez, casi gratis después. Elimina: agentes que vuelven a derivar la forma del repo en cada sesión — el mayor impuesto de latencia y tokens en un repo sin índice.

Un código indexado responde gratis “dónde vive X”. La mayoría de los repos no tiene
índice, así que cada sesión paga el mismo impuesto: recorrer el árbol, redescubrir la
estructura y olvidarlo todo al cerrar. Esta skill paga una vez. Recorre el árbol una
vez, escribe lo aprendido en un solo mapa y hace que cada pregunta posterior lea el
mapa antes de caminar.

## Cuándo correrla

- En la primera sesión sobre un repo frío — sin mapa ni índice.
- Cada vez que el mapa quede viejo (ver la regla de vigencia abajo).

## Los pasos

1. **Recorre el árbol una vez.** Una pasada por la estructura real: directorios,
   puntos de entrada y dónde vive cada cosa. Debería ser el único recorrido completo
   que el repo necesite.
2. **Escribe un `CODE_MAP.md` en la raíz del repo.** Lleva:
   - los puntos de entrada — dónde comienza la ejecución;
   - las secciones y costuras, cada una con una línea de propósito;
   - dónde viven los tests;
   - los comandos de build, ejecución y test;
   - las rutas calientes — sembradas desde el historial (frecuencia de
     `git log --name-only`), o vacías para que sesiones posteriores las completen.
3. **Mantenlo ligero.** Es un mapa, no documentación. Una línea por hecho. Si una
   entrada crece hasta ser párrafo, se está volviendo doc — córtala a un puntero.
4. **Registra la forma del árbol.** Guarda en el mapa una huella barata,
   `git ls-files | sha256sum` (detecta altas, movimientos y renombres), para que una
   sesión posterior sepa si la forma cambió.

## La ley de mapa primero

Investigación, orientación y plays leen el mapa ANTES de recorrer el árbol. El
recorrido crudo es el fallback cuando el mapa no responde — y todo lo que enseñe ese
recorrido se escribe DENTRO del mapa antes de seguir. El mapa absorbe cada caminata.
La re-derivación se paga una vez, nunca por sesión.

## La regla de vigencia

Actualiza el mapa solo cuando cambie la forma del árbol — archivos agregados, movidos
o renombrados desde el estado registrado. Compara la huella guardada
(`git ls-files | sha256sum`) con el árbol vivo. Nunca actualices por calendario.
Nunca en cada sesión. Un mapa reconstruido por horario es el impuesto por sesión con
otro nombre.

## Reglas duras

- **Hechos y ubicaciones, nunca opiniones.** “Auth vive en `src/auth/`” pertenece
  al mapa; “el código de auth es un desastre” no.
- **Un puntero muerto muere al encontrarlo.** Una ruta que ya no resuelve se arregla
  o se corta al instante. Un mapa que miente es peor que no tener mapa.
- **El mapa nunca carga secretos.** Nada de keys, tokens, credenciales ni hostnames
  privados. Es un archivo trackeado; trátalo como tal.

## Combina bien con

- [live-research](../live-research/SKILL.md) — el investigador lee primero el mapa y luego la fuente.
- [wayfinder](../wayfinder/SKILL.md) — la orientación empieza desde el mapa, no desde un recorrido frío.
- [session-handoff](../session-handoff/SKILL.md) — el mapa es la pieza del handoff que comparten todas las sesiones.
