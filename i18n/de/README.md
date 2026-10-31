<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../../assets/reflex-seam-dark.svg">
  <img alt="Die Reflexnaht. Links besitzt eine deterministische Runtime den Zustand, die Dateien, die Regeln und die Tests. Rechts besitzt ein Urteilskern des Modells die Inferenz, die Richtlinien, die Umkehrbarkeit und die Priorität. Dazwischen verläuft eine gezackte Naht. Entscheidungssignale laufen vom Modell zur Runtime, Zustandsänderungen laufen zurück. Eine nicht erlaubte Zustandsänderung wird laut abgelehnt." src="../../assets/reflex-seam-light.svg">
</picture>

# BACKS AIOS Skills

**Lies das auf:** [English](../../README.md) · [Español](../es/README.md) · [Português (BR)](../pt-BR/README.md) · [Français](../fr/README.md) · [हिन्दी](../hi/README.md) · [简体中文](../zh-CN/README.md)

**Das Modell entscheidet. Die Runtime besitzt den Zustand, die Dateien und die Regeln —
und wenn das Modell nach einem Zustand greift, der ihm nicht gehört, scheitert das System
laut, statt zu raten.**

Diese Linie ist der **Reflex Seam**, und dieses Pack installiert sie auf einem Agenten,
den du schon benutzt. Der Kontext-Hook liefert vor der Arbeit die tatsächlichen
Texte von Optimus, Yoke und Build Flow. Er lädt fehlenden Kontext nach, ohne Tools
zu blockieren oder erworbene Erdung zu entziehen. Der Agent arbeitet mit gelesenen
Regeln und prüfbaren Belegen.

Zwei Regeln fahren mit. **Kein Mock-Theater:** Ein Test, der grün ist, während die Sache
kaputt ist, ist eine Lüge — also prüfen Tests echte Wirkungen. **Wer baut, bewertet
nicht:** Der fehlschlagende Test wird zuerst geschrieben, und etwas, das den Code nicht
geschrieben hat, muss ihn durchwinken.

*Deutsche Ausgabe — das englische Original ist die maßgebliche Fassung: [README (Englisch)](../../README.md)*

Ein Agenten-Harness mit **62 Skill-Ordnern**: **54 Nicht-Command-Skill-Ordner**
(einschließlich Kompatibilitätsaliasen), **8 Play-Einstiege** und **15 Command-Adaptern**.
Die 8 benannten Plays und ihre Methoden stammen aus
einer laufenden Agenten-Plattform gezogen und als schlichtes Markdown neu gebaut,
das jeder Agent laden kann.

