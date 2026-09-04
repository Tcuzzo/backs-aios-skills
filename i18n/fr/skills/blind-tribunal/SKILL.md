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
pas) ; ensuite les modèles cloud à faible latence ; sécurité opérateur → ton
codeur le plus fort ancré sur la sécurité ; généraliste → un grand généraliste fiable.
Chaque échelle finit sur un barreau local de survie.

**Montage solo.** Quand une seule famille de modèles est disponible, dégrade
EXPLICITEMENT : un contexte ou une session vierge qui n'a jamais vu la conversation de
l'auteur joue le correcteur aveugle, ou l'humain relit l'enveloppe expurgée. Le rapport
doit nommer la barrière affaiblie — « noté même-famille-à-l'aveugle, pas
inter-familles » — jamais faire semblant, en silence, que la barrière inter-familles a
tenu.

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
