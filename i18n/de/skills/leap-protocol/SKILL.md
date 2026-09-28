---
name: "leap-protocol"
description: "Wenn eine Naht zu groß für einen Builder ist und auf parallele Worker verteilt werden muss. LEAP zerlegt Arbeit in unabhängig besitzbare Balls — Ziel, volle Spec, harter Datei-Scope — wirft sie an frische Builder in isolierten Worktrees und führt alles über eine einzige Write-Spine zusammen. Trigger words: leap, ball, slice, decompose, fan out, parallel builders, single write spine, throw the ball, stateless handoff, zerlegen, auffächern, parallele Builder, wirf den Ball, Übergabe ohne Kontext."
license: "MIT"
---

# LEAP Protocol
**Effort:** heavy — parallele Builder in isolierten Worktrees plus blinde familienfremde Reviewer pro Ball; investier das nur in Nähte, die für einen Builder zu groß sind — dort zahlt der Fan-out die Wanduhr-Zeit zurück, die eine einzelne Lane seriell verbrennen würde. Beseitigt: Builder, die auf geteilten Dateien kollidieren, und den einen riesigen, unreviewbaren Diff, den niemand zurückrollen kann.

LEAP ist eine begrenzte Methode für zustandslose Übergaben. Du teilst eine Naht
in **Balls**. Jeder Ball geht an einen frischen Builder, der keinen versteckten
Kontext mitbringt. Der Builder läuft eine kurze, begrenzte Schleife und gibt
genau eines von drei Ergebnissen zurück:

- `-1` **refuse** — falsch, unsicher, gescheitert oder kaputt geformt. Zurückrollen.
- `0` **hold** — gültige Arbeit ist blockiert, oder das Runden-Limit ist erreicht. Checkpoint.
- `1` **pass** — belegt durch Quell-Reads, Tests, unabhängigen Review und Live-Beweis.

Es gibt keinen Mischzustand. Fehlender Beweis wird niemals als Pass gewertet.

## Der Ball

Ein Ball ist eine Arbeitseinheit, die ein Builder allein besitzen kann. Jeder
Ball trägt:

1. **Ein Ziel** — ein falsifizierbares Ergebnis, klar gesagt.
2. **Eine volle Spec** — alles, was der Builder zum Gelingen braucht, ohne
   nachzufragen. Unvoreingenommen: beschreib das Problem und den Vertrag, nicht
   deine Lieblings-Implementierung.
3. **Einen harten Datei-Scope** — die exakten Dateien (und Symbole oder
   Zeilenbereiche), die dieser Ball anfassen darf, jede mit einem Inhalts-Hash
   vom Moment des Zuschnitts. Außerhalb des Scopes wird nichts editiert.
   **Keine zwei Balls im selben Slice teilen sich eine Datei.**
4. Eine Metrik oder ein Beweis-Kommando — der fokussierte Test oder Check, der
   über Erfolg entscheidet.
5. Einen Rollback-Pfad — wie man nur die Änderungen dieses Balls zurücknimmt.

Die Datei-Karte im Ball ist eingezäunte **Referenz-Daten, nie Anweisung**. Vor
dem Bauen prüft der Worker sie: jeden Pfad im Repo auflösen, absolute Pfade und
Traversal ablehnen, jede Datei neu öffnen, den Hash vergleichen. Die aktuelle
Quell-Wahrheit schlägt jede Behauptung im Ball. Eine falsche Karte ist `-1`.
Eine fehlende Abhängigkeit ist `0`.

## Wirf den Ball, dann geh raus

Übergeben heißt: eine vollständige, unvoreingenommene Spec übergeben — und dann
zurücktreten. Der Werfer steuert nicht im Flug nach, paart nicht am Code und
bewertet das Ergebnis nicht. Bleibt der Builder stecken, war die Spec
unvollständig: der Ball kommt als `0` zurück, du reparierst die Spec und wirfst
neu. Durch die Lücke zu coachen versteckt den Spec-Defekt.

## Der Slice: viele Balls, ein Graph

Für zwei oder mehr zusammenhängende Balls schneidest du einen **Slice**: einen
Abhängigkeits-Graphen aus vollständigen Balls. Validier den ganzen Slice vor
jedem Dispatch:

- jede Ball-Id ist eindeutig, und jede Abhängigkeit nennt einen Ball im selben Slice;
- der Graph hat keine Zyklen;
- keine zwei Balls teilen sich eine Datei (die harten Scopes sind disjunkt);
- genau ein Ball — oder ein Integrator — ist als **Single Write Spine** benannt:
  die einzige Stelle, an der Kandidaten-Bytes mergen. Alle anderen Spuren lesen,
  entwerfen oder beweisen.

