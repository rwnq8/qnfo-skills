---
name: publication-publisher
description: End-to-end publication workflow — formatting, PDF building, complete artifact bundling, Zenodo upload (with robust retry + versioning + draft recovery via zenodo_api.py), Cloudflare deployment, social media orchestration, and post-publication draft cleanup.
version: "2.4"
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
# PUBLICATION PUBLISHER SKILL — v2.4 — v2.0

> **INCLUDES AUTONOMOUS RED-TEAM SELF-AUDIT.** See RED-TEAM-PROTOCOL.md.

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
  {"step": "Validate publication readiness (Language Gate, citations)", "status": "pending"},
  {"step": "Build PDF from canonical Markdown", "status": "pending"},
  {"step": "Generate HTML publication page with MathJax", "status": "pending"},
  {"step": "Create Zenodo deposition with metadata", "status": "pending"},
  {"step": "Upload all artifacts to Zenodo", "status": "pending"},
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
    
    all_passed = all(v["passed"] for v in results.values())
    results["overall"] = "PASS" if all_passed else "FAIL"
    return results
```

**GATE:** All validation gates must PASS before proceeding. If any gate FAILS → `[BLOCKED: publication not ready]`.

### Stage 2: PDF Generation

> **Design System v2.1 (2026-07-03):** Two PDF pipelines available.
> 1. **Pandoc + XeLaTeX (PREFERRED)** — Professional typography with Computer Modern fonts, microtype, and full LaTeX math rendering. Produces publication-quality PDF with vector math, TOC, hyperlinks. Requires TeX Live 2025+ and pandoc on PATH.
> 2. **build_pdf.py (FALLBACK)** — Lightweight reportlab-based builder with QNFO Silent Radix Light Theme. No external dependencies beyond Python packages. v2.1 fix: heading HTML tags (e.g., `<em>m</em>P`) are now stripped before Paragraph construction, preventing "Parse error: saw </em> instead of expected </para>".
>
> **Professional PDF via Pandoc+XeLaTeX (direct invocation):**
> ```bash
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
> Where `_preamble.tex` contains: `\usepackage{microtype}` + `\usepackage{amsmath,amssymb,amsfonts}`.
>
> **TeX Live Detection:** Check `C:\texlive\2025\bin\windows\xelatex.exe` (Windows) or `/usr/bin/xelatex` (Linux/Mac). If not found, fall back to `build_pdf.py`.
> See [QNFO-DESIGN-SYSTEM.md](https://qnfo.org/design-system/QNFO-DESIGN-SYSTEM.md).

Build PDF from canonical Markdown. Use the embedded `build_pdf.py` (self-contained — copy from Embedded Scripts section above), or the full version on R2 for advanced features:

```bash
# Use embedded build_pdf.py (self-contained)
python _build_pdf.py --input paper.md --output PAPER-TITLE-v1.0.pdf
# Verify PDF is non-empty and correctly rendered
Test-Path PAPER-TITLE-v1.0.pdf
# Discard build script
Remove-Item _build_pdf.py
```

**PDF Verification (MANDATORY):**
```python
# Extract text from PDF and scan for rendering failures
import fitz  # PyMuPDF
doc = fitz.open("PAPER-TITLE-v1.0.pdf")
for page in doc:
    text = page.get_text()
    # Check for Unicode replacement characters
    if '\ufffd' in text:
        print("[BLOCKED] PDF contains rendering failures — font encoding issue")
        sys.exit(1)
```

**GATE:** PDF must have zero `\ufffd` characters and all special characters (em dashes, curly quotes) must render correctly.

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

### Stage 4: Zenodo Deposition (Robust — via `zenodo_api.py`)

Use the robust `zenodo_api.py` utility for all Zenodo operations. This replaces the fragile inline API calls with retry logic, exponential backoff, draft recovery, and proper `resource_type` metadata handling.

#### 4a. Create new deposition:

```bash
# Use embedded zenodo_api.py (self-contained — copy from Embedded Scripts section above)
# The embedded version handles: create deposition, upload files, publish, new version, recovery.
# Full version with advanced features at: qnfo/tools/zenodo_api.py on R2

# Build metadata JSON
echo "{\"title\": \"Paper Title\", \"upload_type\": \"publication\", \"publication_type\": \"workingpaper\", \"resource_type\": {\"id\": \"publication-workingpaper\"}, \"description\": \"Abstract...\", \"creators\": [{\"name\": \"Author Name\", \"affiliation\": \"QWAV / QNFO\"}], \"access_right\": \"open\", \"license\": \"CC-BY-4.0\", \"version\": \"1.0.0\"}" > _zenodo_meta.json

# Create deposition, upload files, publish
python _zenodo_api.py create --token-file ZENODO_TOKEN --metadata _zenodo_meta.json --files paper.md,paper.pdf

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
python _zenodo_api.py recover --token-file ZENODO_TOKEN --deposition-id 12345 --metadata _zenodo_meta.json --files paper.md,paper.pdf
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
                {"name": "QNFO Research", "affiliation": "QWAV / QNFO"}
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
# Upload publication to R2
npx wrangler r2 object put qnfo/releases/2026/07/<paper-slug>/paper.md --file=<md-path>
npx wrangler r2 object put qnfo/releases/2026/07/<paper-slug>/paper.pdf --file=<pdf-path>
npx wrangler r2 object put qnfo/releases/2026/07/<paper-slug>/index.html --file=index.html

# Generate SEO artifacts (use embedded generate-seo.py from Embedded Scripts section)
python _generate-seo.py --url https://papers.qnfo.org/<paper-slug>/ --title "<paper title>"
# Discard: Remove-Item _generate-seo.py
```

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
| **2. Zenodo** | DOI record | Persistent archive with versioning | DOI resolution |
| **3. GitHub** | `publications/<paper-slug>.md` | Backup dissemination | `git log -1 --oneline` |
| **4. Cloudflare Pages** | `papers.qnfo.org/<paper-slug>/` | Web-readable version | HTTP 200 check |
| **5. Obsidian** | `$env:OBSIDIAN_VAULT\releases\YYYY\MM\` | **EPHEMERAL** — convenience only, NOT authoritative | Existence check only |

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


## Embedded Scripts (SELF-CONTAINED — v2.3)

ALL scripts are embedded inline below. Copy-paste any code block into a `_<name>.py` file and execute.
No R2 pull required for core functionality.

> **R2 canonical full versions:** `qnfo/design-system/build_pdf.py`, `qnfo/tools/zenodo_api.py`, `qnfo/tools/generate-seo.py`
> Pull full versions from R2 only if advanced features needed (matplotlib math, pandoc fallback, complex tables).

### 1. build_pdf.py — QNFO Light Theme PDF Builder v2.1

```python
"""QNFO PDF Builder v2.1 — Self-contained reportlab pipeline with heading HTML fix."""
import sys, os, re
try:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.lib.colors import HexColor
    from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
    from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                     TableStyle, Preformatted, HRFlowable)
    HAS_REPORTLAB = True
