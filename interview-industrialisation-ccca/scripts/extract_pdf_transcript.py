#!/usr/bin/env python3
"""Extract transcript text from a PDF using pdftotext with layout preservation."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path


def run_pdftotext(pdf_path: Path, output_path: Path) -> None:
    cmd = ["pdftotext", "-layout", str(pdf_path), str(output_path)]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        stderr = (result.stderr or "").strip()
        raise RuntimeError(f"pdftotext failed: {stderr}")


def summarize_text(path: Path) -> dict:
    text = path.read_text(encoding="utf-8", errors="ignore")
    lines = text.splitlines()
    timestamps = re.findall(r"\b\d{2}:\d{2}:\d{2}\b", text)
    return {
        "output_path": str(path),
        "line_count": len(lines),
        "timestamp_mentions": len(timestamps),
        "first_timestamp": timestamps[0] if timestamps else None,
        "last_timestamp": timestamps[-1] if timestamps else None,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Extract transcript from PDF into _extracted.txt")
    parser.add_argument("--pdf-path", required=True, help="Path to source PDF transcription")
    parser.add_argument("--output-path", help="Output text file path (default: <pdf>_extracted.txt)")
    parser.add_argument("--force", action="store_true", help="Overwrite output file if it exists")
    args = parser.parse_args()

    pdf_path = Path(args.pdf_path).expanduser().resolve()
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    if args.output_path:
        output_path = Path(args.output_path).expanduser().resolve()
    else:
        output_path = pdf_path.with_name(f"{pdf_path.stem}_extracted.txt")

    if output_path.exists() and not args.force:
        summary = summarize_text(output_path)
        summary["status"] = "already_exists"
        print(json.dumps(summary, ensure_ascii=True, indent=2))
        return 0

    run_pdftotext(pdf_path, output_path)
    summary = summarize_text(output_path)
    summary["status"] = "created"
    print(json.dumps(summary, ensure_ascii=True, indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:  # pragma: no cover
        print(json.dumps({"status": "error", "message": str(exc)}, ensure_ascii=True), file=sys.stderr)
        raise SystemExit(1)
