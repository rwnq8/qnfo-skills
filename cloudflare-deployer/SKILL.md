---
name: cloudflare-deployer
description: Cloudflare platform deployment operations — Pages, R2, Workers, Vectorize, DNS, redirects, and Containers. Use when the agent needs to deploy, manage, or troubleshoot Cloudflare infrastructure.
version: "2.1"
---


---

# CLOUDFLARE DEPLOYER SKILL — v2.1

> **On-demand skill.** Load via `skill_view('cloudflare-deployer')` for all Cloudflare operations.
> Source: `templates/CLOUDFLARE-DEPLOYMENT.md` v2.1 + QWAV-DEFAULT.md §0.6.5-0.6.7

---
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

**Scopes:** ALL Cloudflare policies: Pages (deploy), R2 (read+write+delete), Workers, Vectorize, D1, DNS (zone:edit), redirect rules, zones, AI, containers, queues, pipelines, secrets store.

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
| **Pages** | ✅ Full | 10 projects (5 active, 5 dormant/support) | `/accounts/:id/pages/projects` | `wrangler pages project list` |
| **Workers** | ✅ Full | 30 scripts | `/accounts/:id/workers/scripts` | `wrangler deploy` |
| **D1** | ✅ Full | 5 databases | `/accounts/:id/d1/database` | `wrangler d1 list` |
| **KV** | ✅ Full | 2 namespaces | `/accounts/:id/storage/kv/namespaces` | `wrangler kv namespace list` |
| **Vectorize** | ✅ Full | 3 indexes (qwav-research-v2, qnfo-handoffs, qnfo-tasks) | `/accounts/:id/vectorize/indexes` | `wrangler vectorize list` |
| **Queues** | ✅ Full | 2 queues | `/accounts/:id/queues` | `wrangler queues list` |
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

**D1 Databases (5):**
- `qnfo-cms` (0458a344) — CMS content management (34 entries, 5 types)
- `qnfo-graph` (a1954b92-d681-4d02-b1f6-f9a2eb4c265d) — Knowledge graph storage
- `qnfo-audit` (35e2e573-92f3-46ac-83c6-22f6429fc5e5) — Audit trail storage
- `living-paper` (70a58cb3-b2cd-498d-877f-ecca86859a22) — **CANONICAL QNFO PUBLICATIONS DATABASE** (170 papers, table: `papers`). Single source of truth for all QNFO-authored papers/publications/releases. Queried directly by papers-server Worker (D1 binding `env.DB`). Updated by publication-publisher skill (Stage 2.5).
- `portfolio-state` (d80fdf2a-0a60-45a3-968b-2907ce806dcd) — Portfolio state

**KV Namespaces (1):**
- `equation-cache` (2fbbb9fa2d774a6e80d3a3d2547f8b5f) — Equation rendering cache
- ~~`git-on-cloudflare-routes`~~ — DEPRECATED (GitHub fully deprecated per ADR-001)

**Vectorize Indexes (3):**
- `qwav-research-v2` — 1024-dim cosine, active (bge-m3 compatible). Used by ask-qwav Worker.
- `qnfo-handoffs` — 768-dim cosine, handoffs semantic search
- `qnfo-tasks` — 768-dim cosine, tasks semantic search
- ~~`qwav-research` (768-dim)~~ — DELETED (replaced by v2)
- ~~`paper-similarity` (1024-dim)~~ — DELETED (empty, redundant)

**Queues (2):**
- `qnfo-lifecycle-queue` — Lifecycle pipeline (archival jobs, auto-transitions)
- `git-on-cloudflare-repo-maint` (296cceec) — Git repository maintenance (DEPRECATED — GitHub deprecated per ADR-001)

**Pages Projects (5):** qnfo-hub (qnfo.org, www.qnfo.org), qnfo-publications (papers.qnfo.org), qnfo-legal (legal.qnfo.org), qwav (deep.qwav.tech), qnfo-design-system (design.qnfo.org)

