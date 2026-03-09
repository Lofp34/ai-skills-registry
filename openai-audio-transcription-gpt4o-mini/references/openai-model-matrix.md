# OpenAI Model Matrix - Transcription Audio

## Objectif
Choisir rapidement le bon modele et le bon endpoint selon le besoin.

## Modeles cibles

### `gpt-4o-mini-transcribe`
- Usage: transcription standard, cout optimise, latence reduite.
- Endpoint: `/v1/audio/transcriptions`
- Formats de sortie usuels: `json`, `text` (verifier la version API active).
- Cas ideal: notes vocales, comptes rendus simples, apps a volume eleve.

### `gpt-4o-transcribe`
- Usage: transcription plus exigeante en precision.
- Endpoint: `/v1/audio/transcriptions`
- Formats de sortie usuels: `json`, `text` (selon version API).
- Cas ideal: contenu metier sensible, vocabulaire plus technique.

### `gpt-4o-transcribe-diarize`
- Usage: transcription multi-locuteurs avec etiquettes.
- Endpoint: `/v1/audio/transcriptions` uniquement.
- Format requis pour segments locuteurs: `diarized_json`.
- Contraintes importantes:
  - exiger `chunking_strategy` pour audio > 30 s.
  - ne pas utiliser `prompt`, `logprobs`, `timestamp_granularities[]`.

## Limite taille fichier
- Limite de televersement API: 25 MB.
- Bonne pratique: viser < 24 MB par chunk pour marge de securite.

## Langue
- Toujours passer le code ISO-639-1 (`fr`, `en`, etc.) pour stabiliser precision et latence.

## Post-traitement texte (hors transcription)
- Pour titres, resumes, CRM, Q/R: utiliser un appel separe sur `gpt-5-mini`.
- Guardrails payload observes:
  - preferer `max_completion_tokens` (pas `max_tokens`).
  - eviter temperature custom si le modele ne l accepte pas (cas observe sur `gpt-5-mini`).

## Sources
- https://platform.openai.com/docs/guides/speech-to-text
- https://platform.openai.com/docs/api-reference/audio/createTranscription
- https://platform.openai.com/docs/api-reference/chat/create
