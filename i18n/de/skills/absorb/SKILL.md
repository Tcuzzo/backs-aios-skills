---
name: absorb
description: Nutze das, wenn du eine Fähigkeit brauchst, die ein Open-Source-Projekt schon liefert — übernimm sie und baue sie als nativen Skill neu, statt ein Duplikat zu erfinden. Trigger words: absorb, adopt, port, re-engineer, ingest a repo, prior art, capability port, make this native, absorbieren, übernehmen, portieren, nachbauen, einverleiben, Vorarbeit nutzen, nativ machen.
license: MIT
---

# Absorb — Übernimm Vorarbeit, erfinde sie nicht neu

**Die Fähigkeit ist König.** Ein Repo ist ein Vehikel für eine Fähigkeit. Wenn du etwas
brauchst, das ein bestehendes Projekt schon kann, bau kein Duplikat von null, und mach
kein Clone-and-Paste. Finde die beste Vorarbeit, extrahiere die Fähigkeit, baue sie
passend zu deinem Harness neu und zitiere das Gerüst. Das Zitat ist ein Fakt, keine Deko.

## Wann einsetzen

- Du sollst eine Fähigkeit hinzufügen (ein Tool, einen Skill, einen Agenten, eine
  Pipeline), die Open Source sehr wahrscheinlich schon gelöst hat.
- Du bist kurz davor, per `git clone` Code wortwörtlich zu kopieren — stopp; dieser
  Weg hier ist stattdessen der richtige.
- Lass es bei einem einzelnen Snippet, einem Config-Wert oder einem Fakten-Lookup.
  Die liest du einfach.

## Schritte

1. **Jage zuerst nach Vorarbeit.** Suche, bevor du baust. Ein Duplikat, das du
   erfindest, ist schlechter als ein Gerüst, das du übernimmst: Du erbst null
   Praxiserprobung und schuldest alle Bugs selbst.
2. **Lies tiefer als das README.** Hol die Projekt-Metadaten (Lizenz, Aktivität,
   Sprache) über die Plattform-API. Shallow-Clone in ein Scratch-Verzeichnis. Lies
   den Code und die Tests. Das README ist Marketing; der Code ist die Wahrheit.
3. **Fahre die Vertrauens-Gates.**
   - *Lizenz:* permissiv (MIT / Apache / BSD / MPL) = sicher zum Nachbauen.
     Copyleft (GPL / AGPL) = nur die Technik — bau die Idee nach, kopiere nie den
     Code. Keine Lizenz = behandeln wie „alle Rechte vorbehalten“, nur die Technik.
     Nicht-kommerzielle Bedingungen = ein Blocker; geh damit zu deinem Menschen.
   - *Shady-Scan:* grep nach Cloaking-, Spam-, Fake-Review- und Scam-Mustern.
     Melde laut.
   - *Keine wilden Installs:* nie `pip install` / `npm install` auf eine ungeprüfte
     Abhängigkeit (Typo-Squatting ist ein realer Supply-Chain-Angriff). Bau
     stattdessen dünnen Code über deinen eigenen Primitiven.
   - *Ist die Fähigkeit echt?* Prüfe Behauptungen gegen unabhängige Belege. Der
     Blog eines Verkäufers ist eine Behauptung, kein Beleg. Urteil: echt / Hype /
     Scam / nicht verifizierbar.
   - *Begrenzter Egress:* alles, was die übernommene Version nachlädt, muss
     gedrosselt, gecacht und abschaltbar sein.
4. **Zerlege in eine Fähigkeiten-Karte.** Für jede Fähigkeit des Projekts notiere:
   was sie tut, wie, ihre tragenden Nähte, ihren Ballast oder ihr Risiko, was du aus
   deinem eigenen Stack wiederverwenden kannst, und ob sie nativ landet oder hinter
   einem dünnen Adapter. Jede Fähigkeit wird **erhalten oder mit Belegen widerlegt**.
   Eine still fallengelassene Fähigkeit ist ein Defekt.
5. **Schreib die Neubau-Spezifikation.** Die Nähte, die du baust, den Ballast, den du
   wegwirfst (laut festgehalten, nie still), und pro Fähigkeit ein fehlschlagender
   Contract-Test, der einen echten Nebeneffekt prüft — eine Datei, eine
   Datenbankzeile, echte Ausgabe. Mocke höchstens den Transport einer bezahlten
   externen API, nie die Logik.
6. **Baue rot-zuerst wieder auf.** Committe die fehlschlagenden Tests, dann baue, bis
   die ganze Naht grün ist. Ein Modell aus einer anderen Familie als der Builder
   bewertet das Ergebnis — der Builder bewertet nie die eigene Arbeit.
7. **Zitiere und dokumentiere.** Schreib den Gerüst-Credit dorthin, wo die Fähigkeit
   jetzt lebt: Autor, Projekt, Lizenz, was geliehen ist (das Gerüst) und was deins
   ist (der Neubau). Erfinde nie einen Credit. Entferne nie einen.

## Harte Regeln — eine einzige verletzt, und der Skill ist gescheitert

- Code wortwörtlich kopieren, statt die Fähigkeit neu zu bauen.
- Ein Duplikat bauen, ohne je nach Vorarbeit gesucht zu haben.
- Dem README oder einer Marketing-Seite mehr glauben als dem Code.
- Eine wilde Abhängigkeit installieren, statt die Technik nachzubauen.
- Copyleft- oder unlizenzierten Code kopieren (nur die Technik, immer).
- Eine Fähigkeit fallenlassen ohne schriftliche Widerlegung.
- Mock-Theater in einem Fähigkeits-Test — der Test muss einen echten Nebeneffekt
  anfassen.
- Ausliefern ohne das Gerüst-Zitat.

## Passt gut zu

- [red-first](../red-first/SKILL.md) — die Contract-Tests, die jede Fähigkeit absichern.
- [sniper-testing](../sniper-testing/SKILL.md) — echte Nebeneffekte, kein Mock-Theater.
- [blind-tribunal](../blind-tribunal/SKILL.md) — Cross-Family-Bewertung des Ports.
- [decision-bar](../decision-bar/SKILL.md) — Lizenz-Blocker und Geschmacksfragen gehen an deinen Menschen; alles andere wird ausgeführt.
