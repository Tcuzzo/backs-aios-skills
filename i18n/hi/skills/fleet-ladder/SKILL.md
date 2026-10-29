---
name: "fleet-ladder"
description: "Dispatch से पहले role और capability के आधार पर चयन की प्रक्रिया; public pack में resolver या Fleet executable नहीं है। Trigger words: fleet, ladder, dispatch, fallback, model down, provider down, which model, availability, कौन सा model, सीढ़ी, विकल्प क्रम, उपलब्धता."
license: "MIT"
---

# Fleet Ladder
**Effort:** light — किसी भी dispatch से पहले rung की एक cached live probe। हटाता है: मरे हुए providers को गए dispatches, और call sites पर hardcode हुए model नाम जो model के retire होते ही टूट जाते हैं।

यह skill चयन का तरीका बताती है, स्वयं model resolve नहीं करती। Public pack में resolver या Fleet executable नहीं है; आवश्यक runtime सुविधा गायब हो तो उसे gap के रूप में बताएं। Skills, prompts या call sites में model IDs hardcode न करें।

## कब चलाएँ

- किसी model को KOI भी dispatch करने से पहले: build, grade, review या bounded worker job.
- जब कोई provider down हो और जानना हो कि क्या किस पर गिरता है।
- जिस पल आप code या prompt template में model का नाम टाइप करते खुद को पकड़ें।

## कदम

1. **Role और ज़रूरी capabilities तय करें।** Configured ladder और उसका क्रम पढ़ें; काम, क्षमता और उपलब्धता के आधार पर उपयुक्त उम्मीदवार चुनें। Example config केवल template है। यह skill खुद candidates को rank या filter नहीं करती।
2. **स्वतंत्रता जांचें।** Review एक नई author से अलग execution में, author के context से रहित frozen packet पर करें। यदि configured runtime अनुमति दे तो वही सक्षम model या family इस्तेमाल हो सकती है। अतिरिक्त runtime पाबंदी को gap के रूप में बताएं।
3. **असली inference जांचें।** Model list inference, क्षमता या quota का प्रमाण नहीं है। चुने हुए उम्मीदवार पर वास्तविक bounded inference चलाएं; परिणाम उचित अवधि के लिए cache करें और backoff रखें। Fallback पर क्षमता फिर जांचें।
4. **नीचे उतरो, ज़ोर से।** सबसे अच्छे AVAILABLE पायदान पर dispatch करो। Transport
   failure पर failure को ज़ोर से report करो, फिर अगला पायदान आज़माओ। चुपचाप skip
   कभी नहीं — record में दिखना चाहिए कौन से पायदान fail हुए और क्यों।
5. **ख़ात्मा ज़ोर से fail होता है।** हर पायदान down है, तो एक साफ़ error उठाओ जो
   बताए क्या-क्या आज़माया गया। जो job dispatch नहीं हो सकता वो कभी चुपचाप कामयाब
   नहीं होता, हमेशा के लिए इंतज़ार नहीं करता, न ही किसी गढ़े हुए जवाब पर उतरता है।
6. **Provenance log करो।** हर dispatch एक log में जोड़ो: role, चुना गया model,
   छोड़े गए पायदान और वजह। बाद में आपको जवाब देना आना चाहिए: "यह काम असल में
   किसने किया?"

## सख़्त नियम — एक भी टूटा तो skill fail

- Skills, prompts या call sites में model IDs hardcode न करें; सक्रिय config से role और आवश्यक capabilities लें।
- वास्तविक bounded inference ज़रूरी है; केवल catalog पर्याप्त नहीं।
- Review में नई author से अलग execution और author-context रहित frozen packet ज़रूरी है; अलग model या family न तो अनिवार्य है, न स्वतंत्रता का प्रमाण।
- Failures और fallback दर्ज करें; अनुपलब्ध resolver या isolation को runtime gap बताएं।


## इनके साथ अच्छा चलता है

- [blind-tribunal](../blind-tribunal/SKILL.md)
- [bounded-loops](../bounded-loops/SKILL.md)
- [model-fusion](../model-fusion/SKILL.md)
