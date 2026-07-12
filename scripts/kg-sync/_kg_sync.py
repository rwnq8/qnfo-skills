"""
KG Cross-Reference & Update Script
Queries: KG API, Zenodo API, Papers DB, GitHub
Identifies missing nodes/edges, seeds them into KG
"""
import urllib.request, json, os, sys

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
# 1. CURRENT KG STATE
###############################################################################
print("=" * 70)
print("PHASE 1: Current KG State")
print("=" * 70)

stats = kg_get("/stats")
print(f"Nodes: {stats['totalNodes']}  Edges: {stats['totalEdges']}")

projects_raw = kg_get("/nodes?label=Project")
kg_projects = {}
for p in projects_raw.get("nodes", []):
    kg_projects[p["name"]] = p
print(f"KG Projects: {len(kg_projects)}")

zenodo_raw = kg_get("/nodes?label=ZenodoRecord")
kg_zenodo = {}
for z in zenodo_raw.get("nodes", []):
    doi = z.get("properties", {}).get("doi", "")
    if doi:
        kg_zenodo[doi] = z
print(f"KG Zenodo Records: {len(kg_zenodo)}")

phases_raw = kg_get("/nodes?label=Phase")
kg_phases = {p["name"]: p["id"] for p in phases_raw.get("nodes", [])}
print(f"KG Phases: {len(kg_phases)}")

###############################################################################
# 2. KNOWN ENTITIES FROM WORKSPACE
###############################################################################

# Kepler Program phases
kepler_phases = {
    "kepler-p1-oft-foundations": "Kepler P1: OFT Foundations & Ostrowski",
    "kepler-p2-qec-architecture": "Kepler P2: QEC Architecture & IP",
    "kepler-p3-multi-prime-hensel": "Kepler P3: Multi-Prime Hensel Codec",
    "kepler-p4-quantum-hardware": "Kepler P4: Quantum Hardware",
    "kepler-p5-silent-radix-bmr": "Kepler P5: Silent Radix & BMR",
    "kepler-p6-planck-informatics": "Kepler P6: Planck Informatics",
    "kepler-p7-2adic-signal-posner": "Kepler P7: 2-adic Signal & Posner",
    "kepler-p8-reentry-temporal": "Kepler P8: Re-Entry & Temporal Structure",
    "kepler-p9-infrastructure": "Kepler P9: Infrastructure",
    "kepler-p10-synthesis-capstone": "Kepler P10: Synthesis & Capstone"
}

# Verified Zenodo DOIs
verified_zenodo = {
    "10.5281/zenodo.21304469": "OFT Theorem Proof (Kepler P1)",
    "10.5281/zenodo.20109836": "Bruhat-Tits Architecture (Kepler P2)",
    "10.5281/zenodo.21120469": "Page-Wootters Protocol (Kepler P8)",
    "10.5281/zenodo.21314315": "Kepler Program Complete Bundle (Iteration 3)"
}

# MASTER-INVENTORY Workers (25)
essential_workers = [
    "ask-qwav", "graph-api", "papers-server", "qnfo-lifecycle",
    "qnfo-archive-worker", "qnfo-agent-session", "infra-lock-manager",
    "api-gateway", "qnfo-data-api", "ultrametric-tree-api",
    "qnfo-edge-router", "search-worker", "portfolio-api", "audit-worker",
    "cron-graph-re-seed"
]
support_workers = [
    "qnfo-ai-worker", "paper-pipeline", "murtagh-engine", "braid-matrix",
    "qnfo-infra-mcp", "qnfo-asset-api", "qnfo-analytics-dashboard",
    "archive-worker", "paper-catalog", "qwav-unified"
]
all_workers = essential_workers + support_workers

# Pages projects
pages_projects = [
    "qnfo-hub", "qnfo-publications", "qnfo-legal", "qnfo-design-system",
    "ask-qwav-pages", "qwav", "hensel-code"
]

# D1 databases
d1_databases = [
    "qnfo-audit", "qnfo-graph", "qnfo-cms", "living-paper", "portfolio-state"
]

print(f"\nKepler Phases expected: {len(kepler_phases)}")
print(f"Kepler Phases in KG: {len(kg_phases)}")
missing_phases = [p for p in kepler_phases if p not in kg_phases]
if missing_phases:
    print(f"MISSING PHASES: {missing_phases}")
else:
    print("All Kepler phases already in KG")

missing_zenodo = [d for d in verified_zenodo if d not in kg_zenodo]
if missing_zenodo:
    print(f"MISSING ZENODO DOIs: {missing_zenodo}")
