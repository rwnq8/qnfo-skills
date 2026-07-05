---
name: infrastructure-audit
description: Audit all Cloudflare infrastructure resources (D1, R2, Workers, Pages, Vectorize, Queues) including lifecycle pipeline. Reports orphaned/duplicate resources, state mismatches, lifecycle health, and archival integrity.
version: "2.0"
---
> **INCLUDES AUTONOMOUS RED-TEAM SELF-AUDIT.** See RED-TEAM-PROTOCOL.md.



### Programmatic Loading & Execution
This skill is loaded and executed **programmatically by the LLM system** 
during response generation. Loading is triggered automatically via 
`skill_view('infrastructure-audit')` or `read()` with filesystem path.
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

# INFRASTRUCTURE AUDIT SKILL — v1.0 -- v2.0

> **LIFECYCLE-AWARE. GAP-AUDIT INTEGRATION. RED-TEAM-DOD INTEGRATION. RESOURCE GOVERNANCE. 522-PREVENTION. UPDATED 2026-07-01.** v1.9 adds §0.8 522 Root Cause Detection (CNAME × Pages cross-reference), §0.9 CNAME Chain Detection, §0.10 Dead Worker CNAME Detection, and §0.11 Empty Zone Detection — all learned from the 2026-07-01 qwav.tech 522 outage. Prevents the #1 failure mode: CNAME to `.pages.dev` without domain registration.

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
  {"step": "Query D1 databases via API Worker", "status": "pending"},
  {"step": "Query KV namespaces", "status": "pending"},
  {"step": "Query Vectorize indexes", "status": "pending"},
  {"step": "Query Pages projects", "status": "pending"},
  {"step": "Query Workers deployments", "status": "pending"},
  {"step": "Query Queues", "status": "pending"},
  {"step": "Check Lifecycle Worker health", "status": "pending"},
  {"step": "Check Archive Worker health", "status": "pending"},
  {"step": "Run archival integrity checks", "status": "pending"},
  {"step": "Generate health recommendations report", "status": "pending"},
])

---

## Purpose

The #1 cause of duplicate work in QNFO is agents executing tasks without checking live infrastructure state. This skill automates the Infrastructure State Verification Gate (qnfo-agent §3.2 step 1.6) by querying all Cloudflare resources including the automated lifecycle pipeline and comparing against handoff/Discovery Index claims.

## When to Use

| Trigger | Action |
|:--------|:-------|
| Session startup | Full audit + health report |
| "Check infrastructure" | Run all checks |
| "Audit Cloudflare resources" | Full audit with recommendations |
| Before any upload/deploy/data task | Quick pre-execution check |
| "What's orphaned/duplicate?" | Orphan detection only |
| "Check lifecycle pipeline" | Worker + queue health verification |

## Workflow

### Phase 1: Full Infrastructure Audit

```python
import urllib.request, json, os

TOKEN = os.environ.get('CLOUDFLARE_API_TOKEN', '')
ACCOUNT = 'edb167b78c9fb901ea5bca3ce58ccc4b'

def cf(endpoint):
    url = f'https://api.cloudflare.com/client/v4/accounts/{ACCOUNT}/{endpoint}'
    req = urllib.request.Request(url)
    req.add_header('Authorization', f'Bearer {TOKEN}')
    return json.loads(urllib.request.urlopen(req, timeout=15).read())

# Query all services
d1 = cf('d1/database')
kv = cf('storage/kv/namespaces')
vec = cf('vectorize/v2/indexes')
pages = cf('pages/projects')
workers = cf('workers/scripts')
queues = cf('queues')

print(f'D1: {len(d1.get("result",[]))} | KV: {len(kv.get("result",[]))} | Vectorize: {len(vec.get("result",[]))}')
print(f'Pages: {len(pages.get("result",[]))} | Workers: {len(workers.get("result",[]))} | Queues: {len(queues.get("result",[]))}')
# Expected: D1: 5 | KV: 1 | Vectorize: 3 | Pages: 10 | Workers: 32 | Queues: 1
```

### Phase 1.5: Lifecycle Pipeline Health (NEW)

