# Naming — यह pack चीज़ों के नाम कैसे रखता है, और क्यों

इस pack में नाम बोझ उठाते हैं। agent task को नाम और description से मिलाकर skill
चुनता है, इसलिए गलत बात कहने वाला नाम काम को गलत अनुशासन की तरफ़ भेज देता है।
नीचे का convention routing को ईमानदार रखता है।

## नामों की तीन किस्में

- **Skills noun-phrase अनुशासन हैं।** skill वह context है जिसे agent सोचने के लिए
  load करता है — नियमों का पिंड, कोई action नहीं। इसलिए उसका नाम अनुशासन जैसा है:
  `red-first`, `seam-engineering`, `sniper-testing`। अनुशासन को load किया जाता
  है; उसे "run" नहीं किया जाता।
- **Commands imperatives हैं।** command एक action है जिसकी शुरुआत और अंत होता है,
  इसलिए उसका नाम एक verb है, या उस play/skill का नाम जिसे वह चलाती है: boot,
  build, hunt, grade, tribunal।
- **Invariant floor क़ानून है।** `invariant-floor` वह अकेली skill है जिसे बाक़ी
  हर skill inherit करती है। उसका नाम वही है जो वह है — floor — क्योंकि pack का
  हर hard rule उसी पर खड़ा है, और कोई skill उसके नीचे कोई बदलाव land नहीं कर
  सकती।

## Ship हुई commands

| Command | क्या चलाती है |
| --- | --- |
| `/agent-build` | `plays/agent-builds.md` |
| `/bughunt` | `plays/bughunt.md` |
| `/design-taste` | `plays/design-taste.md` |
| `/elite-build` | `plays/elite-build.md` |
| `/grade` | `plays/grading-verification.md` |
| `/optimus` | `skills/optimus/SKILL.md` |
| `/parallel-work` | `plays/parallel-work.md` |
| `/secure-delivery` | `plays/security-delivery.md` |
| `/tribunal` | `skills/blind-tribunal/SKILL.md` |
| `/web-build` | `plays/web-app-builds.md` |

`design-taste` का skill, play, और command — तीनों रूपों में होना जान-बूझकर है —
एक अनुशासन, तीन दरवाज़े: skill context है, play नुस्ख़ा है, command trigger है।
कोई उलझन नहीं, क्योंकि command play को चलाती है; play skill को link करता है।

## हर किस्म की जानकारी कहाँ रहती है

हर परत एक अलग सवाल का जवाब देती है, और कुछ भी दोहराया नहीं जाता:

- **नाम mechanism बताता है।** `blind-tribunal` file खोलने से पहले ही बता देता है
  कि यह कैसे काम करता है: jurors, लेखक से अंधे।
- **description में trigger words रहते हैं।** runtime आपके शब्दों को descriptions
  से मिलाता है, इसलिए description में वह हर वाक्यांश रहता है जो कोई इंसान उस
  skill की ज़रूरत पर बोलेगा — पुराने नाम भी (नीचे देखें)।
- **body में नियम रहते हैं।** steps, skill को fail करने वाले hard rules, और वे
  skills जिनके साथ वह जोड़ी बनाती है। body ही अनुशासन है; नाम और description
  सिर्फ़ उसका पता हैं।

## Rename से कभी कुछ नहीं टूटता

जब किसी skill का नाम बदलता है, तो उसका पुराना नाम description में trigger word
बनकर चला जाता है, ताकि हर आदत और हर doc जो पुराना नाम इस्तेमाल करता था, अब भी
सही जगह पहुँचे:

- **optimus** अपना नाम पूरा का पूरा रखता है — वह boot का brand है, pack का
  इकलौता proper name, और वही command जो आप सबसे पहले type करते हैं (`/optimus`)।
- **"yoke"** `human-calibration` पर trigger word बनकर ज़िंदा है — दोनों में से
  कोई भी बोलें, वही अनुशासन load होता है।

जो rename किसी मौजूदा trigger को तोड़ दे, वह सफ़ाई नहीं, regression है।

## Effort stamps

हर skill अपने title के नीचे एक **Effort:** पंक्ति रखती है, जो दो सवालों का जवाब
देती है: इसे चलाने में क्या ख़र्च होता है, और यह कौन-सी बर्बाद मेहनत हटाती है?
तीन tiers:

- **free** — शुद्ध अनुशासन: कोई अतिरिक्त model call नहीं, कोई अतिरिक्त tooling
  run नहीं। कुछ free skills net लागत सीधे घटाती हैं, और उनके stamps यह साफ़ कहते हैं।
