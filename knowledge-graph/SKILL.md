---
name: knowledge-graph
description: QNFO Knowledge Graph querying for due diligence, impact analysis, and cross-system discovery. Use when agents need to understand project dependencies, trace audit trails, or answer "what depends on X?" questions. Now with POST /sync for live graph updates.
version: "1.1"
---

# QNFO Knowledge Graph — Agent Skill v1.1

> **SELF-CONTAINED:** This skill provides access to the QNFO ecosystem graph database.
> All queries go through the deployed Cloudflare Worker API. No local installation required.

## Overview

The QNFO Knowledge Graph is a D1-backed graph database (Cloudflare-native, zero external services) connecting every entity in the QNFO ecosystem: projects, papers, Cloudflare resources, agent sessions, decisions, templates, skills, and more. It enables impact analysis, complete audit trails, and cross-system discovery that are impossible with flat files alone.

**Deployed API:** `https://graph-api.q08.workers.dev` (Cloudflare Worker, D1 qnfo-graph)
**Current State:** 183 nodes, 282 edges, 8 API endpoints (verified live 2026-06-19)

## When to Use This Skill

| Scenario | Query Type |
|:---------|:-----------|
| **Due Diligence** — What exists before I start work? | List all projects, find related decisions |
| **Impact Analysis** — What breaks if I change X? | `/impact/{nodeName}` endpoint |
| **Dependency Check** — What does this project depend on? | Neighbor traversal |
| **Cross-Reference** — Which projects use this template? | Edge query by type |
| **Audit Trail** — Who changed what, when? | Session → Commit → Deployment chains |
| **Discovery** — What Cloudflare assets exist? | List nodes by label |
| **Ecosystem Health** — Any dead/broken DNS or deployments? | Query with status filters |

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
```

### GET /nodes?label=Project&search=pdf
List nodes, optionally filtered by label and/or name search.

```python
# All Projects
url = "https://graph-api.q08.workers.dev/nodes?label=Project"

# Search by name
url = "https://graph-api.q08.workers.dev/nodes?label=Template&search=PHYSICS"
```

### GET /nodes/:id
Get a specific node with its properties and relationships.

```python
url = "https://graph-api.q08.workers.dev/nodes/pdf-builder"
```

### GET /neighbors/:id
Get all neighbors of a node (what it connects to).

```python
url = "https://graph-api.q08.workers.dev/neighbors/pdf-builder"
```

### GET /edges?type=DEPENDS_ON&source=project-a&target=project-b
List edges, filterable by relationship type, source, and target.

```python
# All DEPENDS_ON relationships
url = "https://graph-api.q08.workers.dev/edges?type=DEPENDS_ON"

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
    {"name": "no-bullshit-physics-writing", "label": "Paper", "relationship": "PRODUCED", "depth": 1},
    {"name": "retrospective-prophecy-astrology", "label": "Paper", "relationship": "PRODUCED", "depth": 1}
  ],
  "totalDependents": 2,
  "maxDepth": 1
}
```

### POST /sync
**Phase 2 — Live Graph Updates.** Bulk upsert or delete nodes and edges. Use this to seed new entities after session close-out or ecosystem changes.

```python
import urllib.request, json

# Bulk upsert (idempotent — safe to re-run)
body = json.dumps({
    "action": "bulk",
    "nodes": [
        {"id": "project-new-project", "label": "Project", "name": "new-project",
         "properties": {"status": "active", "phase": "1", "priority": "HIGH"}},
        {"id": "decision-adr-020", "label": "Decision", "name": "ADR-020: Something",
         "properties": {"decision_id": "ADR-020", "date": "2026-06-03", "status": "accepted"}}
    ],
    "edges": [
        {"id": "edge-001", "source_id": "project-new-project", "target_id": "decision-adr-020",
         "relationship_type": "AFFECTED_BY", "properties": {}}
    ]
}).encode()

r = urllib.request.Request("https://graph-api.q08.workers.dev/sync",
    data=body, method="POST",
    headers={"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"})
result = json.loads(urllib.request.urlopen(r, timeout=15).read())
# Returns: {action, upserted_nodes, upserted_edges, deleted_nodes, deleted_edges, errors, total_changes}
```

**Delete a node or edge:**
```python
body = json.dumps({
    "action": "delete",
    "nodes": [{"id": "decision-test-001", "_delete": True}],
    "edges": [{"id": "edge-001", "_delete": True}]
}).encode()
```

**Reseed the entire graph** (pull latest Discovery Index + Decision Log from R2, push to /sync):
```bash
cd qnfo/projects/qnfo-knowledge-graph
npx wrangler r2 object get qnfo/discovery/index.json --remote --file=_discovery_index.json
npx wrangler r2 object get qnfo/audit/decisions/DECISION-LOG.md --remote --file=_decision_log.md
python seed_live_d1.py
```
This script parses the Discovery Index and Decision Log, creates node/edge payloads, and POSTs to /sync for live D1 updates. No manual SQL needed.

## Query Recipes (Common Patterns)

### Recipe 1: Due Diligence — What Should I Know Before Working on X?
```python
# Step 1: Check if project exists
GET /nodes?label=Project&search=X

