---
name: sniper-testing
description: "Úsala durante un ciclo de construcción o reparación, o antes de confiar en un resultado verde, cuando la verificación deba cubrir el candidato real sin repetir innecesariamente toda la suite."
license: MIT
---

# Sniper Testing

Verifica el comportamiento modificado a través de su consumidor real. Elige
comprobaciones con el diff completo de la tarea; después repite solo las afectadas
por el siguiente cambio. Hereda el mismo cupo de misión de
[bounded-loops](../bounded-loops/SKILL.md).

## 1. Fija el alcance real

Conserva el `base_sha` verificado anterior a la tarea y el `candidate_sha`
confirmado actual en el paquete de [Build Flow](../backs-build-flow/SKILL.md).
Un árbol limpio tras confirmar RED y la reparación sigue teniendo un diff de
tarea. Usar solo `git diff HEAD` lo pierde.

Usa la herramienta de alcance de solo lectura incluida, desde el directorio
resuelto de esta skill:

```bash
python scripts/changed_files.py --repo <verified-repo> --base <base-sha> --candidate <candidate-sha>
```

Durante la iteración añade `--include-worktree` solo si el candidato es HEAD.
Informa por separado rutas confirmadas, preparadas, sin preparar y sin seguimiento,
conservando nombres inusuales. El alcance agregado incluye borrados y ambos lados
de un renombrado. Marca como preservado el trabajo pendiente ajeno; no te atribuyas
todas las rutas devueltas. Base ausente o revisión inválida es un error que resolver,
nunca un alcance vacío que justifique omitir comprobaciones. La herramienta no
descarga ni modifica el historial.

## 2. Elige y ejecuta comprobaciones reales

Relaciona archivos cambiados y llamadas/consumidores afectados con tests de
comportamiento; lee scripts, CI y configuración reales del repo para los comandos.

| Comprobación | Alcance y evidencia |
| --- | --- |
| Lint y formato | Archivos modificados compatibles con la configuración existente; usa modo de comprobación antes de reformatear. |
| Tipos o compilador | Límite del paquete/proyecto afectado; dependencias de tipos pueden exigir un destino mayor. |
| Comportamiento | Ruta real modificada y una regresión que falle si se rompe la capacidad. |
| Contrato/integración | Consumidores, alias, empaquetado, preservación de ajustes o límites de runtime tocados. |
| Puertas obligatorias de integración | Suites exigidas por el repo cuando el candidato se estabilice. |

Declara cada comando, por qué cubre el riesgo, revisión/estado pendiente,
resultado ejecutado y fallos restantes. Linter/typechecker ausente significa
**no disponible** o **no aplicable**, con razón; no inventes un pase. No instales
herramientas nuevas solo porque un ejemplo las nombra. Lint verde no sustituye
tests de comportamiento.

Durante la iteración elige el destino útil más pequeño. No es necesario repetir
una comprobación aprobada si no cambiaron código ejercitado, entradas o entorno
pertinente. Una dependencia indirecta concreta sin resolver o una puerta obligatoria
justifica ampliar pruebas; registra por qué. Al integrar, ejecuta una vez los
chequeos agregados requeridos del candidato final. Cambios posteriores invalidan
solo la evidencia afectada y las puertas de commit requeridas.

## 3. Haz que los tests detecten roturas reales

Comprueba un efecto observable: artefacto válido existente, datos recuperados de
una base local real, bytes reales de contexto recibidos por el host o elemento de
UI renderizado. Ejercita archivos, bases de datos y sockets locales sin mockearlos.
La hoja de transporte externo de pago puede sustituirse por un fixture determinista,
manteniendo reales la construcción de petición, enrutamiento, análisis y consumidor
local. Nunca afirmes que ese fixture demuestra que se ejecutó el servicio externo.

Conserva idéntico byte a byte el archivo RED sellado de [red-first](../red-first/SKILL.md).
Ante un hueco nuevo, añade un archivo separado de regresión suplementaria siguiendo
las reglas de evidencia y sellado de esa skill. Nunca debilites, renombres,
sustituyas ni edites el archivo sellado original.

## Salida

Devuelve alcance del candidato, resultados ejecutados de lint/tipos/tests,
evidencia de efectos reales y puertas pendientes al mismo responsable.
[clean-code-gauntlet](../clean-code-gauntlet/SKILL.md) usa esa evidencia como primera
etapa, no como motivo para repetir comprobaciones sin cambios.
