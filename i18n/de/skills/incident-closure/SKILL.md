---
name: "incident-closure"
description: "Nutze das, wenn der Mensch Bruch meldet oder \"fix it\" sagt — besonders wenn die normale Steuerungsebene (API, CLI, Service) tot ist und du darunter greifen musst. Die Antwort ist ein voller Understanding-first-Abschluss — Root Cause mit Evidenz, fehlschlagender Test zuerst, grün, Live-Beweis auf dem eigenen Pfad des Menschen, Commit — nie ein Optionsmenü zurück an ihn. Trigger words: fix it, fix shit, full close, broken, wiped, down, it stopped working, recover, restore, kaputt, reparieren, wiederherstellen, ausgefallen, geht nicht mehr."
license: "MIT"
---

# Voller Abschluss
**Effort:** free — Reihenfolge-Disziplin an einem Fix, den du ohnehin schuldest: Platten-Wahrheits-Proben und der fehlschlagende Test kommen zuerst, nicht obendrauf. Beseitigt: Options-Menüs und Schritt-für-Schritt-Rückfragen, die dem Menschen mitten im Ausfall zugeworfen werden.

Wenn der Mensch Bruch meldet oder „fix it“ sagt, gibt es genau eine richtige
Antwort: einen vollen, Understanding-first-Abschluss. Root Cause mit Evidenz, ein
fehlschlagender Test zuerst, grün, Live-Beweis auf dem eigenen Pfad des Menschen,
dann Commit. Nie ein Optionsmenü zurück an ihn, und nie ein Bestätigungs-Prompt
pro Schritt — er hat schon gesagt: fix it.

Wo Geschwister-Skills ein explizites Ja für destruktive Akte verlangen, gewinnt
diese Regel nur die reversible Hälfte: Das „fix it“ des Menschen IST das stehende
Ja für reversible Recovery-Writes, die eine Backup-Spur hinterlassen; alles
Irreversible — Datenvernichtung, Ausgaben, Sendungen nach außen — geht weiter
über die [decision-bar](../decision-bar/SKILL.md), und die Latte gewinnt.

Bitte den Menschen nur um etwas, wenn es nachweislich überall sonst verloren ist
und nur er es liefern kann. Jeden anderen Input gehst du suchen.

## Die Methode

1. **Probe die normale Oberfläche — dann hör auf, ihr zu trauen.** Rufe die API
   oder CLI einmal. Antwortet sie normal, ist das kein Incident-Closure-Fall;
   übergib. Kommt 401/403, Connection refused, leere Ergebnisse, wo Daten sein
   sollten, oder abgestandene Daten: Behandle diese Oberfläche nicht mehr als
   maßgeblich.
2. **Stelle die Bodenwahrheit von der Platte her, nicht von der API.** Vertraue
   nie einem kaputten Service, den eigenen Zustand zu beschreiben. Lies
   Datendateien, Verzeichnislisten und Änderungszeiten selbst, und vergleiche mit
   dem, was die API behauptet. Divergenz ist das diagnostische Signal.
3. **Scanne den Explosionsradius.** Durchsuche jedes Top-Level-Datenverzeichnis
   nach Dateien, die im Fehlerfenster angefasst wurden (z. B.
   `find /data/volumes -newermt "<start>" ! -newermt "<end>"`). Ziel ist eine
   Ein-Bildschirm-Antwort auf „Was wurde berührt, was nicht“. Ein enger Radius
   (ein Volume, eine Tabelle) ist hier erholbar. Ein breiter Radius (viele
   Volumes, das ganze Datenverzeichnis) ist Disaster Recovery — eskalieren, nicht
   improvisieren.
4. **Inventarisiere Überlebende vs. Verluste.** Klassifiziere jedes betroffene
   Asset:
   - intakt auf der Platte — wiederherstellen, wie es ist
   - aus dem Repo rekonstruierbar — Configs und Backups in Git
   - aus Env- oder Credential-Dateien rekonstruierbar — Tokens, Passwörter
   - dauerhaft verloren — verschlüsselt mit fehlendem Schlüssel, reiner
     Laufzeit-Zustand
   Nur der letzte Eimer rechtfertigt, den Menschen zu fragen. Alles andere baust
   du wieder auf.