```python
# Check Lifecycle Worker
r = urllib.request.Request("https://qnfo-lifecycle.q08.workers.dev/health",
    headers={"User-Agent": "Mozilla/5.0"})
lifecycle_health = json.loads(urllib.request.urlopen(r, timeout=10).read())
print(f"Lifecycle Worker: {lifecycle_health.get('status','?')}")

# Check Archive Worker
r2 = urllib.request.Request("https://qnfo-archive-worker.q08.workers.dev/health",
    headers={"User-Agent": "Mozilla/5.0"})
archive_health = json.loads(urllib.request.urlopen(r2, timeout=10).read())
print(f"Archive Worker: {archive_health.get('status','?')}")

# Check lifecycle status
r3 = urllib.request.Request("https://qnfo-lifecycle.q08.workers.dev/status",
    headers={"User-Agent": "Mozilla/5.0"})
status = json.loads(urllib.request.urlopen(r3, timeout=15).read())
print(f"Lifecycle Scan: {status.get('totalProjects', 0)} projects, distribution: {status.get('statusDistribution', {})}")

# Check Knowledge Graph
r4 = urllib.request.Request("https://graph-api.q08.workers.dev/stats",
    headers={"User-Agent": "Mozilla/5.0"})
kg = json.loads(urllib.request.urlopen(r4, timeout=10).read())
print(f"Knowledge Graph: {kg.get('totalNodes',0)} nodes, {kg.get('totalEdges',0)} edges")
# Expected: 261 nodes, 401 edges
```

### Phase 1.7: DNS Resolution & Domain Classification Audit (v1.7 — 2026-07-01)

> **CRITICAL:** The 2026-07-01 front-end audit found 28 dead DNS records. Every infrastructure audit must now verify DNS resolution and classify all domains.

```python
# Audit: every domain must resolve to HTTP 200 and be classified
import urllib.request, ssl, json

ctx = ssl.create_default_context()
H = {'User-Agent': 'Mozilla/5.0'}

# Pull ALL DNS records across zones
zones = ['84e9dc1d7fb72629ccdbe3174ed24420',  # qnfo.org
         'dd6908d3cc04acb2efee47382fb94e8e',  # q-wave.tech
         '26699a3b10699f257eabc34a0faee56d',  # qnfo.uk
         'd4e7855f3ed5f0a93204b7bd34e286ab',  # qnfo.net
         'fa732a265dd53230b9777908734a74d5']  # q08.org

for zone_id in zones:
    url = f'https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records?per_page=100'
    req = urllib.request.Request(url, headers={'Authorization': f'Bearer {TOKEN}'})
    records = json.loads(urllib.request.urlopen(req, timeout=10, context=ctx).read())

    for r in records.get('result', []):
        name = r.get('name', '')
        rtype = r.get('type', '')
        if rtype in ('A', 'CNAME', 'AAAA'):
            # Test resolution
            try:
                resp = urllib.request.urlopen(urllib.request.Request(f'https://{name}', headers=H), timeout=10, context=ctx)
                body = resp.read().decode('utf-8', errors='replace')[:500]
                # Classify: LANDING or CONTENT?
                is_index = 'index' in body.lower() or 'catalog' in body.lower() or 'hub' in body.lower()
                is_content = 'paper' in body.lower() or 'abstract' in body.lower()
                klass = 'LANDING' if is_index else ('CONTENT' if is_content else 'UNKNOWN')
                print(f'  [{klass}] {name}: HTTP {resp.status}')
            except Exception as e:
                print(f'  [DEAD] {name}: {e} — DELETE DNS RECORD')
```

**GATE (UPDATED v1.9):** Every DNS record must resolve to HTTP 200 within 10 seconds. Any [DEAD] domain → DELETE the DNS record. Any [UNKNOWN] classification → manually classify as LANDING or CONTENT. **Additionally, run the §0.8 cross-reference check** — every CNAME to `.pages.dev` MUST have a matching domain registration on the target Pages project.

### Phase 1.6: HTTP Behavior Verification (DEPRECATED — redirects deprecated per 2026-07-01)

> **2026-07-01:** Redirect verification is now REPLACED by Phase 1.7 (DNS Resolution & Domain Classification). All former redirect domains (deep.qwav.tech, archive.qnfo.org, adelic.qnfo.org, primer.qwav.tech) now serve content directly. No redirects remain in the QNFO ecosystem.

