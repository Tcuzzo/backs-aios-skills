---
name: sniper-testing
description: "In Build- oder Reparaturschleifen oder vor Vertrauen in ein grünes Ergebnis, wenn die Verifikation den tatsächlichen Kandidaten ohne redundante Gesamtsuite-Läufe abdecken muss."
license: MIT
---

# Sniper Testing

Prüfe das geänderte Verhalten über seinen echten Verbraucher. Wähle Prüfungen
anhand des vollständigen Aufgaben-Diffs und wiederhole danach nur Prüfungen,
die von der nächsten Änderung betroffen sind. Übernimm dasselbe Missionskontingent
von [bounded-loops](../bounded-loops/SKILL.md).

## 1. Den tatsächlichen Umfang festhalten

Bewahre verifizierten `base_sha` vor Aufgabenbeginn und aktuellen committeten
`candidate_sha` im [Build Flow](../backs-build-flow/SKILL.md)-Paket. Ein sauberer
Arbeitsbaum nach RED- und Fix-Commit hat weiterhin einen Aufgaben-Diff.
`git diff HEAD` allein verliert ihn.

Nutze den mitgelieferten Nur-Lese-Helfer aus dem aufgelösten Skill-Verzeichnis:

```bash
python scripts/changed_files.py --repo <verified-repo> --base <base-sha> --candidate <candidate-sha>
```

Füge während der Iteration `--include-worktree` nur hinzu, wenn der Kandidat HEAD
ist. Der Helfer meldet committete, gestagte, ungestagte und unversionierte Pfade
getrennt und bewahrt ungewöhnliche Dateinamen. Der Gesamtumfang enthält Löschungen
und beide Seiten einer Umbenennung. Markiere fremde ausstehende Arbeit als
bewahrt; beanspruche nicht jeden ausgegebenen Pfad. Fehlende Basis oder ungültige
Revision sind zu klärende Fehler, kein leerer Umfang zum Überspringen von Prüfungen.
Der Helfer lädt keine Historie nach und verändert sie nicht.

## 2. Tatsächliche Prüfungen wählen und ausführen

Ordne geänderte Dateien sowie betroffene Aufrufer/Verbraucher Verhaltenstests zu
und lies die tatsächlichen Skripte, CI und Konfiguration des Repositories für die passenden Befehle.

| Prüfung | Umfang und Beleg |
| --- | --- |
| Lint und Formatprüfung | Geänderte unterstützte Dateien mit bestehender Konfiguration; Prüfmodus vor einer Neuformatierungsentscheidung. |
| Typprüfung oder Compiler | Betroffene Paket-/Projektgrenze; Typabhängigkeiten können ein breiteres Ziel erfordern. |
| Verhaltenstests | Tatsächlich geänderter Pfad und Regression, die bei kaputter Fähigkeit fehlschlägt. |
| Vertrags-/Integrationstests | Betroffene Verbraucher, Aliase, Paketierung, Einstellungserhalt oder Runtime-Grenzen. |
| Vorgeschriebene Landungsprüfungen | Vom Repository verlangte Suiten, sobald der Kandidat feststeht. |

Benenne jeden Befehl, abgedecktes Risiko, Revision/ausstehenden Zustand,
ausgeführtes Ergebnis und verbleibende Fehler. Ein fehlender Linter/Typprüfer ist
**nicht verfügbar** oder **nicht anwendbar**, mit Grund; erfinde keinen Erfolg.
Installiere kein neues Tool, nur weil ein Beispiel es nennt. Grünes Lint ersetzt keine Verhaltenstests.

Wähle während der Iteration das kleinste sinnvolle Ziel. Eine bestandene Prüfung
muss nicht erneut laufen, wenn getesteter Code, Eingaben und relevante Umgebung
unverändert sind. Eine konkrete offene Kopplung oder vorgeschriebene Projektprüfung
rechtfertigt breitere Tests; dokumentiere den Grund. Führe zur Landung die
geforderten Gesamtprüfungen einmal auf dem finalen Kandidaten aus. Danach geänderte
Bytes entwerten nur betroffene Belege und vorgeschriebene Commit-Prüfungen.

## 3. Tests müssen echte Defekte erkennen

Prüfe eine beobachtbare Wirkung: Ein Artefakt existiert und ist gültig, Daten
lassen sich aus einer echten lokalen Datenbank zurücklesen, der Host erhält
tatsächliche Kontextbytes oder ein UI-Element wird gerendert. Verwende lokale
Dateien, Datenbanken und Sockets statt Mocks. Ein abgerechnetes externes
Transport-Endstück darf eine deterministische Fixture ersetzen, während
Request-Aufbau, Routing, Parsing und lokaler Verbraucher echt bleiben. Behaupte
nie, die Fixture beweise einen Lauf des externen Dienstes.

Bewahre die versiegelte RED-Datei von [red-first](../red-first/SKILL.md) byteidentisch.
Lege für eine neue Lücke eine separate ergänzende Regressionsdatei an und befolge
dabei die Beleg- und Versiegelungsregeln dieses Skills. Die ursprüngliche versiegelte
Datei darf niemals abgeschwächt, umbenannt, ersetzt oder bearbeitet werden.

## Ausstieg

Gib Kandidatenumfang, ausgeführte Lint-/Typ-/Testergebnisse, echte Wirkungsbelege
und offene Prüfungen an denselben Verantwortlichen zurück.
[clean-code-gauntlet](../clean-code-gauntlet/SKILL.md) nutzt diese Belege als erste
Stufe, nicht als Anlass, unveränderte Prüfungen zu wiederholen.
