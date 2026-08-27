# Elite Build — das Master-Play

Das Default-Play für jede Anfrage der Art „bau X“, „fix X“ oder „uplift X“. Der
Mensch nennt das Ziel einmal; dieses Play baut die ganze Umgebung zusammen, sodass
er die Baseline nie neu erklären muss. Lies die Absicht, lade den Menschen, gate den
Plan, beweise ihn rot, baue, teste eng, miss, benote blind, lande.

## Wann dieses Play läuft

Jeder Build, Fix oder Uplift, bei dem wirklich etwas auf dem Spiel steht. Eine
triviale Ein-Zeilen-Änderung darf direkt zu
[sniper-testing](../skills/sniper-testing/SKILL.md) springen und landen.

## Die Kette

0. [optimus](../skills/optimus/SKILL.md) — boote den Harness, bevor irgendetwas
   editiert. Der Boden lädt zuerst, jede Session, jedes Mal.
1. [intent-compiler](../skills/intent-compiler/SKILL.md) — lies die Anfrage als die
   Spezifikation, als Ganzes. Leite die Absicht ab, bevor du irgendeine
   Auslieferungs- oder Optionsentscheidung hochreichst. Präsentiere niemals ein
   Optionsmenü, wenn eine klare Lösung existiert — löse es.
2. [human-calibration](../skills/human-calibration/SKILL.md) — lade das validierte
   Profil des Menschen und wende es an. Verhöre nie neu einen Menschen, den du
   schon kennst.
3. [understanding-gates](../skills/understanding-gates/SKILL.md) — Design → Plan →
   Build → Test → Ship, jede Stufe mit Gate. Vor jedem Design: Lies über
   [live-research](../skills/live-research/SKILL.md), was schon existiert, verwende
   wieder, was schon geschrieben ist, kartiere die ganze Topologie. Die Antwort
   steht meistens schon irgendwo.
4. [wayfinder](../skills/wayfinder/SKILL.md) — wenn du an irgendeinem Schritt
   verloren bist, zeichne die Route aus Beweisen. Parke niemals eine Frage beim
   Menschen, die Beweise beantworten können.
5. [red-first](../skills/red-first/SKILL.md) — schreibe den fehlschlagenden
   Contract-Test und committe ihn, BEVOR irgendein Builder läuft. Der Builder darf
   diesen Test nicht anfassen.
6. Baue. Fächere standardmäßig parallele Lanes auf — serialisiere nie, was
   gleichzeitig laufen kann. Jede Lane bekommt ihren eigenen Scratch-Branch oder
   ihr eigenes Worktree. Solo, eine Session? Dann IST eine Lane das Auffächern —
   bau auf einem Scratch-Branch und mach weiter. (Ein Worktree ist ein zweiter
   Checkout desselben Repos in einem anderen Ordner, damit zwei Builder nie
   dieselben Dateien anfassen.) Löse die Builder über
   [fleet-ladder](../skills/fleet-ladder/SKILL.md) auf; kombiniere Entwürfe mit
   [model-fusion](../skills/model-fusion/SKILL.md). Für einen Bug fahre den
   [repair-loop](../skills/repair-loop/SKILL.md) und schließe die KLASSE an der
   gemeinsamen Seam nach [seam-engineering](../skills/seam-engineering/SKILL.md).
7. [sniper-testing](../skills/sniper-testing/SKILL.md) — während der Iteration nur
   gescopte Läufe; der eine volle Durchlauf über die berührten Module wartet bis
   zur Landung (Schritt 10).
8. [clean-code-gauntlet](../skills/clean-code-gauntlet/SKILL.md) — miss vor der
   Landung: Sniper-Suite, Risiko-Score aus Komplexität mal Coverage unter deiner
   Obergrenze, dann Mutation-Tests bis auf null Überlebende. Miss den Code;
   beäuge ihn nie nur.
9. [blind-eval](../skills/blind-eval/SKILL.md), dann
   [blind-tribunal](../skills/blind-tribunal/SKILL.md) — ein Envelope ohne
   Autorenangabe geht an Prüfer aus einer anderen Modellfamilie als der Builder.
   Der Builder benotet nie seine eigene Arbeit. Jeder Juroren-Fund wird ein neuer
   roter Test; das Tribunal tagt neu, bis jeder Juror besteht. Solo-Rig?
   Degradiere nach der Solo-Rig-Regel im blind-tribunal — und benenne das
   geschwächte Gate im Landungsbericht.
10. Lande — merge sauber, fahre EINEN vollen Durchlauf über die Suiten der
    berührten Module, starte den echten Service neu und beweise das Verhalten auf
    der eigenen Oberfläche des Menschen (die Seite, die er lädt, das Kommando, das
    er ausführt) — niemals eine Proxy-Probe. Dann berichte.

## Harte Gates (ein einziges Rot blockiert die Landung)

- Der fehlschlagende Test wurde vor dem Build committet und ist unberührt — der
  Prüfer verifiziert, dass der Diff der Testdatei leer ist.
- Der Builder ist niemals der Prüfer, und der Prüfer ist eine andere Modellfamilie.
- Jeder aufgetauchte Fund ist geschlossen — oder mit dokumentierten Beweisen als
  „kein Bug“ beurteilt. Niemals still vertagt. Ganze-Seam-Schließung — die Seam
  ist die gemeinsame Stelle im Code, an der diese Bug-Klasse wohnt — oder keine
  Landung.
- Live-Beweis auf der echten Oberfläche des Menschen. Grüne Tests bei kaputter
  Fähigkeit sind Scheitern, nicht Erfolg.
- Berichte in zwei Worten — PROVEN oder STILL-BUILDING — in
  [human-voice](../skills/human-voice/SKILL.md). Proven heißt: gelandet, plus
  unabhängig benotet, plus live demonstriert.
- Committe nur die eigenen Dateien dieser Änderung — niemals die laufende Arbeit
  einer anderen Session.

## Passt gut zu

- [optimus](../skills/optimus/SKILL.md) — den Boden nach einer Kompaktierung oder einem Neustart neu booten
- [invariant-floor](../skills/invariant-floor/SKILL.md) — der festgeschriebene Boden, den jede Landung erfüllen muss
- [decision-bar](../skills/decision-bar/SKILL.md) — was den Menschen erreicht vs. was einfach ausgeführt wird
- [bounded-loops](../skills/bounded-loops/SKILL.md) — Budgets und Kill-Switches auf langen Läufen
- [session-handoff](../skills/session-handoff/SKILL.md) — den Zustand versiegeln, bevor du stoppst
