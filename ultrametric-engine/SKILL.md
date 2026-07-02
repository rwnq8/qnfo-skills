---
name: ultrametric-engine
description: Deploy 20 mathematical principles (ultrametric distance, p-adic valuation, Ostrowski's theorem, Hensel's lemma, Mahler compression, Berkovich spaces, Tate/Amice spectral analysis, Hasse local-global, Witt vectors, Bruhat-Tits buildings, p-adic caching, intrinsic Amice transform) as a production Cloudflare discovery engine. Use when building ultrametric tree-based search, p-adic ranked paper corpora, hierarchical dendrogram visualizations, or multi-endpoint Workers with R2/D1/Pages/Vectorize bindings.
---


---

# ULTRAMETRIC ENGINE SKILL — v1.0

## Purpose

Deploy a complete ultrametric discovery engine on Cloudflare Workers. This skill covers the full 20-principle stack proven in the Ask QWAV production system: ultrametric tree construction, p-adic ranking, 3-phase search, dendrogram visualization, and 27+ API endpoints across 6 Cloudflare properties.

## When to Use

| Trigger | Action |
|:---
---

-----|:-------|
| "Build an ultrametric search engine" | Full deployment workflow |
| "Add p-adic ranking to my paper corpus" | Principles 1-8 focused deployment |
| "Deploy a hierarchical discovery system" | Use the 3-phase engine pattern |
| "Visualize a corpus as a dendrogram" | Pages + D3.js pattern |

## Deployment Architecture

```
Worker (27+ endpoints)
├── /did-you-mean        — 3-phase discovery (word → cluster → tree)
├── /ultrametric-tree    — 451-leaf dendrogram stats
├── /spectral-analysis   — Tate + Amice + Intrinsic Amice
├── /validate + /multi   — Hasse local-global
├── /paper-versions      — Witt vectors
├── /perceptron          — p-adic neuron
├── /dendrogram-json     — D3 tree data
├── /berkovich-explorer  — Berkovich spaces
├── /bruhat-tits         — Bruhat-Tits building
├── /stats               — pAdicTimeClusters
├── /stats/csv           — export
└── /buffer-schedule     — social scheduling
R2: tree.json, title-index.json, email-digest.json
D1: papers, paper_clusters, paper_versions
Pages: 🌳 Tree + 🌲 Dendrogram tabs
```

## Quick Start

```bash
# 1. Clone the reference implementation
git clone https://github.com/rwnq8/ask-qwav.git
cd ask-qwav/worker

# 2. Deploy
npx wrangler deploy worker.js --config wrangler.toml

# 3. Verify
curl https://<worker>.workers.dev/health
curl https://<worker>.workers.dev/ultrametric-tree
curl "https://<worker>.workers.dev/did-you-mean?q=quantm"
```

## Core Patterns

### 3-Phase Discovery Engine
```javascript
// Phase 1: Word-level Levenshtein (direct matches)
// Phase 2: Ultrametric cluster expansion (structural neighbors)
// Phase 3: Tree-based search (strong-triangle pruning)
function suggestCorrections(query, titles, maxResults=5, maxDistance=5) {
  // 1. Word matches
  const wordMatches = findWordMatches(query, titles, maxDistance);
  // 2. Cluster expansion — find ultrametrically related papers
  const clusterNeighbors = expandClusters(wordMatches, ultrametricTree);
  // 3. Tree fallback
  const treeResults = searchUltrametricTree(query, ultrametricTree, maxDistance);
  // Merge and return
}
```

### Ultrametric Tree Builder (Single-Linkage)
```javascript
function buildUltrametricTree(titles) {
  // Agglomerative single-linkage (only linkage guaranteeing ultrametricity)
  // O(n³) ≈ 15M ops for n=451 — acceptable for Worker (2-3s)
  // Store in R2 for cold-start resilience (<100ms restore)
}
```

### p-adic Cache TTL
```javascript
function getPAdicCacheTTL(query) {
  // ord₂ = (maxDepth - queryDepth) / scale
  // TTL = 15s × 2^ord₂, capped at 960s
  // Foundational queries get longer cache
}
```

## Bindings Required

```toml
[[d1_databases]]  binding = "DB"          # qnfo-audit
[[d1_databases]]  binding = "PAPERS_DB"   # living-paper
[[vectorize]]     binding = "VECTORIZE_INDEX"
[[r2_buckets]]    binding = "PAPERS_R2"   # qnfo
[ai]              binding = "AI"
[triggers]        crons = ["*/30 * * * *"]
```

## Verification Checklist

- [ ] `/health` returns `paper_count`, `chunks_in_vectorize`
- [ ] `/did-you-mean?q=quantm` returns `discoveries` (cluster neighbors beyond word matches)
- [ ] `/ultrametric-tree` includes all 19 fields
- [ ] `/spectral-analysis` includes `intrinsicAmice` (Principle #20)
- [ ] `/buffer-schedule` returns "token not configured" until secret is set
- [ ] Tree persists across cold starts via R2
- [ ] Frontend renders D3 dendrogram
