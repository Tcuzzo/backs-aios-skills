# Web App Builds

साफ़ ढाँचे और सुरक्षित supply chain के साथ web app या site कैसे बनाएँ। web builds
का ज़्यादातर नुकसान dependencies और boundaries से घुसता है, आपकी अपनी logic से
नहीं — इसलिए hygiene ही play है, बाद की सोच नहीं।

## कब चलाएँ

कोई भी web app, site, API, या deliver होने वाली repo बनाते या बढ़ाते समय, जिसे कोई
और install करके चलाएगा।

## साझा task और limits

यह play current [BACKS Build Flow](../skills/backs-build-flow/SKILL.md) task packet
के भीतर चलाएँ। एक integration owner, requested `task_mode`, pinned `base_sha`, current
`candidate_sha`, operator essence और current evidence रखें। Applicable loaded skill
bodies reuse करें; यह play अपने domain gates जोड़ता है, task फिर शुरू नहीं करता।

[bounded-loops](../skills/bounded-loops/SKILL.md) original deadline और remaining
allowances को retries, workers, models, reviews और handoffs में संभालता है। Nested play
के लिए उन्हें reset न करें। Exhaustion पर candidate, evidence, unmet gates और next action
सहित **STILL-BUILDING** checkpoint करें। Useful authorized work remaining allowance में
ही करें; missing gate कभी pass नहीं बनता।

## चेन

1. Stack या structure चुनने से पहले Build Flow के established intent और operator
   essence लें; पूरा request और current corrections लागू करें।

2. [understanding-gates](../skills/understanding-gates/SKILL.md) — पहले ढाँचा
   design करें: एक documented entrypoint, एक स्पष्ट dependency manifest, और एक
   commit की हुई lockfile। files का बेतरतीब फैलाव नहीं।
3. Dependency hygiene (किसी भी install से पहले):
   - हर referenced package को registry के खिलाफ़ validate करें: वह मौजूद है, वह
     आपके project से पुराना है, उसके publisher का इतिहास है। AI के गढ़े हुए
     package नाम squatting का चारा हैं — नापी गई research बताती है कि गढ़े हुए
     नामों में से क़रीब 43% एक जैसे re-runs में दोबारा आते हैं (Spracklen et al.
     (2025), USENIX Security 25), इसलिए हमलावर उन्हें पहले से register कर सकते
     हैं।
   - compiled lockfile से सब कुछ hash-pin करें (जैसे `pip install
     --require-hashes`, `npm ci --ignore-scripts`); किसी भी integrity mismatch को
     ठुकराएँ।
   - install-time lifecycle scripts को default में block करें। जो package सिर्फ़
     postinstall script चलाकर काम करता है, वह एक red flag है।
   - हर CI workflow dependency को पूरे 40-अक्षर वाले commit SHA पर pin करें, कभी
     बदल सकने वाले version tag पर नहीं।
   - गिनती कम रखें: हर dependency एक सोच-समझा फ़ैसला है, एक आदत नहीं। standard
     library या platform के primitive को तरजीह दें।
4. [red-first](../skills/red-first/SKILL.md) — routes, loaders, और validation
   paths के लिए failing contract tests — उन्हें बनाने से पहले।
5. नीचे दिए doctrine के हिसाब से बनाएँ। किसी भी UI surface के लिए
   [design-taste](../skills/design-taste/SKILL.md) का तरीक़ा चलाएँ — पहले tokens,
   accessibility एक hard gate की तरह।
6. [sniper-testing](../skills/sniper-testing/SKILL.md) — pinned aggregate candidate
   diff से repo के real lint/type/test commands scope करें; gaps और justified N/A
   बताएँ। अपनी validation या serialization कभी mock न करें; mocked web boundary
   app को वह स्वीकार करने देती है जिसे reject करना चाहिए।

7. [clean-code-gauntlet](../skills/clean-code-gauntlet/SKILL.md) — route handlers,
   data loaders और form/validation paths deploy से पहले pass हों। Shared budget में
   validation/auth predicates mutate करें; meaningful survivors deployment रोकते हैं।
   Missing regression separate file में दें, sealed original RED बचाएँ। Flipped boundary
   comparison का pass होना public surface पर खुला दरवाज़ा है।

8. [blind-tribunal](../skills/blind-tribunal/SKILL.md) — deploy से पहले independent
   juror panel; हर reviewer configured rung matrix से capability/availability अनुसार
   live चुनें, authoring execution provenance में record और exclude करें। Review fresh
   author-disjoint session में हो। हर proved finding को इस task में separate RED और
   bounded repair दें। Remaining budget में re-convene करें; हर required juror pass करे।
   Full affected-suite landing gate रखें और real app surface पर authorized delivery verify करें।

## Doctrine (build को क्या-क्या पूरा करना है)

- source में कोई secrets नहीं: credentials environment या किसी secret store से
  पढ़ें। commit हुई key build fail कर देती है।
- Output की handling context के हिसाब से हो: SQL के लिए parameterized queries, और
  किसी भी value के shell, database, या DOM तक पहुँचने से पहले सही encoding।
  untrusted input को कभी string जोड़कर न मिलाएँ।
- एक machine-readable SBOM निकालें — software bill of materials (जैसे
  CycloneDX) — ताकि पाने वाला पूरी dependency tree का audit कर सके।
- build को reproducible रखें: pinned toolchain versions, deterministic install,
  और test run के दौरान कोई EXTERNAL network access नहीं (local loopback वाली
  services — databases, fixtures — ठीक हैं और अपेक्षित हैं)।

## Hard gates

- unvalidated या unpinned dependency install रोक देती है।
- commit हुआ secret build रोक देता है।
- validation या auth predicates में mutation survivors deploy रोक देते हैं।
- tests के दौरान external network access landing रोक देती है (loopback ठीक है)।

## इनके साथ अच्छा चलता है

- [seam-engineering](../skills/seam-engineering/SKILL.md) — boundary की खोट को एक class की तरह ठीक करने के लिए
- [bounded-loops](../skills/bounded-loops/SKILL.md) — rate-limit का ध्यान रखने वाली outbound calls

**Weight:** पूरे build में free hygiene अनुशासन; heavy खर्च validation और auth predicates पर mutation और tribunal का है — यह हर public surface पर वसूल होता है, जहाँ एक उलटा comparison खुला दरवाज़ा है।
