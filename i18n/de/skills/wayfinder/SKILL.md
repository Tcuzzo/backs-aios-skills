---
name: "wayfinder"
description: "Wenn du verloren bist, der Weg nach vorn unklar ist oder du entscheiden musst, woran als Nächstes gearbeitet wird. Kartiert eine Entscheidungs-Karte zum Ziel, statt eine Frage beim Menschen zu parken. Trigger words: wayfinder, the path, chart the route, map the work, what next, lost, fog of war, decision map, frontier, der Pfad, Route kartieren, was als Nächstes, verloren, Nebel, Entscheidungs-Karte."
license: "MIT"
---

# Wayfinder
**Effort:** free — pure Kartierungs-Disziplin: eine Entscheidungskarte, gebaut aus Beweisen, die schon auf der Platte liegen; keine zusätzlichen Modell-Calls. Beseitigt: Fragen, die beim Menschen geparkt werden, obwohl Beweise sie beantworten könnten, und Bauarbeit, die startet, bevor die Entscheidungen davor gefallen sind.

Wenn du den Weg nicht kennst, ist der billige Zug, anzuhalten und dem Menschen
eine Frage zu stellen, für deren Antwort er dich angeheuert hat. Der Wayfinder
kartiert stattdessen die Route: bau eine Entscheidungs-Karte, lös Unbekanntes
aus Beweisen auf und schick nur die Calls nach oben, die wirklich dem Menschen
gehören.

## Wann laufen lassen

- Du bist verloren, oder der nächste Schritt ist unklar.
- Ein großes Vorhaben muss zerlegt werden, bevor irgendwer baut.
- Du spürst den Drang zu fragen: „Was soll ich denn machen?“

## Die Schritte

1. **Benenn das Ziel.** Ein benanntes Ziel in deinem Tracker, plus ein
   Abschluss-Kriterium: woran du erkennst, dass es fertig ist. Das Ziel
   fixiert den Umfang.
2. **Kartier, was du sehen kannst.** Leg Tickets an der Front an — die
   Entscheidungen, die jetzt auflösbar sind. Jedes Ticket löst eine
   **Entscheidung** auf, kein Stück Bau-Arbeit.
3. **Lass den Rest im Nebel.** Entscheidungen, die du kommen spürst, aber noch
   nicht festnageln kannst, kommen in einen Abschnitt **Noch nicht
   spezifiziert**: die vermutete Frage, der Bereich zum Wiederkommen.
   Zerschneide den Nebel nicht vorab in Ticket-Häppchen — er ist gröber als
   ein Ticket, und ein Fleck kann zu mehreren Tickets aufsteigen, oder zu
   keinem.
4. **Schließ Arbeit laut aus.** Arbeit jenseits des Ziels ist kein Nebel — sie
   kommt in einen Abschnitt **Außerhalb des Umfangs** und steigt nie auf.
   Stellt sich heraus, dass ein lebendes Ticket hinter dem Ziel liegt, schließ
   es und lass eine Zeile in Außerhalb des Umfangs stehen.
5. **Typisier jedes Ticket** (siehe Ticket-Typen unten).
6. **Lös eine Entscheidung aus Beweisen.** Lies den Code, die Doku, den
   Datensatz — deterministischer Beweis schließt ein Ticket ohne Raten. Ein
   aufgelöstes Ticket lichtet den Nebel dahinter: lass, was jetzt
   spezifizierbar ist, zu frischen Tickets aufsteigen, eins nach dem anderen.
7. **Übergib, wenn der Weg klar ist.** Die Karte ist fertig, wenn nichts mehr
   zu entscheiden bleibt, bevor jemand losgeht und die Sache macht. Der Drang,
   die Arbeit einfach selbst zu tun, ist das Signal, dass du den Rand der
   Karte erreicht hast.

## Nebel oder Ticket?

Der Test ist, ob du die Frage jetzt **präzise** stellen kannst — nicht, ob du
sie jetzt beantworten kannst. Ticket, wenn die Frage scharf ist, selbst wenn
sie blockiert ist. Noch-nicht-spezifiziert, wenn du sie noch nicht so scharf
formulieren kannst.

## Ticket-Typen

Jedes Ticket ist **human-in-loop** (live mit einem Menschen bearbeitet) oder
**agent-alone**. Ein Human-in-loop-Ticket löst sich nur im echten Austausch —
der Agent springt nie für die Seite des Menschen ein. Ein Agent, der seine
eigenen Grill-Fragen beantwortet, hat das gebrochen.

- **Research** (agent-alone) — ein Hintergrund-Research-Agent löst es auf;
  Funde landen auf einem Scratch-Branch mit einem Zeiger vom Ticket. Siehe
  [live-research](../live-research/SKILL.md).
- **Prototype** (human-in-loop) — heb die Auflösung mit einem billigen groben
  Artefakt, auf das der Mensch reagieren kann.
- **Grilling** (human-in-loop) — ein Gespräch, das die Entscheidung
  herauszieht. Der Standard-Typ.
- **Task** (beides) — manuelle Arbeit, die passieren muss, bevor eine
  Entscheidung fallen kann: bei einem Dienst anmelden, Zugang einrichten,
  Daten bewegen. Der eine Typ, der *tut* statt entscheidet; er verdient seinen
  Platz, weil er eine Entscheidung entblockt.

## Harte Regeln

- **Park nie eine Frage beim Menschen,** die Beweise, der Code oder stehende
  Regeln beantworten können. Nur Geschmack, Vision und Destruktiv-Risiko gehen
  nach oben — siehe [decision-bar](../decision-bar/SKILL.md).
- **Nenn Arbeit beim Namen, nie bei einer nackten Id.** Eine Wand aus #42,
  #43, #44 ist unleserlich; Namen liest man auf einen Blick. Die Id oder der
  Link reitet im Namen mit — sie ersetzt ihn nie.
- **Eine Entscheidung pro Session.** Lös höchstens ein Ticket pro Session auf,
  Research-Tickets ausgenommen. Kartieren ist eine Session Arbeit; es löst
  nebenbei nichts von Hand.
- **Planen, nicht tun.** Die Karte produziert Entscheidungen, keine
  Liefergegenstände.
- **Ist die Bitte selbst der Nebel** — das Ziel unklar, weil die Anfrage als
  Prosa oder Metapher kam — lies die Anfrage zuerst mit
  [intent-compiler](../intent-compiler/SKILL.md), dann kartier von dem aus,
  was sie wirklich sagt.

## Passt gut zu

- [live-research](../live-research/SKILL.md) — löst die Agent-allein-Research-Tickets auf.
- [decision-bar](../decision-bar/SKILL.md) — welche Entscheidungen den Menschen wirklich erreichen.
- [human-voice](../human-voice/SKILL.md) — wie die Karte sich für einen Menschen liest.

> Scaffold credit: Matt Pocock, wayfinder (mattpocock/skills, MIT). Komposition und harte Regeln hier sind BACKS AIOS.
