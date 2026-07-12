# QNFO CLOUDFLARE ECOSYSTEM MASTER INVENTORY — 2026-07-12 (Session: Architecture Reset + Patents)
## Workers: 23 (new: ipatent-api) | Pages: 13 (new: ipatent-me) | D1: 5 | Vectorize: 3 | Papers: 616 | KG: 3277n/4705e

**⚠️ ARCHITECTURE RESET:** This inventory is SECONDARY to `UNIFIED-ARCHITECTURE.md` (canonical publication pipeline). This document tracks live state only.

---

## D1 DATABASES — 5 (ALL ESSENTIAL)

| Database | ID | Content | Size | Status |
|:---------|:---|:--------|:-----|:------|
| qnfo-audit | 35e2e573 | tasks(73), projects(78) | ~954KB | ESSENTIAL |
| qnfo-graph | a1954b92 | KG(3277n/4705e) | ~368KB | ESSENTIAL |
| qnfo-cms | 0458a344 | CMS(34e/5t) | ~208KB | ESSENTIAL |
| living-paper | 70a58cb3 | papers(616) — **SINGLE SOURCE OF TRUTH** | ~241KB | ESSENTIAL |
| portfolio-state | d80fdf2a | resources(66), handoffs(8), decisions(26) | ~118KB | ESSENTIAL |

---

## VECTORIZE — 3

| Index | Dims | Vectors | Metric | Status |
|:------|:-----|:--------|:--------|:------|
| qwav-research-v2 | 1024 | ~461 | cosine | ESSENTIAL — **needs re-seed: 616 papers target** |
| qnfo-handoffs | 768 | ? | cosine | SUPPORT |
| qnfo-tasks | 768 | ? | cosine | SUPPORT |

---

## WORKERS — 22 (Live 2026-07-12)

### TIER 1: ESSENTIAL (14 Workers)

| Worker | Purpose | Key Binding |
|:-------|:--------|:------------|
| **papers-server** (v3.3) | Paper rendering + SEO + self-healing R2 cache | D1 living-paper + R2 qnfo |
| ask-qwav | AI pipeline — semantic search + LLM synthesis | Vectorize + Workers AI |
| graph-api | Knowledge Graph queries (3277n/4705e) | D1 qnfo-graph |
| api-gateway | Single API entry point | All workers |
| qnfo-data-api | Cross-system data aggregation | All D1 |
| qnfo-lifecycle | Daily cron — project lifecycle | D1 qnfo-audit + Queue |
| paper-pipeline | Paper processing + Vectorize sync (cron daily) | D1 + Vectorize |
| qnfo-edge-router | Domain routing (papers.qnfo.org → papers-server) | Service bindings |
| cron-graph-re-seed | KG ↔ D1 reconciliation (every 15 min) | D1 qnfo-graph + D1 living-paper |
| qnfo-agent-session | DO+SQLite agent sessions + locks | Durable Objects |
| infra-lock-manager | DEC-034 deployment concurrency control | Durable Objects |
| search-worker | Full-text search | D1 |
| portfolio-api | Infrastructure inventory | D1 portfolio-state |
| audit-worker | Audit trail storage | R2 + D1 |
| ultrametric-tree-api | Ultrametric tree computations | D1 qnfo-graph |

### TIER 2: SUPPORT (7 Workers)

| Worker | Purpose |
|:-------|:--------|
| archive-worker | R2 archival queue consumer |
| braid-matrix | Braid matrix research |
| murtagh-engine | Murtagh research engine |
| paper-catalog | DO: D1→KG paper sync |
| qnfo-ai-worker | AI assistance |
| qnfo-asset-api | Asset management |
| qwav-unified | deep.qwav.tech hostname-based routing |

---

## PAGES — 10

| Project | Domain | Status |
|:--------|:-------|:------|
| qnfo-hub | hub.qnfo.org, qnfo.org | ✅ ESSENTIAL |
| qnfo-publications | papers.qnfo.org (→ Worker) | ✅ ESSENTIAL |
| qnfo-legal | legal.qnfo.org | ✅ ESSENTIAL |
| qnfo-design-system | design.qnfo.org | ✅ SUPPORT |
| ask-qwav | ask.qwav.tech | ✅ SUPPORT |
| qwav | deep.qwav.tech | ⚠️ ACTIVE |
| hensel-code | hensel.qnfo.org (301→papers) | ⚠️ ACTIVE |
| qnfo-ipfs-archive | .pages.dev | ⚠️ SUPPORT |
| ultrametric-benchmark | .pages.dev | ❌ DELETE (Session 9-10) |
| ultrametric-paradigm | .pages.dev | ❌ DELETE (Session 9-10) |
| unity-of-ultrametric-physics | .pages.dev | ❌ DELETE (Session 9-10) |

