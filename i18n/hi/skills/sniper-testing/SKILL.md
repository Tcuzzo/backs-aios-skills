---
name: sniper-testing
description: "Build या repair loop में, या green result पर भरोसा करने से पहले, जब verification को बेकार whole-suite reruns के बिना actual candidate cover करना हो, तब उपयोग करें।"
license: MIT
---

# Sniper Testing

बदले हुए behavior को उसके real consumer से सत्यापित करें। Checks चुनने में पूरा task
 diff लें, फिर अगली change से प्रभावित checks ही दोहराएँ।
[bounded-loops](../bounded-loops/SKILL.md) की वही mission allowance अपनाएँ।

## 1. असली scope स्थिर करें

[Build Flow](../backs-build-flow/SKILL.md) packet में verified pre-task `base_sha`
और current committed `candidate_sha` सुरक्षित रखें। RED और fix commit करने के बाद
clean working tree में भी task diff होता है। अकेला `git diff HEAD` उसे खो देता है।

इस skill की resolved directory से bundled read-only scope helper चलाएँ:

```bash
python scripts/changed_files.py --repo <verified-repo> --base <base-sha> --candidate <candidate-sha>
```

Iteration में `--include-worktree` तभी जोड़ें जब candidate HEAD हो। यह committed,
staged, unstaged और untracked paths अलग दिखाता है, unusual filenames बचाते हुए।
Aggregate scope में deletions और rename के दोनों sides शामिल हैं। असंबंधित pending
काम को preserved बताएँ; हर लौटे path को अपना न कहें। Missing base या invalid revision
सुलझाने वाला error है, checks छोड़ने का empty scope नहीं। Helper fetch नहीं करता और
history नहीं बदलता।

## 2. वास्तविक checks चुनें और चलाएँ

Changed files तथा affected callers/consumers को behavior tests से जोड़ें, फिर repo के
वास्तविक scripts, CI और configuration पढ़कर applicable commands चुनें।

| Check | Scope और evidence |
| --- | --- |
| Lint और format-check | Existing config से changed supported files; reformat तय करने से पहले check mode लें। |
| Typecheck या compiler | प्रभावित package/project boundary; type dependencies broader target माँग सकती हैं। |
| Behavior tests | Real changed path और capability टूटने पर fail होने वाला regression। |
| Contract/integration tests | इस change से प्रभावित consumers, aliases, packaging, settings preservation या runtime boundaries। |
| Required landing gates | Candidate स्थिर होने पर repository-mandated suites। |

हर command, वह किस risk को cover करती है, revision/pending state, executed result और
remaining failures बताएँ। Linter/typechecker न हो तो reason के साथ **unavailable** या
**not applicable** लिखें; pass न गढ़ें। Example में नाम होने भर से नया tool install न करें।
Green lint run behavior tests का विकल्प नहीं।

Iteration में सबसे संकीर्ण सार्थक target चुनें। Exercised code, inputs या relevant
environment न बदले हों तो पहले पास हुआ check फिर जरूरी नहीं। कोई ठोस unresolved coupling
या required project gate broader testing का आधार है; कारण दर्ज करें। Landing पर final
candidate के required aggregate checks एक बार चलाएँ। उसके बाद के बदलाव केवल affected
evidence और required commit gates को अमान्य करते हैं।

## 3. Tests को असली breakage पकड़ने दें

Observable effect assert करें: artifact मौजूद और valid है, real local database से data
पढ़ता है, host actual context bytes पाता है, या UI element render होता है। Local files,
databases और sockets exercise करें, उन्हें mock न करें। Metered external transport leaf
को deterministic fixture से बदल सकते हैं, जबकि request construction, routing, parsing
और local consumer वास्तविक रहें। Fixture से external service चलने का दावा कभी न करें।

[red-first](../red-first/SKILL.md) की sealed RED file byte-identical रखें। नया gap
मिले तो उस skill के evidence और sealing नियमों के अनुसार अलग supplemental
regression file जोड़ें। Original sealed file को कभी कमजोर, rename, replace
या edit न करें।

## Exit

Candidate scope, executed lint/type/test results, real side-effect evidence और
unresolved gates उसी owner को लौटाएँ।
[clean-code-gauntlet](../clean-code-gauntlet/SKILL.md) इसे अपना first stage evidence
मानता है; unchanged checks फिर चलाने की वजह नहीं।
