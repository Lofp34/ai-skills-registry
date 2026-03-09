#!/usr/bin/env python3
"""Refresh enterprise client context: email ingestion + tracking stamps."""

from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path
import re
import subprocess
import sys
from typing import Any, Dict, List, Tuple

try:
    from zoneinfo import ZoneInfo
except ImportError:  # pragma: no cover
    ZoneInfo = None  # type: ignore


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Refresh context for a standardized enterprise client folder.",
    )
    parser.add_argument("--project-dir", default=".", help="Client folder path")
    parser.add_argument(
        "--python-bin",
        default=sys.executable,
        help="Python interpreter used to run sub-scripts (default: current interpreter)",
    )
    parser.add_argument(
        "--config-path",
        default="documentation/client-config.yaml",
        help="Config path relative to project-dir",
    )
    parser.add_argument("--client-secret", default="", help="Override Gmail client secret path")
    parser.add_argument("--token-file", default="", help="Override Gmail token file path")
    parser.add_argument("--months-back", type=int, default=0, help="Override email window in months")
    parser.add_argument("--start-date", default="", help="Override YYYY-MM-DD (takes precedence)")
    parser.add_argument("--max-messages", type=int, default=0, help="Override max Gmail messages")
    parser.add_argument(
        "--include-public-domains",
        action="store_true",
        help="Force include public domains in domain matching",
    )
    parser.add_argument(
        "--download-attachments",
        action="store_true",
        help="Force attachment download",
    )
    parser.add_argument(
        "--progress-mode",
        choices=["auto", "bar", "log", "none"],
        default="auto",
        help="Progress display mode",
    )
    parser.add_argument(
        "--tracker-mode",
        choices=["manual", "auto", "off"],
        default="manual",
        help="Stamp tracking metadata mode",
    )
    parser.add_argument("--dry-run", action="store_true", help="Run without writing emails")
    return parser.parse_args()

def parse_scalar(raw: str) -> Any:
    value = raw.strip()
    if not value:
        return ""
    if value.startswith(("\"", "'")) and value.endswith(("\"", "'")) and len(value) >= 2:
        return value[1:-1]
    lowered = value.lower()
    if lowered in {"true", "false"}:
        return lowered == "true"
    if re.fullmatch(r"-?\d+", value):
        try:
            return int(value)
        except ValueError:
            return value
    return value


def load_simple_yaml(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}

    root: Dict[str, Any] = {}
    stack: List[Tuple[int, Dict[str, Any]]] = [(-1, root)]

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue

        indent = len(raw_line) - len(raw_line.lstrip(" "))
        line = raw_line.strip()

        if line.startswith("- "):
            continue
        if ":" not in line:
            continue

        key, raw_value = line.split(":", 1)
        key = key.strip()
        raw_value = raw_value.strip()

        while stack and indent <= stack[-1][0]:
            stack.pop()
        parent = stack[-1][1] if stack else root

        if raw_value == "":
            child: Dict[str, Any] = {}
            parent[key] = child
            stack.append((indent, child))
        else:
            parent[key] = parse_scalar(raw_value)

    return root


def nested_get(data: Dict[str, Any], path: str, default: Any = "") -> Any:
    current: Any = data
    for part in path.split("."):
        if not isinstance(current, dict) or part not in current:
            return default
        current = current[part]
    return current


def as_bool(value: Any, default: bool = False) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, int):
        return value != 0
    if isinstance(value, str):
        return value.strip().lower() in {"1", "true", "yes", "on"}
    return default


def now_tz_label(tz_name: str) -> str:
    if ZoneInfo is None:
        now = datetime.now()
    else:
        try:
            now = datetime.now(ZoneInfo(tz_name))
        except Exception:
            now = datetime.now()
    return now.strftime("%Y-%m-%d %H:%M")


def append_bullet_under_heading(file_path: Path, heading: str, bullet: str) -> None:
    if not file_path.exists():
        return

    lines = file_path.read_text(encoding="utf-8").splitlines()
    insert_idx = None
    section_start = None
    section_end = None

    for i, line in enumerate(lines):
        if line.strip() == heading:
            j = i + 1
            while j < len(lines) and not lines[j].startswith("## "):
                j += 1
            insert_idx = j
            section_start = i + 1
            section_end = j
            break

    if insert_idx is None:
        lines.append("")
        lines.append(heading)
        lines.append(bullet)
        lines.append("")
    else:
        section_lines = [x.strip() for x in lines[section_start:section_end] if x.strip()] if section_start is not None and section_end is not None else []
        if bullet.strip() in section_lines:
            return
        lines.insert(insert_idx, bullet)
        lines.insert(insert_idx + 1, "")

    normalized: List[str] = []
    prev_nonempty = False
    prev_blank = False
    for line in lines:
        if not line.strip():
            if prev_blank:
                continue
            normalized.append("")
            prev_blank = True
            continue
        if line.startswith("## ") and prev_nonempty and not prev_blank:
            normalized.append("")
        normalized.append(line)
        prev_nonempty = True
        prev_blank = False

    file_path.write_text("\n".join(normalized).rstrip() + "\n", encoding="utf-8")


