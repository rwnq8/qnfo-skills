---
name: publication-publisher
description: End-to-end publication workflow — formatting, PDF building (LaTeX-typeset via Pandoc+XeLaTeX ONLY — no reportlab/HTML fallbacks), complete artifact bundling, Zenodo upload (with robust retry + versioning + draft recovery via zenodo_api.py), Cloudflare deployment, social media orchestration, and post-publication draft cleanup.
version: "3.3"
---

### Programmatic Loading & Execution
This skill is loaded and executed **programmatically by the LLM system** 
during response generation. Loading is triggered automatically via 
`skill_view('publication-publisher')` or `read()` with filesystem path.
**The user NEVER manually loads this skill.** The `skill-autoloader` 
detects task patterns and handles all skill loading. If this skill fails 
to load, the LLM system automatically retries via the fallback chain 
documented below.
**Pinning:** This skill is [Priority 1 — auto-loads for relevant operations].

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
# PUBLICATION PUBLISHER SKILL — v3.2 — v3.2

> **INCLUDES AUTONOMOUS RED-TEAM SELF-AUDIT.** Before claiming this skill complete, autonomously run: (1) Output Verification -- negative verification. (2) Assumption Challenge -- state and test every assumption. (3) Edge Case Check -- empty/null/max/boundary/desync. (4) DoD Integration -- run _dod_enforce.py if exists. (5) Iteration -- retry on failure, max 3. ANTI-PATTERN: User should NEVER ask about quality.


### Domain Self-Critique (Post-Publication)

After every publication, autonomously verify:
- **DOI resolution:** Did the Zenodo DOI actually resolve? Wait 30s after publish, then curl https://doi.org/DOI and verify redirect to Zenodo record.
- **PDF-MD consistency:** Does the published PDF match the canonical Markdown? Diff the text content (not layout) between source .md and extracted .pdf text.
- **MathJax on deployed page:** Is MathJax actually loaded? Check deployed HTML for MathJax CDN script tag and verify it is not blocked by CSP.
- **Citation integrity:** Did any citations break during PDF conversion? Verify all citation references in source exist in the generated bibliography.
- **Artifact completeness:** Are ALL artifacts (paper.md, paper.pdf, PROVENANCE-BUNDLE.zip, README.md) present on both Zenodo and R2?

> **Related:** cloudflare-deployer, citation-manager, seo-discoverability

> **Phase 4–5 of LRAP.** Handles Zenodo deposition, Cloudflare Pages deployment, PDF generation, and artifact archival for QNFO/QWAV research publications.

---

## execute_plan (MANDATORY — Before Any Execution)

**This skill involves execution-heavy workflows.** Before executing, use update_plan to populate a concrete, verifiable checklist. Every item must be short, specific, and testable with tool evidence.

### Execution Protocol

1. **Populate update_plan** with workflow phases as concrete checklist items
2. **Execute one item at a time** — at most ONE in_progress
3. **Mark items completed ONLY with tool evidence** (Test-Path, exec output, git log)
4. **Never claim completion without execution evidence** — Rule 14 enforcement
5. **If blocked:** Flag as [BLOCKED: reason] and move to the next item

### Example Plan

update_plan([
  {"step": "Validate publication readiness (Language Gate, citations, provenance)", "status": "pending"},
  {"step": "Build PDF from canonical Markdown", "status": "pending"},
  {"step": "Generate HTML publication page with MathJax", "status": "pending"},
  {"step": "Stage 3.5: Assemble PROVENANCE BUNDLE (filesystem snapshot + conversation history)", "status": "pending"},
  {"step": "Create Zenodo deposition with metadata", "status": "pending"},
  {"step": "Upload ALL artifacts (paper.md, paper.pdf, PROVENANCE-BUNDLE.zip, README.md) to Zenodo", "status": "pending"},
  {"step": "Publish deposition and obtain DOI", "status": "pending"},
  {"step": "Deploy HTML page to Cloudflare Pages", "status": "pending"},
  {"step": "Verify MathJax on deployed page", "status": "pending"},
  {"step": "Upload artifacts to R2 canonical storage", "status": "pending"},
  {"step": "Generate SEO metadata for discoverability", "status": "pending"},
  {"step": "Update Discovery Index with new publication", "status": "pending"},
])

---

## Purpose

Publish QNFO/QWAV research publications through a verified pipeline: validate publication readiness, build PDF and HTML artifacts, deposit to Zenodo for DOI assignment, deploy HTML to Cloudflare Pages, archive canonical copies to R2, and register in the Discovery Index. Ensures every publication meets QNFO standards (Research Integrity Mandate, Publication Language Gate, MathJax verification).

## When to Use

| Trigger | Action |
|:--------|:-------|
| "Publish this paper" / "Publish to Zenodo" | Full publication pipeline |
| "Build PDF for [paper]" | PDF generation only |
| "Deploy to Cloudflare Pages" | Pages deployment only |
| "Generate HTML for [paper]" | HTML generation only |
| Phase 4–5 of LRAP | Automatic trigger via `research-orchestrator` |

## Prerequisites

1. **Zenodo Access Token** — stored at `%USERPROFILE%\.zenodo_token` (utf-8, no BOM) or in `$env:ZENODO_TOKEN`
2. **Cloudflare API Token** — stored at `$env:CLOUDFLARE_API_TOKEN`
3. **Publication passes all quality gates** — Language Gate (§7.1), citation audit, fabrication audit
4. **Canonical Markdown source** — the single source of truth from which PDF and HTML are generated
5. **Conversation History Accessible** — DeepChat session must have `get_conversation_history` available for provenance export
6. **Project Files Present** — working directory must contain project files for filesystem snapshot into provenance bundle

---

## Workflow — 7 Stages

### Stage 1: Pre-Publication Validation

Verify the publication meets QNFO standards:

```python
def validate_publication(md_path: str) -> dict:
    """Run all pre-publication quality gates on a Markdown paper."""
    results = {}
    
    # 1. Publication Language Gate — zero internal project language
    banned_terms = [
        "Module N", "Task N", "SPRINT", "PROCEED", "RESUME",
        "PROJECT STATE", "0.N.py", "0.N.md", "cp1252",
        "ready for handoff", "new agent starting from cold"
    ]
    with open(md_path, 'r', encoding='utf-8') as f:
        text = f.read()
    hits = {term: text.count(term) for term in banned_terms if term in text}
    results["language_gate"] = {
        "passed": len(hits) == 0,
        "violations": hits
    }
    
    # 2. Author block present
    results["author_block"] = {
        "passed": "**Author:**" in text and "**Date:**" in text and "**License:**" in text
    }
    
    # 3. Math in LaTeX delimiters (no bare Unicode math)
    bare_math_chars = ['α', 'β', 'γ', 'δ', 'ε', 'π', 'σ', '∞', '∑', '∫', '√', '≤', '≥', '≠']
    bare_hits = [c for c in bare_math_chars if c in text]
    results["math_format"] = {
        "passed": len(bare_hits) == 0,
        "violations": bare_hits
    }
    
    # 4. Citations present and verify
    import re
    citations = re.findall(r'\[@(\w+(?:[,;\s]+@\w+)*)\]', text)
    results["citations"] = {
        "count": len(citations),
        "passed": len(citations) > 0
    }
    
    # 5. Certainty labels present (≥5% of substantive paragraphs)
    paragraphs = [p for p in text.split('\n\n') if len(p.strip()) > 100]
    certainty_labels = ['[established]', '[speculative]', '[my conjecture]', '[debated]', 
                        '[mainstream interpretation]', '[not yet falsifiable]', '[PHILOSOPHY]',
                        '[LLM-INFERRED]']
    labeled = sum(1 for p in paragraphs if any(lbl in p for lbl in certainty_labels))
    label_ratio = labeled / max(len(paragraphs), 1)
    results["certainty_labels"] = {
        "count": labeled,
        "total_paragraphs": len(paragraphs),
        "ratio": round(label_ratio, 3),
        "passed": label_ratio >= 0.05
    }
    
    # 6. Provenance readiness (v2.6)
    import os
    results["provenance"] = {
        "conversation_available": True,  # Agent verifies at runtime
        "project_files_present": os.path.exists(".") and len(os.listdir(".")) > 0,
        "passed": True  # Agent overrides if conversation history unavailable
    }
    
    all_passed = all(v["passed"] for v in results.values())
    results["overall"] = "PASS" if all_passed else "FAIL"
    return results
```

**GATE:** All validation gates must PASS before proceeding. If any gate FAILS → `[BLOCKED: publication not ready]`.

### Stage 2: PDF Generation — MANDATORY (v2.5 — 2026-07-05)

> **🔴 MANDATORY GATE:** PDF generation is **NOT optional.** Every publication MUST include a professionally rendered PDF alongside the Markdown source. Publications without PDFs are BLOCKED at this gate. This gate was added after a session where 5 papers were published without PDFs, requiring retroactive generation and Zenodo new versions.

> **Design System v2.5 (2026-07-05):** Two PDF pipelines available.
> 1. **Pandoc + XeLaTeX (PREFERRED)** — Professional typography with Computer Modern fonts, microtype, and full LaTeX math rendering. Produces publication-quality PDF with vector math, TOC, hyperlinks. Requires TeX Live 2025+ and pandoc on PATH.
> 2. **build_pdf.py (FALLBACK)** — Lightweight reportlab-based builder with QNFO Silent Radix Light Theme. No external dependencies beyond Python packages.

