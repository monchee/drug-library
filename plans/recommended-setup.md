# Recommended Setup & Plugins for Drug Library

## Current State Summary

| Area | Status | Notes |
|------|--------|-------|
| Theme | ✅ `materialx` | Correct — community successor to mkdocs-material, based on v9.7.1 |
| Plugins | ⚠️ Only `search` | `document-dates` assets exist but plugin not configured in mkdocs.yml |
| Markdown Extensions | Good baseline | 12 extensions active, but MaterialX supports many more |
| Dependency Pinning | ❌ Missing | No `requirements.txt` or `pyproject.toml` |
| Glossary Snippets | ⚠️ Partial | `pymdownx.snippets` enabled but not wired to `includes/glossary.md` |
| Tags | ⚠️ Unused | Drug pages define `tags` in frontmatter but no tag index |
| Deployment | ✅ Cloudflare Pages | `wrangler.toml` configured |

---

## 🔴 High Priority — Clinical Safety & Maintainability

### 1. Pin Dependencies with `requirements.txt`

No dependency file exists. Builds are not reproducible. Create a `requirements.txt`:

```
mkdocs-materialx>=10.0
pymdown-extensions>=10.0
mkdocs-document-dates
mkdocs-glightbox
```

### 2. Enable the `document-dates` Plugin

MaterialX includes a next-generation **`document-dates`** plugin that replaces both `mkdocs-git-revision-date-localized` and `mkdocs-git-committers-plugin-2`. It is:

- **O(1) build speed** — vs O(n) for the git-based plugins
- **Works in any environment** — Git, no-Git, Docker, all CI/CD systems
- **Fully automatic** — no manual date configuration needed
- **Shows creation date, last updated, and authors** with avatars

The config assets already exist at [`docs/assets/document_dates/user.config.js`](docs/assets/document_dates/user.config.js) and [`docs/assets/document_dates/user.config.css`](docs/assets/document_dates/user.config.css).

**Add to `mkdocs.yml`:**

```yaml
plugins:
  - document-dates:
      type: timeago
      locale: en
      show_created: true
      show_updated: true
      show_author: true
      exclude:
        - index.md
        - '*/index.md'
```

**Optional — Recently Updated Module:**

Add a sidebar section showing recently updated protocols:

```yaml
  - document-dates:
      ...
      recently-updated:
        limit: 10
        exclude:
          - index.md
          - '*/index.md'
```

