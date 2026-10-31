---
name: "absorb"
description: "Úsala cuando una capacidad necesaria pueda existir en un proyecto open source, o el operador pida absorber, adoptar, portar, hacer reingeniería, ingerir un repo, evaluar arte previo o volver nativa una capacidad."
license: "MIT"
---

# Absorb — Adopta el arte previo, no lo reinventes
**Effort:** light — una ingesta del repo (sondeo de metadatos + clon superficial) y una calificación independiente (asiento no autor, resuelto por capacidad) del port. Elimina: reinventar una capacidad que el arte previo ya resolvió — el duplicado desde cero cuyos bugs cargarías todos tú.

**La capacidad manda.** Un repo es un vehículo para una capacidad. Cuando necesitas
algo que un proyecto existente ya hace, no construyas un duplicado desde cero, y
tampoco clones y pegues. Busca el mejor arte previo, extrae la capacidad, hazle
reingeniería para que encaje en tu harness, y cita el andamiaje. La cita es un
hecho, no un adorno.

## Cuándo ejecutarla

- Te piden agregar una capacidad (una herramienta, una skill, un agente, un pipeline)
  que el open source probablemente ya resolvió.
- Estás a punto de hacer `git clone` y copiar código tal cual — detente; este es el
  camino en su lugar.
- Sáltatela para un snippet suelto, un valor de config o un dato puntual. Eso solo se lee.

## Pasos

Usa el paquete actual de [BACKS Build Flow](../backs-build-flow/SKILL.md) y su
responsable de integración. Una invocación directa crea ese paquete una vez;
una llamada anidada devuelve evidencia de adopción a quien llama. Reutiliza
contexto válido, esencia del operador y cuerpos ya cargados.
[bounded-loops](../bounded-loops/SKILL.md) controla plazo y cupos restantes de la
misión; descubrimiento, construcción, mutaciones, revisiones, cambios de modelo
y traspasos consumen ese mismo presupuesto. Otra fase o trabajador no lo reinicia.
Respeta `task_mode`: revisar o diagnosticar no autoriza ediciones nativas ni entrega.

1. **Caza el arte previo primero.** Busca antes de construir. Un duplicado que
   inventas es peor que un andamiaje que adoptas: heredas cero pruebas de campo y
   todos los bugs corren por tu cuenta.
2. **Descubre más allá del README.** Trae metadatos del proyecto (licencia,
   actividad, lenguaje) desde la API de la plataforma. Clona superficialmente en
   un directorio temporal. Lee código y tests. Para artefactos distribuidos o
   comportamiento solicitado que el código no permita resolver, llama a
   [rea-investigation](../rea-investigation/SKILL.md) con destino exacto y pregunta
   acotada. REA devuelve evidencia a este llamador; no reinicia Absorb. Registra
   identidad original, observaciones, límites e incógnitas antes de elegir qué
   adoptar. Los hallazgos estáticos no establecen comportamiento de runtime.
3. **Corre las puertas de confianza.**
   - *Licencia:* permisiva (MIT / Apache / BSD / MPL) = segura para reingeniería.
     Copyleft (GPL / AGPL) = solo la técnica — reconstruye la idea, nunca copies
     el código. Sin licencia = trátalo como todos-los-derechos-reservados, solo la
     técnica. Términos no comerciales = un bloqueo; llévaselo a tu humano.
   - *Escaneo de cosas turbias:* usa `rg` para buscar patrones de cloaking / spam /
     reseñas falsas / estafa. Señálalo con ruido.
   - *Nada de instalaciones a lo loco:* nunca hagas `pip install` / `npm install`
     de una dependencia sin examinar (el typo-squatting es un ataque real a la
     cadena de suministro). Mejor reconstruye la técnica como código delgado sobre
     tus propias primitivas.
   - *¿La capacidad es real?* Verifica las afirmaciones contra evidencia
     independiente. El blog del que vende es una afirmación, no evidencia.
     Veredicto: real / humo / estafa / no verificable.
   - *Egreso acotado:* todo lo que la versión adoptada descargue debe llevar
     throttle, caché y una forma de matarlo.
