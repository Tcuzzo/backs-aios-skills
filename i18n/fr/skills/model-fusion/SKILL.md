---
name: "model-fusion"
description: "À utiliser lorsque comparer des approches élaborées indépendamment aide la tâche et tient dans le budget restant, ou lorsque l’opérateur demande un panel. Brouillons, sélection ou synthèse et vérification indépendants du modèle ; un même modèle configuré peut remplir des rôles séparés dans des sessions isolées."
license: "MIT"
---

# Model Fusion
**Effort:** heavy — brouillons indépendants, un évaluateur et un rédacteur optionnel ; utilise le panel lorsque son utilité pour la tâche justifie son coût dans le budget restant.

Le panel est facultatif. Des exécutions séparées traitent la même tâche ; un
évaluateur qui n'a participé à aucune de ces exécutions choisit ou combine les
candidats. Le résultat est vérifié contre la demande d'origine. Un même modèle
configuré et capable peut rédiger, évaluer et composer dans des sessions séparées
et isolées. Aucun changement de modèle ou de fournisseur n'est nécessaire.
L'évaluateur n'hérite ni de la conversation ni du contexte de travail des auteurs.

## Quand le lancer

- Lorsque comparer des approches peut résoudre une incertitude précise et que
  leur évaluation tient dans le budget restant de la mission.
- Lorsque l'opérateur demande un panel ; indique les rôles disponibles et leurs
  limites. Une tâche importante n'impose pas à elle seule un panel.
- Pour une modification simple, applique directement le changement et vérifie-le.

Lie [bounded-loops](../bounded-loops/SKILL.md). Brouillons, juge, rédacteur et
tours de réparation partagent échéance, tentatives restantes et ressources de la
mission actuelle. De nouveaux rôles ou sessions ne réinitialisent pas ces limites.
Exécute les brouillons indépendants en parallèle si l'hôte le permet, sinon
successivement dans les mêmes limites. Ne prétends pas disposer d'une isolation
de session que l'hôte n'offre pas.

## Les trois étapes

### 1. Panel — brouillons indépendants

1. Donne la même tâche et le même dossier de contexte à chaque session de
   rédaction isolée.
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
     puis une exécution de rédaction séparée compose la réponse finale à partir
     de cette analyse. Garde les rôles et les sessions séparés ; un même modèle
     configuré et capable peut remplir les deux.
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

- Choisis la taille du panel et les rôles selon les capacités requises,
  la disponibilité réelle, la configuration actuelle et le budget restant.
  Aucun modèle fixe, fournisseur préféré ou quota de diversité n'est imposé.
  Signale les lacunes de configuration.
- Le format de config, les rôles-pas-les-noms et la résolution par sonde live
  appartiennent à [fleet-ladder](../fleet-ladder/SKILL.md).

## Règles dures — une seule enfreinte et le skill a échoué

- **Le builder ne juge jamais.** L'exécution évaluatrice n'a rédigé aucun
  candidat et n'hérite pas de la conversation ou du contexte de ses auteurs.
  Le correcteur final travaille dans une session vierge et disjointe de l'auteur.
- **Aucun nom de modèle en dur** à aucun point d'appel. Les rôles dans le code,
  les modèles dans la config.
- **Aucune dégradation silencieuse.** Rédacteurs écartés, repli du juge, échecs
  au filtre et épuisement sont tous bruyants. Un résultat innotable ne passe
  jamais par défaut.
- **Réparation bornée.** Les relances ont un plafond dur et consomment le budget
  restant de la mission ; arrête à la première limite atteinte. L'épuisement
  produit un checkpoint visible, jamais une boucle infinie.
- **Des tests verts seuls, ce n'est pas fini.** Le gagnant est prouvé sur le
  comportement live.

## Fonctionne bien avec

- [fleet-ladder](../fleet-ladder/SKILL.md) — résoudre quels modèles sont debout avant que le panel tire.
- [blind-tribunal](../blind-tribunal/SKILL.md) — la cour de notation fail-closed quand le correcteur principal meurt.
- [red-first](../red-first/SKILL.md) — le test en échec que le brouillon gagnant doit faire passer au vert.
- [blind-eval](../blind-eval/SKILL.md) — le filtre de goût garder-ou-revenir quand aucun test ne peut trancher.
