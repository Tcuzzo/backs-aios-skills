---
name: "blind-eval"
description: "Nutze das vor dem Landen von allem, wo Geschmack oder Output-Qualität die Frage ist und kein Test entscheiden kann. Bewertet eine Änderung nach Substanz mit verdeckter Autorschaft, dann keep oder revert — ein Unentschieden wird verworfen, nur bewiesener Uplift landet. Trigger words: blind eval, karpathy, keep or revert, quality gate, taste call, blind judge, A/B judge, prove uplift, Blindbewertung, behalten oder verwerfen, Qualitätsgate, Geschmacksfrage, Uplift beweisen."
license: "MIT"
---

# Blind Eval
**Effort:** light — ein blinder Richter-Lauf: mehrere gemischte Lesungen des eingefrorenen Paars durch ein Modell, das keines von beiden geschrieben hat. Beseitigt: selbstbenotete „ist besser“-Landungen — Geschmacks-Regressionen, die der Autor durchwinken würde.

Ein Keep-or-Revert-Qualitätsgate für Entscheidungen, die kein Test treffen kann —
Prosaqualität, UI-Texte, die Lesbarkeit eines Refactors, der Output eines Prompts,
das Gefühl eines Designs. Bewerte die Änderung nach Substanz, mit verdeckter
Autorschaft, dann BEHALTE sie (keep) oder VERWIRF sie (revert). Ein Unentschieden
wird verworfen. Nur bewiesener Uplift landet.

## Wann einsetzen

- Vor dem Landen jeder Änderung, bei der „ist es besser?“ eine Geschmacks- oder
  Qualitätsfrage ist.
- Als Gate in einer Verbesserungsschleife: vorschlagen → probieren → messen →
  behalten oder verwerfen.
- Immer wenn der Autor versucht ist, die eigene Arbeit zur Verbesserung zu erklären.

## Die Methode

1. **Schreib „besser“ auf, BEVOR du hinschaust.** Ein Ziel in klarer Sprache. Ein
   primäres Maß oder eine Rubrik-Achse mit harter Latte — eine Höhe, die zu nehmen
   ist, keine Zahl zum Hochtreiben. Sekundäre Achsen in Prioritätsreihenfolge
   (Kosten, Länge, Latenz).
2. **Friere beide Versionen ein.** Die Baseline und den Kandidaten, als echte
   Artefakte — nie als Beschreibung davon.
3. **Entferne die Autorschaft.** Beschrifte sie A und B, mische die Reihenfolge,
   streiche jeden Namen, jede Modell-ID und die Begründung des Autors. Der Judge
   sieht nur die Artefakte und die Rubrik.
4. **Setze einen Judge ein, der keins von beiden geschrieben hat** — ein Modell aus
   einer anderen Familie, oder einen Menschen. Der Autor bewertet nie die eigene
   Arbeit.
5. **Urteile nach Substanz.** Punkte pro Rubrik-Achse. Belege jede Wertung mit
   Evidenz aus dem Artefakt — ein Urteil ohne Beleg ist geraten.
6. **KEEP nur, wenn der Kandidat die Latte nimmt UND die Baseline strikt schlägt.**
   Ein Unentschieden ist kein Uplift — revert.
7. **Reverte sauber.** Stelle den Baum byte-identisch auf den Zustand vor der
   Änderung zurück (ein Scratch-Branch oder Stash macht das zu einem Befehl).
   Protokolliere das Urteil so oder so.

## Regeln, die das Gaming stoppen

- **Die Latte wird zuerst geprüft, und die Achsen zählen in ihrer Reihenfolge.**
  Eine Regression auf einer höher priorisierten Achse ist fatal, selbst wenn jede
  niedrigere Achse besser wird. Und die Latte mit Extra-Abstand zu nehmen bringt
  nichts — du kannst das primäre Maß nicht übererfüllen, um eine Kosten-Regression
  zu „bezahlen“.
- **Senke die Latte nie, nachdem du das Ergebnis gesehen hast.** Den Score zu
  reparieren, indem man das Eval schwächt, ist verboten. Halte Rubrik und Eval
  außerhalb der Dateien, die die Änderung anfassen darf.
- **Kein Self-Grading.** Der Judge sieht nie die Begründung des Autors — ein Judge,
  der den Verkaufstext liest, bewertet den Verkaufstext, nicht die Arbeit.
