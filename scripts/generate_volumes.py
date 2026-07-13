# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "httpx>=0.27",
#   "beautifulsoup4>=4.12",
#   "lxml>=5",
#   "pyyaml>=6",
# ]
# ///
"""Generate the volumes/ section from the Stadt.Geschichte.Basel DOI list.

Reads the DOI list from the sgb-minimal-html repository, fetches metadata
from DataCite, the minimal-HTML chapter editions from GitHub, and the galley
download links from emono.unibas.ch, then writes committed .qmd pages:

    volumes/index.qmd                       overview of all volumes
    volumes/band-0X/index.qmd               one page per volume
    volumes/band-0X/<doi-suffix>/index.qmd  one page per chapter

Usage:
    uv run scripts/generate_volumes.py            # all volumes (HTML from GitHub main)
    uv run scripts/generate_volumes.py --volume 3
    uv run scripts/generate_volumes.py --only 10.21255/sgb-03.01-669037
    uv run scripts/generate_volumes.py --source /path/to/sgb-minimal-html  # local html/
"""

from __future__ import annotations

import argparse
import re
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from urllib.parse import urljoin

import httpx
import yaml
from bs4 import BeautifulSoup

DOIS_URL = "https://raw.githubusercontent.com/Stadt-Geschichte-Basel/sgb-minimal-html/main/pdf/dois.txt"
DATACITE_API = "https://api.datacite.org/dois/"
MINIMAL_HTML_URL = "https://raw.githubusercontent.com/Stadt-Geschichte-Basel/sgb-minimal-html/main/html/volume-{volume:02d}/{suffix}.html"
LICENSE_LABELS = {"cc-by-nc-4.0": "CC BY-NC 4.0"}
LICENSE_URLS = {"cc-by-nc-4.0": "https://creativecommons.org/licenses/by-nc/4.0/"}
DEFAULT_LICENSE_URL = "https://creativecommons.org/licenses/by-nc/4.0/"
DOI_RE = re.compile(r"^10\.21255/(sgb-(\d{2})(?:\.(\d{2}))?-\d+)$")


@dataclass
class Creator:
    name: str  # "Family, Given"
    orcid: str | None
    is_editor: bool


@dataclass
class Record:
    doi: str
    suffix: str  # e.g. sgb-03.01-669037
    volume: int
    chapter: int | None  # None for volume records
    title: str = ""
    year: int = 0
    creators: list[Creator] = field(default_factory=list)
    license_id: str | None = None
    landing_url: str = ""
    pdf_url: str | None = None
    firstpage: str | None = None
    lastpage: str | None = None
    abstract: str | None = None
    body_html: str | None = None


def parse_doi(doi: str) -> tuple[str, int, int | None]:
    m = DOI_RE.match(doi.strip())
    if not m:
        raise ValueError(f"unexpected DOI shape: {doi}")
    suffix, vol, chap = m.group(1), int(m.group(2)), m.group(3)
    return suffix, vol, int(chap) if chap is not None else None


def get(client: httpx.Client, url: str) -> httpx.Response:
    for attempt in range(3):
        try:
            r = client.get(url)
            r.raise_for_status()
            return r
        except httpx.HTTPError:
            if attempt == 2:
                raise
            time.sleep(2 * (attempt + 1))
    raise AssertionError("unreachable")


def fetch_datacite(client: httpx.Client, rec: Record) -> None:
    attrs = get(client, DATACITE_API + rec.doi).json()["data"]["attributes"]
    rec.title = attrs["titles"][0]["title"].strip()
    # DataCite occasionally returns publicationYear as a string; keep it an int.
    rec.year = int(attrs["publicationYear"])
    rec.landing_url = attrs["url"]
    for c in attrs["creators"]:
        is_editor = c["name"].endswith(" (ed.)")
        if c.get("givenName") and c.get("familyName"):
            name = f"{c['givenName']} {c['familyName']}"
        else:
            name = c["name"].removesuffix(" (ed.)")
            if ", " in name:
                family, given = name.split(", ", 1)
                name = f"{given} {family}"
        orcid = None
        for ident in c.get("nameIdentifiers", []):
            if ident.get("nameIdentifierScheme") == "ORCID":
                # Some records carry stray whitespace inside the identifier.
                orcid = ident["nameIdentifier"].strip().rsplit("/", 1)[-1]
        rec.creators.append(Creator(name=name.strip(), orcid=orcid, is_editor=is_editor))
    for rights in attrs.get("rightsList", []):
        if rights.get("rightsIdentifier"):
            rec.license_id = rights["rightsIdentifier"]


