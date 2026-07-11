# CLOUDFLARE ECOSYSTEM MASTER INVENTORY — 2026-07-11
## Consolidated for LLM Maintenance Capacity | Updated: 13 orphaned Pages deleted, live counts verified

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

## PAGES PROJECTS — 15 (13 orphans deleted 2026-07-11) → TARGET 6

**2026-07-11 UPDATE v2:** 13 orphaned projects deleted (no custom domains). 5 additional CONSOLIDATE targets already deleted (Pages projects + DNS records removed). Live count: 10 projects with custom domains. Target: 6 (keep 5 essential + ask-qwav).

| Project | Domain(s) | Tier | Action | Status |
|:--------|:----------|:-----|:------|:------|
| qnfo-hub | hub.qnfo.org, qnfo.org, www.qnfo.org, q08.org | ESSENTIAL | KEEP — landing | ✅ |
| qnfo-publications | papers.qnfo.org, archive.qnfo.org | ESSENTIAL | KEEP — library | ✅ |
| qnfo-legal | legal.qnfo.org | ESSENTIAL | KEEP — legal | ✅ |
| qnfo-design-system | design.qnfo.org | ESSENTIAL | KEEP — CSS/components | ✅ |
| ask-qwav | ask.qwav.tech | SUPPORT | KEEP — AI interface | ✅ |
| qwav | deep.qwav.tech, primer.qwav.tech | ACTIVE | KEEP — has active content | ⚠️ SKIP |
| hensel-code | hensel.qnfo.org | CONSOLIDATE | 301→papers.qnfo.org | ✅ DONE 2026-07-11 |
| discovery-momentum | momentum.qnfo.org | CONSOLIDATE | 301→papers.qnfo.org | ❌ DEAD DNS |
| verb-lexicon | lexicon.qnfo.org | CONSOLIDATE | 301→papers.qnfo.org | ❌ DEAD DNS |
| uqc-benchmark | uqc-benchmark.qnfo.org | CONSOLIDATE | 301→papers.qnfo.org | ❌ DEAD DNS |
| ~unity-of-ultrametric-physics~ | ~unity.qnfo.org~ | DELETED | Pages project already deleted | ✅ |
| ~ultrametric-paradigm~ | ~paradigm.qnfo.org~ | DELETED | Pages project already deleted | ✅ |
| ~ultrametric-benchmark~ | ~ultrametric-benchmark.qnfo.org~ | DELETED | Pages project already deleted | ✅ |
| ~ultrametric-ai-poc~ | ~ai-poc.qnfo.org~ | DELETED | Pages project already deleted | ✅ |
| ~two-ways-of-measuring~ | ~measure.qnfo.org~ | DELETED | Pages project already deleted | ✅ |

**Deleted 2026-07-11 (13 orphans, .pages.dev only):** oft-proof, scaffold-lab, cocyle, different-physics, analytics-dashboard, adelic-qec-synthesis, solo-scientist, yogananda-scientific-claims, ultrametric-tree-ai, ultrametric-quantum, toward-p-adic-qec, retrospective-prophecy-astrology, qwav-marquee

---

## WORKERS — 33 → TARGET 15

**2026-07-11 RECLASSIFICATION:** MASTER-INVENTORY classification was stale (many classified workers no longer exist, 21 unclassified July-burst workers). This section reclassified against live workers as of 2026-07-11.

### TIER 1: ESSENTIAL CORE (15 — actively maintained)

| Worker | Domain | Rationale |
|:-------|:-------|:----------|
| ask-qwav | AI Synthesis | Core AI pipeline — semantic search + LLM synthesis |
| graph-api | Knowledge | KG queries — 3190 nodes, 4629 edges |
| papers-server | Publications | Dynamic paper rendering (replaces static Pages deploys) |
| qnfo-lifecycle | Lifecycle | Automated project lifecycle (cron daily 06:00 UTC) |
| qnfo-archive-worker | Archive | Queue consumer for R2 archival migration |
| qnfo-agent-session | State | DO+SQLite for agent sessions, locks (kg-mutex) |
| infra-lock-manager | Deploy | DEC-034 deployment concurrency control |
| api-gateway | Routing | Single entry point per MASTER-PLAN |
| qnfo-data-api | Data | Cross-system data aggregation |
| ultrametric-tree-api | Research | Ultrametric tree computations |
| qnfo-edge-router | Routing | Edge traffic routing |
| search-worker | Search | Full-text search |
| portfolio-api | Inventory | Infrastructure inventory (D1 portfolio-state) |
| audit-worker | Audit | Audit trail storage |
| cron-graph-re-seed | Cron | KG-D1 paper reconciliation (every 15 min) |

