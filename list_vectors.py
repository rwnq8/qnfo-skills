"""Simple script to list all vector IDs from Vectorize index."""
import subprocess, json, sys

index = "qwav-research-v2"
all_ids = []
cursor = None
page = 0

while page < 20:
    page += 1
    args = f"npx wrangler vectorize list-vectors {index} --count 100 --json"
    if cursor:
        args += f" --cursor {cursor}"
    
    result = subprocess.run(args, capture_output=True, text=True, shell=True, timeout=60)
    output = result.stdout.strip() or result.stderr.strip()
    
    try:
        data = json.loads(output)
    except json.JSONDecodeError:
        print(f"ERROR parsing page {page}: {output[:200]}")
        break
    
    vectors = data.get("vectors", [])
    for v in vectors:
        all_ids.append(v["id"])
    
    print(f"Page {page}: +{len(vectors)} vectors, total {len(all_ids)}", flush=True)
    
    if not data.get("isTruncated"):
        break
    cursor = data.get("nextCursor")
    if not cursor:
        break

print(f"\nTOTAL: {len(all_ids)} vectors", flush=True)
with open("_vector_ids.json", "w") as f:
    json.dump(all_ids, f)
print("Saved to _vector_ids.json", flush=True)
