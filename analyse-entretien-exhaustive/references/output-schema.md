# Contrat de sortie JSON + Markdown

## Arborescence attendue
```
analysis/<job-id>/
  manifest.json
  raw.txt
  segments.jsonl
  global_overview.json
  topic_candidates.json
  topic_map.json
  rhetorical_map.json
  qa_report.json
  topics/
    topic-001.json
    topic-001.md
  reports/
    02_analyse-rhetorique.md
    03_compte-rendu-exhaustif.md
```

## `segments.jsonl` (1 objet par ligne)
```json
{
  "segment_id": "s000001",
  "start_time": "00:06:48",
  "speaker": "Participant 3",
  "text": "...",
  "source_ref": "/absolute/path/raw.txt"
}
```
- `start_time` peut être `null`.

## `manifest.json`
```json
{
  "skill_version": "1.0.0",
  "source_file": "/path/transcript.pdf",
  "language": "fr",
  "segment_count": 1234,
  "topic_count": 12,
  "coverage_ratio": 0.986,
  "qa_status": "pass",
  "created_at": "2026-02-13T10:00:00Z"
}
```

## `global_overview.json`
```json
{
  "summary_scope": "global",
  "macro_themes": ["..."],
  "objectives_expressed": ["..."],
  "actors": ["..."],
  "constraints": ["..."],
  "temporal_markers": ["..."],
  "evidence_refs": ["s000014", "s000028"]
}
```

## `topic_candidates.json`
```json
{
  "candidates": [
    {
      "candidate_id": "c01",
      "label": "...",
      "definition": "...",
      "segment_refs": ["s000001", "s000002"],
      "confidence": 0.73
    }
  ]
}
```

## `topic_map.json`
```json
{
  "topics": [
    {
      "topic_id": "t01",
      "label": "...",
      "definition": "...",
      "parent_topic_id": null,
      "segment_refs": ["s000003", "s000099"]
    }
  ]
}
```

## `topics/topic-XXX.json`
```json
{
  "topic_id": "t01",
  "label": "...",
  "key_ideas": ["..."],
  "claims": ["..."],
  "decisions": ["..."],
  "open_questions": ["..."],
  "risks": ["..."],
  "contradictions": ["..."],
  "rhetorical_moves": ["..."],
  "evidence_refs": [
    "s000003",
    {"segment_id": "s000099", "quote": "...", "timestamp": "00:25:03"}
  ]
}
```

## `rhetorical_map.json`
```json
{
  "moves": [{"type": "problematization", "segment_id": "s000120"}],
  "speaker_profile": [{"speaker": "Participant 3", "style_markers": ["..."]}],
  "influence_patterns": [{"pattern": "reframing", "segment_refs": ["s000031"]}],
  "ambiguities": [{"topic": "...", "segment_refs": ["s000845"]}]
}
```

## `qa_report.json`
```json
{
  "status": "pass",
  "coverage_ratio": 0.986,
  "schema_checks": "pass",
  "traceability_checks": "pass",
  "warnings": []
}
```

## `topics/topic-XXX.md`
- Résumé du topic
- Faits et décisions
- Contradictions et risques
- Preuves (segment_id + timestamp)

## `reports/02_analyse-rhetorique.md`
- Cartographie des mouvements discursifs
- Analyse influence / cadrage / objections / concessions
- Ambiguïtés décisionnelles

## `reports/03_compte-rendu-exhaustif.md`
- Table des sujets
- Développement complet par sujet
- Liens explicites vers les preuves
- Questions ouvertes et prochaines investigations
