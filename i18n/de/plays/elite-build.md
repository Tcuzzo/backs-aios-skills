# Elite Build — das Master-Play

Nutze das vollständige Play, wenn es ausdrücklich angefordert ist oder ein Build,
Fix oder Uplift seine kombinierten Design-, Build-, Qualitäts- und Reviewstufen
braucht. Der Mensch nennt das Ziel einmal. Eine begrenzte Änderung darf relevante
Methoden aus BACKS Build Flow nutzen, ohne dieses ganze Play zu starten; wird
es gewählt, bleiben alle folgenden anwendbaren Gates erhalten.

## Eine Aufgabe, ein Integrationsverantwortlicher

[BACKS Build Flow](../skills/backs-build-flow/SKILL.md) besitzt Aufgabenpaket,
`task_mode`, Operator-Essence und Abschluss. Verwende aktuellen Kontext, tatsächlich
geladene Skill-Texte und Belege weiter; erneuere eine Stufe nur bei geänderten
Eingaben oder Kandidaten. Bewahre festen `base_sha`, aktuellen `candidate_sha`
und einen Integrationsverantwortlichen über alle Lanes. Ein Spezialist startet keinen zweiten Lebenszyklus.

[bounded-loops](../skills/bounded-loops/SKILL.md) besitzt ursprüngliche Frist und
Missionsrestkontingente. Recherche, Builder, Lint-/Typ-/Tests, Mutation, Reviews,
Fallback-Modelle und Übergaben verbrauchen dieselben Grenzen. Setze sie im
verschachtelten Play nie zurück. Bei Erschöpfung: **STILL-BUILDING** mit Kandidat,
Belegen, offenen Gates und nächster Handlung sichern; erledige nützliche
autorisierte Arbeit, die das erschöpfte Kontingent nicht verbraucht. Eine Budgetgrenze erlässt kein Gate.

## Die Kette

0. [optimus](../skills/optimus/SKILL.md) — Fundament und Build Flow einmal pro
   Session herstellen. Verwende tatsächliche Texte weiter, die noch im Kontext
   stehen, samt ihren Quellenbelegen; ein Beleg allein ersetzt keinen fehlenden
   Text. Ein verschachtelter Aufruf startet den Lebenszyklus nicht neu und
   behauptet keinen nie erfolgten Skill-Aufruf.
1. Nutze Absicht und Operator-Essence aus Build Flow. Lies ganze Anfrage und
   aktuelle Korrekturen; leite die Direktive vor einer Liefer- oder Optionsfrage
   ab. Löse durch Belege entscheidbare Fragen direkt.
2. [human-calibration](../skills/human-calibration/SKILL.md) — wende das validierte
   Profil aus dem Aufgabenpaket an. Lade fehlenden relevanten Kontext; verhöre
   den Menschen nicht erneut und rekonstruiere nicht in jeder Stufe dasselbe Profil.
3. [turn-and-burn](../skills/turn-and-burn/SKILL.md) — bewahre Modelllisten- und
   Planreview-Anforderungen der Mission. Konsultiere Modell-Essences (know-thyself),
   `docs/BACKS_LESSONS_LEARNED.md` und `memory/MEMORY.md`, soweit verfügbar. Diese
   Fähigkeits- und Erfahrungsdaten sind von Operator-Essence getrennt. Nutze
   aktuelle Burn-Belege weiter; nötige Absorb-Arbeit teilt dieselbe Mission und
   liefert ihr Ergebnis an den Integrationsverantwortlichen zurück.
4. [understanding-gates](../skills/understanding-gates/SKILL.md) — bewahre
   Design → Plan → Build → Test → Ship. Prüfe mit
   [live-research](../skills/live-research/SKILL.md) betroffenen Pfad, Verantwortliche,
   Verbraucher und Liefergrenze. Folge weiteren Abhängigkeiten, wenn Belege zeigen,
   dass sie das Ergebnis ändern können; wiederhole vor jedem Edit keine
   Gesamtsystemaufnahme. Beginne den nächsten ausführbaren Schritt, sobald
   Build Flows Bedingungen für ausreichenden Kontext erfüllt sind.
5. [architecture-engineer](../skills/architecture-engineer/SKILL.md) — bei Änderungen
   an Modulgrenze, Abhängigkeitsrichtung oder geteilter Schnittstelle strukturelles
   Review und Klassifizierung der Autoritätsfläche anwenden. Belege jeden Verstoß
   mit lokaler Regel oder konkretem Fehlermodus; dauerhafte Entscheidungen bekommen eine ADR.
6. [wayfinder](../skills/wayfinder/SKILL.md) — kartiere eine tatsächlich offene
   Route aus Belegen. Starte keine neue Planung, wenn der Weg bereits bekannt ist.
7. [red-first](../skills/red-first/SKILL.md) — beobachte und committe den echten
   Fehlervertrag vor seinem Builder. Erfasse das Siegel und bewahre die
   Originaldatei Byte für Byte. Spätere Befunde erhalten separate Ergänzungstests;
   sie schreiben das ursprüngliche RED nicht um.
