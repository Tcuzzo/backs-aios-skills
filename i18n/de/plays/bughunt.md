# Play: Bughunt

Eine begrenzte, parallele Bug-Jagd. Zeichne die Jagd als Karte, fächere Finder darüber
aus, verifiziere jeden Fund adversarial und schließe ganze Seams — eine Seam ist die
gemeinsame Stelle im Code, an der eine Fehlerklasse wohnt — niemals einzelne Symptome.

## Wann dieses Play läuft

- Ein Audit, ein Sweep oder eine Jagd über viele Seams — nicht ein einzelner
  gemeldeter Bug (dafür ist der Repair-Loop da).
- Ein Rückstau an Funden muss parallel angegriffen werden, ohne Drift und ohne dass
  sich Lanes gegenseitig zertrampeln.

## Gemeinsame Aufgabe und Grenzen

Wende dieses Play im aktuellen [BACKS Build Flow](../skills/backs-build-flow/SKILL.md)-
Aufgabenpaket an. Bewahre einen Integrationsverantwortlichen, gewünschten
`task_mode`, feste Basis- und Kandidatenrevisionen, Operator-Essence und aktuelle
Belege. Verwende passende geladene Skill-Texte weiter; dieses Play ergänzt seine
Fachprüfungen, ohne die Aufgabe neu zu starten.

[bounded-loops](../skills/bounded-loops/SKILL.md) besitzt ursprüngliche Frist und
Restkontingente über Wiederholungen, Mitarbeiter, Modelle, Reviews und Übergaben
hinweg. Setze sie für ein verschachteltes Play nie zurück. Bei Erschöpfung:
**STILL-BUILDING** mit Kandidat, Belegen, offenen Gates und nächster Handlung
sichern. Nützliche autorisierte Arbeit bleibt im Restkontingent; kein fehlendes
Gate wird zum bestandenen erklärt.

## Die Kette

1. [wayfinder](../skills/wayfinder/SKILL.md) — zeichne die Jagd ZUERST als eine
   Karte mit einem Knoten pro Seam oder Fund. Finder beanspruchen Knoten atomar von
   der Frontier; wer einen Knoten schließt, schreibt die Frage des nächsten. Nichts
   wird abseits der Karte erfunden.
2. [leap-protocol](../skills/leap-protocol/SKILL.md) — jeder Knoten ist ein Ball:
   Ziel, Spezifikation, harter Datei-Scope, begrenzte Runden, dreiwertiges Ergebnis.
   Verwandte Bälle fahren auf einer nach Abhängigkeiten geordneten Slice mit genau
   EINEM Schreiber.
3. [root-cause-first](../skills/root-cause-first/SKILL.md) — reproduziere den Bug
   und prüfe die Root-Cause-Beweise, BEVOR sich am Code irgendetwas ändert. Keine
   Mutation auf eine Vermutung hin.
4. [repair-loop](../skills/repair-loop/SKILL.md) — innere Disziplin jedes Balls:
   [red-first](../skills/red-first/SKILL.md)-Fehlertest vor dem Fix committet,
   echte Lint-/Typ-/Tests mit [sniper-testing](../skills/sniper-testing/SKILL.md)
   aus dem festgehaltenen Kandidatengesamtdiff, einmal volle betroffene Modulsuiten
   zur Landung. Bewahre ursprüngliches RED; neue Befunde erhalten separate
   Ergänzungstests. Gib Belege an den Jagdverantwortlichen zurück, ohne ein Play neu zu starten.

5. [blind-tribunal](../skills/blind-tribunal/SKILL.md) — jeder Fund wird
   adversarial angegriffen: Ein Prüfer, der ihn nicht verfasst hat, greift mit
   Ablehnen-als-Default an; Juroren beurteilen ein Envelope ohne Autorenangabe.
   Der Builder benotet nie seine eigene Arbeit.
6. [seam-engineering](../skills/seam-engineering/SKILL.md) — schließe die KLASSE
   an der gemeinsamen Seam, niemals das einzelne Symptom.
7. [clean-code-gauntlet](../skills/clean-code-gauntlet/SKILL.md) — der
   Abschlussbeweis: Der gefixte Branch muss unter Mutation STERBEN. Ein Abschluss,
   dessen Mutant überlebt, ist unbewiesen — der Fund bleibt offen.

## Wann ein Ball schließt

Ein Ball schließt nur über das Score-Gate des
[leap-protocol](../skills/leap-protocol/SKILL.md) — Quellen-Wahrheit,
Keep-or-Revert, blinde Review, Live-Beweis, Provenienz; fehlende Beweise werden
niemals als bestanden gewertet. Jagd-spezifische Endzustände: Jeder Fund endet als
FIXED oder REFUTED-WITH-EVIDENCE (gefixt oder mit Beweisen widerlegt).

Ein erschöpftes Kontingent lässt den Befund mit einem STILL-BUILDING-Checkpoint
offen; es ist kein terminales FIXED oder REFUTED-WITH-EVIDENCE. Bewahre
Versuchshistorie und verbleibende Missionsgrenzen vor dem nächsten erlaubten Knoten.

## Regeln der Jagd

- Senke dein Vertrauen in dich selbst. Erde dich neu am Ledger und an der
  Versuchs-Historie des Knotens, nie an deinem eigenen Gedächtnis. Neustart heißt:
  neu von der Frontier beanspruchen; übergib über
  [session-handoff](../skills/session-handoff/SKILL.md).
- Streame den Fortschritt laufend in menschlicher Sprache. Unbekannt bleibt
  unbekannt — es wird niemals zu „bestanden“.
- Sobald Kandidaten-Bytes, Kommandos, Tests und Urteil eingefroren sind, ist das
  Landen ein deterministisches Replay. Kein Modell-Call entscheidet ein bereits
  entschiedenes Kommando neu.
- Respektiere die Kiste: Miss die Ressourcen vor dem Spawnen, begrenze die
  Parallelität, räume tote Lanes ab, stoppe LAUT nach einem zweiten Tod am selben
  Knoten, drossle jeden externen Call. Der Kill-Switch stoppt neue Claims —
  niemals eine Mutation mitten im Flug.
- Benenne die Verschwendung jeder Slice und miss vorher/nachher. Nimm einen
  Effizienzgewinn nur, wenn ein Vergleichslauf null Fähigkeitsverlust beweist;
  Über-Bloat ist genauso ein Defekt.
- Berichte in zwei Worten: PROVEN oder STILL-BUILDING.

## Harte Gates — eines reicht, und das Play ist gescheitert

- Eine Mutation, bevor reproduzierte Root-Cause-Beweise geprüft wurden.
- Ein Builder, der seinen eigenen Fund benotet.
- Ein Fund, der geschlossen wurde, während auf dem gefixten Branch ein Mutant
  überlebt.
- Ein Volllauf der Suite mitten in der Jagd — snipe nur die eigene Seam des Funds.
- Mock-Theater in einem Abschluss-Test: Es öffnet den Bug still wieder, während
  das Ledger behauptet, er sei zu.
- Ein Fund, der still geparkt oder ohne Fix oder belegte Widerlegung als geschlossen markiert wurde.

**Weight:** free-Jagd-Disziplin im Kern; der heavy-Einsatz ist dreifach — LEAP-Fan-out, das adversariale Tribunal und der Mutations-Beweis jedes Abschlusses — er zahlt sich aus, wenn ein ganzer Backlog parallel schließt und jeder Abschluss unter Mutation bewiesen ist.
