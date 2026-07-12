---
name: pdf-builder
description: Build publication-quality PDFs from Markdown files using Pandoc+XeLaTeX for proper TeX typesetting with full LaTeX math rendering. Use when the agent needs to convert .md to .pdf for QNFO publications, papers, or reports. XeLaTeX ONLY — no reportlab or HTML fallbacks permitted for publications.
version: "4.2"
---
> **INCLUDES AUTONOMOUS RED-TEAM SELF-AUDIT.** Before claiming this skill complete, autonomously run: (1) Output Verification -- negative verification. (2) Assumption Challenge -- state and test every assumption. (3) Edge Case Check -- empty/null/max/boundary/desync. (4) DoD Integration -- run _dod_enforce.py if exists. (5) Iteration -- retry on failure, max 3. ANTI-PATTERN: User should NEVER ask about quality.


### Domain Self-Critique (Post-Execution)

After every PDF build, autonomously verify:
- **Silent fallback check:** Did pandoc silently fall back from XeLaTeX? Check stderr for "xelatex not found" or "falling back to pdflatex."
- **Font availability:** Are Computer Modern / Latin Modern fonts installed? Test-Path the TeX Live font directories.
- **Output validity:** Is the output actually a valid PDF? Check first bytes for "%PDF-" header.
- **Math rendering:** Do NOT trust that math rendered correctly. Open the PDF and visually spot-check at least 3 equations.
- **Embedded vs. raster:** Are equations true vector TeX or rasterized fallback images? Check file size — rasterized math inflates PDFs 5-10x.

> **Related:** publication-publisher



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

## execute_plan (MANDATORY -- Before Any Execution)

**This skill involves execution-heavy workflows.** Before executing, use update_plan to populate a concrete, verifiable checklist. Every item must be short, specific, and testable with tool evidence.

### Execution Protocol

1. **Populate update_plan** with workflow phases as concrete checklist items
2. **Execute one item at a time** -- at most ONE in_progress
3. **Mark items completed ONLY with tool evidence** (Test-Path, exec output, git log)
4. **Never claim completion without execution evidence** -- Rule 14 enforcement
5. **If blocked:** Flag as [BLOCKED: reason] and move to the next item

### Example Plan

update_plan([
  {"step": "Read canonical Markdown source", "status": "pending"},
  {"step": "Convert to PDF via matplotlib mathtext/LaTeX", "status": "pending"},
  {"step": "Verify math rendering (no \ufffd characters)", "status": "pending"},
  {"step": "Verify em dashes, curly quotes render correctly", "status": "pending"},
  {"step": "Output publication-quality PDF", "status": "pending"}
])


# PDF BUILDER SKILL — v4.0

> **Bundled skill.** All scripts and references are self-contained in this skill directory.
> Deployed via `_deploy.py` to `%USERPROFILE%\.deepchat\skills\pdf-builder\` (DeepChat runtime directory).

---

## Purpose

Convert Markdown (`.md`) files to **LaTeX-typeset, publication-quality PDFs**
with proper TeX math rendering (inline and block), Computer Modern fonts,
microtype-optimized typography, and CSS-styled HTML tables.

**v4.0 (2026-07-06):** 🔴 **PRIMARY pipeline is now Pandoc + XeLaTeX.** Proper TeX typesetting
with full LaTeX math, Computer Modern / Latin Modern fonts, microtype, and vector-quality output.
This is MANDATORY for all QNFO published papers. No fallbacks permitted — reportlab and HTML+MathJax+playwright pipelines are BLOCKED.

**v3.0 (deprecated, BLOCKED):** MD → HTML+CSS+MathJax → playwright PDF. BLOCKED for publications.
**v2.0 (deprecated, BLOCKED):** MD → HTML+CSS+MathJax → playwright PDF. BLOCKED for publications.
**v1.4 (legacy, BLOCKED):** reportlab + matplotlib mathtext. BLOCKED for publications.

---

## Quick Start

```bash
# 🔴 PRIMARY pipeline (Pandoc + XeLaTeX — REQUIRED for publications):
pandoc paper.md -o paper.pdf \
  --pdf-engine="C:\texlive\2025\bin\windows\xelatex.exe" \
  --from=markdown+tex_math_dollars+tex_math_single_backslash+smart \
  --standalone \
  -H _preamble.tex \
  -V documentclass=article -V papersize=a4 \
  -V geometry=margin=1in -V fontsize=11pt \
  -V colorlinks=true -V linkcolor=blue \
  --toc --metadata title="Paper Title"
