---
name: publication-publisher
description: End-to-end publication workflow — formatting, PDF building, complete artifact bundling, Zenodo upload (with semantic versioning), Cloudflare deployment, social media orchestration, and post-publication draft cleanup. Use when publishing papers, reports, or other documents.
version: "1.5"
---

# PUBLICATION PUBLISHER SKILL — v1.5

> **On-demand skill.** Load via `skill_view('publication-publisher')` for publication workflows.
> Source: DEFAULT.md §11 + `ZENODO-PUBLISH.md` + `pdf-builder` skill

---

## Publication Pipeline

```
Draft Complete → Format (§11) → Build PDF → Assemble Artifact Bundle → Zenodo Upload (ALL artifacts, versioned) → Cloudflare Deploy → Social Posts → Draft Cleanup
```

### CRITICAL RULES (v1.4)
1. **Zenodo uploads MUST include ALL project artifacts** — PDF, source code, data files, README, supplementary materials, configs. NOT just the final output PDF.
2. **Semantic versioning is MANDATORY** — every publication (new or updated) gets a MAJOR.MINOR.PATCH version. Updates to existing publications create NEW VERSIONS via `--doi`, never duplicate records.
3. **Draft cleanup is MANDATORY after publication** — remove all temporary build artifacts, draft markdowns, and ephemeral files. Verify R2 holds canonical copies.

---

## Step 1: Format (§11 Standards)

### Visible Author Block (MANDATORY)
Every release document must start with:
```
**Author:** Rowan Quni-Gudzinas | **Date:** YYYY-MM-DD | **License:** QNFO Unified License Agreement (QNFO-ULA)
```

### Curly Quotes
All publication documents use curly/smart quotes (Unicode: \u201c \u201d \u2018 \u2019). Code blocks exempt.

### Pre-Publication Checklist
- [ ] Visible Author Block present
- [ ] Curly quotes applied
- [ ] REVIEWER subagent passed fabrication audit
- [ ] All file references verified (`Test-Path`)
- [ ] Git log confirms all changes committed
- [ ] PDF generated
- [ ] **PDF rendering verified — no `\ufffd` characters, em dashes/curly quotes render correctly**
- [ ] **Artifact bundle assembled — ALL project files catalogued (source, data, README, supplementary, configs)**
- [ ] **Semantic version assigned — MAJOR.MINOR.PATCH documented in manifest**
- [ ] **Zenodo duplicate check passed — existing DOI identified for version bump, or confirmed new publication**
- [ ] **ALL artifacts uploaded to Zenodo — NOT just the PDF. Manifest cross-referenced.**
- [ ] Cloudflare Pages deployed and URL verified
- [ ] **Draft cleanup complete — all temp build files removed, R2 canonical verified**

---

## Step 2: Build PDF

Use `skill_view('pdf-builder')` to load the skill, then follow its workflow:
1. Verify prerequisites: `python -c "import reportlab, matplotlib; print('OK')"`
2. Build: `python "%APPDATA%\DeepChat\skills\pdf-builder\scripts\build_pdf.py" --input "paper.md" --output "paper.pdf"`
3. Verify rendering (MANDATORY): See skill's Step 4 for the fitz verification script.

For math-free drafts, add `--no-math` for lighter/faster builds.

### PDF Rendering Verification (MANDATORY)
After building PDF, extract text and verify ALL Unicode characters render correctly:
```bash
python -c "
import fitz
doc = fitz.open('output.pdf')
text = ''.join(page.get_text() for page in doc)
# Check for replacement character (corrupted Unicode)
if '\ufffd' in text:
    print('[BLOCKED] PDF contains Unicode replacement characters! Fix font encoding.')
    print('First occurrence:', text[max(0,text.index('\ufffd')-20):text.index('\ufffd')+20])
else:
    print('[OK] No replacement characters found.')
# Check key typographic characters
for char, name in [('\u2014','em dash'), ('\u201c','left curly quote'), ('\u201d','right curly quote')]:
    count = text.count(char)
    print(f'[{chr(0x2713) if count>0 else chr(0x2717)}] {name}: {count} found')
"
```
If ANY character fails: PDF is NOT publication-ready. Fix font encoding in `build_pdf.py` BEFORE proceeding.

---

## Step 2.5: Assemble Complete Artifact Bundle (MANDATORY — v1.4)

