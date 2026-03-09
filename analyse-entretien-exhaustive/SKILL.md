---
name: analyse-entretien-exhaustive
description: Analyse exhaustive de transcriptions d’entretiens business B2B longs avec pipeline multi-passes sémantique et rhétorique. Utiliser quand l’utilisateur veut cartographier tous les sujets/sous-sujets, extraire preuves horodatées, détecter contradictions implicites, produire des sorties JSON+Markdown actionnables, et vérifier la complétude via métriques QA.
---

# Analyse Entretien Exhaustive

## Objectif
Produire une analyse exhaustive, traçable et réutilisable d’une transcription (`.pdf`, `.txt`, `.md`) sans réduire le travail à un résumé.

## Entrées attendues
- Un fichier de transcription source.
- Une langue cible (par défaut `fr`).
- Un dossier de sortie.

## Sortie standard
Produire un dossier d’analyse contenant:
- `manifest.json`
- `segments.jsonl`
- `global_overview.json`
- `topic_candidates.json`
- `topic_map.json`
- `topics/topic-XXX.json`
- `topics/topic-XXX.md`
- `rhetorical_map.json`
- `reports/02_analyse-rhetorique.md`
- `reports/03_compte-rendu-exhaustif.md`
- `qa_report.json`

Le schéma détaillé est dans `references/output-schema.md`.

## Workflow opératoire
1. Extraire le texte brut.
2. Normaliser la transcription en segments atomiques.
3. Exécuter les passes d’analyse 1 à 7 (global -> sujets -> consolidation -> approfondissement -> rhétorique -> synthèse -> QA).
4. Vérifier la qualité avec `scripts/validate_outputs.py`.

### 1) Extraction (Pass 0)
```bash
python3 scripts/extract_transcript.py \
  --input /chemin/transcript.pdf \
  --output /chemin/analyse/raw.txt \
  --language fr \
  --format auto
```

### 2) Segmentation
```bash
python3 scripts/segment_normalize.py \
  --input /chemin/analyse/raw.txt \
  --output /chemin/analyse/segments.jsonl
```

## Passes analytiques (LLM)
Utiliser les gabarits stricts de `references/pass-prompts.md`.

- Pass 1: produire `global_overview.json`
- Pass 2: produire `topic_candidates.json`
- Pass 3: produire `topic_map.json`
- Pass 4A/B/C: produire `topics/topic-XXX.json` + `topics/topic-XXX.md`
- Pass 5: produire `rhetorical_map.json` + `reports/02_analyse-rhetorique.md`
- Pass 6: produire `reports/03_compte-rendu-exhaustif.md`
- Pass 7: produire `qa_report.json`

Taxonomie rhétorique: `references/rhetorical-taxonomy.md`.
Rubrique qualité: `references/quality-rubric.md`.

## Validation QA
```bash
python3 scripts/validate_outputs.py \
  --analysis-dir /chemin/analyse \
  --min-coverage 0.98 \
  --strict
```

## Règles de fiabilité
- Sourcer toute affirmation importante avec des références de segments (`segment_id`, timestamp si disponible).
- Ne pas inventer d’acteurs, décisions ou chiffres absents de la transcription.
- Conserver les noms et informations complètes (pas de pseudonymisation par défaut).
- Signaler explicitement les ambiguïtés et contradictions.
- Prioriser la complétude de couverture sur l’élégance stylistique.

## Lecture progressive recommandée
- Toujours lire `references/output-schema.md` avant de générer les fichiers JSON.
- Lire `references/pass-prompts.md` pour les formats de sortie attendus par pass.
- Lire `references/workflow.md` pour l’enchaînement complet et les checkpoints.
- Lire `references/rhetorical-taxonomy.md` si analyse rhétorique demandée.
- Lire `references/quality-rubric.md` avant la validation finale.
