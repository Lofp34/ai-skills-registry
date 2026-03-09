#!/usr/bin/env python3
"""
Preflight validator for OpenAI transcription and chat payloads.

Use:
  python3 validate_transcription_stack.py --mode audio --payload payload-audio.json --file-size-bytes 28000000 --duration-seconds 95
  python3 validate_transcription_stack.py --mode chat --payload payload-chat.json
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

MAX_UPLOAD_BYTES = 25 * 1024 * 1024
SAFE_UPLOAD_BYTES = 24 * 1024 * 1024


def load_payload(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # pragma: no cover
        raise ValueError(f"Impossible de lire le payload JSON: {exc}") from exc


def add_issue(bucket: list[str], level: str, message: str) -> None:
    bucket.append(f"[{level}] {message}")


def validate_chat(payload: dict[str, Any], issues: list[str]) -> None:
    model = str(payload.get("model", "")).strip()
    if not model:
        add_issue(issues, "ERROR", "Le champ 'model' est manquant.")

    if "messages" not in payload:
        add_issue(issues, "ERROR", "Le champ 'messages' est manquant.")

    if model.startswith("gpt-5"):
        if "max_tokens" in payload:
            add_issue(
                issues,
                "ERROR",
                "gpt-5* utilise 'max_completion_tokens' et non 'max_tokens'.",
            )

        if "temperature" in payload and payload.get("temperature") != 1:
            add_issue(
                issues,
                "ERROR",
                "Temperature non supportee pour ce payload gpt-5* (garder la valeur par defaut).",
            )

    if "max_completion_tokens" not in payload and "max_tokens" not in payload:
        add_issue(
            issues,
            "WARN",
            "Aucune limite de tokens definie. Ajouter max_completion_tokens si besoin de controle cout/longueur.",
        )


def validate_audio(
    payload: dict[str, Any],
    issues: list[str],
    file_size_bytes: int | None,
    duration_seconds: float | None,
) -> None:
    model = str(payload.get("model", "")).strip()
    if not model:
        add_issue(issues, "ERROR", "Le champ 'model' est manquant.")

    supported = {
        "gpt-4o-transcribe",
        "gpt-4o-mini-transcribe",
        "gpt-4o-mini-transcribe-2025-12-15",
        "gpt-4o-transcribe-diarize",
        "whisper-1",
    }
    if model and model not in supported:
        add_issue(
            issues,
            "WARN",
            f"Modele non reconnu dans la matrice locale: {model}. Verifier la doc OpenAI a jour.",
        )

    if file_size_bytes is not None:
        if file_size_bytes > MAX_UPLOAD_BYTES:
            add_issue(
                issues,
                "ERROR",
                f"Taille fichier {file_size_bytes} > 25MB. Chunking requis.",
            )
        elif file_size_bytes > SAFE_UPLOAD_BYTES:
            add_issue(
                issues,
                "WARN",
                "Taille > 24MB. Risque eleve d echec. Preferer decoupage local.",
            )

    language = payload.get("language")
    if not language:
        add_issue(
            issues,
            "WARN",
            "Le champ 'language' est absent. Recommande pour precision et latence.",
        )

    response_format = payload.get("response_format")

    if model == "gpt-4o-transcribe-diarize":
        if response_format == "diarized_json":
            pass
        elif response_format in {"json", "text", None}:
            add_issue(
                issues,
                "WARN",
                "Pour obtenir les segments locuteurs, utiliser response_format='diarized_json'.",
            )
        else:
            add_issue(
                issues,
                "ERROR",
                f"response_format non compatible diarize: {response_format}.",
            )

        if "prompt" in payload:
            add_issue(
                issues,
                "WARN",
                "prompt non supporte avec gpt-4o-transcribe-diarize.",
            )

        include = payload.get("include")
        if isinstance(include, list) and any("logprobs" in str(item) for item in include):
            add_issue(
                issues,
                "WARN",
                "logprobs non supporte avec gpt-4o-transcribe-diarize.",
            )

        if "timestamp_granularities" in payload:
            add_issue(
                issues,
                "WARN",
                "timestamp_granularities non supporte avec gpt-4o-transcribe-diarize.",
            )

        if duration_seconds is not None and duration_seconds > 30 and "chunking_strategy" not in payload:
            add_issue(
                issues,
                "ERROR",
                "Audio > 30s avec diarize: ajouter chunking_strategy (auto recommande).",
            )

    if model in {"gpt-4o-transcribe", "gpt-4o-mini-transcribe", "gpt-4o-mini-transcribe-2025-12-15"}:
        if response_format == "diarized_json":
            add_issue(
                issues,
                "ERROR",
                "diarized_json reserve a gpt-4o-transcribe-diarize.",
            )


def main() -> int:
    parser = argparse.ArgumentParser(description="Valider les payloads transcription/chat OpenAI.")
    parser.add_argument("--mode", choices=["audio", "chat"], required=True)
    parser.add_argument("--payload", required=True, help="Chemin vers un JSON de payload.")
    parser.add_argument("--file-size-bytes", type=int, default=None)
    parser.add_argument("--duration-seconds", type=float, default=None)
    args = parser.parse_args()

    payload_path = Path(args.payload)
    if not payload_path.exists():
        print("[ERROR] Fichier payload introuvable.")
        return 2

    try:
        payload = load_payload(payload_path)
    except ValueError as exc:
        print(f"[ERROR] {exc}")
        return 2

    issues: list[str] = []
    if args.mode == "chat":
        validate_chat(payload, issues)
    else:
        validate_audio(payload, issues, args.file_size_bytes, args.duration_seconds)

    if not issues:
        print("[OK] Aucun probleme detecte.")
        return 0

    for line in issues:
        print(line)

    has_error = any(line.startswith("[ERROR]") for line in issues)
    return 1 if has_error else 0


if __name__ == "__main__":
    sys.exit(main())
