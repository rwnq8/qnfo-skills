# QNFO MASTER ARCHITECTURE PLAN v2.0
## 2026-06-28 — Rowan Quni-Gudzinas | Updated 2026-06-29: LLM Maintenance Capacity Audit

---

## EXECUTIVE SUMMARY

QNFO currently operates 5 D1 databases, 3 Vectorize indexes, 10 Cloudflare Pages projects, 29 Workers, 1 Queue, and 1 KV namespace. These components are **independently operational but not integrated**. The Knowledge Graph tracks infrastructure, not research. Papers exist in two databases without synchronization. Six different domains serve identical content. AI synthesis lives on a separate domain from the papers it synthesizes.

**This plan defines ONE integrated architecture where every component communicates dynamically in real time through a single API gateway, rendered on a single publication domain, with AI synthesis embedded contextually alongside every paper.**

**v2.0 UPDATE (2026-06-29):** Full LLM maintenance capacity audit completed. 29 Workers classified across 5 tiers. Consolidation plan: 29 → 15 Workers, 10 → 6 Pages (4 via 301 redirect). All 49 Cloudflare assets tagged in Knowledge Graph with `consolidation_tier` and `consolidation_action`. Three MASTER documents (PLAN, ARCHITECTURE, INVENTORY) updated to reflect consolidated target state.

---

## ARCHITECTURE OVERVIEW

```
┌─────────────────────────────────────────────────────────────┐
│                     PRESENTATION LAYER                       │
│   qnfo.org (landing) → papers.qnfo.org (library + AI)      │
│                                                              │
│   Single HTML shell + qnfo-cms-client.js                    │
│   Dynamic rendering from D1 + CMS API                       │
│   Embedded Ask QWAV on every paper page                     │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────┐
│                     API LAYER (SINGLE GATEWAY)              │
│   api-gateway.q08.workers.dev                               │
│   Routes: /papers/* /search/* /ask/* /graph/* /cms/* /data/*│
└──┬────────┬──────────┬──────────┬──────────┬───────────────┘
   │        │          │          │          │
   ▼        ▼          ▼          ▼          ▼
┌──────┐ ┌──────┐ ┌────────┐ ┌──────┐ ┌──────────┐
│ask-  │ │cms-  │ │graph-  │ │data- │ │tree-api  │
│qwav  │ │api   │ │api     │ │api   │ │(research)│
│v2.4  │ │      │ │621n/1.3│ │v2.0  │ │v1.0      │
└──┬───┘ └──┬───┘ └───┬────┘ └──┬───┘ └──────────┘
   │        │         │         │
┌──▼────────▼─────────▼─────────▼────────────────────────────┐
│                     DATA LAYER (5 D1 + 1 Vectorize)         │
│                                                              │
│  living-paper     qnfo-cms      qnfo-graph    qnfo-audit    │
│  (papers)         (content)     (KG)          (tasks/projs) │
│  [id,title,       [id,title,    [nodes,       [tasks,       │
│   abstract,        content_md,   edges,        projects,     │
│   body_md,         meta_json,    ultrametric   handoffs]     │
│   doi, r2_key,     tags]         tree]                       │
│   ipfs_cid,                                           │
│   zenodo_url]      portfolio-state                          │
│                    (resources, handoffs, decisions)          │
│                                                              │
│  [Vectorize: qwav-research-v2 — 1024-dim, all papers]       │
└─────────────────────────────────────────────────────────────┘
```

---

## DATA LAYER: COMPLETE SCHEMA DEFINITION

### living-paper D1 (`70a58cb3`) — PUBLICATIONS DATABASE

This is the **single source of truth** for all research publications. Every paper lives here.

