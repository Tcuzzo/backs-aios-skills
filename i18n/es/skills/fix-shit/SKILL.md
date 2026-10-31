---
name: fix-shit
description: "Úsala cuando el operador reporte comportamiento roto, diga fix shit o que dejes de ocultar errores, o pida terminar un bug persistente."
license: MIT
---

# Fix Shit

Entrada rápida a `root-cause-first` y `repair-loop` dentro de la tarea actual de
[BACKS Build Flow](../backs-build-flow/SKILL.md). Conserva su único responsable,
esencia del operador, `task_mode`, identidad del candidato y evidencia; no recargues
un paquete válido ni inicies otro ciclo de vida. Una invocación directa establece
el paquete una vez. Presupuesto restante y plazo de
[bounded-loops](../bounded-loops/SKILL.md) se aplican a cada reproducción, arreglo,
modelo alternativo y revisión. Esta skill no los reinicia ni oculta fallos.

1. Nombra el comportamiento roto del usuario y la superficie exacta donde aparece.
2. Crea una señal roja repetible desde la ruta real. Sigue la entrada y cada límite
   hasta hallar dónde divergen comportamiento real y esperado. Sella el contrato
   original con [red-first](../red-first/SKILL.md) antes de que un constructor cambie
   la costura responsable. Una tarea diagnóstica devuelve esa evidencia.
3. Identifica causa raíz y todas las llamadas a la costura rota. Conserva el error
   original en logs o estado visible; una alternativa puede proteger la app, pero
   no convertir fallo en éxito falso.
4. Para un arreglo autorizado, aplica [repair-loop](../repair-loop/SKILL.md) en el
   flujo: reparación mínima de la clase, comandos reales acotados de lint/tipos/tests
   desde el diff agregado fijado y calidad/mutación de clean-code-gauntlet. Conserva
   el original sellado; un hueco nuevo recibe test suplementario separado. Reutiliza
   etapas verificadas sin repetirlas.
5. Completa revisión requerida independiente del autor (author-disjoint), puerta de integración de
   suites afectadas y ruta real de la app para la entrega solicitada. Verifica
   resultado deseado y estado de fallo explícito. Falta de capacidad revisora es
   un hueco del entorno, nunca un pase independiente emitido por ti mismo.
6. Devuelve candidato y evidencia al responsable de integración. Informa PROVEN
   solo con revisión requerida y evidencia real de entrega; de lo contrario guarda
   STILL-BUILDING con el bloqueo rojo exacto y siguiente acción. Agotar presupuesto
   conserva trabajo y límites; continúa trabajo útil desbloqueado solo dentro del
   cupo restante.

Si el error es intermitente, captura tiempos y una tasa de reproducción acotada;
no deduzcas la causa de una sola repetición verde. Para ambigüedad de ubicación,
empieza por `building-with-backs` y su comprobación de destino.

## Evidencia y revisión independiente

Para ejecutables distribuidos, paquetes o comportamiento solicitado de runtime,
invoca [rea-investigation](../rea-investigation/SKILL.md) y la skill independiente
`reverse-engineer-anything` cuando su análisis sea útil; usa un proveedor Ghidra
existente para objetivos nativos compatibles. No trates evidencia estática como
comportamiento vivo ni instales proveedores ausentes silenciosamente. Para adoptar
una capacidad open source, invoca [absorb](../absorb/SKILL.md). Usa
[fleet-ladder](../fleet-ladder/SKILL.md) para enrutar por rol y capacidad, sin fijar
modelos. Si se requiere tribunal, sigue [blind-tribunal](../blind-tribunal/SKILL.md):
una ejecución nueva separada del autor revisa un paquete congelado sin datos de
autoría. Informa resolutores, revisores o evidencia ausentes como huecos del entorno.
