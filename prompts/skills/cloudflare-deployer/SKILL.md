---
name: cloudflare-deployer
description: "Cloudflare platform deployment operations -- Pages, R2, Workers, Vectorize, DNS, redirects, and Containers. Use when user says deploy, ship to production, host on Cloudflare, or push to Cloudflare, or when the agent needs to deploy, manage, or troubleshoot Cloudflare infrastructure."
version: "1.3"
---


### DEC-034 Safe Deploy Protocol (v1.5 — 2026-07-10)

**CRITICAL:** Multiple LLM sessions can deploy Workers, Pages, or DNS records simultaneously. Without coordination, the last deploy silently overwrites prior changes. ALL Cloudflare deployments MUST use the InfraLockManager DO for concurrency control.

**Safe Deploy Flow:** lock(resource) → deploy → verify → unlock

**Resource Lock Matrix:** Worker: worker:<name> (600s), Pages: pages:<project> (600s), DNS: dns:<zone>:<record> (300s), R2: r2:<path> (300s), KV: kv:<ns>:<key> (120s), Vectorize: vectorize:<index> (300s)

**Collision Handling:** Exponential backoff (1s, 2s, 4s) on LockCollision. Max 3 retries.

**DO endpoint:** `https://infra-lock-manager.q08.workers.dev`
**Client:** `infra_lock_client.py` | **Protocol:** DEC-034 Universal Multi-Session Write Collision Prevention


> **INCLUDES AUTONOMOUS RED-TEAM SELF-AUDIT.** Before claiming this skill complete, autonomously run: (1) Output Verification -- negative verification. (2) Assumption Challenge -- state and test every assumption. (3) Edge Case Check -- empty/null/max/boundary/desync. (4) DoD Integration -- run _dod_enforce.py if exists. (5) Iteration -- retry on failure, max 3. ANTI-PATTERN: User should NEVER ask about quality.


### Domain Self-Critique (Post-Deployment)

After every Cloudflare deployment, autonomously verify:
- **522 prevention:** For every CNAME to .pages.dev, is the domain registered on the target Pages project? Run infrastructure-audit sec 0.8 cross-reference.
- **Wrangler version compatibility:** Is the current wrangler version compatible? Check for deprecated commands (e.g., r2 object list removed in v4.95+).
- **Caching drift:** Did the deployment actually reach users? curl the production URL with ?cache-bust=timestamp and compare against local build.
- **Stale build artifacts:** Are there orphaned deployments? Check wrangler pages deployment list for stale preview deployments.

> **Related:** infrastructure-audit, closeout-manager, github-cloudflare-sync



### Programmatic Loading & Execution
This skill is loaded and executed **programmatically by the LLM system** 
during response generation. Loading is triggered automatically via 
`skill_view('cloudflare-deployer')` or `read()` with filesystem path.
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

### DEC-034 Safe Deploy Protocol (v1.5 — 2026-07-10)

CRITICAL: Multiple LLM sessions can deploy Workers/Pages/DNS simultaneously. Use InfraLockManager DO.
Lock matrix: worker:<name>(600s), pages:<project>(600s), dns:<zone>:<record>(300s), r2:<path>(300s), kv:<ns>:<key>(120s).
DO: https://infra-lock-manager.q08.workers.dev | Protocol: DEC-034


# CLOUDFLARE DEPLOYER SKILL — v1.3 — v2.2

> **On-demand skill.** Load via `skill_view('cloudflare-deployer')` for all Cloudflare operations.
> Source: `templates/CLOUDFLARE-DEPLOYMENT.md` v2.1 + QWAV-DEFAULT.md §0.6.5-0.6.7

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
  {"step": "Verify wrangler auth", "status": "pending"},
  {"step": "Pull test suite from R2", "status": "pending"},
  {"step": "Pull build script from R2", "status": "pending"},
  {"step": "Build publication artifacts", "status": "pending"},
  {"step": "Deploy to Cloudflare Pages", "status": "pending"},
  {"step": "Run post-deploy red-team verification", "status": "pending"},
  {"step": "Verify MathJax config on deployed page", "status": "pending"},
  {"step": "Upload artifacts to R2", "status": "pending"},
  {"step": "Clean up ephemeral files", "status": "pending"},
])

### Autonomous Continuation Protocol (v2.4)

**Composite deployment operations execute autonomously without user intervention.** The agent MUST:

1. After ANY step marked [EXECUTED] with tool evidence, immediately proceed to the next step
2. Before advancing to next deployment phase: tag `[AUTO-CONTINUE -> <phase>]` in the response
3. If a deployment fails: tag `[BLOCKED: reason]`, attempt retry (max 3), then fall back to REST API if wrangler fails
4. **Composite deploy:** When deploying a full publication, chain: Pages → R2 → DNS verify → redirect check → cleanup — as a single autonomous sequence
5. At completion of all steps: tag `[DEPLOY-COMPLETE: <url>]`
6. **Post-deploy red-team:** After every deployment, autonomously verify: 522 prevention, wrangler version compatibility, caching drift, stale build artifacts
7. Never wait for user confirmation between deployment steps

