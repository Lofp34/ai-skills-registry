#!/usr/bin/env python3
"""
Centralize Gmail emails by project from contacts.csv.

Outputs:
- Readable format: Markdown per message
- LLM-friendly format: JSON per message
- Direct classification by project folder
- Message subfolders by interlocutor (messages/<interlocutor>/)

Default time window: last 6 months (sliding).
"""

from __future__ import annotations

import argparse
import base64
import csv
from dataclasses import dataclass, field
from datetime import date, datetime, timezone
from email.utils import getaddresses
import json
from pathlib import Path
import re
import shutil
import sys
import time
import unicodedata
from typing import Dict, Iterable, List, Set, Tuple


SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

PUBLIC_EMAIL_DOMAINS = {
    "gmail.com",
    "googlemail.com",
    "hotmail.com",
    "outlook.com",
    "live.com",
    "msn.com",
    "icloud.com",
    "me.com",
    "yahoo.com",
    "yahoo.fr",
    "proton.me",
    "protonmail.com",
    "mailo.com",
    "orange.fr",
    "wanadoo.fr",
    "free.fr",
    "laposte.net",
    "gmx.com",
}

NAME_STOPWORDS = {
    "a",
    "au",
    "aux",
    "de",
    "des",
    "du",
    "la",
    "le",
    "les",
    "et",
    "mr",
    "mme",
    "mlle",
    "madame",
    "monsieur",
    "dr",
    "team",
    "equipe",
    "service",
    "programme",
    "projet",
    "upvd",
    "incube",
    "universite",
    "univ",
}


@dataclass
class ProjectProfile:
    project_id: str
    nom_projet: str
    statut: str = ""
    exact_emails: Set[str] = field(default_factory=set)
    domains: Set[str] = field(default_factory=set)
    query_names: Set[str] = field(default_factory=set)
    contact_names_normalized: Set[str] = field(default_factory=set)
    contact_name_signatures: List[Set[str]] = field(default_factory=list)
    contacts: List[Dict[str, str]] = field(default_factory=list)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Centralize Gmail emails into project folders from contacts.csv.",
    )
    parser.add_argument("--contacts-file", default="contacts.csv", help="Path to contacts CSV.")
    parser.add_argument("--output-dir", default="emails", help="Output root directory.")
    parser.add_argument(
        "--client-secret",
        default="secrets/gmail_client_secret.json",
        help="OAuth client secret JSON path.",
    )
    parser.add_argument(
        "--token-file",
        default="secrets/gmail_read_token.json",
        help="OAuth token cache file for readonly scope.",
    )
    parser.add_argument("--months-back", type=int, default=6, help="Sliding window in months.")
    parser.add_argument(
        "--start-date",
        default="",
        help="Override start date in YYYY-MM-DD format (takes precedence over --months-back).",
    )
    parser.add_argument("--max-messages", type=int, default=2000, help="Max Gmail messages to scan.")
    parser.add_argument(
        "--gmail-query-mode",
        choices=["focused", "broad"],
        default="focused",
        help="Gmail prefilter mode: focused is faster and more precise.",
    )
    parser.add_argument(
        "--progress-every",
        type=int,
        default=25,
        help="Print progress every N scanned messages.",
    )
    parser.add_argument(
        "--progress-mode",
        choices=["auto", "bar", "log", "none"],
        default="auto",
        help="Progress display mode.",
    )
    parser.add_argument(
        "--progress-width",
        type=int,
        default=28,
        help="Width of the progress bar when progress-mode=bar.",
    )
    parser.add_argument(
        "--include-public-domains",
        action="store_true",
        help="Include public domains (gmail.com, outlook.com...) for domain expansion.",
    )
    parser.add_argument(
        "--name-match-mode",
        choices=["on", "off"],
        default="on",
        help="Enable matching by participant display names extracted from message headers.",
    )
    parser.add_argument(
        "--name-query-mode",
        choices=["on", "off"],
        default="on",
        help="Include contact names in Gmail prefilter queries.",
    )
    parser.add_argument(
        "--name-min-tokens",
        type=int,
        default=2,
        help="Minimum normalized token count required for name-based matching.",
    )
    parser.add_argument(
        "--download-attachments",
        action="store_true",
        default=False,
        help="Download attachments (disabled by default).",
    )
    parser.add_argument(
        "--no-download-attachments",
        action="store_false",
        dest="download_attachments",
        help="Disable attachment downloads.",
    )
    parser.add_argument(
        "--max-domain-projects",
        type=int,
        default=1,
        help="Skip domain-based matching when a domain maps to more than this many projects.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Authenticate, scan and show counters without writing files.",
    )
    return parser


def subtract_months(input_date: date, months: int) -> date:
    year = input_date.year
    month = input_date.month - months
    while month <= 0:
        year -= 1
        month += 12
    # Clamp to day=1 to keep Gmail query stable and predictable.
    return date(year, month, min(input_date.day, 28))


