# QNFO CLOUDFLARE ECOSYSTEM MASTER INVENTORY — 2026-07-12 (Session: H-1→H-5 + IPATENT Complete)
## QNFO: 23 Workers | 7 Pages | 5 D1 | 3 Vectorize | 616 Papers | KG: 3277n/4705e (Paper: 600, drift:16)
## IPATENT (SEPARATE PROGRAM): 1 Worker | 1 Pages | 1 D1 | 1 Vectorize (4 vectors) — DO NOT COMMINGLE

**⚠️ MULTI-PROGRAM:** QNFO/QWAV and IPATENT share the Cloudflare Quniverse account but are ARCHITECTURALLY ISOLATED. QNFO scripts/skills must NEVER access ipatent resources. See FULL-STACK-INTEGRATION.md for program boundary rules.

**🗑 DEPRECATION NOTICE (2026-07-12):** Discovery Index (`qnfo/discovery/index.json` on R2) is FULLY DEPRECATED. All structured data (projects, resources, publications, skills) lives exclusively in D1 (qnfo-audit, portfolio-state, living-paper). R2 is for file artifacts only. The local `discovery/index.json` has been deleted. See this session's Discovery Index deprecation audit for full rationale.

---

## D1 DATABASES — 6 (5 QNFO + 1 IPATENT)

### QNFO/QWAV (5 — ESSENTIAL)

| Database | ID | Content | Size | Status |
|:---------|:---|:--------|:-----|:------|
| qnfo-audit | 35e2e573 | tasks(73), projects(78) | ~954KB | ESSENTIAL |
| qnfo-graph | a1954b92 | KG(3277n/4705e) | ~368KB | ESSENTIAL |
| qnfo-cms | 0458a344 | CMS(34e/5t) | ~208KB | ESSENTIAL |
| living-paper | 70a58cb3 | papers(616) — **SINGLE SOURCE OF TRUTH** | ~241KB | ESSENTIAL |
| portfolio-state | d80fdf2a | resources(66), handoffs(8), decisions(26) | ~118KB | ESSENTIAL |

### IPATENT (1 — SEPARATE PROGRAM — DO NOT COMMINGLE)

| Database | ID | Content | Status |
|:---------|:---|:--------|:------|
| ipatent-db | 19cc87d6 | Patent analysis data | 🟡 SEPARATE PROGRAM |

---

## VECTORIZE — 3

| Index | Dims | Vectors | Metric | Status |
|:------|:-----|:--------|:--------|:------|
| qwav-research-v2 | 1024 | **839** | cosine | ✅ RE-SEEDED — all 616 papers (2026-07-12) |
| qnfo-handoffs | 768 | ? | cosine | SUPPORT |
| qnfo-tasks | 768 | ? | cosine | SUPPORT |

---

## WORKERS — 22 (Live 2026-07-12)

### TIER 1: ESSENTIAL (14 Workers)

| Worker | Purpose | Key Binding |
|:-------|:--------|:------------|
| **papers-server** (v3.4) | Paper rendering + SEO + self-healing R2 cache | D1 living-paper + R2 qnfo |
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

### TIER 2: QNFO SUPPORT (7 Workers)

| Worker | Purpose |
|:-------|:--------|
| archive-worker | R2 archival queue consumer |
| braid-matrix | Braid matrix research |
| murtagh-engine | Murtagh research engine |
| paper-catalog | DO: D1→KG paper sync |
| qnfo-ai-worker | AI assistance |
| qnfo-asset-api | Asset management |
| qwav-unified | deep.qwav.tech hostname-based routing |

### IPATENT (1 — SEPARATE PROGRAM — DO NOT COMMINGLE)

| Worker | Purpose |
|:-------|:--------|
| ipatent-api | Patent analysis API (SEPARATE PROGRAM) |

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
| ~~ultrametric-benchmark~~ | ~~.pages.dev~~ | ~~🗑 DELETED~~ |
| ~~ultrametric-paradigm~~ | ~~.pages.dev~~ | ~~🗑 DELETED~~ |
| ~~unity-of-ultrametric-physics~~ | ~~.pages.dev~~ | ~~🗑 DELETED~~ |

---

## KNOWLEDGE GRAPH (Live 2026-07-12)

| Metric | Value |
|:-------|:------|
| Total Nodes | 3277 |
| Total Edges | 4705 |
| Paper nodes | **600** (was 1830, cleaned 1230 orphans) |
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

### Recovered + Completed (2026-07-12)
- ✅ papers-server v3.4 self-healing: all 616 papers serve content (0 stubs)
- ✅ papers.qnfo.org production: all pages working
- ✅ Sitemap: 616+ URLs, 104KB
- ✅ llms.txt: 616 entries
- ✅ **ADMIN_TOKEN set** on papers-server (admin endpoints secured with 401 enforcement)
- ✅ **Vectorize re-seeded**: 839 vectors covering all 616 papers (was 222)
- ✅ **KG cleaned**: 1230 orphan Paper nodes deleted, 600→616 (drift:16)
- ✅ **3 orphan Pages deleted**: ultrametric-benchmark, ultrametric-paradigm, unity-of-ultrametric-physics
- ✅ **IPATENT Vectorize**: 4/4 submissions indexed in ipatent-disclosures
- ✅ **IPATENT SSL**: Domain re-added with certificate_authority = google (free tier limit, can't change)

### Remaining (Deferred)
- 🟡 KG: seed 16 missing papers into KG
- 🟡 Worker consolidation: 22→15 per MASTER-PLAN (Phase 1)
- 🟡 IPATENT route scoping: zone_name empty → should be "ipatent.me"
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