### TIER 2: SUPPORT / RESEARCH (10 — keep with audit)

| Worker | Domain | Purpose |
|:-------|:-------|:--------|
| qnfo-ai-worker | AI | Workers AI computation |
| paper-pipeline | Pipeline | Paper processing pipeline |
| murtagh-engine | Research | Murtagh ultrametric engine |
| braid-matrix | Research | Braid co-occurrence matrix |
| conjecture-test | Research | Braided Register conjecture verification |
| qnfo-infra-mcp | Infra | Infrastructure management MCP server |
| dns-cleanup | DNS | Automated DNS scanning + cleanup (5 zones) |
| qnfo-asset-api | Assets | Asset query API |
| qnfo-analytics-dashboard | Analytics | Analytics dashboard |
| archive-worker | Archive | Archive operations (VERIFY: duplicate of qnfo-archive-worker?) |

### TIER 3: SEO/META (8 — consolidation candidates)

| Worker | Domain | Consolidation Path |
|:-------|:-------|:-------------------|
| seo-inline | SEO | Merge into qnfo-seo-proxy or papers-server |
| r2-seo-uploader | SEO | Merge into qnfo-seo-proxy |
| qnfo-seo-proxy | SEO | Become single SEO gateway (absorb seo-inline + r2-seo-uploader) |
| qnfo-meta | Meta | Metadata management |
| deep-qwav-meta | Meta | deep.qwav.tech metadata (merge into qnfo-meta?) |
| qwav-redirect | Redirect | QWAV redirect — could be Pages redirect rules |
| status-validator | Status | One-time validation — may be deletable |
| paper-catalog | Papers | Paper catalog (duplicate of papers-server /papers list) |

### TIER 4: CONSOLIDATION TARGET (merge 18 → reach ~15)

| Action | Count | Workers |
|:-------|:-----:|:--------|
| SEO worker merge | 3→1 | seo-inline, r2-seo-uploader → qnfo-seo-proxy |
| Meta worker merge | 2→1 | deep-qwav-meta → qnfo-meta |
| Paper dedup | 2→1 | paper-catalog → papers-server |
| Archive dedup | 2→1 | archive-worker → qnfo-archive-worker (verify) |
| Redirect to Pages rules | 1→0 | qwav-redirect → Pages _redirects |
| One-time workers | 2→0 | dns-cleanup, status-validator (delete after verification) |
| **Net reduction** | **12→3** | **33 → ~24, then further to ~15** |

### TIER 5: DELETED/REMOVED (historical)

| Worker | Date | Reason |
|:-------|:-----|:-------|
| cms-api | 2026-07-01 | Non-functional, returned 404 |
| umbrella-router | pre-2026-07 | DNS routing via Pages aliases |
| All TIER 4 cron workers | pre-2026-07 | Never deployed (aspirational)liases + redirect rules |
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

### 2026-07-11 UPDATE: 13 orphan Pages deleted. Workers still at 33 (18 new since June plan — reclassification needed). Full worker consolidation deferred to dedicated session.

1. **MERGE Workers** (create cron-scheduler, merge into cms-api/ask-qwav/living-papers-api/qnfo-data-api)
2. **DELETE** deprecated Workers (umbrella-router, qnfo-kaizen-analytics, qnfo-design-system-worker, living-paper-proxy)
3. **301 REDIRECT** Pages (qwav, qnfo-archive, adelic-qft, qlof-primer → papers.qnfo.org)
4. **COMPLETE** living-paper D1 schema (8 missing columns per MASTER-PLAN Phase 1)
5. **UPDATE** KG to reflect new state, OWNS edges updated