```python
# Verify claimed HTTP redirects
redirects = [
    ('https://deep.qwav.tech', 'https://papers.qnfo.org', 'qwav'),
    ('https://archive.qnfo.org', 'https://papers.qnfo.org/archive', 'qnfo-archive'),
    ('https://adelic.qnfo.org', 'https://papers.qnfo.org', 'adelic-qft'),
    ('https://primer.qwav.tech', 'https://papers.qnfo.org', 'qlof-primer'),
]
for url, expected, name in redirects:
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        resp = urllib.request.urlopen(req, timeout=10, context=ctx)
        if resp.status in (301, 302, 307, 308):
            loc = resp.headers.get('Location', '')
            print(f'  {name}: {resp.status} -> {loc[:60]}')
        else:
            print(f'  [FAIL] {name}: returns {resp.status}, not redirecting')
    except Exception as e:
        print(f'  [FAIL] {name}: {e}')
```

### Phase 2: Orphan Detection

Compare live resources against Discovery Index to find unregistered or stale entries.

```python
# Check for projects in DI with no R2 path
# Check for workers/queues not in DI
# Check for R2 paths that no longer have backing data
```

### Phase 3: Archival Integrity (NEW)

```python
import json, urllib.request

# Pull Discovery Index
# D1-FIRST: Query D1 instead of R2 discovery index
# Projects: npx wrangler d1 execute qnfo-audit --remote --command 'SELECT * FROM discovery_projects' -y
# Resources: npx wrangler d1 execute portfolio-state --remote --command 'SELECT * FROM resources' -y
    headers={"Authorization": f"Bearer {TOKEN}", "User-Agent": "Mozilla/5.0"})
di = json.loads(urllib.request.urlopen(r, timeout=15).read())
projects = di.get("projects", {})

# Check archived projects have archive paths
archived = [(n, p.get("r2_path","")) for n, p in projects.items() if "ARCHIVED" in (p.get("status","")).upper()]
for name, path in archived:
    has_archive = "/archive/" in path
    print(f"  {name}: {'CORRECT' if has_archive else 'MISMATCH — still at projects/'} - {path}")

# Check project paths exist on R2
no_path = [n for n, p in projects.items() if not p.get("r2_path")]
if no_path:
    print(f"  [WARN] No R2 path: {no_path}")

# Verify ultrametric taxonomy
r = urllib.request.Request("https://graph-api.q08.workers.dev/nodes?label=Concept",
    headers={"User-Agent": "Mozilla/5.0"})
concepts = json.loads(urllib.request.urlopen(r, timeout=10).read())
domain_nodes = [c for c in concepts.get("nodes", []) if c.get("properties", {}).get("level") == 1]
program_nodes = [c for c in concepts.get("nodes", []) if c.get("properties", {}).get("level") == 2]
print(f"Ultrametric Taxonomy: {len(domain_nodes)} domains, {len(program_nodes)} programs")
```

### Phase 4: Health Recommendations

Based on audit findings, report orphaned resources, stale entries, archival mismatches, and cleanup recommendations.

#### 4.1 Paper → Knowledge Graph Sync Health (NEW — v2.0)

> **The #2 undetected failure mode: D1 living-paper has N papers but KG has < N Paper nodes.** This check prevents the systemic desync where publications exist in the database but are invisible to Knowledge Graph queries, impact analysis, and ultrametric ball queries.

```python
import urllib.request, json

# Get KG Paper node count
r = urllib.request.Request("https://graph-api.q08.workers.dev/stats",
    headers={"User-Agent": "Mozilla/5.0"})
kg = json.loads(urllib.request.urlopen(r, timeout=10).read())
kg_papers = kg.get("labelCounts", {}).get("Paper", 0)
print(f"  KG Paper nodes: {kg_papers}")

# Get D1 living-paper count
r2 = urllib.request.Request("https://qnfo-data-api.q08.workers.dev/v2/stats",
    headers={"User-Agent": "Mozilla/5.0"})
try:
    d1 = json.loads(urllib.request.urlopen(r2, timeout=10).read())
    d1_papers = d1.get("living_paper", {}).get("papers", 0) if isinstance(d1.get("living_paper", {}), dict) else 0
    print(f"  D1 living-paper: {d1_papers}")
    
    diff = abs(d1_papers - kg_papers)
    if diff <= 5:
        print(f"  [OK] Paper-KG sync: {d1_papers}/{kg_papers} (diff={diff} ≤ 5)")
    elif diff <= 20:
        print(f"  [WARN] Paper-KG DESYNC: {d1_papers}/{kg_papers} (diff={diff}) — run cron-graph-re-seed")
    else:
        print(f"  [BLOCKING] Paper-KG SEVERE DESYNC: {d1_papers}/{kg_papers} (diff={diff} > 20) — IMMEDIATE reconciliation required")
except Exception as e:
    print(f"  [WARN] D1 query failed: {e} — cannot verify KG sync")
```

