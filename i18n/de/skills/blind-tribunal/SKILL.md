---
name: "blind-tribunal"
description: "Nutze das, wenn eine autonome Änderung vor dem Landen eine unabhängige Bewertung braucht und kein Mensch in der Schleife ist. Beruft blinde Cross-Family-Juroren ein — eine Linse pro Kopf — über einen autor-geschwärzten Umschlag ganzer Dateien; jeder Befund wird ein neuer fehlschlagender Test; Schleife, bis jeder Juror passt. Trigger words: blind tribunal, grill tribunal, tribunal, jurors, cross-family grade, convene, blind grade, independent grade, grade before landing, Tribunal, Juroren, blinde Bewertung, unabhängige Bewertung, vor dem Landen bewerten."
license: "MIT"
---

# Blind Tribunal
**Effort:** heavy — acht Juroren, eine Linse pro Kopf, nach Stufe an die günstigste ausreichende Modellfamilie geroutet, jede Runde auf frischen Umschlägen neu einberufen, bis sie einstimmig sind; investier das in autonome Änderungen, die ohne menschliches Review landen. Beseitigt: entgleiste Landungen, die nichts bewacht außer dem eigenen Wort des Builders.

Die Bewertungsschleife, mit der der Mensch weggehen kann, ohne dass der Agent
entgleist. Ein Panel aus Juroren prüft die Änderung blind, mit entfernter
Autorschaft. Jeder Befund wird ein neuer fehlschlagender Test. Die Schleife läuft,
bis jeder Juror passt. Nichts landet allein auf das Wort des Builders.

## Wann einsetzen

- Vor dem Landen jeder autonomen Änderung, die kein Mensch reviewen wird.
- Jede Änderung mit großem Explosionsradius: sicherheitsnah, datenberührend,
  autoritätsnah.
- Wenn ein Grader nicht reicht und du unabhängige Linsen auf demselben Artefakt willst.

## Die Sitze

Acht Juroren, eine Linse pro Kopf. Jeder ist ein Modell aus einer ANDEREN Familie als
der Builder (gleicher Hersteller = gleiche Familie). Ein Juror, der alles prüfen soll,
prüft nichts richtig.

| Juror | Linsen-Id | Stufe | Die Frage, die er stellt |
| --- | --- | --- | --- |
| Defekt | `defect` | Generalist | Was geht wirklich kaputt? Logikfehler, Syntaxfehler, neue Defekte. |
| Proportion | `proportion` | Generalist | Ist das die richtige Größe? Überbaut, oder passend zur Absicht? |
| Konsequenz | `operator_consequence` | Operator-Sicherheit | Wenn ein Mensch das auf seiner Maschine ausführt — was ist zerstörerisch, unsicher oder schädlich? |
| Reversibilität | `reversibility` | Deep State | Bleiben irreversible Nebeneffekte? Stirbt es mittendrin — rollt das System sauber zurück? |
| Kontinuität | `state_continuity` | Deep State | Verwaiste Variablen, überschriebener globaler Zustand, verlorener Kontext für nachgelagerte Knoten? |
| Ökonomie | `resource_economy` | schnell-strukturell | Unoptimierte Schleifen, redundante Netz-/API-Aufrufe, Speicher-Bloat? |
| Grenzfall | `boundary_condition` | schnell-strukturell | Null, leer, falscher Typ, absichtlich kaputt — fällt es sauber aus? |
| Telemetrie | `telemetry` | Operator-Sicherheit | Lässt sich ein Fehler hier aus Logs und Fehlerbehandlung diagnostizieren? |

**Routing-Stufen (die günstigste ausreichende Route zuerst):** Deep State → größter
Kontext und tiefstes Reasoning, idealerweise durch einen Harness, der das Repo LIEST
(nie schreibt); schnell-strukturell → erst eine freie lokale GPU, FUSIONIERT mit einem
billigen Cloud-Verifizierer, der denselben Prompt beurteilt: die Linse besteht nur, wenn
beide bestehen; ohne Cloud bleibt das lokale Urteil, markiert UNVERIFIED, nie stillschweigend
„verifiziert"; und das lokale Modell muss das GANZE Artefakt sehen (`num_ctx` auf den
Prompt dimensionieren — Ollamas Default 4096 kürzt stillschweigend — und vor dem Senden
ablehnen, was nicht passt); danach die Cloud-Modelle mit niedriger Latenz; Operator-Sicherheit →
dein stärkster Coder mit Sicherheits-Grounding; Generalist → ein großer, zuverlässiger
Generalist. Jede Leiter endet auf einer lokalen Überlebens-Sprosse.

**Solo-Rig.** Wenn nur eine Modellfamilie verfügbar ist, degradiere EXPLIZIT: Ein
frischer Kontext oder eine frische Session, die die Konversation des Autors nie
gesehen hat, agiert als blinder Grader, oder der Mensch prüft den geschwärzten
Umschlag. Der Bericht muss das geschwächte Gate benennen — „same-family-blind
bewertet, nicht cross-family" — und nie still so tun, als hätte das
Cross-Family-Gate gehalten.

## Der Umschlag

Juroren sehen nie das Repo, den Builder oder die Konversation. Sie sehen einen
Umschlag:

- **Ganze aktuelle Dateien** für jede Datei, die die Änderung berührt hat, plus
  ihre Testdateien. Nie nackte Diff-Hunks — ein Hunk versteckt den umgebenden
  Contract und provoziert falsche Befunde.
