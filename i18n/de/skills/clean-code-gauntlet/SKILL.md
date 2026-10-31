---
name: "clean-code-gauntlet"
description: "Beim Härten oder Landen ausführbarer Änderungen, die gemessene Komplexität, Coverage, Regressionsstärke und unabhängiges Designreview benötigen."
license: "MIT"
---

# Clean Code Gauntlet
**Effort:** heavy — echte Rechenzeit: Coverage- und Komplexitäts-Läufe plus ein begrenzter Mutations-Durchgang, dann ein Geschmacks-Modell; investier das in Änderungen, die ausgeliefert werden. Beseitigt: menschliches Zeile-für-Zeile-Review ganzer Diffs und die falsch-grünen Tests, hinter denen sich eine Regression versteckt.

## Warum es das gibt

Unordentlicher Code lässt Agenten strampeln, und Regeln, die in einem langen
Prompt vergraben sind, verblassen mitten im Kontext — deterministische Checks
verblassen nie. Also fahre Clean Code als **Spießrutenlauf, den der Code bestehen
muss**, nicht als Prosa, die sich das Modell merken soll.

**Messen, nicht reviewen.** Gate auf Zahlen, die ein Tool berechnet: Coverage,
zyklomatische Komplexität (eine Zählung unabhängiger Pfade durch eine Funktion),
Modulgröße, Mutation-Kills. Menschen und Modelle auditieren Stichproben — nie
ganze Diffs.

## Die Kette (in Reihenfolge fahren; jede Stufe stoppt laut bei Fehlschlag)

Binde `base_sha`, `candidate_sha`, Integrationsverantwortlichen und verbleibendes
[bounded-loops](../bounded-loops/SKILL.md)-Missionskontingent des bestehenden
[Build Flow](../backs-build-flow/SKILL.md)-Pakets ein. Verwende weiterhin gültige
Belege; Review-Runden und Mutationskampagnen setzen das Budget nicht zurück.

1. **Gezielte Lint-, Typ- und Verhaltensprüfungen grün.** Führe passende Befehle
   des Repositories aus — siehe [sniper-testing](../sniper-testing/SKILL.md).
   Erfasse nicht verfügbare oder unanwendbare Prüfungen ausdrücklich, nicht als
   bestanden. Eine rote Baseline heißt: stoppen und reparieren; nie auf Rot mutieren oder bewerten.
2. **CRAP unter der Schwelle** auf echten Coverage-Daten (siehe das Gate unten).
   Riss → die Funktion herunter-refactoren oder voll abdecken. Nie die Latte
   senken.
3. **Mutation: keine ungeklärten Überlebenden im Umfang.** Ein nicht äquivalenter
   Überlebender ist eine Regressionslücke. Lege eine separate Ergänzungstestdatei
   an; bewahre den ursprünglichen versiegelten [red-first](../red-first/SKILL.md)-
   Vertrag Byte für Byte. Dokumentiere die belegte Widerlegung äquivalenter
   Mutanten. Toolfehler oder Timeout sind unentschieden, niemals getötete Mutanten.
4. **Leichtes Geschmacks-Review** — ein Modell beurteilt nur, was Zahlen nicht
   können.

## Tools, die das berechnen

| Stack | Tools |
| --- | --- |
| Python | coverage.py + radon + mutmut |
| JS/TS | c8 (oder istanbul) + Stryker |
| Go | go test -cover + gocyclo + go-mutesting |
| Rust | cargo-tarpaulin + cargo-mutants |
| Java | JaCoCo + PIT |
| Andere | irgendein Coverage-% + irgendein Zähler für zyklomatische Komplexität |

Eine Befehlsform pro Stufe:
- Coverage: `coverage run -m pytest <sniper files> && coverage report` (JS/TS: `npx c8 vitest run <files>`)
- Komplexität: `radon cc -s <changed files>`
- Mutation: `mutmut run --paths-to-mutate <changed files>` (JS/TS: `npx stryker run --mutate "<glob>"`)

Diese Befehle sind Beispiele, keine Installationsanweisungen oder stabilen
CLI-Garantien. Nutze festgelegte Repository-Tools und unterstützte Flags.
Validiere bei reinen Dokumentationsänderungen Links, Struktur, Distribution und
Verhaltensszenarien; Codekomplexität oder Mutation können unanwendbar sein.
Dokumentiere den Grund, statt Messwerte zu erfinden.

## Das CRAP-Gate

```
CRAP(m) = comp(m)^2 * (1 - cov(m)/100)^3 + comp(m)
```

- Bei 100 % Coverage kollabiert der Score auf die Komplexität selbst.
- 30 ist die klassische „crappy“-Linie (Komplexität 5 bei null Coverage erreicht
  sie).
- Menschen halten grob 4–5 Komplexität pro Funktion. Ein Agent darf 6–8 tragen,
  NUR bei nahezu 100 % Coverage — die Coverage bezahlt den Spielraum.
- Eine Funktion mit hohem CRAP hat genau zwei Ausgänge: herunter-refactoren oder
  voll abdecken. **Nie die Schwelle senken, um zu bestehen.**

## Wessen Schulden sind das — AUTHORED / WORSENED / UNCHANGED

Ein absoluter Score versteckt, wessen Schulden es sind. Teile jedes Komplexitäts-
und CRAP-Delta gegen den festgehaltenen `base_sha` vor Aufgabenbeginn auf,
mit vergleichbaren tatsächlichen Coverage-Daten:

