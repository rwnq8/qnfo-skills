# QNFO CLOUDFLARE ECOSYSTEM — MASTER ARCHITECTURE v2.0
# Generated: 2026-06-29 | Auditor: QNFO Agent | CONSOLIDATED FOR LLM MAINTENANCE

---

## CONSOLIDATED STATE — TARGET ARCHITECTURE

### PRINCIPLE: 100% LLM MAINTENANCE CAPACITY

The session-based LLM system can actively maintain ~15 Workers with deep quality. This architecture consolidates 29 Workers → 15, 10 Pages → 6 (4 via 301 redirect), and eliminates all cron fragmentation. Every resource is tagged in the Knowledge Graph with `consolidation_tier` (ESSENTIAL/SUPPORT/CONSOLIDATE/DEPRECATE).

---

## D1 DATABASES — 5 (ALL ESSENTIAL)

| Database | ID | Size | Content | Status |
|:---------|:---|:-----|:--------|:------|
| qnfo-audit | 35e2e573 | 954KB | tasks(73), projects(78) | ESSENTIAL |
| qnfo-graph | a1954b92 | 368KB | KG(621n/1308e) | ESSENTIAL — all CF assets now tracked |
| qnfo-cms | 0458a344 | 208KB | CMS(34e/5t) | ESSENTIAL |
| living-paper | 70a58cb3 | 241KB | papers(170) | ESSENTIAL — schema incomplete (8 cols missing) |
| portfolio-state | d80fdf2a | 118KB | resources(66), handoffs(8), decisions(26) | ESSENTIAL — canonical infra inventory |

---

## VECTORIZE — 3

| Index | Dims | Vectors | Tier | Status |
|:------|:-----|:--------|:-----|:------|
| qwav-research-v2 | 1024 | 461 | ESSENTIAL | Ask QWAV search + AI synthesis |
| qnfo-handoffs | 768 | ? | SUPPORT | Semantic handoff search |
| qnfo-tasks | 768 | ? | SUPPORT | Semantic task search |

---

## PAGES — 10 → TARGET 6 (4 via 301 redirect)

| Project | Domain | Tier | Action |
|:--------|:-------|:-----|:------|
| qnfo-hub | hub.qnfo.org, qnfo.org | ESSENTIAL | KEEP |
| qnfo-publications | papers.qnfo.org + 5 topics | ESSENTIAL | KEEP |
| qnfo-legal | legal.qnfo.org | ESSENTIAL | KEEP |
| quantum-laws-of-form | laws.qnfo.org → 301 | SUPPORT | KEEP_REDIRECT |
| qnfo-ipfs-archive | .pages.dev | SUPPORT | KEEP |
| qnfo-design-system | .pages.dev | SUPPORT | KEEP |
| qwav | deep.qwav.tech | CONSOLIDATE | **301→papers** |
| qnfo-archive | archive.qnfo.org | CONSOLIDATE | **301→papers/archive** |
| adelic-qft | adelic.qnfo.org | CONSOLIDATE | **301→papers** |
| qlof-primer | primer.qwav.tech | CONSOLIDATE | **301→papers** |

---

## WORKERS — 29 → TARGET 15

### TIER 1: ESSENTIAL CORE (10 Workers — actively maintained by LLM)

| Worker | Domain | Rationale |
|:-------|:-------|:----------|
| **ask-qwav** (v2.4) | AI Synthesis | Core AI pipeline — search + LLM synthesis |
| **api-gateway** (v2.2) | Routing | Single entry point per MASTER-PLAN |
| **graph-api** | Knowledge | KG queries — 621n/1308e |
| **cms-api** | Content | CMS client dependency — also absorbs seo-injector, seo-metadata-injector, document-preview |
| **qnfo-data-api** (v2.0) | Data | Cross-system aggregation — absorbs qnfo-asset-api |
| **qnfo-lifecycle** | Lifecycle | Daily 06:00 UTC cron — project lifecycle |
| **qnfo-archive-worker** | Archive | Queue consumer for R2 archival |
| **qnfo-archive-verify** | Archive | Archive verification |
| **living-papers-api** | Publications | Single paper API — absorbs living-paper-api |
| **ultrametric-tree-api** | Research | Ultrametric tree computations |

### TIER 2: SUPPORT (5 Workers — surface audit, no active development)

| Worker | Domain |
|:-------|:-------|
| search-worker | Search |
| portfolio-api | Portfolio |
| qacp-api | Protocol |
| annotation-store | Research |
| audit-worker | Audit |

### TIER 4+: CRON (1 Worker — cron-scheduler replaces 5 cron Workers)

