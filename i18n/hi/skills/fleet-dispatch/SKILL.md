---
name: "fleet-dispatch"
description: "जब कोई pack peer \"invoke skill fleet-dispatch\" भेजे, या यह agent अपने काम के लिए अपना fleet rung dispatch करे, तब इसका उपयोग करें। लोकल fleet resolver को कॉल करता है, FLEET_RECEIPT पढ़ता है और उत्तर को provenance के साथ लौटाता है। Model-agnostic: क्रम ladder तय करती है। Trigger words: fleet-dispatch, fleet rung, dispatch, role agent, role bot, invoke skill, fleet ladder. ट्रिगर शब्द: फ़्लीट डिस्पैच, fleet rung, skill invoke."
license: "MIT"
---

# फ़्लीट डिस्पैच

पूरी canonical गाइड लोड करें और उसका पालन करें। role और spec पढ़ें, लोकल fleet resolver को कॉल करें, और उत्तर तथा FLEET_RECEIPT दोनों साथ लौटाएँ। कभी model का नाम hardcode न करें, कभी resolver को bypass न करें; सब कुछ अंग्रेज़ी मूल के ठीक अनुसार चलता है।

[Canonical skill](../../../../skills/fleet-dispatch/SKILL.md)
