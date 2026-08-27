# BACKS AIOS Skills

**इसे इन भाषाओं में पढ़ें:** [English](../../README.md) · [Español](../es/README.md) · [Português (BR)](../pt-BR/README.md) · [Français](../fr/README.md) · [Deutsch](../de/README.md) · [简体中文](../zh-CN/README.md)

> यह English मूल संस्करण [../../README.md](../../README.md) का हिन्दी अनुवाद है — English ही canonical है।

एक agent harness, 27 portable skills और 8 नामी plays में निचोड़ा हुआ — एक चलते हुए
agent platform से निकालकर सादे markdown में दोबारा बनाया गया, जिसे कोई भी agent
load कर सकता है।

## Mission

यह pack उन लोगों के लिए है जो elite agent नतीजों की क़ीमत से बाहर छूट जाते —
coders, designers, और builders जो platform engineers नहीं हैं। harness और skills
बराबरी लाने वाले हैं: वे उन इंसानों को उठाते हैं जो सबसे बड़े models का खर्च नहीं
उठा सकते, और model की tier की अहमियत घटा देते हैं। यही इस pack की शर्त है: मज़बूत
harness के अंदर एक छोटा model, खुला छोड़े गए बड़े model को हरा सकता है। इसे
इस्तेमाल करने के लिए यह जानना ज़रूरी नहीं कि harness कैसे बना — आप trigger words
बोलते हैं, और अनुशासन चल पड़ता है।

## Philosophy

इस pack की हर file में तीन विश्वास दौड़ते हैं।

**Programmed, prompted नहीं।** इस pack के पीछे वाला agent साफ़ बोलता है और गलत
चालें ठुकराता है, क्योंकि ये गुण harness में structural नियमों की तरह engineer
किए गए हैं — hooks, gates, tests — किसी prompt में सुझाए नहीं गए। जो नियम agent
को याद रखना पड़े, वह ठीक तब टूटता है जब agent सबसे व्यस्त होता है। इसलिए जो नियम
मायने रखते हैं, वे वहाँ लागू होते हैं जहाँ भूलना नामुमकिन है: harness में, model
की याददाश्त में नहीं।

**Machines सोचती नहीं — वे निचोड़ती हैं।** model को काम करने के लिए कुछ असली न दो,
तो वह हवा को निचोड़ता है — एक आत्मविश्वासी गलत जवाब। उसी model को सही context दो,
और वह सही कर देता है। जिसे हम reasoning कहते हैं, वह context पर distillation है:
model जो मिला उसे एक जवाब में निचोड़ता है। research के बिना reasoning, hallucination
है। skills इसीलिए हैं। एक skill वह context है जिसके साथ agent किसी चीज़ के बारे
में सोचता है — वह agent को ऊँची समझ से उतारकर विषय की गहराई तक ले जाती है, ताकि
निचोड़ने के लिए कुछ असली हो।

**Reasoning सिर्फ़ वहाँ, जहाँ reasoning ही अकेला काम करने वाला औज़ार है।** जो कुछ
deterministic है, वह harness का है — gates, tests, hooks, budgets। model की सोच
सिर्फ़ वहाँ खर्च होती है जहाँ वह अपनी क़ीमत कमाती है: judgment, design, intent
पढ़ना। यही बँटवारा pack को model-equalizing बनाता है: भारी काम harness उठाता है,
इसलिए model की tier नतीजा तय करना बंद कर देती है।

## Quick start

### तरीका 1 — Claude Code plugin

    /plugin marketplace add Tcuzzo/backs-aios-skills
    /plugin install backs-aios

फिर `/optimus` type करें और floor boot हो जाता है। skills load होती हैं, play
commands मिल जाती हैं, और grounding hook चालू हालत में ship होता है (kill-switch:
`AIOS_GATE=off`)।

### तरीका 2 — manual

`skills/` वाले folders अपने agent की skill directory में डालें और trigger words
बोलें। हर agent के paths — Claude Code, कोई भी Agent Skills runtime, OpenClaw,
Hermes, एक bare API loop — [INSTALL.md](INSTALL.md) में हैं।

| जब आपको चाहिए... | बोलें... |
| --- | --- |
| कुछ टूट गया | "repair loop" (या "ठीक करो") |
| कोई feature बनाना है | `/elite-build` (plugin) या `plays/elite-build.md` पढ़ें (manual) |
| क्या यह ship करने लायक़ है? | "clean code gauntlet" |
| मेरा काम जाँचो, blind | "blind tribunal" |
| मैं अटक गया — अब क्या? | "wayfinder" (या "रास्ता दिखाओ") |
| माँग बस ढीली-ढाली भाषा में है | "prose is the spec" |

## यह काम कैसे करता है

- **Skills** अकेले अनुशासन हैं। हर एक की description में trigger words, नंबर वाले
  steps, ऐसे hard rules जो skill को fail कर देते हैं, और उन skills के links जिनके
  साथ वह जोड़ी बनाती है। हर एक की एक file: `skills/<name>/SKILL.md`।
