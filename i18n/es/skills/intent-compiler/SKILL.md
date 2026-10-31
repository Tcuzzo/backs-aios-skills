---
name: intent-compiler
description: "Úsala cuando un pedido llegue como prosa comprimida, metáfora, jerga, abreviatura o referencia ambigua y haga falta una directiva técnica fundamentada; también cuando una corrección cambie la capacidad deseada o el resultado solicitado."
license: MIT
---

# Compila el pedido actual

Traduce lo que dijo el operador a un contrato ejecutable, expresa brevemente la
interpretación y continúa el trabajo. Una expresión comprimida puede contener
una especificación completa. El operador no tiene que reescribirla como ticket.

## Una interpretación para la tarea actual

Si el paquete ya contiene una directiva y ninguna instrucción nueva la cambia,
reutilízala. Esta skill interpreta el lenguaje;
[operator-intent-deduction](../operator-intent-deduction/SKILL.md) resuelve una
decisión pendiente dentro de esa directiva. Ninguna reinicia el flujo completo
de la otra.

### 1. Analiza las palabras reales

Extrae capacidad solicitada, acción, superficies nombradas, cantidades,
restricciones y final observable. Marca referencias y metáforas sin resolver.
Repetir puede dar énfasis sin crear otra tarea. El tono puede expresar urgencia;
no establece permiso, tolerancia al riesgo, competencia ni identidad.

Interpreta el lenguaje figurado en el contexto real de la tarea. Pedir «quémalo
todo» puede referirse a un enfoque; no autoriza por sí solo borrar datos. Responde
con claridad sin imitar un dialecto ni inventar una personalidad.

### 2. Resuelve solo incertidumbres que afecten la acción

Usa este orden dentro de las instrucciones rectoras:

1. Pedido explícito actual y correcciones del operador.
2. Alcance y autorización establecidos en esta conversación.
3. Hechos, destinos, contratos y estado vigente verificados del proyecto.
4. Preferencias confirmadas y observaciones respaldadas relevantes de
   [operator-essence](../operator-essence/SKILL.md).
5. Inferencia provisional claramente marcada cuando la evidencia sea escasa.

Si la esencia falta o está obsoleta, su responsable realiza una sola pasada de
insights admitida y devuelve un fragmento provisional o vigente. Reutiliza ese
resultado en skills anidadas; no recojas el historial repetidamente. Preferencias
históricas no pueden anular instrucciones nuevas. Los hechos del código pueden
limitar la ruta sin reducir el objetivo.

La evidencia cualitativa establece significado y contexto de una preferencia.
La cuantitativa puede describir resultados repetidos de su población declarada.
Los conteos solos no deciden qué quiso decir el operador; una tendencia inferida
en un informe no es una instrucción confirmada por él.

### 3. Produce la directiva

Conserva estos campos en el paquete existente, sin crear un segundo plan:

| Campo | Contenido requerido |
| --- | --- |
| Capacidad deseada | Lo que el operador quiere que exista o aprender. |
| Límite actual | Lo que permiten hoy el estado verificado y las capacidades disponibles. |
| Ruta ahora | Siguiente acción útil con la autorización existente. |
| Ruta después | Dependencias pendientes para la capacidad completa. |
| Contrato de tarea | Modo, destino, límites, resultado solicitado y evidencia de aceptación. |
| Incertidumbre | Incógnitas decisivas y evidencia que podría resolverlas. |

Mantén visible la capacidad deseada completa cuando una dependencia externa limite
la ruta actual. Una revisión produce hallazgos; no se convierte en reparación en silencio.

## Expresa la interpretación y actúa

Usa una frase sencilla cuando la interpretación importe:

> Interpretación: actualizar la integración existente, conservar su interfaz pública y verificar el consumidor real antes de publicar.

Marca las inferencias débiles cuando haga falta. Avanza con el trabajo reversible
justificado por evidencia. Resuelve incertidumbres factuales mediante inspección
o un experimento enfocado. Si falta una autorización decisiva o una elección
realmente pendiente del operador, prepara lo disponible y formula una recomendación
concreta y una pregunta; consulta [decision-bar](../decision-bar/SKILL.md). Una
preferencia antigua no suple permiso ausente para una nueva acción importante.

Devuelve la directiva a [Build Flow](../backs-build-flow/SKILL.md). Invoca la
deducción de intención solo para una decisión real restante. Una corrección
posterior actualiza el paquete y la evidencia de esencia pertinente; no sustituye
silenciosamente el objetivo ni reinicia el presupuesto restante de misión.