- **light** — एक अतिरिक्त pass: एक subagent, एक validator run, एक probe, एक
  test-first लिखाई।
- **heavy** — कई models या agents, या असली compute (mutation runs, juror
  panels)। heavy stamp को यह भी बताना होगा कि खर्च कब वसूल होता है।

ईमानदारी का क़ानून: stamp एक ऐसा दावा है जिसे skill का body साबित करे — free का
ठप्पा लगा tribunal झूठ है। "हटाता है:" वाला हिस्सा उस ख़ास बर्बादी का नाम लेता है
जिसे skill मिटाती है (ख़त्म हुआ rework, ख़त्म हुई rogue landings, ख़त्म हुए
full-suite reruns), कभी कोई सामान्य "समय बचाता है" नहीं। हर play उसी अंदाज़ में
अपनी chain का जोड़ बताती एक **Weight:** पंक्ति पर ख़त्म होती है।

## हर skill के नाम की वजह

| नाम | यही नाम क्यों |
| --- | --- |
| absorb | बाहरी capability को अंदर लेकर native की तरह re-engineer करने का अनुशासन, नक़ल बनाने की जगह। |
| blind-eval | लेखक छिपाकर evaluation — अंधापन ही mechanism है। |
| blind-tribunal | jurors का एक panel, लेखक से अंधा, अलग-अलग model families से। tribunal = panel और verdict, दोनों। |
| bounded-loops | जो गुण लागू होता है वही नाम है: हर loop एक bound रखता है — budget, checkpoint, kill-switch। |
| clean-code-gauntlet | gauntlet सख़्त जाँचों की एक कतार है; clean code वह है जो उससे बचकर निकलता है। |
| decision-bar | एक bar जिस पर हर फ़ैसला नापा जाता है, इंसान तक पहुँचने से पहले। |
| design-taste | visual काम में taste का अनुशासन — gate और जाँच के साथ, vibes के भरोसे नहीं। |
| fleet-ladder | model fleet एक fallback ladder की तरह resolve होती है, क्रम से चढ़ी जाती है। |
| gpu-dispatch | GPU काम का dispatch क़ानून: हर card पर एक model, loop भर गर्म। |
| guided-steps | वे steps जो सिर्फ़ इंसान कर सकता है, एक-एक stage करके guide किए हुए। |
| human-calibration | build को उस इंसान पर calibrate करना जिसकी वह सेवा करता है। (पहले "yoke" था — पुराना नाम trigger word बनकर ज़िंदा है।) |
| incident-closure | incident पूरा बंद होता है — root cause से live proof तक — कभी इंसान की तरफ़ वापस triage नहीं। |
| intent-compiler | सहज भाषा को execute होने लायक़ directive में compile करता है। prose ही source है; directive output है। |
| invariant-floor | नंबर वाले क़ानूनों का floor जिसे हर बदलाव को पार करना है। क़ानून, सलाह नहीं। |
| leap-protocol | बड़े काम को parallel builders पर उछालने और एक spine से land कराने का protocol। |
| live-research | live sources के खिलाफ़ research — docs और code जैसे वे अभी हैं — model की याददाश्त नहीं। |
| model-fusion | कई models draft बनाते हैं, एक स्वतंत्र judge चुनता है — outputs का fusion, कोई vote नहीं। |
| optimus | boot का brand, proper name की तरह रखा गया। वह floor boot करता है; हर session यहीं से शुरू होता है। |
| human-voice | जो लागू करता है उसी पर नाम: agent वैसे लिखता है जैसे इंसान बोलता है, और कठिन विचार फिर भी पूरे पहुँचते हैं। |
| red-first | failing (red) test पहले आता है, build शुरू होने से पहले commit होकर। |
| repair-loop | पूरा fix loop, अपनी शक्ल पर नाम: ground, reproduce, fix, verify, land। |
| root-cause-first | operations का क्रम ही नियम है: पहले cause, फिर fix, हमेशा। |
| seam-engineering | fixes seam पर land होते हैं — साझा primitive पर — कभी बिखरे point patches की तरह नहीं। |
| session-handoff | अपने artifact पर नाम: एक handoff file जिससे ठंडा session आगे बढ़ सके। |
| sniper-testing | एक गोली, एक निशाना: सिर्फ़ वे tests चलाओ जो छुए गए हिस्से को cover करते हैं। |
| understanding-gates | हर build stage पर gates जो समझ जाँचते हैं, सिर्फ़ syntax नहीं। |
| wayfinder | खो जाने पर रास्ता खोजता है, इंसान पर सवाल टाँगने की जगह। |