# Step 2: What are its dependencies?
GET /neighbors/X

# Step 3: What decisions affect it?
POST /query {"query": "SELECT n.* FROM nodes n JOIN edges e ON n.id = e.source_id WHERE e.target_id = (SELECT id FROM nodes WHERE name = ?) AND e.relationship_type = 'AFFECTS'", "params": ["X"]}

# Step 4: Any open issues?
POST /query {"query": "SELECT n.* FROM nodes n JOIN edges e ON n.id = e.source_id WHERE e.target_id = (SELECT id FROM nodes WHERE name = ?) AND n.label = 'Issue' AND n.properties LIKE '%open%'", "params": ["X"]}
```

### Recipe 2: Impact Analysis — What Breaks If I Change X?
```python
GET /impact/X
```
Then check each dependent for active status and recent sessions.

### Recipe 3: Template/Skill Usage — Which Projects Use This?
```python
GET /edges?type=USES_TEMPLATE&target=TEMPLATE_NAME
GET /edges?type=USES_SKILL&target=SKILL_NAME
```

### Recipe 4: Ecosystem Health — Dead Assets
```python
# Find Cloudflare assets without active projects
POST /query {"query": "SELECT n.name FROM nodes n WHERE n.label = 'CloudflareAsset' AND n.name NOT IN (SELECT e.target_id FROM edges e WHERE e.relationship_type = 'DEPLOYED_TO')", "params": []}
```

### Recipe 5: Full Audit Trail for a Paper
```python
# Start from paper, traverse backward through sessions, commits, deployments
GET /neighbors/PAPER_SLUG
```

## Integration Into Agent Workflow

### In Due Diligence (Step 0 of any workflow)

Before starting work on any project, template, or skill, query the graph:

```python
import urllib.request, json

def graph_query(endpoint):
    """Query the QNFO Knowledge Graph API."""
    url = f"https://graph-api.q08.workers.dev{endpoint}"
    r = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    return json.loads(urllib.request.urlopen(r, timeout=10).read())

# 1. Check ecosystem stats
stats = graph_query("/stats")
print(f"Graph: {stats['totalNodes']} nodes, {stats['totalEdges']} edges")

# 2. Impact analysis for the target
target = "pdf-builder"  # or whatever you're about to modify
impact = graph_query(f"/impact/{target}")
if impact.get("totalDependents", 0) > 0:
    print(f"[WARN] {target} has {impact['totalDependents']} dependents:")
    for dep in impact.get("dependents", []):
        print(f"  - {dep['name']} ({dep['label']}) via {dep['relationship']}")
else:
    print(f"[OK] No dependents found for {target}")
```

### On Session Close-Out

After completing work, note new entities that should be added to the graph (via the Phase 3 ingestion pipeline). If the pipeline isn't live, flag as `[GRAPH-SYNC-NEEDED]` so the next session can reconcile.

## D1 Schema Reference

The graph is stored in D1 (Cloudflare's serverless SQLite) with a universal schema:

**nodes table:**
| Column | Type | Description |
|:-------|:-----|:-----------|
| id | TEXT PRIMARY KEY | Unique node identifier (usually the name/slug) |
| label | TEXT | Node type (Project, Paper, Template, etc.) |
| name | TEXT | Human-readable name |
| properties | TEXT | JSON blob of additional properties |
| created_at | TEXT | ISO 8601 timestamp |

**edges table:**
| Column | Type | Description |
|:-------|:-----|:-----------|
| id | TEXT PRIMARY KEY | Unique edge identifier |
| source_id | TEXT | Source node id |
| target_id | TEXT | Target node id |
| relationship_type | TEXT | Edge label (DEPENDS_ON, PRODUCED, etc.) |
| properties | TEXT | JSON blob of temporal/contextual properties |
| created_at | TEXT | ISO 8601 timestamp |

**Node labels (14 types):**
Organization, Project, Paper, AgentSession, CloudflareAsset, GitCommit, Decision, Template, Skill, Person, Issue, Domain, Deployment, Concept

**Relationship types (16 types):**
OWNS, PRODUCED, DEPLOYED_TO, USES_TEMPLATE, USES_SKILL, MADE_DECISION, COMMITTED, REFERENCES, VERSION_OF, AFFECTS, BLOCKED_BY, DEPENDS_ON, SERVES, MENTIONS, CREATED, MODIFIED

## Embedded Scripts

> **SELF-CONTAINED:** Before executing any script, verify it exists at its canonical path.

| Script | Canonical Path | Purpose |
|:-------|:---------------|:--------|
| `seed_live_d1.py` | `qnfo/projects/qnfo-knowledge-graph\seed_live_d1.py` | **Primary seeder:** pulls Discovery Index + Decision Log from R2, generates nodes/edges, POSTs to /sync for live D1 updates. Phase 2 pipeline. |
| `seed_graph.py` | `qnfo/projects/qnfo-knowledge-graph\seed_graph.py` | Generate seed Cypher from discovery index (legacy — prefer seed_live_d1.py) |
| `ingest_session.py` | `qnfo/projects/qnfo-knowledge-graph\ingest_session.py` | Parse DeepChat exports into AgentSession + MENTIONS nodes |

### Bootstrap Protocol
```powershell
# Pull seed scripts from R2
npx wrangler r2 object get qnfo/tools/seed_live_d1.py --remote --file=_seed_live_d1.py

