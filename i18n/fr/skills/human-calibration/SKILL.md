---
name: "human-calibration"
description: "À utiliser quand un build, un design ou une décision UX qui compte démarre et qu'il faut d'abord rencontrer l'humain qu'il sert. Charge ou construit un profil de session — comment cet humain pense, décide et veut qu'on lui parle — puis pilote tout le build à travers lui. Trigger words: yoke, know your human, human profile, session profile, grounding ladder, interaction model, intent, connais ton humain, profil humain, profil de session, échelle d'ancrage, intention."
license: "MIT"
---

# Connais ton humain
**Effort:** light — une passe de profil : charger le profil sauvegardé, ou le construire à partir d'au plus 7 questions posées l'air de rien. Élimine : réinterroger un humain qui a déjà répondu, et le rework des builds qui ont mal lu son goût.

Un build qui lit mal son humain est faux avant la première ligne écrite. Ce skill
remplace la devinette par un modèle de travail de l'humain qu'il sert : sa façon de
penser, son goût, son registre, et les endroits où sa parole se prend telle quelle.
Rejoins l'humain là où il est — ne l'oblige jamais à monter au niveau du système.

## Quand l'utiliser

Au départ de tout build, design, amélioration ou décision d'UX qui engage. Pas une
décoration de chat.

## Le flux : profil ou questions

1. **Identifie l'humain.** Regarde `.agent/profiles/<humain>.md` dans le projet, puis
   le dossier de config du home de l'agent (par ex. `~/.claude/profiles/<humain>.md`)
   pour un profil tous-projets. Si un profil validé existe là, charge-le et
   applique-le. Ne re-questionne jamais un humain qui en a déjà un.
2. **Pas de profil ? Lance le protocole de questions** (plus bas). Jusqu'à 7 questions
   décontractées, plus au maximum 3 relances là où une réponse ouvre un fil. Toujours
   optionnel — un humain qui en esquive une se profile depuis le comportement observé
   à la place. Jamais une barrière sur le travail.
3. **Synthétise un profil de session** (template plus bas). Chaque champ porte une
   `source` et un `status`. Une section sans preuve reste vide : vide est honnête,
   deviné est une inférence cachée.
4. **Réconcilie l'objectif.** Reformule l'intention du build à travers le profil, dans
   le registre propre de l'humain — un paragraphe simple, pas une spec. Il confirme ou
   corrige. Sa correction est définitive.
5. **Re-prompte-toi.** Avant d'exécuter, réécris ton prompt de travail à travers le
   profil : ce qu'il a voulu dire, quelles affirmations croire, lesquelles méritent un
   contrôle discret, ce qui lui paraîtra vivant et ce qui lui paraîtra irrespectueux.
6. **Construis avec le profil comme main directrice** — les décisions de design,
   d'ingénierie, d'UX et de goût passent toutes par lui.
7. **Apprends.** Les choix observés, les rejets et les corrections mettent le profil à
   jour — sauvegardé dans `.agent/profiles/<humain>.md` (ou le dossier de config du
   home pour un profil tous-projets). La correction gagne, instantanément.

## L'échelle d'ancrage (ordre de priorité, absolu)

```
CORRECTION DE L'HUMAIN
  > COMPORTEMENT RÉPÉTÉ OBSERVÉ
  > ARCHÉTYPE DÉCLARÉ     (ce qu'il dit être)
  > MOTIF CULTUREL        (ce que cet archétype déclaré implique d'habitude)
  > SUPPOSITION DU MODÈLE
```

Aucun barreau du bas n'écrase jamais un barreau du dessus. Les archétypes et les
motifs culturels sont un contexte de pilotage, jamais une case — le comportement
observé et la correction passent devant.

## Le protocole de questions

Règles de conception : aucun diplôme requis pour répondre. Du vrai/faux et du
soit-l'un-soit-l'autre, décontractés. Une à la fois, semées dans la conversation sur
l'objectif — jamais tirées en rafale, jamais notées, jamais répétées. Capture la
formulation propre de l'humain ; elle compte autant que la réponse.

Les 7 questions cœur (chacune lit deux axes ou plus à la fois) :
1. Nouveau gadget : tu lis d'abord comment ça marche, ou tu appuies direct sur les
   boutons ? → style de traitement, confort au risque.