def fetch_minimal_html(client: httpx.Client, rec: Record, source: Path | None = None) -> None:
    if source is not None:
        local = source / "html" / f"volume-{rec.volume:02d}" / f"{rec.suffix}.html"
        html = local.read_text(encoding="utf-8")
    else:
        html = get(client, MINIMAL_HTML_URL.format(volume=rec.volume, suffix=rec.suffix)).text
    soup = BeautifulSoup(html, "lxml")
    for name in ("citation_firstpage", "citation_lastpage"):
        meta = soup.find("meta", attrs={"name": name})
        if meta and meta.get("content"):
            setattr(rec, name.removeprefix("citation_"), meta["content"])
    body = soup.body
    if body is None:
        raise ValueError(f"no <body> in minimal HTML for {rec.doi}")
    if body.header:
        body.header.decompose()
    # A nested <main> would be invalid inside the theme's <main>; Quarto's
    # appendix supplies its own endnotes heading (see section-title-footnotes).
    if (main := body.main) is not None:
        main.name = "div"
        main["class"] = "sgb-chapter"
    endnotes = body.find("section", attrs={"role": "doc-endnotes"})
    if endnotes is not None and endnotes.h2 is not None:
        endnotes.h2.decompose()
    # Promote the chapter's lead paragraph to the `abstract:` metadata field so
    # Quarto renders it in the title block (labelled «Zusammenfassung») instead
    # of as an oversized paragraph at the top of the body.
    lead = body.find("p", class_="lead")
    if lead is not None:
        text = " ".join(lead.get_text().split())
        if text:
            rec.abstract = text
        lead.decompose()
    rec.body_html = "\n".join(
        child.decode() for child in body.children if child.name is not None
    ).strip()


PDF_HREF_RE = re.compile(r"href:\s*(\S+/catalog/download/\S+)")


def scrape_pdf_url(client: httpx.Client, rec: Record, out_root: Path) -> None:
    try:
        resp = get(client, rec.landing_url)
    except httpx.HTTPStatusError as exc:
        # emono landing pages occasionally 5xx transiently. A single flaky page
        # must not fail the whole run or silently drop a working download link,
        # so on a server error we keep the link already committed for this page.
        if exc.response.status_code >= 500:
            rec.pdf_url = existing_pdf_url(out_root, rec)
            note = f"reusing committed link ({rec.pdf_url})" if rec.pdf_url else "no PDF link"
            print(f"  emono {exc.response.status_code} for {rec.landing_url}; {note}", file=sys.stderr)
            return
        raise
    soup = BeautifulSoup(resp.text, "lxml")
    for a in soup.find_all("a", class_="cmp_download_link"):
        if a.get_text(strip=True) == "PDF" and a.get("href"):
            # Resolve relative hrefs against the landing page before rewriting.
            href = urljoin(rec.landing_url, a["href"])
            rec.pdf_url = href.replace("/catalog/view/", "/catalog/download/")
            return


def existing_pdf_url(out_root: Path, rec: Record) -> str | None:
    """PDF download link from the already-committed chapter page, if any."""
    page = out_root / f"band-{rec.volume:02d}" / rec.suffix / "index.qmd"
    if not page.exists():
        return None
    m = PDF_HREF_RE.search(page.read_text(encoding="utf-8"))
    return m.group(1) if m else None


def frontmatter(data: dict) -> str:
    dumped = yaml.safe_dump(
        data, sort_keys=False, allow_unicode=True, width=10_000, default_flow_style=False
    )
    return f"---\n{dumped}---\n"


def author_block(creators: list[Creator]) -> list[dict]:
    authors = []
    for c in creators:
        entry: dict = {"name": c.name}
        if c.orcid:
            entry["orcid"] = c.orcid
        authors.append(entry)
    return authors


