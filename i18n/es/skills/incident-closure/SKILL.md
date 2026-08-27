---
name: incident-closure
description: Úsala cuando el humano reporta algo roto o dice "arréglalo" — sobre todo cuando el plano de control normal (API, CLI, servicio) está muerto y debes meterte por debajo. La respuesta es un cierre completo con entendimiento primero — causa raíz con evidencia, test que falla primero, verde, prueba en vivo en el propio camino del humano, commit — nunca un menú de opciones de vuelta. Trigger words: fix it, fix shit, full close, broken, wiped, down, it stopped working, recover, restore. Disparadores: arréglalo, cierre completo, roto, borrado, caído, dejó de funcionar, recuperar, restaurar.
license: MIT
---

# Cierre completo
**Effort:** free — disciplina de orden sobre un arreglo que ya debes: los sondeos de la verdad en disco y el test que falla van primero, no son extra. Elimina: menús de opciones y confirmaciones paso a paso lanzadas al humano en plena caída.

Cuando el humano reporta algo roto o dice "arréglalo", hay exactamente una
respuesta correcta: un cierre completo, con entendimiento primero. Causa raíz con
evidencia, un test que falla primero, verde, prueba en vivo en el propio camino
del humano, y luego commit. Nunca un menú de opciones de vuelta, y nunca un aviso
de confirmación por paso — ya dijo arréglalo.

Donde las skills hermanas exigen un sí explícito para actos destructivos, esta
regla gana solo la mitad reversible: el "arréglalo" del humano ES el sí vigente
para escrituras de recuperación reversibles que dejan un rastro de respaldo;
cualquier cosa irreversible — destrucción de datos, gasto, envíos externos —
sigue cruzando la [decision-bar](../decision-bar/SKILL.md), y la barra gana.

Pídele algo al humano solo cuando esté demostrablemente perdido en todos los
demás lugares y solo él pueda proveerlo. Todo otro insumo, lo vas a buscar tú.

## El método

1. **Sondea la superficie normal — y luego deja de confiar en ella.** Llama a la
   API o al CLI una vez. Si responde normal, esto no es una situación de cierre de
   incidente; pásala. Si devuelve 401/403, conexión rechazada, resultados vacíos
   donde debería haber datos, o datos viejos, deja de tratar esa superficie como
   autoridad.
2. **Establece la verdad de base desde el disco, no desde la API.** Nunca confíes
   en que un servicio roto describa su propio estado. Lee tú mismo los archivos de
   datos, los listados de directorios y las fechas de modificación, y compáralos
   con lo que la API afirma. La divergencia es la señal diagnóstica.
3. **Escanea el radio de impacto.** Busca en cada directorio de datos de primer
   nivel los archivos tocados dentro de la ventana de la falla (p. ej. `find
   /data/volumes -newermt "<start>" ! -newermt "<end>"`). Apunta a una respuesta
   de una pantalla para "qué fue tocado, qué no". Un radio angosto (un volumen,
   una tabla) es recuperable aquí. Un radio amplio (muchos volúmenes, el
   directorio de datos entero) es recuperación de desastre — escala, no
   improvises.
4. **Inventaría sobrevivientes vs pérdidas.** Clasifica cada activo afectado:
   - intacto en disco — recupéralo tal cual
   - reconstruible desde el repo — configs y respaldos versionados en git
   - reconstruible desde archivos de env o credenciales — tokens, contraseñas
   - perdido para siempre — cifrado con una clave ausente, estado que solo vivía en runtime
   Solo el último grupo amerita preguntarle al humano. Todo lo demás lo reconstruyes.
5. **Causa raíz con evidencia, y luego un test en rojo.** Nombra por qué se
   rompió, con prueba desde el disco — no una conjetura. Donde el defecto es
   código, escribe el test que falla y lo captura antes del arreglo, y llévalo a
   verde. Mira [red-first](../red-first/SKILL.md) y
   [root-cause-first](../root-cause-first/SKILL.md).
6. **Cae en cascada hacia abajo por las capas — nunca hacia arriba al humano.**
   Cuando el camino preferido está roto, baja una capa e intenta de nuevo:
   API / SDK → CLI dentro del contenedor → escrituras directas a la DB → cirugía
   de sistema de archivos. No molestes al humano mientras queden cascadas sin
   probar. Cada peldaño hacia abajo es más barato que preguntar.
7. **Asume que las dependencias también están rotas.** El código de recuperación
   usa solo la librería estándar de tu lenguaje para HTTP y JSON — los clientes
   de terceros pueden ser parte de lo que murió.
8. **Escribe de forma idempotente, con rastros de respaldo.** Cada escritura a
   disco deja una copia `.bak` con marca de tiempo junto al objetivo. Lee,
   verifica que tenga sentido, copia, escribe, re-verifica — nunca sobrescribas a
   ciegas. Si intercambias temporalmente una credencial para acuñar una clave
   nueva, respalda la original primero y restáurala antes de volver: el login
   propio del humano sobrevive intacto.
9. **Verifica con llamadas en vivo en el propio camino del humano.** Vuelve a
   correr el sondeo del paso 1 y confirma que los números coinciden con el
   inventario pre-incidente o con los respaldos del repo. Un estado verde en la
   DB no es prueba; la superficie que el humano usa funcionando de nuevo sí lo es.
10. **Commitea y reporta.** Commitea solo los archivos propios del arreglo.
    Reporta: qué se sondeó, el radio de impacto, las acciones en orden, los
    conteos restaurados, qué se perdió para siempre (vacío si nada), y cualquier
    paso que falló sin ser fatal.

## Banderas rojas — detente y vuelve a sondear

- "Déjame preguntarle al humano por qué se rompió" — no; averígualo primero desde el disco.
- "La API dice que aquí no hay nada" — la vista que una API rota tiene de sí misma no es verdad.
- "Mejor reinstalo limpio" — estás descartando estado recuperable.
- "La clave se perdió, así que las credenciales no sirven" — los valores en texto
  plano muchas veces siguen viviendo en archivos de env o de credenciales;
  recrea la credencial.
- "¿Confirmo antes de cada paso?" — el humano dijo arréglalo; corre la cascada y reporta al final.

## Reglas duras — cualquiera de estas reprueba la skill

- Opciones presentadas de vuelta al humano cuando existe una solución clara.
- Una escritura destructiva sin rastro `.bak`.
- Pedirle algo al humano antes de que la cascada y el inventario se agotaran.
- Un subsistema retirado restaurado "por ayudar" — un servicio dado de baja que
  sigue abajo es el estado deseado, y volver a activarlo es una decisión
  deliberada del humano.
- Recuperación declarada lista desde el estado interno en vez de un sondeo en
  vivo en su camino.
- Arreglo dejado sin commit (salvo que el humano dijera explícitamente que no).

## Combina bien con

- [repair-loop](../repair-loop/SKILL.md) — el loop de arreglo de código que este cierre corre cuando el defecto está en código.
- [root-cause-first](../root-cause-first/SKILL.md) · [red-first](../red-first/SKILL.md)
- [decision-bar](../decision-bar/SKILL.md) — qué puede llegar al humano, y cómo.
