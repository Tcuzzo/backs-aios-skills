---
name: "optimus"
description: "Beim Start oder Fortsetzen einer Agent-Session, eines Jobs oder einer autonomen Schleife, die das BACKS-Harness und relevante Aufgaben-Skills braucht."
license: "MIT"
---

# Harness Boot
**Effort:** light — ein Boot-Durchgang pro Session, der den Boden und die Skills des Jobs lädt, plus ein deterministischer Hook, dessen Lauf nichts kostet. Beseitigt: ungeerdete Edits — Mutationen, gemacht bevor die Regeln gelesen waren, und das Nochmal-Machen, das folgt, sobald sie es sind.

Eine Regel: **kein Code und kein Job, bis das Harness geladen ist.** Das Harness
ist das Invarianten-Fundament des Packs plus die Skills, die diesen Job
abdecken. Jede Session, jede Runtime, jedes Mal. Warum: eine Regel, an die sich
ein Agent erinnern muss, versagt genau dann, wenn der Agent am meisten zu tun
hat — also ist das Laden der Regeln die erste Handlung, und ein Hook macht sie
strukturell statt nur gut gemeint.

## Wann laufen lassen

Am Anfang einer Session oder eines neuen Jobs; nach Kontext-Reset oder Übergabe erneut prüfen.
Eine innere Wiederholung nutzt gültige Erdung und dasselbe Aufgabenpaket. Lade nur
fehlende oder veränderte Texte nach; boote nicht bei jeder Iteration den ganzen Lebenszyklus neu.

## Die Boot-Sequenz

1. **Lade das Invarianten-Fundament.** Lies
   [invariant-floor](../invariant-floor/SKILL.md), bevor du irgendwas anfasst.
   Das ist der Boden, auf dem die ganze Session steht.
2. **Wende [Build Flow](../backs-build-flow/SKILL.md) an.** Es besitzt Aufgabenmodus,
   Handlungsreife, Skill-Auswahl, begrenztes RED/GREEN mit gezieltem Lint und Tests,
   Gauntlet-Belege und Lieferung. Verwende ein verifiziertes Paket weiter und
   sammle nur fehlende Fakten für die nächste konkrete Handlung. Spezialisten
   kehren zu einem Verantwortlichen zurück.
3. **Wende Menschenkontext an** ([human-calibration](../human-calibration/SKILL.md)),
   soweit relevant. [operator-essence](../operator-essence/SKILL.md) besitzt die
   belegte Kontextdatei und den Insights-Durchgang bei fehlender Datei;
   starte keinen zweiten Profilzyklus.
4. **Lade die Session.** Der Session-Hook liefert die tatsächlichen Texte von
   Optimus, Yoke und Build Flow sowie das nachgewiesene native Harness, wenn
   verfügbar. Kompaktierung lädt diese Texte nach, ohne erworbene Erdung zu
   entziehen. Ein fehlender Marker bei einem mutierenden Tool löst Laden aus,
   niemals eine Tool-Verweigerung. Hosts ohne Kontexthook können nutzen:
   ```bash
   node "$HOME/.local/share/backs-aios/current/hooks/aios_gate.js" --load backs-aios:optimus
   ```
   Hänge in einer Codex-Shell die aktive `CODEX_SESSION_ID` als letztes Argument
   an. Python steht über den passenden `aios_gate.py`-Loader bereit. Unbekannte
   Skills liefern einen Fehlerstatus, ohne einen Beleg zu erfinden.
5. **Wende die Skills an, die die nächste Handlung braucht.** Benenne jeweils Zweck,
   Ergebnis und Ausstieg. Ein nur genannter Skill hat nicht stattgefunden.
   Verwende echte Texte weiter, die im aktuellen Kontext verfügbar sind;
   erinnerte Zusammenfassung oder Dateihash ersetzen sie nicht.
6. Erst dann: Code schreiben, mutierende Kommandos fahren, irgendwas ändern.

## Automatische Erdung

Der vorhandene Hook liest die Fundamentdateien und liefert ihre Texte durch den
Host-Kontext. Er erfasst Quellhashes erst nach der Lieferung. Kontextladebelege
sind von tatsächlichen Skill-Event-Belegen verschieden; ein Zeiger oder Dateihash
ist kein Aufruf dieses Skills.

- Session-Start und Kompaktierung laden das Fundament nach, ohne Tools zu entziehen.
- Ein fehlender Session-Marker löst beim nächsten passenden Tool automatisches Laden aus.
- Fehlende oder unlesbare Texte erzeugen sichtbare Diagnose und keinen falschen
  Beleg; Operator und Agenten behalten ihre Tools.
- `--rearm <session_id>` fordert erneutes Laden an. Es sperrt die Session nie.
- `AIOS_GATE=off` bleibt der bestehende reversible Kill-Switch des Operators.
- Hooks sind lokal und deterministisch. Kein Modellaufruf und keine Netzabhängigkeit kommen hinzu.

## Harte Regeln (was diesen Skill reißen lässt)

- Irgendeine Mutation, bevor das Harness geladen ist.
- Ein Skill, der im Report genannt, aber in der Session nie aufgerufen wurde.
- Ein Hook, der irgendein Tool verweigert, erworbene Erdung entzieht oder Laden meldet, das nicht stattfand.
- Ein zweites Gate, oder irgendeine neue Reibung für den Menschen. Der
  Kill-Switch bleibt seiner.

## Passt gut zu

- [invariant-floor](../invariant-floor/SKILL.md) — das Fundament, das der Boot zuerst lädt.
- [human-calibration](../human-calibration/SKILL.md) — der Profil-Schritt des Boots.
- [repair-loop](../repair-loop/SKILL.md) — was ein Fix-Job nach dem Boot fährt.
- [bounded-loops](../bounded-loops/SKILL.md) — Budgets für jede Schleife, die der Boot startet.
- [wayfinder](../wayfinder/SKILL.md) — wenn der Boot zeigt, dass du die Route nicht kennst.
