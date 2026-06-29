"""Add missing paper nodes to KG."""
import json, urllib.request, time

UA = "QNFO-Phase2/1.0"
ASK_QWAV = "https://ask-qwav.q08.workers.dev"
GRAPH_API = "https://graph-api.q08.workers.dev"

# Get all D1 paper IDs
req = urllib.request.Request(f"{ASK_QWAV}/api/papers?limit=200", headers={"User-Agent": UA})
with urllib.request.urlopen(req, timeout=30) as resp:
    papers = json.loads(resp.read())["data"]
all_ids = {p["id"] for p in papers}
print(f"D1 paper IDs: {len(all_ids)}")

# Get all KG paper IDs
req2 = urllib.request.Request(f"{GRAPH_API}/nodes?label=Paper", headers={"User-Agent": UA})
with urllib.request.urlopen(req2, timeout=30) as resp:
    kg_data = json.loads(resp.read())

kg_ids = set()
for n in kg_data.get("nodes", []):
    pid = (n.get("properties") or {}).get("paper_id", "")
    if pid:
        kg_ids.add(pid)
print(f"KG paper IDs: {len(kg_ids)}")

# Find missing
missing = all_ids - kg_ids
print(f"Missing from KG: {len(missing)}")
print(f"Sample missing: {sorted(missing)[:10]}")

# Create nodes for missing papers
paper_map = {p["id"]: p for p in papers}
nodes = []
for pid in sorted(missing):
    p = paper_map[pid]
    title = (p.get("title") or "Untitled").strip()[:250]
    nodes.append({
        "id": f"paper-{pid}",
        "label": "Paper",
        "name": title,
        "properties": {
            "paper_id": pid,
            "title": title,
            "authors": p.get("authors", ""),
            "doi": p.get("doi") or "",
            "status": "active",
            "source": "living-paper-d1"
        }
    })

print(f"\nCreating {len(nodes)} missing paper nodes...")

# Sync in batches
for i in range(0, len(nodes), 25):
    batch = nodes[i:i+25]
    body = json.dumps({"action": "bulk", "nodes": batch, "edges": []}).encode()
    r = urllib.request.Request(GRAPH_API + "/sync", data=body, method="POST",
        headers={"Content-Type": "application/json", "User-Agent": UA})
    with urllib.request.urlopen(r, timeout=60) as resp:
        result = json.loads(resp.read())
    print(f"  Batch {i//25 + 1}: {result.get('upserted_nodes', '?')} ()")
    time.sleep(0.2)

# Verify
req3 = urllib.request.Request(f"{GRAPH_API}/nodes?label=Paper", headers={"User-Agent": UA})
with urllib.request.urlopen(req3, timeout=30) as resp:
    kg_data2 = json.loads(resp.read())
print(f"\nAfter sync: {kg_data2.get('count', 0)} Paper nodes in KG")

req4 = urllib.request.Request(f"{GRAPH_API}/stats", headers={"User-Agent": UA})
with urllib.request.urlopen(req4, timeout=30) as resp:
    stats = json.loads(resp.read())
for nl in stats.get("nodeLabels", []):
    if nl["label"] == "Paper":
        print(f"Paper nodes (stats): {nl['count']}")
