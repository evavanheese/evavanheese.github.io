"""
Fetch publications from the ORCID public API and write them to
src/data/publications.json in the format expected by papers.astro.

Fields produced per publication:
  title           - paper title
  link            - https://doi.org/<doi>  (or ORCID work page as fallback)
  authors         - comma-separated author names
  journal         - journal / container title
  time            - publication year
  abstract        - abstract text (empty string when not available in ORCID)
  is_preprint     - true when the work is a preprint / OSF report
  is_first_author - true when Eva van Heese is the first listed author
  doi             - normalised DOI for deduplication

Manual entries from src/data/publications-manual.json are merged in and
deduplicated by DOI and title so hand-curated records always win.
Preprints are suppressed when a published version with the same title exists.
"""

import json
import re
import sys
import time
import unicodedata
from pathlib import Path

import requests

ORCID_ID = "0000-0002-1954-5014"
BASE_URL = f"https://pub.orcid.org/v3.0/{ORCID_ID}"
HEADERS = {"Accept": "application/json"}
OUT_PATH = Path(__file__).parent.parent / "src" / "data" / "publications.json"
MANUAL_PATH = Path(__file__).parent.parent / "src" / "data" / "publications-manual.json"

BULK_SIZE = 50
REQUEST_DELAY = 1.0

# DOIs to exclude entirely (normalised: lowercase, no https://doi.org/ prefix)
BLOCKED_DOIS: set[str] = {
    "10.1101/2025.03.19.25324269",   # Precise perivascular space segmentation (HCP-Aging)
    "10.31222/osf.io/dc5ey_v1",      # ENIGMA open-science preprint, published in Aperture Neuro
    "10.1101/2024.11.04.24316690",   # Narcolepsy MRI clearance preprint, published in JSR
}

PREPRINT_DOI_PREFIXES = (
    "10.1101/",   # bioRxiv / medRxiv
    "10.31222/",  # OSF preprints
    "10.17605/",  # OSF.io
    "10.31234/",  # PsyArXiv
    "10.31219/",  # OSF preprints (older prefix)
)

PREPRINT_JOURNAL_KEYWORDS = (
    "biorxiv", "medrxiv", "preprint", "osf", "arxiv",
)

# Matches: Eva van Heese, Eva M. van Heese, E. van Heese, E.M. van Heese, E. M. van Heese
AUTHOR_PATTERN = re.compile(
    r"\bE(?:va)?\.?\s*M?\.?\s*van\s+Heese\b",
    re.IGNORECASE,
)


def normalise_doi(doi: str) -> str:
    return doi.replace("https://doi.org/", "").replace("http://doi.org/", "").lower().strip()


def normalise_title(title: str) -> str:
    """Normalise a title for fuzzy comparison: lowercase, strip punctuation and extra whitespace."""
    # Unicode normalisation handles non-standard hyphens, accents, etc.
    title = unicodedata.normalize("NFKD", title.lower().strip())
    # Remove all punctuation so hyphens, dashes, etc. don't cause mismatches
    title = re.sub(r"[^\w\s]", "", title)
    title = re.sub(r"\s+", " ", title).strip()
    return title


def detect_preprint(doi: str | None, journal: str) -> bool:
    if doi:
        doi_norm = normalise_doi(doi)
        if any(doi_norm.startswith(p) for p in PREPRINT_DOI_PREFIXES):
            return True
    return any(kw in journal.lower() for kw in PREPRINT_JOURNAL_KEYWORDS)


def detect_first_author(authors: str) -> bool:
    if not authors:
        return False
    first = authors.split(",")[0].strip()
    return bool(AUTHOR_PATTERN.search(first))


def get_all_put_codes() -> list[int]:
    response = requests.get(f"{BASE_URL}/works", headers=HEADERS, timeout=30)
    response.encoding = "utf-8"
    response.raise_for_status()
    data = response.json()
    put_codes: list[int] = []
    for group in data.get("group", []):
        for work_summary in group.get("work-summary", []):
            put_codes.append(work_summary["put-code"])
    return put_codes


def get_work_details_bulk(put_codes: list[int]) -> list[dict]:
    codes_str = ",".join(str(c) for c in put_codes)
    response = requests.get(f"{BASE_URL}/works/{codes_str}", headers=HEADERS, timeout=60)
    response.encoding = "utf-8"
    response.raise_for_status()
    return response.json().get("bulk", [])


def extract_doi(work: dict) -> str | None:
    ext_ids = ((work.get("external-ids") or {}).get("external-id") or [])
    for ext_id in ext_ids:
        if ext_id.get("external-id-type") == "doi":
            value = ext_id.get("external-id-value", "").strip()
            if value:
                return value
    return None


