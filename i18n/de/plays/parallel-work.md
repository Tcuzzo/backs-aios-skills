# Play: Parallel Work

Wie man Arbeit über Agenten auffächert, ohne dass sie sich gegenseitig zertrampeln.
Die Regel, die alles andere bezahlt: ein Schreib-Rückgrat, viele Leser.

## Wann dieses Play läuft

- Eine Aufgabe zerfällt in Recherche, Scannen, Testen oder Benoten, das
  gleichzeitig laufen kann.
- Mehr als ein Agent wird im selben Zeitfenster dasselbe Repository anfassen.
- Du bist versucht, zwei Agenten parallel Code schreiben zu lassen. Lies das hier
  zuerst.

## Gemeinsame Aufgabe und Grenzen

Wende dieses Play im aktuellen [BACKS Build Flow](../skills/backs-build-flow/SKILL.md)-
Aufgabenpaket an. Bewahre einen Integrationsverantwortlichen, gewünschten
`task_mode`, feste Basis- und Kandidatenrevisionen, Operator-Essence und aktuelle
Belege. Verwende passende geladene Skill-Texte weiter; dieses Play ergänzt seine
Fachprüfungen, ohne die Aufgabe neu zu starten.

[bounded-loops](../skills/bounded-loops/SKILL.md) besitzt ursprüngliche Frist und
Restkontingente über Wiederholungen, Mitarbeiter, Modelle, Reviews und Übergaben
hinweg. Setze sie für ein verschachteltes Play nie zurück. Bei Erschöpfung:
**STILL-BUILDING** mit Kandidat, Belegen, offenen Gates und nächster Handlung
sichern. Nützliche autorisierte Arbeit bleibt im Restkontingent; kein fehlendes
Gate wird zum bestandenen erklärt.

## Die Kette

1. [leap-protocol](../skills/leap-protocol/SKILL.md) — zerlege vor jedem Agentenstart
   in Bälle mit Ziel, Spezifikation und hartem Dateiumfang. Jede Lane bekommt
   aktuelles Paket, feste Basis/Kandidat, RED-Siegel und zugeteiltes Restkontingent.
   Keine Lane darf Frist oder Gesamtkontingent der Elternmission verlängern.

2. Spawne Leser, keine Schreiber — fächere Subagenten NUR für lese-lastige Arbeit
   mit wenigen Querabhängigkeiten auf: Recherche, Test-Läufe, Security-Scans,
   Benotung. Niemals für voneinander abhängiges Code-Schreiben.
3. Isoliere jede Lane — jeder parallele Agent bekommt sein EIGENES Worktree (einen
   separaten Checkout desselben Repos). Konflikte tauchen dann beim Merge als
   echte Merge-Konflikte auf, nie als stille Überschreibungen, die ohne Warnung
   Daten verlieren.
4. [clean-code-gauntlet](../skills/clean-code-gauntlet/SKILL.md) — jede Lane führt
   ihr Qualitäts-Gauntlet in erlaubtem Worktree/Isolation vor Landung aus. Nutze
   zuerst [sniper-testing](../skills/sniper-testing/SKILL.md) für echte Lint-/Typ-/
   Testbefehle aus dem festen Kandidatengesamtdiff; benenne fehlende oder N/A-Checks.
   Verwende gültige Belege nur für exakt gleichen Kandidaten und Prüfumfang weiter,
   nie das Grün einer anderen Lane für andere Bytes. Fehlende Abdeckung erhält
   eine separate Ergänzungsdatei unter Erhalt der versiegelten Originale.

5. [blind-tribunal](../skills/blind-tribunal/SKILL.md) — der prüfende Agent
   bekommt einen SAUBEREN Kontext, niemals den des Autors. Geteilter Kontext
   verrottet und stimmt sich selbst zu.
6. Merge eine Lane nach der anderen im eigenen Merge-Arbeitsbereich, am Test-Exitcode
   geprüft. Der Integrationsverantwortliche verifiziert gemeinsamen Kandidaten,
   betroffene Verbraucher und vorgeschriebenen vollen Landungslauf. Einzelne
   Lane-Erfolge beweisen ihre Zusammensetzung nicht. Lieferbehauptungen brauchen Belege am echten Ziel.

## Koordinationsregeln

- EIN Agent schreibt Code pro Arbeitsbereich, in einem zusammenhängenden Kontext.
  Parallele Schreiber treffen widersprüchliche implizite Entscheidungen, die kein
  Merge versöhnen kann.
- Deklariere die Datei-Zuständigkeit pro Agent vorab. Jeder Agent editiert NUR
  seine benannten Dateien.
- Koordiniere über einen Tracker (Issues, Tickets) — niemals über eine geteilte
  Checklisten-Datei im Working Tree. Diese Datei ist selbst eine
  Merge-Konflikt-Fläche und führt dazu, dass zwei Agenten dieselbe Aufgabe
  greifen.
- Jeder Subagent liefert eine destillierte Zusammenfassung zurück — Kernfakten,
  Entscheidungen, offene Punkte, ein bis zwei Seiten — niemals sein volles
  Transkript.
- Persistiere Plan, Spezifikation und Entscheidungen auf der Platte und lies sie
  neu ein. Lange Läufe kompaktieren den Kontext und lassen Instruktionen still
  fallen; Regeln, die immer gelten müssen, wohnen in der immer geladenen Datei und
  nirgendwo sonst.

## Merge-Disziplin

- Test-gate JEDEN Merge über den Exit-Code, bevor er landet. Eine rote Suite
  blockiert den Merge. Das allein schneidet den größten Teil der
  agentenverursachten Brüche weg.
- Merge in einem eigenen Merge-Arbeitsbereich und stat-verifiziere dann das
  Ergebnis: Dateizahlen, Diffstat, die benannten Dateien jeder Lane vorhanden.
  Ein Merge, der die Dateien einer Lane still fallen lässt, ist der Kardinalfehler
  unter den Merges — prüfe jedes Mal darauf.

## Harte Gates — eines reicht, und das Play ist gescheitert

- Zwei Agenten, die zur selben Zeit im selben Arbeitsbereich Code schreiben.
- Eine Lane, die außerhalb ihres deklarierten Datei-Scopes editiert.
- Ein Merge, der ohne grünen Exit-Code oder ohne Stat-Verifikation gelandet ist.
- Ein Reviewer, der sich den Kontext mit dem Autor geteilt hat.
- Eine Lane, die auf den Testergebnissen einer anderen Lane landet — oder die
  Seam mockt, die sie geändert hat.

**Weight:** heavy per Design — LEAP-Zerlegung, ein Gauntlet pro Lane und ein Tribunal mit sauberem Kontext — der Einsatz zahlt sich nur aus, wenn die Arbeit groß genug zum Aufteilen ist, und nur dann gehört dieses Play überhaupt gefahren.
