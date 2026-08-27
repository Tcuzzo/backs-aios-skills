# Play: Grading & Verification

Adversarial grading का play। इसका एक ही विश्वास है: green नतीजा एक दावा है, सबूत
नहीं। grader हमला करता है, और floor ऐसा बना होता है कि उसे game करना नामुमकिन हो।

## कब चलाएँ

- कोई भी बना हुआ बदलाव land होना चाहता है — code, config, docs, किसी agent का
  output।
- कोई suite green होने का दावा करती है और किसी ने उसे पहले fail होते नहीं देखा।
- काम एक model ने बनाया है और आपको उस पर एक ईमानदार verdict चाहिए।

## चेन

1. [red-first](../skills/red-first/SKILL.md) — पक्का करें कि fix के आने से पहले
   suite non-zero exit के साथ fail हुई थी। जो suite कभी red थी ही नहीं, वह कुछ
   साबित नहीं करती।
2. [sniper-testing](../skills/sniper-testing/SKILL.md) — जाँचें कि builder ने
   iteration के दौरान scoped tests चलाए और जिस seam को बदला, उस पर कोई mock
   theater नहीं किया।
3. Cross-family grade — काम को builder से एक ALAG family के model के हाथ में दें।
   एक ही family के भीतर grading नापे जाने लायक़ हद तक win-rates फुलाती है — grader
   अपने ही खानदान का पक्ष लेते हैं; उसी family का दूसरा instance काफ़ी नहीं है।
4. [blind-tribunal](../skills/blind-tribunal/SKILL.md) — गंभीर नतीजों वाले बदलावों
   के लिए, jurors को एक author-redacted envelope पर बिठाएँ। हर finding एक नया red
   test बनती है, और tribunal तब तक दोबारा बैठता है जब तक सारे jurors pass न दें।
5. [clean-code-gauntlet](../skills/clean-code-gauntlet/SKILL.md) — grader खुद
   gauntlet दोबारा चलाता है (coverage-बनाम-complexity, सीमित mutation testing)।
   builder की अपने ही आँकड़ों की रिपोर्ट पर कभी भरोसा न करें।

## दो-तरफ़ा सबूत (दोनों चाहिए, वरना pass नहीं)

- **Fail-to-pass:** जो tests red थे वे अब green हैं — fix साबित हुआ।
- **Pass-to-pass:** जो कुछ green था वह अब भी green है — कोई regression नहीं।
- जो run सिर्फ़ नए passing tests जोड़ता है, वह दोनों में से कोई शर्त पूरी नहीं
  करता। दोनों को hermetically चलाएँ।

## Fake-green के पहरेदार (इनमें से कोई एक भी दिखा, तो वही सुराग़ है)

- exit-code का escape hatch — ऐसा harness जो कुछ भी हो जाए, साफ़ exit करता है।
- computed नतीजों की जगह hardcoded या रटे हुए outputs।
- delete किए गए, skip किए गए, या कमज़ोर किए गए tests।
- कोई भी edit किया हुआ grader, timer, या scorer। edit हुआ harness जो green हो
  जाए — वही सुराग़ है।
- green suite के नीचे ज़िंदा बचा mutant। mutant इस बात का सबूत है कि assertions
  उस branch तक पहुँचे ही नहीं — परिभाषा से fake green।

## Judge का bias हटाएँ

Judge-mechanics का floor [blind-eval](../skills/blind-eval/SKILL.md) के "De-bias
the judge" section में है — उसे पूरा लागू करें।

## Hard gates — कोई एक भी टूटा तो play fail

- builder और grader एक ही model family से हैं।
- fix से पहले suite को red दिखाया नहीं जा सकता।
- graded run में fail-to-pass या pass-to-pass गायब है।
- ऊपर वाला कोई भी fake-green सुराग़ मौजूद है।
- grader ने checks खुद दोबारा चलाने की जगह builder की अपनी रिपोर्ट पर भरोसा कर लिया।

**Weight:** शुरुआत में free red और sniper जाँचें; heavy खर्च tribunal और grader का खुद gauntlet दोबारा चलाना है — यह land होने की माँग करने वाले हर बदलाव पर वसूल होता है, क्योंकि एक fake green सारी grades की मिली-जुली लागत से ज़्यादा महँगा पड़ता है।