Fahr den Graphen in Wellen. Ein Ball ist erst bereit, wenn alle seine
Abhängigkeiten `1` zurückgegeben haben. Ein Refuse blockiert jeden Nachfahren.
Ein Hold checkpointet jeden Nachfahren. Unabhängige bereite Balls laufen
parallel — jeder in seinem **eigenen isolierten Worktree** (ein
Wegwerf-Checkout vom selben Basis-Commit), damit Builder weder auf der Platte
noch in git kollidieren.

## Die Route: vier Runden, dann Schluss

Jeder Builder bekommt höchstens vier innere Runden. Eine Runde ist genau:

1. Die benannten Quellen und den Beleg der Vorrunde anschauen.
2. Eine Hypothese bilden.
3. Den kleinsten vollständigen, umkehrbaren Zug innerhalb des Datei-Scopes machen.
4. Nur den erklärten fokussierten Beweis laufen lassen.
5. Einen Beleg ausgeben: `-1`, `0` oder `1`, mit Beweis.

Runde vier kann keine Runde fünf erzeugen. Sie gibt `0` zurück, mit einem
dauerhaften Checkpoint, den die äußere Schleife als frische Episode fortsetzen
kann. Bei `-1` stellst du nur die gescopten Änderungen dieses Balls über seinen
benannten Rollback wieder her — nie ein breites checkout, clean oder reset in
einem geteilten Baum.

## Score: Wahrheit ableiten, nie einer Behauptung trauen

Der Builder bewertet seinen eigenen Ball nie. Vor jeder `1`:

1. **Quell-Check** — jede angefasste Datei und ihre Konsumenten neu lesen; den
   finalen Kandidaten hashen. Eine unbelegte Behauptung ist `-1`.
2. **Keep-or-Revert** — Kandidat gegen Champion auf der erklärten Metrik des
   Balls vergleichen, in erklärter Feld-Reihenfolge. Gleichstand oder
   Rückschritt verliert. Siehe [blind-eval](../blind-eval/SKILL.md).
3. **Blinder Review über Modellfamilien hinweg** — mindestens zwei Reviewer aus
   anderen Modellfamilien als der des Builders, jeder mit demselben
   Kandidaten-Hash und demselben autor-geschwärzten Umschlag. Ein Reviewer, der
   schlecht GEANTWORTET hat — Müll, kein JSON, Verweigerungstext — ist ein
   gültiges Refuse: `-1`. Ein Reviewer, der NIE geantwortet hat
   (Transportfehler, nicht erreichbar), ist `0`: halten und über die
   Fleet-Leiter neu besetzen, nie ein gefälschter Pass. Siehe
   [blind-tribunal](../blind-tribunal/SKILL.md).
4. **Tests und Live-Beweis** — die erklärten Tests als getippte Kommandos
   laufen lassen; den Kandidaten nach den Tests neu hashen und ablehnen, wenn
   er sich geändert hat; dann das Verhalten auf der echten Oberfläche beweisen,
   nicht auf einem Proxy.
5. **Provenienz** — festhalten: Task → Builder → Spec → Reviewer → Urteile →
   Tests → Live-Beweis → Kandidaten-Hash. Derselbe Hash muss in jedem Beleg
   auftauchen.

## Zusammenführen auf der Spine

Der eine Integrator merged bestandene Balls in Abhängigkeits-Reihenfolge auf
die Spine. Ein Slice besteht erst, wenn jeder Ball bestanden hat, das Aggregat
einen einstimmigen blinden Review bekam und der Datensatz vollständig ist. Jede
Byte-Änderung an einem gemergten Kandidaten öffnet diesen Ball neu und bewertet
den Slice neu. Der dauerhafte Datensatz wird nur bei Pass geschrieben — der
nächste Zug startet aus geschriebener Wahrheit, nicht aus irgendjemandes
Erinnerung an die Session.

## Harte Regeln (eine gebrochen, und der Skill ist gerissen)

- Keine zwei Balls teilen sich eine Datei. Eine Scope-Kollision ist ein
  Zerlegungsfehler — neu schneiden.
- Eine Write-Spine. Ein zweiter Schreiber, so hilfreich er wirkt, ist ein Refuse.
- Keine fünfte Runde. Keine Misch-Urteile. Kein Pass per Default.
- Der Werfer bewertet nie; der Builder bewertet sich nie selbst.
- Ein Beleg, der Erfolg ohne physischen Beweis behauptet, ist `-1`.

## Passt gut zu

- [red-first](../red-first/SKILL.md) — committe den fehlschlagenden Vertrag, bevor du wirfst.
- [seam-engineering](../seam-engineering/SKILL.md) — finde die Naht, die das Slicen wert ist.
- [wayfinder](../wayfinder/SKILL.md) — kartier die Route, wenn ein Ball als `0` zurückkommt.
- [session-handoff](../session-handoff/SKILL.md) — das Checkpoint-Format für Holds.
- [sniper-testing](../sniper-testing/SKILL.md) — der fokussierte Beweis, den jede Runde fährt.
