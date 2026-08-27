---
name: optimus
description: किसी भी agent session, job या loop की शुरुआत में लगाओ — कोई भी code लिखने से पहले। Harness-first boot: invariant floor और job के लिए ज़रूरी skills load करो, ताकि agent काम से पहले नियम पढ़े; इसमें grounding-gate hook pattern भी है जो harness load होने तक mutating tools को रोकता है। Trigger words: optimus, harness-boot, harness first, load the harness, boot the floor, grounding gate, read the floor, no code without harness, session start, boot sequence, harness पहले, पहले नियम पढ़ो, बिना harness कोई code नहीं, session की शुरुआत.
license: MIT
---

# Harness Boot

एक नियम: **harness load होने तक न कोई code, न कोई job।** Harness = pack का
invariant floor + वे skills जो इस job को cover करती हैं। हर session, हर
runtime, हर बार। क्यों: जो नियम agent को याद रखना पड़े, वह ठीक तब fail होता
है जब agent सबसे ज़्यादा busy हो — इसलिए नियम load करना पहला काम है, और एक
hook उसे सलाह की जगह structural बना देता है।

## कब चलाएँ

हर session, job, mission और loop की शुरुआत में। Context reset या handoff के
बाद फिर से। एक बार harness load करके हफ़्ते भर उसी पर चलते रहना harness load
करना नहीं है।

## Boot sequence

1. **Invariant floor load करो।** कुछ भी छूने से पहले
   [invariant-floor](../invariant-floor/SKILL.md) पढ़ो। पूरा session इसी
   floor पर खड़ा है।
2. **इस job का नक्शा load करो।** नाम लेकर बताओ: कौन-सी files, कौन-से नियम,
   और pack की कौन-सी skills इसी काम पर लागू हैं। नाम नहीं ले सकते, तो edit
   करने के लिए तैयार नहीं हो।
3. **Human profile load करो** ([human-calibration](../human-calibration/SKILL.md))
   जब job किसी इंसान की पसंद, सतह या workflow को छूता हो।
4. **Job को जिन skills की ज़रूरत है, उन्हें invoke करो — real time में, इसी
   session में।** जो skill नाम भर ली गई पर invoke नहीं हुई, वह हुई ही नहीं।
   "Skill की याद से" काम करना उसे invoke करना नहीं है।
5. सिर्फ़ उसके बाद: code लिखो, mutating commands चलाओ, या कुछ भी बदलो।

## Grounding-gate pattern

Step 4 को structural बनाओ एक deterministic **pre-tool-use hook** से — एक
छोटी script जिसे तुम्हारा agent runtime हर tool call से पहले बुलाता है:

- हर session **RED** से शुरू होता है।
- RED में read-only tools (read, grep, search, fetch) हमेशा pass होते हैं।
  Agent खुलकर ख़ुद को ground करता है।
- RED में hook **mutating tools को रोकता है** (edit, write, delete) और primary
  mutating shell verbs भी (commit, push, rm, install, service restart,
  in-place edits)।
- कोई भी harness skill invoke करना session को **GREEN कर देता है** (एक
  post-tool-use hook पकड़ता है)। फिर agent काम कर सकता है।
- **Re-arm:** हर session की शुरुआत पर state वापस RED। लंबे sessions में हर
  job या हर action पर re-arm करो, ताकि बासी GREEN कभी बिना-grounding वाले
  काम में न घुसे।

Hook के अपने design नियम:

- **Deterministic और मुफ़्त।** न कोई model call, न network, न dependencies।
  State हर session की एक छोटी file है, atomically लिखी हुई।
- **यह grounding पर मजबूर करता है, sandbox नहीं है।** सिर्फ़ primary mutating
  verbs match करो; dual-use wrappers और copy tools को छोड़ दो, ताकि grounding
  के commands कभी न फँसें।
- **Fail open, पर ज़ोर से।** Crash हुआ hook session को कभी न जाम करे — और
  चुपचाप allow भी कभी न करे। Error वहाँ छापो जहाँ इंसान देख सके।
- **Session को कभी मत फँसाओ।** Session की पहचान अनजान हो तो allow करो, एक
  ज़ोरदार warning line के साथ। जो session कभी GREEN हो ही नहीं सकता, उसे RED
  में कभी block नहीं किया जा सकता।
- **एक ही इंसान-का kill-switch** (एक env var), default ON, बंद होने पर ज़ोर
  से log करता है। Gate agents को बाँधता है, इंसान को कभी नहीं। दूसरा gate
  कभी मत जोड़ो।

Generic hook (pseudocode, ~25 lines):

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

## Hard rules (क्या इस skill को fail करता है)

- Harness load होने से पहले कोई भी mutation।
- Report में नाम ली गई कोई skill जो session में कभी invoke नहीं हुई।
- ऐसा hook जो read-only tools रोके, session को RED में फँसाए, या चुपचाप
  fail हो।
- दूसरा gate, या इंसान पर रखी कोई नई friction। Kill-switch उन्हीं का रहता है।

## इनके साथ अच्छा चलता है

- [invariant-floor](../invariant-floor/SKILL.md) — वह floor जो boot सबसे पहले load करता है।
- [human-calibration](../human-calibration/SKILL.md) — boot का profile वाला step।
- [repair-loop](../repair-loop/SKILL.md) — boot के बाद fix job जो चलाता है।
- [bounded-loops](../bounded-loops/SKILL.md) — boot से शुरू हर loop के budgets।
- [wayfinder](../wayfinder/SKILL.md) — जब boot दिखाए कि रास्ता पता नहीं।
