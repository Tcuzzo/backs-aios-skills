# Jugada: Grading & Verification

La jugada de calificación adversarial. Su única creencia: un resultado verde es una
afirmación, no una prueba. El evaluador ataca, y el piso está construido para que
no se le pueda hacer trampa.

## Cuándo ejecutarla

- Cualquier cambio construido pide aterrizar — código, config, docs, la salida de un
  agente.
- Una suite afirma verde y nadie la vio fallar primero.
- Un modelo construyó el trabajo y necesitas un veredicto honesto sobre él.

## La cadena

1. [red-first](../skills/red-first/SKILL.md) — confirma que la suite falló con
   salida distinta de cero ANTES de que el arreglo existiera. Una suite que nunca
   estuvo en rojo no prueba nada.
2. [sniper-testing](../skills/sniper-testing/SKILL.md) — verifica que el constructor
   usó tests acotados durante la iteración y no corrió teatro de mocks sobre la
   costura que cambió.
3. Calificación entre familias — entrega el trabajo a un modelo de una familia
   DISTINTA a la del constructor. Calificar dentro de la misma familia infla las
   tasas de victoria de forma medible — los evaluadores favorecen a los suyos;
   otra instancia de la misma familia no alcanza.
4. [blind-tribunal](../skills/blind-tribunal/SKILL.md) — para cambios con
   consecuencias, convoca jurados sobre un sobre con el autor tachado. Cada hallazgo
   se vuelve un nuevo test rojo, y el tribunal se vuelve a convocar hasta que todos
   los jurados lo aprueben.
5. [clean-code-gauntlet](../skills/clean-code-gauntlet/SKILL.md) — el evaluador
   re-corre el gauntlet por su cuenta (cobertura contra complejidad, testing de
   mutación acotado). Nunca confíes en el reporte del constructor sobre sus propios
   números.

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

- El constructor y el evaluador comparten familia de modelos.
- La suite no se puede mostrar en rojo antes del arreglo.
- Falta fail-to-pass o pass-to-pass en la corrida calificada.
- Cualquiera de las señales de verde falso de arriba está presente.
- El evaluador confió en el reporte del propio constructor en vez de re-correr los
  chequeos.
