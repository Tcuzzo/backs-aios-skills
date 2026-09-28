---
name: "design-taste"
description: "À utiliser avant de construire quoi que ce soit de visuel — un site, une app, un dashboard, une console ou un deck — pour livrer avec du vrai goût au lieu des réglages génériques de l'IA. Trigger words: design, UI, taste, design tokens, design system, accessibility, WCAG, screenshot critique, dark mode, restyle, goût, maquette, interface, accessibilité, critique de capture d'écran, mode sombre, refonte visuelle."
license: "MIT"
---

# Design Taste — Les tokens d'abord, les yeux ouverts, l'accessibilité dure
**Effort:** light — un fichier de tokens avant tout composant, plus une passe capture d'écran → critique vision par surface rendue. Élimine : relivrer les réglages génériques de l'IA — le rework de restylage et la mise à niveau d'accessibilité après livraison.

L'UI générique est un bug de workflow, pas un bug de modèle. Répare-le
structurellement : lis le brief comme une spec, fixe des design tokens exacts avant
tout composant, interdis les défauts par leur nom, donne des yeux au builder avec une
boucle de captures d'écran, et barre la sortie sur l'accessibilité — dur.

## Quand l'utiliser

- Toute demande « construis-moi / dessine-moi un… » qui affiche des pixels.
- Avant d'échafauder un frontend ou un livrable face client.
- Quand une surface existante fait générique et a besoin d'une direction précise et
  défendable.

## Les étapes

1. **Lis le brief comme une spec.** Une métaphore, une cadence, une époque, un artiste
   ou un lieu nommés dans les mots de l'humain sont une contrainte de design concrète,
   pas une décoration. La discipline complète de lecture du brief :
   [intent-compiler](../intent-compiler/SKILL.md).
2. **Choisis une direction ancrée.** Prends une référence *pilote* (un vrai design
   system ou une vraie bibliothèque qui pose la base structurelle) et une référence
   *accent* (une qui appose sa signature par-dessus). Les deux doivent être réelles et
   actuelles, avec une signature de goût vérifiable. Une ambiance inventée fait
   échouer la barrière, fermée.
3. **Émets les tokens EN PREMIER.** Avant tout composant, écris un fichier de design
   tokens lisible par une machine, à trois niveaux (primitif → sémantique →
   composant ; format de tokens W3C, `$value` + `$type`). Fixe d'entrée : une rampe de
   couleurs perceptuellement régulière (Oklch — un espace de couleurs où des pas égaux
   paraissent égaux), une vraie échelle typographique sur une police non par défaut,
   un seul incrément d'espacement (base 4px → 4/8/12/16/24/32/48/64), une échelle de
   rayons, une échelle d'élévation, et des tokens de mouvement nommés (durée +
   accélération par entrée / défilement / changement d'état ; respecte
   `prefers-reduced-motion`). Le sombre et le clair sont de première classe et se
   résolvent tous deux depuis les MÊMES tokens sémantiques.
4. **Interdis les défauts génériques par leur nom.** Les interdictions battent les
   adjectifs : pas de police réflexe (Inter/Roboto), pas de dégradés violets, pas de
   héros centré, pas de rangée de trois cartes égales, pas de pavé gris sur blanc.
   Ajoute ta propre liste bannie par projet.
5. **Construis sous contrainte.** Les composants ne consomment que des tokens. Un hex
   brut, un px ou une famille de polices codés en dur dans un composant sont un défaut.
6. **Ferme la boucle capture d'écran → critique-vision.** Pour tout ce qui est rendu :
   affiche-le dans un navigateur headless aux largeurs mobile et desktop, capture, et
   fais noter par un modèle de vision — puis corrige, en passes séparées (critique →
   correction structurelle → audit → polish), jamais en un seul coup. Le critique est
   un correcteur : un modèle d'une autre famille que le builder, qui note des axes
   nommés, jamais une note holistique unique. Résous le modèle critique depuis la
   config au moment de l'appel — un id de modèle épinglé finit par prendre sa retraite
   et emporte toute la boucle avec lui.
7. **Note la grille de goût à 8 axes.** 0–3 par axe, et chaque axe doit faire ≥ 2 :
   adhérence-aux-tokens · mise en page/hiérarchie · typographie · couleur/contraste ·
   mouvement · parité sombre-clair · accessibilité · le test viscéral
   dessiné-ou-moyenne (« est-ce que ça a l'air dessiné, ou comme la moyenne de
   tout ? »). Un seul axe sous 2 = pas fini.
8. **Applique la barrière DURE d'accessibilité (WCAG 2.2).** Cibles de pointeur
   ≥ 24×24 px CSS. Indicateur de focus visible ≥ 2px de périmètre à un contraste
   ≥ 3:1. Contraste du texte ≥ 4.5:1 en texte normal, ≥ 3:1 pour le grand texte et les
   composants d'UI. Entièrement navigable au clavier. Contraste vérifié dans LES DEUX
   thèmes. C'est une barrière, pas une suggestion : échec = on ne livre pas.
9. **Teste le code derrière les pixels.** Les résolveurs de tokens, les bascules de
   thème, les calculateurs de contraste et les réducteurs d'état reçoivent de vrais
   tests sur du vrai DOM rendu — une comparaison inversée dans un contrôle de
   contraste livre un bel écran silencieusement inaccessible. Les tests jugent le
   code ; la grille et la barrière WCAG jugent le goût.

## Règles dures — une seule fait rater le skill

- Un composant écrit avant que le fichier de tokens existe.
- Un hex / px / famille de polices brut dans un composant.
- Tout élément de la liste des défauts bannis qui apparaît en sortie.
- Sauter la boucle capture → critique pour quoi que ce soit de rendu.
- Le builder qui note ses propres visuels, ou une note holistique unique au lieu
  d'axes.
- Un axe de la grille sous 2, ou un contrôle WCAG 2.2 en échec, au moment de livrer.
- Une direction de goût impossible à ancrer dans une référence réelle et vérifiable.

## Marche bien avec

- [intent-compiler](../intent-compiler/SKILL.md) — la discipline complète de lecture du brief.
- [blind-eval](../blind-eval/SKILL.md) — garder-ou-annuler quand la question est le goût.
- [clean-code-gauntlet](../clean-code-gauntlet/SKILL.md) — durcir le code derrière les pixels.
- [blind-tribunal](../blind-tribunal/SKILL.md) — la notation inter-familles avant de livrer.

> Crédit d'échafaudage : W3C Design Tokens Community Group (format de tokens) ;
> WCAG 2.2, W3C (barrière d'accessibilité) ; UICrit, UIST 2024 (critique d'UI notée
> par axes) ; AI Jason, & JackJack. (2025). superdesign: AI design agent [Computer
> software]. GitHub. https://github.com/superdesigndev/superdesign (AGPL-3.0;
> dual-licensed with a commercial enterprise license) — l'interdiction des défauts.
> La composition et les règles dures d'ici sont BACKS AIOS.
