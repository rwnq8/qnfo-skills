---
name: knowledge
description: QNFO Knowledge Graph and durable memory management -- graph querying for due diligence and impact analysis (stats, nodes, neighbors, impact, query endpoints), ultrametric clustering and taxonomy edge seeding, semantic memory search via Vectorize, persistent fact storage in D1/Vectorize, cross-system discovery, and paper context retrieval. Use for remembering, recalling, and discovering knowledge across the QNFO ecosystem.
version: "2.0"
triggers: ["knowledge graph", "KG", "graph", "graph-api", "dependencies", "impact", "neighbors", "nodes", "edges", "due diligence", "memory", "remember", "recall", "durable learning", "semantic search", "Vectorize", "D1 memory", "fact storage", "discovery", "cross-system", "ultrametric", "p-adic", "taxonomy", "impact analysis", "what exists", "who depends", "ecosystem", "paper search", "memory search", "fact", "knowledge base"]
related: ["qnfo-agent"]
priority: 1
platform: cloudflare
autonomous: true
self_sufficient: true
---

# KNOWLEDGE -- v2.0 (Ultra-Consolidated KG + Memory)

> **Merges 2:** knowledge-graph + memory-management
> **Related:** Always load with `qnfo-agent` for Due Diligence Protocol (§3) -- KG-First Discovery Gate.
> **Cloudflare Full-Stack:** KG API runs on Cloudflare Workers. Memories persist in D1 + Vectorize (768-dim cosine). All knowledge infrastructure is Cloudflare-native.

## execute_plan

update_plan([
  {"step": "Query KG /stats for ecosystem overview (nodes, edges, labels)", "status": "pending"},
  {"step": "Query KG /nodes or /neighbors for specific entity discovery", "status": "pending"},
  {"step": "Query D1 + Vectorize for durable memories and paper context", "status": "pending"},
  {"step": "Perform impact analysis or store new facts as needed", "status": "pending"},
  {"step": "Seed taxonomy edges for orphaned KG nodes (minimum 1 edge per entity)", "status": "pending"},
])

---

## Knowledge Graph API

All endpoints accessible via `query_graph()` tool.

### /stats -- Ecosystem Overview
```python
# Who am I working with? What's out there?
stats = query_graph('stats')
# Returns: totalNodes, totalEdges, nodeLabels (with counts), relationshipTypes (with counts)
print(f"KG: {stats['totalNodes']} nodes, {stats['totalEdges']} edges")
for label in stats.get('nodeLabels', []):
    print(f"  {label['label']}: {label['count']}")
```

**Current state (2026-07):** 3,242 nodes, 4,697 edges. Paper=1,227, Project=92, Skill=60, Concept=49, ResearchQuestion=49, Finding=44, GovernancePolicy=14.

## Reusable Scripts