```

### Prerequisites

```bash
# 🔴 PRIMARY pipeline (REQUIRED for publications):
# TeX Live 2025+ with XeLaTeX: https://tug.org/texlive/
# pandoc: https://pandoc.org/installing.html
# Verify: xelatex --version && pandoc --version
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
author: "Rowan Brad Quni-Gudzinas"
date: "2026-06-28"
license: "QNFO Unified License Agreement (QNFO-ULA)"
abstract: >
  This is the abstract. It can span multiple lines
  using YAML folded block scalar syntax (>).
---
```

---

## Architecture (v4.1)

```
┌─────────────────────────────────────────────────────────────────┐
│               🔴 PRIMARY PIPELINE (v4.1 — MANDATORY)              │
│                                                                  │
│  paper.md                                                        │
│     │                                                            │
│     ▼                                                            │
│  Pandoc ─── Parses Markdown + LaTeX math → intermediate TeX     │
│     │                                                            │
│     ▼                                                            │
│  XeLaTeX ─── Professional typesetting: Computer Modern fonts,   │
│     │        microtype, full LaTeX math, vector output, TOC      │
│     ▼                                                            │
│  paper.pdf (LaTeX-typeset, publication-quality, vector math)    │
│                                                                  │
├─────────────────────────────────────────────────────────────────┤
│  🔴 ALL OTHER PIPELINES BLOCKED for publications (v4.1):         │
│  • HTML+MathJax+playwright — browser-based, NOT TeX typesetting │
│  • reportlab — programmer-art, bitmap math, BLOCKED             │
│  If XeLaTeX unavailable → publication is BLOCKED. No fallbacks. │
└─────────────────────────────────────────────────────────────────┘
```

### Why XeLaTeX (Not Browser-Based Rendering)

Published papers require proper TeX typesetting — not browser-based approximations.
The Pandoc+XeLaTeX pipeline delivers what MathJax+playwright cannot:

| Aspect | 🔴 XeLaTeX (PRIMARY) | MathJax+playwright | reportlab |
|:-------|:--------------------:|:------------------:|:---------:|
| Font quality | ✅ Computer Modern vectors | ⚠️ Browser fonts | ❌ TTF registration |
| Math rendering | ✅ Native TeX (full LaTeX) | ⚠️ MathJax (JS-rendered) | ❌ mathtext subset |
| `\begin{align}` | ✅ Native | ✅ MathJax | ❌ |
| `\begin{cases}` | ✅ Native | ✅ MathJax | ❌ |
| Microtype | ✅ Character protrusion | ❌ | ❌ |
| Ligatures | ✅ fi, fl, ffi, ffl | ⚠️ Browser-dependent | ❌ |
| Hyphenation | ✅ TeX algorithm | ⚠️ Browser-dependent | ❌ |
| TOC / hyperlinks | ✅ Native | ⚠️ Manual | ❌ |
| Vector math | ✅ Type 1 / OpenType | ⚠️ HTML Canvas | ❌ Bitmap |
| Reproducibility | ✅ Deterministic | ⚠️ Browser-dependent | ✅ Deterministic |
| Publication standard | ✅ arXiv / journals | ❌ Not accepted | ❌ Not accepted |

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
# 🔴 PRIMARY pipeline prerequisites (REQUIRED for publications)
# Windows:
if (Test-Path "C:\texlive\2025\bin\windows\xelatex.exe") { Write-Output "xelatex: FOUND" } else { Write-Output "xelatex: MISSING — Install from https://tug.org/texlive/" ; exit 1 }
pandoc --version 2>$null | Select-Object -First 1

# Create preamble (required — amsmath, microtype, hyperref, LoF symbols)
echo "\usepackage{microtype}" > _preamble.tex
echo "\usepackage{amsmath,amssymb,amsfonts}" >> _preamble.tex
echo "\usepackage{hyperref}" >> _preamble.tex
echo "\providecommand{\rrcorner}{\ensuremath{\urcorner}}" >> _preamble.tex
```

