# Completing the Zenodo Record 17751267 Talk Entry

This directory contains a template for the talk associated with Zenodo record 17751267.

## Automated Population (Recommended)

A Python script has been created to automatically populate most fields from Zenodo. To use it:

```bash
# Ensure PyYAML is installed (usually available in standard Python environments)
pip install pyyaml

# Run from the repository root directory
python3 products/talks-posters/zenodo-17751267/populate_zenodo_talk.py 17751267 zenodo-17751267
```

This will automatically fill in:

- Title
- Authors (with ORCID if available)
- Date
- DOI
- Description/Abstract

You'll still need to manually add:

- Event name
- Container title for citation
- Any additional links (event website, etc.)
- PDF file if you want to embed it

## Manual Completion

Alternatively, visit https://zenodo.org/records/17751267 and manually fill in the following information in `index.qmd`:

### Essential Fields

1. **Title**: The main title of the talk/presentation
2. **Subtitle**: If applicable
3. **Author(s)**: Name, email, ORCID, and affiliation for each author
4. **Date**: The date of the presentation (YYYY-MM-DD format)
5. **Event**: The name of the event/conference where the talk was presented
6. **Abstract**: A description of the talk content

### Optional Fields

7. **other-links**: Add relevant links (event website, program, etc.)
8. **PDF file**: If available, download from Zenodo and place in `/assets/files/` directory, then update the iframe reference
9. **references.bib**: Add any citations in BibTeX format

## Directory Naming

Once you have the information, you may want to rename this directory from `zenodo-17751267` to something more descriptive following the pattern of other talks (e.g., `event-name-topic`).

## Testing

After filling in the information, test the page by running:

```bash
uv run quarto preview
```

Then navigate to the talks page to see if it appears correctly in the listing.
