---
name: root-cause-first
description: Bei einem harten Bug, einem stillen Versagen, einer Regressions-Jagd oder einer riskanten Änderung, die leise einen nachgelagerten Konsumenten brechen könnte. Keine Fixes ohne Untersuchung — Fehler lesen, auf Kommando reproduzieren, jüngste Änderungen prüfen, Komponenten-Grenzen instrumentieren, den Datenfluss rückwärts zur Quelle verfolgen. Trigger words: debug, root cause, why is this failing, silent failure, regression, works in tests but fails live, systematic debugging, Ursache, Grundursache, warum schlägt das fehl, stilles Versagen, läuft im Test aber nicht live, systematisches Debuggen.
license: MIT
---

# Root Cause First
**Effort:** free — pure Untersuchungs-Disziplin, die die Kosten meist unterm Strich senkt: Eine entscheidende Probe ersetzt das Abfeuern der ganzen Pipeline, nur um zu sehen, was passiert. Beseitigt: Pflaster auf der falschen Stelle — den Symptom-Fix, der den echten Bug versteckt und einen nachgelagerten Konsumenten bricht.

Keine Fixes ohne Untersuchung. Ein Pflaster, geklebt bevor du das Versagen
verstehst, fixt das Falsche, versteckt den echten Bug und bricht etwas
weiter unten. Dein Produkt ist kein Patch — es ist eine Grundursache, bewiesen
durch eine entscheidende Probe, und ein Fix, bewiesen frei von Regressionen.

Zwei Gesetze regieren alles hier drunter:

1. **Keine Annahmen — der Code, die Daten und das Live-System sind die
   Wahrheit; Notizen sind nur Hinweise.** Ein Kommentar, eine Erinnerung, ein
   früherer Schluss, selbst dein eigener letzter Satz ist eine Hypothese, bis
   eine Probe sie bestätigt. Die Wörter „alle / jeder / keiner“ lösen einen
   Drei-Punkt-Check aus: die Umgebung, eine repo-weite Suche und ein Scan über
   jeden Aufrufer.
2. **Ein verifiziertes Gegenbeispiel killt den früheren Schluss sofort.** Wenn
   eine Probe widerlegt, was du geglaubt hast, sag klar „Ich lag falsch — es
   ist in Wirklichkeit X" und mach vom neuen Fakt aus weiter. Nie drüber
   tapezieren.

## Die Schleife (in dieser Reihenfolge; nichts überspringen)

1. **Lies den Fehler.** Benenn das Symptom in einem präzisen Satz. Lies die
   echte Meldung, nicht das, was du erwartest. Benenn den Explosionsradius:
   was hängt an dem Ding, das du verdächtigst?
2. **Reproduzier.** Bring das Versagen auf Kommando — live, oder in einem
   fehlschlagenden Test. **Stopp die Zeit.** Ein „Versagen“, das in
   Millisekunden zurückkommt, wo echte Arbeit Sekunden braucht, ist eine früh
   geschluckte Exception, kein echtes Arbeits-Versagen. Die Zeitlücke ist
   selbst ein Hinweis.
3. **Prüf jüngste Änderungen.** Diffe, was sich geändert hat, seit es zuletzt
   lief — Code, Config, Umgebung, Abhängigkeiten. Ist die Historie lang,
   bisektier sie.
4. **Kartier die Konsumenten.** Bei einem Bug in einer geteilten Fläche: list
   jeden Aufrufer und wie er sie nutzt (exakter String-Match? Boolean? Liste?).
   Die echte Regression versteckt sich meist in einem nachgelagerten
   Exakt-Match-Vergleich, nicht in dem Regler, an dem du drehst.
5. **Instrumentier die Grenzen.** Logge oder probe an jeder Komponenten-Naht —
   was rein geht, was raus kommt. Verfolg die schlechten Daten rückwärts,
   Grenze für Grenze, bis du an der Quelle bist. Fix die Quelle, nie das
   Symptom.
6. **Grundursache per Hypothese.** Bild eine falsifizierbare Hypothese. Find
   die EINE entscheidende Probe, die sie von den Alternativen trennt, und fahr
   nur die. Feuer nicht die ganze Pipeline ab, „um zu sehen, was passiert“.
7. **Fix chirurgisch, an der richtigen Naht.** Die kleinste Änderung, die die
   Grundursache auflöst. Bevorzug die eine geteilte Quelle (ein Normalizer,
   ein Runner) statt N Aufrufstellen zu editieren. Wo möglich, mach den Fix
   inert auf dem funktionierenden Pfad — er ändert dort beweisbar nichts und
   greift nur auf dem kaputten. Keine Nachbar-Refactors als Beifahrer.
