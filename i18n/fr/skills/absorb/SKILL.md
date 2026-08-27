---
name: absorb
description: À utiliser quand il te faut une capacité qu'un projet open source fournit déjà — adopte-la et réingénie-la en skill natif au lieu d'inventer un doublon. Trigger words: absorb, adopt, port, re-engineer, ingest a repo, prior art, capability port, make this native, absorber, adopter, porter, réingénier, ingérer un repo, l'existant, rendre natif.
license: MIT
---

# Absorb — Adopter l'existant, pas le réinventer
**Effort:** light — une ingestion de repo (sonde des métadonnées + clone superficiel) et une notation inter-famille du portage. Élimine : réinventer une capacité que l'existant a déjà résolue — le doublon écrit de zéro dont chaque bug serait à ta charge.

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

1. **Chasse l'existant d'abord.** Cherche avant de construire. Un doublon que tu
   inventes vaut moins qu'un échafaudage que tu adoptes : tu hérites de zéro test
   terrain et tous les bugs sont pour toi.
2. **Ingère au-delà du README.** Récupère les métadonnées du projet (licence, activité,
   langage) via l'API de la plateforme. Fais un clone superficiel dans un répertoire de
   brouillon. Lis le code et les tests. Le README, c'est du marketing ; le code, c'est
   la vérité.
3. **Passe les barrières de confiance.**
   - *Licence :* permissive (MIT / Apache / BSD / MPL) = réingénierie sans risque.
     Copyleft (GPL / AGPL) = technique seulement — réingénie l'idée, ne copie jamais le
     code. Pas de licence = traite comme tous-droits-réservés, technique seulement.
     Clause non commerciale = un blocage ; remonte-le à ton humain.
   - *Scan louche :* greppe les motifs de cloaking / spam / faux avis / arnaque.
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
6. **Reconstruis rouge d'abord.** Committe les tests en échec, puis construis jusqu'au
   vert sur toute la couture. Un modèle d'une autre famille que le builder note le
   résultat — le builder ne note jamais son propre travail.
7. **Cite et consigne.** Écris le crédit d'échafaudage là où la capacité vit
   désormais : auteur, projet, licence, ce qui est emprunté (l'échafaudage) et ce qui
   est à toi (la réingénierie). N'invente jamais un crédit. N'en retire jamais un.

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
- [blind-tribunal](../blind-tribunal/SKILL.md) — la notation inter-familles du portage.
- [decision-bar](../decision-bar/SKILL.md) — les blocages de licence et les questions de goût remontent à ton humain ; tout le reste s'exécute.
