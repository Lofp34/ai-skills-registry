#!/usr/bin/env python3
"""Detect folder changes and manage tracker metadata in project-status.md."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, List

try:
    from zoneinfo import ZoneInfo
except ImportError:  # pragma: no cover
    ZoneInfo = None  # type: ignore

EXCLUDE_DIRS = {
    ".git",
    ".hg",
    ".svn",
    "node_modules",
    "__pycache__",
    ".venv",
    "venv",
}
EXCLUDE_FILES = {".DS_Store"}
META_PATTERN = re.compile(r"<!--\s*tracker-meta\s*(.*?)\s*-->", re.DOTALL)


@dataclass
class FileEntry:
    path: str
    size: int
    mtime_ns: int


def now_in_tz(tz_name: str) -> datetime:
    if ZoneInfo is None:
        return datetime.now()
    return datetime.now(ZoneInfo(tz_name))


def normalize_path(path_value: str, base_dir: Path | None = None) -> Path:
    path = Path(path_value)
    if not path.is_absolute() and base_dir is not None:
        path = base_dir / path
    return path.resolve()


def should_skip_dir(name: str) -> bool:
    return name in EXCLUDE_DIRS or name.startswith(".")


def should_skip_file(name: str) -> bool:
    return name in EXCLUDE_FILES or name.startswith("~$")


def collect_entries(project_dir: Path, status_file: Path) -> List[FileEntry]:
    entries: List[FileEntry] = []
    for root, dirs, files in os.walk(project_dir):
        dirs[:] = [d for d in dirs if not should_skip_dir(d)]
        root_path = Path(root)
        for filename in files:
            if should_skip_file(filename):
                continue
            file_path = root_path / filename
            if file_path.resolve() == status_file:
                continue
            if file_path.is_symlink():
                continue
            try:
                stat = file_path.stat()
            except OSError:
                continue
            rel_path = file_path.resolve().relative_to(project_dir).as_posix()
            entries.append(FileEntry(path=rel_path, size=stat.st_size, mtime_ns=stat.st_mtime_ns))
    entries.sort(key=lambda e: e.path)
    return entries


def snapshot_hash(entries: List[FileEntry]) -> str:
    hasher = hashlib.sha256()
    for entry in entries:
        chunk = f"{entry.path}|{entry.size}|{entry.mtime_ns}\n"
        hasher.update(chunk.encode("utf-8"))
    return hasher.hexdigest()


def read_meta(status_file: Path) -> Dict[str, str]:
    if not status_file.exists():
        return {}
    text = status_file.read_text(encoding="utf-8", errors="replace")
    match = META_PATTERN.search(text)
    if not match:
        return {}

    raw_block = match.group(1)
    meta: Dict[str, str] = {}
    for raw_line in raw_block.splitlines():
        line = raw_line.strip()
        if not line or ":" not in line:
            continue
        key, value = line.split(":", 1)
        meta[key.strip()] = value.strip()
    return meta


def upsert_meta_block(text: str, meta_lines: List[str]) -> str:
    meta_block = "<!-- tracker-meta\n" + "\n".join(meta_lines) + "\n-->"
    if META_PATTERN.search(text):
        return META_PATTERN.sub(meta_block, text, count=1)

    stripped = text.rstrip()
    if stripped:
        return stripped + "\n\n" + meta_block + "\n"
    return meta_block + "\n"


def fmt_iso(dt: datetime) -> str:
    return dt.isoformat(timespec="seconds")


def fmt_date(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%d")


def decide(args: argparse.Namespace) -> int:
    project_dir = normalize_path(args.project_dir)
    status_file = normalize_path(args.status_file, project_dir)

    entries = collect_entries(project_dir, status_file)
    current_hash = snapshot_hash(entries)
    meta = read_meta(status_file)

    now = now_in_tz(args.tz)
    today = fmt_date(now)

    last_hash = meta.get("last_hash", "")
    last_auto_update_date = meta.get("last_auto_update_date", "")

    changed_since_last_hash = current_hash != last_hash if last_hash else True

    if args.force:
        should_update = True
        reason = "manual_force"
    elif not status_file.exists():
        should_update = True
        reason = "status_file_missing"
    elif not last_hash:
        should_update = True
        reason = "metadata_missing"
    elif not changed_since_last_hash:
        should_update = False
        reason = "no_file_change"
    elif last_auto_update_date == today:
        should_update = False
        reason = "already_updated_today"
    else:
        should_update = True
        reason = "file_changes_detected"

    recent = sorted(entries, key=lambda e: e.mtime_ns, reverse=True)[: args.max_recent_files]
    recent_files = [
        {
            "path": item.path,
            "size": item.size,
            "mtime_ns": item.mtime_ns,
        }
        for item in recent
    ]

    payload = {
        "should_update": should_update,
        "reason": reason,
        "project_dir": str(project_dir),
        "status_file": str(status_file),
        "status_file_exists": status_file.exists(),
        "today": today,
        "timezone": args.tz,
        "current_hash": current_hash,
        "last_hash": last_hash,
        "changed_since_last_hash": changed_since_last_hash,
        "last_auto_update_date": last_auto_update_date,
        "recent_files": recent_files,
    }

    if args.json_pretty:
        print(json.dumps(payload, indent=2, ensure_ascii=True))
    else:
        print(json.dumps(payload, ensure_ascii=True))
    return 0


def stamp(args: argparse.Namespace) -> int:
    project_dir = normalize_path(args.project_dir)
    status_file = normalize_path(args.status_file, project_dir)
    status_file.parent.mkdir(parents=True, exist_ok=True)

    existing_text = ""
    if status_file.exists():
        existing_text = status_file.read_text(encoding="utf-8", errors="replace")
    else:
        existing_text = "# Project Status\n\n"

    entries = collect_entries(project_dir, status_file)
    current_hash = snapshot_hash(entries)
    now = now_in_tz(args.tz)
    today = fmt_date(now)

    old_meta = read_meta(status_file)
    last_auto_update_date = old_meta.get("last_auto_update_date", "")
    if args.mode == "auto":
        last_auto_update_date = today

    meta_lines = [
        "schema_version: 1",
        f"last_hash: {current_hash}",
        f"last_update_at: {fmt_iso(now)}",
        f"last_update_date: {today}",
        f"last_update_mode: {args.mode}",
        f"last_auto_update_date: {last_auto_update_date}",
    ]

    updated_text = upsert_meta_block(existing_text, meta_lines)
    status_file.write_text(updated_text, encoding="utf-8")

    payload = {
        "status": "ok",
        "status_file": str(status_file),
        "mode": args.mode,
        "today": today,
        "timezone": args.tz,
        "last_hash": current_hash,
        "last_auto_update_date": last_auto_update_date,
    }
    if args.json_pretty:
        print(json.dumps(payload, indent=2, ensure_ascii=True))
    else:
        print(json.dumps(payload, ensure_ascii=True))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Decide/stamp updates for documentation/project-status.md",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    decide_parser = subparsers.add_parser("decide", help="Decide if report update is required")
    decide_parser.add_argument("--project-dir", default=".", help="Client project folder")
    decide_parser.add_argument(
        "--status-file",
        default="documentation/project-status.md",
        help="Path to project status markdown file (absolute or relative to project-dir)",
    )
    decide_parser.add_argument("--tz", default="Europe/Paris", help="Timezone for daily rule")
    decide_parser.add_argument("--force", action="store_true", help="Force update decision")
    decide_parser.add_argument("--max-recent-files", type=int, default=20, help="Max recent files in output")
    decide_parser.add_argument("--json-pretty", action="store_true", help="Pretty JSON output")
    decide_parser.set_defaults(func=decide)

    stamp_parser = subparsers.add_parser("stamp", help="Write tracker metadata after report update")
    stamp_parser.add_argument("--project-dir", default=".", help="Client project folder")
    stamp_parser.add_argument(
        "--status-file",
        default="documentation/project-status.md",
        help="Path to project status markdown file (absolute or relative to project-dir)",
    )
    stamp_parser.add_argument("--tz", default="Europe/Paris", help="Timezone for metadata timestamps")
    stamp_parser.add_argument("--mode", choices=["auto", "manual"], required=True, help="Update mode")
    stamp_parser.add_argument("--json-pretty", action="store_true", help="Pretty JSON output")
    stamp_parser.set_defaults(func=stamp)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
