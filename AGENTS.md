# Agent Guidelines for stadt-geschichte-basel.github.io

This document provides guidance for AI agents (like GitHub Copilot, custom bots, or LLMs) working with this repository. Following these guidelines will improve the developer experience and ensure consistency across contributions.

## Repository Overview

This repository contains the documentation platform for Stadt.Geschichte.Basel, focusing on research data management (RDM) and public history. The project uses **Quarto** to build a documentation website from Markdown and QMD (Quarto Markdown) files.

**Key Information:**

- **Project Type**: Documentation website built with Quarto
- **Primary Languages**: Quarto Markdown (`.qmd`), R, Python, JavaScript
- **Deployment**: GitHub Pages (published to `https://dokumentation.stadtgeschichtebasel.ch/`)
- **Licenses**: Code (AGPL-3.0), Data/Content (CC BY 4.0)

## Purpose & Audience

- **Purpose**: Provide public-facing documentation of methods, guidelines, products, and activities of Stadt.Geschichte.Basel, with reproducible and citable outputs when appropriate.
- **Audience**: Researchers, cultural heritage professionals, educators, students, and partners. Content under `products/interna/` primarily serves internal workflows and team collaboration.
- **Publication**: Built with Quarto and deployed via GitHub Pages. Rendered output lives in `_site/`; cached, reproducible artifacts are stored in `_freeze/`.

## Technology Stack

### Core Technologies

- **Quarto**: Static site generator for scientific and technical publishing
- **R**: Statistical computing and data analysis (managed with `renv`)
- **Python**: Scripting and automation (managed with `uv`)
- **Node.js**: JavaScript tooling, linting, and formatting

### Package Managers

- **npm**: Node.js packages (`package.json`)
- **uv**: Python packages and virtual environments (`pyproject.toml`)
- **renv**: R packages (`renv.lock`)

## Repository Structure