> **Pre-Flight Check (MANDATORY — before any publication):**
> ```bash
> # Check pandoc + xelatex availability
> pandoc --version 2>&1
> Test-Path "C:\texlive\2025\bin\windows\xelatex.exe"  # Windows
> # If pandoc unavailable: fall back to build_pdf.py (reportlab)
> ```

> **Professional PDF via Pandoc+XeLaTeX (direct invocation):**
> ```bash
> # Create preamble (required — see below for LoF symbol support)
> echo "\usepackage{microtype}" > _preamble.tex
> echo "\usepackage{amsmath,amssymb,amsfonts}" >> _preamble.tex
> echo "\usepackage{hyperref}" >> _preamble.tex
> echo "% Spencer-Brown Laws of Form symbols (required for \lrcorner/\rrcorner)" >> _preamble.tex
> echo "\providecommand{\rrcorner}{\ensuremath{\urcorner}}" >> _preamble.tex
>
> # Generate PDF
> pandoc paper.md -o paper.pdf \
>   --pdf-engine="C:\texlive\2025\bin\windows\xelatex.exe" \
>   --from=markdown+tex_math_dollars+tex_math_single_backslash+smart \
>   --standalone \
>   -H _preamble.tex \
>   -V documentclass=article -V papersize=a4 \
>   -V geometry=margin=1in -V fontsize=11pt \
>   -V colorlinks=true -V linkcolor=blue \
>   --toc --metadata title="Paper Title"
> ```
> **LoF Symbol Note:** Papers using Spencer-Brown cross symbols (`\lrcorner`/`\rrcorner`) MUST include `\providecommand{\rrcorner}{\ensuremath{\urcorner}}` in the preamble. `\lrcorner` is defined by amssymb; `\rrcorner` is NOT standard and requires this definition. Without it, pandoc+XeLaTeX will fail with "Undefined control sequence."

> **TeX Live Detection:** Check `C:\texlive\2025\bin\windows\xelatex.exe` (Windows) or use `Get-Command xelatex` for cross-platform detection (Linux/Mac). If not found, **BLOCK publication** — do NOT fall back to reportlab or HTML pipelines. Install from https://tug.org/texlive/.

Build PDF from canonical Markdown using Pandoc+XeLaTeX **ONLY**. No fallback permitted — reportlab and HTML+MathJax+playwright pipelines are **BLOCKED** for publications. If XeLaTeX is unavailable, the publication is BLOCKED until TeX Live is installed.

```bash
# 🔴 VERIFY LATEX TOOLCHAIN FIRST (gate BEFORE build — v3.3)
$XELATEX = $null
if (Test-Path "C:\texlive\2025\bin\windows\xelatex.exe") {
    $XELATEX = "C:\texlive\2025\bin\windows\xelatex.exe"
} elseif (Get-Command xelatex -ErrorAction SilentlyContinue) {
    $XELATEX = (Get-Command xelatex).Source
}

if (-not $XELATEX) {
    Write-Error "[BLOCKED] TeX Live + XeLaTeX required for publication PDF. Install from https://tug.org/texlive/"
    exit 1
}

# Generate publication-quality LaTeX PDF
pandoc paper.md -o PAPER-TITLE-v1.0.pdf --pdf-engine="$XELATEX" --from=markdown+tex_math_dollars+tex_math_single_backslash+smart --standalone -H _preamble.tex -V documentclass=article -V papersize=a4 -V geometry=margin=1in -V fontsize=11pt -V colorlinks=true -V linkcolor=blue --toc --metadata title="Paper Title"

# Verify PDF exists and is non-empty
Test-Path PAPER-TITLE-v1.0.pdf
```

**PDF Verification (MANDATORY — 🔴 LaTeX Enforcement Gate):**

```python
# LaTeX Enforcement Gate (from pdf-builder v4.0)
import fitz, sys

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

result = verify_latex_typesetting("PAPER-TITLE-v1.0.pdf")
if not result['passed']:
    print(f"[BLOCKED] {result['status']}")
    sys.exit(1)
print(f"[PASS] LaTeX-typeset: {result['latex_fonts']} LaTeX fonts, 0 ufffd")
```

**GATE (🔴 LaTeX Enforcement):** PDF must:
- Use LaTeX fonts (Latin Modern / Computer Modern / AMS) — NOT reportlab fonts (Helvetica/Courier)
- Have zero `\ufffd` Unicode replacement characters
- Be typeset with Pandoc+XeLaTeX for publications (reportlab is BLOCKED for publications)
**If PDF verification fails → publication is BLOCKED. Do NOT proceed to Zenodo or Pages without a verified LaTeX-typeset PDF.**

### Stage 3: HTML Publication Page Generation

Generate HTML from canonical Markdown using the `HTML-PUBLICATION-PAGE` template:

```python
def generate_html(md_path: str, metadata: dict) -> str:
    """Generate publication HTML page from Markdown source."""
    import markdown
    
    with open(md_path, 'r', encoding='utf-8') as f:
        md_text = f.read()
    
    # Convert Markdown to HTML body
    html_body = markdown.markdown(md_text, extensions=['extra', 'codehilite', 'tables'])
    
    # MathJax configuration — MUST come before the MathJax script
    mathjax_config = """
    <script>
    window.MathJax = {
      tex: {
        inlineMath: [['$', '$'], ['\\\\(', '\\\\)']],
        displayMath: [['$$', '$$'], ['\\\\[', '\\\\]']],
        macros: {
          "\\R": "\\mathbb{R}",
          "\\Q": "\\mathbb{Q}",
          "\\Z": "\\mathbb{Z}",
          "\\N": "\\mathbb{N}",
          "\\C": "\\mathbb{C}",
          "\\F": "\\mathbb{F}",
          "\\Qp": "\\mathbb{Q}_p",
          "\\Zp": "\\mathbb{Z}_p",
          "\\cA": "\\mathcal{A}",
          "\\cC": "\\mathcal{C}",
          "\\cB": "\\mathcal{B}"
        }
      },
      options: {
        ignoreHtmlClass: 'no-mathjax',
        processHtmlClass: 'mathjax-process'
      },
      chtml: {
        displayAlign: 'left'
      }
    };
    </script>
    <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
    """
    
    # Build complete HTML
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{metadata['title']}</title>
    <meta name="citation_title" content="{metadata['title']}">
    <meta name="citation_author" content="{metadata['author']}">
    <meta name="citation_publication_date" content="{metadata['date']}">
    <meta name="citation_doi" content="{metadata.get('doi', '')}">
    <link rel="stylesheet" href="https://qnfo.org/design-system/qnfo-light.css">
    {mathjax_config}
</head>
<body>
    <header>
        <h1>{metadata['title']}</h1>
        <div class="author-block">
            <p><strong>Author:</strong> {metadata['author']} | <strong>Date:</strong> {metadata['date']} | <strong>License:</strong> QNFO-ULA</p>
            {f'<p><strong>DOI:</strong> <a href="https://doi.org/{metadata["doi"]}">{metadata["doi"]}</a></p>' if metadata.get('doi') else ''}
        </div>
    </header>
    <main>
        {html_body}
    </main>
    <footer>
        <p><em>Published under the QNFO Unified License Agreement. See <a href="https://legal.qnfo.org/">legal.qnfo.org</a>.</em></p>
    </footer>
</body>
</html>"""
    
    return html
```

**CRITICAL:** MathJax config MUST come BEFORE the `<script id="MathJax-script">` tag. Verify:
```bash
# Verify MathJax config ordering — write check script, execute, discard
echo "import sys; html=open('index.html','r',encoding='utf-8').read(); c=html.find('window.MathJax'); s=html.find('MathJax-script'); sys.exit(0 if c>=0 and s>=0 and c<s else 1)" > _verify_mathjax.py
python _verify_mathjax.py
Remove-Item _verify_mathjax.py
```

**GATE:** MathJax config must be before MathJax script in the generated HTML.

### Stage 3.5: Provenance Bundle Assembly — MANDATORY (v2.6 — 2026-07-05)

> **🔴 MANDATORY GATE (v2.6):** Zenodo publication records MUST contain the FULL project record/filesystem AND LLM conversation history for provenance and reproducibility — NOT just the final paper/release documents. This gate was mandated 2026-07-05. Publications without a provenance bundle are BLOCKED at Zenodo upload.

#### 3.5a. What the Provenance Bundle Contains

The `PROVENANCE-BUNDLE.zip` is a complete record of HOW the research was conducted:

| Component | Source | Format | Purpose |
|:----------|:-------|:-------|:--------|
| **Conversation History** | DeepChat session (via `get_conversation_history`) | `conversation.md` | Full LLM-agent dialogue that produced the research |
| **Session Metadata** | `tape_info` + system state | `session-metadata.json` | Agent, model, timestamps, tool invocation count, execution ratio |
| **Project Filesystem Snapshot** | Working directory (ephemeral project files) | `project-files/` directory | All scripts, data, intermediate outputs used during research |
| **Git State** | `git log`, `git diff`, `git status` | `git-state.txt` | Branch, commits, diff from `main` |
| **README.md** | Auto-generated | `README.md` | Human-readable entry point — what this is, how to navigate, how to reproduce |
| **Provenance Manifest** | Auto-generated | `PROVENANCE.md` | Human-readable index of all bundle contents + chain of custody |