**HARD RULE: Zenodo uploads MUST include ALL project artifacts, NOT just the final PDF.** The Zenodo record is the permanent scholarly archive. A PDF alone is incomplete — the record must enable reproducibility.

### Artifact Categories (ALL required unless noted as optional)

| Category | Required? | Examples |
|:---------|:----------|:---------|
| **Primary Output** | YES | PDF of the publication |
| **Source Documents** | YES | Markdown/LaTeX source, figures, diagrams |
| **Data Files** | YES (if any) | CSVs, JSON datasets, simulation outputs used in the paper |
| **Code** | YES (if any) | Python scripts, notebooks, analysis code |
| **Supplementary Materials** | YES (if any) | Appendices, extended proofs, additional figures |
| **README** | YES | Project overview, reproduction instructions, build commands |
| **Configuration** | YES | Requirements files, environment specs, build configs |
| **License** | YES | QNFO Unified License Agreement (QNFO-ULA) — see https://legal.qnfo.org/ |

### Artifact Bundle Assembly Protocol

**Step 2.5.1: Enumerate all project files**

```powershell
# List ALL files in the project directory
Get-ChildItem -Path "<project_dir>" -Recurse -File | ForEach-Object { $_.FullName }
```

**Step 2.5.2: Classify each file** into the categories above. Any file NOT fitting a category → flag as `[UNCLASSIFIED: <reason>]` and either reclassify or exclude with documented rationale.

**Step 2.5.3: Generate artifact manifest (`ARTIFACT-MANIFEST.json`)**

Create a structured manifest listing every file with checksums. Use a Python script (via temp file):

```python
import json, hashlib, os, sys
from pathlib import Path

project_dir = Path(sys.argv[1])
version = sys.argv[2]  # MAJOR.MINOR.PATCH

manifest = {
    "publication_title": sys.argv[3],
    "version": version,
    "semantic_versioning": {
        "major": int(version.split('.')[0]),
        "minor": int(version.split('.')[1]),
        "patch": int(version.split('.')[2]),
        "version_change_notes": sys.argv[4] if len(sys.argv) > 4 else "Initial publication"
    },
    "artifacts": [],
    "generated_at": None  # populated below
}

from datetime import datetime, timezone
manifest["generated_at"] = datetime.now(timezone.utc).isoformat()

categories = {
    ".pdf": "primary_output",
    ".md": "source_document",
    ".tex": "source_document",
    ".py": "code",
    ".ipynb": "code",
    ".csv": "data",
    ".json": "data",
    ".txt": "supplementary",
    ".png": "figure",
    ".svg": "figure",
    ".jpg": "figure",
    ".yml": "configuration",
    ".yaml": "configuration",
    ".toml": "configuration",
    ".cfg": "configuration",
    ".txt": "supplementary"
}

for filepath in sorted(project_dir.rglob('*')):
    if filepath.is_file() and not filepath.name.startswith('_') and '__pycache__' not in str(filepath):
        rel = str(filepath.relative_to(project_dir))
        ext = filepath.suffix.lower()
        category = categories.get(ext, "unclassified")
        
        sha256 = hashlib.sha256(filepath.read_bytes()).hexdigest()
        
        manifest["artifacts"].append({
            "path": rel,
            "category": category,
            "size_bytes": filepath.stat().st_size,
            "sha256": sha256
        })

manifest["total_files"] = len(manifest["artifacts"])
manifest["categories_count"] = {}
for a in manifest["artifacts"]:
    manifest["categories_count"][a["category"]] = manifest["categories_count"].get(a["category"], 0) + 1

# Verify mandatory categories present
required = ["primary_output", "source_document"]
missing = [r for r in required if r not in manifest["categories_count"]]
if missing:
    print(f"[BLOCKED] Missing required artifact categories: {missing}")
    sys.exit(1)

# Warn if any unclassified
unclassified = [a for a in manifest["artifacts"] if a["category"] == "unclassified"]
if unclassified:
    print(f"[WARNING] {len(unclassified)} unclassified files:")
    for u in unclassified:
        print(f"  {u['path']}")

output_path = project_dir / "ARTIFACT-MANIFEST.json"
json.dump(manifest, open(output_path, 'w', encoding='utf-8'), indent=2, ensure_ascii=False)
print(f"[OK] Manifest written: {output_path}")
print(f"  Version: {version}")
print(f"  Total artifacts: {manifest['total_files']}")
for cat, count in sorted(manifest['categories_count'].items()):
    print(f"  {cat}: {count}")
```

