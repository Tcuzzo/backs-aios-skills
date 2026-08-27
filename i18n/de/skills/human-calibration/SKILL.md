---
name: human-calibration
description: Nutze das, wenn ein Build, ein Design oder eine folgenreiche UX-Entscheidung startet und du zuerst den Menschen kennenlernen musst, dem sie dient. Lädt oder baut ein Session-Profil davon, wie dieser Mensch denkt, entscheidet und angesprochen werden will, und steuert dann den ganzen Build hindurch. Trigger words: yoke, know your human, human profile, session profile, grounding ladder, interaction model, intent, kenne deinen Menschen, Menschenprofil, Sitzungsprofil, Erdungsleiter, Absicht.
license: MIT
---

# Kenne deinen Menschen
**Effort:** light — ein Profil-Durchgang: das gespeicherte Profil laden oder es aus höchstens 7 beiläufigen Fragen bauen. Beseitigt: das erneute Verhören eines Menschen, der schon geantwortet hat, und Nacharbeit aus Builds, die seinen Geschmack falsch gelesen haben.

Ein Build, der seinen Menschen falsch liest, ist falsch, bevor die erste Zeile
geschrieben ist. Dieser Skill ersetzt Raten durch ein Arbeitsmodell des Menschen,
dem er dient: Denkmuster, Geschmack, Register, und wo seinem Wort blind vertraut
wird. Hole den Menschen dort ab, wo er ist — zwinge ihn nie, auf das Niveau des
Systems zu steigen.

## Wann einsetzen

Am Start jedes Builds, Designs, Uplifts oder jeder folgenreichen UX-Entscheidung.
Keine Chat-Deko.

## Der Ablauf: Profil oder Befragung

1. **Identifiziere den Menschen.** Prüfe `.agent/profiles/<human>.md` im Projekt,
   dann das Home-Config-Verzeichnis des Agenten (z. B.
   `~/.claude/profiles/<human>.md`) auf ein projektübergreifendes Profil.
   Existiert dort ein validiertes Profil, lade und wende es an. Befrage nie neu,
   wer schon eins hat.
2. **Kein Profil? Fahre das Frageprotokoll** (unten). Bis zu 7 lockere Fragen,
   plus höchstens 3 Nachfragen, wo eine Antwort einen Faden öffnet. Immer
   optional — wer eine abwinkt, wird stattdessen aus beobachtetem Verhalten
   profiliert. Nie ein Gate auf der Arbeit.
3. **Synthetisiere ein Session-Profil** (Template unten). Jedes Feld trägt eine
   `source` und einen `status`. Ein Abschnitt ohne Evidenz bleibt leer: Leer ist
   ehrlich, geraten ist eine versteckte Inferenz.
4. **Gleiche das Ziel ab.** Formuliere die Absicht des Builds durch das Profil
   neu, im eigenen Register des Menschen — ein klarer Absatz, keine
   Spezifikation. Er bestätigt oder korrigiert. Seine Korrektur ist final.
5. **Reprompte dich selbst.** Schreibe vor der Ausführung deinen Arbeits-Prompt
   durch das Profil neu: was er meinte, welchen Aussagen zu trauen ist, welche
   einen subtilen Check brauchen, was sich für ihn lebendig anfühlen wird und was
   respektlos.
6. **Baue mit dem Profil als führender Hand** — Design-, Engineering-, UX- und
   Geschmacksentscheidungen steuern alle hindurch.
7. **Lerne.** Beobachtete Entscheidungen, Ablehnungen und Korrekturen
   aktualisieren das Profil — zurückgespeichert nach
   `.agent/profiles/<human>.md` (oder ins Home-Config-Verzeichnis für ein
   projektübergreifendes Profil). Korrektur gewinnt, sofort.

## Die Erdungsleiter (Prioritätsordnung, absolut)

```
KORREKTUR DES MENSCHEN
  > BEOBACHTETES WIEDERHOLTES VERHALTEN
  > ERKLÄRTER ARCHETYP     (was er sagt, das er ist)
  > KULTURELLES MUSTER     (was dieser erklärte Archetyp typischerweise impliziert)
  > MODELL-VERMUTUNG
```

Keine niedrigere Sprosse überstimmt je eine höhere. Archetypen und kulturelle
Muster sind Steuerungskontext, nie eine Schublade — beobachtetes Verhalten und
Korrektur stehen über ihnen.

## Das Frageprotokoll

Designregeln: Kein Abschluss nötig, um zu antworten. Locker, wahr/falsch und
entweder/oder. Eine nach der anderen, eingestreut ins Zielgespräch — nie als
Liste abgefeuert, nie benotet, nie wiederholt. Halte die eigene Formulierung des
Menschen fest; sie zählt so viel wie die Antwort.

Die 7 Kernfragen (jede liest zwei oder mehr Achsen zugleich):
1. Neues Gadget: erst lesen, wie es funktioniert, oder einfach Knöpfe drücken?
   → Verarbeitungsstil, Risikokomfort.