- **Plays** नामी combos हैं। एक play skills को तय क्रम में चलाता है और उन hard
  gates की सूची देता है जो landing रोकते हैं। हर एक की एक file: `plays/<name>.md`।
  हर play का wireframe एक **Lord of the Loop** चिह्नित करता है — loop का मालिक,
  जो iteration तब तक चलाता है जब तक landing gate green न हो जाए; इस भूमिका की
  परिभाषा [NAMING.md](NAMING.md#lord-of-the-loop) में है।
- **Commands** वे slash entries हैं जो plugin install करता है — हर एक कोई play या
  skill load करके चलाती है। हर एक की एक file `commands/` में।
- **Naming convention** — skills noun phrases क्यों हैं, commands verbs क्यों, और
  floor क़ानून क्यों — [NAMING.md](NAMING.md) में है।
- **Effort stamps** — हर skill का एक-पंक्ति लागत-दावा (free / light / heavy) और हर
  play की आख़िरी Weight पंक्ति — दोनों की व्याख्या
  [NAMING.md](NAMING.md#effort-stamps) में है।

## Skills

| Skill | क्या करती है |
| --- | --- |
| [absorb](skills/absorb/SKILL.md) | किसी मौजूदा open-source capability को अपनाकर native skill की तरह re-engineer करती है, नक़ल बनाने की जगह। |
| [blind-eval](skills/blind-eval/SKILL.md) | बदलाव को लेखक छिपाकर उसकी खूबियों पर परखती है, फिर रखती है या revert करती है। सिर्फ़ साबित हुआ uplift ही land होता है। |
| [blind-tribunal](skills/blind-tribunal/SKILL.md) | अलग-अलग model families के blind jurors बदलाव का grade करते हैं, हर एक का एक lens। हर finding एक failing test बनती है। तब तक loop, जब तक सब pass न दें। |
| [bounded-loops](skills/bounded-loops/SKILL.md) | हर loop पर budget की छत, checkpoints, और kill-switches। किसी API को hammering structurally नामुमकिन बना देती है। |
| [clean-code-gauntlet](skills/clean-code-gauntlet/SKILL.md) | एक deterministic quality bar: sniper tests, CRAP score (complexity x coverage), सीमित mutation testing, फिर एक हल्की taste review। |
| [decision-bar](skills/decision-bar/SKILL.md) | हर फ़ैसले के लिए एक bar: सिर्फ़ taste, vision, या destructive risk ही इंसान तक पहुँचते हैं। बाक़ी सब execute होता है। |
| [design-taste](skills/design-taste/SKILL.md) | ऐसा visual काम ship करती है जो designed दिखे, generated नहीं: पहले design tokens, screenshot critique, एक सख़्त accessibility gate। |
| [fleet-ladder](skills/fleet-ladder/SKILL.md) | live model ladder resolve करती है: जो चालू है उसे probe करो, क्रम से fallback लो, ladder खत्म हो तो ज़ोर से fail करो। |
| [gpu-dispatch](skills/gpu-dispatch/SKILL.md) | हर GPU पर एक model, system RAM में कोई spill नहीं, loop भर card गर्म रखो, loop के अंत पर unload। |
| [guided-steps](skills/guided-steps/SKILL.md) | वे steps script करती है जो सिर्फ़ इंसान कर सकता है — dashboards, credentials, secrets — stage दर stage, हर value को कैद करते हुए। |
| [human-calibration](skills/human-calibration/SKILL.md) | इस इंसान के सोचने, तय करने, और बात सुनने के तरीक़े की profile बनाती है, फिर पूरे build को उसी से चलाती है। |
| [incident-closure](skills/incident-closure/SKILL.md) | "ठीक करो" का मतलब पूरा बंद करना है — सबूत के साथ root cause, failing test, green, live proof — इंसान की तरफ़ options का menu कभी नहीं। |
| [intent-compiler](skills/intent-compiler/SKILL.md) | इंसान की सहज भाषा — बोली, रूपक, छोटे इशारे — को पूरे spec की तरह पढ़ती है, फिर उसे पूरा execute करती है। हर बोली एक वैध grammar है; skill संस्कृति को अपनी भीतरी logic वाले context की तरह पढ़ती है, कभी stereotype की तरह नहीं। |
| [invariant-floor](skills/invariant-floor/SKILL.md) | वे नंबर वाले क़ानून जो हर autonomous बदलाव को land होने से पहले पूरे करने हैं। वह floor जिस पर पूरा pack खड़ा है। |
| [leap-protocol](skills/leap-protocol/SKILL.md) | बड़े काम को अलग-अलग सँभाली जा सकने वाली balls में तोड़ती है, उन्हें अलग worktrees में parallel builders को बाँटती है, और एक write spine से जोड़ती है। |
| [live-research](skills/live-research/SKILL.md) | एक parallel research agent live source पढ़ता है — READMEs, docs, असली code — ताकि reasoning वहीं टिके जो सच में मौजूद है, याददाश्त में नहीं। |
| [model-fusion](skills/model-fusion/SKILL.md) | models का एक panel parallel में drafts बनाता है, एक स्वतंत्र judge चुनता है, और जीतने वाले को मूल intent के खिलाफ़ validate किया जाता है। |
| [optimus](skills/optimus/SKILL.md) | harness load हुए बिना कोई code नहीं। एक deterministic hook mutating tools को तब तक रोकता है जब तक agent नियम पढ़ न ले। |
| [human-voice](skills/human-voice/SKILL.md) | no-degree bar: अगर पढ़ने के लिए degree चाहिए, तो दोबारा लिखो। पूरा विचार बचाकर machine के सुराग़ हटाती है। |
| [red-first](skills/red-first/SKILL.md) | build शुरू होने से पहले एक साबित-failing test commit करो। builder उसे छू नहीं सकता। एक grader जाँचता है कि वह कभी हिला नहीं। |
| [repair-loop](skills/repair-loop/SKILL.md) | पूरा fix loop: floor में ज़मीन पकड़ो, reproduce करो, red test, class ठीक करो, असली path पर verify करो, independent grade, land। |
| [root-cause-first](skills/root-cause-first/SKILL.md) | बिना जाँच के कोई fix नहीं। माँगते ही reproduce करो, boundaries पर instrument लगाओ, data को पीछे source तक trace करो। |
| [seam-engineering](skills/seam-engineering/SKILL.md) | खोट की class को उसके साझा primitive पर एक बार ठीक करो, हर भाई-बंधु को sweep करो, और एक guard बिठाओ जो अगले offender को पकड़े। |
| [session-handoff](skills/session-handoff/SKILL.md) | session को एक flat file में निचोड़ती है जिसे एक बिल्कुल नया agent ठंडा पढ़कर आगे बढ़ा सके। secrets हटाकर। |
| [sniper-testing](skills/sniper-testing/SKILL.md) | सिर्फ़ वे tests चलाओ जो छुए गए हिस्से को cover करते हैं। mock theater मारो — वे tests जो pass होते हैं जबकि capability टूटी है। |
| [understanding-gates](skills/understanding-gates/SKILL.md) | Design, Plan, Build, Test, और Ship पर approve/revise/reject verdicts वाले gates, ताकि build माँग से मेल खाता रहे। |
| [wayfinder](skills/wayfinder/SKILL.md) | खो जाने पर मंज़िल तक एक decision map बनाती है, इंसान पर सवाल टाँगने की जगह। |

## Plays

| Play | क्या चलाता है |
| --- | --- |
| [elite-build](plays/elite-build.md) | किसी भी build, fix, या uplift का मास्टर play: intent पढ़ो, plan पर gate लगाओ, पहले red साबित करो, बनाओ, कसकर test करो, blind grade कराओ, live-proven land करो। |
| [agent-builds](plays/agent-builds.md) | agents और services बनाना: deterministic primitives भारी काम उठाते हैं; model सिर्फ़ वहीं सोचता है जहाँ सोच ही अकेली काम करने वाली चीज़ है। |
| [web-app-builds](plays/web-app-builds.md) | साफ़ ढाँचे और सुरक्षित supply chain वाले web apps और sites — dependency hygiene ही play है, बाद की सोच नहीं। |
| [design-taste](plays/design-taste.md) | ऐसा UI जो designed दिखे, generated नहीं: taste बनाना implementation से अलग, पहले tokens, agent को आँखें, accessibility पर gate। |
| [grading-verification](plays/grading-verification.md) | adversarial grading: green नतीजा एक दावा है, सबूत नहीं। grader हमला करता है, और floor को game नहीं किया जा सकता। |
| [parallel-work](plays/parallel-work.md) | agents के बीच काम बाँटो बिना उन्हें एक-दूसरे को रौंदने दिए: write की spine एक, readers कई। |
| [security-delivery](plays/security-delivery.md) | हर उस चीज़ का ship gate जिसे कोई customer या दूसरी machine चलाएगी। बनावट से सुरक्षित, याददाश्त से नहीं। |
| [bughunt](plays/bughunt.md) | एक सीमाबद्ध, parallel bug hunt: नक्शा बनाओ, finders फैलाओ, हर finding को adversarial तरीके से जाँचो, पूरे seams बंद करो। |

## इनके साथ सबसे अच्छा

ये skills **BACKS AIOS** की portable परत हैं — एक agent platform जिसे
[Tcuzzo](https://github.com/Tcuzzo) ने बनाया है — एक graph-indexed, gate-enforced
system जिसमें अनुशासन model नहीं, harness के पास रहता है। पूरा system — उसकी
memory का design, उसके model-behavior profiles, उसका code graph — इस pack में नहीं
है। फिर भी ये skills किसी भी agent पर अपने पैरों पर खड़ी हैं: Claude Code,
OpenClaw, Hermes, Codex, Cursor, या एक bare API loop। आपके agent की autonomy
जितनी बड़ी, floor की क़ीमत उतनी ही ज़्यादा वसूल।

## Credit

Composition और conversion: [Tcuzzo](https://github.com/Tcuzzo)। कुछ skills उस
published काम के scaffold credits रखती हैं जिस पर वे टिकी हैं; वे जगह-जगह note
हैं और [NOTICE.md](../../NOTICE.md) में इकट्ठी हैं। License: [MIT](../../LICENSE)।
Contributions का स्वागत है — credits बरक़रार रखें।
