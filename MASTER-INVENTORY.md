# QNFO CLOUDFLARE ECOSYSTEM MASTER INVENTORY — 2026-07-12 (Session 14 Update)
## Consolidated for LLM Maintenance Capacity | Workers: 33→28→26→25→24, Archive: merged+queue, SEO: Worker-backed

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

## WORKERS — 24 (was 33; 5 deleted Session 11, 2 deleted Session 12, 2 merged→1 Session 13, 1 deleted Session 14)

### TIER 1: ESSENTIAL CORE (14)

| Worker | Purpose |
|:-------|:--------|
| ask-qwav | AI pipeline — semantic search + LLM synthesis |
| graph-api | Knowledge Graph queries (3200n/4634e) |
| papers-server | Dynamic paper rendering + SEO (v2.1, R2-backed) |
| qnfo-lifecycle | Automated project lifecycle (cron daily) |
| archive-worker | **MERGED v2.0** — HTML pages + queue consumer (R2 archival), QNFO_BUCKET binding |
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

### TIER 2: SUPPORT / RESEARCH (8)

| Worker | Purpose |
|:-------|:--------|
| qnfo-ai-worker | AI assistance |
| paper-pipeline | Paper processing + vectorize sync (cron daily, should be TIER 1) |
| murtagh-engine | Murtagh research engine |
| braid-matrix | Braid matrix research |
| qnfo-infra-mcp | Infrastructure MCP stub (low value, candidate for deletion) |
| qnfo-asset-api | Asset management |
| qnfo-analytics-dashboard | Analytics dashboard (low value, consider Pages static) |
| **paper-catalog** | **DO: D1→KG paper sync** |

### TIER 3: MERGED/DELETED (0 remaining)

| Worker | Purpose | Action |
|:-------|:--------|:------|
| ~~deep-qwav-meta~~ | deep.qwav.tech SEO+OG proxy | MERGED into qwav-unified → DELETED |
| ~~qwav-redirect~~ | 301→deep.qwav.tech | MERGED into qwav-unified → DELETED |
| **qwav-unified** | Hostname-based routing: meta injection + redirect | **NEW (Session 13)** — handles both qwav domains |

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

### Session 13 Merges/Deletions
| deep-qwav-meta | Merged into qwav-unified — deleted |
| qwav-redirect | Merged into qwav-unified — deleted |
| r2-binding-test | Session 13 test Worker — deleted after verification |

### Session 14 Merge/Deletion
| qnfo-archive-worker | Merged queue consumer into archive-worker v2.0 — deleted |
| archive-worker | **UPGRADED to v2.0** — now serves archive.qnfo.org HTML + qnfo-lifecycle-queue consumer + QNFO_BUCKET R2 binding |

---

## SEO STATUS (papers.qnfo.org) — ✅ WORKER-BACKED (v2.2)

| Endpoint | Status | Content |
|:---------|:------|:--------|
| /sitemap.xml | 200 | 617 URLs (616 papers + index), 122KB, R2-backed via Worker |
| /llms.txt | 200 | 616 paper entries with titles/DOIs/abstracts, 160KB, R2-backed |
| /robots.txt | 200 | Standard + Sitemap directive |

**Served by:** papers-server v2.2 Worker via Worker routes (not Pages static files)
**R2 path:** `seo/sitemap.xml` and `seo/llms.txt` (bucket: qnfo)
**Note:** Session 12 used Pages static files. Session 13 migrated to Worker-backed serving after fixing R2 key paths.

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

| Resource | Session 9 | Session 11 | Session 12 | Session 13 | Session 14 | Target |
|:---------|:---------:|:----------:|:----------:|:----------:|:----------:|:------:|
| Workers | 33 | 28 | 26 | 25 | **24** (−9) | 15 |
| Pages | 10 | 7 | 7 | 7 | 7 | 6 |
| D1 | 5 | 5 | 5 | 5 | 5 | 5 |
| Vectorize | 3 | 3 | 3 | 3 | 3 | 3 |

---

## REMAINING TASKS

| Task | Notes |
|:-----|:------|
| Transfer 5 domains away from Registrar | Manual Dashboard action. Zones blocked by Cloudflare Registrar (clientTransferProhibited). **ipatent.me expires 2026-07-28 (16 days!)** |
| Disable workers_dev on papers-server | Requires Dashboard (API token lacks subdomain permission). Low risk. |
| Consider delete qnfo-infra-mcp | Stub MCP server — no bindings, no routes, minimal value |
| Consider migrate qnfo-analytics-dashboard to Pages | Simple HTML dashboard with /api/stats — could be static |
| Reclassify paper-pipeline as TIER 1 | Has cron trigger + critical D1/R2/Vectorize bindings |
| Complete MASTER-PLAN Phase 1 | living-paper schema completion, Pages→Worker migration |
