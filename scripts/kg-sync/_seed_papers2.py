"""Seed papers from downloaded llms.txt"""
import json, urllib.request, re

BASE = "https://graph-api.q08.workers.dev"
H = {"User-Agent": "Mozilla/5.0", "Content-Type": "application/json"}

def kg_post(path, body):
    data = json.dumps(body).encode()
    req = urllib.request.Request(BASE + path, data=data, method="POST", headers=H)
    return json.loads(urllib.request.urlopen(req, timeout=30).read())

with open("_llms.txt", "r", encoding="utf-8") as f:
    ll = f.read()

print(f"llms.txt: {len(ll)} chars, {len(ll.splitlines())} lines")

paper_nodes = []
for line in ll.strip().split("\n"):
    line = line.strip()
    if not line or line.startswith("#"):
        continue
    if ":" not in line:
        continue
    
    slug, title_info = line.split(":", 1)
    slug = slug.strip()
    title_info = title_info.strip()
    if len(slug) > 100:
        continue
    
    doi_match = re.search(r"(10\.\d{4,}/[^\s,\)]+)", title_info)
    paper_doi = doi_match.group(1) if doi_match else None
    
    paper_nodes.append({
        "id": f"paper-{slug.replace('/','-')[:60]}",
        "label": "Paper",
        "name": slug[:80],
        "properties": {
            "title": title_info[:250],
            "doi": paper_doi or "",
            "source": "papers-llms.txt",
            "indexed": "2026-07-12"
        }
    })

print(f"Total papers parsed: {len(paper_nodes)}")

# Show a few
for p in paper_nodes[:5]:
    print(f"  {p['name'][:40]} | {p['properties']['title'][:60]}")

# Sync in chunks
total_upserted = 0
for i in range(0, len(paper_nodes), 50):
    chunk = paper_nodes[i:i+50]
    print(f"  Chunk {i//50 + 1}: {len(chunk)} papers...", end=" ")
    try:
        result = kg_post("/sync", {"action": "bulk", "nodes": chunk, "edges": []})
        u = result.get("upserted_nodes", 0)
        errs = result.get("errors", [])
        total_upserted += u
        print(f"upserted={u}, errors={len(errs)}")
    except Exception as e:
        print(f"ERROR: {e}")

print(f"\nTotal papers upserted: {total_upserted}")

# Final stats
r = urllib.request.Request(BASE + "/stats", headers={"User-Agent": "Mozilla/5.0"})
stats = json.loads(urllib.request.urlopen(r, timeout=15).read())
print(f"KG now: {stats['totalNodes']} nodes, {stats['totalEdges']} edges")
pn = [nl for nl in stats.get("nodeLabels", []) if nl["label"] == "Paper"]
if pn:
    print(f"Paper nodes: {pn[0]['count']}")