#### 3.5b. Assembly Protocol

Execute ALL of these steps. The bundle is assembled in a temporary `_provenance/` directory, zipped, and cleaned up after Zenodo upload.

**Step 1: Export Conversation History**

```python
# _export_conversation.py — ephemeral, delete after execution
import json, os
from datetime import datetime, timezone

# The agent MUST call get_conversation_history for the current session
# This tool returns the complete conversation.
# Write the output to conversation.md

# Pseudo-code (the agent uses the actual get_conversation_history tool):
# history = get_conversation_history(conversationId="<current>", includeSystem=False)
# Format as Markdown with role headers

output = []
output.append(f"# QNFO Research Session — Conversation History")
output.append(f"")
output.append(f"**Exported:** {datetime.now(timezone.utc).isoformat()}")
output.append(f"**Session ID:** <session-id>")
output.append(f"")
output.append("---")
output.append("")

for msg in history["messages"]:
    role = msg["role"].upper()
    content = msg["content"]
    timestamp = msg.get("timestamp", "")
    output.append(f"## {role} ({timestamp})")
    output.append("")
    output.append(content)
    output.append("")
    output.append("---")
    output.append("")

with open("_provenance/conversation.md", "w", encoding="utf-8") as f:
    f.write("\n".join(output))
print("[OK] conversation.md written")
```

**Step 2: Capture Session Metadata**

```python
# _capture_metadata.py — ephemeral
import json, os, subprocess
from datetime import datetime, timezone

metadata = {
    "export_timestamp": datetime.now(timezone.utc).isoformat(),
    "session_id": "<session-id>",
    "agent": "QNFO Research Agent (DEFAULT-DEEPSEEK)",
    "model": "<model-id>",
    "conversation_id": "<conversation-id>",
    "git_branch": subprocess.run(["git", "branch", "--show-current"], capture_output=True, text=True).stdout.strip(),
    "git_commit": subprocess.run(["git", "log", "-1", "--oneline"], capture_output=True, text=True).stdout.strip(),
    "project": "<project-name>",
    "publication_title": "<paper-title>",
    "publication_version": "<version>",
}

with open("_provenance/session-metadata.json", "w", encoding="utf-8") as f:
    json.dump(metadata, f, indent=2, ensure_ascii=False)
print("[OK] session-metadata.json written")
```

**Step 3: Snapshot Project Filesystem**

```bash
# Create project-files directory and copy all ephemeral project files
# Exclude: .git/, _provenance/, __pycache__/, *.pdf (the final PDF is uploaded separately)
mkdir _provenance/project-files

# Copy all project-relevant files (scripts, data, intermediate outputs)
# Use robocopy on Windows, cp on Linux/Mac
robocopy . _provenance\project-files /E /XF *.pdf /XD .git _provenance __pycache__ /NFL /NDL /NJH /NJS

# Or for Git Bash / WSL:
# find . -not -path './.git/*' -not -path './_provenance/*' -not -path './__pycache__/*' -not -name '*.pdf' -type f -exec cp --parents {} _provenance/project-files/ \;
```

**Step 4: Capture Git State**

```bash
# Write git log, diff, and status
git log --oneline --graph --all -20 > _provenance/git-state.txt
echo "---" >> _provenance/git-state.txt
git diff main --stat >> _provenance/git-state.txt 2>&1
echo "---" >> _provenance/git-state.txt
git status --short >> _provenance/git-state.txt
```

**Step 5: Write Provenance Manifest**

```python
# _write_manifest.py — ephemeral
manifest = f"""# Provenance Manifest — {{{{paper_title}}}} v{{{{version}}}}

## Chain of Custody

1. **Research conducted:** {{{{date_range}}}}
2. **Agent:** QNFO Research Agent (DEFAULT-DEEPSEEK v3.30+)
3. **Conversation exported:** {{{{export_timestamp}}}}
4. **Zenodo deposition:** {{{{doi}}}} (assigned after upload)

## Bundle Contents

| File | Description | Size |
|:-----|:------------|:-----|
| `conversation.md` | Full LLM-agent conversation history | — |
| `session-metadata.json` | Agent, model, timestamps, git state | — |
| `project-files/` | Complete project filesystem snapshot | — |
| `git-state.txt` | Git log, diff, and status at publication time | — |
| `PROVENANCE.md` | This manifest | — |

## Reproducibility Notes

- The conversation history records every prompt, tool invocation, and agent response.
- The project filesystem snapshot preserves all working scripts and data.
- Together, these enable independent verification of the research process.
- The final paper (`{{{{paper_slug}}}}.md` and `{{{{paper_slug}}}}.pdf`) are uploaded separately alongside this bundle.

## Verification

To verify this research:
1. Read `conversation.md` to understand the research dialogue
2. Examine `project-files/` for all working code and data
3. Cross-reference claims in the paper against the conversation and code
4. Check `git-state.txt` for the exact commit state at publication time
"""

with open("_provenance/PROVENANCE.md", "w", encoding="utf-8") as f:
    f.write(manifest)
print("[OK] PROVENANCE.md written")
```

**Step 5.5: Generate README.md for the bundle (v2.6 — 2026-07-05)**

The README is the first thing a visitor sees when opening the Zenodo record. It must provide a clear entry point: what this research is, how to navigate the artifacts, and how to reproduce the work.

```python
# _generate_readme.py — ephemeral
readme = f"""# {{{{paper_title}}}} — v{{{{version}}}}

**DOI:** {{{{doi}}}} (assigned after Zenodo deposition)
**Author:** {{{{author}}}}
**Date:** {{{{date}}}}
**License:** QNFO Unified License Agreement (QNFO-ULA)
**GitHub:** {{{{github_repo_url}}}}

## What This Is

{{{{one_paragraph_abstract}}}}

## Repository Contents

| File | Description |
|:-----|:------------|
| `{{{{paper_slug}}}}.md` | Canonical Markdown source |
| `{{{{paper_slug}}}}.pdf` | Rendered PDF |
| `PROVENANCE-BUNDLE.zip` | Full project filesystem + conversation history |
| **Inside the bundle:** | |
| `conversation.md` | Full LLM-agent dialogue |
| `session-metadata.json` | Agent, model, git state |
| `project-files/` | All working scripts and data |
| `git-state.txt` | Git log at publication time |
| `PROVENANCE.md` | Chain of custody manifest |
| `README.md` | This file |

## Quick Start

### Read the Paper
Open `{{{{paper_slug}}}}.md` (Markdown) or `{{{{paper_slug}}}}.pdf` (rendered).

### Verify Reproducibility
1. Unzip `PROVENANCE-BUNDLE.zip`
2. Read `PROVENANCE.md` for the chain of custody
3. Read `conversation.md` for the research dialogue
4. Examine `project-files/` for all working code
5. Cross-reference claims against the conversation and code

### Version-Controlled Repository
The complete version-controlled git repository is available at:
{{{{github_repo_url}}}}

This repository contains the full commit history, branches, and all development artifacts.

## Citation

```bibtex
@{{{{bibtex_type}}}}{{{{{{citation_key}}}}},
  author = {{{{{{author}}}}}},
  title = {{{{{{{paper_title}}}}}}},
  year = {{{{{{year}}}}}},
  doi = {{{{{{doi}}}}}},
  publisher = {{Zenodo}},
  note = {{QNFO/QWAV Research Publication}}
}
```

## Provenance

This research was conducted by a QNFO Research Agent (DEFAULT-DEEPSEEK). The full conversation history, project filesystem snapshot, and git state are preserved in `PROVENANCE-BUNDLE.zip`. See `PROVENANCE.md` inside the bundle for the complete chain of custody.

## License

QNFO Unified License Agreement (QNFO-ULA): https://legal.qnfo.org/
"""

with open("_provenance/README.md", "w", encoding="utf-8") as f:
    f.write(readme)
print("[OK] README.md written")
```

**GATE:** README.md must exist inside `_provenance/` before creating the zip bundle.

**Step 6: Create Zip Bundle**

```bash
# Create the zip
python -c "import shutil; shutil.make_archive('PROVENANCE-BUNDLE', 'zip', '_provenance')"
# Verify
python -c "import zipfile, os; z=zipfile.ZipFile('PROVENANCE-BUNDLE.zip'); print(f'Bundle: {len(z.namelist())} files, {os.path.getsize(\"PROVENANCE-BUNDLE.zip\")} bytes'); z.close()"
```

**Step 7: Clean up temp directory**

```bash
Remove-Item -Recurse -Force _provenance
# Script cleanup
Remove-Item _export_conversation.py, _capture_metadata.py, _write_manifest.py, _generate_readme.py -ErrorAction SilentlyContinue
```

**GATE:** `PROVENANCE-BUNDLE.zip` must exist and be non-empty (≥1KB) before proceeding to Stage 4. If assembly fails → `[BLOCKED: provenance bundle assembly failed]`. Do NOT proceed to Zenodo without a verified provenance bundle.

#### 3.5c. Size Considerations