else:
    print("All verified Zenodo DOIs already in KG")

###############################################################################
# 3. ZENODO API CROSS-REFERENCE
###############################################################################
print("\n" + "=" * 70)
print("PHASE 2: Zenodo API Cross-Reference")
print("=" * 70)

try:
    zenodo_req = urllib.request.Request(
        "https://zenodo.org/api/records?q=QNFO&sort=mostrecent&size=20",
        headers={"User-Agent": "Mozilla/5.0"}
    )
    zenodo_data = json.loads(urllib.request.urlopen(zenodo_req, timeout=20).read())
    hits = zenodo_data.get("hits", {}).get("hits", [])
    print(f"Zenodo records matching 'QNFO': {len(hits)}")
    for h in hits[:20]:
        doi = h.get("doi", "")
        title = h.get("metadata", {}).get("title", "N/A")
        in_kg = "IN_KG" if doi in kg_zenodo else "MISSING"
        print(f"  {title[:70]:70s} {doi} [{in_kg}]")
except Exception as e:
    print(f"Zenodo query error: {e}")

###############################################################################
# 4. PAPERS DATABASE CROSS-REFERENCE
###############################################################################
print("\n" + "=" * 70)
print("PHASE 3: Papers Database Cross-Reference")
print("=" * 70)

try:
    papers_req = urllib.request.Request(
        "https://papers.qnfo.org/api/papers?limit=10",
        headers={"User-Agent": "Mozilla/5.0"}
    )
    papers_data = json.loads(urllib.request.urlopen(papers_req, timeout=20).read())
    papers_list = papers_data.get("papers", papers_data.get("results", []))
    print(f"Papers DB (first 10): {len(papers_list)}")
    for p in papers_list[:10]:
        title = p.get("title", "N/A")
        doi = p.get("doi", "N/A")
        print(f"  {title[:70]:70s} {doi}")
except Exception as e:
    print(f"Papers DB error: {e}")

###############################################################################
# 5. GITHUB CROSS-REFERENCE
###############################################################################
print("\n" + "=" * 70)
print("PHASE 4: GitHub Cross-Reference")
print("=" * 70)

# Try to get repo info via git remote
try:
    remote = os.popen("git remote get-url origin 2>&1").read().strip()
    print(f"Current repo: {remote}")
except:
    print("No git remote found in workspace")

###############################################################################
# 6. DIFF SUMMARY
###############################################################################
print("\n" + "=" * 70)
print("PHASE 5: Diff Summary")
print("=" * 70)

# Check Kepler Program project node
kepler_in_kg = "kepler-program" in kg_projects or "Kepler Program" in kg_projects
print(f"Kepler Program project in KG: {kepler_in_kg}")

# Check QNFO Program node
qnfo_in_kg = "qnfo" in kg_projects
print(f"QNFO program node in KG: {qnfo_in_kg}")

# Check key publications
pub_deposits = {
    "ultrametric-foundation": "Ultrametric Foundations Thesis"
}
for pub_id, pub_name in pub_deposits.items():
    in_kg = pub_id in kg_projects
    print(f"Publication '{pub_name}' in KG: {in_kg}")

###############################################################################
# 7. SEED MISSING NODES
###############################################################################
print("\n" + "=" * 70)
print("PHASE 6: Seeding Missing Nodes & Edges")
print("=" * 70)

nodes_to_add = []
edges_to_add = []
edge_counter = 90000

# --- Kepler Phase nodes ---
for phase_id, phase_name in kepler_phases.items():
    if phase_id not in kg_phases:
        nodes_to_add.append({
            "id": phase_id,
            "label": "Phase",
            "name": phase_id,
            "properties": {
                "title": phase_name,
                "program": "Kepler Program",
                "iteration": 4,
                "verified": True
            }
        })
        print(f"  + Phase: {phase_id}")

# --- Kepler Program project ---
if not kepler_in_kg:
    nodes_to_add.append({
        "id": "kepler-program",
        "label": "Project",
        "name": "Kepler Program",
        "properties": {
            "status": "PUBLISHED",
            "last_active": "2026-07-11T00:00:00Z",
            "description": "Adelic Quantum Computing & Ultrametric Physics — Iteration 4 (Verified)",
            "zenodo_doi": "10.5281/zenodo.21314315",
            "iteration": 4
        }
    })
    print("  + Project: kepler-program")

