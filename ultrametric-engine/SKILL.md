---
name: ultrametric-engine
description: Deploy 20 mathematical principles (ultrametric distance, p-adic valuation, Ostrowski's theorem, Hensel's lemma, Mahler compression, Berkovich spaces, Tate/Amice spectral analysis, Hasse local-global, Witt vectors, Bruhat-Tits buildings, p-adic caching, intrinsic Amice transform) as a production Cloudflare discovery engine. Use when building ultrametric tree-based search, p-adic ranked paper corpora, hierarchical dendrogram visualizations, or multi-endpoint Workers with R2/D1/Pages/Vectorize bindings.
version: "1.1"
---

> **INCLUDES AUTONOMOUS RED-TEAM SELF-AUDIT.** Before claiming this skill complete, autonomously run: (1) Output Verification -- negative verification. (2) Assumption Challenge -- state and test every assumption. (3) Edge Case Check -- empty/null/max/boundary/desync. (4) DoD Integration -- verify all criteria met with tool evidence. (5) Iteration -- retry on failure, max 3. ANTI-PATTERN: User should NEVER ask about quality.

### Programmatic Loading & Execution
This skill is loaded and executed **programmatically by the LLM system** 
during response generation. Loading is triggered automatically via 
`skill_view('ultrametric-engine')` or `read()` with filesystem path.
**The user NEVER manually loads this skill.** The `skill-autoloader` 
detects task patterns and handles all skill loading. If this skill fails 
to load, the LLM system automatically retries via the fallback chain 
documented below.
**Pinning:** This skill is [On-demand — loads when triggered by task patterns].

### Skill Loading Retry Protocol
If `skill_view('name')` fails during programmatic loading, the LLM system 
MUST execute this fallback chain:
1. **Retry 1:** `read('%USERPROFILE%\.deepchat\skills\<name>\SKILL.md')`
2. **Retry 2:** Pull from Cloudflare R2: `npx wrangler r2 object get 
   qnfo/prompts/skills/<name>/SKILL.md --remote --file=_skill.md`
3. **Retry 3:** If R2 fails, search local filesystem for any cached copy
4. **Fallback:** If ALL retries fail, continue with `[SKILL-UNAVAILABLE: <name>]` 
   and best-effort knowledge
**NEVER silently proceed without a skill's critical instructions.** If a skill 
is required for the task and cannot be loaded after 3 retries, escalate to 
the user with the specific failure reason.

---

> **Related:** knowledge-graph

---

## execute_plan (MANDATORY -- Before Any Execution)

**This skill involves execution-heavy workflows.** Before executing, use update_plan to populate a concrete, verifiable checklist. Every item must be short, specific, and testable with tool evidence.

### Execution Protocol

1. **Populate update_plan** with workflow phases as concrete checklist items
2. **Execute one item at a time** -- at most ONE in_progress
3. **Mark items completed ONLY with tool evidence** (Test-Path, exec output, git log)
4. **Never claim completion without execution evidence** -- Rule 14 enforcement
5. **If blocked:** Flag as [BLOCKED: reason] and move to the next item

### Example Plan

update_plan([
  {"step": "Define ultrametric distance metric", "status": "pending"},
  {"step": "Build hierarchical tree from data", "status": "pending"},
  {"step": "Implement p-adic valuation and ball queries", "status": "pending"},
  {"step": "Deploy as Cloudflare Worker with R2/D1/Vectorize bindings", "status": "pending"},
  {"step": "Verify ultrametric properties hold", "status": "pending"}
])


# ULTRAMETRIC ENGINE SKILL — v1.0

> **Version:** v1.0 (Kaizen-audited 2026-07-05)

> **Version:** v1.0 (Kaizen-audited 2026-07-05)


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
