import urllib.request, json
BASE = "https://graph-api.q08.workers.dev"
H = {"User-Agent": "Mozilla/5.0"}

# Check Zenodo nodes with 213 in them
r = urllib.request.Request(f"{BASE}/nodes?label=ZenodoRecord&search=213", headers=H)
d = json.loads(urllib.request.urlopen(r, timeout=15).read())
print("=== ZENODO NODES with '213' ===")
for n in d.get("nodes", []):
    doi = n.get("properties", {}).get("doi", "N/A")
    nid = n.get("id", "?")
    print(f"  id={nid:40s} doi={doi}")

# Check kepler-program neighbors for Zenodo edges
r2 = urllib.request.Request(f"{BASE}/neighbors/kepler-program", headers=H)
d2 = json.loads(urllib.request.urlopen(r2, timeout=15).read())
print("\n=== KEPLER-PROGRAM NEIGHBORS ===")
for n in d2.get("neighbors", []):
    lbl = n.get("label", "?")
    name = n.get("name", "?")
    rt = n.get("relationship_type", "?")
    print(f"  {lbl:20s} {name:50s} [{rt}]")

# Check papers sitemap
try:
    import re
    r3 = urllib.request.Request("https://papers.qnfo.org/sitemap.xml", headers=H)
    sm = urllib.request.urlopen(r3, timeout=15).read().decode()
    slugs = re.findall(r"<loc>https://papers\.qnfo\.org/([^<]+)</loc>", sm)
    print(f"\n=== PAPERS SITEMAP: {len(slugs)} papers ===")
    for s in slugs[:15]:
        print(f"  - {s}")
except Exception as e:
    print(f"\nSitemap: {e}")

# Check llms.txt
try:
    r4 = urllib.request.Request("https://papers.qnfo.org/llms.txt", headers=H)
    ll = urllib.request.urlopen(r4, timeout=15).read().decode()
    lines = [l for l in ll.strip().split("\n") if l.strip()]
    print(f"\n=== llms.txt: {len(lines)} lines ===")
    for l in lines[:10]:
        print(f"  {l[:120]}")
except Exception as e:
    print(f"\nllms.txt: {e}")
