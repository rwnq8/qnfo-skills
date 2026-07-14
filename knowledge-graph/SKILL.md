---
name: knowledge-graph
description: QNFO Knowledge Graph querying for due diligence, impact analysis, ultrametric clustering, and cross-system discovery. Supports ball queries, hierarchical taxonomy, and lifecycle-aware project queries.
version: "2.4"
---
> **INCLUDES AUTONOMOUS RED-TEAM SELF-AUDIT.** Before claiming this skill complete, autonomously run: (1) Output Verification -- negative verification. (2) Assumption Challenge -- state and test every assumption. (3) Edge Case Check -- empty/null/max/boundary/desync. (4) DoD Integration -- run _dod_enforce.py if exists. (5) Iteration -- retry on failure, max 3. ANTI-PATTERN: User should NEVER ask about quality.

> **Related:** qnfo-agent, infrastructure-audit



### Programmatic Loading & Execution
This skill is loaded and executed **programmatically by the LLM system** 
during response generation. Loading is triggered automatically via 
`skill_view('knowledge-graph')` or `read()` with filesystem path.
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

## Autonomous Continuation Protocol (v1.0)

**All graph operations execute autonomously.** Agent MUST: (1) chain query→analyze→seed→verify without user prompts, (2) tag `[AUTO-CONTINUE]` between stages. **ANTI-PATTERN:** User NEVER says "CONTINUE."

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
  {"step": "Query graph-api /stats for ecosystem overview", "status": "pending"},
  {"step": "Query /neighbors/{entity} for dependencies", "status": "pending"},
  {"step": "Run impact analysis on target entity", "status": "pending"},
  {"step": "Seed missing BELONGS_TO edges for orphaned entities", "status": "pending"},
  {"step": "Verify connectivity with re-query", "status": "pending"}
])


# QNFO Knowledge Graph — Agent Skill v2.4

> **ULTRAMETRIC-AWARE.** This release adds ultrametric taxonomy support, ball queries, and lifecycle-aware project filtering.
> All queries go through the deployed Cloudflare Worker API. No local installation required.

## Overview

The QNFO Knowledge Graph is a D1-backed graph database (Cloudflare-native, zero external services) connecting every entity in the QNFO ecosystem. It now includes an **ultrametric hierarchical taxonomy** where projects are organized into 4 domains, 12 programs, forming a 2-adic tree with distances that satisfy the strong triangle inequality: $d(x,z) \leq \max(d(x,y), d(y,z))$.

**Deployed API:** `https://graph-api.q08.workers.dev` (Cloudflare Worker, D1 qnfo-graph)
**Current State:** 1680 nodes, 2927 edges, 8 API endpoints (verified live 2026-07-05)

## Ultrametric Taxonomy Structure

```
Root (d=1.0, level 0)
├── QWAV Physics (d=0.5)
│   ├── Quantum Error Correction (d=0.25) — 4 projects
│   ├── Ultrametric Theory (d=0.25) — 2 projects
│   └── General Research (d=0.25) — 3 projects
├── Infrastructure (d=0.5)
│   ├── Knowledge & Data (d=0.25) — 3 projects
│   ├── Deployment & Storage (d=0.25) — 5 projects
│   ├── Automation (d=0.25) — 3 projects
│   └── Portfolio (d=0.25) — 3 projects
├── Content & Publications (d=0.5)
│   ├── Papers (d=0.25) — 3 projects
│   ├── Sites & Design (d=0.25) — 3 projects
│   └── Discovery & Assets (d=0.25) — 4 projects
└── Research Programs (d=0.5)
    ├── Retrospective Analysis (d=0.25) — 2 projects
    └── Computational (d=0.25) — 3 projects
```

**Distance function:** $d(x,y) = 2^{-\text{LCA\_depth}}$ (2-adic metric)
- Same program: $d = 0.25$
- Same domain: $d = 0.50$
- Different domain: $d = 1.00$

**Verified:** 0 violations on 500 random triples of the strong triangle inequality. All triangles are isosceles.

## When to Use This Skill

