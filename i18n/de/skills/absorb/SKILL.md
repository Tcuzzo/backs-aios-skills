---
name: "absorb"
description: "Wenn eine benötigte Fähigkeit bereits in Open Source existieren könnte oder der Operator Übernahme, Portierung, Neubau, Repository-Ingest, Vorarbeitsbewertung oder native Integration verlangt."
license: "MIT"
---

# Absorb — Übernimm Vorarbeit, erfinde sie nicht neu
**Effort:** light — ein Repo-Ingest (Metadaten-Probe + Shallow Clone) und eine unabhängige Benotung der Portierung. Beseitigt: das Neuerfinden einer Fähigkeit, die Vorarbeit schon gelöst hat — das Von-null-Duplikat, für dessen sämtliche Bugs du geradestehen müsstest.

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

Nutze aktuelles [BACKS Build Flow](../backs-build-flow/SKILL.md)-Paket und
Integrationsverantwortlichen. Ein direkter Aufruf legt das Paket einmal an; ein
verschachtelter gibt Übernahmebelege an den Aufrufer zurück. Verwende gültigen
Kontext, Operator-Essence und geladene Skill-Texte weiter.
[bounded-loops](../bounded-loops/SKILL.md) besitzt Missionsfrist und Restversuche/-runden;
Erkundung, Builds, Mutation, Reviews, Modellwechsel und Übergaben verbrauchen
dasselbe Budget. Weder neue Phase noch neuer Mitarbeiter setzen es zurück.
Beachte `task_mode`: Review oder Diagnose autorisieren keine nativen Änderungen oder Lieferung.

1. **Jage zuerst nach Vorarbeit.** Suche, bevor du baust. Ein Duplikat, das du
   erfindest, ist schlechter als ein Gerüst, das du übernimmst: Du erbst null
   Praxiserprobung und schuldest alle Bugs selbst.
2. **Erkundung über das README hinaus.** Hole Projektmetadaten (Lizenz, Aktivität,
   Sprache) per Plattform-API, klone flach in Scratch, lies Code und Tests.
   Rufe für ausgelieferte Artefakte oder gewünschtes Laufzeitverhalten, das
   Quellprüfung nicht klärt, [rea-investigation](../rea-investigation/SKILL.md)
   mit genauem Ziel und begrenzter Frage auf. REA liefert diesem Aufrufer Belege
   zurück und startet Absorb nicht neu. Halte Upstream-Identität, Beobachtungen,
   Grenzen und Unbekanntes vor der Auswahl fest. Statische Befunde beweisen kein Laufzeitverhalten.
3. **Fahre die Vertrauens-Gates.**
   - *Lizenz:* permissiv (MIT / Apache / BSD / MPL) = sicher zum Nachbauen.
     Copyleft (GPL / AGPL) = nur die Technik — bau die Idee nach, kopiere nie den
     Code. Keine Lizenz = behandeln wie „alle Rechte vorbehalten“, nur die Technik.
     Nicht-kommerzielle Bedingungen = ein Blocker; geh damit zu deinem Menschen.
   - *Shady-Scan:* nutze `rg` für Cloaking-, Spam-, Fake-Review- und Scam-Mustern.
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
6. **Native Integration.** Wende [red-first](../red-first/SKILL.md) an: Beobachte
   echten Fehler und versiegle den Vertrag vor dem minimalen Fix an der zuständigen
   Schnittstelle. Bewahre die ursprüngliche Testdatei. Begrenze echte Lint-/Typ-/
   Testbefehle des Repositories mit [sniper-testing](../sniper-testing/SKILL.md)
   anhand von `base_sha` und aktuellem `candidate_sha`, gegebenenfalls einschließlich
   eigener ausstehender Pfade. Benenne nicht verfügbare oder nicht anwendbare
   Prüfungen; installiere keinen beliebigen Prüfer und erfinde keinen Erfolg.
   Führe [clean-code-gauntlet](../clean-code-gauntlet/SKILL.md) für Qualitäts- und
   Mutationsbelege im Ablauf aus. Testlücken erhalten separate Ergänzungstests,
   niemals Änderungen am versiegelten Original. Alles bleibt im gemeinsamen Budget.
7. **Übernommene Fähigkeit verifizieren.** Prüfe das native Ergebnis gegen die
   Fähigkeitenkarte und echte Nutzeroberfläche. Verwende Erkundungsbelege weiter;
   fordere weitere REA-Beobachtung nur für einen konkreten offenen Vergleich
   innerhalb bestehender Provider- und Ausführungsgrenzen an. Wähle einen fähigen
   Prüfer über die konfigurierte Sprossenmatrix für ein frisches autor-disjunktes
   Review des genauen Gesamtkandidaten; erfasse und disqualifiziere die erstellende
   Ausführung. Der Builder bewertet nie sich selbst. Führe die vorgeschriebene
   Landungssuite aus und folge der autorisierten Lieferung des Projekts. Statische
   Upstream-Belege oder lokales GREEN allein beweisen keine native Live-Lieferung.
8. **Zitiere und dokumentiere.** Schreib den Gerüst-Credit dorthin, wo die Fähigkeit
   jetzt lebt: Autor, Projekt, Lizenz, was geliehen ist (das Gerüst) und was deins
   ist (der Neubau). Erfinde nie einen Credit. Entferne nie einen. Gib
   Fähigkeitenkarte, genauen Kandidaten, Prüfergebnisse, Attribution und offene
   Lücken an den Integrationsverantwortlichen zurück. Bei erschöpftem Budget oder
   nicht ausführbarer Pflichtprüfung: **STILL-BUILDING** mit Restarbeit und
   nächster Handlung sichern. Setze nützliche autorisierte Arbeit fort, die das
   erschöpfte Kontingent nicht nutzt. Erfinde kein **PROVEN** und lasse keine Fähigkeit still fallen.

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
- [blind-tribunal](../blind-tribunal/SKILL.md) — unabhängige, nicht-autorisierte Bewertung des Ports.
- [decision-bar](../decision-bar/SKILL.md) — Lizenz-Blocker und Geschmacksfragen gehen an deinen Menschen; alles andere wird ausgeführt.
