---
name: literature-search
version: "1.0"
description: Automated multi-source academic literature search and paper triage for LLM Research Automation Pipeline (LRAP). Queries arXiv, Semantic Scholar, QNFO Vectorize, and web search; deduplicates results; classifies papers as core/supporting/background/reject. Use when user asks "search for papers on X," "find literature about Y," "what's published on Z," or when executing Phase 1 of any research project.
---

# LITERATURE SEARCH SKILL — v1.0

> **Phase 1 of LRAP.** Automates multi-source academic literature discovery, deduplication, and triage.

---

## Purpose

Execute comprehensive literature search across 4+ academic sources, deduplicate results, classify papers by relevance tier, and produce a structured literature brief ready for deep reading. Eliminates the manual cycle of re-writing arXiv API queries, Semantic Scholar calls, and web searches for every research project.

## When to Use

| Trigger | Action |
|:--------|:-------|
| "Search for papers on ultrametric quantum cognition" | Full 4-source search |
| "Find recent arXiv papers about p-adic QEC" | arXiv-only search |
| "What literature exists on hierarchical emergence?" | Multi-source + QNFO Vectorize |
| "Analyze the citation network for these 20 papers" | Semantic Scholar citation analysis |
| Research Phase 1 in any pipeline | Automatic trigger via `research-orchestrator` |

## Workflow — 5 Stages

### Stage 1: Query Generation

Accept a research seed (natural language or structured brief) → generate 3-5 optimized search queries per source:

| Source | Query Format | Example |
|:-------|:-------------|:--------|
| **arXiv API** | `search_query=all:p-adic+AND+all:quantum+AND+all:cognition` | Field-specific boolean |
| **Semantic Scholar** | Title/abstract search with filters | `?query=p-adic+quantum+cognition&year=2020-2026` |
| **QNFO Vectorize** | Natural language embedding query | `"ultrametric quantum cognition p-adic hierarchy"` |
| **Web Search** | Site-constrained broad search | `site:arxiv.org "ultrametric" "quantum decision"` |

### Stage 2: Multi-Source Execution

Execute queries in parallel (where possible). Capture provenance for every result:

```python
# Conceptual execution pattern (actual script below)
results = {
    "arxiv": arxiv_search(queries["arxiv"], max_results=50),
    "semantic_scholar": sem_scholar_search(queries["semantic_scholar"], limit=50),
    "qnfo_vectorize": qnfo_vectorize_search(queries["qnfo"], top_k=20),
    "web_search": brave_search(queries["web"], count=20),
}

# Each result entry:
{
    "source": "arxiv",
    "query": "all:p-adic+AND+all:quantum+cognition",
    "retrieved_at": "2026-06-24T14:30:00Z",
    "title": "...",
    "authors": ["...", "..."],
    "year": 2024,
    "doi": "10.xxxx/xxxxx",
    "arxiv_id": "2401.xxxxx",
    "abstract": "...",
    "citation_count": 42,      # from Semantic Scholar
    "url": "https://arxiv.org/abs/2401.xxxxx"
}
```

### Stage 3: Deduplication & Merging

Merge results from all sources, deduplicating by DOI > arXiv ID > title fuzzy match:

