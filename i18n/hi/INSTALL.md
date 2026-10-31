# Install — pack को किसी असली agent पर कसें

> **Portable installer:** Claude Code, Codex, Cursor, OpenCode और portable agents के लिए मौजूदा one-step registration: `./install.sh --target all --locale hi`। script किसी मौजूदा path को overwrite नहीं करती; PowerShell पर `./install.ps1` चलाएँ। पूरी current path matrix [canonical install guide](../../INSTALL.md) में है।

Pack में 62 canonical skill folders (54 non-command locale skills और 8 command
wrappers), 8 plays और 15 command adapters हैं। Skill body `skills/<name>/SKILL.md`
में और play `plays/<name>.md` में है। Installer पहले canonical folder content लेता है,
फिर locale bodies overlay करता है, ताकि references और helper scripts भी उपलब्ध हों।
केवल `i18n/hi/skills/` copy करने से helper content छूट सकता है; translated install के
लिए ऊपर का `--locale hi` रास्ता लें।

Skill frontmatter में `name`, `description` और `license` होते हैं; कुछ native skills
additional binding metadata रखते हैं। Open Agent Skills convention (agentskills.io)
`name` और `description` माँगता है। Host का current loader और canonical install guide
देखें; सभी native metadata को हर runtime पर executable binding न मानें।

## 1. Claude Code plugin (सुझाया हुआ तरीका)

Claude Code के अंदर दो commands:

    /plugin marketplace add Tcuzzo/backs-aios-skills
    /plugin install backs-aios

इससे skills, slash commands और context-loading hook install होते हैं। `/optimus`
floor और Build Flow शुरू करता है। Hook actual **Optimus + Yoke + Build Flow** bodies
host context में देता है; यह tool-blocking gate नहीं है। Session start/compaction पर
ज़रूरी bodies reload होती हैं, earned grounding वापस नहीं लिया जाता। Matched mutating
tool पर missing marker auto-load करता है। Missing/unreadable bodies visible diagnostic
dेती हैं; tools उपलब्ध रहते हैं और false receipt नहीं बनती। Context-loading receipt और
actual Skill-event evidence अलग हैं। `--rearm <session_id>` फिर load माँगता है, lock
नहीं करता। Operator का reversible kill switch `AIOS_GATE=off` है। Updates `/plugin`
से लें।

Context hook न देने वाले hosts supported loader चला सकते हैं:

```bash
node "$HOME/.local/share/backs-aios/current/hooks/aios_gate.js" --load backs-aios:optimus
```

Codex shell में active `CODEX_SESSION_ID` आखिरी argument दें। Matching Python loader
`aios_gate.py` भी उपलब्ध है। Unknown skill nonzero लौटाती है; loading का evidence न गढ़ें।

## 2. Claude Code, manual

Claude Code दो folders से भी skills खोजता है (official docs के खिलाफ़ पुष्टि की
गई, 2026-08): personal `~/.claude/skills/<name>/SKILL.md` (आपकी machine का हर
project) और project `.claude/skills/` (एक repo के साथ चलता है)।

Personal, एक line में:

    git clone https://github.com/Tcuzzo/backs-aios-skills.git ~/backs-aios-skills && ln -s ~/backs-aios-skills/skills/* ~/.claude/skills/

Project: `cp -r ~/backs-aios-skills/skills/* .claude/skills/`

symlink तब, जब आप चाहते हैं कि pack के updates अपने-आप बहें; copy तब, जब version
pin रखना हो (या symlinks आपके runtime को परेशान करें)। नया session शुरू करें।
skill तब चलती है जब task उसकी `description` से मेल खाता है — trigger words बोलें
और agent file load कर लेता है। manual रास्ते पर plays skills नहीं हैं: उन्हें
clone में ही रखें और session की शुरुआत में agent से एक पढ़वाएँ
(`read ~/backs-aios-skills/plays/elite-build.md`), या अपना default play project
की CLAUDE.md में paste कर दें।

