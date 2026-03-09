# Playbook iOS Swift - Integration Transcription Audio

## Architecture recommandee
1. `AudioRecorderManager`
- Gerer enregistrement local (format stable type m4a).
- Exposer timer, etat recording, start/stop.

2. `WhisperTranscriber` (ou service equivalent)
- Geler la logique API transcription.
- Gerer chunking local, requetes multipart, parsing diarise/non diarise.
- Exposer progression, messages de statut et erreurs.

3. `RecordingsStore`
- Persister metadonnees et etat: `isTranscribing`, `transcription`, `title`.
- Sauvegarder incrementalement pour resilience.

4. `AIActionManager` (optionnel post-traitement)
- Isoler les appels texte GPT-5-mini (resume, titre, Q/R).
- Ne pas melanger transcription et post-traitement dans la meme requete.

## Pipeline robuste
1. Arreter enregistrement et persister fichier local.
2. Evaluer taille fichier.
3. Si > 24 MB, decouper en chunks.
4. Envoyer chaque chunk vers `/v1/audio/transcriptions`.
5. Fusionner texte + segments avec offset temporel.
6. Persister resultat final.
7. Lancer post-traitement (titre, resume) sur transcription finale.

## Tache de fond iOS
- Utiliser `URLSessionConfiguration.background(...)` pour upload long.
- Completer avec `UIApplication.beginBackgroundTask` pour couvrir la transition.
- Nettoyer les ressources temporaires apres completion.

## UX minimale obligatoire
- Etats explicites: `preparation`, `upload`, `traitement`, `succes`, `erreur`.
- Barre de progression visible pour upload et processing.
- Message d erreur actionnable (pas seulement "Erreur API").
- Boutons d action IA desactives tant que transcription absente.

## Parser defensif
- Accepter:
  - `message.content` string
  - `message.content` tableau d objets texte
- En diarisation:
  - mapper `speaker`, `start`, `end`, `text`.
  - conserver l ordre et les offsets.

## Notes legales produit
- iOS ne fournit pas l audio natif de l appel telephonique aux apps tierces.
- Toujours verifier les obligations legales locales sur l enregistrement de conversations.
