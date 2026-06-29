# QNFO MASTER ARCHITECTURE PLAN v1.0
## 2026-06-28 — Rowan Quni-Gudzinas

---

## EXECUTIVE SUMMARY

QNFO currently operates 5 D1 databases, 3 Vectorize indexes, 10 Cloudflare Pages projects, ~30 Workers, 2 Queues, and 2 KV namespaces. These components are **independently operational but not integrated**. The Knowledge Graph tracks infrastructure, not research. Papers exist in two databases without synchronization. Six different domains serve identical content. AI synthesis lives on a separate domain from the papers it synthesizes.

**This plan defines ONE integrated architecture where every component communicates dynamically in real time through a single API gateway, rendered on a single publication domain, with AI synthesis embedded contextually alongside every paper.**

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
│v2.4  │ │      │ │261n/401│ │v2.0  │ │v1.0      │
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
│                    (handoffs, decisions, sessions)           │
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

Current state: 261 nodes, 401 edges. **Problem: tracks infrastructure (OWNS 205 edges), not research (REFERENCES 1 edge).**

**Required new edges:**
- `REFERENCES` — Paper A → Paper B (citation)
- `RELATES_TO` — Paper → Concept (topic association)
- `AUTHORED_BY` — Paper → Person
- `PUBLISHED_AS` — Paper → Zenodo DOI
- `EMBEDDED_IN` — Paper → Vectorize vector

**Ultrametric taxonomy (4 domains, 12 programs) is defined in the skill but not populated in the live KG.** Need to seed concept nodes and connect papers to their research programs.

### Vectorize (`qwav-research-v2`) — SEMANTIC SEARCH

- Dimensions: 1024 (bge-m3 embedding model)
- Current vectors: 461 (includes orphaned vectors from deleted stubs)
- **Target:** Re-seed with ALL papers that have body_md. Vector ID = paper ID. Metadata: title + abstract + DOI + categories.

---

## PRESENTATION LAYER: 3 SITES, 1 ENGINE

### Site 1: `qnfo.org` — RESEARCH HUB

```
┌──────────────────────────────────────────────────┐
│  QNFO Research Platform                          │
│  [Search all papers ▸________________________]   │  ← Vectorize search
│                                                  │
│  RECENT PUBLICATIONS  (from D1, live)            │
│  ┌────────────────────────────────────────────┐  │
│  │ The Ultrametric Foundation  · DOI  · v1.0  │  │
│  │ Ultrametric QEC: p-Adic Framework          │  │
│  │ [View all papers ▸]                        │  │
│  └────────────────────────────────────────────┘  │
│                                                  │
│  RESEARCH DOMAINS                                │
│  [Ultrametric] [QEC] [p-Adic] [Dynamics] ...     │
└──────────────────────────────────────────────────┘

CMS content: data-cms-content="hub"
Living papers: data-lp-papers data-lp-limit="6"
```

### Site 2: `papers.qnfo.org` — PUBLICATIONS LIBRARY (with AI)

```
┌──────────────────────────────────────────────────┐
│  QNFO Publications         [Search ▸_______]     │
│                                                  │
│  ALL PAPERS (filterable by domain/tag)           │
│  ┌────────────────────────────────────────────┐  │
│  │ Paper Title  ·  Authors  ·  DOI  ·  v1.0   │  │
│  │ Abstract...                                 │  │
│  │ [Read full paper ▸]  [Ask AI about this ▸] │  │
│  └────────────────────────────────────────────┘  │
│                                                  │
│  PAPER PAGE (when reading):                      │
│  ┌────────────────────────────────────────────┐  │
│  │ Title · Authors · DOI · Zenodo · IPFS      │  │
│  │ Version · Published · Categories           │  │
│  │ ──────────────────────────────────────     │  │
│  │ FULL TEXT (rendered from body_md)          │  │
│  │ ...                                        │  │
│  │ ──────────────────────────────────────     │  │
│  │ ┌── AI SYNTHESIS ───────────────────────┐  │  │
│  │ │ Related papers: [A] [B] [C]           │  │  │
│  │ │ Citations: referenced by X papers     │  │  │
│  │ │ [Ask a question about this paper ▸]   │  │  │
│  │ └──────────────────────────────────────┘  │  │
│  └────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────┘

CMS content: data-cms-content="papers"
Living papers: data-lp-papers data-lp-limit="20"
Embedded Ask QWAV: on every paper page
```

### Site 3: `legal.qnfo.org` — LEGAL (static)

License text, terms of service, privacy policy. Standalone. No CMS needed.

### ELIMINATED SITES (301 redirects):

| Current URL | Redirect to |
|:------------|:------------|
| deep.qwav.tech | papers.qnfo.org (with search open) |
| archive.qnfo.org | papers.qnfo.org?view=archive |
| adelic.qnfo.org | papers.qnfo.org?topic=adelic-qft |
| adelic-qec.qnfo.org | papers.qnfo.org?topic=adelic-qec |
| benchmark.qnfo.org | papers.qnfo.org?topic=benchmark |
| p-adic.qnfo.org | papers.qnfo.org?topic=p-adic |
| p-adic-hw.qnfo.org | papers.qnfo.org?topic=p-adic-hw |
| uqc.qnfo.org | papers.qnfo.org?topic=uqc |
| primer.qwav.tech | papers.qnfo.org?topic=qlof-primer |
| laws.qnfo.org | papers.qnfo.org/papers/quantum-laws-of-form/ (keep existing 301) |

---

## REAL-TIME DYNAMIC DATA FLOW

