---
name: repair-loop
description: À utiliser pour corriger un bug, clore un problème signalé, ou uplifter une couture de bout en bout. Déroule la boucle de réparation complète — s'ancrer dans le socle, reproduire sur la vérité live, test de contrat rouge, fixer la classe à la couture, vérifier sur le vrai chemin, note indépendante, atterrir — et itère jusqu'à ce que ce soit vrai. Trigger words: repair loop, dev mode, fix this, uplift, close the seam, dev build, boucle de réparation, corrige ça, fermer la couture, répare.
license: MIT
---

# Repair Loop
**Effort:** light — la boucle elle-même est de la discipline plus une passe de notation indépendante ; les étapes plus lourdes qu'elle enchaîne (gauntlet, tribunal) portent leurs propres tampons et ne se déclenchent que sur les changements qui livrent. Élimine : les atterrissages verts-mais-cassés, et le rework de bug rouvert qu'ils coûtent.

La boucle par défaut pour tout fix, clôture de bug ou uplift. C'est un
comportement, pas une machinerie d'approbation : elle n'ajoute aucune barrière
et aucune friction pour l'humain. Elle lie l'agent à une discipline qui rend
« vert mais cassé » structurellement difficile à livrer.

## Charger d'abord, avant tout design ou toute édition

1. [invariant-floor](../invariant-floor/SKILL.md) — lis tes règles avant de travailler.
2. [human-calibration](../human-calibration/SKILL.md) — applique le profil de l'humain ; ne le ré-interroge jamais.
3. [understanding-gates](../understanding-gates/SKILL.md) — le planificateur diagnostique : Design → Plan → Build → Test → Ship.
4. [wayfinder](../wayfinder/SKILL.md) — quand tu es perdu, trace la route ; ne dépose jamais une question sur l'humain.
5. Si la demande arrive en prose ou en métaphore, passe d'abord par [intent-compiler](../intent-compiler/SKILL.md) et boucle sur la directive déduite.

## La boucle

1. **Ancre-toi dans le socle.** Charge les règles et la vérité propre du projet
   (docs, source, tracker) avant de toucher au code. Le travail fait de mémoire
   des règles ne compte pas.
2. **Reproduis sur la vérité live.** Vois l'échec toi-même, sur le vrai chemin
   que l'humain utilise — pas une sonde proxy, pas la parole du rapport de bug.
   Pas de reproduction, pas de fix.
3. **Test de contrat rouge.** Écris un test en échec qui capture le défaut, et
   committe-le avant le fix. Prouve qu'il est vraiment rouge. Le fix le fait
   passer au vert ; le fix n'édite jamais le test. Voir
   [red-first](../red-first/SKILL.md).
4. **Fixe la CLASSE à la couture** — pas un patch ponctuel par symptôme. La
   formule complète vit dans [seam-engineering](../seam-engineering/SKILL.md).
5. **Vérifie sur le vrai chemin.** Fais confiance mais vérifie. La capacité se
   prouve sur la surface propre de l'humain — l'interface où il tape, la
   commande qu'il lance — jamais sur un test vert par-dessus une couture
   mockée. Vérifie chaque affirmation (« l'autre branche l'a atterri », « ce
   service est down ») contre la vérité live avant d'agir dessus.
6. **Mesure le fix.** En cours de boucle, ne lance que les tests qui couvrent
   la couture que tu as touchée — voir [sniper-testing](../sniper-testing/SKILL.md).
   Puis passe le [clean-code-gauntlet](../clean-code-gauntlet/SKILL.md) sur le
   code modifié : tests ciblés, score complexité-contre-couverture, tests de
   mutation bornés. Un mutant qui survit à ton fix veut dire que le test n'a
   jamais atteint la branche que tu as changée — faux vert ; continue d'itérer.
7. **Note indépendante.** Un correcteur qui n'a pas écrit le changement —
   idéalement un modèle d'une autre famille que le builder — doit le valider.
   Le builder ne note jamais son propre travail. Voir
   [blind-tribunal](../blind-tribunal/SKILL.md).
8. **Vérifie le travail concurrent.** Avant de modifier un état partagé,
   vérifie que le travail en vol des autres sessions est préservé (sur une
   branche ou un commit). Ne committe et ne nettoie jamais du travail qui n'est
   pas le tien.
9. **Atterris.** Une passe complète sur les suites des modules touchés à
   l'atterrissage, puis committe. Clos chaque constat que la boucle a fait
   remonter sur cette couture — ou enregistre un verdict « pas un bug »
   explicite et étayé par constat. « Fixé le gros, reporté le reste »
   n'atterrit jamais.

## Itère jusqu'à ce que ce soit vrai

Une règle pas encore satisfaite n'arrête pas la boucle — elle la propulse.
Escalade le modèle ou le palier, lève le blocage, réessaie, jusqu'à ce que
chaque étape ci-dessus soit vraie et que le changement atterrisse. « Assez
bien » n'est pas un statut. Si tu es vraiment coincé deux fois sur la même
couture, logge les preuves exactes du blocage et passe au morceau suivant non
bloqué — ne mouline jamais en silence.

## Règles dures — une seule suffit à faire échouer le skill

- Fix livré sans reproduction sur la vérité live.
- Test écrit après le fix, ou édité par le fix.
- Symptôme rafistolé pendant que la classe reste ouverte à la couture.
- Capacité déclarée verte sur un proxy pendant que le chemin propre de l'humain
  est cassé.
- Builder qui a noté son propre changement.
- Un constat remonté puis reporté en silence à l'atterrissage.
- Boucle abandonnée à « assez bien » au lieu d'escaladée.

## Rapport

Deux mots — **PROVEN** ou **STILL-BUILDING** — plus l'intention en langage
simple et l'unique décision posée devant l'humain, s'il y en a une. Les
questions ne vont à l'humain que pour le goût, la vision, ou le risque
destructeur ; voir [decision-bar](../decision-bar/SKILL.md).

## Fonctionne bien avec

- [incident-closure](../incident-closure/SKILL.md) — quand l'humain signale une casse, cette boucle tourne dans une clôture complète.
- [red-first](../red-first/SKILL.md) · [seam-engineering](../seam-engineering/SKILL.md) · [sniper-testing](../sniper-testing/SKILL.md)
- [blind-tribunal](../blind-tribunal/SKILL.md) · [clean-code-gauntlet](../clean-code-gauntlet/SKILL.md)
