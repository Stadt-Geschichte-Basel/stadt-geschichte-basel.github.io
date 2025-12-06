#!/usr/bin/env python3
"""
Script to populate talk metadata from Zenodo record.

Usage:
    python3 populate_zenodo_talk.py 17751267 zenodo-17751267

This script fetches metadata from a Zenodo record and populates the template
index.qmd file with the correct information.
"""

import sys
import json
import urllib.request
import yaml
from pathlib import Path


def fetch_zenodo_metadata(record_id):
    """Fetch metadata from Zenodo API."""
    url = f"https://zenodo.org/api/records/{record_id}"
    try:
        with urllib.request.urlopen(url, timeout=30) as response:
            return json.loads(response.read().decode())
    except Exception as e:
        print(f"Error fetching metadata: {e}", file=sys.stderr)
        return None


def format_authors(creators):
    """Format authors for Quarto YAML."""
    authors = []
    for creator in creators:
        author = {
            "name": creator.get("name", ""),
        }
        if "orcid" in creator:
            author["orcid"] = creator["orcid"]
        if "affiliation" in creator:
            author["affiliation"] = creator["affiliation"]
        authors.append(author)
    return authors


def populate_template(metadata, directory_name):
    """Populate the index.qmd template with Zenodo metadata."""
    md = metadata.get("metadata", {})
    
    title = md.get("title", "")
    description = md.get("description", "")
    creators = md.get("creators", [])
    publication_date = md.get("publication_date", "")
    doi = md.get("doi", "")
    
    # Format authors using the helper function
    authors = format_authors(creators)
    
    # Build YAML frontmatter using yaml library for safety
    frontmatter = {
        "title": title,
        "author": authors,
        "date": publication_date,
        "doi": doi,
        "categories": "Vortrag",
        "event": "TODO - Add event name",
        "lang": "de",
        "bibliography": "references.bib",
        "nocite": "@*",
        "citation": {
            "type": "standard",
            "title": title,
            "container-title": "TODO - Add container title (event/conference name)"
        },
        "appendix-cite-as": "display",
        "other-links": [
            {
                "text": "Slides (Zenodo)",
                "icon": "filetype-pdf",
                "href": f"https://doi.org/{doi}"
            }
        ]
    }
    
    # Generate YAML frontmatter
    yaml_str = yaml.dump(frontmatter, default_flow_style=False, allow_unicode=True, sort_keys=False)
    
    # Create the complete content with YAML frontmatter and body
    content = f"""---
{yaml_str}---

## Vortrag

{description}

::: {{.callout-tip title="Präsentation anzeigen (Vorschau)" icon="false" collapse="true"}}
Diese Ansicht zeigt eine komprimierte Vorschau der Präsentation. Die hochaufgelösten Original-Slides sind [auf Zenodo verfügbar](https://doi.org/{doi}).

<!-- TODO: Add iframe with PDF if available -->
:::
"""
    
    # Write to file
    base_path = Path("products/talks-posters") / directory_name
    index_path = base_path / "index.qmd"
    
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(content)
    
    print(f"✓ Updated {index_path}")
    print("\nRemaining TODOs:")
    print("- Add event name")
    print("- Add container title for citation")
    print("- Add PDF file to /assets/files/ if available")
    print("- Update other-links with event website if applicable")
    print("- Consider renaming directory to something more descriptive")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 populate_zenodo_talk.py RECORD_ID DIRECTORY_NAME")
        print("Example: python3 populate_zenodo_talk.py 17751267 zenodo-17751267")
        sys.exit(1)
    
    record_id = sys.argv[1]
    directory_name = sys.argv[2]
    
    print(f"Fetching metadata for Zenodo record {record_id}...")
    metadata = fetch_zenodo_metadata(record_id)
    
    if metadata:
        populate_template(metadata, directory_name)
    else:
        print("Failed to fetch metadata. Please check the record ID and try again.")
        sys.exit(1)
