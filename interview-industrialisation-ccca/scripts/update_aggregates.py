#!/usr/bin/env python3
"""Update evidence matrix, decision log, and qa report for one interview.

Idempotence strategy:
- Evidence rows deduplicated by source/timestamp/fait_brut/implication/impact.
- Decision rows deduplicated by decision/owner/rationale/date/impact/revisit_condition.
- QA interview entry replaced if interview_id already exists.
"""

from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path

EVIDENCE_HEADERS = [
    "id",
    "source",
    "timestamp_ou_page",
    "fait_brut",
    "implication_business",
    "impact_sur_proposition",
]

DECISION_HEADERS = [
    "decision",
    "owner",
    "rationale",
    "date",
    "impact",
    "revisit_condition",
]

CORE_CODES = ["Q00"] + [f"Q{i:02d}" for i in range(1, 13)]
MODULE_CODES = {
    "CE": [f"CE0{i}" for i in range(1, 5)],
    "CA": [f"CA0{i}" for i in range(1, 5)],
    "SUPPORT": [f"SU0{i}" for i in range(1, 5)],
    "PREVOT": [f"PR0{i}" for i in range(1, 5)],
    "CRC": [f"CR0{i}" for i in range(1, 5)],
    "PRODUCTION": [f"PD0{i}" for i in range(1, 5)],
    "DIR": [f"DI0{i}" for i in range(1, 5)],
}
CLOSURE_CODES = ["QC1", "QC2", "QC3"]


def read_csv_rows(path: Path, headers: list[str]) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        rows = []
        for row in reader:
            clean = {h: (row.get(h, "") or "") for h in headers}
            rows.append(clean)
        return rows


