Utilise le skill $enterprise-client-folder-bootstrap pour normaliser ce dossier client.

Alias conversationnel reconnu:
- "Mets a jour ce dossier avec $enterprise-client-folder-bootstrap"

Objectif:
- Mettre le dossier au standard V1 sans casser l'existant.
- Preparer un contexte exploitable pour Codex (docs, sources, emails, transcriptions).

Actions attendues:
1) Auditer rapidement l'existant et lister ce qui est deja present.
2) Lancer le bootstrap sur le dossier courant (`.`) en mode non destructif (pas de `--force`).
3) Completer `documentation/client-config.yaml` avec les infos du client.
4) Creer/completer `contacts.csv` a partir des elements deja dans le dossier.
5) Mettre a jour `documentation/sources-index.md` et `documentation/project-status.md` avec les sources et l'etat reel.
6) Si OAuth Gmail est pret: activer `email_ingestion.enabled: true` et lancer `refresh_context.py`.
   Sinon: laisser `email_ingestion.enabled: false` et preparer le dossier pour l'activation ulterieure.
7) Verifier que la structure email est bien par interlocuteur dans `emails/<projet>/messages/<interlocuteur>/...` (pas de dossier `senders`).
8) Rendre un resume final: fichiers crees/modifies, commandes executees, points bloquants eventuels.
