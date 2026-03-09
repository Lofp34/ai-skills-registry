# Test Plan - Transcription Audio OpenAI

## Objectif
Valider robustesse fonctionnelle, technique et UX avant release.

## A. Cas fonctionnels
1. Transcription courte FR (< 2 min, 1 locuteur).
2. Transcription longue (> 45 min) avec chunking.
3. D i a r i s a t i o n multi-locuteurs avec `diarized_json`.
4. Post-traitement titre resume Q/R sur texte transcrit.

## B. Cas limites
1. Fichier proche 25 MB (24.5 MB).
2. Fichier > 25 MB (doit passer par chunking).
3. Reseau lent ou intermittent.
4. Sortie d app pendant upload/transcription.
5. Reprise app apres interruption.

## C. Validation API
1. Verifier absence de `max_tokens` sur payload GPT-5-mini.
2. Verifier absence de `temperature` non supportee.
3. Verifier `language` renseignee.
4. Verifier `chunking_strategy` sur `gpt-4o-transcribe-diarize` si > 30 s.

## D. Validation donnees
1. Segments diarises correctement ordonnes.
2. Offsets temporels preserves apres fusion de chunks.
3. Texte final coherent sans perte notable.
4. Titre de carte explicite (2 a 5 mots, non derive des premiers mots bruts).

## E. Validation UX
1. Progression visible a chaque etape.
2. Messages d erreur clairs et actionnables.
3. Boutons d action disables tant que prerequis manquants.

## F. Criteres de sortie
- 0 erreur bloquante.
- 0 regression sur transcriptions existantes.
- Temps de traitement acceptable pour taille cible.
- Taux de succes stable sur 10 runs consecutifs.