def write_csv_rows(path: Path, headers: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        for row in rows:
            writer.writerow({h: row.get(h, "") for h in headers})


def renumber_evidence(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    width = max(2, len(str(max(1, len(rows)))))
    for idx, row in enumerate(rows, start=1):
        row["id"] = f"E{idx:0{width}d}"
    return rows


def get_answered_codes(questions: list[dict]) -> set[str]:
    answered = set()
    for q in questions:
        code = str(q.get("code", "")).strip()
        answer = str(q.get("answer", "")).strip()
        if code and answer:
            answered.add(code)
    return answered


def build_qa_entry(interview_json: dict, source_pdf: str, quality_flags: list[str], status: str) -> dict:
    role = interview_json["role"]
    questions = interview_json.get("questions", [])
    answered_codes = get_answered_codes(questions)

    core_completed = sum(1 for code in CORE_CODES if code in answered_codes)
    module_expected_codes = MODULE_CODES.get(role, [])
    module_completed = sum(1 for code in module_expected_codes if code in answered_codes)
    closure_completed = sum(1 for code in CLOSURE_CODES if code in answered_codes)

    evidence_points = sum(len(q.get("evidence", [])) for q in questions if isinstance(q.get("evidence", []), list))
    kpi_mentions = sum(len(q.get("kpi_mentions", [])) for q in questions if isinstance(q.get("kpi_mentions", []), list))

    interview_id = interview_json["interview_id"]
    return {
        "interview_id": interview_id,
        "source_pdf": source_pdf,
        "outputs": {
            "txt": f"01_interviews/{interview_id}.txt",
            "json": f"01_interviews/{interview_id}.json",
            "md": f"01_interviews/{interview_id}.md",
        },
        "coverage": {
            "core_questions_expected": len(CORE_CODES),
            "core_questions_completed": core_completed,
            "module_questions_expected": len(module_expected_codes),
            "module_questions_completed": module_completed,
            "closure_questions_expected": len(CLOSURE_CODES),
            "closure_questions_completed": closure_completed,
            "evidence_points": evidence_points,
            "kpi_mentions": kpi_mentions,
        },
        "quality_flags": quality_flags,
        "status": status,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Update kit aggregates for one interview")
    parser.add_argument("--kit-root", default="transcriptions/interviews-industrialisees-2026")
    parser.add_argument("--interview-json", required=True)
    parser.add_argument("--source-pdf", required=True, help="Relative path like 01_interviews/file.pdf")
    parser.add_argument("--evidence-json", help="JSON list with evidence rows (without id/source)")
    parser.add_argument("--decisions-json", help="JSON list with decision rows")
    parser.add_argument("--quality-flag", action="append", default=[])
    parser.add_argument("--status", choices=["pass", "pass_with_warnings", "fail"], default=None)
    args = parser.parse_args()

    kit_root = Path(args.kit_root).expanduser().resolve()
    aggregates_dir = kit_root / "02_aggregates"
    aggregates_dir.mkdir(parents=True, exist_ok=True)

    interview_path = Path(args.interview_json).expanduser().resolve()
    interview_json = json.loads(interview_path.read_text(encoding="utf-8"))

    evidence_path = aggregates_dir / "evidence-matrix.csv"
    decision_path = aggregates_dir / "decision-log.csv"
    qa_path = aggregates_dir / "qa-report.json"

    existing_evidence = read_csv_rows(evidence_path, EVIDENCE_HEADERS)
    existing_decisions = read_csv_rows(decision_path, DECISION_HEADERS)

    incoming_evidence = []
    if args.evidence_json:
        payload = json.loads(Path(args.evidence_json).read_text(encoding="utf-8"))
        for row in payload:
            incoming_evidence.append(
                {
                    "id": "",
                    "source": row.get("source", args.source_pdf),
                    "timestamp_ou_page": row.get("timestamp_ou_page", ""),
                    "fait_brut": row.get("fait_brut", ""),
                    "implication_business": row.get("implication_business", ""),
                    "impact_sur_proposition": row.get("impact_sur_proposition", ""),
                }
            )

    incoming_decisions = []
    if args.decisions_json:
        payload = json.loads(Path(args.decisions_json).read_text(encoding="utf-8"))
        for row in payload:
            incoming_decisions.append({h: row.get(h, "") for h in DECISION_HEADERS})

    evidence_seen = {
        (
            row.get("source", ""),
            row.get("timestamp_ou_page", ""),
            row.get("fait_brut", ""),
            row.get("implication_business", ""),
            row.get("impact_sur_proposition", ""),
        )
        for row in existing_evidence
    }

    for row in incoming_evidence:
        key = (
            row.get("source", ""),
            row.get("timestamp_ou_page", ""),
            row.get("fait_brut", ""),
            row.get("implication_business", ""),
            row.get("impact_sur_proposition", ""),
        )
        if key not in evidence_seen:
            existing_evidence.append(row)
            evidence_seen.add(key)

    existing_evidence = renumber_evidence(existing_evidence)
    write_csv_rows(evidence_path, EVIDENCE_HEADERS, existing_evidence)

    decision_seen = {
        tuple(row.get(h, "") for h in DECISION_HEADERS)
        for row in existing_decisions
    }
    for row in incoming_decisions:
        key = tuple(row.get(h, "") for h in DECISION_HEADERS)
        if key not in decision_seen:
            existing_decisions.append(row)
            decision_seen.add(key)

    write_csv_rows(decision_path, DECISION_HEADERS, existing_decisions)

    now_iso = datetime.now().astimezone().isoformat(timespec="seconds")
    status = args.status or ("pass_with_warnings" if args.quality_flag else "pass")

    if qa_path.exists():
        qa_report = json.loads(qa_path.read_text(encoding="utf-8"))
    else:
        qa_report = {
            "generated_at": now_iso,
            "scope": str(kit_root),
            "interviews_processed": 0,
            "interviews": [],
            "aggregates": {
                "evidence_matrix_rows": 0,
                "decision_log_rows": 0,
            },
            "global_status": "pass",
        }

    new_entry = build_qa_entry(
        interview_json=interview_json,
        source_pdf=args.source_pdf,
        quality_flags=args.quality_flag,
        status=status,
    )

    interviews = qa_report.get("interviews", [])
    replaced = False
    for idx, item in enumerate(interviews):
        if item.get("interview_id") == new_entry["interview_id"]:
            interviews[idx] = new_entry
            replaced = True
            break
    if not replaced:
        interviews.append(new_entry)

    qa_report["generated_at"] = now_iso
    qa_report["scope"] = "transcriptions/interviews-industrialisees-2026"
    qa_report["interviews"] = interviews
    qa_report["interviews_processed"] = len(interviews)
    qa_report["aggregates"] = {
        "evidence_matrix_rows": len(existing_evidence),
        "decision_log_rows": len(existing_decisions),
    }

    if any(item.get("status") == "fail" for item in interviews):
        global_status = "fail"
    elif any(item.get("status") == "pass_with_warnings" for item in interviews):
        global_status = "pass_with_warnings"
    else:
        global_status = "pass"

    qa_report["global_status"] = global_status

    qa_path.write_text(json.dumps(qa_report, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")

    result = {
        "status": "updated",
        "interview_id": interview_json["interview_id"],
        "evidence_rows": len(existing_evidence),
        "decision_rows": len(existing_decisions),
        "interviews_processed": len(interviews),
        "global_status": global_status,
    }
    print(json.dumps(result, ensure_ascii=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
