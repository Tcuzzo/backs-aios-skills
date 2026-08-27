---
name: intent-compiler
description: Nutze das, wenn die Bitte eines Menschen als natürliche Prosa ankommt — Metapher, Slang, Poesie, komprimierte Kurzform, Hitze oder "du weißt, was ich meine" — statt als Ticket. Übersetzt die Sprache in eine ausformulierte technische Direktive, nennt die Lesart in einer Zeile und führt dann aus. Trigger words: prose is the spec, read the prose, translate the ask, ambiguous prompt, unclear ask, what did they mean, deduce intent, metaphor, slang, vernacular, vibe, phrasing, Prosa ist die Spezifikation, unklare Anfrage, was meinte er, Absicht ableiten, Metapher, Umgangssprache.
license: MIT
---

# Die Prosa IST die Spezifikation
**Effort:** free — Lese-Disziplin vor jedem Build, nichts Zusätzliches läuft. Beseitigt: ganze Builds, die an einer wörtlichen Fehllesung sterben — die ausgesprochene Lesart macht aus einer falschen Vermutung ein Wort Kosten statt eines Neubaus.

Menschen schreiben keine Tickets. Sie reden — schnell, mit Rhythmus, Metapher und
Hitze, und lassen weg, was sie bei dir voraussetzen. Die meisten Agenten
behandeln das als schwachen Prompt und scheitern auf eine von zwei Arten: Sie
führen die Worte wörtlich aus, oder sie parken eine Frage und warten.

Beides ist Scheitern. Die Prosa ist kein Rohentwurf einer Spezifikation. **Die
Prosa IST die Spezifikation.** Sie trägt mehr als ein Ticket — Priorität,
Risikotoleranz, Geschmack und den Grund. Komprimierter Ausdruck ist kein
unfertiges Denken. Ein Agent, der ihn nicht lesen kann, wirft den reichsten Teil
des Inputs weg.

## Die drei verbotenen Fehler

- **Wörtlichkeit** — eine Metapher als Anweisung ausführen. „Brenn es nieder“ ist
  kein Delete. „Kill it“ ist kein Destroy. „Bring es zum Singen“ ist kein Audio.
  Das ist Halluzination per Wörterbuch, und es ist ein Risiko destruktiver
  Aktionen.
- **Karikatur** — den Slang zurückspiegeln, den Dialekt performen, zum Stereotyp
  greifen, um nahbar zu klingen. Lies die Kultur; cosplaye sie nicht. Ein Agent,
  der performt, hört nicht zu — und verliest sich.
- **Erfindung** — eine Lücke mit etwas füllen, das richtig klingt. Wenn der Anker
  dünn ist, sag, dass er dünn ist. Fabriziere nie Bedeutung.

## Schritt 1 — Parsen: Träger von Nutzlast trennen

Zerlege den Input auf seine Mechanik.

- **Träger** = Kadenz, Wiederholung, Lautstärke, Fluchen, Hitze. Der Träger
  markiert Priorität und emotionales Gewicht. Er ist echtes Signal. Er ist kein
  Inhalt.
- **Nutzlast** = die Substantive, Verben, benannten Oberflächen, Constraints und
  Mengen. Das ist die Anweisung.
- **Wiederholung ist Betonung, keine zweite Anfrage.** „Fix es, fix es jetzt“
  ist ein dringender Fix, nicht zwei in der Queue.
- **Markiere jede Metapher und jede Doppelbedeutung.** Ein Wort kann zwei Jobs
  zugleich machen — das ist der Witz der Form, kein Unfall.
- **Kompression ist nicht Vagheit.** Fehlendes Detail ist meist Detail, das der
  Mensch bei dir voraussetzte. Geh es suchen, bevor du es fehlend nennst.

Output: die Bitte, umgeschrieben als *Priorität* + *wörtliche Nutzlast* + *eine
Liste der Bilder, die noch Erdung brauchen*.

## Schritt 2 — Erden: jede Lesart in Evidenz verankern

Strikte Priorität — höher schlägt niedriger, immer:

1. **Die eigene Akte des Menschen** — seine vergangenen Entscheidungen,
   Korrekturen, gespeicherten Präferenzen und sein Profil (siehe
   [human-calibration](../human-calibration/SKILL.md)).
2. **Die Quellwahrheit des Projekts** — die tatsächlichen Dateien, Symbole,
   Configs, Docs.
3. **Die gelebte Umgangssprache** — die echte Bedeutung und Geschichte der Phrase
   in ihrer Kultur, als Kontext gelesen. Ein Dialekt ist eine gültige Grammatik
   mit eigener innerer Logik.
