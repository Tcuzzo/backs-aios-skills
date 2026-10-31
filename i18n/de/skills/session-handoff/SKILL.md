---
name: "session-handoff"
description: "Wenn eine Session endet, Kontext kompaktiert wird, ein Missionskontingent erschöpft ist oder unfertige Arbeit in einem anderen Agenten oder Harness weitergehen muss. Trigger words: handoff, compact, save state, before restart, Übergabe."
license: "MIT"
---

# Session Handoff
**Effort:** free — eine flache Datei, geschrieben bevor der Kontext stirbt; keine Modell-Calls, und beim nächsten Session-Start senkt sie die Kosten unterm Strich. Beseitigt: dass der frische Agent den Zustand neu herleitet, schon bezahlte Fallen noch einmal bezahlt und Entscheidungen in einem toten Kontextfenster verliert.

Ein Kontextfenster stirbt; die Arbeit darf es nicht. Bevor eine Session endet
oder kompaktiert, schreib eine flache Datei, die ein brandneuer Agent kalt
lesen und fortsetzen kann — was getan wurde, wo es liegt, was halb fertig ist
und das exakte nächste Kommando. Eine Build-Übergabe muss das Kontextfenster
überleben. Nutze den vorhandenen [BACKS Build Flow](../backs-build-flow/SKILL.md)-
Aufgabeneintrag; dieser Skill überträgt die Aufgabe, statt einen neuen
Verantwortlichen, Kontextdurchgang oder eine neue Mission zu erzeugen.

## Wann eine schreiben

- Bevor das Kontextfenster kompaktiert oder geleert wird.
- Beim Beenden einer Session mit noch offener Arbeit.
- Direkt nach dem Landen von etwas Großem (die Commit-Id notieren, solange sie
  frisch ist).
- In dem Moment, in dem eine echte Entscheidung zu deinem Menschen geht
  (festhalten, was jede Wahl bedeutet).

## Wohin sie geht

Ein bekannter Ort, an dem der nächste Agent ZUERST schaut. Teilt der nächste
Agent dein Projekt, nimm eine stabile Ledger-Datei im Repo und committe das
Update, damit es einen Maschinen-Neustart überlebt, nicht nur ein
Kontext-Leeren. Ist der nächste Agent ein anderes Harness oder ein frischer
Login, schreib eine flache portable Datei ins Temp-Verzeichnis — sie ist
Gerüst, kein getracktes Artefakt.

Beachte `task_mode` und Schreibbefugnisse. Gib bei Nur-Lese- oder eingefrorenem
Review die Übergabe in der Antwort oder einem bereits autorisierten externen
Eintrag zurück; schreibe kein Journal ins geschützte Repository, um diesen Skill zu erfüllen.

## Erst Parallel-Arbeit verifizieren (bevor du ein Wort schreibst)

Prüf, dass Arbeit aus ANDEREN Sessions gesichert ist. Fahr `git status`,
`git log` und `git worktree list`. Notier schmutzige Dateien und ungemergte
Branches ehrlich im Dokument. Änder nie die uncommitteten Sachen einer anderen
Session, damit die Übergabe sauber aussieht — das ist der
Datenverlust-Defekt. Eine Übergabe, die einen sauberen Zustand beschreibt,
während eine andere Session Arbeit im Flug hat, ist eine falsche Behauptung.

## Was rein gehört — je ein kurzer Abschnitt

1. **Ziel.** Die Arbeit in einem Satz. Der nächste Agent darf nicht raten müssen,
   was „fertig“ heißt. Übertrage `mission_id`, `task_mode`, Integrationsverantwortlichen,
   gewünschten Abschluss und bereits autorisierte Lieferhandlungen.

2. **Zustand.** Gelandet (Commit-IDs), im Bau, wartend. Verweise auf Spezifikationen,
   Pläne, Issues und Diffs per Pfad oder URL, ohne Inhalte zu duplizieren.
   Enthalten sein müssen fester `base_sha`, aktueller `candidate_sha`, versiegelte
   RED-Pfade/Commit/Hashes, Prüfbefehle/-ergebnisse und genauer Kandidat jedes Belegs.

3. **Wo die Arbeit lebt.** Branches, Worktrees, schmutzige Dateien. Benenn die
   exakten Dateien, die der nächste Agent zuerst lesen muss.