| Scenario | Query Type |
|:---------|:-----------|
| **Due Diligence** — What exists before I start work? | Ball query: `/neighbors/{project}` filters by ultrametric distance |
| **Impact Analysis** — What breaks if I change X? | `/impact/{nodeName}` endpoint |
| **Ultrametric Clustering** — What projects are in my ball? | `GET /neighbors/concept-domain-X` or `/neighbors/concept-program-Y` |
| **Paradigm Forecasting** — What research will matter most? | `query_graph` for domain nodes → feed to `deep-research` skill for Bayesian cascade modeling |
| **Dependency Check** — What does this project depend on? | Neighbor traversal with edge type filter |
| **Cross-Reference** — Which projects use this template? | Edge query by type |
| **Audit Trail** — Who changed what, when? | Session → Commit → Deployment chains |
| **Lifecycle Status** — Is this project active or archived? | Node properties: `status`, `last_active` |
| **Ecosystem Health** — Any dead/broken deployments? | Query with status filters |

## API Reference

All endpoints return JSON. The Worker supports CORS (any origin).

### GET /stats
Graph statistics — node counts by label, relationship counts by type.

```python
import urllib.request, json
r = urllib.request.Request("https://graph-api.q08.workers.dev/stats",
    headers={"User-Agent": "Mozilla/5.0"})
data = json.loads(urllib.request.urlopen(r, timeout=10).read())
# Returns: {totalNodes, totalEdges, nodeLabels: [...], relationshipTypes: [...]}
# Current: 2721 nodes, 3993 edges
```

### GET /nodes?label=Project&search=pdf
List nodes, optionally filtered by label and/or name search.

```python
# All Projects (74 currently)
url = "https://graph-api.q08.workers.dev/nodes?label=Project"

# Ultrametric concept nodes (32 — 16 domain, 12 program, 4 other)
url = "https://graph-api.q08.workers.dev/nodes?label=Concept"

# Search by name
url = "https://graph-api.q08.workers.dev/nodes?label=Template&search=PHYSICS"
```

### GET /nodes/:id
Get a specific node with its properties and relationships.

```python
# Project node
url = "https://graph-api.q08.workers.dev/nodes/pdf-builder"

# Ultrametric domain node
url = "https://graph-api.q08.workers.dev/nodes/concept-domain-qwav-physics"
```

### GET /neighbors/:id — Including Ultrametric Hierarchy
Get all neighbors of a node. For concept nodes, returns all children in the ultrametric tree.

```python
# What's in the Quantum Error Correction program?
url = "https://graph-api.q08.workers.dev/neighbors/concept-program-quantum-error-correction"
# Returns: [toward-p-adic-qec, ultrametric-benchmark, p-adic-hardware-co-design, adelic-qec-synthesis]

# What projects are in my ultrametric ball? (same domain = d ≤ 0.5)
url = "https://graph-api.q08.workers.dev/neighbors/concept-domain-infrastructure"
# Returns: [Knowledge & Data, Deployment & Storage, Automation, Portfolio] + QNFO

# What does pdf-builder connect to?
url = "https://graph-api.q08.workers.dev/neighbors/pdf-builder"
```

### GET /edges?type=DEPENDS_ON&source=project-a&target=project-b
List edges, filterable by relationship type, source, and target.

```python
# All DEPENDS_ON relationships
url = "https://graph-api.q08.workers.dev/edges?type=DEPENDS_ON"

# Ultrametric containment edges
url = "https://graph-api.q08.workers.dev/edges?type=ULTRA_CONTAINS"

# Taxonomy edges (BELONGS_TO)
url = "https://graph-api.q08.workers.dev/edges?type=BELONGS_TO"

# What depends on pdf-builder?
url = "https://graph-api.q08.workers.dev/edges?type=DEPENDS_ON&target=pdf-builder"
```

### POST /query
Run arbitrary SQL queries against the D1 graph database.

```python
import urllib.request, json
body = json.dumps({
    "query": "SELECT n.name, n.label FROM nodes n JOIN edges e ON n.id = e.target_id WHERE e.source_id = (SELECT id FROM nodes WHERE name = ?) AND e.relationship_type = 'DEPENDS_ON'",
    "params": ["pdf-builder"]
}).encode()
r = urllib.request.Request("https://graph-api.q08.workers.dev/query",
    data=body, headers={"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"})
data = json.loads(urllib.request.urlopen(r, timeout=10).read())
```

