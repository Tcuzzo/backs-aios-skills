---
name: "root-cause-first"
description: "तब लगाओ जब सामने कोई कड़ा bug हो, silent failure हो, regression की खोज हो, या ऐसा जोखिम भरा बदलाव जो चुपचाप किसी downstream consumer को तोड़ सकता हो। बिना जाँच कोई fix नहीं — error पढ़ो, माँग पर reproduce करो, हाल के बदलाव देखो, component की सीमाओं पर instrument लगाओ, data के बहाव को पीछे source तक trace करो। Trigger words: debug, root cause, why is this failing, silent failure, regression, works in tests but fails live, systematic debugging, जड़ पकड़ो, असली वजह ढूँढो, यह fail क्यों हो रहा है, पहले जाँच फिर fix."
license: "MIT"
---

# Root Cause First
**Effort:** free — शुद्ध जाँच का अनुशासन जो अक्सर लागत सीधे घटाता है: एक निर्णायक probe उस पूरी pipeline को दाग़ने की जगह लेती है जो सिर्फ़ "देखें क्या होता है" के लिए चलती। हटाता है: ग़लत चीज़ पर patch — वह symptom fix जो असली bug छिपा देता है और किसी downstream consumer को तोड़ देता है।

बिना जाँच कोई fix नहीं। Failure समझे बिना बना patch ग़लत चीज़ ठीक करता है,
असली bug छिपाता है, और downstream कुछ तोड़ देता है। तुम्हारा product patch
नहीं है — वह एक निर्णायक probe से साबित हुई root cause है, और ऐसा fix जो
साबित हो चुका है कि कुछ भी regress नहीं करता।

नीचे की हर बात पर दो क़ानून राज करते हैं:

1. **कोई assumption नहीं — code, data और live system ही सच हैं; notes सिर्फ़
   इशारे हैं।** एक comment, एक याद, पिछला नतीजा, यहाँ तक कि तुम्हारा अपना
   पिछला वाक्य भी — probe की पुष्टि तक hypothesis है। "सब / हर / कोई नहीं"
   जैसे शब्द तीन-बिंदु जाँच trigger करते हैं: environment, repo-भर की खोज,
   और हर caller का scan।
2. **Verify हुआ counter-example पिछले नतीजे को फ़ौरन मार देता है।** Probe
   तुम्हारे यक़ीन के ख़िलाफ़ जाए, तो साफ़ कहो "मैं ग़लत था — असल में X है,"
   और नए fact से आगे बढ़ो। लीपापोती कभी नहीं।

## Loop (क्रम से चलाओ; कोई step मत छोड़ो)

1. **Error पढ़ो।** Symptom एक सटीक वाक्य में बताओ। असली message पढ़ो, वह
   नहीं जो तुम्हें उम्मीद है। Blast radius का नाम लो: जिस चीज़ पर शक है, उस
   पर क्या-क्या टिका है?
2. **Reproduce करो।** Failure को माँग पर होने दो — live, या failing test
   में। **वक़्त नापो।** जो "failure" milliseconds में लौटे जबकि असली काम
   seconds लेता है, वह जल्दी निगला गया exception है, असली काम का fail होना
   नहीं। Timing का फ़र्क़ ख़ुद एक सुराग़ है।
3. **हाल के बदलाव देखो।** आख़िरी बार काम करने के बाद से क्या बदला — code,
   config, environment, dependencies — उसका diff लो। History लंबी हो तो
   bisect करो।
4. **Consumers का नक्शा बनाओ।** Shared सतह के bug पर हर caller की list बनाओ
   और हर एक उसे कैसे इस्तेमाल करता है (exact string match? boolean? list?)।
   असली regression अक्सर downstream के exact-match comparison में छिपता है,
   उस knob में नहीं जो तुम घुमा रहे हो।
5. **सीमाओं पर instrument लगाओ।** हर component के seam पर log या probe — क्या
   अंदर जाता है, क्या बाहर आता है। ख़राब data को सीमा-दर-सीमा पीछे trace
   करो, source तक। Source ठीक करो, symptom कभी नहीं।
6. **Hypothesis से root-cause निकालो।** एक falsifiable hypothesis बनाओ। वह
   एक निर्णायक probe ढूँढो जो उसे बाक़ी विकल्पों से अलग कर दे, और सिर्फ़ वही
   चलाओ। "देखें क्या होता है" कहकर पूरी pipeline मत दाग़ो।
