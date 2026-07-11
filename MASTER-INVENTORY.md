# CLOUDFLARE ECOSYSTEM MASTER INVENTORY — 2026-06-29
## Consolidated for LLM Maintenance Capacity

---

## D1 DATABASES — 5 (ALL ESSENTIAL)

| Database | ID | Content | Status |
|:---------|:---|:--------|:------|
| qnfo-audit | 35e2e573 | tasks(73), projects(78) | ESSENTIAL — task/project audit |
| qnfo-graph | a1954b92 | KG(3190n/4629e) | ESSENTIAL — knowledge graph (33 node types, 57 edge types) |
| qnfo-cms | 0458a344 | CMS(34e/5t) | ESSENTIAL — content management |
| living-paper | 70a58cb3 | papers(616) | ESSENTIAL — needs schema completion |
| portfolio-state | d80fdf2a | resources(66), handoffs(8), decisions(26) | ESSENTIAL — infrastructure inventory |

---

## VECTORIZE INDEXES — 3

| Index | Dimensions | Vectors | Tier | Status |
|:------|:-----------|:--------|:-----|:------|
| qwav-research-v2 | 1024 | 461 | ESSENTIAL | Ask QWAV semantic search |
| qnfo-handoffs | 768 | ? | SUPPORT | Handoff semantic search |
| qnfo-tasks | 768 | ? | SUPPORT | Task semantic search |

---

## PAGES PROJECTS — 10 → TARGET 6

| Project | Domain(s) | Tier | Action |
|:--------|:----------|:-----|:------|
| qnfo-hub | hub.qnfo.org, qnfo.org, www.qnfo.org | ESSENTIAL | KEEP — landing |
| qnfo-publications | papers.qnfo.org + 5 topic domains | ESSENTIAL | KEEP — library |
| qnfo-legal | legal.qnfo.org | ESSENTIAL | KEEP — legal |
| quantum-laws-of-form | laws.qnfo.org → 301 | SUPPORT | KEEP_REDIRECT |
| qnfo-ipfs-archive | .pages.dev | SUPPORT | KEEP — IPFS archive |
| qnfo-design-system | .pages.dev | SUPPORT | KEEP — CSS/components |
| qwav | deep.qwav.tech | CONSOLIDATE | 301→papers.qnfo.org |
| qnfo-archive | archive.qnfo.org | CONSOLIDATE | 301→papers.qnfo.org/archive |
| adelic-qft | adelic.qnfo.org | CONSOLIDATE | 301→papers.qnfo.org |
| qlof-primer | primer.qwav.tech | CONSOLIDATE | 301→papers.qnfo.org |

---

## WORKERS — 33 → TARGET 15

### TIER 1: ESSENTIAL CORE (10 — actively maintained by LLM)

| Worker | Domain | Rationale |
|:-------|:-------|:----------|
| ask-qwav (v2.4) | AI Synthesis | Core AI pipeline — semantic search + LLM synthesis |
| api-gateway (v2.2) | Routing | Single entry point per MASTER-PLAN |
| graph-api | Knowledge | KG queries — 621n/1308e |
| cms-api | Content | Content management — CMS client depends on this |
| qnfo-data-api (v2.0) | Data | Cross-system data aggregation |
| qnfo-lifecycle | Lifecycle | Automated project lifecycle (cron daily 06:00 UTC) |
| qnfo-archive-worker | Archive | Queue consumer for R2 archival migration |
| qnfo-archive-verify | Archive | Archive verification |
| living-papers-api | Publications | Single paper API (post-merge of living-paper-api, living-paper-proxy) |
| ultrametric-tree-api | Research | Ultrametric tree computations |

### TIER 2: SUPPORT (5 — surface audit only)

| Worker | Domain |
|:-------|:-------|
| search-worker | Search |
| portfolio-api | Portfolio state |
| qacp-api | Agent protocol |
| annotation-store | Research annotations |
| audit-worker | Audit trails |

### TIER 3: CONSOLIDATE — MERGE (10 → absorbed into Tier 1)

| Worker | Merge Target | Rationale |
|:-------|:-------------|:----------|
| seo-injector | → cms-api | Near-duplicate of seo-metadata-injector |
| seo-metadata-injector | → cms-api | Near-duplicate of seo-injector |
| living-paper-api | → living-papers-api | Near-duplicate API |
| living-paper-ai | → ask-qwav | AI synthesis in ask-qwav |
| living-paper-proxy | → DELETE | Unnecessary proxy layer |
| document-preview | → cms-api | Content preview = CMS domain |
| qnfo-asset-api | → qnfo-data-api | Asset queries = data API domain |

### TIER 4: CRON — MERGE (5 → single cron-scheduler Worker)

| Worker | Merge Target |
|:-------|:-------------|
| cron-dead-link-check | → cron-scheduler |
| cron-graph-re-seed | → cron-scheduler |
| cron-paper-index-refresh | → cron-scheduler |
| cron-r2-state-audit | → cron-scheduler |
| cron-stale-project-flag | → cron-scheduler |

### TIER 5: DEPRECATE — DELETE (3)

| Worker | Rationale |
|:-------|:----------|
| umbrella-router | DNS routing via Pages aliases + redirect rules |
| qnfo-kaizen-analytics | Covered by audit-worker + qnfo-data-api |
| qnfo-design-system-worker | Design system = static Pages site, not Worker |

---

## QUEUES — 1

| Queue | Status |
|:------|:------|
| qnfo-lifecycle-queue | ESSENTIAL — consumed by qnfo-archive-worker |

---

## KV NAMESPACES — 1

| Namespace | Status |
|:----------|:------|
| equation-cache | ESSENTIAL — MathJax caching |

---

## CONSOLIDATION PROGRESS

| Resource | Before | After |
|:---------|:------:|:-----:|
| Workers | 29 | **15** (−14) |
| Pages | 10 | **6** (−4 via 301) |
| D1 | 5 | 5 |
| Vectorize | 3 | 3 |
| KV | 1 | 1 |
| Queues | 1 | 1 |
| **Total** | **49** | **31** (−18) |
| **LLM Active Maintenance** | 29 workers | **15 workers** ✓ |

### Execution Plan

1. **MERGE Workers** (create cron-scheduler, merge into cms-api/ask-qwav/living-papers-api/qnfo-data-api)
2. **DELETE** deprecated Workers (umbrella-router, qnfo-kaizen-analytics, qnfo-design-system-worker, living-paper-proxy)
3. **301 REDIRECT** Pages (qwav, qnfo-archive, adelic-qft, qlof-primer → papers.qnfo.org)
4. **COMPLETE** living-paper D1 schema (8 missing columns per MASTER-PLAN Phase 1)
5. **UPDATE** KG to reflect new state, OWNS edges updated
