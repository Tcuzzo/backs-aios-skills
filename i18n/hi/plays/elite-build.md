# Elite Build — मास्टर play

किसी भी "X बनाओ", "X ठीक करो", या "X uplift करो" वाली माँग का default play। इंसान
लक्ष्य एक बार बताता है; यह play पूरा माहौल खुद जोड़ लेता है, ताकि baseline कभी
दोबारा समझानी न पड़े। intent पढ़ो, इंसान को load करो, plan पर gate लगाओ, पहले red
साबित करो, बनाओ, कसकर test करो, नापो, blind grade कराओ, land करो।

## कब चलाएँ

कोई भी build, fix, या uplift जिसमें असली दाँव लगा हो। छोटा-सा one-line edit सीधे
[sniper-testing](../skills/sniper-testing/SKILL.md) पर जाकर land हो सकता है।

पूरा loop, एक नज़र में:

```
+--------------------------------------------+
| 0 optimus  boot the floor first            |
+--------------------------------------------+
| 1 intent-compiler  the ask is the spec     |
+--------------------------------------------+
| 2 human-calibration  load the profile      |
+--------------------------------------------+
| 3 understanding-gates + live-research --   |
|   read first, then gate Design -> Ship     |
+--------------------------------------------+
| 4 wayfinder  lost? chart the route         |
+--------------------------------------------+
| 5 red-first  failing test committed first  |<--------------------------+
+--------------------------------------------+  finding -> new red test  |
| 6 build  fleet-ladder + model-fusion;      |   +---------------------+ |
|   bugs: repair-loop + seam-engineering     |   |  LORD OF THE LOOP   |-+
+--------------------------------------------+   | one hand drives the |
| 7 sniper-testing  scoped runs only         |   | loop: dispatch,     |
+--------------------------------------------+   | judge, loop back    |
| 8 clean-code-gauntlet  measure + mutate    |   | until the gate is   |
+--------------------------------------------+   | green. a lane never |
| 9 blind-eval, then blind-tribunal          |-->| lands its own work. |
+--------------------------------------------+   +---------------------+
          |
          | every juror passes
          v
+--------------------------------------------+
| 10 LANDING GATE -- all green or no land:   |
|    red test untouched . builder != grader  |
|    every finding closed . one full pass .  |
|    live proof on the human's own surface . |
|    own files only . two-word report        |
+--------------------------------------------+
```

*Lord of the Loop = loop का मालिक — एक ही हाथ जो dispatch, judge और दोहराव तब तक चलाता है जब तक landing gate green न हो जाए; LAND = बदलाव का final उतरना — हर gate green होने पर merge होकर ship होना।*

## चेन

0. [optimus](../skills/optimus/SKILL.md) — कुछ भी edit होने से पहले harness boot
   करें। floor सबसे पहले load होता है — हर session, हर बार।
1. [intent-compiler](../skills/intent-compiler/SKILL.md) — माँग को ही spec की तरह,
   पूरा पढ़ें। कोई ship या option वाला फ़ैसला सामने रखने से पहले intent निकालें।
   जब साफ़ हल मौजूद हो, options का menu कभी न परोसें — हल कर दें।
2. [human-calibration](../skills/human-calibration/SKILL.md) — इंसान की validated
   profile load करें और लागू करें। जिस इंसान को आप पहले से जानते हैं, उससे दोबारा
   पूछताछ कभी न करें।
3. [understanding-gates](../skills/understanding-gates/SKILL.md) — Design → Plan →
   Build → Test → Ship, हर stage पर gate। किसी भी design से पहले: जो मौजूद है उसे
   [live-research](../skills/live-research/SKILL.md) से पढ़ें, जो लिखा है उसे reuse
   करें, पूरी topology का नक्शा बनाएँ। जवाब अक्सर पहले से लिखा होता है।
4. [wayfinder](../skills/wayfinder/SKILL.md) — किसी भी कदम पर खो जाएँ, तो सबूत से
   रास्ता बनाएँ। जिस सवाल का जवाब सबूत दे सकता है, वह इंसान पर कभी न टाँगें।
5. [red-first](../skills/red-first/SKILL.md) — failing contract test लिखें और किसी
   भी builder के चलने से पहले commit करें। builder उस test को छू नहीं सकता।