**ANTI-PATTERN:** User should NEVER need to say "CONTINUE" between deployment operations. The agent autonomously chains all deployment steps into a single composite deploy.

---

## ⚠️ WRANGLER v4.95+ COMPATIBILITY

**`r2 object list` was REMOVED in wrangler v4.95+.** Only `get`, `put`, `delete` are available.
The `--remote` flag is **REQUIRED** for remote R2 access. Without it, wrangler defaults to local R2 simulator. Verified: wrangler v4.107.0 outputs "Resource location: local — Use --remote if you want to access the remote instance." For directory enumeration, deploy a list-objects Worker or use per-object `get` operations.

**R2 Object Listing via REST API (WORKAROUND for wrangler 4.x `r2 object list` removal):** The Cloudflare REST API supports R2 object enumeration even when the wrangler CLI does not:

```python
# List R2 objects via REST API
import urllib.request, json
url = f'https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/r2/buckets/{BUCKET}/objects?prefix={prefix}'
req = urllib.request.Request(url, headers={'Authorization': f'Bearer {TOKEN}'})
result = json.loads(urllib.request.urlopen(req).read())
# NOTE: result is a flat LIST of objects, NOT a dict with "objects" key
# Parse: for obj in result["result"]: print(obj["key"], obj["size"])
```

**CAUTION:** The response `result` is a FLAT LIST (not `{"objects": [...]}`). Code that does `result.get("objects", [])` will silently return empty — this was the root cause of false "0 objects" reports in multiple sessions (2026-07-04).

---

## Authentication

**PERSISTENT -- 2026-06-19 (UPDATED 2026-07-10):** The CLOUDFLARE_API_TOKEN is stored at User-level with ALL Cloudflare permissions. No manual loading needed. Token survives reboots. **CRITICAL: As of 2026-07-10, `CF_API_TOKEN` (cfat_Imj...) is the working token. `CLOUDFLARE_API_TOKEN` (cfat_ffMOS...) is STALE/INVALID. Set `$env:CLOUDFLARE_API_TOKEN = $env:CF_API_TOKEN` at session start until the env var is updated.**

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
| **Workers** | ✅ Full | 25 scripts | `/accounts/:id/workers/scripts` | `wrangler deploy` |
| **D1** | ✅ Full | 5 databases | `/accounts/:id/d1/database` | `wrangler d1 list` |
| **KV** | ✅ Full | 2 namespaces | `/accounts/:id/storage/kv/namespaces` | `wrangler kv namespace list` |
| **Vectorize** | ✅ Full | 3 indexes (qwav-research-v2, qnfo-handoffs, qnfo-tasks) | `/accounts/:id/vectorize/v2/indexes` | `wrangler vectorize list` |
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
| **Secrets Store** | ✅ Full | 1 store (default_secrets_store), 20 secrets | `/accounts/:id/secrets_store` | `wrangler secrets-store` [open beta] |
| **Flagship (Feature Flags)** | ✅ Granted | Configurable | API | `wrangler flagship` [open beta] |
| **Versions (Gradual Rollout)** | ✅ Full | Available | API | `wrangler versions upload/deploy/list` |
| **Triggers** | ✅ Full | Available | API | `wrangler triggers deploy` [experimental] |
| **VPC** | ✅ Granted | Configurable | API | `wrangler vpc service` [open beta] |
| **Web Search** | ✅ Granted | Configurable | API | `wrangler websearch search` [experimental] |
| **Cert (Client mTLS)** | ✅ Granted | Configurable | API | `wrangler cert upload/list/delete` [open beta] |
| **Artifacts** | ✅ Granted | Configurable | API | `wrangler artifacts` [private beta] |
| **Dispatch Namespaces** | ✅ Full | Configurable | API | `wrangler dispatch-namespace` |
| **Preview Deployments** | ✅ Full | Configurable | API | `wrangler preview` [private beta] |
| **Email Sending** | ✅ Granted | Configurable | API | `wrangler email sending` [open beta] |

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

**Pages Projects (10):** 5 active — qnfo-hub (qnfo.org, www.qnfo.org), qnfo-publications (papers.qnfo.org), qnfo-legal (legal.qnfo.org), qwav (deep.qwav.tech), qnfo-design-system (design.qnfo.org); 5 dormant — cocyle, different-physics, qlof-primer, quantum-laws-of-form, prompts-wiki

