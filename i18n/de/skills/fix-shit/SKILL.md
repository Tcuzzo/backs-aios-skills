---
name: fix-shit
description: "Wenn der Operator kaputtes Verhalten meldet, fix shit oder stop swallowing errors sagt oder einen hartnäckigen Bug abgeschlossen haben möchte."
license: MIT
---

# Fix Shit

Nutze diesen schnellen Einstieg in `root-cause-first` und `repair-loop` innerhalb
der aktuellen [BACKS Build Flow](../backs-build-flow/SKILL.md)-Aufgabe. Bewahre
Integrationsverantwortlichen, Operator-Essence, `task_mode`, Kandidatenidentität
und Belege; lade kein gültiges Kontextpaket erneut und starte keinen zweiten
Lebenszyklus. Ein direkter Aufruf legt das Paket einmal an. Restbudget und Frist
von [bounded-loops](../bounded-loops/SKILL.md) gelten für jede Reproduktion,
Reparatur, Modell-Fallback und Prüfung. Dieser Skill setzt sie nie zurück und
versteckt kein Fehlersignal.

1. Name the user's broken behavior and the exact surface where it appears.
2. Erzeuge ein wiederholbares rotes Signal auf dem echten Pfad. Verfolge Eingabe
   und jede Grenze bis zur Abweichung zwischen tatsächlichem und erwartetem
   Verhalten. Versiegle den ursprünglichen Fehlervertrag mit
   [red-first](../red-first/SKILL.md), bevor ein Builder die zuständige
   Schnittstelle ändert. Eine Diagnoseaufgabe gibt diesen Beleg zurück.
3. Identify the root cause and all callers of the broken seam. Preserve the
   original error in logs or the operator-facing state; a fallback may protect
   the app, but it must not turn failure into false success.
4. Nutze für einen autorisierten Fix [repair-loop](../repair-loop/SKILL.md)
   innerhalb des Ablaufs: kleinste Reparatur der Fehlerklasse, echte Lint-/Typ-/
   Testbefehle im Umfang des festgehaltenen Kandidatengesamtdiffs, danach Qualität
   und Mutation mit clean-code-gauntlet. Bewahre das versiegelte Original;
   neue Lücken erhalten separate Ergänzungstests. Verwende verifizierte Stufen weiter.
5. Schließe vorgeschriebenes autor-disjunktes Review (author-disjoint), Landungsprüfung betroffener
   Suiten und echte App-Pfadprüfungen für die gewünschte Lieferung ab. Prüfe
   gewünschtes Ergebnis und ausdrücklichen Fehlerzustand. Fehlende Reviewer-
   Fähigkeit ist eine Runtime-Lücke, kein selbst ausgestellter unabhängiger Erfolg.
6. Gib Kandidat und Belege an den Integrationsverantwortlichen zurück. Melde PROVEN
   nur mit erforderlichem Review und realen Lieferbelegen; andernfalls sichere
   STILL-BUILDING mit genauem offenen Fehler und nächster Handlung. Erschöpftes
   Budget bewahrt Arbeit und Grenzen; setze nützliche freie Arbeit nur innerhalb
   ihres Restkontingents fort.

If the error is intermittent, capture timing and a bounded reproduction rate;
do not infer a cause from one green rerun. For code-location ambiguity, start
with `building-with-backs` and its target check.


## Belege und unabhängige Prüfung

Für ausgelieferte Programme, Pakete oder angefragtes Laufzeitverhalten nutze [rea-investigation](../rea-investigation/SKILL.md) und den separat installierten Skill `reverse-engineer-anything`, wenn dessen Analyse nützt; verwende bei unterstützten nativen Zielen einen vorhandenen Ghidra-Provider. Statische Befunde beweisen kein Live-Verhalten; installiere fehlende Provider nicht stillschweigend. Zur Übernahme von Open-Source-Fähigkeiten nutze [absorb](../absorb/SKILL.md). Wähle über [fleet-ladder](../fleet-ladder/SKILL.md) nach Rolle und Fähigkeit, ohne Modellnamen fest zu codieren. Wenn ein Tribunal nötig ist, befolge [blind-tribunal](../blind-tribunal/SKILL.md): Eine frische, vom Autor getrennte Ausführung prüft ein eingefrorenes, um Autorendaten bereinigtes Paket. Melde fehlende Resolver, Reviewer oder Belege als Laufzeitlücke.
