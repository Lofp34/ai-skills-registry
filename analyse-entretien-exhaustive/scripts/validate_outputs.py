#!/usr/bin/env python3
"""Validate exhaustive interview-analysis output folders."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Set

REQUIRED_ROOT_FILES = [
    "manifest.json",
    "global_overview.json",
    "topic_candidates.json",
    "topic_map.json",
    "rhetorical_map.json",
    "qa_report.json",
    "reports/02_analyse-rhetorique.md",
    "reports/03_compte-rendu-exhaustif.md",
]

REQUIRED_MANIFEST_FIELDS = {
    "skill_version": str,
    "source_file": str,
    "language": str,
    "segment_count": int,
    "topic_count": int,
    "coverage_ratio": (int, float),
    "qa_status": str,
    "created_at": str,
}

REQUIRED_TOPIC_FIELDS = {
    "topic_id": str,
    "label": str,
    "definition": str,
    "parent_topic_id": (str, type(None)),
    "segment_refs": list,
}

REQUIRED_TOPIC_DETAIL_FIELDS = [
    "key_ideas",
    "claims",
    "decisions",
    "open_questions",
    "risks",
    "contradictions",
    "rhetorical_moves",
    "evidence_refs",
]


@dataclass
class ValidationState:
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

    def error(self, message: str) -> None:
        self.errors.append(message)

    def warn(self, message: str) -> None:
        self.warnings.append(message)



def _load_json(path: Path, state: ValidationState) -> Optional[Dict[str, Any]]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        state.error(f"Missing file: {path}")
        return None
    except json.JSONDecodeError as exc:
        state.error(f"Invalid JSON in {path}: {exc}")
        return None

    if not isinstance(data, dict):
        state.error(f"JSON root must be an object in {path}")
        return None
    return data


def _check_required_files(analysis_dir: Path, state: ValidationState) -> None:
    for rel in REQUIRED_ROOT_FILES:
        path = analysis_dir / rel
        if not path.exists():
            state.error(f"Missing required output: {rel}")

    topics_dir = analysis_dir / "topics"
    if not topics_dir.exists() or not topics_dir.is_dir():
        state.error("Missing required directory: topics/")
        return

    topic_files = sorted(topics_dir.glob("topic-*.json"))
    if not topic_files:
        state.error("No topic detail file found in topics/ (expected topic-*.json)")



def _validate_manifest(manifest: Dict[str, Any], state: ValidationState) -> None:
    for field_name, expected_type in REQUIRED_MANIFEST_FIELDS.items():
        if field_name not in manifest:
            state.error(f"manifest.json missing field '{field_name}'")
            continue
        if not isinstance(manifest[field_name], expected_type):
            state.error(
                f"manifest.json field '{field_name}' has invalid type "
                f"({type(manifest[field_name]).__name__})"
            )

    coverage = manifest.get("coverage_ratio")
    if isinstance(coverage, (int, float)) and not 0 <= float(coverage) <= 1:
        state.error("manifest.json coverage_ratio must be between 0 and 1")



def _validate_topic_map(topic_map: Dict[str, Any], state: ValidationState) -> Set[str]:
    topics = topic_map.get("topics")
    if not isinstance(topics, list) or not topics:
        state.error("topic_map.json must contain a non-empty 'topics' array")
        return set()

    segment_refs: Set[str] = set()

    for idx, topic in enumerate(topics, start=1):
        if not isinstance(topic, dict):
            state.error(f"topic_map.json topics[{idx}] must be an object")
            continue

        for field_name, expected_type in REQUIRED_TOPIC_FIELDS.items():
            if field_name not in topic:
                state.error(f"topic_map.json topics[{idx}] missing field '{field_name}'")
                continue
            if not isinstance(topic[field_name], expected_type):
                state.error(
                    f"topic_map.json topics[{idx}] field '{field_name}' has invalid type"
                )

        for ref in topic.get("segment_refs", []):
            if isinstance(ref, str):
                segment_refs.add(ref)
            else:
                state.warn(f"Non-string segment ref in topic '{topic.get('topic_id', idx)}'")

    return segment_refs



def _validate_rhetorical_map(rhet_map: Dict[str, Any], state: ValidationState) -> None:
    for key in ["moves", "speaker_profile", "influence_patterns", "ambiguities"]:
        if key not in rhet_map:
            state.error(f"rhetorical_map.json missing '{key}'")
        elif not isinstance(rhet_map[key], list):
            state.error(f"rhetorical_map.json '{key}' must be an array")



def _extract_segment_refs(value: Any) -> Iterable[str]:
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        segment_id = value.get("segment_id")
        if isinstance(segment_id, str):
            yield segment_id
    elif isinstance(value, list):
        for item in value:
            yield from _extract_segment_refs(item)



def _validate_topic_files(analysis_dir: Path, state: ValidationState) -> Set[str]:
    topics_dir = analysis_dir / "topics"
    refs: Set[str] = set()

    for topic_file in sorted(topics_dir.glob("topic-*.json")):
        data = _load_json(topic_file, state)
        if not data:
            continue

        for field_name in REQUIRED_TOPIC_DETAIL_FIELDS:
            if field_name not in data:
                state.error(f"{topic_file.name} missing field '{field_name}'")
                continue
            if not isinstance(data[field_name], list):
                state.error(f"{topic_file.name} field '{field_name}' must be an array")

        for ref in _extract_segment_refs(data.get("evidence_refs", [])):
            refs.add(ref)

    return refs



def _read_segments(analysis_dir: Path, state: ValidationState) -> Set[str]:
    segments_path = analysis_dir / "segments.jsonl"
    if not segments_path.exists():
        state.warn("segments.jsonl not found: coverage computed from manifest/topic refs only")
        return set()

    ids: Set[str] = set()
    for i, line in enumerate(segments_path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            state.error(f"Invalid JSONL row in segments.jsonl at line {i}")
            continue
        segment_id = row.get("segment_id")
        if not isinstance(segment_id, str):
            state.error(f"segments.jsonl line {i} missing string segment_id")
            continue
        ids.add(segment_id)
    return ids



def _format_ratio(value: float) -> str:
    return f"{value:.4f}"



def main() -> None:
    parser = argparse.ArgumentParser(
        description="Validate exhaustive interview analysis outputs against expected schema and QA rules."
    )
    parser.add_argument("--analysis-dir", required=True, help="Analysis output directory")
    parser.add_argument(
        "--min-coverage",
        type=float,
        default=0.98,
        help="Minimum required segment coverage ratio (default: 0.98)",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Fail on warnings in addition to errors.",
    )
    args = parser.parse_args()

    analysis_dir = Path(args.analysis_dir).expanduser().resolve()
    if not analysis_dir.exists() or not analysis_dir.is_dir():
        _die = f"Analysis directory not found: {analysis_dir}"
        print(f"Error: {_die}", file=sys.stderr)
        raise SystemExit(1)

    state = ValidationState()
    _check_required_files(analysis_dir, state)

    manifest = _load_json(analysis_dir / "manifest.json", state)
    topic_map = _load_json(analysis_dir / "topic_map.json", state)
    rhet_map = _load_json(analysis_dir / "rhetorical_map.json", state)

    if manifest:
        _validate_manifest(manifest, state)
    topic_map_refs: Set[str] = set()
    if topic_map:
        topic_map_refs = _validate_topic_map(topic_map, state)
    if rhet_map:
        _validate_rhetorical_map(rhet_map, state)

    topic_detail_refs = _validate_topic_files(analysis_dir, state)
    known_segments = _read_segments(analysis_dir, state)

    ref_union = topic_map_refs.union(topic_detail_refs)

    if known_segments:
        covered = len(known_segments.intersection(ref_union))
        coverage = covered / len(known_segments)
    elif manifest and isinstance(manifest.get("coverage_ratio"), (int, float)):
        coverage = float(manifest["coverage_ratio"])
    else:
        coverage = 0.0
        state.warn("Cannot compute coverage ratio from files")

    if coverage < args.min_coverage:
        state.error(
            f"Coverage below threshold: got {_format_ratio(coverage)}, "
            f"required >= {_format_ratio(args.min_coverage)}"
        )

    if manifest and isinstance(manifest.get("coverage_ratio"), (int, float)):
        manifest_cov = float(manifest["coverage_ratio"])
        if abs(manifest_cov - coverage) > 0.02:
            state.warn(
                "manifest coverage_ratio differs from computed coverage by more than 0.02"
            )

    print(f"Analysis dir: {analysis_dir}")
    print(f"Computed coverage: {_format_ratio(coverage)}")
    print(f"Errors: {len(state.errors)}")
    print(f"Warnings: {len(state.warnings)}")

    for msg in state.errors:
        print(f"ERROR: {msg}")
    for msg in state.warnings:
        print(f"WARN: {msg}")

    if state.errors:
        raise SystemExit(1)
    if args.strict and state.warnings:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