**Workers (25 scripts):** Deployed — including `qnfo-agent-session` (DO+SQLite, 2026-07-04), `qnfo-ai-worker` (Workers AI, 2026-07-04), `paper-catalog` (2026-07-04) Deployed — key workers include `graph-api` (Knowledge Graph), `qnfo-lifecycle` (automated project lifecycle, cron: daily 06:00 UTC), `living-papers-api` (Living Papers with D1 + IPFS), `qnfo-archive-worker` (queue consumer for R2 archival migration), `qnfo-archive-verify` (archive verification), `umbrella-router` (traffic routing). Query via `wrangler deployments` with specific worker names.

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

### Embedded Script: test_suite.py (self-sufficient — no R2 pull needed)

Write the following code to `_test_suite.py`, execute, then delete:

```python
#!/usr/bin/env python3
"""QNFO Test Suite v1.1 — redirects deprecated. --quick / --redirects / --handoff-verify / --all"""
import argparse, json, os, ssl, sys, http.client as hc, urllib.request
from datetime import datetime, timezone

ACCOUNT = 'edb167b78c9fb901ea5bca3ce58ccc4b'
STORE_ID = '8ef28060302e4311b064ba3529493e8b'  # Cloudflare Secrets Store
TOKEN = os.environ.get('CLOUDFLARE_API_TOKEN', '')
API = f'https://api.cloudflare.com/client/v4/accounts/{ACCOUNT}'
CTX = ssl._create_unverified_context()

total_tests = total_pass = total_fail = critical_failures = 0

def cf(endpoint):
    req = urllib.request.Request(f'{API}/{endpoint}')
    req.add_header('Authorization', f'Bearer {TOKEN}')
    return json.loads(urllib.request.urlopen(req, timeout=15, context=CTX).read())

def test_result(name, passed, severity='NORMAL'):
    global total_tests, total_pass, total_fail, critical_failures
    total_tests += 1
    if passed: total_pass += 1
    else: total_fail += 1; critical_failures += 1 if severity.upper() == 'CRIT' else 0
    status = 'PASS' if passed else 'FAIL'
    marker = ' [CRIT]' if severity.upper() == 'CRIT' else ''
    print(f'  [{status}]{marker} {name}')
    return passed

def run_quick():
    print('\n## SMOKE TEST')
    if not TOKEN: test_result('CLOUDFLARE_API_TOKEN set', False, 'CRIT'); return
    try:
        resp = cf(''); test_result('API token valid', True, 'CRIT')
    except: test_result('API token valid', False, 'CRIT'); return
    for name, count, endpoint in [
        ('D1', 5, 'd1/database'), ('KV', 1, 'storage/kv/namespaces'),
        ('Pages', 8, 'pages/projects'), ('Queues', 1, 'queues'),
        ('Vectorize', 0, 'vectorize/indexes')]:
        try:
            r = cf(endpoint); actual = len(r.get('result',[]))
            test_result(f'{name}: {actual} (expected {count})', actual >= count, 'NORMAL')
        except: test_result(f'{name} accessible', False, 'NORMAL')

def run_redirects():
    print('\n## HTTP REDIRECT VERIFICATION (deprecated)')
    redirects = [
        ('deep.qwav.tech', 'papers.qnfo.org', 'qwav'),
        ('archive.qnfo.org', 'papers.qnfo.org/archive', 'qnfo-archive'),
        ('adelic.qnfo.org', 'papers.qnfo.org', 'adelic-qft'),
        ('primer.qwav.tech', 'papers.qnfo.org', 'qlof-primer'),
    ]
    for host, expected, name in redirects:
        try:
            conn = hc.HTTPSConnection(host, context=CTX, timeout=15)
            conn.request('GET', '/', headers={'User-Agent': 'QNFO-TestSuite/1.1'})
            resp = conn.getresponse()
            is_redirect = resp.status in (301,302,307,308)
            loc = resp.getheader('Location', 'NONE')
            status_icon = 'PASS' if is_redirect else 'INFO'
            print(f'  [{status_icon}] {name}: {resp.status} -> {loc[:80]}' if is_redirect else f'  [{status_icon}] {name}: HTTP {resp.status} (no redirect — deprecated)')
            test_result(f'{name} redirect', is_redirect and expected in str(loc), 'NORMAL')
        except Exception as e:
            print(f'  [INFO] {name}: {str(e)[:80]}'); test_result(f'{name} redirect', False, 'NORMAL')

def main():
    p = argparse.ArgumentParser(description='QNFO Test Suite v1.1')
    p.add_argument('--quick', action='store_true'); p.add_argument('--redirects', action='store_true')
    p.add_argument('--all', action='store_true')
    args = p.parse_args()
    run_q = args.quick or args.all; run_r = args.redirects or args.all
    if not (run_q or run_r): p.print_help(); return 0
    print('=' * 60); print(f'QNFO TEST SUITE v1.1 — {datetime.now(timezone.utc).isoformat()}')
    print('(redirects deprecated 2026-06-29)'); print('=' * 60)
    if run_q: run_quick()
    if run_r: run_redirects()
    print('\n' + '=' * 60)
    print(f'RESULTS: {total_pass}/{total_tests} passed, {total_fail} failed')
    if critical_failures: print(f'CRITICAL FAILURES: {critical_failures}')
    print('=' * 60)
    if critical_failures > 0: print('\n[BLOCKED]'); return 1
    elif total_fail > 0: print('\n[WARN]'); return 0
    else: print('\n[ALL TESTS PASSED]'); return 0

if __name__ == '__main__': sys.exit(main())

```