**GATE:** If diff > 20 → BLOCKING. Run immediate reconciliation via `cron-graph-re-seed` or manual `graph-api /sync`. If diff 5-20 → HIGH severity warning; flag in audit report for next maintenance window.

## Infrastructure Resource Inventory

| Resource | Expected Count | Current (2026-07-01) |
|:---------|:-----:|:------|
| D1 Databases | 5 | qnfo-cms (page content), **living-paper (CANONICAL PUBLICATIONS DATABASE — 170 papers)**, qnfo-audit, qnfo-graph, portfolio-state |
| KV Namespaces | 1 | equation-cache |
| Vectorize Indexes | 3 | qwav-research-v2 (1024-dim, active), qnfo-handoffs, qnfo-tasks |
| Pages Projects | 10 (5 active, 5 dormant) | qnfo-hub, qnfo-publications, qnfo-legal, qwav, qnfo-design-system + 5 dormant |
| Workers | 30 | papers-server, ask-qwav, graph-api, qnfo-agent-session (DO+SQLite), qnfo-ai-worker (Workers AI), +25 more |
| **Durable Objects** | 2 namespaces, 3 classes | `portfolio-api_StateRegistry` (StateRegistry), `qnfo-agent-session` (AgentSession + QnfoAgentSession w/ **SQLite ON**) — Fully persistent agent state, KG mutex, lifecycle state machine |
| Queues | 1 | qnfo-lifecycle-queue (essential) |
| **R2 Event Rules** | 2 | releases/*.md + discovery/*.json → qnfo-lifecycle-queue (created 2026-07-04) |
| **Secrets Store** | 1 store, 10 secrets | `default_secrets_store` — CLOUDFLARE_API_TOKEN, R2_ACCESS_KEY_ID, ZENODO_API_TOKEN, BUFFER_ACCESS_TOKEN, GITHUB_TOKEN, S3_ENDPOINT, ADMIN_API_TOKEN, ADMIN_TOKEN, CF_API_TOKEN |
| **Workers AI** | 60 models, 10 task types | Text Gen, Embeddings (1024-dim), Translation, TTS, Image Gen confirmed |
| Knowledge Graph | 882 nodes, 1854 edges | ACTIVE — graph-api Worker, D1 qnfo-graph |
| R2 Bucket | 1 (qnfo) | papers, publications, discovery, archive, projects, releases, tools |
| Live Domains | 30 (verified 2026-07-04) | 10 zones, all resolving HTTP 200 |

## Lifecycle Pipeline Health Checks

| Component | Check | Endpoint |
|-----------|-------|----------|
| Lifecycle Worker | HTTP 200, status=ok | `GET /health` on `qnfo-lifecycle.q08.workers.dev` |
| Lifecycle Scan | Projects scanned, transitions | `GET /status` |
| Archive Worker | HTTP 200, status=ok | `GET /health` on `qnfo-archive-worker.q08.workers.dev` |
| Lifecycle Queue | Exists, producers + consumers configured | `wrangler queues list` |
| Discovery Index | 38 projects, archived paths correct | D1 `portfolio-state.resources` + `qnfo-audit.discovery_projects` (R2 index DEPRECATED) |
| Knowledge Graph | Ultrametric taxonomy intact | `/nodes?label=Concept`, domain/program counts |

## Output Format

```
# INFRASTRUCTURE AUDIT REPORT
**Date:** YYYY-MM-DD | **Auditor:** QNFO Agent

## Resource Inventory
| Resource | Count | Status |
|:---------|:-----:|:------:|
| D1 Databases | 5 | OK |
| KV Namespaces | 2→1 | OK (git-on-cloudflare-routes deprecated) |
| Vectorize Indexes | 3 | OK (qwav-research-v2 active, 2 obsolete deleted) |
| Pages Projects | 10 | OK (3 essential, 4 redirecting, 3 support) |
| Workers | 27 | OK |
| Queues | 2 | OK (git-on-cloudflare-repo-maint deprecated) |
| Knowledge Graph | 261n/401e | ACTIVE (needs paper REFERENCES edges) |
| Lifecycle Worker | Running | OK |
| Archive Worker | Running | OK |

## Issues Found
**Auto-populated from gap audit (closeout-manager §2.6):**
| Gap ID | Category | Severity | Description |
|:-------|:---------|:---------|:------------|
| — | — | — | (List from gap audit output) |

## Lifecycle Pipeline
- Daily scan active (06:00 UTC)
- 0 projects currently stale
- 17 ARCHIVED with correct archive paths
- Ultrametric taxonomy: 4 domains, 12 programs

## Recommendations
No action needed.
```

### 0.5 GAP AUDIT INTEGRATION (v1.3)

### 0.7 RESOURCE GOVERNANCE — Unchecked Proliferation Prevention (v1.8)

> **CRITICAL:** The 2026-07-01 session audit found 18 worker routes, 30 Workers, 10 Pages projects, 42 DNS records, 7 zones, and 4 redirect chains — all grown unconstrained. Root cause: no cross-reference between resources, no baseline counts, no automated enforcement. The session session deleted 24 DNS records, 13 routes, 5 Workers, 5 Pages projects, and 2 redirect rulesets. **These rules prevent recurrence.**

**Resource Baselines (alert if exceeded):** Worker routes ≤ 6, Workers ≤ 32 (was 27 — baseline raised 2026-07-04 to match actual 32 deployed Workers; 2026-07-04 RED-TEAM audit verified 0 orphans), Pages ≤ 10 (was 5 — baseline lifted 2026-07-04 to match actual usage; 26 projects trimmed to 10 in 2026-07-01 cleanup), DNS ≤ 16, Zones ≤ 7 (12 total with 5 Registrar-managed unremovable zones excluded from baseline), Redirects = 0. **Cross-Reference Enforcement:** every route must target a live Worker; every DNS CNAME to `.pages.dev` must have domain registered on that Pages project; every domain must resolve to HTTP 200. **Growth Detection:** before creating any resource, count current resources; if over baseline, audit and clean up first. **Anti-Proliferation:** create DNS CNAME → add domain to Pages FIRST; create Worker route → verify Worker deployed FIRST; delete Worker → delete all routes FIRST; delete Pages → remove all domains FIRST.

**GATE:** Resource counts MUST be within baseline at session start.

When the infrastructure audit runs (session start or on-demand), it automatically:
1. Feeds findings into the POST-PHASE GAP AUDIT (closeout-manager §2.6)
2. Maps infrastructure health to gap severity: health FAIL → BLOCKING/HIGH, orphan resources → MEDIUM, warnings → LOW
3. Outputs gap-audit-compatible report format with Gap ID, Category, Severity, Description columns

### 0.8 522 ROOT CAUSE DETECTION — CNAME × Pages Cross-Reference (v1.9)

> **CRITICAL — LEARNED FROM 2026-07-01 qwav.tech 522 OUTAGE.** The qwav.tech 522 "Connection timed out" was caused by 5 CNAME records pointing to `qwav.pages.dev` but only 1 of those domains (`deep.qwav.tech`) was registered on the `qwav` Cloudflare Pages project. The other 4 domains received 522 because Pages rejected traffic for unrecognized domains. **This is the #1 infrastructure failure mode.**

**The 522 Pattern:**
```
DNS: qwav.tech CNAME → qwav.pages.dev    ← CNAME EXISTS
Pages: qwav project domains = [deep.qwav.tech]  ← qwav.tech NOT REGISTERED
Result: 522 Connection timed out                           ← PAGES REJECTS TRAFFIC
```

**Detection — runs during every Phase 1 audit:**

```python
import urllib.request, json, os, ssl

TOKEN = os.environ.get('CLOUDFLARE_API_TOKEN', '')
ctx = ssl.create_default_context()
ACCOUNT = 'edb167b78c9fb901ea5bca3ce58ccc4b'

def cf(endpoint, timeout=15):
    url = 'https://api.cloudflare.com/client/v4/' + endpoint
    req = urllib.request.Request(url)
    req.add_header('Authorization', 'Bearer ' + TOKEN)
    return json.loads(urllib.request.urlopen(req, timeout=timeout, context=ctx).read())

# Step 1: Build Pages → domains map
pages_domains = {}
for p in cf('accounts/' + ACCOUNT + '/pages/projects').get('result', []):
    pname = p['name']
    doms = cf('accounts/' + ACCOUNT + '/pages/projects/' + pname + '/domains').get('result', [])
    pages_domains[pname] = set(d['name'] for d in doms)

# Step 2: Build .pages.dev target → project name map
pages_targets = {}
for p in cf('accounts/' + ACCOUNT + '/pages/projects').get('result', []):
    sub = p.get('subdomain', '')
    if sub:
        pages_targets[sub] = p['name']  # sub already includes '.pages.dev' from API

# Step 3: Scan ALL DNS CNAME records for .pages.dev targets
zones = cf('zones?per_page=50').get('result', [])
violations = []
for z in zones:
    recs = cf('zones/' + z['id'] + '/dns_records?per_page=100').get('result', [])
    for r in recs:
        if r.get('type') == 'CNAME':
            target = r.get('content', '')
            if target.endswith('.pages.dev'):
                domain = r.get('name', '')
                project = pages_targets.get(target, 'UNKNOWN')
                if project != 'UNKNOWN' and domain not in pages_domains.get(project, set()):
                    violations.append({
                        'domain': domain, 'target': target,
                        'project': project, 'zone': z['name'],
                        'fix': f'Register {domain} on {project} Pages project'
                    })
                    print(f'  [522-RISK] {domain} CNAME→{target} BUT NOT REGISTERED on {project}!')

if violations:
    print(f'\n!!! {len(violations)} DOMAINS AT RISK OF 522 — FIX BEFORE DEPLOYING !!!')
    for v in violations:
        print(f'  FIX: {v["fix"]}')
```

**Automated Fix — register domain on Pages project:**

```python
def cf_post(endpoint, data, timeout=15):
    url = 'https://api.cloudflare.com/client/v4/' + endpoint
    req = urllib.request.Request(url, method='POST')
    req.add_header('Authorization', 'Bearer ' + TOKEN)
    req.add_header('Content-Type', 'application/json')
    req.data = json.dumps(data).encode('utf-8')
    return json.loads(urllib.request.urlopen(req, timeout=timeout, context=ctx).read())

for v in violations:
    r = cf_post('accounts/' + ACCOUNT + '/pages/projects/' + v['project'] + '/domains',
                {'name': v['domain']})
    print(f"  {'FIXED' if r.get('success') else 'FAILED'}: {v['domain']} → {v['project']}")
```

**GATE:** 522-RISK count MUST be 0 at session start. Any detected violations → immediate auto-fix (register domain on Pages project). If auto-fix fails → BLOCKING gap.

**Verification after fix:**
```python
import urllib.request, ssl
ctx = ssl.create_default_context()
H = {'User-Agent': 'Mozilla/5.0'}
for v in violations:
    try:
        resp = urllib.request.urlopen(urllib.request.Request('https://' + v['domain'], headers=H),
                                      timeout=10, context=ctx)
        print(f"  [VERIFIED] {v['domain']} → HTTP {resp.status}")
    except Exception as e:
        print(f"  [FAILED] {v['domain']} → {e} — DELETE DNS RECORD")
```

### 0.9 CNAME CHAIN DETECTION (v1.9)

> **CRITICAL — LEARNED FROM 2026-07-01 AUDIT.** CNAME chains (A → B → C) are fragile. Every CNAME to a `.pages.dev` target should be DIRECT, not through another domain. The `score.qwav.tech → qwav.tech → qwav.pages.dev` chain broke when `qwav.tech` was not registered. Repoint all chain CNAMEs directly to their ultimate `.pages.dev` target.

**Detection:**
```python
# Build a map of all CNAME chains
cname_map = {}
for r in all_dns_records:
    if r['type'] == 'CNAME':
        cname_map[r['name']] = r['content']

# Find chains (A→B→C where C is .pages.dev)
chains = []
for name, target in cname_map.items():
    if target in cname_map and '.pages.dev' not in target:
        ultimate = target
        visited = {name}
        hops = 1
        while ultimate in cname_map:
            next_target = cname_map[ultimate]
            if next_target == ultimate:  # self-reference guard
                break
            ultimate = next_target
            hops += 1
            if ultimate in visited:  # loop detection
                ultimate = 'LOOP:' + ultimate
                break
            visited.add(ultimate)
        if hops > 1:
            chains.append((name, target, cname_map.get(ultimate, ultimate), hops))
            print(f'  [CHAIN DETECTED] {name} → {target} → {cname_map.get(ultimate, ultimate)} ({hops} hops) — REPOINT DIRECTLY')
```

**Fix:** Repoint the chain origin CNAME directly to the ultimate `.pages.dev` target.
```python
# PUT /zones/{zone_id}/dns_records/{record_id} with content = ultimate .pages.dev target
```

**GATE:** CNAME chains to `.pages.dev` must be ≤ 1 hop. Any 2+ hop chains → repoint directly.

### 0.10 DEAD WORKER CNAME DETECTION (v1.9)

> **CRITICAL — LEARNED FROM 2026-07-01 AUDIT.** `analytics.qwav.tech` CNAME → `qnfo-kaizen-analytics.q08.workers.dev` but no such Worker was deployed. CNAME records pointing to non-existent Workers must be detected and deleted.

**Detection:**
```python
# Get all deployed Worker names
workers = cf('accounts/' + ACCOUNT + '/workers/scripts').get('result', [])
worker_names = set(w.get('id', '') for w in workers)

# Scan DNS for CNAMEs to *.workers.dev
for r in all_dns_records:
    if r['type'] == 'CNAME' and '.workers.dev' in r.get('content', ''):
        target_worker = r['content'].split('.')[0]  # Extract worker name from subdomain
        if target_worker not in worker_names:
            print(f"  [DEAD-WORKER] {r['name']} CNAME→{r['content']} — Worker '{target_worker}' NOT DEPLOYED — DELETE DNS RECORD")
```

**Fix:** DELETE the DNS record immediately. Dead worker references serve no purpose.

**GATE:** DEAD-WORKER count MUST be 0. Any detected → delete DNS record.

### 0.11 EMPTY ZONE DETECTION (v1.9)

> **CRITICAL — LEARNED FROM 2026-07-01 AUDIT.** The `q-wave.tech` zone had 0 DNS records but consumed a zone slot and appeared in audit reports. Empty zones waste resources and confuse audits.

**Detection:**
```python
for z in zones:
    recs = cf('zones/' + z['id'] + '/dns_records?per_page=100').get('result', [])
    if len(recs) == 0:
        print(f"  [EMPTY-ZONE] {z['name']} ({z['id']}) — 0 DNS records — DELETE ZONE")
```

**Fix:** DELETE the zone via API. If zone is Cloudflare Registrar-managed (error 1315), flag as `UNREMOVABLE` and exclude from baseline counts.

**GATE:** Empty zones should be deleted. If unremovable, exclude from all counts and audits.

## Integration

- Runs automatically at session start (qnfo-agent §3.2 step 1.6)
- Pre-execution gate: before any upload/deploy task
- Feeds into Discovery Index updates
- Validates lifecycle pipeline health before archival operations

---

*infrastructure-audit v1.9 — Resource Governance (§0.7) + 522 Prevention (§0.8-§0.11). Automated CNAME×Pages cross-reference, chain detection, dead worker detection, empty zone detection. 25-check audit with automated fix capability.*

*v1.8 and earlier deprecated 2026-07-01. Replaced by v1.9 with automated 522 root cause detection, CNAME chain detection, dead worker detection, and empty zone detection.*

## RT: RED-TEAM SELF-AUDIT

Before claiming this skill complete, autonomously run:

1. Output Verification (negative verification)
2. Assumption Challenge (state and test every assumption)
3. Edge Case Check (empty/null/max/boundary/desync)
4. DoD Integration (run _dod_enforce.py if exists)
5. Iteration (retry on failure, max 3)

ANTI-PATTERN: User should NEVER ask about quality.
Refer to RED-TEAM-PROTOCOL.md for full protocol.

