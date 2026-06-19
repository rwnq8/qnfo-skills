---
name: cloudflare-deployer
description: Cloudflare platform deployment operations — Pages, R2, Workers, Vectorize, DNS, redirects, and Sandboxes. Use when the agent needs to deploy, manage, or troubleshoot Cloudflare infrastructure.
version: "1.3"
---

# CLOUDFLARE DEPLOYER SKILL — v1.3

> **On-demand skill.** Load via `skill_view('cloudflare-deployer')` for all Cloudflare operations.
> Source: `templates/CLOUDFLARE-DEPLOYMENT.md` v2.1 + QWAV-DEFAULT.md §0.6.5-0.6.7

---

## ⚠️ WRANGLER v4.95+ COMPATIBILITY

**`r2 object list` was REMOVED in wrangler v4.95+.** Only `get`, `put`, `delete` are available.
The `--remote` flag is deprecated (remote is default in v4+). For directory enumeration, deploy a list-objects Worker or use per-object `get` operations.

---

## Authentication

**PERSISTENT -- 2026-06-19:** The CLOUDFLARE_API_TOKEN is stored at User-level with ALL Cloudflare permissions. No manual loading needed. Token survives reboots.

**Token:** API Token with ALL PERMISSIONS (full account access)
- Account: quniverse (edb167b78c9fb901ea5bca3ce58ccc4b)
- Email: rwnquni@outlook.com
- Persistence: User env var (set via [Environment]::SetEnvironmentVariable)
- Token prefix: cfat_Imj... (53 chars)

**Scopes:** ALL Cloudflare policies: Pages (deploy), R2 (read+write+delete), Workers, Vectorize, D1, DNS (zone:edit), redirect rules, zones, AI, sandboxes, queues, pipelines, secrets store.

**S3-compatible access:**
- Endpoint: https://edb167b78c9fb901ea5bca3ce58ccc4b.r2.cloudflarestorage.com
- Access Key ID: 2b87ede317499c6a6a2f8e5c42667c52
- Secret Access Key: stored in persistent env

For direct API calls, use the token via Bearer auth:
```bash
curl -H "Authorization: Bearer $env:CLOUDFLARE_API_TOKEN" https://api.cloudflare.com/client/v4/...
```


-
## Policy Access Matrix (v1.3 — Verified 2026-06-19)

All Cloudflare policies verified via both wrangler CLI and REST API direct calls. Actual enumerated resource counts from the quniverse account.

| Service | Access | Count | API Endpoint | Wrangler Command |
|:--------|:------:|:------|:-------------|:-----------------|
| **R2** | ✅ Read+Write+Delete | 1 bucket (qnfo) | `/accounts/:id/r2/buckets` | `wrangler r2 object {get,put,delete}` |
| **Pages** | ✅ Full | 10 projects | `/accounts/:id/pages/projects` | `wrangler pages project list` |
| **Workers** | ✅ Full | 18 scripts | `/accounts/:id/workers/scripts` | `wrangler deploy` |
| **D1** | ✅ Full | 4 databases | `/accounts/:id/d1/database` | `wrangler d1 list` |
| **KV** | ✅ Full | 2 namespaces | `/accounts/:id/storage/kv/namespaces` | `wrangler kv namespace list` |
| **Vectorize** | ✅ Full | 1 index (qwav-research) | `/accounts/:id/vectorize/indexes` | `wrangler vectorize list` |
| **Queues** | ✅ Full | 4 queues | `/accounts/:id/queues` | `wrangler queues list` |
| **AI (Workers AI)** | ✅ Full | Models available | `/accounts/:id/ai/models/search` | `wrangler ai models list` |
| **Pipelines** | ✅ Full | Configured | `/accounts/:id/pipelines` | `wrangler pipelines` |
| **Hyperdrive** | ✅ Full | Configured | `/accounts/:id/hyperdrive/configs` | `wrangler hyperdrive` |
| **Workflows** | ✅ Full | Configured | `/accounts/:id/workflows` | `wrangler workflows` |
| **DNS / Zones** | ✅ Granted | 0 zones | `/zones` | `wrangler dns` (zone context required) |
| **Secrets Store** | ✅ Granted | Configurable | `/accounts/:id/secrets-store` | `wrangler secrets-store` |
| **AI Search** | ✅ Granted | Configurable | `/accounts/:id/ai-search` | `wrangler ai-search` |
| **Browser Run** | ✅ Granted | Configurable | `/accounts/:id/browser` | `wrangler browser` |
| **Containers** | ✅ Granted | Configurable | `/accounts/:id/containers` | `wrangler containers` |
| **VPC** | ✅ Granted | Configurable | API | `wrangler vpc` |
| **Certificates (mTLS)** | ✅ Granted | Configurable | API | `wrangler cert` / `wrangler mtls-certificate` |
| **Email Routing** | ✅ Granted | Configurable | API | `wrangler email` |
| **Artifacts** | ✅ Granted | Configurable | API | `wrangler artifacts` |
| **Agent Memory** | ✅ Granted | Configurable | API | `wrangler agent-memory` |
| **Web Search** | ✅ Granted | Configurable | API | `wrangler websearch` |
| **Dispatch Namespaces** | ✅ Granted | Configurable | API | `wrangler dispatch-namespace` |
| **Tunnels** | ✅ Granted | Configurable | API | `wrangler tunnel` |

