---
name: decision-bar
description: Nutze das, wenn du deinem Menschen gleich eine Frage stellen, auf Freigabe warten oder eine Entscheidung während autonomer Arbeit parken willst. Filtert jede Entscheidung durch eine Latte — nur Geschmack, Vision oder destruktives Risiko erreichen den Menschen; alles andere wird ausgeführt. Trigger words: ask-me bar, ask me, approval, permission, should I, decision, escalate, human in the loop, blocked on you, Freigabe, Erlaubnis, soll ich, Entscheidung, eskalieren, Rückfrage.
license: MIT
---

# Die Frag-mich-Latte

Agenten enttäuschen ihre Menschen auf zwei Arten: Sie unterbrechen mit Fragen, die
die Regeln längst beantworten, oder sie „surfacen“ eine echte Entscheidung an
einem Ort, den nie jemand sieht. Dieser Skill schließt beides.

## Die Latte

Eine Entscheidung erreicht den Menschen NUR, wenn sie wirklich seine ist:

- **Geschmack** — Stil, Wortwahl, Look, Gefühl; die Frage hat keine objektiv
  richtige Antwort.
- **Vision** — Richtung, Umfang, Produktabsicht; ein Fehlgriff verbiegt die Mission.
- **Destruktives Risiko** — Datenverlust, unumkehrbare Aktion, echtes Geld, echte
  Menschen.

Alles unterhalb dieser Latte WIRD AUSGEFÜHRT — aufgelöst aus den stehenden Regeln,
der eigenen Wahrheit des Projekts, der bekannten Absicht des Menschen und
vernünftigen Defaults. Null zusätzliche Reibung.

## Schritte

1. Fang den Moment. Du bist dabei zu fragen, zu warten oder zu vertagen. Halt an
   und leg die Latte an.
2. Prüfe: Ist das Geschmack, Vision oder destruktives Risiko? Wenn nichts davon —
   ist es keine Frage.
3. Unterhalb der Latte: erst suchen, dann fragen. Lies die stehenden Regeln und
   den Code noch mal. Die Antwort steht fast immer schon da. Löse es auf, führe
   aus, und notiere die Entscheidung in deinem Arbeitslog, damit der Mensch sie
   später prüfen kann.
4. An der Latte: LIEFERE die Frage. Eine klare Zusammenfassung der Lage, dann die
   Optionen als kurze Liste — als Buttons, wenn der Kanal des Menschen sie kann —
   auf dem Kanal, den der Mensch wirklich anschaut. Dann arbeite an allem weiter,
   was nicht von der Antwort abhängt.
5. Nie parken. Eine Entscheidung, die in einem Doc, einer Commit-Message, einer
   Ledger-Zeile oder einem langen Absatz liegt, existiert für den Menschen nicht.
   Eine geparkte Entscheidung ist ein verstecktes Gate.

## Harte Regeln (eine verletzt, und der Skill ist gescheitert)

- Etwas fragen, das aus stehenden Regeln, dem Code oder vernünftigen Defaults
  beantwortbar ist.
- Neue Freigabe-Maschinerie erfinden — ein Flag, eine Queue, einen
  Sign-off-Schritt — für Arbeit unterhalb der Latte. Verifikation darf dazu;
  Gates nicht.
- Eine Freigabe für eine Entscheidung fabrizieren, die die stehenden Regeln des
  Menschen längst getroffen haben.
- Eine echte Entscheidung irgendwo parken, wo der Mensch nicht aktiv hinschaut.
- „Fertig“ oder „grün“ von einer Proxy-Probe melden statt von der Oberfläche des
  Menschen — das Beweisgesetz lebt in [invariant-floor](../invariant-floor/SKILL.md).

## Passt gut zu

- [wayfinder](../wayfinder/SKILL.md) — bei Unbekanntem unterhalb der Latte die Route kartieren, statt zu fragen.
- [human-voice](../human-voice/SKILL.md) — das Register, in dem jede gelieferte Frage geschrieben ist.
- [invariant-floor](../invariant-floor/SKILL.md) — die stehenden Regeln, die vor jeder Frage nach oben noch mal gelesen werden.
