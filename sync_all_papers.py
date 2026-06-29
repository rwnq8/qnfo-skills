"""Sync ALL 170 paper nodes to KG using paginated API."""
import json, urllib.request, time

UA = "QNFO-Phase2/1.0"
ASK_QWAV = "https://ask-qwav.q08.workers.dev"
GRAPH_API = "https://graph-api.q08.workers.dev"

# Get ALL papers via pagination
all_papers = []
for offset in [0, 100]:
    req = urllib.request.Request(f"{ASK_QWAV}/api/papers?limit=100&offset={offset}", headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read())
    batch = data.get("data", [])
    all_papers.extend(batch)
    print(f"Offset {offset}: got {len(batch)} papers, total: {len(all_papers)}")
    if len(batch) < 100:
        break

print(f"Total papers from D1: {len(all_papers)}")

# Sync ALL as Paper nodes
nodes = []
for p in all_papers:
    title = (p.get("title") or "Untitled").strip()[:250]
    nodes.append({
        "id": f"paper-{p['id']}",
        "label": "Paper",
        "name": title,
        "properties": {
            "paper_id": p["id"],
            "title": title,
            "authors": p.get("authors", ""),
            "doi": p.get("doi") or "",
            "status": "active",
            "source": "living-paper-d1"
        }
    })

print(f"Syncing {len(nodes)} paper nodes to KG...")
for i in range(0, len(nodes), 50):
    batch = nodes[i:i+50]
    body = json.dumps({"action": "bulk", "nodes": batch, "edges": []}).encode()
    r = urllib.request.Request(GRAPH_API + "/sync", data=body, method="POST",
        headers={"Content-Type": "application/json", "User-Agent": UA})
    with urllib.request.urlopen(r, timeout=60) as resp:
        result = json.loads(resp.read())
    upserted = result.get("upserted_nodes", "?")
    print(f"  Batch {i//50 + 1}/{ (len(nodes)+49)//50 }: {upserted} synced")
    time.sleep(0.2)

# Verify
req = urllib.request.Request(GRAPH_API + "/stats", headers={"User-Agent": UA})
with urllib.request.urlopen(req, timeout=30) as resp:
    stats = json.loads(resp.read())
for nl in stats.get("nodeLabels", []):
    if nl["label"] == "Paper":
        print(f"\n✅ Paper nodes: {nl['count']}")
print(f"Total nodes: {stats['totalNodes']}, Total edges: {stats['totalEdges']}")
