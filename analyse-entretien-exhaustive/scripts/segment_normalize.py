#!/usr/bin/env python3
"""Normalize transcript text into atomic JSONL segments."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional

DEFAULT_SPEAKER_PATTERN = r"^(?P<speaker>[A-Za-zÀ-ÖØ-öø-ÿ0-9 _.-]{2,80})\s*:\s*(?P<text>.*)$"
DEFAULT_TIMESTAMP_PATTERN = r"^(?P<ts>\d{2}:\d{2}:\d{2})$"


def _die(message: str, code: int = 1) -> None:
    print(f"Error: {message}", file=sys.stderr)
    raise SystemExit(code)


def _clean_line(line: str) -> str:
    line = line.replace("\ufeff", "").replace("\f", "")
    return line.strip()


def _compact_text(parts: List[str]) -> str:
    text = " ".join(part.strip() for part in parts if part.strip())
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def _parse_segments(
    raw_text: str,
    source_ref: str,
    speaker_re: re.Pattern[str],
    ts_re: re.Pattern[str],
) -> List[Dict[str, object]]:
    segments: List[Dict[str, object]] = []
    current_ts: Optional[str] = None
    current_speaker: Optional[str] = None
    current_parts: List[str] = []

    def flush() -> None:
        nonlocal current_speaker, current_parts
        if current_speaker is None and not current_parts:
            return

        text = _compact_text(current_parts)
        if not text:
            current_speaker = None
            current_parts = []
            return

        segment_id = f"s{len(segments) + 1:06d}"
        segments.append(
            {
                "segment_id": segment_id,
                "start_time": current_ts,
                "speaker": current_speaker or "Unknown",
                "text": text,
                "source_ref": source_ref,
            }
        )
        current_speaker = None
        current_parts = []

    lines = raw_text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    for raw_line in lines:
        line = _clean_line(raw_line)
        if not line:
            continue

        ts_match = ts_re.match(line)
        if ts_match:
            flush()
            current_ts = ts_match.groupdict().get("ts") or line
            continue

        speaker_match = speaker_re.match(line)
        if speaker_match:
            flush()
            gd = speaker_match.groupdict()
            current_speaker = gd.get("speaker", "Unknown").strip() or "Unknown"
            opening_text = (gd.get("text") or "").strip()
            current_parts = [opening_text] if opening_text else []
            continue

        # Drop common OCR/page artefacts.
        if line in {"|", "_", "-", "--"}:
            continue

        if current_speaker is None:
            current_speaker = "Unknown"
            current_parts = [line]
        else:
            current_parts.append(line)

    flush()
    return segments


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Normalize a transcript text file into atomic segments JSONL."
    )
    parser.add_argument("--input", required=True, help="Path to raw transcript text file")
    parser.add_argument("--output", required=True, help="Path to output JSONL file")
    parser.add_argument(
        "--speaker-pattern",
        default=DEFAULT_SPEAKER_PATTERN,
        help=(
            "Regex for speaker lines. Must define named group 'speaker'. "
            "Optional named group 'text' for same-line content."
        ),
    )
    parser.add_argument(
        "--timestamp-pattern",
        default=DEFAULT_TIMESTAMP_PATTERN,
        help="Regex for timestamps. Optional named group 'ts'.",
    )
    args = parser.parse_args()

    input_path = Path(args.input).expanduser().resolve()
    output_path = Path(args.output).expanduser().resolve()

    if not input_path.exists():
        _die(f"Input file not found: {input_path}")

    try:
        speaker_re = re.compile(args.speaker_pattern)
    except re.error as exc:
        _die(f"Invalid --speaker-pattern regex: {exc}")
    if "speaker" not in speaker_re.groupindex:
        _die("--speaker-pattern must expose named group 'speaker'")

    try:
        ts_re = re.compile(args.timestamp_pattern)
    except re.error as exc:
        _die(f"Invalid --timestamp-pattern regex: {exc}")

    raw_text = input_path.read_text(encoding="utf-8")
    segments = _parse_segments(raw_text, str(input_path), speaker_re, ts_re)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as handle:
        for segment in segments:
            handle.write(json.dumps(segment, ensure_ascii=False) + "\n")

    with_ts = sum(1 for s in segments if s.get("start_time"))
    print(
        f"[OK] Segments written | total={len(segments)} | with_timestamp={with_ts} "
        f"| output={output_path}",
        file=sys.stderr,
    )


if __name__ == "__main__":
    main()