Zenodo has a 50GB per-record limit. For most QNFO publications, the provenance bundle will be <10MB (conversation text + small project files). If the bundle exceeds 50MB:
- Exclude large binary files (model weights, datasets) — reference them by external DOI/URL instead
- Compress conversation history by removing redundant tool output (keep first occurrence only)
- Flag in PROVENANCE.md what was excluded and why

### Stage 4: Zenodo Deposition (Robust — via `zenodo_api.py`)

Use the robust `zenodo_api.py` utility for all Zenodo operations. This replaces the fragile inline API calls with retry logic, exponential backoff, draft recovery, and proper `resource_type` metadata handling.

#### 4a. Create new deposition (with MANDATORY PDF + PROVENANCE BUNDLE + README + GitHub link + ALL related Zenodo records):

```bash
# Build metadata JSON with GitHub repo link + ALL related Zenodo DOIs via related_identifiers
# PDF, PROVENANCE BUNDLE, README, and cross-references are ALL MANDATORY
# Agent MUST query Knowledge Graph, Discovery Index, and D1 for related papers to populate related_identifiers
echo "{\"title\": \"Paper Title\", \"upload_type\": \"publication\", \"publication_type\": \"workingpaper\", \"description\": \"Abstract...\", \"creators\": [{\"name\": \"Author Name\", \"affiliation\": \"QWAV / QNFO\"}], \"access_right\": \"open\", \"license\": \"CC-BY-4.0\", \"version\": \"1.0.0\", \"related_identifiers\": [{\"relation\": \"isSupplementedBy\", \"identifier\": \"https://github.com/qnfo/<repo>\", \"resource_type\": \"software\"}, {\"relation\": \"isNewVersionOf\", \"identifier\": \"10.5281/zenodo.<prior-version>\", \"resource_type\": \"publication\"}, {\"relation\": \"cites\", \"identifier\": \"10.5281/zenodo.<related-paper-doi>\", \"resource_type\": \"publication\"}]}" > _zenodo_meta.json

# Create deposition, upload ALL FOUR files (PDF + PROVENANCE BUNDLE + README are MANDATORY)
python _zenodo_api.py create --token-file ZENODO_TOKEN --metadata _zenodo_meta.json --files paper.md,paper.pdf,PROVENANCE-BUNDLE.zip,README.md

# Clean up
Remove-Item _zenodo_api.py, _zenodo_meta.json
```

#### 4b. Create new version of existing deposition:

```bash
# Use embedded zenodo_api.py (self-contained — copy from Embedded Scripts section above)

# Create new version of existing DOI
python _zenodo_api.py new-version --token-file ZENODO_TOKEN --deposition-id 12345 --metadata _zenodo_meta.json --files expanded-paper.md

# Clean up
Remove-Item _zenodo_api.py
```

#### 4c. Recovery from stranded draft:

```bash
# If a previous publish attempt left an orphaned draft:
python _zenodo_api.py recover --token-file ZENODO_TOKEN --deposition-id 12345 --metadata _zenodo_meta.json --files paper.md,paper.pdf,PROVENANCE-BUNDLE.zip,README.md
```

This automatically: lists drafts, removes files from orphaned drafts, deletes orphaned drafts, creates a fresh new version, uploads files, and publishes.

#### 4d. List all drafts:

```bash
python _zenodo_api.py list-drafts --token-file ZENODO_TOKEN
```

```python
def create_zenodo_deposition(metadata: dict, files: list[str], token: str) -> dict:
    """Create and publish a Zenodo deposition."""
    import urllib.request, json
    
    BASE = "https://zenodo.org/api"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # 1. Create deposition
    dep_metadata = {
        "metadata": {
            "title": metadata["title"],
            "upload_type": "publication",
            "publication_type": metadata.get("publication_type", "workingpaper"),
            "description": metadata.get("description", ""),
            "creators": metadata.get("creators", [
                {"name": "Rowan Brad Quni-Gudzinas", "affiliation": "QWAV / QNFO"}
            ]),
            "keywords": metadata.get("keywords", []),
            "license": metadata.get("license", "CC-BY-4.0"),
            "access_right": "open",
            "version": metadata.get("version", "1.0.0")
        }
    }
    
    req = urllib.request.Request(
        f"{BASE}/deposit/depositions",
        data=json.dumps(dep_metadata).encode("utf-8"),
        headers=headers,
        method="POST"
    )
    resp = json.loads(urllib.request.urlopen(req, timeout=30).read())
    deposition_id = resp["id"]
    bucket_url = resp["links"]["bucket"]
    
    # 2. Upload files
    for file_path in files:
        file_name = file_path.split("/")[-1] if "/" in file_path else file_path.split("\\")[-1]
        with open(file_path, "rb") as f:
            data = f.read()
        
        upload_url = f"{bucket_url}/{file_name}"
        upload_headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/octet-stream"
        }
        req = urllib.request.Request(upload_url, data=data, headers=upload_headers, method="PUT")
        urllib.request.urlopen(req, timeout=60)
    
    # 3. Publish
    req = urllib.request.Request(
        f"{BASE}/deposit/depositions/{deposition_id}/actions/publish",
        headers=headers,
        method="POST"
    )
    result = json.loads(urllib.request.urlopen(req, timeout=30).read())
    
    return {
        "doi": result["doi"],
        "conceptdoi": result["conceptdoi"],
        "record_url": result["links"]["record"],
        "deposition_id": deposition_id
    }
```

**Token Setup:**
```bash
# Store Zenodo token (one-time setup)
# Write setup script to file, execute, discard
echo "import os; token = input('Zenodo Access Token: ').strip(); path = os.path.expandvars(r'%USERPROFILE%\\.zenodo_token'); open(path, 'w', encoding='utf-8').write(token); print('[OK] Zenodo token stored')" > _setup_zenodo_token.py
python _setup_zenodo_token.py
Remove-Item _setup_zenodo_token.py
```

### Stage 5: Cloudflare Pages Deployment

> ⚠️ **SCALING LIMIT (v2.5):** Cloudflare Pages has a 100-project limit per account. Static per-paper Pages deployments do NOT scale to hundreds of papers. For production scale (100+ papers), use one of the dynamic rendering approaches below. This stage is suitable for small-scale or individual publication deployments only.

**Dynamic Rendering Alternatives (for 100+ papers):**

| Approach | Complexity | Cost | Best For |
|:---------|:-----------|:-----|:---------|
| **Single Pages project + Worker** | Medium | $5/mo + usage | Dynamic routes: `/papers/<slug>` → Worker renders from D1 |
| **JS-side Markdown rendering** | Low | $0 | Single HTML page fetches `.md` from R2 via presigned URL, renders client-side |
| **API Worker** | Low | $0.15/M req | `GET /v2/papers/<slug>/html` → rendered HTML from D1 |

Deploy the HTML publication page to Cloudflare Pages:

```bash
# Create deployment directory
mkdir _pages_deploy
# Copy index.html and supporting assets
cp index.html _pages_deploy/
# CSS served from qnfo.org/design-system/qnfo-light.css (canonical)
# Copy any figures
cp -r figures _pages_deploy/ 2>$null
# Deploy
npx wrangler pages deploy _pages_deploy --project-name qnfo-publications --branch main
# Clean up
Remove-Item -Recurse _pages_deploy
```

**Post-Deploy Verification (MANDATORY):**
```bash
# Verify MathJax on the deployed page — write check script, execute, discard
echo "import urllib.request, sys; url = sys.argv[1]; html = urllib.request.urlopen(url).read().decode('utf-8'); c = html.find('window.MathJax'); s = html.find('MathJax-script'); assert c >= 0, 'MathJax config missing'; assert s >= 0, 'MathJax script missing'; assert c < s, 'Config AFTER script — math WILL NOT render'; print(f'[OK] MathJax verified: config@{c}, script@{s}')" > _verify_deployed_mathjax.py
python _verify_deployed_mathjax.py <deployed-url>
Remove-Item _verify_deployed_mathjax.py
```

### Stage 6: R2 Archival and SEO

Upload canonical artifacts to R2 and generate SEO metadata:

```bash
# Upload publication + provenance to R2
npx wrangler r2 object put qnfo/releases/2026/07/<paper-slug>/paper.md --file=<md-path>
npx wrangler r2 object put qnfo/releases/2026/07/<paper-slug>/paper.pdf --file=<pdf-path>
npx wrangler r2 object put qnfo/releases/2026/07/<paper-slug>/PROVENANCE-BUNDLE.zip --file=PROVENANCE-BUNDLE.zip
npx wrangler r2 object put qnfo/releases/2026/07/<paper-slug>/README.md --file=README.md
npx wrangler r2 object put qnfo/releases/2026/07/<paper-slug>/index.html --file=index.html

# Generate SEO artifacts (use embedded generate-seo.py from Embedded Scripts section)
python _generate-seo.py --url https://papers.qnfo.org/<paper-slug>/ --title "<paper title>"
# Discard: Remove-Item _generate-seo.py
```

### Stage 6.5: Knowledge Graph Auto-Seeding (MANDATORY — v2.5)

> **The #2 undetected failure mode: papers are published (Zenodo, R2, Pages) but are invisible to Knowledge Graph queries.** Every paper MUST be seeded in the QNFO Knowledge Graph after R2 upload. This enables: impact analysis (`/impact/{paper}`), ultrametric ball queries, and due diligence discovery.

