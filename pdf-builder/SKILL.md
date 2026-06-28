---
name: pdf-builder
description: Build publication-quality PDFs from Markdown files with math rendering via matplotlib mathtext. Use when the agent needs to convert .md to .pdf for QNFO publications, papers, or reports. Handles inline math ($...$), display math ($$...$$), code blocks, and Unicode typography. Supports --no-math flag for Unicode fallback rendering.
version: "1.4"
---
> **INCLUDES AUTONOMOUS RED-TEAM SELF-AUDIT.** See RED-TEAM-PROTOCOL.md.


# PDF BUILDER SKILL — v1.4

> **Bundled skill.** All scripts and references are self-contained in this skill directory.
> Deployed via `_deploy.py` to `%USERPROFILE%\.deepchat\skills\pdf-builder\` (DeepChat runtime directory).

---

## Purpose

Convert Markdown (`.md`) or HTML (`.html`) files to publication-quality PDFs using
reportlab. Renders mathematical expressions using matplotlib's mathtext parser.

**v1.4 (2026-06-06):** Markdown table rendering via reportlab Table + LaTeX math pre-processing (auto-fix \bmod, \operatorname, \\text).
**v1.3 (2026-06-05):** YAML frontmatter handling + publication stylesheet system.
**v1.1:** Math rendering via matplotlib mathtext.

**⚠️ RECOMMENDED WORKFLOW:** For most publications, use `build_pdf.py` directly (v1.4+ handles tables and
common LaTeX). For documents with complex environments (`\begin{align}`, `\begin{cases}`,
`\tag`, `\ref`) or custom LaTeX packages, use the **HTML + papers.css + MathJax** pipeline:
1. Convert `.md` → `.html` with `md_to_html.py` (uses `papers.css` for professional academic styling)
2. Deploy HTML to Cloudflare Pages
3. Build PDF from HTML via playwright/weasyprint for download

---

## Quick Start

```bash
# Basic build (auto-detects YAML frontmatter for title/author/date/abstract)
python "%APPDATA%\DeepChat\skills\pdf-builder\scripts\build_pdf.py" --input paper.md --output paper.pdf

# With publication stylesheet
python "%APPDATA%\DeepChat\skills\pdf-builder\scripts\build_pdf.py" --input paper.md --output paper.pdf \
  --stylesheet "%APPDATA%\DeepChat\skills\pdf-builder\references\publication-stylesheet.json"

# With title override (overrides YAML frontmatter)
python "%APPDATA%\DeepChat\skills\pdf-builder\scripts\build_pdf.py" --input paper.md --output paper.pdf --title "My Paper" --author "Name" --date "2026-06-03"

# Skip math rendering (Unicode fallback):
python "%APPDATA%\DeepChat\skills\pdf-builder\scripts\build_pdf.py" --input paper.md --output paper.pdf --no-math
```

### YAML Frontmatter Support (v1.3)

Build_pdf.py now automatically strips YAML frontmatter from markdown files and extracts
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
date: "2026-06-05"
license: "QNFO Unified License Agreement (QNFO-ULA)"
abstract: >
  This is the abstract. It can span multiple lines
  using YAML folded block scalar syntax (>).
---
```

### Publication Stylesheet (v1.3)

For consistent professional formatting across all QNFO publications, use the stylesheet:

```bash
python build_pdf.py --input paper.md --output paper.pdf \
  --stylesheet references/publication-stylesheet.json
```

The stylesheet (`references/publication-stylesheet.json`) defines typography, colors,
spacing, and layout for:
- Title page (title font, abstract box styling, license footer)
- Headings (H1-H4 hierarchy)
- Body text (font, size, leading, justification)
- Code blocks (font, background color)
- Page layout (margins, header line, page numbers)

Override any style by editing the JSON — no code changes needed.

---

## Workflow

### Step 1: Verify Prerequisites

```bash
python -c "import reportlab, matplotlib; print('OK')"
# Expected: OK (no ImportError)
```

If missing: `pip install reportlab matplotlib markdown pymupdf`

### Step 2: Verify Input

```bash
Test-Path "<input>.md"
```

