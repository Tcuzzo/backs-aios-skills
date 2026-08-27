# Naming — wie dieses Pack Dinge benennt, und warum

Namen in diesem Pack tragen Last. Ein Agent wählt einen Skill, indem er die Aufgabe
gegen Name und Beschreibung abgleicht — ein Name, der das Falsche sagt, leitet
Arbeit an die falsche Disziplin. Die Konvention unten hält das Routing ehrlich.

## Die drei Arten von Namen

- **Skills sind Disziplinen als Nominalphrasen.** Ein Skill ist der Kontext, den
  ein Agent lädt, um damit zu denken — ein Körper aus Regeln, keine Aktion. Also
  wird er wie eine Disziplin benannt: `red-first`, `seam-engineering`,
  `sniper-testing`. Eine Disziplin lädt man; man „führt“ sie nicht „aus“.
- **Commands sind Imperative.** Ein Command ist eine Aktion mit Anfang und Ende,
  also ist sein Name ein Verb — oder der Name des Plays oder Skills, den er
  feuert: boot, build, hunt, grade, tribunal.
- **Der Invariant-Floor ist Gesetz.** `invariant-floor` ist der eine Skill, den
  jeder andere Skill erbt. Er ist nach dem benannt, was er ist — der Boden — weil
  jede harte Regel im Pack auf ihm steht und kein Skill eine Änderung unterhalb
  davon landen darf.

## Die mitgelieferten Commands

| Command | Feuert |
| --- | --- |
| `/agent-build` | `plays/agent-builds.md` |
| `/bughunt` | `plays/bughunt.md` |
| `/design-taste` | `plays/design-taste.md` |
| `/elite-build` | `plays/elite-build.md` |
| `/grade` | `plays/grading-verification.md` |
| `/optimus` | `skills/optimus/SKILL.md` |
| `/parallel-work` | `plays/parallel-work.md` |
| `/secure-delivery` | `plays/security-delivery.md` |
| `/tribunal` | `skills/blind-tribunal/SKILL.md` |
| `/web-build` | `plays/web-app-builds.md` |

Dass `design-taste` zugleich als Skill, Play und Command existiert, ist Absicht —
eine Disziplin, drei Eingangsformen: Der Skill ist der Kontext, das Play das
Rezept, der Command der Auslöser. Eindeutig, weil der Command das Play feuert und
das Play den Skill verlinkt.

## Wo welche Art von Information wohnt

Jede Schicht beantwortet eine andere Frage, und nichts ist doppelt:

- **Der Name sagt den Mechanismus.** `blind-tribunal` sagt dir, wie es
  funktioniert, bevor du die Datei öffnest: Juroren, blind gegenüber dem Autor.
- **Die Beschreibung trägt die Trigger-Worte.** Die Runtime gleicht deine Worte
  gegen Beschreibungen ab, also hält die Beschreibung jede Phrase, die ein Mensch
  sagen würde, wenn er den Skill braucht — auch alte Namen (siehe unten).
- **Der Body trägt die Regeln.** Schritte, harte Regeln, an denen der Skill
  scheitert, und die Skills, mit denen er sich paart. Der Body ist die Disziplin;
  Name und Beschreibung sind nur ihre Adresse.

## Umbenennungen brechen nie

Wird ein Skill umbenannt, wandert sein alter Name als Trigger-Wort in die
Beschreibung, damit jede Gewohnheit und jede Doku, die den alten Namen benutzt
hat, weiter richtig routet:

- **optimus** behält seinen Namen komplett — es ist die Boot-Marke, der eine
  Eigenname im Pack und das Kommando, das du zuerst tippst (`/optimus`).
- **„yoke“** überlebt als Trigger-Wort auf `human-calibration` — sag eines von
  beiden, und dieselbe Disziplin lädt.

Eine Umbenennung, die einen bestehenden Trigger bricht, ist eine Regression, kein
Aufräumen.

## Begründung pro Skill

| Name | Warum dieser Name |
| --- | --- |
| absorb | Die Disziplin, eine externe Fähigkeit aufzunehmen und nativ neu zu bauen, statt sie zu duplizieren. |
| blind-eval | Bewertung mit verdeckter Autorschaft — die Blindheit ist der Mechanismus. |
| blind-tribunal | Ein Panel von Juroren, blind gegenüber dem Autor, aus verschiedenen Modellfamilien. Tribunal = Panel plus Urteil. |
| bounded-loops | Die erzwungene Eigenschaft: Jede Schleife trägt eine Grenze — Budget, Checkpoint, Kill-Switch. |
| clean-code-gauntlet | Ein Gauntlet ist ein Spießrutenlauf harter Checks; sauberer Code ist, was ihn überlebt. |
| decision-bar | Eine Latte, an der jede Entscheidung gemessen wird, bevor sie den Menschen erreichen darf. |
| design-taste | Die Disziplin des Geschmacks in visueller Arbeit — mit Gates geprüft, nicht dem Gefühl überlassen. |
| fleet-ladder | Die Modell-Flotte als Fallback-Leiter aufgelöst, in fester Reihenfolge erklommen. |
| gpu-dispatch | Das Dispatch-Gesetz für GPU-Arbeit: ein Modell pro Karte, warm durch die Schleife. |
| guided-steps | Schritte, die nur ein Mensch tun kann, angeleitet Etappe für Etappe. |
| human-calibration | Den Build auf den Menschen kalibrieren, dem er dient. (Hieß „yoke“ — der alte Name überlebt als Trigger-Wort.) |
| incident-closure | Ein Vorfall wird vollständig geschlossen — von der Root Cause bis zum Live-Beweis — nie zurück an den Menschen triagiert. |
| intent-compiler | Kompiliert natürliche Sprache in eine ausführbare Direktive. Die Prosa ist die Quelle; die Direktive ist der Output. |
| invariant-floor | Der Boden aus nummerierten Gesetzen, die jede Änderung erfüllen muss. Gesetz, keine Empfehlung. |
| leap-protocol | Das Protokoll, große Arbeit über parallele Builder springen zu lassen und über ein Rückgrat zu landen. |
| live-research | Recherche gegen lebende Quellen — Doku und Code, wie sie jetzt sind — nicht Modell-Gedächtnis. |
| model-fusion | Viele Modelle entwerfen, ein unabhängiger Richter wählt — Fusion der Outputs, keine Abstimmung. |
| optimus | Die Boot-Marke, als Eigenname behalten. Sie bootet den Boden; jede Session beginnt hier. |
| human-voice | Benannt nach dem, was er erzwingt: Der Agent schreibt, wie ein Mensch spricht, und harte Ideen kommen trotzdem ganz an. |
| red-first | Der fehlschlagende (rote) Test kommt zuerst, committet, bevor der Build startet. |
| repair-loop | Die volle Fix-Schleife, benannt nach ihrer Form: erden, reproduzieren, fixen, verifizieren, landen. |
| root-cause-first | Die Reihenfolge ist die Regel: erst die Ursache, dann der Fix, immer. |
| seam-engineering | Fixes landen an der Seam — dem gemeinsamen Primitiv — nie als verstreute Punkt-Patches. |
| session-handoff | Benannt nach seinem Artefakt: eine Übergabe-Datei, mit der eine kalte Session weitermachen kann. |
| sniper-testing | Ein Schuss, ein Ziel: nur die Tests fahren, die abdecken, was du angefasst hast. |
| understanding-gates | Gates auf jeder Build-Stufe, die Verständnis prüfen, nicht nur Syntax. |
| wayfinder | Findet den Weg, wenn man verloren ist, statt eine Frage beim Menschen zu parken. |