### GET /impact/:nodeName
**Most important endpoint.** Traverses all downstream dependents of a node.

```python
# What depends on pdf-builder?
url = "https://graph-api.q08.workers.dev/impact/pdf-builder"

# What depends on the PHYSICS-STYLE template?
url = "https://graph-api.q08.workers.dev/impact/PHYSICS-STYLE"

# What depends on the qnfo R2 bucket?
url = "https://graph-api.q08.workers.dev/impact/qnfo"
```

Returns:
```json
{
  "node": {"name": "pdf-builder", "label": "Project"},
  "dependents": [
    {"id": "project-living-paper", "label": "Project", "relationship_type": "DEPENDS_ON", "depth": 1}
  ],
  "totalDependents": 1,
  "maxDepth": 1
}
```

### POST /sync
**Bulk upsert or delete nodes and edges.** Use to seed new entities.

```python
import urllib.request, json

# Bulk upsert (idempotent — safe to re-run)
body = json.dumps({
    "action": "bulk",
    "nodes": [
        {"id": "project-new-project", "label": "Project", "name": "new-project",
         "properties": {"status": "active", "last_active": "2026-06-21T00:00:00Z"}},
        {"id": "decision-adr-021", "label": "Decision", "name": "ADR-021: Something"}
    ],
    "edges": [
        {"id": "edge-001", "source_id": "project-new-project", "target_id": "decision-adr-021",
         "relationship_type": "AFFECTED_BY", "properties": {}}
    ]
}).encode()

r = urllib.request.Request("https://graph-api.q08.workers.dev/sync",
    data=body, method="POST",
    headers={"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"})
result = json.loads(urllib.request.urlopen(r, timeout=15).read())
```

### GET /ball/:project ?radius=0.5 (Conceptual — Implemented via /neighbors)

While the `/ball` endpoint is not yet a first-class API path, ball queries are available via ultrametric concept node neighbors:

```python
def ultrametric_ball(project_name, radius):
    """Get all projects within ultrametric distance r of target."""
    # Step 1: Query project node to find its program
    proj = graph_query(f"/nodes/{project_name}")
    props = proj.get("properties", {})
    
    # Step 2: Get program from taxonomy
    neighbors = graph_query(f"/neighbors/{project_name}")
    program_nodes = [n for n in neighbors.get("neighbors", [])
                     if n.get("relationship_type") == "BELONGS_TO"]
    
    if not program_nodes:
        return []
    
    program = program_nodes[0]
    program_name = program.get("name", "")
    
    if radius <= 0.25:
        # Same program only
        return [n for n in graph_query(f"/neighbors/concept-program-{program_name.lower().replace(' ','-').replace('&','and')}").get("neighbors", [])
                if n.get("label") == "Project"]
    elif radius <= 0.5:
        # Same domain
        domain_name = program.get("properties", {}).get("parent_domain", "")
        domain_id = f"concept-domain-{domain_name.lower().replace(' ','-').replace('&','and')}"
        return [n for n in graph_query(f"/neighbors/{domain_id}").get("neighbors", [])
                if n.get("label") in ("Project", "Concept")]
    else:
        # Global
        return graph_query("/nodes?label=Project").get("nodes", [])
```

## Query Recipes (Common Patterns)

### Recipe 1: Due Diligence — What Should I Know Before Working on X?
```python
# Step 1: Check if project exists and get its taxonomy
GET /nodes?label=Project&search=X

# Step 2: What's in its ultrametric ball? (same program = siblings)
GET /neighbors/concept-program-<program-name>

# Step 3: What depends on it?
GET /impact/X

# Step 4: What's its lifecycle status?
# Check node properties: status, last_active
```

### Recipe 2: Ultrametric Clustering — Find Related Projects
```python
# Get all projects in the same domain (d <= 0.5)
GET /neighbors/concept-domain-infrastructure
# Returns: 14 projects across 4 programs

# Get all projects in Quantum Error Correction (d <= 0.25)
GET /neighbors/concept-program-quantum-error-correction
# Returns: 4 QEC projects
```