### Step 3: Build PDF

```bash
python "%APPDATA%\DeepChat\skills\pdf-builder\scripts\build_pdf.py" --input "<input>.md" --output "<output>.pdf"
```

### Step 4: Verify Rendering (MANDATORY)

```bash
python -c "
import fitz
doc = fitz.open('<output>.pdf')
text = ''.join(page.get_text() for page in doc)
if '\ufffd' in text:
    print('[BLOCKED] PDF contains Unicode replacement characters')
else:
    print('[OK] No replacement characters')
doc.close()
"
```

If verification fails: PDF is NOT publication-ready. See `references/math-rendering.md` for
troubleshooting.

### Step 5: Clean Up (if using R2-pulled ephemeral copy)

```bash
Remove-Item _build_pdf.py -ErrorAction SilentlyContinue
```

---

## Math Rendering

### Supported Delimiters

| Delimiter | Type | Example |
|:----------|:-----|:--------|
| `$...$` | Inline math | `$E = mc^2$` |
| `$$...$$` | Display math (single-line) | `$$\hat{H}\psi = E\psi$$` |
| `$$` (block) | Display math (multi-line) | `$$\n...\n$$` |

### --no-math Mode

Converts LaTeX to Unicode approximations instead of rendering images:
- `$\alpha$` → α, `$\hbar$` → ℏ, `$\int$` → ∫, `$\infty$` → ∞
- Use for drafts or when matplotlib is unavailable
- See `references/math-rendering.md` for the full conversion table

### Limitations — READ BEFORE USING (updated v1.4)

**This skill now handles tables and common LaTeX commands (v1.4).** For documents with
complex math environments (`\begin{align}`, `\begin{cases}`, `\tag`, `\ref`) or custom
LaTeX packages, use the HTML-to-PDF alternative (see §Alternative below).

#### Math: Mathtext is NOT Full LaTeX

matplotlib's mathtext parser supports a SUBSET of LaTeX math. These specific commands
are KNOWN to fail and will produce `[MATH RENDER ERROR]` in output:

| Command | Status (v1.4) | Notes |
|:--------|:-------------|:------|
| `\bmod` | ✅ Auto-fixed | Converted to `\ \mathrm{mod}\ ` automatically |
| `\operatorname{...}` | ✅ Auto-fixed | Converted to `\mathrm{...}` automatically |
| `\\text{...}` (double backslash) | ✅ Auto-fixed | Converted to `\text{...}` (single backslash) |
| `\pmod{...}` | ✅ Auto-fixed | Converted to `(\mathrm{mod}\ ...)` automatically |
| `\bm{...}` | ✅ Auto-fixed | Converted to `\mathbf{...}` automatically |
| `\tfrac`, `\dfrac`, `\dbinom`, `\tbinom` | ✅ Auto-fixed | Converted to standard equivalents |
| `\begin{align}...\end{align}` | ❌ Not supported | Use separate `$$...$$` blocks per line |
| `\begin{cases}...\end{cases}` | ⚠️ Best-effort | Converted to `\left\{ \begin{array}{l}...` |
| `\tag{...}` / `\label{...}` / `\ref{...}` | ❌ Not supported | Add equation numbers manually |
| `\mathcal{...}` | ⚠️ Limited | Test before deploying |

**Pre-flight check:** Before building a PDF, scan the source file for unsupported
commands:
```bash
rg -n '\\\\bmod|\\\\\\\\text|\\\\operatorname|\\\\begin\{align|\\\\begin\{cases|\\\\bm\{|\\\\tag\{|\\\\label\{|\\\\ref\{' input.md
```
Any hits = this document uses unsupported math environments. Use HTML-to-PDF instead. (Note: `\bmod`, `\operatorname`, `\bm`, and `\\text` are auto-fixed in v1.4 and no longer block.)

#### Tables: SUPPORTED (v1.4)

**Markdown tables are now rendered** using reportlab's `Table` flowable with:
- Header rows with dark background and white text
- Alternating row colors for readability
- Column alignment from markdown hints (`:---`, `:---:`, `---:`)
- Inline math in table cells (`$...$`) rendered as math images
- Grid borders with professional styling