8. **Beweis es.** Schreib den fehlschlagenden Test, der den Bug reproduziert;
   sieh ihn rot werden; fix; sieh ihn grün werden. Dann fahr die Tests für
   jeden Konsumenten-Pfad aus Schritt 4 — grün dort ist dein
   Null-Regressions-Boden. Eine Suite, die genau die Naht mockt, die versagt
   hat, beweist nichts.
9. **Verifizier live.** Fahr das echte System — echte Requests, echte
   Datenbank, echte Logs. Nie ein Beiwagen-Skript, das den Code in deinen
   eigenen Prozess importiert. Halt Vorher/Nachher-Beweise fest.
10. **Lern.** Schreib das Symptom, die entscheidende Probe, die Grundursache
    und das Anti-Muster auf, das sie versteckt hat — damit der nächste Bug
    dieser Form billiger wird.

## Bau die Reproduktions-Schleife, BEVOR du Theorien baust

Ertappst du dich beim Code-Lesen für eine Theorie, bevor ein rot-fähiges
Kommando existiert — stopp. Kein rot-fähiges Kommando, keine Theorie. Ein
enges Pass/Fail-Signal, das bei DIESEM Bug rot wird, ist der größte einzelne
Debugging-Hebel. Investier hier überproportional.

Wege, eins zu bauen, grob in dieser Reihenfolge: ein fehlschlagender Test; ein
HTTP-Skript gegen einen Dev-Server; ein CLI-Lauf mit Fixture-Eingabe, gedifft
gegen einen bekannten guten Snapshot; ein Headless-Browser-Skript; ein
mitgeschnittenes echtes Payload, isoliert durch den Codepfad zurückgespielt;
ein Wegwerf-Harness, das eine Funktion aufruft; eine Fuzz-Schleife über
Zufallseingaben; ein Bisektions-Harness, damit automatisches Bisect läuft;
eine Differential-Schleife (gleiche Eingabe durch alte und neue Version, die
Ausgaben gedifft).

Dann zieh sie fest: schneller (Setup cachen, Scope verengen), schärfer (das
konkrete Symptom asserten, nicht „ist nicht abgestürzt“), deterministisch
(Zeit pinnen, RNG seeden, Netz einfrieren). Eine deterministische
Zwei-Sekunden-Schleife ist eine Superkraft.

Bei flatterhaften Bugs jag eine höhere Reproduktionsrate, keine saubere Repro:
loope den Auslöser 100-mal, gib Stress dazu, verenge die Timing-Fenster. Ein
50%-Flake ist debugbar; ein 1%-Flake nicht.

Kriegst du wirklich keine Schleife gebaut, stopp und sag es. List auf, was du
versucht hast, und bitte deinen Menschen um Zugang, ein mitgeschnittenes
Artefakt oder temporäre Instrumentierung. Theoretisier nicht ohne Schleife.
Und existiert keine Naht, die das echte Aufrufmuster nachstellen kann, IST
dieses Fehlen ein Fund — flagg die Architektur-Lücke, nachdem der Fix
gelandet ist.

## Anti-Muster (wie harte Bugs am Leben bleiben)

- Aus einer Notiz oder einem Kommentar schließen, ohne Probe.
- Fixen vor dem Reproduzieren.
- Einer grünen Suite trauen, die genau die Naht mockt, die live versagt.
- Beiwagen-Verifikation — den Code importieren, statt das Live-System zu fahren.
- Einen Config-Regler drehen, ohne die Exakt-Match-Konsumenten zu kartieren,
  die er füttert.
- Breite Refactors als Beifahrer eines Fixes.
- „alle / jeder / keiner“ sagen, ohne den Drei-Punkt-Check.

## Passt gut zu

- [red-first](../red-first/SKILL.md) — committe den fehlschlagenden Test vor dem Fix.
- [sniper-testing](../sniper-testing/SKILL.md) — gescopte Tests beim Iterieren.
- [seam-engineering](../seam-engineering/SKILL.md) — fix die Klasse, nicht die Instanz.
- [repair-loop](../repair-loop/SKILL.md) — der volle Fix-und-Lande-Zyklus.

> Scaffold credit: Matt Pocock, diagnosing-bugs (mattpocock/skills). Komposition und harte Regeln hier sind BACKS AIOS.
