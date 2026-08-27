# Agent Builds

Wie man einen Agenten oder Service baut, der eigenständig handelt. Der Kerngedanke:
Deterministische Primitive stemmen die schwere Arbeit; das Modell denkt nur dort nach,
wo Nachdenken das Einzige ist, das funktioniert. Ein Design, das nur aus LLM besteht
und null Primitive hat, ist ungültig.

## Wann dieses Play läuft

Beim Bau jedes Agenten, Bots, Workers oder dauerhaft laufenden Services — alles, was
Tools hält, Netzwerke anspricht oder handelt, ohne dass ein Mensch jeden Schritt
beobachtet.

Der Build auf einen Blick:

```
    +--------------------------------------------+
    | 1 intent-compiler  mission + limits from   |
    |   the human's own words                    |
    +--------------------------------------------+
+-->| 2 understanding-gates  DOMAIN PRIMITIVES   |
|   |   first; LLM slot for genuine reasoning    |
|   +--------------------------------------------+
|   | 3 red-first  a failing contract test per   |<--------------------------+
|   |   typed IO boundary, committed first       |  finding -> a new red     |
|   +--------------------------------------------+  test -> fix ->           |
|   | 4 build to the doctrine -- every loop      |  re-convene               |
|   |   inside bounded-loops                     |   +---------------------+ |
|   +--------------------------------------------+   |  LORD OF THE LOOP   |-+
|   | 5 sniper-testing  mock transport only      |   | one hand drives the |
|   +--------------------------------------------+   | loop: dispatch,     |
|   | 6 clean-code-gauntlet  mutate decision     |   | judge, loop back    |
|   |   paths to zero survivors                  |   | until the gate is   |
|   +--------------------------------------------+   | green. a lane never |
|   | 7 blind-tribunal  cross-family graders     |-->| lands its own work. |
|   +--------------------------------------------+   +---------------------+
|             |
|             | every juror passes
|             v
|   +--------------------------------------------+
|   | LANDING GATE -- all green or no ship:      |
|   | no fail-open boundary, silent fallback,    |
|   | or swallowed error . zero mutation         |
|   | survivors in decision paths . cross-       |
|   | family pass; the builder never grades .    |
+---| zero primitives = invalid -> redesign      |
    +--------------------------------------------+
```

*Labels im Diagramm: „Lord of the Loop“ = der Besitzer des Loops, der die Iteration treibt, bis das Landing-Gate grün ist; „LAND“ = die Landung — die Änderung zieht erst ein, wenn jedes Gate grün ist.*

## Die Kette

1. [intent-compiler](../skills/intent-compiler/SKILL.md) — lies die Anfrage als
   Ganzes; die Mission und ihre Grenzen kommen aus den eigenen Worten des Menschen.
2. [understanding-gates](../skills/understanding-gates/SKILL.md) — benenne in der
   Design-Phase zuerst die DOMÄNEN-PRIMITIVE: Jede Kernfähigkeit ist eine
   deterministische, offline laufende Funktion, die im Fehlerfall dichtmacht
   (fail-closed). Der LLM-Slot bleibt echtem Nachdenken vorbehalten.
3. [red-first](../skills/red-first/SKILL.md) — committe für jede typisierte
   IO-Grenze einen fehlschlagenden Contract-Test, bevor du sie baust.
4. Baue nach der Doktrin unten. Halte jede Schleife innerhalb von
   [bounded-loops](../skills/bounded-loops/SKILL.md): Budgets, Checkpoints,
   Backoff und ein lauter Kill-Switch — niemals ein hämmernder Retry.
5. [sniper-testing](../skills/sniper-testing/SKILL.md) — nur der ausgehende
   Transport darf gemockt werden — niemals Routing, Prompt-Bau oder Parsing.