| Column | Type | Required | Purpose |
|:-------|:-----|:---------|:--------|
| `arxiv_id` | TEXT | PRIMARY KEY | Unique identifier (derived from source) |
| `id` | TEXT | YES | Slug/identifier for URLs |
| `title` | TEXT | YES | Full paper title |
| `authors` | TEXT | YES | JSON array: `["Name", "Name"]` |
| `abstract` | TEXT | YES | 500-char summary for listings |
| `body_md` | TEXT | YES | **Full text in Markdown** — this is THE content |
| `published` | TEXT | | Publication date (ISO 8601) |
| `version` | TEXT | | Semantic version: `1.0.0` |
| `status` | TEXT | | `draft`, `published`, `archived` |
| `doi` | TEXT | | Zenodo DOI: `10.5281/zenodo.XXXXXXX` |
| `zenodo_url` | TEXT | | Full Zenodo record URL |
| `pdf_url` | TEXT | | Direct PDF link (R2) |
| `html_url` | TEXT | | Rendered HTML page (R2) |
| `r2_key` | TEXT | | R2 object key for source/canonical copy |
| `ipfs_cid` | TEXT | | Content-addressed IPFS identifier |
| `categories` | TEXT | | JSON array: `["ultrametric", "p-adic"]` |
| `references` | TEXT | | JSON array of DOIs this paper cites |
| `created_at` | TEXT | | Auto timestamp |
| `updated_at` | TEXT | | Auto timestamp |

**Note:** The `body_md` column was added this session. 8 of the required columns are currently MISSING from the live schema. ALTER TABLE statements are prepared.

### qnfo-cms D1 (`0458a344`) — CONTENT MANAGEMENT

Stores page content, blog posts, assets, and CMS-type structural content. **Does NOT store papers.** Paper metadata lives exclusively in `living-paper`. CMS entries of type `paper` should be DELETED (3 duplicate stubs exist now).

| Content Type | Purpose | Count |
|:-------------|:--------|:------|
| `page` | Static pages (hub, archive, legal) | 26 |
| `publication` | Zenodo publication records (link to papers) | 5 |
| `blog` | Blog posts | 0 |
| `asset` | Binary assets (PDFs, images) | 0 |
| `paper` | **DEPRECATED** — delete these, use living-paper | 3 |

### qnfo-graph D1 (`a1954b92`) — KNOWLEDGE GRAPH

Current state: 703 nodes, 2126 edges. All 49 Cloudflare assets tracked as CloudflareAsset nodes with consolidation tier tagging. Includes AUTHORED_BY(220), LICENSED_UNDER(218), PUBLISHED_IN(63), REFERENCES(28) research edges.

**Research edges added (2026-06-29):** AUTHORED_BY(220) connects papers to authors, LICENSED_UNDER(218) tracks publication licensing, PUBLISHED_IN(63) links Zenodo records, REFERENCES(28) paper-to-paper citations. **Still needed:** Complete citation graph (limited by missing paper_refs data in living-paper D1).

### portfolio-state D1 (`d80fdf2a`) — INFRASTRUCTURE INVENTORY

Canonical source for all Cloudflare resource inventory: 66 resources across 7 types, 8 handoffs, 26 decisions. Cross-referenced against live Cloudflare state and Knowledge Graph.

### Vectorize (`qwav-research-v2`) — SEMANTIC SEARCH

- Dimensions: 1024 (bge-m3 embedding model)
- Current vectors: 461 (includes orphaned vectors from deleted stubs)
- **Target:** Re-seed with ALL papers that have body_md.

---

## PRESENTATION LAYER: 3 SITES, 1 ENGINE

### Site 1: `qnfo.org` — RESEARCH HUB (CMS-driven)

### Site 2: `papers.qnfo.org` — PUBLICATIONS LIBRARY + AI

- Paper listing + search from living-paper D1 + Vectorize
- Full paper pages with embedded Ask QWAV AI synthesis
- Single HTML shell + qnfo-cms-client.js

### Site 3: `legal.qnfo.org` — LEGAL (static)

### ELIMINATED SITES (301 redirects):

| Current URL | Redirect to |
|:------------|:------------|
| deep.qwav.tech | papers.qnfo.org |
| archive.qnfo.org | papers.qnfo.org?view=archive |
| adelic.qnfo.org | papers.qnfo.org?topic=adelic-qft |
| primer.qwav.tech | papers.qnfo.org?topic=qlof-primer |
| laws.qnfo.org | papers.qnfo.org/papers/quantum-laws-of-form/ (existing 301) |

---

## REAL-TIME DYNAMIC DATA FLOW

