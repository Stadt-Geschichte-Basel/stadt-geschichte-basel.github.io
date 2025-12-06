# Completion Guide for Zenodo Record 17751267

## Current Status

A template structure has been created for the talk associated with [Zenodo record 17751267](https://zenodo.org/records/17751267). The following files have been created:

- `index.qmd` - Template with all required YAML fields and TODO markers
- `references.bib` - Empty bibliography file ready for citations
- `populate_zenodo_talk.py` - Python script to automate metadata population
- `README.md` - Basic instructions
- This file - Comprehensive completion guide

## Quick Start (Recommended)

### Option 1: Automated Population

Run the Python script from the repository root to automatically fill most fields:

```bash
python3 products/talks-posters/zenodo-17751267/populate_zenodo_talk.py 17751267 zenodo-17751267
```

This will fetch and populate:

- Title
- Authors (with ORCID if available)
- Date
- Description/Abstract

### Option 2: Manual Population

Visit https://zenodo.org/records/17751267 and copy the following information into `index.qmd`:

1. **Title**: Copy from Zenodo's main title field
2. **Subtitle**: If present, add it; otherwise remove the line
3. **Author(s)**: For each author, add:
   ```yaml
   - name: Full Name
     email: email@address
     orcid: 0000-0000-0000-0000 # if available
     affiliation: Institution Name
   ```
4. **Date**: Format as YYYY-MM-DD (e.g., 2025-11-15)
5. **Event**: The name of the conference/event where presented
6. **Abstract**: Copy from Zenodo's description field
7. **Citation container-title**: Usually the event name or conference proceedings

## Additional Steps

### 1. Add Event Links

In the `other-links` section of `index.qmd`, add relevant links:

```yaml
other-links:
  - text: Veranstaltungswebseite
    icon: house
    href: 'URL_TO_EVENT_WEBSITE'
  - text: Konferenzprogramm
    icon: calendar4-range
    href: 'URL_TO_PROGRAM'
  - text: Slides (Zenodo)
    icon: filetype-pdf
    href: 'https://doi.org/10.5281/zenodo.17751267'
```

### 2. Add PDF Slides (Optional but Recommended)

If you want to embed the presentation slides:

1. Download the PDF from Zenodo
2. Compress it if necessary (recommended for web display)
3. Place it in `/assets/files/` with a descriptive name (e.g., `YYMMDD-Author-Topic.pdf`)
4. Update the iframe in `index.qmd`:

```html
<iframe
	src="/assets/files/YOUR_FILE.pdf"
	width="100%"
	height="600px"
	loading="lazy"
	allowfullscreen
	title="TITLE_HERE"
>
	This browser does not support PDFs. Please
	<a href="/assets/files/YOUR_FILE.pdf">download the PDF</a> to view it.
</iframe>
```

### 3. Add References (If Applicable)

If the talk cites other works:

1. Export the BibTeX entry from Zenodo (click "Export" → "BibTeX")
2. Add it to `references.bib`
3. Add any other references cited in the talk

### 4. Rename Directory (Optional)

For consistency with other talks, consider renaming the directory to something more descriptive:

Examples from existing talks:

- `soda-forum` (event name)
- `c2dh-public-history` (venue + topic)
- `daschcon-2025` (event + year)

To rename:

```bash
git mv products/talks-posters/zenodo-17751267 products/talks-posters/NEW-NAME
```

## Testing

After completing the fields:

1. Preview the site:

   ```bash
   uv run quarto preview
   ```

2. Navigate to the Vorträge page to verify:
   - The talk appears in the listing
   - All metadata displays correctly
   - Links work properly
   - PDF embeds correctly (if added)

3. Check formatting:
   ```bash
   npm run format
   npm run check
   ```

## Verification Checklist

Before finalizing, ensure:

- [ ] All TODO markers removed from `index.qmd`
- [ ] Title and authors are correct
- [ ] Date is in YYYY-MM-DD format
- [ ] DOI is correct (10.5281/zenodo.17751267)
- [ ] Event name is filled in
- [ ] Citation block is complete
- [ ] At least one other-link besides Zenodo is added (if available)
- [ ] Abstract/description is present
- [ ] PDF is embedded (if available)
- [ ] References are added to `references.bib` (if applicable)
- [ ] Directory name is descriptive (optional)
- [ ] Site preview shows talk correctly
- [ ] All files are formatted (`npm run format`)

## Automatic Integration

Once the `index.qmd` file is complete, the talk will automatically appear in:

1. The Vorträge (Talks) listing on `/products/products.qmd#vorträge`
2. The site navigation
3. Search results

This happens because the `products.qmd` file has a listing configuration that automatically includes all files matching `talks-posters/*/index.qmd` with `categories: Vortrag`.

## Troubleshooting

### Talk doesn't appear in listing

- Check that `categories: Vortrag` is set correctly
- Ensure the `date` field is present and valid
- Run `uv run quarto render` to regenerate the site

### PDF doesn't embed

- Verify the PDF path is correct
- Check that the PDF is in `/assets/files/`
- Try opening the PDF directly in the browser

### Build errors

- Check YAML syntax (indentation matters!)
- Ensure all required fields are present
- Look for unclosed quotes or brackets

## Need Help?

- Check other talk examples in `products/talks-posters/`
- See the template: `docs/sample-index.qmd`
- Refer to repository documentation: `AGENTS.md`
- Ask in the GitHub issue: https://github.com/Stadt-Geschichte-Basel/stadt-geschichte-basel.github.io/issues/79