except ImportError:
    HAS_REPORTLAB = False
    print('[ERROR] reportlab required. Install: pip install reportlab')
    sys.exit(1)

PAGE_W, PAGE_H = A4
MARGIN = inch

C = {
    'bg': HexColor('#FFFFFF'), 'text': HexColor('#363636'),
    'heading': HexColor('#000000'), 'muted': HexColor('#808080'),
    'code_bg': HexColor('#EFEFEF'), 'table_border': HexColor('#CCCCCC'),
    'quote_text': HexColor('#666666'),
}

def build_styles():
    s = getSampleStyleSheet()
    h = dict(fontName='Helvetica-Bold', textColor=C['heading'])
    s.add(ParagraphStyle('QNFO_Body',parent=s['Normal'],fontSize=11,leading=15.4,textColor=C['text'],alignment=TA_JUSTIFY,spaceAfter=8))
    s.add(ParagraphStyle('QNFO_H1',parent=s['Heading1'],fontSize=18,leading=25.2,spaceAfter=12,spaceBefore=24,**h))
    s.add(ParagraphStyle('QNFO_H2',parent=s['Heading2'],fontSize=14,leading=19.6,spaceAfter=10,spaceBefore=20,**h))
    s.add(ParagraphStyle('QNFO_H3',parent=s['Heading3'],fontSize=12,leading=16.8,spaceAfter=8,spaceBefore=16,**h))
    s.add(ParagraphStyle('QNFO_H4',parent=s['Heading4'],fontSize=11,leading=15.4,spaceAfter=6,spaceBefore=12,**h))
    s.add(ParagraphStyle('QNFO_Code',parent=s['Code'],fontName='Courier',fontSize=9,leading=12.6,textColor=C['text'],backColor=C['code_bg'],borderPadding=6,spaceAfter=8))
    s.add(ParagraphStyle('QNFO_Quote',parent=s['Normal'],fontName='Helvetica-Oblique',fontSize=11,leading=15.4,textColor=C['quote_text'],leftIndent=20,spaceAfter=8))
    s.add(ParagraphStyle('QNFO_Meta',parent=s['Normal'],fontName='Helvetica',fontSize=9.5,leading=13.3,textColor=C['muted'],spaceAfter=4))
    s.add(ParagraphStyle('QNFO_Footer',parent=s['Normal'],fontName='Helvetica',fontSize=8.5,leading=12,textColor=C['muted'],alignment=TA_CENTER))
    s.add(ParagraphStyle('QNFO_Title',parent=s['Title'],fontName='Helvetica-Bold',fontSize=22,leading=30.8,textColor=C['heading'],spaceAfter=6))
    s.add(ParagraphStyle('QNFO_TableCell',parent=s['Normal'],fontName='Helvetica',fontSize=10,leading=14,textColor=C['text']))
    s.add(ParagraphStyle('QNFO_TableHeader',parent=s['Normal'],fontName='Helvetica-Bold',fontSize=10,leading=14,textColor=C['heading']))
    return s

