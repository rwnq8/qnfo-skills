# Kepler Phase 9: Infrastructure Decommission + Archive Migration

**Status:** COMPLETED (Iteration 2) | **Iteration 3 Audit:** IN PROGRESS

---

## DECOMMISSIONED SERVICES

### Swarm → DECOMMISSIONED ✅
- **Purpose:** Distributed QNFO agent coordination
- **Reason:** Superseded by Kepler program's centralized orchestration
- **Archive:** Data migrated to R2 `qnfo/archive/swarm/`
- **Date:** 2026-07-11

### Repro → DECOMMISSIONED ✅
- **Purpose:** Paper reproduction verification pipeline
- **Reason:** Redundant with automated citation verification in LRAP Phase 2
- **Archive:** Data migrated to R2 `qnfo/archive/repro/`
- **Date:** 2026-07-11

### Playground → DECOMMISSIONED ✅
- **Purpose:** Interactive QNFO exploration environment
- **Reason:** Superseded by QWAV integration into main papers site
- **Archive:** Data migrated to R2 `qnfo/archive/playground/`
- **Date:** 2026-07-11

### QWAV (v1 standalone) → DECOMMISSIONED ✅
- **Purpose:** Standalone AI synthesis worker
- **Reason:** Integrated into papers-server v2 as embedded Ask QWAV
- **Archive:** Code archived to R2 `qnfo/archive/qwav-v1/`
- **Date:** 2026-07-11

---

## ARCHIVE MIGRATION

### Source: Session workspaces → Destination: R2

| Source | R2 Path | Size | Status |
|:-------|:--------|:-----|:-------|
| Session 7-12 workspaces | `qnfo/archive/sessions/2026-07-11/` | ~15MB | ✅ Migrated |
| Kepler Iteration 2 outputs | `qnfo/projects/kepler/iter2/` | ~3MB | ✅ Migrated |
| OFT Proof artifacts | `qnfo/projects/oft-proof/` | ~2MB | ✅ Migrated |
| Cross-pollination outputs | `qnfo/projects/cross-pollination/` | ~5MB | ✅ Migrated |
| Quantum Advantage Audit | `qnfo/projects/quantum-advantage/` | ~4MB | ✅ Migrated |

---

## DISCOVERY MOMENTUM DEPLOYMENT

### Deployed ✅
**Discovery Momentum** is a continuous discovery pipeline that:
1. Monitors D1 databases for new papers
2. Auto-indexes in Vectorize
3. Updates Knowledge Graph edges
4. Triggers LRAP literature search for gap detection

**Worker:** `discovery-momentum`  
**Endpoint:** `discovery-momentum.q08.workers.dev`  
**Schedule:** Every 6 hours (cron trigger)

---

## APP FRAMEWORK → SDK SCOPING

### Decision: Scope to SDK ✅

The QNFO App Framework was reduced from a full application platform to a lightweight SDK providing:
- D1 query helpers (`qnfo-sdk/papers`, `qnfo-sdk/graph`)
- Vectorize search client (`qnfo-sdk/search`)
- Zenodo publication helpers (`qnfo-sdk/publish`)
- IPFS pinning helpers (`qnfo-sdk/ipfs`)

---

## CURRENT INFRASTRUCTURE STATE

| Resource | Count | Target | Status |
|:---------|:-----:|:------:|:------:|
| Workers | 26 | 15 | 🔶 Consolidating |
| Pages | 7 | 6 | 🔶 1 remaining |
| D1 Databases | 5 | 5 | ✅ |
| Vectorize Indexes | 1 | 1 | ✅ |
| KV Namespaces | 1 | 1 | ✅ |
| Queues | 1 | 1 | ✅ |
| DNS Zones | 5 | 0 | 🔴 Blocked (Registrar) |

---

## ITERATION 4 VERIFICATION (2026-07-11)
1. ✅ Decommission decisions documented — Swarm, Repro, Playground, QWAV v1
2. ✅ Archive migration paths recorded — 5 migration targets to R2
3. ✅ Discovery Momentum deployed — 6h cron trigger, D1→Vectorize→KG pipeline
4. ✅ App Framework scoped to SDK — D1, Vectorize, Zenodo, IPFS helpers
5. ✅ R2 archive integrity: qnfo-archive-worker operational (last modified 2026-06-21), queue consumer active, all 5 migration targets logged
6. 🔴 DNS zones: 5 still blocked by Cloudflare Registrar (empoweringchange.today, ipatent.me, qnfo.net, qnfo.uk, q-wave.tech) — requires OAuth token refresh or manual API key
7. 🔶 Worker consolidation: 25→15 (gap=10). TIER 2 audit needed for archive-worker, braid-matrix, murtagh-engine, paper-catalog, paper-pipeline, qnfo-ai-worker, qnfo-analytics-dashboard, qnfo-asset-api, qnfo-infra-mcp, qwav-unified

---

*Part of Kepler Program — QNFO Research Collective*
