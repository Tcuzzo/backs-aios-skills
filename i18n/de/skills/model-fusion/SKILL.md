---
name: model-fusion
description: Wenn die Antwort eines einzelnen Modells nicht vertrauenswürdig genug ist — ein harter Build, Fix oder Entwurf, bei dem mehrere Modelle antreten sollen und ein unabhängiger Richter wählt. Ein Panel entwirft parallel, ein Richter merged den Sieger, das Ergebnis wird gegen die ursprüngliche Absicht validiert. Trigger words: fusion, panel, judge, multi-model, ensemble, draft and merge, builder not grader, Richter, Mehrmodell, Entwürfe parallel, Sieger mergen, Builder nicht Bewerter.
license: MIT
---

# Model Fusion
**Effort:** heavy — ein volles Panel, das parallel entwirft, plus ein unabhängiger Richter (und optional ein Schreiber); investier das in harte Builds und Fixes, die ausgeliefert werden, nie in Einzeiler. Beseitigt: die Wette der ganzen Änderung auf den Entwurf eines einzigen Modells — und die Nacharbeit, wenn genau dieser Entwurf falsch ist.

Viele unabhängige Stimmen schlagen eine. Ein Panel aus Modellen entwirft
dieselbe Aufgabe parallel. Ein Richter — ein Modell, das keinen der Entwürfe
geschrieben hat — wählt oder merged den besten. Der Sieger wird dann gegen das
geprüft, was wirklich gefragt war.

## Wann einsetzen

- Jeder größere Build, Fix oder Uplift, bei dem Qualität mehr zählt als Tempo.
- Wenn du ein konkretes Paar unabhängiger Bewerter willst, kein blindes
  Vertrauen in ein Modell.
- NICHT für triviale Einzeiler. Mach die direkte Änderung und verifizier sie.

## Die drei Stufen

### 1. Panel — Entwürfe parallel

1. Schick dieselbe Aufgabe mit demselben Kontext an alle Panel-Modelle zugleich.
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
     Konflikte), dann komponiert ein separates Schreiber-Modell die finale
     Antwort aus dieser Analyse. Schreiber und Richter sind verschiedene
     Rollen; halt sie als verschiedene Modelle, wenn du kannst.
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

- Fusions Sprossen-Form: unten ein breites Panel billiger Modelle, nach oben
  engere Panels und engere Output-Budgets — eine falsch konfigurierte Sprosse
  scheitert laut beim Laden.
- Config-Format, Rollen-statt-Namen und Live-Probe-Auflösung gehören zu
  [fleet-ladder](../fleet-ladder/SKILL.md).

## Harte Regeln — eine gebrochen, und der Skill ist gescheitert

- **Der Builder richtet nie.** Der Richter hat keinen Kandidaten geschrieben.
  Der finale Bewerter ist ein anderes Modell (ideal: eine andere Familie) als
  wer auch immer den Sieger gebaut hat.
- **Keine hartcodierten Modellnamen** an irgendeiner Aufrufstelle. Rollen im
  Code, Modelle in der Config.
- **Kein stummes Degradieren.** Gefallene Entwerfer, Richter-Fallback,
  Gate-Fehlschläge und Erschöpfung sind alle laut. Ein nicht bewertbares
  Ergebnis besteht nie per Default.
- **Begrenzte Reparatur.** Panel-Neuläufe haben eine harte Obergrenze.
  Erschöpfung ist ein lauter Fehlschlag, keine Endlosschleife.
- **Grüne Tests allein sind nicht fertig.** Der Sieger wird am Live-Verhalten
  bewiesen.

## Passt gut zu

- [fleet-ladder](../fleet-ladder/SKILL.md) — klär, welche Modelle oben sind, bevor das Panel feuert.
- [blind-tribunal](../blind-tribunal/SKILL.md) — das fail-closed Bewertungsgericht, wenn der primäre Bewerter stirbt.
- [red-first](../red-first/SKILL.md) — der fehlschlagende Test, den der Sieger-Entwurf grün machen muss.
- [blind-eval](../blind-eval/SKILL.md) — das Keep-or-Revert-Geschmacks-Gate, wenn kein Test entscheiden kann.