**Workers (26 scripts):** Deployed — key workers include `graph-api` (Knowledge Graph), `qnfo-lifecycle` (automated project lifecycle, cron: daily 06:00 UTC), `living-papers-api` (Living Papers with D1 + IPFS), `qnfo-archive-worker` (queue consumer for R2 archival migration), `qnfo-archive-verify` (archive verification), `umbrella-router` (traffic routing). Query via `wrangler deployments` with specific worker names.

-

## Prerequisites

1. **Cloudflare API Token** — auto-available via `$env:CLOUDFLARE_API_TOKEN` (User-level env var, survives reboots). Verify: `npx wrangler whoami` must show account `quniverse`.
2. **Node.js 18+ / npm** — required for `npx wrangler`. Verify: `node --version`.
3. **Python 3.8+** — required for build scripts and R2 utilities.
4. **Network access** — `api.cloudflare.com` must be reachable.
5. **Git workspace** — all operations must run from within a git-tracked project directory.

**Pre-flight check:**
```bash
npx wrangler whoami              # Must show quniverse account
node --version                    # Must be >= 18
python --version                  # Must be >= 3.8
```

---

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

### Post-Deploy Verification (MANDATORY for ALL deploys — v1.7)

**This is the deployment instance of the RED-TEAM → DoD → ITERATE → REFINE cycle.** See `skill_view('red-team-dod')` for the canonical framework.

After deploying ANY content to Cloudflare Pages or Workers, run the post-deploy red-team:

```bash
# Pull test suite from R2 (ephemeral)
npx wrangler r2 object get qnfo/tools/test_suite.py --remote --file=_test_suite.py

# Run deploy verification (Pages + CMS + KG)
python _test_suite.py --cms --pages --kg

# Content quality gate — MUST PASS
python _test_suite.py --content

# Discard
Remove-Item _test_suite.py
```

**GATE:** If ANY test marked `CRIT` fails → deployment is NOT complete. Fix before claiming [EXECUTED].
**GATE:** If ANY page shows `stub=True` → deployment is REJECTED. Content must be professional.
**GATE:** If ANY publication shows `EMPTY body` → content is NOT ready.

### Post-Deploy Redirect Verification (MANDATORY for Redirect Deployments)

After deploying redirects, verify they actually work:

```bash
python _dod_enforce.py --preflight-only && python _test_suite.py --redirects
```

**GATE:** `_dod_enforce.py` must return exit 0 AND `_test_suite.py --redirects` must show all redirects as PASS.

### Post-Deploy MathJax Verification (MANDATORY for Publication Pages)

After deploying ANY publication page to Cloudflare Pages, verify MathJax is correctly configured:

```bash
# Post-deploy MathJax verification — write check script, execute, discard
echo "import urllib.request, sys; url = sys.argv[1]; html = urllib.request.urlopen(url).read().decode('utf-8'); config_pos = html.find('window.MathJax'); script_pos = html.find('MathJax-script'); assert config_pos >= 0, f'MathJax config missing on {url}'; assert script_pos >= 0, f'MathJax script missing on {url}'; assert config_pos < script_pos, f'Config AFTER script on {url}'; print(f'[OK] MathJax correct: config@{config_pos}, script@{script_pos}')" > _verify_cf_mathjax.py
python _verify_cf_mathjax.py <deployed-url>
Remove-Item _verify_cf_mathjax.py
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

## Cloudflare Containers

```bash
# Create
npx wrangler containers create <name> --image ubuntu-22.04

# Execute
npx wrangler containers exec <name> -- "<command>"

# List
npx wrangler containers list

# Stop
npx wrangler containers stop <name>
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
| Containers | Free quota | $0.002/min |

---


---

## Naming Conventions (v2.0 — 2026-07-01)

> **CRITICAL:** The 2026-07-01 audit found 8 resources named "living paper" and 2 labeled "CMS." Confusing names lead to wrong architecture decisions.

### Rules

