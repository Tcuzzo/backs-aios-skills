---
name: "blind-tribunal"
description: "À utiliser quand un changement autonome a besoin d'une note indépendante avant d'atterrir et qu'aucun humain n'est dans la boucle. Convoque des jurés à l'aveugle, de familles de modèles différentes — un angle chacun — sur une enveloppe de fichiers entiers expurgée de l'auteur ; chaque constat devient un nouveau test en échec ; boucle jusqu'à ce que chaque juré valide. Trigger words: blind tribunal, grill tribunal, tribunal, jurors, cross-family grade, convene, blind grade, independent grade, grade before landing, tribunal à l'aveugle, jurés, note inter-familles, convoquer, noter avant de livrer, verdict indépendant."
license: "MIT"
---

# Blind Tribunal — le tribunal à l'aveugle
**Effort:** heavy — huit jurés, un angle chacun, routés par palier vers la famille de modèles la moins chère qui suffit, reconvoqués sur des enveloppes fraîches à chaque tour jusqu'à l'unanimité ; à dépenser sur les changements autonomes qui atterrissent sans revue humaine. Élimine : les atterrissages sauvages que rien ne garde, sinon la parole du builder lui-même.

La boucle de notation qui permet à l'humain de s'éloigner sans que l'agent parte en
roue libre. Un panel de jurés examine le changement à l'aveugle, auteur effacé. Chaque
constat devient un nouveau test en échec. La boucle recommence jusqu'à ce que chaque
juré valide. Rien n'est livré sur la seule parole du builder.

## Quand le convoquer

- Avant de livrer tout changement autonome qu'aucun humain ne relira.
- Tout changement à grand rayon d'impact : sécurité, données, proche de l'autorité.
- Quand un seul correcteur ne suffit pas et que tu veux des angles indépendants sur le
  même artefact.

## Les sièges

Huit jurés, un angle chacun. Chacun est un modèle d'une famille DIFFÉRENTE de celle du
builder (même éditeur = même famille). Un juré à qui on demande de tout vérifier ne
vérifie rien correctement.

| Juré | Id d'angle | Palier | La question qu'il pose |
| --- | --- | --- | --- |
| Défaut | `defect` | généraliste | Qu'est-ce qui casse vraiment ? Erreurs de logique, de syntaxe, défauts nouveaux. |
| Proportion | `proportion` | généraliste | Est-ce la bonne taille ? Sur-construit, ou à la mesure de l'intention ? |
| Conséquence | `operator_consequence` | sécurité opérateur | Si un opérateur humain exécute ceci, qu'est-ce qui est destructeur, dangereux ou nuisible ? |
| Réversibilité | `reversibility` | état profond | Effets irréversibles ? S'il meurt en plein vol, le système revient-il en arrière proprement ? |
| Continuité | `state_continuity` | état profond | Variables orphelines, état global écrasé, contexte perdu pour les nœuds en aval ? |
| Économie | `resource_economy` | structurel rapide | Boucles non optimisées, appels réseau/API redondants, mémoire gonflée ? |
| Bornes | `boundary_condition` | structurel rapide | Entrées nulles, vides, mal typées ou malformées — échoue-t-il proprement ? |
| Télémétrie | `telemetry` | sécurité opérateur | Une panne ici se diagnostique-t-elle depuis les logs et la gestion d'erreurs ? |

**Paliers de routage (la route la moins chère qui suffit d'abord) :** état profond → le
plus grand contexte et le raisonnement le plus profond, idéalement via un harness qui LIT
le repo (n'écrit jamais) ; structurel rapide → d'abord un GPU local gratuit, FUSIONNÉ avec
un vérificateur cloud bon marché qui juge le même prompt : la lentille ne passe que si les
deux passent ; sans cloud, le verdict local reste, marqué UNVERIFIED, jamais « vérifié » en
silence ; et le modèle local doit voir TOUT l'artefact (dimensionne `num_ctx` sur le prompt
— le défaut d'Ollama, 4096, tronque en silence — et refuse avant l'envoi ce qui ne tient
pas) ; le vérificateur n'est jamais de la même famille que le siège primaire, et un siège UNVERIFIED est une mise en attente (jamais l'unanimité) ; les jurés par harness tournent en read-only, et chaque convocation porte un `run_id` et écrit son résumé en dernier ; ensuite les modèles cloud à faible latence ; sécurité opérateur → ton
codeur le plus fort ancré sur la sécurité ; généraliste → un grand généraliste fiable.
Chaque échelle finit sur un barreau local de survie.

**Montage solo.** Quand une seule famille de modèles est disponible, dégrade
EXPLICITEMENT : un contexte ou une session vierge qui n'a jamais vu la conversation de
l'auteur joue le correcteur aveugle, ou l'humain relit l'enveloppe expurgée. Le rapport
doit nommer la barrière affaiblie — « noté même-famille-à-l'aveugle, pas
inter-familles » — jamais faire semblant, en silence, que la barrière inter-familles a
tenu.

