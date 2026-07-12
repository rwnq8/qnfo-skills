"""GitHub repo cross-reference"""
import json, urllib.request

BASE = "https://graph-api.q08.workers.dev"
H = {"User-Agent": "Mozilla/5.0", "Content-Type": "application/json"}

def kg_post(path, body):
    data = json.dumps(body).encode()
    req = urllib.request.Request(BASE + path, data=data, method="POST", headers=H)
    return json.loads(urllib.request.urlopen(req, timeout=20).read())

repos = ["rwnq8/qnfo-skills", "rwnq8/ultrametric-foundation", "rwnq8/qnfo-core", "rwnq8/kepler-program"]

nodes = []
edges = []
ec = 96000

for repo in repos:
    try:
        req = urllib.request.Request(
            f"https://api.github.com/repos/{repo}",
            headers={"User-Agent": "QNFO-KG-Sync", "Accept": "application/vnd.github+json"})
        resp = json.loads(urllib.request.urlopen(req, timeout=10).read())
        if resp.get("full_name"):
            desc = resp.get("description", "")[:200]
            stars = resp.get("stargazers_count", 0)
            updated = resp.get("updated_at", "N/A")
            print(f"  {repo}: stars={stars}, updated={updated}")
            nid = f"github-{repo.replace('/', '-')}"
            nodes.append({
                "id": nid, "label": "CloudflareAsset", "name": repo,
                "properties": {"type": "GitHubRepo", "description": desc, "stars": stars, "updated_at": updated}
            })
            edges.append({"id": f"edge-{ec}", "source_id": nid, "target_id": "kepler-program", "relationship_type": "BELONGS_TO", "properties": {}})
            ec += 1
        else:
            print(f"  {repo}: NOT FOUND")
    except Exception as e:
        print(f"  {repo}: {type(e).__name__}: {e}")

if nodes:
    result = kg_post("/sync", {"action": "bulk", "nodes": nodes, "edges": edges})
    print(f"Seeded: nodes={result.get('upserted_nodes',0)}, edges={result.get('upserted_edges',0)}")

# Check final paper count
r = urllib.request.Request(BASE + "/stats", headers={"User-Agent": "Mozilla/5.0"})
stats = json.loads(urllib.request.urlopen(r, timeout=10).read())
pn = [x for x in stats.get("nodeLabels", []) if x["label"] == "Paper"]
print(f"\nCurrent Papers: {pn[0]['count'] if pn else 0}")
