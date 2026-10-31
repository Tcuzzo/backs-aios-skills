---
name: "clean-code-gauntlet"
description: "Pour durcir ou livrer des modifications exécutables exigeant des mesures de complexité, couverture et force des régressions, ainsi qu'une revue de design indépendante."
license: "MIT"
---

# Clean Code Gauntlet — le parcours d'épreuves
**Effort:** heavy — du vrai calcul : des runs de couverture et de complexité plus une passe de mutation bornée, puis un seul modèle de goût ; à dépenser sur les changements qui livrent. Élimine : la revue humaine ligne à ligne de diffs entiers, et les tests faux-verts derrière lesquels une régression se cache.

## Pourquoi ce skill existe

Le code sale fait patiner les agents, et les règles enterrées dans un long prompt
s'estompent en cours de contexte — les contrôles déterministes, eux, ne s'estompent
jamais. Alors fais tourner Clean Code comme un **parcours d'épreuves que le code doit
franchir**, pas comme de la prose que le modèle doit retenir.

**Mesure, ne relis pas.** Barre l'entrée sur des chiffres qu'un outil calcule :
couverture, complexité cyclomatique (le nombre de chemins indépendants à travers une
fonction), taille des modules, mutants tués. Les humains et les modèles auditent des
échantillons — jamais des diffs entiers.

## La chaîne (dans l'ordre ; chaque étape s'arrête fort en cas d'échec)

Lie `base_sha`, `candidate_sha`, responsable de l'intégration et quota de mission
[bounded-loops](../bounded-loops/SKILL.md) restant du dossier
[Build Flow](../backs-build-flow/SKILL.md) existant. Réutilise les preuves encore
valides ; tours de revue et campagnes de mutation ne rechargent pas le budget.

1. **Lint, typage et comportement ciblés au vert.** Exécute les commandes
   applicables du dépôt — voir [sniper-testing](../sniper-testing/SKILL.md).
   Consigne explicitement contrôles absents ou inapplicables sans les déclarer
   réussis. Une base rouge exige arrêt et correction ; ni mutation ni notation sur du rouge.
2. **CRAP sous le seuil** sur de vraies données de couverture (voir la barrière plus
   bas). Dépassement → refactore la fonction vers le bas, ou couvre-la à fond. Ne
   baisse jamais la barre.
3. **Mutation : aucun survivant inexpliqué dans le périmètre.** Un survivant non
   équivalent est une lacune de régression. Ajoute un fichier supplémentaire
   distinct ; préserve le contrat [red-first](../red-first/SKILL.md) initial scellé
   octet pour octet. Consigne les réfutations étayées des mutants équivalents.
   Une erreur d'outil ou un délai dépassé est non concluant, jamais un mutant tué.
4. **Revue de goût légère** — un modèle ne juge que ce que les chiffres ne peuvent pas.

## Les outils qui calculent ça

| Pile | Outils |
| --- | --- |
| Python | coverage.py + radon + mutmut |
| JS/TS | c8 (ou istanbul) + Stryker |
| Go | go test -cover + gocyclo + go-mutesting |
| Rust | cargo-tarpaulin + cargo-mutants |
| Java | JaCoCo + PIT |
| Autre | n'importe quel % de couverture + n'importe quel compteur de complexité cyclomatique |

Une forme de commande par étape :
- Couverture : `coverage run -m pytest <fichiers snipers> && coverage report` (JS/TS : `npx c8 vitest run <fichiers>`)
- Complexité : `radon cc -s <fichiers modifiés>`
- Mutation : `mutmut run --paths-to-mutate <fichiers modifiés>` (JS/TS : `npx stryker run --mutate "<glob>"`)

Ces commandes sont des exemples, pas des instructions d'installation ni des
promesses de CLI stable. Utilise les outils épinglés du dépôt et leurs options
prises en charge. Pour la documentation seule, valide liens, structure,
distribution et scénarios de comportement ; complexité de code ou mutation
peuvent être inapplicables. Note la raison au lieu d'inventer des mesures.

## La barrière CRAP

```
CRAP(m) = comp(m)^2 * (1 - cov(m)/100)^3 + comp(m)
```