## Le constructeur est déclaré, et l'exclusion est structurelle

« Famille différente du constructeur » était une règle que les jurés devaient retenir. Lors du
propre test du tribunal, le siège de sécurité opérateur était mené par le modèle même qui avait
construit le candidat, et rien ne l'a enregistré ni exclu : l'auteur a noté son propre travail
pendant deux tours. Donc :

- **Convoquez avec le constructeur nommé** (`--builder <modèle-ou-famille>`). Le registre porte
  `builder_family`. Chaque barreau de cette famille est refusé à voix haute, avant tout envoi, sur
  chaque échelle. Une lentille sans barreau est EN ATTENTE — jamais renvoyée au constructeur.
- **Même fournisseur = même famille.** Une déclaration exclut tout le fournisseur.
- **Prouvez-le sur l'échelle vivante, pas dans un test :** la table de routage doit montrer que
  ses sièges sont passés à une autre famille. Sinon l'exclusion est décorative.

## L'enveloppe

Les jurés ne voient jamais le repo, le builder, ni la conversation. Ils voient une
seule enveloppe :

- **Les fichiers courants entiers** pour chaque fichier touché par le changement, plus
  ses fichiers de test. Jamais des bouts de diff nus — un hunk cache le contrat qui
  l'entoure et induit de faux constats.
- **Le contrat de revue** : l'intention du changement en une ligne, et les critères de
  réussite.
- **Zéro trace d'auteur.** Pas de noms, pas d'ids de modèle, pas d'auteurs de commit,
  pas d'historique de chat. Si l'identité fuit, la construction de l'enveloppe échoue
  fort — on ne note jamais sans l'aveugle.
- **Aucune prose sur l'ancien comportement.** Décrire ce que le code « faisait avant »
  plante des défauts fantômes. Les fichiers parlent d'eux-mêmes.

## Le verdict

Du JSON strict, lisible par une machine, un seul objet, pas de prose :

```json
{"verdict": "pass" | "refuse",
 "findings": [{"severity": "blocker|major|minor|info",
               "claim": "...", "evidence": "..."}]}
```

- **Un pass qui liste un constat `[blocker]` ou `[major]` n'est pas un pass.** Contradictoire, il
  échoue fermé en refuse, en nommant la sévérité.
- **Un verdict pour une autre lentille que celle siégée** est un barreau rejeté, pas un verdict :
  noté avec les deux lentilles, la marche passe au barreau suivant ; seulement si tous répondent à
  côté, la lentille est en attente. Jamais un pass.
- **Le répertoire de sortie est possédé avant d'être balayé.** L'organe appose un sceau (stamp) sur
  le répertoire qu'il revendique ; un répertoire portant ces formes de fichiers SANS le sceau est
  refusé, fichiers et remède nommés, rien supprimé. Un répertoire de fichiers étrangers n'a jamais
  été en danger et n'est pas bloqué.
- **Une lentille qui explose ne jette jamais les verdicts déjà payés.** Chaque échec est enregistré
  par lentille ; verdicts et résumé sont écrits AVANT de lever l'erreur.
- **La preuve de mutation nomme un fichier réécrit** (`changed_paths`).
- **Tout ce que l'organe écrit est réservé au propriétaire (0600).**
- **Un modèle local débordé n'est déchargé que par son DERNIER détenteur.** Deux lentilles peuvent
  partager une carte ; la première finie ne retire pas le modèle à l'autre en plein appel.
- **Un barreau qui ne peut pas contenir l'artefact est sauté avant l'appel**, raison notée ; un
  refus de capacité est un TYPE et la marche continue — jamais un arrêt.
- Un juré qui a MAL répondu — du déchet, du non-JSON, un texte de refus — compte comme
  **refuse** ; un juré qui n'a JAMAIS répondu (panne de transport, injoignable) est un
  **hold** : re-siège-le via [fleet-ladder](../fleet-ladder/SKILL.md), jamais un pass
  silencieux. Un seul essai par juré qui répond et par tour — pas de retries.
- Un pass nu, zéro constat et zéro preuve, est un **vote pauvre en information**. Il
  compte, mais jamais comme seule preuve — deux pass nus ne pèsent pas plus qu'un
  refuse détaillé. Un pass solide nomme ce qu'il a vérifié.

## La boucle

1. Rouge d'abord : committe le test-contrat en échec AVANT de construire le correctif,
   et consigne ce commit. Le builder n'a pas le droit de toucher le test
   ([red-first](../red-first/SKILL.md)).
2. Construis jusqu'au vert.
3. Construis l'enveloppe à partir des fichiers COURANTS.
4. Assieds les huit jurés, par palier, — des familles différentes de celle du builder
   ([fleet-ladder](../fleet-ladder/SKILL.md) résout ce qui est en vie).
