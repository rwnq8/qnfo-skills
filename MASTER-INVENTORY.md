# QNFO CLOUDFLARE ECOSYSTEM MASTER INVENTORY — 2026-07-11 (Session 12 Update)
## Consolidated for LLM Maintenance Capacity | Workers: 33→28→26, SEO verified, Red-Team audited

---

## D1 DATABASES — 5 (ALL ESSENTIAL)

| Database | ID | Content | Status |
|:---------|:---|:--------|:------|
| qnfo-audit | 35e2e573 | tasks(73), projects(78) | ESSENTIAL |
| qnfo-graph | a1954b92 | KG(3200n/4634e) | ESSENTIAL |
| qnfo-cms | 0458a344 | CMS(34e/5t) | ESSENTIAL |
| living-paper | 70a58cb3 | papers(616) | ESSENTIAL |
| portfolio-state | d80fdf2a | resources(66), handoffs(8), decisions(26) | ESSENTIAL |

---

## VECTORIZE INDEXES — 3

| Index | Dimensions | Vectors | Status |
|:------|:-----------|:--------|:------|
| qwav-research-v2 | 1024 | 461 | ESSENTIAL |
| qnfo-handoffs | 768 | ? | SUPPORT |
| qnfo-tasks | 768 | ? | SUPPORT |

---

## PAGES PROJECTS — 7 (with custom domains) + ask-qwav

| Project | Domain(s) | Status |
|:--------|:----------|:------|
| qnfo-hub | hub.qnfo.org, qnfo.org, www.qnfo.org, q08.org | ✅ ESSENTIAL |
| qnfo-publications | papers.qnfo.org, archive.qnfo.org | ✅ ESSENTIAL |
| qnfo-legal | legal.qnfo.org | ✅ ESSENTIAL |
| qnfo-design-system | design.qnfo.org | ✅ ESSENTIAL |
| ask-qwav | ask.qwav.tech | ✅ SUPPORT |
| qwav | deep.qwav.tech, primer.qwav.tech | ⚠️ ACTIVE |
| hensel-code | hensel.qnfo.org | ✅ 301→papers |

**Deleted (Sessions 9-10):** discovery-momentum, verb-lexicon, uqc-benchmark, unity-of-ultrametric-physics, ultrametric-paradigm, ultrametric-benchmark, ultrametric-ai-poc, two-ways-of-measuring + 13 orphans

---

## WORKERS — 26 (was 33; 5 deleted Session 11, 2 deleted Session 12)

### TIER 1: ESSENTIAL CORE (15)

| Worker | Purpose |
|:-------|:--------|
| ask-qwav | AI pipeline — semantic search + LLM synthesis |
| graph-api | Knowledge Graph queries (3200n/4634e) |
| papers-server | Dynamic paper rendering + SEO (v2.1, R2-backed) |
| qnfo-lifecycle | Automated project lifecycle (cron daily) |
| qnfo-archive-worker | Queue consumer for R2 archival migration |
| qnfo-agent-session | DO+SQLite agent sessions + locks (kg-mutex) |
| infra-lock-manager | DEC-034 deployment concurrency control |
| api-gateway | Single entry point (MASTER-PLAN) |
| qnfo-data-api | Cross-system data aggregation |
| ultrametric-tree-api | Ultrametric tree computations |
| qnfo-edge-router | Edge traffic routing |
| search-worker | Full-text search |
| portfolio-api | Infrastructure inventory (D1 portfolio-state) |
| audit-worker | Audit trail storage |
| cron-graph-re-seed | KG-D1 paper reconciliation (every 15 min) |

### TIER 2: SUPPORT / RESEARCH (11)

| Worker | Purpose |
|:-------|:--------|
| qnfo-ai-worker | AI assistance |
| paper-pipeline | Paper processing pipeline |
| murtagh-engine | Murtagh research engine |
| braid-matrix | Braid matrix research |
| conjecture-test | Conjecture testing |
| qnfo-infra-mcp | Infrastructure MCP server |
| dns-cleanup | DNS cleanup utility |
| qnfo-asset-api | Asset management |
| qnfo-analytics-dashboard | Analytics dashboard |
| archive-worker | Archive worker |
| **paper-catalog** | **RECLASSIFIED: D1→KG paper sync DO** |

### TIER 3: REMAINING META/SEO (2)

| Worker | Purpose | Action |
|:-------|:--------|:------|
| deep-qwav-meta | deep.qwav.tech SEO+OG proxy | KEEP (active domain) |
| qwav-redirect | 301→deep.qwav.tech | KEEP (needs route check) |

---

## DELETED WORKERS (Session 11)

| Worker | Reason |
|:-------|:------|
| r2-seo-uploader | One-off R2 upload utility — replaced by local script |
| status-validator | One-off audit enforcement — executed |
| seo-inline | Hardcoded SEO for hub/hensel — redundant |
| qnfo-meta | JSON-LD injector — can be baked into Pages |
| qnfo-seo-proxy | R2 SEO proxy — papers-server handles SEO now |

### Session 12 Deletions
| dns-cleanup | One-off DNS cleanup utility — 0 traffic |
| conjecture-test | Test worker — 0 traffic |

---

## SEO STATUS (papers.qnfo.org) — ✅ VERIFIED

| Endpoint | Status | Content |
|:---------|:------|:--------|
| /sitemap.xml | 200 | 617 URLs (616 papers + index) |
| /llms.txt | 200 | 616 paper entries with titles/DOIs/abstracts |
| /robots.txt | 200 | Standard + Sitemap directive |

Files generated from D1 living-paper (616 papers), stored in R2 at `qnfo/seo/`.

---

## QUEUES — 1

| Queue | Status |
|:------|:------|
| qnfo-lifecycle-queue | ESSENTIAL |

## KV — 1

| Namespace | Status |
|:----------|:------|
| equation-cache | ESSENTIAL |

---

## CONSOLIDATION PROGRESS

| Resource | Session 9 | Session 11 | Target |
|:---------|:---------:|:----------:|:------:|
| Workers | 33 | 28 | **26** (−7) | 15 |
| Pages | 10 | 7 | 6 |
| D1 | 5 | 5 | 5 |
| Vectorize | 3 | 3 | 3 |

---

## REMAINING TASKS

| Task | Notes |
|:-----|:------|
| Delete 5 empty DNS zones | OAuth token expired — need refresh or API key. Zones: empoweringchange.today, ipatent.me, qnfo.net, qnfo.uk, q-wave.tech |
| Consolidate TIER 2 workers | 11 support/research workers — need individual audit |
| Merge deep-qwav-meta + qwav-redirect | 2 remaining TIER 3 workers |
| Complete MASTER-PLAN Phase 1 | living-paper schema completion, Pages→Worker migration |
| API key refresh | OAuth token expired 2026-07-09; wrangler manages auto-refresh for deploys but not API calls |
