# Instalación — monta el pack sobre un agente real

El pack son carpetas de markdown. Cada skill es `skills/<name>/SKILL.md`. Cada
jugada es `plays/<name>.md`. Sin binarios, sin servidor, sin paso de build. Instalar
significa poner el markdown donde tu agente busca skills.

El frontmatter es, a propósito, el subconjunto mínimo de 3 claves — `name`,
`description`, `license` — de la convención abierta Agent Skills (agentskills.io). La
spec exige solo `name` y `description`, y los runtimes conformes ignoran las claves
que no reconocen. Así el pack carga nativo donde cargue la convención, y se lee como
markdown plano en todos lados.

## 1. Plugin de Claude Code (recomendado)

Dos comandos dentro de Claude Code:

    /plugin marketplace add Tcuzzo/backs-aios-skills
    /plugin install backs-aios

Eso instala todo de una: las skills se cargan, los comandos slash quedan disponibles
(escribe `/optimus` para arrancar el piso), y el hook de grounding viene activado —
bloquea las herramientas que mutan hasta que el harness esté cargado. El kill-switch
del hook es tuyo: pon `AIOS_GATE=off` en el entorno para apagarlo, con ruido. Las
actualizaciones fluyen por `/plugin` cuando el repo del marketplace se mueve.

## 2. Claude Code, manual

Claude Code también descubre skills desde dos carpetas (confirmado contra la
documentación oficial, 2026-08): la personal `~/.claude/skills/<name>/SKILL.md`
(todos los proyectos de tu máquina) y la de proyecto `.claude/skills/` (viaja con un
solo repo).

Personal, una línea:

    git clone https://github.com/Tcuzzo/backs-aios-skills.git ~/backs-aios-skills && ln -s ~/backs-aios-skills/skills/* ~/.claude/skills/

Proyecto: `cp -r ~/backs-aios-skills/skills/* .claude/skills/`

Symlink si quieres que las actualizaciones del pack fluyan solas; copia si quieres la
versión fijada (o si los symlinks le dan problemas a tu runtime). Abre una sesión
nueva. Una skill se dispara cuando la tarea coincide con su `description` — di las
palabras gatillo y el agente carga el archivo. En la ruta manual, las jugadas no son
skills: déjalas en el clon y dile al agente que lea una
(`read ~/backs-aios-skills/plays/elite-build.md`) al empezar la sesión, o pega tu
jugada por defecto en el CLAUDE.md del proyecto.

## 3. Cualquier runtime de Agent Skills (la convención abierta)

La convención está adoptada mucho más allá de Claude — OpenAI Codex, Gemini CLI,
Cursor, VS Code y más (según el ecosistema de la spec, 2026-08). Las reglas que
importan aquí: el archivo se llama exactamente `SKILL.md`; el nombre del directorio
es igual al `name` del frontmatter; solo `name` + `description` son obligatorios.
Este pack cumple las tres. Instalar = copiar `skills/*` a donde tu runtime guarde
las skills (Cursor usa `.cursor/skills/`, por ejemplo). No verificamos la carpeta de
cada runtime — revisa la documentación de tu plataforma para la ruta exacta.

## 4. OpenClaw, Hermes, otros frameworks de agentes

Confirmado contra su documentación actual (2026-08):

- **OpenClaw** descubre cualquier `SKILL.md` bajo sus raíces de skills configuradas.
  Copia `skills/*` a la carpeta `skills/` de tu workspace, o a la global compartida
  `~/.openclaw/skills`. La CLI `openclaw skills` maneja instalaciones y
  actualizaciones.
- **Hermes (Nous Research)** guarda una carpeta por skill en `~/.hermes/skills/`, y
  carga el SKILL.md de una skill dentro del system prompt cuando la tarea lo activa.
  Copia `skills/*` ahí.

Cualquier otro framework — el patrón genérico, sin código:

1. Monta o pega cada `SKILL.md` como contexto invocable por herramienta (una
   herramienta de documentos, una entrada en una librería de prompts, un almacén de
   recuperación). Mantén intacta la línea `description` — sus palabras gatillo son
   el contrato de invocación.
2. Carga una jugada (`plays/*.md`) como contexto de sistema para la sesión. Una
   jugada nombra las skills que dispara, en orden; el agente después trae cada skill
   por su nombre.
3. Verifica el mecanismo de instalación actual del framework en su propia
   documentación antes de confiar en este archivo — los mecanismos cambian rápido;
   aquí solo afirmamos lo que confirmamos arriba.

## 5. Bucle de API pelado (sin framework)

El harness eres tú. En cada vuelta:

1. Pon `skills/invariant-floor/SKILL.md` en el system prompt, siempre. Ese es el
   piso que todo cambio debe superar.
2. Elige la jugada que calce con el pedido — construir → `plays/elite-build.md`,
   bug → `plays/bughunt.md`, calificar → `plays/grading-verification.md` — y
   agrégala al final.
3. Compara las palabras del usuario con las palabras gatillo de la `description` de
   cada skill. Nunca inyectes el pack entero — inyecta de una a tres skills, las
   que calcen. El pack es liviano en tokens; mantenlo así.
4. Re-inyecta en cada reinicio de contexto. Una regla que se cayó del contexto no
   está cargada.

## Primera sesión

Instalación por plugin: escribe `/optimus` y dale la tarea. Instalación manual:

    Tú:     lee ~/.claude/skills/optimus/SKILL.md y arranca. Esta sesión lo sigue.
    Tú:     tarea — el total del checkout sale mal cuando se apilan un cupón y una gift card.
    Agente: [arranca: carga invariant-floor, elige plays/bughunt.md, nombra las skills que va a disparar]
    Tú:     dale.
    Agente: [la jugada conduce: reproducir, test rojo, arreglar la clase, verificar en vivo, calificar a ciegas, aterrizar]