Für visuelles Lernen gibt es einen [Leitfaden mit Skill-Maps und Abläufen](../../docs/FLOWCHARTS.md).

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
Play-Kommandos werden verfügbar, und der aktivierte Kontext-Hook liefert die
Skill-Texte ohne Toolblockade (Kill-Switch: `AIOS_GATE=off`).

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
- **Plays** kombinieren Methoden und Fachprüfungen innerhalb des vorhandenen
  Build-Flow-Pakets. Ein Integrationsverantwortlicher führt die begrenzte Iteration;
  alle Pflichtgates bleiben vor der Landung erhalten. Eine Datei pro Play:
  `plays/<name>.md`. Zur Rolle siehe [NAMING.md](NAMING.md#lord-of-the-loop).
- **Commands** sind die Slash-Einträge, die das Plugin installiert — jeder lädt
  ein Play oder einen Skill und führt ihn aus. Eine Datei pro Command in
  `command-adapters/`.
- **Die Namenskonvention** — warum Skills Nominalphrasen sind, Commands Verben
  und der Boden Gesetz ist — steht in [NAMING.md](NAMING.md).
- **Effort-Stempel** — die einzeilige Kosten-Angabe jedes Skills (free / light /
  heavy) und die abschließende Weight-Zeile jedes Plays werden in
  [NAMING.md](NAMING.md#effort-stempel) entschlüsselt.

## Build Flow und Operator Essence

[Build Flow](skills/backs-build-flow/SKILL.md) hält eine Aufgabe, einen
Integrationsverantwortlichen und ein gemeinsames Restbudget zusammen. Es startet
bei ausreichendem Kontext und führt begrenztes RED → GREEN mit den tatsächlichen
Lint-, Typ- und Testbefehlen des Projekts sowie dem Clean Code Gauntlet aus.
Versiegelte RED-Dateien bleiben unverändert; neue Lücken bekommen separate Tests.

[Operator Essence](skills/operator-essence/SKILL.md) liefert privaten, belegten
Operatorkontext. Fehlt die Datei oder ist sie veraltet, wird der verfügbare
Insights-Weg einmal ermittelt und versucht; ohne verfügbaren Aufruf dient
relevanter autorisierter Verlauf als ausdrücklich benannter Ersatz. Qualitative
Beobachtungen und quantitative Zählwerte behalten Quellen, Nenner, Unsicherheit
und Gegenbeispiele. Aktuelle Anfrage und Korrekturen haben Vorrang. Spezialisten
verwenden diesen Ausschnitt weiter und kehren zum selben Aufgabenverantwortlichen zurück.

Dieser Spiegel enthält alle **54 Nicht-Command-Skill-Ordner** und **8 Plays**.
Die **15 Adapter** liegen zentral in `command-adapters/`; das Installationspaket
ergänzt die acht Command-Skill-Einstiege und übernimmt kanonische Skripte und
Referenzen zusammen mit den übersetzten Skill-Texten.

## Die Skills

| Skill | Was er tut |
| --- | --- |
| [absorb](skills/absorb/SKILL.md) | Eine bestehende Open-Source-Fähigkeit übernehmen und als nativen Skill neu bauen, statt ein Duplikat zu schreiben. |
| [blind-eval](skills/blind-eval/SKILL.md) | Eine Änderung nach ihrem Wert beurteilen, mit verdeckter Autorschaft, dann behalten oder zurückrollen. Nur bewiesener Fortschritt landet. |
| [blind-tribunal](skills/blind-tribunal/SKILL.md) | Blinde Juroren prüfen in frischen autor-disjunkten Sitzungen. Belegte Befunde erhalten separate RED-Tests und Reparatur im gemeinsamen Restbudget; alle Pflichtjuroren müssen vor Landung bestehen. |
| [bounded-loops](skills/bounded-loops/SKILL.md) | Eine Missionsfrist und gemeinsame Restkontingente über Wiederholungen, Mitarbeiter, Modelle, Reviews und Übergaben tragen; bei Erschöpfung ehrlich sichern. |
| [clean-code-gauntlet](skills/clean-code-gauntlet/SKILL.md) | Gezielte Lint-/Typ-/Tests, gemessene Komplexität und Coverage, isolierte begrenzte Mutation und unabhängiges Designreview auf demselben Kandidaten. |
| [decision-bar](skills/decision-bar/SKILL.md) | Eine Latte für jede Entscheidung: Nur Geschmack, Vision oder destruktives Risiko erreichen den Menschen. Alles andere wird ausgeführt. |
| [design-taste](skills/design-taste/SKILL.md) | Visuelle Arbeit liefern, die designt aussieht, nicht generiert: Design-Tokens zuerst, Screenshot-Kritik, ein hartes Barrierefreiheits-Gate. |
| [fleet-ladder](skills/fleet-ladder/SKILL.md) | Die Live-Modell-Leiter auflösen: prüfen, was oben ist, in fester Reihenfolge zurückfallen, laut scheitern, wenn die Leiter erschöpft ist. |
| [gpu-dispatch](skills/gpu-dispatch/SKILL.md) | Ein Modell pro GPU, kein Überlauf in den System-RAM, die Karte durch die Schleife warm halten, am Schleifenende entladen. |
| [guided-steps](skills/guided-steps/SKILL.md) | Die Schritte skripten, die nur ein Mensch tun kann — Dashboards, Credentials, Secrets — Etappe für Etappe, jeden Wert festhaltend. |
| [human-calibration](skills/human-calibration/SKILL.md) | Relevante bestätigte Präferenzen und belegte Beobachtungen aus Operator Essence anwenden; aktuelle Korrekturen haben Vorrang. |
| [incident-closure](skills/incident-closure/SKILL.md) | „Fix it“ heißt vollständiger Abschluss — Root Cause mit Beweisen, fehlschlagender Test, grün, Live-Beweis — niemals ein Optionsmenü zurück an den Menschen. |
| [intent-compiler](skills/intent-compiler/SKILL.md) | Mehrdeutige aktuelle Anfragen einmal in einen belegten Handlungsvertrag übersetzen, ohne Persona, Risikotoleranz oder zusätzliche Befugnisse zu erfinden. |
| [invariant-floor](skills/invariant-floor/SKILL.md) | Die nummerierten Gesetze, die jede autonome Änderung erfüllen muss, bevor sie landet. Der Boden, auf dem das ganze Pack steht. |
| [leap-protocol](skills/leap-protocol/SKILL.md) | Große Arbeit in unabhängig besitzbare Bälle zerlegen, an parallele Builder in isolierten Worktrees ausfächern, über ein einziges Schreib-Rückgrat zusammenführen. |
| [live-research](skills/live-research/SKILL.md) | Ein paralleler Recherche-Agent liest die lebende Quelle — READMEs, Doku, echten Code — damit das Denken in dem gründet, was wirklich da ist, nicht im Gedächtnis. |
| [model-fusion](skills/model-fusion/SKILL.md) | Ein Panel von Modellen entwirft parallel, ein unabhängiger Richter wählt, der Gewinner wird gegen die ursprüngliche Absicht validiert. |
| [optimus](skills/optimus/SKILL.md) | Fundament, Optimus, Yoke und Build Flow als tatsächliche Texte laden; der deterministische Hook lädt Kontext nach und blockiert keine Tools. |
| [human-voice](skills/human-voice/SKILL.md) | Die Latte ohne Studium: Wenn man zum Lesen einen Abschluss braucht, schreib es um. Behält die ganze Idee und entfernt die Maschinen-Marker. |
| [red-first](skills/red-first/SKILL.md) | Einen bewiesen-fehlschlagenden Test committen, bevor der Build startet. Der Builder darf ihn nicht anfassen. Ein Prüfer verifiziert, dass er sich nie bewegt hat. |
| [repair-loop](skills/repair-loop/SKILL.md) | Dieselbe begrenzte Reparatur von echtem RED über Schnittstellenfix, Lint/Typ/Tests, Gauntlet und unabhängige Prüfung bis zum angeforderten Abschluss führen. |
| [repo-map](skills/repo-map/SKILL.md) | Kartiert zuerst die echte Repository-Struktur, Einstiegspunkte, Konfigurationen und Laufzeitpfade, bevor Code geändert wird. |
| [root-cause-first](skills/root-cause-first/SKILL.md) | Keine Fixes ohne Untersuchung. Auf Abruf reproduzieren, Grenzen instrumentieren, die Daten rückwärts bis zur Quelle verfolgen. |
| [seam-engineering](skills/seam-engineering/SKILL.md) | Die Fehlerklasse einmal am gemeinsamen Primitiv fixen, jedes Geschwister durchfegen, eine Wache landen, die den nächsten Täter fängt. |
| [session-handoff](skills/session-handoff/SKILL.md) | Dasselbe Aufgabenpaket mit Basis/Kandidat, RED-Siegeln, Belegen, Frist und Restbudget weitergeben; Nur-Lese-Grenzen bewahren. |
| [sniper-testing](skills/sniper-testing/SKILL.md) | Lint-, Typ-, Verhaltens- und Integrationstests aus dem vollständigen Basis-bis-Kandidat-Diff wählen; echte Wirkungen und unveränderte RED-Siegel prüfen. |
| [understanding-gates](skills/understanding-gates/SKILL.md) | Design, Plan, Build, Test und Ship mit Freigeben/Nacharbeiten/Ablehnen-Urteilen gaten, damit der Build weiter zur Anfrage passt. |
| [wayfinder](skills/wayfinder/SKILL.md) | Wenn verloren: eine Entscheidungskarte zum Ziel zeichnen, statt eine Frage beim Menschen zu parken. |
| [architecture-engineer](skills/architecture-engineer/SKILL.md) | Architekturgrenzen, Abhängigkeitsrichtungen und strukturelle Abweichungen prüfen; dauerhafte Entscheidungen als ADR festhalten. |
| [backs-build-flow](skills/backs-build-flow/SKILL.md) | Eine Anfrage mit einem Verantwortlichen, einem Aufgabenpaket und gemeinsamem Budget von ausreichendem Kontext über RED/GREEN, Lint/Typ/Tests und Gauntlet bis zum gewünschten Abschluss führen. |
| [backs-pack-sync](skills/backs-pack-sync/SKILL.md) | Private Runtime-Abdeckung mit dem öffentlichen Pack vergleichen und nur separat verfasste, geprüfte öffentliche Brücken übernehmen. |
| [backs-session-rollover](skills/backs-session-rollover/SKILL.md) | Sitzungsübergaben mit geprüftem Zustand durchführen und dieselbe Aufgabe nach Kontextwechsel fortsetzen. |
| [building-with-backs](skills/building-with-backs/SKILL.md) | Gewünschtes Repository, Checkout und Zielpfad verifizieren; autorisierte Arbeit bis zur tatsächlichen Runtime nachweisen. |
| [cam-iot-inventory](skills/cam-iot-inventory/SKILL.md) | Kamera-, IoT- und WLAN-Inventar mit stabiler Geräteidentität und ehrlich getrennten Inventar-/Bildnachweisen prüfen. |
| [co-health](skills/co-health/SKILL.md) | Watchdog-Gesundheit und Nachweise auf der Kadenz des Operators prüfen. |
| [conscientious-objector](skills/conscientious-objector/SKILL.md) | Nachvollziehbare Harness-Nutzung, Qualitätsnachweise und Abweichungen zwischen Behauptung und Code beobachten. |
| [context-compiler](skills/context-compiler/SKILL.md) | Kompatibilitätsalias von context-engineer; dasselbe belegte Aufgabenpaket und dieselbe Methode. |
| [context-engineer](skills/context-engineer/SKILL.md) | Nur fehlenden handlungsrelevanten Kontext rekonstruieren; Basis, Kandidat, Befugnisse, Operatorkontext und Restbudget weitergeben. |
| [context_engineer](skills/context_engineer/SKILL.md) | Kompatibilitätsalias von context-engineer mit byte-identischem Skill-Text. |
| [debugging-engineer](skills/debugging-engineer/SKILL.md) | Schwierige Regressionen, stille Fehler und Nebenläufigkeit mit widerlegbaren Hypothesen vor Änderungen untersuchen. |
| [design-critique](skills/design-critique/SKILL.md) | Produktoberflächen anhand Nutzeraufgabe, Belegstruktur, Bedienbarkeit, Bewegung, Barrierefreiheit und Kohärenz beurteilen. |
| [fix-shit](skills/fix-shit/SKILL.md) | Gemeldeten Defekt innerhalb derselben Aufgabe reproduzieren, versiegeln, begrenzt reparieren und echte Lieferbelege zurückgeben. |
| [fleet-dispatch](skills/fleet-dispatch/SKILL.md) | Konfigurierte Fleet-Routen ausführen und tatsächliche Provider-, Modell- und Laufbelege zurückgeben. |
| [harness-optimizer](skills/harness-optimizer/SKILL.md) | Harness-Verbesserungen mit begrenztem Baseline-/Kandidatenvergleich, Holdouts und dauerhaften Belegen messen. |
| [karpathy](skills/karpathy/SKILL.md) | Begrenzte messbare Experimente in einem Wegwerf-Clone ausführen und nur nachgewiesene Verbesserungen behalten. |
| [operator-essence](skills/operator-essence/SKILL.md) | Privaten Operatorkontext aus qualitativen und quantitativen Belegen ableiten; fehlende Insights einmal prüfen, Unsicherheit bewahren und aktuelle Anweisungen priorisieren. |
| [operator-intent-deduction](skills/operator-intent-deduction/SKILL.md) | Offene Entscheidungen aus aktueller Anfrage, Projektfakten und belegtem Operatorkontext lösen, ohne persönliche Regeln festzuschreiben. |
| [operator_intent_deduction](skills/operator_intent_deduction/SKILL.md) | Kompatibilitätsalias von operator-intent-deduction mit byte-identischem Skill-Text. |
| [osha-bot](skills/osha-bot/SKILL.md) | Watchdogs selbst auf Verfassungsabweichungen, Qualitätsmängel und versteckte Einschränkungen beobachten. |
| [rea-investigation](skills/rea-investigation/SKILL.md) | Mit vorhandener REA-Installation Erkundungs- oder Verifikationsbelege liefern und zum aktuellen Aufgabenverantwortlichen zurückkehren. |
| [reload-vsc-and-verify](skills/reload-vsc-and-verify/SKILL.md) | Installationspfade neuer Skills erkennen, autorisiertes Neuladen auslösen und tatsächliche Entdeckung prüfen. |
| [scrub-plugin-pack-literals](skills/scrub-plugin-pack-literals/SKILL.md) | Private Literale vor Veröffentlichung an der gemeinsamen Scrub-Grenze erkennen und bereinigen. |
| [truth-audit](skills/truth-audit/SKILL.md) | Schreibgeschützt tatsächliche Runtime und Defekte prüfen und eine belegte Reparaturspezifikation liefern. |
| [turn-and-burn](skills/turn-and-burn/SKILL.md) | Missionsplanung, Modellfähigkeiten, fehlende Skills und vorhandene Erkenntnisse vor Ausführung prüfen. |

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
