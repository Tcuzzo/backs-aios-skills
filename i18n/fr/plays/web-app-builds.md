# Web App Builds

Comment construire une app ou un site web avec une structure propre et une
chaîne d'approvisionnement défendue. La plupart des dégâts d'un build web
entrent par les dépendances et les frontières, pas par ta propre logique —
l'hygiène EST donc le play, pas une réflexion d'après-coup.

## Quand le lancer

Pour construire ou étendre toute app web, site, API ou dépôt livré que
quelqu'un d'autre va installer et exécuter.

## La chaîne

1. [intent-compiler](../skills/intent-compiler/SKILL.md) — lis la demande en
   entier avant de choisir une stack ou une structure.
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
6. [sniper-testing](../skills/sniper-testing/SKILL.md) — ne mocke jamais ta
   propre validation ni ta sérialisation : une frontière web mockée livre une
   app qui accepte ce qu'elle devrait rejeter.
7. [clean-code-gauntlet](../skills/clean-code-gauntlet/SKILL.md) — les handlers
   de routes, les loaders de données et les chemins de formulaire/validation
   passent avant le déploiement ; fais tourner la mutation sur les prédicats de
   validation et d'authentification jusqu'à ce que rien ne survive. Un check de
   frontière dont la comparaison inversée passe encore la suite est une porte
   ouverte sur une surface publique.
8. [blind-tribunal](../skills/blind-tribunal/SKILL.md) — notation inter-famille
   avant le déploiement.

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