- À 100 % de couverture, le score s'effondre sur la complexité elle-même.
- 30 est la ligne « crappy » classique (une complexité de 5 avec zéro couverture
  l'atteint).
- Les humains tiennent environ 4–5 de complexité par fonction. Un agent peut porter
  6–8 SEULEMENT à une couverture proche de 100 % — la couverture paie le mou.
- Une fonction à CRAP élevé a exactement deux sorties : la refactorer vers le bas, ou
  la couvrir à fond. **Ne baisse jamais le seuil pour passer.**

## À qui est la dette — AUTHORED / WORSENED / UNCHANGED

Un score absolu cache à qui appartient la dette. Découpe chaque delta de complexité et
de CRAP contre le `base_sha` épinglé avant la tâche, avec une couverture réelle comparable :

- **AUTHORED** — les fonctions que ce changement a créées. La barre entière s'applique.
- **WORSENED** — les fonctions préexistantes que ce changement a aggravées. Le delta
  est facturé à ce changement ; il doit revenir à la base ou mieux.
- **UNCHANGED** — la dette préexistante que le changement n'a jamais touchée.
  Rapporte-la, classe-la, ne la facture jamais à ce changement — et ne t'en sers
  jamais comme couverture pour sauter le parcours.

## Règles de mutation (borné, jamais imprudent)

- **Jamais l'arbre de travail partagé.** Mute dans un checkout de brouillon du
  `candidate_sha` commité exact. Fichiers cibles ou tests modifiés : sauvegarde et
  termine d'abord le candidat. Préserve le travail sans rapport dans le checkout initial.
- **Le coût se mesure, il ne se suppose jamais.** Chronomètre la suite ciblée une
  fois, annonce ETA = base x nombre de mutants AVANT de dépenser quoi que ce soit.
  Propose un essai à blanc.
- **Borné et reprenable.** Plafonne mutants et minutes dans le quota restant. Un
  arrêt budget sauvegarde les mutants non vérifiés et laisse la barrière incomplète.
  Reprends seulement avec un quota restant ou explicitement étendu.
- **Couverture d'abord.** Ne mute que les lignes couvertes ; une ligne non couverte
  est un trou de couverture que la barrière CRAP a déjà attrapé.
- **Périmètre seulement.** Mute ce que le diff a touché, jamais le repo entier.
- Un mutant réellement équivalent peut être réfuté au lieu d'être tué — avec la
  réfutation écrite noir sur blanc, jamais sautée en silence.
- **Pas d'outil de mutation pour ta pile ?** Consigne limite et preuves de
  substitution réelles. Applique la politique d'acceptation du dépôt ; une barrière
  obligatoire reste incomplète jusqu'à acceptation d'une alternative documentée par son responsable.

## La revue de goût (en dernier, et légère)

Les barrières déterministes passent d'abord ; ne dépense un modèle que là où le
raisonnement est le seul outil. Le relecteur travaille dans une session vierge et disjointe de l'auteur ;
le builder ne note jamais son propre travail. Il ne juge que le design et le
goût : le nommage, les responsabilités mélangées, la largeur des interfaces, et les
six odeurs — rigidité, fragilité, immobilité, complexité inutile, répétition inutile,
opacité. L'arithmétique, elle, a déjà été réglée par les barrières.

Le plancher d'artisanat que la revue tient : des fonctions petites, qui font une seule
chose, peu d'arguments, pas d'argument-drapeau, des noms honnêtes ; des modules
profonds — une petite interface qui cache de la vraie logique ; des tests rapides,
indépendants, répétables, un seul comportement vérifié chacun.

## Règles dures (une seule enfreinte fait rater le skill)

- Ne jamais baisser un seuil ni affaiblir le jeu de mutants pour forcer un pass.
- Ne jamais muter l'arbre de travail partagé ; ne jamais tourner sans borne.
- Ne jamais facturer la dette UNCHANGED au changement courant.
- Un test qui ne peut pas échouer est du théâtre — les tests de mutation sont la
  preuve de quels tests sont réels.
- Dis le vrai coût — le temps machine est bon marché, les régressions non. Ne fabrique
  jamais du faux vert pour sauver l'heure.

## Marche bien avec

- [sniper-testing](../sniper-testing/SKILL.md) — choisit le périmètre de tests de l'étape 1
- [red-first](../red-first/SKILL.md) — le contrat en échec qui précède tout build
- [blind-eval](../blind-eval/SKILL.md) — garder-ou-annuler quand la question est le goût
- [blind-tribunal](../blind-tribunal/SKILL.md) — un verdict noté plus complet avant de livrer

> Crédit d'échafaudage : Robert C. Martin, *Clean Code* (2008) ; Alberto Savoia &
> Bob Evans, the CRAP metric (2007) ; John Ousterhout, deep modules
> (*A Philosophy of Software Design*, 2018) ; Pocock, M., & Martin, R. C.
> (2026, Aug 19). LIVE: Uncle Bob on Software Fundamentals in the Age of AI
> [Video]. YouTube. https://www.youtube.com/watch?v=zcLPGC-tvgk — source de la bande
> CRAP pour agents et de la mutation couverture-d'abord. La composition et les règles
> dures d'ici sont BACKS AIOS.
