"""KG Sync Phase 4: Fix Zenodo FK edges + seed papers"""
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
# 1. FIND ACTUAL ZENODO NODE IDs FOR KEPLER DOIs
###############################################################################
print("=== ZENODO NODE ID MAP ===")
zr = kg_get("/nodes?label=ZenodoRecord&search=zenodo.213")
zr2 = kg_get("/nodes?label=ZenodoRecord&search=zenodo.201")
zr3 = kg_get("/nodes?label=ZenodoRecord&search=zenodo.211")
all_z = zr.get("nodes", []) + zr2.get("nodes", []) + zr3.get("nodes", [])

zenodo_id_map = {}  # doi -> actual node ID
for n in all_z:
    doi = n.get("properties", {}).get("doi", "")
    nid = n.get("id", "")
    if isinstance(doi, str) and doi:
        zenodo_id_map[doi] = nid
        print(f"  {doi:40s} → {nid}")

###############################################################################
# 2. CREATE ZENODO → PHASE EDGES WITH CORRECT IDs
###############################################################################
kepler_zenodo = {
    "10.5281/zenodo.21304469": "kepler-p1-oft-foundations",
    "10.5281/zenodo.20109836": "kepler-p2-qec-architecture",
    "10.5281/zenodo.21120469": "kepler-p8-reentry-temporal",
    "10.5281/zenodo.21314315": "kepler-p10-synthesis-capstone",
}

edges = []
ec = 93000
for doi, phase_id in kepler_zenodo.items():
    zn_id = zenodo_id_map.get(doi)
    if zn_id:
        print(f"  {phase_id} PUBLISHED_AS {zn_id}")
        edges.append({
            "id": f"edge-{ec}",
            "source_id": phase_id,
            "target_id": zn_id,
            "relationship_type": "PUBLISHED_AS",
            "properties": {"doi": doi, "verified": True}
        })
        ec += 1
    else:
        print(f"  MISSING: {doi} not found in KG")

if edges:
    result = kg_post("/sync", {"action": "bulk", "nodes": [], "edges": edges})
    print(f"Zenodo edges: upserted={result.get('upserted_edges',0)}, errors={result.get('errors',[])}")

###############################################################################
# 3. PAPER CROSS-REFERENCE
###############################################################################
print("\n=== PAPERS CROSS-REFERENCE ===")
try:
    r = urllib.request.Request("https://papers.qnfo.org/sitemap.xml", headers={"User-Agent": "Mozilla/5.0"})
    sm = urllib.request.urlopen(r, timeout=15).read().decode()
    slugs = re.findall(r"<loc>https://papers\.qnfo\.org/([^<]+)</loc>", sm)
    # Filter out trailing slashes, index, etc.
    paper_slugs = [s for s in slugs if s and s != "/" and not s.endswith("/")]
    print(f"Papers in sitemap: {len(paper_slugs)}")
    
    # Get llms.txt for titles
    try:
        r2 = urllib.request.Request("https://papers.qnfo.org/llms.txt", headers={"User-Agent": "Mozilla/5.0"})
        ll = urllib.request.urlopen(r2, timeout=15).read().decode()
        # Parse: typically "slug: Title — DOI: 10.xxx"
        ll_entries = {}
        for line in ll.strip().split("\n"):
            if ":" in line and not line.startswith("#"):
                parts = line.split(":", 1)
                slug = parts[0].strip()
                rest = parts[1].strip()
                ll_entries[slug] = rest
        print(f"llms.txt entries with titles: {len(ll_entries)}")
    except:
        ll_entries = {}

    # Seed top 50 papers as Paper nodes in KG
    paper_nodes = []
    paper_edges = []
    pc = 94000

    for slug in paper_slugs[:50]:
        paper_id = f"paper-{slug}"
        title_info = ll_entries.get(slug, slug)
        # Extract DOI if present
        doi_match = re.search(r"(10\.\d{4,}/[^\s]+)", title_info)
        paper_doi = doi_match.group(1) if doi_match else None

        paper_nodes.append({
            "id": paper_id,
            "label": "Paper",
            "name": slug,
            "properties": {
                "title": title_info[:200],
                "doi": paper_doi or "",
                "source": "papers-sitemap",
                "indexed": "2026-07-12"
            }
        })
        # Link to kepler-program if relevant
        if any(kw in slug.lower() for kw in ["ultrametric", "p-adic", "qec", "hensel", "bruhat", "adelic", "quantum"]):
            paper_edges.append({
                "id": f"edge-{pc}",
                "source_id": paper_id,
                "target_id": "kepler-program",
                "relationship_type": "RELATES_TO",
                "properties": {}
            })
            pc += 1

    print(f"\nSeeding {len(paper_nodes)} paper nodes + {len(paper_edges)} edges...")
    if paper_nodes:
        result = kg_post("/sync", {
            "action": "bulk",
            "nodes": paper_nodes,
            "edges": paper_edges
        })
        print(f"Papers result: nodes={result.get('upserted_nodes',0)}, edges={result.get('upserted_edges',0)}, errors={result.get('errors',[])}")
except Exception as e:
    print(f"Papers error: {e}")

###############################################################################
# 4. FINAL VERIFICATION
###############################################################################
print("\n=== FINAL STATE ===")
stats = kg_get("/stats")
print(f"Nodes: {stats['totalNodes']}  Edges: {stats['totalEdges']}")

# Kepler neighbor summary
kepler = kg_get("/neighbors/kepler-program")
nbs = kepler.get("neighbors", [])
by_label = {}
for n in nbs:
    lbl = n.get("label", "?")
    by_label[lbl] = by_label.get(lbl, 0) + 1
print(f"\nKepler Program — {len(nbs)} neighbors by label:")
for lbl, cnt in sorted(by_label.items()):
    print(f"  {lbl}: {cnt}")

print("\n=== DONE ===")