def parse_start_date(raw_value: str) -> date:
    value = (raw_value or "").strip()
    if not value:
        raise ValueError("start date is empty")
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError as exc:
        raise ValueError(
            f"Invalid --start-date value '{value}'. Expected format: YYYY-MM-DD."
        ) from exc


def slugify(value: str) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9]+", "-", value.strip().lower())
    cleaned = cleaned.strip("-")
    return cleaned or "project"


def norm_email(raw: str) -> str:
    return raw.strip().lower()


def normalize_text(raw: str) -> str:
    text = unicodedata.normalize("NFKD", raw or "")
    text = text.encode("ascii", "ignore").decode("ascii")
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def build_name_signature(normalized_name: str) -> Set[str]:
    tokens = [t for t in normalized_name.split() if len(t) >= 2 and t not in NAME_STOPWORDS]
    return set(tokens)


def email_domain(email_value: str) -> str:
    if "@" not in email_value:
        return ""
    return email_value.rsplit("@", 1)[-1].lower()


def load_contacts(
    contacts_file: Path,
    include_public_domains: bool,
    default_project_id: str = "P001",
    default_project_name: str = "General",
) -> Dict[str, ProjectProfile]:
    profiles: Dict[str, ProjectProfile] = {}
    with contacts_file.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            project_id = (row.get("project_id") or "").strip() or default_project_id
            nom_projet = (row.get("nom_projet") or "").strip() or default_project_name
            if project_id not in profiles:
                profiles[project_id] = ProjectProfile(
                    project_id=project_id,
                    nom_projet=nom_projet,
                )
            email_value = norm_email(row.get("email") or "")
            if "@" not in email_value:
                continue
            domain = email_domain(email_value)
            profile = profiles[project_id]
            profile.exact_emails.add(email_value)
            if include_public_domains or domain not in PUBLIC_EMAIL_DOMAINS:
                profile.domains.add(domain)
            contact_name = (row.get("porteur_nom") or "").strip()
            normalized_name = normalize_text(contact_name)
            if contact_name:
                profile.query_names.add(contact_name)
            if normalized_name:
                profile.contact_names_normalized.add(normalized_name)
                signature = build_name_signature(normalized_name)
                if signature and signature not in profile.contact_name_signatures:
                    profile.contact_name_signatures.append(signature)
            profile.contacts.append(
                {
                    "porteur_nom": contact_name,
                    "email": email_value,
                }
            )
    return profiles


def load_or_create_credentials(client_secret_file: Path, token_file: Path):
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow

    creds = None
    if token_file.exists():
        creds = Credentials.from_authorized_user_file(str(token_file), SCOPES)

    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    elif not creds or not creds.valid:
        if not client_secret_file.exists():
            raise FileNotFoundError(
                f"OAuth client secret not found at: {client_secret_file}\n"
                "Provide a valid OAuth desktop app client secret JSON."
            )
        flow = InstalledAppFlow.from_client_secrets_file(str(client_secret_file), SCOPES)
        try:
            creds = flow.run_local_server(port=0, open_browser=True)
        except Exception:
            creds = flow.run_console()

        token_file.parent.mkdir(parents=True, exist_ok=True)
        token_file.write_text(creds.to_json(), encoding="utf-8")

    return creds


def decode_part_data(data: str) -> str:
    if not data:
        return ""
    raw = base64.urlsafe_b64decode(data.encode("utf-8"))
    return raw.decode("utf-8", errors="replace")