#### 6.5a. Seed Knowledge Graph Node with ALL Known Locations (v3.0)

The KG Paper node MUST include ALL known internal and external locations. This enables one-query discovery of every place a publication lives — R2, Zenodo, GitHub, Pages, and social media.

```bash
# Write KG seed script to file, execute, discard
# Properties MUST include ALL known locations: r2_path, zenodo_url, github_url, pages_url, social_urls
echo "import urllib.request, json; PAPER_ID='paper-<paper-slug>'; TITLE='<title>'; DOI='<doi>'; payload={'action':'bulk','nodes':[{'id':PAPER_ID,'label':'Paper','name':TITLE,'properties':{'doi':DOI,'author':'Rowan Brad Quni-Gudzinas','date':'<date>','status':'published','r2_path':'qnfo/releases/YYYY/MM/<paper-slug>/paper.md','zenodo_url':'https://zenodo.org/records/<id>','github_url':'https://github.com/qnfo/<repo>','pages_url':'https://papers.qnfo.org/<paper-slug>/','social_urls':'[]'}}],'edges':[{'id':f'belongs-{PAPER_ID}-domain','source_id':PAPER_ID,'target_id':'domain-qwav-physics','relationship_type':'BELONGS_TO','properties':{}}]}; body=json.dumps(payload).encode(); req=urllib.request.Request('https://graph-api.q08.workers.dev/sync',data=body,method='POST',headers={'Content-Type':'application/json','User-Agent':'Mozilla/5.0'}); result=json.loads(urllib.request.urlopen(req,timeout=15).read()); print(f'KG seeded: nodes={result.get(\"upserted_nodes\",\"?\")}, edges={result.get(\"upserted_edges\",\"?\")}')" > _seed_kg.py
python _seed_kg.py
Remove-Item _seed_kg.py
```

**Paper Node Properties (all known locations):**

| Property | Value | Source |
|:---------|:------|:-------|
| `r2_path` | `qnfo/releases/YYYY/MM/<slug>/paper.md` | Stage 6 upload (internal) |
| `zenodo_url` | `https://zenodo.org/records/<id>` | Stage 4 DOI resolution (external) |
| `github_url` | `https://github.com/qnfo/<repo>` | Pre-publication setup (external) |
| `pages_url` | `https://papers.qnfo.org/<paper-slug>/` | Stage 5 deploy (external) |
| `social_urls` | `[]` (populated by `buffer-integration` after posting) | Post-publication auto-update (external) |

#### 6.5b. Verify KG Connectivity (MANDATORY)

```bash
# Verify the paper node was created with edges
echo "import urllib.request, json; r=urllib.request.Request('https://graph-api.q08.workers.dev/neighbors/paper-<paper-slug>',headers={'User-Agent':'Mozilla/5.0'}); data=json.loads(urllib.request.urlopen(r,timeout=10).read()); n=len(data.get('neighbors',[])); assert n>0,f'KG node missing! 0 edges'; print(f'[OK] KG: {n} edges')" > _verify_kg.py
python _verify_kg.py
Remove-Item _verify_kg.py
```

**GATE:** If the paper has 0 KG edges after seeding → `[BLOCKED: KG sync failed]`. Retry with mutex: POST `https://qnfo-agent-session.q08.workers.dev/kg-mutex/acquire` → graph-api `/sync` → POST `/kg-mutex/release`.

#### 6.5c. Architecture: R2 Event Notifications → Queue → Auto-KG-Sync (background)

The KG seeding in this stage is the **immediate** (synchronous) path. The infrastructure also supports an **asynchronous** auto-sync pipeline:

```
R2 qnfo/releases/*/paper.md (create/update)
 → R2 Event Notification (wrangler.toml: r2_buckets[].event_notification)
 → qnfo-lifecycle-queue (producer: R2, consumer: cron-worker)
 → cron-graph-re-seed Worker (periodic, every 15 min)
   → Parse YAML, acquire /kg-mutex, graph-api /sync, release mutex
```

The synchronous seeding (Stage 6.5a) is the primary path. The async pipeline is the reconciliation safety net. Both paths must pass before the paper is considered fully published.

#### 6.5d. Social Media KG Auto-Update Hook (v3.0 — buffer-integration)

> The `social_urls` property on the Paper KG node is initialized as `"[]"` (empty JSON array). After the paper is shared on social media via `buffer-integration`, the buffer skill MUST update this property with the resolved post URLs. This creates a bidirectional link: paper → social media → paper.

**Auto-update contract (implemented in buffer-integration):**
```python
# After posting to social media, update the KG Paper node's social_urls property
import urllib.request, json

PAPER_ID = 'paper-<paper-slug>'
SOCIAL_URLS = json.dumps([
    'https://twitter.com/qnfo/status/<tweet-id>',
    'https://linkedin.com/feed/update/<post-id>',
    'https://bsky.app/profile/qnfo.org/post/<post-id>'
])

# POST to graph-api /sync with action 'patch' to update only social_urls
payload = {
    'action': 'bulk',
    'nodes': [{
        'id': PAPER_ID,
        'label': 'Paper',
        'properties': {'social_urls': SOCIAL_URLS}
    }],
    'edges': []  # No new edges, just property update
}
body = json.dumps(payload).encode()
req = urllib.request.Request(
    'https://graph-api.q08.workers.dev/sync',
    data=body, method='POST',
    headers={'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'}
)
result = json.loads(urllib.request.urlopen(req, timeout=15).read())
print(f'[KG] Social URLs updated: nodes={result.get("upserted_nodes","?")}')
```

**GATE:** After social media posting, verify `social_urls` is non-empty: `GET https://graph-api.q08.workers.dev/neighbors/paper-<paper-slug>` must show `social_urls` with at least one URL. If `social_urls` is still `"[]"` after posting → `[BLOCKED: social URLs not synced to KG]`.

### Stage 6.6: Cloudflare Provenance Mirror (MANDATORY — v2.9)

> **🔴 MANDATORY GATE (v2.9):** The provenance bundle (PROVENANCE-BUNDLE.zip) MUST be mirrored across all Cloudflare infrastructure — R2, D1, and Knowledge Graph — for internal archival access, search, and literature reviews. Zenodo is the external/public archive; Cloudflare is the internal operational mirror. Publications without a Cloudflare provenance mirror are BLOCKED.

#### 6.6a. R2 Archival (Already in Stage 6)

The `PROVENANCE-BUNDLE.zip` is uploaded to R2 in Stage 6 (`qnfo/releases/YYYY/MM/<paper-slug>/PROVENANCE-BUNDLE.zip`). This is the canonical cloud copy. ✅ Already handled.

#### 6.6b. D1 Provenance Metadata (MANDATORY)

Seed the `qnfo-audit` D1 database with provenance metadata for internal search and literature reviews:

```bash
# Write D1 provenance seed script, execute, discard
echo "import json, subprocess; subprocess.run(['npx', 'wrangler', 'd1', 'execute', 'qnfo-audit', '--remote', '--command'], input=f\"INSERT INTO provenance_bundles (paper_slug, doi, r2_path, zenodo_url, bundle_size, components, created_at) VALUES ('<paper-slug>', '<doi>', 'qnfo/releases/YYYY/MM/<paper-slug>/PROVENANCE-BUNDLE.zip', 'https://zenodo.org/records/<id>', <size_bytes>, '{json.dumps([\"conversation.md\",\"session-metadata.json\",\"project-files/\",\"git-state.txt\",\"PROVENANCE.md\",\"README.md\"])}', '<ISO-8601>');\".encode(), capture_output=True), print(f'[D1] Provenance metadata seeded');" > _seed_d1_provenance.py
python _seed_d1_provenance.py
Remove-Item _seed_d1_provenance.py
```

**D1 Schema:**
| Column | Type | Description |
|:-------|:-----|:------------|
| `paper_slug` | TEXT PRIMARY KEY | Publication slug |
| `doi` | TEXT | Zenodo DOI |
| `r2_path` | TEXT | R2 path to PROVENANCE-BUNDLE.zip |
| `zenodo_url` | TEXT | Zenodo record URL |
| `bundle_size` | INTEGER | Bundle size in bytes |
| `components` | TEXT (JSON array) | List of files in the bundle |
| `conversation_export_id` | TEXT | Reference to conversation history in `audit_sessions` |
| `created_at` | TEXT (ISO 8601) | Creation timestamp |

#### 6.6c. Knowledge Graph Provenance Node (MANDATORY)

Seed the Knowledge Graph with a `Provenance` node linked to the paper via `HAS_PROVENANCE` edge:

