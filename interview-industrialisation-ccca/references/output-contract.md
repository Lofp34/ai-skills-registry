# Output Contract

## Interview Triplet (01_interviews)

For each interview ID, maintain:
- `INT_... .txt`
- `INT_... .json`
- `INT_... .md`

### JSON minimum contract

- Top-level required fields follow `schemas/interview-schema-v1.json`.
- `questions[]` must include:
  - opening (`Q00`, `Q00B`)
  - tronc commun (`Q01`..`Q12`)
  - module profile codes (4 codes based on role)
  - closure (`QC1`, `QC2`, `QC3`)
- Each question object includes:
  - `code`, `question`, `answer`, `evidence[]`, `kpi_mentions[]`

## Aggregates (02_aggregates)

- `evidence-matrix.csv`
  - Keep columns: `id,source,timestamp_ou_page,fait_brut,implication_business,impact_sur_proposition`
  - IDs are globally sequential (`E01`, `E02`, ...).

- `decision-log.csv`
  - Keep columns: `decision,owner,rationale,date,impact,revisit_condition`

- `qa-report.json`
  - Keep one entry per interview in `interviews[]`.
  - Update `interviews_processed` and row counters in `aggregates`.

## Ambiguity Protocol

If metadata cannot be inferred with confidence:
- block final write,
- request explicit values,
- continue only after confirmation.
