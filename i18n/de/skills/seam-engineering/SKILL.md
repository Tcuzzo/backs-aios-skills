---
name: "seam-engineering"
description: "Beim Reparieren eines Bugs oder beim Abschließen eines Audits oder einer Bug-Jagd. Fixt die Fehler-Klasse einmal an ihrem geteilten Primitiv, fegt jeden Geschwister-Fall mit, landet eine Wache, die die nächste Instanz fängt, und schließt jeden hochgekommenen Fund — kein stilles Vertagen. Trigger words: seam, class fix, whole-seam closure, point patch, structural guard, do it right the first time, Naht, Klassen-Fix, ganze Naht schließen, Punkt-Pflaster, strukturelle Wache, gleich beim ersten Mal richtig."
license: "MIT"
---

# Seam Engineering
**Effort:** free — pure Reparatur-Disziplin: ein Klassen-Fix am geteilten Primitiv statt N Punkt-Pflastern. Beseitigt: denselben Bug, an jeder Geschwister-Stelle noch einmal repariert, und den vertagten Medium-Befund, der zu dem Rätsel-Bug wird, den in sechs Monaten niemand mehr findet.

Eine Naht (im Code: die Stelle, an der alles zusammenläuft) ist korrekt und
vollständig geschlossen — oder sie ist nicht geschlossen. Der schnelle Patch
von heute ist der Bug, den in sechs Monaten niemand findet. Dieser Skill macht
aus einem Bug-Report eine geschlossene Klasse von Bugs.

## Wann einsetzen

Jede Reparatur: ein gemeldeter Bug, ein fehlgeschlagener Test, eine Fundliste
aus Audit oder Bug-Jagd. Besonders dann, wenn du den Drang spürst, „das hier
einfach kurz zu flicken".

## Schritte

1. **Grundursache mit Beweis.** Fix die Ursache, nicht das Symptom. Bevor du
   den Fix schreibst, zeig den Beleg: eine fehlschlagende Repro, eine
   Log-Zeile, ein Trace, der auf die echte Naht zeigt. Ein Fix ohne Beweis ist
   eine Vermutung.
2. **Benenn die Fehler-KLASSE.** Frag: welche Familie von Fehler ist das, und
   wo könnte derselbe Fehler noch wohnen? Schreib die Klasse in einem Satz auf.
3. **Fix vertikal — einmal, am geteilten Primitiv.** Das geteilte Primitiv ist
   die eine Funktion oder das eine Modul, durch das jedes Vorkommen fließt.
   Fix es dort. Nie N Punkt-Pflaster. Nie den-schlechten-Fall-markieren-und-
   kompensieren.
4. **Feg horizontal.** Such jedes Geschwister-Vorkommen der Klasse und fix sie
   in derselben Änderung, nicht „später“.
5. **Lande eine strukturelle Wache.** Ein Test oder automatischer Check, der
   bei der NÄCHSTEN Instanz der Klasse fehlschlägt. Die Klasse bleibt zu, weil
   etwas sie bewacht — nicht, weil alle dran denken.
6. **Schließ die ganze Naht.** List jeden Fund, den die Jagd hochgebracht hat.
   Vor dem Landen ist jeder entweder gefixt und grün, oder er trägt ein
   explizites, festgehaltenes „kein Bug“-Urteil mit Beweis. Nie ein stilles
   Vertagen. Nie „in einem Doc geparkt“.

## Harte Regeln

- **Eine Reparatur, die eine neue Fehlerbedingung einbaut, ist selbst ein
  Bug.** Ein Rollback-Helfer, der crashen kann, ein Aufräumer, der Zustand
  strandet, ein Test, umgebogen, um den Defekt zu segnen, den er fangen
  sollte — alles Bugs. Entwirf die Änderung neu, als eine atomare Einheit oder
  als explizite crash-sichere State-Machine. Nie drüber tapezieren.
- **„Die Schweren gefixt; der Rest sind Follow-ups“ reißt den Skill.** Genau
  diese Gewohnheit soll dieser Skill töten. Ein vertagter mittlerer Bug ist
  der Rätsel-Bug von morgen. Jeder Fund auf der Naht zählt gleich.
- **„Gut genug zum Landen“ ist kein Status.** Ist die Naht nicht richtig,
  iterier weiter — Blocker weg, auf ein stärkeres Modell oder einen stärkeren
  Reviewer eskalieren, neu versuchen — bis sie es ist.
- **Ein Punkt-Pflaster neben einem existierenden geteilten Primitiv reißt den
  Skill.** Besitzt ein Primitiv die Naht schon, reitet der Fix darauf; ein
  Vorbei-Fix erschafft die Klasse neu.
- **Ein entschiedenes „kein Bug“ braucht Beweis,** keine Abstimmung. Halt
  fest, was geprüft wurde und warum der Fund nicht hält.

## Passt gut zu

- [root-cause-first](../root-cause-first/SKILL.md) — die
  Untersuchungs-Disziplin hinter Schritt 1.
- [red-first](../red-first/SKILL.md) — der fehlschlagende Test, der den Fix
  beweist, und das Wachen-Muster für Schritt 5.
- [sniper-testing](../sniper-testing/SKILL.md) — gescopte Tests beim
  Iterieren; ein voller Durchlauf beim Landen.
- [repair-loop](../repair-loop/SKILL.md) — die End-zu-End-Schleife, in der
  diese Disziplin läuft.
- [incident-closure](../incident-closure/SKILL.md) — „fix es“ heißt voller
  Abschluss, nie ein Optionsmenü.
