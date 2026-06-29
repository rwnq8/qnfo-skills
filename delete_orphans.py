"""Compute orphan vector diff and delete them."""
import json
import urllib.request

UA = "QNFO-Phase2/1.0"
ASK_QWAV = "https://ask-qwav.q08.workers.dev"

# Get paper IDs from worker
print("Fetching paper IDs...")
req = urllib.request.Request(f"{ASK_QWAV}/api/vector-list", headers={"User-Agent": UA})
with urllib.request.urlopen(req, timeout=30) as resp:
    paper_data = json.loads(resp.read())
paper_ids = set(paper_data["paper_ids"])
print(f"Paper IDs: {len(paper_ids)}")

# Get vector IDs from file
with open("_vector_ids.json") as f:
    vector_ids = set(json.load(f))
print(f"Vector IDs: {len(vector_ids)}")

# Compute diff
orphans = vector_ids - paper_ids
matched = vector_ids & paper_ids
missing = paper_ids - vector_ids

print(f"\nOrphans (vectors not in papers): {len(orphans)}")
print(f"Matched (vectors with papers): {len(matched)}")
print(f"Missing (papers not in vectors): {len(missing)}")

# Show sample orphans
orphan_list = sorted(orphans)
print(f"\nSample orphans (first 20):")
for o in orphan_list[:20]:
    print(f"  {o}")

# Delete orphans via worker endpoint
if orphans:
    orphan_list = list(orphans)
    print(f"\nDeleting {len(orphan_list)} orphans via /api/vector-purge...")
    
    batch_size = 50
    total_deleted = 0
    
    for i in range(0, len(orphan_list), batch_size):
        batch = orphan_list[i:i+batch_size]
        body = json.dumps({"ids": batch}).encode()
        req = urllib.request.Request(
            f"{ASK_QWAV}/api/vector-purge",
            data=body,
            method="POST",
            headers={"Content-Type": "application/json", "User-Agent": UA}
        )
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                result = json.loads(resp.read())
            deleted = result.get("deleted", 0)
            total_deleted += deleted
            print(f"  Batch {i//batch_size + 1}: deleted {deleted}, remaining: {result.get('remaining', '?')}")
            if result.get("errors"):
                print(f"    Errors: {result['errors']}")
        except Exception as e:
            print(f"  ERROR batch {i//batch_size + 1}: {e}")
    
    print(f"\nTotal deleted: {total_deleted}")
    
    # Verify
    health_req = urllib.request.Request(f"{ASK_QWAV}/api/health", headers={"User-Agent": UA})
    with urllib.request.urlopen(health_req, timeout=10) as resp:
        health = json.loads(resp.read())
    print(f"Health check: {health}")
else:
    print("No orphans to delete!")
