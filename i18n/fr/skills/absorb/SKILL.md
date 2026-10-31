---
name: "absorb"
description: "Quand une capacité nécessaire peut déjà exister dans un projet open source, ou si l'opérateur demande adoption, portage, réingénierie, ingestion de dépôt, étude de l'existant ou intégration native."
license: "MIT"
---

# Absorb — Adopter l'existant, pas le réinventer
**Effort:** light — une ingestion de repo (sonde des métadonnées + clone superficiel) et une notation indépendante du portage. Élimine : réinventer une capacité que l'existant a déjà résolue — le doublon écrit de zéro dont chaque bug serait à ta charge.

**La capacité est reine.** Un repo n'est qu'un véhicule pour une capacité. Quand tu as
besoin d'une chose qu'un projet existant fait déjà, ne construis pas un doublon à partir
de zéro, et ne fais pas de cloner-coller. Trouve le meilleur existant, extrais la
capacité, réingénie-la pour qu'elle s'ajuste à ton harnais, et cite l'échafaudage. La
citation est un fait, pas une décoration.

## Quand l'utiliser

- On te demande d'ajouter une capacité (un outil, un skill, un agent, un pipeline) que
  l'open source a sans doute déjà résolue.
- Tu t'apprêtes à `git clone` puis copier du code tel quel — stop ; c'est ce chemin-ci
  qu'il faut prendre à la place.
- Passe ton tour pour un simple snippet, une valeur de config ou une info à vérifier.
  Ceux-là, lis-les, c'est tout.

## Les étapes

Utilise le dossier [BACKS Build Flow](../backs-build-flow/SKILL.md) actuel et son
responsable de l'intégration. Un appel direct crée ce dossier une fois ; un appel
imbriqué rend ses preuves d'adoption à l'appelant. Réutilise contexte valide,
essence opérateur et textes déjà chargés. [bounded-loops](../bounded-loops/SKILL.md)
possède échéance et essais/tours restants ; découverte, builds, mutation, revues,
changements de modèle et relèves consomment le même budget. Ni nouvelle phase ni
nouvel agent ne le rechargent. Respecte `task_mode` : revue et diagnostic n'autorisent
ni modifications natives ni livraison.

1. **Chasse l'existant d'abord.** Cherche avant de construire. Un doublon que tu
   inventes vaut moins qu'un échafaudage que tu adoptes : tu hérites de zéro test
   terrain et tous les bugs sont pour toi.
2. **Découvrir au-delà du README.** Récupère métadonnées du projet (licence,
   activité, langage) via l'API, clone superficiellement dans un brouillon et lis
   code et tests. Pour un artefact distribué ou un comportement runtime demandé
   que l'inspection des sources n'explique pas, appelle
   [rea-investigation](../rea-investigation/SKILL.md) avec cible exacte et question
   bornée. REA rend les preuves à cet appelant sans relancer Absorb. Consigne
   identité amont, observations, limites et inconnues avant le choix d'adoption.
   Les constats statiques n'établissent pas le comportement runtime.
