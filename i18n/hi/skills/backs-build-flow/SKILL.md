---
name: backs-build-flow
description: "जब build, fix, review, resume या delivery में context, skills और verification का समन्वय करते हुए काम आगे बढ़ाना हो, तब उपयोग करें।"
license: MIT
---

# BACKS Build Flow

एक integration owner अनुरोध को context से सत्यापित delivery तक ले जाता है।
विशेषज्ञ skills उसी owner को evidence लौटाती हैं; वे workflow दोबारा शुरू नहीं करतीं।
साधारण उत्तर में build या investigation न हो, तो केवल संबंधित चरण अपनाएँ।

## कार्रवाई के लिए पर्याप्त context जुटाएँ

1. उपयोगकर्ता का उद्देश्य, सीमाएँ, मौजूदा authorization और माँगा गया परिणाम बनाए रखें।
   mode चुनें: **build/fix**, **read-only review**, **investigate**, या **resume/deliver**।
   Review अपने आप edits, install या deployment की अनुमति नहीं देता।
2. वर्तमान task packet दोबारा उपयोग करें। वह न हो तो
   [context-engineer](../context-engineer/SKILL.md) से target, लागू instructions,
   प्रभावित caller/consumer path, मौजूदा काम और acceptance check सत्यापित करें।
   [building-with-backs](../building-with-backs/SKILL.md) checkout और promotion का
   रास्ता तय करता है। बदलाव से पहले का `base_sha` स्थिर रखें; commits के साथ
   `candidate_sha` अपडेट करें।
3. वर्तमान operator के लिए [operator-essence](../operator-essence/SKILL.md) अपनाएँ:
   प्रासंगिक awareness slice लोड करें, या profile न होने पर उसका insight bootstrap
   एक बार चलाएँ। गुणात्मक observations और मात्रात्मक evidence communication और
   verification को दिशा देते हैं; वे अधिकार नहीं देते और स्थायी persona नहीं बनाते।
   कम evidence को provisional लिखें और उपयोगी अधिकृत काम जारी रखें। अस्पष्ट intent के
   लिए ही [intent-compiler](../intent-compiler/SKILL.md) लें;
   [operator-intent-deduction](../operator-intent-deduction/SKILL.md) तय करता है कि
   कोई महत्वपूर्ण अनसुलझा चुनाव वास्तव में operator से पूछना जरूरी है या नहीं।
4. **जब target, अगली ठोस कार्रवाई, सीमाएँ और देखा जा सकने वाला acceptance check बता
   सकें, काम शुरू करें।** आगे की पढ़ाई किसी ऐसे स्पष्ट सवाल का उत्तर दे जो उस कार्रवाई
   को बदल सकता हो। बार-बार पूरे repo का नक्शा न बनाएँ।

## हर skill को एक बार जोड़ें, output और exit के साथ

वास्तविक संबंधित skill bodies पढ़ें; केवल नाम या receipt application नहीं है। Context में
मौजूद और अभी भी सही bodies तथा evidence दोबारा उपयोग करें। Compaction के बाद केवल
अगली कार्रवाई की जरूरत वाली सामग्री फिर पढ़ें। हर specialist का उद्देश्य, अपेक्षित
 evidence और exit condition बताएँ; गहरे references जरूरत पर पढ़ें। एक वर्तमान task
packet ownership, state और next action रखता है
([packet और handoff format](references/task-packet.md))। दूसरा ledger न बनाएँ।

Adoption में [absorb](../absorb/SKILL.md) capability mapping और native integration
का owner है। [rea-investigation](../rea-investigation/SKILL.md) जरूरत पर discovery
या verification evidence देता है; वह caller को लौटता है, Absorb को फिर शुरू नहीं करता।
सामान्य source कार्य में सीधे source और tests उपयोग करें।

## सीमाबद्ध RED → GREEN loop चलाएँ

Retries से पहले [bounded-loops](../bounded-loops/SKILL.md) लागू करें: एक
`mission_id`, deadline, attempt/round allowance और शेष resource budget। Child
workers, model changes, repair findings और review rounds इसी allowance से खर्च होते हैं।

1. **RED:** [red-first](../red-first/SKILL.md) fix से पहले वास्तविक failing behavior
   check बनाता है। उसकी sealed file और baseline identity सुरक्षित रखें। Review या
   research task में उसका evidence contract उपयोग करें; अनावश्यक edits न गढ़ें।
2. **Build:** owning seam पर सबसे छोटा पूर्ण बदलाव करें; प्रभावित consumers और
   compatibility surfaces अपडेट करें। असंबंधित काम सुरक्षित रखें।
3. **Lint और test:** [sniper-testing](../sniper-testing/SKILL.md) `base_sha` से
   current candidate तक, संबंधित pending work सहित, scope निकालता है। Repo के लागू
   lint, format-check, typecheck और behavior tests चलाएँ। सटीक commands, revision,
   results तथा unavailable या inapplicable checks दर्ज करें। Clean working tree से
   committed scope मिटता नहीं है।
4. **Quality:** [clean-code-gauntlet](../clean-code-gauntlet/SKILL.md) उसी scope और
   budget में measured quality, सीमाबद्ध isolated mutation और independent review
   चलाता है। नए gaps के लिए supplemental tests जोड़ें; sealed RED न बदलें।
5. **Evidence पर कार्रवाई:** सिद्ध finding ठीक करें और केवल प्रभावित checks फिर चलाएँ।
   वही failure दोहरने पर hypothesis या तरीका बदलना जरूरी है। Limits समाप्त होने पर
   अधूरा काम checkpoint करें; budget reset या checks कमजोर कभी न करें।

Candidate स्थिर होने पर repo के आवश्यक aggregate landing gates चलाएँ। इस host की
वास्तविक क्षमताएँ बताएँ; tools, tests या reviews गढ़ें नहीं।

## माँगा गया परिणाम पूरा करें

जब अनुरोध में हों, तो अधिकृत packaging, commit, publication और verification तक
जारी रहें। वास्तव में जरूरी external approval माँगने से पहले पूरा reviewable result
तैयार करें। Findings, वर्तमान कार्रवाई, evidence और live work देखने की जगह बताते
रहें; updates की उपयोगकर्ता की पसंदीदा गति अपनाएँ।

**माँगा गया task delivered** और invariant floor की **PROVEN** capability status
अलग रखें। Local patch या read-only review पूरा होने से live deployment सिद्ध नहीं होता।
Failed या unavailable आवश्यक gates स्पष्ट रखें: सटीक blocker, शेष allowance और next
 action के साथ **STILL-BUILDING** checkpoint करें। Read-only mode में packet response
या पहले से अधिकृत external task record में लौटाएँ; अपने आप repo ledger या essence
file न बनाएँ।
