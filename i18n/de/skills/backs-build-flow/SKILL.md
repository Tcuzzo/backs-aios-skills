---
name: backs-build-flow
description: "Beim Bauen, Reparieren, Prüfen, Fortsetzen oder Liefern von Arbeit, wenn Kontext, Skills und Verifikation koordiniert werden müssen, ohne den Arbeitsfluss zu verlieren."
license: MIT
---

# BACKS Build Flow

Ein Integrationsverantwortlicher führt die Anfrage vom Kontext bis zur verifizierten
Lieferung. Spezialisten geben ihm Belege zurück; sie starten den Ablauf nicht neu.
Für eine einfache Antwort ohne Build oder Untersuchung genügen die relevanten Schritte.

## Genug Kontext herstellen, um zu handeln

1. Bewahre Ziel, Einschränkungen, bestehende Autorisierung und gewünschtes Ergebnis
   des Nutzers. Wähle den Modus: **Build/Fix**, **Nur-Lese-Review**,
   **Untersuchung** oder **Fortsetzen/Liefern**. Ein Review autorisiert weder
   Änderungen noch Installation oder Deployment.
2. Verwende ein aktuelles Aufgabenpaket weiter. Andernfalls verifiziert
   [context-engineer](../context-engineer/SKILL.md) Ziel, maßgebliche Anweisungen,
   betroffenen Aufrufer-/Verbraucherpfad, vorhandene Arbeit und Abnahmeprüfung.
   [building-with-backs](../building-with-backs/SKILL.md) klärt Checkout und
   Promotion. Halte den `base_sha` vor der Änderung fest; aktualisiere
   `candidate_sha`, sobald Arbeit committet wird.
3. Wende [operator-essence](../operator-essence/SKILL.md) für den aktuellen
   Operator an: Lade den relevanten Kontextausschnitt oder führe dessen
   Insights-Initialisierung bei fehlendem Profil einmal aus. Qualitative
   Beobachtungen und quantitative Belege steuern Kommunikation und Verifikation;
   sie erteilen keine Befugnisse und schreiben keine Persona fest. Kennzeichne
   dünne Belege als vorläufig und setze nützliche autorisierte Arbeit fort.
   Verwende [intent-compiler](../intent-compiler/SKILL.md) nur bei mehrdeutiger
   Absicht; [operator-intent-deduction](../operator-intent-deduction/SKILL.md)
   entscheidet, ob eine wesentliche offene Wahl wirklich den Operator braucht.
4. **Beginne mit der Ausführung, sobald du Ziel, nächste konkrete Handlung,
   Einschränkungen und eine beobachtbare Abnahmeprüfung benennen kannst.**
   Weitere Lektüre muss eine benannte Frage klären, die diese Handlung ändern
   könnte. Kartiere nicht wiederholt das ganze Repository.

## Skills einmal zuordnen, mit Ergebnis und Ausstieg

Lade die tatsächlich relevanten Skill-Texte; Name oder Beleg allein sind keine
Anwendung. Nutze noch vorhandene, aktuelle Texte und Belege weiter. Lade nach
Kompaktierung nur nach, was die nächste Handlung braucht. Benenne für jeden
Spezialisten Zweck, erwarteten Beleg und Ausstiegskriterium; lies tiefere Referenzen
bei Bedarf. Ein aktuelles Aufgabenpaket führt Verantwortung, Zustand und nächste
Handlung ([Paket- und Übergabeformat](references/task-packet.md)). Keine doppelten Journale.

Bei Übernahmen verantwortet [absorb](../absorb/SKILL.md) die Fähigkeitskarte und
native Integration. [rea-investigation](../rea-investigation/SKILL.md) liefert bei
Bedarf Entdeckungs- oder Verifikationsbelege und kehrt zum Aufrufer zurück, ohne
Absorb rekursiv neu zu starten. Normale Quelltextarbeit verwendet direkt Code und Tests.

## Die begrenzte RED → GREEN-Schleife ausführen

Binde vor Wiederholungen [bounded-loops](../bounded-loops/SKILL.md) ein: eine
`mission_id`, Frist, Versuchs-/Rundenkontingent und verbleibendes Ressourcenbudget.
Unteragenten, Modellwechsel, Reparaturbefunde und Review-Runden verbrauchen dasselbe Kontingent.

1. **RED:** [red-first](../red-first/SKILL.md) weist vor dem Fix ein tatsächlich
   scheiterndes Verhalten nach. Bewahre die versiegelte Datei und Baseline-Identität.
   Verwende bei Review oder Recherche den Belegvertrag, ohne Änderungen zu erfinden.
2. **Build:** Implementiere die kleinste vollständige Änderung an der zuständigen
   Schnittstelle; aktualisiere betroffene Verbraucher und Kompatibilitätsflächen.
   Bewahre fremde Arbeit.
3. **Lint und Tests:** [sniper-testing](../sniper-testing/SKILL.md) leitet den Umfang
   von `base_sha` bis zum aktuellen Kandidaten einschließlich relevanter ausstehender
   Arbeit ab. Führe die geltenden Lint-, Formatprüf-, Typprüf- und Verhaltenstests
   des Repositories aus. Dokumentiere genaue Befehle, Revision, Ergebnisse sowie
   nicht verfügbare oder nicht anwendbare Prüfungen. Ein sauberer Arbeitsbaum
   löscht den bereits committeten Umfang nicht.
4. **Qualität:** [clean-code-gauntlet](../clean-code-gauntlet/SKILL.md) verwendet
   denselben Umfang und dasselbe Budget für gemessene Qualität, begrenzte isolierte
   Mutation und unabhängiges Review. Ergänze separate Tests für neue Lücken,
   ohne den versiegelten RED-Test umzuschreiben.
5. **Auf Belege reagieren:** Behebe einen belegten Befund und wiederhole nur
   betroffene Prüfungen. Identische wiederholte Fehler erfordern eine geänderte
   Hypothese oder Taktik. Sichere bei erschöpften Grenzen offene Arbeit; setze
   niemals das Budget zurück und senke niemals die Prüfanforderungen.

Führe die vorgeschriebenen gemeinsamen Landungsprüfungen des Repositories aus,
sobald der Kandidat feststeht. Melde die tatsächlichen Fähigkeiten dieses Hosts;
erfinde keine Tools, Tests oder Reviews.

## Das angeforderte Ergebnis abschließen

Führe autorisierte Paketierung, Commit, Veröffentlichung und Verifikation aus,
wenn sie Teil des Auftrags sind. Bereite bei tatsächlich erforderlicher externer
Freigabe zuerst das vollständige prüfbare Ergebnis vor. Informiere den Nutzer über
Befunde, aktuelle Handlung, Belege und den Ort der laufenden Arbeit; beachte seine Kadenz.

Unterscheide **angeforderte Aufgabe geliefert** vom Fähigkeitsstatus **PROVEN**
des Invarianten-Fundaments. Ein fertiger lokaler Patch oder Nur-Lese-Review bedeutet
kein Live-Deployment. Fehlende oder gescheiterte Pflichtprüfungen bleiben sichtbar:
Sichere **STILL-BUILDING** mit genauem Blocker, Restkontingent und nächster Handlung.
Gib im Nur-Lese-Modus das Paket in der Antwort oder einem bereits autorisierten
externen Aufgabeneintrag zurück; lege nicht stillschweigend ein Repository-Journal
oder eine Essence-Datei an.