5. Chaque juré vérifie aussi, il ne se contente pas de lire : les nouveaux tests
   passent ; la suite de régression n'est pas pire que la base ; et un contrôle
   anti-faux-vert — un test qui DEVRAIT échouer (le bug réintroduit) échoue bien. Un
   faux vert vaut refuse.
6. Sur tout refuse : CHAQUE constat — blocker, major et minor — devient un NOUVEAU
   test en échec, qui échoue pour la vraie raison du constat. Corrige. Reconstruis
   l'enveloppe sur les fichiers révisés. Reconvoque TOUS les jurés. Un verdict sur des
   fichiers périmés n'est pas un verdict.
7. Ne livre que sur pass unanime. Les constats minor levés au dernier tour se ferment
   aussi, jamais reportés — « les blockers corrigés, les minors plus tard » est
   exactement la fuite que ce skill existe pour stopper. Un constat finit CORRIGÉ ou
   réfuté avec preuve consignée, jamais garé.

## Le pied nomme la lentille, un barreau rejeté garde ses mots, et le plancher a trois barreaux

Le tour 4 a mis deux lentilles en attente avec zéro refus, et chaque maillon était au dossier. Trois lois en sont sorties :

- **Énonce la forme de la réponse à côté de la réponse.** Le pied du protocole porte le nom littéral de la lentille (`"lens": "defect"`), jamais le marqueur `<your lens>`. Un juré à qui l'on demandait de se rappeler la lentille énoncée 350 KB plus haut, dans un artefact qui nomme les huit lentilles, a répondu la mauvaise lentille trois fois en deux tours. Remplis le marqueur au rendu.
- **Un barreau rejeté laisse ses mots au dossier.** Une réponse à la mauvaise lentille ou un verdict annulé porte un `raw_tail` borné sur l'entrée rejetée, pour que le tour suivant lise la cause au lieu de la deviner.
- **Deux barreaux cloud ne font pas un plancher.** Chaque niveau tient au moins trois barreaux sans `context_tokens` déclaré (ils portent un artefact de 120k tokens) avant sa queue locale. Une mauvaise lentille plus une annulation ne doivent jamais mettre une lentille en attente.
- **Rien d'autre n'écrit dans le dépôt du tribunal pendant qu'il siège.** Le fichier d'état d'un correcteur concurrent, dans le checkout, a changé des octets sous un siège, et l'organe a annulé ce verdict honnêtement : il ne peut pas attribuer un changement. Sérialise les écrivains, ou siège sur un worktree séparé du même commit.

## Règles dures — une seule enfreinte annule la note

- Le builder ne note jamais son propre travail : ni la même instance, ni la même
  famille.
- **Un refus de juré ne vaut que ce que vaut l'enveloppe.** Avant d'écrire un test à
  partir d'un constat, vérifie le constat contre les fichiers réels. Un constat sur du
  code que l'enveloppe n'a jamais porté veut dire : corrige l'enveloppe, pas le code.
- Mesure la convergence sur les NOUVEAUX constats par tour, pas sur le total brut. Des
  nouveaux constats stables ou en hausse deux tours de suite : arrête et remonte à
  l'humain. Ne t'acharne jamais.
- N'affaiblis ni ne modifie jamais les tests en échec pour arracher un pass. Les jurés
  vérifient que les fichiers de test n'ont pas bougé depuis le commit rouge.
- **Un survivant est une affirmation ; une preuve verte est une affirmation.** Relancez à la main
  chaque mutant survivant, dans un arbre isolé, avec un plafond qui survit à la charge. Un timeout
  n'est pas un survivant ; une erreur de collecte n'est pas une mort. Chaque chemin de verdict doit
  pouvoir dire INVALID, et un harnais dont la ligne de base sans mutation n'est pas vert propre
  refuse d'émettre des verdicts.
- Un pass unanime ouvre la porte ; ce n'est pas l'arrivée. Livre, puis prouve la
  capacité en vif sur la vraie surface. Vert sans preuve en vif, ce n'est pas fini.

## Marche bien avec

- [red-first](../red-first/SKILL.md) — le contrat en échec, committé avant que le builder ne tourne.
- [sniper-testing](../sniper-testing/SKILL.md) — de vrais effets, des runs ciblés, pas de théâtre de mocks.
- [seam-engineering](../seam-engineering/SKILL.md) — corriger la classe, balayer les frères, poser un garde.
- [repair-loop](../repair-loop/SKILL.md) — la boucle de build que ce tribunal note.
- [blind-eval](../blind-eval/SKILL.md) — la barrière garder-ou-annuler, plus légère, quand la question est le goût, pas les défauts.

> Crédit d'échafaudage : Matt Pocock, grill-me / grilling (mattpocock/skills, MIT).
> Le design du tribunal adversarial aveugle inter-familles est BACKS AIOS.