# Or use the local copy
Test-Path "qnfo/projects/qnfo-knowledge-graph\seed_live_d1.py"
Test-Path "qnfo/projects/qnfo-knowledge-graph\ingest_session.py"
# If MISSING: check git repo — these are version-controlled in the qnfo-knowledge-graph project
```

## Failure Handling

| Scenario | Response |
|:---------|:---------|
| **API unreachable** | Graph API at `graph-api.q08.workers.dev` may be cold-starting (~90ms avg, no cold start penalty observed). Retry once after 2s. If still down: mark query results as `[GRAPH-UNAVAILABLE]`, proceed with local filesystem discovery. |
| **Node not found** | `/nodes/X` and `/impact/X` return HTTP 200 with `{"error": "Node 'X' not found"}` (NOT 404). Check for `error` key in response. Flag as `[GRAPH-MISSING: node X not yet in graph]`. Do NOT fabricate. |
| **Impact returns error** | API returns `{"error": "..."}` for unknown nodes. Code MUST check for `error` key BEFORE accessing `totalDependents`. Pattern: `if 'error' in impact: handle; elif impact.get('totalDependents',0) > 0: ...` |
| **Pagination truncation** | `/nodes` endpoint hard-limits at 100 results. Currently ~83 of 183 nodes are invisible. For complete enumeration, use `/nodes?label=X` to filter by type, or POST `/query` with custom SQL. |
| **Empty impact (no dependents)** | No dependents found. Could mean (a) truly no dependents, or (b) graph isn't fully populated. Flag: `[GRAPH-IMPACT-EMPTY: verify with filesystem]`. |
| **Rate limited** | The Worker has generous limits. If rate-limited, wait 5s and retry. |
| **Stale data** | The graph may lag behind reality (sync gap between ecosystem changes and reseed). Always cross-reference with `_discovery_index.json` and local filesystem for critical decisions. Trigger a reseed if the graph is >24h stale: `POST /sync` with latest data. |
| **Query syntax error** | POST /query returns error. Verify SQL syntax against the D1 schema above. Test with a simpler query first. |

## Verification Gate

Before acting on graph results:
1. Does the graph node count match what you'd expect? (Check `/stats`)
2. Are recent entities missing? (Graph may be stale — cross-reference with discovery index)
3. For critical impact decisions: verify with filesystem search as backup

## Version History

| Version | Date | Changes |
|:--------|:-----|:--------|
| v1.1 | 2026-06-03 | **Phase 2/3 Integration:** Added POST /sync endpoint documentation (bulk upsert/delete). Added reseed protocol (seed_live_d1.py → POST /sync pipeline). Updated graph stats (183 nodes, 282 edges, 8 endpoints). Added seed_live_d1.py to embedded scripts. Updated stale data handling (sync pipeline now live). Architecture corrected: D1-native, not Neo4j-backed. |
| v1.0.1 | 2026-06-01 | **Edge Case Audit:** Corrected Failure Handling — API returns HTTP 200 with `error` key for missing nodes (not 404). Added Pagination Truncation entry (100-node limit). Added Impact Returns Error entry. Verified against live API (125 nodes, 132 edges, ~95ms avg latency). |
| v1.0 | 2026-06-01 | Initial skill. Graph API integration, query recipes, due diligence workflow. |
