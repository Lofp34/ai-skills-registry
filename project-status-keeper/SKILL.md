---
name: project-status-keeper
description: Ensure a project master status document exists and stays coherent with the original objectives. Use when starting a project, opening a PR, or making substantial changes so Codex checks `documentation/project-status.md`, creates it if missing, and updates it after each PR to track scope, decisions, progress, risks, and next steps.
---

# Project Status Keeper

## Overview

Maintain a single master document that keeps the project aligned with its original objectives and scope. Ensure the document exists, stays coherent, and is updated at every PR so the project remains on track.

## Workflow

### 1) Locate or create the master document
- Look for `documentation/project-status.md`.
- If missing, create it using the template below.
- Add a link to it in `README.md` if not already present.

### 2) Validate coherence with objectives
- Compare the current work/PR against the "Objectif" and "Perimetre".
- If scope drift is detected, flag it explicitly and propose adjustments.
- Keep the doc concise; avoid verbose narratives.

### 3) Update after each PR
- Update "Ce qui est en place" to reflect shipped features.
- Update "Decisions prises" if a new decision was made.
- Update "Risques / Blocages" if any risk appeared or was resolved.
- Update "Prochaine etape (proposee)" with the next 3-5 items.
- Add a one-line entry to "Journal des evolutions".

### 4) Quality bar
- Keep each section short and scannable (1-5 bullets).
- Use ASCII text by default.
- Do not add extra docs; this is the single source of truth.

## Master document template

Use this template when creating `documentation/project-status.md`:

```
# Project Status (MVP)

## Objectif
<1-2 lignes>

## Perimetre (scope)
- In:
- Out:

## Ce qui est en place
- ...

## Decisions prises
- ...

## Risques / Blocages
- ...

## Prochaine etape (proposee)
1) ...
2) ...
3) ...

## Journal des evolutions
- YYYY-MM-DD: <ligne courte>
```
