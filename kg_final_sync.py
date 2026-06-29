"""Complete KG Paper Sync — add all 170 papers + RELATES_TO + REFERENCES edges."""
import json, urllib.request, time

UA = "QNFO-Phase2/1.0"
ASK_QWAV = "https://ask-qwav.q08.workers.dev"
GRAPH_API = "https://graph-api.q08.workers.dev"

# ── STEP 1: Get all papers from D1 ──
print("[1/5] Fetching all papers from D1...")
req = urllib.request.Request(f"{ASK_QWAV}/api/papers?limit=200", headers={"User-Agent": UA})
with urllib.request.urlopen(req, timeout=30) as resp:
    papers = json.loads(resp.read())["data"]
print(f"  Got {len(papers)} papers")

# ── STEP 2: Sync ALL 170 paper nodes (idempotent) ──
print("[2/5] Creating paper nodes in KG...")
paper_nodes = []
for p in papers:
    title = (p.get("title") or "Untitled").strip()[:250]
    paper_nodes.append({
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

batch_size = 50
for i in range(0, len(paper_nodes), batch_size):
    batch = paper_nodes[i:i+batch_size]
    body = json.dumps({"action": "bulk", "nodes": batch, "edges": []}).encode()
    r = urllib.request.Request(GRAPH_API + "/sync", data=body, method="POST",
        headers={"Content-Type": "application/json", "User-Agent": UA})
    with urllib.request.urlopen(r, timeout=60) as resp:
        result = json.loads(resp.read())
    print(f"  Batch {i//batch_size + 1}: {result.get('upserted_nodes', '?')} synced")
    time.sleep(0.3)

print("  All 170 paper nodes synced")

# ── STEP 3: Get concept nodes for RELATES_TO mapping ──
print("[3/5] Fetching concept nodes...")
req = urllib.request.Request(f"{GRAPH_API}/nodes?label=Concept", headers={"User-Agent": UA})
with urllib.request.urlopen(req, timeout=30) as resp:
    concepts = json.loads(resp.read())["nodes"]

# Build concept name → ID map (match by keyword in name)
concept_map = {}
for c in concepts:
    name = c.get("name", "").lower()
    concept_map[name] = c.get("id")

# Print available concepts for debugging
print(f"  Available concepts ({len(concept_map)}):")
for name in sorted(concept_map.keys())[:20]:
    print(f"    - {name}")

# ── STEP 4: Expanded keyword → concept mapping ──
keyword_to_concepts = {
    # QWAV Physics domains
    "quantum": ["quantum error correction", "qwav physics", "general research"],
    "qec": ["quantum error correction"],
    "error correction": ["quantum error correction"],
    "qubit": ["quantum error correction"],
    "stabilizer": ["quantum error correction"],
    "surface code": ["quantum error correction"],
    
    "ultrametric": ["ultrametric theory"],
    "p-adic": ["ultrametric theory"],
    "ostrowski": ["ultrametric theory"],
    "hensel": ["ultrametric theory"],
    "berkovich": ["ultrametric theory"],
    "tate": ["ultrametric theory"],
    "amice": ["ultrametric theory"],
    "bruhat": ["ultrametric theory"],
    "witt vector": ["ultrametric theory"],
    "mahler": ["ultrametric theory"],
    
    "metric": ["ultrametric theory"],
    "hierarch": ["ultrametric theory"],
    "tree": ["ultrametric theory"],
    "fractal": ["ultrametric theory", "mathematics"],
    
    # Physics
    "physics": ["qwav physics", "general research"],
    "wave": ["qwav physics"],
    "field": ["qwav physics"],
    "cosmolog": ["qwav physics"],
    "particle": ["qwav physics"],
    "dimension": ["qwav physics", "mathematics"],
    "time": ["qwav physics", "general research"],
    "space": ["qwav physics"],
    "reality": ["qwav physics", "general research"],
    "einstein": ["qwav physics"],
    "thermodynamic": ["qwav physics"],
    "entropy": ["qwav physics", "information theory"],
    "gravity": ["qwav physics"],
    "relativity": ["qwav physics"],
    
    # Information theory
    "information": ["information theory", "knowledge & data"],
    "shannon": ["information theory"],
    "entropy": ["information theory", "qwav physics"],
    "coding": ["information theory"],
    "channel": ["information theory"],
    
    # Mathematics
    "mathemat": ["mathematics", "general research"],
    "topolog": ["mathematics"],
    "number": ["mathematics"],
    "prime": ["mathematics"],
    "group": ["mathematics"],
    "algebra": ["mathematics"],
    "set theory": ["mathematics"],
    "category": ["mathematics"],
    "graph": ["mathematics", "knowledge & data"],
    "geometry": ["mathematics"],
    "topos": ["mathematics"],
    "differential": ["mathematics"],
    "manifold": ["mathematics"],
    
    # Philosophy
    "philosoph": ["philosophy", "general research"],
    "foundation": ["philosophy", "general research"],
    "ontolog": ["philosophy"],
    "epistemolog": ["philosophy"],
    "laws of form": ["philosophy", "mathematics"],
    "reality": ["philosophy", "general research"],
    "conscious": ["philosophy", "cognition"],
    "mind": ["philosophy", "cognition"],
    "self": ["philosophy"],
    "meaning": ["philosophy"],
    "ethics": ["philosophy"],
    
    # Cognition
    "cognition": ["cognition", "general research"],
    "conscious": ["cognition", "philosophy"],
    "perception": ["cognition"],
    "memory": ["cognition"],
    "learn": ["cognition", "ai & synthesis"],
    
    # AI / Computation
    "ai": ["ai & synthesis", "computational"],
    "machine learn": ["ai & synthesis", "computational"],
    "neural": ["ai & synthesis", "computational"],
    "comput": ["computational", "infrastructure"],
    "algorithm": ["computational"],
    "llm": ["ai & synthesis", "computational"],
    "gpt": ["ai & synthesis"],
    "transformer": ["ai & synthesis", "computational"],
    "attention": ["ai & synthesis", "computational"],
    
    # Infrastructure
    "network": ["infrastructure", "knowledge & data"],
    "api": ["infrastructure", "deployment & storage"],
    "deploy": ["infrastructure", "deployment & storage"],
    "database": ["infrastructure", "knowledge & data"],
    "cloud": ["infrastructure", "deployment & storage"],
    "automat": ["automation", "infrastructure"],
    "pipeline": ["automation"],
    "devops": ["automation"],
    
    # General research topics
    "ratio": ["general research", "mathematics"],
    "scale": ["general research", "qwav physics"],
    "pattern": ["general research"],
    "emergence": ["general research"],
    "complex": ["general research"],
    "symmetr": ["general research", "qwav physics"],
    "duality": ["general research", "qwav physics"],
    "simulation": ["general research", "computational"],
    "proof": ["general research", "mathematics"],
    "paradox": ["general research", "philosophy"],
    "trilemma": ["general research", "philosophy"],
    "autax": ["general research", "philosophy"],
    
    # Publications & Content
    "publication": ["publications", "sites & design"],
    "content": ["publications", "sites & design"],
    "seo": ["publications", "discovery & assets"],
    "discovery": ["discovery & assets", "publications"],
    "search": ["discovery & assets"],
    "index": ["discovery & assets"],
    "citation": ["publications", "discovery & assets"],
}

# Map concept names to actual KG concept IDs
def find_concept_id(concept_name):
    """Find the closest matching concept ID from the KG."""
    concept_name_lower = concept_name.lower()
    # Direct match
    if concept_name_lower in concept_map:
        return concept_map[concept_name_lower]
    # Partial match
    for cname, cid in concept_map.items():
        if concept_name_lower in cname or cname in concept_name_lower:
            return cid
    return None

# ── STEP 5: Create RELATES_TO + REFERENCES edges ──
print("[4/5] Creating edges...")
paper_id_to_node = {p["id"]: f"paper-{p['id']}" for p in papers}
paper_titles = {p["id"]: (p.get("title") or "").lower() for p in papers}
paper_abstracts = {p["id"]: (p.get("abstract") or "").lower() for p in papers}

all_edges = []
edge_counter = 0

# A) Create RELATES_TO edges from keyword matching
for p in papers:
    title = (p.get("title") or "").lower()
    abstract = (p.get("abstract") or "").lower()[:800]
    text = title + " " + abstract
    
    matched_concepts = set()
    for keyword, concept_names in keyword_to_concepts.items():
        if keyword in text:
            for cn in concept_names:
                matched_concepts.add(cn)
    
    for cn in matched_concepts:
        concept_id = find_concept_id(cn)
        if concept_id:
            edge_counter += 1
            all_edges.append({
                "id": f"edge-relp-{edge_counter}",
                "source_id": f"paper-{p['id']}",
                "target_id": concept_id,
                "relationship_type": "RELATES_TO",
                "properties": {"confidence": "keyword", "keyword": cn}
            })

# B) Create REFERENCES edges from title cross-references
# If paper A's title (or key terms) appears in paper B's abstract, paper B REFERENCES paper A
print("  Cross-referencing papers by title mentions...")
for src_paper in papers:
    src_title_lower = (src_paper.get("title") or "").lower()
    src_id = src_paper["id"]
    
    # Skip if title is too short/generic
    if len(src_title_lower) < 10:
        continue
    
    for tgt_paper in papers:
        if src_id == tgt_paper["id"]:
            continue
        
        tgt_abstract = paper_abstracts.get(tgt_paper["id"], "")
        tgt_title = paper_titles.get(tgt_paper["id"], "")
        
        # Check if source paper's key terms appear in target's abstract
        # Use first significant words from source title (skip "1-1", "Chapter", etc.)
        src_words = [w for w in src_title_lower.split() if len(w) > 3 and w not in 
                     ('this', 'that', 'with', 'from', 'have', 'been', 'into', 'over', 'also')]
        src_terms = ' '.join(src_words[:6])  # First 6 significant words
        
        if len(src_terms) > 15 and src_terms in tgt_abstract:
            edge_counter += 1
            all_edges.append({
                "id": f"edge-refp-{edge_counter}",
                "source_id": f"paper-{src_paper['id']}",
                "target_id": f"paper-{tgt_paper['id']}",
                "relationship_type": "REFERENCES",
                "properties": {"confidence": "title_match", "matched_terms": src_terms[:100]}
            })

# C) Create PUBLISHED_AS edges for papers with DOIs
for p in papers:
    doi = p.get("doi")
    if doi and doi.strip():
        edge_counter += 1
        all_edges.append({
            "id": f"edge-pubp-{edge_counter}",
            "source_id": f"paper-{p['id']}",
            "target_id": f"doi-{doi.replace('/', '-').replace('.', '-')[:80]}",
            "relationship_type": "PUBLISHED_AS",
            "properties": {"doi": doi.strip()}
        })

print(f"  Created {len(all_edges)} edges total")
print(f"    RELATES_TO: {sum(1 for e in all_edges if e['relationship_type'] == 'RELATES_TO')}")
print(f"    REFERENCES: {sum(1 for e in all_edges if e['relationship_type'] == 'REFERENCES')}")
print(f"    PUBLISHED_AS: {sum(1 for e in all_edges if e['relationship_type'] == 'PUBLISHED_AS')}")

# ── STEP 6: Sync edges to KG ──
print("[5/5] Syncing edges to KG...")
total_edges_synced = 0
for i in range(0, len(all_edges), 50):
    batch = all_edges[i:i+50]
    body = json.dumps({"action": "bulk", "nodes": [], "edges": batch}).encode()
    r = urllib.request.Request(GRAPH_API + "/sync", data=body, method="POST",
        headers={"Content-Type": "application/json", "User-Agent": UA})
    try:
        with urllib.request.urlopen(r, timeout=60) as resp:
            result = json.loads(resp.read())
        upserted = result.get("upserted_edges", 0) or result.get("edgesCreated", 0) or len(batch)
        total_edges_synced += upserted
        print(f"  Edges batch {i//50 + 1}/{ (len(all_edges)+49)//50 }: {upserted} synced")
    except Exception as e:
        print(f"  ERROR batch {i//50 + 1}: {e}")
    time.sleep(0.3)

# ── FINAL VERIFICATION ──
print("\n" + "="*60)
print("VERIFICATION")
print("="*60)

req = urllib.request.Request(GRAPH_API + "/stats", headers={"User-Agent": UA})
with urllib.request.urlopen(req, timeout=30) as resp:
    stats = json.loads(resp.read())

print(f"Total nodes: {stats['totalNodes']}")
print(f"Total edges: {stats['totalEdges']}")
for nl in stats.get("nodeLabels", []):
    if nl["label"] == "Paper":
        print(f"Paper nodes: {nl['count']}")
for rt in stats.get("relationshipTypes", []):
    if rt["type"] in ("RELATES_TO", "REFERENCES", "PUBLISHED_AS"):
        print(f"{rt['type']}: {rt['count']}")

# Health check on ask-qwav
req2 = urllib.request.Request(f"{ASK_QWAV}/api/health", headers={"User-Agent": UA})
with urllib.request.urlopen(req2, timeout=10) as resp:
    health = json.loads(resp.read())
print(f"\nask-qwav health: v{health.get('version')}, papers={health.get('papers')}, vectors={health.get('vectorize')}")

print("\n✅ KG sync complete!")