### Step 2: Build PDF (🔴 PRIMARY — Pandoc + XeLaTeX)

```bash
# Detect xelatex path
# Windows: C:\texlive\2025\bin\windows\xelatex.exe
# Linux/Mac: /usr/bin/xelatex or `which xelatex`

pandoc paper.md -o PAPER-TITLE-v1.0.pdf \
  --pdf-engine="C:\texlive\2025\bin\windows\xelatex.exe" \
  --from=markdown+tex_math_dollars+tex_math_single_backslash+smart \
  --standalone \
  -H _preamble.tex \
  -V documentclass=article -V papersize=a4 \
  -V geometry=margin=1in -V fontsize=11pt \
  -V colorlinks=true -V linkcolor=blue \
  --toc --metadata title="Paper Title"
```

### Step 3: Verify Rendering (MANDATORY — LaTeX Gate)

```bash
# Run LaTeX Enforcement Gate
python -c "
import fitz, sys
pdf = 'PAPER-TITLE-v1.0.pdf'
doc = fitz.open(pdf)
text = ''.join(page.get_text() for page in doc)
has_ufffd = '\ufffd' in text

# Check for LaTeX fonts
latex_fonts = set()
for page in doc:
    for b in page.get_text('dict').get('blocks', []):
        if 'lines' in b:
            for l in b['lines']:
                for s in l['spans']:
                    f = s.get('font', '')
                    if any(k in f.lower() for k in ['lmroman','latinmodern','cmr','cmmi','cmsy','cmex','msam','msbm','lmmath']):
                        latex_fonts.add(f[:30])
doc.close()

is_latex = len(latex_fonts) > 0
is_reportlab = any(k in str(latex_fonts).lower() for k in ['helvetica','courier'])

if is_reportlab:
    print('[BLOCKED] PDF uses reportlab fonts — NOT LaTeX-typeset. Rebuild with Pandoc+XeLaTeX.')
    sys.exit(1)
elif not is_latex:
    print('[BLOCKED] No LaTeX fonts detected.')
    sys.exit(1)
elif has_ufffd:
    print('[BLOCKED] PDF contains Unicode replacement characters.')
    sys.exit(1)
else:
    print(f'[PASS] LaTeX-typeset: {len(latex_fonts)} LaTeX fonts, 0 ufffd')
"

# Clean up preamble
Remove-Item _preamble.tex -ErrorAction SilentlyContinue
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

The `references/papers.css` file provides professional academic styling. CSS is injected via the Pandoc `-H` flag (custom header) or `--css` flag:

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

## Pipeline Decision Flow (v4.1)

```
🔴 ALWAYS use Pandoc + XeLaTeX for published papers ──→ LaTeX-typeset output
  │
  ├── xelatex unavailable? ──→ Install TeX Live: https://tug.org/texlive/
  │
  ├── pandoc unavailable? ──→ Install: https://pandoc.org/installing.html
  │
  └── Both unavailable? ──→ 🔴 BLOCKED: publication cannot proceed until toolchain is installed
