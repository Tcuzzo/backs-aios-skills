---
name: rea-investigation
description: "Wenn ausgelieferte Programme, Pakete oder angefragtes Laufzeitverhalten REA zur Diagnose, Fähigkeitserkundung oder Verifikation einer nativen Übernahme brauchen."
license: MIT
---

# REA-Artefaktuntersuchung

Nutze die installierte REA-Engine und den zugehörigen eigenständigen Skill für ausgelieferte Binärdateien, Pakete oder angefragtes Laufzeitverhalten. Bei gewöhnlichen Quellcode-Repositories nutze direkt Quellcode und Tests. Diese Brücke installiert weder REA, Ghidra, Provider noch MCP-Server und behauptet nicht deren Verfügbarkeit.

Nutze [BACKS Build Flow](../backs-build-flow/SKILL.md)-Paket, Integrationsverantwortlichen
und erlaubten `task_mode` des Aufrufers. Eine direkte Untersuchung legt dieses
Paket einmal an. [bounded-loops](../bounded-loops/SKILL.md) besitzt Frist und
Restkontingente; Provider-Wiederholungen, Modellwechsel und Übergaben übernehmen
sie. Diese Brücke liefert Belege, sie besitzt keine zweite Übernahme oder Reparatur.

1. Bestimme genaues Ziel, Identität/Hash, Frage und Phase: **Erkundung** des
   Upstream-Artefakts oder **Verifikation** eines bestimmten nativen Ergebnisses.
   Lies den installierten ursprünglichen Skill `reverse-engineer-anything` und
   relevante Referenzen im Skill-Verzeichnis des Hosts; wähle diese Brücke nicht
   rekursiv. Fehlt er, melde es und untersuche mit verfügbaren Werkzeugen im bestehenden Budget weiter.
2. Nutze verbundene REA-Werkzeuge, sofern verfügbar, oder die installierte REA-CLI. Für unterstützte native Binärdateien nutze einen vorhandenen kompatiblen Ghidra-Provider; melde fehlende oder nicht verfügbare Provider, statt Ergebnisse zu erfinden oder ohne Erlaubnis Abhängigkeiten zu installieren.
3. Beginne mit schreibgeschützter statischer Prüfung. Erfasse Zielidentität, Beleg-IDs, Umfang, Grenzen und offene Fragen. Statische Befunde beweisen kein Laufzeitverhalten; beobachte live nur im angefragten Umfang und innerhalb der erklärten Ausführungs- und Änderungsgrenzen des Werkzeugs.
4. Gib dem Aufrufer ein Belegpaket zurück: Zielidentität, Phase, Befehls-/Toolbelege,
   Beleg-IDs, Beobachtungen, Trennung statisch/Laufzeit, offene Fragen und
   Missionsrestbudget. Der Aufrufer besitzt den nächsten Schritt: Absorb wendet
   Lizenz-/Abhängigkeitsprüfungen und native Integration an; ein Reparaturverantwortlicher
   nutzt root-cause-first und repair-loop. Starte keinen dieser Lebenszyklen
   rekursiv aus der Brücke. Liefert die Verifikation einen Defekt, gib die
   Beobachtung für versiegeltes RED und begrenzte Reparatur-/Prüfschleife zurück;
   behaupte nicht, die Reparatur sei bereits erfolgt.
5. Wähle über die konfigurierte fleet-ladder nach Rolle und Fähigkeit, nie über
   feste Modell-IDs. Ist unabhängige Bewertung erforderlich, nutze die frische,
   autor-disjunkte Ausführung und das autorenbereinigte Paket von blind-tribunal
   entsprechend tatsächlichen Host-Fähigkeiten. Fehlender Provider oder
   erschöpftes Budget erzeugt einen **STILL-BUILDING**-Checkpoint mit nützlichen
   Beobachtungen und präziser nächster Handlung, niemals erfundenen Laufzeitbeweis.
   Freie Untersuchung bleibt im Restkontingent.

Scaffold: REA by morluto, MIT license, https://github.com/morluto/rea.
Engine, ursprünglicher Skill und Provider werden getrennt installiert.
