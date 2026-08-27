---
name: live-research
description: Wenn du über eine Codebase, eine API oder ein System nachdenkst, dessen echte Form zählt. Startet einen parallelen Research-Agenten, der die Live-Wahrheit liest — die eigenen READMEs des Projekts, die Abschnitts-Doku, den echten Quellcode — damit Schlüsse auf dem gründen, was wirklich da ist, nicht auf Modell-Gedächtnis. Trigger words: live research, ground the reasoning, read the real source, check what is actually there, primary sources, background research, verify against the repo, what do the docs say, lies die echte Quelle, Primärquellen, gegen das Repo prüfen, was sagt die Doku, Recherche im Hintergrund.
license: MIT
---

# Live Research
**Effort:** light — ein Recherche-Agent im Hintergrund, der die Live-Quelle liest, während die Hauptspur weiterarbeitet. Beseitigt: Schlüsse, gebaut auf Modell-Gedächtnis, das das echte Repo dann widerlegt — die Nacharbeit, wenn eine Vermutung ausgeliefert wurde.

Modell-Gedächtnis ist eine Vermutung darüber, wie ein Projekt zur Trainingszeit
aussah. Die Live-Wahrheit ist, was jetzt gerade auf der Platte und in der
offiziellen Doku steht. Dieser Skill fährt beide Spuren zugleich: während die
Hauptspur über ein Ziel nachdenkt, liest ein Research-Agent das echte Ding, und
seine Funde fließen ins Denken ein, **bevor** ein Schluss gezogen wird.

## Wann laufen lassen

- Du willst gleich über die Struktur eines Projekts, den Vertrag einer API oder
  das Verhalten einer Library nachdenken — und hast den aktuellen Quellcode
  nicht gelesen.
- Ein Design, ein Fix oder eine Behauptung hängt an Fakten, die seit deinen
  Trainingsdaten gedriftet sein könnten.
- Eine Frage braucht Fakten aus der echten Welt, die der Arbeitskontext allein
  nicht liefern kann.

## Die Schritte

1. **Starte den Rechercheur parallel.** In dem Moment, in dem das Nachdenken
   über ein Ziel beginnt, schick einen Research-Agenten im Hintergrund auf
   dasselbe Ziel. Die Hauptspur arbeitet weiter; der Rechercheur liest.
   Blockier die Arbeit nie mit Laufarbeit, die ein Agent allein erledigen kann.
2. **Lies die Live-Wahrheit, das Nächste zuerst.** Das README des Projekts,
   dann die Abschnitts-Doku am nächsten am Ziel, dann die echte Quellstruktur —
   echtes Verzeichnis-Listing, echte Dateiinhalte, echte Signaturen. Für Fakten
   außerhalb des Projekts: offizielle Doku, Quellcode, Specs, First-Party-APIs.
   Ein Blog, der die Doku zusammenfasst, ist keine Primärquelle.
3. **Streame Funde zurück, bevor Schlüsse fallen.** Funde fließen zur
   Hauptspur, sobald sie da sind, und das Denken arbeitet sie ein und
   korrigiert den Kurs. Ein Schluss, der gezogen wurde, bevor der Rechercheur
   zu dem Punkt berichtet hat, ist eine Vermutung — markier ihn als solche, bis
   die Live-Wahrheit ihn bestätigt oder kippt.
4. **Hefte jede Behauptung an die Quelle, der sie gehört.** Jeder Fund trägt
   seine Quelle direkt bei sich: einen Dateipfad, eine zitierte Zeile, einen
   Link, einen Commit. Eine Behauptung ohne Quelle wird laut als unbelegt
   markiert — nie als Fakt verkleidet.
5. **Schreib eine zitierte Datei.** Funde landen in einer einzigen
   Markdown-Datei, jede Behauptung mit Quelle. Leg sie dort ab, wo das Projekt
   solche Notizen schon sammelt; gibt es keine Konvention, wähl einen
   vernünftigen Ort und sag, wo — damit der nächste Agent sie findet.
6. **Erinnern vor Neu-Lesen.** Prüf zuerst Notizen aus früheren Sessions —
   dieselbe Quelle kann schon gezogen sein. Nutz den gecachten Fund wieder und
   zitier dieselbe Quelle. Minuten Erinnern schlagen Stunden Wiederentdecken.

## Harte Regeln

- **Kein Schluss vor dem Zusammenführen.** Hat der Rechercheur zu einem Punkt
  nicht berichtet, darf die Hauptspur den Punkt nicht als geklärt hinstellen.
- **Nur Primärquellen.** Verfolg jede Behauptung zurück zur Quelle, der sie
  gehört. Eine Zweitverwertung ist ein Zeiger, kein Beweis.
- **Headless, nie unter Beobachtung.** Hintergrund-Recherche nutzt einen
  Headless-Abrufpfad — nie einen Live-Browser, dem ein Mensch zuschaut; das ist
  eine andere Spur.
- **Nicht belegbar heißt: sag es.** Ein Fund ohne Primärquelle geht markiert
  raus, nie stumm unter den Rest gemischt.
- **Null Reibung für den Menschen.** Dieser Skill fügt keinen
  Freigabe-Schritt und kein Gate hinzu. Er ist Methoden-Disziplin, kein
  Kontrollpunkt.

## Was zurückkommt

Eine geerdete, zitierte Markdown-Datei — plus eine Denk-Spur, die mitten im
Flug korrigiert wurde statt erst, nachdem der Schluss schon raus war. Die
Hauptspur liest die Datei und macht weiter.

## Passt gut zu

- [wayfinder](../wayfinder/SKILL.md) — Research-Tickets sind der Agent-allein-Typ, den dieser Skill auflöst.
- [root-cause-first](../root-cause-first/SKILL.md) — dieselbe Quellen-zuerst-Disziplin, gerichtet auf Bugs.

> Scaffold credit: Matt Pocock, research (mattpocock/skills, MIT). Komposition und harte Regeln hier sind BACKS AIOS.