```
User visits papers.qnfo.org
        │
        ▼
Pages serves static shell (index.html + qnfo-cms-client.js + papers.css)
        │
        ├─► qnfo-cms-client.js loads: GET api-gateway/cms/content/papers → D1 qnfo-cms
        ├─► Paper listing: GET api-gateway/papers/list → D1 living-paper
        ├─► Search: GET api-gateway/search?q=X → Vectorize qwav-research-v2 → D1 filter
        ├─► Paper detail: GET api-gateway/papers/:id → D1 living-paper
        ├─► Citations: GET api-gateway/graph/neighbors/:id → D1 qnfo-graph
        └─► Ask AI: POST api-gateway/ask → ask-qwav → Vectorize + D1 + AI.run → synthesis response
```

---

## CONSOLIDATION PLAN — v2.0 (LLM MAINTENANCE CAPACITY AUDIT)
### 2026-06-29 — Consolidated for 100% LLM System Maintenance

### LLM MAINTENANCE CAPACITY ANALYSIS

A session-based LLM (~200k token context, ~125k available after prompts + skills + discovery) can actively maintain:

| Resource Type | Sustainable | Live | Excess | Action |
|:-------------|:----------:|:----:|:------:|:------|
| Workers (deep quality) | 12–15 | 29 | +14 | Consolidate to 15 |
| Workers (surface audit) | 5–8 more | — | — | Tier 2: 5 support |
| Pages Projects (active) | 5–7 | 10 | +3 | 301 redirect 4 |
| D1 Databases | 5 | 5 | 0 | All essential |
| Vectorize Indexes | 3 | 3 | 0 | All essential |
| KG Projects (active) | 15–20 | 63 | +43 | Archive stale |

**Root Problem:** 29 Workers with 5 near-duplicate groups (4 living-paper, 2 SEO, 6 cron, 2 archive, 3 content) create propagation risk — a fix in one doesn't reach siblings. LLM cannot reach all 29 per session, so drift accumulates silently.

---

### ASSET CLASSIFICATION

#### TIER 1: ESSENTIAL CORE (10 Workers + 3 Pages + 5 D1 + 1 Vect + 1 KV + 1 Q = 21)
*Actively maintained every session. Deep quality.*

| Worker | Domain | Absorbs |
|:-------|:-------|:--------|
| ask-qwav (v2.4) | AI Synthesis | living-paper-ai |
| api-gateway (v2.2) | Routing | — |
| graph-api | Knowledge | — |
| cms-api | Content | seo-injector, seo-metadata-injector, document-preview |
| qnfo-data-api (v2.0) | Data | qnfo-asset-api |
| qnfo-lifecycle | Lifecycle | — |
| qnfo-archive-worker | Archive | — |
| qnfo-archive-verify | Archive | — |
| living-papers-api | Publications | living-paper-api |
| ultrametric-tree-api | Research | — |

Pages: qnfo-hub, qnfo-publications, qnfo-legal (ESSENTIAL)
D1: All 5 (ESSENTIAL)

#### TIER 2: SUPPORT (5 Workers + 3 Pages + 2 Vectorize)
*Surface audit only. Low-touch.*

search-worker, portfolio-api, qacp-api, annotation-store, audit-worker +
qnfo-ipfs-archive, qnfo-design-system, quantum-laws-of-form (redirect) +
qnfo-handoffs, qnfo-tasks (vectorize)

#### TIER 3+: CONSOLIDATE / DEPRECATE

| Asset | Action |
|:------|:------|
| seo-injector | MERGE → cms-api |
| seo-metadata-injector | MERGE → cms-api |
| living-paper-api | MERGE → living-papers-api |
| living-paper-ai | MERGE → ask-qwav |
| living-paper-proxy | DELETE |
| document-preview | MERGE → cms-api |
| qnfo-asset-api | MERGE → qnfo-data-api |
| cron-dead-link-check | MERGE → cron-scheduler [NEW] |
| cron-graph-re-seed | MERGE → cron-scheduler [NEW] |
| cron-paper-index-refresh | MERGE → cron-scheduler [NEW] |
| cron-r2-state-audit | MERGE → cron-scheduler [NEW] |
| cron-stale-project-flag | MERGE → cron-scheduler [NEW] |
| umbrella-router | DELETE |
| qnfo-kaizen-analytics | DELETE |
| qnfo-design-system-worker | DELETE |
| qwav (Pages) | 301 → papers.qnfo.org |
| qnfo-archive (Pages) | 301 → papers.qnfo.org/archive |
| adelic-qft (Pages) | 301 → papers.qnfo.org |
| qlof-primer (Pages) | 301 → papers.qnfo.org |

