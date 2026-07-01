---
name: publication-publisher
description: End-to-end publication workflow — formatting, PDF building, complete artifact bundling, Zenodo upload (with robust retry + versioning + draft recovery via zenodo_api.py), Cloudflare deployment, social media orchestration, and post-publication draft cleanup.
version: "2.0"
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
# PUBLICATION PUBLISHER SKILL — v2.0

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

> **Design System v2.0:** PDF builder now at `qnfo/design-system/build_pdf.py` (v2.0).
> Uses Silent Radix Light Theme — white background, system fonts, clean tables.
> See [QNFO-DESIGN-SYSTEM.md](https://qnfo.org/design-system/QNFO-DESIGN-SYSTEM.md).

Build PDF from canonical Markdown via `build_pdf.py` (shared with cloudflare-deployer):

```bash
# Pull build script from R2
npx wrangler r2 object get qnfo/design-system/build_pdf.py --remote --file=_build_pdf.py
# Build PDF
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
# Pull zenodo_api.py from R2 (ephemeral)
npx wrangler r2 object get qnfo/tools/zenodo_api.py --remote --file=_zenodo_api.py

# Build metadata JSON
echo "{\"title\": \"Paper Title\", \"upload_type\": \"publication\", \"publication_type\": \"workingpaper\", \"resource_type\": {\"id\": \"publication-workingpaper\"}, \"description\": \"Abstract...\", \"creators\": [{\"name\": \"Author Name\", \"affiliation\": \"QWAV / QNFO\"}], \"access_right\": \"open\", \"license\": \"CC-BY-4.0\", \"version\": \"1.0.0\"}" > _zenodo_meta.json

# Create deposition, upload files, publish
python _zenodo_api.py create --token-file ZENODO_TOKEN --metadata _zenodo_meta.json --files paper.md,paper.pdf

# Clean up
Remove-Item _zenodo_api.py, _zenodo_meta.json
```

#### 4b. Create new version of existing deposition:

```bash
# Pull zenodo_api.py from R2 (ephemeral)
npx wrangler r2 object get qnfo/tools/zenodo_api.py --remote --file=_zenodo_api.py

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

# Generate SEO artifacts
# Pull from R2: npx wrangler r2 object get qnfo/tools/generate-seo.py --remote --file=_generate-seo.py
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

## Embedded Scripts

| Script | R2 Canonical | Execution Cache | Purpose |
|:-------|:-------------|:----------------|:--------|
| `build_pdf.py` | `qnfo/design-system/build_pdf.py` | `_build_pdf.py` | Markdown → PDF generation |
| `generate-seo.py` | `qnfo/tools/generate-seo.py` | `_generate-seo.py` | SEO metadata generation |
| `zenodo_api.py` | `qnfo/tools/zenodo_api.py` | `_zenodo_api.py` | Robust Zenodo deposition management with retry + versioning + draft recovery |

### Bootstrap Protocol

```bash
# Pull from R2
npx wrangler r2 object get qnfo/tools/<script>.py --remote --file=_<script>.py
# Verify
Test-Path _<script>.py
```

---



---

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

*publication-publisher v1.0 — Phase 4–5 of LRAP. Zenodo deposition, Cloudflare Pages deployment, PDF generation, and archival for QNFO/QWAV publications.*

## RT: RED-TEAM SELF-AUDIT

Before claiming this skill complete, autonomously run:

1. Output Verification (negative verification)
2. Assumption Challenge (state and test every assumption)
3. Edge Case Check (empty/null/max/boundary/desync)
4. DoD Integration (run _dod_enforce.py if exists)
5. Iteration (retry on failure, max 3)

ANTI-PATTERN: User should NEVER ask about quality.
Refer to RED-TEAM-PROTOCOL.md for full protocol.
