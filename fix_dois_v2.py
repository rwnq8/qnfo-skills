"""FIX v2: Generate DOIs with proper Zenodo publish via file upload approach.
Creates deposition → uploads placeholder README → sets metadata → PUBLISHES.
This is the proven approach from zenodo_publish.py.
"""
import json, urllib.request, urllib.error, time, sys
from pathlib import Path

ZENODO = "https://zenodo.org/api"
ASK_QWAV = "https://ask-qwav.q08.workers.dev"
UA = "QNFO-DOI-v2/1.0"
DELAY = 2.0

token = (Path.home() / ".zenodo_token").read_text().strip()

# Get ALL papers via pagination (API caps at 100)
print("Fetching papers...")
all_papers = []
for offset in [0, 100]:
    req = urllib.request.Request(f"{ASK_QWAV}/api/papers?limit=100&offset={offset}", headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read())
    batch = data.get("data", [])
    all_papers.extend(batch)
    if len(batch) < 100:
        break
papers = all_papers
print(f"Processing {len(papers)} papers")

dois_created = 0
errors = []

PLACEHOLDER = b"# QNFO Research Paper\n\nFull text and metadata at https://qnfo.org\nThis is an auto-indexed Zenodo record.\n"

for idx, paper in enumerate(papers):
    paper_id = paper["id"]
    title = (paper.get("title") or "Untitled")[:250]
    
    try:
        # Step 1: Create deposition
        dep_req = urllib.request.Request(f"{ZENODO}/deposit/depositions",
            data=json.dumps({}).encode(), method="POST",
            headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"})
        with urllib.request.urlopen(dep_req, timeout=30) as r:
            dep = json.loads(r.read())
        dep_id = dep["id"]
        bucket = dep["links"]["bucket"]
        
        # Step 2: Upload placeholder file
        file_req = urllib.request.Request(f"{bucket}/README.md",
            data=PLACEHOLDER, method="PUT",
            headers={"Authorization": f"Bearer {token}", "Content-Type": "application/octet-stream"})
        with urllib.request.urlopen(file_req, timeout=30) as r:
            pass  # File uploaded
        
        # Step 3: Set metadata
        authors_raw = paper.get("authors", "") or ""
        try:
            authors_list = json.loads(authors_raw) if isinstance(authors_raw, str) else authors_raw
        except:
            authors_list = ["Rowan Quni-Gudzinas"]
        if not authors_list:
            authors_list = ["Rowan Quni-Gudzinas"]
        
        creators = []
        for a in (authors_list if isinstance(authors_list, list) else [str(authors_list)]):
            name = a.strip() if isinstance(a, str) else a.get("name", str(a))
            creators.append({"name": name, "affiliation": "QNFO Research"})
        
        keywords = ["QNFO", "research"]
        for kw in ["quantum","ultrametric","p-adic","physics","mathematics","information",
                     "philosophy","autaxic","trilemma","reality","cosmology","wave","field"]:
            if kw in title.lower() and kw not in keywords:
                keywords.append(kw)
        
        abstract = (paper.get("abstract") or f"Research paper: {title}")[:2000]
        meta = {"metadata": {
            "title": title,
            "upload_type": "publication",
            "publication_type": "preprint",
            "description": abstract,
            "creators": creators[:5],
            "access_right": "open",
            "license": "cc-by-4.0",
            "keywords": keywords[:10],
            "notes": f"QNFO auto-indexed paper. ID: {paper_id}"
        }}
        
        meta_req = urllib.request.Request(f"{ZENODO}/deposit/depositions/{dep_id}",
            data=json.dumps(meta).encode(), method="PUT",
            headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"})
        with urllib.request.urlopen(meta_req, timeout=30) as r:
            pass
        
        # Step 4: PUBLISH
        pub_req = urllib.request.Request(f"{ZENODO}/deposit/depositions/{dep_id}/actions/publish",
            data=b"", method="POST",
            headers={"Authorization": f"Bearer {token}"})
        with urllib.request.urlopen(pub_req, timeout=30) as r:
            pub = json.loads(r.read())
        
        doi = pub.get("metadata",{}).get("prereserve_doi",{}).get("doi") or pub.get("doi")
        zenodo_url = pub.get("links",{}).get("html", f"https://zenodo.org/records/{dep_id}")
        
        if doi:
            # Update D1
            up = json.dumps({"paper_id": paper_id, "doi": doi, "zenodo_url": zenodo_url}).encode()
            up_req = urllib.request.Request(f"{ASK_QWAV}/api/paper-doi",
                data=up, method="POST",
                headers={"Content-Type": "application/json", "User-Agent": UA})
            with urllib.request.urlopen(up_req, timeout=15) as r:
                pass
            dois_created += 1
            print(f"  [{idx+1}/{len(papers)}] ✅ {title[:50]}... → {doi}")
        else:
            errors.append(f"{paper_id}: no DOI in response")
            print(f"  [{idx+1}/{len(papers)}] ❌ {title[:50]}... no DOI")
        
        time.sleep(DELAY)
        
    except urllib.error.HTTPError as e:
        body = e.read().decode()[:300]
        errors.append(f"{paper_id}: HTTP {e.code}")
        print(f"  [{idx+1}/{len(papers)}] ❌ {paper_id}: HTTP {e.code} {body[:80]}")
        time.sleep(DELAY)
    except Exception as e:
        errors.append(f"{paper_id}: {str(e)[:100]}")
        print(f"  [{idx+1}/{len(papers)}] ❌ {paper_id}: {e}")
        time.sleep(DELAY)

print(f"\n{'='*60}")
print(f"RESULTS: {dois_created} DOIs published, {len(errors)} errors")
for e in errors[:5]:
    print(f"  - {e}")

# Verify
try:
    req = urllib.request.Request(f"{ASK_QWAV}/api/stats", headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=10) as r:
        s = json.loads(r.read())
    print(f"\nFinal: {s.get('stats',{})}")
except:
    pass