```bash
# Write KG provenance seed script, execute, discard
echo "import urllib.request, json; PAPER_ID='paper-<paper-slug>'; PROV_ID='provenance-<paper-slug>'; payload={'action':'bulk','nodes':[{'id':PROV_ID,'label':'Provenance','name':f'Provenance Bundle — <paper-title>','properties':{'doi':'<doi>','r2_path':'qnfo/releases/YYYY/MM/<paper-slug>/PROVENANCE-BUNDLE.zip','bundle_size':<size_bytes>,'components':'conversation.md, session-metadata.json, project-files/, git-state.txt, PROVENANCE.md, README.md','created_at':'<ISO-8601>'}}],'edges':[{'id':f'has-provenance-{PAPER_ID}','source_id':PAPER_ID,'target_id':PROV_ID,'relationship_type':'HAS_PROVENANCE','properties':{'created_at':'<ISO-8601>'}}]}; body=json.dumps(payload).encode(); req=urllib.request.Request('https://graph-api.q08.workers.dev/sync',data=body,method='POST',headers={'Content-Type':'application/json','User-Agent':'Mozilla/5.0'}); result=json.loads(urllib.request.urlopen(req,timeout=15).read()); print(f'[KG] Provenance node seeded: nodes={result.get(\"upserted_nodes\",\"?\")}, edges={result.get(\"upserted_edges\",\"?\")}')" > _seed_kg_provenance.py
python _seed_kg_provenance.py
Remove-Item _seed_kg_provenance.py
```

#### 6.6d. Verify Cloudflare Provenance Mirror (MANDATORY)

```bash
# 1. Verify R2: bundle exists and is non-zero
npx wrangler r2 object get qnfo/releases/YYYY/MM/<paper-slug>/PROVENANCE-BUNDLE.zip --remote --file=_verify_bundle.zip
python -c "import os; s=os.path.getsize('_verify_bundle.zip'); print(f'[R2] Bundle: {s} bytes'); assert s>1000, 'Bundle too small!'"
Remove-Item _verify_bundle.zip

# 2. Verify D1: provenance metadata row exists
npx wrangler d1 execute qnfo-audit --remote --command "SELECT paper_slug, doi, r2_path FROM provenance_bundles WHERE paper_slug='<paper-slug>';"

# 3. Verify KG: Provenance node exists and has HAS_PROVENANCE edge
python _verify_kg_provenance.py
Remove-Item _verify_kg_provenance.py
```

**GATE:** If ANY of R2, D1, or KG provenance checks fail → `[BLOCKED: Cloudflare provenance mirror incomplete]`. Fix before claiming publication complete.

### Stage 7: Discovery Index Update

Register the new publication in the Discovery Index:

```bash
# Pull current index
npx wrangler r2 object get qnfo/discovery/index.json --remote --file=_discovery_index.json

# Update Discovery Index with new publication entry
# Write update script to file, execute, discard
echo "import json; idx = json.load(open('_discovery_index.json','r',encoding='utf-8')); idx.setdefault('publications',{})['<paper-slug>'] = {'title':'<title>','doi':'<doi>','date':'<date>','r2_path':'qnfo/releases/YYYY/MM/<paper-slug>/','pages_url':'https://papers.qnfo.org/<paper-slug>/','zenodo_url':'https://zenodo.org/records/<id>'}; json.dump(idx, open('_discovery_index.json','w',encoding='utf-8'), indent=2)" > _update_di.py
python _update_di.py

# Upload updated index
npx wrangler r2 object put qnfo/discovery/index.json --file=_discovery_index.json --remote

# Clean up
Remove-Item _discovery_index.json
Remove-Item _update_di.py
```

---

### Stage 8: Cross-Channel Dissemination Verification (MANDATORY)

> **CLOUDFLARE-FIRST POLICY (v2.2 — 2026-07-03):** R2 is canonical. GitHub is backup dissemination. Local Obsidian copy is ephemeral convenience only. NO publication is complete until all three channels are synchronized and verified.

**After every publication, verify dissemination across ALL channels:**

```bash
# 1. Cloudflare R2 (CANONICAL — MUST succeed first)
npx wrangler r2 object put qnfo/releases/YYYY/MM/<paper-slug>/paper.md --file=<paper>.md --remote
# Verify R2 upload by pulling back and comparing
npx wrangler r2 object get qnfo/releases/YYYY/MM/<paper-slug>/paper.md --remote --file=_r2_verify.md
python -c "import os; r2=os.path.getsize('_r2_verify.md'); local=os.path.getsize('<paper>.md'); print('SYNCED' if r2==local else 'DRIFT!')"

# 2. GitHub (backup dissemination)
git add publications/<paper-slug>.md
git commit -m "ACTION:CREATE FILE: publications/<paper-slug>.md RATIONALE:<paper-title> v<version> — canonical on R2 qnfo/releases/YYYY/MM/<paper-slug>/"
git push

# 3. Obsidian (ephemeral convenience copy — NOT canonical)
cp <paper>.md "$env:OBSIDIAN_VAULT\releases\YYYY\MM\<paper-slug>.md"
# NOTE: This local copy is ephemeral and non-persistent. It exists for Obsidian convenience only.
# The canonical source of truth is ALWAYS Cloudflare R2.
```

**Canonical Hierarchy (MANDATORY — enforced by this skill):**

| Priority | Location | Status | Verification |
|:---------|:---------|:-------|:------------|
| **1. Cloudflare R2** | `qnfo/releases/YYYY/MM/<paper-slug>/` | **CANONICAL** — single source of truth | Pull-back + size comparison |
| **2. Cloudflare D1** | `qnfo-audit.provenance_bundles` | **PROVENANCE METADATA** — internal search/review | Row count query |
| **3. Knowledge Graph** | `Provenance -[HAS_PROVENANCE]-> Paper` node | **PROVENANCE GRAPH** — impact analysis, discovery | KG neighbor query |
| **4. Zenodo** | DOI record (paper.md + paper.pdf + PROVENANCE-BUNDLE.zip + README.md) | Persistent archive with versioning + full provenance + GitHub link | DOI resolution |
| **5. GitHub** | `publications/<paper-slug>.md` | Backup dissemination | `git log -1 --oneline` |
| **6. Cloudflare Pages** | `papers.qnfo.org/<paper-slug>/` | Web-readable version | HTTP 200 check |
| **7. Obsidian** | `$env:OBSIDIAN_VAULT\releases\YYYY\MM\` | **EPHEMERAL** — convenience only, NOT authoritative | Existence check only |

**GATES:**
- If R2 upload fails → **BLOCK publishing.** R2 is canonical — all other channels depend on it.
- If GitHub push fails → **WARNING.** R2 and Zenodo are sufficient; git is backup.
- If Obsidian copy step fails → **NON-BLOCKING.** May not exist (thin-client mandate).
- **NEVER treat Obsidian as canonical.** Any agent reading from Obsidian MUST verify R2 has the same content.

**Post-Dissemination Verification (MANDATORY):**
```python
import os, hashlib

def verify_dissemination(local_path, r2_path, git_path):
    """Verify a publication is synchronized across all channels."""
    results = {}
    
    # 1. R2 canonical
    r2_size = os.path.getsize('_r2_verify.md')
    local_size = os.path.getsize(local_path)
    results['r2_synced'] = r2_size == local_size
    
    # 2. Git tracked
    import subprocess
    r = subprocess.run(['git', 'ls-files', '--error-unmatch', git_path],
                       capture_output=True)
    results['git_tracked'] = r.returncode == 0
    
    # 3. All pass?
    results['all_pass'] = all(results.values())
    return results
```

## Integration Points

| Upstream Skill | How It Feeds Publication Publisher |
|:---------------|:-----------------------------------|
| `research-orchestrator` | Calls this skill as Phases 4–5 of LRAP |
| `citation-manager` | Verified citations → publication-ready bibliography |
| `fabrication-audit` | Audited claims → publication-ready content |

| Downstream Skill | How Publication Publisher Enables It |
|:-----------------|:-------------------------------------|
| `social-orchestrator` / `buffer-integration` | Published DOI → social media dissemination |
| `seo-discoverability` | Deployed page → SEO optimization |
| `knowledge-graph` | New publication node → graph seeding |

---


## Embedded Scripts (SELF-CONTAINED — v3.1)

Scripts 1–3 are the publication toolchain. Scripts 4–7 are the PROVENANCE BUNDLE toolchain — used by Stage 3.5 to assemble the complete project record for Zenodo deposition. Every script is self-contained with `argparse` CLI and `if __name__ == '__main__'` entry point. No external dependencies beyond Python stdlib.

ALL scripts are embedded inline below. Copy-paste any code block into a `_<name>.py` file and execute.
No R2 pull required for core functionality.

> **R2 canonical full versions:** `qnfo/design-system/build_pdf.py`, `qnfo/tools/zenodo_api.py`, `qnfo/tools/generate-seo.py`, `qnfo/tools/export_conversation.py`, `qnfo/tools/capture_metadata.py`, `qnfo/tools/write_manifest.py`, `qnfo/tools/generate_readme.py`
> Pull full versions from R2 only if advanced features needed. All scripts are self-contained — no external dependencies beyond Python stdlib.
> Scripts 4–7 are the PROVENANCE BUNDLE toolchain used by Stage 3.5.

### 1. build_pdf.py — LEGACY (REMOVED v3.3 — reportlab pipeline BLOCKED for publications)

> **🔴 REMOVED 2026-07-06.** The reportlab-based `build_pdf.py` (157 lines) has been removed from this skill per the LaTeX Enforcement Gate (pdf-builder v4.0). Reportlab produces programmer-art PDFs with Helvetica fonts, bitmap math, no microtype, no ligatures, and is BLOCKED for ALL QNFO publications.
>
> **Canonical historical copy preserved on R2:** `qnfo/tools/archive/build_pdf.py`
> **All publication PDFs MUST use Pandoc+XeLaTeX (pdf-builder v4.0 PRIMARY pipeline).**
> If XeLaTeX is unavailable → publication is BLOCKED until TeX Live is installed.
> No fallback. No reportlab. No HTML+MathJax+playwright.

### 2. zenodo_api.py — Zenodo Deposition Client

```python
import urllib.request, json, os
from urllib.parse import quote