**Execution:** `python _test_suite.py` → verify → `Remove-Item _test_suite.py`
 --file=_test_suite.py

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
| `living-paper` D1 | **CANONICAL QNFO PUBLICATIONS DATABASE** — papers table, 119 papers |
| `qnfo-cms` D1 | Page content (34 entries — hub text, legal, navigation) — NOT a CMS |
| `cms-api` Worker | **DELETED 2026-07-01** — was returning 404, non-functional |
| `living-paper-api` Worker | Legacy publications API (may duplicate ask-qwav) |
| `living-papers-api` Worker | Legacy publications API (note plural — different from above) |
| `living-paper-ai` Worker | AI-enhanced paper queries |
| `living-paper-proxy` Worker | Proxy for paper access |
| `archive.qnfo.org` | Archive page — title changed from "QNFO Living Papers" to "QNFO Research Archive" (2026-07-01) |

## Skills Backup & Recovery (v1.3)

All 28 QNFO DeepChat skills are redundantly backed up. This skill itself is recoverable from:

| Source | Location | Recovery Command |
|:-------|:---------|:-----------------|
| **GitHub** | `rwnq8/qnfo-skills` | `git clone https://github.com/rwnq8/qnfo-skills.git %USERPROFILE%\.deepchat\skills` |
| **R2** | `qnfo/prompts/skills/cloudflare-deployer/SKILL.md` | `python bootstrap_skills.py --source r2` |
| **Discovery Index** | `qnfo/discovery/index.json` (skills_backup) | JSON lookup |

**Bootstrap tools on R2:**
- `qnfo/tools/bootstrap_skills.py` — One-command restore from GitHub or R2
- `qnfo/tools/skills-recovery-guide.md` — Full recovery documentation

**Keep synced after any skill change:**
```bash
python "%USERPROFILE%\.deepchat\skills\bootstrap_skills.py" --sync
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

## Auto-Sync Architecture: R2 → Queue → Knowledge Graph (v2.2)

> **The #2 infrastructure failure mode: papers are on R2 and D1 but invisible to the Knowledge Graph.** The following architecture ensures this CANNOT happen by providing both synchronous (agent) and asynchronous (event-driven) paths to KG seeding.

### Primitives

| Primitive | Role | Status |
|:----------|:-----|:-------|
| `qnfo-lifecycle-queue` | Decouple R2 events from KG consumers | ✅ Deployed (2 producers, 1 consumer) |
| `graph-api` (`/sync`) | Bulk upsert Paper nodes + edges | ✅ Deployed (graph-api.q08.workers.dev) |
| `qnfo-agent-session` (DO+SQLite) | `/kg-mutex/acquire|release` — distributed lock for concurrent KG writes | ✅ Deployed v2.0 (qnfo-agent-session.q08.workers.dev) |
| `cron-graph-re-seed` | Periodic reconciliation: scan R2 for unsynced papers | ✅ Deployed 2026-06-02 |
| R2 Event Notifications | Trigger on `qnfo/releases/*/paper.md` create/update | Config in wrangler.toml (`r2_buckets[].event_notification`) |

### Synchronous Path (Publication-Publisher Stage 6.5)

Every paper published through the `publication-publisher` skill gets a KG node immediately after R2 upload. The agent calls `graph-api /sync` to seed a `Paper` node with `BELONGS_TO` edges to the `domain-qwav-physics` concept node. See `publication-publisher` skill v2.5+, Stage 6.5.

### Asynchronous Path (Event-Driven Reconciliation)

```
R2 object create/update (qnfo/releases/*/paper.md)
  → Event Notification (suffix filter: paper.md)
  → qnfo-lifecycle-queue
  → cron-graph-re-seed Worker (periodic, every 15 min)
    → REST API: List R2 objects (prefix: qnfo/releases/)
    → DIFF against graph-api nodes (by DOI or slug)
    → For each missing:
        → POST qnfo-agent-session /kg-mutex/acquire
        → Parse paper.md YAML frontmatter
        → POST graph-api /sync (Paper node + BELONGS_TO edges)
        → UPSERT D1 living-paper.papers table
        → POST qnfo-agent-session /kg-mutex/release
