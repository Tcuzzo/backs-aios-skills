# Web App Builds

Wie man eine Web-App oder Website mit sauberer Struktur und verteidigter Supply
Chain baut. Der meiste Schaden bei Web-Builds kommt über Dependencies und Grenzen
herein, nicht über deine eigene Logik — deshalb ist Hygiene das Play, kein
Nachgedanke.

## Wann dieses Play läuft

Beim Bauen oder Erweitern jeder Web-App, Website, API oder jedes ausgelieferten
Repos, das jemand anderes installieren und ausführen wird.

## Gemeinsame Aufgabe und Grenzen

Wende dieses Play im aktuellen [BACKS Build Flow](../skills/backs-build-flow/SKILL.md)-
Aufgabenpaket an. Bewahre einen Integrationsverantwortlichen, gewünschten
`task_mode`, feste Basis- und Kandidatenrevisionen, Operator-Essence und aktuelle
Belege. Verwende passende geladene Skill-Texte weiter; dieses Play ergänzt seine
Fachprüfungen, ohne die Aufgabe neu zu starten.

[bounded-loops](../skills/bounded-loops/SKILL.md) besitzt ursprüngliche Frist und
Restkontingente über Wiederholungen, Mitarbeiter, Modelle, Reviews und Übergaben
hinweg. Setze sie für ein verschachteltes Play nie zurück. Bei Erschöpfung:
**STILL-BUILDING** mit Kandidat, Belegen, offenen Gates und nächster Handlung
sichern. Nützliche autorisierte Arbeit bleibt im Restkontingent; kein fehlendes
Gate wird zum bestandenen erklärt.

## Die Kette

1. Nutze Absicht und Operator-Essence aus Build Flow vor Stack- oder Strukturwahl;
   wende die ganze Anfrage und aktuelle Korrekturen an.

2. [understanding-gates](../skills/understanding-gates/SKILL.md) — designe zuerst
   die Struktur: ein dokumentierter Entrypoint, ein explizites
   Dependency-Manifest und ein committetes Lockfile. Kein wilder Dateiwildwuchs.
3. Dependency-Hygiene (VOR jedem Install):
   - Validiere jedes referenzierte Paket gegen die Registry: Es existiert, es ist
     älter als dein Projekt, sein Publisher hat Historie. Von KI halluzinierte
     Paketnamen sind Squatting-Köder — gemessene Forschung zeigt, dass rund 43%
     der halluzinierten Namen über identische Wiederholungsläufe wiederkehren
     (Spracklen et al. (2025), USENIX Security 25), Angreifer können sie also
     vorregistrieren.
   - Pinne alles per Hash aus einem kompilierten Lockfile (z. B. `pip install
     --require-hashes`, `npm ci --ignore-scripts`); weise jeden
     Integritäts-Mismatch ab.
   - Blocke Lifecycle-Skripte zur Installationszeit standardmäßig. Ein Paket, das
     nur funktioniert, wenn ein postinstall-Skript läuft, ist ein Warnsignal.
   - Pinne jede CI-Workflow-Dependency auf einen vollen 40-Zeichen-Commit-SHA,
     niemals auf einen veränderlichen Versions-Tag.
   - Minimiere die Anzahl: Jede Dependency ist eine geprüfte Entscheidung, kein
     Reflex. Bevorzuge die Standardbibliothek oder das Plattform-Primitiv.
4. [red-first](../skills/red-first/SKILL.md) — fehlschlagende Contract-Tests für
   Routen, Loader und Validierungspfade, bevor du sie baust.
5. Baue nach der Doktrin unten. Für jede UI-Fläche fahre die Methode aus
   [design-taste](../skills/design-taste/SKILL.md) — Tokens zuerst,
   Barrierefreiheit als hartes Gate.
6. [sniper-testing](../skills/sniper-testing/SKILL.md) — nutze echte Lint-/Typ-/Tests
   des Repositories aus dem festen Kandidatengesamtdiff; melde Lücken und begründetes
   N/A. Mocke nie eigene Validierung oder Serialisierung: Eine gemockte Web-Grenze
   liefert eine App, die annimmt, was sie ablehnen sollte.

7. [clean-code-gauntlet](../skills/clean-code-gauntlet/SKILL.md) — Routen-Handler,
   Daten-Loader und Formular-/Validierungspfade bestehen vor Deployment. Mutiere
   Validierungs- und Auth-Prädikate im gemeinsamen Budget; relevante Überlebende
   blockieren Deployment. Ergänze fehlende Regressionen separat und bewahre das
   versiegelte ursprüngliche RED. Ein Grenzcheck, dessen umgedrehter Vergleich
   die Suite weiter besteht, ist eine offene Tür auf öffentlicher Oberfläche.

8. [blind-tribunal](../skills/blind-tribunal/SKILL.md) — unabhängiges Panel vor
   Deployment, alle Juroren live nach Fähigkeit und Verfügbarkeit aus der
   konfigurierten Sprossenmatrix. Erfasse und disqualifiziere die erstellende
   Ausführung; Prüfer nutzen frische autor-disjunkte Sessions. Jeder belegte Befund
   erhält separates RED und begrenzte Reparatur in dieser Aufgabe. Tage im
   Restbudget erneut; alle erforderlichen Juroren müssen bestehen. Bewahre volle
   betroffene Landungssuite und verifiziere autorisierte Lieferung an der echten App-Oberfläche.

## Die Doktrin (was der Build erfüllen muss)

- Keine Secrets im Quellcode: Lies Credentials aus der Umgebung oder einem
  Secret-Store. Ein committeter Key lässt den Build scheitern.
- Output-Handling ist kontextbewusst: parametrisierte Queries für SQL und das
  korrekte Encoding, bevor irgendein Wert Shell, Datenbank oder DOM erreicht.
  Konkateniere niemals nicht vertrauenswürdige Eingaben als String.
- Erzeuge eine maschinenlesbare SBOM — eine Software-Stückliste (z. B.
  CycloneDX) — damit der Empfänger den vollen Dependency-Baum auditieren kann.
- Halte den Build reproduzierbar: gepinnte Toolchain-Versionen, deterministischer
  Install und kein EXTERNER Netzwerkzugriff während des Testlaufs (lokale
  Loopback-Services — Datenbanken, Fixtures — sind fein und erwartet).

## Harte Gates

- Eine unvalidierte oder ungepinnte Dependency blockiert den Install.
- Ein committetes Secret blockiert den Build.
- Überlebende Mutanten in Validierungs- oder Auth-Prädikaten blockieren das
  Deploy.
- Externer Netzwerkzugriff während der Tests blockiert die Landung (Loopback ist
  fein).

## Passt gut zu

- [seam-engineering](../skills/seam-engineering/SKILL.md) — einen Grenzfehler als Klasse fixen
- [bounded-loops](../skills/bounded-loops/SKILL.md) — ausgehende Calls, die Rate-Limits respektieren

**Weight:** free-Hygiene-Disziplin durch den ganzen Build; der heavy-Einsatz ist Mutation über die Validierungs- und Auth-Prädikate plus das Tribunal — er zahlt sich auf jeder öffentlichen Oberfläche aus, wo ein einziger gekippter Vergleich eine offene Tür ist.