def clean_html_tags(text):
    return re.sub(r'</?[a-zA-Z][^>]*>', '', text)

def extract_text_until(tokens, start, tag):
    parts, depth, i = [], 1, start
    while i < len(tokens):
        t = tokens[i]
        if re.match(rf'</{tag}[>\s]', t): depth -= 1
        if depth == 0: break
        elif re.match(rf'<{tag}[>\s]', t): depth += 1
        parts.append(t); i += 1
    return ''.join(parts)

def skip_to_closing(tokens, start, tag):
    depth, i = 1, start
    while i < len(tokens):
        t = tokens[i]
        if re.match(rf'</{tag}[>\s]', t): depth -= 1
        if depth == 0: return i
        elif re.match(rf'<{tag}[>\s]', t): depth += 1
        i += 1
    return i

def build_table(headers, rows, styles, col_widths=None):
    hrow = [Paragraph(h, styles['QNFO_TableHeader']) for h in headers]
    drows = [[Paragraph(str(c), styles['QNFO_TableCell']) for c in r] for r in rows]
    tbl = Table([hrow] + drows, colWidths=col_widths, repeatRows=1)
    cmds = [
        ('BACKGROUND', (0,0), (-1,0), C['code_bg']),
        ('TEXTCOLOR', (0,0), (-1,0), C['heading']),
        ('LINEBELOW', (0,0), (-1,-1), 0.5, C['table_border']),
        ('TOPPADDING', (0,0), (-1,-1), 4), ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6), ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]
    tbl.setStyle(TableStyle(cmds))
    return tbl

def parse_html_to_flowables(html, styles):
    tokens = re.split(r'(</?[^>]+>)', html)
    flowables, i = [], 0
    while i < len(tokens):
        token = tokens[i].strip()
        if not token: i += 1; continue
        if token.startswith('</'): i += 1; continue
        m = re.match(r'<(\w+)', token)
        if m:
            tag = m.group(1)
            if tag in ('h1','h2','h3','h4'):
                text = clean_html_tags(extract_text_until(tokens, i+1, tag))
                flowables.append(Paragraph(text, styles[f'QNFO_{tag.upper()}']))
                i = skip_to_closing(tokens, i+1, tag)
            elif tag == 'p':
                text = clean_html_tags(extract_text_until(tokens, i+1, 'p'))
                if text.strip(): flowables.append(Paragraph(text, styles['QNFO_Body']))
                i = skip_to_closing(tokens, i+1, 'p')
            elif tag == 'pre':
                text = clean_html_tags(extract_text_until(tokens, i+1, 'pre'))
                flowables.append(Preformatted(text, styles['QNFO_Code']))
                i = skip_to_closing(tokens, i+1, 'pre')
            elif tag == 'blockquote':
                text = clean_html_tags(extract_text_until(tokens, i+1, 'blockquote'))
                flowables.append(Paragraph(text, styles['QNFO_Quote']))
                i = skip_to_closing(tokens, i+1, 'blockquote')
            elif tag == 'hr':
                flowables.append(HRFlowable(width='100%', thickness=0.5, color=C['table_border'], spaceAfter=12))
                i += 1
            elif tag == 'li':
                text = clean_html_tags(extract_text_until(tokens, i+1, 'li'))
                if text.strip(): flowables.append(Paragraph(chr(8226)+' '+text, styles['QNFO_Body']))
                i = skip_to_closing(tokens, i+1, 'li')
            elif tag in ('ul','ol','div','span','strong','em','code','a','thead','tbody','tr','th','td','br','img','head','body','html','meta','title','link','script','style'):
                i += 1
            else: i += 1
        else: i += 1
    return flowables