### Recipe 3: Impact Analysis — What Breaks If I Change X?
```python
GET /impact/X
# Then check each dependent for lifecycle status
```

### Recipe 4: Ecosystem Health — Lifecycle Audit
```python
# Find projects with no status
POST /query {"query": "SELECT name FROM nodes WHERE label='Project' AND json_extract(properties, '$.status') IS NULL", "params": []}

# Find stale ACTIVE projects
POST /query {"query": "SELECT name, json_extract(properties, '$.last_active') as last FROM nodes WHERE label='Project' AND json_extract(properties, '$.status')='ACTIVE'", "params": []}

# Find ARCHIVED projects with new archive paths
POST /query {"query": "SELECT name, json_extract(properties, '$.r2_path') as path FROM nodes WHERE label='Project' AND json_extract(properties, '$.r2_path') LIKE '%archive%'", "params": []}
```

### Recipe 5: Full Audit Trail for a Paper
```python
GET /neighbors/PAPER_SLUG
```

## Edge Type Reference

| Type | Count | Purpose |
|------|:-----:|---------|
| RELATES_TO | 522 | General-purpose relationship |
| OWNS | 274 | Organizational hierarchy |
| BELONGS_TO | 154 | Ultrametric taxonomy edges |
| PUBLISHED_AS | 124 | Publication DOI mapping |
| AUTHORED_BY | 109 | Paper authorship |
| HOSTED_AT | 108 | Pages deployment hosting |
| LICENSED_UNDER | 108 | License attribution |
| STORED_AT | 103 | R2 storage location |
| PUBLISHED_IN | 63 | Zenodo venue records |
| ULTRA_CONTAINS | 59 | 2-adic hierarchical containment |
| REFERENCES | 38 | Paper-to-paper citations |
| AFFECTS | 35 | Cross-entity impact |
| DEPENDS_ON | 34 | Infrastructure dependency |
| OWNED_BY | 24 | Reverse organizational |

## Lifecycle Integration

The Knowledge Graph is the central registry for project lifecycle. Key properties on each project node:

| Property | Example | Purpose |
|----------|---------|---------|
| `status` | `ACTIVE`, `ARCHIVED`, `NEEDS-TRIAGE` | Lifecycle state |
| `last_active` | `2026-06-21T00:00:00Z` | ISO timestamp for staleness detection |
| `r2_path` | `qnfo/archive/projects/pdf-builder/` | Canonical storage path |
| `source` | `discovery-index` | Origin of the data |

## Failure Handling

| Scenario | Response |
|:---------|:---------|
| **API unreachable** | Graph API at `graph-api.q08.workers.dev` may cold-start. Retry once after 2s. If still down: mark `[GRAPH-UNAVAILABLE]`. |
| **Node not found** | Returns HTTP 200 with `{"error": "Node 'X' not found"}`. Check for `error` key. Flag `[GRAPH-MISSING]`. |
| **Pagination truncation** | `/nodes` hard-limits at 100 results. For complete enumeration, use `/nodes?label=X` to filter by type. |
| **Stale data** | Graph may lag behind DI (sync gap). Always cross-reference with Discovery Index for critical decisions. |
| **Query syntax error** | POST /query returns error. Verify SQL against D1 schema. Test with simpler query first. |

## Version History

