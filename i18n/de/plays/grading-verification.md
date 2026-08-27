# Play: Grading & Verification

Das Play für adversariales Benoten. Sein einziger Glaubenssatz: Ein grünes Ergebnis
ist eine Behauptung, kein Beweis. Der Prüfer greift an, und der Boden ist so gebaut,
dass er sich nicht austricksen lässt.

## Wann dieses Play läuft

- Irgendeine gebaute Änderung will landen — Code, Config, Doku, der Output eines
  Agenten.
- Eine Suite behauptet Grün, und niemand hat sie zuerst scheitern sehen.
- Ein Modell hat die Arbeit gebaut, und du brauchst ein ehrliches Urteil darüber.

## Die Kette

1. [red-first](../skills/red-first/SKILL.md) — bestätige, dass die Suite mit einem
   Exit-Code ungleich null gescheitert ist, BEVOR der Fix existierte. Eine Suite,
   die nie rot war, beweist nichts.
2. [sniper-testing](../skills/sniper-testing/SKILL.md) — verifiziere, dass der
   Builder während der Iteration gescopte Tests benutzt hat und kein Mock-Theater
   auf der Seam lief, die er geändert hat.
3. Familienfremde Benotung — gib die Arbeit einem Modell aus einer ANDEREN Familie
   als der Builder. Benotung innerhalb derselben Familie bläht die Gewinnraten
   messbar auf — Prüfer bevorzugen die eigene Verwandtschaft; eine andere Instanz
   derselben Familie reicht nicht.
4. [blind-tribunal](../skills/blind-tribunal/SKILL.md) — berufe bei folgenschweren
   Änderungen Juroren über ein Envelope ohne Autorenangabe ein. Jeder Fund wird
   ein neuer roter Test, und das Tribunal tagt neu, bis alle Juroren die Änderung
   bestehen lassen.
5. [clean-code-gauntlet](../skills/clean-code-gauntlet/SKILL.md) — der Prüfer
   fährt das Gauntlet selbst noch einmal (Coverage gegen Komplexität, begrenzte
   Mutation-Tests). Vertraue niemals dem Bericht des Builders über seine eigenen
   Zahlen.

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

Der Boden der Richter-Mechanik steht im Abschnitt „De-bias the judge“ („den Richter
ent-biasen“) von [blind-eval](../skills/blind-eval/SKILL.md) — wende ihn als Ganzes
an.

## Harte Gates — eines reicht, und das Play ist gescheitert

- Builder und Prüfer teilen eine Modellfamilie.
- Die Suite lässt sich nicht als rot vor dem Fix zeigen.
- Fail-to-pass oder pass-to-pass fehlt im benoteten Lauf.
- Eines der Fake-Grün-Zeichen oben ist vorhanden.
- Der Prüfer hat dem eigenen Bericht des Builders vertraut, statt die Checks
  selbst neu zu fahren.