- **Der Review-Contract**: die Absicht der Änderung in einer Zeile, und die
  Pass-Kriterien.
- **Null Autorschaft.** Keine Namen, keine Modell-IDs, keine Commit-Autoren, keine
  Chat-History. Sickert Identität durch, schlägt der Umschlag-Bau laut fehl — nie
  unverblindet bewerten.
- **Keine Prosa über das alte Verhalten.** Zu beschreiben, was der Code „früher
  tat", pflanzt Phantom-Defekte. Die Dateien sprechen für sich.

## Das Urteil

Striktes, maschinenlesbares JSON, ein Objekt, keine Prosa:

```json
{"verdict": "pass" | "refuse",
 "findings": [{"severity": "blocker|major|minor|info",
               "claim": "...", "evidence": "..."}]}
```

- Ein Juror, der SCHLECHT geantwortet hat — Müll, kein JSON, Verweigerungstext —
  zählt als **refuse**; ein Juror, der NIE geantwortet hat (Transportfehler,
  unerreichbar), ist ein **hold**: neu besetzen via
  [fleet-ladder](../fleet-ladder/SKILL.md), nie ein stiller Pass. Ein Schuss pro
  antwortendem Juror pro Runde — keine Retries.
- Ein nackter Pass mit null Befunden und ohne Evidenz ist eine
  **informationsarme Stimme**. Sie zählt, aber nie als einziger Beweis — zwei
  nackte Passes überstimmen keinen detaillierten Refuse. Ein starker Pass benennt,
  was er geprüft hat.

## Die Schleife

1. Rot zuerst: committe den fehlschlagenden Contract-Test, BEVOR der Fix gebaut
   wird, und halte diesen Commit fest. Der Builder darf den Test nicht anfassen
   ([red-first](../red-first/SKILL.md)).
2. Baue bis grün.
3. Baue den Umschlag aus den AKTUELLEN Dateien.
4. Besetze die acht Juroren, nach Stufe, — andere Familien als der Builder
   ([fleet-ladder](../fleet-ladder/SKILL.md) klärt, was live ist).
5. Jeder Juror verifiziert auch, statt nur zu lesen: Die neuen Tests bestehen; die
   Regressions-Suite ist nicht schlechter als die Baseline; und ein
   Fake-Green-Check — ein Test, der fehlschlagen SOLLTE (der Bug wieder
   eingebaut), schlägt wirklich fehl. Ein Fake Green ist ein Refuse.
6. Bei jedem Refuse: JEDER Befund — Blocker, Major und Minor — wird ein NEUER
   fehlschlagender Test, der aus dem echten Grund des Befunds fehlschlägt. Behebe
   ihn. Baue den Umschlag über den überarbeiteten Dateien neu. Berufe ALLE Juroren
   neu ein. Ein Urteil über veraltete Dateien ist kein Urteil.
7. Lande nur bei einstimmigem Pass. Minor-Befunde aus der letzten Runde werden
   auch geschlossen, nie vertagt — „Blocker gefixt, Minors später“ ist genau das
   Leck, das dieser Skill stopfen soll. Ein Befund endet GEFIXT oder mit
   dokumentierter Evidenz widerlegt, nie geparkt.

## Harte Regeln — eine gebrochen, und die Bewertung ist nichtig

- Der Builder bewertet nie die eigene Arbeit: nicht dieselbe Instanz, nicht
  dieselbe Familie.
- **Ein Juror-Refuse ist nur so gut wie der Umschlag.** Bevor du aus einem Befund
  einen Test schreibst, prüfe den Befund gegen die tatsächlichen Dateien. Ein
  Befund über Code, den der Umschlag nie enthielt, heißt: den Umschlag fixen,
  nicht den Code.
- Miss Konvergenz an NEUEN Befunden pro Runde, nicht an der Rohsumme. Neue Befunde
  zwei Runden in Folge flach oder steigend: stoppen und an den Menschen
  eskalieren. Nie stur weitermahlen.
- Schwäche oder editiere die fehlschlagenden Tests nie, um einen Pass zu
  erreichen. Juroren verifizieren, dass die Testdateien seit dem Rot-Commit
  unverändert sind.
- Ein einstimmiger Pass öffnet das Tor; er ist nicht das Ziel. Lande, dann beweise
  die Fähigkeit live auf der echten Oberfläche. Grün ohne Live-Beweis ist nicht
  fertig.

## Passt gut zu

- [red-first](../red-first/SKILL.md) — der fehlschlagende Contract, committet bevor der Builder läuft.
- [sniper-testing](../sniper-testing/SKILL.md) — echte Nebeneffekte, begrenzte Läufe, kein Mock-Theater.
- [seam-engineering](../seam-engineering/SKILL.md) — die Klasse fixen, Geschwister durchkämmen, einen Guard landen.
- [repair-loop](../repair-loop/SKILL.md) — die Bauschleife, die dieses Tribunal bewertet.
- [blind-eval](../blind-eval/SKILL.md) — das leichtere Keep-or-Revert-Gate, wenn die Frage Geschmack ist, nicht Defekte.

> Gerüst-Credit: Matt Pocock, grill-me / grilling (mattpocock/skills, MIT). Das
> Design des blinden, adversarialen Cross-Family-Tribunals ist BACKS AIOS.