Then download the [nav.html override template](https://github.com/jaywhj/mkdocs-document-dates/blob/main/templates/overrides/partials/nav.html) to `docs/overrides/partials/nav.html`.

### 3. Wire Up Glossary Snippets

[`docs/includes/glossary.md`](docs/includes/glossary.md) defines abbreviations (SPT, IDT, PPL, etc.) but `pymdownx.snippets` is not configured to auto-include it. Add:

```yaml
markdown_extensions:
  - pymdownx.snippets:
      auto_append:
        - includes/glossary.md
```

This lets authors use `*[SPT]:` anywhere and have it automatically expanded.

### 4. Add Missing Markdown Extensions

MaterialX supports many useful extensions not yet enabled. Recommended additions for a clinical drug library:

| Extension | Use Case |
|-----------|----------|
| `pymdownx.tasklist` with `custom_checkbox: true` | Checklist-style preparation steps — e.g., equipment checklists |
| `pymdownx.keys` | Keyboard shortcut notation in documentation |
| `pymdownx.mark` | `==Highlight==` important drug concentrations or critical warnings |
| `pymdownx.betterem` | Smarter emphasis handling |
| `pymdownx.caret` | `^^superscript^^` notation |
| `pymdownx.tilde` | `~~subscript~~` notation |
| `def_list` | Definition lists for drug terminology |
| `footnotes` | Reference footnotes for clinical citations |
| `pymdownx.magiclink` | Auto-link GitHub issues/PRs if repo is connected |

---

## 🟡 Medium Priority — UX & Navigation

### 5. Enable Tags Plugin

Drug pages already define tags in frontmatter (e.g., `tags: [beta-lactam, penicillin, antibiotic, spt, idt, ogc]`). MaterialX has built-in tag support:

```yaml
plugins:
  - tags:
      tags_file: reference/tags.md
```

Create `docs/reference/tags.md` with:

```markdown
---
title: Tags
---

# Tags

Browse all drug protocols by tag.
```

This lets clinicians click a tag like `antibiotic` and see all antibiotic protocols at once.

### 6. Additional Theme Features

Add these to `theme.features` in [`mkdocs.yml`](mkdocs.yml:25):

| Feature | Benefit |
|---------|---------|
| `navigation.path` | Breadcrumb trail — helps users know where they are in the drug hierarchy |
| `navigation.prune` | Hides empty nav sections — keeps sidebar clean |
| `search.suggest` | Shows search suggestions as you type |
| `content.action.edit` | Edit this page link — lets nurses suggest protocol corrections |
| `content.action.view` | View page source link |
| `content.tooltips` | MaterialX-native tooltip support |
| `content.footnote.tooltips` | Hover tooltips on footnotes |
| `toc.integrate` | Moves TOC into sidebar — more screen space for drug protocol content |

### 7. Enable `glightbox` Plugin

MaterialX bundles support for `glightbox` for image lightboxes. Useful if you ever add drug images, structure diagrams, or equipment photos:

```yaml
plugins:
  - glightbox
```

### 8. Edit URL Configuration

If the repo is on GitHub, enable edit links so clinicians can propose changes:

```yaml
edit_uri: edit/main/docs/
repo_url: https://github.com/your-org/drug-library
repo_name: your-org/drug-library
```

### 9. Social Cards / SEO

MaterialX auto-generates Open Graph images for each page. Useful when sharing protocol links in Slack/Teams:

```yaml
extra:
  social:
    - icon: fontawesome/brands/github
      link: https://github.com/your-org/drug-library
      name: GitHub
```

---

## 🟢 Lower Priority — Nice to Have

### 10. Print Stylesheet

Clinical staff frequently print protocols for bedside use. Add to [`docs/stylesheets/extra.css`](docs/stylesheets/extra.css):

```css
@media print {
  .md-header, .md-tabs, .md-sidebar, .md-footer { display: none !important; }
  .md-content { margin: 0 !important; }
}
```

### 11. Minify Plugin

Reduces HTML/CSS/JS size for faster page loads on slow hospital networks:

```yaml
plugins:
  - minify:
      minify_html: true
      minify_css: true
      minify_js: true
```

### 12. Enhanced Author Configuration

Create `docs/authors.yml` to show nurse/clinician profiles with avatars:

```yaml
authors:
  nurse1:
    name: Jane Smith
    avatar: assets/avatars/jane.jpg
    email: jane.smith@health.nsw.gov.au
    description: Clinical Nurse Specialist
```

### 13. Sitemap SEO Enhancement

Use the `document-dates` template variable to set correct `lastmod` in sitemap.xml for better search engine indexing. Download the [sitemap.xml override](https://github.com/jaywhj/mkdocs-document-dates/blob/main/templates/overrides/sitemap.xml) to `docs/overrides/sitemap.xml`.

### 14. Table Reader Plugin

The [`reference/`](reference/) directory contains Excel files. This plugin can embed Excel tables directly into Markdown pages:

```yaml
plugins:
  - table-reader:
      data_path: reference
```

---

## Proposed Final `mkdocs.yml` Structure

```yaml
site_name: SCRATCH
site_description: Skin & Challenge Reference for Allergy Testing Clinical Handbook — RPAH Clinical Immunology & Allergy
site_author: RPAH Allergy Nurses
site_url: https://scratch.pages.dev
copyright: "Copyright &copy; 2026 Department of Clinical Immunology and Allergy - Royal Prince Alfred Hospital"

repo_name: your-org/drug-library
repo_url: https://github.com/your-org/drug-library
edit_uri: edit/main/docs/

extra:
  social:
    - icon: fontawesome/brands/github
      link: https://github.com/your-org/drug-library
      name: GitHub

theme:
  name: materialx
  palette:
    - scheme: default
      primary: custom
      accent: custom
      toggle:
        icon: material/weather-night
        name: Switch to dark mode
    - scheme: slate
      primary: custom
      accent: custom
      toggle:
        icon: material/weather-sunny
        name: Switch to light mode
  font:
    text: Inter
    code: JetBrains Mono
  features:
    - navigation.instant
    - navigation.instant.progress
    - navigation.tracking
    - navigation.top
    - navigation.tabs
    - navigation.sections
    - navigation.expand
    - navigation.indexes
    - navigation.path
    - navigation.prune
    - navigation.footer
    - search.highlight
    - search.share
    - search.suggest
    - content.tabs.link
    - content.code.copy
    - content.code.annotate
    - content.action.edit
    - content.action.view
    - content.tooltips
    - content.footnote.tooltips
    - toc.follow
  topbar_style: primary
  icon:
    repo: fontawesome/brands/github

plugins:
  - search:
      separator: '[\s\-,:!=\[\]()"/]+'
  - document-dates:
      type: timeago
      locale: en
      show_created: true
      show_updated: true
      show_author: true
      exclude:
        - index.md
        - '*/index.md'
  - tags:
      tags_file: reference/tags.md
  - glightbox
  # - minify:
  #     minify_html: true
  #     minify_css: true
  #     minify_js: true

markdown_extensions:
  - admonition
  - attr_list
  - def_list
  - footnotes
  - md_in_html
  - tables
  - toc:
      permalink: true
  - abbr
  - pymdownx.details
  - pymdownx.superfences
  - pymdownx.tabbed:
      alternate_style: true
  - pymdownx.highlight:
      anchor_linenums: true
  - pymdownx.inlinehilite
  - pymdownx.snippets:
      auto_append:
        - includes/glossary.md
  - pymdownx.emoji:
      emoji_index: !!python/name:material.extensions.emoji.twemoji
      emoji_generator: !!python/name:material.extensions.emoji.to_svg
  - pymdownx.tasklist:
      custom_checkbox: true
  - pymdownx.keys
  - pymdownx.mark
  - pymdownx.betterem
  - pymdownx.caret
  - pymdownx.tilde

extra_css:
  - stylesheets/extra.css

nav:
  # ... existing nav structure ...
```

## Proposed `requirements.txt`

```
mkdocs-materialx>=10.0
pymdown-extensions>=10.0
mkdocs-document-dates
mkdocs-glightbox
```

---

## Decision Points for User

1. **Document dates**: Enable with `timeago` format, or use `date` format for clinical precision?
2. **Recently Updated module**: Add to sidebar navigation?
3. **Edit links**: Is the repo on GitHub? Should clinicians be able to suggest edits?
4. **Tags index**: Create a browsable tag cloud page?
5. **Author profiles**: Set up `authors.yml` with nurse/clinician profiles?
6. **Print support**: Add print-optimized CSS?
7. **Minification**: Enable for faster page loads?
8. **Excel embedding**: Embed the reference Excel files as tables in the docs?
