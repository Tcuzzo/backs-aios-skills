# Install — pack को किसी असली agent पर कसें

> **v0.7 portable installer:** Claude Code, Codex, Cursor, OpenCode और portable agents के लिए मौजूदा one-step registration: `./install.sh --target all --locale hi`। script किसी मौजूदा path को overwrite नहीं करती; PowerShell पर `./install.ps1` चलाएँ। पूरी current path matrix [canonical install guide](../../INSTALL.md) में है।

यह pack markdown के folders है। हर skill है `skills/<name>/SKILL.md`। हर play है
`plays/<name>.md`। कोई binaries नहीं, कोई server नहीं, कोई build step नहीं।
install करने का मतलब है markdown को वहाँ रखना जहाँ आपका agent skills ढूँढता है।

frontmatter जान-बूझकर open Agent Skills convention (agentskills.io) का सबसे छोटा
3-key subset है — `name`, `description`, `license`। spec सिर्फ़ `name` और
`description` माँगता है, और नियम मानने वाले runtimes अनजान keys को अनदेखा कर देते
हैं। इसलिए जहाँ भी वह convention load होता है, pack native तरीके से load हो जाता
है — और बाक़ी हर जगह सादे markdown की तरह पढ़ा जाता है।

## 1. Claude Code plugin (सुझाया हुआ तरीका)

Claude Code के अंदर दो commands:

    /plugin marketplace add Tcuzzo/backs-aios-skills
    /plugin install backs-aios

इससे सब कुछ एक साथ install हो जाता है: skills load होती हैं, slash commands मिल
जाती हैं (floor boot करने के लिए `/optimus` type करें), और grounding hook चालू
हालत में आता है — वह mutating tools को तब तक रोकता है जब तक harness load न हो
जाए। hook का kill-switch आपका है: environment में `AIOS_GATE=off` रखें और वह
ज़ोर से, खुले में बंद हो जाता है। marketplace repo के आगे बढ़ने पर updates
`/plugin` से आते हैं।

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
2. माँग से मेल खाता play चुनें — build → `plays/elite-build.md`, bug →
   `plays/bughunt.md`, grading → `plays/grading-verification.md` — और उसे जोड़
   दें।
3. user के शब्दों को हर skill की `description` के trigger words से मिलाएँ। कभी
   पूरा pack inject न करें — जो एक से तीन skills मेल खाती हैं, वही inject करें।
   pack token-lean है; उसे वैसा ही रखें।
4. हर context reset पर दोबारा inject करें। जो नियम context से गिर गया, वह loaded
   नहीं है।

## पहला session

Plugin install: `/optimus` type करें और task दे दें। Manual install:

    You:   read ~/.claude/skills/optimus/SKILL.md and boot. This session follows it.
    You:   task — checkout total is wrong when a coupon and a gift card stack.
    Agent: [boots: loads invariant-floor, picks plays/bughunt.md, names the skills it will fire]
    You:   go.
    Agent: [the play drives: reproduce, red test, fix the class, verify live, blind grade, land]