```

### Verification

```bash
# Check sync health: D1 paper count vs KG Paper node count
python -c "import urllib.request, json; kg=json.loads(urllib.request.urlopen(urllib.request.Request('https://graph-api.q08.workers.dev/stats',headers={'User-Agent':'Mozilla/5.0'}),timeout=10).read()); print(f'KG Paper nodes: {kg.get(\"labelCounts\",{}).get(\"Paper\",\"?\")}')"
```

**GATE:** D1 `living-paper.papers` count and KG `Paper` node count should differ by ≤ 5 at all times. Any larger discrepancy → run immediate reconciliation via `cron-graph-re-seed`.

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
# Pull from R2: 
### Embedded Script: generate-seo.py (self-sufficient — no R2 pull needed)

Write the following code to `_generate-seo.py`, execute, then delete:

```python
#!/usr/bin/env python3
"""
generate-seo.py — SEO file generator for QNFO/QWAV publications.
Generates sitemap.xml, robots.txt, and llms.txt for discoverability.
v1.0 — 2026-05-31

Usage:
  # SEO deployed from R2 canonical: qnfo/sites/deep.qwav.tech/
# python generate-seo.py --domain deep.qwav.tech --dir <r2-canonical> --base-url "https://deep.qwav.tech"
  # SEO deployed from R2 canonical: qnfo/projects/qlof/deploy/
# python generate-seo.py --domain laws.qnfo.org --dir <r2-canonical>
"""

import argparse
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin, quote
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom


def discover_html_files(root_dir):
    """Recursively find all .html files in a directory tree."""
    html_files = []
    root = Path(root_dir)
    for f in root.rglob('*.html'):
        # Skip node_modules, .git, _site, etc.
        if any(part.startswith('.') or part.startswith('_') or part == 'node_modules'
               for part in f.parts):
            continue
        html_files.append(f)
    return sorted(html_files)


def get_lastmod(filepath):
    """Get ISO 8601 last-modified date for a file."""
    mtime = os.path.getmtime(filepath)
    dt = datetime.fromtimestamp(mtime, tz=timezone.utc)
    return dt.strftime('%Y-%m-%d')


def url_from_path(filepath, root_dir, base_url):
    """Convert filesystem path to URL path."""
    rel_path = Path(filepath).relative_to(root_dir)
    # index.html -> directory URL
    if rel_path.name == 'index.html':
        url_path = str(rel_path.parent).replace('\\', '/')
        if url_path == '.':
            url_path = ''
    else:
        url_path = str(rel_path).replace('\\', '/')
    return urljoin(base_url.rstrip('/') + '/', url_path)


def generate_sitemap(html_files, root_dir, base_url):
    """Generate sitemap.xml."""
    urlset = Element('urlset', {
        'xmlns': 'http://www.sitemaps.org/schemas/sitemap/0.9',
        'xmlns:xhtml': 'http://www.w3.org/1999/xhtml',
    })
    
    for filepath in html_files:
        url_elem = SubElement(urlset, 'url')
        
        loc = SubElement(url_elem, 'loc')
        loc.text = url_from_path(filepath, root_dir, base_url)
        
        lastmod = SubElement(url_elem, 'lastmod')
        lastmod.text = get_lastmod(filepath)
        
        # Priority: root > section > leaf
        rel = Path(filepath).relative_to(root_dir)
        depth = len(rel.parts)
        if depth <= 1:
            priority = '1.0'
        elif depth <= 2:
            priority = '0.8'
        else:
            priority = '0.5'
        prio = SubElement(url_elem, 'priority')
        prio.text = priority
    
    xml_str = minidom.parseString(tostring(urlset, 'utf-8')).toprettyxml(indent='  ')
    return '<?xml version="1.0" encoding="UTF-8"?>\n' + xml_str.split('\n', 1)[1]


def generate_robots_txt(base_url, sitemap_exists=True):
    """Generate robots.txt allowing all crawlers."""
    lines = [
        '# robots.txt — QNFO Research Infrastructure',
        '# Generated by generate-seo.py',
        '',
        'User-agent: *',
        'Allow: /',
        '',
    ]
    if sitemap_exists:
        lines.append(f'Sitemap: {base_url.rstrip("/")}/sitemap.xml')
    
    return '\n'.join(lines) + '\n'


