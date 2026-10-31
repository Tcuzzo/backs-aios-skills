---
name: building-with-backs
description: "Úsala al construir o reparar un proyecto BACKS, resolver ambigüedades de carpeta o checkout, o llevar un cambio autorizado del IDE a su runtime real."
license: MIT
---

# Construir con BACKS

Esta skill cierra un fallo recurrente: un buen parche en el checkout equivocado,
o un test verde que nunca llega a la app del operador. El destino es el producto
y la ruta solicitados. Descubre el destino antes de escribir.

Únete al paquete existente de [BACKS Build Flow](../backs-build-flow/SKILL.md);
una invocación directa lo establece una sola vez. Mantén un responsable de integración
y reutiliza esencia y contexto existentes. Respeta `task_mode` y conserva plazo
y cupos restantes de [bounded-loops](../bounded-loops/SKILL.md) entre trabajadores,
modelos y traspasos. Resolver otra ruta no reinicia presupuesto ni autoriza despliegues.

1. **Resuelve el destino.** Usa la ruta exacta nombrada por el humano. Si no indicó
   ninguna, inspecciona workspace activo, referencias recientes y mapa del repo.
   No sustituyas por un clon cercano solo porque coincide el nombre. Ejecuta
   `python scripts/resolve_target.py --repo <path> --target <file-or-directory>`
   desde el directorio de esta skill; añade `--expected-root <path>` si nombró
   el checkout. El comando devuelve código distinto de cero si falta la raíz,
   la ruta sale de ella, el checkout no coincide o falta una revisión Git. Un
   archivo nuevo puede no existir todavía; su directorio padre debe existir.
   Para un proyecto no Git nombrado expresamente, añade `--allow-non-git` y
   registra que no hay revisión disponible.
2. **Fija la verdad inicial.** Registra raíz resuelta, rama o HEAD separado,
   `base_sha`, `candidate_sha` actual, estado del worktree, destino solicitado,
   punto de entrada de app/servicio y comprobaciones. Mantén fija la base original
   tras commits; actualiza explícitamente el candidato y revisa rutas pendientes.
   Conserva ediciones ajenas. Si otro checkout es más reciente, compara revisiones
   y árboles reales antes de elegir; «más reciente» se mide.
3. **Traza la ruta.** Sigue acción del usuario hasta entrada, implementación,
   datos, salidas y costura de despliegue. Nombra responsable existente y consumidores
   dependientes. Usa `repo-map`, `architecture-engineer` y `root-cause-first`
   cuando esas costuras sean inciertas.
4. **Construye en el lugar resuelto.** Asigna preguntas distintas a lectores paralelos
   y archivos sin solapamiento o worktrees aislados a escritores. Mantén un responsable
   de integración. Haz el cambio mínimo que cierre la clase de fallo; aplica
   `repair-loop` dentro del flujo actual. Sigue el play completo `elite-build`
   cuando se seleccione o solicite expresamente, reutilizando etapas válidas sin
   arrancar de nuevo. Una revisión o diagnóstico devuelve hallazgos sin editar.
5. **Prueba la ruta.** Sigue RED sellado → corrección mínima → comprobaciones
   sniper de lint/tipos/tests → clean-code-gauntlet. Deriva alcance del diff agregado
   fijado; usa comandos reales del repo y declara huecos o N/A honestamente.
   Conserva revisión independiente del autor y pasada completa requerida de las
   suites afectadas al integrar. Inspecciona superficie real de app/CLI y logs dentro
   del alcance. Registra revisión/hash exacto desplegado y comportamiento observado;
   nombra todo lo que no pudo ejercitarse.
6. **Promueve por la ruta propia del proyecto.** Lee sus instrucciones de despliegue
   y aprobación en ese repo. Nunca trasplantes un comando de otro proyecto.
   Repite la comprobación de destino antes de instalar y verifica después que
   el proceso en ejecución usa el código instalado.

Si el destino sigue ambiguo, continúa la investigación de solo lectura y pregunta
por la ruta solo después de comprobar la evidencia disponible. Nunca afirmes
instalación entre hosts solo porque copiaste archivos; verifica descubrimiento en
cada host o márcalo sin verificar.

Si un cupo se agota, guarda **STILL-BUILDING** con destino verificado, candidato,
evidencia pendiente y siguiente acción exacta. Conserva límites originales;
termina trabajo útil autorizado que no consuma el cupo agotado. Una comprobación
local no sustituye evidencia de la entrega solicitada.
