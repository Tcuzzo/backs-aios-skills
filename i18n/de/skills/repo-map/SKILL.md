---
name: "repo-map"
description: "Beim ersten Einsatz in einem kalten Repo ohne Index verwenden und immer dann, wenn die Karte veraltet ist. Durchläuft den Baum einmal, schreibt eine CODE_MAP.md ins Repo-Root und lässt jede spätere Session zuerst die Karte lesen — Karte zuerst, Rohbaum nur wenn die Karte keine Antwort hat. Trigger words: repo map, code map, map first, map-first, index the repo, cold repo, stale map, refresh the map, Repo-Karte, Code-Karte, Repo indexieren, Karte aktualisieren."
license: "MIT"
---

# Repo Map
**Effort:** light — ein Durchlauf beim ersten Mal, danach fast kostenlos. Beseitigt: dass Agenten die Form des Repos in jeder Session neu herleiten — die größte Latenz- und Tokensteuer eines nicht indexierten Repos.

Eine indexierte Codebase beantwortet „wo liegt X“ kostenlos. Die meisten Repos haben
keinen Index, deshalb zahlt jede Session dieselbe Steuer: Baum ablaufen, Struktur neu
entdecken, am Session-Ende alles vergessen. Dieser Skill zahlt die Steuer einmal.
Lauf den Baum einmal ab, schreib das Gelernte in eine Kartendatei und lass jede
spätere Frage die Karte lesen, bevor sie läuft.

## Wann laufen lassen

- In der ersten Session in einem kalten Repo — ohne Karte und ohne Index.
- Immer wenn die Karte veraltet ist (siehe Regel unten).

## Die Schritte

1. **Lauf den Baum einmal ab.** Ein Durchgang über die echte Struktur:
   Verzeichnisse, Einstiegspunkte und Fundorte. Das sollte der einzige vollständige
   Lauf sein, den das Repo je braucht.
2. **Schreib eine `CODE_MAP.md` ins Repo-Root.** Sie trägt:
   - die Einstiegspunkte — wo Ausführung beginnt;
   - Bereiche und Schnittstellen, je mit einem Einzeiler zum Zweck;
   - wo die Tests liegen;
   - Build-, Start- und Testbefehle;
   - die heißen Pfade — aus der Historie ableiten (`git log --name-only` nach
     Häufigkeit), oder leer lassen und spätere Sessions ergänzen lassen.
3. **Halte sie schlank.** Eine Karte, keine Dokumentation. Eine Zeile pro Fakt.
   Wird ein Eintrag zum Absatz, driftet er in Doku ab — kürz ihn auf einen Zeiger.
4. **Speichere die Form des Baums.** Lege einen billigen Fingerabdruck in der
   Karte ab: `git ls-files | sha256sum` (erkennt Hinzufügen, Verschieben und
   Umbenennen), damit spätere Sessions sehen, ob sich die Form geändert hat.

## Das Karte-zuerst-Gesetz

Recherche, Wegfindung und Plays lesen die Karte, BEVOR sie den Baum ablaufen. Der
Rohlauf ist der Fallback, wenn die Karte keine Antwort hat — und alles Gelernte wird
IN die Karte geschrieben, bevor die Session weitergeht. Die Karte nimmt jeden Lauf
auf. Neu-Herleitung wird einmal bezahlt, nie pro Session.

## Die Veraltungsregel

Aktualisiere die Karte nur, wenn sich die Form des Baums geändert hat — Dateien
wurden seit dem gespeicherten Stand hinzugefügt, verschoben oder umbenannt. Vergleiche
den gespeicherten Fingerabdruck (`git ls-files | sha256sum`) mit dem Live-Baum. Nie
nach Zeitplan aktualisieren. Nie jede Session aktualisieren. Eine planmäßig neu
gebaute Karte ist nur die Session-Steuer mit neuem Namen.

## Harte Regeln

- **Fakten und Orte, nie Meinungen.** „Auth liegt in `src/auth/`“ gehört in die
  Karte; „der Auth-Code ist chaotisch“ nicht.
- **Ein toter Zeiger stirbt beim Fund.** Ein Pfad, der nicht mehr auflöst, wird
  sofort repariert oder entfernt. Eine lügende Karte ist schlimmer als keine.
- **Die Karte trägt nie Secrets.** Keine Keys, Tokens, Credentials oder privaten
  Hostnamen. Sie ist eine getrackte Datei; behandel sie so.

## Passt gut zu

- [live-research](../live-research/SKILL.md) — der Rechercheur liest zuerst die Karte, dann die Quelle.
- [wayfinder](../wayfinder/SKILL.md) — das Kartieren startet von der Karte, nicht von einem kalten Lauf.
- [session-handoff](../session-handoff/SKILL.md) — die Karte ist der Teil eines Handoffs, den jede Session teilt.