def generate_llms_txt(html_files, root_dir, base_url, domain):
    """Generate llms.txt — AI-readable site index (llmstxt.org spec)."""
    lines = [
        f'# {domain}',
    ]
    
    # Try to find a description from the root index.html
    root_index = Path(root_dir) / 'index.html'
    description = ''
    if root_index.exists():
        import re
        text = root_index.read_text(encoding='utf-8', errors='replace')
        # Try meta description
        m = re.search(r'<meta\s+name="description"\s+content="([^"]+)"', text, re.IGNORECASE)
        if m:
            description = m.group(1)
        else:
            # Try first substantial paragraph
            m = re.search(r'<p[^>]*>(.{50,200})</p>', text)
            if m:
                import html
                description = html.unescape(re.sub(r'<[^>]+>', '', m.group(1))).strip()
    
    if description:
        lines.append(f'> {description}')
    lines.append('')
    
    for filepath in html_files:
        url = url_from_path(filepath, root_dir, base_url)
        rel = Path(filepath).relative_to(root_dir)
        
        # Extract title from HTML
        title = rel.stem.replace('-', ' ').title()
        try:
            text = filepath.read_text(encoding='utf-8', errors='replace')
            import re as re_mod
            m = re_mod.search(r'<title[^>]*>(.+?)</title>', text, re_mod.IGNORECASE)
            if m:
                import html
                title = html.unescape(m.group(1)).strip()
        except Exception:
            pass
        
        # Get a snippet
        snippet = ''
        try:
            text = filepath.read_text(encoding='utf-8', errors='replace')
            m = re.search(r'<p[^>]*>(.{40,150})</p>', text)
            if m:
                import html
                snippet = ' — ' + html.unescape(re.sub(r'<[^>]+>', '', m.group(1))).strip()
        except Exception:
            pass
        
        # Indent based on depth
        depth = max(0, len(rel.parts) - 1)
        indent = '  ' * depth
        
        is_index = rel.name == 'index.html'
        prefix = '- ' if not is_index else ''
        lines.append(f'{indent}{prefix}[{title}]({url}){snippet}')
    
    return '\n'.join(lines) + '\n'


def main():
    parser = argparse.ArgumentParser(description="Generate SEO files for QNFO publications")
    parser.add_argument('--domain', required=True, help='Site domain (e.g., deep.qwav.tech)')
    parser.add_argument('--dir', required=True, help='Root directory containing HTML files')
    parser.add_argument('--base-url', help='Base URL (defaults to https://domain)')
    parser.add_argument('--no-sitemap', action='store_true', help='Skip sitemap.xml generation')
    parser.add_argument('--no-llms', action='store_true', help='Skip llms.txt generation')
    parser.add_argument('--dry-run', action='store_true', help='Print files that would be generated')
    args = parser.parse_args()
    
    root_dir = Path(args.dir)
    if not root_dir.exists():
        print(f"[ERROR] Directory not found: {args.dir}")
        sys.exit(1)
    
    base_url = args.base_url or f'https://{args.domain}'
    
    # Discover HTML files
    html_files = discover_html_files(root_dir)
    if not html_files:
        print(f"[WARN] No HTML files found in {args.dir}")
        return
    
    print(f"[OK] Found {len(html_files)} HTML files")
    
    output_files = {}
    
    # Generate sitemap.xml
    if not args.no_sitemap:
        sitemap_content = generate_sitemap(html_files, root_dir, base_url)
        output_files['sitemap.xml'] = sitemap_content
    
    # Generate robots.txt
    robots_content = generate_robots_txt(base_url, sitemap_exists=(not args.no_sitemap))
    output_files['robots.txt'] = robots_content
    
    # Generate llms.txt
    if not args.no_llms:
        llms_content = generate_llms_txt(html_files, root_dir, base_url, args.domain)
        output_files['llms.txt'] = llms_content
    
    if args.dry_run:
        print("\n[DRY RUN] Would generate:")
        for filename, content in output_files.items():
            output_path = root_dir / filename
            print(f"  {output_path} ({len(content)} bytes)")
    else:
        for filename, content in output_files.items():
            output_path = root_dir / filename
            output_path.write_text(content, encoding='utf-8')
            print(f"[OK] Generated: {output_path} ({len(content)} bytes)")


if __name__ == '__main__':
    main()

