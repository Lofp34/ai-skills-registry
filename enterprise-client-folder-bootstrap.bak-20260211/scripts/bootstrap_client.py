#!/usr/bin/env python3
"""Bootstrap an enterprise client folder with a reusable V1 structure."""

from __future__ import annotations

import argparse
import csv
from datetime import datetime
from pathlib import Path
import re
from typing import Any, Dict, List, Tuple

try:
    from zoneinfo import ZoneInfo
except ImportError:  # pragma: no cover
    ZoneInfo = None  # type: ignore


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Initialize a standardized enterprise client folder.",
    )
    parser.add_argument("--target-dir", default=".", help="Client folder to initialize")
    parser.add_argument(
        "--config-path",
        default="documentation/client-config.yaml",
        help="Config file path relative to target-dir",
    )
    parser.add_argument(
        "--contacts-path",
        default="contacts.csv",
        help="Contacts CSV path relative to target-dir",
    )
    parser.add_argument(
        "--timezone",
        default="Europe/Paris",
        help="Fallback timezone when mission.timezone is missing",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite generated files if they already exist",
    )
    parser.add_argument(
        "--no-sample-contacts",
        action="store_true",
        help="Do not create contacts.csv when missing",
    )
    return parser.parse_args()


def skill_root() -> Path:
    return Path(__file__).resolve().parents[1]


def now_tz(tz_name: str) -> datetime:
    if ZoneInfo is None:
        return datetime.now()
    try:
        return datetime.now(ZoneInfo(tz_name))
    except Exception:
        return datetime.now()


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
    """Parse a simple nested YAML map (single-level nesting + scalars)."""
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


def render_template(text: str, values: Dict[str, str]) -> str:
    rendered = text
    for key, value in values.items():
        rendered = rendered.replace(f"{{{{{key}}}}}", value)
    return rendered


def write_text(path: Path, content: str, force: bool) -> bool:
    if path.exists() and not force:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return True


def ensure_dirs(target_dir: Path) -> None:
    for rel in [
        "documentation",
        "emails",
        "transcriptions",
        "notes",
        "deliverables",
        "sources",
        "secrets",
    ]:
        (target_dir / rel).mkdir(parents=True, exist_ok=True)


def create_contacts_csv(path: Path, force: bool) -> bool:
    if path.exists() and not force:
        return False

    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "project_id",
                "nom_projet",
                "porteur_nom",
                "email",
                "role",
                "organisation",
                "notes",
            ]
        )
    return True


def main() -> int:
    args = parse_args()

    target_dir = Path(args.target_dir).resolve()
    config_path = target_dir / args.config_path
    contacts_path = target_dir / args.contacts_path

    root = skill_root()
    template_config = root / "assets" / "client-config.template.yaml"
    template_status = root / "references" / "project-status-template.md"
    template_sources = root / "references" / "sources-index-template.md"

    ensure_dirs(target_dir)

    created: List[str] = []
    skipped: List[str] = []

    if write_text(config_path, template_config.read_text(encoding="utf-8"), args.force):
        created.append(str(config_path.relative_to(target_dir)))
    else:
        skipped.append(str(config_path.relative_to(target_dir)))

    config = load_simple_yaml(config_path)
    tz = str(nested_get(config, "mission.timezone", args.timezone) or args.timezone)
    now = now_tz(tz)

    replacements = {
        "CLIENT_NAME": str(nested_get(config, "client.name", target_dir.name) or target_dir.name),
        "MISSION_NAME": str(nested_get(config, "mission.name", "Mission") or "Mission"),
        "FOLDER_NAME": target_dir.name,
        "TIMEZONE": tz,
        "UPDATED_AT": now.strftime("%Y-%m-%d %H:%M"),
        "TODAY": now.strftime("%Y-%m-%d"),
    }

    status_content = render_template(template_status.read_text(encoding="utf-8"), replacements)
    status_path = target_dir / "documentation" / "project-status.md"
    if write_text(status_path, status_content, args.force):
        created.append(str(status_path.relative_to(target_dir)))
    else:
        skipped.append(str(status_path.relative_to(target_dir)))

    sources_content = render_template(template_sources.read_text(encoding="utf-8"), replacements)
    sources_path = target_dir / "documentation" / "sources-index.md"
    if write_text(sources_path, sources_content, args.force):
        created.append(str(sources_path.relative_to(target_dir)))
    else:
        skipped.append(str(sources_path.relative_to(target_dir)))

    if not args.no_sample_contacts:
        if create_contacts_csv(contacts_path, args.force):
            created.append(str(contacts_path.relative_to(target_dir)))
        else:
            skipped.append(str(contacts_path.relative_to(target_dir)))

    print("Bootstrap completed.")
    print(f"Target folder: {target_dir}")
    print(f"Created/updated files: {len(created)}")
    for item in created:
        print(f"  + {item}")
    if skipped:
        print(f"Skipped existing files: {len(skipped)}")
        for item in skipped:
            print(f"  = {item}")

    print("\nNext steps:")
    print("1) Edit documentation/client-config.yaml")
    print("2) Fill contacts.csv")
    print("3) Run refresh_context.py to ingest emails and stamp tracking metadata")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
