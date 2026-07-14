---
name: literature-search
description: Automated multi-source academic literature search and paper triage for LLM Research Automation Pipeline (LRAP). Queries preprint servers, Semantic Scholar, QNFO Vectorize, and web search; deduplicates results; classifies papers as core/supporting/background/reject. Use when user asks "search for papers on X," "find literature about Y," "what's published on Z," or when executing Phase 1 of any research project.
version: "1.1"
---

> **INCLUDES AUTONOMOUS RED-TEAM SELF-AUDIT.** Before claiming this skill complete, autonomously run: (1) Output Verification -- negative verification. (2) Assumption Challenge -- state and test every assumption. (3) Edge Case Check -- empty/null/max/boundary/desync. (4) DoD Integration -- verify all criteria met with tool evidence. (5) Iteration -- retry on failure, max 3. ANTI-PATTERN: User should NEVER ask about quality.

### Programmatic Loading & Execution
This skill is loaded and executed **programmatically by the LLM system** 
during response generation. Loading is triggered automatically via 
`skill_view('literature-search')` or `read()` with filesystem path.
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

> **Related:** publication-publisher, citation-manager

---

## Autonomous Continuation Protocol (v1.1)

**All 5 search stages execute autonomously without user intervention.** The agent MUST:

1. After ANY stage marked [EXECUTED], immediately proceed to next stage
2. Before advancing: tag `[AUTO-CONTINUE -> Stage N+1]` in the response
3. If a source API fails: tag `[BLOCKED: <source> unavailable]`, continue with remaining sources
4. At completion of all stages: tag `[SEARCH-COMPLETE: <total> papers, <core> core]`
5. Never wait for user confirmation between stages

**ANTI-PATTERN:** User should NEVER need to say "CONTINUE" between search stages.

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
  {"step": "Query preprint servers (arXiv, Semantic Scholar)", "status": "pending"},
  {"step": "Query QNFO Vectorize for internal papers", "status": "pending"},
  {"step": "Deduplicate and classify results (core/supporting/background/reject)", "status": "pending"},
  {"step": "Generate triage report with DOIs and abstracts", "status": "pending"},
  {"step": "Cross-reference against existing QNFO publications", "status": "pending"}
])


# LITERATURE SEARCH SKILL — v1.0

> **Version:** v1.0 (Kaizen-audited 2026-07-05)

> **Version:** v1.0 (Kaizen-audited 2026-07-05)


> **Phase 1 of LRAP.** Automates multi-source academic literature discovery, deduplication, and triage.

---
---

## Purpose

Execute comprehensive literature search across 4+ academic sources, deduplicate results, classify papers by relevance tier, and produce a structured literature brief ready for deep reading. Eliminates the manual cycle of re-writing preprint API queries, Semantic Scholar calls, and web searches for every research project.

## When to Use

| Trigger | Action |
|:--------|:-------|
| "Search for papers on ultrametric quantum cognition" | Full 4-source search |
| "Find recent preprint papers about p-adic QEC" | preprint-only search |
| "What literature exists on hierarchical emergence?" | Multi-source + QNFO Vectorize |
| "Analyze the citation network for these 20 papers" | Semantic Scholar citation analysis |
| Research Phase 1 in any pipeline | Automatic trigger via `research-orchestrator` |

## Workflow — 5 Stages

### Stage 1: Query Generation

Accept a research seed (natural language or structured brief) → generate 3-5 optimized search queries per source:

| Source | Query Format | Example |
|:-------|:-------------|:--------|
| **Preprint API** | `search_query=all:p-adic+AND+all:quantum+AND+all:cognition` | Field-specific boolean |
| **Semantic Scholar** | Title/abstract search with filters | `?query=p-adic+quantum+cognition&year=2020-2026` |
| **QNFO Vectorize** | Natural language embedding query | `"ultrametric quantum cognition p-adic hierarchy"` |
| **Web Search** | Site-constrained broad search | `site:preprint.example.org "ultrametric" "quantum decision"` |

