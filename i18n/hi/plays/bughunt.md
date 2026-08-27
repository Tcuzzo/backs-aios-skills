# Play: Bughunt

एक सीमाबद्ध, parallel bug hunt। शिकार का पहले एक नक्शा बनाएँ, उस पर finders फैलाएँ,
हर finding को adversarial तरीके से जाँचें, और पूरे-के-पूरे seams बंद करें — कभी
अकेले लक्षण नहीं।

## कब चलाएँ

- कई seams के आर-पार कोई audit, sweep, या hunt — किसी एक report हुए bug के लिए
  नहीं (उसके लिए repair loop चलाएँ)।
- findings का backlog बिना भटकाव और बिना एक-दूसरे को रौंदे parallel में निपटाना हो।

पूरा hunt, एक नज़र में:

```
    +--------------------------------------------+
+-->| 1 wayfinder  chart the hunt as one map,    |
|   |   a node per seam; claim from the frontier |
|   +--------------------------------------------+
|   | 2 leap-protocol  one node = one ball:      |
|   |   goal, spec, hard file scope, ONE writer  |
|   +--------------------------------------------+
|   | 3 root-cause-first  reproduce + review     |
|   |   evidence BEFORE any code changes         |
|   +--------------------------------------------+
|   | 4 repair-loop  red-first test committed,   |<--------------------------+
|   |   sniper-testing while iterating           |  finding or survivor ->   |
|   +--------------------------------------------+   +---------------------+ |
|   | 5 blind-tribunal  a non-author grader      |-->|  LORD OF THE LOOP   |-+
|   |   attacks; jurors judge redacted work      |   | one hand drives the |
|   +--------------------------------------------+   | loop: dispatch,     |
|   | 6 seam-engineering  close the CLASS at     |   | judge, loop back    |
|   |   the shared seam, never the symptom       |   | until the gate is   |
|   +--------------------------------------------+   | green. a lane never |
|   | 7 clean-code-gauntlet  the fixed branch    |-->| lands its own work. |
|   |   must DIE under mutation, or stay open    |   +---------------------+
|   +--------------------------------------------+
|             |
|             | jurors pass + mutant dies
|             v
|   +--------------------------------------------+
|   | LANDING GATE -- leap-protocol Score gate:  |
|   | source truth . keep-or-revert . blind      |
|   | review . live proof . provenance -- each   |
|   | finding ends FIXED or REFUTED-W-EVIDENCE   |
+---| ball closed -> claim the next node         |
    +--------------------------------------------+
```

*Lord of the Loop = loop का मालिक — एक ही हाथ जो dispatch, judge और दोहराव तब तक चलाता है जब तक landing gate green न हो जाए; LAND = बदलाव का final उतरना — हर gate green होने पर merge होकर ship होना।*

## चेन

1. [wayfinder](../skills/wayfinder/SKILL.md) — शिकार का नक्शा सबसे पहले बनाएँ:
   एक map, हर seam या finding के लिए एक node। finders frontier से node
   atomically claim करते हैं; एक node बंद होते ही अगले node का सवाल लिखा जाता है।
   map से बाहर कुछ भी मत गढ़ें।
2. [leap-protocol](../skills/leap-protocol/SKILL.md) — हर node एक ball है: goal,
   spec, सख़्त file scope, सीमित rounds, tri-state नतीजा। आपस में जुड़ी balls एक
   dependency-ordered slice पर चलती हैं जिसमें writer ठीक एक ही होता है।
3. [root-cause-first](../skills/root-cause-first/SKILL.md) — code में कोई भी बदलाव
   करने से पहले bug को reproduce करें और root-cause के सबूत की समीक्षा करें।
   अंदाज़े पर कोई mutation नहीं।
4. [repair-loop](../skills/repair-loop/SKILL.md) — हर ball का भीतरी अनुशासन:
   [red-first](../skills/red-first/SKILL.md) — fix से पहले failing test commit,
   [sniper-testing](../skills/sniper-testing/SKILL.md) — iteration के दौरान सिर्फ़
   scoped runs, और landing पर छुए गए modules का एक पूरा pass।
5. [blind-tribunal](../skills/blind-tribunal/SKILL.md) — हर finding पर adversarial
   हमला होता है: एक ऐसा grader जो उसका लेखक नहीं है, refuse-by-default रुख़ से
   हमला करता है; jurors एक author-redacted envelope पर फ़ैसला देते हैं। builder
   कभी अपने ही काम का grade नहीं करता।
6. [seam-engineering](../skills/seam-engineering/SKILL.md) — साझा seam पर पूरी
   CLASS बंद करें, कभी अकेला लक्षण नहीं।
7. [clean-code-gauntlet](../skills/clean-code-gauntlet/SKILL.md) — बंद होने का
   सबूत: ठीक की गई branch को mutation के नीचे मरना ही चाहिए। जिस closure का
   mutant ज़िंदा बच जाए, वह साबित नहीं हुआ — और finding खुली रहती है।

## Ball कब बंद होती है

एक ball सिर्फ़ [leap-protocol](../skills/leap-protocol/SKILL.md) के Score gate से
होकर बंद होती है — source truth, keep-or-revert, blind review, live proof,
provenance; सबूत की कमी कभी pass में default नहीं होती। hunt की अपनी terminal
states: हर finding या तो FIXED पर खत्म होती है या REFUTED-WITH-EVIDENCE पर।

## शिकार के नियम

- अपना confidence नीचे रखें। ledger और node की attempt history से दोबारा ज़मीन
  पकड़ें, कभी अपनी याददाश्त से नहीं। relaunch का मतलब है frontier से फिर claim
  करना; हैंडऑफ़ [session-handoff](../skills/session-handoff/SKILL.md) से करें।
- चलते-चलते progress को इंसानी आवाज़ में stream करें। unknown, unknown ही रहता
  है — वह कभी "pass" नहीं बन जाता।
- जब candidate bytes, commands, tests, और verdict एक बार freeze हो गए, तो landing
  एक deterministic replay है। तय हो चुकी command को कोई model call दोबारा तय नहीं
  करती।
- box की इज़्ज़त करें: spawn से पहले resources नापें, concurrency को bound करें,
  मरी हुई lanes को reap करें, एक ही node पर दूसरी मौत के बाद LOUD रुकें, हर
  external call को throttle करें। kill-switch नए claims रोकता है — कभी बीच-उड़ान
  में चल रही mutation को नहीं।
- हर slice की बर्बादी का नाम लें और before/after नापें। efficiency की जीत तभी
  लें जब एक comparator साबित करे कि capability का शून्य नुकसान हुआ; over-bloat भी
  उतना ही defect है।
- रिपोर्ट दो शब्दों में: PROVEN या STILL-BUILDING।

## Hard gates — कोई एक भी टूटा तो play fail

- reproduce हुए root-cause सबूत की समीक्षा से पहले की गई कोई mutation।
- builder का अपनी ही finding को grade करना।
- ऐसी finding बंद करना जिसकी ठीक की गई branch पर mutant अब भी ज़िंदा है।
- hunt के बीच full-suite run — sniper से सिर्फ़ उस finding का अपना seam चलाएँ।
- closure test में mock theater: ledger "बंद" बताता है जबकि bug चुपचाप फिर खुल
  जाता है।
- कोई finding park कर दी गई — न fix हुई, न सबूत के साथ refute।

**Weight:** केंद्र में free शिकार-अनुशासन; heavy खर्च तिहरा है — leap fan-out, adversarial tribunal, और mutation से closure का सबूत — यह तब वसूल होता है जब पूरा backlog parallel में बंद होता है और हर closure mutation के नीचे साबित होता है।
