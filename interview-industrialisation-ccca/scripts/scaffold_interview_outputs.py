#!/usr/bin/env python3
"""Create semi-automatic interview scaffolds with ambiguity checks.

Preview mode prints inferred metadata and uncertain fields.
Confirm mode writes:
- 01_interviews/<INTERVIEW_ID>.txt
- 01_interviews/<INTERVIEW_ID>.json
- 01_interviews/<INTERVIEW_ID>.md
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import unicodedata
from datetime import datetime
from pathlib import Path
from typing import Iterable

ROLE_MAP = {
    "ce": "CE",
    "ca": "CA",
    "support": "SUPPORT",
    "prevot": "PREVOT",
    "crc": "CRC",
    "production": "PRODUCTION",
    "dir": "DIR",
}

SITE_MAP = {
    "nimes": "NIMES",
    "nime": "NIMES",
    "toulouse": "TOULOUS",
    "toulous": "TOULOUS",
    "montpellier": "MONTPEL",
    "montpel": "MONTPEL",
    "colomiers": "COLOMIE",
    "colomie": "COLOMIE",
    "albi": "ALBI",
    "rodez": "RODEZ",
    "montauban": "MONTAUB",
    "eauze": "EAUZE",
    "baillargues": "BAILLAR",
}

CORE_QUESTIONS = [
    ("Q00", "Consentement, usage des donnees, rappel confidentialite."),
    ("Q00B", "Validation metadonnees (site, role, perimetre exact)."),
    ("Q01", "Mission reelle du poste aujourd'hui (et part du temps par activite)."),
    ("Q02", "Objectifs 2026 attendus sur votre perimetre (chiffres si possible)."),
    ("Q03", "Processus actuel de bout en bout (etapes, outils, handoffs)."),
    ("Q04", "Ou le flux casse le plus souvent, et pourquoi."),
    ("Q05", "KPI reellement suivis aujourd'hui (definition + frequence + source)."),
    ("Q06", "Irritants majeurs (3 max) et cout operationnel associe."),
    ("Q07", "Risque concret si rien ne change d'ici 3 a 6 mois."),
    ("Q08", "Priorites sur les 4 axes contractuels."),
    ("Q09", "Quick wins realisables en 30 jours (preuves attendues)."),
    ("Q10", "Plan d'execution J15/J30/J60/J90 (actions + owners)."),
    ("Q11", "Ce qui aiderait a passer de cueillette a chasse organisee."),
    ("Q12", "Pieces/faits disponibles pour prouver le diagnostic."),
]

MODULE_QUESTIONS = {
    "CE": [
        ("CE01", "Prospection proactive: volume, cadence, qualite de ciblage."),
        ("CE02", "Promesses d'embauche: creation, conversion, causes d'echec."),
        ("CE03", "Objections entreprises: top 3 + tactiques actuelles."),
        ("CE04", "Conditions concretes pour accelerer le closing."),
    ],
    "CA": [
        ("CA01", "Sourcing jeunes: canaux performants vs faibles."),
        ("CA02", "Accompagnement candidats: points de rupture."),
        ("CA03", "Abandons: causes, moment de rupture, prevention."),
        ("CA04", "Coordination CE/CA: handoff et responsabilites."),
    ],
    "SUPPORT": [
        ("SU01", "Qualite de saisie et fiabilite de donnees."),
        ("SU02", "Delais administratifs qui ralentissent le flux."),
        ("SU03", "Points de rupture recurrents (documents, validations, relances)."),
        ("SU04", "Standard minimal pour fiabiliser."),
    ],
    "PREVOT": [
        ("PR01", "Prescription metiers: pratiques qui fonctionnent."),
        ("PR02", "Orientation jeunes en metiers tension."),
        ("PR03", "Influence locale: freins et leviers."),
        ("PR04", "Actions concretement activables en 30 jours."),
    ],
    "CRC": [
        ("CR01", "Generation leads: volume, qualite, regularite."),
        ("CR02", "Qualite des leads transmis aux conseillers."),
        ("CR03", "Taux d'exploitation reel des leads transmis."),
        ("CR04", "Campagnes prioritaires et conditions de succes."),
    ],
    "PRODUCTION": [
        ("PD01", "Interface commercial/production: frictions principales."),
        ("PD02", "Capacite et contraintes d'execution."),
        ("PD03", "Informations critiques manquantes cote commercial."),
        ("PD04", "Regles simples pour fluidifier le passage."),
    ],
    "DIR": [
        ("DI01", "Arbitrages critiques et criteres de priorisation."),
        ("DI02", "Gouvernance et escalade (qui decide quoi, quand)."),
        ("DI03", "KPI de direction reellement utilises en decision."),
        ("DI04", "Seuils d'alerte et mecanisme de correction rapide."),
    ],
}

CLOSURE_QUESTIONS = [
    ("QC1", "Reformulation des 3 points cles valides."),
    ("QC2", "Liste des elements manquants a transmettre + date."),
    ("QC3", "Validation des 2 priorites immediates."),
]



def normalize(text: str) -> str:
    value = "" if text is None else str(text)
    value = "".join(ch for ch in unicodedata.normalize("NFD", value) if unicodedata.category(ch) != "Mn")
    return value.lower()


def tokenize_filename(stem: str) -> list[str]:
    raw = re.split(r"[_\-\s]+", stem)
    return [tok for tok in raw if tok]


def parse_date_from_tokens(tokens: Iterable[str]) -> tuple[str | None, bool]:
    for tok in tokens:
        if re.fullmatch(r"\d{8}", tok):
            if tok.startswith("20"):
                # yyyymmdd
                dt = datetime.strptime(tok, "%Y%m%d")
                return dt.strftime("%Y-%m-%d"), False
            # ddmmyyyy
            dt = datetime.strptime(tok, "%d%m%Y")
            return dt.strftime("%Y-%m-%d"), False
    return None, True


def detect_role(tokens: Iterable[str]) -> tuple[str | None, bool]:
    for tok in tokens:
        key = normalize(tok)
        if key in ROLE_MAP:
            return ROLE_MAP[key], False
    return None, True


def detect_site(tokens: Iterable[str]) -> tuple[str | None, bool]:
    for tok in tokens:
        key = normalize(tok)
        if key in SITE_MAP:
            return SITE_MAP[key], False
    return None, True


def detect_participant(tokens: list[str], role: str | None, site: str | None) -> tuple[str | None, bool]:
    filtered = []
    normalized_role = normalize(role) if role else ""
    normalized_site = normalize(site) if site else ""

    for tok in tokens:
        key = normalize(tok)
        if key in ROLE_MAP:
            continue
        if key in SITE_MAP:
            continue
        if re.fullmatch(r"\d{8}", tok):
            continue
        if key in {"coaching", "entretien", "interview"}:
            continue
        if key == normalized_role or key == normalized_site:
            continue
        filtered.append(tok)

    if not filtered:
        return None, True

    participant = " ".join(filtered).replace("  ", " ").strip()
    participant = " ".join(p.capitalize() for p in participant.split())
    uncertain = len(filtered) < 2
    return participant, uncertain


def compute_initials(participant_name: str | None) -> tuple[str | None, bool]:
    if not participant_name:
        return None, True
    parts = [p for p in re.split(r"\s+", participant_name.strip()) if p]
    if len(parts) >= 2:
        return (parts[0][0] + parts[-1][0]).upper(), False
    if len(parts) == 1 and len(parts[0]) >= 2:
        return parts[0][:2].upper(), True
    return None, True


def build_interview_id(date_value: str, site: str, role: str, initials: str) -> str:
    return f"INT_{date_value.replace('-', '')}_{site}_{role}_{initials}"


def ensure_extracted_text(pdf_path: Path, force: bool = False) -> Path:
    output_path = pdf_path.with_name(f"{pdf_path.stem}_extracted.txt")
    if output_path.exists() and not force:
        return output_path
    cmd = ["pdftotext", "-layout", str(pdf_path), str(output_path)]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        stderr = (result.stderr or "").strip()
        raise RuntimeError(f"pdftotext failed: {stderr}")
    return output_path


def make_json_payload(interview_id: str, date_value: str, site: str, role: str, participant_name: str, interviewer: str) -> dict:
    questions = []
    for code, question in CORE_QUESTIONS + MODULE_QUESTIONS[role] + CLOSURE_QUESTIONS:
        questions.append(
            {
                "code": code,
                "question": question,
                "answer": "",
                "evidence": [],
                "kpi_mentions": [],
            }
        )

    return {
        "interview_id": interview_id,
        "date": date_value,
        "site": site,
        "role": role,
        "participant_nom": participant_name,
        "interviewer": interviewer,
        "duree_minutes": 45,
        "questions": questions,
        "module": role,
        "risques_statu_quo": [],
        "quick_wins_30j": [],
        "actions_j15_j30_j60_j90": [
            {"horizon": "J15", "action": "", "owner": ""},
            {"horizon": "J30", "action": "", "owner": ""},
            {"horizon": "J60", "action": "", "owner": ""},
            {"horizon": "J90", "action": "", "owner": ""},
        ],
        "axes_contrat": {
            "sourcing_novateur": "",
            "accompagnement_orientation": "",
            "optimisation_parcours_client": "",
            "optimisation_reseau_anciens": "",
        },
        "contradictions_detectees": [],
        "pieces_citees": [],
        "niveau_confiance": "moyen",
    }


def make_txt_payload(interview_id: str, date_value: str, site: str, role: str, participant_name: str, interviewer: str) -> str:
    module_codes = MODULE_QUESTIONS[role]

    lines = [
        "[METADONNEES]",
        f"interview_id: {interview_id}",
        f"date: {date_value}",
        f"site: {site}",
        f"role: {role}",
        f"participant_nom: {participant_name}",
        f"interviewer: {interviewer}",
        "duree_cible_minutes: 45",
        "",
        "[OUVERTURE]",
        "Q00 - Consentement / confidentialite:",
        "Q00b - Validation metadonnees:",
        "",
        "[TRONC COMMUN]",
    ]

    for code, label in CORE_QUESTIONS[2:]:
        lines.append(f"{code} - {label}")

    lines.extend(["", "[MODULE PROFIL]"])
    for code, _ in module_codes:
        lines.append(f"{code}:")

    lines.extend(
        [
            "",
            "[CLOTURE]",
            "QC1 - 3 points cles valides:",
            "QC2 - Elements manquants + date:",
            "QC3 - 2 priorites immediates:",
            "",
            "[NOTES INTERVIEWEUR]",
            "- CONTRADICTION:",
            "- PARKING_LOT:",
            "- PREUVES_HORODATEES:",
            "",
        ]
    )

    return "\n".join(lines)


def make_md_payload(interview_id: str, date_value: str, site: str, role: str, participant_name: str, interviewer: str) -> str:
    return "\n".join(
        [
            f"# Compte rendu entretien - {interview_id}",
            "",
            "## Metadonnees",
            f"- Date: {date_value}",
            f"- Site: {site}",
            f"- Role: {role}",
            f"- Participant: {participant_name}",
            f"- Interviewer: {interviewer}",
            "- Duree:",
            "",
            "## Synthese executive (5 lignes max)",
            "-",
            "",
            "## Faits majeurs",
            "1.",
            "2.",
            "3.",
            "",
            "## Risques statu quo (3-6 mois)",
            "1.",
            "2.",
            "3.",
            "",
            "## Quick wins 30 jours",
            "1.",
            "2.",
            "3.",
            "",
            "## Plan d'action J15/J30/J60/J90",
            "- J15:",
            "- J30:",
            "- J60:",
            "- J90:",
            "",
            "## Contradictions detectees",
            "-",
            "",
            "## Pieces citees",
            "-",
            "",
            "## Niveau de confiance",
            "- faible / moyen / eleve",
            "",
        ]
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Preview and scaffold interview outputs with ambiguity checks")
    parser.add_argument("--pdf-path", required=True)
    parser.add_argument("--kit-root", default="transcriptions/interviews-industrialisees-2026")
    parser.add_argument("--language", default="fr")
    parser.add_argument("--participant-name")
    parser.add_argument("--site")
    parser.add_argument("--role", choices=sorted(set(ROLE_MAP.values())))
    parser.add_argument("--date")
    parser.add_argument("--initials")
    parser.add_argument("--interviewer", default="Laurent Serre")
    parser.add_argument("--confirm", action="store_true", help="Write output files")
    parser.add_argument("--allow-inferred", action="store_true", help="Allow uncertain metadata on confirm")
    parser.add_argument("--force", action="store_true", help="Overwrite output files if they exist")
    args = parser.parse_args()

    pdf_path = Path(args.pdf_path).expanduser().resolve()
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    kit_root = Path(args.kit_root).expanduser().resolve()
    interviews_dir = kit_root / "01_interviews"
    if not interviews_dir.exists():
        raise FileNotFoundError(f"Kit interviews directory not found: {interviews_dir}")

    tokens = tokenize_filename(pdf_path.stem)

    date_value, uncertain_date = (args.date, False) if args.date else parse_date_from_tokens(tokens)
    role_value, uncertain_role = (args.role, False) if args.role else detect_role(tokens)
    site_value, uncertain_site = (args.site, False) if args.site else detect_site(tokens)
    participant_value, uncertain_participant = (
        (args.participant_name, False) if args.participant_name else detect_participant(tokens, role_value, site_value)
    )
    initials_value, uncertain_initials = (args.initials, False) if args.initials else compute_initials(participant_value)

    uncertain_fields = []
    if uncertain_date or not date_value:
        uncertain_fields.append("date")
    if uncertain_site or not site_value:
        uncertain_fields.append("site")
    if uncertain_role or not role_value:
        uncertain_fields.append("role")
    if uncertain_participant or not participant_value:
        uncertain_fields.append("participant_name")
    if uncertain_initials or not initials_value:
        uncertain_fields.append("initials")

    candidate_interview_id = None
    if all([date_value, site_value, role_value, initials_value]):
        candidate_interview_id = build_interview_id(date_value, site_value, role_value, initials_value)

    preview = {
        "pdf_path": str(pdf_path),
        "kit_root": str(kit_root),
        "language": args.language,
        "detected": {
            "date": date_value,
            "site": site_value,
            "role": role_value,
            "participant_name": participant_value,
            "initials": initials_value,
            "interviewer": args.interviewer,
            "candidate_interview_id": candidate_interview_id,
        },
        "uncertain_fields": uncertain_fields,
        "status": "preview",
    }

    if not args.confirm:
        print(json.dumps(preview, ensure_ascii=True, indent=2))
        return 0

    if uncertain_fields and not args.allow_inferred:
        preview["status"] = "blocked_ambiguous"
        print(json.dumps(preview, ensure_ascii=True, indent=2))
        return 2

    if not candidate_interview_id:
        raise ValueError("Unable to build interview_id. Provide --date, --site, --role, and --initials.")

    extracted_path = ensure_extracted_text(pdf_path, force=args.force)

    txt_path = interviews_dir / f"{candidate_interview_id}.txt"
    json_path = interviews_dir / f"{candidate_interview_id}.json"
    md_path = interviews_dir / f"{candidate_interview_id}.md"

    for out in (txt_path, json_path, md_path):
        if out.exists() and not args.force:
            raise FileExistsError(f"Output already exists (use --force): {out}")

    txt_payload = make_txt_payload(candidate_interview_id, date_value, site_value, role_value, participant_value, args.interviewer)
    json_payload = make_json_payload(candidate_interview_id, date_value, site_value, role_value, participant_value, args.interviewer)
    md_payload = make_md_payload(candidate_interview_id, date_value, site_value, role_value, participant_value, args.interviewer)

    txt_path.write_text(txt_payload, encoding="utf-8")
    json_path.write_text(json.dumps(json_payload, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
    md_path.write_text(md_payload, encoding="utf-8")

    result = {
        "status": "written",
        "interview_id": candidate_interview_id,
        "files": {
            "extracted": str(extracted_path),
            "txt": str(txt_path),
            "json": str(json_path),
            "md": str(md_path),
        },
        "uncertain_fields": uncertain_fields,
    }
    print(json.dumps(result, ensure_ascii=True, indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:  # pragma: no cover
        print(json.dumps({"status": "error", "message": str(exc)}, ensure_ascii=True), file=sys.stderr)
        raise SystemExit(1)
