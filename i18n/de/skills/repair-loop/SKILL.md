---
name: "repair-loop"
description: "Beim Reparieren eines Bugs, Schließen eines gemeldeten Issues, Verbessern einer gemeinsamen Schnittstelle oder Fortsetzen einer unfertigen begrenzten Reparatur. Trigger words: repair loop, dev mode, fix this, uplift, close the seam, dev build, Reparaturschleife."
license: "MIT"
---

# Repair Loop
**Effort:** light — die Schleife selbst ist Disziplin plus ein unabhängiger Benotungs-Durchgang; die schwereren Schritte, die sie verkettet (Gauntlet, Tribunal), tragen ihre eigenen Stempel und feuern nur bei Änderungen, die ausgeliefert werden. Beseitigt: Grün-aber-kaputt-Landungen und die Nacharbeit an wieder aufgerissenen Bugs, die sie kosten.

Die Standard-Schleife für jeden Fix, jeden Bug-Abschluss, jeden Uplift. Sie ist
ein Verhalten, keine Freigabe-Maschinerie: sie fügt dem Menschen null Gates und
null Reibung hinzu. Sie bindet den Agenten an eine Disziplin, die „grün, aber
kaputt" strukturell schwer auslieferbar macht.

## In die aktuelle Aufgabe einsteigen

Nutze [BACKS Build Flow](../backs-build-flow/SKILL.md) für Aufgabenpaket,
Operator-Essence und einen Integrationsverantwortlichen. Verwende passende Regeln,
Kontext, geladene Skill-Texte und Belege des Aufrufers weiter; erneuere nur
Verändertes. Ein direkter Aufruf klärt fehlenden Kontext einmal. Lade Fundament
und erforderliche Understanding-Gates, sofern noch nicht verfügbar; nutze wayfinder
nur für eine offene Route. Starte für einen Reparaturbefund nicht das äußere Build-Play neu.

[bounded-loops](../bounded-loops/SKILL.md) besitzt gemeinsame Frist und Restversuche/-runden.
Bewahre `mission_id`, `task_mode`, festen `base_sha` und aktuellen `candidate_sha`
über Reproduktion, Änderungen, Tools, Modelle, Reviews und Übergaben hinweg.
Verschachtelte Aufrufe setzen das Budget nie zurück. Review und Diagnose liefern
Belege ohne Änderungen oder Promotion; Build-Handlungen brauchen diesen Aufgabenrahmen.

## Die Schleife

1. **Den betroffenen Pfad erden.** Prüfe Regeln, aktuellen Projektcode,
   Aufruferverträge und vorhandene Prüfungen. Nutze aktuelle relevante Belege
   weiter, statt das ganze Repository erneut zu auditieren.
2. **Auf Live-Wahrheit reproduzieren.** Sieh das Versagen selbst, auf dem
   echten Pfad, den der Mensch nutzt — kein Proxy-Probe, kein Vertrauen aufs
   Wort des Bug-Reports. Keine Reproduktion, kein Fix.
3. **Roter Vertrags-Test.** Schreib einen fehlschlagenden Test, der den Defekt
   einfängt, und committe ihn vor dem Fix. Beweis, dass er wirklich rot ist.
   Der Fix macht ihn grün; der Fix editiert den Test nie. Siehe
   [red-first](../red-first/SKILL.md).
4. **Fix die KLASSE an der Naht** — kein Punkt-Pflaster pro Symptom. Die volle
   Formel steht in [seam-engineering](../seam-engineering/SKILL.md).
5. **Gezielte Prüfungen ausführen.** Leite mit [sniper-testing](../sniper-testing/SKILL.md)
   den Umfang aus dem Gesamtdiff von festem `base_sha` bis `candidate_sha` und
   eigenen ausstehenden Pfaden ab. Führe die echten Lint-, Typprüf- und Testbefehle
   des Repositories für diesen Umfang aus. Erfasse Befehl, Ergebnis und Revision.
   Kennzeichne Unanwendbares als **N/A** mit Grund; ein fehlendes Pflichttool ist
   eine Lücke. Installiere keine beliebigen Tools und erfinde keine Erfolge.
   Versiegelte Tests bleiben Byte für Byte identisch.
