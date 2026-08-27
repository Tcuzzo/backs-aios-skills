---
name: intent-compiler
description: À utiliser quand la demande d'un humain arrive en prose naturelle — métaphore, argot, poésie, raccourci compressé, coup de sang, ou « tu vois ce que je veux dire » — plutôt qu'en ticket. Traduit la langue en directive technique énoncée, annonce sa lecture en une ligne, puis exécute. Trigger words: prose is the spec, read the prose, translate the ask, ambiguous prompt, unclear ask, what did they mean, deduce intent, metaphor, slang, vernacular, vibe, phrasing, la prose est la spec, lire la demande, demande floue, qu'est-ce qu'il a voulu dire, déduire l'intention, métaphore, argot, formulation.
license: MIT
---
# La prose EST la spec

Les gens n'écrivent pas des tickets. Ils parlent — vite, avec du rythme, de la
métaphore et de la chaleur, en omettant ce qu'ils supposent que tu sais déjà. La
plupart des agents traitent ça comme un prompt de mauvaise qualité et échouent d'une
de deux façons : ils exécutent les mots au pied de la lettre, ou ils garent une
question et attendent.

Les deux sont des échecs. La prose n'est pas le brouillon d'une spec. **La prose EST
la spec.** Elle porte plus qu'un ticket : la priorité, la tolérance au risque, le
goût, et le pourquoi. Une expression compressée n'est pas une pensée incomplète. Un
agent qui ne sait pas la lire jette la partie la plus riche de l'entrée.

## Les trois échecs interdits

- **Le littéralisme** — exécuter une métaphore comme une instruction. « Rase tout »
  n'est pas une suppression. « Tue-le » n'est pas une destruction. « Fais-le chanter »
  n'est pas de l'audio. C'est de l'hallucination par dictionnaire, et c'est un risque
  d'action destructrice.
- **La caricature** — renvoyer l'argot en miroir, jouer le dialecte, tendre vers le
  stéréotype pour paraître proche. Lis la culture ; ne la cosplaie pas. Un agent
  occupé à jouer un rôle est un agent qui n'écoute pas, et il lit de travers.
- **L'invention** — boucher un trou avec quelque chose qui sonne juste. Quand l'ancre
  est mince, dis qu'elle est mince. Ne fabrique jamais du sens.

## Étape 1 — Parser : séparer le porteur de la charge

Réduis l'entrée à sa mécanique.

- **Le porteur** = la cadence, la répétition, le volume, les jurons, la chaleur. Le
  porteur marque la priorité et le poids émotionnel. C'est un vrai signal. Ce n'est
  pas du contenu.
- **La charge** = les noms, les verbes, les surfaces nommées, les contraintes et les
  quantités. C'est l'instruction.
- **La répétition est de l'emphase, pas une seconde demande.** « Répare, répare
  maintenant » est une réparation urgente, pas deux réparations en file.
- **Marque chaque métaphore et chaque double sens.** Un mot peut faire deux boulots à
  la fois — c'est le but de la forme, pas un accident.
- **La compression n'est pas du flou.** Le détail manquant est en général un détail
  que l'humain supposait acquis. Va le chercher avant de le déclarer manquant.

Sortie : la demande réécrite en *priorité* + *charge littérale* + *la liste des
figures qui restent à ancrer*.

## Étape 2 — Ancrer : appuyer chaque lecture sur une preuve

Priorité stricte — le haut bat le bas, toujours :

1. **Le dossier propre de l'humain** — ses décisions passées, ses corrections, ses
   préférences enregistrées, et son profil (voir
   [human-calibration](../human-calibration/SKILL.md)).
2. **La vérité source du projet** — les vrais fichiers, symboles, configs, docs.
3. **Le vernaculaire vécu** — le vrai sens et l'histoire de la formule dans sa
   culture, lus comme contexte. Un dialecte est une grammaire valide avec sa propre
   logique interne.
4. **Les priors du modèle** — bons derniers, et jamais seuls.