```
User visits papers.qnfo.org
        │
        ▼
Pages serves static shell (index.html + qnfo-cms-client.js + papers.css)
        │
        ├─► qnfo-cms-client.js loads:
        │     GET api-gateway.q08.workers.dev/cms/content/papers  → D1 qnfo-cms (page layout)
        │
        ├─► data-lp-papers triggers:
        │     GET api-gateway.q08.workers.dev/papers/list?limit=20  → D1 living-paper (paper list)
        │
        ├─► Search bar:
        │     GET api-gateway.q08.workers.dev/search?q=X  → Vectorize qwav-research-v2 → D1 filter
        │
        ├─► Paper detail page:
        │     GET api-gateway.q08.workers.dev/papers/:id   → D1 living-paper (title, body_md, doi, etc.)
        │     GET api-gateway.q08.workers.dev/graph/neighbors/:id  → D1 qnfo-graph (citations, concepts)
        │
        └─► Ask AI (embedded):
              POST api-gateway.q08.workers.dev/ask  → ask-qwav Worker
                → Vectorize (find relevant papers by embedding)
                → D1 (retrieve full text)
                → AI.run(deepseek-r1-32b) (synthesize answer from context)
                → Return answer + source papers
```

---

## CONSOLIDATION PLAN

### Phase 1: COMPLETE PAPER SCHEMA (now)

| Action | Status |
|:-------|:-------|
| ADD body_md column to living-paper | ✅ DONE |
| ADD zenodo_url, pdf_url, version, status columns | 🔲 TODO — ALTER TABLE prepared |
| Re-ingest papers from R2 (454 entries, ~30% survive) | 🔄 RUNNING — 120/454, 41 OK so far |
| Delete 3 CMS paper-type duplicates | 🔲 TODO |
| Re-seed Vectorize with all papers (clean, no orphans) | 🔲 TODO — after re-ingestion completes |

### Phase 2: SITE CONSOLIDATION (30 min)

| Action | Impact |
|:-------|:-------|
| Set up 301 redirects for 10 domains → papers.qnfo.org | Single domain |
| Delete/archive unused Pages projects (adelic-qft, qlof-primer, qnfo-archive) | Clean dashboard |
| Keep: qnfo-hub, qnfo-publications, qnfo-legal | 3 sites |
| Update nav: remove self-referential links, show breadcrumbs | Coherent UX |

### Phase 3: API CONSOLIDATION (20 min)

| Action | Impact |
|:-------|:-------|
| Merge qnfo-data-api into api-gateway (both are routers) | Single gateway |
| Delete git-on-cloudflare Worker + Queue + KV (GitHub deprecated per ADR-001) | Remove dead code |
| Verify all Workers route through api-gateway | Consistent routing |

### Phase 4: KNOWLEDGE GRAPH REBUILD (30 min)

| Action | Impact |
|:-------|:-------|
| Seed paper-to-paper REFERENCES edges (from D1 references column) | KG becomes research graph |
| Seed paper-to-concept edges (from D1 categories) | Ultrametric taxonomy connected |
| Connect papers to Zenodo DOIs | Publication lineage in KG |
| Verify ultrametric triangle inequality on paper embeddings | Mathematical consistency |

### Phase 5: AI SYNTHESIS INTEGRATION (20 min)

| Action | Impact |
|:-------|:-------|
| Embed Ask QWAV on paper detail pages (not separate domain) | Contextual AI |
| Add "Ask about this paper" button per paper | One-click synthesis |
| Show KG-sourced related papers and citation counts | Research context |
| Verify search → AI → KG pipeline end-to-end | Live testing |

### Phase 6: STALE SKILL UPDATE (10 min)

| Skill | Fix |
|:------|:----|
| infrastructure-audit v1.4→1.5 | Update counts: 5 D1, 3 Vectorize, 10 Pages, 3 sites |
| knowledge-graph v2.1→2.2 | Update live state: 261n/401e, add paper edges |
| publication-publisher v1.6→1.7 | Fix Pages project name: qnfo-publications, not qwav |

---

## PAPER CORPUS STATUS

| Metric | Current | Target |
|:-------|:--------|:-------|
| Papers in D1 | 48 | 454 (all source files) |
| Papers with full text (body_md) | 41 | 454 |
| Papers with DOI | 1 | 454 |
| Papers in Vectorize | 461 (with orphans) | 454 (clean) |
| Papers in Knowledge Graph | 0 | 454 (with citations + concepts) |

**The gap:** Only ~30% of paper source files survived in R2 (thin-client deletion). The remaining ~70% must be recovered from:
1. Local Obsidian vault (primary source of the chapter content)
2. Zenodo publications (5 publication records exist in CMS)
3. Re-export from the source system

**Action required:** User must re-export paper source files to R2 (or provide access path) for full corpus recovery.

---

## KEY METRICS — BEFORE AND AFTER

| Metric | Before | After |
|:-------|:-------|:------|
| Sites with custom domains | 12 | 3 |
| Workers | 30 | ~25 (consolidated) |
| Vectorize indexes | 5 | 3 (1 active for papers) |
| D1 paper duplicates | 3 in CMS | 0 |
| KG paper connections | 0 | 454+ |
| AI synthesis domain | deep.qwav.tech | papers.qnfo.org (embedded) |
| Self-referential nav links | On every page | None |
| Page content without JS | "Loading..." | Server-rendered metadata |
| Master architecture doc | None | This document |

---

*MASTER-PLAN.md v1.0 — Single source of truth for QNFO Cloudflare architecture. All sites, Workers, databases, and data flows documented. To be updated at every infrastructure change.*
