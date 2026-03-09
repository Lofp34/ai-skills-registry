---
name: enterprise-client-folder-bootstrap
description: Standardize enterprise client mission folders and keep them context-ready for Codex. Use when creating a new client folder, normalizing an existing folder, centralizing Gmail emails from contacts.csv, and maintaining documentation/project-status.md plus documentation/sources-index.md with a repeatable workflow. Also trigger when the user says mets a jour ce dossier avec $enterprise-client-folder-bootstrap.
---

# Enterprise Client Folder Bootstrap

Initialize and operate a repeatable enterprise folder standard for client missions (commercial teams, sales directors, executives). Keep it practical: one mission folder, one `contacts.csv`, one `documentation/client-config.yaml`.

## Commande Rapide

When the user writes `mets a jour ce dossier avec $enterprise-client-folder-bootstrap` (or a close variant), execute directly the full "existing folder update" workflow from `assets/prompt-update-existing-client-folder.md` without asking for a separate prompt template.

## Scope

- In: enterprise missions, folder bootstrap, Gmail email centralization, context maintenance.
- Out: HubSpot sync, incubator-specific multi-portfolio logic, complex CRM pipelines.

## Folder Standard V1

Create or maintain this structure in the mission root:

- `documentation/client-config.yaml`
- `documentation/project-status.md`
- `documentation/sources-index.md`
- `contacts.csv`
- `emails/`
- `transcriptions/`
- `notes/`
- `deliverables/`
- `sources/`
- `secrets/`

## Mandatory Config Fields

In `documentation/client-config.yaml`, keep these fields populated:

- `client.name`
- `mission.name`
- `mission.timezone`
- `data.contacts_csv`
- `email_ingestion.enabled`
- `email_ingestion.months_back` (default: `6`)

Optional tuning fields:

- `auth.gmail_client_secret`
- `auth.gmail_token_file`
- `email_ingestion.max_messages`
- `email_ingestion.include_public_domains`
- `email_ingestion.gmail_query_mode`
- `email_ingestion.name_query_mode`
- `email_ingestion.name_match_mode`
- `email_ingestion.name_min_tokens`
- `email_ingestion.max_domain_projects`

## Workflow

1) Bootstrap the folder
- Run `scripts/bootstrap_client.py` on the mission folder.
- This creates the standard directories and templates without overwriting existing files unless `--force` is used.

2) Configure mission metadata
- Edit `documentation/client-config.yaml`.
- Keep values concrete and operational (client name, mission label, timezone, confidentiality).

3) Populate contacts source of truth
- Fill `contacts.csv` with one row per contact.
- Minimum practical columns: `project_id,nom_projet,porteur_nom,email`.
- Add role/org notes when useful.

4) Refresh context package
- Run `scripts/refresh_context.py`.
- It orchestrates Gmail ingestion (via `scripts/centralize_project_emails.py`) and updates logs in:
  - `documentation/sources-index.md`
  - `documentation/project-status.md`
- It also stamps tracker metadata with `scripts/update_tracker_metadata.py`.
- Email outputs are written by project and by interlocutor:
  - `emails/<project>/messages/<interlocuteur>/*.md|*.json` (message-level, grouped by interlocutor)
  - `emails/<project>/messages/<interlocuteur>/index.md|index.json` (interlocutor-level navigation)
  - `emails/<project>/messages/index.md|index.json` (all interlocutors for the project)

5) Repeat cadence
- Run context refresh weekly, or after major meetings/transcriptions.
- Keep transcriptions and source register in sync with decisions and risks.

## Commands

Bootstrap:

```bash
python ~/.codex/skills/enterprise-client-folder-bootstrap/scripts/bootstrap_client.py \
  --target-dir "/path/to/client-folder"
```

Refresh context (default 6 months from config):

```bash
python ~/.codex/skills/enterprise-client-folder-bootstrap/scripts/refresh_context.py \
  --project-dir "/path/to/client-folder" \
  --python-bin /tmp/codex-pdf-venv/bin/python
```

Refresh with explicit start date and broader search:

```bash
python ~/.codex/skills/enterprise-client-folder-bootstrap/scripts/refresh_context.py \
  --project-dir "/path/to/client-folder" \
  --start-date 2025-09-01 \
  --include-public-domains \
  --progress-mode bar
```

## Gmail Prerequisites

- OAuth desktop client JSON at: `secrets/gmail_client_secret.json`
- Token cache generated at first run: `secrets/gmail_read_token.json`
- Required Python packages for Gmail scripts:
  - `google-api-python-client`
  - `google-auth-oauthlib`
  - `google-auth-httplib2`

## Resources

- `assets/client-config.template.yaml`: baseline mission config.
- `assets/prompt-update-existing-client-folder.md`: prompt template to update an already-started client folder from IDE root.
- `references/project-status-template.md`: project tracker template.
- `references/sources-index-template.md`: source registry template.
- `scripts/bootstrap_client.py`: folder + template initializer.
- `scripts/refresh_context.py`: operational orchestrator.
- `scripts/centralize_project_emails.py`: Gmail ingestion and project classification.
- `scripts/update_tracker_metadata.py`: tracker metadata decide/stamp utility.