- **AUTHORED** — Funktionen, die diese Änderung erzeugt hat. Die volle Latte gilt.
- **WORSENED** — bestehende Funktionen, die diese Änderung verschlechtert hat. Das
  Delta wird dieser Änderung angelastet; es muss zurück auf Baseline oder besser.
- **UNCHANGED** — bestehende Schulden, die die Änderung nie berührt hat. Berichten,
  ablegen, nie dieser Änderung anlasten — und nie als Deckung nutzen, um den
  Spießrutenlauf zu überspringen.

## Mutations-Regeln (begrenzt, nie leichtsinnig)

- **Nie der geteilte Working Tree.** Mutiere in einem Scratch-Checkout der exakten
  committeten `candidate_sha`. Schmutzige Ziel-/Testdateien: Checkpoint und zuerst
  Kandidat fertigstellen. Bewahre fremde Arbeit im ursprünglichen Checkout.
- **Kosten werden gemessen, nie angenommen.** Stoppe die gescopte Suite einmal,
  berichte ETA = Baseline x Mutantenzahl, BEVOR irgendetwas ausgegeben wird.
  Biete einen Dry Run an.
- **Begrenzt und wiederaufnehmbar.** Deckle Mutanten und Minuten im Missionsrestkontingent.
  Ein Budget-Stopp sichert ungeprüfte Mutanten und lässt das Gate unvollständig.
  Fortsetzung nur mit verbleibendem oder ausdrücklich erweitertem Kontingent.
- **Coverage zuerst.** Mutiere nur abgedeckte Zeilen; eine unabgedeckte Zeile ist
  eine Coverage-Lücke, die das CRAP-Gate schon gefangen hat.
- **Nur im Scope.** Mutiere, was der Diff berührt hat, nie das ganze Repo.
- Ein wirklich äquivalenter Mutant darf widerlegt statt getötet werden — mit
  aufgeschriebener Widerlegung, nie still übersprungen.
- **Kein Mutation-Tool für deinen Stack?** Erfasse Einschränkung und tatsächliche
  Ersatzbelege. Wende die Abnahmeregeln des Repositories an; ein Pflichtgate bleibt
  offen, bis sein Verantwortlicher eine dokumentierte Alternative akzeptiert.

## Das Geschmacks-Review (zuletzt, und leicht)

Deterministische Gates zuerst; gib ein Modell nur dort aus, wo Denken das einzige
Werkzeug ist. Der Reviewer ist ein nicht-vom-Builder stammender Prüfer, live
nach Fähigkeit und Verfügbarkeit aus der konfigurierten Sprossen-Matrix
gewählt; die ausführende Session, die gebaut hat, und jede Session, die die
Konversation oder den Kontext des Builders geerbt hat, sind disqualifiziert; die Bewertung erfolgt in einer frischen, autor-disjunkten Session — der
Builder bewertet nie die eigene Arbeit. Er beurteilt
nur Design und Geschmack: Benennung, vermischte Belange, Interface-Breite und
die sechs Gerüche — Starrheit, Zerbrechlichkeit, Unbeweglichkeit, unnötige
Komplexität, unnötige Wiederholung, Undurchsichtigkeit. Die Arithmetik haben
die Gates schon erledigt.

Der Handwerks-Boden, den das Review hält: Funktionen klein, tun eine Sache, wenige
Argumente, keine Flag-Argumente, ehrliche Namen; tiefe Module — ein kleines
Interface, das echte Logik verbirgt; Tests schnell, unabhängig, wiederholbar, ein
Verhalten pro Assertion.

## Harte Regeln (eine gebrochen, und der Skill ist gescheitert)

- Nie eine Schwelle senken oder das Mutationsset schwächen, um einen Pass zu
  erzwingen.
- Nie den geteilten Working Tree mutieren; nie unbegrenzt laufen.
- Nie UNCHANGED-Schulden der aktuellen Änderung anlasten.
- Ein Test, der nicht fehlschlagen kann, ist Theater — Mutation-Testing beweist,
  welche Tests echt sind.
- Sag die echten Kosten — Maschinenzeit ist billig, Regressionen sind es nicht.
  Nie Grün faken, um die Stunde zu sparen.

## Passt gut zu

- [sniper-testing](../sniper-testing/SKILL.md) — wählt den Test-Scope für Stufe 1
- [red-first](../red-first/SKILL.md) — der fehlschlagende Contract vor jedem Build
- [blind-eval](../blind-eval/SKILL.md) — Keep-or-Revert, wenn Geschmack die Frage ist
- [blind-tribunal](../blind-tribunal/SKILL.md) — ein volleres, benotetes Urteil vor dem Landen

> Gerüst-Credit: Robert C. Martin, *Clean Code* (2008); Alberto Savoia &
> Bob Evans, die CRAP-Metrik (2007); John Ousterhout, deep modules
> (*A Philosophy of Software Design*, 2018); Pocock, M., & Martin, R. C.
> (2026, Aug 19). LIVE: Uncle Bob on Software Fundamentals in the Age of AI
> [Video]. YouTube. https://www.youtube.com/watch?v=zcLPGC-tvgk — Quelle des
> Agenten-CRAP-Bands und der Coverage-first-Mutation. Die Komposition und die
> harten Regeln hier sind BACKS AIOS.
