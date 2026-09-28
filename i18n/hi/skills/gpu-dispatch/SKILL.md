---
name: "gpu-dispatch"
description: "तब इस्तेमाल करें जब local models GPUs पर dispatch करने हों — inference का काम schedule करना, card चुनना या model residency सँभालना; हर GPU पर एक model, system RAM में कोई spill नहीं, loop भर warm रखो, loop के अंत में unload करो, दाख़िला नापे हुए सच से। Trigger words: gpu, vram, gpu dispatch, model loading, keep alive, resident model, local inference, spill, warm, कार्ड, गरम रखो, लोकल मॉडल."
license: "MIT"
---

# GPU Dispatch Law
**Effort:** free — dispatcher से लागू नियम, node की अपनी live state से पढ़े हुए; लागत सीधे घटाता है। हटाता है: VRAM से छलके runs जो चुपचाप 10x धीमे चलते हैं, jobs के बीच cold-start की खटपट, और मान लिए गए fences से खाली बैठे cards।

GPUs पर local models चलाने के चार नियम। ये इसलिए हैं क्योंकि दो आम failure
modes एक-दूसरे के उलट हैं और बराबर महँगे: loads और spills से cards को रौंदना,
और hardware पर इतनी बाड़ लगाना कि वो बेकार बैठा रहे। दोनों खोई हुई capability
हैं। इन्हें dispatcher में code की तरह लागू करो — कभी ऐसे नियम की तरह नहीं जो
model को याद रखना पड़े।

## कब चलाएँ

- किसी भी inference job को local GPU पर dispatch करने से पहले।
- कोई dispatcher, scheduler या model router design या review करते समय।
- जब कोई local run रहस्यमय ढंग से धीमा हो, या कोई card रहस्यमय ढंग से "unavailable"।

## चार नियम

1. **हर card पर एक model resident, एक समय पर।** किसी भी dispatch से पहले, node
   की live loaded-model हालत runtime के अपने API से पढ़ो। कोई दूसरा model
   resident है, तो या उसे इस्तेमाल करो या पहले unload करो। उसके बग़ल में दूसरा
   model कभी मत लादो।
2. **System RAM में spill नहीं — abort, धीमा run नहीं।** Dispatch से पहले जाँचो
   कि model card की खाली VRAM में पूरा समाता है, और काम के दौरान assert करो कि
   वो पूरी तरह VRAM में ही है। System RAM में कोई भी spill एक ABORT है, degraded
   run नहीं — spill हुआ model चुपचाप 10x धीमा होता है और अपने पीछे के हर job को
   ज़हर देता है। जो model card के reserved floor के ऊपर नहीं समाता, वो उस card
   पर dispatch नहीं होता; छोटा model चुनो या दूसरा card।
3. **पूरे work loop के लिए card warm रखो।** Model को एक सीमित keep-alive के साथ
   resident रखो — एक floor और ceiling जो आप configure करते हैं, कभी unlimited
   नहीं — और loop चलते हुए उसे refresh करो। एक ही loop के jobs के बीच cold-start
   की खिचखिच नहीं।
4. **Unload सिर्फ loop पूरा होने पर।** Loop के अंत में explicit release — हर job
   के बाद नहीं। हर-job unload cold-start खिचखिच है; कभी unload न करना leak है।
   Loop-end release ही सही seam है।

## दाख़िला नापे हुए सच से

कोई card काम ले सकता है या नहीं, यह live नाप तय करती है, कभी धारणा नहीं:

- Node की **असली probe** — config में पड़ा बासी "unreachable" नोट नहीं।
- Card के reserved floor के ऊपर **असली खाली VRAM** — floor ही इकलौती स्थायी
  सीमा है; उसके ऊपर सब कुछ इस्तेमाल के लिए आज़ाद है।
- Interactive workloads के लिए **असल चलती process की जाँच।** Card पर चलता हुआ
  game, stream या editing session फ़ौरन जीत जाता है — पर उसकी मौजूदगी नापी जाती
  है, किसी marker file या hardcoded "cold" सूची से मानी नहीं जाती।

Fail-closed defaults, "unknown purpose" वाले इनकार, और ऐसी marker files जिनकी
ग़ैरमौजूदगी का मतलब "बाड़ चालू" हो — सब एक ही bug हैं: runtime उस hardware को
ठुकरा रहा है जो इंसान का अपना है। अपने ही hardware पर ज़्यादा बाड़ लगाना खोई हुई
capability है, और खोई capability एक defect है। बाड़ सिर्फ इंसान का live शब्द
लगाता या हटाता है।

## सख़्त नियम (क्या इस skill को fail करता है)

- ऐसे card पर दूसरा model लादना जिस पर पहले से एक resident है।
- VRAM spill पकड़ने के बाद abort की जगह run जारी रखना।
- Unbounded keep-alive, या एक loop के अंदर jobs के बीच unload करना।
- Live probe की जगह config नोट, marker file या धारणा के आधार पर card को मना करना।
- इनमें से कुछ भी dispatcher के code की जगह prompt से लागू करना।

## इनके साथ अच्छा चलता है

- [invariant-floor](../invariant-floor/SKILL.md) — नापा हुआ सच और ज़ोरदार
  failures floor के क़ानून हैं; यह skill उन्हें GPUs पर लागू करती है।
- [fleet-ladder](../fleet-ladder/SKILL.md) — पहले resolve करो कौन सा model
  dispatch होगा, फिर तय करो कहाँ चलेगा।
- [bounded-loops](../bounded-loops/SKILL.md) — वो work loop जिसके दायरे में
  keep-alive और loop-end release बँधे हैं।