### Stage 2: Multi-Source Execution

Execute queries in parallel (where possible). Capture provenance for every result:

```python
# Conceptual execution pattern (actual script below)
results = {
    "preprints": preprint_search(queries["preprints"], max_results=50),
    "semantic_scholar": sem_scholar_search(queries["semantic_scholar"], limit=50),
    "qnfo_vectorize": qnfo_vectorize_search(queries["qnfo"], top_k=20),
    "web_search": brave_search(queries["web"], count=20),
}

# Each result entry:
{
    "source": "preprints",
    "query": "all:p-adic+AND+all:quantum+cognition",
    "retrieved_at": "2026-06-24T14:30:00Z",
    "title": "...",
    "authors": ["...", "..."],
    "year": 2024,
    "doi": "10.xxxx/xxxxx",
    "preprint_id": "2401.xxxxx",
    "abstract": "...",
    "citation_count": 42,      # from Semantic Scholar
    "url": "https://preprint.example.org/abs/2401.xxxxx"
}
```

### Stage 3: Deduplication & Merging

Merge results from all sources, deduplicating by DOI > preprint ID > title fuzzy match:

```python
def deduplicate(results_list):
    """Merge multi-source results, deduplicate by DOI > preprint ID > title similarity."""
    seen_dois = set()
    seen_preprint_ids = set()
    merged = []

    for paper in sorted(results_list, key=lambda p: p.get("citation_count", 0), reverse=True):
        doi = paper.get("doi", "")
        preprint_id = paper.get("preprint_id", "")

        if doi and doi in seen_dois:
            # Merge sources (add QNFO Vectorize score, combine metadata)
            _merge_into_existing(merged, paper, doi)
            continue
        if preprint_id and preprint_id in seen_preprint_ids:
            _merge_into_existing(merged, paper, preprint_id)
            continue

        # Fuzzy title check
        if _title_similarity_match(paper, merged):
            continue

        if doi:
            seen_dois.add(doi)
        if preprint_id:
            seen_preprint_ids.add(preprint_id)
        merged.append(paper)

    return merged
```

### Stage 4: Paper Triage & Classification

Classify each paper into relevance tiers:

| Tier | Criteria | Expected Count | Action |
|:-----|:---------|:--------------:|:-------|
| **Core** | Directly addresses research question; must cite | 8-15 | Deep read, extract contributions |
| **Supporting** | Provides context or adjacent results | 10-20 | Read abstract + methods |
| **Background** | Foundational/survey papers | 5-10 | Note for intro/related work |
| **Reject** | Not relevant after abstract review | Variable | Document rejection reason |

Classification uses:
1. Semantic similarity score (from QNFO Vectorize if available, or compute locally)
2. Keyword overlap with research question
3. Citation count as signal of field importance
4. Recency (prefer last 5 years unless foundational)

### Stage 5: Literature Brief Output

Produce a structured literature brief in Markdown:

```markdown
# LITERATURE BRIEF: [Research Topic]
**Generated:** YYYY-MM-DD | **Sources:** Preprint servers, Semantic Scholar, QNFO Vectorize, Web Search
**Papers Found:** [total] | **Core:** [N] | **Supporting:** [M] | **Background:** [K]

## Search Strategy
- Preprint query: `[query]` → [N] results
- Semantic Scholar: `[query]` → [M] results
- QNFO Vectorize: `[query]` → [K] results
- Web search: `[query]` → [J] results

## Core Papers ([N])
| # | Title | Authors | Year | Citations | Key Contribution |
|:--|:------|:--------|:-----|:---------|:-----------------|
| 1 | ... | ... | 2024 | 42 | ... |

## Supporting Papers ([M])
[Table]

## Background Papers ([K])
[Table]

## Thematic Clusters
1. **Cluster A: [Theme]** — [N] papers on [topic]. Dominant approach: [method].
2. **Cluster B: [Theme]** — [M] papers on [topic]. Emerging direction: [angle].

## Gap Analysis
- **Well-covered:** [area with many papers]
- **Under-explored:** [area with few papers] ← POTENTIAL CONTRIBUTION
- **No papers found on:** [missing topics]

## Search Provenance
- Preprint API queried at: [timestamp]
- Semantic Scholar queried at: [timestamp]
- All URLs and DOIs captured for verification
```