### Available Resources (Enumerated)

**R2 Buckets:** `qnfo` (primary) — audit trails, releases, deployments, tools, projects, discovery index

**D1 Databases (4):**
- `qnfo-graph` (a1954b92-d681-4d02-b1f6-f9a2eb4c265d) — Knowledge graph storage
- `qnfo-audit` (35e2e573-92f3-46ac-83c6-22f6429fc5e5) — Audit trail storage
- `living-paper` (70a58cb3-b2cd-498d-877f-ecca86859a22) — Living paper data
- `portfolio-state` (d80fdf2a-0a60-45a3-968b-2907ce806dcd) — Portfolio state

**KV Namespaces (2):**
- `equation-cache` (2fbbb9fa2d774a6e80d3a3d2547f8b5f) — Equation rendering cache
- `git-on-cloudflare-routes` (3e80529348004360b768e3efea7192a7) — Git proxy routing

**Vectorize Indexes (1):**
- `qwav-research` — 768-dim cosine, QWAV research corpus semantic search

**Queues (4):**
- `emailqueue` (81cffc48) — Email processing
- `git-on-cloudflare-repo-maint` (296cceec) — Git repository maintenance
- `paper-ingestion-queue` (6754f550) — Paper ingestion pipeline
- `pipeline-dedup` (a20a038f) — Pipeline deduplication

**Pages Projects (10):** qwav, prompts-wiki, qnfo-archive, quantum-laws-of-form, qlof-primer, rwnq8, +4 more

**Workers (18 scripts):** Deployed — query via `wrangler deployments` with specific worker names

-

## Cloudflare Pages

```bash
# List all Pages projects
npx wrangler pages project list

# Deploy
npx wrangler pages deploy <dir> --project-name <name> --branch main

# Custom domain
npx wrangler pages project set-domain <name> <domain>

# Deployment history
npx wrangler pages deployment list --project-name <name>

# Rollback
npx wrangler pages deployment rollback --project-name <name>
```

**Active Projects:** qwav (deep.qwav.tech), prompts-wiki, qnfo-archive (archive.qnfo.org),
quantum-laws-of-form (laws.qnfo.org), qlof-primer (primer.qwav.tech), +11 more.

### Post-Deploy MathJax Verification (MANDATORY for Publication Pages)

After deploying ANY publication page to Cloudflare Pages, verify MathJax is correctly configured:

```bash
python -c "
import urllib.request, sys
url = sys.argv[1]
html = urllib.request.urlopen(url).read().decode('utf-8')
config_pos = html.find('window.MathJax')
script_pos = html.find('MathJax-script')
if config_pos == -1:
    print(f'[BLOCKED] No MathJax config found on {url}')
    sys.exit(1)
if script_pos == -1:
    print(f'[BLOCKED] No MathJax script found on {url}')
    sys.exit(1)
if config_pos > script_pos:
    print(f'[BLOCKED] MathJax config AFTER script on {url} — math WILL NOT render.')
    print(f'  Config pos: {config_pos}, Script pos: {script_pos}')
    sys.exit(1)
print(f'[OK] MathJax correctly configured on {url}')
print(f'  Config pos: {config_pos}, Script pos: {script_pos}')
" (via script file) <deployed-url>
```

**CRITICAL:** The `window.MathJax` configuration MUST come BEFORE the `<script id="MathJax-script">` tag. If config is after the script, MathJax initializes without macros and math will NOT render. This is the #1 cause of "MathJax isn't rendering."

For the canonical MathJax configuration, see `templates/MATHJAX-CONFIG.md` and `templates/HTML-PUBLICATION-PAGE.md`.

---

## Cloudflare R2 (Object Storage)

```bash
# Get an object (v4.95+ compatible)
npx wrangler r2 object get qnfo/audit/state/<project>.json

# Put an object
npx wrangler r2 object put qnfo/audit/state/<project>.json --file=<local-file>

# Delete an object
npx wrangler r2 object delete qnfo/audit/state/<project>.json

# NOTE: r2 object list does NOT exist in v4.95+
# Use per-object get operations instead
```

