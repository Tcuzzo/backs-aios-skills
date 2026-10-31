---
name: "optimus"
description: "Au démarrage ou à la reprise d'une session, d'un job ou d'une boucle autonome qui a besoin du harnais BACKS et des skills pertinents."
license: "MIT"
---

# Harness Boot
**Effort:** light — une passe de démarrage par session pour charger le socle et les skills du job, plus un hook déterministe qui ne coûte rien à exécuter. Élimine : les éditions sans ancrage — des mutations faites avant que les règles soient lues, et la reprise qui suit une fois qu'elles le sont.

Une règle : **pas de code et pas de job tant que le harnais n'est pas chargé.**
Le harnais, c'est le socle d'invariants du pack plus les skills qui couvrent ce
job. Chaque session, chaque runtime, chaque fois. Pourquoi : une règle qu'un
agent doit retenir échoue exactement quand l'agent est le plus occupé — donc
charger les règles est le premier geste, et un hook rend ça structurel au lieu
de consultatif.

## Quand le lancer

Au début d'une session ou d'un nouveau job ; revalide après remise à zéro du contexte ou relève.
Un réessai interne réutilise l'ancrage actuel et le même dossier. Recharge les
textes absents ou modifiés ; ne redémarre pas tout le cycle à chaque itération.

## La séquence de boot

1. **Charge le socle invariant.** Lis [invariant-floor](../invariant-floor/SKILL.md)
   avant de toucher à quoi que ce soit. C'est le sol de toute la session.
2. **Applique [Build Flow](../backs-build-flow/SKILL.md).** Il possède mode de tâche,
   préparation à agir, choix des skills, RED/GREEN borné avec lint et tests ciblés,
   preuves du gauntlet et livraison. Réutilise un dossier vérifié ; recueille
   seulement les faits manquants pour la prochaine action. Les spécialistes
   reviennent à un seul responsable.
3. **Applique le contexte humain** ([human-calibration](../human-calibration/SKILL.md))
   si pertinent. [operator-essence](../operator-essence/SKILL.md) possède le fichier
   de contexte étayé et le passage d'insights si le fichier manque ; ne lance pas un second cycle de profil.
4. **Charge la session.** Le hook livre les textes réels d'Optimus, Yoke et Build
   Flow, plus le harnais natif prouvé s'il est disponible. La compaction recharge
   ces textes sans retirer l'ancrage acquis. Un marqueur absent lors d'un outil
   de modification déclenche le chargement, jamais le refus de l'outil. Les hôtes
   sans hook de contexte peuvent utiliser :
   ```bash
   node "$HOME/.local/share/backs-aios/current/hooks/aios_gate.js" --load backs-aios:optimus
   ```
   Dans un shell Codex, ajoute le `CODEX_SESSION_ID` actif comme dernier argument.
   Python est disponible via le chargeur `aios_gate.py` correspondant. Un skill
   inconnu renvoie un code non nul sans fabriquer de reçu.
5. **Applique les skills nécessaires à la prochaine action.** Nomme but, résultat
   et sortie de chacun. Un skill nommé sans invocation n'a pas eu lieu.
   Réutilise les textes réels encore disponibles dans le contexte ; ni résumé
   mémorisé ni hash de fichier ne les remplacent.
6. Ensuite seulement : écrire du code, lancer des commandes de modification ou changer quoi que ce soit.

## Ancrage automatique

Le hook existant lit les fichiers du socle et transmet leur texte par le
contexte hôte. Il consigne les hashes des sources seulement après livraison.
Les reçus de chargement de contexte sont distincts des vrais événements Skill ;
charger un pointeur ou hacher un fichier n'est pas invoquer le skill.

- Démarrage et compaction rechargent le socle sans retirer d'outils.
- Un marqueur de session absent provoque le chargement automatique au prochain outil correspondant.
- Textes absents ou illisibles produisent un diagnostic visible, sans faux reçu ;
  opérateur et agents conservent leurs outils.
- `--rearm <session_id>` demande un nouveau chargement. Il ne verrouille jamais la session.
- `AIOS_GATE=off` reste le kill-switch existant et réversible de l'opérateur.
- Les hooks sont locaux et déterministes. Aucun appel de modèle ni dépendance réseau n'est ajouté.

## Règles dures (ce qui fait échouer ce skill)

- Toute mutation avant que le harnais soit chargé.
- Un skill nommé dans un rapport qui n'a jamais été invoqué dans la session.
- Un hook qui refuse un outil, retire l'ancrage acquis ou annonce un chargement qui n'a pas eu lieu.
- Une deuxième barrière, ou toute nouvelle friction posée sur l'humain. Le
  kill-switch reste le sien.

## Fonctionne bien avec

- [invariant-floor](../invariant-floor/SKILL.md) — le socle que le boot charge en premier.
- [human-calibration](../human-calibration/SKILL.md) — l'étape profil du boot.
- [repair-loop](../repair-loop/SKILL.md) — ce qu'un job de fix exécute après le boot.
- [bounded-loops](../bounded-loops/SKILL.md) — les budgets de chaque boucle que le boot démarre.
- [wayfinder](../wayfinder/SKILL.md) — quand le boot montre que tu ne connais pas la route.