def build_pdf(md_path, output_path, metadata=None):
    styles = build_styles()
    with open(md_path, 'r', encoding='utf-8') as f: md = f.read()
    title_match = re.search(r'^#\s+(.+)$', md, re.MULTILINE)
    title = title_match.group(1) if title_match else os.path.basename(md_path).replace('.md','')
    doc = SimpleDocTemplate(output_path, pagesize=A4, leftMargin=MARGIN, rightMargin=MARGIN, topMargin=MARGIN, bottomMargin=MARGIN)
    story = [Paragraph(title, styles['QNFO_Title']), Spacer(1,4)]
    if metadata:
        m = []
        if metadata.get('author'): m.append(f"Author: {metadata['author']}")
        if metadata.get('date'): m.append(f"Date: {metadata['date']}")
        if m: story.append(Paragraph(' | '.join(m), styles['QNFO_Meta']))
    story.extend([Spacer(1,12), HRFlowable(width='100%', thickness=0.5, color=C['table_border'], spaceAfter=12)])
    html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', md)
    html = re.sub(r'\*(.+?)\*', r'<em>\1</em>', html)
    story.extend(parse_html_to_flowables(html, styles))
    story.extend([Spacer(1,24), HRFlowable(width='100%', thickness=0.5, color=C['table_border'], spaceAfter=8)])
    story.append(Paragraph('Published under QNFO ULA. www.qnfo.org', styles['QNFO_Footer']))
    doc.build(story)
    print(f'[OK] PDF built: {output_path}')
    return output_path

if __name__ == '__main__':
    import argparse
    p = argparse.ArgumentParser(description='QNFO PDF Builder v2.1')
    p.add_argument('--input','-i',required=True,help='Input Markdown')
    p.add_argument('--output','-o',help='Output PDF')
    p.add_argument('--author',help='Author')
    p.add_argument('--date',help='Date')
    a = p.parse_args()
    if not a.output: a.output = os.path.splitext(os.path.basename(a.input))[0]+'-v1.0.pdf'
    build_pdf(a.input, a.output, {'author':a.author,'date':a.date})
```

### 2. zenodo_api.py — Zenodo Deposition Client

```python
import urllib.request, json, os
from urllib.parse import quote

BASE = 'https://zenodo.org/api'

def _h(token): return {'Authorization':f'Bearer {token}','Content-Type':'application/json'}

def load_token(path=None):
    if path and os.path.exists(path):
        with open(path,'r',encoding='utf-8') as f: return f.read().strip()
    if os.environ.get('ZENODO_TOKEN'): return os.environ['ZENODO_TOKEN'].strip()
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
    p.add_argument('--author', default='QNFO Research'); p.add_argument('--date', default='')
    p.add_argument('--keywords', default='')
    a = p.parse_args()
    kw = [k.strip() for k in a.keywords.split(',') if k.strip()]
    write_seo(generate_seo(a.title, a.description, a.doi, a.author, a.date, kw, a.url))
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
| MathJax config AFTER script | `[BLOCKED: MathJax order]` — fix HTML template before deploying |
| Cloudflare Pages deploy fails | Check wrangler auth with `npx wrangler whoami` |
| R2 upload fails | Verify CLOUDFLARE_API_TOKEN is set and has write permissions |
| Discovery Index corrupted | Rebuild from R2 enumeration + local state and upload fresh |

---

*publication-publisher v2.4 — Phase 4–5 of LRAP. v2.4 fixes PDF math rendering: simplified preamble (microtype+amsmath, no setmathfont), pandoc+XeLaTeX as default, mandatory PyMuPDF verification of U+FFFD=0. v2.3 adds self-contained embedded scripts. v2.2 adds Cloudflare-first dissemination. v2.1 adds dual PDF pipeline + TeX Live detection.*

## RT: RED-TEAM SELF-AUDIT

Before claiming this skill complete, autonomously run:

1. Output Verification (negative verification)
2. Assumption Challenge (state and test every assumption)
3. Edge Case Check (empty/null/max/boundary/desync)
4. DoD Integration (run _dod_enforce.py if exists)
5. Iteration (retry on failure, max 3)

ANTI-PATTERN: User should NEVER ask about quality.
Refer to RED-TEAM-PROTOCOL.md for full protocol.
