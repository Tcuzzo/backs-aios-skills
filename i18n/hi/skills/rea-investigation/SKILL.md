---
name: rea-investigation
description: जब विफलता के निदान या सुधार के लिए ज़रूरी हो, प्रकाशित executable, package या देखे गए runtime व्यवहार की जाँच में REA इस्तेमाल करें।
license: MIT
---

# REA से आर्टिफैक्ट जाँच

प्रकाशित binaries, packages या अनुरोधित runtime व्यवहार की जाँच में स्थापित REA engine और उसकी अलग skill इस्तेमाल करें। सामान्य source repositories के लिए सीधे source और tests देखें। यह bridge REA, Ghidra, provider या MCP server स्थापित नहीं करता और उनकी उपलब्धता का दावा नहीं करता।

1. सटीक लक्ष्य और प्रश्न तय करें। Host के agent skill directory में स्थापित मूल REA skill और उसके ज़रूरी references पढ़ें; इस bridge को दोबारा चुनने से बचें। उपलब्ध न हो तो बताएं और उपलब्ध tools से उपयोगी जाँच जारी रखें।
2. जुड़े हुए REA tools उपलब्ध हों तो उनका, अन्यथा स्थापित REA CLI का इस्तेमाल करें। समर्थित native binary के लिए मौजूदा compatible Ghidra provider इस्तेमाल करें; provider न मिले तो बताएं, नतीजे न गढ़ें और बिना अनुमति dependencies स्थापित न करें।
3. केवल पढ़ने वाली static जाँच से शुरू करें। लक्ष्य की पहचान, evidence IDs, scope, सीमाएँ और अज्ञात बातें दर्ज करें। Static निष्कर्ष runtime व्यवहार साबित नहीं करते; live observation केवल उपयोगकर्ता के अनुरोधित scope और tool की घोषित execution तथा mutation सीमाओं में करें।
4. निष्कर्ष root-cause-first और repair-loop को दें। Open-source capability अपनाने के लिए absorb और उसके license तथा dependency checks चलाएं। Configured fleet-ladder से role और capability के आधार पर चयन करें; model IDs hardcode न करें। स्वतंत्र आकलन में blind-tribunal की नई, लेखक से अलग execution और लेखक की जानकारी हटाए हुए frozen packet का प्रयोग करें, host runtime की वास्तविक क्षमताओं के अनुसार।

Scaffold: REA by morluto, MIT license, https://github.com/morluto/rea.
Engine, मूल skill और providers अलग-अलग installations हैं।
