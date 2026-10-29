---
name: "fleet-ladder"
description: "Guide de sélection par rôle et capacité avant un envoi ; le pack public ne fournit ni résolveur ni exécutable Fleet. Trigger words: fleet, ladder, dispatch, fallback, model down, provider down, which model, availability, échelle de modèles, repli, modèle en panne, fournisseur à terre, quel modèle, disponibilité."
license: "MIT"
---

# Fleet Ladder — l'échelle de la flotte
**Effort:** light — une sonde en direct, mise en cache, du barreau avant tout dispatch. Élimine : les dispatches vers des providers morts, et les noms de modèles codés en dur aux points d'appel, qui cassent le jour où le modèle part à la retraite.

Ce skill décrit la sélection sans résoudre lui-même les modèles. Le pack public ne fournit ni résolveur ni exécutable Fleet ; signale toute fonction manquante comme une lacune du runtime. Ne code pas les identifiants de modèle en dur dans les skills, prompts ou appels.

## Quand la dérouler

- Avant TOUT envoi de travail à un modèle : build, notation, revue, ou job de worker
  borné.
- Quand un fournisseur est à terre et que tu dois savoir ce qui se replie sur quoi.
- À l'instant où tu te surprends à taper un nom de modèle dans du code ou un template
  de prompt.

## Les étapes

1. **Déclare le rôle et les capacités.** Lis l’échelle configurée et son ordre ; choisis un candidat adapté à la tâche, aux capacités et à la disponibilité. La configuration d’exemple est seulement un modèle. Ce skill ne classe ni ne filtre les candidats.
2. **Vérifie l’indépendance.** La revue utilise une nouvelle exécution séparée de l’auteur et un paquet figé sans contexte de l’auteur. Le même modèle capable ou la même famille est permis si le runtime configuré l’autorise. Signale toute restriction supplémentaire comme une lacune du runtime.
3. **Teste une inférence réelle.** Une liste de modèles ne prouve ni l’inférence, ni la capacité, ni le quota. Lance une inférence réelle et bornée sur le candidat ; mets le résultat en cache pour une durée raisonnable et respecte le backoff. Vérifie à nouveau la capacité lors d’un repli.
4. **Descends, à voix haute.** Envoie au meilleur barreau DISPONIBLE. Sur une panne de
   transport, signale l'échec fort, puis tente le barreau suivant. Ne saute jamais en
   silence — le registre doit montrer quels barreaux ont échoué et pourquoi.
5. **L'épuisement échoue fort.** Si tous les barreaux sont à terre, lève une erreur
   claire qui nomme ce qui a été tenté. Un job impossible à envoyer ne réussit jamais
   en silence, n'attend jamais pour toujours, et ne se dégrade jamais en réponse
   inventée.
6. **Journalise la provenance.** Ajoute chaque envoi à un journal : rôle, modèle
   choisi, barreaux sautés et pourquoi. Plus tard, tu dois pouvoir répondre à « qui a
   réellement fait ce travail ? »

## Règles dures — une seule cassée et le skill a échoué

- Ne code pas d’identifiant de modèle en dur dans les skills, prompts ou appels ; utilise le rôle et les capacités de la configuration active.
- Une inférence réelle et bornée est nécessaire ; un catalogue seul ne suffit pas.
- La revue exige une nouvelle exécution séparée de l’auteur et un paquet figé sans son contexte ; changer de modèle ou de famille n’est ni obligatoire ni une preuve de séparation.
- Journalise les échecs et replis ; signale les résolveurs ou mécanismes d’isolation manquants comme des lacunes du runtime.


## Marche bien avec

- [blind-tribunal](../blind-tribunal/SKILL.md)
- [bounded-loops](../bounded-loops/SKILL.md)
- [model-fusion](../model-fusion/SKILL.md)
