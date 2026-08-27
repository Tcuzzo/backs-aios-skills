# Agent Builds

Comment construire un agent ou un service qui agit tout seul. L'idée centrale :
les primitives déterministes font le gros du travail ; le modèle ne raisonne que
là où le raisonnement est le seul outil qui marche. Un design tout-LLM, sans
aucune primitive, n'est pas valable.

## Quand le lancer

Pour construire n'importe quel agent, bot, worker ou service qui tourne en
continu — tout ce qui tient des outils, appelle le réseau ou agit sans qu'un
humain surveille chaque étape.

## La chaîne

1. [intent-compiler](../skills/intent-compiler/SKILL.md) — lis la demande en
   entier ; la mission et ses limites viennent des mots de l'humain lui-même.
2. [understanding-gates](../skills/understanding-gates/SKILL.md) — dès la phase
   de design, nomme d'abord les PRIMITIVES MÉTIER : chaque capacité cœur est une
   fonction déterministe, hors ligne, qui échoue fermé (fail-closed). Réserve la
   place du LLM au raisonnement véritable, rien d'autre.
3. [red-first](../skills/red-first/SKILL.md) — commite des tests de contrat qui
   échouent pour chaque frontière d'entrées/sorties typée, avant de la construire.
4. Construis selon la doctrine ci-dessous. Garde chaque boucle dans
   [bounded-loops](../skills/bounded-loops/SKILL.md) : budgets, checkpoints,
   backoff, et un kill-switch bruyant — jamais de retry qui martèle.
5. [sniper-testing](../skills/sniper-testing/SKILL.md) — seul le transport
   sortant peut être mocké — jamais le routage, la construction du prompt ou le
   parsing.
6. [clean-code-gauntlet](../skills/clean-code-gauntlet/SKILL.md) — les handlers
   d'outils et les fonctions de décision de l'agent passent le gauntlet : score
   de risque sous ton plafond, puis mutation sur les chemins de décision jusqu'à
   zéro survivant. Une logique de branche qui survit à une comparaison inversée
   n'a jamais vraiment été testée.
7. [blind-tribunal](../skills/blind-tribunal/SKILL.md) — des graders (les
   évaluateurs) d'une autre famille de modèles valident l'agent avant la
   livraison. Le builder (celui qui construit) ne note jamais son propre travail.

## La doctrine (ce que le build doit satisfaire)

- Chaque frontière d'entrées/sorties déclare un contrat typé (entrées → sorties)
  et ÉCHOUE FERMÉ — elle lève une erreur ou refuse sur une entrée invalide.
  Jamais d'échec ouvert, jamais d'erreur avalée.
- Chaque couture réseau est testable en cassette : enveloppe les appels sortants
  derrière une couture record/replay pour que la suite tourne hors ligne sur des
  fixtures.
- Tout trafic sortant passe par une allowlist explicite de noms d'hôtes, en
  refus par défaut. Un hôte inconnu lève une erreur ; il ne se connecte jamais
  en silence.
- Modélise l'agent comme un flux d'événements typé / une machine à états, avec
  des états de validation déterministes (draft → review → ready → done) que
  l'agent calcule lui-même — une primitive, pas une friction humaine. Aucune
  action ne saute son état.
- Ne confirme QUE les actions vraiment destructrices ou irréversibles (une
  dépense, une suppression, un envoi externe impossible à annuler), contre
  l'état commité, avant de tirer. Ne mets jamais de barrière sur une action
  bénigne ou en lecture seule, et jamais sur l'humain — voir
  [decision-bar](../skills/decision-bar/SKILL.md).
- Persiste l'état durable (objectifs, décisions, registre) sur disque, HORS de
  la fenêtre de contexte, et relis-le. Ne fais jamais confiance à la mémoire en
  contexte sur une longue session.
- Livre un doc d'exploitation que l'agent charge avant chaque tâche — le fichier
  le plus proche gagne, taille plafonnée — avec les règles qui s'appliquent
  toujours.
- Un échec d'outil renvoie une erreur structurée vers la place de raisonnement,
  pour auto-correction. Une erreur d'outil avalée est un bug.
- Moindre privilège : l'agent porte exactement les outils que sa mission exige —
  aucune autorité ambiante sur le système de fichiers ou le réseau.

## Barrières dures

- Zéro primitive = design invalide ; retourne à l'étape 2.
- Toute frontière fail-open, tout fallback silencieux, toute erreur avalée
  bloque la livraison.
- Des mutants survivants dans les chemins de décision bloquent la livraison.
- La note inter-famille doit passer ; le builder n'est jamais le grader.

## Marche bien avec

- [root-cause-first](../skills/root-cause-first/SKILL.md) — quand l'agent déraille
- [session-handoff](../skills/session-handoff/SKILL.md) — l'état durable, fait proprement

**Weight:** surtout de la discipline free plus une porte de design light ; la dépense heavy, ce sont les runs de mutation du gauntlet et le tribunal inter-famille — elle se rentabilise sur tout agent qui agira sans personne pour regarder.
