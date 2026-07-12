"""KG Sync — Paper seeding only (quick)"""
import urllib.request, json, re

BASE = "https://graph-api.q08.workers.dev"
H = {"User-Agent": "Mozilla/5.0", "Content-Type": "application/json"}

def kg_post(path, body):
    data = json.dumps(body).encode()
    req = urllib.request.Request(BASE + path, data=data, method="POST", headers=H)
    return json.loads(urllib.request.urlopen(req, timeout=30).read())

# Fetch llms.txt
print("Fetching llms.txt...")
r = urllib.request.Request("https://papers.qnfo.org/llms.txt", headers={"User-Agent": "Mozilla/5.0"})
ll = urllib.request.urlopen(r, timeout=15).read().decode()
print(f"Got {len(ll)} chars, {len(ll.splitlines())} lines")

paper_nodes = []
paper_edges = []
ec = 95000

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
            "indexed": "2026-07-12",
            "url": f"https://papers.qnfo.org/{slug}"
        }
    })

print(f"Parsed {len(paper_nodes)} papers")

# Batch sync in chunks of 20
for i in range(0, len(paper_nodes), 20):
    chunk = paper_nodes[i:i+20]
    print(f"  Syncing chunk {i//20 + 1}: {len(chunk)} papers...")
    try:
        result = kg_post("/sync", {"action": "bulk", "nodes": chunk, "edges": []})
        u = result.get("upserted_nodes", 0)
        errs = result.get("errors", [])
        print(f"    upserted={u}, errors={len(errs)}")
    except Exception as e:
        print(f"    ERROR: {e}")

print("\nDone!")