def run_command(cmd: List[str]) -> None:
    print("$ " + " ".join(cmd), flush=True)
    subprocess.run(cmd, check=True)


def main() -> int:
    args = parse_args()

    project_dir = Path(args.project_dir).resolve()
    python_bin = str(Path(args.python_bin).expanduser())
    config_path = project_dir / args.config_path
    if not config_path.exists():
        print(f"Missing config file: {config_path}", file=sys.stderr)
        print("Run bootstrap_client.py first.", file=sys.stderr)
        return 2

    config = load_simple_yaml(config_path)
    tz = str(nested_get(config, "mission.timezone", "Europe/Paris") or "Europe/Paris")

    contacts_csv_rel = str(nested_get(config, "data.contacts_csv", "contacts.csv") or "contacts.csv")
    contacts_csv = (project_dir / contacts_csv_rel).resolve()

    email_enabled = as_bool(nested_get(config, "email_ingestion.enabled", True), True)
    months_back = int(args.months_back or nested_get(config, "email_ingestion.months_back", 6) or 6)
    max_messages = int(args.max_messages or nested_get(config, "email_ingestion.max_messages", 2000) or 2000)
    include_public_domains = args.include_public_domains or as_bool(
        nested_get(config, "email_ingestion.include_public_domains", False),
        False,
    )
    max_domain_projects = int(nested_get(config, "email_ingestion.max_domain_projects", 1) or 1)
    name_query_mode = str(nested_get(config, "email_ingestion.name_query_mode", "on") or "on")
    name_match_mode = str(nested_get(config, "email_ingestion.name_match_mode", "on") or "on")
    name_min_tokens = int(nested_get(config, "email_ingestion.name_min_tokens", 2) or 2)
    gmail_query_mode = str(nested_get(config, "email_ingestion.gmail_query_mode", "focused") or "focused")
    download_attachments = args.download_attachments or as_bool(
        nested_get(config, "email_ingestion.download_attachments", False),
        False,
    )
    start_date = args.start_date or str(nested_get(config, "email_ingestion.start_date", "") or "")

    config_client_secret = str(
        nested_get(config, "auth.gmail_client_secret", "secrets/gmail_client_secret.json")
        or "secrets/gmail_client_secret.json"
    )
    config_token_file = str(
        nested_get(config, "auth.gmail_token_file", "secrets/gmail_read_token.json")
        or "secrets/gmail_read_token.json"
    )
    client_secret = (
        Path(args.client_secret).resolve()
        if args.client_secret
        else (project_dir / config_client_secret).resolve()
    )
    token_file = (
        Path(args.token_file).resolve()
        if args.token_file
        else (project_dir / config_token_file).resolve()
    )

    scripts_dir = Path(__file__).resolve().parent
    centralize_script = scripts_dir / "centralize_project_emails.py"
    tracker_script = scripts_dir / "update_tracker_metadata.py"

    if email_enabled:
        cmd = [
            python_bin,
            str(centralize_script),
            "--contacts-file",
            str(contacts_csv),
            "--output-dir",
            str(project_dir / "emails"),
            "--client-secret",
            str(client_secret),
            "--token-file",
            str(token_file),
            "--months-back",
            str(months_back),
            "--max-messages",
            str(max_messages),
            "--gmail-query-mode",
            gmail_query_mode,
            "--name-query-mode",
            name_query_mode,
            "--name-match-mode",
            name_match_mode,
            "--name-min-tokens",
            str(name_min_tokens),
            "--max-domain-projects",
            str(max_domain_projects),
            "--progress-mode",
            args.progress_mode,
        ]
        if start_date.strip():
            cmd.extend(["--start-date", start_date.strip()])
        if include_public_domains:
            cmd.append("--include-public-domains")
        if download_attachments:
            cmd.append("--download-attachments")
        if args.dry_run:
            cmd.append("--dry-run")

        try:
            run_command(cmd)
        except subprocess.CalledProcessError as exc:
            print(f"Email ingestion failed with exit code {exc.returncode}", file=sys.stderr)
            return exc.returncode
    else:
        print("Email ingestion disabled by config (email_ingestion.enabled=false).")

    if not args.dry_run:
        stamp_time = now_tz_label(tz)
        sources_index = project_dir / "documentation" / "sources-index.md"
        project_status = project_dir / "documentation" / "project-status.md"

        append_bullet_under_heading(
            sources_index,
            "## Refresh Log",
            f"- {stamp_time} {tz} | refresh-context | Email ingestion refreshed ({months_back} months window)",
        )
        append_bullet_under_heading(
            project_status,
            "## Daily Update Log",
            f"- {stamp_time} {tz} | manual | Context refresh executed (emails + indexes) | Continue weekly review rhythm",
        )

        if args.tracker_mode != "off" and tracker_script.exists():
            tracker_cmd = [
                python_bin,
                str(tracker_script),
                "stamp",
                "--project-dir",
                str(project_dir),
                "--status-file",
                "documentation/project-status.md",
                "--mode",
                args.tracker_mode,
            ]
            try:
                run_command(tracker_cmd)
            except subprocess.CalledProcessError as exc:
                print(f"Tracker stamp failed with exit code {exc.returncode}", file=sys.stderr)
                return exc.returncode

    print("Context refresh completed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
