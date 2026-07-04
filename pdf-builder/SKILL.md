---
name: pdf-builder
description: Build publication-quality PDFs from Markdown files with math rendering via matplotlib mathtext. Use when the agent needs to convert .md to .pdf for QNFO publications, papers, or reports.
version: "3.0"
---
> **INCLUDES AUTONOMOUS RED-TEAM SELF-AUDIT.** See RED-TEAM-PROTOCOL.md.



### Programmatic Loading & Execution
This skill is loaded and executed **programmatically by the LLM system** 
during response generation. Loading is triggered automatically via 
`skill_view('pdf-builder')` or `read()` with filesystem path.
**The user NEVER manually loads this skill.** The `skill-autoloader` 
detects task patterns and handles all skill loading. If this skill fails 
to load, the LLM system automatically retries via the fallback chain 
documented below.
**Pinning:** This skill is [On-demand — loads when triggered by task patterns].

### Skill Loading Retry Protocol
If `skill_view('name')` fails during programmatic loading, the LLM system 
MUST execute this fallback chain:
1. **Retry 1:** `read('%USERPROFILE%\.deepchat\skills\<name>\SKILL.md')`
2. **Retry 2:** Pull from Cloudflare R2: `npx wrangler r2 object get 
   qnfo/prompts/skills/<name>/SKILL.md --remote --file=_skill.md`
3. **Retry 3:** If R2 fails, search local filesystem for any cached copy
4. **Fallback:** If ALL retries fail, continue with `[SKILL-UNAVAILABLE: <name>]` 
   and best-effort knowledge
**NEVER silently proceed without a skill's critical instructions.** If a skill 
is required for the task and cannot be loaded after 3 retries, escalate to 
the user with the specific failure reason.

---

# PDF BUILDER SKILL — v1.0 — v2.0

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
| `scripts/build_pdf.py` | Main PDF builder (v3.0 — LOCKED 2026-07-01) |
| `scripts/md_to_html.py` | Markdown → styled HTML converter (CSS + MathJax embedding) |
| `references/papers.css` | Professional academic CSS stylesheet (Obsidian-quality typography) |

---

## Detailed Workflow

### Step 1: Verify Prerequisites

```bash
# Primary pipeline prerequisites
echo "import playwright, markdown, yaml; print('Primary: OK')" > _check_deps.py && python _check_deps.py && Remove-Item _check_deps.py

# Legacy pipeline prerequisites (optional)
echo "import reportlab, matplotlib; print('Legacy: OK')" > _check_legacy.py && python _check_legacy.py && Remove-Item _check_legacy.py

# Verify playwright has chromium
echo "from playwright.sync_api import sync_playwright; p = sync_playwright().start(); b = p.chromium.launch(); b.close(); p.stop(); print('Chromium: OK')" > _check_chromium.py && python _check_chromium.py && Remove-Item _check_chromium.py
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
# Write PDF verification script, execute, discard
echo "import fitz; doc = fitz.open('paper.pdf'); text = ''.join(page.get_text() for page in doc); print('[BLOCKED] PDF contains Unicode replacement characters' if '\ufffd' in text else '[OK] No replacement characters'); [(print(f'[{\"OK\" if text.count(c)>0 else \"MISSING\"}] {n}: {text.count(c)} found')) for c,n in [('\u2014','em dash'),('\u201c','left curly quote'),('\u201d','right curly quote')]]; doc.close()" > _verify_pdf.py
python _verify_pdf.py
Remove-Item _verify_pdf.py
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



---

## QNFO Design System Compliance (v3.0 — LOCKED 2026-07-01 — 2026-06-30)

**ALL QNFO/QWAV publications, pages, PDFs, and web artifacts MUST use the papers.qnfo.org canonical design (LOCKED v3.0).**

| Resource | Location |
|:---------|:---------|
| Design doc (full spec) | `qnfo/design-system/QNFO-DESIGN-SYSTEM.md` |
| PDF builder (v3.0) | `qnfo/design-system/build_pdf.py` |

### Mandatory Rules

🚫 **DARK THEMES FORBIDDEN.** All output must use:
- Inter + Source Serif 4 fonts, #1a1a2e text, #1a56db blue palette
- Max-width 960px centered layout
- Clean tables with border-collapse: collapse
- MathJax CHTML with left-aligned display equations
- AI Query box + Related Papers mandatory on all paper pages

### Verification
```bash
# Check any page for dark theme violations
python -c "import urllib.request;h=urllib.request.urlopen('URL').read().decode();print('DARK' if '#0a0a0f' in h or '#0d1117' in h else 'LIGHT')"
```
 SELF-AUDIT

Before claiming this skill complete, autonomously run:

1. Output Verification (negative verification)
2. Assumption Challenge (state and test every assumption)
3. Edge Case Check (empty/null/max/boundary/desync)
4. DoD Integration (run _dod_enforce.py if exists)
5. Iteration (retry on failure, max 3)

ANTI-PATTERN: User should NEVER ask about quality.
Refer to RED-TEAM-PROTOCOL.md for full protocol.
