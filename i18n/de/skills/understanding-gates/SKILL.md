---
name: understanding-gates
description: Wenn ein Build, Fix oder Uplift von der Absicht Richtung Auslieferung wandert und du Beweis brauchst, dass er noch zur ursprünglichen Bitte passt. Verhört Design, Plan, Build, Test und Ship mit approve/revise/reject-Urteilen, benannten Fehlschlägen als Reparatur-Zielen und einem Wiederholungslauf nach jeder Reparatur. Trigger words: understanding, stage gates, validate build, spec match, verdict, green but wrong, echo check, done means done, Verständnis, Stufen-Gates, Build validieren, Urteil, grün aber falsch, fertig heißt fertig.
license: MIT
---

# Understanding Gates
**Effort:** light — ein Validator-Durchgang pro Stufe, gescored gegen die ursprüngliche Bitte und nach jeder Reparatur neu gefahren. Beseitigt: Drift, validiert gegen eine Paraphrase — den Build, der grün landet, aber eine Frage beantwortet, die niemand gestellt hat.

Eine Validierungs-Disziplin für Builds. Sie verhört die Arbeit an fünf Stufen — Design, Plan, Build, Test, Ship — immer gegen die URSPRÜNGLICHE Bitte, nie gegen die eigene Nacherzählung der Arbeit. Jedes Gate liefert Beweise zurück: Scores, ein Urteil, benannte Fehlschläge und Reparatur-Aktionen. Es bindet den Agenten, nicht den Menschen: kein neuer Freigabe-Schritt, keine Reibung für die Person, die gefragt hat.

## Wann einsetzen

- Jeder Build, Fix oder Uplift, der irgendwo real landet.
- Jedes Mal, wenn du gleich „fertig“ sagen willst und der einzige Beweis ein grüner Test ist.
- Nach jeder Reparatur, auf derselben Stufe, die gescheitert ist.

## Stufe 0 — die Absicht verankern

Bevor irgendwas gescored wird, fixier den Vergleichs-Anker: die ORIGINAL-Worte des Menschen, plus eine einzeilige übersetzte Direktive (siehe [intent-compiler](../intent-compiler/SKILL.md)). Jedes Gate scored gegen diesen Anker. Score nie gegen deine eigene Paraphrase — eine Paraphrase driftet, und dann validiert jedes Gate leise die Drift statt die Bitte.

## Die fünf Gates

Jedes Gate stellt eine Frage gegen die ursprüngliche Absicht:

| Stufe | Frage |
| --- | --- |
| Design | Ist die Spec klar und treu zur ursprünglichen Bitte? |
| Plan | Beantwortet der Plan die Absicht und passt er zu der Fläche, auf die er ausliefert? |
| Build | Erfüllt der Code die Spec ohne Drift? |
| Test | Üben die Tests das echte Verhalten aus, nicht einen Stellvertreter davon? |
| Ship | Lässt es sich sauber anwenden, scheitert es laut, und übersteht die Auslieferungs-Behauptung einen Faktencheck? |

Score JEDES Gate auf denselben fünf Linsen, jede 0–4: Spec-Treffer, Architektur-Passung, Typ-Sicherheit, Testbarkeit, Sicherheit — formuliert für die Stufe (bei Design fragt „Testbarkeit“, ob die Spec prüfbar ist; bei Ship, ob die Auslieferungs-Behauptung es ist). Roll-up: die fünf Linsen summieren (0–20), mit 5 multiplizieren — das ist der 0–100-Urteils-Score des Gates. Halt jede Linse fest, nicht nur die Summe — die Summe versteckt, welche Linse gescheitert ist.

## Urteile

Roll die Linsen in einen 0–100-Score und band ihn:

- **Approve** (80+): starker Beweis. Trotzdem kein Beweis für fertig — siehe das zweite Gesetz.
- **Revise** (60–79): benannte Fehlschläge existieren. Jeder ist ein Reparatur-Ziel.
- **Reject** (unter 60): die Arbeit verfehlt die Absicht. Geh eine Stufe zurück.

Ein Urteil ohne benannte Fehlschläge dahinter ist ein Urteil mit wenig Information. Verlang die Liste.

## Reparatur-Disziplin

1. Halt die ursprüngliche Absicht als Anker für jeden Wiederholungslauf.
2. Halt die Scores pro Linse fest, nicht nur die Kopfzahl.
3. Behandle jeden benannten Fehlschlag als Reparatur-Ziel. Kein Fehlschlag ist Deko.
4. Reparier, dann FAHR DASSELBE GATE NEU. Eine Reparatur ohne Wiederholungslauf ist nur eine Behauptung.
5. Befördere Zuversicht nie zu Bereitschaft. Tests und die echte Fläche entscheiden.

## Die zwei Gesetze

**1. Das Echo-Gesetz.** Ein Check, der nur zustimmen kann, ist ein Echo, kein Validator. Der Ehrlichkeits-Beweis ist Widerlegung: füttere ihm eine Behauptung, von der du weißt, dass sie falsch ist, und sieh ihn diese Behauptung durchfallen lassen. Winkt er die Lüge durch, ist der Check Theater. Korollar zum Mocken: mock nur das instabile externe Blatt — eine bezahlte API, ein flatterhaftes Netz. Mock nie das Organ, dessen Verhalten DER Beweis ist; sein Scoring, seine Behauptungs-Extraktion und seine Pass/Fail-Logik müssen echt laufen.

**2. Notwendig, nicht hinreichend.** Ein bestandener Test ist notwendig, nie hinreichend. Fertig heißt: die echte Fläche — die, die der Mensch wirklich nutzt — macht den Job von allein. Benenn diese Fläche, stoß den echten Pfad an und sieh das korrekte Ergebnis ankommen. Befördere nie einen Unit-Test-Beleg zu einer Live-Fähigkeits-Behauptung.

## Harte Regeln (was diesen Skill reißen lässt)

- Gegen eine Paraphrase scoren statt gegen die ursprüngliche Bitte.
- Ein Revise- oder Reject-Urteil ohne angehängte benannte Fehlschläge.
- Reparieren, ohne das gescheiterte Gate neu zu fahren.
- Den Validator selbst mocken, oder genau die Naht, die geändert wird.
- Fertig behaupten aus einem grünen Test ohne Beweis auf der echten Fläche.

## Führ einen Build-Datensatz

Für jede Stufe halt fest: die Absicht, das exakte Eingabe-Artefakt, die Scores, die benannten Fehlschläge, die durchgeführte Reparatur, das Ergebnis des Wiederholungslaufs und den Beweis von der echten Fläche. Ein Datensatz, der nicht auf reproduzierbare Beweise zeigt, ist ein Banner, kein Datensatz.

## Passt gut zu

- [intent-compiler](../intent-compiler/SKILL.md) — übersetz die Bitte, bevor du sie scorst.
- [red-first](../red-first/SKILL.md) — der Vertrag des Test-Gates: fehlschlagender Test zuerst committet.
- [sniper-testing](../sniper-testing/SKILL.md) — echte Nebeneffekte, kein Mock-Theater.
- [blind-tribunal](../blind-tribunal/SKILL.md) — unabhängige Bewerter oben auf diesen Gates.
- [repair-loop](../repair-loop/SKILL.md) — die Schleife, die Revise-Urteile auf grün treibt.
