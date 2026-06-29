"""Complete KG paper sync - add remaining papers and better edges."""
import json
import urllib.request

UA = "QNFO-Phase2/1.0"
ASK_QWAV = "https://ask-qwav.q08.workers.dev"
GRAPH_API = "https://graph-api.q08.workers.dev"

# Get all papers from D1
print("Fetching all papers from D1...")
all_req = urllib.request.Request(f"{ASK_QWAV}/api/papers?limit=200", headers={"User-Agent": UA})
with urllib.request.urlopen(all_req, timeout=30) as resp:
    papers_data = json.loads(resp.read())
papers = papers_data.get("data", [])
print(f"Got {len(papers)} papers from D1")

# Get existing paper nodes from KG
print("Fetching existing KG paper nodes...")
kg_req = urllib.request.Request(f"{GRAPH_API}/nodes?label=Paper", headers={"User-Agent": UA})
with urllib.request.urlopen(kg_req, timeout=30) as resp:
    kg_data = json.loads(resp.read())
existing_nodes = kg_data.get("nodes", [])
existing_paper_ids = set()
for n in existing_nodes:
    props = n.get("properties", {})
    pid = props.get("paper_id", "")
    if pid:
        existing_paper_ids.add(pid)
print(f"Existing KG papers: {len(existing_paper_ids)}")

# Find papers NOT yet in KG
missing_papers = [p for p in papers if p["id"] not in existing_paper_ids]
print(f"Papers missing from KG: {len(missing_papers)}")

# Get concept nodes
concept_req = urllib.request.Request(f"{GRAPH_API}/nodes?label=Concept", headers={"User-Agent": UA})
with urllib.request.urlopen(concept_req, timeout=30) as resp:
    concept_data = json.loads(resp.read())
concept_nodes = concept_data.get("nodes", [])
concept_map = {c.get("name", "").lower(): c.get("id") for c in concept_nodes}
print(f"Concept nodes: {len(concept_map)}")

# Keywords → concept name mapping
keyword_map = {
    "quantum": ["quantum error correction", "ultrametric theory", "general research", "qwav physics"],
    "qec": ["quantum error correction"],
    "error correction": ["quantum error correction"],
    "ultrametric": ["ultrametric theory"],
    "p-adic": ["ultrametric theory", "p-adic"],
    "metric": ["ultrametric theory"],
    "hierarch": ["ultrametric theory"],
    "information": ["information theory", "knowledge & data"],
    "entropy": ["information theory"],
    "physics": ["qwav physics", "general research"],
    "wave": ["qwav physics"],
    "field": ["qwav physics"],
    "cosmolog": ["qwav physics"],
    "particle": ["qwav physics"],
    "reality": ["general research", "philosophy"],
    "philosoph": ["philosophy"],
    "cognition": ["cognition", "general research"],
    "conscious": ["cognition"],
    "mathemat": ["mathematics", "general research"],
    "foundation": ["general research", "philosophy"],
    "time": ["qwav physics", "general research"],
    "space": ["qwav physics"],
    "dimension": ["qwav physics", "mathematics"],
    "topolog": ["mathematics"],
    "network": ["infrastructure", "knowledge & data"],
    "graph": ["mathematics", "knowledge & data"],
    "laws of form": ["general research", "mathematics"],
    "computation": ["computational", "infrastructure"],
    "algorithm": ["computational"],
    "ai": ["ai & synthesis", "computational"],
    "machine learn": ["ai & synthesis", "computational"],
}

# Sync missing papers and create edges
all_sync_nodes = []
all_sync_edges = []
edge_counter = 0

for p in missing_papers:
    node_id = f"paper-{p['id']}"
    all_sync_nodes.append({
        "id": node_id,
        "label": "Paper",
        "name": (p.get("title") or "Untitled")[:200],
        "properties": {
            "paper_id": p["id"],
            "title": p.get("title", "Untitled"),
            "authors": p.get("authors", ""),
            "doi": p.get("doi") or "",
            "status": "active",
            "source": "living-paper-d1"
        }
    })

# Also create edges for ALL papers (including existing ones)
# Use title + abstract for keyword matching
for p in papers:
    title = (p.get("title") or "").lower()
    abstract = (p.get("abstract") or "").lower()[:500]
    text = title + " " + abstract
    
    matched_concepts = set()
    for keyword, concept_names in keyword_map.items():
        if keyword in text:
            for cn in concept_names:
                matched_concepts.add(cn)
    
    for cn in matched_concepts:
        # Find closest concept ID
        concept_id = None
        for cname, cid in concept_map.items():
            if cn in cname or cname in cn:
                concept_id = cid
                break
        
        if concept_id:
            edge_counter += 1
            all_sync_edges.append({
                "id": f"edge-relates-{edge_counter}",
                "source_id": f"paper-{p['id']}",
                "target_id": concept_id,
                "relationship_type": "RELATES_TO",
                "properties": {"confidence": "keyword", "keyword": cn}
            })

print(f"\nCreating {len(all_sync_nodes)} new paper nodes")
print(f"Creating {len(all_sync_edges)} RELATES_TO edges")

# Sync nodes in batches
batch_size = 50
for i in range(0, len(all_sync_nodes), batch_size):
    batch = all_sync_nodes[i:i+batch_size]
    body = json.dumps({"action": "bulk", "nodes": batch, "edges": []}).encode()
    req = urllib.request.Request(
        f"{GRAPH_API}/sync",
        data=body, method="POST",
        headers={"Content-Type": "application/json", "User-Agent": UA}
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            result = json.loads(resp.read())
        print(f"  Nodes batch {i//batch_size + 1}: {result.get('upserted_nodes', 0)} synced")
    except Exception as e:
        print(f"  ERROR nodes batch {i//batch_size + 1}: {e}")

# Sync edges in batches
for i in range(0, len(all_sync_edges), batch_size):
    batch = all_sync_edges[i:i+batch_size]
    body = json.dumps({"action": "bulk", "nodes": [], "edges": batch}).encode()
    req = urllib.request.Request(
        f"{GRAPH_API}/sync",
        data=body, method="POST",
        headers={"Content-Type": "application/json", "User-Agent": UA}
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            result = json.loads(resp.read())
        print(f"  Edges batch {i//batch_size + 1}: {result.get('upserted_edges', 0)} synced")
    except Exception as e:
        print(f"  ERROR edges batch {i//batch_size + 1}: {e}")

# Final stats
stats_req = urllib.request.Request(f"{GRAPH_API}/stats", headers={"User-Agent": UA})
with urllib.request.urlopen(stats_req, timeout=30) as resp:
    stats = json.loads(resp.read())
print(f"\nFinal KG: {stats.get('totalNodes')} nodes, {stats.get('totalEdges')} edges")
for rt in stats.get("relationshipTypes", []):
    if "RELATES" in rt.get("type", ""):
        print(f"  {rt['type']}: {rt['count']}")
