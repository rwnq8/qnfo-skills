"""
KG Sync Phase 2: Edge connections, paper cross-ref, GitHub repos
"""
import urllib.request, json, os

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
# 1. CHECK EXISTING PHASE NODES
###############################################################################
print("=== EXISTING KG PHASES ===")
phases_raw = kg_get("/nodes?label=Phase")
existing_phases = {}
for p in phases_raw.get("nodes", []):
    pid = p.get("id", "")
    name = p.get("name", "")
    props = p.get("properties", {})
    existing_phases[name] = p
    if isinstance(props, str):
        print(f"  {name:45s} id={pid:45s} props={props[:50]}")
    else:
        print(f"  {name:45s} id={pid:45s} title={props.get('title', 'N/A')[:50] if props else 'N/A'}")

###############################################################################
# 2. ADD PHASE → KEPLER-PROGRAM EDGES
###############################################################################
print("\n=== ADDING PHASE → KEPLER EDGES ===")

kepler_phase_ids = [
    "kepler-p1-oft-foundations", "kepler-p2-qec-architecture",
    "kepler-p3-multi-prime-hensel", "kepler-p4-quantum-hardware",
    "kepler-p5-silent-radix-bmr", "kepler-p6-planck-informatics",
    "kepler-p7-2adic-signal-posner", "kepler-p8-reentry-temporal",
    "kepler-p9-infrastructure", "kepler-p10-synthesis-capstone"
]

edges_to_add = []
edge_counter = 91000
for phase_id in kepler_phase_ids:
    edges_to_add.append({
        "id": f"edge-{edge_counter}",
        "source_id": phase_id,
        "target_id": "kepler-program",
        "relationship_type": "BELONGS_TO",
        "properties": {"program": "Kepler Program", "iteration": 4}
    })
    edge_counter += 1
    # Cross-phase edges for verification matrix
    cross_links = {
        "kepler-p1-oft-foundations": [
            ("kepler-p3-multi-prime-hensel", "COMPUTATIONALLY_VERIFIES"),
            ("kepler-p8-reentry-temporal", "VALUATION_MAPS_TO"),
        ],
        "kepler-p5-silent-radix-bmr": [
            ("kepler-p8-reentry-temporal", "ISOMORPHIC_TO"),
        ],
        "kepler-p6-planck-informatics": [
            ("kepler-p7-2adic-signal-posner", "HIERARCHICAL_BASIS_OF"),
        ],
        "kepler-p7-2adic-signal-posner": [
            ("kepler-p8-reentry-temporal", "COHERENCE_MAPS_TO"),
        ],
    }
    if phase_id in cross_links:
        for target_id, rel_type in cross_links[phase_id]:
            edges_to_add.append({
                "id": f"edge-{edge_counter}",
                "source_id": phase_id,
                "target_id": target_id,
                "relationship_type": rel_type,
                "properties": {"verified": True, "iteration": 4}
            })
            edge_counter += 1

# Add kepler-program to Zenodo edges
zenodo_edge_data = [
    ("10.5281/zenodo.21304469", "zenodo-21304469", "OFT Theorem Proof"),
    ("10.5281/zenodo.20109836", "zenodo-20109836", "Bruhat-Tits Architecture"),
    ("10.5281/zenodo.21120469", "zenodo-21120469", "Page-Wootters Protocol"),
    ("10.5281/zenodo.21314315", "zenodo-21314315", "Kepler Bundle v3"),
]
for doi, zid, desc in zenodo_edge_data:
    # Phase-to-Zenodo edges
    phase_map = {
        "zenodo-21304469": "kepler-p1-oft-foundations",
        "zenodo-20109836": "kepler-p2-qec-architecture",
        "zenodo-21120469": "kepler-p8-reentry-temporal",
        "zenodo-21314315": "kepler-p10-synthesis-capstone",
    }
    target_phase = phase_map.get(zid, "kepler-program")
    edges_to_add.append({
        "id": f"edge-{edge_counter}",
        "source_id": target_phase,
        "target_id": zid,
        "relationship_type": "PUBLISHED_AS",
        "properties": {"doi": doi}
    })
    edge_counter += 1

if edges_to_add:
    print(f"Adding {len(edges_to_add)} edges...")
    result = kg_post("/sync", {
        "action": "bulk",
        "nodes": [],
        "edges": edges_to_add
    })
    print(f"Result: upserted_edges={result.get('upserted_edges', 0)}, errors={result.get('errors', [])}")
else:
    print("No new edges needed")

###############################################################################
# 3. TRY PAPERS DB CROSS-REFERENCE
###############################################################################
print("\n=== PAPERS DB CROSS-REFERENCE ===")
try:
    # Try multiple endpoints
    for endpoint in ["/api/papers", "/papers", "/", "/index.json"]:
        try:
            papers_req = urllib.request.Request(
                f"https://papers.qnfo.org{endpoint}",
                headers={"User-Agent": "Mozilla/5.0", "Accept": "application/json"}
            )
            resp = urllib.request.urlopen(papers_req, timeout=15)
            content_type = resp.headers.get("Content-Type", "")
            body = resp.read().decode()[:500]
            print(f"  {endpoint}: {resp.status} {content_type[:50]} | {body[:200]}")
        except Exception as e2:
            print(f"  {endpoint}: {type(e2).__name__}: {e2}")
except Exception as e:
    print(f"Papers DB: {e}")

###############################################################################
# 4. GITHUB REPOS
###############################################################################
print("\n=== GITHUB REPOS ===")
# Current repo has qnfo-skills, check for others
import subprocess
try:
    result = subprocess.run(
        ["git", "remote", "-v"],
        capture_output=True, text=True, timeout=10
    )
    print(f"Current remotes:\n{result.stdout.strip()}")
except Exception as e:
    print(f"Git error: {e}")

# Check for known repos
known_repos = [
    "rwnq8/qnfo-skills",
    "rwnq8/qnfo-core",
    "rwnq8/ultrametric-foundation",
    "rwnq8/kepler-program",
]
for repo in known_repos:
    try:
        req = urllib.request.Request(
            f"https://api.github.com/repos/{repo}",
            headers={"User-Agent": "Mozilla/5.0"}
        )
        resp = json.loads(urllib.request.urlopen(req, timeout=10).read())
        print(f"  github.com/{repo}: EXISTS, stars={resp.get('stargazers_count', 0)}, updated={resp.get('updated_at', 'N/A')}")
    except Exception as e:
        print(f"  github.com/{repo}: {type(e).__name__}")

###############################################################################
# 5. FINAL VERIFICATION
###############################################################################
print("\n=== FINAL VERIFICATION ===")
stats = kg_get("/stats")
print(f"Total: {stats['totalNodes']} nodes, {stats['totalEdges']} edges")

# Verify Kepler phases are now connected
try:
    kepler_neighbors = kg_get("/neighbors/kepler-program")
    neighbor_names = [n.get("name", "") for n in kepler_neighbors.get("neighbors", [])]
    neighbor_types = [n.get("relationship_type", "") for n in kepler_neighbors.get("neighbors", [])]
    print(f"Kepler Program neighbors: {len(neighbor_names)}")
    phase_neighbors = [n for n in kepler_neighbors.get("neighbors", []) if n.get("label") == "Phase"]
    print(f"  Connected phases: {len(phase_neighbors)}")
    for pn in phase_neighbors[:15]:
        print(f"    - {pn.get('name', 'N/A')}")
except Exception as e:
    print(f"Neighbor check error: {e}")

print("\nDone!")