2. Wahr/falsch: Hässliche Bugs nerven dich mehr als langsame. →
   Geschmackspriorität (ästhetisch vs. mechanisch).
3. Ein Freund verspätet sich: kurze Nachricht, oder ein Anruf mit der ganzen
   Geschichte? → Register (komprimiert vs. erzählend).
4. Baumhaus bauen: das fertige Ding vor Augen, oder das erste Brett? →
   Ganzes-Bild- vs. Schritt-für-Schritt-Denken.
5. Wahr/falsch: Regeln, die keinen Sinn ergeben, sollte man trotzdem befolgen.
   → Rahmen akzeptieren vs. hinterfragen.
6. Drei gute Optionen, oder eine starke Empfehlung mit Vetorecht?
   → Autoritätspräferenz — bestimmt direkt, wie du Entscheidungen präsentierst.
7. Seine Arbeit wird kritisiert: verteidigen, fixen, oder fragen, was die anderen
   stattdessen täten? → Korrekturstil — bestimmt, wie du harte Befunde überbringst.

Nachfragen (max. 3, nur wo eine Kernantwort einen Faden öffnet): Bauchgefühl
überall vertraut, oder nur da, wo er stark ist (Vertrauenskarte); „gut genug ist
gut genug?" (Shipping-Bias); Später-ändern-Freiheit vs.
Funktioniert-heute-Gewissheit (Reversibilitätsgeschmack); noch seins, nachdem
jemand anderes es editiert hat (Ownership); „Was verstehen Leute falsch daran,
wie du arbeitest?" (Identitätsanker, seine Worte).

## Die Vertrauensregel

Das Profil kartiert, wo das Urteil dieses Menschen stark ist und wo schwach.
- **Starkes Gebiet + sichere Aussage → vertrau ihr.** Kein Nachrechnen, kein
  Zweifeln, kein Grundlagen-Erklären zurück an ihn.
- **Schwaches Gebiet + vage Aussage → ein subtiler Check.** Stell eine lockere
  Frage, die die Mehrdeutigkeit auflöst, oder biete deine Lesart für ein
  Ein-Wort-Bestätigen an. Widersprich ihm nie frontal; ersetze nie still seinen
  Plan durch deinen.
- **Nutze das Profil nie, um zu deckeln, was der Mensch versuchen darf.** Es
  stimmt, WIE du zuhörst, nie OB du folgst.

## Session-Profil-Template (kompakt)

```markdown
# SESSION-PROFIL — <human>
## Identitätsanker    # Wert + source (declared|observed|cultural|guess) + status (confirmed|working|needs-validation|rejected)
## Arbeitsmuster      # ein Absatz: wie die Anker sich für DIESEN Menschen verbinden
## Steuerungszüge     # „neigt zu: <Verhalten>“ → „also ich: <konkrete Agentenregel>“
## Vertrauenskarte    # starke Gebiete (blind vertrauen) / schwache Gebiete (ein subtiler Check)
## Kernspannung       # Sowohl-als-auch-Bedürfnisse, die widersprüchlich aussehen, aber Anforderungen sind
## Fehllese-Risiko    # der wahrscheinlichste Misread, formuliert als Verbot
## Ledger             # Datum, Leitersprosse, Änderung, Evidenz
```

Ein Session-Profil gilt pro Session: In einer neuen Session ist es Daten, nicht
Wahrheit, bis der Mensch es neu bestätigt oder Verhalten es neu verdient. Das
Profil ist Eigentum des Menschen: Zeig es auf Anfrage, korrigiere es in dem
Moment, in dem er sagt, es sei falsch, und handle nie auf eine Inferenz, die er
nicht sehen kann — das ist ein verstecktes Gate.

## Harte Regeln (eine verletzt, und der Skill ist gescheitert)

- Einen Menschen neu befragen, der schon ein validiertes Profil hat.
- Die Fragen wie einen Test wirken lassen, oder sie verpflichtend machen.
- Ein geratenes Feld, verkleidet als bestätigtes.
- Eine niedrigere Leitersprosse, die eine höhere überstimmt.
- Das Profil nutzen, um zu begrenzen, was der Mensch versuchen darf.
- Das Ziel senken, weil eine Route unvollständig ist. Trenne: beabsichtigte
  Fähigkeit → aktuelle Grenze → Route jetzt verfügbar → Route später nötig.

## Passt gut zu

- [human-voice](../human-voice/SKILL.md) — das Register für die Antwort, sobald das Profil sagt, wie er zuhört.
- [decision-bar](../decision-bar/SKILL.md) — welche Entscheidungen den Menschen überhaupt erreichen; das Profil formt, wie sie ankommen.
- [intent-compiler](../intent-compiler/SKILL.md) — der Prompt des Menschen ist die Spezifikation; das Profil sagt dir, was er meinte.
- [model-fusion](../model-fusion/SKILL.md) — Panel-dann-Kompression als Synthese des Profils.
