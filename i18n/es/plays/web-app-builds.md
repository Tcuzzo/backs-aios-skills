# Web App Builds

Cómo construir una app o un sitio web con estructura limpia y una cadena de
suministro defendida. La mayor parte del daño en builds web entra por las
dependencias y las fronteras, no por tu propia lógica — así que la higiene es la
jugada, no una idea de último minuto.

## Cuándo ejecutarla

Al construir o extender cualquier app web, sitio, API o repo entregado que otra
persona va a instalar y correr.

## La cadena

1. [intent-compiler](../skills/intent-compiler/SKILL.md) — lee el pedido completo
   antes de elegir stack o estructura.
2. [understanding-gates](../skills/understanding-gates/SKILL.md) — diseña primero la
   estructura: un punto de entrada documentado, un manifiesto de dependencias
   explícito y un lockfile commiteado. Nada de desorden de archivos ad-hoc.
3. Higiene de dependencias (hazla ANTES de cualquier install):
   - Valida cada paquete referenciado contra el registro: existe, es anterior a tu
     proyecto, su publicador tiene historial. Los nombres de paquetes alucinados por
     IA son carnada de squatting — la investigación medida muestra que cerca del 43%
     de los nombres alucinados se repiten en re-corridas idénticas (Spracklen et al.
     (2025), USENIX Security 25), así que los atacantes pueden pre-registrarlos.
   - Fija todo por hash desde un lockfile compilado (p. ej. `pip install
     --require-hashes`, `npm ci --ignore-scripts`); rechaza cualquier discrepancia
     de integridad.
   - Bloquea por defecto los scripts de ciclo de vida del install. Un paquete que
     solo funciona corriendo un script postinstall es una bandera roja.
   - Fija cada dependencia de un workflow de CI a un SHA de commit completo de 40
     caracteres, nunca a un tag de versión mutable.
   - Minimiza el conteo: cada dependencia es una decisión revisada, no un reflejo.
     Prefiere la librería estándar o la primitiva de la plataforma.
4. [red-first](../skills/red-first/SKILL.md) — tests de contrato que fallen para las
   rutas, los loaders y los caminos de validación, antes de construirlos.
5. Construye según la doctrina de abajo. Para cualquier superficie de UI, corre el
   método [design-taste](../skills/design-taste/SKILL.md) — tokens primero,
   accesibilidad como puerta dura.
6. [sniper-testing](../skills/sniper-testing/SKILL.md) — nunca mockees tu propia
   validación o serialización: una frontera web mockeada entrega una app que acepta
   lo que debería rechazar.
7. [clean-code-gauntlet](../skills/clean-code-gauntlet/SKILL.md) — los manejadores
   de rutas, los cargadores de datos y los caminos de formularios/validación pasan
   antes del deploy; corre mutación sobre los predicados de validación y auth hasta
   que nada sobreviva. Un chequeo de frontera cuya comparación invertida igual pasa
   la suite es una puerta abierta en una superficie pública.
8. [blind-tribunal](../skills/blind-tribunal/SKILL.md) — calificación entre familias
   antes del deploy.

## La doctrina (lo que el build debe cumplir)

- Sin secretos en el código fuente: lee las credenciales del entorno o de un almacén
  de secretos. Una llave commiteada hace fallar el build.
- El manejo de la salida es consciente del contexto: consultas parametrizadas para
  SQL, y la codificación correcta antes de que cualquier valor llegue al shell, a la
  base de datos o al DOM. Nunca concatenes input no confiable como string.
- Emite un SBOM legible por máquina — un inventario de software (p. ej. CycloneDX) —
  para que quien lo recibe pueda auditar el árbol completo de dependencias.
- Mantén el build reproducible: versiones de toolchain fijadas, install determinista
  y sin acceso a red EXTERNA durante la corrida de tests (los servicios locales en
  loopback — bases de datos, fixtures — están bien y se esperan).

## Puertas duras

- Una dependencia sin validar o sin fijar bloquea el install.
- Un secreto commiteado bloquea el build.
- Mutantes sobrevivientes en predicados de validación o auth bloquean el deploy.
- Acceso a red externa durante los tests bloquea el aterrizaje (loopback está bien).

## Combina bien con

- [seam-engineering](../skills/seam-engineering/SKILL.md) — arregla una falla de frontera como clase
- [bounded-loops](../skills/bounded-loops/SKILL.md) — llamadas salientes conscientes del límite de tasa

**Weight:** disciplina free de higiene a lo largo del build; el gasto heavy es la mutación sobre los predicados de validación y de auth más el tribunal — se paga en cada superficie pública, donde una comparación volteada es una puerta abierta.
