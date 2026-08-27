---
name: repair-loop
description: Beim Fixen eines Bugs, beim Schließen eines gemeldeten Issues oder beim Uplift einer Naht von Anfang bis Ende. Fährt die volle Reparatur-Schleife — im Fundament erden, auf Live-Wahrheit reproduzieren, roter Vertrags-Test, die Klasse an der Naht fixen, auf dem echten Pfad verifizieren, unabhängige Bewertung, landen — und iteriert, bis es wahr ist. Trigger words: repair loop, dev mode, fix this, uplift, close the seam, dev build, Reparatur-Schleife, fix das, Naht schließen, bau das fertig.
license: MIT
---

# Repair Loop

Die Standard-Schleife für jeden Fix, jeden Bug-Abschluss, jeden Uplift. Sie ist
ein Verhalten, keine Freigabe-Maschinerie: sie fügt dem Menschen null Gates und
null Reibung hinzu. Sie bindet den Agenten an eine Disziplin, die „grün, aber
kaputt" strukturell schwer auslieferbar macht.

## Zuerst laden, vor jedem Entwurf und jedem Edit

1. [invariant-floor](../invariant-floor/SKILL.md) — lies dein Regelwerk, bevor du arbeitest.
2. [human-calibration](../human-calibration/SKILL.md) — wende das Profil des Menschen an; verhör ihn nie neu.
3. [understanding-gates](../understanding-gates/SKILL.md) — der Diagnose-Planer: Design → Plan → Build → Test → Ship.
4. [wayfinder](../wayfinder/SKILL.md) — wenn du verloren bist, kartier die Route; park nie eine Frage beim Menschen.
5. Kommt die Bitte als Prosa oder Metapher, fahr zuerst [intent-compiler](../intent-compiler/SKILL.md) und loope auf der abgeleiteten Direktive.

## Die Schleife

1. **Im Fundament erden.** Lade die Regeln und die eigene Wahrheit des Projekts
   (Doku, Quellcode, Tracker), bevor du Code anfasst. Arbeit aus der Erinnerung
   an die Regeln zählt nicht.
2. **Auf Live-Wahrheit reproduzieren.** Sieh das Versagen selbst, auf dem
   echten Pfad, den der Mensch nutzt — kein Proxy-Probe, kein Vertrauen aufs
   Wort des Bug-Reports. Keine Reproduktion, kein Fix.
3. **Roter Vertrags-Test.** Schreib einen fehlschlagenden Test, der den Defekt
   einfängt, und committe ihn vor dem Fix. Beweis, dass er wirklich rot ist.
   Der Fix macht ihn grün; der Fix editiert den Test nie. Siehe
   [red-first](../red-first/SKILL.md).
4. **Fix die KLASSE an der Naht** — kein Punkt-Pflaster pro Symptom. Die volle
   Formel steht in [seam-engineering](../seam-engineering/SKILL.md).
5. **Auf dem echten Pfad verifizieren.** Vertrauen ist gut, prüfen ist Pflicht.
   Fähigkeit wird auf der eigenen Oberfläche des Menschen bewiesen — die UI, in
   die er tippt, das Kommando, das er fährt — nie über einen grünen Test auf
   einer gemockten Naht. Prüf jede Behauptung („der andere Branch hat es
   gelandet", „der Service ist down“) gegen die Live-Wahrheit, bevor du danach
   handelst.
6. **Den Fix vermessen.** Mitten in der Schleife nur die Tests fahren, die die
   angefasste Naht abdecken — siehe [sniper-testing](../sniper-testing/SKILL.md).
   Dann den [clean-code-gauntlet](../clean-code-gauntlet/SKILL.md) über den
   geänderten Code: gescopte Tests, Komplexität-gegen-Coverage-Score,
   begrenztes Mutation-Testing. Überlebt ein Mutant deinen Fix, hat der Test
   den geänderten Zweig nie erreicht — Fake-Green; weiter iterieren.
7. **Unabhängige Bewertung.** Ein Bewerter, der die Änderung nicht geschrieben
   hat — ideal ein Modell aus einer anderen Familie als der Builder — muss sie
   durchwinken. Der Builder bewertet seine eigene Arbeit nie. Siehe
   [blind-tribunal](../blind-tribunal/SKILL.md).
8. **Nebenläufige Arbeit prüfen.** Bevor du geteilten Zustand änderst,
   verifizier, dass die laufende Arbeit anderer Sessions gesichert ist (auf
   einem Branch oder Commit). Committe oder räum nie Arbeit weg, die nicht
   deine ist.
9. **Landen.** Ein voller Durchlauf über die Suiten der angefassten Module beim
   Landen, dann committen. Schließ jeden Fund, den die Schleife auf dieser Naht
   hochgebracht hat — oder halt pro Fund ein explizites, belegtes
   „kein Bug“-Urteil fest. „Den Großen gefixt, der Rest kommt später“ landet
   nie.

## Iterieren, bis es wahr ist

Eine noch nicht erfüllte Regel stoppt die Schleife nicht — sie treibt sie an.
Eskalier das Modell oder die Stufe, beseitig den Blocker, versuch es neu, bis
jeder Schritt oben wahr ist und die Änderung landet. „Gut genug“ ist kein
Status. Bist du an derselben Naht zweimal ehrlich festgefahren, logg den
exakten Blocker-Beweis und geh zum nächsten freien Stück — nie stumm
weiterschleifen.

## Harte Regeln — eine davon, und der Skill ist gerissen

- Fix ausgeliefert ohne Reproduktion auf Live-Wahrheit.
- Test nach dem Fix geschrieben, oder vom Fix editiert.
- Symptom geflickt, während die Klasse an der Naht offen bleibt.
- Fähigkeit über einen Proxy als grün behauptet, während der eigene Pfad des
  Menschen kaputt ist.
- Der Builder hat seine eigene Änderung bewertet.
- Ein hochgekommener Fund beim Landen stumm vertagt.
- Schleife bei „gut genug“ abgebrochen statt eskaliert.

## Report

Zwei Wörter — **PROVEN** oder **STILL-BUILDING** — plus die Absicht in
Klartext und die eine Entscheidung, die vor dem Menschen liegt, falls es eine
gibt. Fragen gehen nur für Geschmack, Vision oder destruktives Risiko an den
Menschen; siehe [decision-bar](../decision-bar/SKILL.md).

## Passt gut zu

- [incident-closure](../incident-closure/SKILL.md) — meldet der Mensch Bruch, läuft diese Schleife in einem vollen Abschluss.
- [red-first](../red-first/SKILL.md) · [seam-engineering](../seam-engineering/SKILL.md) · [sniper-testing](../sniper-testing/SKILL.md)
- [blind-tribunal](../blind-tribunal/SKILL.md) · [clean-code-gauntlet](../clean-code-gauntlet/SKILL.md)