---

## Embedded Script

### `scripts/literature_search.py`

```python
#!/usr/bin/env python3
"""
Literature Search Script — Multi-source academic paper discovery.
Usage: python literature_search.py --query "p-adic quantum cognition" --max 50
"""

import argparse
import json
import os
import re
import sys
import time
import urllib.request
import urllib.parse
from datetime import datetime, timezone
from typing import Optional

# ─── Preprint API ───────────────────────────────────────────────────

def search_preprints(query: str, max_results: int = 50) -> list[dict]:
    """Search preprint servers for papers matching query."""
    base_url = "http://export.arxiv.org/api/query"  # preprint API query endpoint
    params = {
        "search_query": query,
        "start": 0,
        "max_results": max_results,
        "sortBy": "relevance",
        "sortOrder": "descending",
    }
    url = f"{base_url}?{urllib.parse.urlencode(params)}"

    req = urllib.request.Request(url)
    req.add_header("User-Agent", "QNFO-LiteratureSearch/1.0 (mailto:rwnquni@outlook.com)")
    
    try:
        response = urllib.request.urlopen(req, timeout=30)
        xml_data = response.read().decode("utf-8")
    except Exception as e:
        print(f"[WARN] Preprint API error: {e}", file=sys.stderr)
        return []

    # Parse preprint Atom XML response
    papers = []
    entries = xml_data.split("<entry>")
    
    for entry in entries[1:]:  # Skip first split (header)
        try:
            title = _extract_xml(entry, "title")
            authors = re.findall(r"<name>(.*?)</name>", entry)
            summary = _extract_xml(entry, "summary").strip()
            paper_id = _extract_xml(entry, "id")
            # Extract preprint ID from URL
            preprint_id = paper_id.split("/abs/")[-1] if "/abs/" in paper_id else paper_id
            
            published = _extract_xml(entry, "published")
            year = int(published[:4]) if published else 0
            
            doi = ""
            for link in re.findall(r'<link[^>]*>', entry):
                if 'title="doi"' in link:
                    doi_match = re.search(r'href="([^"]+)"', link)
                    if doi_match:
                        doi = doi_match.group(1).replace("http://dx.doi.org/", "")
            
            papers.append({
                "title": title.strip().replace("\n", " "),
                "authors": authors,
                "year": year,
                "abstract": summary,
                "preprint_id": preprint_id,
                "doi": doi,
                "url": paper_id,
                "source": "preprints",
                "published": published,
            })
        except Exception:
            continue

    return papers


def _extract_xml(xml: str, tag: str) -> str:
    """Extract text content from XML tag."""
    pattern = f"<{tag}[^>]*>(.*?)</{tag}>"
    match = re.search(pattern, xml, re.DOTALL)
    return match.group(1) if match else ""


# ─── Semantic Scholar API ────────────────────────────────────────

def search_semantic_scholar(query: str, limit: int = 50) -> list[dict]:
    """Search Semantic Scholar API for papers."""
    base_url = "https://api.semanticscholar.org/graph/v1/paper/search"
    params = {
        "query": query,
        "limit": min(limit, 100),
        "fields": "title,authors,year,abstract,externalIds,citationCount,url,publicationDate",
    }
    url = f"{base_url}?{urllib.parse.urlencode(params)}"

    req = urllib.request.Request(url)
    req.add_header("User-Agent", "QNFO-LiteratureSearch/1.0")

    try:
        response = urllib.request.urlopen(req, timeout=15)
        data = json.loads(response.read().decode("utf-8"))
    except Exception as e:
        print(f"[WARN] Semantic Scholar API error: {e}", file=sys.stderr)
        return []

    papers = []
    for paper in data.get("data", []):
        external_ids = paper.get("externalIds", {})
        authors_list = paper.get("authors", [])
        
        papers.append({
            "title": paper.get("title", ""),
            "authors": [a.get("name", "") for a in authors_list],
            "year": paper.get("year", 0),
            "abstract": paper.get("abstract", ""),
            "doi": external_ids.get("DOI", ""),
            "preprint_id": external_ids.get("ArXiv", ""),
            "citation_count": paper.get("citationCount", 0),
            "url": paper.get("url", ""),
            "source": "semantic_scholar",
        })

    return papers


# ─── QNFO Vectorize ─────────────────────────────────────────────

def search_qnfo_vectorize(query: str, top_k: int = 20, token: Optional[str] = None) -> list[dict]:
    """Search QNFO Vectorize index for semantically similar papers."""
    if not token:
        token = os.environ.get("CLOUDFLARE_API_TOKEN", "")  # Canonical: Secrets Store (store_id=8ef28060302e4311b064ba3529493e8b)
    
    if not token:
        print("[WARN] No Cloudflare API token for Vectorize search", file=sys.stderr)
        return []

    # Use Vectorize query endpoint
    # This requires the vectorize index binding in a Worker or direct REST API
    # For now, returns empty — deploy a search Worker to enable this
    print("[INFO] QNFO Vectorize search requires deployed Worker endpoint", file=sys.stderr)
    print("[INFO] Using text-based fallback instead", file=sys.stderr)
    return []


# ─── Deduplication ──────────────────────────────────────────────

def deduplicate(papers: list[dict]) -> list[dict]:
    """Deduplicate papers by DOI > preprint ID > title similarity."""
    seen_dois = set()
    seen_preprint_ids = set()
    seen_titles_lower = set()
    merged = []

    for paper in sorted(papers, key=lambda p: p.get("citation_count", 0) or 0, reverse=True):
        doi = paper.get("doi", "").lower().strip()
        preprint_id = paper.get("preprint_id", "").lower().strip()
        title = paper.get("title", "").lower().strip()[:80]  # First 80 chars

        if doi and doi in seen_dois:
            continue
        if preprint_id and preprint_id in seen_preprint_ids:
            continue
        if title and title in seen_titles_lower:
            continue

        if doi:
            seen_dois.add(doi)
        if preprint_id:
            seen_preprint_ids.add(preprint_id)
        if title:
            seen_titles_lower.add(title)
        
        merged.append(paper)

    return merged


# ─── Classification ─────────────────────────────────────────────

def classify_papers(papers: list[dict], research_topic: str) -> list[dict]:
    """Classify papers into core/supporting/background tiers."""
    # Extract keywords from research topic
    keywords = set(re.findall(r'[a-zA-Z]{4,}', research_topic.lower()))
    
    for paper in papers:
        title_lower = paper.get("title", "").lower()
        abstract_lower = paper.get("abstract", "").lower()
        text = title_lower + " " + abstract_lower
        
        # Count keyword matches
        keyword_hits = sum(1 for kw in keywords if kw in text)
        citation_count = paper.get("citation_count", 0) or 0
        year = paper.get("year", 0) or 0
        
        # Classification heuristic
        if keyword_hits >= 4 and citation_count >= 5 and year >= 2018:
            paper["tier"] = "core"
        elif keyword_hits >= 2 and year >= 2015:
            paper["tier"] = "supporting"
        elif keyword_hits >= 1 or citation_count >= 50:
            paper["tier"] = "background"
        else:
            paper["tier"] = "reject"

    return papers


# ─── Output Generation ──────────────────────────────────────────

def generate_brief(papers: list[dict], research_topic: str, queries: dict) -> str:
    """Generate a structured literature brief in Markdown."""
    core = [p for p in papers if p.get("tier") == "core"]
    supporting = [p for p in papers if p.get("tier") == "supporting"]
    background = [p for p in papers if p.get("tier") == "background"]
    
    now = datetime.now(timezone.utc).isoformat()

    lines = [
        f"# LITERATURE BRIEF: {research_topic}",
        f"**Generated:** {now} | **Sources:** Preprints, Semantic Scholar",
        f"**Papers Found:** {len(papers)} | **Core:** {len(core)} | **Supporting:** {len(supporting)} | **Background:** {len(background)}",
        "",
        "## Search Strategy",
    ]
    
    for source, query in queries.items():
        lines.append(f"- **{source}:** `{query}`")

    # Core papers table
    lines.extend(["", "## Core Papers", "", "| # | Title | Authors | Year | Citations |", "|:--|:------|:--------|:-----|:---------:|"])
    for i, p in enumerate(core[:15], 1):
        authors = ", ".join(p.get("authors", [])[:3])
        if len(p.get("authors", [])) > 3:
            authors += " et al."
        lines.append(f"| {i} | {p['title'][:80]} | {authors} | {p.get('year', '?')} | {p.get('citation_count', 0)} |")

    # Supporting papers table
    lines.extend(["", "## Supporting Papers", "", "| # | Title | Authors | Year | Citations |", "|:--|:------|:--------|:-----|:---------:|"])
    for i, p in enumerate(supporting[:20], 1):
        authors = ", ".join(p.get("authors", [])[:2])
        if len(p.get("authors", [])) > 2:
            authors += " et al."
        lines.append(f"| {i} | {p['title'][:80]} | {authors} | {p.get('year', '?')} | {p.get('citation_count', 0)} |")

    lines.extend([
        "",
        "## Next Steps",
        "1. Deep-read all Core papers with full note-taking",
        "2. Skim Supporting papers for methodology and key claims",
        "3. Extract BibTeX entries for all cited papers",
        "4. Run `citation-manager` skill to verify and format bibliography",
        "",
        f"*Generated by literature-search skill v1.0. All URLs and DOIs captured for verification.*",
    ])

    return "\n".join(lines)


# ─── Main ───────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Multi-source academic literature search")
    parser.add_argument("--query", "-q", required=True, help="Research topic or search query")
    parser.add_argument("--max", type=int, default=50, help="Max results per source")
    parser.add_argument("--output", "-o", default="literature-brief.md", help="Output file path")
    parser.add_argument("--sources", default="preprints,semantic_scholar", 
                        help="Comma-separated sources: preprints,semantic_scholar,qnfo_vectorize,web")
    parser.add_argument("--json", action="store_true", help="Output raw JSON instead of brief")
    args = parser.parse_args()

    queries = {
        "preprints": f"all:{args.query.replace(' ', '+AND+all:')}",
        "semantic_scholar": args.query,
        "qnfo_vectorize": args.query,
    }

    all_papers = []
    sources = args.sources.split(",")

    if "preprints" in sources:
        print(f"[SEARCH] Preprints: {queries['preprints']}")
        preprint_results = search_preprints(queries["preprints"], args.max)
        print(f"  → {len(preprint_results)} papers")
        all_papers.extend(preprint_results)
        time.sleep(1)  # Rate limit courtesy

    if "semantic_scholar" in sources:
        print(f"[SEARCH] Semantic Scholar: {queries['semantic_scholar']}")
        ss_results = search_semantic_scholar(queries["semantic_scholar"], args.max)
        print(f"  → {len(ss_results)} papers")
        all_papers.extend(ss_results)
        time.sleep(0.5)

    if "qnfo_vectorize" in sources:
        print(f"[SEARCH] QNFO Vectorize: {queries['qnfo_vectorize']}")
        vec_results = search_qnfo_vectorize(queries["qnfo_vectorize"], min(args.max, 20))
        print(f"  → {len(vec_results)} papers")
        all_papers.extend(vec_results)

    # Deduplicate
    before_dedup = len(all_papers)
    all_papers = deduplicate(all_papers)
    print(f"\n[DEDUP] {before_dedup} → {len(all_papers)} papers ({before_dedup - len(all_papers)} duplicates removed)")

    # Classify
    all_papers = classify_papers(all_papers, args.query)
    
    tiers = {}
    for p in all_papers:
        tiers[p.get("tier", "unknown")] = tiers.get(p.get("tier", "unknown"), 0) + 1
    print(f"[CLASSIFY] {tiers}")

    if args.json:
        output = json.dumps(all_papers, indent=2, ensure_ascii=False)
    else:
        output = generate_brief(all_papers, args.query, queries)

    with open(args.output, "w", encoding="utf-8") as f:
        f.write(output)

    print(f"\n[DONE] Literature brief written to: {args.output}")
    print(f"  Core papers for deep reading: {len([p for p in all_papers if p.get('tier') == 'core'])}")


if __name__ == "__main__":
    main()
```