def license_callout(rec: Record) -> str:
    label = LICENSE_LABELS.get(rec.license_id or "", rec.license_id)
    url = LICENSE_URLS.get(rec.license_id or "", DEFAULT_LICENSE_URL)
    return (
        '::: {.callout-tip title="Lizenz" icon="false" }\n'
        "© Stadt.Geschichte.Basel / Christoph Merian Verlag. "
        f"Text lizenziert unter [{label}]({url}). "
        f"Quelle: [doi.org/{rec.doi}](https://doi.org/{rec.doi})\n"
        ":::\n"
    )


def chapter_qmd(rec: Record, volume: Record) -> str:
    if rec.chapter == 0:
        blurb = f"Einleitung zu Band {rec.volume} «{volume.title}» von Stadt.Geschichte.Basel."
    else:
        blurb = f"Kapitel {rec.chapter} aus Band {rec.volume} «{volume.title}» von Stadt.Geschichte.Basel."
    citation: dict = {
        "type": "chapter",
        "title": rec.title,
        "container-title": volume.title,
    }
    if rec.firstpage and rec.lastpage:
        citation["page"] = f"{rec.firstpage}-{rec.lastpage}"
    citation.update(
        {
            "publisher": "Christoph Merian Verlag",
            "publisher-place": "Basel",
            "issued": rec.year,
            "url": f"https://doi.org/{rec.doi}",
        }
    )
    if volume.creators and all(c.is_editor for c in volume.creators):
        citation["editor"] = [c.name for c in volume.creators]
    fm: dict = {
        "title": rec.title,
        "description": blurb,
        "lang": "de",
        "categories": ["Kapitel"],
        "order": rec.chapter,
        "doi": rec.doi,
    }
    if rec.abstract:
        fm["abstract"] = rec.abstract
    if rec.license_id in LICENSE_LABELS:
        fm["license"] = LICENSE_LABELS[rec.license_id]
    fm["author"] = author_block(rec.creators)
    fm["citation"] = citation
    fm["appendix-cite-as"] = "display"
    other_links = [
        {"text": "Verlagsseite (eMono)", "icon": "book", "href": rec.landing_url}
    ]
    if rec.pdf_url:
        other_links.append(
            {"text": "PDF herunterladen", "icon": "filetype-pdf", "href": rec.pdf_url}
        )
    fm["other-links"] = other_links
    fm["language"] = {"section-title-footnotes": "Anmerkungen"}
    fm["date-modified"] = "last-modified"
    return (
        frontmatter(fm)
        + "\n"
        + license_callout(rec)
        + "\n"
        + "````{=html}\n"
        + (rec.body_html or "")
        + "\n````\n"
    )


def volume_qmd(rec: Record) -> str:
    citation: dict = {
        "type": "book",
        "title": rec.title,
        "publisher": "Christoph Merian Verlag",
        "publisher-place": "Basel",
        "issued": rec.year,
        "url": f"https://doi.org/{rec.doi}",
    }
    if rec.creators and all(c.is_editor for c in rec.creators):
        citation["editor"] = [c.name for c in rec.creators]
    fm: dict = {
        "title": rec.title,
        "subtitle": f"Stadt.Geschichte.Basel, Band {rec.volume}",
        "description": f"Band {rec.volume} der neunbändigen Buchreihe Stadt.Geschichte.Basel.",
        "lang": "de",
        "categories": ["Band"],
        "order": rec.volume,
        "doi": rec.doi,
    }
    if rec.license_id in LICENSE_LABELS:
        fm["license"] = LICENSE_LABELS[rec.license_id]
    fm["author"] = author_block(rec.creators)
    fm["citation"] = citation
    fm["appendix-cite-as"] = "display"
    fm["other-links"] = [
        {"text": "Verlagsseite (eMono)", "icon": "book", "href": rec.landing_url}
    ]
    fm["listing"] = [
        {
            "id": "chapters",
            "type": "table",
            "contents": ["sgb-*/index.qmd"],
            "sort": "order",
            "sort-ui": False,
            "filter-ui": False,
            "categories": False,
            "page-size": 100,
            "fields": ["title", "author"],
            "field-display-names": {"title": "Titel", "author": "Autor:innen"},
        }
    ]
    fm["date-modified"] = "last-modified"
    return (
        frontmatter(fm)
        + "\n"
        + license_callout(rec)
        + "\n## Kapitel\n\n::: {#chapters}\n:::\n"
    )


