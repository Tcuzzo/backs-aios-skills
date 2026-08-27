---
name: optimus
description: À utiliser au démarrage de toute session, job ou boucle d'agent — avant d'écrire la moindre ligne de code. Boot harnais-d'abord : charge le socle d'invariants et les skills que le job exige, pour que l'agent lise les règles avant de travailler ; inclut le patron de hook grounding-gate qui bloque les outils mutants tant que le harnais n'est pas chargé. Trigger words: optimus, harness-boot, harness first, load the harness, boot the floor, grounding gate, read the floor, no code without harness, session start, boot sequence, harnais d'abord, charger le harnais, booter le socle, lire le socle, pas de code sans harnais, démarrage de session, séquence de boot.
license: MIT
---

# Harness Boot

Une règle : **pas de code et pas de job tant que le harnais n'est pas chargé.**
Le harnais, c'est le socle d'invariants du pack plus les skills qui couvrent ce
job. Chaque session, chaque runtime, chaque fois. Pourquoi : une règle qu'un
agent doit retenir échoue exactement quand l'agent est le plus occupé — donc
charger les règles est le premier geste, et un hook rend ça structurel au lieu
de consultatif.

## Quand le lancer

Au début de chaque session, job, mission et boucle. À nouveau après un reset de
contexte ou une passation. Charger le harnais une fois puis rouler en roue libre
une semaine, ce n'est pas charger le harnais.

## La séquence de boot

1. **Charge le socle d'invariants.** Lis [invariant-floor](../invariant-floor/SKILL.md)
   avant de toucher à quoi que ce soit. C'est le sol sur lequel toute la session
   se tient.
2. **Charge la carte de ce job.** Nomme quels fichiers, quelles règles et quels
   skills du pack gouvernent ce travail précis. Si tu ne peux pas les nommer, tu
   n'es pas prêt à éditer.
3. **Charge le profil humain** ([human-calibration](../human-calibration/SKILL.md))
   quand le job touche au goût, à la surface ou au workflow d'un humain.
4. **Invoque les skills que le job exige — en temps réel, dans cette session.**
   Un skill nommé mais pas invoqué n'a pas eu lieu. Travailler « de mémoire d'un
   skill », ce n'est pas l'invoquer.
5. Seulement ensuite : écrire du code, lancer des commandes mutantes, ou changer
   quoi que ce soit.

## Le patron grounding-gate

Rends l'étape 4 structurelle avec un **hook pre-tool-use** déterministe — un
petit script que ton runtime d'agent appelle avant chaque appel d'outil :

- Chaque session démarre **ROUGE**.
- Tant que c'est ROUGE, les outils en lecture seule (read, grep, search, fetch)
  passent toujours. L'agent s'ancre librement.
- Tant que c'est ROUGE, le hook **bloque les outils mutants** (edit, write,
  delete) et les verbes shell mutants principaux (commit, push, rm, install,
  restart de service, éditions en place).
- Invoquer n'importe quel skill du harnais **fait passer la session au VERT**
  (capté par un hook post-tool-use). Ensuite l'agent peut agir.
- **Réarmement :** l'état repasse au ROUGE à chaque démarrage de session. Pour
  les longues sessions, réarme par job ou par action, pour qu'un VERT périmé ne
  se glisse jamais dans du travail sans ancrage.

Règles de conception pour le hook lui-même :

- **Déterministe et gratuit.** Aucun appel de modèle, aucun réseau, aucune
  dépendance. L'état est un petit fichier par session, écrit atomiquement.
- **Il force l'ancrage, ce n'est pas un bac à sable.** Ne matche que les verbes
  mutants principaux ; laisse tranquilles les wrappers à double usage et les
  outils de copie, pour que les commandes d'ancrage ne se retrouvent jamais
  piégées.
- **Fail open, mais bruyant.** Un hook qui crashe ne doit jamais briquer la
  session — et ne doit jamais autoriser en silence. Affiche l'erreur là où
  l'humain peut la voir.
- **Ne jamais piéger une session.** Identité de session inconnue : autoriser,
  avec une ligne d'avertissement bien visible. Une session qui ne pourra jamais
  passer au VERT ne doit jamais être bloquée au ROUGE.
- **Un seul kill-switch, propriété de l'humain** (une variable d'env), ON par
  défaut, qui logge bruyamment quand il est off. La barrière lie les agents,
  jamais l'humain. N'ajoute jamais une deuxième barrière.

Hook générique (pseudocode, ~25 lignes) :

```python
HARNESS_SKILLS = {"optimus", "repair-loop", "invariant-floor"}  # le set de ton pack
MUTATING_TOOLS = {"Edit", "Write", "Delete"}
MUTATING_SHELL = r"^\s*(sudo\s+)?(git (commit|push|reset|checkout)|rm|pip install|" \
                 r"npm install|systemctl (restart|stop)|sed .*-i)"

def handle(event, session_id, tool, args):
    if kill_switch_off():                    # variable d'env possédée par l'humain, ex. HARNESS_GATE=off
        return ALLOW                         # désactivé bruyamment, jamais en silence
    if not session_id:
        warn("no session id — allowing; the gate never traps a session")
        return ALLOW
    if event == "SessionStart":
        set_state(session_id, "RED")         # chaque session se réarme à RED
        return ALLOW
    if event == "PostToolUse":
        if tool == "Skill" and args.get("skill") in HARNESS_SKILLS:
            set_state(session_id, "GREEN")   # harnais invoqué -> l'agent peut agir
        return ALLOW
    if event == "PreToolUse":
        mutating = tool in MUTATING_TOOLS or (
            tool == "Bash" and matches(MUTATING_SHELL, args.get("command", "")))
        if not mutating or get_state(session_id) == "GREEN":
            return ALLOW                     # la lecture seule passe toujours
        return BLOCK("RED: invoke a harness skill first, then act")
    return ALLOW
```

## Règles dures (ce qui fait échouer ce skill)

- Toute mutation avant que le harnais soit chargé.
- Un skill nommé dans un rapport qui n'a jamais été invoqué dans la session.
- Un hook qui bloque des outils en lecture seule, piège une session au ROUGE,
  ou échoue en silence.
- Une deuxième barrière, ou toute nouvelle friction posée sur l'humain. Le
  kill-switch reste le sien.

## Fonctionne bien avec

- [invariant-floor](../invariant-floor/SKILL.md) — le socle que le boot charge en premier.
- [human-calibration](../human-calibration/SKILL.md) — l'étape profil du boot.
- [repair-loop](../repair-loop/SKILL.md) — ce qu'un job de fix exécute après le boot.
- [bounded-loops](../bounded-loops/SKILL.md) — les budgets de chaque boucle que le boot démarre.
- [wayfinder](../wayfinder/SKILL.md) — quand le boot montre que tu ne connais pas la route.
