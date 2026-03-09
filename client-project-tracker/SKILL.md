---
name: client-project-tracker
description: Maintain a single `documentation/project-status.md` for client engagements by scanning project documents, extracting concise document summaries, tracking completed and pending tasks, and planning next steps with three specialist lenses (McKinsey consultant, Bain consultant, Salesforce RevOps architect). Use when starting a client folder, asking where a project stands, requesting a daily status refresh, or updating progress after new files, notes, transcripts, or proposals are added.
---

# Client Project Tracker

## Overview
Maintain one source of truth for delivery progress in `documentation/project-status.md`. Keep the report action-oriented, evidence-based, and updated once per day when the client folder changed (or anytime on explicit user request).

## Core Workflow

### 1) Confirm update trigger
- Run `scripts/update_tracker_metadata.py decide --project-dir <client-folder> --status-file documentation/project-status.md`.
- Use `--force` only when the user explicitly asks for a manual refresh.
- If `should_update=false`, return a short status note and stop.

### 2) Build evidence from project files
- Scan relevant files in the client folder (`.md`, `.txt`, `.pdf`, `.docx`, `.csv`, `.xlsx`, and notes).
- Extract only factual signals: objectives, milestones, commitments, deliverables, dates, owners, decisions, blockers.
- Add short summaries per document (max 3 bullets each) with impact and next action.
- If data is missing or conflicting, add it under `Hypotheses` and `Open questions`.

### 3) Apply the 3 specialist lenses
- Load `references/specialists.md`.
- Produce three compact analysis blocks:
  - McKinsey consultant: MECE structure, gap-to-target, risk map.
  - Bain consultant: 80/20 priority sequencing, execution focus.
  - Salesforce RevOps architect: pipeline and KPI instrumentation, data quality.
- Keep roles exclusive. Do not duplicate the same conclusion across all three blocks.

### 4) Create or update the master report
- If missing, create `documentation/project-status.md` from `references/project-status-template.md`.
- Preserve history; append to `Daily Update Log` instead of rewriting old entries.
- Keep language direct and scannable. Prefer short bullets and tables.
- Track: done, in-progress, not-started, next 7/30 days, risks, decisions, dependencies.

### 5) Stamp tracker metadata
- After writing the report, run:
  - `scripts/update_tracker_metadata.py stamp --project-dir <client-folder> --status-file documentation/project-status.md --mode auto`
- For user-forced refreshes, use `--mode manual`.
- Metadata controls the once-per-day auto-update rule.

## Report Quality Bar
- Use facts first. Do not invent dates, owners, or outcomes.
- Flag uncertainty explicitly under `Hypotheses`.
- Keep each section concise (1-6 bullets).
- Keep document summaries short and action-linked.
- Use timezone `Europe/Paris` for timestamps.

## Required Output Contract
Always keep these sections in `documentation/project-status.md`:
- Context Snapshot
- Target State and Success Criteria
- Milestones and Phase Status
- Progress Snapshot (Done / In Progress / Not Started)
- Document Summaries (short)
- Specialist Analysis (McKinsey / Bain / RevOps)
- KPI and Pipeline Signals
- Risks, Decisions, and Dependencies
- Next 7 Days and Next 30 Days
- Daily Update Log
- Open Questions
- Hypotheses

## References
- `references/specialists.md`: role definitions and analysis checklist for the 3 specialists.
- `references/project-status-template.md`: canonical structure for `documentation/project-status.md`.
- `references/example-compagnons-occitanie.md`: worked example based on the Compagnons project (example only; keep the skill generic).

## Example user requests
- "Use $client-project-tracker to tell me exactly where this client project stands."
- "Refresh project status for this folder and plan next 30 days."
- "Update documentation/project-status.md after these new notes."
- "Force a manual status update now with risks and priorities."
