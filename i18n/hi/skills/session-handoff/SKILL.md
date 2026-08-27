---
name: session-handoff
description: तब लगाओ जब session ख़त्म हो रहा हो, context window compact होने वाली हो, या काम किसी और agent या harness में जारी रहना हो। Session को एक flat file में समेटता है जिसे बिल्कुल नया agent ठंडा पढ़कर आगे बढ़ा सके — state, अधूरा काम, ठीक-ठीक अगला command, खुले फ़ैसले — secrets redact करके और साथ चल रहे काम को बचा हुआ verify करके। Trigger words: handoff, hand off, compact, save state, continue in another session, portable handoff, before restart, session सौंपो, state बचाओ, आगे के लिए लिखो, restart से पहले.
license: MIT
---

# Session Handoff
**Effort:** free — context के मरने से पहले लिखी एक flat file; कोई model call नहीं, और अगले session की शुरुआत पर लागत सीधे घटाता है। हटाता है: नए agent का state दोबारा निकालना, चुक चुकी traps की क़ीमत दोबारा चुकाना, और मरी हुई context window में खोए फ़ैसले।

Context window मरती है; काम नहीं मरना चाहिए। Session ख़त्म या compact होने से
पहले एक flat file लिखो जिसे बिल्कुल नया agent ठंडा पढ़कर आगे बढ़ा सके — क्या
हो रहा था, कहाँ रहता है, क्या अधूरा है, और ठीक-ठीक अगला command। जो handoff
chat के गद्य या अकेली याददाश्त में park है, उसका वजूद ही नहीं।

## कब लिखें

- Context window compact या clear होने से पहले।
- खुला काम छोड़कर session ख़त्म करते वक़्त।
- कुछ बड़ा land करने के ठीक बाद (commit id ताज़ी-ताज़ी दर्ज करो)।
- जिस पल कोई असली फ़ैसला तुम्हारे इंसान के पास जाए (दर्ज करो हर विकल्प का
  मतलब क्या है)।

## कहाँ जाए

एक जानी-पहचानी जगह जहाँ अगला agent SABSE PEHLE देखेगा। अगला agent तुम्हारा
project share करता हो, तो repo में एक stable ledger file लो और update commit
करो, ताकि वह machine restart से भी बचे, सिर्फ़ context clear से नहीं। अगला
agent अलग harness या fresh login हो, तो temp dir में एक flat portable file
लिखो — वह scaffolding है, tracked artifact नहीं।

## पहले साथ चल रहा काम verify करो (एक शब्द लिखने से पहले)

जाँचो कि DUSRE sessions का काम बचा हुआ है। `git status`, `git log` और
`git worktree list` चलाओ। Dirty files और unmerged branches doc में ईमानदारी
से नोट करो। Handoff को साफ़ दिखाने के लिए किसी दूसरे session का uncommitted
काम कभी मत बदलो — वही data-loss वाला defect है। जो handoff साफ़ state बताए
जबकि दूसरा session काम की उड़ान में है, वह झूठा दावा है।

## अंदर क्या जाए — हर एक का एक छोटा section

1. **Goal।** काम एक वाक्य में। अगले agent को अंदाज़ा न लगाना पड़े कि "done"
   का मतलब क्या है।
2. **State।** Landed (commit ids), building, queued। Specs, plans, issues और
   diffs का हवाला path या URL से दो — उनका content कभी duplicate मत करो।
3. **काम कहाँ रहता है।** Branches, worktrees, dirty files। वे exact files नाम
   लो जो अगले agent को सबसे पहले पढ़नी हैं।
4. **Verdict की पगडंडी।** हर टुकड़े को किसने या किस चीज़ ने grade किया और
   असली पकड़ें क्या थीं। नामी defects वाला failed verdict green से ZYADA
   क़ीमती है — defects जस के तस लिखो।
5. **अधूरा काम और ठीक-ठीक अगला command।** क्या बीच उड़ान में है, और वह
   literal command जो उसे आगे बढ़ाता है।
6. **खुले फ़ैसले।** जो कुछ तुम्हारे इंसान का इंतज़ार कर रहा है, और हर विकल्प
   का मतलब। कोई फ़ैसला सिर्फ़ एक मरी हुई context window में कभी नहीं रहना
   चाहिए।
7. **अधूरे contracts।** अब भी red पड़े tests, अब भी ग़ायब proofs, किए गए पर
   अब तक न निभाए वादे।
8. **जाल।** हर एक की एक line। जिस जाल की क़ीमत तुम चुका चुके हो, वह green से
   ज़्यादा क़ीमती है — लिख दो, ताकि अगला session दोबारा न चुकाए।
9. **सुझाई skills।** अगले agent को कौन-सी skills पहले load करनी चाहिए, और
   एक line क्यों। यही doc को harnesses के पार portable बनाता है।

## Hard rules

- **Redact करो।** कोई API keys, passwords, tokens या personal data नहीं। कोई
  असली hostnames, internal IPs या home paths नहीं — सिर्फ़ placeholders;
  असली values की तरफ़ env var के नाम से इशारा करो। Handoff वह file है जिसके
  machine से बाहर जाने की सबसे ज़्यादा संभावना है; उससे leak हुआ secret ही
  bug है।
- **ग़ैरमौजूदगी के दावे सबसे तेज़ सड़ते हैं।** "X मौजूद नहीं" या "X land नहीं
  हुआ" लिखने से पहले मौजूदा commit पर दोबारा verify करो — तुम्हारे लिखते-लिखते
  parallel काम land होता रहता है।
- **हर item पर दो-शब्द का status: PROVEN या STILL-BUILDING।** Live proof के
  बिना green tests STILL-BUILDING हैं, और handoff ठीक-ठीक बताता है कौन-सा
  proof ग़ायब है।
- **दो मिनट में पढ़ने लायक़ रखो** (क़रीब 120 lines)। उससे बढ़ जाए, तो सबसे
  पुराने खंड history section में खिसकाकर archive करो — delete करके कभी नहीं।

## Pickup (दूसरा आधा)

Handoff से शुरू होने वाला session उसे SABSE PEHLE पढ़ता है, फिर उस पर काम
करने से पहले ऊपर के दो-तीन दावे `git log` और live tree से मिलाता है। Handoff
नक्शा है, सच नहीं — KAHAN देखना है इसके लिए उस पर भरोसा करो; KYA कहता है वह
verify करो।

## इनके साथ अच्छा चलता है

- [root-cause-first](../root-cause-first/SKILL.md) — वह जाँच जो अगला session आगे बढ़ाता है।
- [repair-loop](../repair-loop/SKILL.md) — seam गँवाए बिना loop के बीच handoff।
- [decision-bar](../decision-bar/SKILL.md) — खुले फ़ैसले तुम्हारे इंसान तक कैसे पहुँचते हैं।

> Scaffold credit: Matt Pocock, handoff (mattpocock/skills). यहाँ का
> composition और hard rules BACKS AIOS के हैं।