### D1 KG 4-D Seed Script
```js
// _kg_seed_4d.js — Seed Knowledge Graph Paper nodes with 4-D distribution properties
const T = process.env.CLOUDFLARE_API_TOKEN; // requires D1:Edit permission
const ACCOUNT = '...'; // Cloudflare account ID
const DB = '...'; // qnfo-graph database UUID

// === Seed single node ===
const props = {
  distribution_status: 'complete', // draft|published|distributed|durable|complete
  ipfs_cid: 'bafkrei...',
  arweave_tx: 'CFC5MQLe...',
  dns_link: '_dnslink.mypaper.mydomain.org',
  zenodo_doi: '10.5281/zenodo.XXXXX',
  internet_archive: 'https://web.archive.org/web/...',
  distribution_date: new Date().toISOString().split('T')[0]
};

const sql = `UPDATE nodes SET properties = json_set(
  COALESCE(properties,'{}'),
  '$.distribution_status', ?1,
  '$.ipfs_cid', ?2,
  '$.arweave_tx', ?3,
  '$.dns_link', ?4,
  '$.zenodo_doi', ?5,
  '$.internet_archive', ?6,
  '$.distribution_date', ?7
) WHERE id = 'node-id'`;

await fetch('https://api.cloudflare.com/client/v4/accounts/' + ACCOUNT + '/d1/database/' + DB + '/query', {
  method: 'POST',
  headers: { 'Authorization': 'Bearer ' + T, 'Content-Type': 'application/json' },
  body: JSON.stringify({ sql, params: [props.distribution_status, props.ipfs_cid, props.arweave_tx, props.dns_link, props.zenodo_doi, props.internet_archive, props.distribution_date] })
});

// === Bulk seed all draft nodes ===
await fetch('https://api.cloudflare.com/client/v4/accounts/' + ACCOUNT + '/d1/database/' + DB + '/query', {
  method: 'POST',
  headers: { 'Authorization': 'Bearer ' + T, 'Content-Type': 'application/json' },
  body: JSON.stringify({ sql: "UPDATE nodes SET properties = json_set(COALESCE(properties,'{}'), '$.distribution_status', 'draft') WHERE label = 'Paper' AND (properties IS NULL OR properties NOT LIKE '%distribution_status%')" })
});

// === Verify ===
const r = await fetch('https://api.cloudflare.com/client/v4/accounts/' + ACCOUNT + '/d1/database/' + DB + '/query', {
  method: 'POST',
  headers: { 'Authorization': 'Bearer ' + T, 'Content-Type': 'application/json' },
  body: JSON.stringify({ sql: "SELECT COUNT(*) as c FROM nodes WHERE label = 'Paper' AND properties LIKE '%distribution_status%'" })
});
const d = await r.json();
console.log('Papers with 4-D properties:', d.result[0].results[0].c);
```
When seeding or updating KG Paper nodes, include 4-D distribution properties:
```json
{
  "distribution_status": "draft|published|distributed|durable|complete",
  "ipfs_cid": "bafkreicod...",
  "filecoin_cid": "bafybeid6z...",
  "arweave_tx": "WCauEwD...",
  "dns_link": "_dnslink.{slug}.qnfo.org",
  "internet_archive": "https://web.archive.org/web/...",
  "zenodo_doi": "10.5281/zenodo.XXXXX"
}
```
**GATE:** Paper nodes without 4-D properties are `distribution_status: "draft"` — not published.

### /nodes -- Query by Label
```python
# Find all papers, projects, concepts...
papers = query_graph('nodes', {'label': 'Paper'})
projects = query_graph('nodes', {'label': 'Project'})
rqs = query_graph('nodes', {'label': 'ResearchQuestion'})

# Search by name
results = query_graph('nodes', {'label': 'Paper', 'search': 'quantum'})
# Returns: [{id, name, slug, doi, ev_score, ...}, ...]
```

### /neighbors/{id} -- What's Connected?
```python
# What depends on this? What does it depend on?
neighbors = query_graph('neighbors', {'id': 'paper-cfpe-forecast'})
# Returns: [{id, name, label, relationship}, ...]
```

### /impact/{id} -- Impact Analysis
```python
# What would break if this changed?
impact = query_graph('impact', {'id': 'project-qnfo-gov'})
# Returns: upstream dependencies, downstream dependents, total impact score
print(f"Impact: {impact.get('totalDependents', 0)} downstream dependents")
```

### /query -- Raw Graph Queries
```python
# Custom traversal
results = query_graph('query', {
    'query': "MATCH (p:Paper)-[:BELONGS_TO]->(c:Concept) WHERE p.slug CONTAINS 'quantum' RETURN p, c"
})
```

---

## Due Diligence Gate (MANDATORY -- KG-First Discovery)

**Before ANY task involving "what exists" or ecosystem discovery:**

### Step 0a: KG /stats (MANDATORY first API call)
The Knowledge Graph is the canonical ecosystem registry. MUST query `/stats` before claiming "comprehensive" or "all" discovery.

### Step 0b: KG Label Counts
Enumerate what exists by label:
```
Paper: 1227, Project: 92, Skill: 60, Concept: 49
ResearchQuestion: 49, Finding: 44, GovernancePolicy: 14
Decision: ??, Handoff: ??, Session: ??
```

### Step 0c: D1 + Vectorize Cross-Reference
- D1 portfolio-state: `npx wrangler d1 execute portfolio-state --remote --command "SELECT type, COUNT(*) as count FROM resources GROUP BY type" -y`
- D1 living-paper: paper count vs KG Paper count
- Vectorize: `search_memories({query: "project state", limit: 5})`

**GATE:** If KG was NOT queried before "comprehensive" claim -> cherry-picking violation. Files on disk are an incomplete, stale subset.

---