BASE = 'https://zenodo.org/api'

def _h(token): return {'Authorization':f'Bearer {token}','Content-Type':'application/json'}

def load_token(path=None):
    if path and os.path.exists(path):
        with open(path,'r',encoding='utf-8') as f: return f.read().strip()
    if os.environ.get('ZENODO_TOKEN'): return os.environ['ZENODO_TOKEN'].strip()  # Canonical: Secrets Store (store_id=8ef28060302e4311b064ba3529493e8b)
    p = os.path.expandvars(r'%USERPROFILE%\.zenodo_token')
    if os.path.exists(p):
        with open(p,'r',encoding='utf-8') as f: return f.read().strip()
    raise ValueError('ZENODO_TOKEN not found')

def create_dep(token, meta):
    r = urllib.request.Request(f'{BASE}/deposit/depositions',data=json.dumps({'metadata':meta}).encode(),headers=_h(token),method='POST')
    return json.loads(urllib.request.urlopen(r,timeout=30))

def upload_file(token, bucket, fpath, fname=None):
    if fname is None: fname = os.path.basename(fpath)
    with open(fpath,'rb') as f: data = f.read()
    h = {'Authorization':f'Bearer {token}','Content-Type':'application/octet-stream'}
    r = urllib.request.Request(f'{bucket}/{quote(fname)}',data=data,headers=h,method='PUT')
    return json.loads(urllib.request.urlopen(r,timeout=120))

def publish(token, dep_id):
    r = urllib.request.Request(f'{BASE}/deposit/depositions/{dep_id}/actions/publish',headers=_h(token),method='POST',data=b'')
    return json.loads(urllib.request.urlopen(r,timeout=30))

def new_version(token, dep_id):
    r = urllib.request.Request(f'{BASE}/deposit/depositions/{dep_id}/actions/newversion',headers=_h(token),method='POST',data=b'')
    return json.loads(urllib.request.urlopen(r,timeout=30))

def find_by_doi(doi):
    r = urllib.request.Request(f'{BASE}/records?q=doi:{quote(doi)}')
    hits = json.loads(urllib.request.urlopen(r,timeout=15)).get('hits',{}).get('hits',[])
    return hits[0] if hits else None

def publish_new_version(token, concept_doi, metadata, files):
    rec = find_by_doi(concept_doi)
    if not rec: raise ValueError(f'Not found: {concept_doi}')
    draft = new_version(token, rec['id'])
    for fp in files: upload_file(token, draft['links']['bucket'], fp)
    r = urllib.request.Request(f'{BASE}/deposit/depositions/{draft["id"]}',data=json.dumps({'metadata':metadata}).encode(),headers=_h(token),method='PUT')
    json.loads(urllib.request.urlopen(r,timeout=30))
    pub = publish(token, draft['id'])
    return {'doi':pub['doi'],'conceptdoi':pub.get('conceptdoi',concept_doi),'deposition_id':draft['id']}

if __name__ == '__main__':
    import argparse
    p = argparse.ArgumentParser()
    sp = p.add_subparsers(dest='cmd')
    sp.add_parser('list-drafts')
    a = p.parse_args()
    token = load_token()
    if a.cmd == 'list-drafts':
        r = urllib.request.Request(f'{BASE}/deposit/depositions?status=unsubmitted',headers=_h(token))
        drafts = json.loads(urllib.request.urlopen(r,timeout=15))
        for d in drafts[:10]: print(f'  {d["id"]}: {d.get("title","")[:80]}')
```

### 3. generate-seo.py — SEO Metadata Generator

```python
import json, os

def generate_seo(title, description, doi, author, date, keywords, url):
    return {
        'title': title, 'description': description,
        'og': {'title': title, 'description': description[:200], 'type': 'article', 'url': url},
        'citation': {'title': title, 'author': author, 'date': date, 'doi': doi},
        'robots': 'index, follow', 'keywords': ', '.join(keywords),
    }

def write_seo(meta, path='seo-metadata.json'):
    with open(path, 'w', encoding='utf-8') as f: json.dump(meta, f, indent=2, ensure_ascii=False)
    print(f'[SEO] {path}')

if __name__ == '__main__':
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument('--url', required=True); p.add_argument('--title', required=True)
    p.add_argument('--description', default=''); p.add_argument('--doi', default='')
    p.add_argument('--author', default='Rowan Brad Quni-Gudzinas'); p.add_argument('--date', default='')
    p.add_argument('--keywords', default='')
    a = p.parse_args()
    kw = [k.strip() for k in a.keywords.split(',') if k.strip()]
    write_seo(generate_seo(a.title, a.description, a.doi, a.author, a.date, kw, a.url))
```

### 4. export_conversation.py — Conversation History Exporter (v1.0 — Stage 3.5)

```python
"""Export DeepChat conversation history as Markdown for provenance bundle.

DEPENDENCY: Requires get_conversation_history() runtime tool (DeepChat agent only).
This script provides formatting and I/O; the agent provides the data via --input.

USAGE (agent-driven):
  1. Agent calls get_conversation_history(conversationId="<current>", includeSystem=False)
  2. Agent writes result to temp JSON file
  3. python _export_conversation.py --input _conv.json --output _provenance/conversation.md --session-id <id>
"""
import sys, os, json, argparse
from datetime import datetime, timezone

def format_conversation(conversation_data: dict, output_path: str,
                        session_id: str = "unknown") -> str:
    """Format conversation history as Markdown."""
    lines = []
    lines.append("# QNFO Research Session — Conversation History")
    lines.append("")
    lines.append(f"**Exported:** {datetime.now(timezone.utc).isoformat()}")
    lines.append(f"**Session ID:** {session_id}")
    lines.append("")
    lines.append("---")
    lines.append("")

    messages = conversation_data.get("messages", [])
    for msg in messages:
        role = msg.get("role", "unknown").upper()
        content = msg.get("content", "")
        timestamp = msg.get("timestamp", "")
        lines.append(f"## {role} ({timestamp})")
        lines.append("")
        lines.append(content)
        lines.append("")
        lines.append("---")
        lines.append("")

    text = "\n".join(lines)
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"[OK] conversation.md written ({os.path.getsize(output_path)} bytes, {len(messages)} messages)")
    return output_path

if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Format DeepChat conversation as Markdown")
    p.add_argument("--input", "-i", help="JSON from get_conversation_history")
    p.add_argument("--output", "-o", default="_provenance/conversation.md")
    p.add_argument("--session-id", default="unknown")
    args = p.parse_args()
    if args.input and os.path.exists(args.input):
        with open(args.input, "r", encoding="utf-8") as f:
            data = json.load(f)
        format_conversation(data, args.output, args.session_id)
    else:
        print("[INFO] No input file — agent provides data via get_conversation_history()")
```

### 5. capture_metadata.py — Session Metadata Capture (v1.0 — Stage 3.5)

```python
"""Capture session metadata for provenance bundle — self-contained, no external deps."""
import json, os, sys, argparse, subprocess
from datetime import datetime, timezone

def capture_metadata(**overrides) -> dict:
    md = {
        "export_timestamp": datetime.now(timezone.utc).isoformat(),
        "session_id": overrides.get("session_id", ""),
        "agent": "QNFO Research Agent (DEFAULT-DEEPSEEK v3.30+)",
        "model": overrides.get("model", ""),
        "conversation_id": overrides.get("conversation_id", ""),
        "project": overrides.get("project", ""),
        "publication_title": overrides.get("title", ""),
        "publication_version": overrides.get("version", ""),
    }
    try:
        r = subprocess.run(["git", "branch", "--show-current"], capture_output=True, text=True)
        md["git_branch"] = r.stdout.strip()
    except Exception:
        md["git_branch"] = "unknown"
    try:
        r = subprocess.run(["git", "log", "-1", "--oneline"], capture_output=True, text=True)
        md["git_commit"] = r.stdout.strip()
    except Exception:
        md["git_commit"] = "unknown"
    return md

if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Capture session metadata for provenance")
    p.add_argument("--output", "-o", default="_provenance/session-metadata.json")
    p.add_argument("--session-id", default=""); p.add_argument("--model", default="")
    p.add_argument("--conversation-id", default=""); p.add_argument("--project", default="")
    p.add_argument("--title", default=""); p.add_argument("--version", default="")
    args = p.parse_args()
    overrides = {k: v for k, v in vars(args).items() if v and k not in ("output",)}
    md = capture_metadata(**overrides)
    os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(md, f, indent=2, ensure_ascii=False)
    print(f"[OK] session-metadata.json written ({os.path.getsize(args.output)} bytes)")
```

### 6. write_manifest.py — Provenance Manifest Generator (v1.0 — Stage 3.5)

```python
"""Generate PROVENANCE.md manifest for provenance bundle — self-contained."""
import os, argparse
from datetime import datetime, timezone