def extract_authors(work: dict) -> str:
    contributors = ((work.get("contributors") or {}).get("contributor") or [])
    names = [
        ((c.get("credit-name") or {}).get("value", "")).strip()
        for c in contributors
    ]
    names = [n for n in names if n]
    if names:
        return ", ".join(names)
    for line in (work.get("citation") or {}).get("citation-value", "").splitlines():
        if line.strip().lower().startswith("author"):
            return line.split("=", 1)[-1].strip().strip("{},")
    return ""


def build_publication(work: dict) -> dict | None:
    title_obj = work.get("title") or {}
    title = ((title_obj.get("title") or {}).get("value", "")).strip()
    if not title:
        return None

    doi = extract_doi(work)

    if doi and normalise_doi(doi) in BLOCKED_DOIS:
        print(f"  Skipping blocked: {title[:70]}")
        return None

    link = f"https://doi.org/{doi}" if doi else (
        f"https://orcid.org/{ORCID_ID}"
        + (f"#work-{work.get('put-code')}" if work.get("put-code") else "")
    )

    journal_title_obj = work.get("journal-title") or {}
    journal = (
        journal_title_obj.get("value", "").strip()
        if isinstance(journal_title_obj, dict)
        else str(journal_title_obj).strip()
    )

    pub_date = work.get("publication-date") or {}
    year_obj = pub_date.get("year") or {}
    time_str = (
        year_obj.get("value", "").strip()
        if isinstance(year_obj, dict)
        else str(year_obj).strip()
    )

    authors = extract_authors(work)

    return {
        "title": title,
        "link": link,
        "authors": authors,
        "journal": journal,
        "time": time_str,
        "abstract": (work.get("short-description") or "").strip(),
        "is_preprint": detect_preprint(doi, journal),
        "is_first_author": detect_first_author(authors),
        "shared_first_author": False,
        "doi": normalise_doi(doi) if doi else "",
        "type": None,
    }


def load_manual_publications() -> list[dict]:
    if not MANUAL_PATH.exists():
        return []
    with MANUAL_PATH.open(encoding="utf-8") as f:
        return json.load(f)


def suppress_duplicate_preprints(pubs: list[dict]) -> list[dict]:
    """Remove preprints when a published version with the same title exists."""
    published_titles = {
        normalise_title(p["title"])
        for p in pubs
        if not p.get("is_preprint")
    }
    before = len(pubs)
    pubs = [
        p for p in pubs
        if not p.get("is_preprint") or normalise_title(p["title"]) not in published_titles
    ]
    suppressed = before - len(pubs)
    if suppressed:
        print(f"  Suppressed {suppressed} preprint(s) with a published counterpart.")
    return pubs


def main() -> None:
    print(f"Fetching put-codes for ORCID {ORCID_ID} ...")
    put_codes = get_all_put_codes()
    print(f"  Found {len(put_codes)} works.")

    orcid_pubs: list[dict] = []
    for i in range(0, len(put_codes), BULK_SIZE):
        chunk = put_codes[i : i + BULK_SIZE]
        print(f"  Fetching details for works {i + 1}–{i + len(chunk)} ...")
        for item in get_work_details_bulk(chunk):
            pub = build_publication(item.get("work") or {})
            if pub:
                orcid_pubs.append(pub)
        if i + BULK_SIZE < len(put_codes):
            time.sleep(REQUEST_DELAY)

    # Manual entries win on deduplication by both DOI and normalised title
    manual = load_manual_publications()
    manual_dois = {normalise_doi(p.get("doi") or "") for p in manual if p.get("doi")}
    manual_titles = {normalise_title(p.get("title", "")) for p in manual}

    merged = [
        p for p in orcid_pubs
        if p.get("doi") not in manual_dois
        and normalise_title(p.get("title", "")) not in manual_titles
    ]
    merged.extend(manual)

    # Suppress preprints that have a published counterpart in the merged list
    merged = suppress_duplicate_preprints(merged)

    merged.sort(key=lambda p: p.get("time", "") or "", reverse=True)

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with OUT_PATH.open("w", encoding="utf-8") as f:
        json.dump(merged, f, indent=2, ensure_ascii=False)
        f.write("\n")

    print(f"Wrote {len(merged)} publications ({len(manual)} manual, {len(merged) - len(manual)} from ORCID)")


if __name__ == "__main__":
    try:
        main()
    except requests.HTTPError as exc:
        print(f"HTTP error: {exc}", file=sys.stderr)
        sys.exit(1)
