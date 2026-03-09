# Aggregate Payload Formats

## evidence.json

JSON list. Each item:

```json
{
  "timestamp_ou_page": "00:12:34-00:13:20",
  "fait_brut": "Observed fact",
  "implication_business": "Business implication",
  "impact_sur_proposition": "Impact on proposal",
  "source": "01_interviews/MyInterview.pdf"
}
```

Notes:
- `source` is optional; defaults to `--source-pdf` if omitted.
- Do not provide `id`; IDs are recalculated globally.

## decisions.json

JSON list. Each item:

```json
{
  "decision": "Decision statement",
  "owner": "Laurent Serre",
  "rationale": "Why this choice",
  "date": "2026-02-23",
  "impact": "Expected impact",
  "revisit_condition": "When to revisit"
}
```

## Quality Flags

Pass one or more `--quality-flag` values to annotate QA status, for example:
- `site_metadata_confirmed`
- `participant_identity_confirmed`
- `inference_used_for_kpi`
- `consentement_non_explicite`