def strip_html_basic(html_text: str) -> str:
    text = re.sub(r"(?is)<(script|style).*?>.*?</\1>", "", html_text)
    text = re.sub(r"(?is)<br\s*/?>", "\n", text)
    text = re.sub(r"(?is)</p>", "\n\n", text)
    text = re.sub(r"(?is)<.*?>", "", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def extract_text_body(payload: dict) -> str:
    plain_parts: List[str] = []
    html_parts: List[str] = []

    def walk(part: dict):
        mime = part.get("mimeType", "")
        body = part.get("body", {})
        data = body.get("data", "")

        if mime == "text/plain" and data:
            plain_parts.append(decode_part_data(data))
        elif mime == "text/html" and data:
            html_parts.append(decode_part_data(data))

        for child in part.get("parts", []) or []:
            walk(child)

    walk(payload)

    if plain_parts:
        return "\n".join(p.strip() for p in plain_parts if p.strip()).strip()
    if html_parts:
        merged = "\n".join(p for p in html_parts if p)
        return strip_html_basic(merged)
    return ""


def extract_headers(payload: dict) -> Dict[str, str]:
    headers = {}
    for h in payload.get("headers", []) or []:
        name = (h.get("name") or "").strip().lower()
        value = (h.get("value") or "").strip()
        if name:
            headers[name] = value
    return headers


def build_interlocutor_slug(porteur_nom: str, email_value: str) -> str:
    if porteur_nom.strip():
        return slugify(porteur_nom)
    if email_value.strip():
        return slugify(email_value.split("@", 1)[0])
    return "non-attribue"


def detect_interlocutors(profile: ProjectProfile, addresses: Set[str]) -> List[Dict[str, str]]:
    matches: List[Dict[str, str]] = []
    seen_keys: Set[str] = set()

    for contact in profile.contacts:
        email_value = norm_email(contact.get("email", ""))
        if not email_value or email_value not in addresses:
            continue
        porteur_nom = (contact.get("porteur_nom") or "").strip()
        dedup_key = email_value or porteur_nom.lower()
        if dedup_key in seen_keys:
            continue
        seen_keys.add(dedup_key)
        matches.append(
            {
                "porteur_nom": porteur_nom,
                "email": email_value,
                "slug": build_interlocutor_slug(porteur_nom, email_value),
                "match_type": "contact_email",
            }
        )

    if matches:
        return matches

    return [
        {
            "porteur_nom": "Interlocuteur non attribue",
            "email": "",
            "slug": "non-attribue",
            "match_type": "fallback",
        }
    ]


def collect_message_identities(headers: Dict[str, str]) -> Tuple[Set[str], Set[str], List[Set[str]]]:
    fields = ["from", "to", "cc", "bcc", "reply-to", "delivered-to"]
    raw_values = [(headers.get(field, "") or "").strip() for field in fields]
    raw_values = [v for v in raw_values if v]
    parsed = getaddresses(raw_values)
    emails = {norm_email(addr) for _, addr in parsed if "@" in addr}
    addresses = {email for email in emails if email}

    normalized_names: Set[str] = set()
    participant_signatures: List[Set[str]] = []

    for display_name, addr in parsed:
        n = normalize_text(display_name or "")
        if n:
            normalized_names.add(n)
            sig = build_name_signature(n)
            if sig:
                participant_signatures.append(sig)

        # Fallback: infer a rough identity from local part when display name is absent.
        if addr and "@" in addr:
            local = addr.split("@", 1)[0].replace(".", " ").replace("_", " ").replace("-", " ")
            n_local = normalize_text(local)
            if n_local:
                normalized_names.add(n_local)
                sig_local = build_name_signature(n_local)
                if sig_local:
                    participant_signatures.append(sig_local)

    return addresses, normalized_names, participant_signatures


def compute_project_matches(
    addresses: Set[str],
    participant_names: Set[str],
    participant_name_signatures: List[Set[str]],
    profiles: Dict[str, ProjectProfile],
    domain_index: Dict[str, Set[str]],
    max_domain_projects: int,
    enable_name_match: bool,
    name_min_tokens: int,
) -> Tuple[List[Tuple[str, str]], int, int]:
    matches: List[Tuple[str, str]] = []
    matched_project_ids: Set[str] = set()
    ambiguous_domains_skipped = 0
    name_matches = 0

    for project_id, profile in profiles.items():
        if profile.exact_emails.intersection(addresses):
            matched_project_ids.add(project_id)
            matches.append((project_id, "exact_email"))

    addr_domains = {email_domain(a) for a in addresses if "@" in a}
    for domain in sorted(addr_domains):
        project_ids = domain_index.get(domain, set())
        if not project_ids:
            continue
        if len(project_ids) > max_domain_projects:
            ambiguous_domains_skipped += 1
            continue
        for project_id in sorted(project_ids):
            if project_id in matched_project_ids:
                continue
            matched_project_ids.add(project_id)
            matches.append((project_id, "domain_match"))

    if enable_name_match:
        for project_id, profile in profiles.items():
            if project_id in matched_project_ids:
                continue

            # Exact normalized display name match.
            if profile.contact_names_normalized.intersection(participant_names):
                matched_project_ids.add(project_id)
                matches.append((project_id, "name_match"))
                name_matches += 1
                continue

            # Token signature subset match.
            has_signature_match = False
            for signature in profile.contact_name_signatures:
                if len(signature) < name_min_tokens:
                    continue
                for participant_sig in participant_name_signatures:
                    if signature.issubset(participant_sig):
                        has_signature_match = True
                        break
                if has_signature_match:
                    break

            if has_signature_match:
                matched_project_ids.add(project_id)
                matches.append((project_id, "name_match"))
                name_matches += 1

    return matches, ambiguous_domains_skipped, name_matches


def parse_attachments(payload: dict) -> List[dict]:
    attachments: List[dict] = []

    def walk(part: dict):
        filename = (part.get("filename") or "").strip()
        body = part.get("body", {}) or {}
        attachment_id = body.get("attachmentId")
        if filename and attachment_id:
            attachments.append(
                {
                    "filename": filename,
                    "mimeType": part.get("mimeType", ""),
                    "attachmentId": attachment_id,
                    "size": body.get("size", 0),
                }
            )
        for child in part.get("parts", []) or []:
            walk(child)

    walk(payload)
    return attachments


def sanitize_filename(name: str) -> str:
    safe = re.sub(r"[^\w.\-() ]+", "_", name, flags=re.UNICODE)
    return safe[:180] if safe else "attachment.bin"


def msg_datetime_utc(internal_date_ms: str) -> datetime:
    ts = int(internal_date_ms) / 1000
    return datetime.fromtimestamp(ts, tz=timezone.utc)


def ensure_dir(path: Path):
    path.mkdir(parents=True, exist_ok=True)


def format_duration(seconds: float) -> str:
    seconds = max(int(seconds), 0)
    h, rem = divmod(seconds, 3600)
    m, s = divmod(rem, 60)
    if h > 0:
        return f"{h:02d}:{m:02d}:{s:02d}"
    return f"{m:02d}:{s:02d}"


def print_progress_bar(
    current: int,
    total: int,
    counters: Dict[str, int],
    started_at: float,
    width: int,
):
    if total <= 0:
        return
    elapsed = max(time.time() - started_at, 1e-6)
    ratio = min(max(current / total, 0.0), 1.0)
    filled = int(ratio * width)
    bar = "#" * filled + "-" * (width - filled)
    rate = current / elapsed
    eta = (total - current) / rate if rate > 0 else 0.0
    line = (
        f"\r[{bar}] {ratio * 100:6.2f}% {current}/{total} | "
        f"match={counters['matched_messages']} "
        f"name={counters.get('name_matches', 0)} "
        f"write={counters['written_messages']} "
        f"unmatch={counters['unmatched_messages']} | "
        f"{rate:4.1f}/s ETA {format_duration(eta)}"
    )
    print(line, end="", flush=True)
    if current >= total:
        print()


def write_message_files(
    project_dir: Path,
    message_payload: dict,
    metadata: dict,
    body_text: str,
    interlocutor_slug: str = "",
):
    messages_dir = project_dir / "messages"
    if interlocutor_slug:
        messages_dir = messages_dir / interlocutor_slug
    ensure_dir(messages_dir)

    msg_time = msg_datetime_utc(metadata["internalDate"])
    ts = msg_time.strftime("%Y%m%dT%H%M%SZ")
    msg_id = metadata["id"]
    base_name = f"{ts}_{msg_id}"

    json_path = messages_dir / f"{base_name}.json"
    md_path = messages_dir / f"{base_name}.md"

    record = {
        "gmail_id": metadata["id"],
        "thread_id": metadata.get("threadId", ""),
        "label_ids": metadata.get("labelIds", []),
        "internal_date_utc": msg_time.isoformat(),
        "headers": metadata["headers"],
        "addresses": sorted(metadata["addresses"]),
        "participant_names": metadata.get("participant_names", []),
        "match_reason": metadata["match_reason"],
        "snippet": metadata.get("snippet", ""),
        "body_text": body_text,
        "attachments": metadata.get("attachments", []),
        "interlocuteur": metadata.get("interlocuteur", {}),
    }
    json_path.write_text(json.dumps(record, indent=2, ensure_ascii=False), encoding="utf-8")

    subject = metadata["headers"].get("subject", "(Sans objet)")
    sender = metadata["headers"].get("from", "")
    to_line = metadata["headers"].get("to", "")
    md = [
        f"# {subject}",
        "",
        f"- Gmail ID: `{metadata['id']}`",
        f"- Thread ID: `{metadata.get('threadId', '')}`",
        f"- Date UTC: `{msg_time.isoformat()}`",
        f"- From: {sender}",
        f"- To: {to_line}",
        f"- Match: `{metadata['match_reason']}`",
        (
            f"- Interlocuteur: {metadata.get('interlocuteur', {}).get('porteur_nom', '')} "
            f"<{metadata.get('interlocuteur', {}).get('email', '')}>"
            if metadata.get("interlocuteur")
            else "- Interlocuteur: _(non attribue)_"
        ),
        "",
        "## Extrait",
        "",
        metadata.get("snippet", ""),
        "",
        "## Corps",
        "",
        body_text or "_(aucun texte extrait)_",
        "",
    ]
    if metadata.get("attachments"):
        md.append("## Pieces jointes")
        md.append("")
        for att in metadata["attachments"]:
            md.append(f"- {att.get('filename', '')} ({att.get('size', 0)} bytes)")
        md.append("")

    md_path.write_text("\n".join(md), encoding="utf-8")
    return json_path, md_path, base_name


def chunk_terms(terms: List[str], max_chars: int = 900) -> List[List[str]]:
    chunks: List[List[str]] = []
    current: List[str] = []
    current_len = 0
    for term in terms:
        added = len(term) + (4 if current else 0)  # " OR "
        if current and current_len + added > max_chars:
            chunks.append(current)
            current = [term]
            current_len = len(term)
        else:
            current.append(term)
            current_len += added
    if current:
        chunks.append(current)
    return chunks


def build_gmail_queries(
    start_date: date,
    tracked_addresses: List[str],
    query_domains: List[str],
    tracked_names: List[str],
    mode: str,
    name_query_enabled: bool,
) -> List[str]:
    after_clause = f"after:{start_date.strftime('%Y/%m/%d')}"
    if mode == "broad":
        return [after_clause]

    terms: List[str] = []
    for email_value in tracked_addresses:
        terms.extend(
            [
                f"from:{email_value}",
                f"to:{email_value}",
                f"cc:{email_value}",
                f"bcc:{email_value}",
            ]
        )
    for domain in query_domains:
        # Domain query is useful mostly for professional domains.
        terms.extend([f"from:{domain}", f"to:{domain}", f"cc:{domain}", f"bcc:{domain}"])

    if name_query_enabled:
        for raw_name in tracked_names:
            normalized = normalize_text(raw_name)
            signature = build_name_signature(normalized)
            if len(signature) < 2:
                continue
            safe_name = re.sub(r"[\"\\]", " ", raw_name).strip()
            if not safe_name:
                continue
            terms.extend([f'from:"{safe_name}"', f'to:"{safe_name}"'])

    if not terms:
        return [after_clause]

    queries: List[str] = []
    for chunk in chunk_terms(terms):
        queries.append(f"{after_clause} ({' OR '.join(chunk)})")
    return queries


def fetch_messages(service, queries: List[str], max_messages: int) -> List[dict]:
    out: List[dict] = []
    seen_ids: Set[str] = set()

    for query in queries:
        page_token = None
        while True:
            response = (
                service.users()
                .messages()
                .list(
                    userId="me",
                    q=query,
                    includeSpamTrash=False,
                    maxResults=min(500, max_messages - len(out)),
                    pageToken=page_token,
                )
                .execute()
            )
            for msg in response.get("messages", []):
                msg_id = msg.get("id")
                if not msg_id or msg_id in seen_ids:
                    continue
                seen_ids.add(msg_id)
                out.append(msg)
                if len(out) >= max_messages:
                    return out[:max_messages]

            page_token = response.get("nextPageToken")
            if not page_token:
                break
            if len(out) >= max_messages:
                return out[:max_messages]
    return out[:max_messages]


def download_attachment(service, msg_id: str, attachment_id: str) -> bytes:
    response = (
        service.users()
        .messages()
        .attachments()
        .get(userId="me", messageId=msg_id, id=attachment_id)
        .execute()
    )
    data = response.get("data", "")
    return base64.urlsafe_b64decode(data.encode("utf-8")) if data else b""


def build_project_dir(output_root: Path, profile: ProjectProfile) -> Path:
    name_slug = slugify(profile.nom_projet)
    return output_root / f"{profile.project_id}_{name_slug}"


def cleanup_legacy_message_layout(project_dir: Path) -> None:
    """Remove legacy sender folder and flat files at messages root."""
    senders_dir = project_dir / "senders"
    if senders_dir.exists() and senders_dir.is_dir():
        shutil.rmtree(senders_dir, ignore_errors=True)

    messages_root = project_dir / "messages"
    if not messages_root.exists() or not messages_root.is_dir():
        return

    for pattern in ("*.md", "*.json"):
        for path in messages_root.glob(pattern):
            try:
                path.unlink()
            except OSError:
                pass


def main():
    parser = build_parser()
    args = parser.parse_args()

    contacts_file = Path(args.contacts_file).resolve()
    output_root = Path(args.output_dir).resolve()
    client_secret_file = Path(args.client_secret).resolve()
    token_file = Path(args.token_file).resolve()

    if not contacts_file.exists():
        print(f"Missing contacts file: {contacts_file}", file=sys.stderr)
        sys.exit(2)

    profiles = load_contacts(contacts_file, args.include_public_domains)
    domain_index: Dict[str, Set[str]] = {}
    for project_id, profile in profiles.items():
        for domain in profile.domains:
            domain_index.setdefault(domain, set()).add(project_id)

    active_count = len(profiles)
    tracked_addresses = sorted({e for p in profiles.values() for e in p.exact_emails})
    tracked_domains = sorted({d for p in profiles.values() for d in p.domains})
    tracked_names = sorted({n for p in profiles.values() for n in p.query_names})
    if active_count == 0 or not tracked_addresses:
        print(
            "No usable contacts found in contacts.csv. "
            "Ensure at least one row has a valid email.",
            file=sys.stderr,
        )
        sys.exit(3)

    today = datetime.now(timezone.utc).date()
    if (args.start_date or "").strip():
        try:
            start_date = parse_start_date(args.start_date)
        except ValueError as exc:
            print(str(exc), file=sys.stderr)
            sys.exit(2)
    else:
        start_date = subtract_months(today, args.months_back)
    query_domains = sorted(
        [d for d in tracked_domains if len(domain_index.get(d, set())) <= args.max_domain_projects]
    )
    skipped_query_domains = sorted(
        [d for d in tracked_domains if len(domain_index.get(d, set())) > args.max_domain_projects]
    )
    queries = build_gmail_queries(
        start_date=start_date,
        tracked_addresses=tracked_addresses,
        query_domains=query_domains,
        tracked_names=tracked_names,
        mode=args.gmail_query_mode,
        name_query_enabled=(args.name_query_mode == "on"),
    )

    print(f"Active projects: {active_count}")
    print(f"Tracked exact emails: {len(tracked_addresses)}")
    print(f"Tracked domains: {len(tracked_domains)}")
    print(f"Tracked names: {len(tracked_names)}")
    print(f"Gmail query mode: {args.gmail_query_mode}")
    print(f"Name query mode: {args.name_query_mode}")
    print(f"Name match mode: {args.name_match_mode}")
    print(f"Gmail query count: {len(queries)}")
    print(f"Gmail query base: after:{start_date.strftime('%Y/%m/%d')}")
    if args.include_public_domains:
        print(
            "Warning: include-public-domains is enabled. "
            "This can significantly increase noise and processing time."
        )
    if skipped_query_domains:
        print(
            f"Skipped ambiguous domains in Gmail prefilter ({len(skipped_query_domains)}): "
            + ", ".join(skipped_query_domains)
        )
    if args.download_attachments:
        print("Attachments: enabled")
    else:
        print("Attachments: disabled")

    creds = load_or_create_credentials(client_secret_file, token_file)
    from googleapiclient.discovery import build

    service = build("gmail", "v1", credentials=creds)
    candidates = fetch_messages(service, queries, args.max_messages)
    print(f"Candidate messages (window): {len(candidates)}")

    if args.progress_mode == "auto":
        progress_mode = "bar" if sys.stdout.isatty() else "log"
    else:
        progress_mode = args.progress_mode
    print(f"Progress mode: {progress_mode}")

    counters = {
        "written_messages": 0,
        "matched_messages": 0,
        "unmatched_messages": 0,
        "attachments_downloaded": 0,
        "ambiguous_domain_hits_skipped": 0,
        "name_matches": 0,
    }
    project_summaries: Dict[str, dict] = {}
    project_interlocutor_summaries: Dict[str, Dict[str, dict]] = {}

    if not args.dry_run:
        ensure_dir(output_root)

    for profile in profiles.values():
        project_summaries[profile.project_id] = {
            "project_id": profile.project_id,
            "nom_projet": profile.nom_projet,
            "statut": profile.statut,
            "exact_emails": sorted(profile.exact_emails),
            "domains": sorted(profile.domains),
            "messages": 0,
        }
        project_interlocutor_summaries[profile.project_id] = {}

    total_candidates = len(candidates)
    started_at = time.time()
    for i, item in enumerate(candidates, start=1):
        msg_id = item.get("id")
        if not msg_id:
            counters["unmatched_messages"] += 1
        else:
            full = (
                service.users()
                .messages()
                .get(userId="me", id=msg_id, format="full")
                .execute()
            )
            payload = full.get("payload", {})
            headers = extract_headers(payload)
            addresses, participant_names, participant_name_signatures = collect_message_identities(headers)

            matches, skipped_ambiguous, name_matches = compute_project_matches(
                addresses,
                participant_names,
                participant_name_signatures,
                profiles,
                domain_index,
                args.max_domain_projects,
                enable_name_match=(args.name_match_mode == "on"),
                name_min_tokens=max(1, args.name_min_tokens),
            )
            counters["ambiguous_domain_hits_skipped"] += skipped_ambiguous
            counters["name_matches"] += name_matches
            if not matches:
                counters["unmatched_messages"] += 1
            else:
                counters["matched_messages"] += 1
                body_text = extract_text_body(payload)
                attachments = parse_attachments(payload)

                for project_id, match_reason in matches:
                    profile = profiles[project_id]
                    project_dir = build_project_dir(output_root, profile)
                    metadata = {
                        "id": full.get("id", ""),
                        "threadId": full.get("threadId", ""),
                        "labelIds": full.get("labelIds", []),
                        "internalDate": full.get("internalDate", "0"),
                        "snippet": full.get("snippet", ""),
                        "headers": headers,
                        "addresses": addresses,
                        "participant_names": sorted(participant_names),
                        "match_reason": match_reason,
                        "attachments": attachments,
                    }
                    interlocutors = detect_interlocutors(profile, addresses)
                    msg_time = msg_datetime_utc(metadata["internalDate"])
                    saved_attachments: List[str] = []

                    if not args.dry_run:
                        if args.download_attachments and attachments:
                            ts = msg_time.strftime("%Y%m%dT%H%M%SZ")
                            attachment_dir = project_dir / "attachments" / f"{ts}_{msg_id}"
                            ensure_dir(attachment_dir)
                            for att in attachments:
                                raw = download_attachment(service, msg_id, att["attachmentId"])
                                filename = sanitize_filename(att["filename"])
                                target = attachment_dir / filename
                                target.write_bytes(raw)
                                saved_attachments.append(str(target.relative_to(project_dir)))
                                counters["attachments_downloaded"] += 1

                    for interlocutor in interlocutors:
                        metadata_for_interlocutor = dict(metadata)
                        metadata_for_interlocutor["interlocuteur"] = interlocutor

                        if not args.dry_run:
                            json_path, md_path, _ = write_message_files(
                                project_dir,
                                full,
                                metadata_for_interlocutor,
                                body_text,
                                interlocutor_slug=interlocutor["slug"],
                            )
                            rel_md = str(md_path.relative_to(project_dir))
                            rel_json = str(json_path.relative_to(project_dir))

                            if saved_attachments:
                                record = json.loads(json_path.read_text(encoding="utf-8"))
                                record["attachment_paths"] = saved_attachments
                                json_path.write_text(
                                    json.dumps(record, indent=2, ensure_ascii=False),
                                    encoding="utf-8",
                                )

                            interlocutor_key = interlocutor.get("email") or interlocutor.get("slug", "non-attribue")
                            interlocutor_bucket = project_interlocutor_summaries[project_id].setdefault(
                                interlocutor_key,
                                {
                                    "porteur_nom": interlocutor.get("porteur_nom", ""),
                                    "email": interlocutor.get("email", ""),
                                    "slug": interlocutor.get("slug", "non-attribue"),
                                    "messages": [],
                                },
                            )
                            interlocutor_bucket["messages"].append(
                                {
                                    "gmail_id": metadata["id"],
                                    "thread_id": metadata.get("threadId", ""),
                                    "internal_date_utc": msg_time.isoformat(),
                                    "subject": headers.get("subject", "(Sans objet)"),
                                    "match_reason": match_reason,
                                    "message_md": rel_md,
                                    "message_json": rel_json,
                                }
                            )

                        counters["written_messages"] += 1

                    project_summaries[project_id]["messages"] += 1

        if progress_mode == "bar":
            print_progress_bar(
                current=i,
                total=total_candidates,
                counters=counters,
                started_at=started_at,
                width=max(10, args.progress_width),
            )
        elif progress_mode == "log":
            if args.progress_every > 0 and (i % args.progress_every == 0 or i == total_candidates):
                print(
                    f"[progress] scanned {i}/{total_candidates} | "
                    f"matched={counters['matched_messages']} | "
                    f"name={counters['name_matches']} | "
                    f"written={counters['written_messages']} | "
                    f"unmatched={counters['unmatched_messages']}"
                )

    if not args.dry_run:
        for project_id, summary in project_summaries.items():
            profile = profiles[project_id]
            project_dir = build_project_dir(output_root, profile)
            ensure_dir(project_dir)
            cleanup_legacy_message_layout(project_dir)
            messages_dir = project_dir / "messages"
            ensure_dir(messages_dir)
            interlocutor_buckets = list(project_interlocutor_summaries.get(project_id, {}).values())
            interlocutor_buckets.sort(
                key=lambda item: (
                    (item.get("porteur_nom") or "").lower(),
                    (item.get("email") or "").lower(),
                )
            )
            interlocutor_index_records: List[dict] = []

            for interlocutor_bucket in interlocutor_buckets:
                interlocutor_slug = interlocutor_bucket.get("slug", "non-attribue")
                interlocutor_messages = sorted(
                    interlocutor_bucket.get("messages", []),
                    key=lambda msg: msg.get("internal_date_utc", ""),
                )
                interlocutor_record = {
                    "porteur_nom": interlocutor_bucket.get("porteur_nom", ""),
                    "email": interlocutor_bucket.get("email", ""),
                    "slug": interlocutor_slug,
                    "messages_count": len(interlocutor_messages),
                    "messages": interlocutor_messages,
                }

                interlocutor_json_path = messages_dir / interlocutor_slug / "index.json"
                interlocutor_md_path = messages_dir / interlocutor_slug / "index.md"
                ensure_dir(interlocutor_json_path.parent)
                interlocutor_json_path.write_text(
                    json.dumps(interlocutor_record, indent=2, ensure_ascii=False),
                    encoding="utf-8",
                )

                interlocutor_label = interlocutor_record["porteur_nom"] or interlocutor_record["email"] or "Interlocuteur non attribue"
                md_lines = [
                    f"# Interlocuteur: {interlocutor_label}",
                    "",
                    f"- Email: {interlocutor_record['email'] or '(inconnu)'}",
                    f"- Messages: {interlocutor_record['messages_count']}",
                    "",
                    "## Messages",
                    "",
                ]
                for msg in interlocutor_messages:
                    md_lines.append(
                        "- "
                        f"{msg.get('internal_date_utc', '')} | "
                        f"{msg.get('subject', '(Sans objet)')} | "
                        f"{msg.get('message_md', '')}"
                    )
                md_lines.append("")
                interlocutor_md_path.write_text("\n".join(md_lines), encoding="utf-8")

                interlocutor_index_records.append(
                    {
                        "porteur_nom": interlocutor_record["porteur_nom"],
                        "email": interlocutor_record["email"],
                        "slug": interlocutor_record["slug"],
                        "messages_count": interlocutor_record["messages_count"],
                        "folder": f"messages/{interlocutor_record['slug']}",
                        "index_json": f"messages/{interlocutor_record['slug']}/index.json",
                        "index_md": f"messages/{interlocutor_record['slug']}/index.md",
                    }
                )

            (messages_dir / "index.json").write_text(
                json.dumps(interlocutor_index_records, indent=2, ensure_ascii=False),
                encoding="utf-8",
            )
            messages_index_lines = [
                f"# Interlocuteurs - {summary['project_id']} {summary['nom_projet']}",
                "",
                f"- Nombre d'interlocuteurs: {len(interlocutor_index_records)}",
                "",
                "## Liste",
                "",
            ]
            for interlocutor_item in interlocutor_index_records:
                interlocutor_label = (
                    interlocutor_item.get("porteur_nom")
                    or interlocutor_item.get("email")
                    or "Interlocuteur non attribue"
                )
                messages_index_lines.append(
                    "- "
                    f"{interlocutor_label} | "
                    f"{interlocutor_item.get('messages_count', 0)} messages | "
                    f"{interlocutor_item.get('folder', '')}"
                )
            messages_index_lines.append("")
            (messages_dir / "index.md").write_text("\n".join(messages_index_lines), encoding="utf-8")

            summary["interlocuteurs_count"] = len(interlocutor_index_records)
            summary["interlocuteurs"] = interlocutor_index_records

            index_json = project_dir / "index.json"
            index_md = project_dir / "index.md"
            index_json.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")

            lines = [
                f"# {summary['project_id']} - {summary['nom_projet']}",
                "",
                f"- Statut: {summary['statut']}",
                f"- Contacts suivis: {len(summary['exact_emails'])}",
                f"- Domaines suivis: {len(summary['domains'])}",
                f"- Messages classes: {summary['messages']}",
                f"- Interlocuteurs detectes: {summary.get('interlocuteurs_count', 0)}",
                "",
                "## Contacts suivis",
                "",
            ]
            for e in summary["exact_emails"]:
                lines.append(f"- {e}")
            lines.append("")
            if summary["domains"]:
                lines.append("## Domaines suivis")
                lines.append("")
                for d in summary["domains"]:
                    lines.append(f"- {d}")
                lines.append("")
            if summary.get("interlocuteurs"):
                lines.append("## Interlocuteurs")
                lines.append("")
                for interlocutor_item in summary["interlocuteurs"]:
                    interlocutor_label = (
                        interlocutor_item.get("porteur_nom")
                        or interlocutor_item.get("email")
                        or "Interlocuteur non attribue"
                    )
                    lines.append(
                        "- "
                        f"{interlocutor_label} "
                        f"({interlocutor_item.get('messages_count', 0)} messages) -> "
                        f"{interlocutor_item.get('folder', '')}"
                    )
                lines.append("")
            index_md.write_text("\n".join(lines), encoding="utf-8")

        summary_payload = {
            "generated_at_utc": datetime.now(timezone.utc).isoformat(),
            "window_start": start_date.isoformat(),
            "window_end": today.isoformat(),
            "months_back": args.months_back,
            "active_projects": active_count,
            "tracked_exact_emails": len(tracked_addresses),
            "tracked_domains": len(tracked_domains),
            "tracked_names": len(tracked_names),
            "name_match_mode": args.name_match_mode,
            "name_query_mode": args.name_query_mode,
            "max_messages": args.max_messages,
            "counters": counters,
            "projects": list(project_summaries.values()),
        }
        (output_root / "ingestion-summary.json").write_text(
            json.dumps(summary_payload, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

    print("----")
    print("Ingestion completed.")
    print(json.dumps(counters, indent=2, ensure_ascii=True))


if __name__ == "__main__":
    main()
