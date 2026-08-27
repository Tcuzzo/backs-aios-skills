# Play: Parallel Work

Agents के बीच काम कैसे बाँटें कि वे एक-दूसरे को रौंदें नहीं। वह एक नियम जो बाक़ी
सबकी क़ीमत चुकाता है: write की spine एक, readers कई।

## कब चलाएँ

- कोई task research, scanning, testing, या grading में बँटता है जो एक साथ चल सकते
  हैं।
- एक ही window में एक से ज़्यादा agents एक ही repository को छूने वाले हैं।
- मन कर रहा है कि दो agents parallel में code लिखें। पहले यह पढ़ लें।

## चेन

1. [leap-protocol](../skills/leap-protocol/SKILL.md) — किसी भी agent के spawn होने
   से पहले काम को balls में तोड़ें: goals, specs, और सख़्त file scopes के साथ।
2. readers spawn करें, writers नहीं — subagents सिर्फ़ ऐसे read-heavy काम के लिए
   फैलाएँ जिनमें आपसी निर्भरता कम हो: research, test चलाना, security scans,
   grading। आपस में जुड़े code-लेखन के लिए कभी नहीं।
3. हर lane को अलग रखें — हर parallel agent को अपनी ALAG worktree मिले (उसी repo
   की एक अलग checkout)। तब टकराव merge पर असली merge conflicts बनकर सामने आते
   हैं — कभी उन silent overwrites की तरह नहीं जो बिना चेतावनी data खा जाते हैं।
4. [clean-code-gauntlet](../skills/clean-code-gauntlet/SKILL.md) — हर lane, land
   माँगने से पहले, अपनी ही worktree के अंदर अपना quality gauntlet चलाती है। पहले
   dry-run, ताकि lane को अपनी लागत पता हो। कोई lane दूसरी lane के green पर land
   नहीं होती।
5. [blind-tribunal](../skills/blind-tribunal/SKILL.md) — review करने वाले agent को
   एक साफ़ context मिले, कभी लेखक वाला नहीं। साझा context सड़ता है और खुद से ही
   सहमत हो जाता है।
6. एक बार में एक lane merge करें, एक अलग merge workspace में, exit code से
   test-gated।

## तालमेल के नियम

- हर workspace में code एक ही agent लिखता है, एक सुसंगत context में। parallel
  writers ऐसे टकराते हुए अनकहे फ़ैसले लेते हैं जिन्हें कोई merge नहीं सुलझा सकता।
- हर agent की file ownership पहले से घोषित करें। हर agent सिर्फ़ अपनी नामी files
  edit करता है।
- तालमेल किसी tracker से करें (issues, tickets) — working tree की किसी साझा
  checklist file से कभी नहीं। वह file खुद merge-conflict की सतह है और दो agents
  को एक ही task उठवा देती है।
- हर subagent एक निचोड़ा हुआ सार लौटाता है — मुख्य तथ्य, फ़ैसले, खुले मुद्दे, एक-दो
  पन्ने — कभी अपना पूरा transcript नहीं।
- plan, spec, और फ़ैसलों को disk पर लिखें और दोबारा पढ़ें। लंबे runs context
  compact करते हैं और निर्देश चुपचाप गिरा देते हैं; जो नियम हमेशा लागू रहने हैं,
  वे always-loaded file में रहते हैं — और कहीं नहीं।

## Merge का अनुशासन

- हर merge को land होने से पहले exit code से test-gate करें। red suite merge रोक
  देती है। अकेला यही नियम agent से होने वाले ज़्यादातर टूट-फूट काट देता है।
- merge एक अलग merge workspace में करें, फिर नतीजे को stat-verify करें: file
  counts, diffstat, हर lane की नामी files मौजूद। जो merge किसी lane की files
  चुपचाप गिरा देता है, वही सबसे बड़ा गुनाह वाला ख़राब merge है — हर बार उसकी जाँच
  करें।

## Hard gates — कोई एक भी टूटा तो play fail

- एक ही workspace में एक ही समय पर दो agents code लिख रहे हैं।
- कोई lane अपनी घोषित file scope के बाहर edit कर रही है।
- कोई merge बिना green exit code के, या बिना stat-verification के land हुआ।
- कोई reviewer जिसने लेखक के साथ context साझा किया।
- कोई lane दूसरी lane के test नतीजों पर land हुई, या जिस seam को बदला उसी को mock
  कर दिया।

**Weight:** design से ही heavy — leap विभाजन, हर lane पर एक gauntlet, और एक clean-context tribunal — खर्च तभी वसूल होता है जब काम बाँटने लायक़ बड़ा हो, और यह play चलाने का बस वही एक मौक़ा है।
