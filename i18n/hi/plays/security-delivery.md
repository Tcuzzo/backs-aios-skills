# Play: Security & Delivery

हर उस चीज़ का ship gate जिसे कोई customer या कोई दूसरी machine चलाएगी। बनावट से
ही सुरक्षित: harness नियम लागू करता है, model की याददाश्त पर कभी भरोसा नहीं किया
जाता।

## कब चलाएँ

- कोई repo, agent, या app deliver, publish, या deploy होने वाला है।
- tools वाला कोई agent untrusted content छूता है — web pages, issues, email, input।
- आप किसी ship होने वाली चीज़ में dependencies या CI जोड़ रहे हैं।

ship gate, एक नज़र में:

```
+--------------------------------------------+
| 1 secret gate  verified-only scan; one     |
|   live credential fails the build          |
+--------------------------------------------+
| 2 egress lockdown  deny by default;        |
|   canonicalize before allowlist match      |
+--------------------------------------------+
| 3 break the lethal trifecta  one leg       |
|   always missing on every path             |
+--------------------------------------------+
| 4 taint tracking  tainted session =>       |
|   policy-gate every exfil-capable action   |
+--------------------------------------------+
| 5 supply chain  hash-pin every dep, no     |
|   install scripts, SHA-pinned CI           |
+--------------------------------------------+
| 6 clean-code-gauntlet  mutate detectors,   |<--------------------------+
|   parsers, predicates to zero survivors    |  a survivor or a          |
+--------------------------------------------+  sandbox catch ->         |
| 7 sniper-testing  mock outbound network    |   +---------------------+ |
|   only, never payload or parser            |   |  LORD OF THE LOOP   |-+
+--------------------------------------------+   | one hand drives the |
| 8 sandbox before ship  outbound blocked,   |-->| loop: dispatch,     |
|   watch writes + calls, hard-kill armed    |   | judge, loop back    |
+--------------------------------------------+   | until the gate is   |
| 9 provenance  SBOM + signed provenance;    |   | green. a lane never |
|   still review the source                  |   | lands its own work. |
+--------------------------------------------+   +---------------------+
          |
          | every gate green
          v
+--------------------------------------------+
| LANDING GATE -- all green or no ship:      |
| no live credential anywhere . no path      |
| holds all three trifecta legs . deps +     |
| CI hash-pinned . zero surviving mutants    |
| . sandboxed before ship                    |
+--------------------------------------------+
```

*Lord of the Loop = loop का मालिक — एक ही हाथ जो dispatch, judge और दोहराव तब तक चलाता है जब तक landing gate green न हो जाए; LAND = बदलाव का final उतरना — हर gate green होने पर merge होकर ship होना।*

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
6. [clean-code-gauntlet](../skills/clean-code-gauntlet/SKILL.md) — security code
   पर सबसे सख़्त bar लगती है। हर detector, parser, और policy predicate पर
   mutation testing चलाएँ, और बचे हुए mutants को शून्य तक ले जाएँ। threat check
   के अंदर उलटी हुई comparison, जिसे suite फिर भी pass कर दे — वही vulnerability
   है।
7. [sniper-testing](../skills/sniper-testing/SKILL.md) — mock सिर्फ़ बाहर जाते
   network का करें, कभी उस payload या parser का नहीं जो test के नीचे है: mocked
   detector production में एक अंधा sensor है।
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
