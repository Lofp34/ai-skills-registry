#!/usr/bin/env python3
"""Extract raw transcript text from PDF/TXT/MD files."""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path

ALLOWED_FORMATS = {"auto", "pdf", "txt", "md"}


def _die(message: str, code: int = 1) -> None:
    print(f"Error: {message}", file=sys.stderr)
    raise SystemExit(code)


def _normalize_text(text: str) -> str:
    # Normalize line endings and trim right-side noise, keep content fidelity.
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = text.replace("\ufeff", "")
    text = "\n".join(line.rstrip() for line in text.split("\n"))
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip() + "\n"


def _detect_format(path: Path, forced: str) -> str:
    if forced != "auto":
        return forced
    suffix = path.suffix.lower().lstrip(".")
    if suffix in {"txt", "md", "pdf"}:
        return suffix
    _die(
        f"Cannot auto-detect format from extension '{path.suffix}'. "
        "Use --format pdf|txt|md explicitly."
    )


def _extract_pdf_with_pdftotext(path: Path) -> str | None:
    binary = shutil.which("pdftotext")
    if not binary:
        return None
    try:
        result = subprocess.run(
            [binary, str(path), "-"],
            check=True,
            capture_output=True,
            text=True,
        )
    except subprocess.CalledProcessError as exc:
        _die(f"pdftotext failed with code {exc.returncode}: {exc.stderr.strip()}")
    return result.stdout


def _extract_pdf_with_pypdf(path: Path) -> str | None:
    try:
        from pypdf import PdfReader  # type: ignore
    except Exception:
        return None

    reader = PdfReader(str(path))
    chunks = []
    for page in reader.pages:
        page_text = page.extract_text() or ""
        chunks.append(page_text)
    return "\n\n".join(chunks)


def _extract_text(path: Path, input_format: str) -> str:
    if input_format in {"txt", "md"}:
        return path.read_text(encoding="utf-8")

    if input_format == "pdf":
        text = _extract_pdf_with_pdftotext(path)
        if text is not None:
            return text

        text = _extract_pdf_with_pypdf(path)
        if text is not None:
            return text

        _die(
            "No PDF extractor available. Install `pdftotext` or `pypdf`, "
            "then retry."
        )

    _die(f"Unsupported format: {input_format}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Extract transcript text from PDF/TXT/MD into a normalized UTF-8 text file."
    )
    parser.add_argument("--input", required=True, help="Input transcript path")
    parser.add_argument("--output", required=True, help="Output text file path")
    parser.add_argument(
        "--language",
        default="fr",
        help="Language hint metadata (default: fr).",
    )
    parser.add_argument(
        "--format",
        default="auto",
        choices=sorted(ALLOWED_FORMATS),
        help="Input format (auto|pdf|txt|md).",
    )
    args = parser.parse_args()

    input_path = Path(args.input).expanduser().resolve()
    output_path = Path(args.output).expanduser().resolve()

    if not input_path.exists():
        _die(f"Input file not found: {input_path}")
    if not input_path.is_file():
        _die(f"Input path is not a file: {input_path}")

    input_format = _detect_format(input_path, args.format)
    raw = _extract_text(input_path, input_format)
    normalized = _normalize_text(raw)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(normalized, encoding="utf-8")

    line_count = normalized.count("\n")
    word_count = len(normalized.split())
    print(
        f"[OK] Extracted transcript | format={input_format} | language={args.language} "
        f"| lines={line_count} | words={word_count} | output={output_path}",
        file=sys.stderr,
    )


if __name__ == "__main__":
    main()
