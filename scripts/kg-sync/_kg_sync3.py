"""
KG Sync Phase 3: Fix FK errors, add old→new phase links, paper cross-ref
"""
import urllib.request, json

BASE_KG = "https://graph-api.q08.workers.dev"
HEADERS = {"User-Agent": "Mozilla/5.0", "Content-Type": "application/json"}

def kg_get(path):
    req = urllib.request.Request(BASE_KG + path, headers={"User-Agent": "Mozilla/5.0"})
    return json.loads(urllib.request.urlopen(req, timeout=20).read())

def kg_post(path, body):
    data = json.dumps(body).encode()
    req = urllib.request.Request(BASE_KG + path, data=data, method="POST", headers=HEADERS)
    return json.loads(urllib.request.urlopen(req, timeout=20).read())

###############################################################################
# 1. CHECK ZENODO NODE IDs
###############################################################################
print("=== ZENODO NODES IN KG ===")
zr = kg_get("/nodes?label=ZenodoRecord")
zenodo_nodes = {}
for z in zr.get("nodes", []):
    zid = z.get("id", "?")
    doi = z.get("properties", {}).get("doi", "")
    if isinstance(doi, str):
        zenodo_nodes[doi] = z
    print(f"  id={zid:30s} doi={doi}")

###############################################################################
# 2. FIX ZENODO EDGES — use correct node IDs
###############################################################################
print("\n=== FIXING ZENODO EDGES ===")
target_dois = {
    "zenodo-21304469": "10.5281/zenodo.21304469",
    "zenodo-20109836": "10.5281/zenodo.20109836",
    "zenodo-21120469": "10.5281/zenodo.21120469",
    "zenodo-21314315": "10.5281/zenodo.21314315",
}

phase_to_doi = {
    "kepler-p1-oft-foundations": ("10.5281/zenodo.21304469", "zenodo-21304469"),
    "kepler-p2-qec-architecture": ("10.5281/zenodo.20109836", "zenodo-20109836"),
    "kepler-p8-reentry-temporal": ("10.5281/zenodo.21120469", "zenodo-21120469"),
    "kepler-p10-synthesis-capstone": ("10.5281/zenodo.21314315", "zenodo-21314315"),
}

edges_to_add = []
edge_counter = 92000

for phase_id, (doi, expected_zid) in phase_to_doi.items():
    # Find the actual Zenodo node
    actual_zid = None
    for z_d, z_node in zenodo_nodes.items():
        if z_d == doi:
            actual_zid = z_node.get("id")
            break

    if actual_zid:
        print(f"  {phase_id} → {actual_zid} (doi={doi})")
        edges_to_add.append({
            "id": f"edge-{edge_counter}",
            "source_id": phase_id,
            "target_id": actual_zid,
            "relationship_type": "PUBLISHED_AS",
            "properties": {"doi": doi}
        })
        edge_counter += 1
    else:
        print(f"  MISSING Zenodo node for doi={doi}")

if edges_to_add:
    result = kg_post("/sync", {
        "action": "bulk",
        "nodes": [],
        "edges": edges_to_add
    })
    print(f"Result: upserted={result.get('upserted_edges',0)}, errors={result.get('errors',[])}")

###############################################################################
# 3. LINK OLD PHASE NODES → NEW (REFINES)
###############################################################################
print("\n=== LINKING OLD PHASES → NEW ===")
old_phase_map = {
    "phase-1-ostrowski-proof": "kepler-p1-oft-foundations",
    "phase-2-file-ip": "kepler-p2-qec-architecture",
    "phase-3-hensel-code": "kepler-p3-multi-prime-hensel",
    "phase-4-pw-experiment": "kepler-p4-quantum-hardware",
    "phase-5-silent-radix-memory": "kepler-p5-silent-radix-bmr",
    "phase-6-dimensionless": "kepler-p6-planck-informatics",
    "phase-7-fmo-bridge": "kepler-p7-2adic-signal-posner",
    "phase-8-cross-cutting": "kepler-p8-reentry-temporal",
    "phase-9-infrastructure": "kepler-p9-infrastructure",
    "phase-10-synthesis": "kepler-p10-synthesis-capstone",
}

link_edges = []
for old_id, new_id in old_phase_map.items():
    link_edges.append({
        "id": f"edge-{edge_counter}",
        "source_id": new_id,
        "target_id": old_id,
        "relationship_type": "REFINES",
        "properties": {"iteration": "v4 → successor of v3"}
    })
    edge_counter += 1
    print(f"  {new_id} REFINES {old_id}")

result = kg_post("/sync", {"action": "bulk", "nodes": [], "edges": link_edges})
print(f"REFINES edges: upserted={result.get('upserted_edges',0)}")

###############################################################################
# 4. TRY PAPERS CROSS-REFERENCE VIA papers-server
###############################################################################
print("\n=== PAPERS CROSS-REFERENCE ===")
# The papers site returns HTML - let's try the sitemap
try:
    sitemap_req = urllib.request.Request(
        "https://papers.qnfo.org/sitemap.xml",
        headers={"User-Agent": "Mozilla/5.0"}
    )
    sitemap = urllib.request.urlopen(sitemap_req, timeout=15).read().decode()
    paper_count = sitemap.count("<url>")
    print(f"Sitemap: {paper_count} paper URLs")
    # Extract first few paper slugs
    import re
    slugs = re.findall(r"/papers/([^<]+)</loc>", sitemap)
    print(f"Paper slugs found: {len(slugs)}")
    for s in slugs[:10]:
        print(f"  - {s}")
except Exception as e:
    print(f"Sitemap error: {e}")

# Try llms.txt
try:
    llms_req = urllib.request.Request(
        "https://papers.qnfo.org/llms.txt",
        headers={"User-Agent": "Mozilla/5.0"}
    )
    llms = urllib.request.urlopen(llms_req, timeout=15).read().decode()
    # Count entries
    lines = llms.strip().split("\n")
    print(f"\nllms.txt: {len(lines)} lines")
    # Show a few
    for line in lines[:20]:
        print(f"  {line[:100]}")
except Exception as e:
    print(f"llms.txt error: {e}")

###############################################################################
# 5. FINAL STATE
###############################################################################
print("\n=== FINAL STATE ===")
stats = kg_get("/stats")
print(f"Nodes: {stats['totalNodes']}  Edges: {stats['totalEdges']}")

# Check Kepler neighbors
kepler = kg_get("/neighbors/kepler-program")
nbs = kepler.get("neighbors", [])
print(f"\nKepler Program: {len(nbs)} neighbors")
for n in nbs:
    print(f"  {n.get('label','?'):20s} {n.get('name','?'):50s} [{n.get('relationship_type','?')}]")