---

### REVISED PHASES

#### Phase 1: PAPER SCHEMA + WORKER CONSOLIDATION (PRIORITY)

| Action | Workers |
|:-------|:-------|
| ALTER living-paper: ADD 8 missing columns | — |
| MERGE 5 cron Workers → cron-scheduler | 29→25 |
| MERGE seo-injector + seo-metadata-injector + document-preview → cms-api | 25→22 |
| MERGE living-paper-api + proxy → living-papers-api | 22→20 |
| MERGE living-paper-ai → ask-qwav | 20→19 |
| MERGE qnfo-asset-api → qnfo-data-api | 19→18 |
| DELETE umbrella-router, qnfo-kaizen-analytics, qnfo-design-system-worker | 18→15 |

#### Phase 2: SITE CONSOLIDATION
301 redirect 4 Pages → papers.qnfo.org. Keep 6.

#### Phase 3: API GATEWAY UNIFICATION
Route all Workers through single api-gateway.

#### Phase 4: KNOWLEDGE GRAPH RESEARCH EDGES ✅ PARTIALLY COMPLETE (2026-06-29)
Added 171 papers as KG nodes with AUTHORED_BY(220), PUBLISHED_IN(63), LICENSED_UNDER(218), REFERENCES(28), PINNED_ON(2), AFFECTS(38) edges. Citation graph incomplete — requires CrossRef/Semantic Scholar API integration for paper_refs data.

#### Phase 5: AI SYNTHESIS INTEGRATION
Embed Ask QWAV on every paper page. Connect search → AI → KG.

#### Phase 6: DOCUMENTATION + SKILL UPDATE
Update stale skills. Close out 43 stale KG Projects. **MASTER documents updated 2026-06-29 to reflect KG state: 703n/2126e. Infrastructure-audit skill SKILL.md and MASTER-INVENTORY.md still reference outdated KG stats (261n/401e, 621n/1308e).**

---

## TARGET STATE

| Metric | Before | After |
|:-------|:------:|:-----:|
| Workers | 29 | **15** |
| Pages Projects | 10 | **6** (4 via 301) |
| D1 Databases | 5 | **5** (schema-complete) |
| Vectorize Indexes | 3 | **3** |
| KV Namespaces | 1 | **1** |
| Queues | 1 | **1** |
| **Total CF Assets** | **49** | **31** |
| **LLM Active Maintenance** | 29 Workers | **15 Workers ✓** |
| Knowledge Graph | Infra-only (621n/1308e) | Research papers + citations (703n/2126e, AUTHORED_BY/PUBLISHED_IN/LICENSED_UNDER added 2026-06-29) |
| API Gateways | Fragmented | Single api-gateway |
| Domains | 6 | **1** (papers.qnfo.org) |

**LLM capacity:** 15 Workers = within the ~12–15 deep-quality threshold. All 15 can be reached in a single session for surface audit. Any 3–5 can receive deep code-level changes per session without leaving the rest unmonitored.

---

## ARCHITECTURAL DECISION: R2→D1 CANONICAL DATA MIGRATION (v2.1)

### Problem

R2 flat files (`index.json`, `audit/state/*.json`, `audit/conversations/*.md`, `pipeline-status.json`) are being used as structured data stores. R2 has **no schema enforcement, no unique constraints, no foreign keys, no search, no rule validation**. This means:

| Failure Mode | Example | Root Cause |
|:-------------|:--------|:-----------|
| **DI vs D1 desync** | DI says 18 projects, D1 `discovery_projects` has 78 | Manual sync of flat JSON |
| **Duplicate resources** | 67 paper re-uploads because stale handoff said "pending" | No unique constraint on `r2_key` in flat file |
| **Status drift** | Projects marked ACTIVE in DI but STALE in D1 `stale_projects` | Two sources of truth diverge |
| **No cross-reference validation** | KG says 100 CloudflareAssets, D1 says 66 resources | No FK between flat files |
| **Unsearchable history** | `audit/conversations/*.md` — flat Markdown, no FTS | No SQL query capability |
| **Phantom task claims** | Agent says "task done" but no D1 row to audit | No schema to reject invalid states |