| Rule | Rationale |
|:-----|:----------|
| **NO new "CMS" names.** The word "CMS" misled the architecture. Use "dynamic renderer" or "page content" instead. | The `cms-api` Worker returned 404. The `qnfo-cms` D1 has 34 page entries — not a CMS. |
| **"living-paper" = CANONICAL PUBLICATIONS DATABASE.** The `living-paper` D1 (70a58cb3) is the single source of truth for all QNFO papers. Despite the confusing name, it's the definitive database. | Avoids creating paper data in multiple places. |
| **One name, one purpose.** No `living-paper-api` AND `living-papers-api` doing different things. | Current state: 5 Workers with "living-paper" in name. Future: consolidate. |
| **Dormant resources MUST be documented.** 5 Pages projects are dormant (no domains, no content). Agents must know they exist but shouldn't deploy to them. | Prevents dead domains and confusion. |

### Current State

| Name | What It Actually Is |
|:-----|:--------------------|
| `living-paper` D1 | **CANONICAL QNFO PUBLICATIONS DATABASE** — papers table, 170 papers |
| `qnfo-cms` D1 | Page content (34 entries — hub text, legal, navigation) — NOT a CMS |
| `cms-api` Worker | **DELETED 2026-07-01** — was returning 404, non-functional |
| `living-paper-api` Worker | Legacy publications API (may duplicate ask-qwav) |
| `living-papers-api` Worker | Legacy publications API (note plural — different from above) |
| `living-paper-ai` Worker | AI-enhanced paper queries |
| `living-paper-proxy` Worker | Proxy for paper access |
| `archive.qnfo.org` | Archive page — title changed from "QNFO Living Papers" to "QNFO Research Archive" (2026-07-01) |

## R2 Migration & Thin-Client Enforcement (Merged from local-to-r2-migration skill)

> **Thin-Client Mandate:** The ONLY files that persist locally are the DeepChat runtime (`qnfo/prompts/`). Everything else lives on R2.

### File Classification

| Classification | Pattern | Action |
|:---------------|:--------|:-------|
| **ORPHANED-EPHEMERAL** | `_*` prefix | DELETE immediately |
| **PYTHON-CACHE** | `__pycache__/`, `*.pyc` | DELETE |
| **BUILD-ARTIFACT** | `*.o`, `*.rmeta`, `*.d` | DELETE |
| **R2-MIGRATION-CANDIDATE** | `.md`, `.py`, `.json`, `.html`, etc. | UPLOAD to R2 → verify → delete local |
| **IMPORT-SURFACE** | Inside `qnfo/prompts/` | SKIP |
| **UNKNOWN** | Everything else | ASK USER |

### Usage

```bash
# Full migration: scan → purge → upload → index → cleanup
npx wrangler r2 object get qnfo/tools/migration_scanner.py --remote --file=_migration_scanner.py
python _migration_scanner.py --scan "qnfo/projects" --output _migration_report.json
```

**R2 path convention:** `qnfo/projects/<project>/<file>` → `qnfo/projects/<project>/<file>`

All 28 QNFO DeepChat skills are redundantly backed up. This skill itself is recoverable from:

| Source | Location | Recovery Command |
|:-------|:---------|:-----------------|
| **GitHub** | `rwnq8/qnfo-skills` | `git clone https://github.com/rwnq8/qnfo-skills.git %APPDATA%\.deepchat\skills` |
| **R2** | `qnfo/prompts/skills/cloudflare-deployer/SKILL.md` | `python bootstrap_skills.py --source r2` |
| **Discovery Index** | `qnfo/discovery/index.json` (skills_backup) | JSON lookup |

**Bootstrap tools on R2:**
- `qnfo/tools/bootstrap_skills.py` — One-command restore from GitHub or R2
- `qnfo/tools/skills-recovery-guide.md` — Full recovery documentation

**Keep synced after any skill change:**
```bash
python "%APPDATA%\.deepchat\skills\bootstrap_skills.py" --sync
```
This pushes to GitHub AND uploads to R2 in a single command.

## DNS Hygiene Rules (v1.9 — 2026-07-01)

> **CRITICAL:** The 2026-07-01 front-end audit found 28 dead DNS records, 6 duplicate CNAMEs, and 4 redirect chains. These rules prevent recurrence.

