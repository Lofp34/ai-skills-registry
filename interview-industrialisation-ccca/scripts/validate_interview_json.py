#!/usr/bin/env python3
"""Validate interview JSON against required structure and basic patterns."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROLE_SET = {"CE", "CA", "SUPPORT", "PREVOT", "CRC", "PRODUCTION", "DIR"}
CONFIDENCE_SET = {"faible", "moyen", "eleve"}
TIMESTAMP_RE = re.compile(r"^([0-9]{2}:){2}[0-9]{2}$")
INTERVIEW_ID_RE = re.compile(r"^INT_[0-9]{8}_[A-Z0-9]+_(CE|CA|SUPPORT|PREVOT|CRC|PRODUCTION|DIR)_[A-Z0-9]+$")
DATE_RE = re.compile(r"^20[0-9]{2}-[0-9]{2}-[0-9]{2}$")

REQUIRED_TOP = [
    "interview_id",
    "date",
    "site",
    "role",
    "participant_nom",
    "interviewer",
    "duree_minutes",
    "questions",
    "module",
    "risques_statu_quo",
    "quick_wins_30j",
    "actions_j15_j30_j60_j90",
    "axes_contrat",
    "contradictions_detectees",
    "pieces_citees",
    "niveau_confiance",
]


def validate(path: Path) -> list[str]:
    data = json.loads(path.read_text(encoding="utf-8"))
    errors: list[str] = []

    for key in REQUIRED_TOP:
        if key not in data:
            errors.append(f"missing top-level field: {key}")

    if not INTERVIEW_ID_RE.match(str(data.get("interview_id", ""))):
        errors.append("invalid interview_id pattern")
    if not DATE_RE.match(str(data.get("date", ""))):
        errors.append("invalid date pattern")
    if data.get("role") not in ROLE_SET:
        errors.append("invalid role")
    if data.get("module") not in ROLE_SET:
        errors.append("invalid module")
    if data.get("niveau_confiance") not in CONFIDENCE_SET:
        errors.append("invalid niveau_confiance")

    if not isinstance(data.get("questions"), list) or len(data.get("questions", [])) < 1:
        errors.append("questions must be a non-empty array")
    else:
        for i, q in enumerate(data["questions"]):
            for key in ["code", "question", "answer", "evidence", "kpi_mentions"]:
                if key not in q:
                    errors.append(f"questions[{i}] missing {key}")
            evidence = q.get("evidence", [])
            if not isinstance(evidence, list):
                errors.append(f"questions[{i}].evidence must be array")
            else:
                for j, ev in enumerate(evidence):
                    if "timestamp" not in ev or "verbatim" not in ev:
                        errors.append(f"questions[{i}].evidence[{j}] missing fields")
                    ts = str(ev.get("timestamp", ""))
                    if ts and not TIMESTAMP_RE.match(ts):
                        errors.append(f"questions[{i}].evidence[{j}] invalid timestamp")

            kpis = q.get("kpi_mentions", [])
            if not isinstance(kpis, list):
                errors.append(f"questions[{i}].kpi_mentions must be array")
            else:
                for j, kpi in enumerate(kpis):
                    for key in ["name", "value", "period"]:
                        if key not in kpi:
                            errors.append(f"questions[{i}].kpi_mentions[{j}] missing {key}")

    actions = data.get("actions_j15_j30_j60_j90", [])
    if not isinstance(actions, list) or len(actions) < 4:
        errors.append("actions_j15_j30_j60_j90 must have at least 4 items")
    else:
        valid_horizons = {"J15", "J30", "J60", "J90"}
        for i, action in enumerate(actions):
            for key in ["horizon", "action", "owner"]:
                if key not in action:
                    errors.append(f"actions[{i}] missing {key}")
            if action.get("horizon") not in valid_horizons:
                errors.append(f"actions[{i}] invalid horizon")

    axes = data.get("axes_contrat", {})
    for key in [
        "sourcing_novateur",
        "accompagnement_orientation",
        "optimisation_parcours_client",
        "optimisation_reseau_anciens",
    ]:
        if key not in axes:
            errors.append(f"axes_contrat missing {key}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate interview JSON structure")
    parser.add_argument("--interview-json", required=True)
    args = parser.parse_args()

    path = Path(args.interview_json).expanduser().resolve()
    if not path.exists():
        raise FileNotFoundError(f"Interview JSON not found: {path}")

    errors = validate(path)
    if errors:
        print(json.dumps({"status": "invalid", "errors": errors}, ensure_ascii=True, indent=2))
        return 1

    print(json.dumps({"status": "valid", "file": str(path)}, ensure_ascii=True, indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:  # pragma: no cover
        print(json.dumps({"status": "error", "message": str(exc)}, ensure_ascii=True), file=sys.stderr)
        raise SystemExit(1)
