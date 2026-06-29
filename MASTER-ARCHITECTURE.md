# QNFO CLOUDFLARE ECOSYSTEM — MASTER ARCHITECTURE v1.0
# Generated: 2026-06-28 | Auditor: QNFO Agent

## CONSOLIDATED STATE (post-cleanup)

### D1 DATABASES — 5 ESSENTIAL
| Database | ID | Size | Content | Status |
|:---------|:---|:-----|:--------|:------|
| qnfo-audit | 35e2e573 | 954KB | tasks(73), projects(78) | ESSENTIAL |
| qnfo-graph | a1954b92 | 368KB | KG(261n/401e) | ESSENTIAL — needs research edges |
| qnfo-cms | 0458a344 | 208KB | CMS(34e/5t) | ESSENTIAL — needs paper dedup |
| living-paper | 70a58cb3 | 241KB | papers(9) | ESSENTIAL — schema incomplete |
| portfolio-state | d80fdf2a | 118KB | handoffs(6), decisions(26) | ESSENTIAL |

### VECTORIZE — 3 ACTIVE (deleted 2 obsolete)
| Index | Dimensions | Vectors | Status |
|:------|:-----------|:--------|:------|
| qwav-research-v2 | 1024 | 461 | ESSENTIAL — Ask QWAV search + AI synthesis |
| qnfo-handoffs | 768 | ? | UNDERDEVELOPED — semantic handoff search |
| qnfo-tasks | 768 | ? | UNDERDEVELOPED — semantic task search |
| ~~qwav-research~~ | ~~768~~ | DELETED | ~~OBSOLETE (replaced by v2)~~ |
| ~~paper-similarity~~ | ~~1024~~ | DELETED | ~~REDUNDANT (empty duplicate)~~ |

### CLOUDFLARE PAGES — 10 remaining (deleted 1)
| Project | Domain(s) | Status |
|:--------|:----------|:------|
| qnfo-hub | hub.qnfo.org, qnfo.org, www.qnfo.org | ESSENTIAL — landing |
| qnfo-publications | papers.qnfo.org, adelic-qec.qnfo.org, benchmark.qnfo.org, p-adic-hw.qnfo.org, p-adic.qnfo.org, uqc.qnfo.org | ESSENTIAL — library |
| quantum-laws-of-form | laws.qnfo.org → 301 | ESSENTIAL — redirect |
| qnfo-legal | legal.qnfo.org | ESSENTIAL — legal |
| qwav | deep.qwav.tech | REDUNDANT — merge into papers |
| qnfo-archive | archive.qnfo.org | REDUNDANT — merge into papers |
| adelic-qft | adelic.qnfo.org | REDUNDANT — redirect to papers |
| qlof-primer | primer.qwav.tech | REDUNDANT — redirect to papers |
| qnfo-ipfs-archive | .pages.dev | UNDERDEVELOPED — IPFS archive |
| qnfo-design-system | .pages.dev | UNDERDEVELOPED — CSS/components |
| ~~qnfo-openclaw-hermes-analysis~~ | DELETED | ~~OBSOLETE~~ |

### WORKERS — 30 identified
| Category | Workers |
|:---------|:--------|
| ESSENTIAL | ask-qwav (v2.4), graph-api, cms-api, qnfo-lifecycle, qnfo-archive-worker |
| ROUTING | api-gateway (v2.2), qnfo-data-api (v2.0) — NEEDS CONSOLIDATION |
| OPERATIONAL | qnfo-archive-verify, git-on-cloudflare, annotation-store, +others |
| RESEARCH | ultrametric-tree-api (v1.0.0) |

### QUEUES — 2
| Queue | Producer | Consumer | Status |
|:------|:---------|:---------|:------|
| qnfo-lifecycle-queue | qnfo-lifecycle | qnfo-archive-worker | ESSENTIAL |
| git-on-cloudflare-repo-maint | git-on-cloudflare | git-on-cloudflare | DEPRECATED (GitHub deprecated per ADR-001) |

### KV — 2
| Namespace | Status |
|:----------|:------|
| equation-cache | KEEP — MathJax caching |
| git-on-cloudflare-routes | DEPRECATED (GitHub deprecated) |

---

## DYNAMIC REAL-TIME DATA FLOW

```
User visits papers.qnfo.org
        │
        ▼
Pages serves static shell + qnfo-cms-client.js
        │
        ├──► api-gateway.q08.workers.dev/papers/*  → ask-qwav → D1 living-paper (paper metadata)
        ├──► api-gateway.q08.workers.dev/search/*  → ask-qwav → Vectorize qwav-research-v2 (semantic search)
        ├──► api-gateway.q08.workers.dev/ask/*     → ask-qwav → AI.run(deepseek) + Vectorize context
        ├──► api-gateway.q08.workers.dev/graph/*   → graph-api → D1 qnfo-graph (citations, concepts)
        └──► api-gateway.q08.workers.dev/cms/*     → cms-api  → D1 qnfo-cms (page content)
```

---

## CONSOLIDATION EXECUTED THIS SESSION

| Action | Result |
|:-------|:-------|
| DELETE Vectorize `qwav-research` (768-dim OLD) | ✅ DONE |
| DELETE Vectorize `paper-similarity` (empty) | ✅ DONE |
| DELETE Pages `qnfo-openclaw-hermes-analysis` | ✅ DONE |
| D1 stub cleanup (449→9 papers) | ✅ DONE |
| Worker v2.3→v2.4 (stub filter, cleanup endpoint) | ✅ DONE |
| Vectorize re-seeded (12→461 vectors) | ✅ DONE |
| Skills synced to R2 (38/38) | ✅ DONE |
| D1 paper duplicates flagged (CMS has 3 stubs) | ✅ IDENTIFIED |
| D1 schema gaps documented (missing 8 fields) | ✅ IDENTIFIED |
