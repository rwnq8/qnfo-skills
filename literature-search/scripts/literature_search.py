#!/usr/bin/env python3
# literature_search.py v1.0 -- Multi-source academic paper discovery
# Part of the literature-search skill. Usage: python literature_search.py --query "topic" --max 50

import argparse, json, os, re, sys, time, urllib.request, urllib.parse
from datetime import datetime, timezone
from typing import Optional

def search_arxiv(query: str, max_results: int = 50) -> list[dict]:
    base_url = "http://export.arxiv.org/api/query"
    params = {"search_query": query, "start": 0, "max_results": max_results, "sortBy": "relevance", "sortOrder": "descending"}
    url = f"{base_url}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url)
    req.add_header("User-Agent", "QNFO-LiteratureSearch/1.0 (mailto:rwnquni@outlook.com)")
    try:
        response = urllib.request.urlopen(req, timeout=30)
        xml_data = response.read().decode("utf-8")
    except Exception as e:
        print(f"[WARN] arXiv API error: {e}", file=sys.stderr)
        return []
    papers = []
    for entry in xml_data.split("<entry>")[1:]:
        try:
            title = re.search(r"<title[^>]*>(.*?)</title>", entry, re.DOTALL).group(1).strip().replace("\n", " ")
            authors = re.findall(r"<name>(.*?)</name>", entry)
            summary = re.search(r"<summary[^>]*>(.*?)</summary>", entry, re.DOTALL).group(1).strip()
            arxiv_id_full = re.search(r"<id>(.*?)</id>", entry).group(1)
            arxiv_id = arxiv_id_full.split("/abs/")[-1] if "/abs/" in arxiv_id_full else arxiv_id_full
            published = (re.search(r"<published>(.*?)</published>", entry) or [None, ""])[1]
            year = int(published[:4]) if published else 0
            doi = ""
            for link in re.findall(r'<link[^>]*>', entry):
                if 'title="doi"' in link:
                    doi_match = re.search(r'href="([^"]+)"', link)
                    if doi_match: doi = doi_match.group(1).replace("http://dx.doi.org/", "")
            papers.append({"title": title, "authors": authors, "year": year, "abstract": summary, "arxiv_id": arxiv_id, "doi": doi, "url": arxiv_id_full, "source": "arxiv", "published": published})
        except: continue
    return papers

def search_semantic_scholar(query: str, limit: int = 50) -> list[dict]:
    base_url = "https://api.semanticscholar.org/graph/v1/paper/search"
    params = {"query": query, "limit": min(limit, 100), "fields": "title,authors,year,abstract,externalIds,citationCount,url,publicationDate"}
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
        ext = paper.get("externalIds", {})
        authors = [a.get("name", "") for a in paper.get("authors", [])]
        papers.append({"title": paper.get("title", ""), "authors": authors, "year": paper.get("year", 0), "abstract": paper.get("abstract", ""), "doi": ext.get("DOI", ""), "arxiv_id": ext.get("ArXiv", ""), "citation_count": paper.get("citationCount", 0), "url": paper.get("url", ""), "source": "semantic_scholar"})
    return papers

def deduplicate(papers: list[dict]) -> list[dict]:
    seen_dois, seen_arxiv_ids, seen_titles = set(), set(), set()
    merged = []
    for paper in sorted(papers, key=lambda p: p.get("citation_count", 0) or 0, reverse=True):
        doi = paper.get("doi", "").lower().strip()
        aid = paper.get("arxiv_id", "").lower().strip()
        title = paper.get("title", "").lower().strip()[:80]
        if (doi and doi in seen_dois) or (aid and aid in seen_arxiv_ids) or (title and title in seen_titles): continue
        if doi: seen_dois.add(doi)
        if aid: seen_arxiv_ids.add(aid)
        if title: seen_titles.add(title)
        merged.append(paper)
    return merged

def classify_papers(papers: list[dict], topic: str) -> list[dict]:
    keywords = set(re.findall(r'[a-zA-Z]{4,}', topic.lower()))
    for p in papers:
        text = (p.get("title", "") + " " + p.get("abstract", "")).lower()
        hits = sum(1 for kw in keywords if kw in text)
        cites = p.get("citation_count", 0) or 0
        year = p.get("year", 0) or 0
        if hits >= 4 and cites >= 5 and year >= 2018: p["tier"] = "core"
        elif hits >= 2 and year >= 2015: p["tier"] = "supporting"
        elif hits >= 1 or cites >= 50: p["tier"] = "background"
        else: p["tier"] = "reject"
    return papers

def generate_brief(papers: list[dict], topic: str, queries: dict) -> str:
    core = [p for p in papers if p.get("tier") == "core"]
    supp = [p for p in papers if p.get("tier") == "supporting"]
    back = [p for p in papers if p.get("tier") == "background"]
    lines = [f"# LITERATURE BRIEF: {topic}", f"**Generated:** {datetime.now(timezone.utc).isoformat()}", f"**Papers:** {len(papers)} total | Core: {len(core)} | Supporting: {len(supp)} | Background: {len(back)}", "", "## Search Strategy"]
    for s, q in queries.items(): lines.append(f"- **{s}:** `{q}`")
    lines.extend(["", "## Core Papers", "", "| # | Title | Authors | Year | Citations |", "|:--|:------|:--------|:-----|:---------:|"])
    for i, p in enumerate(core[:15], 1):
        authors = ", ".join(p.get("authors", [])[:3])
        if len(p.get("authors", [])) > 3: authors += " et al."
        lines.append(f"| {i} | {p['title'][:80]} | {authors} | {p.get('year','?')} | {p.get('citation_count',0)} |")
    return "\n".join(lines)

def main():
    p = argparse.ArgumentParser(description="Multi-source academic literature search")
    p.add_argument("--query", "-q", required=True); p.add_argument("--max", type=int, default=50)
    p.add_argument("--output", "-o", default="literature-brief.md"); p.add_argument("--json", action="store_true")
    p.add_argument("--sources", default="arxiv,semantic_scholar")
    args = p.parse_args()
    queries = {"arxiv": args.query, "semantic_scholar": args.query}
    all_papers = []
    if "arxiv" in args.sources.split(","):
        print(f"[SEARCH] arXiv: {queries['arxiv']}")
        r = search_arxiv(queries["arxiv"], args.max); print(f"  -> {len(r)} papers"); all_papers.extend(r); time.sleep(1)
    if "semantic_scholar" in args.sources.split(","):
        print(f"[SEARCH] Semantic Scholar: {queries['semantic_scholar']}")
        r = search_semantic_scholar(queries["semantic_scholar"], args.max); print(f"  -> {len(r)} papers"); all_papers.extend(r)
    before = len(all_papers)
    all_papers = deduplicate(all_papers)
    print(f"\n[DEDUP] {before} -> {len(all_papers)} ({before-len(all_papers)} duplicates)")
    all_papers = classify_papers(all_papers, args.query)
    tiers = {}; [tiers.update({p.get("tier","?"): tiers.get(p.get("tier","?"),0)+1}) for p in all_papers]
    print(f"[CLASSIFY] {tiers}")
    output = json.dumps(all_papers, indent=2, ensure_ascii=False) if args.json else generate_brief(all_papers, args.query, queries)
    with open(args.output, "w", encoding="utf-8") as f: f.write(output)
    print(f"\n[DONE] -> {args.output}")
    print(f"  Core: {len([p for p in all_papers if p.get('tier')=='core'])}")

if __name__ == "__main__": main()
