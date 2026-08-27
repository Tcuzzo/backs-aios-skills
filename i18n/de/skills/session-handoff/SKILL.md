---
name: session-handoff
description: Wenn eine Session endet, das Kontextfenster gleich kompaktiert oder die Arbeit in einem anderen Agenten oder Harness weitergehen muss. Verdichtet die Session in eine flache Datei, die ein brandneuer Agent kalt lesen und fortsetzen kann — Zustand, Halbfertiges, das exakte nächste Kommando, offene Entscheidungen — mit geschwärzten Secrets und verifiziert gesicherter Parallel-Arbeit. Trigger words: handoff, hand off, compact, save state, continue in another session, portable handoff, before restart, Übergabe, Zustand sichern, in anderer Session weitermachen, vor dem Neustart.
license: MIT
---

# Session Handoff

Ein Kontextfenster stirbt; die Arbeit darf es nicht. Bevor eine Session endet
oder kompaktiert, schreib eine flache Datei, die ein brandneuer Agent kalt
lesen und fortsetzen kann — was getan wurde, wo es liegt, was halb fertig ist
und das exakte nächste Kommando. Eine Übergabe, die nur in Chat-Prosa oder im
Gedächtnis parkt, existiert nicht.

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

## Erst Parallel-Arbeit verifizieren (bevor du ein Wort schreibst)

Prüf, dass Arbeit aus ANDEREN Sessions gesichert ist. Fahr `git status`,
`git log` und `git worktree list`. Notier schmutzige Dateien und ungemergte
Branches ehrlich im Dokument. Änder nie die uncommitteten Sachen einer anderen
Session, damit die Übergabe sauber aussieht — das ist der
Datenverlust-Defekt. Eine Übergabe, die einen sauberen Zustand beschreibt,
während eine andere Session Arbeit im Flug hat, ist eine falsche Behauptung.

## Was rein gehört — je ein kurzer Abschnitt

1. **Ziel.** Die Arbeit in einem Satz. Der nächste Agent darf nicht raten
   müssen, was „fertig“ heißt.
2. **Zustand.** Gelandet (Commit-Ids), im Bau, in der Warteschlange. Verweis
   auf Specs, Pläne, Issues und Diffs per Pfad oder URL — dupliziere nie ihren
   Inhalt.
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
9. **Empfohlene Skills.** Welche Skills der nächste Agent zuerst laden soll,
   und je eine Zeile warum. Das macht das Dokument über Harness-Grenzen hinweg
   portabel.

## Harte Regeln

- **Schwärzen.** Keine API-Keys, Passwörter, Tokens oder persönlichen Daten.
  Keine echten Hostnamen, internen IPs oder Home-Pfade — nur Platzhalter;
  zeig auf echte Werte per Env-Variablen-Name. Eine Übergabe ist die Datei,
  die am ehesten die Maschine verlässt; ein Secret, das durch sie leckt, IST
  der Bug.
- **Abwesenheits-Behauptungen verrotten am schnellsten.** Bevor du „X
  existiert nicht" oder „X ist nicht gelandet“ schreibst, verifizier neu am
  aktuellen Commit — Parallel-Arbeit landet, während du schreibst.
- **Zwei-Wort-Status pro Punkt: PROVEN oder STILL-BUILDING.** Grüne Tests ohne
  Live-Beweis sind STILL-BUILDING, und die Übergabe sagt exakt, welcher Beweis
  fehlt.
- **In zwei Minuten lesbar halten** (rund 120 Zeilen). Wächst sie darüber,
  archivier die ältesten Blöcke in einen Historien-Abschnitt — nie durch
  Löschen.

## Aufnehmen (die andere Hälfte)

Eine Session, die aus einer Übergabe startet, liest sie ZUERST und verifiziert
dann die obersten zwei, drei Behauptungen gegen `git log` und den Live-Baum,
bevor sie danach handelt. Die Übergabe ist eine Karte, keine Wahrheit — trau
ihr für das WO, verifizier das WAS.

## Passt gut zu

- [root-cause-first](../root-cause-first/SKILL.md) — die Untersuchung, die die nächste Session fortsetzt.
- [repair-loop](../repair-loop/SKILL.md) — mitten in der Schleife übergeben, ohne die Naht zu verlieren.
- [decision-bar](../decision-bar/SKILL.md) — wie offene Entscheidungen deinen Menschen erreichen.

> Scaffold credit: Matt Pocock, handoff (mattpocock/skills). Komposition und harte Regeln hier sind BACKS AIOS.
