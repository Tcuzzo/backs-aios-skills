# BACKS AIOS Skills

**Lies das auf:** [English](../../README.md) · [Español](../es/README.md) · [Português (BR)](../pt-BR/README.md) · [Français](../fr/README.md) · [हिन्दी](../hi/README.md) · [简体中文](../zh-CN/README.md)

*Deutsche Ausgabe — das englische Original ist die maßgebliche Fassung: [README (Englisch)](../../README.md)*

Ein Agenten-Harness, destilliert in 27 portable Skills und 8 benannte Plays — aus
einer laufenden Agenten-Plattform gezogen und als schlichtes Markdown neu gebaut,
das jeder Agent laden kann.

## Mission

Dieses Pack existiert für die Menschen, die sich Elite-Agenten-Ergebnisse sonst
nicht leisten könnten — Coder, Designer und Macher, die keine Plattform-Ingenieure
sind. Der Harness und die Skills sind der Gleichmacher: Sie tragen die Menschen,
die sich die größten Modelle nicht leisten können, und sie machen die Modellklasse
weniger wichtig. Das ist die Wette dieses Packs: Ein kleines Modell in einem
starken Harness kann ein großes Modell schlagen, das frei herumläuft. Du musst
nicht wissen, wie der Harness gebaut wurde, um ihn zu benutzen — du sagst die
Trigger-Worte, und die Disziplin feuert.

## Philosophie

Drei Überzeugungen ziehen sich durch jede Datei in diesem Pack.

**Programmiert, nicht geprompted.** Der Agent hinter diesem Pack kommuniziert klar
und verweigert schlechte Züge, weil diese Eigenschaften als strukturelle Regeln in
den Harness eingebaut sind — Hooks, Gates, Tests — nicht in einem Prompt
vorgeschlagen. Eine Regel, die sich ein Agent merken muss, versagt genau dann,
wenn der Agent am meisten zu tun hat. Also werden die Regeln, die zählen, dort
erzwungen, wo Vergessen unmöglich ist: im Harness, nicht im Gedächtnis des
Modells.

**Maschinen denken nicht — sie destillieren.** Gib einem Modell nichts Echtes zum
Arbeiten, und es komprimiert dünne Luft — eine selbstbewusste falsche Antwort. Gib
demselben Modell den richtigen Kontext, und es liegt richtig. Was wir Reasoning
nennen, ist Destillation über Kontext: Das Modell komprimiert, was es bekommen
hat, zu einer Antwort. Reasoning ohne Recherche ist Halluzination. Genau dafür
gibt es Skills. Ein Skill ist der Kontext, MIT dem ein Agent denkt, während er
ÜBER eine Sache nachdenkt — er trägt den Agenten vom groben Verständnis hinunter
in die fachliche Tiefe, damit die Destillation etwas Echtes zu destillieren hat.

**Denke nur dort nach, wo Nachdenken das einzige Werkzeug ist, das funktioniert.**
Alles Deterministische gehört dem Harness — Gates, Tests, Hooks, Budgets. Das
Reasoning des Modells wird nur dort ausgegeben, wo es seine Kosten verdient:
Urteil, Design, Absicht lesen. Diese Trennung macht das Pack zum
Modell-Gleichmacher: Der Harness stemmt die schwere Arbeit, und die Modellklasse
hört auf, das Ergebnis zu bestimmen.

## Schnellstart

### Option 1 — Claude-Code-Plugin

    /plugin marketplace add Tcuzzo/backs-aios-skills
    /plugin install backs-aios

Tippe dann `/optimus`, um den Boden zu booten. Die Skills laden, die
Play-Kommandos werden verfügbar, und der Grounding-Hook kommt aktiviert mit
(Kill-Switch: `AIOS_GATE=off`).

### Option 2 — manuell

