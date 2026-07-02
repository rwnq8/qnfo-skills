#!/usr/bin/env python3
"""Multi-source academic literature search with deduplication and classification."""
import argparse, json, os, re, sys, time, urllib.request, urllib.parse
from datetime import datetime, timezone
from typing import Optional

def search_preprints(query: str, max_results: int = 50) -> list[dict]:
    """Search preprint servers for papers matching query."""
    base_url = "http://export.arxiv.org/api/query"  # preprint API query endpoint
    params = {"search_query": query, "start": 0, "max_results": max_results,
              "sortBy": "relevance", "sortOrder": "descending"}
    url = f"{base_url}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url)
    req.add_header("User-Agent", "QNFO-LiteratureSearch/1.0 (mailto:rwnquni@outlook.com)")
    try:
        response = urllib.request.urlopen(req, timeout=30)
        xml_data = response.read().decode("utf-8")
    except Exception as e:
        print(f"[WARN] Preprint API error: {e}", file=sys.stderr)
        return []
    papers, entries = [], xml_data.split("<entry>")
    for entry in entries[1:]:
        try:
            title = _extract_xml(entry, "title")
            authors = re.findall(r"<name>(.*?)</name>", entry)
            summary = _extract_xml(entry, "summary").strip()
            paper_id = _extract_xml(entry, "id")
            preprint_id = paper_id.split("/abs/")[-1] if "/abs/" in paper_id else paper_id
            published = _extract_xml(entry, "published")
            year = int(published[:4]) if published else 0
            doi = ""
            for link in re.findall(r'<link[^>]*>', entry):
                if 'title="doi"' in link:
                    doi_match = re.search(r'href="([^"]+)"', link)
                    if doi_match: doi = doi_match.group(1).replace("http://dx.doi.org/", "")
            papers.append({"title": title.strip().replace("\n", " "), "authors": authors,
                          "year": year, "abstract": summary, "preprint_id": preprint_id,
                          "doi": doi, "url": paper_id, "source": "preprints", "published": published})
        except Exception: continue
    return papers

def _extract_xml(xml: str, tag: str) -> str:
    pattern = f"<{tag}[^>]*>(.*?)</{tag}>"
    match = re.search(pattern, xml, re.DOTALL)
    return match.group(1) if match else ""

def search_semantic_scholar(query: str, limit: int = 50) -> list[dict]:
    base_url = "https://api.semanticscholar.org/graph/v1/paper/search"
    params = {"query": query, "limit": min(limit, 100),
              "fields": "title,authors,year,abstract,externalIds,citationCount,url,publicationDate"}
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
        papers.append({"title": paper.get("title", ""),
                      "authors": [a.get("name", "") for a in authors_list],
                      "year": paper.get("year", 0), "abstract": paper.get("abstract", ""),
                      "doi": external_ids.get("DOI", ""), "preprint_id": external_ids.get("ArXiv", ""),
                      "citation_count": paper.get("citationCount", 0),
                      "url": paper.get("url", ""), "source": "semantic_scholar"})
    return papers

def deduplicate(papers: list[dict]) -> list[dict]:
    seen_dois, seen_preprint_ids, seen_titles = set(), set(), set()
    merged = []
    for paper in sorted(papers, key=lambda p: p.get("citation_count", 0) or 0, reverse=True):
        doi = paper.get("doi", "").lower().strip()
        preprint_id = paper.get("preprint_id", "").lower().strip()
        title = paper.get("title", "").lower().strip()[:80]
        if doi and doi in seen_dois: continue
        if preprint_id and preprint_id in seen_preprint_ids: continue
        if title and title in seen_titles: continue
        if doi: seen_dois.add(doi)
        if preprint_id: seen_preprint_ids.add(preprint_id)
        if title: seen_titles.add(title)
        merged.append(paper)
    return merged

