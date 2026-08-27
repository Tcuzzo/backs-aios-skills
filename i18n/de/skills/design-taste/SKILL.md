---
name: design-taste
description: Nutze das, bevor du irgendetwas Visuelles baust — Site, App, Dashboard, Konsole oder Deck — damit es mit echtem Geschmack shippt statt mit generischen KI-Defaults. Trigger words: design, UI, taste, design tokens, design system, accessibility, WCAG, screenshot critique, dark mode, restyle, Gestaltung, Geschmack, Designsystem, Barrierefreiheit, umgestalten.
license: MIT
---

# Design-Geschmack — Tokens zuerst, Augen drauf, Barrierefreiheit hart

Generische UI ist ein Workflow-Bug, kein Modell-Bug. Behebe ihn strukturell: Lies
das Briefing als Spezifikation, setze exakte Design-Tokens vor jeder Komponente,
verbiete die Defaults beim Namen, gib dem Builder Augen mit einer
Screenshot-Schleife, und gate auf Barrierefreiheit — hart.

## Wann einsetzen

- Jede „Bau mir ein / Designe mir ein …“-Anfrage, die Pixel rendert.
- Bevor ein Frontend oder ein kundengerichtetes Deliverable aufgesetzt wird.
- Wenn eine bestehende Oberfläche generisch aussieht und eine spezifische,
  verteidigbare Richtung braucht.

## Schritte

1. **Lies das Briefing als Spezifikation.** Eine Metapher, ein Rhythmus, eine
   benannte Ära, ein Künstler oder ein Ort in den Worten des Menschen ist eine
   konkrete Design-Constraint, keine Deko. Volle Briefing-Disziplin:
   [intent-compiler](../intent-compiler/SKILL.md).
2. **Wähle eine geerdete Richtung.** Wähle eine *Lead*-Referenz (ein echtes
   Designsystem oder eine Library, die die strukturelle Baseline setzt) und eine
   *Akzent*-Referenz (eine, die ihre Signatur oben drauf prägt). Beide müssen echt
   und aktuell sein, mit verifizierbarer Geschmackssignatur. Ein erfundener Vibe
   lässt das Gate geschlossen scheitern.
3. **Emittiere Tokens ZUERST.** Schreibe vor jeder Komponente eine
   maschinenlesbare, dreistufige Design-Token-Datei (primitiv → semantisch →
   Komponente; W3C-Token-Format, `$value` + `$type`). Lege vorab fest: eine
   perzeptuell gleichmäßige Farbrampe (Oklch — ein Farbraum, in dem gleiche
   Schritte gleich aussehen), eine echte Typo-Skala auf einer
   Nicht-Default-Schrift, ein Spacing-Inkrement (4px-Basis →
   4/8/12/16/24/32/48/64), eine Radius-Skala, eine Elevations-Skala und benannte
   Motion-Tokens (Dauer + Easing pro Enter / Scroll / State-Change; respektiere
   `prefers-reduced-motion`). Dark und Light sind erstklassig, und beide lösen aus
   DENSELBEN semantischen Tokens auf.
4. **Verbiete die generischen Defaults beim Namen.** Verbote schlagen Adjektive:
   keine Reflex-Schrift (Inter/Roboto), keine lila Verläufe, kein zentrierter
   Hero, keine Reihe aus drei gleichen Karten, keine Grau-auf-Weiß-Platte. Ergänze
   pro Projekt deine eigene Bannliste.
5. **Baue unter Constraint.** Komponenten konsumieren nur Tokens. Ein rohes Hex,
   px oder eine Font-Family, hart in einer Komponente codiert, ist ein Defekt.
6. **Schließe die Schleife Screenshot → Vision-Kritiker.** Für alles Gerenderte:
   in einem Headless-Browser bei Mobil- und Desktop-Breiten rendern, screenshotten
   und von einem Vision-Modell bewerten lassen — dann fixen, in getrennten
   Durchgängen (Kritik → strukturelle Korrektur → Audit → Politur), nie in einem
   Rutsch. Der Kritiker ist ein Grader: Nimm ein Modell aus einer anderen Familie
   als der Builder, mit benannten Achsen, nie einem holistischen Gesamtscore.
   Löse das Kritiker-Modell zur Laufzeit aus der Config auf — eine gepinnte
   Modell-ID geht irgendwann in Rente und reißt die ganze Schleife mit.
7. **Score die 8-Achsen-Geschmacksrubrik.** 0–3 pro Achse, und jede Achse muss
   ≥ 2 erreichen: Token-Treue · Layout/Hierarchie · Typografie · Farbe/Kontrast ·
   Motion · Dark-Light-Parität · Barrierefreiheit · Designed-vs-Durchschnitt-
   Bauchcheck („sieht das designt aus, oder wie der Durchschnitt von allem?“).
   Eine Achse unter 2 = nicht fertig.
8. **Erzwinge das HARTE Barrierefreiheits-Gate (WCAG 2.2).** Pointer-Ziele
   ≥ 24×24 CSS-px. Sichtbarer Fokusindikator ≥ 2px Umfang bei ≥ 3:1 Kontrast.
   Textkontrast ≥ 4.5:1 normal, ≥ 3:1 großer Text und UI-Komponenten. Voll per
   Tastatur navigierbar. Kontrast in BEIDEN Themes verifiziert. Das ist ein Gate,
   kein Vorschlag: durchgefallen = nicht ausliefern.
9. **Teste den Code hinter den Pixeln.** Token-Resolver, Theme-Switches,
   Kontrastrechner und State-Reducer bekommen echte Tests auf echt gerendertem
   DOM — ein verdrehter Vergleich in einem Kontrast-Check shippt einen schönen
   Screen, der still unzugänglich ist. Tests beurteilen den Code; die Rubrik und
   das WCAG-Gate beurteilen den Geschmack.

## Harte Regeln — eine einzige verletzt, und der Skill ist gescheitert

- Eine Komponente, geschrieben bevor die Token-Datei existiert.
- Ein rohes Hex / px / eine Font-Family in einer Komponente.
- Irgendein Eintrag der Bannliste taucht im Output auf.
- Die Schleife Screenshot → Kritiker für Gerendertes überspringen.
- Der Builder bewertet die eigenen Visuals, oder ein einzelner Gesamtscore statt
  Achsen.
- Irgendeine Rubrik-Achse unter 2, oder irgendein WCAG-2.2-Check rot, zum
  Ship-Zeitpunkt.
- Eine Geschmacksrichtung, die sich nicht in einer echten, verifizierbaren
  Referenz erden lässt.

## Passt gut zu

- [intent-compiler](../intent-compiler/SKILL.md) — die volle Briefing-Disziplin.
- [blind-eval](../blind-eval/SKILL.md) — Keep-or-Revert, wenn Geschmack die Frage ist.
- [clean-code-gauntlet](../clean-code-gauntlet/SKILL.md) — das Härten des Codes hinter den Pixeln.
- [blind-tribunal](../blind-tribunal/SKILL.md) — Cross-Family-Bewertung vor dem Landen.

> Gerüst-Credit: W3C Design Tokens Community Group (Token-Format); WCAG 2.2, W3C
> (Barrierefreiheits-Gate); UICrit, UIST 2024 (achsen-bewertete UI-Kritik);
> AI Jason, & JackJack. (2025). superdesign: AI design agent [Computer software].
> GitHub. https://github.com/superdesigndev/superdesign (AGPL-3.0; dual-licensed
> with a commercial enterprise license) — forbid-the-defaults. Die Komposition und
> die harten Regeln hier sind BACKS AIOS.