### Core Rules

1. **NEVER create a DNS CNAME record without verifying the target Pages project exists AND the domain is registered on it.** CNAME to `.pages.dev` without custom domain registration = 404/522.
2. **NEVER create a redirect rule that chains to another redirect.** Single-hop only. Target must resolve to HTTP 200.
3. **After ANY DNS change, verify resolution:** `curl -sI https://<domain> | head -1` must return 200.
4. **Audit all DNS records against live Pages projects before every deployment.** Delete records pointing to non-existent projects.
5. **Every domain must resolve to a page.** No dead domains. No domains serving the same content as another (unless intentional mirror).
6. **NEVER chain CNAMEs to `.pages.dev`.** Every CNAME to `.pages.dev` must be DIRECT (1 hop). Chains like `X → Y → qwav.pages.dev` are fragile — if Y breaks, X breaks too. Repoint all chain CNAMEs directly to the ultimate `.pages.dev` target. See infrastructure-audit §0.9 for automated chain detection.

### Pre-DNS-Change Checklist (v2.1 — MANDATORY)

> **2026-07-01:** Resource proliferation was the #1 failure mode. Before creating ANY DNS record, verify current resource counts are within baseline and the target exists.

| Check | Command |
|:------|:--------|
| **Worker routes < 8?** | Count routes — if ≥ 8, audit for orphans first |
| **Workers < 30?** | Count Workers — if ≥ 30, delete dead ones first |
| **DNS records < 20?** | Count DNS — if ≥ 20, run resolution sweep first |
| Target Pages project exists? | `cf pages/projects/<name>` must return 200 |
| Target Worker deployed? | `cf workers/scripts/<name>` must return 200 |
| Domain registered on target? | List Pages project domains — target must be present. **If missing: POST /accounts/:id/pages/projects/:name/domains** |
| Domain not already serving something? | `curl -sI https://<domain>` — note current status |
| No redirect chain? | If target is a CNAME, verify the CNAME target itself resolves to 200 |
| **No 522 risk? (NEW v2.1)** | **Run §0.8 cross-reference: every CNAME→`.pages.dev` has matching domain registration** |

### Post-DNS-Change Verification

```python
# Verify every DNS record resolves to HTTP 200 within 60 seconds
import urllib.request, ssl, json
ctx = ssl.create_default_context()
for record in dns_records:
    url = f"https://{record['name']}"
    try:
        resp = urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent':'Mozilla/5.0'}), timeout=10, context=ctx)
        assert resp.status == 200, f"Expected 200, got {resp.status}"
        print(f"  [OK] {record['name']} -> HTTP 200 ({len(resp.read())}B)")
    except Exception as e:
        print(f"  [FAIL] {record['name']} -> {e}")
        # DELETE the DNS record if it cannot resolve
```

### Domain Page Classification (v2.0 — 2026-07-01)

> **Every domain must be classified as LANDING or CONTENT.** This prevents the #2 failure mode: content pages linked as landing pages, and vice versa.

| Class | Definition | Example |
|:------|:-----------|:--------|
| **LANDING** | Hub/CMS/index page with navigation and search | qnfo.org (hub), papers.qnfo.org (index) |
| **CONTENT** | Individual paper/publication/project page | papers.qnfo.org/papers/<slug>/ (paper), deep.qwav.tech (QWAV) |
| **REDIRECT** | CNAME transparently pointing to another domain | qnfo.net → qnfo.org |
| **API** | Worker endpoint, not a user-facing page | graph-api.qnfo.org |

**Rule:** LANDING pages may link to CONTENT or other LANDING pages. CONTENT pages should link BACK to LANDING pages (nav). No CONTENT → CONTENT links without an intermediate LANDING/index page.

### Domain Lifecycle

| Phase | Duration | Action |
|:------|:---------|:-------|
| CREATE | Immediate | Only with verified target + user request. Domain MUST be added to Pages project AND classified. |
| ACTIVE | Indefinite | Must resolve to HTTP 200. Must be classified (LANDING/CONTENT). |
| DEPRECATED | 7 days | Serve redirect notice → hub, then DELETE |
| DELETE | Immediate | Remove DNS record FIRST, then remove from Pages project domains |

