---
name: "repo-map"
description: "À utiliser lors de la première session dans un repo froid sans index, puis chaque fois que la carte vieillit. Parcourt l'arbre une fois, écrit un CODE_MAP.md à la racine et force les sessions suivantes à lire la carte d'abord — carte d'abord, parcours brut seulement si la carte n'a pas la réponse. Trigger words: repo map, code map, map first, map-first, index the repo, cold repo, stale map, refresh the map, carte du repo, carte du code, indexer le repo, rafraîchir la carte."
license: "MIT"
---

# Repo Map
**Effort:** light — un parcours au premier passage, presque gratuit ensuite. Élimine : les agents qui redérivent la forme du repo à chaque session — la plus grosse taxe de latence et de tokens d'un repo non indexé.

Un codebase indexé répond gratuitement à « où vit X ? ». La plupart des repos n'ont
pas d'index, donc chaque session paie la même taxe : parcourir l'arbre, redécouvrir la
structure, tout oublier à la fin. Ce skill paie une fois. Parcours l'arbre une fois,
écris ce que tu apprends dans une carte, puis fais lire la carte avant chaque parcours.

## Quand le lancer

- À la première session dans un repo froid — sans carte ni index.
- Chaque fois que la carte vieillit (voir la règle ci-dessous).

## Les étapes

1. **Parcours l'arbre une fois.** Une passe sur la vraie structure : répertoires,
   points d'entrée et emplacement des choses. Ce devrait être le seul parcours
   complet dont le repo ait jamais besoin.
2. **Écris un `CODE_MAP.md` à la racine du repo.** Il contient :
   - les points d'entrée — où l'exécution commence ;
   - les sections et coutures, chacune avec son but en une ligne ;
   - l'emplacement des tests ;
   - les commandes de build, d'exécution et de test ;
   - les chemins chauds — amorcés par l'historique (fréquence de
     `git log --name-only`), ou laissés vides pour les sessions suivantes.
3. **Garde-le léger.** Une carte, pas de la documentation. Une ligne par fait. Si une
   entrée devient un paragraphe, elle dérive en doc — recoupe-la en pointeur.
4. **Enregistre la forme de l'arbre.** Stocke une empreinte bon marché dans la carte,
   `git ls-files | sha256sum` (détecte ajouts, déplacements et renommages), pour que
   la session suivante voie si la forme a changé.

## La loi carte-d'abord

La recherche, l'orientation et les plays lisent la carte AVANT de parcourir l'arbre.
Le parcours brut est le fallback quand la carte n'a pas la réponse — et tout ce qu'il
apprend est écrit DANS la carte avant de continuer. La carte absorbe chaque parcours.
La redérivation se paie une fois, jamais par session.

## La règle de fraîcheur

Rafraîchis la carte seulement si la forme de l'arbre a changé — fichiers ajoutés,
déplacés ou renommés depuis l'état enregistré. Compare l'empreinte stockée
(`git ls-files | sha256sum`) avec l'arbre vivant. Jamais de rafraîchissement au
minuteur. Jamais à chaque session. Une carte reconstruite sur planning n'est que la
taxe par session sous un autre nom.

## Règles dures

- **Des faits et des emplacements, jamais des opinions.** « Auth vit dans
  `src/auth/` » appartient à la carte ; « le code auth est sale » n'y appartient pas.
- **Un pointeur mort meurt dès qu'on le trouve.** Un chemin qui ne résout plus est
  corrigé ou supprimé sur-le-champ. Une carte qui ment est pire qu'aucune carte.
- **La carte ne porte jamais de secrets.** Ni clés, ni tokens, ni credentials, ni
  hostnames privés. C'est un fichier suivi ; traite-le comme tel.

## Fonctionne bien avec

- [live-research](../live-research/SKILL.md) — le chercheur lit la carte d'abord, puis la source.
- [wayfinder](../wayfinder/SKILL.md) — l'orientation part de la carte, pas d'un parcours froid.
- [session-handoff](../session-handoff/SKILL.md) — la carte est la pièce du handoff que toutes les sessions partagent.
