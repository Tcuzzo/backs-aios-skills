---
name: "design-taste"
description: "तब इस्तेमाल करें जब कुछ भी visual बनाना हो — site, app, dashboard, console या deck — ताकि वो generic AI defaults की जगह असली taste के साथ ship हो। Trigger words: design, UI, taste, design tokens, design system, accessibility, WCAG, screenshot critique, dark mode, restyle, डिज़ाइन, रूप-रंग, सौंदर्य, सुलभता, स्क्रीनशॉट समीक्षा."
license: "MIT"
---

# Design Taste — पहले Tokens, नज़रें खुली, Accessibility सख़्त
**Effort:** light — किसी भी component से पहले एक token file, साथ में हर rendered surface पर एक screenshot → vision-critic pass। हटाता है: generic AI defaults को फिर से ship करना — restyle का rework और ship के बाद की accessibility retrofit।

Generic UI एक workflow bug है, model bug नहीं। इसे ढाँचे से ठीक करो: brief को
spec की तरह पढ़ो, किसी भी component से पहले exact design tokens तय करो, defaults
को नाम लेकर मना करो, builder को screenshot loop से आँखें दो, और accessibility
पर gate लगाओ — सख़्त।

## कब चलाएँ

- कोई भी "मुझे … बना दो / design कर दो" वाली माँग जो pixels render करती है।
- कोई frontend या customer-facing deliverable scaffold करने से पहले।
- जब कोई मौजूदा surface generic दिखे और उसे एक specific, बचाव-योग्य दिशा चाहिए।

## कदम

1. **Brief को spec की तरह पढ़ो।** इंसान के शब्दों में कोई रूपक, कोई लय, कोई नामित
   दौर, कलाकार या जगह एक ठोस design constraint है, सजावट नहीं। पूरी
   read-the-brief discipline: [intent-compiler](../intent-compiler/SKILL.md)।
2. **ज़मीन से जुड़ी दिशा चुनो।** एक *lead* reference चुनो (कोई असली design system
   या library जो structural baseline तय करे) और एक *accent* reference (जो ऊपर से
   अपनी छाप लगाए)। दोनों असली और current होने चाहिएँ, verify होने लायक taste
   signature के साथ। गढ़ी हुई vibe gate को बंद करके fail होती है।
3. **सबसे PEHLE tokens निकालो।** किसी भी component से पहले एक machine-readable,
   तीन-स्तर की design-token file लिखो (primitive → semantic → component; W3C
   token format, `$value` + `$type`)। शुरू में ही तय करो: perceptually एकसार
   color ramp (Oklch — एक color space जहाँ बराबर क़दम बराबर दिखते हैं), किसी
   non-default typeface पर असली type scale, एक spacing increment (4px base →
   4/8/12/16/24/32/48/64), एक radius scale, एक elevation scale, और नामित motion
   tokens (हर enter / scroll / state change के लिए duration + easing;
   `prefers-reduced-motion` का सम्मान)। Dark और light दोनों first-class हैं और
   दोनों एक ही (SAME) semantic tokens से निकलते हैं।
4. **Generic defaults को नाम लेकर मना करो।** मनाही adjectives से ज़्यादा असर
   करती है: default-आदत वाला font नहीं (Inter/Roboto), purple gradients नहीं,
   centered hero नहीं, तीन-बराबर-card वाली row नहीं, gray-on-white slab नहीं।
   हर project में अपनी banned list जोड़ो।
5. **पाबंदी में बनाओ।** Components सिर्फ tokens खाते हैं। Component के अंदर
   hardcoded raw hex, px या font family एक defect है।
6. **Screenshot → vision-critic loop बंद करो।** जो भी render होता है: उसे
   headless browser में mobile और desktop चौड़ाइयों पर render करो, screenshot
   लो, और किसी vision model से score करवाओ — फिर ठीक करो, अलग-अलग passes में
   (critique → structural fix → audit → polish), कभी one-shot नहीं। Critic एक
   grader है: builder से अलग family का model, नामित axes पर score, कभी एक
   holistic score नहीं। Critic model को call के वक़्त config से resolve करो —
   pinned model id एक दिन retire होती है और पूरा loop साथ ले डूबती है।
7. **8-axis taste rubric पर score दो।** हर axis पर 0–3, और हर axis का score ≥ 2
   होना ही चाहिए: token-adherence · layout/hierarchy · typography ·
   color/contrast · motion · dark-light parity · accessibility ·
   designed-vs-mean gut check ("यह designed दिखता है, या सबका average?")।
   एक भी axis 2 से नीचे = काम पूरा नहीं।
8. **Accessibility का HARD gate लागू करो (WCAG 2.2)।** Pointer targets ≥ 24×24
   CSS px. दिखता हुआ focus indicator ≥ 2px perimeter, ≥ 3:1 contrast पर। Text
   contrast ≥ 4.5:1 सामान्य, ≥ 3:1 बड़े text और UI components पर। पूरी तरह
   keyboard से चलने लायक। Contrast DONO themes में verify। यह gate है, सुझाव
   नहीं: fail = ship नहीं।
9. **Pixels के पीछे के code को test करो।** Token resolvers, theme switches,
   contrast calculators और state reducers को असली rendered DOM पर असली tests
   मिलते हैं — contrast जाँच में उलटी तुलना एक ख़ूबसूरत screen ship कर देती है
   जो चुपचाप inaccessible है। Tests code को परखते हैं; rubric और WCAG gate
   taste को।

## सख़्त नियम — इनमें से कोई एक भी टूटा तो skill fail

- Token file बनने से पहले लिखा गया component।
- Component के अंदर raw hex / px / font family।
- Banned-defaults सूची की कोई भी चीज़ output में दिखना।
- जो भी render होता है उस पर screenshot → critic loop छोड़ देना।
- Builder का अपने ही visuals grade करना, या axes की जगह एक holistic score।
- Ship के वक़्त कोई rubric axis 2 से नीचे, या कोई WCAG 2.2 जाँच fail।
- ऐसी taste दिशा जो किसी असली, verify होने लायक reference पर टिक न सके।

## इनके साथ अच्छा चलता है

- [intent-compiler](../intent-compiler/SKILL.md) — पूरी read-the-brief discipline.
- [blind-eval](../blind-eval/SKILL.md) — जब सवाल taste हो, तब keep-or-revert.
- [clean-code-gauntlet](../clean-code-gauntlet/SKILL.md) — pixels के पीछे के code की hardening.
- [blind-tribunal](../blind-tribunal/SKILL.md) — उतरने से पहले cross-family grading.

> Scaffold credit: W3C Design Tokens Community Group (token format); WCAG 2.2, W3C
> (accessibility gate); UICrit, UIST 2024 (axis-scored UI critique); AI Jason, &
> JackJack. (2025). superdesign: AI design agent [Computer software]. GitHub.
> https://github.com/superdesigndev/superdesign (AGPL-3.0; dual-licensed with a
> commercial enterprise license) — forbid-the-defaults. The composition and hard
> rules here are BACKS AIOS.