**Step 2.5.4: Verify manifest completeness**

```powershell
# Verify ALL files listed match files on disk
python -c "
import json
m = json.load(open('ARTIFACT-MANIFEST.json','r',encoding='utf-8'))
paths = {a['path'] for a in m['artifacts']}
print(f'Manifest: {len(paths)} files')
# Verify PDF is included
pdfs = [a for a in m['artifacts'] if a['path'].endswith('.pdf')]
print(f'PDF artifacts: {len(pdfs)}')
if not pdfs:
    print('[BLOCKED] NO PDF in artifact manifest!')
" (via script file)
```

**GATE:** If manifest assembly fails or required categories are missing → `[BLOCKED: incomplete artifact bundle]`. Do NOT proceed to Zenodo upload.

### Semantic Versioning Protocol (MANDATORY)

Every publication MUST carry a semantic version. This applies at artifact assembly time — the version is embedded in the manifest and used for Zenodo versioning.

**Version format:** `MAJOR.MINOR.PATCH`

| Bump | When |
|:-----|:-----|
| MAJOR | Breaking changes — new incompatible methodology, restructured argument, substantially new findings |
| MINOR | New content added — additional sections, new data, expanded analysis, new co-author |
| PATCH | Corrections — typo fixes, formatting, small clarifications, metadata updates |

**Version assignment protocol:**
1. **First publication:** Start at `1.0.0`
2. **Update to existing publication:** Determine bump type using the table above. Use `--doi <existing_doi>` with Zenodo to create new version.
3. **Version in filename:** `PROJECT-NAME-v1.0.0.pdf` (NOT just `PROJECT-NAME-v1.pdf` or `PROJECT-NAME.pdf`)
4. **Version in manifest:** Embedded in `ARTIFACT-MANIFEST.json` with change notes

---

## Step 3: Zenodo Upload (ALL Artifacts — NOT just PDF)

**Zenodo Duplicate Prevention (MANDATORY — execute BEFORE creating any record):**

1. Check for existing Zenodo record by searching the Discovery Index for a prior DOI for this publication title:
```bash
python -c "import json; d=json.load(open('_discovery_index.json','r',encoding='utf-8')); pubs=[p for p in d.get('publications',[]) if '<publication_title>' in p.get('title','')]; print(json.dumps(pubs, indent=2))" (via script file)
```
2. **If existing DOI found → MUST create a NEW VERSION (not a duplicate record).** This is NON-NEGOTIABLE. Use `--doi <existing_doi>` flag. Semantic version bump per §2.5 protocol.
3. If Zenodo API search needed: use `brave_web_search` for `site:zenodo.org "<publication_title>"` to find existing records.
4. **Never create a new Zenodo record for a publication that already has one.** This creates DUPLICATE records and violates scholarly archiving standards.
5. If unsure whether a record exists: search first. Create only when search returns zero results.

**Artifact Upload Protocol (v1.4 — ALL artifacts required):**

The Zenodo upload MUST include ALL files from the artifact bundle, not just the PDF:

```bash
# Pull from R2: npx wrangler r2 object get qnfo/tools/zenodo_publish.py --remote --file=_zenodo_publish.py

# Upload ALL artifacts (not just PDF)
python _zenodo_publish.py \
  --title "<publication_title> v<MAJOR.MINOR.PATCH>" \
  --author "<Last, First>" \
  --artifacts-dir "<project_dir>" \
  --manifest "ARTIFACT-MANIFEST.json" \
  --version "<MAJOR.MINOR.PATCH>" \
  --upload-type publication \
  --license "other" \
  {{#doi}}--doi "<existing_doi>"{{/doi}}

# Verify upload completeness
python _zenodo_publish.py --verify --deposition-id <id>

# Discard: Remove-Item _zenodo_publish.py
```

**Upload Verification (MANDATORY):**
After upload, verify the Zenodo record contains ALL artifacts by cross-referencing against `ARTIFACT-MANIFEST.json`:
```bash
python -c "
import json
manifest = json.load(open('ARTIFACT-MANIFEST.json','r',encoding='utf-8'))
expected = manifest['total_files']
print(f'Expected artifacts: {expected}')
print(f'Categories: {manifest[\"categories_count\"]}')
# Zenodo API check (via zenodo_publish.py --verify output above)
print('Compare Zenodo file count against manifest — must match')
" (via script file)
```

