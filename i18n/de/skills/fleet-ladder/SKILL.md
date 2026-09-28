---
name: "fleet-ladder"
description: "Nutze das, bevor Arbeit an ein Modell geht — Bauen, Bewerten oder ein begrenzter Worker-Job — oder wenn ein Provider down ist und du die Fallback-Reihenfolge brauchst. Löst die LIVE-Modellleiter auf: probe, was wirklich läuft, wähle das beste Verfügbare nach expliziter Fallback-Ordnung, scheitere laut, wenn die Leiter erschöpft ist. Trigger words: fleet, ladder, dispatch, fallback, model down, provider down, which model, availability, Leiter, Modellleiter, Ausfall, welches Modell, Verfügbarkeit."
license: "MIT"
---

# Fleet Ladder
**Effort:** light — eine gecachte Live-Probe der Sprosse vor jedem Dispatch. Beseitigt: Dispatches an tote Provider und an Call-Sites hartkodierte Modellnamen, die an dem Tag brechen, an dem das Modell in Rente geht.

Bau nie einen Provider-Call von Hand, und codiere nie einen Modellnamen an einer
Aufrufstelle hart. Ein Resolver besitzt die Frage „welches Modell macht diesen Job
jetzt gerade?" — und er antwortet aus der Live-Wahrheit, nicht aus der Meinung
einer Config-Datei.

## Wann einsetzen

- Vor JEDEM Dispatch an ein Modell: Build, Grade, Review oder begrenzter
  Worker-Job.
- Wenn ein Provider down ist und du wissen musst, was worauf zurückfällt.
- In dem Moment, in dem du dich ertappst, wie du einen Modellnamen in Code oder
  ein Prompt-Template tippst.

## Die Schritte

1. **Deklariere die Rolle, nicht das Modell.** Jeder Job fragt nach einer Rolle —
   `builder`, `grader` oder `worker`. Die Leiter mappt Rollen auf geordnete
   Modellkandidaten.
   - `builder`: implementiert und repariert.
   - `grader`: unabhängiges Review — strukturell nie dasselbe Modell, das gebaut
     hat.
   - `worker`: begrenzte, gut spezifizierte Jobs. Billigere Sprossen sind hier
     okay.
2. **Lies die Leiter aus der Config.** Eine Datei listet pro Rolle die Kandidaten
   in expliziter Fallback-Reihenfolge: das stärkste zuerst, runter bis zu deinem
   lokalen Überlebensschwanz (was auch immer du auf eigener Hardware fahren
   kannst, wenn jeder Cloud-Provider dunkel ist). Um ein Modell zu ändern oder
   hinzuzufügen, editiere diese Datei — nie den Code. Starterform:
   [ladder.example.yaml](ladder.example.yaml) — kopieren, Platzhalter tauschen.
3. **Probe live, bevor du vertraust.** Ein Config-Eintrag ist eine Behauptung,
   keine Wahrheit. Ein veralteter Eintrag listet Modelle, die tot sind; und er
   verschweigt Modelle, die leben. Probe den Provider, bevor du auf eine Sprosse
   dispatchst — ein Call auf den Models-Endpoint oder ein Ein-Token-Request,
   z. B.:
   `curl -s "$PROVIDER_BASE_URL/v1/models" -H "Authorization: Bearer $API_KEY"`
   (oder dieselbe Form gegen den Chat-Endpoint mit `"max_tokens": 1`).
   Cache das Probe-Ergebnis für ein vernünftiges Fenster — hämmere Provider nicht
   durch Re-Proben bei jedem Call. Erneuere den Cache nur, wenn du wirklich
   frische Wahrheit brauchst.
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

- **Kein Modellname an einer Aufrufstelle.** Code fragt nach einer Rolle; die
  Leiter antwortet mit einem Modell. Greppe deine Codebasis nach
  Modellnamen-Literalen — jedes ist ein Bug.
- **Die Live-Probe schlägt die Config.** Wenn der Mensch sagt, ein Modell
  existiert, und die Config widerspricht: probe es. Geprüft-und-es-antwortet ist
  erledigt; eine veraltete Liste nicht.
- **Builder und Grader lösen nie auf dasselbe Modell auf** für dieselbe Änderung.
  Würde die Leiter sie auf ein Modell kollabieren, nimmt der Grader die nächste
  unabhängige Sprosse — oder der Job scheitert laut.
- **Begrenztes Proben.** Probes sind billig, gecacht und Backoff-bewusst. Eine
  enge Retry-Schleife gegen einen toten Provider ist verboten.
- **Kein stiller Fallback.** Jeder Schritt die Leiter hinunter ist im Log und im
  Bericht sichtbar. Leises Degradieren ist die Art, wie eine kaputte Route
  unbemerkt stirbt.

## Passt gut zu

- [model-fusion](../model-fusion/SKILL.md) — Panel und Judge lösen ihre Modelle über diese Leiter auf.
- [blind-tribunal](../blind-tribunal/SKILL.md) — Juroren kommen aus verschiedenen Familien; die Leiter wählt lebende.
- [bounded-loops](../bounded-loops/SKILL.md) — Probe-Kadenz, Backoff und Kill-Switches.
