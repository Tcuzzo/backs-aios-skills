---
name: guided-steps
description: Úsala cuando una configuración necesita pasos que solo un humano puede dar — dashboards de terceros, credenciales, secretos de CI, aprovisionamiento, migraciones únicas, cutovers. Redacta un script interactivo por etapas que abre cada URL, dice qué clickear y qué copiar, captura los valores y los escribe donde corresponden. Trigger words: wizard, human-only steps, provision, credentials, dashboard setup, CI secrets, cutover. Disparadores: asistente, pasos humanos, aprovisionar, credenciales, configurar dashboard, secretos de CI.
license: MIT
---

# El asistente de pasos humanos
**Effort:** free — disciplina de autoría más un chequeo estático de sintaxis; sin llamadas a modelos. Elimina: re-explicar en cada corrida la misma ruta de clics que solo un humano puede hacer, y secretos pegados de paso en archivos rastreados.

Algunos pasos solo un humano puede darlos: clickear a través del dashboard de un
tercero, crear credenciales, aprobar una pantalla de aprovisionamiento. Son
tediosos de hacer a mano y tediosos de re-explicar cada vez. El asistente los
convierte en una corrida guiada: un script de shell interactivo por etapas que
abre cada URL, dice exactamente qué clickear y qué copiar, captura los valores y
los escribe donde corresponden.

## Cuándo usarla

- Una configuración necesita que un humano maneje una UI que ninguna API alcanza —
  dashboards, consolas, pantallas de credenciales, páginas de secretos de CI,
  migraciones únicas, cutovers.
- El camino es lo bastante largo como para que re-explicarlo cada vez duela.

Cuándo NO usarla: una API puede hacer el paso (automatízalo — un asistente es el
último recurso), o el procedimiento es de uno o dos pasos (solo díselo al humano
en palabras llanas).

## La forma

Un script, dos partes:

- **Una librería de ayuda arriba** — idéntica en todos los asistentes, jamás
  editada a mano. Provee: encabezados de etapa con progreso ("etapa 3 de 7"),
  narración con voz humana, apertura de URLs multiplataforma, entrada oculta
  para secretos, upserts idempotentes al `.env` (actualiza la clave si existe,
  añádela si no), escrituras al almacén de secretos de tu proveedor de CI, un
  paso de confirmar/pausar, y un resumen de cierre con todo lo capturado.
- **Las etapas debajo de un marcador** — la única parte que redactas. Una etapa
  por paso humano: abre la URL, di qué clickear y qué copiar, captura el valor,
  escríbelo en su destino. Fija el conteo total de etapas para que el progreso
  mostrado sea honesto.

## Proceso

1. **Alcance.** Lee el archivo de ejemplo de env, el README, la config de deploy
   y los workflows de CI. Cada secreto o variable que referencian es un valor que
   el asistente debe producir. Muéstrale al humano las etapas ordenadas y los
   valores por adelantado — confirma el plan antes de redactar.
2. **Mapea el camino de cada etapa.** Una línea por etapa: URL → acción → valor →
   destino. El humano ve el camino completo antes de empezar.
3. **Redacta.** Copia la plantilla. Escribe solo las etapas; nunca toques la
   librería. Mantén la narración en palabras llanas — la persona que corre esto
   puede no ser ingeniera.
4. **Verifica estáticamente.** Chequea la sintaxis del script (`bash -n`,
   shellcheck), hazlo ejecutable, y luego recorre cada etapa a mano: ¿cada URL es
   correcta, cada instrucción es clara, cada destino de escritura es el que toca?
   NO lo corras de punta a punta — abre navegadores y se bloquea esperando al
   humano.

## Reglas duras

- **Los secretos nunca tocan archivos rastreados.** Los valores capturados
  aterrizan en el `.env` ignorado por git o en el almacén de secretos del CI. El
  script en sí lleva solo marcadores; el humano pega los valores reales al
  ejecutar. Una clave real, un hostname real o un dato personal en el script
  redactado ES el bug.
- **Cada escritura remota es de un solo disparo y acotada.** Una escritura al
  almacén de secretos es una llamada a una API: sin loops de reintento, sin
  martillar. Falla con ruido y deja que el humano vuelva a correr la etapa.
- **Efímero por defecto.** Un asistente se construye para una corrida y se borra
  después. Commitéalo solo cuando el humano pida un camino de configuración
  repetible — y un asistente commiteado sigue llevando solo marcadores.
- **El paso de confirmación es el botón de pausa del propio humano, no una
  puerta.** Existe para que pueda revisar su trabajo — nunca para ponerle
  fricción de aprobación encima.

## Combina bien con

- [session-handoff](../session-handoff/SKILL.md) — registra qué etapas corrieron si la corrida se parte en dos.
- [human-voice](../human-voice/SKILL.md) — el registro en el que narra cada etapa.
- [bounded-loops](../bounded-loops/SKILL.md) — la regla de no martillar detrás de las escrituras remotas.

> Crédito de andamiaje: Matt Pocock, wizard (mattpocock/skills). La composición y las reglas duras de aquí son de BACKS AIOS.
