# Elite Build — मास्टर play

यह full play तब लें जब explicitly माँगा गया हो, या build/fix/uplift को इसके संयुक्त
design, build, quality और review stages चाहिए हों। Human goal एक बार कहता है। Scoped
change पूरे play को शुरू किए बिना BACKS Build Flow के relevant methods ले सकता है;
यह play चुनने पर नीचे के हर applicable gate को बनाए रखें।

## एक task, एक integration owner

[BACKS Build Flow](../skills/backs-build-flow/SKILL.md) task packet, `task_mode`,
operator essence और finish का owner है। Current context, actual loaded skill bodies
और evidence reuse करें; stage के inputs/candidate बदलें तभी उसे refresh करें। सभी lanes
में pinned `base_sha`, current `candidate_sha` और एक integration owner रखें। Specialist
call दूसरा lifecycle शुरू नहीं करती।

[bounded-loops](../skills/bounded-loops/SKILL.md) original deadline और remaining
mission allowances का owner है। Research, builders, lint/type/test checks, mutation,
reviews, fallback models और handoffs उन्हीं limits को खर्च करते हैं। Nested play में
reset न करें। Exhaustion पर candidate, evidence, unmet gates और next action के साथ
**STILL-BUILDING** checkpoint करें; useful authorized work exhausted allowance खर्च
किए बिना पूरा करें। Budget limit किसी gate को माफ नहीं करती।

## चेन

0. [optimus](../skills/optimus/SKILL.md) — floor और Build Flow session में एक बार
   स्थापित करें। Context में मौजूद actual bodies और उनकी source receipts reuse करें;
   receipt अकेली missing body की जगह नहीं लेती। Nested call lifecycle reboot नहीं
   करता और कभी न हुए invocation का दावा नहीं करता।
1. Build Flow के established intent और operator essence लें। पूरा request और current
   corrections पढ़ें; ship/option decision पूछने से पहले directive निकालें। Evidence
   से सुलझ सकने वाले choice को सीधे सुलझाएँ।
2. [human-calibration](../skills/human-calibration/SKILL.md) — task packet में मौजूद
   validated profile अपनाएँ। Missing applicable context load करें; human से दोबारा
   पूछताछ या हर stage में वही profile फिर न बनाएँ।
3. [turn-and-burn](../skills/turn-and-burn/SKILL.md) — mission के roster और plan-review
   requirements बनाए रखें। उपलब्ध हों तो हर model की essence (know-thyself),
   `docs/BACKS_LESSONS_LEARNED.md` और `memory/MEMORY.md` देखें। ये capability/lesson
   records operator essence से अलग हैं। Current burn evidence reuse करें; जरूरी Absorb
   work इसी mission में रहे और integration owner को result लौटाए।
4. [understanding-gates](../skills/understanding-gates/SKILL.md) — Design → Plan →
   Build → Test → Ship stage gates रखें।
   [live-research](../skills/live-research/SKILL.md) से affected path, owners,
   consumers और delivery seam देखें। Evidence कहे कि result बदल सकता है तभी additional
   dependencies trace करें; हर edit से पहले whole-system survey न दोहराएँ। Build Flow
   की context readiness पूरी हो तो next executable step शुरू करें।
5. [architecture-engineer](../skills/architecture-engineer/SKILL.md) — module boundary,
   dependency direction या shared seam छूने वाले diff पर structural review और authority
   surface classifier अपनाएँ। हर violation के पीछे local rule या concrete failure
   mode दें; durable decision के लिए ADR लें।
6. [wayfinder](../skills/wayfinder/SKILL.md) — वास्तव में unresolved route evidence से
   chart करें। Route ज्ञात हो तो दूसरा planning pass न शुरू करें।
7. [red-first](../skills/red-first/SKILL.md) — builder से पहले real failing contract
   देखें और commit करें। Seal record करें, original file byte-for-byte रखें। बाद का
   finding separate supplemental test पाए; वह original RED नहीं बदल सकता।
