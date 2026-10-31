---
skill_id: operator-intent-deduction
name: operator-intent-deduction
description: "Wenn eine offene Implementierungswahl, Abwägung oder vorgeschlagene Operatorfrage vorliegt und aktuelle Absicht, Projektbelege oder Operatorkontext bereits eine Entscheidung tragen könnten."
license: MIT
---

# Entscheidungen aus aktuellen Belegen ableiten

Löse Entscheidungen, die ein Agent verantwortlich selbst lösen kann, und handle.
Nutze Ziele und Belege des aktuellen Operators; dieser Skill enthält keine
permanenten Prioritäten, Finanzziele, numerischen Risikovorgaben oder Modelllisten einer Person.

## Eingaben und Verantwortung

Beginne mit vorhandener Direktive, Aufgabenmodus, Abnahmekriterien, Autorisierung
und Missionsrestbudget. Ist die Sprache noch nicht ausgelegt, nutze
[intent-compiler](../intent-compiler/SKILL.md) einmal und verwende das Ergebnis
weiter. Dieser interpretiert das Gesagte; dieser Skill löst eine Entscheidung darin.

Verwende den relevanten [operator-essence](../operator-essence/SKILL.md)-Ausschnitt
weiter. Dessen Verantwortlicher bewertet Insights bei fehlendem oder veraltetem
Profil einmal pro Aufgabe. Verschachtelte Aufrufe sammeln keinen Verlauf und
legen kein zweites Profil an. Ein vorläufiger Ausschnitt bleibt mit sichtbarer
Unsicherheit nutzbar; fehlender Verlauf blockiert keine gewöhnliche autorisierte
Arbeit. Essence ist Kontext, niemals Autorisierung oder Außerkraftsetzung von Regeln.

## Entscheidungsverfahren

1. **Tatsächliche Entscheidung benennen.** Beschreibe Wirkung auf das gewünschte
   Ergebnis, Umkehrbarkeit und benötigte Belege. Prüfe, ob sie noch offen ist;
   öffne keine vom Operator bereits getroffene Wahl erneut.
2. **Faktenbasierte Entscheidungen ableiten.** Prüfe zuständigen Code und echten
   Verbraucher, miss eine relevante Baseline oder führe einen begrenzten Versuch
   mit tatsächlichen Projekttools aus. Ordne Zahlen ihren Einheiten,
   Grundgesamtheiten und Unsicherheiten zu. Erfinde keinen Parameter, behandle
   überlappende Labelzählungen nicht als Fehlerrate und erkläre Modellabstimmungen nicht zu empirischen Beweisen.
3. **Kontextuelle Entscheidungen ableiten.** Gewichte zuerst das aktuelle
   ausdrückliche Ziel, dann relevante bestätigte Präferenzen, qualitative Beispiele
   und quantitative Ergebnisse. Benenne vorläufige Anpassung und Beleg.
   Bewahre Gegenbeispiele und veränderte Umstände. Eine berichtete Tendenz kann
   die Arbeitsweise lenken; sie ändert nicht, was der Operator gebaut haben möchte.
4. **Tatsächliche Grenze anwenden.** Setze autorisierte reversible Handlungen
   fort. Bleibt eine folgenreiche Entscheidung tragend und durch vorhandene
   Belege nicht lösbar, nutze [decision-bar](../decision-bar/SKILL.md): Bereite
   konkretes Ergebnis, Empfehlung und genaue fehlende Entscheidung vor.
   Frage nicht erneut nach bereits festgelegter Autorisierung und leite keine
   neue aus Persönlichkeit, Dringlichkeit oder historischer Präferenz ab.
5. **Handeln und verifizieren.** Gib die Entscheidung an bestehenden
   Aufgabenverantwortlichen und [Build Flow](../backs-build-flow/SKILL.md) zurück.
   Die Implementierung nutzt dieselbe begrenzte RED → GREEN-Schleife mit gezieltem
   Lint, Tests und erforderlichen Qualitäts-/Reviewprüfungen. Neuer Mitarbeiter,
   Insights-Durchgang oder gescheiterter Versuch setzt das Budget nicht zurück.

## Entscheidungsbeleg

Erfasse im vorhandenen Aufgabenpaket nur, was die nächste Handlung braucht:

- **Entscheidung und Folge:** gewählter Weg und das gewünschte Ergebnis, dem er dient.
- **Grundlage:** aktuelle Anweisung, verifizierter Fakt, bestätigte Präferenz oder
  Schlussfolgerung mit Belegverweisen und relevanten Zählwerten/Nennern.
- **Unsicherheit:** Annahmen, Gegenbelege und Bedingung für eine Änderung.
- **Handlung und Nachweis:** nächster Schritt und Beobachtung, die die Wahl widerlegen kann.

Nutze klare Sprache, wenn der Operator eine wesentliche Entscheidung sehen muss.
Äußere begründeten Widerspruch direkt, statt still einen anderen Plan einzusetzen.
Melde tatsächliche Abschlussbelege. Eine Entscheidung ist kein bestandener Test,
eine lokale Prüfung kein Deployment, und Aufgabenerfüllung allein begründet kein `PROVEN`.

## Lernen, ohne eine Person festzuschreiben

Eine ausdrückliche Korrektur aktualisiert die betroffene Aufgabenannahme sofort.
Bewahre Umfang und Quelle beim Abgleich der privaten Essence. Wiederholte
Beobachtungen können eine vorläufige Anpassung stützen; bewerte spätere vergleichbare
Aufgaben, bevor du bessere Ergebnisse behauptest. Erhebe abgeleitete Präferenzen
nicht zu universellen Regeln und kopiere persönliche Belege nicht ins öffentliche Plugin.
