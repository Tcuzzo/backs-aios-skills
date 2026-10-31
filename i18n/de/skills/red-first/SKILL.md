---
name: "red-first"
description: "Vor dem Dispatch eines Builders für eine durch Tests beweisbare Verhaltensänderung oder wenn ein Reviewbefund oder eine Mutationslücke einen Regressionsvertrag braucht. Trigger words: red first, failing test first, contract test, red baseline, tamper-proof test, test before build, erst der rote Test."
license: "MIT"
---

# Red-First, manipulationssicher
**Effort:** free — pure Reihenfolge-Disziplin: Der Test, den du ohnehin schreiben würdest, wird zuerst geschrieben, rot bewiesen und mit einem Commit versiegelt; der Manipulations-Check ist ein einzelnes git diff. Beseitigt: Tests, die nach dem Fix aufs Bestehen zugeschnitten wurden, und grüne Urteile, die ein Builder durchs Editieren des Tests verbogen hat.

Ein grünes Ergebnis, das erst nach dem Fix beobachtet wurde, belegt weder den
ursprünglichen Fehler noch, dass der Test ihn erkennen kann. Weise das ursprüngliche
RED vor dem Fix nach und versiegle es; der Builder lässt diese Datei unverändert.
Ein separater Ergänzungstest kann später an einem kontrollierten Mutanten scheitern
und am Kandidaten ohne Mutation bestehen, wie unten beschrieben.

Nutze das aktuelle [BACKS Build Flow](../backs-build-flow/SKILL.md)-Paket. Dieser
Skill besitzt das RED-Siegel, keinen zweiten Build-Verantwortlichen oder Ablauf.
Bewahre festen `base_sha`, aktuellen `candidate_sha` und Missionsidentität.
Frist und Restversuche aus [bounded-loops](../bounded-loops/SKILL.md) gelten für
Reproduktion, Builder, Ergänzungstests und unabhängige Reviews. Verwende einen
gültigen RED-Beleg weiter, statt einen neuen Fehler zu erzeugen.

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
3. **Committe den roten Test VOR dem Builder-Dispatch.** Erfasse Commit-ID,
   genaue Testpfade und Bytes, fehlgeschlagenen Befehl/Ausgabe und Grund. Dieser
   Commit ist die rote Baseline und das Manipulationssiegel. Er ersetzt nicht
   den festen `base_sha` der Mission für den Gesamtumfang der Änderung.
4. **Schick den Builder mit einem Job los: mach ihn grün.** Dem Builder ist
   verboten, die Test-Datei anzufassen. Sag das im Auftrag ausdrücklich.
5. **Bewerte unabhängig.** Ein Bewerter, der die Änderung nicht geschrieben
   hat, prüft zwei Dinge:
   - der Test besteht jetzt;
   - die Test-Datei ist Byte für Byte identisch mit der roten Baseline —
     `git diff <red-sha> <candidate_sha> -- tests/test_contract.py` gibt nichts aus.
     Beziehen Prüfungen ausstehende Arbeit ein, vergleiche auch die tatsächlich
     getesteten Dateibytes mit dem Siegel; ein leerer Commit-Diff entschuldigt
     keine gestagte oder ungestagte Änderung.
   Jeder Diff auf der Test-Datei lässt die Bewertung durchfallen. Keine
   Ausnahmen, auch nicht „nur ein Tippfehler-Fix“.
6. **Zieh eine strukturelle Wache zehn Punkt-Tests vor.** Eine strukturelle
   Wache ist ein Check (ein grep-Durchlauf, ein AST-Scan, eine Lint-Regel),
   der beim NÄCHSTEN Verstoß fehlschlägt, nicht nur bei diesem einen. Eine
   Wache schlägt zehn Punkt-Tests, die je einen Fall festnageln.

## Ein neuer Befund nach dem ursprünglichen Siegel

Ein überlebender Mutant oder Reviewbefund kann eine fehlende Assertion zeigen.
Bewahre die ursprüngliche RED-Datei Byte für Byte und lege eine **separate
Ergänzungstestdatei** an. Beobachte deren Fehler für den neuen Defekt vor dem Fix;
weise bei einer Mutationslücke isoliert das Scheitern am kontrollierten Mutanten
und das Bestehen am unmutierten Kandidaten nach. Erfasse und versiegle den
Zusatzbeleg, bevor der nächste Builder diese Schnittstelle ändert. Behaupte nicht,
dies sei die ursprüngliche Baseline. Der Prüfer kontrolliert beide Siegel und den
genauen Gesamtkandidaten. Ein neuer Test erlaubt niemals Abschwächen, Umbenennen
oder Ersetzen des ursprünglichen Vertrags.

Ist das gemeinsame Budget erschöpft oder RED nicht belegbar, sichere
**STILL-BUILDING** mit Lücke und genauer nächster Handlung. Erfinde kein RED und
starte die Mission nicht neu, um ein grünes Ergebnis zu erzwingen.

## Harte Regeln

- **Rot muss bewiesen rot sein.** Laufen lassen, fehlschlagen sehen — vorher
  zählt es nicht.
- **Der Builder editiert den Test nie.** Der leere Test-Datei-Diff seit der
  roten Baseline gehört zum Landegate, er ist keine Höflichkeitsprüfung.
- **Der Builder ist nie der Bewerter.** Nimm einen nicht-vom-Builder
  stammenden Prüfer, live nach Fähigkeit und Verfügbarkeit aus der
  konfigurierten Sprossen-Matrix gewählt; die ausführende Session, die gebaut
  hat, und jede Session, die die Konversation oder den Kontext des Builders
  geerbt hat, sind disqualifiziert. Der Prüfer arbeitet in einer frischen,
  autor-disjunkten Session.
- **Grün allein ist kein Beweis.** Grün + unangetasteter Test + unabhängige
  Bewertung belegen diesen Vertrag; eine Live-Fähigkeitsbehauptung braucht weiterhin
  echte Oberflächen- und Lieferbelege aus dem Aufgabenablauf.
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
