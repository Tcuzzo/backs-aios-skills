# Play: Security & Delivery

हर उस चीज़ का ship gate जिसे कोई customer या कोई दूसरी machine चलाएगी। बनावट से
ही सुरक्षित: harness नियम लागू करता है, model की याददाश्त पर कभी भरोसा नहीं किया
जाता।

## कब चलाएँ

- कोई repo, agent, या app deliver, publish, या deploy होने वाला है।
- tools वाला कोई agent untrusted content छूता है — web pages, issues, email, input।
- आप किसी ship होने वाली चीज़ में dependencies या CI जोड़ रहे हैं।

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

1. Secret gate — secret scanner को verified-only mode में चलाएँ (वह हर candidate
   credential को live provider के खिलाफ़ जाँचता है)। एक भी confirmed-live
   credential build fail कर देता है। कोई अपवाद नहीं।
2. Egress lockdown — बाहर जाने वाला traffic default में deny हो; सब कुछ एक ऐसे
   proxy से गुज़रे जो सिर्फ़ bare hostnames allowlist करता है। match करने से पहले
   hostname को canonicalize और validate करें: null bytes, percent वाली चालें, और
   CRLF ठुकराएँ। null-byte वाला `evil-host\x00.trusted.com` bypass असली है और
   production तक पहुँच चुका है।
3. Lethal trifecta तोड़ें — हर execution path को ऐसा design करें कि इन तीन में से
   कम-से-कम एक हमेशा गायब रहे: private data तक पहुँच, untrusted content के सामने
   आना, बाहरी communication। prompt injection को आप पूरी तरह रोक नहीं सकते; पर
   आप उसे चोरी के लायक़ नहीं छोड़ सकते।
4. Taint tracking — untrusted content अंदर आते ही session को tainted mark करें।
   जब तक tainted है, हर exfil-लायक़ action (बाहर जाता HTTP, email, PR बनाना) पर
   harness में policy-gate लगे — यह कभी model के विवेक पर नहीं छूटता।
5. Supply chain — हर dependency को hash-pin करें और install-time scripts block
   करें। हर CI action को पूरे commit hash पर pin करें, tag पर नहीं।
6. [clean-code-gauntlet](../skills/clean-code-gauntlet/SKILL.md) — security code पर
   strictest bar। Shared budget में हर detector, parser और policy predicate की mutation
   testing करें; meaningful survivors ship रोकते हैं। Missing assertions separate
   supplemental tests में जोड़ें; original sealed RED बचाएँ। Threat check का flipped
   comparison suite में pass हो जाए तो वही vulnerability है।

7. [sniper-testing](../skills/sniper-testing/SKILL.md) — pinned aggregate candidate
   diff से scoped actual repo lint/type/test commands लें; gaps और reason वाले N/A
   लिखें। केवल outbound network mock करें, tested payload/parser कभी नहीं; mocked
   detector production में blind sensor है। Gauntlet से पहले current scoped evidence
   reuse करें और required full affected-suite landing gate तथा author-disjoint review रखें।

8. Ship से पहले sandbox — बने हुए artifact को एक ephemeral sandbox में चलाएँ,
   जिसमें सारा outbound blocked हो और resource hard-kill तैयार हो। देखें कि वह
   क्या लिखता है और किसे call करने की कोशिश करता है।
9. Provenance — एक software bill of materials निकालें, और signed provenance भी,
   अगर आपके पास है। फिर भी source की समीक्षा करें: provenance दुर्भावनापूर्ण
   source पर भी उतनी ही वफ़ादारी से दस्तख़त करता है।

## किसी भी build run के दौरान खड़े रहने वाले बचाव

- संवेदनशील paths पर deny-write: shell की startup files, git config और hooks, DNS
  config, SSH keys।
- least-privilege tools। confirm-step सिर्फ़ सचमुच destructive या irreversible
  operations के लिए है — data का नुकसान, खर्च, कोई वापस-न-होने वाला बाहरी action।
  किसी benign capability पर gate कभी नहीं, और अपने इंसान पर तो कभी नहीं।

## Hard gates — कोई एक भी टूटा तो play fail

- deliverable या उसकी history में कहीं भी एक confirmed-live credential।
- कोई execution path जिसके पास trifecta के तीनों पाए एक साथ हैं।
- कोई unpinned dependency, कोई install script, या tag पर pin हुआ CI action।
- किसी detector, parser, या policy predicate में ज़िंदा बचा mutant।
- artifact ship से पहले कभी sandbox में चलाया ही नहीं गया।

**Weight:** ज़्यादातर free निर्माण-अनुशासन और light scanner व sandbox passes; heavy कदम हर detector और policy predicate पर mutation है — यह हर उस चीज़ पर वसूल होता है जिसे कोई customer या दूसरी machine चलाएगी।
