---
name: "model-fusion"
description: "Wenn mehrere unabhängig erarbeitete Lösungsansätze der Aufgabe helfen und ins verbleibende Budget passen, oder der Operator ausdrücklich ein Panel verlangt. Modellunabhängige Entwürfe, Auswahl oder Synthese und Verifikation; dasselbe konfigurierte Modell darf getrennte Rollen in isolierten Sitzungen ausführen."
license: "MIT"
---

# Model Fusion
**Effort:** heavy — unabhängige Entwürfe, ein Prüfer und optional ein Schreiber; setze das Panel nur ein, wenn sein Nutzen für die Aufgabe den Aufwand im verbleibenden Budget rechtfertigt.

Das Panel ist optional. Getrennte Ausführungen entwerfen dieselbe Aufgabe; ein
Prüfer, der an keiner dieser Ausführungen beteiligt war, wählt oder kombiniert
Kandidaten. Der gewählte Entwurf wird gegen den ursprünglichen Auftrag geprüft.
Dasselbe geeignete konfigurierte Modell darf Entwurf, Prüfung und Schreiben in
getrennten, isolierten Sitzungen übernehmen. Modell- oder Anbieterwechsel sind
keine Voraussetzung. Der Prüfer erbt weder Gespräch noch Arbeitskontext der Autoren.

## Wann einsetzen

- Wenn unterschiedliche Ansätze eine konkrete Unsicherheit der Aufgabe klären
  können und ihre Prüfung in das verbleibende Missionsbudget passt.
- Wenn der Operator ausdrücklich ein Panel verlangt; benenne verfügbare Rollen
  und Grenzen. Umfangreiche Arbeit allein macht ein Panel nicht verpflichtend.
- Für einfache Änderungen reicht die direkte Umsetzung mit passender Verifikation.

Binde [bounded-loops](../bounded-loops/SKILL.md) ein. Entwürfe, Richter, Schreiber
und Reparaturrunden teilen Frist, Restversuche und Ressourcen der bestehenden
Mission. Neue Rollen oder Sitzungen setzen diese Grenzen nicht zurück. Führe
unabhängige Entwürfe parallel aus, wenn der Host es unterstützt, sonst nacheinander
innerhalb derselben Grenzen. Behaupte keine nicht vorhandene Sitzungsisolation.

## Die drei Stufen

### 1. Panel — unabhängige Entwürfe

1. Gib jeder isolierten Entwurfssitzung dieselbe Aufgabe und dasselbe Aufgabenpaket.
2. Jeder Entwerfer arbeitet allein. Kein Entwerfer sieht die Arbeit eines anderen.
3. Ein Entwerfer, der einen Fehler wirft, in den Timeout läuft oder leer
   zurückkommt, wird geloggt und fallen gelassen. Er killt nie die Runde.
   Logg den Drop laut — schluck ihn nie.
4. Sammle jeden nicht-leeren Kandidaten ein.

### 2. Richter — ein Außenstehender wählt und merged

1. Vor dem Richten läuft ein billiges mechanisches Gate über jeden Kandidaten:
   lässt er sich sauber anwenden? Parst er? Fahr die Probe auf einer
   Wegwerf-Kopie, nie auf dem Live-Baum. Kandidaten, die am Gate scheitern,
   sind raus, bevor der Richter sie sieht.
2. Zwei Richter-Formen — wähl pro Config eine:
   - **Synthese:** der Richter analysiert jeden Kandidaten (Stärken, Defekte,
     Konflikte), dann komponiert eine getrennte Schreibausführung die finale
     Antwort aus dieser Analyse. Rollen und Sitzungen bleiben getrennt;
     dasselbe geeignete konfigurierte Modell darf beide ausführen.
   - **Auswahl:** der Richter wählt den einen besten Kandidaten, der das Gate
     bestanden hat. Billiger. Nimm sie, wenn Mergen nichts bringt.
3. Ist Richter oder Schreiber nicht verfügbar, degradier LAUT auf Auswahl über
   dieselben Kandidaten. Verschwende das Panel nie stumm; tu nie so, als hätte
   eine Synthese stattgefunden.
4. Überlebt kein Kandidat das Gate, häng den besten Fehler an den Prompt und
   lass das Panel neu laufen — begrenzt, höchstens 2 Reparatur-Runden. Bei
   Erschöpfung gib Fehlschlag mit der vollen Fehlerliste zurück. Gib nie ein
   leeres oder wirkungsloses Ergebnis als Erfolg zurück.

### 3. Validieren — den Sieger gegen die Absicht prüfen

1. Lies die ursprüngliche Frage neu. Tut der Sieger, was gefragt war — alles
   davon, und nichts, was nicht gefragt war?
2. Prüf semantische Korrektheit, Stil-Passung zum umliegenden Code, und dass er
   sich weiterhin sauber anwenden lässt.
3. Niedriges Vertrauen wird als Eskalations-Flag sichtbar gemacht, nicht
   versteckt. Dann beweis es auf dem normalen Weg: erst der fehlschlagende
   Test, dann grün, dann Live-Verhalten. Ein gemergter Entwurf, der nie lief,
   ist eine Vermutung.

## Die Leiter

- Wähle Panelgröße und Rollen nach benötigten Fähigkeiten, tatsächlicher
  Verfügbarkeit, aktueller Konfiguration und Restbudget. Keine festen Modelle,
  Anbieterpräferenzen oder vorgeschriebene Modellvielfalt. Melde Konfigurationslücken.
- Config-Format, Rollen-statt-Namen und Live-Probe-Auflösung gehören zu
  [fleet-ladder](../fleet-ladder/SKILL.md).

## Harte Regeln — eine gebrochen, und der Skill ist gescheitert

- **Der Builder richtet nie.** Die prüfende Ausführung hat keinen Kandidaten
  verfasst und erbt kein Gespräch oder Arbeitskontext der Autoren. Der finale
  Bewerter arbeitet in einer frischen, vom Autor getrennten Sitzung.
- **Keine hartcodierten Modellnamen** an irgendeiner Aufrufstelle. Rollen im
  Code, Modelle in der Config.
- **Kein stummes Degradieren.** Gefallene Entwerfer, Richter-Fallback,
  Gate-Fehlschläge und Erschöpfung sind alle laut. Ein nicht bewertbares
  Ergebnis besteht nie per Default.
- **Begrenzte Reparatur.** Panel-Neuläufe haben eine harte Obergrenze und
  verbrauchen das verbleibende Missionsbudget. Es gilt die zuerst erreichte
  Grenze. Erschöpfung ergibt einen sichtbaren Checkpoint, keine Endlosschleife.
- **Grüne Tests allein sind nicht fertig.** Der Sieger wird am Live-Verhalten
  bewiesen.

## Passt gut zu

- [fleet-ladder](../fleet-ladder/SKILL.md) — klär, welche Modelle oben sind, bevor das Panel feuert.
- [blind-tribunal](../blind-tribunal/SKILL.md) — das fail-closed Bewertungsgericht, wenn der primäre Bewerter stirbt.
- [red-first](../red-first/SKILL.md) — der fehlschlagende Test, den der Sieger-Entwurf grün machen muss.
- [blind-eval](../blind-eval/SKILL.md) — das Keep-or-Revert-Geschmacks-Gate, wenn kein Test entscheiden kann.