4. **Descompón en un mapa de capacidades.** Por cada habilidad que el proyecto
   ofrece, registra: qué hace, cómo, sus costuras que cargan peso, su grasa o su
   riesgo, qué puedes reutilizar de tu propio stack, y si aterriza nativa o detrás
   de un adaptador delgado. Cada capacidad queda **preservada o refutada con
   evidencia**. Una capacidad descartada en silencio es un defecto.
5. **Escribe la especificación de reingeniería.** Las costuras a construir, la
   grasa que vas a soltar (registrada con ruido, nunca en silencio), y un test de
   contrato en rojo por capacidad que verifique un efecto real — un archivo, una
   fila en la base de datos, salida de verdad. Mockea solo el transporte de una API
   externa de pago, nunca la lógica.
6. **Integración nativa.** Aplica [red-first](../red-first/SKILL.md): observa
   un fallo real y sella el contrato antes del arreglo mínimo en la costura responsable.
   Conserva intacto el test original. Acota los comandos reales de lint, tipos
   y tests del repo mediante [sniper-testing](../sniper-testing/SKILL.md), con
   `base_sha` fijado y `candidate_sha` actual, incluyendo rutas pendientes propias.
   Registra comprobaciones no disponibles o no aplicables; nunca instales un
   comprobador arbitrario ni inventes un pase. Ejecuta
   [clean-code-gauntlet](../clean-code-gauntlet/SKILL.md) en el mismo flujo para
   evidencia de calidad/mutación. Un hueco recibe regresión suplementaria separada,
   nunca una edición del original sellado. Todo consume el presupuesto compartido.
7. **Verifica la capacidad adoptada.** Ejercita el resultado nativo contra el
   mapa de capacidades y la superficie real del usuario. Reutiliza evidencia de
   descubrimiento; solicita otra observación REA solo para una comparación concreta
   pendiente, dentro de sus límites existentes de proveedor y ejecución. Elige
   evaluador capaz mediante la matriz configurada para revisión nueva independiente
   del autor del candidato agregado exacto; registra y excluye la ejecución autora.
   El constructor nunca se evalúa a sí mismo. Ejecuta la pasada requerida de suites
   afectadas y sigue la entrega autorizada del proyecto. Evidencia estática original
   o GREEN local no demuestra entrega nativa en vivo.
8. **Cita y registra.** Conserva el crédito del andamiaje donde vive la capacidad:
   autor, proyecto, licencia, qué se tomó prestado y qué es reingeniería propia.
   Nunca inventes ni borres créditos. Devuelve mapa de capacidades, candidato exacto,
   comprobaciones, atribución y huecos al responsable de integración. Si se agota
   presupuesto o no puede ejecutarse una puerta requerida, guarda **STILL-BUILDING**
   con trabajo restante y siguiente acción; continúa trabajo útil autorizado que
   no consuma el cupo agotado. Nunca fabriques **PROVEN** ni omitas capacidades
   para obtener un pase.

## Reglas duras — cualquiera de estas reprueba la skill

- Copiar código tal cual en vez de hacerle reingeniería a la capacidad.
- Construir un duplicado sin haber buscado arte previo.
- Confiar en el README o en una página de marketing por encima del código.
- Instalar una dependencia a lo loco en vez de reconstruir la técnica.
- Copiar código copyleft o sin licencia (solo la técnica, siempre).
- Descartar una capacidad sin una refutación escrita.
- Teatro de mocks en un test de capacidad — el test debe tocar un efecto real.
- Publicar sin la cita del andamiaje.

## Combina bien con

- [red-first](../red-first/SKILL.md) — los tests de contrato que custodian cada capacidad.
- [sniper-testing](../sniper-testing/SKILL.md) — efectos reales, sin teatro de mocks.
- [blind-tribunal](../blind-tribunal/SKILL.md) — evaluación independiente del port.
- [decision-bar](../decision-bar/SKILL.md) — los bloqueos de licencia y las decisiones de gusto van a tu humano; todo lo demás se ejecuta.
