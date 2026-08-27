# Jugada: Security & Delivery

La puerta de salida para cualquier cosa que un cliente u otra máquina vaya a correr.
Segura por construcción: el harness la impone; nunca se confía en que el modelo lo
recuerde.

## Cuándo ejecutarla

- Un repo, agente o app está por entregarse, publicarse o desplegarse.
- Un agente con herramientas toca contenido no confiable — páginas web, issues,
  correo, input.
- Estás agregando dependencias o CI a algo que se entrega.

La puerta de salida, de un vistazo:

```
+--------------------------------------------+
| 1 secret gate  verified-only scan; one     |
|   live credential fails the build          |
+--------------------------------------------+
| 2 egress lockdown  deny by default;        |
|   canonicalize before allowlist match      |
+--------------------------------------------+
| 3 break the lethal trifecta  one leg       |
|   always missing on every path             |
+--------------------------------------------+
| 4 taint tracking  tainted session =>       |
|   policy-gate every exfil-capable action   |
+--------------------------------------------+
| 5 supply chain  hash-pin every dep, no     |
|   install scripts, SHA-pinned CI           |
+--------------------------------------------+
| 6 clean-code-gauntlet  mutate detectors,   |<--------------------------+
|   parsers, predicates to zero survivors    |  a survivor or a          |
+--------------------------------------------+  sandbox catch ->         |
| 7 sniper-testing  mock outbound network    |   +---------------------+ |
|   only, never payload or parser            |   |  LORD OF THE LOOP   |-+
+--------------------------------------------+   | one hand drives the |
| 8 sandbox before ship  outbound blocked,   |-->| loop: dispatch,     |
|   watch writes + calls, hard-kill armed    |   | judge, loop back    |
+--------------------------------------------+   | until the gate is   |
| 9 provenance  SBOM + signed provenance;    |   | green. a lane never |
|   still review the source                  |   | lands its own work. |
+--------------------------------------------+   +---------------------+
          |
          | every gate green
          v
+--------------------------------------------+
| LANDING GATE -- all green or no ship:      |
| no live credential anywhere . no path      |
| holds all three trifecta legs . deps +     |
| CI hash-pinned . zero surviving mutants    |
| . sandboxed before ship                    |
+--------------------------------------------+
```

En el diagrama: **Lord of the Loop** = el dueño del bucle, la mano que conduce la iteración — despacha, juzga y vuelve a iterar — hasta que la puerta de aterrizaje está en verde; **LAND / LANDING GATE** = aterrizar — integrar el cambio solo cuando todo está en verde.

## La cadena

1. Puerta de secretos — corre un escáner de secretos en modo solo-verificados
   (chequea cada credencial candidata contra el proveedor en vivo). Una credencial
   confirmada viva hace fallar el build. Sin excepción.
2. Cierre de egreso — deniega la salida por defecto; enruta todo por un proxy con
   allowlist de hostnames pelados. Canonicaliza y valida el hostname ANTES de
   comparar: rechaza bytes nulos, trucos de porcentaje y CRLF. El bypass del byte
   nulo `evil-host\x00.trusted.com` es real y ya llegó a producción.
3. Rompe la trifecta letal — diseña cada ruta de ejecución para que al menos UNA de
   estas tres falte siempre: acceso a datos privados, exposición a contenido no
   confiable, comunicación externa. No puedes bloquear del todo la inyección de
   prompts; sí puedes lograr que no pueda robar.
4. Rastreo de contaminación — ingerir contenido no confiable marca la sesión como
   contaminada. Mientras esté contaminada, ponle puerta de política a cada acción
   capaz de exfiltrar (HTTP saliente, correo, creación de PRs) en el harness —
   nunca lo dejes al juicio del modelo.
5. Cadena de suministro — fija cada dependencia por hash y bloquea los scripts de
   instalación. Fija cada acción de CI a un hash de commit completo, no a un tag.
6. [clean-code-gauntlet](../skills/clean-code-gauntlet/SKILL.md) — el código de
   seguridad lleva la vara más estricta. Corre testing de mutación sobre cada
   detector, parser y predicado de política, y lleva los mutantes sobrevivientes a
   cero. Una comparación invertida dentro de un chequeo de amenazas que la suite
   igual pasa ES la vulnerabilidad.
7. [sniper-testing](../skills/sniper-testing/SKILL.md) — mockea SOLO la red
   saliente, nunca el payload ni el parser bajo prueba: un detector mockeado es un
   sensor ciego en producción.
8. Sandbox antes de entregar — corre el artefacto construido en un sandbox efímero
   con toda la salida bloqueada y un corte duro de recursos armado. Mira qué escribe
   y qué intenta llamar.
9. Procedencia — emite un inventario de software (SBOM), más procedencia firmada si
   la tienes. Y aun así revisa la fuente: la procedencia también firma con fidelidad
   una fuente maliciosa.

## Protecciones permanentes durante cualquier corrida de build

- Denegar escritura en rutas sensibles: archivos de arranque del shell, config y
  hooks de git, config de DNS, llaves SSH.
- Herramientas con privilegio mínimo. Un paso de confirmación se reserva SOLO para
  operaciones genuinamente destructivas o irreversibles — pérdida de datos, gasto,
  una acción externa irreversible. Nunca le pongas puerta a una capacidad benigna, y
  nunca a tu humano.

## Puertas duras — cualquiera hace fallar la jugada

- Una credencial confirmada viva en cualquier parte del entregable o de su historia.
- Cualquier ruta de ejecución que sostenga las tres patas de la trifecta a la vez.
- Una dependencia sin fijar, un script de instalación o una acción de CI fijada a un
  tag.
- Un mutante sobreviviente en un detector, parser o predicado de política.
- El artefacto nunca corrió en un sandbox antes de la entrega.

**Weight:** mayormente disciplina free de construcción más pasadas light de escáner y sandbox; el paso heavy es la mutación sobre cada detector y cada predicado de política — se paga en cualquier cosa que un cliente u otra máquina va a correr.
