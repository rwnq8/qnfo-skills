---
name: infrastructure-audit
description: Audit all Cloudflare infrastructure resources (D1, R2, Workers, Pages, Vectorize, Queues) including lifecycle pipeline. Reports orphaned/duplicate resources, state mismatches, lifecycle health, and archival integrity.
version: "1.2"
---
> **INCLUDES AUTONOMOUS RED-TEAM SELF-AUDIT.** See RED-TEAM-PROTOCOL.md.


# INFRASTRUCTURE AUDIT SKILL — v1.4

> **LIFECYCLE-AWARE. GAP-AUDIT INTEGRATION. RED-TEAM-DOD INTEGRATION.** This release adds the RED-TEAM → DoD → ITERATE → REFINE cycle to infrastructure audits. See `skill_view('red-team-dod')`. Also includes lifecycle pipeline health checks, archival path verification, ultrametric taxonomy validation, and §0.5 GAP AUDIT INTEGRATION — Phase 4 health recommendations now output gap-audit-compatible report format.

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
vec = cf('vectorize/indexes')
pages = cf('pages/projects')
workers = cf('workers/scripts')
queues = cf('queues')

print(f'D1: {len(d1.get("result",[]))} | KV: {len(kv.get("result",[]))} | Vectorize: {len(vec.get("result",[]))}')
print(f'Pages: {len(pages.get("result",[]))} | Workers: {len(workers.get("result",[]))} | Queues: {len(queues.get("result",[]))}')
# Expected: D1: 4 | KV: 2 | Vectorize: 1 | Pages: 10 | Workers: 26 | Queues: 2
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
# Expected: 223 nodes, 340 edges
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
r = urllib.request.Request(f'https://api.cloudflare.com/client/v4/accounts/{ACCOUNT}/r2/buckets/qnfo/objects/qnfo/discovery/index.json',
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

## Infrastructure Resource Inventory

| Resource | Expected Count | Current |
|:---------|:-----:|:------:|
| D1 Databases | 4 | qnfo-graph, qnfo-audit, living-paper, portfolio-state |
| KV Namespaces | 2 | equation-cache, git-on-cloudflare-routes |
| Vectorize Indexes | 1 | qwav-research (768-dim) |
| Pages Projects | 10 | qwav, prompts-wiki, qnfo-archive, quantum-laws-of-form, qlof-primer, rwnq8, +4 more |
| Workers | 26 | graph-api, qnfo-lifecycle, living-papers-api, qnfo-archive-worker, qnfo-archive-verify, umbrella-router, +20 more |
| Queues | 2 | qnfo-lifecycle-queue, git-on-cloudflare-repo-maint |
| Knowledge Graph | 223 nodes, 340 edges | 4-domain ultrametric taxonomy, 57 project nodes |
| R2 Bucket | 1 (qnfo) | discovery, archive, projects, releases, tools |

## Lifecycle Pipeline Health Checks

| Component | Check | Endpoint |
|-----------|-------|----------|
| Lifecycle Worker | HTTP 200, status=ok | `GET /health` on `qnfo-lifecycle.q08.workers.dev` |
| Lifecycle Scan | Projects scanned, transitions | `GET /status` |
| Archive Worker | HTTP 200, status=ok | `GET /health` on `qnfo-archive-worker.q08.workers.dev` |
| Lifecycle Queue | Exists, producers + consumers configured | `wrangler queues list` |
| Discovery Index | 38 projects, archived paths correct | R2 `qnfo/discovery/index.json` |
| Knowledge Graph | Ultrametric taxonomy intact | `/nodes?label=Concept`, domain/program counts |

## Output Format

```
# INFRASTRUCTURE AUDIT REPORT
**Date:** YYYY-MM-DD | **Auditor:** QNFO Agent

## Resource Inventory
| Resource | Count | Status |
|:---------|:-----:|:------:|
| D1 Databases | 4 | OK |
| KV Namespaces | 2 | OK |
| Vectorize Indexes | 1 | OK |
| Pages Projects | 10 | OK |
| Workers | 26 | OK |
| Queues | 2 | OK |
| Knowledge Graph | 223n/340e | OK |
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

When the infrastructure audit runs (session start or on-demand), it automatically:
1. Feeds findings into the POST-PHASE GAP AUDIT (closeout-manager §2.6)
2. Maps infrastructure health to gap severity: health FAIL → BLOCKING/HIGH, orphan resources → MEDIUM, warnings → LOW
3. Outputs gap-audit-compatible report format with Gap ID, Category, Severity, Description columns

## Integration

- Runs automatically at session start (qnfo-agent §3.2 step 1.6)
- Pre-execution gate: before any upload/deploy task
- Feeds into Discovery Index updates
- Validates lifecycle pipeline health before archival operations

---

*infrastructure-audit v1.4 — Lifecycle-aware. RED-TEAM-DOD integration. Gap-audit integration (§0.5). Pipeline health checks, archival integrity, ultrametric taxonomy validation.*

## RT: RED-TEAM SELF-AUDIT

Before claiming this skill complete, autonomously run:

1. Output Verification (negative verification)
2. Assumption Challenge (state and test every assumption)
3. Edge Case Check (empty/null/max/boundary/desync)
4. DoD Integration (run _dod_enforce.py if exists)
5. Iteration (retry on failure, max 3)

ANTI-PATTERN: User should NEVER ask about quality.
Refer to RED-TEAM-PROTOCOL.md for full protocol.