**GATE:** If uploaded file count != manifest file count → `[BLOCKED: incomplete Zenodo upload]`. Re-upload missing files.

---

## Step 4: Cloudflare Deploy

> **HARD RULE:** NEVER create a new Cloudflare Pages project for an existing publication resource. All QNFO publications deploy under the single `qwav` umbrella project via subdirectory routing (e.g., `/papers/<slug>/`). Creating additional Pages projects for the same resource clutters the dashboard, wastes quota, and creates maintenance burden.

### Pre-Deploy Checklist
- [ ] Verify the target deployment uses `--project-name qwav` (NEVER a new project)
- [ ] Verify the publication deploys to a subdirectory path: `/papers/<kebab-case-title>/`
- [ ] Verify no duplicate R2 artifact already exists at `qnfo/releases/YYYY/MM/<file>.pdf`
- [ ] **Verify HTML is generated from canonical Markdown** (see §4.1 below) — NEVER hand-code publication HTML
- [ ] **Verify MathJax config is BEFORE script tag** — `window.MathJax` config MUST precede `<script id="MathJax-script">` in `index.html`. If config comes after, math WILL NOT render.

### 4.1 HTML Generation from Canonical Markdown (MANDATORY)

**HARD RULE: ALL publication HTML pages MUST be generated from canonical Markdown.** HTML is a derived output format, not a content source. Use the `HTML-PUBLICATION-PAGE` template:

```
fill_prompt_template("HTML-PUBLICATION-PAGE", {
  "title": "<publication_title>",
  "author": "<Author Name (Affiliation)>",
  "date": "<YYYY-MM-DD>",
  "doi": "<10.5281/zenodo.XXXXXXXX>",
  "description": "<one-sentence description>",
  "stylesheet_path": "stylesheets/papers.css",
  "canonical_md_path": "<path/to/paper.md>",
  "extra_macros": "{...}"  // optional publication-specific macros
})
```

The template generates `index.html` from `paper.md` with:
- Correct MathJax config-before-script ordering
- QNFO standard macros (blackboard bold, calligraphic, Greek shortcuts)
- Publication metadata (citation_* meta tags)
- Responsive viewport
- GA4 integration (if measurement ID provided)

### 4.2 MathJax Config Order Verification (MANDATORY)

Before deploying, verify MathJax config ordering in `index.html`:

```bash
python -c "
import sys
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()
config_pos = html.find('window.MathJax')
script_pos = html.find('MathJax-script')
if config_pos == -1:
    print('[BLOCKED] No MathJax config found in index.html!')
    sys.exit(1)
if script_pos == -1:
    print('[BLOCKED] No MathJax script found in index.html!')
    sys.exit(1)
if config_pos > script_pos:
    print('[BLOCKED] MathJax config AFTER script! Math WILL NOT render.')
    print('  Config at pos {}, Script at pos {}'.format(config_pos, script_pos))
    print('  FIX: Move MathJax config <script> BEFORE MathJax-script <script>')
    sys.exit(1)
print('[OK] MathJax config correctly placed BEFORE script.')
print('  Config at pos {}, Script at pos {}'.format(config_pos, script_pos))
" (via script file)
```

**GATE:** If config is AFTER script → `[BLOCKED: MathJax order]`. Fix `index.html` BEFORE deploying. This is the #1 cause of "MathJax isn't rendering."

For the canonical MathJax configuration, see `templates/MATHJAX-CONFIG.md`.

### 4.3 Deploy

```bash
# Deploy to Cloudflare Pages
npx wrangler pages deploy <dir> --project-name qwav --branch main

# Upload PDF to R2
npx wrangler r2 object put qnfo/releases/YYYY/MM/<file>.pdf --file=<path>

# Generate SEO files
# Pull from R2: npx wrangler r2 object get qnfo/tools/generate-seo.py --remote --file=_generate-seo.py
python _generate-seo.py
# Discard: Remove-Item _generate-seo.py
```

---

## Step 5: Social Media Orchestration

Use `fill_prompt_template("SOCIAL-ORCHESTRATOR-TEMPLATE", {...})` to generate posts for all channels.
Post via Buffer API `create_post` tool with `schedulingType: "notification"` for manual approval.

