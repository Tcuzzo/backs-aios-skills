---
name: building-with-backs
description: "Beim Bauen oder Reparieren eines BACKS-Projekts, bei falschem Ordner oder unklarem Checkout oder beim Überführen einer autorisierten Änderung von der IDE in die tatsächliche Runtime."
license: MIT
---

# Building with BACKS

This skill closes a recurring failure: a good patch in the wrong checkout or a
green test that never reaches the operator's app. The destination is the human's
requested product and path. Discover the target before writing.

Nutze das bestehende [BACKS Build Flow](../backs-build-flow/SKILL.md)-Paket;
ein direkter Aufruf legt es einmal an. Bewahre einen Integrationsverantwortlichen
und bereits ermittelten Operator- und Ausführungskontext. Beachte `task_mode` und
übertrage Missionsfrist und Restkontingent von [bounded-loops](../bounded-loops/SKILL.md)
über Mitarbeiter, Modelle und Übergaben hinweg. Ein neu geklärter Pfad setzt kein
Budget zurück und autorisiert kein Deployment.

1. **Resolve the destination.** Use the exact path named by the human. If none was
   named, inspect the active workspace, recent project references, and repository
   map. Do not substitute a nearby clone merely because it has a matching name.
   Run `python scripts/resolve_target.py --repo <path> --target <file-or-directory>`
   from this skill's directory;
   add `--expected-root <path>` when the human named the checkout. The command
   returns nonzero for a missing target root, a path outside that root, or a
   checkout mismatch or missing Git revision. A new target file may not exist
   yet; its parent must. For a specifically named non-Git project, add
   `--allow-non-git` and record that no revision is available.
2. **Pin the starting truth.** Record the resolved root, branch or detached HEAD,
   `base_sha`, aktuellen `candidate_sha`, Arbeitsbaumzustand, gewünschtes Ziel,
   App-/Service-Einstiegspunkt und Prüfungen. Halte die ursprüngliche Basis bei
   weiteren Commits fest; aktualisiere Kandidatenidentität ausdrücklich und prüfe ausstehende Pfade erneut.
   Preserve unrelated edits. If another checkout is newer, compare revisions and
   actual working trees before choosing; "newest" is a measured claim.
3. **Map the route.** Trace user action to entry point, implementation, data,
   outputs, and deployment seam. Name the existing owner of the behavior and
   any dependent consumers. Use `repo-map`, `architecture-engineer`, and
   `root-cause-first` when those seams are uncertain.
4. **Am aufgelösten Ort bauen.** Gib parallelen Lesern verschiedene Fragen und
   Schreibern getrennte Dateien oder isolierte Worktrees. Bewahre einen
   Integrationsverantwortlichen. Schreibe die kleinste Änderung, die die
   Fehlerklasse schließt; wende `repair-loop` für einen Defekt im aktuellen Ablauf
   an. Folge dem vollständigen `elite-build`-Play, wenn es ausgewählt oder
   ausdrücklich angefordert ist, und verwende gültige Stufen weiter, statt neu zu
   booten. Ein Review oder eine Diagnose liefert Befunde ohne Änderungen.
5. **Den Pfad nachweisen.** Folge der aktuellen Schleife: versiegeltes RED →
   minimaler Fix → Sniper-Lint-/Typ-/Tests → clean-code-gauntlet. Leite Prüfungen
   aus dem festgehaltenen Gesamtdiff des Kandidaten ab; nutze echte Repository-
   Befehle und benenne fehlende oder nicht anwendbare Prüfungen ehrlich. Bewahre
   autor-disjunktes Review und den vorgeschriebenen Gesamtlauf betroffener Suiten
   zur Landung. Prüfe echte App-/CLI-Oberfläche und Runtime-Logs im angeforderten
   Umfang. Erfasse exakt deployte Quellrevision/Hash und beobachtetes Verhalten;
   benenne alles, was nicht ausgeführt werden konnte.
6. **Promote through the project's own route.** Read its deployment instructions
   and approval rules from that repository. Never transplant a deployment
   command from another project. Re-run the target check before installation
   and verify the running process uses the installed code afterward.

If the destination remains ambiguous, keep read-only investigation moving and
ask for the missing path only after checking available evidence. Never claim a
cross-host installation merely because files were copied; verify discovery in
each host or mark it unverified.

Bei erschöpftem Kontingent: Checkpoint **STILL-BUILDING** mit verifiziertem Ziel,
Kandidat, offenen Belegen und genauer nächster Handlung. Bewahre ursprüngliche
Missionsgrenzen; erledige nützliche autorisierte Arbeit, die das erschöpfte
Kontingent nicht verbraucht. Eine lokale Prüfung ersetzt keinen angeforderten Lieferbeleg.