## Edge Seeding Gate (MANDATORY)

### Trigger
Before executing work on ANY entity, check KG connectivity. Query `/neighbors/{entity}`. If neighbor count is 0 -> entity is orphaned. Seed taxonomy edges BEFORE proceeding.

### Minimum Viable Connection (HARD GATE)
Every entity must have at least ONE `BELONGS_TO` edge to a domain or program concept node.

### Seeding Protocol
1. Query `/nodes?label=Concept` for available domains (level=1) and programs (level=2)
2. Map entity to domain/program based on metadata (tags, domain field, name heuristics)
3. Seed edges via Python script posting to graph-api sync endpoint
4. Verify: re-query `/neighbors/{entity}` -> neighbor count must be > 0

### Why This Matters
Orphaned KG nodes produce fabricated impact analysis. "Nothing depends on this" is true only because no edges exist -- NOT because nothing depends on it.

---

## Memory Management

### Semantic Memory Search
```python
# Find past conversations, decisions, facts by MEANING (not keywords)
results = search_memories({
    "query": "What was the Cloudflare Full-Stack Mandate?",
    "limit": 5,
    "category": "project_fact"  # Optional filter
})
# categories: user_preference, project_fact, task_outcome, heuristic, anti_pattern
```

### Durable Fact Storage
```python
# Persist with vector embedding for future semantic recall
remember_fact({
    "content": "The Cloudflare Full-Stack Mandate requires all infrastructure decisions to evaluate Workers, D1, R2, KV, DO, AI, Vectorize, Queues, Pages, DNS, WAF, CDN as ONE integrated platform.",
    "category": "heuristic",
    "importance": 1.0,
    "summary": "Cloudflare Full-Stack Mandate",
    "session_id": "session-2026-07-17"
})
```

### Structured Recall
```python
# Recall by category or keyword from D1
facts = recall_facts({
    "category": "project_fact",
    "keyword": "CFPE",
    "limit": 10
})
```

### Paper Context & Search
```python
# Get full paper body from D1 living-paper
paper = get_paper_context({
    "slug": "cfpe-forecast-stages3-5-assumption-audit",
    "limit_chars": 10000
})
# Returns: {slug, title, doi, body (full markdown), published_at, ...}

# Semantic search across QWAV papers via Vectorize
papers = search_papers({
    "query": "room temperature quantum coherence biomolecules",
    "limit": 10
})
# Returns: [{slug, title, score, snippet}, ...] ranked by meaning similarity
```

---

## Cross-System Discovery Hierarchy

When discovering "what exists," query in this order:

| Priority | System | API | Returns |
|:---------|:-------|:----|:--------|
| **1. KG (canonical topology)** | graph-api Worker (`query_graph`) | `/stats`, `/nodes`, `/neighbors`, `/impact` | What exists AND how things connect |
| **2. D1 (structured records)** | wrangler D1 exec | `portfolio-state`, `living-paper`, `qnfo-audit` | Row-level structured data |
| **3. Vectorize (semantic search)** | `search_memories`, `search_papers` | 768-dim cosine similarity | Meaning-based search across memories + papers |
| **4. R2 (file artifacts)** | wrangler R2 object get/list | `qnfo/` bucket | Canonical file storage (last resort for discovery) |
| **5. Local filesystem** | `Get-ChildItem`, `glob`, `grep` | CWD | Ephemeral cache -- verify against R2 before trusting |

**Always query KG first.** Files on disk are an incomplete, stale subset. The KG is the single source of truth for ecosystem topology.

---

## Anti-Patterns

| Anti-Pattern | Fix |
|:-------------|:----|
| Claiming "comprehensive" without KG query | KG-First Discovery Gate -- query `/stats` first |
| Trusting stale memories without cross-reference | Verify against KG + D1 (two-system confirmation) |
| Orphaned KG nodes with 0 edges | Seed BELONGS_TO edges to taxonomy (min 1 edge) |
| Searching only files on disk for "what exists" | KG is canonical; disk is secondary confirmation |
| Skipping impact analysis before modifying entity | Query `/impact/{id}` to check downstream dependents |
| Storing memory without category | Always categorize: user_preference/project_fact/task_outcome/heuristic/anti_pattern |
| Ignoring search_memories for context | Semantic search finds decisions by meaning, not keywords |