**Channels:** Twitter/X, Bluesky, LinkedIn (Mastodon pending Buffer plan upgrade)

---

## Step 6: Post-Publication Draft Cleanup (MANDATORY — v1.4)

**HARD RULE: After publication is confirmed (Zenodo DOI obtained, Cloudflare deployed), ALL draft and temporary build artifacts MUST be removed.** The published record on Zenodo and R2 is canonical. Draft copies left on disk create version confusion and waste storage.

### Cleanup Protocol

**Step 6.1: Verify canonical copies exist on R2**

```powershell
# Verify PDF on R2
npx wrangler r2 object get qnfo/releases/YYYY/MM/<file>.pdf --remote
# Verify artifact bundle on R2 (if uploaded separately)
npx wrangler r2 object get qnfo/releases/YYYY/MM/<project>-v<MAJOR.MINOR.PATCH>.zip --remote
```

**GATE:** If canonical copies do NOT exist on R2 → `[BLOCKED: canonical missing]`. Upload to R2 before cleaning local drafts.

**Step 6.2: Identify draft files to remove**

| File Pattern | Action | Rationale |
|:-------------|:-------|:----------|
| `*.draft.md` | DELETE | Draft markdowns — canonical is the published PDF + source |
| `*_v[0-9]*.md` (old versions) | DELETE | Older markdown versions — R2 holds versioned releases |
| `*.aux`, `*.log`, `*.out`, `*.toc` | DELETE | LaTeX build artifacts |
| `__pycache__/` | DELETE | Python bytecode cache |
| `_*` (ephemeral files) | DELETE | Temporary build scripts and caches |
| `paper.pdf` (non-versioned) | DELETE | Rename to versioned name before upload, then delete non-versioned copy |
| `output.pdf`, `final.pdf` | DELETE | Generic PDF names — use descriptive versioned filenames |

| File Pattern | Action | Rationale |
|:-------------|:-------|:----------|
| `ARTIFACT-MANIFEST.json` | UPLOAD to R2, then DELETE local | Manifest is part of the published record — archive on R2 |
| Published PDF (versioned) | UPLOAD to R2, then DELETE local | R2 is canonical — local is cache |
| Project source files | UPLOAD to R2, then DELETE local | R2 stores project bundles |

**Step 6.3: Execute cleanup**

```powershell
# Remove draft files
Get-ChildItem -Path "<project_dir>" -Filter "*.draft.md" | Remove-Item -Force
Get-ChildItem -Path "<project_dir>" -Filter "*.aux" | Remove-Item -Force
Get-ChildItem -Path "<project_dir>" -Filter "*.log" | Remove-Item -Force

# Remove ephemeral files
Get-ChildItem -Path "<project_dir>" -Filter "_*" | Remove-Item -Recurse -Force

# Remove __pycache__
if (Test-Path "<project_dir>/__pycache__") {
    Remove-Item -Recurse -Force "<project_dir>/__pycache__"
}

# Remove generic-named PDF copies
if (Test-Path "<project_dir>/paper.pdf") { Remove-Item "<project_dir>/paper.pdf" }
if (Test-Path "<project_dir>/output.pdf") { Remove-Item "<project_dir>/output.pdf" }
if (Test-Path "<project_dir>/final.pdf") { Remove-Item "<project_dir>/final.pdf" }

# Upload manifest and versioned PDF to R2, then delete local
npx wrangler r2 object put qnfo/releases/YYYY/MM/<project>-v<version>/ARTIFACT-MANIFEST.json --file=ARTIFACT-MANIFEST.json
npx wrangler r2 object put qnfo/releases/YYYY/MM/<project>-v<version>/<file>.pdf --file=<file>.pdf
Remove-Item "ARTIFACT-MANIFEST.json"
Remove-Item "<file>.pdf"
```

**Step 6.4: Verify cleanup**

```powershell
# Verify no draft files remain
$drafts = Get-ChildItem -Path "<project_dir>" -Filter "*.draft.md" -ErrorAction Stop
if ($drafts) { Write-Output "FAILED: $($drafts.Count) draft files remain!" } else { Write-Output "Draft cleanup: OK" }

# Verify no ephemeral files remain
$ephemeral = Get-ChildItem -Path "<project_dir>" -Filter "_*" -ErrorAction Stop
if ($ephemeral) { Write-Output "FAILED: $($ephemeral.Count) ephemeral files remain!" } else { Write-Output "Ephemeral cleanup: OK" }

# Verify R2 has canonical copies
npx wrangler r2 object get qnfo/releases/YYYY/MM/<project>-v<version>/<file>.pdf --remote
Write-Output "R2 canonical verified: OK"
```

