# Play: Security & Delivery

Das Auslieferungs-Gate für alles, was ein Kunde oder eine andere Maschine ausführen
wird. Sicher durch Konstruktion: Der Harness erzwingt es; dem Modell wird nie
zugetraut, sich zu erinnern.

## Wann dieses Play läuft

- Ein Repo, ein Agent oder eine App steht kurz vor Auslieferung, Veröffentlichung
  oder Deployment.
- Ein Agent mit Tools berührt nicht vertrauenswürdige Inhalte — Webseiten, Issues,
  E-Mail, Eingaben.
- Du fügst etwas, das ausgeliefert wird, Dependencies oder CI hinzu.

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

1. Secret-Gate — fahre einen Secret-Scanner im Verified-Only-Modus (er prüft jeden
   Kandidaten-Credential live gegen den Provider). Ein bestätigt-lebendiger
   Credential lässt den Build scheitern. Keine Ausnahme.
2. Egress-Lockdown — verweigere ausgehenden Traffic standardmäßig; leite alles
   über einen Proxy, der nackte Hostnames per Allowlist freigibt. Kanonisiere und
   validiere den Hostname VOR dem Abgleich: Weise Null-Bytes, Prozent-Tricks und
   CRLF ab. Der Null-Byte-Bypass `evil-host\x00.trusted.com` ist real und wurde
   schon ausgeliefert.
3. Brich die tödliche Trifecta — architektiere jeden Ausführungspfad so, dass
   mindestens EINES von diesen dreien immer fehlt: Zugriff auf private Daten,
   Kontakt mit nicht vertrauenswürdigen Inhalten, externe Kommunikation.
   Prompt-Injection lässt sich nicht vollständig blocken; aber du kannst ihr das
   Stehlen unmöglich machen.
4. Taint-Tracking — nimmt die Session nicht vertrauenswürdige Inhalte auf, gilt
   sie als kontaminiert (tainted). Solange sie kontaminiert ist, gate im Harness
   per Policy jede exfiltrationsfähige Aktion (ausgehendes HTTP, E-Mail,
   PR-Erstellung) — überlasse das niemals dem Urteil des Modells.
5. Supply Chain — pinne jede Dependency per Hash und blocke Skripte zur
   Installationszeit. Pinne jede CI-Action auf einen vollen Commit-Hash, nicht auf
   einen Tag.
6. [clean-code-gauntlet](../skills/clean-code-gauntlet/SKILL.md) — Security-Code
   trägt die strengste Latte. Mutiere jeden Detektor, Parser und jedes
   Policy-Prädikat im gemeinsamen Budget; relevante Überlebende blockieren die
   Auslieferung. Ergänze fehlende Assertions in separaten Tests, ohne das
   versiegelte RED zu ändern. Ein umgedrehter Bedrohungsvergleich, den die Suite
   trotzdem besteht, IST die Schwachstelle.

7. [sniper-testing](../skills/sniper-testing/SKILL.md) — nutze echte Lint-/Typ-/Tests
   aus dem festen Kandidatengesamtdiff und melde Lücken oder begründetes N/A.
   Mocke NUR ausgehendes Netzwerk, nie Payload oder getesteten Parser: Ein gemockter
   Detektor ist in Produktion blind. Verwende aktuelle gezielte Belege vor dem
   Gauntlet weiter und bewahre vollständige betroffene Landungssuite sowie autor-disjunktes Review.

8. Sandbox vor der Auslieferung — fahre das gebaute Artefakt in einer flüchtigen
   Sandbox mit komplett geblocktem Ausgang und scharfgestelltem
   Ressourcen-Hard-Kill. Sieh zu, was es schreibt und was es aufzurufen versucht.
9. Provenienz — erzeuge eine Software-Stückliste (SBOM), plus signierte Provenienz,
   wenn du sie hast. Und prüfe dann trotzdem die Quelle: Provenienz signiert auch
   bösartige Quellen treu.

## Stehende Schutzmaßnahmen während jedes Build-Laufs

- Schreibverbot auf sensible Pfade: Shell-Startdateien, Git-Config und -Hooks,
  DNS-Konfiguration, SSH-Keys.
- Least-Privilege-Tools. Ein Bestätigungsschritt ist NUR für wirklich destruktive
  oder unumkehrbare Operationen reserviert — Datenverlust, Geldausgabe, eine
  unumkehrbare externe Aktion. Sperre niemals eine harmlose Fähigkeit hinter einer
  Rückfrage, und sperre niemals deinen Menschen.

## Harte Gates — eines reicht, und das Play ist gescheitert

- Ein bestätigt-lebendiger Credential irgendwo im Auslieferungsgegenstand oder
  seiner Historie.
- Irgendein Ausführungspfad, der alle drei Beine der Trifecta gleichzeitig hält.
- Eine ungepinnte Dependency, ein Install-Skript oder eine tag-gepinnte CI-Action.
- Ein überlebender Mutant in einem Detektor, Parser oder Policy-Prädikat.
- Das Artefakt lief vor der Auslieferung nie in einer Sandbox.

**Weight:** überwiegend free-Konstruktions-Disziplin plus light-Durchgänge für Scanner und Sandbox; der heavy-Schritt ist Mutation über jeden Detektor und jedes Policy-Prädikat — er zahlt sich bei allem aus, was ein Kunde oder eine andere Maschine ausführen wird.
