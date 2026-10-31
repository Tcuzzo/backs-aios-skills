# Play: Grading & Verification

Das Play für adversariales Benoten. Sein einziger Glaubenssatz: Ein grünes Ergebnis
ist eine Behauptung, kein Beweis. Der Prüfer greift an, und der Boden ist so gebaut,
dass er sich nicht austricksen lässt.

## Wann dieses Play läuft

- Irgendeine gebaute Änderung will landen — Code, Config, Doku, der Output eines
  Agenten.
- Eine Suite behauptet Grün, und niemand hat sie zuerst scheitern sehen.
- Ein Modell hat die Arbeit gebaut, und du brauchst ein ehrliches Urteil darüber.

## Gemeinsame Aufgabe und Grenzen

Wende dieses Play im aktuellen [BACKS Build Flow](../skills/backs-build-flow/SKILL.md)-
Aufgabenpaket an. Bewahre einen Integrationsverantwortlichen, gewünschten
`task_mode`, feste Basis- und Kandidatenrevisionen, Operator-Essence und aktuelle
Belege. Verwende passende geladene Skill-Texte weiter; dieses Play ergänzt seine
Fachprüfungen, ohne die Aufgabe neu zu starten.

[bounded-loops](../skills/bounded-loops/SKILL.md) besitzt ursprüngliche Frist und
Restkontingente über Wiederholungen, Mitarbeiter, Modelle, Reviews und Übergaben
hinweg. Setze sie für ein verschachteltes Play nie zurück. Bei Erschöpfung:
**STILL-BUILDING** mit Kandidat, Belegen, offenen Gates und nächster Handlung
sichern. Nützliche autorisierte Arbeit bleibt im Restkontingent; kein fehlendes
Gate wird zum bestandenen erklärt.

## Die Kette

1. [red-first](../skills/red-first/SKILL.md) — bestätige, dass die Suite mit einem
   Exit-Code ungleich null gescheitert ist, BEVOR der Fix existierte. Eine Suite,
   die nie rot war, beweist nichts.
   Der Fehlertest ist vorab committet und für den Builder unveränderlich;
   seine genauen Dateibytes sind der Vertrag.
2. [sniper-testing](../skills/sniper-testing/SKILL.md) — prüfe echte Lint-/Typ-/
   Testbefehle des Repositories im Umfang des festgehaltenen Kandidatengesamtdiffs,
   ohne Mock-Theater an der geänderten Schnittstelle. Prüfe explizite N/A-Gründe
   und fehlende Checks. Friere die Kandidatenidentität für dieses Review ein.

3. Autor-disjunkte Benotung — gib die Arbeit einem Prüfer, dessen ausführende
   Session die Änderung NICHT gebaut hat, live nach Fähigkeit und Verfügbarkeit
   aus der konfigurierten Sprossen-Matrix gewählt; die Prüfung erfolgt in einer frischen, autor-disjunkten Session. Die
   Selbst-Benotung durch die ausführende Session, die gebaut hat, ist von
   Grund auf disqualifiziert.
4. [blind-tribunal](../skills/blind-tribunal/SKILL.md) — berufe bei folgenreichen
   Änderungen Juroren für ein autorenbereinigtes Paket in frischer Session ohne
   geerbtes Gespräch ein. Gib belegte Befunde an den Integrationsverantwortlichen
   für ein separates ergänzendes RED und begrenzte Reparatur zurück; das Original
   bleibt versiegelt. Tage erneut am überarbeiteten eingefrorenen Kandidaten im
   selben Restbudget. Alle erforderlichen Juroren müssen vor der Landung bestehen.

5. [clean-code-gauntlet](../skills/clean-code-gauntlet/SKILL.md) — der Prüfer
   fährt das Gauntlet selbst noch einmal (Coverage gegen Komplexität, begrenzte
   Mutation-Tests). Vertraue niemals dem Bericht des Builders über seine eigenen
   Zahlen.

Bewahre das unveränderliche Ziel des Review-Modus. Führe cache-erzeugende,
code-mutierende oder Dienste ausführende Prüfungen nur in erlaubter Isolation
aus; Mutation darf eingefrorenen Quelltext nie ändern. Fehlende Isolation oder
Runtime-Unterstützung sind Beleglücken, keine Erlaubnis zum Patchen im Review.
Bewahre volle betroffene Landungssuite und trenne lokale Prüfungen von realen
Oberflächen- und Liefernachweisen.

## Der zweiseitige Beweis (beide, oder kein Bestehen)

- **Fail-to-pass:** Die Tests, die rot waren, sind jetzt grün — der Fix ist
  bewiesen.
- **Pass-to-pass:** Alles, was grün war, ist immer noch grün — keine Regression.
- Ein Lauf, der nur grüne Tests HINZUFÜGT, erfüllt keines von beiden. Fahre beide
  hermetisch.

## Wachen gegen Fake-Grün (jede einzelne ist das Verräter-Zeichen)

- Eine Exit-Code-Hintertür — ein Harness, das sauber exitet, egal was passiert ist.
- Hartkodierte oder auswendig gelernte Outputs anstelle von berechneten.
- Gelöschte, geskippte oder aufgeweichte Tests.
- Jeder editierte Prüfer, Timer oder Scorer. Ein editiertes Harness, das grün wird,
  IST das Zeichen.
- Ein überlebender Mutant unter einer grünen Suite. Der Mutant ist der Beweis,
  dass die Assertions diesen Zweig nie erreicht haben — Fake-Grün per Definition.

## Den Richter ent-biasen

Der Boden der Richter-Mechanik steht im Abschnitt „De-bias the judge" („den Richter
ent-biasen") von [blind-eval](../skills/blind-eval/SKILL.md) — wende ihn als Ganzes
an.

## Harte Gates — eines reicht, und das Play ist gescheitert

- Die ausführende Session, die die Änderung gebaut hat, signiert die
  Benotung selbst.
- Die Suite lässt sich nicht als rot vor dem Fix zeigen.
- Fail-to-pass oder pass-to-pass fehlt im benoteten Lauf.
- Eines der Fake-Grün-Zeichen oben ist vorhanden.
- Der Prüfer hat dem eigenen Bericht des Builders vertraut, statt die Checks
  selbst neu zu fahren.

**Weight:** vorneweg free — die Red- und Sniper-Checks; der heavy-Einsatz ist das Tribunal plus der Prüfer, der das Gauntlet selbst noch einmal fährt — er zahlt sich bei jeder Änderung aus, die landen will, denn ein einziges falsches Grün kostet mehr als alle Benotungen zusammen.
