---
name: optimus
description: Beim Start jeder Agent-Session, jedes Jobs, jeder Schleife — bevor irgendein Code geschrieben wird. Harness-first-Boot: lade das Invarianten-Fundament und die Skills, die der Job braucht, damit der Agent die Regeln liest, bevor er arbeitet; enthält das Grounding-Gate-Hook-Muster, das mutierende Tools blockt, bis das Harness geladen ist. Trigger words: optimus, harness-boot, harness first, load the harness, boot the floor, grounding gate, read the floor, no code without harness, session start, boot sequence, Harness laden, Fundament booten, lies erst die Regeln, kein Code ohne Harness, Session-Start.
license: MIT
---

# Harness Boot

Eine Regel: **kein Code und kein Job, bis das Harness geladen ist.** Das Harness
ist das Invarianten-Fundament des Packs plus die Skills, die diesen Job
abdecken. Jede Session, jede Runtime, jedes Mal. Warum: eine Regel, an die sich
ein Agent erinnern muss, versagt genau dann, wenn der Agent am meisten zu tun
hat — also ist das Laden der Regeln die erste Handlung, und ein Hook macht sie
strukturell statt nur gut gemeint.

## Wann laufen lassen

Am Anfang jeder Session, jedes Jobs, jeder Mission und jeder Schleife. Nochmal
nach einem Kontext-Reset oder einer Übergabe. Das Harness einmal laden und dann
eine Woche rollen ist nicht das Harness laden.

## Die Boot-Sequenz

1. **Lade das Invarianten-Fundament.** Lies
   [invariant-floor](../invariant-floor/SKILL.md), bevor du irgendwas anfasst.
   Das ist der Boden, auf dem die ganze Session steht.
2. **Lade die Karte für diesen Job.** Benenn, welche Dateien, welche Regeln und
   welche Pack-Skills genau diese Arbeit regieren. Kannst du sie nicht nennen,
   bist du nicht bereit zu editieren.
3. **Lade das Menschen-Profil**
   ([human-calibration](../human-calibration/SKILL.md)), wenn der Job den
   Geschmack, die Oberfläche oder den Workflow eines Menschen berührt.
4. **Rufe die Skills auf, die der Job braucht — in Echtzeit, in dieser
   Session.** Ein Skill, der genannt, aber nicht aufgerufen wurde, ist nicht
   passiert. „Aus der Erinnerung an einen Skill“ zu arbeiten ist kein Aufrufen.
5. Erst dann: Code schreiben, mutierende Kommandos fahren, irgendwas ändern.

## Das Grounding-Gate-Muster

Mach Schritt 4 strukturell, mit einem deterministischen **Pre-Tool-Use-Hook** —
einem kleinen Skript, das deine Agent-Runtime vor jedem Tool-Call aufruft:

- Jede Session startet **ROT**.
- Solange ROT, passieren Nur-Lese-Tools (read, grep, search, fetch) immer. Der
  Agent erdet sich frei.
- Solange ROT, **blockt der Hook mutierende Tools** (edit, write, delete) und
  primär mutierende Shell-Verben (commit, push, rm, install, Service-Restart,
  In-Place-Edits).
- Das Aufrufen irgendeines Harness-Skills **schaltet die Session GRÜN**
  (gefangen von einem Post-Tool-Use-Hook). Dann darf der Agent handeln.
- **Neu scharf stellen:** der Zustand setzt sich bei jedem Session-Start auf
  ROT zurück. Bei langen Sessions stell pro Job oder pro Aktion neu scharf,
  damit ein abgestandenes GRÜN nie in ungeerdete Arbeit hineinträgt.

Design-Regeln für den Hook selbst:

- **Deterministisch und gratis.** Kein Modell-Call, kein Netz, keine
  Abhängigkeiten. Der Zustand ist eine kleine Datei pro Session, atomar
  geschrieben.
- **Er erzwingt Erdung, keine Sandbox.** Matche nur primär mutierende Verben;
  lass Dual-Use-Wrapper und Kopier-Tools in Ruhe, damit Erdungs-Kommandos nicht
  in der Falle landen.
- **Fail open, aber laut.** Ein abgestürzter Hook darf die Session nie
  lahmlegen — und nie stumm durchwinken. Druck den Fehler dorthin, wo der
  Mensch ihn sieht.
- **Nie eine Session einsperren.** Unbekannte Session-Identität lässt durch,
  mit einer lauten Warnzeile. Eine Session, die nie GRÜN geschaltet werden
  kann, darf nie ROT geblockt werden.
- **Ein Kill-Switch, der dem Menschen gehört** (eine Env-Variable), Default AN,
  loggt laut, wenn aus. Das Gate bindet Agenten, nie den Menschen. Füg nie ein
  zweites Gate hinzu.

Generischer Hook (Pseudocode, ~25 Zeilen):

```python
HARNESS_SKILLS = {"optimus", "repair-loop", "invariant-floor"}  # your pack set
MUTATING_TOOLS = {"Edit", "Write", "Delete"}
MUTATING_SHELL = r"^\s*(sudo\s+)?(git (commit|push|reset|checkout)|rm|pip install|" \
                 r"npm install|systemctl (restart|stop)|sed .*-i)"

def handle(event, session_id, tool, args):
    if kill_switch_off():                    # human-owned env var, e.g. HARNESS_GATE=off
        return ALLOW                         # disabled loudly, never silently
    if not session_id:
        warn("no session id — allowing; the gate never traps a session")
        return ALLOW
    if event == "SessionStart":
        set_state(session_id, "RED")         # every session re-arms to RED
        return ALLOW
    if event == "PostToolUse":
        if tool == "Skill" and args.get("skill") in HARNESS_SKILLS:
            set_state(session_id, "GREEN")   # harness invoked -> agent may act
        return ALLOW
    if event == "PreToolUse":
        mutating = tool in MUTATING_TOOLS or (
            tool == "Bash" and matches(MUTATING_SHELL, args.get("command", "")))
        if not mutating or get_state(session_id) == "GREEN":
            return ALLOW                     # read-only always passes
        return BLOCK("RED: invoke a harness skill first, then act")
    return ALLOW
```

## Harte Regeln (was diesen Skill reißen lässt)

- Irgendeine Mutation, bevor das Harness geladen ist.
- Ein Skill, der im Report genannt, aber in der Session nie aufgerufen wurde.
- Ein Hook, der Nur-Lese-Tools blockt, eine Session in ROT einsperrt oder stumm
  versagt.
- Ein zweites Gate, oder irgendeine neue Reibung für den Menschen. Der
  Kill-Switch bleibt seiner.

## Passt gut zu

- [invariant-floor](../invariant-floor/SKILL.md) — das Fundament, das der Boot zuerst lädt.
- [human-calibration](../human-calibration/SKILL.md) — der Profil-Schritt des Boots.
- [repair-loop](../repair-loop/SKILL.md) — was ein Fix-Job nach dem Boot fährt.
- [bounded-loops](../bounded-loops/SKILL.md) — Budgets für jede Schleife, die der Boot startet.
- [wayfinder](../wayfinder/SKILL.md) — wenn der Boot zeigt, dass du die Route nicht kennst.