def root_index_qmd() -> str:
    fm = {
        "title": "Bände",
        "subtitle": "Die neunbändige Buchreihe Stadt.Geschichte.Basel",
        "description": "Alle neun Bände der Buchreihe Stadt.Geschichte.Basel mit sämtlichen Kapiteln als barrierearme HTML-Ausgaben.",
        "lang": "de",
        "listing": [
            {
                "id": "volumes",
                "type": "grid",
                "grid-columns": 3,
                "contents": ["band-*/index.qmd"],
                "sort": "order",
                "sort-ui": False,
                "filter-ui": False,
                "categories": False,
                "page-size": 9,
                "fields": ["title", "subtitle"],
            }
        ],
        "date-modified": "last-modified",
    }
    body = (
        "\nDie Buchreihe [Stadt.Geschichte.Basel](https://stadtgeschichtebasel.ch/) erzählt "
        "die Geschichte Basels von den ersten Spuren menschlichen Lebens bis in die Gegenwart. "
        "Alle Bände erscheinen im Christoph Merian Verlag und sind Open Access auf "
        "[emono.unibas.ch](https://emono.unibas.ch/stadtgeschichtebasel/catalog) publiziert "
        "([CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/)). "
        "Hier finden Sie sämtliche Kapitel als barrierearme, textbasierte HTML-Ausgaben "
        "mit Zitierhinweisen und Links zu den PDF-Fassungen.\n"
        "\n::: {#volumes}\n:::\n"
    )
    return frontmatter(fm) + body


def load_records(client: httpx.Client) -> list[Record]:
    records = []
    for line in get(client, DOIS_URL).text.splitlines():
        doi = line.strip()
        if not doi:
            continue
        suffix, vol, chap = parse_doi(doi)
        records.append(Record(doi=doi, suffix=suffix, volume=vol, chapter=chap))
    return records


def short_title(title: str) -> str:
    return title.split(".")[0].strip()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--volume", type=int, help="only generate this volume (1-9)")
    parser.add_argument("--only", help="only generate this chapter DOI")
    parser.add_argument("--out", default="volumes", help="output directory")
    parser.add_argument(
        "--source",
        type=Path,
        default=None,
        help="local sgb-minimal-html checkout to read html/ from instead of GitHub",
    )
    args = parser.parse_args()

    out_root = Path(args.out)
    with httpx.Client(timeout=30, follow_redirects=True) as client:
        records = load_records(client)
        volumes = {r.volume: r for r in records if r.chapter is None}
        chapters = [r for r in records if r.chapter is not None]

        if args.volume:
            chapters = [r for r in chapters if r.volume == args.volume]
            volumes = {args.volume: volumes[args.volume]}
        if args.only:
            chapters = [r for r in chapters if r.doi == args.only]
            volumes = {r.volume: volumes[r.volume] for r in chapters}

        for vol in volumes.values():
            fetch_datacite(client, vol)
        for i, rec in enumerate(chapters, 1):
            print(f"[{i}/{len(chapters)}] {rec.doi}", file=sys.stderr)
            fetch_datacite(client, rec)
            fetch_minimal_html(client, rec, source=args.source)
            scrape_pdf_url(client, rec, out_root)

    for rec in chapters:
        page_dir = out_root / f"band-{rec.volume:02d}" / rec.suffix
        page_dir.mkdir(parents=True, exist_ok=True)
        (page_dir / "index.qmd").write_text(
            chapter_qmd(rec, volumes[rec.volume]), encoding="utf-8"
        )
    for vol in volumes.values():
        page_dir = out_root / f"band-{vol.volume:02d}"
        page_dir.mkdir(parents=True, exist_ok=True)
        (page_dir / "index.qmd").write_text(volume_qmd(vol), encoding="utf-8")
    if not args.volume and not args.only:
        (out_root / "index.qmd").write_text(root_index_qmd(), encoding="utf-8")

    print("\nSidebar snippet for _quarto.yml:", file=sys.stderr)
    for v in sorted(volumes):
        print(
            f"          - text: 'Band {v}: {short_title(volumes[v].title)}'\n"
            f"            href: volumes/band-{v:02d}/index.qmd",
            file=sys.stderr,
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
