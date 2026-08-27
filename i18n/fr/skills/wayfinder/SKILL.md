---
name: wayfinder
description: À utiliser quand tu es perdu, que la suite est floue, ou qu'il faut décider quoi travailler ensuite. Trace une carte de décisions vers la destination au lieu de déposer une question sur l'humain. Trigger words: wayfinder, the path, chart the route, map the work, what next, lost, fog of war, decision map, frontier, tracer la route, cartographier le travail, et maintenant, perdu, brouillard de guerre, carte de décisions, frontière.
license: MIT
---

# Wayfinder

Quand tu ne connais pas le chemin, le geste facile est de t'arrêter et de
poser à l'humain une question qu'il t'a embauché pour résoudre. Le wayfinder
trace la route à la place : construis une carte de décisions, résous les
inconnues par la preuve, et ne fais remonter que les appels qui sont vraiment
ceux de l'humain.

## Quand le lancer

- Tu es perdu, ou la prochaine étape est floue.
- Un gros chantier doit être décomposé avant que quiconque construise.
- Tu sens l'envie de demander « qu'est-ce que tu veux que je fasse ? »

## Les étapes

1. **Nomme la destination.** Un objectif nommé dans ton tracker, plus un
   prédicat de clôture : comment tu sauras que c'est fini. La destination fixe
   le périmètre.
2. **Cartographie ce que tu vois.** Crée des tickets sur la frontière — les
   décisions prêtes à être résolues maintenant. Chaque ticket résout une
   **décision**, pas une tranche de travail de build.
3. **Laisse le reste dans le brouillard.** Les décisions que tu sens venir
   sans pouvoir encore les cerner vont dans une section **Pas encore
   spécifié** : la question soupçonnée, la zone à revisiter. Ne prédécoupe pas
   le brouillard en morceaux de la taille d'un ticket — il est plus grossier
   qu'un ticket, et une nappe peut se transformer en plusieurs tickets, ou en
   aucun.
4. **Écarte du travail à voix haute.** Le travail au-delà de la destination
   n'est pas du brouillard — il va dans une section **Hors périmètre** et n'en
   sort jamais. Si un ticket vivant se révèle au-delà de la destination,
   ferme-le et laisse une ligne dans Hors périmètre.
5. **Type chaque ticket** (voir Types de tickets ci-dessous).
6. **Résous une décision par la preuve.** Lis le code, les docs, le dossier —
   une preuve déterministe ferme un ticket sans deviner. Résoudre un ticket
   dissipe le brouillard devant lui : fais passer en tickets neufs ce qui est
   maintenant spécifiable, un par un.
7. **Passe la main quand le chemin est net.** La carte est finie quand il ne
   reste rien à décider avant que quelqu'un aille faire la chose. L'envie de
   juste faire le travail est le signal que tu as atteint le bord de la carte.

## Brouillard ou ticket ?

Le test, c'est si tu peux énoncer la question **précisément** maintenant — pas
si tu peux y répondre maintenant. Ticket quand la question est nette, même
bloquée. Pas-encore-spécifié quand tu ne peux pas encore la formuler aussi
nettement.

## Types de tickets

Chaque ticket est **humain-dans-la-boucle** (travaillé en direct avec un
humain) ou **agent-seul**. Un ticket humain-dans-la-boucle ne se résout que
par l'échange vivant — l'agent ne se substitue jamais au côté humain. Un agent
qui répond à ses propres questions de grill a cassé cette règle.

- **Recherche** (agent-seul) — un agent de recherche en arrière-plan le
  résout ; les trouvailles atterrissent sur une branche de brouillon avec un
  pointeur depuis le ticket. Voir [live-research](../live-research/SKILL.md).
- **Prototype** (humain-dans-la-boucle) — monte la fidélité avec un artefact
  brut et pas cher auquel l'humain peut réagir.
- **Grill** (humain-dans-la-boucle) — la conversation qui fait sortir la
  décision. Le type par défaut.
- **Tâche** (l'un ou l'autre) — du travail manuel qui doit se faire avant
  qu'une décision soit possible : s'inscrire à un service, provisionner un
  accès, déplacer des données. Le seul type qui *fait* au lieu de décider ; il
  gagne sa place en débloquant une décision.

## Règles dures

- **Ne dépose jamais sur l'humain une question** que la preuve, le code ou les
  règles en vigueur peuvent résoudre. Seuls le goût, la vision et le risque
  destructeur remontent — voir [decision-bar](../decision-bar/SKILL.md).
- **Désigne le travail par son nom, jamais par un id nu.** Un mur de #42, #43,
  #44 est illisible ; les noms se lisent d'un coup d'œil. L'id ou le lien
  voyage dans le nom — il ne le remplace jamais.
- **Une décision par session.** Résous au plus un ticket par session, tickets
  de recherche exceptés. Cartographier est le travail d'une session ; ça ne
  résout rien à la main.
- **Planifie, ne fais pas.** La carte produit des décisions, pas des
  livrables.
- **Quand la demande elle-même est le brouillard** — la destination est floue
  parce que la demande est arrivée en prose ou en métaphore — lis d'abord la
  demande avec [intent-compiler](../intent-compiler/SKILL.md), puis
  cartographie à partir de ce qu'elle dit vraiment.

## Fonctionne bien avec

- [live-research](../live-research/SKILL.md) — résout les tickets de recherche agent-seul.
- [decision-bar](../decision-bar/SKILL.md) — quelles décisions atteignent vraiment l'humain.
- [human-voice](../human-voice/SKILL.md) — comment la carte se lit pour un humain.

> Crédit d'échafaudage : Matt Pocock, wayfinder (mattpocock/skills, MIT). La composition et les règles dures ici sont BACKS AIOS.