---

## KNOWLEDGE GRAPH (Live 2026-07-12)

| Metric | Value |
|:-------|:------|
| Total Nodes | 3277 |
| Total Edges | 4705 |
| Paper nodes | 1830 |
| ZenodoRecord nodes | 598 |
| CloudflareAsset nodes | 178 |
| Project nodes | 115 |
| Skill nodes | 56 |
| Concept nodes | 47 (ultrametric taxonomy) |

**⚠️ DRIFT:** KG has 1830 Paper nodes vs D1 living-paper 616 papers. Many stale/duplicate Paper nodes.

---

## QUEUES — 1

| Queue | Status |
|:------|:------|
| qnfo-lifecycle-queue | ESSENTIAL — producer: qnfo-lifecycle, consumer: archive-worker |

---

## R2 — CANONICAL FILE STORE

| Path | Content | Status |
|:-----|:--------|:------|
| `qnfo/papers/{slug}/paper.md` | Paper Markdown (v3.3 self-healing) | ⚠️ Populating on-demand |
| `qnfo/releases/{YYYY}/{MM}/{slug}/` | Legacy paper files | ⚠️ Deprecated — use qnfo/papers/ |
| `qnfo/prompts/skills/{name}/` | Skill definitions | ✅ Active |
| `qnfo/tools/{name}.py` | Utility scripts | ✅ Active |
| `qnfo/audit/{type}/` | Audit artifacts | ✅ Active |
| `research/{project}/` | Research chapter files | ✅ Active |

---

## CANONICAL DOCUMENTS

| Document | Purpose | Version |
|:---------|:--------|:--------|
| **UNIFIED-ARCHITECTURE.md** | Canonical publication pipeline + storage rules | v3.0 (2026-07-12) |
| MASTER-PLAN.md | Strategic consolidation plan | v2.0 (2026-06-29) ⚠️ OUTDATED |
| MASTER-ARCHITECTURE.md | Infrastructure architecture | v2.0 (2026-06-29) ⚠️ OUTDATED |
| MASTER-INVENTORY.md (this file) | Live resource inventory | 2026-07-12 ✅ CURRENT |

---

## CURRENT STATE SUMMARY

### Recovered (2026-07-12)
- ✅ papers-server v3.3 self-healing: all 616 papers serve content (0 stubs)
- ✅ papers.qnfo.org production: all pages working
- ✅ Sitemap: 617 URLs, 104KB
- ✅ llms.txt: 616 entries
- ✅ Cache-Control headers on all pages

### Pending
- 🔴 Vectorize: re-seed all 616 papers (currently ~461)
- 🔴 ADMIN_TOKEN: set on papers-server
- 🔴 D1 columns: r2_key, pdf_url, version, status, categories, ipfs_cid missing
- 🔴 KG cleanup: 1830 Paper nodes vs 616 D1 papers
- 🟡 Worker consolidation: 22 → 15 per MASTER-PLAN
- 🟡 Pages cleanup: delete 3 orphan projects
- 🟡 body_md recovery: ~224 papers lost full-text permanently

---

*MASTER-INVENTORY v2026-07-12-architecture-reset — Live state audit. See UNIFIED-ARCHITECTURE.md for canonical rules.*


## IPATENT.ME — NEW (2026-07-12)

| Component | Detail |
|:----------|:-------|
| Pages Project | ipatent-me (ipatent-me.pages.dev) |
| Worker | ipatent-api (API routes: ipatent.me/api/*) |
| Custom Domain | ipatent.me (pending SSL) |
| D1 Tables | ipatent_submissions, ipatent_analytics (in qnfo-audit) |
| Purpose | US Provisional Patent Disclosure generator with analytics |

## DNS FIX — ZOMBIE DOMAINS WIRED (2026-07-12)

| Domain | CNAME Target | Status |
|:-------|:-------------|:------|
| unity.qnfo.org | unity-of-ultrametric-physics.pages.dev | 301 redirect |
| paradigm.qnfo.org | ultrametric-paradigm.pages.dev | 301 redirect |
| ultrametric-benchmark.qnfo.org | ultrametric-benchmark.pages.dev | 200 redirect page |
| ai-poc.qnfo.org | ultrametric-ai-poc.pages.dev | 301 redirect |
| measure.qnfo.org | two-ways-of-measuring.pages.dev | 301 redirect |
| ipatent.me | ipatent-me.pages.dev | PENDING SSL |

17/17 domains verified. 0 orphan domains remaining.

