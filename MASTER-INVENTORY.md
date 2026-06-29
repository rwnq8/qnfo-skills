# CLOUDFLARE ECOSYSTEM MASTER INVENTORY — 2026-06-28

## D1 DATABASES (5)
# 1. qnfo-audit       (35e2e573) | 954KB | tasks(73), projects(78) | ESSENTIAL
# 2. qnfo-graph       (a1954b92) | 368KB | KG(261n/401e) | ESSENTIAL
# 3. qnfo-cms         (0458a344) | 208KB | CMS(34e/5t) | ESSENTIAL
# 4. living-paper     (70a58cb3) | 241KB | papers(9) | ESSENTIAL — needs schema completion
# 5. portfolio-state  (d80fdf2a) | 118KB | handoffs(6), decisions(26) | ESSENTIAL

## VECTORIZE INDEXES (5)
# 1. qwav-research    (768-dim) | OBSOLETE — replaced by v2
# 2. qwav-research-v2 (1024-dim) | 461 vectors | ESSENTIAL — Ask QWAV uses this
# 3. paper-similarity (1024-dim) | empty, created today | REDUNDANT — merge/delete
# 4. qnfo-handoffs    (768-dim) | UNDERDEVELOPED — exists but usage unclear
# 5. qnfo-tasks       (768-dim) | UNDERDEVELOPED — exists but usage unclear

## PAGES PROJECTS (9 from wrangler)
# 1. qnfo-hub          | hub.qnfo.org, qnfo.org, www.qnfo.org | ESSENTIAL
# 2. qnfo-publications | papers.qnfo.org + 5 other domains | ESSENTIAL
# 3. quantum-laws-of-form | laws.qnfo.org (301→papers) | KEEP REDIRECT
# 4. qnfo-legal        | legal.qnfo.org | KEEP
# 5. qwav              | deep.qwav.tech | MERGE → papers.qnfo.org
# 6. qnfo-archive      | archive.qnfo.org | MERGE → papers.qnfo.org/archive
# 7. adelic-qft        | adelic.qnfo.org | REDIRECT → papers
# 8. qlof-primer       | primer.qwav.tech | REDIRECT → papers
# 9. qnfo-openclaw-hermes-analysis | .pages.dev only | DELETE (internal tool)

## WORKERS (identified so far)
# ESSENTIAL: ask-qwav, api-gateway, graph-api, qnfo-data-api
# REDUNDANT: qnfo-data-api vs api-gateway overlap
# OPERATIONAL: qnfo-lifecycle, qnfo-archive-worker, qnfo-archive-verify
# DEPRECATED: umbrella-router (DNS routing better done via Pages aliases)
# RESEARCH: ultrametric-tree-api (demo, keep)

## QUEUES (2)
# 1. qnfo-lifecycle-queue         | ESSENTIAL — project lifecycle
# 2. git-on-cloudflare-repo-maint | DEPRECATED? — GitHub deprecated per ADR-001

## KV (2)
# 1. equation-cache            | KEEP — MathJax equation caching
# 2. git-on-cloudflare-routes  | DEPRECATED — GitHub deprecated

## CONSOLIDATION PLAN

### PHASE 1: DELETE OBSOLETE/DUPLICATE (30 min)
# Delete Vectorize: qwav-research (768-dim OLD)
# Delete Vectorize: paper-similarity (empty duplicate)
# Delete Pages: qnfo-openclaw-hermes-analysis (internal tool)
# Delete KV: git-on-cloudflare-routes (GitHub deprecated)

### PHASE 2: MERGE/REDIRECT (20 min)
# 301 adelic.qnfo.org → papers.qnfo.org?topic=adelic-qft
# 301 primer.qwav.tech → papers.qnfo.org?topic=qlof-primer
# 301 deep.qwav.tech → papers.qnfo.org?search (embed Ask QWAV on papers)
# 301 archive.qnfo.org → papers.qnfo.org/archive

### PHASE 3: COMPLETE SCHEMA (15 min)
# ALTER living-paper: ADD body_md, zenodo_url, pdf_url, version, status, updated_at

### PHASE 4: BUILD MASTER ARCHITECTURE DOC (20 min)
# Single document describing the consolidated ecosystem

### RESULT: 5 D1 → 5 D1 (all essential)
###         5 Vectorize → 2 Vectorize (qwav-research-v2 + 1 handoff index)
###         9 Pages → 3 Pages (hub, papers, legal)
###         Workers → consolidate QNFO-DATA-API into API-GATEWAY
