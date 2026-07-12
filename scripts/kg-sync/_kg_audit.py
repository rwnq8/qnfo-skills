import urllib.request, json, sys

BASE = "https://graph-api.q08.workers.dev"
HEADERS = {"User-Agent": "Mozilla/5.0"}

def get(path):
    r = urllib.request.Request(BASE + path, headers=HEADERS)
    return json.loads(urllib.request.urlopen(r, timeout=20).read())

# 1. All Project nodes
print("=== KG PROJECT NODES ===")
data = get("/nodes?label=Project")
projects = {p["name"]: p for p in data.get("nodes", [])}
for name in sorted(projects.keys()):
    p = projects[name]
    s = p.get("properties", {}).get("status", "N/A")
    pid = p.get("id", "")
    print(f"  {name:45s} status={s:20s} id={pid}")

# 2. ZenodoRecord nodes (first 30)
print("\n=== KG ZENODO RECORDS (first 30) ===")
data2 = get("/nodes?label=ZenodoRecord")
shown = 0
for z in data2.get("nodes", []):
    if shown >= 30:
        break
    doi = z.get("properties", {}).get("doi", "N/A")
    title = z.get("properties", {}).get("title", "")[:80]
    print(f"  {z['name']:50s} doi={doi}")
    shown += 1

# 3. Phase nodes
print("\n=== KG PHASES ===")
data3 = get("/nodes?label=Phase")
for p in data3.get("nodes", []):
    pid = p.get("id", "")
    print(f"  {p['name']:40s} id={pid}")

# 4. Skill nodes
print("\n=== KG SKILLS ===")
data4 = get("/nodes?label=Skill")
for s in data4.get("nodes", []):
    sid = s.get("id", "")
    print(f"  {s['name']:40s} id={sid}")

# 5. Task nodes
print("\n=== KG TASKS (first 30) ===")
data5 = get("/nodes?label=Task")
for t in data5.get("nodes", [])[:30]:
    tid = t.get("id", "")
    print(f"  {t['name']:50s} id={tid}")

# Summary
print(f"\n=== SUMMARY ===")
print(f"Projects:    {len(projects)}")
print(f"ZenodoRecs:  {len(data2.get('nodes',[]))}")
print(f"Phases:      {len(data3.get('nodes',[]))}")
print(f"Skills:      {len(data4.get('nodes',[]))}")
print(f"Tasks:       {len(data5.get('nodes',[]))}")
