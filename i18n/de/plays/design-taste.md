# Design Taste

Das Play für jedes UI, das designt aussieht, nicht generiert. Generisches UI ist ein
WORKFLOW-Bug, kein Modell-Bug: Trenne die Geschmacksarbeit von der Implementierung,
setze zuerst exakte Design-Tokens, gib dem Agenten Augen und gate auf
Barrierefreiheit (Accessibility).

## Wann dieses Play läuft

Jeder Screen, jede Seite, jede Komponente, jedes Dashboard, jedes visuelle Ergebnis,
das ein Mensch ansehen wird. Der erste Screen setzt den Standard für jeden danach —
fahre dieses Play davor.

Der Geschmacks-Loop auf einen Blick:

```
+--------------------------------------------+
| 1 intent-compiler  WHICH taste do the      |
|   human's words ask for? state the read    |
+--------------------------------------------+
| 2 human-calibration  anchor in the record  |
|   + studied references, never a guess      |
+--------------------------------------------+
| 3 design-taste  emit the three-tier        |
|   token file FIRST, before any component   |
+--------------------------------------------+
| 4 build with the token file as a hard      |<--------------------------+
|   constraint -- no raw hex, px, fonts      |  critique -> fix ->       |
+--------------------------------------------+  re-shoot                 |
| 5 design-taste  screenshot -> critic;      |   +---------------------+ |
|   critic resolved live via fleet-ladder    |-->|  LORD OF THE LOOP   |-+
+--------------------------------------------+   | one hand drives the |
| 6 design-taste  8-axis taste rubric        |   | loop: dispatch,     |
+--------------------------------------------+   | judge, loop back    |
| 7 design-taste  WCAG 2.2 HARD gate         |   | until the gate is   |
+--------------------------------------------+   | green. a lane never |
| 8 clean-code-gauntlet  the code BEHIND     |   | lands its own work. |
|   the pixels; zero surviving mutants       |   +---------------------+
+--------------------------------------------+
          |
          | rubric + WCAG green
          v
+--------------------------------------------+
| LANDING GATE -- all green or no ship:      |
| WCAG 2.2 passes . 8-axis rubric scored .   |
| zero surviving mutants behind the pixels   |
| . critic family != builder family, live-   |
| resolved via fleet-ladder, never pinned    |
+--------------------------------------------+
```

*Labels im Diagramm: „Lord of the Loop“ = der Besitzer des Loops, der die Iteration treibt, bis das Landing-Gate grün ist; „LAND“ = die Landung — die Änderung zieht erst ein, wenn jedes Gate grün ist.*

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