4. **Die Urteils-Spur.** Wer oder was jedes Stück bewertet hat und was die
   echten Treffer waren. Ein gescheitertes Urteil mit benannten Defekten ist
   MEHR wert als ein grünes — schreib die Defekte wortwörtlich hin.
5. **Halbfertiges und das exakte nächste Kommando.** Was mitten im Flug ist,
   und das wörtliche Kommando, das es fortsetzt.
6. **Offene Entscheidungen.** Alles, was auf deinen Menschen wartet, und was
   jede Wahl bedeutet. Eine Entscheidung darf nie nur in einem toten
   Kontextfenster existieren.
7. **Unerfüllte Verträge.** Tests noch rot, Beweise noch fehlend, Versprechen
   gemacht, aber noch nicht gehalten.
8. **Fallen.** Je eine Zeile. Eine Falle, für die du schon bezahlt hast, ist
   mehr wert als ein Grün — schreib sie hin, damit die nächste Session nicht
   nochmal zahlt.
9. **Empfohlene Skills.** Welche Skills der nächste Agent zuerst laden soll und
   warum. Benenne tatsächlich verfügbare Texte/Belege, nötige Aktualisierungen
   und Operator-Essence-Quelle; kopiere kein zweites Profil.
10. **Restbudget.** Übertrage ursprüngliche Frist und Gesamt-/Verbrauchs-/Restwerte
    für Versuche, Runden und weitere Grenzen aus [bounded-loops](../bounded-loops/SKILL.md),
    dazu ausstehende Aufrufe und letzte Hypothese/Fehler. Unbekanntes bleibt
    unbekannt. Setze bei Übergabe, Kompaktierung, Mitarbeiter- oder Modellwechsel
    niemals das Missionsbudget zurück.

## Harte Regeln

- **Schwärzen.** Keine API-Keys, Passwörter, Tokens oder persönlichen Daten.
  Keine echten Hostnamen, internen IPs oder Home-Pfade — nur Platzhalter;
  zeig auf echte Werte per Env-Variablen-Name. Eine Übergabe ist die Datei,
  die am ehesten die Maschine verlässt; ein Secret, das durch sie leckt, IST
  der Bug.
- **Abwesenheits-Behauptungen verrotten am schnellsten.** Bevor du „X
  existiert nicht" oder „X ist nicht gelandet“ schreibst, verifizier neu am
  aktuellen Commit — Parallel-Arbeit landet, während du schreibst.
- **Belegter Status pro Punkt.** Fähigkeitslieferung nutzt PROVEN nur mit
  erforderlichem Review und realem Oberflächennachweis; sonst benennt STILL-BUILDING
  den fehlenden Beleg. Ein abgeschlossener Review oder lokaler Patch kann den
  gewünschten Abschluss erfüllen, ohne zur deployten Fähigkeit umbenannt zu werden.
- **In zwei Minuten lesbar halten** (rund 120 Zeilen). Wächst sie darüber,
  archivier die ältesten Blöcke in einen Historien-Abschnitt — nie durch
  Löschen.

## Aufnehmen (die andere Hälfte)

Eine Session, die aus einer Übergabe startet, liest sie ZUERST und verifiziert
dann die obersten zwei, drei Behauptungen gegen `git log` und den Live-Baum,
bevor sie danach handelt. Die Übergabe ist eine Karte, keine Wahrheit — trau
ihr für das WO, verifizier das WAS.

Setze mit demselben Aufgabenpaket und Restkontingent fort. Prüfe die Frist vor
Arbeitsvergabe erneut; eine frische Session ist kein frisches Budget. Ist ein
Kontingent erschöpft, bewahre den STILL-BUILDING-Checkpoint und erledige nur
nützliche autorisierte Arbeit, die es nicht verbraucht. Bewahre ursprüngliches
RED-Siegel und feste Basis; ändere Kandidatenidentität nur bei tatsächlich geänderten Bytes.

## Passt gut zu

- [root-cause-first](../root-cause-first/SKILL.md) — die Untersuchung, die die nächste Session fortsetzt.
- [repair-loop](../repair-loop/SKILL.md) — mitten in der Schleife übergeben, ohne die Naht zu verlieren.
- [decision-bar](../decision-bar/SKILL.md) — wie offene Entscheidungen deinen Menschen erreichen.

> Scaffold credit: Matt Pocock, handoff (mattpocock/skills). Komposition und harte Regeln hier sind BACKS AIOS.