6. बनाएँ। default में parallel lanes फैलाएँ — जो एक साथ चल सकता है उसे कभी
   serialize न करें। हर lane को अपनी scratch branch या worktree मिले। अकेले, एक
   ही session में? एक lane ही fan-out है — scratch branch पर बनाएँ और आगे बढ़ें।
   (worktree उसी repo की दूसरी checkout है, दूसरे folder में, ताकि दो builders
   कभी एक ही files को न छुएँ।) builders को
   [fleet-ladder](../skills/fleet-ladder/SKILL.md) से resolve करें; drafts को
   [model-fusion](../skills/model-fusion/SKILL.md) से जोड़ें। bug के लिए
   [repair-loop](../skills/repair-loop/SKILL.md) चलाएँ और
   [seam-engineering](../skills/seam-engineering/SKILL.md) के हिसाब से साझा seam
   पर पूरी CLASS बंद करें।
7. [sniper-testing](../skills/sniper-testing/SKILL.md) — iterate करते समय सिर्फ़
   scoped runs; छुए गए modules का एक पूरा pass landing (step 10) तक रुकता है।
8. [clean-code-gauntlet](../skills/clean-code-gauntlet/SKILL.md) — landing से पहले
   नापें: sniper suite, complexity-गुणा-coverage वाला risk score आपकी ceiling के
   नीचे, फिर mutation testing zero survivors तक। code को नापें; कभी सिर्फ़ आँख से
   न आँकें।
9. [blind-eval](../skills/blind-eval/SKILL.md), फिर
   [blind-tribunal](../skills/blind-tribunal/SKILL.md) — एक author-redacted
   envelope builder से अलग model family के graders के पास जाता है। builder कभी
   अपने काम का grade नहीं करता। हर juror finding एक नया red test बनती है;
   tribunal तब तक दोबारा बैठता है जब तक हर juror pass न दे। अकेला rig है?
   blind-tribunal के Solo rig नियम के हिसाब से नीचे उतरें — और landing report में
   कमज़ोर किए गए gate का नाम लिखें।
10. Land — साफ़ merge करें, छुए गए modules की suites पर ठीक एक पूरा pass चलाएँ,
    असली service restart करें, और behavior को इंसान की अपनी surface पर साबित करें
    (जो page वे खोलते हैं, जो command वे चलाते हैं) — proxy probe कभी नहीं। फिर
    रिपोर्ट करें।

## Hard gates (कोई एक भी लाल हुआ तो landing रुक जाती है)

- failing test build से पहले commit हुआ था और अछूता है — grader जाँचता है कि
  test-file का diff खाली है।
- builder कभी grader नहीं, और grader एक अलग model family से है।
- हर सामने आई finding बंद है, या recorded सबूत के साथ "not a bug" की adjudication
  हुई है। चुपचाप टालना कभी नहीं। whole-seam closure — seam code की वह साझा जगह है
  जहाँ bug की यह class रहती है — नहीं तो landing नहीं।
- इंसान की असली surface पर live proof। टूटी capability के साथ green tests सफलता
  नहीं, विफलता है।
- रिपोर्ट दो शब्दों में — PROVEN या STILL-BUILDING —
  [human-voice](../skills/human-voice/SKILL.md) में। Proven का मतलब है: landed,
  साथ में independent grade, साथ में live प्रदर्शन।
- commit में सिर्फ़ इसी बदलाव की अपनी files हों — किसी दूसरे session का अधूरा काम
  कभी नहीं।

## इनके साथ अच्छा चलता है

- [optimus](../skills/optimus/SKILL.md) — compaction या restart के बाद floor दोबारा boot करने के लिए
- [invariant-floor](../skills/invariant-floor/SKILL.md) — वह locked floor जो हर landing को पूरा करना है
- [decision-bar](../skills/decision-bar/SKILL.md) — क्या इंसान तक पहुँचता है बनाम क्या खुद execute होता है
- [bounded-loops](../skills/bounded-loops/SKILL.md) — लंबे runs पर budget और kill-switch
- [session-handoff](../skills/session-handoff/SKILL.md) — रुकने से पहले state सील करें

**Weight:** पूरा stack — free अनुशासन, light gates, और तीन heavy कदम (model fusion, gauntlet, tribunal) — heavy खर्च हर ship होने वाली चीज़ पर वसूल होता है, और यह play है ही उसी के लिए।