# --- Zenodo records not in KG ---
for doi, desc in verified_zenodo.items():
    if doi not in kg_zenodo:
        zen_id = "zenodo-" + doi.split("/")[-1]
        nodes_to_add.append({
            "id": zen_id,
            "label": "ZenodoRecord",
            "name": f"Zenodo-{doi.split('/')[-1]}",
            "properties": {
                "doi": doi,
                "description": desc,
                "date": "2026-07-11"
            }
        })
        # Edge: ZenodoRecord -> PUBLISHED_AS -> Kepler Program
        edges_to_add.append({
            "id": f"edge-{edge_counter}",
            "source_id": "kepler-program",
            "target_id": zen_id,
            "relationship_type": "PUBLISHED_AS",
            "properties": {"doi": doi}
        })
        edge_counter += 1
        print(f"  + ZenodoRecord + edge: {doi}")

# --- Workers (as CloudflareAsset nodes) ---
existing_workers = set()
for w in all_workers:
    if w in kg_projects:
        existing_workers.add(w)

for w in all_workers:
    worker_id = f"worker-{w}"
    if w not in existing_workers:
        nodes_to_add.append({
            "id": worker_id,
            "label": "CloudflareAsset",
            "name": w,
            "properties": {
                "type": "Worker",
                "tier": "essential" if w in essential_workers else "support",
                "status": "active"
            }
        })
        # Edge: Worker BELONGS_TO kepler-program
        edges_to_add.append({
            "id": f"edge-{edge_counter}",
            "source_id": worker_id,
            "target_id": "kepler-program",
            "relationship_type": "BELONGS_TO",
            "properties": {}
        })
        edge_counter += 1
        print(f"  + Worker: {w}")

# --- Pages projects ---
for page in pages_projects:
    page_id = f"pages-{page}"
    if page not in kg_projects:
        nodes_to_add.append({
            "id": page_id,
            "label": "CloudflareAsset",
            "name": page,
            "properties": {
                "type": "Pages",
                "status": "active"
            }
        })
        edges_to_add.append({
            "id": f"edge-{edge_counter}",
            "source_id": page_id,
            "target_id": "kepler-program",
            "relationship_type": "BELONGS_TO",
            "properties": {}
        })
        edge_counter += 1
        print(f"  + Pages: {page}")

# --- D1 databases ---
for db in d1_databases:
    db_id = f"d1-{db}"
    if db not in kg_projects:
        nodes_to_add.append({
            "id": db_id,
            "label": "CloudflareAsset",
            "name": db,
            "properties": {
                "type": "D1",
                "status": "essential" if db in ["qnfo-audit", "qnfo-graph", "living-paper"] else "support"
            }
        })
        edges_to_add.append({
            "id": f"edge-{edge_counter}",
            "source_id": db_id,
            "target_id": "kepler-program",
            "relationship_type": "BELONGS_TO",
            "properties": {}
        })
        edge_counter += 1
        print(f"  + D1: {db}")

# --- Publication: Ultrametric Foundation ---
if "ultrametric-foundation" not in kg_projects:
    nodes_to_add.append({
        "id": "ultrametric-foundation",
        "label": "Project",
        "name": "ultrametric-foundation",
        "properties": {
            "status": "PUBLISHED",
            "last_active": "2026-07-11T00:00:00Z",
            "description": "Ultrametric Foundations of Quantum Computation — Thesis",
            "type": "publication"
        }
    })
    print("  + Project: ultrametric-foundation")

###############################################################################
# 8. EXECUTE SEED
###############################################################################
if nodes_to_add or edges_to_add:
    print(f"\nSeeding: {len(nodes_to_add)} nodes, {len(edges_to_add)} edges")
    body = {
        "action": "bulk",
        "nodes": nodes_to_add,
        "edges": edges_to_add
    }
    try:
        result = kg_post("/sync", body)
        print(f"Result: {json.dumps(result, indent=2)}")
    except Exception as e:
        print(f"Seed error: {e}")
else:
    print("\nNo new nodes/edges to seed — everything already in KG")

###############################################################################
# 9. VERIFY
###############################################################################
print("\n" + "=" * 70)
print("PHASE 7: Verification")
print("=" * 70)
new_stats = kg_get("/stats")
print(f"BEFORE: {stats['totalNodes']} nodes, {stats['totalEdges']} edges")
print(f"AFTER:  {new_stats['totalNodes']} nodes, {new_stats['totalEdges']} edges")
print(f"DELTA:  +{new_stats['totalNodes'] - stats['totalNodes']} nodes, +{new_stats['totalEdges'] - stats['totalEdges']} edges")
