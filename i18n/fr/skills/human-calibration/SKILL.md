---
name: human-calibration
description: "Quand un choix de build, design, communication ou UX important exige de connaître les préférences exprimées et le contexte de travail de l'opérateur."
license: MIT
---

# Connaître son humain

Applique la demande actuelle et les corrections de l'opérateur. Utilise les
preuves de ses préférences de travail pour choisir explications utiles, suivi
d'avancement et compromis de design. Cette connaissance est un contexte révisable,
jamais une personnalité fixe ni une permission.

## Un seul passage de profil

[operator-essence](../operator-essence/SKILL.md) possède le fichier privé de
contexte et ses preuves. Réutilise son extrait actuel depuis
[Build Flow](../backs-build-flow/SKILL.md). S'il manque, lance une fois le workflow
d'insights disponible de ce skill, évalue rapport/historique fournis et crée un
contexte provisoire si les preuves sont rares. Ne relance pas la collecte depuis chaque skill en aval.

Un profil existant désigné par l'opérateur peut apporter des preuves : conserve
source, date, statut de confirmation et incertitude en le rapprochant de l'essence.
Ne fouille pas d'autres profils et ne déduis pas le propriétaire d'un fichier d'un
nom affiché. Garde les informations personnelles hors du code public du plugin.
Une tâche en lecture seule peut transmettre un extrait en mémoire sans écrire de profil.

## Appliquer ce qui est connu

- Les préférences actuelles explicites et les corrections priment sur les
  observations passées. Faits du projet et contrôles d'acceptation restent à vérifier.
- Distingue choix observés et tendances inférées. Un design rejeté ou une demande
  répétée de suivi étaye une adaptation précise ; cela n'établit ni personnalité,
  identité, compétence, ni tolérance générale au risque.
- Utilise le plus petit extrait pertinent : préférence ou observation, preuve,
  adaptation proposée et incertitude. Montre son origine à l'opérateur.
- Préserve les deux côtés d'une vraie tension, telle que profondeur du contexte
  et vitesse d'exécution. Résous-la par une condition concrète de préparation
  et des preuves, sans réduire l'objectif.
- Une question facultative peut résoudre une inconnue importante de goût ou de
  communication. Fais d'abord le travail utile autorisé. N'exige ni questionnaire
  ni reconfirmation de préférences déjà données simplement parce qu'une nouvelle session commence.
- Note corrections et contre-exemples lorsque l'écriture du profil est autorisée.
  Une correction actualise le contexte ; elle ne réécrit pas silencieusement la
  tâche et n'autorise pas des actions sans rapport.

## Résultat

Rends un extrait concis au responsable existant. L'utilisateur peut le consulter
et le corriger. Adapte communication et collecte de preuves ; conserve les mêmes
exigences factuelles, de qualité et d'autorisation pour chaque opérateur.

## Marche bien avec

- [operator-essence](../operator-essence/SKILL.md) — preuves privées et initialisation par insights.
- [human-voice](../human-voice/SKILL.md) — communication claire dans le registre demandé.
- [intent-compiler](../intent-compiler/SKILL.md) — transformer le langage ambigu en contrat d'action.
- [operator-intent-deduction](../operator-intent-deduction/SKILL.md) — résoudre les choix depuis l'intention actuelle.
