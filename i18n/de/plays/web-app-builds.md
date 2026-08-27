# Web App Builds

Wie man eine Web-App oder Website mit sauberer Struktur und verteidigter Supply
Chain baut. Der meiste Schaden bei Web-Builds kommt über Dependencies und Grenzen
herein, nicht über deine eigene Logik — deshalb ist Hygiene das Play, kein
Nachgedanke.

## Wann dieses Play läuft

Beim Bauen oder Erweitern jeder Web-App, Website, API oder jedes ausgelieferten
Repos, das jemand anderes installieren und ausführen wird.

## Die Kette

1. [intent-compiler](../skills/intent-compiler/SKILL.md) — lies die Anfrage als
   Ganzes, bevor du einen Stack oder eine Struktur wählst.
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
6. [sniper-testing](../skills/sniper-testing/SKILL.md) — mocke niemals deine
   eigene Validierung oder Serialisierung: Eine gemockte Web-Grenze liefert eine
   App aus, die annimmt, was sie ablehnen sollte.
7. [clean-code-gauntlet](../skills/clean-code-gauntlet/SKILL.md) —
   Routen-Handler, Daten-Loader und Formular-/Validierungspfade bestehen vor dem
   Deploy; fahre Mutation über die Validierungs- und Auth-Prädikate, bis nichts
   mehr überlebt. Ein Grenz-Check, dessen umgedrehter Vergleich die Suite immer
   noch besteht, ist eine offene Tür auf einer öffentlichen Fläche.
8. [blind-tribunal](../skills/blind-tribunal/SKILL.md) — familienfremde Benotung
   vor dem Deploy.

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