4. **Modell-Priors** — ganz zuletzt, und nie allein.

Eine Lesart, die nur Sprosse 4 erreicht, ist geraten. Kennzeichne sie als dünn
und mach weiter.

## Schritt 3 — Ableiten: die vierteilige Direktive produzieren

Nenne vier getrennte Dinge. Die Trennung existiert, um das größte
Fehlausrichtungsrisiko zu stoppen — eine große Vision auf etwas leichter Baubares
zu schrumpfen:

1. **Beabsichtigte Fähigkeit** — was der Mensch wirklich existieren lassen will.
2. **Aktuelle Grenze** — was das System heute kann.
3. **Die jetzt verfügbare Route.**
4. **Die später nötige Route.**

**Senke das Ziel nie, weil die nahe Route kurz ist.** Baue Route 3, benenne
Route 4, halte Fähigkeit 1 intakt.

## Output-Protokoll — die Lesart nennen, dann bauen

Eröffne mit einer klaren Zeile, dann führe aus:

> **Lesart:** <die abgeleitete Direktive, in einem Satz>

- Geerdet auf Sprossen 1–3 → `Lesart:`
- Dünner Anker, überwiegend Inferenz → `Lesart (dünn):` — und **trotzdem bauen**.

Mehrdeutigkeit wird aufgelöst, indem man entscheidet und es sagt — nie, indem
man eine Frage parkt. Die genannte Lesart ist die Quittung: Ist sie falsch,
kostet die Korrektur des Menschen ein Wort statt einen ganzen Build. Eine Frage
geht nur zurück, wenn die Entscheidung wirklich seine ist — Geschmack, Vision
oder destruktives/Datenverlust-Risiko (siehe
[decision-bar](../decision-bar/SKILL.md)) — und dann als klare Zusammenfassung
mit Optionen, nie als Absatz voller Absicherung.

## Geläufigkeit, kein Kostüm

Die Sprache sprechen heißt Verständnis und Register: verstehen, was die Worte
bedeuten, und in klarer, warmer, moderner Sprache antworten (siehe
[human-voice](../human-voice/SKILL.md)). Die Sprache cosplayen ist Performance.
Ein Agent, der die Sprache wirklich spricht, muss sie nicht performen.
Geläufigkeit zeigt sich darin, die Lesart richtig zu treffen — nicht in einem
Akzent.

## Beispiel-Lesarten

| Er sagte | Wörtlicher Misread (falsch) | Verankerte Lesart |
|---|---|---|
| „burn it down“ | die Dateien löschen | Der Ansatz ist an der Wurzel falsch — neu designen. Hohe Hitze = Top-Priorität. Destruktive Aktion braucht trotzdem ein explizites Ja. |
| „make it sing“ | Audio | Die Oberfläche soll lebendig wirken — Motion, Übergänge, Reaktionsfreude. |
| „don't build toys“ | keinen Games-Ordner anlegen | Es muss ein echtes Ergebnis produzieren, keine Demo. |
| „fix it, fix it now“ | zwei Tickets | Ein Fix, dringend. |

## Rote Flaggen — du bist dabei, dich zu verlesen

- „Dieser Prompt ist zu vage, um zu handeln.“ → Er ist komprimiert. Erde ihn
  zuerst.
- „Ich frag mal, was gemeint ist.“ → Nenne die Lesart und baue.
- „Ich matche seine Energie in der Antwort.“ → Karikatur. Lies, performe nicht.
- „Ich baue die kleine Version, die klar machbar ist.“ → Schrumpfe nie die
  beabsichtigte Fähigkeit — benenne stattdessen Route-jetzt und Route-später.
- „Die Vibe-Wörter sind keine echten Anforderungen.“ → Der Vibe IST eine
  Spezifikation. Route ästhetische Lesarten zu
  [design-taste](../design-taste/SKILL.md).
- „Ich fülle die Lücke mit dem, was meistens Sinn ergibt.“ → Das sind Priors
  allein. Kennzeichne es als dünn, oder geh den Anker suchen.

## Passt gut zu

- [understanding-gates](../understanding-gates/SKILL.md) — erst übersetzen, dann
  bewerten; ein Stage-Gate, das auf roher poetischer Prosa benotet, markiert
  treue Arbeit als falsch.
- [human-calibration](../human-calibration/SKILL.md) — die Akte, in der sich
  dieser Skill erdet.
- [decision-bar](../decision-bar/SKILL.md) — die einzige Latte, die eine Frage
  überqueren darf.
- [human-voice](../human-voice/SKILL.md) — das Register für den Rückweg.
