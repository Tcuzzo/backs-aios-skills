---
name: "incident-closure"
description: "À utiliser quand l'humain signale une casse ou dit « répare ça » — surtout quand le plan de contrôle normal (API, CLI, service) est mort et qu'il faut passer en dessous. La réponse est une clôture complète, compréhension d'abord — cause racine avec preuves, test en échec d'abord, vert, preuve live sur le propre chemin de l'humain, commit — jamais un menu d'options en retour. Trigger words: fix it, fix shit, full close, broken, wiped, down, it stopped working, recover, restore, répare ça, c'est cassé, en panne, ça ne marche plus, récupérer, restaurer, clôture complète."
license: "MIT"
---

# La clôture complète
**Effort:** free — une discipline d'ordre sur un correctif que tu dois déjà : les sondes de vérité disque et le test qui échoue viennent en premier, pas en plus. Élimine : les menus d'options et les confirmations à chaque étape balancés à l'humain en pleine panne.

Quand l'humain signale de la casse ou dit « répare ça », il n'y a qu'une seule bonne
réponse : une clôture complète, compréhension d'abord. La cause racine avec preuve, un
test en échec d'abord, le vert, la preuve en vif sur le chemin propre de l'humain, puis
le commit. Jamais un menu d'options renvoyé vers lui, et jamais une demande de
confirmation à chaque étape — il a déjà dit répare.

Là où les skills voisins exigent un oui explicite pour les actes destructeurs, cette
règle ne gagne que la moitié réversible : le « répare ça » de l'humain EST le oui
permanent pour les écritures de récupération réversibles qui laissent une trace de
sauvegarde ; tout ce qui est irréversible — destruction de données, dépense, envois
externes — passe toujours la [decision-bar](../decision-bar/SKILL.md), et la barre
gagne.

Ne demande quelque chose à l'humain que si c'est prouvé perdu partout ailleurs et que
lui seul peut le fournir. Tout autre intrant, tu vas le chercher.

## La méthode

1. **Sonde la surface normale — puis arrête de lui faire confiance.** Appelle l'API ou
   la CLI une fois. Si elle répond normalement, ce n'est pas une situation de clôture
   d'incident ; passe la main. Si elle renvoie 401/403, connexion refusée, des
   résultats vides là où il devrait y avoir des données, ou des données périmées,
   cesse de traiter cette surface comme une autorité.
2. **Établis la vérité terrain depuis le disque, pas depuis l'API.** Ne fais jamais
   confiance à un service cassé pour décrire son propre état. Lis toi-même les
   fichiers de données, les listings de répertoires et les dates de modification, et
   compare à ce que l'API prétend. La divergence est le signal de diagnostic.
3. **Scanne le rayon d'impact.** Cherche dans chaque répertoire de données de premier
   niveau les fichiers touchés dans la fenêtre de la panne (par ex. `find
   /data/volumes -newermt "<début>" ! -newermt "<fin>"`). Vise une réponse tenant sur
   un écran à « qu'est-ce qui a été touché, qu'est-ce qui ne l'a pas été ». Un rayon
   étroit (un volume, une table) se récupère ici. Un rayon large (beaucoup de volumes,
   tout le répertoire de données) est de la reprise après sinistre — escalade,
   n'improvise pas.
4. **Inventorie survivants vs pertes.** Classe chaque actif touché :
   - intact sur disque — récupère tel quel
   - reconstructible depuis le repo — configs et sauvegardes commitées dans git
   - reconstructible depuis l'env ou les fichiers d'identifiants — tokens, mots de
     passe
   - perdu définitivement — chiffré avec une clé disparue, état vivant uniquement en
     mémoire
   Seul le dernier panier justifie de demander à l'humain. Tout le reste, tu le
   reconstruis.
5. **La cause racine avec preuve, puis un test rouge.** Nomme pourquoi c'est cassé,
   avec la preuve venue du disque — pas une supposition. Là où le défaut est dans le
   code, écris le test en échec qui le capture avant le correctif, et rends-le vert.
   Voir [red-first](../red-first/SKILL.md) et
   [root-cause-first](../root-cause-first/SKILL.md).
6. **Descends les couches en cascade — jamais vers l'humain.** Quand le chemin préféré
   est cassé, descends d'une couche et réessaie :
   API / SDK → CLI dans le conteneur → écritures directes en base → chirurgie du
   système de fichiers. Ne sollicite pas l'humain tant qu'il reste des cascades non
   tentées. Chaque barreau descendu coûte moins cher que demander.
7. **Suppose que les dépendances sont cassées aussi.** Le code de récupération
   n'utilise que la bibliothèque standard de ton langage pour HTTP et JSON — les
   clients tiers font peut-être partie de ce qui est mort.
8. **Écris de façon idempotente, avec des traces de sauvegarde.** Chaque écriture
   disque laisse une copie `.bak` horodatée à côté de la cible. Lire, contrôler,
   copier, écrire, re-contrôler — jamais d'écrasement à l'aveugle. Si tu échanges
   temporairement un identifiant pour frapper une nouvelle clé, sauvegarde l'original
   d'abord et restaure-le avant de rendre la main : le login propre de l'humain
   survit intact.
9. **Vérifie par des appels en vif sur le chemin propre de l'humain.** Relance la
   sonde de l'étape 1 et confirme que les chiffres collent à l'inventaire
   d'avant-incident ou aux sauvegardes du repo. Un état de base vert n'est pas une
   preuve ; la surface que l'humain utilise qui remarche, ça, c'est la preuve.
10. **Committe et rapporte.** Committe les fichiers du correctif seulement. Rapporte :
    ce qui a été sondé, le rayon d'impact, les actions dans l'ordre, les comptes
    restaurés, ce qui est définitivement perdu (vide s'il n'y a rien), et toute étape
    qui a échoué sans être fatale.

## Signaux d'alarme — arrête-toi et re-sonde

- « Je vais demander à l'humain pourquoi c'est cassé » — non ; découvre-le d'abord
  depuis le disque.
- « L'API dit qu'il n'y a rien ici » — la vision qu'une API cassée a d'elle-même n'est
  pas la vérité.
- « Je vais juste réinstaller propre » — tu es en train de jeter de l'état
  récupérable.
- « La clé a disparu donc les identifiants sont inutiles » — les valeurs en clair
  vivent souvent encore dans l'env ou les fichiers d'identifiants ; recrée
  l'identifiant.
- « Confirmer avant chaque étape ? » — l'humain a dit répare ; déroule la cascade,
  rapporte à la fin.

## Règles dures — une seule fait rater le skill

- Des options renvoyées à l'humain alors qu'une solution claire existe.
- Une écriture destructrice sans trace `.bak`.
- L'humain sollicité pour quoi que ce soit avant que la cascade et l'inventaire aient
  été épuisés.
- Un sous-système retraité « gentiment » restauré — un service décommissionné qui
  reste éteint est l'état désiré, et le rallumer est la décision délibérée de
  l'humain.
- Une récupération déclarée finie sur l'état interne au lieu d'une sonde en vif sur
  son chemin.
- Un correctif laissé non committé (sauf si l'humain a explicitement dit pas de
  commit).

## Marche bien avec

- [repair-loop](../repair-loop/SKILL.md) — la boucle de correction de code que cette clôture lance quand le défaut est dans le code.
- [root-cause-first](../root-cause-first/SKILL.md) · [red-first](../red-first/SKILL.md)
- [decision-bar](../decision-bar/SKILL.md) — ce qui a le droit d'atteindre l'humain, et comment.