2. Vrai/faux : les bugs moches te gênent plus que les lents. → priorité de goût
   (esthétique vs mécanique).
3. Un ami en retard : un petit texto, ou un appel avec toute l'histoire ? → registre
   (compressé vs narratif).
4. Construire une cabane : tu vois d'abord la cabane finie, ou la première planche ?
   → pensée d'ensemble vs pensée par étapes.
5. Vrai/faux : une règle qui n'a pas de sens doit quand même être suivie. →
   acceptation vs remise en cause du cadre.
6. Trois bonnes options, ou une recommandation forte que tu peux rejeter ? →
   préférence d'autorité — règle directement comment tu présentes les décisions.
7. Son travail se fait critiquer : il défend, il corrige, ou il demande ce que l'autre
   ferait à sa place ? → style de correction — règle comment tu livres les constats
   durs.

Relances (max 3, seulement là où une réponse cœur ouvre un fil) : l'instinct est-il
fiable partout ou seulement là où il excelle (carte de confiance) ; « assez bien,
c'est assez bien ? » (biais de livraison) ; liberté de changer plus tard vs certitude
que ça marche aujourd'hui (goût de la réversibilité) ; est-ce encore le sien après
qu'un autre l'a édité (propriété) ; « qu'est-ce que les gens comprennent de travers
sur ta façon de bosser ? » (ancre d'identité, dans ses mots).

## La règle de confiance

Le profil cartographie où le jugement de cet humain est fort et où il est faible.
- **Zone forte + affirmation confiante → crois-la.** Pas de re-dérivation, pas de
  double contrôle, pas de rappel des bases.
- **Zone faible + affirmation vague → un contrôle discret.** Pose une question
  décontractée qui lève l'ambiguïté, ou propose ton interprétation pour une
  confirmation en un mot. Ne le contredis jamais en face ; ne substitue jamais ton
  propre plan en silence.
- **N'utilise jamais le profil pour plafonner ce que l'humain a le droit de tenter.**
  Il règle COMMENT tu écoutes, jamais SI tu obéis.

## Template de profil de session (compact)

```markdown
# PROFIL DE SESSION — <humain>
## Ancres d'identité   # valeur + source (declared|observed|cultural|guess) + status (confirmed|working|needs-validation|rejected)
## Schéma de travail   # un paragraphe : comment les ancres se combinent pour CET humain
## Traits de pilotage  # « susceptible de : <comportement> » → « donc je : <règle d'agent concrète> »
## Carte de confiance  # zones fortes (croire telles quelles) / zones faibles (un contrôle discret)
## Tension centrale    # les besoins à-la-fois qui semblent contradictoires mais sont des exigences
## Risque de mal-lu    # la mauvaise lecture la plus probable, énoncée comme interdiction
## Registre            # date, barreau de l'échelle, changement, preuve
```

Un profil de session est borné à la session : dans une nouvelle session, il est une
donnée, pas une vérité, tant que l'humain ne l'a pas reconfirmé ou que le comportement
ne l'a pas re-mérité. Le profil est la propriété de l'humain : montre-le sur demande,
corrige-le à la seconde où il dit que c'est faux, et n'agis jamais sur une inférence
qu'il ne peut pas voir — ça, c'est une barrière cachée.

## Règles dures (une seule fait rater le skill)

- Re-questionner un humain qui a déjà un profil validé.
- Faire ressembler les questions à un examen, ou les rendre obligatoires.
- Un champ deviné déguisé en champ confirmé.
- Un barreau du bas de l'échelle qui écrase un barreau du dessus.
- Utiliser le profil pour limiter ce que l'humain a le droit de tenter.
- Rabaisser l'objectif parce qu'une route est incomplète. Sépare : capacité visée →
  frontière actuelle → route disponible maintenant → route nécessaire plus tard.

## Marche bien avec

- [human-voice](../human-voice/SKILL.md) — le registre pour répondre une fois que le profil dit comment il écoute.
- [decision-bar](../decision-bar/SKILL.md) — quelles décisions atteignent l'humain ; le profil façonne comment elles arrivent.
- [intent-compiler](../intent-compiler/SKILL.md) — le prompt de l'humain est la spec ; le profil te dit ce qu'il a voulu dire.
- [model-fusion](../model-fusion/SKILL.md) — la synthèse panel-puis-compression du profil.