Lege die `skills/`-Ordner in das Skill-Verzeichnis deines Agenten und sag die
Trigger-Worte. Die Pfade pro Agent — Claude Code, jede Agent-Skills-Runtime,
OpenClaw, Hermes, ein nackter API-Loop — stehen in [INSTALL.md](INSTALL.md).

| Wenn du willst... | Sag... |
| --- | --- |
| Etwas ist kaputt | "repair loop" |
| Ein Feature bauen | `/elite-build` (Plugin) oder lies `plays/elite-build.md` (manuell) |
| Ist das gut genug zum Ausliefern? | "clean code gauntlet" |
| Prüf meine Arbeit, blind | "blind tribunal" |
| Ich bin verloren — was jetzt? | "wayfinder" |
| Die Anfrage ist vage Prosa | "prose is the spec" |

## So funktioniert es

- **Skills** sind einzelne Disziplinen. Jeder hat Trigger-Worte in seiner
  Beschreibung, nummerierte Schritte, harte Regeln, an denen der Skill scheitert,
  und Links auf die Skills, mit denen er sich paart. Eine Datei pro Skill:
  `skills/<name>/SKILL.md`.
- **Plays** sind benannte Kombinationen. Ein Play feuert Skills in einer festen
  Reihenfolge und listet die harten Gates, die eine Landung blockieren. Eine
  Datei pro Play: `plays/<name>.md`. Jedes Play-Wireframe markiert einen
  **Lord of the Loop** — den Besitzer des Loops, der die Iteration treibt, bis
  das Landing-Gate grün ist; die Rolle ist in
  [NAMING.md](NAMING.md#lord-of-the-loop) definiert.
- **Commands** sind die Slash-Einträge, die das Plugin installiert — jeder lädt
  ein Play oder einen Skill und führt ihn aus. Eine Datei pro Command in
  `commands/`.
- **Die Namenskonvention** — warum Skills Nominalphrasen sind, Commands Verben
  und der Boden Gesetz ist — steht in [NAMING.md](NAMING.md).
- **Effort-Stempel** — die einzeilige Kosten-Angabe jedes Skills (free / light /
  heavy) und die abschließende Weight-Zeile jedes Plays werden in
  [NAMING.md](NAMING.md#effort-stempel) entschlüsselt.

## Die Skills

| Skill | Was er tut |
| --- | --- |
| [absorb](skills/absorb/SKILL.md) | Eine bestehende Open-Source-Fähigkeit übernehmen und als nativen Skill neu bauen, statt ein Duplikat zu schreiben. |
| [blind-eval](skills/blind-eval/SKILL.md) | Eine Änderung nach ihrem Wert beurteilen, mit verdeckter Autorschaft, dann behalten oder zurückrollen. Nur bewiesener Fortschritt landet. |
| [blind-tribunal](skills/blind-tribunal/SKILL.md) | Blinde Juroren aus verschiedenen Modellfamilien benoten die Änderung, je eine Linse. Jeder Fund wird ein fehlschlagender Test. Schleife, bis alle bestehen. |
| [bounded-loops](skills/bounded-loops/SKILL.md) | Budget-Obergrenzen, Checkpoints und Kill-Switches auf jeder Schleife. Macht das Hämmern auf eine API strukturell unmöglich. |
| [clean-code-gauntlet](skills/clean-code-gauntlet/SKILL.md) | Eine deterministische Qualitätslatte: Sniper-Tests, der CRAP-Score (Komplexität x Coverage), begrenzte Mutation-Tests, dann eine leichte Geschmacks-Review. |
| [decision-bar](skills/decision-bar/SKILL.md) | Eine Latte für jede Entscheidung: Nur Geschmack, Vision oder destruktives Risiko erreichen den Menschen. Alles andere wird ausgeführt. |
| [design-taste](skills/design-taste/SKILL.md) | Visuelle Arbeit liefern, die designt aussieht, nicht generiert: Design-Tokens zuerst, Screenshot-Kritik, ein hartes Barrierefreiheits-Gate. |
| [fleet-ladder](skills/fleet-ladder/SKILL.md) | Die Live-Modell-Leiter auflösen: prüfen, was oben ist, in fester Reihenfolge zurückfallen, laut scheitern, wenn die Leiter erschöpft ist. |
| [gpu-dispatch](skills/gpu-dispatch/SKILL.md) | Ein Modell pro GPU, kein Überlauf in den System-RAM, die Karte durch die Schleife warm halten, am Schleifenende entladen. |
| [guided-steps](skills/guided-steps/SKILL.md) | Die Schritte skripten, die nur ein Mensch tun kann — Dashboards, Credentials, Secrets — Etappe für Etappe, jeden Wert festhaltend. |
| [human-calibration](skills/human-calibration/SKILL.md) | Ein Profil bauen, wie dieser Mensch denkt, entscheidet und angesprochen werden will — und den ganzen Build daran ausrichten. |
| [incident-closure](skills/incident-closure/SKILL.md) | „Fix it“ heißt vollständiger Abschluss — Root Cause mit Beweisen, fehlschlagender Test, grün, Live-Beweis — niemals ein Optionsmenü zurück an den Menschen. |
| [intent-compiler](skills/intent-compiler/SKILL.md) | Die natürliche Sprache eines Menschen — Dialekt, Metapher, Kurzform — als volle Spezifikation lesen und ganz ausführen. Jeder Dialekt ist eine gültige Grammatik; der Skill liest Kultur als Kontext mit eigener innerer Logik, niemals als Stereotyp. |
| [invariant-floor](skills/invariant-floor/SKILL.md) | Die nummerierten Gesetze, die jede autonome Änderung erfüllen muss, bevor sie landet. Der Boden, auf dem das ganze Pack steht. |
| [leap-protocol](skills/leap-protocol/SKILL.md) | Große Arbeit in unabhängig besitzbare Bälle zerlegen, an parallele Builder in isolierten Worktrees ausfächern, über ein einziges Schreib-Rückgrat zusammenführen. |
| [live-research](skills/live-research/SKILL.md) | Ein paralleler Recherche-Agent liest die lebende Quelle — READMEs, Doku, echten Code — damit das Denken in dem gründet, was wirklich da ist, nicht im Gedächtnis. |
| [model-fusion](skills/model-fusion/SKILL.md) | Ein Panel von Modellen entwirft parallel, ein unabhängiger Richter wählt, der Gewinner wird gegen die ursprüngliche Absicht validiert. |
| [optimus](skills/optimus/SKILL.md) | Kein Code, bis der Harness geladen ist. Ein deterministischer Hook blockiert verändernde Tools, bis der Agent die Regeln gelesen hat. |
| [human-voice](skills/human-voice/SKILL.md) | Die Latte ohne Studium: Wenn man zum Lesen einen Abschluss braucht, schreib es um. Behält die ganze Idee und entfernt die Maschinen-Marker. |
| [red-first](skills/red-first/SKILL.md) | Einen bewiesen-fehlschlagenden Test committen, bevor der Build startet. Der Builder darf ihn nicht anfassen. Ein Prüfer verifiziert, dass er sich nie bewegt hat. |
| [repair-loop](skills/repair-loop/SKILL.md) | Die volle Fix-Schleife: im Boden erden, reproduzieren, roter Test, die Klasse fixen, auf dem echten Pfad verifizieren, unabhängig benoten, landen. |
| [root-cause-first](skills/root-cause-first/SKILL.md) | Keine Fixes ohne Untersuchung. Auf Abruf reproduzieren, Grenzen instrumentieren, die Daten rückwärts bis zur Quelle verfolgen. |
| [seam-engineering](skills/seam-engineering/SKILL.md) | Die Fehlerklasse einmal am gemeinsamen Primitiv fixen, jedes Geschwister durchfegen, eine Wache landen, die den nächsten Täter fängt. |
| [session-handoff](skills/session-handoff/SKILL.md) | Eine Session in eine flache Datei kompaktieren, die ein ganz neuer Agent kalt lesen und fortsetzen kann. Secrets geschwärzt. |
| [sniper-testing](skills/sniper-testing/SKILL.md) | Nur die Tests fahren, die abdecken, was du angefasst hast. Mock-Theater töten — Tests, die bestehen, während die Fähigkeit kaputt ist. |
| [understanding-gates](skills/understanding-gates/SKILL.md) | Design, Plan, Build, Test und Ship mit Freigeben/Nacharbeiten/Ablehnen-Urteilen gaten, damit der Build weiter zur Anfrage passt. |
| [wayfinder](skills/wayfinder/SKILL.md) | Wenn verloren: eine Entscheidungskarte zum Ziel zeichnen, statt eine Frage beim Menschen zu parken. |

## Die Plays

| Play | Was es fährt |
| --- | --- |
| [elite-build](plays/elite-build.md) | Das Master-Play für jeden Build, Fix oder Uplift: Absicht lesen, Plan gaten, rot beweisen, bauen, eng testen, blind benoten, live-bewiesen landen. |
| [agent-builds](plays/agent-builds.md) | Agenten und Services bauen: Deterministische Primitive stemmen die schwere Arbeit; das Modell denkt nur dort nach, wo Nachdenken das Einzige ist, das funktioniert. |
| [web-app-builds](plays/web-app-builds.md) | Web-Apps und Websites mit sauberer Struktur und verteidigter Supply Chain — Dependency-Hygiene ist das Play, kein Nachgedanke. |
| [design-taste](plays/design-taste.md) | UI, das designt aussieht, nicht generiert: Geschmacksarbeit von Implementierung trennen, Tokens zuerst setzen, dem Agenten Augen geben, auf Barrierefreiheit gaten. |
| [grading-verification](plays/grading-verification.md) | Adversariales Benoten: Ein grünes Ergebnis ist eine Behauptung, kein Beweis. Der Prüfer greift an, und der Boden lässt sich nicht austricksen. |
| [parallel-work](plays/parallel-work.md) | Arbeit über Agenten auffächern, ohne dass sie sich zertrampeln: ein Schreib-Rückgrat, viele Leser. |
| [security-delivery](plays/security-delivery.md) | Das Auslieferungs-Gate für alles, was ein Kunde oder eine andere Maschine ausführen wird. Sicher durch Konstruktion, nicht durch Erinnerung. |
| [bughunt](plays/bughunt.md) | Eine begrenzte, parallele Bug-Jagd: die Karte zeichnen, Finder ausfächern, jeden Fund adversarial verifizieren, ganze Seams schließen. |

## Funktioniert am besten mit

Diese Skills sind die portable Schicht von **BACKS AIOS**, einer
Agenten-Plattform, gebaut von [Tcuzzo](https://github.com/Tcuzzo) — ein
graph-indiziertes, gate-erzwungenes System, in dem der Harness, nicht das Modell,
die Disziplin hält. Das volle System — sein Memory-Design, seine
Modellverhaltens-Profile, sein Code-Graph — ist nicht in diesem Pack. Die Skills
stehen trotzdem allein auf jedem Agenten: Claude Code, OpenClaw, Hermes, Codex,
Cursor oder ein nackter API-Loop. Je größer die Autonomie deines Agenten, desto
mehr zahlt sich der Boden aus.

## Credit

Komposition und Konvertierung von [Tcuzzo](https://github.com/Tcuzzo). Einige
Skills tragen Scaffold-Credits für die veröffentlichten Arbeiten, auf die sie
aufsetzen; diese sind inline vermerkt und in [NOTICE.md](../../NOTICE.md)
gesammelt (bleibt bewusst englisch — Rechtstexte und Zitate werden nicht
übersetzt). Lizenziert unter [MIT](../../LICENSE). Beiträge sind willkommen —
lass die Credits intakt.