### Post-DNS-Change Resolution Audit (MANDATORY — v2.0)

After ANY DNS change, execute this verification within 60 seconds:

```python
# Audit: every domain must resolve to HTTP 200
import urllib.request, ssl
ctx = ssl.create_default_context()
HEADERS = {'User-Agent': 'Mozilla/5.0'}

ALL_DOMAINS = [
    # LANDING
    'qnfo.org', 'papers.qnfo.org', 'legal.qnfo.org',
    # CONTENT
    'deep.qwav.tech', 'design.qnfo.org', 'archive.qnfo.org',
    # REDIRECT zones
    'www.qnfo.net', 'q08.org', 'www.qnfo.uk',
]

for domain in ALL_DOMAINS:
    url = f'https://{domain}'
    try:
        resp = urllib.request.urlopen(urllib.request.Request(url, headers=HEADERS), timeout=10, context=ctx)
        if resp.status == 200:
            print(f'  [OK] {domain}')
        else:
            print(f'  [FAIL] {domain}: HTTP {resp.status} — DELETE DNS RECORD')
    except Exception as e:
        print(f'  [FAIL] {domain}: {e} — DELETE DNS RECORD')
```

**GATE:** Every domain in ALL_DOMAINS must return HTTP 200. Any that fail → DELETE the DNS record. Deleted records are better than dead domains.

---

## Dynamic Publication Deployment (v1.9 — Replaces Static Pages Deploy)

> **2026-07-01:** Individual paper pages are now served dynamically by the `papers-server` Worker — no static HTML upload to Pages needed.

### For new papers:

1. **Upload canonical markdown to R2:**
```bash
npx wrangler r2 object put qnfo/releases/YYYY/MM/<slug>/paper.md --file=<md-path>
npx wrangler r2 object put qnfo/releases/YYYY/MM/<slug>/paper.pdf --file=<pdf-path>
```

2. **Update D1 metadata** (living-paper database, papers table):
```sql
INSERT INTO papers (id, title, authors, doi, abstract, published, ipfs_cid) 
VALUES ('<slug>', '<title>', '<authors>', '<doi>', '<abstract>', '<date>', '<cid>');
```

3. **Verify paper appears:** `curl -s https://papers.qnfo.org/papers/<slug>/ | grep '<title>'`

**No Pages deployment needed.** The `papers-server` Worker queries D1 directly (via D1 binding `env.DB`) and fetches markdown from R2 (via R2 binding `env.PAPERS_BUCKET`). New papers appear automatically.

### Paper falls into ONE of TWO tiers:

| Tier | Data Source | What You See |
|:-----|:-----------|:-------------|
| **Metadata-only** | D1 (title, authors, DOI, abstract) | Title, author, DOI link, abstract |
| **Full content** | D1 + R2 markdown | Full paper rendered with MathJax |

When `qnfo/releases/YYYY/MM/<slug>/paper.md` exists on R2 → full content. Otherwise → metadata-only (still works, just shows abstract).

---

## Common Patterns

### Deploy a Publication

> **Design System v3.0 (LOCKED 2026-07-01):** All pages must match papers.qnfo.org canonical design.
> Design doc: `qnfo/design-system/QNFO-DESIGN-SYSTEM.md`
> PDF Builder: `qnfo/design-system/build_pdf.py` (v3.0)
> 🚫 **DARK THEMES FORBIDDEN.** Inter + Source Serif 4, #1a56db blue palette, 960px max-width.
```bash
# 1. Build PDF
# Pull from R2: npx wrangler r2 object get qnfo/design-system/build_pdf.py --remote --file=_build_pdf.py
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

### Verify Design System
```bash
# Check if a page uses the light theme
python -c "import urllib.request;h=urllib.request.urlopen('https://papers.qnfo.org/').read().decode();print('DARK' if '#0a0a0f' in h or '#0d1117' in h else 'LIGHT')"
```

---
