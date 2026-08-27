# Play: Parallel Work

Wie man Arbeit über Agenten auffächert, ohne dass sie sich gegenseitig zertrampeln.
Die Regel, die alles andere bezahlt: ein Schreib-Rückgrat, viele Leser.

## Wann dieses Play läuft

- Eine Aufgabe zerfällt in Recherche, Scannen, Testen oder Benoten, das
  gleichzeitig laufen kann.
- Mehr als ein Agent wird im selben Zeitfenster dasselbe Repository anfassen.
- Du bist versucht, zwei Agenten parallel Code schreiben zu lassen. Lies das hier
  zuerst.

Das Auffächern auf einen Blick:

```
+--------------------------------------------+
| 1 leap-protocol  balls with goals, specs,  |
|   hard file scopes BEFORE any agent spawns |
+--------------------------------------------+
| 2 spawn readers, not writers -- fan out    |
|   read-heavy work only                     |
+--------------------------------------------+
| 3 isolate -- every lane gets its OWN       |
|   worktree; conflicts surface at merge     |
+--------------------------------------------+
| 4 clean-code-gauntlet  per lane, in its    |<--------------------------+
|   own worktree, before it asks to land     |  red exit? back to the    |
+--------------------------------------------+  lane -- fix, re-run      |
| 5 blind-tribunal  the reviewer gets a      |                           |
|   CLEAN context, never the author's        |   +---------------------+ |
+--------------------------------------------+   |  LORD OF THE LOOP   |-+
| 6 merge ONE lane at a time, test-gated     |   | the one write spine |
|   by exit code, in a merge workspace       |-->| drives dispatch,    |
+--------------------------------------------+   | judges, merges ONE  |
          |                                      | lane at a time. a   |
          | every merge green + verified         | lane never lands    |
          v                                      | its own work.       |
+--------------------------------------------+   +---------------------+
| LANDING GATE -- all green or no land:      |
| every merge green by exit code AND         |
| stat-verified -- counts, diffstat, each    |
| lane's files present . no lane outside     |
| its scope . reviewer context stayed        |
| clean, never the author's . one writer     |
| per workspace . no lane lands on           |
| another lane's green                       |
+--------------------------------------------+
```

*Labels im Diagramm: „Lord of the Loop“ = der Besitzer des Loops, der die Iteration treibt, bis das Landing-Gate grün ist; „LAND“ = die Landung — die Änderung zieht erst ein, wenn jedes Gate grün ist.*

## Die Kette

1. [leap-protocol](../skills/leap-protocol/SKILL.md) — zerlege die Arbeit in Bälle
   mit Zielen, Spezifikationen und harten Datei-Scopes, BEVOR irgendein Agent
   spawnt.
2. Spawne Leser, keine Schreiber — fächere Subagenten NUR für lese-lastige Arbeit
   mit wenigen Querabhängigkeiten auf: Recherche, Test-Läufe, Security-Scans,
   Benotung. Niemals für voneinander abhängiges Code-Schreiben.
3. Isoliere jede Lane — jeder parallele Agent bekommt sein EIGENES Worktree (einen
   separaten Checkout desselben Repos). Konflikte tauchen dann beim Merge als
   echte Merge-Konflikte auf, nie als stille Überschreibungen, die ohne Warnung
   Daten verlieren.
4. [clean-code-gauntlet](../skills/clean-code-gauntlet/SKILL.md) — jede Lane fährt
   ihr eigenes Qualitäts-Gauntlet im eigenen Worktree, bevor sie landen will. Erst
   der Dry-Run, damit die Lane ihre eigenen Kosten kennt. Keine Lane landet auf
   dem Grün einer anderen Lane.
5. [blind-tribunal](../skills/blind-tribunal/SKILL.md) — der prüfende Agent
   bekommt einen SAUBEREN Kontext, niemals den des Autors. Geteilter Kontext
   verrottet und stimmt sich selbst zu.
6. Merge eine Lane nach der anderen, in einem eigenen Merge-Arbeitsbereich,
   test-gegatet über den Exit-Code.

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
