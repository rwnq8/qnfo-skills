> **INCLUDES AUTONOMOUS RED-TEAM SELF-AUDIT.** See RED-TEAM-PROTOCOL.md.


# PDF BUILDER SKILL — v2.0

> **Bundled skill.** All scripts and references are self-contained in this skill directory.
> Deployed via `_deploy.py` to `%USERPROFILE%\.deepchat\skills\pdf-builder\` (DeepChat runtime directory).

---

## Purpose

Convert Markdown (`.md`) files to **Obsidian-quality, CSS-formatted, professional PDFs**
with full LaTeX math support (inline and block) and beautifully styled tables.

**v2.0 (2026-06-28):** PRIMARY pipeline is now MD → HTML+CSS+MathJax → playwright PDF.
This replaces the old reportlab approach and matches Obsidian's PDF export quality.
Full LaTeX math support (via MathJax 3), CSS-styled tables, professional typography,
and print-optimized output.

**v1.4 (legacy):** reportlab + matplotlib mathtext pipeline kept as `--legacy` fallback.

---

## Quick Start

```bash
# Primary pipeline (Obsidian-quality, RECOMMENDED):
python "%APPDATA%\DeepChat\skills\pdf-builder\scripts\build_pdf.py" --input paper.md --output paper.pdf

# With metadata override:
python "%APPDATA%\DeepChat\skills\pdf-builder\scripts\build_pdf.py" --input paper.md --output paper.pdf --title "My Paper" --author "Name"

# Legacy pipeline (reportlab, lower quality):
python "%APPDATA%\DeepChat\skills\pdf-builder\scripts\build_pdf.py" --input paper.md --output paper.pdf --legacy

# Skip math rendering:
python "%APPDATA%\DeepChat\skills\pdf-builder\scripts\build_pdf.py" --input paper.md --output paper.pdf --no-math
```

### Prerequisites

```bash
# Primary pipeline (required):
pip install playwright markdown pyyaml pymupdf
playwright install chromium

# Legacy pipeline (optional):
pip install reportlab matplotlib
```

### YAML Frontmatter Support

Build_pdf.py automatically strips YAML frontmatter from markdown files and extracts
metadata. The frontmatter is NOT rendered in the PDF output.

**Extracted fields:**
- `title` — Publication title (auto-detected, overridable via `--title` CLI arg)
- `author` — Author name(s)
- `date` — Publication date (YYYY-MM-DD)
- `abstract` — Abstract text (styled in a grey box on the title page)
- `license` — License identifier

**Example frontmatter:**
```yaml
---
title: "My Research Paper"
author: "Rowan Quni-Gudzinas (QNFO/QWAV)"
date: "2026-06-28"
license: "QNFO Unified License Agreement (QNFO-ULA)"
abstract: >
  This is the abstract. It can span multiple lines
  using YAML folded block scalar syntax (>).
---
```

---

## Architecture (v2.0)

```
┌─────────────────────────────────────────────────────────────────┐
│                    PRIMARY PIPELINE (v2.0)                       │
│                                                                  │
│  paper.md                                                        │
│     │                                                            │
│     ▼                                                            │
│  md_to_html.py  ─── Converts MD → HTML + embedded papers.css    │
│     │              + MathJax 3 config (full LaTeX macros)        │
│     ▼                                                            │
│  paper.html (standalone, styled, MathJax-ready)                 │
│     │                                                            │
│     ▼                                                            │
│  playwright (Chromium) ─── Renders HTML, executes MathJax,      │
│     │                       prints to PDF (A4, print CSS)        │
│     ▼                                                            │
│  paper.pdf (Obsidian-quality, CSS-formatted, professional)      │
│                                                                  │
├─────────────────────────────────────────────────────────────────┤
│                    LEGACY PIPELINE (--legacy)                    │
│                                                                  │
│  paper.md → reportlab + matplotlib mathtext → paper.pdf         │
│  (programmatic PDF, LaTeX subset only, lower visual quality)    │
└─────────────────────────────────────────────────────────────────┘
```

### Why This Architecture (matching Obsidian)

Obsidian renders Markdown → HTML with CSS → then prints to PDF via the browser engine
(Chromium/Electron). This is the exact same approach our v2.0 primary pipeline uses:

| Aspect | v2.0 (playwright) | v1.x (reportlab) | Obsidian |
|:-------|:-----------------:|:----------------:|:--------:|
| CSS styling | ✅ Full CSS | ❌ JSON config only | ✅ Full CSS |
| Tables | ✅ CSS-styled HTML | ⚠️ reportlab Table | ✅ CSS-styled |
| Math rendering | ✅ MathJax 3 (full LaTeX) | ⚠️ mathtext (subset) | ✅ MathJax |
| `\begin{align}` | ✅ Native | ❌ Not supported | ✅ Native |
| Typography | ✅ CSS fonts + print | ⚠️ TTF registration | ✅ CSS fonts |
| Print optimization | ✅ @media print CSS | ❌ Manual | ✅ @media print |
| Visual quality | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

---

## Bundled Files

| File | Purpose |
|:-----|:--------|
| `scripts/build_pdf.py` | Main PDF builder (v2.0 with playwright primary + legacy fallback) |
| `scripts/md_to_html.py` | Markdown → styled HTML converter (CSS + MathJax embedding) |
| `references/papers.css` | Professional academic CSS stylesheet (Obsidian-quality typography) |

---

## Detailed Workflow

### Step 1: Verify Prerequisites

```bash
# Primary pipeline prerequisites
python -c "import playwright, markdown, yaml; print('Primary: OK')"