## 3. कोई भी Agent Skills runtime (open convention)

यह convention Claude से बहुत आगे तक अपनाया जा चुका है — OpenAI Codex, Gemini CLI,
Cursor, VS Code और भी (spec ecosystem के हिसाब से, 2026-08)। यहाँ जो नियम मायने
रखते हैं: file का नाम ठीक `SKILL.md` हो; directory का नाम frontmatter के `name`
के बराबर हो; सिर्फ़ `name` + `description` ज़रूरी हैं। यह pack तीनों पूरे करता
है। install = `skills/*` को वहाँ copy करें जहाँ आपका runtime skills रखता है
(जैसे Cursor `.cursor/skills/` इस्तेमाल करता है)। हमने हर runtime का folder
जाँचा नहीं है — सटीक path के लिए अपने platform के docs देखें।

## 4. OpenClaw, Hermes, दूसरे agent frameworks

उनके मौजूदा docs के खिलाफ़ पुष्टि की गई (2026-08):

- **OpenClaw** अपनी configure की हुई skill roots के नीचे कोई भी `SKILL.md` खोज
  लेता है। `skills/*` को अपने workspace के `skills/` folder में copy करें, या
  साझा global `~/.openclaw/skills` folder में। `openclaw skills` CLI installs और
  updates सँभालती है।
- **Hermes (Nous Research)** `~/.hermes/skills/` में हर skill का एक folder रखता
  है, और task के activate होने पर skill की SKILL.md को system prompt में load
  करता है। `skills/*` वहाँ copy करें।

कोई भी दूसरा framework — generic pattern, कोई code नहीं चाहिए:

1. हर `SKILL.md` को tool से बुलाए जा सकने वाले context की तरह mount या paste
   करें (कोई document tool, prompt library की entry, कोई retrieval store)।
   `description` वाली line जस-की-तस रखें — उसके trigger words ही invocation का
   contract हैं।
2. session के लिए एक play (`plays/*.md`) system context की तरह load करें। play
   उन skills के नाम, क्रम में, बताता है जिन्हें वह चलाता है; agent फिर हर skill
   को नाम से खींच लेता है।
3. इस file पर भरोसा करने से पहले framework का मौजूदा install तरीका उसके अपने
   docs में जाँचें — तरीक़े तेज़ी से बदलते हैं; हम सिर्फ़ वही कह रहे हैं जो हमने
   ऊपर खुद पक्का किया।

## 5. Bare API loop (कोई framework नहीं)

harness आप खुद हैं। हर loop पर:

1. `skills/invariant-floor/SKILL.md` को system prompt में रखें, हमेशा। वही floor
   है जिसे हर बदलाव को पार करना है।
2. `skills/backs-build-flow/SKILL.md` से एक task owner, mode, target, acceptance
   check और shared budget रखें। जरूरत या explicit request पर संबंधित play जोड़ें;
   हर छोटा build पूरा elite-build play शुरू नहीं करता।
3. user के शब्दों को हर skill की `description` के trigger words से मिलाएँ। कभी
   पूरा pack inject न करें — जो एक से तीन skills मेल खाती हैं, वही inject करें।
   pack token-lean है; उसे वैसा ही रखें।
4. Context reset पर अगली action की missing actual bodies reload करें। Current task
   packet, RED seal, base/candidate और remaining budget बचाएँ; नई context नई mission नहीं।

## पहला session

Plugin install: `/optimus` type करें और task दे दें। Manual install:

    You:   read ~/.claude/skills/optimus/SKILL.md and boot. This session follows it.
    You:   task — checkout total is wrong when a coupon and a gift card stack.
    Agent: [loads the actual floor and Build Flow, verifies the target, sets one bounded task packet]
    Agent: [reproduces, seals RED, fixes the class, runs scoped lint/types/tests and gauntlet, then completes authorized review and delivery]
