---
name: rea-investigation
description: "Úsala cuando ejecutables distribuidos, paquetes o comportamiento solicitado de runtime necesiten investigación REA para diagnóstico, descubrimiento de capacidades o verificación de una adopción nativa."
license: MIT
---

# Investigación de artefactos con REA

Usa el motor REA instalado y su skill independiente para binarios distribuidos,
paquetes o comportamiento solicitado de runtime. Para repositorios de código
ordinarios, usa directamente código y tests. Este puente no instala REA, Ghidra,
proveedores ni servidores MCP, y no afirma que estén disponibles.

Usa el paquete de [BACKS Build Flow](../backs-build-flow/SKILL.md), responsable de
integración y `task_mode` permitido de quien llama. La investigación directa
establece el paquete una vez. [bounded-loops](../bounded-loops/SKILL.md) controla
plazo y cupos restantes; los heredan reintentos de proveedor, modelos y traspasos.
Esta skill produce evidencia; no crea otro responsable de adopción o reparación.

1. Resuelve destino exacto, identidad/hash, pregunta y fase: **descubrimiento**
   del artefacto original o **verificación** de un resultado nativo concreto.
   Lee la skill instalada `reverse-engineer-anything` y sus referencias pertinentes
   desde el directorio de skills del host; evita seleccionar recursivamente este
   puente. Si falta, informa y continúa investigación útil con herramientas
   disponibles dentro del presupuesto existente.
2. Usa herramientas REA conectadas cuando existan o la CLI instalada. Para binarios
   nativos compatibles, usa un proveedor Ghidra existente; informa ausencia o
   indisponibilidad sin inventar resultados ni instalar dependencias sin autorización.
3. Empieza con inspección estática de solo lectura. Registra identidad del destino,
   IDs de evidencia, alcance, límites e incógnitas. Hallazgos estáticos no prueban
   comportamiento de runtime; observa en vivo solo dentro del alcance solicitado
   y los límites declarados de ejecución y mutación de la herramienta.
4. Devuelve a quien llama un paquete con identidad, fase, comandos/recibos,
   IDs de evidencia, observaciones, distinción estática/runtime, incógnitas y
   presupuesto restante. El llamador controla el siguiente paso: Absorb aplica
   puertas de licencia/dependencias e integración nativa; el responsable de reparación
   aplica root-cause-first y repair-loop. No inicies recursivamente esos ciclos
   desde el puente. Si la verificación halla un defecto, devuelve la observación
   para RED sellado y ciclo acotado de arreglo/comprobación; no afirmes haber reparado.
5. Enruta por rol y capacidad mediante fleet-ladder configurado; nunca fijes IDs
   de modelos. Para evaluación independiente requerida, usa la ejecución nueva
   separada del autor de blind-tribunal y un paquete sin autoría, según las
   capacidades reales del host. Proveedor ausente o presupuesto agotado produce
   checkpoint **STILL-BUILDING** con observaciones útiles y siguiente acción exacta;
   nunca prueba inventada de runtime. Mantén investigación desbloqueada dentro
   de su cupo restante.

Andamiaje: REA de morluto, licencia MIT, https://github.com/morluto/rea.
Motor, skill original y proveedores son instalaciones independientes.
