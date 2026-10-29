---
name: rea-investigation
description: Usa REA para investigar un ejecutable distribuido, paquete o comportamiento de ejecución cuando sea necesario para diagnosticar o reparar un fallo.
license: MIT
---

# Investigación de artefactos con REA

Usa el motor REA instalado y su skill independiente para binarios distribuidos, paquetes o comportamiento de ejecución solicitado. Para repositorios de código fuente normales, usa directamente el código y las pruebas. Este puente no instala REA, Ghidra, proveedores ni servidores MCP, ni afirma que estén disponibles.

1. Identifica el objetivo exacto y la pregunta. Lee la skill REA original instalada y sus referencias pertinentes en el directorio de skills del agente, evitando seleccionar este puente recursivamente. Si falta, dilo y continúa la investigación útil con las herramientas disponibles.
2. Usa las herramientas REA conectadas cuando estén disponibles o la CLI instalada. Para binarios nativos compatibles usa un proveedor Ghidra existente y compatible; informa si falta o no está disponible, sin inventar resultados ni instalar dependencias sin autorización.
3. Empieza con inspección estática de solo lectura. Registra la identidad del objetivo, los identificadores de evidencia, el alcance, los límites y las incógnitas. Los hallazgos estáticos no prueban el comportamiento en ejecución; observa en vivo solo dentro del alcance solicitado por el usuario y de los límites declarados de ejecución y modificación de la herramienta.
4. Lleva los hallazgos a root-cause-first y repair-loop. Para adoptar una capacidad de código abierto, invoca absorb y sus controles de licencia y dependencias. Selecciona por rol y capacidad mediante el fleet-ladder configurado, sin fijar identificadores de modelo. Para una evaluación independiente usa una ejecución nueva separada del autor de blind-tribunal y un paquete congelado sin datos del autor, sujeto a las capacidades reales del entorno.

Scaffold: REA by morluto, MIT license, https://github.com/morluto/rea.
El motor, la skill original y los proveedores se instalan por separado.
