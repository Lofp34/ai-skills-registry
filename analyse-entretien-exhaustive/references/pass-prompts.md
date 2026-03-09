# Prompts stricts par pass

## Règles globales
- Ne jamais inventer.
- Utiliser uniquement `segments.jsonl` comme source de vérité.
- Produire exactement le format demandé.
- Ajouter des `segment_refs` pour toute affirmation non triviale.

## Pass 1 — Vue globale
Instruction:
1. Lire l’ensemble de `segments.jsonl`.
2. Extraire macro-thèmes, objectifs, acteurs, contraintes et temporalités.
3. Produire `global_overview.json` conforme au schéma.

Format attendu: JSON objet unique.

## Pass 2 — Découverte des sujets
Instruction:
1. Générer une liste de sujets candidats couvrant tout le transcript.
2. Assigner à chaque candidat des `segment_refs`.
3. Ajouter un `confidence` entre 0 et 1.

Format attendu: `topic_candidates.json`.

## Pass 3 — Consolidation
Instruction:
1. Fusionner les doublons.
2. Séparer les sujets ambigus.
3. Produire une taxonomie stable avec `topic_id`.

Format attendu: `topic_map.json`.

## Pass 4A — Approfondissement initial
Instruction:
1. Pour chaque `topic_id`, extraire idées, claims, décisions, risques.
2. Produire `topics/topic-XXX.json` partiel.

## Pass 4B — Complétude
Instruction:
1. Rebalayer `segments.jsonl`.
2. Identifier les segments pertinents manquants par topic.
3. Mettre à jour `evidence_refs` et `segment_refs`.

## Pass 4C — Contradictions
Instruction:
1. Vérifier cohérence interne de chaque topic.
2. Ajouter `contradictions` et `open_questions` sourcées.
3. Finaliser `topics/topic-XXX.json` + `topics/topic-XXX.md`.

## Pass 5 — Rhétorique transverse
Instruction:
1. Tagger les mouvements discursifs avec taxonomie de `rhetorical-taxonomy.md`.
2. Générer `rhetorical_map.json`.
3. Rédiger `reports/02_analyse-rhetorique.md`.

## Pass 6 — Synthèse exhaustive
Instruction:
1. Rédiger `reports/03_compte-rendu-exhaustif.md`.
2. Structurer par sujets consolidés.
3. Inclure preuves et contradictions.

## Pass 7 — QA final
Instruction:
1. Contrôler couverture, traçabilité, schéma.
2. Produire `qa_report.json`.
3. Exécuter `scripts/validate_outputs.py`.