def classify_papers(papers: list[dict], research_topic: str) -> list[dict]:
    keywords = set(re.findall(r'[a-zA-Z]{4,}', research_topic.lower()))
    for paper in papers:
        title_lower = paper.get("title", "").lower()
        abstract_lower = paper.get("abstract", "").lower()
        text = title_lower + " " + abstract_lower
        keyword_hits = sum(1 for kw in keywords if kw in text)
        citation_count = paper.get("citation_count", 0) or 0
        year = paper.get("year", 0) or 0
        if keyword_hits >= 4 and citation_count >= 5 and year >= 2018:
            paper["tier"] = "core"
        elif keyword_hits >= 2 and year >= 2015:
            paper["tier"] = "supporting"
        elif keyword_hits >= 1 or citation_count >= 50:
            paper["tier"] = "background"
        else:
            paper["tier"] = "reject"
    return papers

def main():
    parser = argparse.ArgumentParser(description="Multi-source academic literature search")
    parser.add_argument("--query", "-q", required=True, help="Research topic or search query")
    parser.add_argument("--max", type=int, default=50, help="Max results per source")
    parser.add_argument("--output", "-o", default="literature-brief.md", help="Output file path")
    parser.add_argument("--sources", default="preprints,semantic_scholar",
                       help="Comma-separated sources")
    parser.add_argument("--json", action="store_true", help="Output raw JSON instead of brief")
    parser.add_argument("--brief", action="store_true", help="Output brief Markdown")
    args = parser.parse_args()

    queries = {"preprints": f"all:{args.query.replace(' ', '+AND+all:')}",
               "semantic_scholar": args.query}
    all_papers, sources = [], args.sources.split(",")

    if "preprints" in sources:
        print(f"[SEARCH] Preprints: {queries['preprints'][:120]}...")
        preprint_results = search_preprints(queries["preprints"], args.max)
        print(f"  -> {len(preprint_results)} papers")
        all_papers.extend(preprint_results)
        time.sleep(1)
    if "semantic_scholar" in sources:
        print(f"[SEARCH] Semantic Scholar: {queries['semantic_scholar']}")
        ss_results = search_semantic_scholar(queries["semantic_scholar"], args.max)
        print(f"  -> {len(ss_results)} papers")
        all_papers.extend(ss_results)
        time.sleep(0.5)

    before = len(all_papers)
    all_papers = deduplicate(all_papers)
    print(f"[DEDUP] {before} -> {len(all_papers)} papers ({before - len(all_papers)} removed)")
    all_papers = classify_papers(all_papers, args.query)
    tiers = {}
    for p in all_papers: tiers[p.get("tier", "unknown")] = tiers.get(p.get("tier", "unknown"), 0) + 1
    print(f"[CLASSIFY] {tiers}")

    if args.json:
        output = json.dumps(all_papers, indent=2, ensure_ascii=False)
    elif args.brief:
        core = [p for p in all_papers if p.get("tier") == "core"]
        supporting = [p for p in all_papers if p.get("tier") == "supporting"]
        lines = [f"# LITERATURE BRIEF: {args.query}",
                f"**Generated:** {datetime.now(timezone.utc).isoformat()}",
                f"**Found:** {len(all_papers)} | Core: {len(core)} | Supporting: {len(supporting)}",
                "", "## Core Papers", "",
                "| # | Title | Authors | Year | Citations |",
                "|:--|:------|:--------|:-----|:---------:|"]
        for i, p in enumerate(core[:15], 1):
            authors = ", ".join(p.get("authors", [])[:3])
            if len(p.get("authors", [])) > 3: authors += " et al."
            lines.append(f"| {i} | {p['title'][:80]} | {authors} | {p.get('year','?')} | {p.get('citation_count',0)} |")
        lines.extend(["", "## Supporting Papers", "",
                      "| # | Title | Authors | Year | Citations |",
                      "|:--|:------|:--------|:-----|:---------:|"])
        for i, p in enumerate(supporting[:20], 1):
            authors = ", ".join(p.get("authors", [])[:2])
            if len(p.get("authors", [])) > 2: authors += " et al."
            lines.append(f"| {i} | {p['title'][:80]} | {authors} | {p.get('year','?')} | {p.get('citation_count',0)} |")
        output = "\n".join(lines)
    else:
        output = json.dumps({"papers": all_papers, "count": len(all_papers),
                            "query": args.query}, indent=2, ensure_ascii=False)

    with open(args.output, "w", encoding="utf-8") as f: f.write(output)
    print(f"[DONE] -> {args.output}")

if __name__ == "__main__": main()
