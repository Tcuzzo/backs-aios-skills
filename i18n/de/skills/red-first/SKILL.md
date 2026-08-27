---
name: red-first
description: Beim Losschicken jedes Builders — ein Agent, ein Modell oder du selbst — für eine Änderung, die ein Test beweisen soll. Committet einen bewiesen fehlschlagenden Vertrags-Test, bevor der Build startet, verbietet dem Builder, ihn anzufassen, und lässt einen unabhängigen Bewerter prüfen, dass der Test nie editiert wurde. Trigger words: red first, failing test first, contract test, red baseline, tamper-proof test, test before build, erst der rote Test, fehlschlagender Test zuerst, Vertrags-Test, rote Baseline, Test vor dem Build.
license: MIT
---

# Red-First, manipulationssicher

Ein Test, der nach dem Fix geschrieben wird, beweist nichts — er wurde
passend geformt. Ein Test, den der Builder editieren kann, beweist noch
weniger — er lässt sich zum Bestehen verbiegen. Also kommt der Test zuerst,
wird versiegelt und unangetastet bewertet.

## Wann einsetzen

Vor dem Losschicken jedes Builds oder Fixes, bei dem ein Test das gewollte
Verhalten festhalten kann. Das ist der Default für Bugfixes wie für neue
Fähigkeiten.

## Schritte

1. **Schreib den fehlschlagenden Vertrags-Test.** Er benennt das Verhalten,
   das du willst — in der kleinsten Form, die sein Fehlen fangen würde. Er muss
   jetzt sofort fehlschlagen.
2. **Beweis, dass er rot ist.** Lass den Test laufen und sieh ihm beim
   Fehlschlagen zu — aus dem richtigen Grund. Ein Test, der beim Import einen
   Fehler wirft oder still durchläuft, ist nicht rot. Ein roter Test, den
   niemand laufen ließ, ist eine Vermutung, keine Baseline.
3. **Committe den roten Test, BEVOR du den Builder losschickst.** Notier die
   Commit-Id. Dieser Commit ist die rote Baseline — das Manipulations-Siegel.
4. **Schick den Builder mit einem Job los: mach ihn grün.** Dem Builder ist
   verboten, die Test-Datei anzufassen. Sag das im Auftrag ausdrücklich.
5. **Bewerte unabhängig.** Ein Bewerter, der die Änderung nicht geschrieben
   hat, prüft zwei Dinge:
   - der Test besteht jetzt;
   - die Test-Datei ist Byte für Byte identisch mit der roten Baseline —
     `git diff <red-sha> HEAD -- tests/test_contract.py` gibt nichts aus.
   Jeder Diff auf der Test-Datei lässt die Bewertung durchfallen. Keine
   Ausnahmen, auch nicht „nur ein Tippfehler-Fix“.
6. **Zieh eine strukturelle Wache zehn Punkt-Tests vor.** Eine strukturelle
   Wache ist ein Check (ein grep-Durchlauf, ein AST-Scan, eine Lint-Regel),
   der beim NÄCHSTEN Verstoß fehlschlägt, nicht nur bei diesem einen. Eine
   Wache schlägt zehn Punkt-Tests, die je einen Fall festnageln.

## Harte Regeln

- **Rot muss bewiesen rot sein.** Laufen lassen, fehlschlagen sehen — vorher
  zählt es nicht.
- **Der Builder editiert den Test nie.** Der leere Test-Datei-Diff seit der
  roten Baseline gehört zum Landegate, er ist keine Höflichkeitsprüfung.
- **Der Builder ist nie der Bewerter.** Nimm eine andere Person, einen anderen
  Agenten oder ein Modell aus einer anderen Familie als der des Builders.
- **Grün allein ist kein Beweis.** Grün + unangetasteter Test + unabhängige
  Bewertung ist Beweis.
- **Steht eine ganze Defekt-Klasse im Raum, bewache die Klasse.** Punkt-Tests
  stoppen diesen Bug; eine strukturelle Wache stoppt den nächsten.

## Passt gut zu

- [sniper-testing](../sniper-testing/SKILL.md) — beim Iterieren nur die Tests
  fahren, die die Änderung berührt; ein voller Durchlauf beim Landen.
- [seam-engineering](../seam-engineering/SKILL.md) — die Klassen-Fix-Disziplin,
  zu der die strukturelle Wache gehört.
- [blind-tribunal](../blind-tribunal/SKILL.md) — unabhängige Bewerter, die den
  Autor nie gesehen haben.
- [repair-loop](../repair-loop/SKILL.md) — die Schleife, die rot → grün →
  bewiesen von Anfang bis Ende trägt.