8. Baue die kleinste vollständige Änderung an der zuständigen Schnittstelle.
   Parallelisiere unabhängige Fragen und Arbeiten mit explizitem Dateibesitz oder
   isolierten Worktrees; bewahre einen Integrationsverantwortlichen und
   Nebenläufigkeitsregeln des Projekts. Wähle Builder über
   [fleet-ladder](../skills/fleet-ladder/SKILL.md), gegebenenfalls mit
   [model-fusion](../skills/model-fusion/SKILL.md). Wende bei Defekten
   [repair-loop](../skills/repair-loop/SKILL.md) innerhalb des Ablaufs an und
   schließe die Klasse an der gemeinsamen Schnittstelle nach
   [seam-engineering](../skills/seam-engineering/SKILL.md). Gib Befunde an diese
   Aufgabe zurück, statt das Play rekursiv neu zu starten.
9. [sniper-testing](../skills/sniper-testing/SKILL.md) — leite Prüfungsumfang aus
   dem festgehaltenen Gesamtdiff von Basis zu Kandidat plus eigenen ausstehenden
   Pfaden ab. Führe tatsächliche Lint-, Typprüf- und gezielte Testbefehle des
   Repositories aus. Erfasse N/A mit Grund und fehlende Pflichttools als Lücken;
   installiere keine beliebigen Prüfer und erfinde keine Erfolge. Iteriere mit gezielten Läufen.
10. [clean-code-gauntlet](../skills/clean-code-gauntlet/SKILL.md) — wende Qualität,
    Komplexität/Coverage und begrenzte Mutation im selben Ablauf auf denselben
    Kandidaten an. Ein relevanter Überlebender oder Befund führt im Restbudget
    zu ergänzendem RED und minimalem Schnittstellenfix. Verwende gültige Belege,
    nie ein altes Urteil für andere Bytes; starte keinen zweiten vollständigen Build-Zyklus.
11. [blind-eval](../skills/blind-eval/SKILL.md), dann
    [blind-tribunal](../skills/blind-tribunal/SKILL.md) — gib ein eingefrorenes,
    autorenbereinigtes Belegpaket an live nach Fähigkeit und Verfügbarkeit
    ausgewählte Prüfer. Reviews brauchen frische autor-disjunkte Ausführungen
    ohne geerbtes Builder-Gespräch. Erfasse die erstellende Ausführung als
    Provenienz und schließe sie aus. Jeder belegte Befund erhält separates RED,
    Fix und erneutes Review im selben Restkontingent. Alle erforderlichen Juroren
    müssen vor der Landung bestehen. Beachte gegebenenfalls die Solo-rig-Regel
    des Tribunals; erfasse tatsächliche Konfiguration und Runtime-Lücken, ohne
    Unabhängigkeit zu schwächen.
12. Erfülle den gewünschten Abschluss. Prüfe Kandidatenidentität erneut, führe
    einen vollen Lauf der betroffenen Modulsuiten plus Projektpflichtprüfungen
    aus, bewahre parallele Arbeit und folge der autorisierten Landungsprozedur.
    Verifiziere beim Deployment installierten/laufenden Code und echte
    Nutzeroberfläche. Starte einen Dienst nur neu, wenn gewünschte Lieferung
    und tatsächliches Verfahren es brauchen. Ein lokaler Patch oder Review
    erhält nicht stillschweigend Freigabeumfang.

## Harte Gates

- Ursprüngliches RED wurde vor dem Fix scheitern gesehen und bleibt Byte für Byte
  identisch; ergänzende Verträge haben eigene Belege und Siegel.
- Pflichtprüfungen für Qualität, Lint/Typ/Tests und Mutation bestehen am exakten
  Kandidaten, mit begründetem N/A und ehrlich gemeldeten tatsächlichen Lücken.
- Erforderliches Review nutzt frische autor-disjunkte Ausführung; der Builder
  bewertet nie sich selbst und gibt dem Prüfer kein gewünschtes Urteil vor.
- Jeder Befund der eigenen Schnittstelle wird gefixt oder mit Belegen entschieden.
  Offene Befunde werden ausdrücklich gesichert und blockieren die Landung; sie werden nie versteckt.
- Anwendbare Burn-, Essence-, Lessons- und Planreview-Anforderungen sind durch
  aktuelle Belege erfüllt. Wiederverwendung erlaubt kein Überspringen von Pflichtgates.
- Fähigkeit **PROVEN** heißt gelandet, unabhängig bewertet und auf der echten
  Nutzeroberfläche demonstriert. Sonst melde **STILL-BUILDING** und den genau
  fehlenden Nachweis nach [human-voice](../skills/human-voice/SKILL.md).
  Benenne einen erfüllten Review- oder lokalen Patchauftrag getrennt von einer Live-Fähigkeitsbehauptung.
- Committe nur Dateien dieser Aufgabe. Bewahre Arbeit anderer Sessions.

## Fleet-Ladder-Richtlinie

Nutze [fleet-ladder](../skills/fleet-ladder/SKILL.md) für tatsächlichen Dispatch,
konfigurierte Routen, Live-Probes, Fallback und Reviewunabhängigkeit. Lies
`config/fleet_ladder.yaml` und `config/gpu_nodes.yaml` der Installation, soweit
vorhanden; das Pack erzeugt keinen Resolver. Bewahre Research-before-lift für
konfigurierte Frontier-Stufen samt erlaubten Web-, GitHub-, Reddit- und Paperquellen.
Beachte konfiguriertes Denkminimum und Token-Effizienz; kodiere keine Modell-IDs
fest und kürze keine Belege, um Konformität vorzutäuschen.

Bewahre mit [session-handoff](../skills/session-handoff/SKILL.md) vor Unterbrechung
Kandidaten, Siegel, Belege, Frist und Missionsrestkontingente.
