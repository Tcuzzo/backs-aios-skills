# Agent Builds

अपने दम पर काम करने वाला agent या service कैसे बनाएँ। मूल बात यह है: deterministic
primitives — यानी वे हिस्से जो हर बार एक-सा, पक्का नतीजा देते हैं — भारी काम उठाते हैं;
model सिर्फ़ वहीं सोचता है जहाँ सोच के अलावा कुछ और काम ही नहीं करता। जिस design में
सब कुछ LLM हो और primitives शून्य — वह design ही अमान्य है।

## कब चलाएँ

कोई भी agent, bot, worker, या लंबा चलने वाला service बनाते समय — ऐसी हर चीज़ जो
tools रखती हो, network call करती हो, या बिना किसी इंसान की हर कदम पर नज़र के
action लेती हो।

## चेन

1. [intent-compiler](../skills/intent-compiler/SKILL.md) — माँग को पूरा पढ़ें;
   mission और उसकी सीमाएँ इंसान के अपने शब्दों से आती हैं।
2. [understanding-gates](../skills/understanding-gates/SKILL.md) — design के स्तर
   पर सबसे पहले DOMAIN PRIMITIVES के नाम तय करें: हर core capability एक
   deterministic, offline, fail-closed function हो। LLM वाली जगह सिर्फ़ असली
   reasoning के लिए बचाकर रखें।
3. [red-first](../skills/red-first/SKILL.md) — हर typed IO boundary के लिए failing
   contract test commit करें — उसे बनाने से पहले।
4. नीचे दिए doctrine के हिसाब से बनाएँ। हर loop को
   [bounded-loops](../skills/bounded-loops/SKILL.md) के अंदर रखें: budget,
   checkpoint, backoff, और एक ज़ोरदार kill-switch — hammering retry कभी नहीं।
5. [sniper-testing](../skills/sniper-testing/SKILL.md) — mock सिर्फ़ बाहर जाने
   वाले transport का हो सकता है — routing, prompt-building, या parsing का कभी नहीं।
6. [clean-code-gauntlet](../skills/clean-code-gauntlet/SKILL.md) — agent के tool
   handlers और decision functions gauntlet से गुज़रें: risk score आपकी ceiling के
   नीचे, फिर decision paths पर mutation testing चलाकर zero survivors तक। जो
   branch logic उलटी comparison के बाद भी ज़िंदा बच जाए, वह असल में कभी test हुई
   ही नहीं थी।
7. [blind-tribunal](../skills/blind-tribunal/SKILL.md) — ship से पहले
   cross-family graders agent को पास करें। builder कभी अपने ही काम का grade नहीं
   करता।

## Doctrine (build को क्या-क्या पूरा करना है)

- हर IO boundary एक typed contract (inputs → outputs) घोषित करे और FAIL CLOSED
  रहे — गलत input पर raise या deny करे। कभी fail open नहीं, कभी error निगलना नहीं।
- हर network seam cassette-testable हो: बाहर जाने वाली calls को एक record/replay
  seam के पीछे रखें, ताकि पूरी suite offline, fixtures के सहारे चल सके।
- सारा egress एक साफ़ deny-by-default hostname allowlist से गुज़रे। अनजान host पर
  raise हो; वह कभी चुपचाप connect न हो।
- agent को एक typed event stream / state machine की तरह model करें, deterministic
  sign-off states के साथ (draft → review → ready → done) जिन्हें agent खुद अपने
  लिए compute करता है — यह एक primitive है, इंसान पर friction नहीं। कोई action
  अपना state skip नहीं कर सकता।
- सिर्फ़ सचमुच destructive या irreversible actions (खर्च, delete, ऐसा बाहरी send
  जो वापस नहीं हो सकता) को fire करने से पहले committed state के खिलाफ़ confirm
  करें। किसी benign या read-only action पर gate कभी न लगाएँ, और इंसान पर तो कभी
  नहीं — देखें [decision-bar](../skills/decision-bar/SKILL.md)।
- टिकाऊ state (objectives, decisions, ledger) context window के बाहर disk पर
  रखें और उसे दोबारा पढ़ें। लंबे run में in-context memory पर कभी भरोसा न करें।
- एक operating doc ship करें जिसे agent हर task से पहले load करे — सबसे नज़दीकी
  file जीतती है, size की सीमा के साथ — और जिसमें हमेशा-लागू-रहने वाले नियम हों।
- tool की failure reasoning slot को एक structured error लौटाए, ताकि agent खुद को
  सुधार सके। निगला हुआ tool error एक bug है।
- least privilege: agent के पास ठीक वही tools हों जो उसके mission को चाहिए — कोई
  ambient filesystem या network authority नहीं।

## Hard gates

- Zero primitives = design ही अमान्य; step 2 पर वापस जाएँ।
- कोई भी fail-open boundary, silent fallback, या निगला हुआ error ship को रोक देता है।
- decision paths में बचे हुए mutation survivors ship को रोक देते हैं।
- cross-family grade पास होना ज़रूरी है; builder कभी grader नहीं होता।

## इनके साथ अच्छा चलता है

- [root-cause-first](../skills/root-cause-first/SKILL.md) — जब agent बहकने लगे
- [session-handoff](../skills/session-handoff/SKILL.md) — टिकाऊ state, सही तरीके से

**Weight:** ज़्यादातर free अनुशासन और एक light design gate; heavy खर्च gauntlet के mutation runs और cross-family tribunal का है — यह हर उस agent पर वसूल होता है जो बिना किसी की निगरानी के काम करेगा।
