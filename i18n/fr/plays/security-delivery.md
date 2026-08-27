# Play : Security & Delivery

La porte de livraison pour tout ce qu'un client ou une autre machine va
exécuter. Sûr par construction : le harnais l'impose, on ne fait jamais
confiance au modèle pour s'en souvenir.

## Quand le lancer

- Un dépôt, un agent ou une app est sur le point d'être livré, publié ou
  déployé.
- Un agent avec des outils touche du contenu non fiable — pages web, issues,
  emails, saisies.
- Tu ajoutes des dépendances ou de la CI à quelque chose qui part en
  production.

## La chaîne

1. Porte des secrets — fais tourner un scanner de secrets en mode
   vérifié-seulement (il teste chaque credential candidat contre le fournisseur
   réel). Un seul credential confirmé actif fait échouer le build. Aucune
   exception.
2. Verrouillage du trafic sortant — refuse la sortie par défaut ; fais tout
   passer par un proxy qui n'autorise que des noms d'hôtes nus, en allowlist.
   Canonicalise et valide le nom d'hôte AVANT de le comparer : rejette les
   octets nuls, les astuces en pourcent et les CRLF. Le contournement à octet
   nul `evil-host\x00.trusted.com` est réel et a déjà été livré en production.
3. Casse le trio létal (la « lethal trifecta ») — architecture chaque chemin
   d'exécution pour qu'au moins UN de ces trois éléments manque toujours :
   accès à des données privées, exposition à du contenu non fiable,
   communication vers l'extérieur. Tu ne peux pas bloquer totalement l'injection
   de prompt ; tu peux la rendre incapable de voler.
4. Suivi de contamination — ingérer du contenu non fiable marque la session
   comme contaminée. Tant qu'elle l'est, chaque action capable d'exfiltrer
   (HTTP sortant, email, création de PR) passe par une politique dans le
   harnais — jamais par le jugement du modèle.
5. Chaîne d'approvisionnement — épingle chaque dépendance par hash et bloque
   les scripts d'installation. Épingle chaque action de CI sur un hash de
   commit complet, pas sur un tag.
6. [clean-code-gauntlet](../skills/clean-code-gauntlet/SKILL.md) — le code de
   sécurité porte la barre la plus stricte. Fais tourner les tests de mutation
   sur chaque détecteur, parseur et prédicat de politique, et pousse les
   mutants survivants à zéro. Une comparaison inversée dans un check de menace
   que la suite laisse passer EST la vulnérabilité.
7. [sniper-testing](../skills/sniper-testing/SKILL.md) — ne mocke QUE le réseau
   sortant, jamais la charge utile ni le parseur sous test : un détecteur mocké
   est un capteur aveugle en production.
8. Sandbox avant la livraison — exécute l'artefact construit dans une sandbox
   éphémère, tout trafic sortant bloqué, avec un arrêt d'urgence armé sur les
   ressources. Regarde ce qu'il écrit et ce qu'il essaie d'appeler.
9. Provenance — émets un inventaire logiciel (un SBOM), plus une provenance
   signée si tu l'as. Puis relis quand même le source : la provenance signe
   aussi fidèlement du source malveillant.

## Protections permanentes pendant tout run de build

- Écriture interdite sur les chemins sensibles : fichiers de démarrage du
  shell, config et hooks git, config DNS, clés SSH.
- Outils à moindre privilège. Une étape de confirmation est réservée UNIQUEMENT
  aux opérations vraiment destructrices ou irréversibles — perte de données,
  dépense, action externe irréversible. Ne mets jamais de barrière sur une
  capacité bénigne, et jamais sur ton humain.

## Barrières dures — une seule suffit à faire échouer le play

- Un credential confirmé actif, où que ce soit dans le livrable ou son
  historique.
- Un chemin d'exécution qui tient les trois jambes du trio létal à la fois.
- Une dépendance non épinglée, un script d'installation, ou une action de CI
  épinglée sur un tag.
- Un mutant survivant dans un détecteur, un parseur ou un prédicat de
  politique.
- L'artefact n'a jamais tourné en sandbox avant la livraison.

**Weight:** surtout de la discipline de construction free plus des passes de scanner et de sandbox light ; l'étape heavy est la mutation sur chaque détecteur et chaque prédicat de politique — elle se rentabilise sur tout ce qu'un client ou une autre machine va exécuter.