```

**Execution:** `python _generate-seo.py` → verify → `Remove-Item _generate-seo.py`
 --file=_generate-seo.py
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


---

## QNFO Design System Compliance (v3.0 — LOCKED 2026-07-01)

> **The papers.qnfo.org design is LOCKED as THE canonical QNFO look and feel. Do not change.**

### Design Tokens (ABSOLUTE)

```css
--blue: #1a56db; --blue-dark: #1040a8; --blue-light: #dbeafe;
--blue-subtle: #eff6ff; --blue-mid: #6094e8;
--text: #1a1a2e; --text-muted: #6b7280; --bg: #ffffff;
--border: #e5e7eb; --card-bg: #f9fafb; --max-w: 960px; --radius: 8px;
```

### Locked Fonts
| Role | Font |
|:-----|:-----|
| Headings, nav, meta | **Inter** |
| Body text | **Source Serif 4** |

### Locked Components (MANDATORY)
1. Sticky topbar with backdrop-blur
2. AI Query box on all paper pages
3. Related Papers section on all paper pages
4. Paper cards with hover shadow
5. Badges (DOI blue, Type purple, Category green, Tag gray, License orange)

### Hard Rules
🚫 **DARK THEMES FORBIDDEN.** Light theme only.
🚫 **DO NOT change fonts, colors, or max-width.** Locked.
🚫 **DO NOT remove components.** AI Query + Related Papers mandatory.

### Design Doc
Full spec: `qnfo/design-system/QNFO-DESIGN-SYSTEM.md` (R2)

### Design Compliance Matrix (2026-07-01 Audit)

| Site | HTTP | Design v3.0 | AI Query | Related | SEO | Notes |
|:-----|:-----|:------------|:---------|:--------|:----|:------|
| papers.qnfo.org | ✅ 200 | ✅ FULL | ✅ | ✅ | ❌ | **CANONICAL** - missing robots/sitemap/llms |
| legal.qnfo.org | ✅ 200 | ✅ FULL | ❌ | ✅ | — | License page |
| deep.qwav.tech | ✅ 200 | ✅ FULL | ✅ | ❌ | ⚠ PARTIAL | Missing sitemap.xml, llms.txt, ai.txt |
| primer.qwav.tech | ✅ 200 | ✅ FULL | ✅ | ❌ | — | Mirrors deep.qwav.tech |
| qnfo.org | ✅ 200 | ⚠ PARTIAL | ❌ | ❌ | ✅ | Missing Serif, #1a56db, max-w=1100px |
| design.qnfo.org | ✅ 200 | ⚠ PARTIAL | ❌ | ❌ | — | Serves same as qnfo.org |
| ask.qwav.tech | ✅ 200 | ⚠ PARTIAL | ❌ | ❌ | — | Missing Serif, #1a56db |
| hensel.qnfo.org | ✅ 200 | ⚠ PARTIAL | ❌ | ❌ | — | **Redirects to qnfo.org** |
| momentum.qnfo.org | ✅ 200 | ⚠ PARTIAL | ❌ | ❌ | — | **Redirects to qnfo.org** |

**12 DEAD DOMAINS (54% failure rate):** archive.qnfo.org (404), solo.qnfo.org, paradigm.qnfo.org, quantum.qnfo.org, unity.qnfo.org, different.qnfo.org, measure.qnfo.org, cocyle.qnfo.org, lexicon.qnfo.org, ai-poc.qnfo.org, adelic.qnfo.org, knowing.qnfo.org — all DNS records exist but do not resolve. Per DNS Hygiene Rules: **delete immediately.**

**Highest-Priority Fix:** papers.qnfo.org missing all SEO artifacts (robots.txt, sitemap.xml, llms.txt, llms-full.txt, ai.txt). The canonical publications site is invisible to search engines and AI crawlers.

**Reference:** Full audit in `qnfo/MASTER-PLAN.md` (R2).

## Failure Handling

| Scenario | Response |
|:---------|:---------|
| `wrangler whoami` fails or shows wrong account | Token expired or wrong — run `npx wrangler login` or verify `$env:CLOUDFLARE_API_TOKEN` |
| R2 upload returns HTTP 401 | Token has insufficient permissions — token must have R2 read+write+delete |
| Pages deploy returns build error | Check build output directory exists and contains `index.html` |
| Worker deploy returns "duplicate script" | Use `--force` flag or delete old version first |
| `r2 object list` returns "command not found" | Feature removed in v4.95+ — use per-object `get` operations or REST API `_r2_list.py` |
| DNS/redirect changes not propagating | Cloudflare DNS TTL is 300s minimum — wait and retry |
| `skill_view('cloudflare-deployer')` returns error | Skill not indexed — run `bootstrap_skills.py --sync` and restart DeepChat |
| MathJax not rendering after deploy | Config is AFTER script tag — fix ordering before redeploying |
| Token not found in environment | Persist token via env var (User-level) AND store canonically in Secrets Store: `PUT /accounts/{ACCOUNT}/secrets_store/stores/8ef28060302e4311b064ba3529493e8b/secrets/CLOUDFLARE_API_TOKEN` |
| **522 Connection timed out after DNS/CNAME change** | **ROOT CAUSE: CNAME→`.pages.dev` exists but domain NOT registered on Pages project.** Fix: Register domain on target Pages project (`POST /accounts/:id/pages/projects/:name/domains`). Then verify HTTP 200. See infrastructure-audit §0.8 for automated detection & fix. |

**Recovery tools on R2:**
- `qnfo/tools/fast_r2_upload.py` — batch R2 upload (250x faster than wrangler)
- `qnfo/tools/r2_list.py` — R2 object listing
- `qnfo/tools/ps_run.py` — Safe Python execution bridge
- `qnfo/design-system/build_pdf.py` — Markdown to PDF
- `qnfo/tools/generate-seo.py` — SEO metadata generation
- `qnfo/tools/bootstrap_skills.py` — Skill sync and recovery



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
- `vectorize-papers.py`: requires Cloudflare API token (auto-available via `$env:CLOUDFLARE_API_TOKEN`; canonical: Secrets Store) and Workers AI access
- `build_pdf.py`: requires `reportlab` and optionally `markdown` packages


*cloudflare-deployer skill v2.2 — +Secrets Store +DO+SQLite +Workers AI +R2 Events +Flagship +Versions. All 28 wrangler commands documented for wrangler v4.107.0. 30 Workers deployed.*

---

*v2.0 and earlier deprecated 2026-07-01. Replaced by v2.1 with 522 root cause pattern, CNAME chain rule, and automated cross-reference verification.*



---

## Secrets Store Integration (v2.3 --- 2026-07-05)

> **READ/WRITE:** Cloudflare Secrets Store (canonical: `default_secrets_store`, id=8ef28060302e4311b064ba3529493e8b). Secret VALUES are NOT readable via REST API --- Python scripts use env vars; Workers use `env.SECRET_NAME` bindings. See `infrastructure-audit` skill for full read/write patterns.

### Current Secrets (20)

| Name | Purpose | Workers Binding |
|:-----|:--------|:----------------|
| `CLOUDFLARE_API_TOKEN` | Full Cloudflare API access | `env.SECRETS.CLOUDFLARE_API_TOKEN` |
| `R2_ACCESS_KEY_ID` | R2 S3 access key | `env.SECRETS.R2_ACCESS_KEY_ID` |
| `R2_SECRET_ACCESS_KEY` | R2 S3 secret key | `env.SECRETS.R2_SECRET_ACCESS_KEY` |
| `ZENODO_API_TOKEN` | Zenodo API | `env.SECRETS.ZENODO_API_TOKEN` |
| `BUFFER_ACCESS_TOKEN` | Buffer social media | `env.SECRETS.BUFFER_ACCESS_TOKEN` |
| `GITHUB_TOKEN` | GitHub PAT | `env.SECRETS.GITHUB_TOKEN` |
| `PINATA_API_KEY` | IPFS Pinata key | `env.SECRETS.PINATA_API_KEY` |
| `PINATA_API_SECRET` | IPFS Pinata secret | `env.SECRETS.PINATA_API_SECRET` |
| `PINATA_JWT` | IPFS Pinata JWT | `env.SECRETS.PINATA_JWT` |
| *+11 more* | FILEBASE_*, GOOGLE_OAUTH_*, BUFFER_CLIENT_*, etc. | Various |

### Store a New Secret

```bash
# Via REST API:
curl -X PUT "https://api.cloudflare.com/client/v4/accounts/{ACCOUNT}/secrets_store/stores/8ef28060302e4311b064ba3529493e8b/secrets/<NAME>" \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"value":"<secret>","comment":"Description","scopes":["workers"]}'
```

### Worker-Side: Bind Secrets Store

In `wrangler.toml`:
```toml
[[secrets_store]]
binding = "SECRETS"
store_id = "8ef28060302e4311b064ba3529493e8b"
```

In Worker code:
```javascript
const token = env.SECRETS.CLOUDFLARE_API_TOKEN;
const zenodoToken = env.SECRETS.ZENODO_API_TOKEN;
```

---

## RT: RED-TEAM SELF-AUDIT

Before claiming this skill complete, autonomously run:

1. Output Verification (negative verification)
2. Assumption Challenge (state and test every assumption)
3. Edge Case Check (empty/null/max/boundary/desync)
4. DoD Integration (run _dod_enforce.py if exists)
5. Iteration (retry on failure, max 3)

ANTI-PATTERN: User should NEVER ask about quality.\n**Skill-Specific Checks:**\n6. Pages Preview URL: Verify deploy accessible at *.pages.dev before custom domain\n7. R2 Sync: Verify qnfo-cms-client.js exists on R2 with correct version\n8. CDN Purge: Verify custom domain serves latest deploy after CDN propagation\n9. MathJax Config: For publication pages, verify MathJax config BEFORE script tag
Refer to RED-TEAM-PROTOCOL.md for full protocol.

> **Version:** (Kaizen-audited 2026-07-08)