**Limitations:**
- Very wide tables (>6 columns) may not fit on A4 — consider reducing columns
- Table cells with complex multi-line content may wrap awkwardly
- Nested tables not supported

For tables with special requirements (merged cells, custom widths), use HTML-to-PDF.

#### Other Limitations

- **No cross-references**: Equation numbering and `\ref{}` not supported.
- **No complex environments**: `\begin{align}`, `\begin{equation}`, `\begin{gather}` not supported — use separate `$$...$$` blocks.
- **Font**: Uses matplotlib's default math font (not Calibri or DejaVu).
- **Very long expressions** (>200 chars): May break across lines incorrectly.

---

## Script

### Bundled Script

`scripts/build_pdf.py` — v1.1 (2026-06-03)

The script is bundled in this skill's `scripts/` directory and is the primary
execution path. It is also backed up to R2 at `qnfo/tools/build_pdf.py`.

### Dependencies

| Package | Version | Purpose |
|:--------|:--------|:--------|
| `reportlab` | ≥4.0 | PDF generation |
| `matplotlib` | ≥3.5 | Math rendering (mathtext) |
| `markdown` | ≥3.0 | Markdown→HTML parsing (optional, fallback available) |
| `pymupdf` (fitz) | ≥1.20 | PDF text extraction for verification |

### Arguments

| Flag | Required | Description |
|:-----|:---------|:------------|
| `--input`, `-i` | Yes | Input file (.md or .html) |
| `--output`, `-o` | Yes | Output PDF file path |
| `--title`, `-t` | No | Publication title (auto-detected from first H1) |
| `--author`, `-a` | No | Author name |
| `--date`, `-d` | No | Publication date (YYYY-MM-DD, defaults to today) |
| `--no-math` | No | Skip math rendering, use Unicode approximations |
| `--check-unicode` | No | Scan input for `\uXXXX` escapes (no PDF build) |
| `--fix-unicode` | No | Auto-correct `\uXXXX` escapes in place |

---

## Reference Files

| File | Purpose |
|:-----|:--------|
| `references/math-rendering.md` | Math rendering limitations, LaTeX→Unicode table, troubleshooting |
| `references/publication-stylesheet.json` | Centralized publication styles (typography, layout, colors) |
| `scripts/build_pdf.py` | The bundled PDF builder script (v1.4 with table rendering + math pre-processing + YAML frontmatter + stylesheet support) |

---

## Alternative: HTML-to-PDF for Complex Documents

**When pdf-builder cannot handle your document** (tables, complex LaTeX, `\bmod`,
`\operatorname`, etc.), build the PDF from the HTML render instead. Modern browsers
render MathJax + HTML tables perfectly — capture that.

### Decision Flow (v1.4)

```
Does document use \begin{align}, \begin{equation}, \begin{gather}? ──YES──→ Use HTML-to-PDF
Does document use \tag, \label, \ref with cross-references? ──YES──→ Use HTML-to-PDF
Does document use custom LaTeX packages (\ce, \si, tikz, etc.)? ──YES──→ Use HTML-to-PDF
Otherwise ──→ pdf-builder is suitable (tables, \bmod, \operatorname, \bm all supported)
```

### Rendering Verification (always works)

Before building the actual PDF, verify the HTML renders correctly using CDP:

```bash
# 1. Start local HTTP server (if not already deployed to Pages)
$server = Start-Process python -ArgumentList '-m','http.server','8765' -PassThru
load_url("http://localhost:8765/_test-pdf-html.html")
# Wait 3-5 seconds for MathJax rendering

# 2. Verify via DOM — confirm math rendered, tables intact
Runtime.evaluate: document.querySelectorAll('mjx-container').length
# Should show 30+ containers with zero MathJax errors

# 3. Capture screenshot for visual verification
cdp_send(method="Page.captureScreenshot", params={"format":"png"})
# Verify: no raw \bmod, no raw | pipes, no \operatorname
```

### Method A: playwright (RECOMMENDED — cross-platform, bundled Chromium)