### Dependencies
- Python 3.8+ (standard library only — `urllib`, `json`, `re`, `argparse`)
- No external packages required
- Preprint API: rate-limited to 1 request per second (enforced)
- Semantic Scholar API: rate-limited to 100 requests per 5 minutes (free tier)

### Usage

```bash
# Basic search
python literature_search.py --query "p-adic quantum error correction" --max 30

# Search preprints only
python literature_search.py --query "ultrametric hierarchy cognition" --sources preprints

# Output raw JSON for pipeline consumption
python literature_search.py --query "quantum decision theory" --json --output papers.json

# Full search across all available sources
python literature_search.py --query "topological quantum computing surface codes" --sources preprints,semantic_scholar,qnfo_vectorize --max 50
```

---

## Integration Points

| Downstream Skill | How It Consumes Literature Search Output |
|:-----------------|:----------------------------------------|
| `citation-manager` | Reads paper DOIs/titles → generates BibTeX entries |
| `research-orchestrator` | Calls this skill as Phase 1, passes brief to Phase 2 |
| `knowledge-graph` | Seeds new paper nodes with metadata |
| `fabrication-audit` | Cross-references claims against identified papers |
| `deep-research` | Stage 1 finding synthesis consumes paper triage (core/supporting/background) to populate gap taxonomy for paradigm-shift forecasting |
## Handoff Protocol (MANDATORY at Closeout)

