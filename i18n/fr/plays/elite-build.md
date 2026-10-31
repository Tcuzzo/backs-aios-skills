# Elite Build — le play maître

Utilise ce play complet sur demande explicite ou lorsqu'un build, correctif ou
uplift exige ses étapes combinées de design, construction, qualité et revue.
L'humain donne l'objectif une fois. Un changement ciblé peut utiliser les méthodes
pertinentes de BACKS Build Flow sans démarrer tout ce play ; choisir ce play
préserve chaque contrôle applicable ci-dessous.

## Une tâche, un responsable de l'intégration

[BACKS Build Flow](../skills/backs-build-flow/SKILL.md) possède dossier de tâche,
`task_mode`, essence opérateur et aboutissement. Réutilise contexte actuel, vrais
textes chargés et preuves ; rafraîchis une étape seulement si ses entrées ou le
candidat changent. Conserve `base_sha` épinglé, `candidate_sha` actuel et un
responsable à travers toutes les lanes. Un spécialiste ne lance pas un second cycle.

[bounded-loops](../skills/bounded-loops/SKILL.md) possède échéance initiale et quotas
restants. Recherche, builders, lint/typage/tests, mutation, revues, modèles de
repli et relèves consomment les mêmes limites. Ne les recharge jamais dans un play
imbriqué. À épuisement, sauvegarde **STILL-BUILDING** avec candidat, preuves,
contrôles non satisfaits et prochaine action ; termine le travail utile autorisé
qui ne consomme pas le quota épuisé. Une limite de budget ne dispense d'aucun contrôle.

## La chaîne

0. [optimus](../skills/optimus/SKILL.md) — établis socle et Build Flow une fois
   par session. Réutilise les vrais textes encore présents dans le contexte et
   leurs reçus de source ; un reçu seul ne remplace pas un texte absent. Un appel
   imbriqué ne redémarre pas le cycle et ne revendique pas une invocation inexistante.
1. Utilise intention et essence opérateur établies par Build Flow. Lis demande
   entière et corrections actuelles ; déduis la directive avant de soumettre
   une décision de livraison ou d'option. Résous directement les choix tranchables par preuves.
2. [human-calibration](../skills/human-calibration/SKILL.md) — applique le profil
   validé déjà présent dans le dossier. Charge le contexte pertinent manquant ;
   ne réinterroge pas l'humain et ne reconstruis pas le même profil à chaque étape.
3. [turn-and-burn](../skills/turn-and-burn/SKILL.md) — conserve les exigences de
   roster et revue de plan de la mission. Consulte essence de chaque modèle
   (know-thyself), `docs/BACKS_LESSONS_LEARNED.md` et `memory/MEMORY.md` si disponibles.
   Ces traces de capacités et de leçons sont distinctes de l'essence opérateur.
   Réutilise les preuves de burn actuelles ; toute adoption Absorb nécessaire
   partage cette mission et rend son résultat au responsable de l'intégration.
4. [understanding-gates](../skills/understanding-gates/SKILL.md) — préserve les
   étapes Design → Plan → Build → Test → Ship. Utilise
   [live-research](../skills/live-research/SKILL.md) pour inspecter chemin touché,
   responsables, consommateurs et frontière de livraison. Suis d'autres dépendances
   lorsque les preuves montrent qu'elles peuvent changer le résultat ; ne répète
   pas une étude du système entier avant chaque édition. Commence la prochaine
   étape exécutable dès que les conditions de contexte prêt de Build Flow sont réunies.
5. [architecture-engineer](../skills/architecture-engineer/SKILL.md) — si le diff
   touche frontière de module, direction de dépendance ou frontière partagée,
   applique revue structurelle et classification de la surface d'autorité. Cite
   règle locale ou mode de panne concret derrière chaque violation ; une décision
   durable reçoit une ADR.
6. [wayfinder](../skills/wayfinder/SKILL.md) — trace une route réellement non résolue
   depuis les preuves. Ne relance pas la planification quand le chemin est connu.
7. [red-first](../skills/red-first/SKILL.md) — observe et committe le vrai contrat
   en échec avant son builder. Note le sceau et préserve le fichier initial octet
   pour octet. Un constat ultérieur reçoit un test supplémentaire distinct ;
   il ne réécrit pas le RED initial.