**GATE:** If any draft/ephemeral files remain OR R2 canonical missing → `[BLOCKED: cleanup incomplete]`.

### Integration with Session Closeout

This cleanup step MUST execute BEFORE session closeout. The closeout-manager skill's `_*` cleanup gate will catch any remaining ephemeral files. If the publication-publisher cleanup was skipped, the closeout gate will fail.

**Post-cleanup state:**
- Zenodo: ALL artifacts archived with DOI (permanent)
- R2: PDF + artifact manifest + project bundle (canonical)
- Cloudflare Pages: Publication deployed (live)
- Local disk: NO drafts, NO ephemeral files, NO non-versioned PDFs

---

## Descriptive Filenames

Use descriptive publication filenames (DEFAULT.md §10):
```
QUANTUM-ERROR-CORRECTION-ULTRAMETRIC-v1.0.pdf
```
NOT: `paper.pdf`, `final.pdf`, `output.pdf`

---


## Embedded Scripts

> **SELF-CONTAINED:** This skill depends on the scripts listed below. Before executing any script, verify it exists at its canonical path. If missing, see the bootstrap note below for recovery.

| Script | R2 Canonical | Execution Cache | Purpose |
|:-------|:-------------|:----------------|:--------|
| `zenodo_publish.py` | `qnfo/tools/zenodo_publish.py` | `_zenodo_publish.py` (ephemeral) | Zenodo DOI registration via REST API |
| `generate-seo.py` | `qnfo/tools/generate-seo.py` | `_generate-seo.py` (ephemeral) | sitemap.xml, robots.txt, llms.txt generator |

> **Note:** `build_pdf.py` is now bundled in the `pdf-builder` skill (`skills/pdf-builder/scripts/build_pdf.py`). Use `skill_view('pdf-builder')` for PDF generation. R2 backup at `qnfo/tools/build_pdf.py`.

### Bootstrap Protocol

**Before using any script, verify it exists:**
```bash
# Pull from R2: npx wrangler r2 object get qnfo/tools/<script>.py --remote --file=_<script>.py
# Verify pull: Test-Path _<script>.py
```

**If script is MISSING:** Scripts are canonical on Cloudflare R2 (`qnfo/tools/`). Pull from R2: `npx wrangler r2 object get qnfo/tools/<script>.py --remote --file=_<script>.py`.
1. Re-pull from R2: `npx wrangler r2 object get qnfo/tools/<script>.py --remote --file=_<script>.py`
2. Check: are you on the correct branch? `git branch --show-current`
3. The canonical source for all tools is the `prompts` repo `tools/` directory.

**Last resort:** If all scripts are missing and unrecoverable from git, flag as `[BLOCKED: missing tools]`.
DO NOT attempt publication without these scripts.

### Dependencies
- `build_pdf.py`: requires `reportlab` and optionally `markdown` packages
- `zenodo_publish.py`: requires `%USERPROFILE%\.zenodo_token` (Zenodo API token with deposit:actions, deposit:write)
- `generate-seo.py`: standard library only, no external dependencies

### Cross-Reference
- `build_pdf.py` is now bundled in the `pdf-builder` skill (`skill_view('pdf-builder')`)
- These scripts are embedded in the `publication-publisher` skill as their primary documentation home

## Reference Files

- Publication standards: DEFAULT.md §11
- PDF builder: `skill_view('pdf-builder')` (bundled skill with `scripts/build_pdf.py`)
- Zenodo: `templates/ZENODO-PUBLISH.md`
- Social orchestrator: `templates/SOCIAL-ORCHESTRATOR-TEMPLATE.md`
- Cloudflare deploy: `templates/CLOUDFLARE-DEPLOYMENT.md`

---

*publication-publisher skill v1.5 — Load on-demand via skill_view(). HTML pages MUST be generated from canonical Markdown with MathJax config BEFORE script.*

---

*publication-publisher v1.5 — QNFO custom skill. Load via read('R2 `qnfo/prompts/skills/publication-publisher\\SKILL.md'). Not accessible via skill_view().*
