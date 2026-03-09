# Incidents Reels et Correctifs

## Contexte
Ces incidents proviennent de l integration reelle de VoiceRecorderApp et doivent etre prevenus systematiquement dans les futurs projets.

## 1) Erreur `max_tokens` non supporte
- Symptome:
  - `Unsupported parameter: 'max_tokens' ... Use 'max_completion_tokens' instead.`
- Cause:
  - Payload Chat non adapte au modele cible.
- Correctif:
  - Remplacer `max_tokens` par `max_completion_tokens` pour GPT-5-mini et stack recente.

## 2) Erreur `temperature` non supportee
- Symptome:
  - `Unsupported value: 'temperature' ... Only the default (1) value is supported.`
- Cause:
  - Valeur custom envoyee a un modele qui impose la valeur par defaut.
- Correctif:
  - Ne pas envoyer `temperature` si non indispensable.
  - Si imposee par le modele, rester a la valeur supportee.

## 3) Limite fichier 25 MB
- Symptome:
  - transcription impossible au-dela d une certaine taille.
- Cause:
  - depassement de limite upload API.
- Correctif:
  - chunking local audio pour rester < 25 MB par requete.
  - marge recommandee: < 24 MB par chunk.

## 4) Transcription interrompue en quittant l app
- Symptome:
  - upload/transcription coupes en sortie d app.
- Cause:
  - session reseau non adaptee au fond.
- Correctif:
  - `URLSession` background + gestion explicite du background task.

## 5) Derive de langue (FR -> EN aleatoire)
- Symptome:
  - transcription partiellement en anglais malgre reglage FR.
- Cause probable:
  - detection automatique instable sur certains segments.
- Correctif:
  - forcer `language` dans la requete.
  - ajouter normalisation post-transcription si necessaire.

## 6) Titre auto non pertinent (`Sans titre` ou debut brut)
- Symptome:
  - cartes mal nommees.
- Cause:
  - prompt titre trop faible ou parsing fragile.
- Correctif:
  - post-traitement GPT-5-mini avec contraintes strictes (2-5 mots explicites).
  - rejeter les titres qui copient les premiers mots de la transcription.

## 7) Compatibilite API de reponse
- Symptome:
  - parsing invalide sur certains retours Chat.
- Cause:
  - `message.content` peut etre string ou tableau.
- Correctif:
  - parser defensif multi-format.

## Check anti-regression
- Avant merge:
  - executer `scripts/validate_transcription_stack.py`.
  - executer matrice de tests de `references/test-plan.md`.