6. **Im Ablauf messen.** Nutze [clean-code-gauntlet](../clean-code-gauntlet/SKILL.md)
   für Qualität und begrenzte Mutationsbelege des Kandidaten. Untersuche einen
   überlebenden Mutanten; zeigt er eine Testlücke, ergänze eine separate Testdatei
   und bewahre das ursprüngliche RED. Repariere die zuständige Schnittstelle und
   wiederhole betroffene Prüfungen im selben Restbudget; schwäche nie ein Gate für GREEN.
7. **Unabhängige Bewertung.** Ein Bewerter, der die Änderung nicht geschrieben
   hat — live nach Fähigkeit und Verfügbarkeit aus der konfigurierten
   Sprossen-Matrix gewählt; die ausführende Session, die gebaut hat, und jede
   Session, die die Konversation oder den Kontext des Builders geerbt hat, sind
   disqualifiziert; ein Prüfer in einer frischen, autor-disjunkten Session
   muss sie durchwinken. Der
   Builder bewertet seine eigene Arbeit nie. Siehe
   [blind-tribunal](../blind-tribunal/SKILL.md).
8. **Nebenläufige Arbeit prüfen.** Bevor du geteilten Zustand änderst,
   verifizier, dass die laufende Arbeit anderer Sessions gesichert ist (auf
   einem Branch oder Commit). Committe oder räum nie Arbeit weg, die nicht
   deine ist.
9. **Im Umfang verifizieren und landen.** Zur Landung ein voller Durchlauf der
   betroffenen Modulsuiten plus vorgeschriebene Projektprüfungen, dann autorisierte
   Lieferprozedur. Prüfe Verhalten auf der echten Nutzeroberfläche oder dem echten
   Kommando und erfasse genaue Kandidaten-/installierte Revision. Lokale Tests
   und statische Upstream-Belege begründen keine Live-Lieferung. Schließe jeden
   Befund dieser Schnittstelle oder dokumentiere je Befund ein ausdrückliches,
   belegtes „kein Bug“. „Den Großen gefixt, den Rest vertagt“ landet nicht.

## Im Missionsbudget iterieren

Eine gescheiterte Prüfung liefert die nächste begrenzte Hypothese. Wiederhole
oder wähle eine fähige konfigurierte Route nur im Restkontingent; Modellwechsel
erzeugen keine neue Mission. Wende Stagnations- und Erschöpfungsregeln von
bounded-loops an. An einer Grenze: **STILL-BUILDING** mit aktuellem Kandidaten,
versiegelten Tests, Fehlerbelegen, offenen Gates und genauer nächster Handlung
sichern. Erledige nützliche autorisierte Arbeit, die das erschöpfte Kontingent
nicht verbraucht. Ein offener Befund blockiert die Landung, löscht aber keinen
Fortschritt und wird nicht zu erfundenem **PROVEN**.

## Harte Regeln — eine davon, und der Skill ist gerissen

- Fix ausgeliefert ohne Reproduktion auf Live-Wahrheit.
- Test nach dem Fix geschrieben, oder vom Fix editiert.
- Symptom geflickt, während die Klasse an der Naht offen bleibt.
- Fähigkeit über einen Proxy als grün behauptet, während der eigene Pfad des
  Menschen kaputt ist.
- Der Builder hat seine eigene Änderung bewertet.
- Ein hochgekommener Fund beim Landen stumm vertagt.
- Schleife zurückgesetzt, still aufgegeben oder trotz unerfülltem Gate als grün gemeldet.

## Report

Zwei Wörter — **PROVEN** oder **STILL-BUILDING** — plus die Absicht in
Klartext und die eine Entscheidung, die vor dem Menschen liegt, falls es eine
gibt. Fragen gehen nur für Geschmack, Vision oder destruktives Risiko an den
Menschen; siehe [decision-bar](../decision-bar/SKILL.md).

## Passt gut zu

- [incident-closure](../incident-closure/SKILL.md) — meldet der Mensch Bruch, läuft diese Schleife in einem vollen Abschluss.
- [red-first](../red-first/SKILL.md) · [seam-engineering](../seam-engineering/SKILL.md) · [sniper-testing](../sniper-testing/SKILL.md)
- [blind-tribunal](../blind-tribunal/SKILL.md) · [clean-code-gauntlet](../clean-code-gauntlet/SKILL.md)
