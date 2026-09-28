---
name: "clean-code-gauntlet"
description: "तब इस्तेमाल करें जब कोई भी build — agent, service, library — hardened या land करनी हो और line-by-line review की जगह एक deterministic quality bar चाहिए; sniper tests, CRAP score (complexity x coverage) और bounded mutation testing चलाता है, फिर हल्का taste review. Trigger words: clean code, gauntlet, unc, uncle bob, crap score, crap, mutation testing, harden, complexity, coverage, quality bar, साफ़ code, गुणवत्ता की कसौटी, सख़्त जाँच."
license: "MIT"
---

# Clean Code Gauntlet
**Effort:** heavy — असली compute: coverage और complexity runs, साथ में एक bounded mutation pass, फिर एक taste model; इसे ship होने वाले बदलावों पर खर्च करें। हटाता है: पूरे diffs की line-by-line इंसानी review, और वे fake-green tests जिनके पीछे regression छिप जाता है।

## यह क्यों है

गंदा code agents को भटकाता है, और लंबे prompt में दबे नियम context के बीच में
धुँधला जाते हैं — deterministic जाँचें कभी नहीं धुँधलातीं। इसलिए Clean Code को
**एक gauntlet की तरह चलाओ जिसे code को पार करना है**, गद्य की तरह नहीं जिसे
model को याद रखना है।

**नापो, review मत करो।** उन नंबरों पर gate लगाओ जो tool गिनता है: coverage,
cyclomatic complexity (किसी function के अंदर से गुज़रते स्वतंत्र रास्तों की गिनती),
module का size, mutation kills। इंसान और model सिर्फ नमूने audit करते हैं —
पूरे diffs कभी नहीं।

## चेन (क्रम में चलाओ; हर stage नाकामी पर ज़ोर से रुकती है)

1. **Sniper tests green.** सिर्फ वे test files चलाओ जो diff के छुए हिस्से को cover
   करती हैं — देखो [sniper-testing](../sniper-testing/SKILL.md)। Red baseline का
   मतलब है रुको और ठीक करो; red पर कभी mutate या grade मत करो।
2. **CRAP threshold के नीचे** असली coverage data पर (नीचे gate देखो)।
   पार हुआ → function को refactor करके नीचे लाओ, या उसे पूरा cover करो। Bar कभी
   नीचे मत करो।
3. **Mutation testing: scope में शून्य survivors.** Survivor TESTS को दोषी ठहराता
   है, code को नहीं — उस test को मज़बूत करो जिसे उसे पकड़ना चाहिए था।
4. **हल्का taste review** — model सिर्फ वही परखता है जो नंबर नहीं परख सकते।

## यह गिनने वाले tools

| Stack | Tools |
| --- | --- |
| Python | coverage.py + radon + mutmut |
| JS/TS | c8 (या istanbul) + Stryker |
| Go | go test -cover + gocyclo + go-mutesting |
| Rust | cargo-tarpaulin + cargo-mutants |
| Java | JaCoCo + PIT |
| बाक़ी | कोई भी coverage % + कोई भी cyclomatic-complexity counter |

हर stage का एक command आकार:
- Coverage: `coverage run -m pytest <sniper files> && coverage report` (JS/TS: `npx c8 vitest run <files>`)
- Complexity: `radon cc -s <changed files>`
- Mutation: `mutmut run --paths-to-mutate <changed files>` (JS/TS: `npx stryker run --mutate "<glob>"`)

## CRAP gate

```
CRAP(m) = comp(m)^2 * (1 - cov(m)/100)^3 + comp(m)
```

- 100% coverage पर score सिमटकर ख़ुद complexity रह जाता है।
- 30 क्लासिक "crappy" रेखा है (शून्य coverage पर complexity 5 वहाँ पहुँच जाती है)।
- इंसान हर function में मोटे तौर पर 4–5 complexity रखते हैं। Agent 6–8 SIRF
  क़रीब-100% coverage पर रख सकता है — वो ढील coverage से चुकती है।
- High-CRAP function के ठीक दो ही निकास हैं: refactor करके नीचे लाओ, या पूरा
  cover करो। **Pass होने के लिए threshold कभी नीचे मत करो।**

## क़र्ज़ किसका है — AUTHORED / WORSENED / UNCHANGED

Absolute score छिपा देता है कि क़र्ज़ किसका है। हर complexity और CRAP delta को
बदलाव-से-पहले वाले baseline के आगे बाँटो:

- **AUTHORED** — functions जो इस बदलाव ने बनाए। पूरी bar लागू।
- **WORSENED** — पहले से मौजूद functions जिन्हें इस बदलाव ने बदतर किया। Delta
  इसी बदलाव के खाते में; उसे baseline पर या उससे बेहतर लौटना ही है।
- **UNCHANGED** — पहले से मौजूद क़र्ज़ जिसे बदलाव ने छुआ ही नहीं। Report करो, file
  करो, इस बदलाव के खाते में कभी मत डालो — और इसे gauntlet टालने का बहाना भी कभी
  मत बनाओ।

## Mutation के नियम (सीमित, कभी लापरवाह नहीं)

- **साझा working tree कभी नहीं।** Committed HEAD से काटे गए scratch checkout में
  mutate करो। Target या test files गंदी हैं = मना करो; पहले commit।
- **Cost नापी जाती है, कभी मानी नहीं जाती।** Scoped suite को एक बार time करो,
  कुछ भी ख़र्चने से PEHLE ETA = baseline x mutant count report करो। Dry run की
  पेशकश करो।
- **सीमित और resumable.** Mutants और मिनटों पर सीमा। Budget-रोक एक checkpoint के
  साथ pause है, failure नहीं — resume करके पूरा करो।
- **Coverage-first.** सिर्फ covered lines mutate करो; uncovered line एक coverage
  gap है जिसे CRAP gate पहले ही पकड़ चुका।
- **सिर्फ scope में।** जो diff ने छुआ वही mutate करो, पूरा repo कभी नहीं।
- सचमुच equivalent mutant को मारने की जगह खंडित किया जा सकता है — खंडन लिखकर,
  कभी चुपचाप skip करके नहीं।
- **आपके stack के लिए कोई mutation tool नहीं?** Landing report में वो दर्ज करो और
  CRAP gate पर टिको — चुपचाप skip कभी नहीं।

## Taste review (आख़िर में, और हल्का)

Deterministic gates पहले चलते हैं; model वहीं ख़र्चो जहाँ reasoning ही इकलौता
औज़ार है। Reviewer builder से अलग family का model है — builder अपना काम खुद कभी
grade नहीं करता। वो सिर्फ design और taste परखता है: naming, गड्ड-मड्ड concerns,
interface की चौड़ाई, और छह smells — rigidity, fragility, immobility, needless
complexity, needless repetition, opacity. हिसाब-किताब gates पहले ही निपटा चुके।

Review जो craft floor थामे रखता है: functions छोटे, एक काम करते हुए, कम
arguments, कोई flag arguments नहीं, ईमानदार नाम; deep modules — छोटा interface
जो असली logic छिपाए; tests तेज़, स्वतंत्र, दोहराने लायक, हर एक में एक behavior
assert.

## सख़्त नियम (कोई एक टूटा तो skill fail)

- Pass निकलवाने के लिए threshold नीचे करना या mutation set कमज़ोर करना — कभी नहीं।
- साझा working tree को mutate करना, या बेलगाम चलाना — कभी नहीं।
- UNCHANGED क़र्ज़ मौजूदा बदलाव के खाते में डालना — कभी नहीं।
- जो test fail हो ही नहीं सकता वो theater है — mutation testing ही साबित करती है
  कि कौन से tests असली हैं।
- असली cost बताओ — machine का समय सस्ता है, regressions नहीं। घंटा बचाने के लिए
  green कभी मत गढ़ो।

## इनके साथ अच्छा चलता है

- [sniper-testing](../sniper-testing/SKILL.md) — stage 1 के लिए test का दायरा चुनता है
- [red-first](../red-first/SKILL.md) — हर build से पहले आने वाला failing contract
- [blind-eval](../blind-eval/SKILL.md) — जब सवाल taste हो, तब keep-or-revert
- [blind-tribunal](../blind-tribunal/SKILL.md) — उतरने से पहले भरा-पूरा graded verdict

> Scaffold credit: Robert C. Martin, *Clean Code* (2008); Alberto Savoia &
> Bob Evans, the CRAP metric (2007); John Ousterhout, deep modules
> (*A Philosophy of Software Design*, 2018); Pocock, M., & Martin, R. C.
> (2026, Aug 19). LIVE: Uncle Bob on Software Fundamentals in the Age of AI
> [Video]. YouTube. https://www.youtube.com/watch?v=zcLPGC-tvgk — source of
> the agent CRAP band and coverage-first mutation. The composition and hard
> rules here are BACKS AIOS.
