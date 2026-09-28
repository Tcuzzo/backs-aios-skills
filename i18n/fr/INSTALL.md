# Installer — brancher le pack sur un vrai agent

> **v0.7 portable installer:** Enregistrement actuel en une étape pour Claude Code, Codex, Cursor, OpenCode et les agents portables : `./install.sh --target all --locale fr`. Le script n’écrase rien ; sous PowerShell, utilise `./install.ps1`. La matrice complète des chemins actuels est dans [le guide d’installation canonique](../../INSTALL.md).

Le pack, c'est des dossiers de markdown. Chaque skill est un
`skills/<name>/SKILL.md`. Chaque play est un `plays/<name>.md`. Pas de
binaires, pas de serveur, pas d'étape de build. Installer, c'est mettre le
markdown là où ton agent cherche ses skills.

Le frontmatter est volontairement le sous-ensemble minimal à 3 clés — `name`,
`description`, `license` — de la convention ouverte Agent Skills
(agentskills.io). La spec n'exige que `name` et `description`, et les runtimes
conformes ignorent les clés qu'ils ne reconnaissent pas. Le pack se charge donc
nativement partout où la convention se charge, et se lit comme du markdown brut
partout ailleurs.

## 1. Plugin Claude Code (recommandé)

Deux commandes dans Claude Code :

    /plugin marketplace add Tcuzzo/backs-aios-skills
    /plugin install backs-aios

Ça installe tout d'un coup : les skills se chargent, les commandes slash
deviennent disponibles (tape `/optimus` pour démarrer le socle), et le hook
d'ancrage arrive activé — il bloque les outils qui modifient tant que le
harnais n'est pas chargé. Le kill-switch du hook t'appartient : mets
`AIOS_GATE=off` dans l'environnement pour le désactiver, bruyamment. Les mises
à jour passent par `/plugin` quand le dépôt marketplace bouge.

## 2. Claude Code, en manuel

Claude Code découvre aussi les skills depuis deux dossiers (confirmé sur les
docs officielles, 2026-08) : le dossier personnel
`~/.claude/skills/<name>/SKILL.md` (tous les projets de ta machine) et le
dossier projet `.claude/skills/` (embarqué avec un seul dépôt).

Personnel, en une ligne :

    git clone https://github.com/Tcuzzo/backs-aios-skills.git ~/backs-aios-skills && ln -s ~/backs-aios-skills/skills/* ~/.claude/skills/

Projet : `cp -r ~/backs-aios-skills/skills/* .claude/skills/`

Symlink si tu veux que les mises à jour du pack coulent d'elles-mêmes ; copie
si tu veux épingler la version (ou si les symlinks embêtent ton runtime).
Ouvre une nouvelle session. Un skill se déclenche quand la tâche matche sa
`description` — dis les mots déclencheurs et l'agent charge le fichier. Sur la
voie manuelle, les plays ne sont pas des skills : garde-les dans le clone et
demande à l'agent d'en lire un
(`read ~/backs-aios-skills/plays/elite-build.md`) en début de session, ou
colle ton play par défaut dans le CLAUDE.md du projet.

## 3. Tout runtime Agent Skills (la convention ouverte)

La convention est adoptée bien au-delà de Claude — OpenAI Codex, Gemini CLI,
Cursor, VS Code et d'autres (selon l'écosystème de la spec, 2026-08). Les
règles qui comptent ici : le fichier s'appelle exactement `SKILL.md` ; le nom
du répertoire égale le `name` du frontmatter ; seuls `name` + `description`
sont requis. Ce pack satisfait les trois. Installer = copier `skills/*` là où
ton runtime garde ses skills (Cursor utilise `.cursor/skills/`, par exemple).
Nous n'avons pas vérifié le dossier de chaque runtime — vérifie le chemin
exact dans les docs de ta plateforme.

## 4. OpenClaw, Hermes, autres frameworks d'agents

Confirmé sur leurs docs actuelles (2026-08) :

- **OpenClaw** découvre tout `SKILL.md` sous ses racines de skills
  configurées. Copie `skills/*` dans le dossier `skills/` de ton espace de
  travail, ou dans le dossier global partagé `~/.openclaw/skills`. La CLI
  `openclaw skills` gère installations et mises à jour.
- **Hermes (Nous Research)** garde un dossier par skill dans
  `~/.hermes/skills/`, et charge le SKILL.md d'un skill dans le prompt système
  quand la tâche l'active. Copie `skills/*` là-bas.

Tout autre framework — le motif générique, zéro code :

1. Monte ou colle chaque `SKILL.md` comme contexte invocable par outil (un
   outil de documents, une entrée de bibliothèque de prompts, un magasin de
   récupération). Garde la ligne `description` intacte — ses mots déclencheurs
   sont le contrat d'invocation.
2. Charge un play (`plays/*.md`) comme contexte système de la session. Un play
   nomme les skills qu'il déclenche, dans l'ordre ; l'agent tire ensuite
   chaque skill par son nom.
3. Vérifie le mécanisme d'installation actuel du framework dans ses propres
   docs avant de faire confiance à ce fichier — les mécanismes changent vite ;
   nous n'affirmons que ce que nous avons confirmé ci-dessus.

## 5. Boucle API nue (sans framework)

Le harnais, c'est toi. À chaque tour de boucle :

1. Mets `skills/invariant-floor/SKILL.md` dans le prompt système, toujours.
   C'est le socle que chaque changement doit franchir.
2. Choisis le play qui colle à la demande — build →
   `plays/elite-build.md`, bug → `plays/bughunt.md`, notation →
   `plays/grading-verification.md` — et ajoute-le à la suite.
3. Matche les mots de l'utilisateur contre les mots déclencheurs de la
   `description` de chaque skill. N'injecte jamais le pack entier — injecte
   le, les deux ou les trois skills qui matchent. Le pack est économe en
   tokens ; garde-le comme ça.
4. Ré-injecte à chaque remise à zéro du contexte. Une règle tombée du contexte
   n'est pas chargée.

## Première session

Installation plugin : tape `/optimus` et donne-lui la tâche. Installation
manuelle :

    Toi :   lis ~/.claude/skills/optimus/SKILL.md et démarre. Cette session le suit.
    Toi :   tâche — le total du panier est faux quand un coupon et une carte cadeau se cumulent.
    Agent : [démarre : charge invariant-floor, choisit plays/bughunt.md, nomme les skills qu'il va déclencher]
    Toi :   vas-y.
    Agent : [le play pilote : reproduire, test rouge, corriger la classe, vérifier en direct, notation à l'aveugle, atterrir]
