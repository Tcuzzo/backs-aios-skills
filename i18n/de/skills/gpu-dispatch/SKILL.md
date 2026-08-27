---
name: gpu-dispatch
description: Nutze das beim Dispatch lokaler Modelle auf GPUs — Inferenzarbeit planen, eine Karte wählen oder Modell-Residenz verwalten. Ein Modell pro GPU, kein Spill ins System-RAM, warm halten durch die Schleife, am Schleifenende entladen, Zulassung nach gemessener Wahrheit. Trigger words: gpu, vram, gpu dispatch, model loading, keep alive, resident model, local inference, spill, warm, Grafikkarte, Modell laden, lokale Inferenz, warmhalten.
license: MIT
---

# Das GPU-Dispatch-Gesetz
**Effort:** free — vom Dispatcher erzwungene Regeln, abgelesen am eigenen Live-Zustand des Knotens; senkt die Kosten unterm Strich. Beseitigt: Läufe, die mit übergelaufenem VRAM still 10x langsamer sind, Kaltstart-Wechselei zwischen Jobs und Karten, die wegen vermuteter Zäune brachliegen.

Vier Regeln für lokale Modelle auf GPUs. Es gibt sie, weil die zwei häufigen
Fehlermodi entgegengesetzt und gleich teuer sind: Karten mit Loads und Spills zu
schreddern, und Hardware so einzuzäunen, dass sie brachliegt. Beides ist verlorene
Fähigkeit. Erzwinge diese Regeln im Dispatcher als Code — nie als Regel, die sich
ein Modell merken muss.

## Wann einsetzen

- Vor dem Dispatch jedes Inferenzjobs auf eine lokale GPU.
- Beim Entwerfen oder Reviewen eines Dispatchers, Schedulers oder Modell-Routers.
- Wenn ein lokaler Lauf rätselhaft langsam ist, oder eine Karte rätselhaft „nicht
  verfügbar".

## Die vier Regeln

1. **Ein Modell resident pro Karte, zur selben Zeit.** Lies vor jedem Dispatch den
   Live-Zustand geladener Modelle des Knotens aus der eigenen API der Runtime.
   Ist ein anderes Modell resident, nutze es oder entlade es zuerst. Lade nie ein
   zweites Modell daneben.
2. **Kein Spill ins System-RAM — abbrechen, nicht langsam weiterlaufen.**
   Verifiziere vor dem Dispatch, dass das Modell komplett in das freie VRAM der
   Karte passt, und stelle während der Arbeit sicher, dass es voll im VRAM
   bleibt. Jeder Spill ins System-RAM ist ein ABBRUCH, kein degradierter Lauf —
   ein übergelaufenes Modell ist still 10x langsamer und vergiftet jeden Job
   dahinter. Ein Modell, das nicht über den reservierten Boden der Karte passt,
   wird nicht auf diese Karte dispatcht; nimm ein kleineres Modell oder eine
   andere Karte.
3. **Halte die Karte warm für die ganze Arbeitsschleife.** Halte das Modell
   resident mit einem begrenzten Keep-Alive — Boden und Deckel, die du
   konfigurierst, nie unbegrenzt — und erneuere es, solange die Schleife läuft.
   Kein Kaltstart-Geschredder zwischen Jobs derselben Schleife.
4. **Entlade nur, wenn die Schleife fertig ist.** Explizite Freigabe am
   Schleifenende — nicht nach jedem Job. Entladen pro Job ist
   Kaltstart-Geschredder; nie entladen ist ein Leck. Freigabe am Schleifenende
   ist die Naht.

## Zulassung nach gemessener Wahrheit

Ob eine Karte Arbeit annehmen darf, entscheidet Live-Messung, nie eine Annahme:

- Eine **echte Probe** des Knotens — keine abgestandene „unreachable“-Notiz in
  einer Config.
- **Echtes freies VRAM** über dem reservierten Boden der Karte — der Boden ist die
  einzige stehende Grenze; alles darüber ist frei nutzbar.
- Ein **echter Check auf laufende Prozesse** für interaktive Workloads. Ein
  laufendes Spiel, ein Stream oder eine Editing-Session auf der Karte gewinnt
  sofort — aber ihre Anwesenheit wird gemessen, nie aus einer Marker-Datei oder
  einer hartcodierten „cold“-Liste angenommen.

Fail-closed-Defaults, Verweigerungen wegen „unbekanntem Zweck“ und
Marker-Dateien, deren Abwesenheit „Zaun an“ bedeutet, sind alle derselbe Bug: die
Runtime verweigert Hardware, die dem Menschen gehört. Eigene Hardware zu
über-gaten ist verlorene Fähigkeit, und verlorene Fähigkeit ist ein Defekt. Nur
das Live-Wort des Menschen setzt oder hebt einen Zaun.

## Harte Regeln (woran dieser Skill scheitert)

- Ein zweites Modell auf eine Karte laden, die schon eins resident hat.
- Einen Lauf nach erkanntem VRAM-Spill fortsetzen, statt abzubrechen.
- Ein unbegrenztes Keep-Alive, oder Entladen zwischen Jobs innerhalb einer
  Schleife.
- Eine Karte auf Basis einer Config-Notiz, Marker-Datei oder Annahme verweigern,
  statt per Live-Probe.
- Irgendetwas davon per Prompt erzwingen, statt im Code des Dispatchers.

## Passt gut zu

- [invariant-floor](../invariant-floor/SKILL.md) — gemessene Wahrheit und laute
  Fehler sind Boden-Gesetze; dieser Skill wendet sie auf GPUs an.
- [fleet-ladder](../fleet-ladder/SKILL.md) — erst auflösen, welches Modell
  dispatcht wird, dann entscheiden, wo es läuft.
- [bounded-loops](../bounded-loops/SKILL.md) — die Arbeitsschleife, auf die
  Keep-Alive und die Freigabe am Schleifenende gescopt sind.
