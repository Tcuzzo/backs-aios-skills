---
skill_id: operator-intent-deduction
name: operator-intent-deduction
description: "Úsala cuando quede una elección de implementación, una compensación o una pregunta propuesta al operador, y la intención actual, la evidencia del proyecto o el contexto del operador ya puedan respaldar una decisión."
license: MIT
---

# Deduce la decisión a partir de evidencia actual

Resuelve las elecciones que el agente pueda resolver responsablemente y actúa.
Usa objetivos y evidencia del operador actual; esta skill no contiene prioridades
permanentes de una persona, objetivos financieros, ajustes numéricos de riesgo
ni una lista fija de modelos.

## Entradas y responsabilidad

Parte de la directiva existente, modo de tarea, criterios de aceptación,
autorización y presupuesto restante. Si el lenguaje no se ha interpretado, usa
[intent-compiler](../intent-compiler/SKILL.md) una vez y reutiliza el resultado.
Esa skill interpreta lo dicho; esta resuelve una decisión dentro de ese alcance.

Reutiliza el fragmento relevante de [operator-essence](../operator-essence/SKILL.md).
Su responsable evalúa insights de un perfil ausente u obsoleto una vez por tarea.
Las llamadas anidadas no recogen historial ni crean otro perfil. Un fragmento
provisional es útil con su incertidumbre visible; no tener historial no bloquea
trabajo autorizado ordinario. La esencia es dato contextual, nunca autorización
ni anulación de políticas.

## Procedimiento de decisión

1. **Nombra la decisión real.** Explica su efecto sobre el resultado solicitado,
   reversibilidad y evidencia necesaria. Comprueba que siga pendiente; no reabras
   una elección ya hecha por el operador.
2. **Deriva las decisiones factuales.** Inspecciona código responsable y consumidor
   real, mide una línea base pertinente o ejecuta un experimento acotado con las
   herramientas reales del proyecto. Vincula afirmaciones numéricas con unidades,
   población e incertidumbre. No inventes parámetros, no conviertas conteos de
   etiquetas superpuestas en tasas de fallo ni votos de modelos en prueba empírica.
3. **Deduce elecciones contextuales.** Pondera primero el objetivo explícito actual;
   después preferencias confirmadas aplicables, ejemplos cualitativos y resultados
   cuantitativos. Declara una adaptación tentativa y su evidencia. Conserva
   contraejemplos y circunstancias nuevas. Una tendencia informada puede orientar
   cómo trabajar; no cambia lo que el operador pidió construir.
4. **Aplica el límite real.** Continúa acciones reversibles autorizadas. Si una
   elección importante sigue siendo decisiva y la evidencia disponible no la
   resuelve, usa [decision-bar](../decision-bar/SKILL.md): prepara el resultado
   concreto, recomendación y decisión exacta faltante. No vuelvas a pedir
   autorización ya establecida ni infieras permisos nuevos a partir de personalidad,
   urgencia o preferencias históricas.
5. **Actúa y verifica.** Devuelve la decisión al responsable existente y a
   [Build Flow](../backs-build-flow/SKILL.md). Implementar usa el mismo ciclo acotado
   RED → GREEN con lint, tests y comprobaciones requeridas de calidad/revisión.
   Otro trabajador, una pasada de insights o un experimento fallido no reinicia
   ese presupuesto.

## Recibo de decisión

Registra solo lo necesario para la siguiente acción en el paquete existente:

- **Decisión y consecuencia:** ruta elegida y resultado solicitado al que sirve.
- **Fundamento:** instrucción actual, hecho verificado, preferencia confirmada o
  inferencia, con referencias y conteos/denominadores pertinentes.
- **Incertidumbre:** supuestos, contraevidencia y condición que cambiaría la decisión.
- **Acción y prueba:** siguiente acción y observación que puede refutar la elección.

Usa lenguaje claro cuando el operador necesite ver una decisión importante.
Expresa directamente un desacuerdo razonado sin sustituir silenciosamente el
plan. Informa evidencia real de finalización. Una decisión no es un test aprobado,
una comprobación local no es un despliegue y entregar la tarea solicitada no
establece por sí solo `PROVEN`.

## Aprende sin fijar a una persona en el código

Una corrección explícita actualiza de inmediato el supuesto afectado de la tarea.
Conserva su alcance y fuente al conciliar la esencia privada. Observaciones
repetidas pueden respaldar una adaptación tentativa; evalúa tareas posteriores
comparables antes de afirmar que mejora resultados. No conviertas una preferencia
inferida en regla universal ni copies evidencia personal en el plugin público.
