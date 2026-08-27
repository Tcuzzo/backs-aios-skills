# Design Taste

Das Play für jedes UI, das designt aussieht, nicht generiert. Generisches UI ist ein
WORKFLOW-Bug, kein Modell-Bug: Trenne die Geschmacksarbeit von der Implementierung,
setze zuerst exakte Design-Tokens, gib dem Agenten Augen und gate auf
Barrierefreiheit (Accessibility).

## Wann dieses Play läuft

Jeder Screen, jede Seite, jede Komponente, jedes Dashboard, jedes visuelle Ergebnis,
das ein Mensch ansehen wird. Der erste Screen setzt den Standard für jeden danach —
fahre dieses Play davor.

## Die Kette

1. [intent-compiler](../skills/intent-compiler/SKILL.md) — leite ab, WELCHEN
   Geschmack die eigenen Worte des Menschen verlangen, und formuliere diese Lesart
   in einer Zeile, bevor du schreibst.
2. [human-calibration](../skills/human-calibration/SKILL.md) — verankere die Lesart
   im Verlauf dieses Menschen und in echten, studierten Referenzen — niemals in
   einer demografischen Vermutung.
3. Erzeuge ZUERST die dreistufige Design-Token-Datei, vor jeder Komponente — die
   volle Token-Spezifikation und die Liste verbotener Defaults stehen in
   [design-taste](../skills/design-taste/SKILL.md).
4. Baue Komponenten mit der Token-Datei als hart injizierter Randbedingung.
   Hardcode niemals einen rohen Hex-Wert, Pixel-Wert oder eine Font-Family in
   einer Komponente.
5. Fahre die Screenshot-→-Kritiker-Schleife nach
   [design-taste](../skills/design-taste/SKILL.md) und löse das Kritiker-Modell
   live über [fleet-ladder](../skills/fleet-ladder/SKILL.md) auf.
6. Bewerte die 8-Achsen-Geschmacks-Rubrik nach
   [design-taste](../skills/design-taste/SKILL.md).
7. Erzwinge das HARTE Barrierefreiheits-Gate nach WCAG 2.2 per
   [design-taste](../skills/design-taste/SKILL.md).
8. [clean-code-gauntlet](../skills/clean-code-gauntlet/SKILL.md) — nur auf dem
   Code HINTER den Pixeln: Token-Resolver, Theme-Umschalter, Kontrast-Rechner und
   State-Reducer bestehen mit null überlebenden Mutanten. Ein umgedrehter
   Vergleich in einem Kontrast-Check liefert einen schönen, unzugänglichen Screen
   aus. Das Gauntlet bewertet niemals Geschmack — die Rubrik und das
   Barrierefreiheits-Gate bleiben die visuellen Richter. Rendere in Tests echtes
   DOM; ein gemocktes Rendering beweist nichts über das, was der Mensch sieht.

## Harte Gates (play-spezifisch — die eigenen harten Regeln des Skills gelten obendrauf)

- Der Kritiker ist eine ANDERE Modellfamilie als der Builder, live über die
  Fleet-Ladder aufgelöst — niemals eine fest gepinnte Modell-ID (ein stillgelegter
  Pin tötet den ganzen Kritiker lautlos).

## Passt gut zu

- [blind-tribunal](../skills/blind-tribunal/SKILL.md) — das ganze Ergebnis benoten lassen
- [sniper-testing](../skills/sniper-testing/SKILL.md) — die Komponenten-Tests scopen

**Weight:** light durch die ganze Schleife — die Kalibrierung und der Screenshot-Kritiker-Durchgang kosten je einen Extra-Lauf; der heavy-Schritt ist das Gauntlet über den Code hinter den Pixeln — er zahlt sich bei jedem Screen aus, den ein Mensch wirklich ansehen wird.
