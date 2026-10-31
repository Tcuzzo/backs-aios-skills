# Jugada: Grading & Verification

La jugada de calificación adversarial. Su única creencia: un resultado verde es una
afirmación, no una prueba. El evaluador ataca, y el piso está construido para que
no se le pueda hacer trampa.

## Cuándo ejecutarla

- Cualquier cambio construido pide aterrizar — código, config, docs, la salida de un
  agente.
- Una suite afirma verde y nadie la vio fallar primero.
- Un modelo construyó el trabajo y necesitas un veredicto honesto sobre él.

## Tarea y límites compartidos

Aplica este play dentro del paquete actual de
[BACKS Build Flow](../skills/backs-build-flow/SKILL.md). Mantén un responsable
de integración, `task_mode` solicitado, revisiones base y candidata fijadas,
esencia del operador y evidencia vigente. Reutiliza cuerpos pertinentes ya cargados;
este play añade puertas de su dominio sin reiniciar la tarea.

[bounded-loops](../skills/bounded-loops/SKILL.md) controla plazo original y cupos
restantes entre reintentos, trabajadores, modelos, revisiones y traspasos.
Nunca los reinicies para un play anidado. Al agotarlos, guarda **STILL-BUILDING**
con candidato, evidencia, puertas pendientes y siguiente acción. Continúa trabajo
útil autorizado solo dentro de su cupo restante; una puerta ausente no se vuelve aprobada.

## La cadena

1. [red-first](../skills/red-first/SKILL.md) — confirma que la suite falló con
   salida distinta de cero ANTES del arreglo. Una suite nunca roja no prueba nada.
   El test fallido queda confirmado y el constructor no puede tocarlo; sus bytes
   exactos son el contrato.

2. [sniper-testing](../skills/sniper-testing/SKILL.md) — verifica comandos reales
   de lint/tipos/tests acotados al diff agregado fijado y ausencia de teatro de mocks
   en la costura modificada. Comprueba razones N/A y chequeos faltantes. Congela
   la identidad del candidato para esta revisión.

3. Evaluación independiente — elige en vivo por capacidad y disponibilidad
   desde la matriz configurada (tarea → capacidad → peldaño → sondeo). Registra
   la ejecución autora cuando el runtime lo soporte y exclúyela. Puede revisar
   cualquier ruta capaz configurada en sesión fresca y disjunta del autor. Se prohíbe
   una sesión que haya visto la conversación o heredado contexto del constructor.

4. [blind-tribunal](../skills/blind-tribunal/SKILL.md) — para cambios importantes,
   convoca jurados sobre un paquete sin autoría, en sesión nueva sin conversación
   heredada. Devuelve hallazgos fundamentados al responsable de integración para
   RED suplementario separado y reparación acotada; el original sigue sellado.
   Reconvoca sobre el candidato revisado y congelado dentro del mismo presupuesto.
   Todos los jurados requeridos deben aprobar antes de integrar.

5. [clean-code-gauntlet](../skills/clean-code-gauntlet/SKILL.md) — el evaluador
   re-corre el gauntlet por su cuenta (cobertura contra complejidad, testing de
   mutación acotado). Nunca confíes en el reporte del constructor sobre sus propios
   números.

Respeta el destino inmutable de revisión. Ejecuta comprobaciones que creen caché,
muten código o ejerciten servicios solo en aislamiento permitido; la mutación
nunca reescribe la fuente congelada. Falta de aislamiento o soporte de runtime
es hueco de evidencia, no permiso para reparar durante revisión. Conserva evidencia
completa requerida de suites afectadas y separa pruebas locales de superficie
real o entrega.

## La prueba de dos lados (ambas, o no pasa)

- **Fail-to-pass:** los tests que estaban rojos ahora están verdes — el arreglo
  queda probado.
- **Pass-to-pass:** todo lo que estaba verde sigue verde — sin regresión.
- Una corrida que solo AGREGA tests que pasan no satisface ninguna de las dos. Corre
  ambas de forma hermética.

## Guardias anti-verde-falso (cualquiera es la señal)

- Una escotilla en el código de salida — un harness que sale limpio pase lo que
  pase.
- Salidas hardcodeadas o memorizadas en lugar de calculadas.
- Tests borrados, salteados o debilitados.
- Cualquier evaluador, temporizador o puntuador editado. Un harness editado que se
  pone verde ES la señal.
- Un mutante que sobrevive bajo una suite verde. El mutante es la prueba de que las
  aserciones nunca llegaron a esa rama — verde falso por definición.

## Quítale el sesgo al juez

El piso de mecánica del juez vive en la sección "De-bias the judge" de
[blind-eval](../skills/blind-eval/SKILL.md) — aplícala completa.

## Puertas duras — cualquiera hace fallar la jugada

- La revisión usó la ejecución autora o una sesión que vio su conversación o
  heredó su contexto; es obligatoria una sesión nueva separada del autor.
- Un jurado del tribunal heredó contexto o vio la conversación del autor.
- La suite no se puede mostrar en rojo antes del arreglo.
- Falta fail-to-pass o pass-to-pass en la corrida calificada.
- Cualquiera de las señales de verde falso de arriba está presente.
- El evaluador confió en el reporte del propio constructor en vez de re-correr los
  chequeos.

**Brechas del entorno.** Selecciona revisores capaces mediante la escalera
configurada y excluye la ejecución autora. Informa restricciones de runtime que
bloqueen un revisor capaz; no afirmes silenciosamente que se resolvieron ni las evadas.

**Weight:** chequeos free de rojo y francotirador por delante; el gasto heavy es el tribunal más el evaluador re-corriendo el gauntlet por su cuenta — se paga en cualquier cambio que pide aterrizar, porque un verde falso cuesta más que todas las calificaciones juntas.