| Version | Date | Changes |
|:--------|:-----|:--------|
| v2.4 | 2026-07-04 | **DO+SQLite + Workers AI Integration:** Added DO+SQLite Worker (qnfo-agent-session) for KG write coordination via `/kg-mutex/*` endpoints. Added R2 Event Notifications auto-trigger for graph re-indexing. Added Workers AI Worker (qnfo-ai-worker) for paper enrichment (classify, citations). Updated API endpoint table with 4 new DO endpoints. |
| v2.3 | 2026-07-02 | **Count refresh:** 2721 nodes (40+ labels), 3993 edges (50+ types). Added Paper (178), CloudflareAsset (148), ZenodoRecord (124), R2Object (115) labels. Edge type table expanded to 14 types. RELATES_TO now dominant (522). Verified live via KG API. |
| v2.2 | 2026-06-28 | **Count refresh:** Verified live — 261 nodes, 401 edges. OWNS now dominant edge (205 vs 99). Needs paper REFERENCES edges (currently 0 paper connections). |
| v2.0 | 2026-06-21 | **Ultrametric Taxonomy:** Added 4-domain/12-program ultrametric tree with BELONGS_TO and ULTRA_CONTAINS edges. Added ball query recipe. Updated graph stats (238/382). Added lifecycle property documentation. Verified 0 violations on 500 triples (strong triangle inequality). |
| v1.1 | 2026-06-03 | Phase 2/3 Integration: POST /sync documentation, reseed protocol. |
| v1.0 | 2026-06-01 | Initial skill. Graph API integration, query recipes. |

---

*knowledge-graph skill v2.3 — Ultrametric-aware. Ball queries, hierarchical taxonomy, lifecycle integration.*

## Known API Limitations

| Issue | Detail | Workaround | Session Root Cause |
|:------|:-------|:-----------|:-------------------|
| **Pagination broken** | `/nodes?offset=N` returns same 100 results at every offset. The `/query` endpoint has a hard cap of 100 results. | Query by specific label + search term to reduce result set. For full inventory, use multiple targeted queries. | `dFIACfjsDq_MFfvRSA8ni`, `L5_a35Udjt-Ou3msEgYVG` (2026-07-04) |
| **DELETE not supported** | `POST /sync` with `"action":"delete"` returns `deleted_nodes: 0`. `DELETE /nodes/:id` returns node data but does NOT delete. | Direct D1 SQL: `DELETE FROM nodes WHERE label='Paper' AND created_at < '2026-07-01'` on `qnfo-graph` D1 database. | `dFIACfjsDq_MFfvRSA8ni` — 169 orphaned obsidian nodes could not be deleted via API |
| **STORED_AT references opaque** | R2Object node IDs are hashes (`r2-3f1a008e7ba4b96d`) — cannot resolve to human-readable R2 paths through the KG. | Store actual R2 path as a property on the R2Object node. | `L5_a35Udjt-Ou3msEgYVG` — blocked paper indexing pipeline |
| **`/query` endpoint format** | Results returned in `rows` key, not `results`. `json_extract()` may not work on all queries. | Parse `rows` from the response JSON. Test queries individually. | `dFIACfjsDq_MFfvRSA8ni` |

## Handoff Protocol (MANDATORY at Closeout)

1. **Verify** ALL execute_plan items marked [EXECUTED] with tool evidence (Test-Path, exec output, git log)
2. **Archive** session artifacts to R2 canonical storage: `npx wrangler r2 object put qnfo/audit/... --remote --file=<artifact>`
3. **Generate** continuation prompt documenting pending work and current state for the next session
4. **Clean up** ephemeral _* files and __pycache__ directories: `Remove-Item _* -Recurse -Force`

### Continuation Prompt Template
```
TASK: [description of pending work from execute_plan]
STATE: [current state — what's executed, what's blocked, why]
NEXT: [first executable action for the next session]
R2: [canonical path for session artifacts]
```


## Closeout Protocol (MANDATORY)

Before declaring this skill workflow complete:
1. **Task Execution Verification:** Compare planned tasks ([PENDING] in execute_plan) vs executed tasks ([EXECUTED] with evidence)
2. **Filesystem Verification:** `Test-Path <file>` for every file claimed as created/modified. Never claim from memory.
3. **Git Verification:** `git log -1 --oneline` for every commit claimed. Verify commit hash exists.
4. **R2 State Upload:** Upload session audit trail to `qnfo/audit/` — conversations, decisions, state files.
5. **Discovery Index Update:** Update `qnfo/discovery/index.json` with any new resources created, projects modified, or publications generated.
6. **Ephemeral Cleanup:** Delete ALL _* prefixed files and __pycache__ directories. Session is not complete until `Get-ChildItem -File -Name | Where-Object { $_ -match '^_' }` returns zero results.

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
