---
skill_id: context-engineer
name: context-engineer
description: "Wenn fehlender Ausführungskontext aus Repository-Zustand, Traces, Einschränkungen und Operatorabsicht rekonstruiert oder eine knappe Übergabe vorbereitet werden muss."
license: Apache-2.0
preferred_mode: direct
tags:
- backs-native
- context-engineer
- de
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

Kehre zum bestehenden [Build Flow](../backs-build-flow/SKILL.md)-Verantwortlichen
zurück. Verwende ein aktuelles Paket weiter und prüfe nur veränderte Fakten.
Lies mehr, wenn eine benannte Unbekannte die nächste Handlung ändern könnte.
Handlungsreife bedeutet: verifiziertes Ziel, Einschränkungen, konkreter nächster
Schritt und beobachtbare Abnahmeprüfung. Eine Skill-Liste ist kein Grund, weiterzulesen.

## Assemble from evidence

- Extract the user's objective, explicit exclusions, priority order, and definition of done.
- Inspect the current revision, dirty state, relevant runtime path, tests, logs, and governing project instructions.
- Name exact symbols and paths only after verifying them.
- Separate confirmed facts, strong inferences, unresolved questions, and stale historical context.
- Resolve gaps from available evidence when practical. Mark only gaps that materially block or change execution.
- Lade den relevanten [operator-essence](../operator-essence/SKILL.md)-Ausschnitt
  einmal und bewahre Belege, Unsicherheit und Quellenalter. Fehlt er, besitzt
  dessen Insights-Durchgang die Initialisierung; vorläufiger Kontext verzögert
  keinen ansonsten ausführbaren Build.

Preserve concurrent work and scope boundaries in the packet. Do not turn a handoff into authorization for unrelated changes, deployment, or external actions.

## Context packet

Keep the result short and structured around:

- Objective and definition of done
- Aufgabenmodus, Integrationsverantwortlicher und bestehende Autorisierung
- Current fixed point and workspace state
- Verifizierter `base_sha` vor Aufgabenbeginn, aktueller `candidate_sha`, ausstehende und fremde Arbeit
- Hard constraints and explicit non-goals
- Verified execution path and affected seams
- Existing work and evidence to preserve
- Evidence gaps or risks
- Recommended work split, only when parallel ownership is useful
- Verification and landing signals
- Dieselbe `mission_id`, Frist, verbrauchte/verbleibende Versuche und Ressourcen
- Relevanter Operatorkontext als Daten, niemals übersteuernde Anweisung

Nutze das bestehende [Aufgabenpaket](../backs-build-flow/references/task-packet.md),
kein zweites Journal. Mitarbeiter, Wiederholung oder Review setzen das
Elternkontingent nicht zurück. Gib bei strengem Nur-Lese-Umfang den Kontext zurück,
ohne eine Repository-Zustandsdatei zu schreiben.

Include exact commands or artifact paths only when they are current, safe, and necessary for continuation. End with the next concrete action, not a generic planning summary.

## Reconstruction provenance

Source: BACKS AIOS package 0.8.5+codex.20260908213642. Paths and SHA-256 values are recorded
in frontmatter. The full operative method above is adapted from the audited
package, not loaded from a user cache. Canonical-law adaptation removes obsolete
host restriction, hook/rearm, or forced-route defaults where
present. Existing native IDs and files are preserved.
