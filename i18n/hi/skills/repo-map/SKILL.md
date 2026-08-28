---
name: "repo-map"
description: "बिना index वाले cold repo में पहली session पर लगाओ, और जब भी map बासी हो जाए। Tree को एक बार walk करता है, repo root पर एक CODE_MAP.md लिखता है, और हर अगली session को पहले map पढ़वाता है — पहले map, raw walk तभी जब map के पास जवाब न हो। Trigger words: repo map, code map, map first, map-first, index the repo, cold repo, stale map, refresh the map, repo का नक्शा, code map बनाओ, repo index करो, map ताज़ा करो."
license: "MIT"
---

# Repo Map
**Effort:** light — पहली बार एक walk, उसके बाद लगभग मुफ़्त। हटाता है: हर session में agent का repo की शक्ल फिर से निकालना — बिना index वाले repo का सबसे बड़ा latency और token tax।

Indexed codebase “X कहाँ रहता है” का जवाब मुफ़्त देता है। ज़्यादातर repos में index
नहीं होता, इसलिए हर session वही tax देती है: tree walk करो, layout फिर खोजो, session
ख़त्म होते ही सब भूल जाओ। यह skill वह tax एक बार देती है। Tree को एक बार walk करो,
जो सीखा उसे एक map file में लिखो, और हर अगला सवाल walk से पहले map पढ़े।

## कब चलाएँ

- Cold repo की पहली session में — जहाँ map और index दोनों नहीं हैं।
- जब भी map बासी हो जाए (नीचे की staleness rule देखो)।

## क़दम

1. **Tree को एक बार walk करो।** असली structure पर एक pass: directories, entry
   points, और कौन-सी चीज़ कहाँ रहती है। Repo को यही एक पूरा walk चाहिए होना चाहिए।
2. **Repo root पर एक `CODE_MAP.md` लिखो।** इसमें हों:
   - entry points — execution कहाँ शुरू होता है;
   - sections और seams, हर एक का एक-line purpose;
   - tests कहाँ रहते हैं;
   - build, run और test commands;
   - hot paths — history से seed करो (`git log --name-only` की frequency), या
     खाली छोड़ो ताकि आगे की sessions भरें।
3. **इसे lean रखो।** यह map है, documentation नहीं। हर fact की एक line। Entry
   paragraph बनने लगे तो वह doc बन रही है — उसे pointer तक काट दो।
4. **Tree की shape दर्ज करो।** Map में एक सस्ता fingerprint रखो:
   `git ls-files | sha256sum` (adds, moves और renames पकड़ता है), ताकि अगली
   session जान सके कि shape बदली या नहीं।

## Map-first law

Research, wayfinding और plays tree walk करने से पहले map पढ़ते हैं। Raw walk तभी
fallback है जब map के पास जवाब न हो — और walk जो सीखता है वह session आगे बढ़ने से
पहले map के अंदर लिखा जाता है। Map हर walk को absorb करता है। Re-derivation की क़ीमत
एक बार, हर session में नहीं।

## Staleness rule

Map तभी refresh करो जब tree की shape बदली हो — recorded state के बाद files add,
move या rename हुई हों। Stored fingerprint (`git ls-files | sha256sum`) को live
tree से मिलाओ। Timer पर कभी refresh मत करो। हर session में कभी refresh मत करो।
Schedule पर दोबारा बना map बस per-session tax का नया नाम है।

## Hard rules

- **Facts और locations, opinions कभी नहीं।** “Auth `src/auth/` में है” map में
  आता है; “auth code गंदा है” नहीं।
- **Dead pointer मिलते ही मरता है।** जो path अब resolve नहीं होता, उसे वहीं fix
  या cut करो। झूठा map, बिना map से बदतर है।
- **Map में secrets कभी नहीं।** कोई keys, tokens, credentials या private hostnames
  नहीं। यह tracked file है; वैसा ही व्यवहार करो।

## इनके साथ अच्छा चलता है

- [live-research](../live-research/SKILL.md) — researcher पहले map, फिर source पढ़ता है।
- [wayfinder](../wayfinder/SKILL.md) — charting cold walk से नहीं, map से शुरू होती है।
- [session-handoff](../session-handoff/SKILL.md) — map handoff का वह हिस्सा है जिसे हर session साझा करती है।
