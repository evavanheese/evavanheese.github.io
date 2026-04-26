"""
Fetch publications from the ORCID public API and write them to
src/data/publications.json in the format expected by PublicationsList.astro.

Fields produced per publication:
  title    - paper title
  link     - https://doi.org/<doi>  (or ORCID work page as fallback)
  authors  - comma-separated author names
  journal  - journal / container title
  time     - publication year
  abstract - abstract text (empty string when not available in ORCID)
"""

import json
import sys
import time
from pathlib import Path

import requests

ORCID_ID = "0000-0002-1954-5014"
BASE_URL = f"https://pub.orcid.org/v3.0/{ORCID_ID}"
HEADERS = {"Accept": "application/json"}
OUT_PATH = Path(__file__).parent.parent / "src" / "data" / "publications.json"

# How many put-codes to fetch in one bulk request (ORCID max is 100)
BULK_SIZE = 50
# Polite delay between bulk requests (seconds)
REQUEST_DELAY = 1.0


def get_all_put_codes() -> list[int]:
    """Return a list of put-codes for all works on the profile."""
    url = f"{BASE_URL}/works"
    response = requests.get(url, headers=HEADERS, timeout=30)
    response.raise_for_status()
    data = response.json()

    put_codes: list[int] = []
    for group in data.get("group", []):
        for work_summary in group.get("work-summary", []):
            put_codes.append(work_summary["put-code"])
    return put_codes


def get_work_details_bulk(put_codes: list[int]) -> list[dict]:
    """Fetch full work records for a list of put-codes in one request."""
    codes_str = ",".join(str(c) for c in put_codes)
    url = f"{BASE_URL}/works/{codes_str}"
    response = requests.get(url, headers=HEADERS, timeout=60)
    response.raise_for_status()
    data = response.json()
    return data.get("bulk", [])


def extract_doi(work: dict) -> str | None:
    """Return the DOI from external identifiers, or None."""
    ext_ids = (
        work.get("external-ids", {}) or {}
    ).get("external-id", []) or []
    for ext_id in ext_ids:
        if ext_id.get("external-id-type") == "doi":
            value = ext_id.get("external-id-value", "").strip()
            if value:
                return value
    return None


def extract_authors(work: dict) -> str:
    """Return a comma-separated author string from contributor records."""
    contributors = (
        work.get("contributors", {}) or {}
    ).get("contributor", []) or []

    names: list[str] = []
    for contrib in contributors:
        credit_name = (
            (contrib.get("credit-name") or {}).get("value", "").strip()
        )
        if credit_name:
            names.append(credit_name)

    if names:
        return ", ".join(names)

    # Fallback: citation metadata sometimes has author info
    citation = work.get("citation") or {}
    citation_value = citation.get("citation-value", "")
    # Very rough BibTeX author extraction
    if "author" in citation_value.lower():
        for line in citation_value.splitlines():
            if line.strip().lower().startswith("author"):
                author_part = line.split("=", 1)[-1].strip().strip("{},")
                return author_part

    return ""


def extract_abstract(work: dict) -> str:
    """Return the short description / abstract, or empty string."""
    return (work.get("short-description") or "").strip()


def build_publication(work: dict) -> dict | None:
    """Convert a raw ORCID work record to a Publication object."""
    title_obj = work.get("title", {}) or {}
    title = (
        (title_obj.get("title") or {}).get("value", "").strip()
    )
    if not title:
        return None

    doi = extract_doi(work)
    if doi:
        link = f"https://doi.org/{doi}"
    else:
        put_code = work.get("put-code")
        link = f"https://orcid.org/{ORCID_ID}" + (
            f"#work-{put_code}" if put_code else ""
        )

    journal_title_obj = work.get("journal-title") or {}
    journal = journal_title_obj.get("value", "").strip() if isinstance(
        journal_title_obj, dict
    ) else str(journal_title_obj).strip()

    pub_date = work.get("publication-date") or {}
    year_obj = pub_date.get("year") or {}
    time_str = (
        year_obj.get("value", "").strip()
        if isinstance(year_obj, dict)
        else str(year_obj).strip()
    )

    authors = extract_authors(work)
    abstract = extract_abstract(work)

    return {
        "title": title,
        "link": link,
        "authors": authors,
        "journal": journal,
        "time": time_str,
        "abstract": abstract,
    }


def main() -> None:
    print(f"Fetching put-codes for ORCID {ORCID_ID} ...")
    put_codes = get_all_put_codes()
    print(f"  Found {len(put_codes)} works.")

    all_publications: list[dict] = []

    for i in range(0, len(put_codes), BULK_SIZE):
        chunk = put_codes[i : i + BULK_SIZE]
        print(f"  Fetching details for works {i + 1}-{i + len(chunk)} ...")
        bulk = get_work_details_bulk(chunk)
        for item in bulk:
            work = item.get("work") or {}
            pub = build_publication(work)
            if pub:
                all_publications.append(pub)
        if i + BULK_SIZE < len(put_codes):
            time.sleep(REQUEST_DELAY)

    # Sort newest first (works without a year sort to the end)
    all_publications.sort(key=lambda p: p.get("time", "") or "", reverse=True)

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with OUT_PATH.open("w", encoding="utf-8") as f:
        json.dump(all_publications, f, indent=2, ensure_ascii=False)
        f.write("\n")

    print(f"Wrote {len(all_publications)} publications to {OUT_PATH}")


if __name__ == "__main__":
    try:
        main()
    except requests.HTTPError as exc:
        print(f"HTTP error: {exc}", file=sys.stderr)
        sys.exit(1)