# Legacy pipeline prerequisites (optional)
python -c "import reportlab, matplotlib; print('Legacy: OK')"

# Verify playwright has chromium
python -c "from playwright.sync_api import sync_playwright; p = sync_playwright().start(); b = p.chromium.launch(); b.close(); p.stop(); print('Chromium: OK')"
```

### Step 2: Build PDF

```bash
python "%APPDATA%\DeepChat\skills\pdf-builder\scripts\build_pdf.py" --input "paper.md" --output "paper.pdf"
```

### Step 3: Verify Rendering (MANDATORY)

```bash
python "%APPDATA%\DeepChat\skills\pdf-builder\scripts\build_pdf.py" --input "paper.pdf" --verify
```

Or directly:

```bash
python -c "
import fitz
doc = fitz.open('paper.pdf')
text = ''.join(page.get_text() for page in doc)
if '\ufffd' in text:
    print('[BLOCKED] PDF contains Unicode replacement characters')
else:
    print('[OK] No replacement characters')
for char, name in [('\u2014','em dash'), ('\u201c','left curly quote'), ('\u201d','right curly quote')]:
    count = text.count(char)
    print(f'[{\"OK\" if count>0 else \"MISSING\"}] {name}: {count} found')
doc.close()
"
```

---

## Math Rendering (v2.0)

### Full LaTeX Support via MathJax 3

The v2.0 pipeline uses MathJax 3 with **full LaTeX math support**:

| Feature | v2.0 (MathJax) | v1.x (mathtext) |
|:--------|:-------------:|:---------------:|
| Inline math (`$...$`) | ✅ | ✅ |
| Display math (`$$...$$`) | ✅ | ✅ |
| `\begin{align}` | ✅ | ❌ |
| `\begin{cases}` | ✅ | ⚠️ |
| `\begin{equation}` | ✅ | ❌ |
| `\begin{gather}` | ✅ | ❌ |
| `\bmod`, `\pmod` | ✅ | ✅ (fixed) |
| `\operatorname{...}` | ✅ | ✅ (fixed) |
| `\bm{...}` | ✅ | ✅ (fixed) |
| `\mathbb{...}` | ✅ | ✅ |
| `\mathcal{...}` | ✅ | ⚠️ |
| `\tag{...}` / `\label{...}` | ✅ | ❌ |
| `\ref{...}` | ✅ | ❌ |
| Custom macros | ✅ (config) | ❌ |
| All LaTeX packages | ✅ | ❌ |

### QNFO Standard Math Macros

The MathJax configuration includes these macros for all publications:

| Macro | Expands to |
|:------|:-----------|
| `\RR` | `\mathbb{R}` |
| `\ZZ` | `\mathbb{Z}` |
| `\NN` | `\mathbb{N}` |
| `\CC` | `\mathbb{C}` |
| `\QQ` | `\mathbb{Q}` |
| `\FF` | `\mathbb{F}` |
| `\calO` | `\mathcal{O}` |
| `\Aut` | `\operatorname{Aut}` |
| `\Gal` | `\operatorname{Gal}` |
| `\Hom` | `\operatorname{Hom}` |
| `\GL`, `\SL`, `\SO`, `\SU` | matrix groups |
| `\eps` | `\varepsilon` |
| `\vphi` | `\varphi` |

---

## Tables (v2.0)

Tables are rendered as **CSS-styled HTML tables**, not programmatic reportlab Tables:

- Dark header row with white text (`#1a5276`)
- Alternating row colors for readability
- Column alignment from markdown hints (`:---`, `:---:`, `---:`)
- Inline math in table cells (`$...$`) rendered by MathJax
- Professional typography (heading font for headers, body font for content)
- Print-friendly with `page-break-inside: avoid`
- Wide tables handled by browser layout engine (better than reportlab)