3. **Passe les barrières de confiance.**
   - *Licence :* permissive (MIT / Apache / BSD / MPL) = réingénierie sans risque.
     Copyleft (GPL / AGPL) = technique seulement — réingénie l'idée, ne copie jamais le
     code. Pas de licence = traite comme tous-droits-réservés, technique seulement.
     Clause non commerciale = un blocage ; remonte-le à ton humain.
   - *Scan louche :* utilise `rg` pour les motifs de cloaking / spam / faux avis / arnaque.
     Signale-les fort.
   - *Pas d'installation sauvage :* jamais de `pip install` / `npm install` d'une
     dépendance non vérifiée (le typo-squatting est une vraie attaque de chaîne
     d'approvisionnement). Réingénie plutôt en code fin par-dessus tes propres
     primitives.
   - *La capacité est-elle réelle ?* Vérifie les affirmations contre des preuves
     indépendantes. Le blog d'un vendeur est une affirmation, pas une preuve.
     Verdict : réel / hype / arnaque / invérifiable.
   - *Sorties réseau bornées :* tout ce que la version adoptée va chercher doit être
     ralenti, mis en cache, et tuable.
4. **Déconstruis en carte de capacités.** Pour chaque capacité que le projet fournit,
   note : ce qu'elle fait, comment, ses coutures porteuses, son gras ou son risque, ce
   que tu peux réutiliser de ta propre pile, et si elle atterrit en natif ou derrière un
   adaptateur fin. Chaque capacité est **préservée ou réfutée avec preuve**. Une
   capacité abandonnée en silence est un défaut.
5. **Écris la spec de réingénierie.** Les coutures à construire, le gras que tu retires
   (consigné à voix haute, jamais en silence), et un test-contrat en échec par capacité,
   qui vérifie un effet réel — un fichier, une ligne en base, une vraie sortie. Ne mocke
   que le transport d'une API externe payante, jamais la logique.
6. **Intégration native.** Applique [red-first](../red-first/SKILL.md) : observe
   un vrai échec et scelle le contrat avant la correction minimale à la frontière
   responsable. Garde le fichier de test initial intact. Cible les vraies commandes
   lint/typage/tests du dépôt avec [sniper-testing](../sniper-testing/SKILL.md)
   depuis `base_sha` jusqu'au `candidate_sha` actuel, chemins en attente possédés
   compris si pertinent. Note contrôles absents ou inapplicables ; n'installe pas
   un vérificateur arbitraire et n'invente pas de réussite. Exécute
   [clean-code-gauntlet](../clean-code-gauntlet/SKILL.md) dans le workflow pour les
   preuves de qualité et mutation. Une lacune reçoit une régression supplémentaire
   distincte, jamais une modification de l'original scellé. Tout reste dans le budget partagé.
7. **Vérifier la capacité adoptée.** Exerce le résultat natif contre la carte de
   capacités et la surface réelle de l'utilisateur. Réutilise les preuves de
   découverte ; demande une autre observation REA seulement pour une comparaison
   précise non résolue, dans les limites du fournisseur et de l'exécution existants.
   Choisis un évaluateur compétent via la matrice configurée pour une revue fraîche
   disjointe de l'auteur sur le candidat agrégé exact ; consigne et exclue
   l'exécution autrice. Le builder ne se note jamais. Exécute la passe obligatoire
   des suites affectées et suis la procédure de livraison autorisée du projet.
   Preuves statiques amont ou GREEN local seuls ne prouvent pas la livraison native réelle.
8. **Cite et consigne.** Écris le crédit d'échafaudage là où la capacité vit
   désormais : auteur, projet, licence, ce qui est emprunté (l'échafaudage) et ce qui
   est à toi (la réingénierie). N'invente jamais un crédit. N'en retire jamais un.
   Rends carte, candidat exact, résultats, attribution et lacunes au responsable.
   Si le budget expire ou un contrôle requis est impossible, sauvegarde
   **STILL-BUILDING** avec reste à faire et prochaine action ; poursuis le travail
   utile autorisé qui ne consomme pas le quota épuisé. Ne fabrique jamais
   **PROVEN** et n'abandonne pas silencieusement une capacité pour obtenir un succès.

## Règles dures — une seule suffit à rater le skill

- Copier du code tel quel au lieu de réingénier la capacité.
- Construire un doublon sans avoir jamais cherché l'existant.
- Croire le README ou une page marketing plutôt que le code.
- Installer une dépendance sauvage au lieu de réingénier la technique.
- Copier du code copyleft ou sans licence (technique seulement, toujours).
- Abandonner une capacité sans réfutation écrite.
- Du théâtre de mocks dans un test de capacité — le test doit toucher un effet réel.
- Livrer sans la citation d'échafaudage.

## Marche bien avec

- [red-first](../red-first/SKILL.md) — les tests-contrats qui gardent chaque capacité.
- [sniper-testing](../sniper-testing/SKILL.md) — de vrais effets, pas de théâtre de mocks.
- [blind-tribunal](../blind-tribunal/SKILL.md) — la notation indépendante du portage.
- [decision-bar](../decision-bar/SKILL.md) — les blocages de licence et les questions de goût remontent à ton humain ; tout le reste s'exécute.
