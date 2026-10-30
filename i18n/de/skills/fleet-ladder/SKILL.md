---
name: "fleet-ladder"
description: "Leitfaden zur Auswahl nach Rolle und Fähigkeit vor einem Dispatch; das öffentliche Paket enthält keinen Resolver oder Fleet-Executable. Trigger words: fleet, ladder, dispatch, fallback, model down, provider down, which model, availability, Leiter, Modellleiter, Ausfall, welches Modell, Verfügbarkeit."
license: "MIT"
---

# Fleet Ladder
**Effort:** light — eine gecachte Live-Probe der Sprosse vor jedem Dispatch. Beseitigt: Dispatches an tote Provider und an Call-Sites hartkodierte Modellnamen, die an dem Tag brechen, an dem das Modell in Rente geht.

Diese Skill beschreibt Auswahlregeln, führt aber selbst keine Modellauflösung aus. Das öffentliche Paket enthält keinen Resolver und kein Fleet-Executable. Fehlt die nötige Laufzeitunterstützung, melde die Lücke. Modell-IDs gehören nicht fest in Skills, Prompts oder Aufrufstellen.

## Wann einsetzen

- Vor JEDEM Dispatch an ein Modell: Build, Grade, Review oder begrenzter
  Worker-Job.
- Wenn ein Provider down ist und du wissen musst, was worauf zurückfällt.
- In dem Moment, in dem du dich ertappst, wie du einen Modellnamen in Code oder
  ein Prompt-Template tippst.

## Die Schritte

1. **Rolle und Fähigkeiten festlegen.** Lies die konfigurierte Leiter und ihre Reihenfolge; wähle einen geeigneten Kandidaten nach Aufgabe, Fähigkeiten und Verfügbarkeit. Eine Beispielkonfiguration ist nur eine Vorlage. Die Skill selbst sortiert oder filtert keine Kandidaten.
2. **Unabhängigkeit prüfen.** Die Begutachtung erfolgt in einer frischen, vom Autor getrennten Ausführung mit einem eingefrorenen, um Autorenkontext bereinigten Paket. Einen geeigneten Prüfer über die konfigurierte Leiter wählen. Zusätzliche Laufzeitbeschränkungen als Lücke benennen.
Jeder geeignete Prüfer kann diese Aufgabe in einer neuen, vom Autor getrennten Sitzung übernehmen; Modell und Anbieter sind keine Einschränkung.
3. **Live-Inferenz prüfen.** Eine Modellliste belegt weder Inferenz noch Fähigkeit oder Kontingent. Führe eine echte, begrenzte Inferenz auf dem vorgesehenen Kandidaten aus; cache das Ergebnis mit angemessenem Ablauf und Backoff. Bei Fallback die Fähigkeiten erneut prüfen.
4. **Steig laut ab.** Dispatche auf die beste VERFÜGBARE Sprosse. Bei
   Transportfehler: den Fehler laut melden, dann die nächste Sprosse versuchen.
   Nie still überspringen — die Aufzeichnung muss zeigen, welche Sprossen
   scheiterten und warum.
5. **Erschöpfung scheitert laut.** Wenn jede Sprosse down ist, wirf einen klaren
   Fehler, der benennt, was versucht wurde. Ein Job, der nicht dispatcht werden
   kann, gelingt nie still, wartet nie ewig und degradiert nie zu einer
   erfundenen Antwort.
6. **Logge Provenienz.** Hänge jeden Dispatch an ein Log an: Rolle, gewähltes
   Modell, übersprungene Sprossen und warum. Später musst du beantworten können:
   „Wer hat diese Arbeit wirklich gemacht?“

## Harte Regeln — eine gebrochen, und der Skill ist gescheitert

- Keine Modell-ID in Skills, Prompts oder Aufrufstellen fest codieren; Rolle und benötigte Fähigkeiten aus der Live-Konfiguration verwenden.
- Nur reale, begrenzte Inferenz belegt die Erreichbarkeit; Kataloglisten allein genügen nicht.
- Eine frische, vom Autor getrennte Review-Ausführung mit anonymisiertem, eingefrorenem Paket ist nötig.
- Fehler und Fallbacks sichtbar machen; fehlende Resolver oder Durchsetzung als Laufzeitlücke melden.


## Passt gut zu

- [blind-tribunal](../blind-tribunal/SKILL.md)
- [bounded-loops](../bounded-loops/SKILL.md)
- [model-fusion](../model-fusion/SKILL.md)
