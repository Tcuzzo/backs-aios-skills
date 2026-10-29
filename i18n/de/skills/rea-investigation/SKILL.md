---
name: rea-investigation
description: Nutze REA zur Untersuchung ausgelieferter ausführbarer Dateien, Pakete oder beobachteten Laufzeitverhaltens, wenn dies zur Fehlerdiagnose oder Reparatur nötig ist.
license: MIT
---

# REA-Artefaktuntersuchung

Nutze die installierte REA-Engine und den zugehörigen eigenständigen Skill für ausgelieferte Binärdateien, Pakete oder angefragtes Laufzeitverhalten. Bei gewöhnlichen Quellcode-Repositories nutze direkt Quellcode und Tests. Diese Brücke installiert weder REA, Ghidra, Provider noch MCP-Server und behauptet nicht deren Verfügbarkeit.

1. Bestimme das genaue Ziel und die Frage. Lies den installierten ursprünglichen REA-Skill und relevante Referenzen im Skill-Verzeichnis des Hosts; wähle diese Brücke nicht rekursiv. Fehlt er, melde dies und untersuche mit verfügbaren Werkzeugen weiter.
2. Nutze verbundene REA-Werkzeuge, sofern verfügbar, oder die installierte REA-CLI. Für unterstützte native Binärdateien nutze einen vorhandenen kompatiblen Ghidra-Provider; melde fehlende oder nicht verfügbare Provider, statt Ergebnisse zu erfinden oder ohne Erlaubnis Abhängigkeiten zu installieren.
3. Beginne mit schreibgeschützter statischer Prüfung. Erfasse Zielidentität, Beleg-IDs, Umfang, Grenzen und offene Fragen. Statische Befunde beweisen kein Laufzeitverhalten; beobachte live nur im angefragten Umfang und innerhalb der erklärten Ausführungs- und Änderungsgrenzen des Werkzeugs.
4. Gib Befunde an root-cause-first und repair-loop weiter. Für die Übernahme einer Open-Source-Fähigkeit nutze absorb mit Lizenz- und Abhängigkeitsprüfungen. Wähle über die konfigurierte fleet-ladder nach Rolle und Fähigkeit, ohne Modell-IDs fest zu codieren. Für unabhängige Bewertung nutze bei blind-tribunal eine frische, vom Autor getrennte Ausführung mit eingefrorenem, um Autorendaten bereinigtem Paket, soweit die Host-Laufzeit dies ermöglicht.

Scaffold: REA by morluto, MIT license, https://github.com/morluto/rea.
Engine, ursprünglicher Skill und Provider werden getrennt installiert.