The repository follows [The Turing Way's Advanced Structure for Data Analysis](https://book.the-turing-way.org/project-design/pd-overview/project-repo/project-repo-advanced/):

```text
├── assets/          # Images, figures, and other media files
├── docs/            # Documentation files and assets
├── products/        # Final products (reports, papers, presentations)
├── renv/            # R environment and package dependencies
├── _extensions/     # Quarto extensions (custom themes)
├── _quarto.yml      # Main Quarto configuration
├── *.qmd            # Quarto markdown content files
└── styles.css       # Custom CSS styles
```

### Content Architecture

- **Top-level pages**: `index.qmd`, `about.qmd`, `team.qmd` are public entry points without DOIs.
- **Products**: Under `products/` grouped by domain (e.g., `publications/`, `talks-posters/`, `research-data/`). These may be citable and often carry DOIs in YAML.
- **Interna**: `products/interna/` holds internal or process documentation; typically not citable and should not carry DOIs.
- **Build artifacts**: `_site/` (rendered site), `_freeze/` (cached outputs for reproducibility), `site_libs/` (client libs). Do not edit these by hand.

## Development Workflow

### Initial Setup

```bash
# Install Node.js dependencies
npm install

# Setup Python environment
uv sync

# Setup R environment
Rscript -e 'install.packages("renv"); renv::restore()'
```

### Common Commands

| Command                 | Description                               |
| ----------------------- | ----------------------------------------- |
| `npm run check`         | Check if all files are properly formatted |
| `npm run format`        | Auto-format all files with Prettier       |
| `npm run commit`        | Run commit message wizard (commitizen)    |
| `npm run changelog`     | Generate CHANGELOG.md                     |
| `uv run quarto preview` | Preview documentation locally             |
| `uv run quarto render`  | Build the documentation site              |
| `uv run quarto check`   | Check Quarto installation and setup       |

### Recommended Development Environment

**GitHub Codespaces** is the preferred development environment. It provides a pre-configured container with all necessary tools:

- Node.js with npm
- Python with uv
- R with renv
- Quarto

## Repository Conventions

### Commit Messages

This project uses [Conventional Commits](https://www.conventionalcommits.org/):

```text
<type>(<scope>): <description>

[optional body]

[optional footer]
```

**Types**: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`, `ci`

Use `npm run commit` to ensure proper formatting.

### Code Formatting

- **Prettier** is used for all file formatting
- Configuration: `.prettierrc`
- Always run `npm run format` before committing
- Pre-commit hooks enforce formatting (via Husky)

### File Naming

- Use lowercase with hyphens for file names: `my-document.qmd`
- Quarto files use `.qmd` extension for markdown with embedded code
- Standard markdown files use `.md` extension

## Multilingual Content

- **Default language**: German (`de`). Keep German as the baseline unless a page requires additional languages.
- **Page-level language**: Set `lang: de` (or `en`, etc.) in page YAML. Translate `title`, `description`, and other metadata per language.

## Accessibility Requirements

Ensure all content meets accessibility standards to make documentation usable for all audiences, including those using assistive technologies.

### Image Alt Text Requirements

**Every image must have descriptive alternative text** using the `fig-alt` attribute:

**Good example:**

```markdown
![Karte der jüdischen Gemeinden in Basel um 1910](assets/img/map-jewish-basel.png){fig-alt="Historische Karte von Basel mit farbig markierten Standorten jüdischer Einrichtungen: Synagoge (rot), Friedhof (grün), Vereinshäuser (blau) und Wohngebiete (gelb). Die Karte zeigt die Konzentration der Einrichtungen im Gundeldinger Quartier."}
```

**What makes good alt text:**

- Describe the content and function of the image
- Convey the same information as the image
- Be concise but complete (aim for 1-2 sentences)
- For complex visualizations (charts, maps), describe the key findings
- Omit phrases like "image of" or "picture of"
- For decorative images, use `{fig-alt=""}`

**Examples of descriptive alt text:**

```markdown
# For a chart

![Bevölkerungsentwicklung Basel](plot.png){fig-alt="Liniendiagramm zeigt kontinuierliches Bevölkerungswachstum in Basel von 50.000 Einwohnern im Jahr 1850 auf 120.000 im Jahr 1914. Steiler Anstieg zwischen 1880 und 1900."}

# For a historical photograph

![Basler Synagoge 1868](synagoge.jpg){fig-alt="Schwarz-Weiss-Fotografie der neoromanischen Basler Synagoge kurz nach ihrer Fertigstellung. Dreischiffiges Gebäude mit zwei Türmen und Rundbogenfenstern."}

# For a diagram

![Workflow](workflow.png){fig-alt="Flussdiagramm des Datenverarbeitungsprozesses: Rohdaten führen zu Bereinigung, dann zu Analyse, schließlich zu Visualisierung und Publikation."}
```

### Descriptive Link Text

**Never use generic phrases like "click here" or "read more".** Link text should describe the destination:

**Bad examples:**

```markdown
Weitere Informationen finden Sie [hier](https://example.com).
Klicken Sie [hier](https://example.com) für Details.
Lesen Sie [mehr](https://example.com).
```

**Good examples:**

```markdown
Weitere Informationen finden Sie in der [Projektdokumentation](https://example.com).
Details zur Methodik sind im [GitHub Repository](https://github.com/example) verfügbar.
Die [vollständige Datenanalyse](https://example.com) bietet tiefere Einblicke.
```

### Proper Heading Hierarchy

Maintain logical heading structure (don't skip levels):

**Bad example:**

```markdown
# Page Title

### Subsection (skipped H2!)
```

**Good example:**

```markdown
# Page Title

## Main Section

### Subsection

#### Detail Level
```

**Rules:**

- Page title is automatically H1 from YAML `title:`
- Start content sections with H2 (`##`)
- Use H3 (`###`) for subsections within H2 sections
- Don't skip heading levels
- Keep headings descriptive and concise

### Foreign-Language Passages

Mark passages in languages other than the page's primary language using the `lang` attribute:

**Example (in a German page):**

```markdown
Die Forschungsgruppe veröffentlichte ihre Ergebnisse unter dem Titel
[Public History and Digital Humanities]{lang=en}.

Das Projekt basiert auf dem Framework [Datasheets for Datasets]{lang=en}
von Gebru et al. (2018).

Der französische Historiker schrieb: [«L'histoire ne se répète pas,
mais elle rime»]{lang=fr}.
```

**When to use:**

- Book/article titles in other languages
- Technical terms that are language-specific
- Quotes in original language
- Proper names that are language-specific

### Table Captions

**Every table should have a descriptive caption:**

```markdown
| Jahr | Einwohner | Jüdische Gemeinde |
| ---- | --------- | ----------------- |
| 1850 | 27,170    | 895               |
| 1880 | 60,500    | 1,322             |
| 1910 | 132,275   | 2,847             |

: Bevölkerungsentwicklung und Wachstum der jüdischen Gemeinde in Basel, 1850–1910 {#tbl-population}
```

**For complex tables with additional context:**

```markdown
::: {#tbl-demographics}
| Kategorie | 1850 | 1910 | Veränderung |
|-----------|------|------|-------------|
| Total | 895 | 2847 | +218% |
| Männer | 445 | 1401 | +215% |
| Frauen | 450 | 1446 | +221% |

Demografische Entwicklung der jüdischen Gemeinde Basel. Daten aus
historischen Adressbüchern und Gemeinderegistern.
:::
```

### Accessibility Checklist

When creating or reviewing content:

- [ ] All images have meaningful `fig-alt` attributes
- [ ] Link text is descriptive (no "click here" or "more")
- [ ] Heading hierarchy is logical (no skipped levels)
- [ ] Foreign-language passages are marked with `lang` attribute
- [ ] Tables have descriptive captions
- [ ] Color is not the only means of conveying information
- [ ] Text has sufficient contrast (this is handled by the theme)
- [ ] PDFs are accessible or have accessible alternatives
- [ ] Video/audio content has transcripts or captions where applicable

## Agent-Specific Guidance

### When Working with Content

1. **Respect Dual Licensing**: Code changes (AGPL-3.0), content changes (CC BY 4.0)
2. **Language**: Primary language is German; maintain consistency
3. **Content Structure**: Follow existing patterns in `.qmd` files
4. **YAML Front Matter**: Include title, description, and other metadata as seen in existing files

### Citation & DOI Policy

- **When to add a DOI**: Citable outputs (e.g., `products/publications/*`, `products/talks-posters/*`) should include a `doi:` in YAML if a DOI exists (typically Zenodo or publisher DOI).
- **Citation block**: Include a `citation:` block in YAML when a canonical reference is available. Prefer standard formats and stable identifiers.
- **Internal pages**: Do not add DOIs to internal or purely informational pages (e.g., `products/interna/*`, top-level landing pages).
- **Links**: Use the canonical resolver form `https://doi.org/<doi>` in content and references.

### Citation & DOI Consistency

Maintain consistent citation practices and DOI usage across all outputs to ensure proper attribution and discoverability.

#### Zenodo DOI Requirements

Use Zenodo for archiving and obtaining DOIs for citable research outputs:

**When to use Zenodo DOIs:**

- Publications (papers, data stories, reports)
- Presentations and posters from conferences
- Research datasets
- Software releases
- Educational materials intended for citation

**When NOT to use DOIs:**

- Internal documentation (`products/interna/*`)
- Process documentation
- Workflow guides
- Top-level landing pages (index.qmd, about.qmd, team.qmd)

#### YAML Citation Block Format

Include a complete `citation:` block in YAML front matter for all citable outputs:

**Example for a publication:**

```yaml
---
title: 'Das jüdische Basel 1850–1914'
author:
  - name: Beni Pfister
  - name: Jonas Schneider
    orcid: 0000-0000-0000-0000
    affiliation: KleioLab GmbH
date: 2024-02-29
doi: 10.5281/zenodo.15681537
categories: ['Data Story']
lang: de
appendix-cite-as: display
citation:
  type: standard
  title: 'Das jüdische Basel 1850–1914'
  container-title: 'Stadt.Geschichte.Basel Digital'
  publisher: 'Stadt.Geschichte.Basel'
  publisher-place: 'Basel'
  url: 'https://doi.org/10.5281/zenodo.15681537'
  doi: 10.5281/zenodo.15681537
---
```

**Example for a talk/poster:**

```yaml
---
title: 'Teach Historians How to Design a Data Story'
author:
  - name: Moritz Mähr
    orcid: 0000-0002-1367-1618
    affiliation: Universität Basel
date: 2022-10-20
event: 'DARIAH-CH Study Day, Università della Svizzera Italiana'
categories: Vortrag
lang: de
doi: 10.5281/zenodo.7198056
citation:
  type: standard
  container-title: 'DARIAH-CH Study Day 2022, Università della Svizzera Italiana'
appendix-cite-as: display
---
```

**Example for a dataset:**

```yaml
---
title: 'Geodata Basel Historical Buildings'
author:
  - name: Data Curator Name
    orcid: 0000-0000-0000-0000
    affiliation: Universität Basel
date: 2025-01-15
doi: 10.5281/zenodo.XXXXXXX
categories: ['Research Data']
lang: de
citation:
  type: dataset
  title: 'Geodata Basel Historical Buildings'
  publisher: 'Zenodo'
  url: 'https://doi.org/10.5281/zenodo.XXXXXXX'
  doi: 10.5281/zenodo.XXXXXXX
---
```

#### Reference Validation Guidance

**Before publishing:**

1. **Verify DOI resolution**: Test that all DOI links resolve correctly using `https://doi.org/<doi>` format
2. **Check ORCID identifiers**: Ensure all author ORCID iDs are valid and follow the ORCID format (four groups of four digits separated by hyphens, where the final character may be a digit or `X`, e.g., `0000-0003-3885-248X` or `0009-0005-7187-9774`)
3. **Validate citation metadata**: Confirm that citation blocks include all required fields for the citation type
4. **Cross-platform consistency**: Ensure metadata matches across:
   - Page YAML front matter
   - Zenodo record
   - GitHub repository (if applicable)
   - CITATION.cff file (for repositories)

**Common validation checks:**

```bash
# Check for DOI format consistency (should always use https://doi.org/)
grep -r "doi.org" products/ --include="*.qmd" | grep -v "https://doi.org/"

# Find pages with DOI in interna (should be none)
grep -r "^doi:" products/interna/ --include="*.qmd"

# Check for ORCID format (four groups of four digits, last character may be X)
grep -r "orcid:" products/ --include="*.qmd" | grep -Pv '[0-9]{4}-[0-9]{4}-[0-9]{4}-[0-9]{3}[0-9X]'
```

**Explicit Rules:**

- **NEVER** add DOIs to pages under `products/interna/*` - these are internal process documents
- **ALWAYS** use Zenodo DOIs (`10.5281/zenodo.XXXXXXX`) for Stadt.Geschichte.Basel outputs
- **ALWAYS** include `appendix-cite-as: display` in YAML to show citation information
- **ALWAYS** use HTTPS for DOI links: `https://doi.org/<doi>`
- **ALWAYS** include ORCIDs for authors when available
- **ALWAYS** ensure the DOI in the `citation:` block matches the `doi:` field in YAML

### When Working with Code

1. **Dependencies**:
   - Always check for existing packages before adding new ones
   - Update lock files: `package-lock.json`, `renv.lock`, `uv.lock`
   - Test that new dependencies work in the Codespace environment

2. **Quarto Configuration**:
   - Main config: `_quarto.yml`
   - Theme customizations: `_extensions/Stadt-Geschichte-Basel/sgb-theme/`
   - Don't modify Quarto settings without understanding their impact

3. **Testing Changes**:
   - Always preview locally with `uv run quarto preview`
   - Check formatting with `npm run check`
   - Verify links are not broken

### Executable Code in Pages

- **R**: Some pages contain R code chunks (```{r}). Execution occurs during Quarto render. Use `renv`to manage packages; prefer`freeze: auto` in YAML for reproducibility.
- **Python**: Python execution is currently uncommon/not required; only add Python chunks (```{python}) if justified and ensure `uv` environment is synced.
- **Avoid heavy ops**: Keep chunks deterministic and resource-light; avoid network calls during build. Cache results or precompute and store artifacts under `assets/` when necessary.

### When Modifying Documentation Structure

1. Update `_quarto.yml` if adding/removing pages or changing navigation
2. Maintain consistency in sidebar structure
3. Update README.md if workflow changes
4. Consider breadcrumb navigation paths

## Common Tasks for Agents

### Adding a New Documentation Page

1. Create new `.qmd` file in appropriate directory
2. Add YAML front matter (title, description, etc.)
   - Template: see [docs/sample-index.qmd](docs/sample-index.qmd) for a canonical example
3. Add entry to `_quarto.yml` sidebar section
4. Preview with `uv run quarto preview`
5. Format with `npm run format`

### QMD Template Generation

When creating new `.qmd` files, follow directory-specific templates to ensure consistency and proper metadata structure.

#### Required YAML Fields Template

All `.qmd` files must include these core fields:

```yaml
---
title: 'Page Title'
description: 'Brief description of the content (1-2 sentences)'
lang: de # Always explicitly specify language (de for German, en for English)
date-modified: last-modified
---
```

#### Directory-Specific Templates

**For `products/publications/*/index.qmd`** (publications and data stories):

```yaml
---
title: 'Publication Title'
subtitle: 'Optional Subtitle'
author:
  - name: Author Name
    orcid: 0000-0000-0000-0000
    affiliation: Universität Basel
date: 2025-01-15
doi: 10.5281/zenodo.XXXXXXX # Zenodo DOI if available
categories: ['Publikation'] # or ["Data Story"]
lang: de
appendix-cite-as: display
citation:
  type: standard
  title: 'Citation Title'
  container-title: 'Journal or Book Title'
  publisher: 'Publisher Name'
  url: 'https://doi.org/10.5281/zenodo.XXXXXXX'
other-links:
  - text: 'Link Description'
    icon: house
    href: 'https://example.com'
code-links:
  - text: 'GitHub Repository'
    icon: github
    href: 'https://github.com/Stadt-Geschichte-Basel/repo-name'
---
```

**For `products/talks-posters/*/index.qmd`** (presentations and posters):

```yaml
---
title: 'Presentation Title'
subtitle: 'Event Context'
author:
  - name: Presenter Name
    orcid: 0000-0000-0000-0000
    affiliation: Universität Basel
date: 2025-01-15
event: 'Conference Name, Location' # Required field
categories: Vortrag # Options: Vortrag, Poster, Workshop, Panel
lang: de
doi: 10.5281/zenodo.XXXXXXX # Zenodo DOI if available
citation:
  type: standard
appendix-cite-as: display
other-links:
  - text: 'Conference Website'
    icon: house
    href: 'https://example.com'
  - text: 'Slides (Zenodo)'
    icon: filetype-pdf
    href: 'https://doi.org/10.5281/zenodo.XXXXXXX'
---
```

**For `products/interna/*/index.qmd`** (internal documentation):

```yaml
---
title: 'Internal Documentation Title'
subtitle: 'Brief Context'
author:
  - name: Author Name
    orcid: 0000-0000-0000-0000
    affiliation: Universität Basel
category: Interna
date-modified: last-modified
lang: de
# NOTE: Internal pages should NEVER have a DOI
code-links:
  - text: 'GitHub Repository'
    icon: github
    href: 'https://github.com/Stadt-Geschichte-Basel/repo-name'
---
```

**For `products/research-data/*/index.qmd`** (research datasets):

```yaml
---
title: 'Dataset Title'
subtitle: 'Dataset Description'
author:
  - name: Data Curator Name
    orcid: 0000-0000-0000-0000
    affiliation: Universität Basel
date: 2025-01-15
doi: 10.5281/zenodo.XXXXXXX # Zenodo DOI for the dataset
lang: de
format:
  sgb-theme-html:
    toc: true
categories: ['Research Data']
other-links:
  - text: 'Dataset on Zenodo'
    icon: database
    href: 'https://doi.org/10.5281/zenodo.XXXXXXX'
code-links:
  - text: 'Data Repository'
    icon: github
    href: 'https://github.com/Stadt-Geschichte-Basel/repo-name'
---
```

**Key Guidelines:**

- Always include `lang: de` explicitly in YAML (or appropriate language code)
- Publications and data stories require `categories: ["Publikation"]` or `["Data Story"]`
- Talks/posters require an `event:` field and appropriate category (Vortrag, Poster, Workshop, Panel)
- Internal documentation (`products/interna/*`) should NEVER include a DOI
- Use Zenodo DOIs (`10.5281/zenodo.XXXXXXX`) for citable outputs
- Include ORCID identifiers for all authors when available
- Use `date-modified: last-modified` for pages that update frequently

### Fixing Formatting Issues

1. Run `npm run check` to identify issues
2. Run `npm run format` to auto-fix
3. For Quarto-specific issues, check with `uv run quarto check`

### Updating Dependencies

**Node.js:**

```bash
npm update
npm run check
```

**Python:**

```bash
uv sync --upgrade
```

**R:**

```bash
Rscript -e 'renv::update()'
```

### Creating New Products/Outputs

1. Place in `products/` directory
2. Follow existing naming and structure conventions
3. Update `products/products.qmd` if it's a new category
4. Update sidebar in `_quarto.yml`

### Research Data Documentation (Datasheets)

When documenting research datasets in `products/research-data/*/index.qmd`, follow the **Datasheets for Datasets** framework ([Gebru et al., 2018](https://arxiv.org/abs/1803.09010)) to ensure comprehensive and transparent documentation.

#### Structure and Content

Research dataset documentation should address these seven key sections:

**1. Motivation**

- Why was the dataset created?
- Who funded the creation of the dataset?
- What are the intended use cases?

Example:

```markdown
## Motivation

Dieses Dataset wurde erstellt, um die räumliche Verteilung jüdischer Gemeinden
in Basel zwischen 1850 und 1914 zu dokumentieren. Die Datensammlung wurde im
Rahmen des Stadt.Geschichte.Basel-Projekts finanziert und dient der historischen
Forschung sowie der öffentlichen Geschichtsvermittlung.
```

**2. Composition**

- What do the instances represent (e.g., people, places, events)?
- How many instances are there in total?
- What data does each instance consist of (fields, variables)?
- Is there a label or target associated with each instance?
- Are relationships between instances made explicit?
- Is there missing data?

**3. Collection Process**

- How was the data acquired (e.g., archival research, digitization)?
- What mechanisms or procedures were used to collect the data?
- Who was involved in the data collection process?
- Over what timeframe was the data collected?
- Were any ethical review processes conducted?

**4. Preprocessing/Cleaning/Labeling**

- Was any preprocessing/cleaning/labeling done?
- Was the "raw" data saved in addition to the processed data?
- What software/tools were used for preprocessing?

Example:

```markdown
## Datenverarbeitung

Die Rohdaten aus historischen Adressbüchern wurden mit R bereinigt und
standardisiert. Geografische Koordinaten wurden durch Geocodierung
historischer Adressen generiert. Sowohl Rohdaten als auch bereinigte
Daten sind im GitHub-Repository verfügbar.
```

**5. Uses**

- What other tasks could the dataset be used for?
- Are there tasks for which the dataset should not be used?
- What are potential impacts of using this dataset?

**6. Distribution**

- How is the dataset distributed (e.g., Zenodo, GitHub)?
- When was it first distributed?
- What license is it distributed under?
- Is the dataset subject to any copyright restrictions?

Example:

```markdown
## Verteilung

Das Dataset ist auf [Zenodo](https://doi.org/10.5281/zenodo.XXXXXXX)
archiviert und über GitHub verfügbar. Es wird unter CC BY 4.0 Lizenz
veröffentlicht und kann frei nachgenutzt werden.
```

**7. Maintenance**

- Who is supporting/hosting/maintaining the dataset?
- How can the owner/curator be contacted?
- Will the dataset be updated? If so, how often?
- If the dataset becomes obsolete, how will this be communicated?

**Implementation Notes:**

- Use these seven sections as H2 headings (`##`) in your dataset documentation
- Adapt the level of detail to the complexity and sensitivity of the dataset
- For Stadt.Geschichte.Basel datasets, emphasize historical context and provenance
- Link to the GitHub repository where code and raw data are stored
- Always include licensing information (typically CC BY 4.0 for data/content)
- Consider adding a `bibliography: references.bib` to cite relevant sources

## Troubleshooting

### Quarto Won't Render

- Check `uv run quarto check` output
- Verify Python/R environments are activated
- Check for syntax errors in `.qmd` files

### Formatting Conflicts

- Prettier may conflict with some generated files
- Check `.prettierrc` for exclusions
- Add problematic files to ignore patterns if needed

### Build Failures

- Check all three package managers are in sync (npm, uv, renv)
- Clear cache: `uv run quarto render --clean`
- Verify environment matches `.devcontainer/devcontainer.json`

## Resources

- [Quarto Documentation](https://quarto.org/docs/)
- [The Turing Way](https://the-turing-way.netlify.app/)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Contributing Guidelines](CONTRIBUTING.md)
- [Code of Conduct](CODE_OF_CONDUCT.md)
- [Security Policy](SECURITY.md)

## Quick Reference for Agents

### Before Making Changes

- [ ] Read README.md for project overview
- [ ] Check CONTRIBUTING.md for contribution guidelines
- [ ] Understand the technology stack (Quarto + R + Python + Node.js)
- [ ] Set up local environment or use Codespace

### During Development

- [ ] Make minimal, focused changes
- [ ] Test locally with `uv run quarto preview`
- [ ] Run `npm run check` to verify formatting
- [ ] Use `npm run commit` for conventional commit messages

### Before Submitting

- [ ] Run `npm run format` to fix formatting
- [ ] Preview the full site build
- [ ] Update relevant documentation
- [ ] Check that no sensitive data is committed
- [ ] Verify licenses are respected (Code: AGPL-3.0, Content: CC BY 4.0)

---

**Last Updated**: 2026-02-02
**Maintained By**: [@Stadt-Geschichte-Basel](https://github.com/Stadt-Geschichte-Basel)
