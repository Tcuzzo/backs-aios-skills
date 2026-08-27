---
name: red-first
description: À utiliser avant d'envoyer n'importe quel builder — un agent, un modèle, ou toi-même — faire un changement qu'un test doit prouver. Committe un test de contrat prouvé en échec avant le début du build, interdit au builder d'y toucher, et fait vérifier par un correcteur indépendant que le test n'a jamais été édité. Trigger words: red first, failing test first, contract test, red baseline, tamper-proof test, test before build, rouge d'abord, test en échec d'abord, test de contrat, base rouge, test inviolable, test avant build.
license: MIT
---

# Red-First, inviolable

Un test écrit après le fix ne prouve rien — il a été taillé pour passer.
Un test que le builder peut éditer prouve encore moins — on peut le tordre
pour qu'il passe. Donc le test vient d'abord, se fait verrouiller, et se fait
noter intact.

## Quand le lancer

Avant d'envoyer tout build ou fix où un test peut énoncer le comportement
voulu. C'est le défaut pour les corrections de bugs comme pour les nouvelles
capacités.

## Les étapes

1. **Écris le test de contrat en échec.** Il énonce le comportement que tu
   veux, sous la plus petite forme qui en détecterait l'absence. Il doit
   échouer maintenant.
2. **Prouve qu'il est rouge.** Lance le test et regarde-le échouer — pour la
   bonne raison. Un test qui plante à l'import, ou qui passe en douce, n'est
   pas rouge. Un test rouge que personne n'a lancé est une supposition, pas
   une base.
3. **Committe le test rouge AVANT d'envoyer le builder.** Note l'id du commit.
   Ce commit est la base rouge — le scellé anti-falsification.
4. **Envoie le builder avec un seul job : le faire passer au vert.** Le builder
   a interdiction de toucher au fichier de test. Dis-le dans l'envoi.
5. **Fais noter indépendamment.** Un correcteur qui n'a pas écrit le changement
   vérifie deux choses :
   - le test passe maintenant ;
   - le fichier de test est identique octet pour octet à la base rouge —
     `git diff <red-sha> HEAD -- tests/test_contract.py` n'affiche rien.
   Tout diff sur le fichier de test fait échouer la note. Aucune exception,
   même pas « juste corrigé une coquille ».
6. **Préfère un garde structurel à des tests ponctuels éparpillés.** Un garde
   structurel est un check (un balayage grep, un scan AST, une règle de lint)
   qui échoue sur le PROCHAIN contrevenant, pas seulement sur cette instance.
   Un garde bat dix tests ponctuels qui épinglent chacun un cas.

## Règles dures

- **Le rouge doit être prouvé rouge.** Lance-le, regarde-le échouer, avant
  qu'il compte.
- **Le builder n'édite jamais le test.** Le diff vide du fichier de test depuis
  la base rouge fait partie de la porte d'atterrissage, ce n'est pas un check
  de courtoisie.
- **Le builder n'est jamais le correcteur.** Prends une autre personne, un
  autre agent, ou un modèle d'une famille différente de celle du builder.
- **Le vert seul n'est pas une preuve.** Vert + test intact + note
  indépendante, ça c'est une preuve.
- **Quand toute une classe de défaut est en jeu, garde la classe.** Les tests
  ponctuels arrêtent ce bug ; un garde structurel arrête le suivant.

## Fonctionne bien avec

- [sniper-testing](../sniper-testing/SKILL.md) — ne lancer que les tests que le
  changement touche pendant l'itération ; une passe complète à l'atterrissage.
- [seam-engineering](../seam-engineering/SKILL.md) — la discipline du fix de
  classe à laquelle le garde structurel appartient.
- [blind-tribunal](../blind-tribunal/SKILL.md) — des correcteurs indépendants
  qui n'ont jamais vu l'auteur.
- [repair-loop](../repair-loop/SKILL.md) — la boucle qui porte rouge → vert
  → prouvé de bout en bout.
