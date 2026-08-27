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

Das Auslieferungs-Gate auf einen Blick:

```
+--------------------------------------------+
| 1 secret gate  verified-only scan; one     |
|   live credential fails the build          |
+--------------------------------------------+
| 2 egress lockdown  deny by default;        |
|   canonicalize before allowlist match      |
+--------------------------------------------+
| 3 break the lethal trifecta  one leg       |
|   always missing on every path             |
+--------------------------------------------+
| 4 taint tracking  tainted session =>       |
|   policy-gate every exfil-capable action   |
+--------------------------------------------+
| 5 supply chain  hash-pin every dep, no     |
|   install scripts, SHA-pinned CI           |
+--------------------------------------------+
| 6 clean-code-gauntlet  mutate detectors,   |<--------------------------+
|   parsers, predicates to zero survivors    |  a survivor or a          |
+--------------------------------------------+  sandbox catch ->         |
| 7 sniper-testing  mock outbound network    |   +---------------------+ |
|   only, never payload or parser            |   |  LORD OF THE LOOP   |-+
+--------------------------------------------+   | one hand drives the |
| 8 sandbox before ship  outbound blocked,   |-->| loop: dispatch,     |
|   watch writes + calls, hard-kill armed    |   | judge, loop back    |
+--------------------------------------------+   | until the gate is   |
| 9 provenance  SBOM + signed provenance;    |   | green. a lane never |
|   still review the source                  |   | lands its own work. |
+--------------------------------------------+   +---------------------+
          |
          | every gate green
          v
+--------------------------------------------+
| LANDING GATE -- all green or no ship:      |
| no live credential anywhere . no path      |
| holds all three trifecta legs . deps +     |
| CI hash-pinned . zero surviving mutants    |
| . sandboxed before ship                    |
+--------------------------------------------+
```

*Labels im Diagramm: „Lord of the Loop“ = der Besitzer des Loops, der die Iteration treibt, bis das Landing-Gate grün ist; „LAND“ = die Landung — die Änderung zieht erst ein, wenn jedes Gate grün ist.*

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
   trägt die strengste Latte. Fahre Mutation-Tests über jeden Detektor, Parser und
   jedes Policy-Prädikat und treibe überlebende Mutanten auf null. Ein umgedrehter
   Vergleich in einem Bedrohungs-Check, den die Suite trotzdem besteht, IST die
   Schwachstelle.
7. [sniper-testing](../skills/sniper-testing/SKILL.md) — mocke NUR das ausgehende
   Netzwerk, niemals die Payload oder den Parser unter Test: Ein gemockter
   Detektor ist ein blinder Sensor in Produktion.
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