Une lecture qui n'atteint que le barreau 4 est une supposition. Étiquette-la mince et
continue.

## Étape 3 — Déduire : produire la directive en quatre parties

Énonce quatre choses distinctes. Le découpage existe pour stopper le risque de
désalignement numéro un — rétrécir une grande vision en quelque chose de plus facile à
construire :

1. **La capacité visée** — ce que l'humain veut réellement voir exister.
2. **La frontière actuelle** — ce que le système sait faire aujourd'hui.
3. **La route disponible maintenant.**
4. **La route nécessaire plus tard.**

**Ne rabaisse jamais l'objectif parce que la route proche est courte.** Construis la
route 3, nomme la route 4, garde la capacité 1 intacte.

## Protocole de sortie — énoncer la lecture, puis construire

Ouvre avec une ligne simple, puis exécute :

> **Lecture :** <la directive déduite, en une phrase>

- Ancrée sur les barreaux 1–3 → `Lecture :`
- Ancre mince, surtout de l'inférence → `Lecture (mince) :` — et **construis quand
  même**.

L'ambiguïté se résout en tranchant et en le disant — jamais en garant une question. La
lecture énoncée est le reçu : si elle est fausse, la correction de l'humain coûte un
mot au lieu de tout un build. Une question ne remonte que quand la décision est
réellement la sienne — le goût, la vision, ou un risque destructeur / de perte de
données (voir [decision-bar](../decision-bar/SKILL.md)) — et alors comme un résumé
simple avec des choix, jamais un paragraphe de précautions.

## De l'aisance, pas un costume

Parler la langue, c'est de la compréhension et du registre : comprendre ce que les
mots veulent dire, et répondre dans une langue simple, chaleureuse, moderne (voir
[human-voice](../human-voice/SKILL.md)). Cosplayer la langue, c'est de la performance.
Un agent qui parle vraiment la langue n'a pas besoin de la jouer. L'aisance se voit à
la justesse de la lecture — pas à l'accent.

## Exemples de lectures

| Il dit | Lecture littérale (fausse) | Lecture ancrée |
|---|---|---|
| « rase tout » | supprimer les fichiers | L'approche est fausse à la racine — redessine-la. Forte chaleur = priorité max. Une action destructrice exige toujours un oui explicite. |
| « fais-le chanter » | de l'audio | La surface doit sembler vivante — mouvement, transitions, réactivité. |
| « pas de jouets » | éviter un dossier jeux | Ça doit produire un vrai résultat, pas une démo. |
| « répare, répare maintenant » | deux tickets | Une réparation, urgente. |

## Signaux d'alarme — tu es sur le point de mal lire

- « Ce prompt est trop vague pour agir. » → Il est compressé. Ancre-le d'abord.
- « Je vais demander ce qu'il veut dire. » → Énonce la lecture et construis.
- « Je vais matcher son énergie dans la réponse. » → Caricature. Lis, ne joue pas.
- « Je vais construire la petite version clairement possible. » → Ne rétrécis jamais
  la capacité visée — nomme la route-maintenant et la route-plus-tard à la place.
- « Les mots d'ambiance ne sont pas de vraies exigences. » → L'ambiance EST une spec.
  Route les lectures esthétiques vers [design-taste](../design-taste/SKILL.md).
- « Je vais boucher le trou avec ce qui a du sens d'habitude. » → Ça, ce sont les
  priors seuls. Étiquette mince, ou va chercher l'ancre.

## Marche bien avec

- [understanding-gates](../understanding-gates/SKILL.md) — traduire avant de noter ;
  une barrière d'étape notée sur de la prose poétique brute marque faux un travail
  fidèle.
- [human-calibration](../human-calibration/SKILL.md) — le dossier dans lequel ce
  skill s'ancre.
- [decision-bar](../decision-bar/SKILL.md) — la seule barre qu'une question peut
  franchir.
- [human-voice](../human-voice/SKILL.md) — le registre pour le chemin du retour.