1. **Verify** ALL execute_plan items marked [EXECUTED] with tool evidence (Test-Path, exec output, git log)
2. **Archive** session artifacts to R2 canonical storage: `npx wrangler r2 object put qnfo/audit/... --remote --file=<artifact>`
3. **Generate** continuation prompt documenting pending work and current state for the next session
4. **Clean up** ephemeral _* files and __pycache__ directories: `Remove-Item _* -Recurse -Force`

### Continuation Prompt Template
```
TASK: [description of pending work from execute_plan]
STATE: [current state — what's executed, what's blocked, why]
NEXT: [first executable action for the next session]
R2: [canonical path for session artifacts]
```


## Closeout Protocol (MANDATORY)

Before declaring this skill workflow complete:
1. **Task Execution Verification:** Compare planned tasks ([PENDING] in execute_plan) vs executed tasks ([EXECUTED] with evidence)
2. **Filesystem Verification:** `Test-Path <file>` for every file claimed as created/modified. Never claim from memory.
3. **Git Verification:** `git log -1 --oneline` for every commit claimed. Verify commit hash exists.
4. **R2 State Upload:** Upload session audit trail to `qnfo/audit/` — conversations, decisions, state files.
5. **Discovery Index Update:** Update `qnfo/discovery/index.json` with any new resources created, projects modified, or publications generated.
6. **Ephemeral Cleanup:** Delete ALL _* prefixed files and __pycache__ directories. Session is not complete until `Get-ChildItem -File -Name | Where-Object { $_ -match '^_' }` returns zero results.