8. Construis le plus petit changement complet à la frontière responsable.
   Parallélise questions et travaux indépendants avec propriété de fichiers
   explicite ou worktrees isolés ; garde un responsable unique et les règles de
   concurrence du projet. Résous les builders via
   [fleet-ladder](../skills/fleet-ladder/SKILL.md), avec
   [model-fusion](../skills/model-fusion/SKILL.md) si la mission le demande.
   Pour un défaut, applique [repair-loop](../skills/repair-loop/SKILL.md) dans le
   workflow et ferme la classe à la frontière partagée selon
   [seam-engineering](../skills/seam-engineering/SKILL.md). Rends les constats à
   cette tâche au lieu de relancer récursivement le play.
9. [sniper-testing](../skills/sniper-testing/SKILL.md) — déduis le périmètre du diff
   agrégé base-candidat épinglé et des chemins en attente possédés. Exécute vraies
   commandes lint, typage et tests ciblés du dépôt. Note N/A avec raison et outils
   requis absents comme lacunes ; n'installe pas de vérificateurs arbitraires et
   n'invente pas de réussites. Garde des runs ciblés pendant l'itération.
10. [clean-code-gauntlet](../skills/clean-code-gauntlet/SKILL.md) — applique qualité,
    complexité/couverture et mutation bornée dans le même workflow au même candidat.
    Un survivant significatif ou constat retourne vers RED supplémentaire et
    correction minimale dans le budget restant. Réutilise les preuves valides,
    jamais un verdict périmé pour d'autres octets ; ne lance pas un second cycle complet.
11. [blind-eval](../skills/blind-eval/SKILL.md), puis
    [blind-tribunal](../skills/blind-tribunal/SKILL.md) — fournis un dossier de
    preuves figé et expurgé de l'auteur à des relecteurs choisis en direct selon
    capacité et disponibilité. La revue exige des exécutions fraîches disjointes
    de l'auteur, sans conversation héritée du builder. Consigne l'exécution
    autrice en provenance et exclue-la. Chaque constat étayé reçoit RED distinct,
    correction et nouvelle revue dans le même quota restant. Tous les jurés requis
    doivent valider avant atterrissage. Applique la règle Solo rig du tribunal si
    pertinente ; note configuration réelle et lacunes runtime sans affaiblir l'indépendance.
12. Termine l'aboutissement demandé. Revérifie l'identité du candidat, exécute
    une passe complète des suites touchées et contrôles projet requis, préserve
    le travail concurrent et suis la procédure d'atterrissage autorisée. Pour un
    déploiement, vérifie code installé/en exécution et vraie surface de l'humain.
    Redémarre un service seulement si livraison demandée et procédure réelle
    l'exigent. Un patch local ou une revue n'acquiert pas silencieusement un périmètre de release.

## Barrières dures

- Le RED initial a été observé en échec avant correction et reste identique octet
  pour octet ; les contrats supplémentaires ont leurs propres preuves et sceaux.
- Contrôles requis de qualité, lint/typage/tests et mutation passent sur le
  candidat exact, avec N/A justifiés et lacunes réelles rapportées honnêtement.
- La revue requise utilise une exécution fraîche disjointe de l'auteur ; le builder
  ne se note jamais et ne fournit pas au relecteur la conclusion désirée.
- Chaque constat sur la frontière possédée est corrigé ou arbitré par preuves.
  Un constat ouvert est sauvegardé explicitement et bloque l'atterrissage ; il n'est jamais masqué.
- Exigences applicables de burn, essence, leçons et revue de plan sont satisfaites
  par des preuves actuelles. Réutiliser une preuve ne permet pas de sauter un contrôle requis.
- Une capacité **PROVEN** est livrée, notée indépendamment et démontrée sur la vraie
  surface de l'humain. Sinon, rapporte **STILL-BUILDING** et la preuve exacte
  manquante selon [human-voice](../skills/human-voice/SKILL.md). Distingue
  l'achèvement demandé d'une revue ou d'un patch local d'une capacité démontrée en direct.
- Committe seulement les fichiers de cette tâche. Préserve le travail des autres sessions.

## Politique Fleet Ladder

Utilise [fleet-ladder](../skills/fleet-ladder/SKILL.md) pour dispatch réel, routes
configurées, sondes live, repli et indépendance de revue. Lis
`config/fleet_ladder.yaml` et `config/gpu_nodes.yaml` du déploiement si fournis ;
le pack ne crée pas de résolveur. Préserve les exigences de recherche avant
travail frontier sur les paliers configurés et leurs sources permises : Web,
GitHub, Reddit et articles. Respecte plancher de raisonnement et politique
d'efficacité des tokens ; ne fige pas d'identifiant de modèle et ne tronque pas
les preuves pour fabriquer une conformité.

Avant interruption, préserve candidat, sceaux, preuves, échéance et quotas restants
via [session-handoff](../skills/session-handoff/SKILL.md).