8. Owning seam पर smallest complete change बनाएँ। Explicit file ownership या isolated
   worktrees से independent questions/work parallel करें; एक integration owner और
   project concurrency rules बनाए रखें। [fleet-ladder](../skills/fleet-ladder/SKILL.md)
   से builders resolve करें; mission की जरूरत पर
   [model-fusion](../skills/model-fusion/SKILL.md) लें। Defect में
   [repair-loop](../skills/repair-loop/SKILL.md) inline लें और
   [seam-engineering](../skills/seam-engineering/SKILL.md) के अनुसार shared seam पर class
   बंद करें। Findings इसी task को लौटाएँ; play recursively फिर न शुरू करें।
9. [sniper-testing](../skills/sniper-testing/SKILL.md) — pinned aggregate base-to-
   candidate diff और owned pending paths से check scope निकालें। Repo की actual lint,
   type-check और focused test commands चलाएँ। Inapplicable पर reason सहित N/A, missing
   required tools को gaps लिखें; arbitrary checkers install या passes न गढ़ें। Iteration
   में scoped runs रखें।
10. [clean-code-gauntlet](../skills/clean-code-gauntlet/SKILL.md) — same candidate पर
    quality, complexity/coverage और bounded mutation inline करें। Meaningful survivor
    या finding remaining budget में supplemental RED और minimal seam fix को लौटता है।
    Valid evidence reuse करें, changed bytes के लिए stale verdict नहीं; दूसरा full
    build lifecycle शुरू न करें।
11. [blind-eval](../skills/blind-eval/SKILL.md), फिर
    [blind-tribunal](../skills/blind-tribunal/SKILL.md) — capability/availability से
    live चुने reviewers को author-redacted frozen evidence packet दें। Review fresh
    author-disjoint executions में हो; builder conversation inherit न हो। Authoring
    execution provenance में record और exclude करें। हर proved finding को same
    remaining allowance में separate RED, fix और re-review दें। सभी required jurors
    landing से पहले pass करें। Applicable हो तो tribunal का Solo rig rule मानें;
    actual configuration और runtime gaps दर्ज करें, independence कमजोर किए बिना।
12. Requested finish पूरा करें। Candidate identity फिर देखें, touched-module suites
    का full pass और required project checks करें, concurrent work बचाएँ और project की
    authorized landing procedure लें। Deployment में installed/running code तथा
    human का real surface verify करें। Service restart तभी करें जब requested delivery
    और actual procedure माँगे। Local patch/review चुपचाप release scope नहीं पाते।

## Hard gates

- Original RED fix से पहले failing देखा गया और byte-identical है; supplemental
  contracts का अपना recorded evidence और seals हैं।
- Required quality, lint/type/test और mutation gates exact candidate पर pass हों;
  justified N/A और actual gaps ईमानदारी से report हों।
- Required review fresh author-disjoint execution में हो; builder अपना काम grade
  नहीं करता और reviewer को desired conclusion नहीं देता।
- Owned seam की हर finding fixed या evidence से adjudicated हो। Open finding explicit
  checkpoint में हो और landing रोके; कभी छिपाई न जाए।
- Applicable burn, essence, lesson और plan-review requirements current evidence से
  पूरी हों। Evidence reuse करना required gate छोड़ने की अनुमति नहीं।
- Capability **PROVEN** का मतलब landed, independently graded और human के actual
  surface पर demonstrated है। अन्यथा **STILL-BUILDING** तथा exact missing proof
  [human-voice](../skills/human-voice/SKILL.md) में दें। Requested review/local patch
  पूरा होना live capability claim से अलग बताएँ।
- केवल इस task की files commit करें; दूसरे session का काम बचाएँ।

## Fleet ladder policy

Actual dispatch, configured routes, live probes, fallback और review independence के
लिए [fleet-ladder](../skills/fleet-ladder/SKILL.md) लें। उपलब्ध deployment की
`config/fleet_ladder.yaml` और `config/gpu_nodes.yaml` पढ़ें; pack resolver नहीं बनाता।
Configured rungs की frontier research-before-lift requirements और allowed web,
GitHub, Reddit तथा paper sources बचाएँ। Configured thinking floor और token-efficiency
policy मानें; model IDs hardcode या evidence truncate करके compliance न गढ़ें।

Interruption से पहले candidate, seals, evidence, deadline और remaining mission
allowances बचाने को [session-handoff](../skills/session-handoff/SKILL.md) लें।
