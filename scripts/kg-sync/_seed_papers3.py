"""Seed papers from llms.txt — small batch approach"""
import json, urllib.request, re, sys

BASE = "https://graph-api.q08.workers.dev"

def kg_post(path, body):
    data = json.dumps(body).encode()
    req = urllib.request.Request(BASE + path, data=data, method="POST",
        headers={"User-Agent": "Mozilla/5.0", "Content-Type": "application/json"})
    return json.loads(urllib.request.urlopen(req, timeout=20).read())

with open("_llms.txt", "r", encoding="utf-8") as f:
    ll = f.read()

paper_nodes = []
for line in ll.strip().split("\n"):
    line = line.strip()
    if not line or line.startswith("#") or ":" not in line:
        continue
    slug, rest = line.split(":", 1)
    slug = slug.strip()
    rest = rest.strip()
    if len(slug) > 100:
        continue
    doi_match = re.search(r"(10\.\d{4,}/[^\s,\)]+)", rest)
    doi = doi_match.group(1) if doi_match else None
    paper_nodes.append({
        "id": f"paper-{slug.replace('/','-')[:60]}",
        "label": "Paper",
        "name": slug[:80],
        "properties": {
            "title": rest[:250],
            "doi": doi or "",
            "source": "papers-llms.txt",
            "indexed": "2026-07-12"
        }
    })

print(f"Parsed {len(paper_nodes)} papers from llms.txt")

total = 0
for i in range(0, len(paper_nodes), 10):
    chunk = paper_nodes[i:i+10]
    try:
        result = kg_post("/sync", {"action": "bulk", "nodes": chunk, "edges": []})
        u = result.get("upserted_nodes", 0)
        total += u
        sys.stdout.write(f"  [{i+1}-{min(i+10, len(paper_nodes))}] upserted={u}")
        errs = result.get("errors", [])
        if errs:
            sys.stdout.write(f" errs={len(errs)}")
        sys.stdout.write("\n")
        sys.stdout.flush()
    except Exception as e:
        print(f"  [{i+1}] ERROR: {e}")

print(f"\nTotal upserted: {total}")

# Final stats
r = urllib.request.Request(BASE + "/stats", headers={"User-Agent": "Mozilla/5.0"})
stats = json.loads(urllib.request.urlopen(r, timeout=10).read())
print(f"KG: {stats['totalNodes']} nodes, {stats['totalEdges']} edges")
pn = [x for x in stats.get("nodeLabels", []) if x["label"] == "Paper"]
print(f"Papers: {pn[0]['count'] if pn else 0}")