- **Entrausche einen stochastischen Judge.** Blindlesungen schwanken von Lauf zu
  Lauf, und Judges bevorzugen die zuerst gezeigte Option. Fahre jeden Vergleich
  mehrmals mit gemischter Reihenfolge und nimm die Mehrheitsentscheidung — das
  Mischen killt den Positions-Bias, die Wiederholungen killen das Rauschen, in
  einem Zug. Ist die echte Verbesserung kleiner als die Lauf-zu-Lauf-Schwankung
  des Judges, kann das Gate Signal nicht von Glück unterscheiden — mehr Lesungen,
  oder ein stabileres Maß.
- **Solo-Rig.** Keine zweite Modellfamilie verfügbar? Dann urteilt eine frische
  Blind-Session, die die Konversation des Autors nie gesehen hat — und der Bericht
  benennt das geschwächte Gate („same-family-blind bewertet, nicht cross-family“).
- **Keine verlässliche Latte? Nimm Dominanz.** Wenn das Baseline-Niveau unbekannt
  oder verrauscht ist, lass die absolute Latte weg und behalte nur, was den
  aktuellen Champion strikt schlägt. Eine Regression kann nie dominieren, also
  braucht es keinen Boden.
- **Bewerte eine Kosten-Achse nie über Fehlschläge.** „Weniger Schritte“, gerechnet
  über gescheiterte Versuche, belohnt schnelles Aufgeben. Rechne Kosten und Aufwand
  nur über Erfolge.

## Den Judge entzerren

Der Boden für die Judge-Mechanik. Diese Regeln leben hier und nirgendwo sonst:

- **Held-out-Suite.** Bewerte auf einer Suite AUSSERHALB der Schreibreichweite des
  Builders — der Builder sieht die bewerteten Tests nie und kann sie darum nicht
  hart codieren.
- **Fresh-Commit-Strip.** Reduziere den Workspace vor einem bewerteten Lauf auf
  einen frischen Commit und blockiere Netz-Egress, damit ein Pass ABGELEITET ist —
  nicht aus der Git-History oder dem Fix von jemand anderem geholt.
- **Längen-Normalisierung.** Judges bevorzugen stark die längere Antwort —
  korrigiere die Länge, bevor du Scores vergleichst.
- **Rotierte Holdout-Kriterien.** Nutze eine Ja/Nein-Rubrik mit benannten Achsen
  und versteckten Holdout-Kriterien, die zwischen Läufen rotieren. Ein sichtbarer
  Gesamtscore wird zu Zitations-Theater gegamet.
- **Endzustand bewerten.** Bewerte mehrstufige Arbeit am FINALEN Endzustand, nicht
  an jedem Zwischenschritt.
- **Judge-Kalibrierung.** Kalibriere den Judge an einem kleinen, menschlich
  gelabelten Set — berichte seine True-Positive- und True-Negative-Raten — bevor
  du ihm in deiner Domäne traust.

Das Mischen der Reihenfolge gehört zur Entrausch-Regel oben — ein Gesetz, einmal
formuliert.

## Die Loop-Variante

Dasselbe Gate treibt eine autonome Verbesserungsschleife: kleine Änderung
vorschlagen → kurzes Experiment fahren → blind messen → behalten, wenn besser,
sonst verwerfen → wiederholen, mit festem Runden-Budget. Gib dem Vorschlagenden
die Fehler-Traces der letzten Runde, nicht nur das Ziel — wer nicht sieht, warum
er scheitert, editiert blind. Selbst eine Schleife, die nichts behält, verdient
ihre Kosten: Die gesammelten Traces zeigen auf konkrete, behebbare Bugs, die kein
aggregierter Score offenlegt.

## Passt gut zu

- [blind-tribunal](../blind-tribunal/SKILL.md) — das schwerere Juroren-Panel, wenn Defekte und nicht Geschmack die Frage sind.
- [red-first](../red-first/SKILL.md) — wenn ein Test es entscheiden KANN, schreib den Test.
- [clean-code-gauntlet](../clean-code-gauntlet/SKILL.md) — gemessene Code-Qualitätsgates als Partner der Geschmacksfrage.

> Namensgeber-Credit: Andrej Karpathy. Namensgeber-Inspiration; die
> Keep-or-Revert-Disziplin findet sich unabhängig parallel in Karpathys
> autoresearch (2026, github.com/karpathy/autoresearch, MIT). Der Blind-Aspekt
> (verdeckte Autorschaft) sowie die Komposition und die harten Regeln hier sind
> BACKS AIOS.