```bash
# One-time setup
pip install playwright
playwright install chromium

# Build PDF from local HTML file
python -c "
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto('file:///qnfo/prompts/_test-pdf-html.html')
    page.wait_for_function('() => document.querySelectorAll(\"mjx-container\").length > 30', timeout=15000)
    page.pdf(path='output.pdf', format='A4', margin={'top':'0.5in','bottom':'0.5in','left':'0.5in','right':'0.5in'})
    browser.close()
    print('[OK] PDF built via playwright')
"
```

### Method B: weasyprint (Linux/macOS native, needs GTK on Windows)

```bash
pip install weasyprint

# From local file (must be absolute path with file://)
python -c "
from weasyprint import HTML
HTML(filename='_test-pdf-html.html').write_pdf('output.pdf')
print('[OK] PDF built via weasyprint')
"
```

> **Windows note:** weasyprint requires GTK3 runtime (`libgobject-2.0-0`).
> Install via MSYS2 or use Method A (playwright) instead.

### Method C: wkhtmltopdf (Windows standalone)

```bash
# Download from https://wkhtmltopdf.org/downloads.html
# Then:
wkhtmltopdf --page-size A4 --margin-top 12mm --margin-bottom 12mm ^
    --javascript-delay 5000 _test-pdf-html.html output.pdf
```

### Verification Gate (Same for All Methods)

```bash
python -c "
import fitz, sys
doc = fitz.open(sys.argv[1])
text = ''.join(page.get_text() for page in doc)
issues = []
if '\ufffd' in text:
    issues.append('Unicode replacement characters')
if '|' in text and '|---' in text:
    issues.append('Raw markdown table pipes in output')
if 'MATH RENDER ERROR' in text:
    issues.append('Math rendering errors')
if r'\bmod' in text or r'\text' in text:
    issues.append('Raw LaTeX commands in output')
if issues:
    print('[BLOCKED]', '; '.join(issues))
else:
    print('[OK] PDF verified — no rendering issues')
doc.close()
" output.pdf
```

### Quick Test Result (2026-06-04 verification)

| Feature | pdf-builder v1.4 (mathtext) | HTML-to-PDF (MathJax + DOM) |
|:--------|:---------------------------:|:---------------------------:|
| `\bmod`, `\operatorname`, `\bm` | ✅ Auto-fixed by preprocessor | ✅ Renders natively |
| `\\text{...}` double backslash | ✅ Auto-fixed → single `\text` | ✅ Works (single \ in HTML) |
| `\pmod{...}` | ✅ Auto-fixed | ✅ Renders natively |
| Markdown tables | ✅ Rendered via reportlab Table | ✅ HTML tables intact |
| Inline math in table cells | ✅ Rendered as math images | ✅ Renders natively |
| `\begin{align}`, `\begin{equation}` | ❌ Not supported | ✅ Renders natively |
| Standard LaTeX ($E=mc^2$, $$\hat{H}$$) | ✅ Works | ✅ Works |
| MathJax containers | N/A | 37 containers, 0 errors |

**Verdict (v1.4):** pdf-builder now handles tables, common LaTeX commands, and inline math
in table cells. HTML-to-PDF is still recommended for documents using complex math
environments (`\begin{align}`, cross-references) or custom LaTeX packages.

---

## Cross-References

- Used by: `publication-publisher` skill (Step 2: Build PDF)
- Related: `cloudflare-deployer` skill (post-PDF deployment)
- Deprecates: `templates/PDF-BUILDER-TEMPLATE.md`

---

*pdf-builder v1.4 — Markdown table rendering + LaTeX math pre-processing + YAML frontmatter support. Tested 2026-06-06.*

## RT: RED-TEAM SELF-AUDIT

Before claiming this skill complete, autonomously run:

1. Output Verification (negative verification)
2. Assumption Challenge (state and test every assumption)
3. Edge Case Check (empty/null/max/boundary/desync)
4. DoD Integration (run _dod_enforce.py if exists)
5. Iteration (retry on failure, max 3)

ANTI-PATTERN: User should NEVER ask about quality.
Refer to RED-TEAM-PROTOCOL.md for full protocol.

