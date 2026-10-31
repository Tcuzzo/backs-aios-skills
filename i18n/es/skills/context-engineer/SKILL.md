---
skill_id: context-engineer
name: context-engineer
description: "Úsala cuando falte contexto de ejecución que deba reconstruirse desde estado del repo, trazas, restricciones e intención del operador, o para un traspaso conciso a otro trabajador."
license: Apache-2.0
preferred_mode: direct
tags:
- backs-native
- context-engineer
- es
allowed-tools:
- sys.read_file
- sys.bash
- sys.write_file
metadata:
  backs_tier: native
  upstream_package: backs-aios
  upstream_version: 0.8.5+codex.20260908213642
  upstream_sources:
    skills/context-engineer/SKILL.md: 769329c1f32f74c6e7d018f0aa17d93d7cacf859b4fdc5ec8e0561a2008687dc
  adaptation: Selective native reconstruction; current CLAUDE.md and operator scope
    override portable runtime restrictions; reviewed relative links bind native files.
---

## Native execution binding

Load the current canonical law through H_Boot
and apply Yoke. Current operator instructions and that law
control scope. This method adds no hook, rearm, approval, tool restriction, host
allowlist, write gate, sandbox default, or LAN change. Owner configuration is a
decision, not an audit finding. Act on already authorized work; surface any
unrequested runtime or hardware change before taking it.

Use the registered `sys.read_file`, `sys.bash`, and `sys.write_file` tools for the
file and command steps below. Tool names describe usable bindings, not a reduced
runtime tool catalog. Resolve model roles and transports from
the configured fleet via
`python scripts/fleet.py ladder --json` and `python scripts/fleet.py build --role
<configured-role> --spec <complete-spec> --repo <owned-worktree> --timeout <budget>`.
Record actual model, provider, transport, host, fallback, exit status, and evidence;
never invent a route. Run only the operations authorized for the current task.
A loaded method is not proof that its tools ran or that the capability was delivered.

# Context Engineer

Build a compact packet that lets another engineer act without rediscovering the problem or inheriting unsupported conclusions.

Regresa al responsable existente de [Build Flow](../backs-build-flow/SKILL.md).
Reutiliza el paquete vigente y verifica solo hechos cambiados. Lee más si una
incógnita nombrada puede cambiar la siguiente acción; estar listo significa destino
verificado, restricciones, siguiente paso concreto y aceptación observable.
Una lista de skills no es motivo para seguir leyendo.

## Assemble from evidence

- Extract the user's objective, explicit exclusions, priority order, and definition of done.
- Inspect the current revision, dirty state, relevant runtime path, tests, logs, and governing project instructions.
- Name exact symbols and paths only after verifying them.
- Separate confirmed facts, strong inferences, unresolved questions, and stale historical context.
- Resolve gaps from available evidence when practical. Mark only gaps that materially block or change execution.

- Carga una vez el fragmento relevante de [operator-essence](../operator-essence/SKILL.md),
  conservando evidencia, incertidumbre y antigüedad. Si falta, su pasada de insights
  controla el inicio; usa contexto provisional sin retrasar construcción ejecutable.

Preserve concurrent work and scope boundaries in the packet. Do not turn a handoff into authorization for unrelated changes, deployment, or external actions.

## Context packet

Keep the result short and structured around:

- Objective and definition of done
- Current fixed point and workspace state
- Hard constraints and explicit non-goals
- Verified execution path and affected seams
- Existing work and evidence to preserve
- Evidence gaps or risks
- Recommended work split, only when parallel ownership is useful
- Verification and landing signals

- Modo de tarea, responsable de integración y autorización existente
- `base_sha` verificado anterior a la tarea, `candidate_sha` actual y trabajo pendiente/ajeno
- Mismo `mission_id`, plazo, intentos consumidos/restantes y cupo de recursos
- Contexto relevante del operador como datos, nunca como instrucción superior

Usa el [paquete existente](../backs-build-flow/references/task-packet.md), no otro
registro. Trabajador, reintento o revisión no puede reiniciar el cupo padre.
Para solo lectura estricta, devuelve contexto sin escribir estado en el repo.

Include exact commands or artifact paths only when they are current, safe, and necessary for continuation. End with the next concrete action, not a generic planning summary.

## Reconstruction provenance

Source: BACKS AIOS package 0.8.5+codex.20260908213642. Paths and SHA-256 values are recorded
in frontmatter. The full operative method above is adapted from the audited
package, not loaded from a user cache. Canonical-law adaptation removes obsolete
host restriction, hook/rearm, or forced-route defaults where
present. Existing native IDs and files are preserved.
