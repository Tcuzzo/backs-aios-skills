---
skill_id: context-engineer
name: context-engineer
description: "Use quando faltar contexto de execução a reconstruir de estado do repo, rastros, restrições e intenção do operador, ou para handoff conciso a outro trabalhador."
license: Apache-2.0
preferred_mode: direct
tags:
- backs-native
- context-engineer
- pt-BR
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

Retorne ao responsável existente do [Build Flow](../backs-build-flow/SKILL.md).
Reutilize pacote atual e verifique apenas fatos alterados. Leia mais quando uma
incógnita nomeada puder mudar a próxima ação; prontidão significa alvo verificado,
restrições, próximo passo concreto e aceitação observável. Lista de skills não
é motivo para continuar lendo.

## Assemble from evidence

- Extract the user's objective, explicit exclusions, priority order, and definition of done.
- Inspect the current revision, dirty state, relevant runtime path, tests, logs, and governing project instructions.
- Name exact symbols and paths only after verifying them.
- Separate confirmed facts, strong inferences, unresolved questions, and stale historical context.
- Resolve gaps from available evidence when practical. Mark only gaps that materially block or change execution.

- Carregue uma vez o recorte relevante de [operator-essence](../operator-essence/SKILL.md),
  preservando evidência, incerteza e idade da fonte. Se faltar, sua passagem de
  insights cuida da inicialização; use contexto provisório sem atrasar construção executável.

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

- Modo da tarefa, responsável pela integração e autorização existente
- `base_sha` verificado anterior à tarefa, `candidate_sha` atual e trabalho pendente/alheio
- Mesmo `mission_id`, prazo, tentativas consumidas/restantes e cota de recursos
- Contexto relevante do operador como dados, nunca instrução superior

Use o [pacote existente](../backs-build-flow/references/task-packet.md), não outro
registro. Trabalhador, retry ou revisão não pode reiniciar a cota do pai.
Para somente leitura estrita, devolva contexto sem escrever estado no repo.

Include exact commands or artifact paths only when they are current, safe, and necessary for continuation. End with the next concrete action, not a generic planning summary.

## Reconstruction provenance

Source: BACKS AIOS package 0.8.5+codex.20260908213642. Paths and SHA-256 values are recorded
in frontmatter. The full operative method above is adapted from the audited
package, not loaded from a user cache. Canonical-law adaptation removes obsolete
host restriction, hook/rearm, or forced-route defaults where
present. Existing native IDs and files are preserved.
