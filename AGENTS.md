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

The repository follows [The Turing Way's Advanced Structure for Data Analysis](https://the-turing-way.netlify.app/project-design/project-repo/project-repo-advanced.html):

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

**Last Updated**: 2025-11-13
**Maintained By**: [@Stadt-Geschichte-Basel](https://github.com/Stadt-Geschichte-Basel)