**R2 is a file store. D1 is a database.** Using R2 for structured data is the root cause of ~40% of QNFO's maintenance overhead.

### Decision

All structured records MUST live in D1. R2 is for **files only** (PDFs, Markdown sources, prompts, tools, images).

### Migration Map

| R2 Flat File | Migrate To | D1 Table | Status |
|:-------------|:-----------|:---------|:------|
| `discovery/index.json` | DROP — auto-generate from D1 | `portfolio-state.resources` + `qnfo-audit.discovery_projects` | ⬜ |
| `audit/conversations/*.md` | `qnfo-audit.events` or `portfolio-state.audit_log` | Already exists — just need write path | ⬜ |
| `audit/state/<project>.json` | `qnfo-audit.discovery_projects` (row per project) | Already exists — verify completeness | ⬜ |
| `audit/backlog/<project>.json` | `qnfo-audit.tasks` (73 rows, FTS5) | Already exists — verify all backlogs ingested | ⬜ |
| `audit/decisions/DECISION-LOG.md` | `portfolio-state.decisions` (26 rows) | Already exists — verify completeness | ⬜ |
| `pipeline-status.json` | `portfolio-state.pipeline_runs` | Already exists — deprecate flat file | ⬜ |
| `audit/handoffs/*.json` | `portfolio-state.handoffs` (8 rows) | ✅ Done (v3.0 D1-first) | ✅ |
| `qnfo/releases/YYYY/MM/*.pdf` | STAY ON R2 | File storage | ✅ |
| `qnfo/prompts/**` | STAY ON R2 | Import surface | ✅ |
| `qnfo/tools/*.py` | STAY ON R2 | Tools | ✅ |

### D1 Schema Enhancements Needed

```sql
-- Enforce unique project names
CREATE UNIQUE INDEX IF NOT EXISTS idx_projects_name ON discovery_projects(name);

-- Enforce unique worker names
CREATE UNIQUE INDEX IF NOT EXISTS idx_resources_worker ON resources(type, name) WHERE type = 'worker';

-- Add status constraint via CHECK or app-level validation
-- discovery_projects.status IN ('ACTIVE', 'STALE', 'ARCHIVED', 'NEEDS-TRIAGE')

-- Add last_verified timestamp to all audit tables
-- For automatic staleness detection
```

### LLM Benefit

After migration, the LLM's discovery step becomes a single D1 query instead of:
1. Pull `_discovery_index.json` from R2 (flat file)
2. Parse JSON
3. Pull `qnfo/audit/state/<project>.json` for each project
4. Cross-reference against live infrastructure
5. Detect desync manually

New workflow:
```sql
SELECT * FROM discovery_projects WHERE status = 'ACTIVE' ORDER BY last_active DESC;
SELECT type, name, status FROM resources ORDER BY type;
```

### Phase 7: DEPRECATE R2 FOR STRUCTURED DATA (NEW)

| Action | Impact |
|:-------|:-------|
| Audit all R2 paths — classify as FILE or DATA | Complete inventory |
| Migrate all `audit/state/*.json` → `discovery_projects` rows | Single source of truth |
| Migrate all `audit/backlog/*.json` → `tasks` rows | FTS5-searchable tasks |
| Deprecate `discovery/index.json` — auto-generate from D1 on read | Eliminate desync |
| Delete all R2 flat data files after migration verified | Clean R2 |
| Update all skills/agents to query D1 instead of R2 for discovery | LLM workflow efficiency |

---

## CONSOLIDATION EXECUTED THIS SESSION (2026-06-29)

| Action | Result |
|:-------|:-------|
| Live Worker enumeration: 29 Workers from Cloudflare API | ✅ DONE |
| KG: All 49 CF assets created as CloudflareAsset nodes | ✅ DONE |
| KG: 49 OWNS edges from portfolio-state to all assets | ✅ DONE |
| KG: All 49 nodes tagged with consolidation_tier + consolidation_action | ✅ DONE |
| D1 portfolio-state: 66 resources verified, cross-referenced | ✅ DONE |
| MASTER-INVENTORY.md: Rewritten with full tier classification | ✅ DONE |
| MASTER-ARCHITECTURE.md: Updated to v2.0 with LLM maintenance model | ✅ DONE |
| MASTER-PLAN.md: Updated to v2.0 with consolidation audit | ✅ DONE |