---

## CSS Customization

### Bundled Stylesheet

The `references/papers.css` file provides professional academic styling:

```bash
# Use default bundled stylesheet (automatic):
python build_pdf.py --input paper.md --output paper.pdf

# Use custom stylesheet:
python build_pdf.py --input paper.md --output paper.pdf --css my-style.css
```

### Style Variables

Override these CSS custom properties for your publication:

```css
:root {
    --color-accent: #1a5276;        /* Heading borders, table headers */
    --font-body: Georgia, serif;    /* Body text font */
    --font-heading: Helvetica, sans-serif;  /* Heading font */
    --font-size-body: 11pt;         /* Base font size */
    --max-width: 42em;              /* Content width */
}
```

---

## Pipeline Decision Flow (v2.0)

```
Always use PRIMARY pipeline (v2.0) ──→ Obsidian-quality output
  │
  ├── playwright unavailable? ──→ Install: pip install playwright && playwright install chromium
  │
  └── Still unavailable? ──→ Fallback: --legacy (reportlab, lower quality)
```

**The legacy pipeline is a LAST RESORT.** It produces programmer-art PDFs with:
- Limited math (matplotlib mathtext — LaTeX subset, no align/cases/tag/ref)
- Programmatic tables (reportlab Table, no CSS styling)
- Limited typography (TTF registration, no CSS font stack)
- No print CSS optimization

---

## Arguments

| Flag | Required | Description |
|:-----|:---------|:------------|
| `--input`, `-i` | Yes | Input file (.md or .html) |
| `--output`, `-o` | Yes | Output PDF file path |
| `--title`, `-t` | No | Publication title (auto-detected) |
| `--author`, `-a` | No | Author name |
| `--date`, `-d` | No | Publication date (defaults to today) |
| `--css` | No | Custom CSS stylesheet (default: bundled papers.css) |
| `--no-math` | No | Skip math rendering |
| `--legacy` | No | Use legacy reportlab pipeline |
| `--stylesheet`, `-s` | No | Legacy: publication stylesheet JSON |
| `--check-unicode` | No | Scan for `\uXXXX` escapes |
| `--fix-unicode` | No | Auto-correct `\uXXXX` escapes |
| `--verify` | No | Verify existing PDF quality |

---

## Cross-References

- Used by: `publication-publisher` skill (Step 2: Build PDF)
- Related: `cloudflare-deployer` skill (post-PDF deployment)
- CSS: `references/papers.css` (bundled academic stylesheet)
- HTML converter: `scripts/md_to_html.py` (MD → styled HTML)

---

*pdf-builder v2.0 — Primary pipeline: MD → HTML+CSS+MathJax → playwright PDF. Obsidian-quality output with full LaTeX math, CSS-styled tables, and professional typography. Legacy reportlab pipeline kept as fallback. Tested 2026-06-28.*

## RT: RED-TEAM SELF-AUDIT

Before claiming this skill complete, autonomously run:

1. Output Verification (negative verification)
2. Assumption Challenge (state and test every assumption)
3. Edge Case Check (empty/null/max/boundary/desync)
4. DoD Integration (run _dod_enforce.py if exists)
5. Iteration (retry on failure, max 3)

ANTI-PATTERN: User should NEVER ask about quality.
Refer to RED-TEAM-PROTOCOL.md for full protocol.
