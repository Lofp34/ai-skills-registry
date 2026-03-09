---
name: interview-industrialisation-ccca
description: Industrialise interview transcriptions into the Compagnons Occitanie 2026 kit outputs with semi-automatic ambiguity checks. Use when a user provides a new interview PDF and wants consistent generation of 01_interviews .txt/.json/.md plus updates to 02_aggregates evidence-matrix.csv, decision-log.csv, and qa-report.json.
---

# Interview Industrialisation CCCA

Create repeatable interview outputs for `transcriptions/interviews-industrialisees-2026` with traceability and safeguards.

## Scope

- In: extract transcript, infer metadata, scaffold output triplet, validate JSON structure, update aggregates with idempotence.
- Out: automatic updates of `Livrables_CCABTP/*`, npm script refactor, workshop-level strategic deliverables.

## Required Inputs

- `pdf_path` (required)
- `kit_root` (default: `transcriptions/interviews-industrialisees-2026`)
- `language` (default: `fr`)

Optional but recommended in confirm mode:
- `participant_name`
- `site`
- `role`
- `date`
- `initials`

## Semi-Auto Workflow (Mandatory)

1. Preview metadata and ambiguity status.
2. Stop and confirm ambiguous fields (`site`, `role`, `participant_name`, `initials`, `date`) before writing files.
3. Scaffold output files only after confirmation.
4. Fill interview substance from transcript with evidence and KPI mentions.
5. Validate interview JSON.
6. Update aggregates idempotently.

## Commands

Run from any directory.

### 1) Extract transcript text

```bash
python /Users/laurents/Documents/00_WORKSPACE_LS/skills/interview-industrialisation-ccca/scripts/extract_pdf_transcript.py \
  --pdf-path "/path/to/interview.pdf"
```

### 2) Preview inferred metadata (no writes)

```bash
python /Users/laurents/Documents/00_WORKSPACE_LS/skills/interview-industrialisation-ccca/scripts/scaffold_interview_outputs.py \
  --pdf-path "/path/to/interview.pdf" \
  --kit-root "/path/to/transcriptions/interviews-industrialisees-2026"
```

### 3) Confirm and scaffold output files

```bash
python /Users/laurents/Documents/00_WORKSPACE_LS/skills/interview-industrialisation-ccca/scripts/scaffold_interview_outputs.py \
  --pdf-path "/path/to/interview.pdf" \
  --kit-root "/path/to/transcriptions/interviews-industrialisees-2026" \
  --participant-name "Juliette Grard" \
  --site NIMES \
  --role PREVOT \
  --date 2026-02-23 \
  --initials JG \
  --confirm
```

### 4) Validate interview JSON structure

```bash
python /Users/laurents/Documents/00_WORKSPACE_LS/skills/interview-industrialisation-ccca/scripts/validate_interview_json.py \
  --interview-json "/path/to/INT_YYYYMMDD_SITE_ROLE_XX.json"
```

### 5) Update aggregates

Prepare payload files first:
- `evidence.json` (list of rows without `id`)
- `decisions.json` (list of decision rows)

Then:

```bash
python /Users/laurents/Documents/00_WORKSPACE_LS/skills/interview-industrialisation-ccca/scripts/update_aggregates.py \
  --kit-root "/path/to/transcriptions/interviews-industrialisees-2026" \
  --interview-json "/path/to/INT_YYYYMMDD_SITE_ROLE_XX.json" \
  --source-pdf "01_interviews/InterviewSource.pdf" \
  --evidence-json "/tmp/evidence.json" \
  --decisions-json "/tmp/decisions.json" \
  --quality-flag "site_metadata_confirmed"
```

## Quality Rules

- Anchor each major statement to transcript evidence (`timestamp`, `verbatim`).
- Keep non-explicit claims labeled as inferences via QA flags.
- Keep CSV column counts stable.
- Preserve interview ID convention: `INT_<YYYYMMDD>_<SITE>_<ROLE>_<INITIALes>`.
- Enforce idempotence: no duplicate evidence/decision rows for same normalized key.

## References

- `references/output-contract.md`
- `references/mapping-trame-codes.md`
- `references/aggregate-payloads.md`