6. [clean-code-gauntlet](../skills/clean-code-gauntlet/SKILL.md) — die Tool-Handler
   und Entscheidungsfunktionen des Agenten bestehen das Gauntlet: Risiko-Score unter
   deiner Obergrenze, dann Mutation über die Entscheidungspfade bis auf null
   Überlebende. Verzweigungslogik, die einen umgedrehten Vergleich überlebt, war
   nie wirklich getestet.
7. [blind-tribunal](../skills/blind-tribunal/SKILL.md) — Prüfer aus einer anderen
   Modellfamilie geben den Agenten frei, bevor er ausgeliefert wird. Der Builder
   benotet nie seine eigene Arbeit.
   Jeder Befund eines Jurors wird ein neuer roter Test; berufe das Tribunal neu ein, bis jeder Juror passt.

## Die Doktrin (was der Build erfüllen muss)

- Jede IO-Grenze deklariert einen typisierten Contract (Eingaben → Ausgaben) und
  MACHT IM FEHLERFALL DICHT — bei schlechter Eingabe: Exception werfen oder
  ablehnen. Niemals fail-open, niemals einen Fehler schlucken.
- Jede Netzwerk-Schnittstelle nach draußen ist kassettentestbar: Leg ausgehende
  Calls hinter eine Record/Replay-Schicht, damit die Suite offline gegen Fixtures
  läuft.
- Aller ausgehende Traffic läuft über eine explizite Hostname-Allowlist, die
  standardmäßig verweigert. Ein unbekannter Host wirft einen Fehler; er verbindet
  sich niemals still.
- Modelliere den Agenten als typisierten Event-Stream / Zustandsautomaten mit
  deterministischen Freigabe-Zuständen (draft → review → ready → done), die der
  Agent selbst berechnet — ein Primitiv, keine menschliche Reibung. Keine Aktion
  darf ihren Zustand überspringen.
- Bestätige NUR wirklich destruktive oder unumkehrbare Aktionen (Geld ausgeben,
  löschen, ein externer Versand, der sich nicht zurückholen lässt) gegen
  committeten Zustand, bevor sie feuern. Sperre niemals eine harmlose oder rein
  lesende Aktion hinter einer Rückfrage, und sperre niemals den Menschen — siehe
  [decision-bar](../skills/decision-bar/SKILL.md).
- Persistiere dauerhaften Zustand (Ziele, Entscheidungen, Ledger) auf der Platte
  AUSSERHALB des Kontextfensters und lies ihn neu ein. Vertraue über einen langen
  Lauf niemals dem Gedächtnis im Kontext.
- Liefere ein Operating-Doc mit, das der Agent vor jeder Aufgabe lädt — die
  nächstgelegene Datei gewinnt, mit Größenlimit — und das die Regeln trägt, die
  immer gelten müssen.
- Tool-Fehler kehren als strukturierter Fehler in den Reasoning-Slot zurück, damit
  der Agent sich selbst korrigiert. Ein geschluckter Tool-Fehler ist ein Bug.
- Least Privilege: Der Agent trägt genau die Tools, die seine Mission braucht —
  keine pauschale Autorität über Dateisystem oder Netzwerk.

## Harte Gates

- Null Primitive = ungültiges Design; zurück zu Schritt 2.
- Jede fail-open-Grenze, jeder stille Fallback, jeder geschluckte Fehler blockiert
  die Auslieferung.
- Überlebende Mutanten in Entscheidungspfaden blockieren die Auslieferung.
- Die familienfremde Benotung muss bestehen; der Builder ist niemals der Prüfer.

## Passt gut zu

- [root-cause-first](../skills/root-cause-first/SKILL.md) — wenn der Agent sich danebenbenimmt
- [session-handoff](../skills/session-handoff/SKILL.md) — dauerhafter Zustand, richtig gemacht

**Weight:** überwiegend free-Disziplin plus ein light-Design-Gate; der heavy-Einsatz sind die Mutations-Läufe des Gauntlets und das familienfremde Tribunal — er zahlt sich bei jedem Agenten aus, der handeln wird, während niemand zuschaut.
