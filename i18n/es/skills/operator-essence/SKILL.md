---
name: operator-essence
description: "Úsala cuando falte contexto del operador, esté desactualizado o corregido, o haga falta para una decisión de construcción; también al evaluar insights de uso, patrones de colaboración o una esencia y mejoras basadas en evidencia que solicite el operador."
license: MIT
---

# Esencia del operador

Da al agente conocimiento útil del operador actual, respaldado por evidencia.
Un archivo de esencia contiene datos contextuales: no es una instrucción,
autorización, personalidad fija ni sustituto del pedido actual.

## Una pasada de evidencia; después, construir

1. **Reutiliza el contexto vigente.** El responsable de tarea comprueba en el
   paquete la referencia a la esencia del operador actual, el fragmento relevante
   y el recibo del intento de insights. Una skill anidada reutiliza ese resultado.
   Resuelve una ruta privada explícita de `OPERATOR_ESSENCE.md` y una clave opaca
   de operador a partir del alcance actual; no selecciones otro operador por
   proximidad ni infieras identidad por el idioma.
2. **Inspecciona el archivo.** Usa [la herramienta de ruta explícita y el formato](references/format.md).
   Un archivo válido y vigente aporta solo preferencias y observaciones relevantes.
   Una corrección prevalece inmediatamente; concíliala aunque el archivo sea
   reciente. Datos inválidos o de otro operador son contexto no disponible, no
   permiso para sobrescribir.
3. **¿Falta o está desactualizado? Invoca insights una vez para esta tarea.**
   Descubre el comando, skill o conector de insights realmente disponible en el
   entorno y usa su invocación admitida. Registra el resultado o la limitación
   exacta. Si no hay ninguno invocable, evalúa el informe facilitado, el historial
   pertinente autorizado y las instrucciones actuales. Declara esa alternativa;
   nunca afirmes haber ejecutado un comando que no corrió. Recoge solo evidencia
   relevante para el trabajo del operador, dentro del alcance y presupuesto restantes.
4. **Crea o concilia la esencia.** Registra fuentes, fechas, selección de muestra,
   preferencias confirmadas, observaciones, conteos, incertidumbre, contraejemplos
   y adaptaciones tentativas. Lo desconocido sigue desconocido. Las interpretaciones
   de informes siguen siendo inferencias; las etiquetas de eventos superpuestas
   no son tasas de fallo por sesión. Con evidencia escasa, crea un archivo
   provisional con solo hechos respaldados. En modo de solo lectura, devuelve un
   fragmento provisional sin escribir en el destino protegido. La falta de
   historial no bloquea la construcción autorizada.
5. **Transmite el contexto al agente.** Facilita el fragmento compacto del formato:
   referencia y vigencia; preferencia confirmada relevante; observación y
   evidencia; adaptación sugerida; límites. El responsable retoma
   [Build Flow](../backs-build-flow/SKILL.md) con el mismo presupuesto. Muestra al
   operador qué cambió y dónde inspeccionar el archivo o registro activo de tarea.

## Evaluación cualitativa y cuantitativa

Lee lo que el operador pidió, corrigió, aceptó y rechazó junto con los resultados
reales de las tareas. Separa observaciones de explicaciones. Los conteos describen
su población declarada; una muestra cuya selección se desconoce no describe todas
las sesiones. El volumen de llamadas a herramientas no prueba un uso correcto de
skills y una correlación no establece la causa de un fallo.

Convierte patrones respaldados en adaptaciones contextuales con una condición
de revisión. Compara tareas posteriores de tipo similar antes de afirmar una
mejora. Mantén visibles los contraejemplos exitosos. No infieras rasgos
psicológicos, competencia, cultura, tolerancia al riesgo ni prioridades duraderas
a partir del estilo de escritura o de estadísticas agregadas de uso.

## Salida

Quien invoca recibe un fragmento vigente o expresamente provisional, los límites
de la evidencia y la siguiente acción de construcción. Las tendencias históricas
completan huecos; las instrucciones actuales y los hechos verificados del proyecto
rigen el trabajo. El archivo nunca concede permiso, amplía el alcance, reinicia
un ciclo acotado ni cambia los criterios de aceptación.