**Primary bucket:** `qnfo`
**R2 paths:** `qnfo/audit/state/`, `qnfo/audit/backlog/`, `qnfo/audit/decisions/`,
`qnfo/releases/YYYY/MM/`, `qnfo/deployments/`

---

## Cloudflare Workers

```bash
# Deploy a worker
npx wrangler deploy --name <worker-name>

# Deployment history
npx wrangler deployments list
```

---

## Cloudflare Sandboxes

```bash
# Create
npx wrangler sandbox create <name> --image ubuntu-22.04

# Execute
npx wrangler sandbox exec <name> -- "<command>"

# List
npx wrangler sandbox list

# Stop (cost: $0 when paused)
npx wrangler sandbox stop <name>
```

---

## Vectorize (Semantic Search)

For paper vectorization, use:
```bash
# Pull from R2: npx wrangler r2 object get qnfo/tools/vectorize-papers.py --remote --file=_vectorize-papers.py
python _vectorize-papers.py
# Discard: Remove-Item _vectorize-papers.py
```

---

## Cost Gate

| Resource | Free Tier | Overage |
|:---------|:----------|:--------|
| Pages builds | 500/month | Builds queue |
| Pages bandwidth | Unlimited | N/A |
| Workers requests | 100k/day | $0.30/M |
| R2 storage | 10 GB | $0.015/GB/mo |
| R2 egress | **Free** | N/A |
| Sandboxes | Free quota | $0.002/min |

---

## Common Patterns

### Deploy a Publication
```bash
# 1. Build PDF
# Pull from R2: npx wrangler r2 object get qnfo/tools/build_pdf.py --remote --file=_build_pdf.py
python _build_pdf.py
# Discard: Remove-Item _build_pdf.py --input <file>

# 2. Deploy to Pages
npx wrangler pages deploy <dir> --project-name qwav --branch main

# 3. Upload PDF to R2
npx wrangler r2 object put qnfo/releases/YYYY/MM/<file>.pdf --file=<path>

# 4. Generate SEO
# Pull from R2: npx wrangler r2 object get qnfo/tools/generate-seo.py --remote --file=_generate-seo.py
python _generate-seo.py
# Discard: Remove-Item _generate-seo.py
```

### Check Infrastructure Health
```bash
npx wrangler whoami
npx wrangler pages project list
npx wrangler r2 object get qnfo/audit/state/qwav.json
```

---

## Reference Files

- Full deployment template: `templates/CLOUDFLARE-DEPLOYMENT.md`
- Cloudflare audit: `qnfo/SESSION-HANDOFF-2026-05-28.md`
- SEO generator: `_generate-seo.py` (R2: `qnfo/tools/generate-seo.py`)
- Vectorize: `_vectorize-papers.py` (R2: `qnfo/tools/vectorize-papers.py`)

---


## Embedded Scripts

> **SELF-CONTAINED:** This skill depends on the scripts listed below. Before executing any script, verify it exists at its canonical path.

| Script | R2 Canonical | Execution Cache | Purpose |
|:-------|:-------------|:----------------|:--------|
| `vectorize-papers.py` | `qnfo/tools/\vectorize-papers.py` | Index papers in Cloudflare Vectorize for semantic search |
| `build_pdf.py` | `qnfo/tools/\build_pdf.py` | Markdown/HTML -> PDF (shared with publication-publisher) |

### Bootstrap Protocol

Before using any script, verify it exists:
```bash
# Pull from R2: npx wrangler r2 object get qnfo/tools/<script>.py --remote --file=_<script>.py
# Verify: Test-Path _<script>.py
```

**If script is MISSING:** Scripts are version-controlled in the prompts repo.
1. `git log --oneline -- qnfo/tools/<script>.py`
2. The canonical source for all tools is R2 (`qnfo/tools/`). Pull from R2: `npx wrangler r2 object get qnfo/tools/<script>.py --remote --file=_<script>.py`.

**Shared scripts:** `build_pdf.py` is primarily maintained in the `publication-publisher` skill.
If missing, check that skill's Embedded Scripts section for recovery guidance.

### Dependencies
- `vectorize-papers.py`: requires Cloudflare API token (`%USERPROFILE%\.cloudflare\api-token`) and Workers AI access
- `build_pdf.py`: requires `reportlab` and optionally `markdown` packages


*cloudflare-deployer skill v1.3 — Load on-demand via skill_view(). Compatible with wrangler v4.95+*

---

*cloudflare-deployer v1.3 — QNFO custom skill. Load via read('R2 `qnfo/prompts/skills/cloudflare-deployer\\SKILL.md'). Not accessible via skill_view().*
