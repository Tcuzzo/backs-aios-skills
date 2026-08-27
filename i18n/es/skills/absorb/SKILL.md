---
name: absorb
description: Úsala cuando necesites una capacidad que un proyecto open source ya ofrece — adóptala y hazle reingeniería como skill nativa en vez de inventar un duplicado. Trigger words: absorb, adopt, port, re-engineer, ingest a repo, prior art, capability port, make this native. Disparadores: absorber, adoptar, portar, reingeniería, ingerir un repo, arte previo, hazlo nativo.
license: MIT
---

# Absorb — Adopta el arte previo, no lo reinventes
**Effort:** light — una ingesta del repo (sondeo de metadatos + clon superficial) y una calificación cross-family del port. Elimina: reinventar una capacidad que el arte previo ya resolvió — el duplicado desde cero cuyos bugs cargarías todos tú.

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

1. **Caza el arte previo primero.** Busca antes de construir. Un duplicado que
   inventas es peor que un andamiaje que adoptas: heredas cero pruebas de campo y
   todos los bugs corren por tu cuenta.
2. **Ingiere más allá del README.** Trae los metadatos del proyecto (licencia,
   actividad, lenguaje) desde la API de la plataforma. Haz un shallow-clone en un
   directorio temporal de trabajo. Lee el código y los tests. El README es
   marketing; el código es la verdad.
3. **Corre las puertas de confianza.**
   - *Licencia:* permisiva (MIT / Apache / BSD / MPL) = segura para reingeniería.
     Copyleft (GPL / AGPL) = solo la técnica — reconstruye la idea, nunca copies
     el código. Sin licencia = trátalo como todos-los-derechos-reservados, solo la
     técnica. Términos no comerciales = un bloqueo; llévaselo a tu humano.
   - *Escaneo de cosas turbias:* haz grep buscando patrones de cloaking / spam /
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
6. **Reconstruye en rojo primero.** Haz commit de los tests que fallan y luego
   construye hasta el verde en toda la costura. Un modelo de una familia distinta a
   la del constructor evalúa el resultado — el que construye nunca califica su
   propio trabajo.
7. **Cita y registra.** Escribe el crédito del andamiaje donde ahora vive la
   capacidad: autor, proyecto, licencia, qué es prestado (el andamiaje) y qué es
   tuyo (la reingeniería). Nunca inventes un crédito. Nunca borres uno.

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
- [blind-tribunal](../blind-tribunal/SKILL.md) — evaluación entre familias del port.
- [decision-bar](../decision-bar/SKILL.md) — los bloqueos de licencia y las decisiones de gusto van a tu humano; todo lo demás se ejecuta.