MANIFEST_TEMPLATE = """# Provenance Manifest — {title} v{version}

## Chain of Custody

1. **Research conducted:** {date_range}
2. **Agent:** QNFO Research Agent (DEFAULT-DEEPSEEK v3.30+)
3. **Conversation exported:** {export_timestamp}
4. **Zenodo deposition:** {doi} (assigned after upload)

## Bundle Contents

| File | Description |
|:-----|:------------|
| `conversation.md` | Full LLM-agent conversation history |
| `session-metadata.json` | Agent, model, timestamps, git state |
| `project-files/` | Complete project filesystem snapshot |
| `git-state.txt` | Git log, diff, and status at publication time |
| `PROVENANCE.md` | This manifest |
| `README.md` | Human-readable entry point |

## Reproducibility Notes

- The conversation history records every prompt, tool invocation, and agent response.
- The project filesystem snapshot preserves all working scripts and data.
- Together, these enable independent verification of the research process.
- The final paper (`{paper_slug}.md` and `{paper_slug}.pdf`) are uploaded separately alongside this bundle.

## Verification

To verify this research:
1. Read `conversation.md` to understand the research dialogue
2. Examine `project-files/` for all working code and data
3. Cross-reference claims in the paper against the conversation and code
4. Check `git-state.txt` for the exact commit state at publication time
"""

if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Generate provenance manifest")
    p.add_argument("--output", "-o", default="_provenance/PROVENANCE.md")
    p.add_argument("--title", required=True, help="Paper title")
    p.add_argument("--version", default="1.0.0")
    p.add_argument("--doi", default="pending")
    p.add_argument("--date-range", default="")
    p.add_argument("--paper-slug", default="")
    args = p.parse_args()
    slug = args.paper_slug or args.title.lower().replace(" ", "-")
    now = datetime.now(timezone.utc)
    manifest = MANIFEST_TEMPLATE.format(
        title=args.title, version=args.version, doi=args.doi,
        date_range=args.date_range or now.strftime("%Y-%m-%d"),
        export_timestamp=now.isoformat(), paper_slug=slug)
    os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as f:
        f.write(manifest)
    print(f"[OK] PROVENANCE.md written ({os.path.getsize(args.output)} bytes)")
```

### 7. generate_readme.py — README Generator (v1.0 — Stage 3.5)

```python
"""Generate README.md for provenance bundle — self-contained, no external deps."""
import os, argparse
from datetime import datetime, timezone

README_TEMPLATE = """# {title} — v{version}

**DOI:** {doi} (assigned after Zenodo deposition)
**Author:** {author}
**Date:** {date}
**License:** QNFO Unified License Agreement (QNFO-ULA)
**GitHub:** {github_url}

## What This Is

{abstract}

## Repository Contents

| File | Description |
|:-----|:------------|
| `{paper_slug}.md` | Canonical Markdown source |
| `{paper_slug}.pdf` | Rendered PDF |
| `PROVENANCE-BUNDLE.zip` | Full project filesystem + conversation history |
| **Inside the bundle:** | |
| `conversation.md` | Full LLM-agent dialogue |
| `session-metadata.json` | Agent, model, git state |
| `project-files/` | All working scripts and data |
| `git-state.txt` | Git log at publication time |
| `PROVENANCE.md` | Chain of custody manifest |
| `README.md` | This file |

## Quick Start

### Read the Paper
Open `{paper_slug}.md` (Markdown) or `{paper_slug}.pdf` (rendered).

### Verify Reproducibility
1. Unzip `PROVENANCE-BUNDLE.zip`
2. Read `PROVENANCE.md` for the chain of custody
3. Read `conversation.md` for the research dialogue
4. Examine `project-files/` for all working code
5. Cross-reference claims against the conversation and code

### Version-Controlled Repository
The complete version-controlled git repository is available at:
{github_url}

## Citation

```bibtex
@{bibtex_type}{{{citation_key},
  author = {{{author}}},
  title = {{{title}}},
  year = {{{year}}},
  doi = {{{doi}}},
  publisher = {{Zenodo}},
  note = {{QNFO/QWAV Research Publication}}
}}
```

## Provenance

This research was conducted by a QNFO Research Agent. The full conversation history, project filesystem snapshot, and git state are preserved in `PROVENANCE-BUNDLE.zip`. See `PROVENANCE.md` inside the bundle for the complete chain of custody.

## License

QNFO Unified License Agreement (QNFO-ULA): https://legal.qnfo.org/
"""

if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Generate README.md for provenance bundle")
    p.add_argument("--output", "-o", default="_provenance/README.md")
    p.add_argument("--title", required=True, help="Paper title")
    p.add_argument("--version", default="1.0.0"); p.add_argument("--doi", default="pending")
    p.add_argument("--author", default="Rowan Brad Quni-Gudzinas")
    p.add_argument("--abstract", default="QNFO/QWAV Research Publication")
    p.add_argument("--github-url", default="https://github.com/qnfo")
    p.add_argument("--paper-slug", default=""); p.add_argument("--bibtex-type", default="article")
    p.add_argument("--citation-key", default="qnfo2026")
    p.add_argument("--year", default=str(datetime.now(timezone.utc).year))
    args = p.parse_args()
    slug = args.paper_slug or args.title.lower().replace(" ", "-")
    readme = README_TEMPLATE.format(
        title=args.title, version=args.version, doi=args.doi, author=args.author,
        abstract=args.abstract, github_url=args.github_url, paper_slug=slug,
        bibtex_type=args.bibtex_type, citation_key=args.citation_key, year=args.year,
        date=datetime.now(timezone.utc).strftime("%Y-%m-%d"))
    os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as f:
        f.write(readme)
    print(f"[OK] README.md written ({os.path.getsize(args.output)} bytes)")
```


## QNFO Design System Compliance (v2.0 — 2026-06-30)

All QNFO/QWAV publications use the **Silent Radix Light Theme** design system:

| Element | Location |
|:--------|:---------|
| Canonical CSS | `https://qnfo.org/design-system/qnfo-light.css` |
| R2 CSS | `qnfo/design-system/qnfo-light.css` |
| HTML template | `qnfo/design-system/publication-template.html` |
| PDF builder (v2.0) | `qnfo/design-system/build_pdf.py` |
| Design documentation | `qnfo/design-system/QNFO-DESIGN-SYSTEM.md` |
| Page rebuild tool | `qnfo/design-system/rebuild_page.py` |

### Design System Rules

**🚫 DARK THEMES FORBIDDEN.** All pages must use:
- White background (`#FFFFFF` / `var(--bg-primary)`)
- Dark text (`#363636` / `var(--text-primary)`)
- System font stack
- Max-width 800px centered layout
- MathJax CHTML with left-aligned display equations
- Clean tables with bottom-borders only

### Extended MathJax Macros
```
\bT, \bP, \bK, \bB, \bM  (mathbb)
\GL, \Gal, \Aut, \End, \Hom  (mathrm)
\Spec, \Proj, \id, \im, \ker, \Tr, \vol
```

## Failure Handling

| Scenario | Response |
|:---------|:---------|
| Publication fails Language Gate | `[BLOCKED: Language Gate]` — list violations, require fix |
| Zenodo API returns 401 | Token expired — regenerate at zenodo.org/account/settings/applications/ |
| PDF rendering has `\ufffd` | Font encoding issue — use `--pdf-engine=xelatex` for Unicode support |
| **PDF uses non-LaTeX fonts (reportlab)** | **[BLOCKED]** — reportlab is prohibited for publications. Rebuild with Pandoc+XeLaTeX. All published paper PDFs MUST use LaTeX fonts (Latin Modern / Computer Modern). See pdf-builder v4.0 LaTeX Enforcement Gate. |
| MathJax config AFTER script | `[BLOCKED: MathJax order]` — fix HTML template before deploying |
| Cloudflare Pages deploy fails | Check wrangler auth with `npx wrangler whoami` |
| R2 upload fails | Verify CLOUDFLARE_API_TOKEN is set and has write permissions |
| Discovery Index corrupted | Rebuild from R2 enumeration + local state and upload fresh |
| Provenance bundle assembly fails | `[BLOCKED: provenance]` — conversation history or project files unavailable; fix before Zenodo upload |
| Provenance bundle > 50GB | Exclude large binaries (reference by external DOI), compress conversation, flag exclusions in PROVENANCE.md |

---

*publication-publisher v3.3 — v3.3 removes reportlab bypass: Stage 2 now BLOCKs publication if XeLaTeX unavailable (no fallback). Embedded 157-line reportlab build_pdf.py removed. Cross-platform TeX Live detection. All escape hatches eliminated — LaTeX Enforcement Gate is now pre-build gate, not post-hoc. v3.2 had LaTeX Enforcement Gate integrated into Stage 2. v3.1 added self-contained PROVENANCE BUNDLE toolchain.*

## RT: RED-TEAM SELF-AUDIT

Before claiming this skill complete, autonomously run:

1. Output Verification (negative verification)
2. Assumption Challenge (state and test every assumption)
3. Edge Case Check (empty/null/max/boundary/desync)
4. DoD Integration (run _dod_enforce.py if exists)
5. Iteration (retry on failure, max 3)

ANTI-PATTERN: User should NEVER ask about quality.
Refer to RED-TEAM-PROTOCOL.md for full protocol.

> **Version:** (Kaizen-audited 2026-07-08)
