# Workflow multi-passes (version opérationnelle)

## 0. Préparation
- Créer un dossier de travail: `/.../analysis/<job-id>/`.
- Déposer le transcript source.
- Exécuter l’extraction puis la segmentation.

## 1. Pass 0: Ingestion
- Entrées: fichier source.
- Sortie: `raw.txt`.
- Outil: `scripts/extract_transcript.py`.

## 2. Pass 0bis: Segmentation
- Entrée: `raw.txt`.
- Sortie: `segments.jsonl`.
- Outil: `scripts/segment_normalize.py`.
- Contrôle: vérifier `segment_id`, `speaker`, `text` non vides.

## 3. Pass 1: Vue globale
- Entrée: `segments.jsonl`.
- Sortie: `global_overview.json`.
- But: macro-thèmes, objectifs, contraintes, acteurs, temporalités.

## 4. Pass 2: Découverte des sujets
- Entrée: `segments.jsonl`, `global_overview.json`.
- Sortie: `topic_candidates.json`.
- But: sujets/sous-sujets candidats avec premières preuves.

## 5. Pass 3: Consolidation des sujets
- Entrée: `topic_candidates.json`, `segments.jsonl`.
- Sortie: `topic_map.json`.
- But: taxonomie stable, fusion/séparation des sujets, couverture de segments.

## 6. Pass 4: Approfondissement par sujet
Répéter pour chaque topic:
- Pass 4A: extraction initiale (`key_ideas`, `claims`, `decisions`).
- Pass 4B: récupération des segments manquants.
- Pass 4C: audit contradictions/incomplétudes.

Sorties:
- `topics/topic-XXX.json`
- `topics/topic-XXX.md`

## 7. Pass 5: Analyse rhétorique transverse
- Entrées: l’ensemble des segments + topics consolidés.
- Sorties:
  - `rhetorical_map.json`
  - `reports/02_analyse-rhetorique.md`
- But: mouvements discursifs, influence, ambiguïtés, zones de friction.

## 8. Pass 6: Synthèse exhaustive finale
- Sortie: `reports/03_compte-rendu-exhaustif.md`.
- But: compte-rendu structuré par sujet avec preuves reliées.

## 9. Pass 7: QA final
- Sortie: `qa_report.json`.
- Outil: `scripts/validate_outputs.py`.
- Contrôles minimaux:
  - couverture >= 0.98
  - cohérence des schémas
  - traçabilité assertions -> preuves

## 10. Manifest
Écrire `manifest.json` avec:
- `skill_version`
- `source_file`
- `language`
- `segment_count`
- `topic_count`
- `coverage_ratio`
- `qa_status`
- `created_at`