5. **Root Cause mit Evidenz, dann ein roter Test.** Benenne, warum es brach, mit
   Beweis von der Platte — keine Vermutung. Wo der Defekt Code ist, schreib den
   fehlschlagenden Test, der ihn festhält, vor dem Fix, und mach ihn grün. Siehe
   [red-first](../red-first/SKILL.md) und
   [root-cause-first](../root-cause-first/SKILL.md).
6. **Kaskadiere durch die Schichten nach unten — nie nach oben zum Menschen.**
   Ist der bevorzugte Pfad kaputt, geh eine Schicht tiefer und versuch es neu:
   API / SDK → CLI im Container → direkte DB-Writes → Dateisystem-Chirurgie.
   Frag den Menschen nicht, solange Kaskaden unversucht sind. Jede Sprosse nach
   unten ist billiger als fragen.
7. **Nimm an, dass Abhängigkeiten auch kaputt sind.** Recovery-Code nutzt nur die
   Standardbibliothek deiner Sprache für HTTP und JSON — Drittanbieter-Clients
   könnten Teil dessen sein, was starb.
8. **Schreibe idempotent, mit Backup-Spuren.** Jeder Platten-Write hinterlässt
   eine zeitgestempelte `.bak`-Kopie neben dem Ziel. Lesen, plausibilisieren,
   kopieren, schreiben, nachprüfen — nie blind überschreiben. Wenn du ein
   Credential temporär tauschst, um einen neuen Key zu prägen: das Original erst
   sichern und vor der Rückkehr wiederherstellen — das eigene Login des Menschen
   überlebt unberührt.
9. **Verifiziere mit Live-Calls auf dem eigenen Pfad des Menschen.** Fahre die
   Probe aus Schritt 1 erneut und bestätige, dass die Zahlen zum
   Vor-Incident-Inventar oder den Repo-Backups passen. Ein grüner DB-Zustand ist
   kein Beweis; die Oberfläche, die der Mensch nutzt, läuft wieder — das ist der
   Beweis.
10. **Committe und berichte.** Committe nur die eigenen Dateien des Fixes.
    Berichte: was geprobt wurde, den Explosionsradius, die Aktionen in
    Reihenfolge, die wiederhergestellten Zählstände, was dauerhaft verloren ist
    (leer, wenn nichts), und jeden Schritt, der nicht-fatal scheiterte.

## Rote Flaggen — anhalten und neu proben

- „Ich frag mal den Menschen, warum es brach“ — nein; finde es zuerst von der
  Platte heraus.
- „Die API sagt, hier ist nichts“ — die Selbstsicht einer kaputten API ist keine
  Wahrheit.
- „Ich installiere einfach sauber neu“ — du wirfst wiederherstellbaren Zustand
  weg.
- „Der Schlüssel ist weg, also sind die Credentials nutzlos“ — Klartextwerte
  leben oft noch in Env- oder Credential-Dateien; lege das Credential neu an.
- „Vor jedem Schritt bestätigen?“ — der Mensch hat fix it gesagt; fahre die
  Kaskade, berichte am Ende.

## Harte Regeln — eine verletzt, und der Skill ist gescheitert

- Optionen zurück an den Menschen, obwohl ein klarer Lösungsweg existiert.
- Ein destruktiver Write ohne `.bak`-Spur.
- Der Mensch wurde um etwas gebeten, bevor Kaskade und Inventar trocken liefen.
- Ein stillgelegtes Subsystem „hilfreich“ wiederbelebt — dass ein außer Dienst
  gestellter Service unten bleibt, ist der gewollte Zustand, und ihn zu
  reaktivieren ist die bewusste Entscheidung des Menschen.
- Recovery aus internem Zustand für fertig erklärt, statt per Live-Probe auf
  seinem Pfad.
- Der Fix uncommittet gelassen (außer der Mensch sagte explizit: kein Commit).

## Passt gut zu

- [repair-loop](../repair-loop/SKILL.md) — die Code-Fix-Schleife, die dieser Abschluss fährt, wenn der Defekt im Code liegt.
- [root-cause-first](../root-cause-first/SKILL.md) · [red-first](../red-first/SKILL.md)
- [decision-bar](../decision-bar/SKILL.md) — was den Menschen erreichen darf, und wie.