7. **Surgical fix, सही seam पर।** Root cause हल करने वाला सबसे छोटा बदलाव। N
   call sites edit करने की जगह अकेला shared source (एक normalizer, एक runner)
   चुनो। जहाँ हो सके, fix को काम कर रहे रास्ते पर inert रखो — साबित हो कि
   वहाँ वह कुछ नहीं बदलता और सिर्फ़ टूटे रास्ते पर जागता है। साथ में कोई
   बग़ल का refactor नहीं।
8. **साबित करो।** Bug reproduce करने वाला failing test लिखो; उसे red होते
   देखो; fix करो; उसे green होते देखो। फिर step 4 में map किए हर consumer
   path के tests चलाओ — वहाँ green ही तुम्हारा zero-regression floor है। जो
   suite ठीक उसी seam को mock करती है जो fail हुआ, वह कुछ साबित नहीं करती।
9. **Live verify करो।** असली system चलाओ — असली requests, असली database,
   असली logs। कभी वह sidecar script नहीं जो code को तुम्हारे अपने process
   में import करती है। पहले/बाद का सबूत capture करो।
10. **सीखो।** Symptom, निर्णायक probe, root cause, और उसे छिपाने वाला
    anti-pattern लिख डालो, ताकि इस शक्ल का अगला bug सस्ता पड़े।

## Theory बनाने से PEHLE reproduction loop बनाओ

अगर पकड़ो कि red-capable command बनने से पहले ही theory गढ़ने के लिए code पढ़
रहे हो — रुको। Red-capable command नहीं, तो theory नहीं। एक कसा pass/fail
signal जो इसी bug पर red हो, debugging की सबसे बड़ी अकेली uplift है। यहाँ
बेहिसाब मेहनत लगाओ।

बनाने के तरीक़े, मोटे तौर पर इसी क्रम में: एक failing test; dev server के
ख़िलाफ़ एक HTTP script; fixture input के साथ CLI run, known-good snapshot से
diff; एक headless browser script; capture किया असली payload, अलग-थलग code
path से replay; एक function बुलाने वाला throwaway harness; random inputs पर
fuzz loop; bisection harness ताकि automated bisect चले; एक differential loop
(वही input पुराने और नए version से, outputs का diff)।

फिर उसे कसो: तेज़ (setup cache करो, scope घटाओ), पैना (ख़ास symptom assert
करो, "crash नहीं हुआ" नहीं), deterministic (time pin करो, RNG seed करो,
network freeze करो)। दो-second का deterministic loop एक superpower है।

Flaky bugs में साफ़ repro नहीं, ऊँची reproduction rate का पीछा करो: trigger
को 100 बार loop करो, stress डालो, timing की खिड़कियाँ छोटी करो। 50% वाला
flake debug हो सकता है; 1% वाला नहीं।

सच में loop बन ही न पाए, तो रुककर कह दो। जो आज़माया वह गिनाओ और अपने इंसान
से access, कोई captured artifact, या अस्थायी instrumentation माँगो। बिना loop
theory मत बनाओ। और अगर कोई seam ही नहीं जो असली call pattern दोहरा सके, तो
वह ग़ैरमौजूदगी ख़ुद एक finding है — fix land होने के बाद architecture का gap
flag करो।

## Anti-patterns (कड़े bugs ऐसे ज़िंदा रहते हैं)

- बिना probe के किसी note या comment से नतीजा निकालना।
- Reproduce करने से पहले fix करना।
- ऐसी green suite पर भरोसा जो ठीक वही seam mock करती है जो live fail होता है।
- Sidecar verification — live system चलाने की जगह code import करना।
- Config का knob बदलना, बिना उसके exact-match consumers का नक्शा बनाए।
- Fix के साथ सवार होकर आते चौड़े refactors।
- तीन-बिंदु जाँच के बिना "सब / हर / कोई नहीं" कहना।

## इनके साथ अच्छा चलता है

- [red-first](../red-first/SKILL.md) — fix से पहले failing test commit करो।
- [sniper-testing](../sniper-testing/SKILL.md) — iterate करते हुए scoped tests।
- [seam-engineering](../seam-engineering/SKILL.md) — instance नहीं, class ठीक करो।
- [repair-loop](../repair-loop/SKILL.md) — पूरा fix-and-land cycle।

> Scaffold credit: Matt Pocock, diagnosing-bugs (mattpocock/skills). यहाँ का
> composition और hard rules BACKS AIOS के हैं।
