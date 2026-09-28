# Install — das Pack an einen echten Agenten schrauben

> **v0.7 portable installer:** Aktuelle Ein-Schritt-Registrierung für Claude Code, Codex, Cursor, OpenCode und portable Agenten: `./install.sh --target all --locale de`. Das Skript überschreibt nichts; PowerShell-Nutzer verwenden `./install.ps1`. Die vollständige aktuelle Pfadmatrix steht in [der kanonischen Installationsanleitung](../../INSTALL.md).

Das Pack ist Ordner voller Markdown. Jeder Skill ist `skills/<name>/SKILL.md`. Jedes
Play ist `plays/<name>.md`. Keine Binaries, kein Server, kein Build-Schritt.
Installieren heißt: das Markdown dorthin legen, wo dein Agent nach Skills sucht.

Das Frontmatter ist bewusst das minimale 3-Schlüssel-Subset — `name`,
`description`, `license` — der offenen Agent-Skills-Konvention (agentskills.io).
Die Spezifikation verlangt nur `name` und `description`, und konforme Runtimes
ignorieren Schlüssel, die sie nicht kennen. Das Pack lädt also nativ überall dort,
wo die Konvention lädt, und liest sich überall sonst als schlichtes Markdown.

## 1. Claude-Code-Plugin (empfohlen)

Zwei Kommandos in Claude Code:

    /plugin marketplace add Tcuzzo/backs-aios-skills
    /plugin install backs-aios

Das installiert alles auf einmal: Die Skills laden, die Slash-Kommandos werden
verfügbar (tippe `/optimus`, um den Boden zu booten), und der Grounding-Hook kommt
aktiviert mit — er blockiert verändernde Tools, bis der Harness geladen ist. Der
Kill-Switch des Hooks gehört dir: Setze `AIOS_GATE=off` in der Umgebung, um ihn
abzuschalten — laut, nicht heimlich. Updates fließen über `/plugin`, wenn sich das
Marketplace-Repo bewegt.

## 2. Claude Code, manuell

Claude Code entdeckt Skills außerdem in zwei Ordnern (gegen die offizielle Doku
bestätigt, 2026-08): persönlich `~/.claude/skills/<name>/SKILL.md` (jedes Projekt
auf deiner Maschine) und projektweise `.claude/skills/` (fährt mit einem Repo
mit).

Persönlich, eine Zeile:

    git clone https://github.com/Tcuzzo/backs-aios-skills.git ~/backs-aios-skills && ln -s ~/backs-aios-skills/skills/* ~/.claude/skills/

Projekt: `cp -r ~/backs-aios-skills/skills/* .claude/skills/`

Symlink, wenn Pack-Updates durchfließen sollen; Kopie, wenn du die Version pinnen
willst (oder wenn Symlinks deiner Runtime Ärger machen). Starte eine neue Session.
Ein Skill feuert, wenn die Aufgabe zu seiner `description` passt — sag die
Trigger-Worte, und der Agent lädt die Datei. Auf dem manuellen Pfad sind Plays
keine Skills: Lass sie im Clone und sag dem Agenten am Session-Start, er soll
eines lesen (`read ~/backs-aios-skills/plays/elite-build.md`), oder füge dein
Default-Play in die CLAUDE.md des Projekts ein.

## 3. Jede Agent-Skills-Runtime (die offene Konvention)

Die Konvention ist weit über Claude hinaus verbreitet — OpenAI Codex, Gemini CLI,
Cursor, VS Code und mehr (laut Spec-Ökosystem, 2026-08). Die Regeln, die hier
zählen: Die Datei heißt exakt `SKILL.md`; der Verzeichnisname entspricht dem
Frontmatter-`name`; nur `name` + `description` sind Pflicht. Dieses Pack erfüllt
alle drei. Install = `skills/*` dorthin kopieren, wo deine Runtime ihre Skills
hält (Cursor nutzt zum Beispiel `.cursor/skills/`). Wir haben nicht jeden
Runtime-Ordner verifiziert — prüfe die Doku deiner Plattform für den exakten
Pfad.

## 4. OpenClaw, Hermes, andere Agenten-Frameworks

Gegen deren aktuelle Doku bestätigt (2026-08):

- **OpenClaw** entdeckt jede `SKILL.md` unter seinen konfigurierten Skill-Wurzeln.
  Kopiere `skills/*` in den `skills/`-Ordner deines Workspace oder in den
  geteilten globalen Ordner `~/.openclaw/skills`. Die CLI `openclaw skills`
  verwaltet Installationen und Updates.
- **Hermes (Nous Research)** hält einen Ordner pro Skill in `~/.hermes/skills/`
  und lädt die SKILL.md eines Skills in den System-Prompt, wenn die Aufgabe ihn
  aktiviert. Kopiere `skills/*` dorthin.

Jedes andere Framework — das generische Muster, ganz ohne Code:

1. Mounte oder füge jede `SKILL.md` als tool-aufrufbaren Kontext ein (ein
   Dokument-Tool, ein Eintrag in der Prompt-Bibliothek, ein Retrieval-Store).
   Lass die `description`-Zeile intakt — ihre Trigger-Worte sind der
   Aufruf-Vertrag.
2. Lade ein Play (`plays/*.md`) als System-Kontext für die Session. Ein Play
   benennt die Skills, die es feuert, in fester Reihenfolge; der Agent zieht dann
   jeden Skill beim Namen.
3. Verifiziere den aktuellen Install-Mechanismus des Frameworks in dessen eigener
   Doku, bevor du dieser Datei vertraust — Mechanismen ändern sich schnell; wir
   behaupten nur, was wir oben bestätigt haben.

## 5. Nackter API-Loop (kein Framework)

Du bist der Harness. In jeder Schleife:

1. Lege `skills/invariant-floor/SKILL.md` in den System-Prompt, immer. Das ist
   der Boden, den jede Änderung erfüllen muss.
2. Wähle das Play, das zur Anfrage passt — Build → `plays/elite-build.md`, Bug →
   `plays/bughunt.md`, Benotung → `plays/grading-verification.md` — und hänge es
   an.
3. Gleiche die Worte des Nutzers gegen die Trigger-Worte jeder
   Skill-`description` ab. Injiziere niemals das ganze Pack — injiziere die ein
   bis drei Skills, die passen. Das Pack ist token-schlank; halte es so.
4. Injiziere nach jedem Kontext-Reset neu. Eine Regel, die aus dem Kontext
   gefallen ist, ist nicht geladen.

## Erste Session

Plugin-Install: Tippe `/optimus` und gib ihm die Aufgabe. Manueller Install:

    Du:    lies ~/.claude/skills/optimus/SKILL.md und boote. Diese Session folgt der Datei.
    Du:    Aufgabe — die Kassensumme stimmt nicht, wenn ein Coupon und eine Geschenkkarte zusammenkommen.
    Agent: [bootet: lädt invariant-floor, wählt plays/bughunt.md, benennt die Skills, die er feuern wird]
    Du:    los.
    Agent: [das Play fährt: reproduzieren, roter Test, die Klasse fixen, live verifizieren, blind benoten, landen]
