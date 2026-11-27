"""Regression tests for the other-links frontmatter of generated pages."""

import importlib.util
import sys
from pathlib import Path

import yaml

SPEC = importlib.util.spec_from_file_location(
    "generate_volumes", Path(__file__).parent.parent / "scripts" / "generate_volumes.py"
)
gv = importlib.util.module_from_spec(SPEC)
sys.modules["generate_volumes"] = gv
SPEC.loader.exec_module(gv)


def frontmatter_of(qmd: str) -> dict:
    return yaml.safe_load(qmd.split("---\n")[1])


def record(chapter, pdf_url=None, volume=1):
    return gv.Record(
        doi="10.21255/x",
        suffix="sgb-01.00-1",
        volume=volume,
        chapter=chapter,
        title="T",
        landing_url="https://emono.unibas.ch/x",
        pdf_url=pdf_url,
    )


def test_all_volumes_have_print_url():
    assert sorted(gv.PRINT_URLS) == list(range(1, 10))
    assert all(u.startswith("https://www.merianverlag.ch/produkt/") for u in gv.PRINT_URLS.values())


def test_volume_links():
    vol = record(None, volume=3)
    links = frontmatter_of(gv.volume_qmd(vol))["other-links"]
    assert [l["text"] for l in links] == [
        "Open-Access-Ausgabe (UB Basel)",
        "Druckausgabe (Christoph Merian Verlag)",
    ]
    assert links[0]["href"] == "https://emono.unibas.ch/x"
    assert links[1]["href"] == gv.PRINT_URLS[3]


def test_chapter_links_with_and_without_pdf():
    vol = record(None)
    with_pdf = frontmatter_of(gv.chapter_qmd(record(0, "https://emono.unibas.ch/pdf"), vol))
    assert [l["text"] for l in with_pdf["other-links"]][-1] == "PDF herunterladen"
    assert with_pdf["other-links"][1]["href"] == gv.PRINT_URLS[1]
    without = frontmatter_of(gv.chapter_qmd(record(0), vol))
    assert len(without["other-links"]) == 2
    assert "Verlagsseite (eMono)" not in gv.chapter_qmd(record(0), vol)
