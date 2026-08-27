---
name: guided-steps
description: À utiliser quand une mise en place exige des étapes que seul un humain peut faire — dashboards tiers, identifiants, secrets CI, provisionnement, migrations ponctuelles, bascules. Rédige un script interactif étape par étape qui ouvre chaque URL, dit quoi cliquer et copier, capture les valeurs, et les écrit là où elles vont. Trigger words: wizard, human-only steps, provision, credentials, dashboard setup, CI secrets, cutover, assistant pas-à-pas, étapes humaines, identifiants, secrets CI, mise en place, bascule.
license: MIT
---

# Le wizard des étapes humaines

Certaines étapes, seul un humain peut les faire : cliquer dans le dashboard d'un tiers,
créer des identifiants, valider un écran de provisioning. C'est pénible à faire à la
main et pénible à réexpliquer à chaque fois. Le wizard (l'assistant pas-à-pas) les
transforme en parcours guidé : un script shell interactif, étape par étape, qui ouvre
chaque URL, dit exactement quoi cliquer et quoi copier, capture les valeurs, et les
écrit là où elles doivent vivre.

## Quand l'utiliser

- Une mise en place exige un humain au volant d'une UI qu'aucune API n'atteint —
  dashboards, consoles, écrans d'identifiants, pages de secrets CI, migrations
  ponctuelles, bascules.
- Le chemin est assez long pour que le réexpliquer à chaque fois fasse mal.

Quand NE PAS l'utiliser : une API peut faire l'étape (automatise-la plutôt — un wizard
est le dernier recours), ou la procédure tient en une ou deux étapes (dis-le
simplement à l'humain, avec des mots).

## La forme

Un seul script, deux parties :

- **Une bibliothèque d'aide en haut** — identique dans chaque wizard, jamais éditée à
  la main. Elle fournit : des en-têtes d'étape avec progression (« étape 3 sur 7 »),
  une narration à voix humaine, l'ouverture d'URL multiplateforme, la saisie masquée
  des secrets, des upserts idempotents dans `.env` (mettre à jour la clé si elle est
  là, l'ajouter sinon), l'écriture vers le coffre de secrets de ton fournisseur CI,
  une étape de confirmation/pause, et un résumé final de tout ce qui a été capturé.
- **Les étapes sous un marqueur** — la seule partie que tu écris. Une étape par action
  humaine : ouvrir l'URL, dire quoi cliquer et quoi copier, capturer la valeur,
  l'écrire à sa destination. Renseigne le nombre total d'étapes pour que l'affichage
  de progression soit honnête.

## Le déroulé

1. **Cadre.** Lis le fichier d'exemple d'env, le README, la config de déploiement et
   les workflows CI. Chaque secret ou variable qu'ils référencent est une valeur que
   le wizard doit produire. Montre à l'humain les étapes ordonnées et les valeurs
   d'entrée de jeu — fais confirmer le plan avant d'écrire.
2. **Trace le trajet de chaque étape.** Une ligne par étape : URL → action → valeur →
   destination. L'humain voit tout le chemin avant de partir.
3. **Écris.** Copie le template. N'écris que les étapes ; ne touche jamais la
   bibliothèque. Garde la narration en mots simples — la personne qui lance ça n'est
   peut-être pas ingénieur.
4. **Vérifie statiquement.** Contrôle la syntaxe du script (`bash -n`, shellcheck),
   rends-le exécutable, puis déroule chaque étape à la main : chaque URL est-elle
   bonne, chaque consigne claire, chaque cible d'écriture correcte ? Ne le lance PAS
   de bout en bout — il ouvre des navigateurs et bloque sur la saisie humaine.

## Règles dures

- **Les secrets ne touchent jamais un fichier suivi par git.** Les valeurs capturées
  atterrissent dans le `.env` gitignoré ou dans le coffre de secrets CI. Le script
  lui-même ne porte que des placeholders ; l'humain colle les vraies valeurs au moment
  du run. Une vraie clé, un vrai nom d'hôte ou un détail personnel dans le script
  écrit EST le bug.
- **Chaque écriture distante est en un seul coup et bornée.** Une écriture au coffre
  de secrets est un appel d'API : pas de boucles de retry, pas de martèlement. Échoue
  fort et laisse l'humain relancer l'étape.
- **Éphémère par défaut.** Un wizard se construit pour un run et se supprime après.
  Ne le committe que si l'humain demande un chemin de mise en place rejouable — et un
  wizard committé ne porte, lui aussi, que des placeholders.
- **L'étape de confirmation est le bouton pause de l'humain, pas une barrière.** Elle
  existe pour qu'il vérifie son travail — jamais pour lui mettre de la friction
  d'approbation.

## Marche bien avec

- [session-handoff](../session-handoff/SKILL.md) — consigner quelles étapes ont tourné si le run est coupé en deux.
- [human-voice](../human-voice/SKILL.md) — le registre dans lequel chaque étape parle.
- [bounded-loops](../bounded-loops/SKILL.md) — la règle anti-martèlement derrière les écritures distantes.

> Crédit d'échafaudage : Matt Pocock, wizard (mattpocock/skills). La composition et les règles dures d'ici sont BACKS AIOS.