```

**🔴 HARD RULE:** The legacy reportlab pipeline and HTML+MathJax+playwright pipeline are **BLOCKED** for ALL QNFO publications.
Reportlab produces programmer-art PDFs with bitmap math, no align/cases/tag/ref, and
unacceptable typography. HTML+MathJax+playwright uses browser-based rendering (NOT TeX typesetting)
with browser fonts instead of Computer Modern, no microtype, and browser-dependent hyphenation.
If XeLaTeX is unavailable, the publication is BLOCKED until the toolchain is installed.

---

## 🔴 LaTeX Enforcement Gate (v4.0 — MANDATORY)

**Every published paper PDF MUST pass this gate. Non-LaTeX PDFs are BLOCKED.**

### Gate Check (Run After Every PDF Build)

```python
import fitz, sys, os

def verify_latex_typesetting(pdf_path: str) -> dict:
    """Verify a PDF was built with proper LaTeX typesetting."""
    doc = fitz.open(pdf_path)
    text = ''.join(page.get_text() for page in doc)

    # 1. Font check: Must contain LaTeX fonts (Latin Modern, Computer Modern, or AMS)
    latex_fonts = set()
    for page in doc:
        for b in page.get_text('dict').get('blocks', []):
            if 'lines' in b:
                for l in b['lines']:
                    for s in l['spans']:
                        font = s.get('font', '')
                        if any(k in font.lower() for k in
                               ['lmroman', 'latinmodern', 'cmr', 'cmmi', 'cmsy',
                                'cmex', 'msam', 'msbm', 'lmmath']):
                            latex_fonts.add(font[:30])
    doc.close()

    # 2. No Unicode replacement characters
    has_ufffd = '\ufffd' in text

    # 3. No reportlab fonts (Helvetica, Courier)
    is_reportlab = any(k in str(latex_fonts).lower()
                       for k in ['helvetica', 'courier'])

    passed = len(latex_fonts) > 0 and not is_reportlab and not has_ufffd
    return {
        'passed': passed,
        'latex_fonts': len(latex_fonts),
        'has_ufffd': has_ufffd,
        'is_reportlab': is_reportlab,
        'status': 'PASS' if passed else 'BLOCKED: Not LaTeX-typeset'
    }

# Usage:
result = verify_latex_typesetting('paper.pdf')
if not result['passed']:
    print(f"[BLOCKED] {result['status']}")
    sys.exit(1)
print(f"[PASS] LaTeX-typeset: {result['latex_fonts']} LaTeX fonts detected")
```

### Gate Criteria

| Criterion | Requirement | Block If |
|:----------|:------------|:---------|
| Font family | Latin Modern / Computer Modern / AMS | Helvetica, Courier, or other non-TeX fonts |
| Math rendering | Native TeX math (vector) | Bitmap/HTML math (reportlab/mathtext) |
| Unicode integrity | Zero `\ufffd` replacement chars | Any `\ufffd` present |
| Microtype | Character protrusion, ligatures | Missing (reportlab) |

### Pre-Flight Check (MANDATORY — before any publication PDF build)

```bash
# Verify TeX Live + pandoc are available
pandoc --version 2>&1 | head -1
xelatex --version 2>&1 | head -1

# Check preamble exists (required for LoF symbols, amsmath, microtype, hyperref)
Test-Path _preamble.tex
```

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

*pdf-builder v4.1 — 🔴 PRIMARY pipeline: Pandoc + XeLaTeX ONLY. Proper TeX typesetting with Computer Modern fonts, full LaTeX math, microtype, vector output, TOC. MANDATORY for all QNFO published papers. Reportlab and HTML+MathJax+playwright pipelines are BLOCKED for publications. No fallbacks. Tested 2026-07-06.*



---

## QNFO Design System Compliance (v3.0 — LOCKED 2026-07-01 — 2026-06-30)

**ALL QNFO/QWAV publications, pages, PDFs, and web artifacts MUST use the papers.qnfo.org canonical design (LOCKED v3.0).**

| Resource | Location |
|:---------|:---------|
| Design doc (full spec) | `qnfo/design-system/QNFO-DESIGN-SYSTEM.md` |
| PDF builder (v4.0) | Pandoc+XeLaTeX (PRIMARY) — see pdf-builder v4.0+ LaTeX Enforcement Gate |

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

> **Version:** (Kaizen-audited 2026-07-08)
