# Web App Builds

Comment construire une app ou un site web avec une structure propre et une
chaîne d'approvisionnement défendue. La plupart des dégâts d'un build web
entrent par les dépendances et les frontières, pas par ta propre logique —
l'hygiène EST donc le play, pas une réflexion d'après-coup.

## Quand le lancer

Pour construire ou étendre toute app web, site, API ou dépôt livré que
quelqu'un d'autre va installer et exécuter.

## Tâche et limites communes

Applique ce play dans le dossier [BACKS Build Flow](../skills/backs-build-flow/SKILL.md)
actuel. Garde un responsable de l'intégration, le `task_mode` demandé, les
révisions base et candidat épinglées, l'essence opérateur et les preuves actuelles.
Réutilise les textes chargés pertinents ; ce play ajoute ses contrôles métier
sans relancer la tâche.

[bounded-loops](../skills/bounded-loops/SKILL.md) possède échéance initiale et quotas
restants à travers réessais, agents, modèles, revues et relèves. Ne les
réinitialise jamais pour un play imbriqué. À épuisement, sauvegarde
**STILL-BUILDING** avec candidat, preuves, barrières non satisfaites et prochaine
action. Le travail utile autorisé reste dans son quota disponible ; aucun
contrôle absent ne devient une réussite.

## La chaîne

1. Utilise intention et essence opérateur établies par Build Flow avant de
   choisir stack ou structure ; applique toute la demande et les corrections actuelles.

2. [understanding-gates](../skills/understanding-gates/SKILL.md) — conçois la
   structure d'abord : un point d'entrée documenté, un manifeste de dépendances
   explicite, et un lockfile commité. Pas d'étalement de fichiers au fil de
   l'eau.
3. Hygiène des dépendances (à faire AVANT toute installation) :
   - Valide chaque package référencé contre le registre : il existe, il est
     antérieur à ton projet, son éditeur a un historique. Les noms de packages
     hallucinés par l'IA sont des appâts à squatting — la recherche mesurée
     montre qu'environ 43 % des noms hallucinés reviennent sur des re-runs
     identiques (Spracklen et al. (2025), USENIX Security 25), donc les
     attaquants peuvent les pré-enregistrer.
   - Épingle tout par hash depuis un lockfile compilé (ex. `pip install
     --require-hashes`, `npm ci --ignore-scripts`) ; refuse tout écart
     d'intégrité.
   - Bloque par défaut les scripts de cycle de vie à l'installation. Un package
     qui ne marche qu'en exécutant un script postinstall est un signal d'alerte.
   - Épingle chaque dépendance de workflow CI sur un SHA de commit complet de
     40 caractères, jamais sur un tag de version mutable.
   - Minimise le nombre : chaque dépendance est une décision relue, pas un
     réflexe. Préfère la bibliothèque standard ou la primitive de la
     plateforme.
4. [red-first](../skills/red-first/SKILL.md) — des tests de contrat qui
   échouent pour les routes, les loaders et les chemins de validation, avant de
   les construire.
5. Construis selon la doctrine ci-dessous. Pour toute surface d'UI, applique la
   méthode [design-taste](../skills/design-taste/SKILL.md) — les tokens
   d'abord, l'accessibilité en barrière dure.
6. [sniper-testing](../skills/sniper-testing/SKILL.md) — utilise les vraies
   commandes lint/typage/tests du dépôt depuis le diff agrégé épinglé ; signale
   lacunes et N/A justifiés. Ne mocke jamais ta validation ou sérialisation : une
   frontière web mockée livre une app qui accepte ce qu'elle devrait rejeter.

7. [clean-code-gauntlet](../skills/clean-code-gauntlet/SKILL.md) — handlers de
   routes, loaders et chemins de formulaire/validation doivent passer avant
   déploiement. Mute validation et authentification dans le budget partagé ; les
   survivants significatifs bloquent le déploiement. Ajoute toute régression
   manquante dans un fichier distinct et préserve RED initial scellé. Une comparaison
   de frontière inversée que la suite laisse passer ouvre la porte sur une surface publique.

8. [blind-tribunal](../skills/blind-tribunal/SKILL.md) — panel indépendant avant
   déploiement, chaque juré choisi en direct selon capacité et disponibilité dans
   la matrice configurée. Consigne et exclue l'exécution autrice ; le relecteur
   utilise une session fraîche disjointe de l'auteur. Chaque constat étayé reçoit
   un RED distinct et une réparation bornée dans cette tâche. Reconvoque dans le
   budget restant ; tous les jurés requis doivent valider. Garde la passe complète
   des suites touchées et vérifie la livraison autorisée sur la vraie surface de l'app.

## La doctrine (ce que le build doit satisfaire)

- Aucun secret dans le source : lis les credentials depuis l'environnement ou
  un coffre à secrets. Une clé commitée fait échouer le build.
- La sortie s'adapte à son contexte : requêtes paramétrées pour le SQL, et le
  bon encodage avant qu'une valeur atteigne le shell, la base de données ou le
  DOM. Ne concatène jamais de l'entrée non fiable dans une chaîne.
- Émets un SBOM lisible par machine — un inventaire logiciel (ex. CycloneDX) —
  pour que le destinataire puisse auditer tout l'arbre de dépendances.
- Garde le build reproductible : versions d'outillage épinglées, installation
  déterministe, et aucun accès réseau EXTERNE pendant les tests (les services
  en loopback local — bases de données, fixtures — sont bienvenus et attendus).

## Barrières dures

- Une dépendance non validée ou non épinglée bloque l'installation.
- Un secret commité bloque le build.
- Des mutants survivants dans les prédicats de validation ou d'authentification
  bloquent le déploiement.
- Un accès réseau externe pendant les tests bloque l'atterrissage (le loopback
  est permis).

## Marche bien avec

- [seam-engineering](../skills/seam-engineering/SKILL.md) — corriger une faille de frontière comme une classe
- [bounded-loops](../skills/bounded-loops/SKILL.md) — des appels sortants qui respectent les limites de débit

**Weight:** une discipline d'hygiène free tout au long du build ; la dépense heavy est la mutation sur les prédicats de validation et d'auth plus le tribunal — elle se rentabilise sur chaque surface publique, où une seule comparaison inversée est une porte ouverte.
