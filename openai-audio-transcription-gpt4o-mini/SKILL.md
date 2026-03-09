---
name: openai-audio-transcription-gpt4o-mini
description: Integrer une transcription audio OpenAI robuste dans des applications iOS, mobile, backend ou web avec les modeles gpt-4o-transcribe, gpt-4o-mini-transcribe et gpt-4o-transcribe-diarize, plus post-traitement GPT-5-mini. Utiliser ce skill quand il faut concevoir, implementer, auditer ou corriger un pipeline de transcription (upload, chunking, diarisation, langue, tache de fond, erreurs API, limites de taille, tests de fiabilite).
---

# OpenAI Audio Transcription GPT-4o Mini

## Objectif
Concevoir un pipeline de transcription audio fiable, maintenable et portable pour les futures applications de Laurent.

## Mode de sortie
- Produire les reponses en francais, concretes et orientees implementation.
- Prioriser des actions testables plutot que des recommandations vagues.

## Workflow obligatoire
1. Identifier le mode d usage: batch fichier, streaming, ou diarisation.
2. Choisir le modele et les parametres avec `references/openai-model-matrix.md`.
3. Concevoir le flux technique selon `references/swift-ios-integration-playbook.md`.
4. Appliquer les garde-fous issus des incidents reels dans `references/incidents-and-fixes.md`.
5. Verifier les payloads avant codage avec `scripts/validate_transcription_stack.py`.
6. Construire un plan de test avec `references/test-plan.md`.
7. Livrer une implementation + checks + plan de rollback.

## Decision tree rapide
- Si l utilisateur dit "GPT-4 mini transcription":
  - Interpretrer comme `gpt-4o-mini-transcribe` sauf demande explicite contraire.
- Si l utilisateur veut etiquettes locuteurs:
  - Utiliser `gpt-4o-transcribe-diarize` + `response_format=diarized_json`.
- Si l utilisateur veut robustesse temps long:
  - Imposer chunking local < 25 MB + reprise en tache de fond.
- Si l utilisateur veut post-traitement (titre, resume, classification):
  - Utiliser GPT-5-mini en etape separee, avec payload compatible.

## Etapes d integration a suivre
1. Definir contrat fonctionnel:
   - format entree, latence cible, besoin diarisation, langue cible, mode hors ecran.
2. Definir contrat technique:
   - endpoint, modele, format de reponse, politique retry, mapping erreurs.
3. Implementer upload robuste:
   - controler taille avant envoi, chunker localement, suivre progression, timeout long.
4. Implementer transcription:
   - parser reponses normales et diarisees, persister segments et texte final.
5. Implementer post-traitement optionnel:
   - appeler GPT-5-mini avec payload valide (`max_completion_tokens`, temperature compatible modele).
6. Implementer UX de resilience:
   - etats explicites, reprise apres interruption, erreurs actionnables.
7. Executer la matrice de tests:
   - taille, langue, interruptions, erreurs API, regression.

## Outils du skill
- `references/openai-model-matrix.md`:
  - choix de modele, endpoint, formats, contraintes.
- `references/swift-ios-integration-playbook.md`:
  - architecture iOS/Swift recommandee (recording, upload, fond, stockage).
- `references/incidents-and-fixes.md`:
  - problemes reels rencontres et corrections appliquees.
- `references/test-plan.md`:
  - checklist de validation avant release.
- `scripts/validate_transcription_stack.py`:
  - preflight des payloads pour detecter des erreurs frequentes.

## Commandes utiles
```bash
python3 scripts/validate_transcription_stack.py --mode audio --payload payload-audio.json --file-size-bytes 28000000 --duration-seconds 95
python3 scripts/validate_transcription_stack.py --mode chat --payload payload-chat.json
```

## Definition of done
- Le modele de transcription est choisi et justifie.
- Les limites de taille et de duree sont gerees.
- Les payloads OpenAI passent la prevalidation.
- Les erreurs historiques critiques sont neutralisees.
- La matrice de test est executee avant livraison.

## Sources officielles OpenAI a consulter
- https://platform.openai.com/docs/guides/speech-to-text
- https://platform.openai.com/docs/api-reference/audio/createTranscription
- https://platform.openai.com/docs/api-reference/chat/create
