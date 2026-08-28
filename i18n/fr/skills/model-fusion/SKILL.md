---
name: "model-fusion"
description: "À utiliser quand la réponse d'un seul modèle n'est pas assez fiable — un build, un fix ou un design difficile où tu veux plusieurs modèles en compétition et un juge indépendant qui tranche. Un panel rédige en parallèle, un juge fusionne le gagnant, le résultat est validé contre l'intention d'origine. Trigger words: fusion, panel, judge, multi-model, ensemble, draft and merge, builder not grader, juge, multi-modèle, brouillons parallèles, fusionner, le builder ne note pas."
license: "MIT"
---

# Model Fusion
**Effort:** heavy — un panel complet qui rédige en parallèle plus un juge indépendant (et un rédacteur en option) ; à dépenser sur les builds durs et les correctifs qui livrent, jamais sur des changements d'une ligne. Élimine : parier le changement sur le brouillon d'un seul modèle, et le rework quand ce brouillon-là est faux.

Plusieurs voix indépendantes battent une seule voix. Un panel de modèles rédige
la même tâche en parallèle. Un juge — un modèle qui n'a écrit aucun des
brouillons — choisit ou fusionne le meilleur. Le gagnant est ensuite vérifié
contre ce qui était vraiment demandé.

## Quand le lancer

- Tout build, fix ou uplift substantiel où la qualité compte plus que la vitesse.
- Quand tu veux une paire précise de correcteurs indépendants, pas une confiance
  aveugle en un seul modèle.
- PAS pour les changements triviaux d'une ligne. Fais le changement direct et
  vérifie-le.

## Les trois étapes

### 1. Panel — brouillons en parallèle

1. Envoie la même tâche, avec le même contexte, à chaque modèle du panel en
   même temps.
2. Chaque rédacteur travaille seul. Aucun rédacteur ne voit le travail d'un autre.
3. Un rédacteur qui plante, dépasse le délai ou renvoie du vide est loggé et
   écarté. Il ne tue jamais le tour. Logge l'éviction bien fort — ne l'avale
   jamais.
4. Collecte chaque candidat non vide.

### 2. Juge — un extérieur choisit et fusionne

1. Avant de juger, fais passer à chaque candidat un filtre mécanique pas cher :
   s'applique-t-il proprement ? Parse-t-il ? Exécute la sonde sur une copie
   jetable, jamais sur l'arbre live. Les candidats qui échouent au filtre
   sortent avant que le juge les voie.
2. Deux formes de juge — choisis-en une par config :
   - **Synthèse :** le juge analyse chaque candidat (forces, défauts, conflits),
     puis un modèle rédacteur séparé compose la réponse finale à partir de cette
     analyse. Rédacteur et juge sont des rôles différents ; garde-les sur des
     modèles différents quand tu peux.
   - **Sélection :** le juge choisit le meilleur candidat unique qui a passé le
     filtre. Moins cher. Utilise-la quand fusionner n'apporte rien.
3. Si le juge ou le rédacteur est indisponible, dégrade BRUYAMMENT vers la
   sélection sur les mêmes candidats. Ne gâche jamais le panel en silence ; ne
   prétends jamais qu'une synthèse a eu lieu.
4. Si aucun candidat ne survit au filtre, ajoute la meilleure erreur au prompt
   et relance le panel — borné, 2 tours de réparation au maximum. À
   l'épuisement, renvoie un échec avec la liste complète des erreurs. Ne
   renvoie jamais un résultat vide ou sans effet comme un succès.

### 3. Valider — vérifier le gagnant contre l'intention

1. Relis la demande d'origine. Le gagnant fait-il ce qui était demandé — tout,
   et rien de ce qui n'était pas demandé ?
2. Vérifie la justesse sémantique, l'accord de style avec le code environnant,
   et qu'il s'applique toujours proprement.
3. Une confiance basse remonte comme un signal d'escalade, jamais cachée. Puis
   prouve-le de la manière normale : test en échec d'abord, vert, comportement
   live. Un brouillon fusionné qui n'a jamais tourné est une supposition.

## L'échelle

- La forme des barreaux de la fusion : un panel large de modèles pas chers en
  bas, des panels plus serrés et des budgets de sortie plus serrés en montant —
  un barreau mal configuré échoue bruyamment au chargement.
- Le format de config, les rôles-pas-les-noms et la résolution par sonde live
  appartiennent à [fleet-ladder](../fleet-ladder/SKILL.md).

## Règles dures — une seule enfreinte et le skill a échoué

- **Le builder ne juge jamais.** Le juge n'a rédigé aucun candidat. Le
  correcteur final est un modèle différent (idéalement d'une autre famille) de
  celui qui a construit le gagnant.
- **Aucun nom de modèle en dur** à aucun point d'appel. Les rôles dans le code,
  les modèles dans la config.
- **Aucune dégradation silencieuse.** Rédacteurs écartés, repli du juge, échecs
  au filtre et épuisement sont tous bruyants. Un résultat innotable ne passe
  jamais par défaut.
- **Réparation bornée.** Les relances du panel ont un plafond dur. L'épuisement
  est un échec bruyant, pas une boucle infinie.
- **Des tests verts seuls, ce n'est pas fini.** Le gagnant est prouvé sur le
  comportement live.

## Fonctionne bien avec

- [fleet-ladder](../fleet-ladder/SKILL.md) — résoudre quels modèles sont debout avant que le panel tire.
- [blind-tribunal](../blind-tribunal/SKILL.md) — la cour de notation fail-closed quand le correcteur principal meurt.
- [red-first](../red-first/SKILL.md) — le test en échec que le brouillon gagnant doit faire passer au vert.
- [blind-eval](../blind-eval/SKILL.md) — le filtre de goût garder-ou-revenir quand aucun test ne peut trancher.