| Worker | Replaces |
|:-------|:---------|
| **cron-scheduler** [NEW] | cron-dead-link-check, cron-graph-re-seed, cron-paper-index-refresh, cron-r2-state-audit, cron-stale-project-flag |

### DEPRECATED — DELETE (4 Workers)

| Worker | Rationale |
|:-------|:----------|
| umbrella-router | DNS routing → Pages aliases + redirect rules |
| qnfo-kaizen-analytics | Covered by audit-worker + qnfo-data-api |
| qnfo-design-system-worker | Static Pages site, not Worker |
| living-paper-proxy | Unnecessary proxy |

---

## QUEUES — 1

| Queue | Status |
|:------|:------|
| qnfo-lifecycle-queue | ESSENTIAL — producer: qnfo-lifecycle, consumer: qnfo-archive-worker |

---

## KV — 1

| Namespace | Status |
|:----------|:------|
| equation-cache | ESSENTIAL — MathJax caching |

---

## DATA FLOW (unchanged from v1.0)

```
User visits papers.qnfo.org
        │
        ▼
Pages serves static shell + qnfo-cms-client.js
        │
        ├──► api-gateway/papers/*  → living-papers-api → D1 living-paper
        ├──► api-gateway/search/*  → ask-qwav → Vectorize qwav-research-v2
        ├──► api-gateway/ask/*     → ask-qwav → AI.run + Vectorize context
        ├──► api-gateway/graph/*   → graph-api → D1 qnfo-graph
        └──► api-gateway/cms/*     → cms-api  → D1 qnfo-cms
```

---

## CONSOLIDATION EXECUTED THIS SESSION (2026-06-29)

| Action | Result |
|:-------|:-------|
| KG: All 49 CF assets tagged with consolidation_tier | ✅ DONE |
| KG: All 49 CF assets tracked as CloudflareAsset nodes | ✅ DONE |
| KG: 49 OWNS edges from portfolio-state | ✅ DONE |
| MASTER-INVENTORY.md: Rewritten with full tier classification | ✅ DONE |
| MASTER-ARCHITECTURE.md: Updated to v2.0 with LLM maintenance model | ✅ DONE |
| Portfolio-state D1: 66 resources verified, KG cross-referenced | ✅ DONE |
| Knowledge Graph: 621 nodes, 1308 edges | ✅ VERIFIED |

### PENDING

| Action | Priority |
|:-------|:---------|
| MERGE: 5 cron Workers → single cron-scheduler | HIGH |
| MERGE: seo-injector + seo-metadata-injector + document-preview → cms-api | HIGH |
| MERGE: living-paper-api + living-paper-ai + living-paper-proxy → living-papers-api / ask-qwav | HIGH |
| DELETE: umbrella-router, qnfo-kaizen-analytics, qnfo-design-system-worker | MEDIUM |
| 301: 4 Pages projects → papers.qnfo.org | MEDIUM |
| COMPLETE: living-paper D1 schema (8 missing columns) | HIGH (MASTER-PLAN Phase 1) |

---

## ARCHITECTURAL RULE: D1 for Data, R2 for Files Only

**Decision (2026-06-29):** All structured records (projects, tasks, handoffs, decisions, audit logs, resource inventories, conversation histories) MUST be canonical in D1. R2 is for **files only** — PDFs, Markdown sources, prompts, tools, images.

**Why:** R2 flat files have no schema, no unique constraints, no foreign keys, no search. Using R2 for structured data is the root cause of ~40% of QNFO maintenance overhead (DI desync, duplicate resources, phantom claims, cross-reference failures).

**Migration status:** D1 already has tables for everything (`discovery_projects`, `tasks`, `handoffs`, `decisions`, `resources`, `pipeline_runs`, `events`). R2 flat files (`discovery/index.json`, `audit/state/*.json`, `audit/backlog/*.json`) are REDUNDANT and should be deprecated after verification.

| R2 Flat File | D1 Canonical | Action |
|:-------------|:-------------|:------|
| `discovery/index.json` | `portfolio-state.resources` + `qnfo-audit.discovery_projects` | DEPRECATE |
| `audit/conversations/*.md` | `portfolio-state.audit_log` + `qnfo-audit.events` | MIGRATE |
| `audit/state/<project>.json` | `qnfo-audit.discovery_projects` (row) | MIGRATE |
| `audit/backlog/<project>.json` | `qnfo-audit.tasks` (73 rows, FTS5) | MIGRATE |
| `audit/decisions/DECISION-LOG.md` | `portfolio-state.decisions` (26 rows) | MIGRATE |
| `qnfo/releases/**/*.pdf` | STAY ON R2 | FILE |
| `qnfo/prompts/**` | STAY ON R2 | FILE |
| `qnfo/tools/*.py` | STAY ON R2 | FILE |