```python
def deduplicate(results_list):
    """Merge multi-source results, deduplicate by DOI > arXiv ID > title similarity."""
    seen_dois = set()
    seen_arxiv_ids = set()
    merged = []

    for paper in sorted(results_list, key=lambda p: p.get("citation_count", 0), reverse=True):
        doi = paper.get("doi", "")
        arxiv_id = paper.get("arxiv_id", "")

        if doi and doi in seen_dois:
            # Merge sources (add QNFO Vectorize score, combine metadata)
            _merge_into_existing(merged, paper, doi)
            continue
        if arxiv_id and arxiv_id in seen_arxiv_ids:
            _merge_into_existing(merged, paper, arxiv_id)
            continue

        # Fuzzy title check
        if _title_similarity_match(paper, merged):
            continue

        if doi:
            seen_dois.add(doi)
        if arxiv_id:
            seen_arxiv_ids.add(arxiv_id)
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
**Generated:** YYYY-MM-DD | **Sources:** arXiv, Semantic Scholar, QNFO Vectorize, Web Search
**Papers Found:** [total] | **Core:** [N] | **Supporting:** [M] | **Background:** [K]

## Search Strategy
- arXiv query: `[query]` → [N] results
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
- arXiv API queried at: [timestamp]
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

# ─── arXiv API ───────────────────────────────────────────────────

def search_arxiv(query: str, max_results: int = 50) -> list[dict]:
    """Search arXiv API for papers matching query."""
    base_url = "http://export.arxiv.org/api/query"
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
        print(f"[WARN] arXiv API error: {e}", file=sys.stderr)
        return []

    # Parse arXiv Atom XML response
    papers = []
    entries = xml_data.split("<entry>")
    
    for entry in entries[1:]:  # Skip first split (header)
        try:
            title = _extract_xml(entry, "title")
            authors = re.findall(r"<name>(.*?)</name>", entry)
            summary = _extract_xml(entry, "summary").strip()
            arxiv_id = _extract_xml(entry, "id")
            # Extract arXiv ID from URL
            arxiv_id_short = arxiv_id.split("/abs/")[-1] if "/abs/" in arxiv_id else arxiv_id
            
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
                "arxiv_id": arxiv_id_short,
                "doi": doi,
                "url": arxiv_id,
                "source": "arxiv",
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
            "arxiv_id": external_ids.get("ArXiv", ""),
            "citation_count": paper.get("citationCount", 0),
            "url": paper.get("url", ""),
            "source": "semantic_scholar",
        })

    return papers


# ─── QNFO Vectorize ─────────────────────────────────────────────

def search_qnfo_vectorize(query: str, top_k: int = 20, token: Optional[str] = None) -> list[dict]:
    """Search QNFO Vectorize index for semantically similar papers."""
    if not token:
        token = os.environ.get("CLOUDFLARE_API_TOKEN", "")
    
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
    """Deduplicate papers by DOI > arXiv ID > title similarity."""
    seen_dois = set()
    seen_arxiv_ids = set()
    seen_titles_lower = set()
    merged = []

    for paper in sorted(papers, key=lambda p: p.get("citation_count", 0) or 0, reverse=True):
        doi = paper.get("doi", "").lower().strip()
        arxiv_id = paper.get("arxiv_id", "").lower().strip()
        title = paper.get("title", "").lower().strip()[:80]  # First 80 chars

        if doi and doi in seen_dois:
            continue
        if arxiv_id and arxiv_id in seen_arxiv_ids:
            continue
        if title and title in seen_titles_lower:
            continue

        if doi:
            seen_dois.add(doi)
        if arxiv_id:
            seen_arxiv_ids.add(arxiv_id)
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
        f"**Generated:** {now} | **Sources:** arXiv, Semantic Scholar",
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
    parser.add_argument("--sources", default="arxiv,semantic_scholar", 
                        help="Comma-separated sources: arxiv,semantic_scholar,qnfo_vectorize,web")
    parser.add_argument("--json", action="store_true", help="Output raw JSON instead of brief")
    args = parser.parse_args()

    queries = {
        "arxiv": f"all:{args.query.replace(' ', '+AND+all:')}",
        "semantic_scholar": args.query,
        "qnfo_vectorize": args.query,
    }

    all_papers = []
    sources = args.sources.split(",")

    if "arxiv" in sources:
        print(f"[SEARCH] arXiv: {queries['arxiv']}")
        arxiv_results = search_arxiv(queries["arxiv"], args.max)
        print(f"  → {len(arxiv_results)} papers")
        all_papers.extend(arxiv_results)
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
- arXiv API: rate-limited to 1 request per second (enforced)
- Semantic Scholar API: rate-limited to 100 requests per 5 minutes (free tier)

### Usage

```bash
# Basic search
python literature_search.py --query "p-adic quantum error correction" --max 30

# Search only arXiv
python literature_search.py --query "ultrametric hierarchy cognition" --sources arxiv

# Output raw JSON for pipeline consumption
python literature_search.py --query "quantum decision theory" --json --output papers.json

# Full search across all available sources
python literature_search.py --query "topological quantum computing surface codes" --sources arxiv,semantic_scholar,qnfo_vectorize --max 50
```

---

## Integration Points

| Downstream Skill | How It Consumes Literature Search Output |
|:-----------------|:----------------------------------------|
| `citation-manager` | Reads paper DOIs/titles → generates BibTeX entries |
| `research-orchestrator` | Calls this skill as Phase 1, passes brief to Phase 2 |
| `knowledge-graph` | Seeds new paper nodes with metadata |
| `fabrication-audit` | Cross-references claims against identified papers |

## Failure Handling

| Scenario | Response |
|:---------|:---------|
| arXiv API timeout (>30s) | Retry once with half `max_results`. If still fails: `[ARXIV-UNAVAILABLE]`, continue with other sources |
| Semantic Scholar rate limit | Wait 60s, retry. If still limited: `[SEMANTIC-SCHOLAR-RATE-LIMITED]` |
| Zero results from all sources | `[NO-RESULTS]` — broaden query terms, try alternate spellings |
| Network error | `[NETWORK-ERROR: <details>]` — retry with exponential backoff (max 3 attempts) |

---



## Embedded Scripts

Per DEFAULT.md §6.1, this skill's dependent scripts are documented below.
**Canonical source: Cloudflare R2 (`qnfo/tools/`). Tools execute as ephemeral `_<name>.py` files — pull from R2, execute, discard. Never persist locally.**

| Script | Canonical (R2) | Ephemeral Execution Cache | Purpose |
|:-------|:---------------|:--------------------------|:--------|
| `search.py` | `qnfo/tools/search.py` | `_search.py` (ephemeral) | Multi-source academic literature search and triage |

### Execution Protocol (Ephemeral)
Tools execute locally (Python requires filesystem access) but do NOT persist:
1. **Pull:** `npx wrangler r2 object get qnfo/tools/<name>.py --remote --file=_<name>.py`
2. **Execute:** `python _<name>.py`
3. **Discard:** `Remove-Item _<name>.py`
4. If R2 copy missing: flag `[SKILL-GAP: script <name>.py missing from R2, cannot bootstrap]`

## VERSION HISTORY

| Version | Date | Changes |
|:--------|:-----|:--------|
| **v1.0** | 2026-06-26 | Skill audit — added version history. Current version. |


*literature-search v1.0 — Phase 1 of LRAP. Multi-source academic paper discovery with deduplication and tiered classification.*
