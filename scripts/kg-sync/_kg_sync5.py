"""KG Sync Phase 5: Paper seeding + GitHub repos"""
import urllib.request, json, re

BASE = "https://graph-api.q08.workers.dev"
H = {"User-Agent": "Mozilla/5.0", "Content-Type": "application/json"}

def kg_get(path):
    req = urllib.request.Request(BASE + path, headers={"User-Agent": "Mozilla/5.0"})
    return json.loads(urllib.request.urlopen(req, timeout=20).read())

def kg_post(path, body):
    data = json.dumps(body).encode()
    req = urllib.request.Request(BASE + path, data=data, method="POST", headers=H)
    return json.loads(urllib.request.urlopen(req, timeout=20).read())

###############################################################################
# 1. FIX PAPER SITEMAP PARSING
###############################################################################
print("=== PAPERS SITEMAP RAW ===")
try:
    r = urllib.request.Request("https://papers.qnfo.org/sitemap.xml", headers={"User-Agent": "Mozilla/5.0"})
    sm = urllib.request.urlopen(r, timeout=15).read().decode()
    # Show first 2000 chars
    print(sm[:2000])
    print(f"\nTotal chars: {len(sm)}")
    
    # Try different regex patterns
    locs = re.findall(r"<loc>([^<]+)</loc>", sm)
    print(f"URLs found: {len(locs)}")
    # Filter for paper pages
    paper_urls = [u for u in locs if "/papers/" in u and u.count("/") >= 2]
    print(f"Paper URLs: {len(paper_urls)}")
    for u in paper_urls[:10]:
        print(f"  {u}")
except Exception as e:
    print(f"Error: {e}")

###############################################################################
# 2. SEED PAPERS FROM LLMS.TXT
###############################################################################
print("\n=== SEEDING PAPERS FROM llms.txt ===")
try:
    r2 = urllib.request.Request("https://papers.qnfo.org/llms.txt", headers={"User-Agent": "Mozilla/5.0"})
    ll = urllib.request.urlopen(r2, timeout=15).read().decode()
    print(f"llms.txt: {len(ll)} chars")
    
    # Parse: "slug: Title info"
    paper_nodes = []
    paper_edges = []
    ec = 95000
    
    for line in ll.strip().split("\n"):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" in line:
            slug, title_info = line.split(":", 1)
            slug = slug.strip()
            title_info = title_info.strip()
            
            doi_match = re.search(r"(10\.\d{4,}/[^\s,\)]+)", title_info)
            paper_doi = doi_match.group(1) if doi_match else None
            
            paper_nodes.append({
                "id": f"paper-{slug[:50]}",
                "label": "Paper",
                "name": slug[:80],
                "properties": {
                    "title": title_info[:250],
                    "doi": paper_doi or "",
                    "source": "papers-llms.txt",
                    "indexed": "2026-07-12",
                    "url": f"https://papers.qnfo.org/{slug}"
                }
            })
            
            # Link quantum/ultrametric-related papers to kepler-program
            combined = (slug + " " + title_info).lower()
            if any(kw in combined for kw in ["ultrametric", "p-adic", "qec", "hensel", "bruhat", "adelic", "quantum", "ostrowski", "informational"]):
                paper_edges.append({
                    "id": f"edge-{ec}",
                    "source_id": f"paper-{slug[:50]}",
                    "target_id": "kepler-program",
                    "relationship_type": "RELATES_TO",
                    "properties": {"source": "llms-txt-match"}
                })
                ec += 1
    
    print(f"\nSeeding {len(paper_nodes)} paper nodes + {len(paper_edges)} edges...")
    if paper_nodes:
        result = kg_post("/sync", {
            "action": "bulk",
            "nodes": paper_nodes,
            "edges": paper_edges
        })
        print(f"Papers: nodes={result.get('upserted_nodes',0)}, edges={result.get('upserted_edges',0)}, errors={result.get('errors',[])}")
except Exception as e:
    print(f"llms.txt error: {e}")

###############################################################################
# 3. GITHUB REPO CROSS-REFERENCE
###############################################################################
print("\n=== GITHUB REPO CROSS-REFERENCE ===")
repos_to_check = [
    "rwnq8/qnfo-skills",
    "rwnq8/ultrametric-foundation", 
    "rwnq8/qnfo-core",
    "rwnq8/kepler-program",
]

repo_nodes = []
repo_edges = []
ec = 96000

for repo in repos_to_check:
    try:
        req = urllib.request.Request(
            f"https://api.github.com/repos/{repo}",
            headers={"User-Agent": "QNFO-KG-Sync/1.0", "Accept": "application/vnd.github+json"}
        )
        resp = json.loads(urllib.request.urlopen(req, timeout=10).read())
        if resp.get("full_name"):
            desc = resp.get("description", "")[:200]
            stars = resp.get("stargazers_count", 0)
            updated = resp.get("updated_at", "N/A")
            html_url = resp.get("html_url", "")
            print(f"  {repo}: stars={stars}, updated={updated}, desc='{desc[:80]}'")
            
            node_id = f"github-{repo.replace('/', '-')}"
            repo_nodes.append({
                "id": node_id,
                "label": "CloudflareAsset",
                "name": repo,
                "properties": {
                    "type": "GitHubRepo",
                    "description": desc,
                    "stars": stars,
                    "updated_at": updated,
                    "url": html_url
                }
            })
            repo_edges.append({
                "id": f"edge-{ec}",
                "source_id": node_id,
                "target_id": "kepler-program",
                "relationship_type": "BELONGS_TO",
                "properties": {"source": "github-api"}
            })
            ec += 1
        else:
            print(f"  {repo}: NOT FOUND")
    except Exception as e:
        print(f"  {repo}: {type(e).__name__}: {e}")

if repo_nodes:
    result = kg_post("/sync", {
        "action": "bulk",
        "nodes": repo_nodes,
        "edges": repo_edges
    })
    print(f"\nGitHub repos: nodes={result.get('upserted_nodes',0)}, edges={result.get('upserted_edges',0)}")

###############################################################################
# 4. FINAL VERIFICATION
###############################################################################
print("\n=== FINAL STATE ===")
stats = kg_get("/stats")
print(f"Nodes: {stats['totalNodes']}  Edges: {stats['totalEdges']}")

# Node label summary
print("\nNode labels:")
for nl in stats.get("nodeLabels", []):
    if nl["count"] > 0:
        print(f"  {nl['label']:25s} {nl['count']}")

# Edge type summary  
print("\nEdge types:")
for rt in stats.get("relationshipTypes", []):
    if rt["count"] > 0:
        print(f"  {rt['type']:30s} {rt['count']}")

print("\n=== SYNC COMPLETE ===")
