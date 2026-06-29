"""FIX: Re-generate DOIs with proper Zenodo PUBLISH step.
Previous batch only reserved DOIs (prereserve_doi) without publishing.
This script: create → metadata → PUBLISH → store DOI + zenodo_url in D1.
"""
import json, urllib.request, urllib.error, time, sys
from pathlib import Path

ZENODO_API = "https://zenodo.org/api"
ASK_QWAV = "https://ask-qwav.q08.workers.dev"
UA = "QNFO-DOI-Fix/1.0"
DELAY = 2.5  # seconds between API calls

# Load token
token_path = Path.home() / ".zenodo_token"
if not token_path.exists():
    print("❌ No Zenodo token")
    sys.exit(1)
token = token_path.read_text().strip()

# Get papers without valid DOIs
print("Fetching papers...")
req = urllib.request.Request(f"{ASK_QWAV}/api/papers?limit=200", headers={"User-Agent": UA})
with urllib.request.urlopen(req, timeout=30) as resp:
    papers = json.loads(resp.read())["data"]

# Process ALL papers, overwriting any existing (potentially invalid prereserve) DOIs
# The only paper with a pre-existing valid DOI is "Ultrametric Foundation" — it will be re-published.
# Zenodo creates a new deposition each time, so old invalid ones become orphaned drafts (harmless).
all_papers = [p for p in papers if (p.get("title") or "").strip()]  # All with titles
print(f"Total papers to process: {len(all_papers)}/{len(papers)}")

print(f"\nProcessing {len(all_papers)} papers with PUBLISH step...")
print("=" * 60)

dois_created = 0
errors = []

for idx, paper in enumerate(all_papers):
    paper_id = paper["id"]
    title = (paper.get("title") or "Untitled")[:250]
    
    try:
        # ── Step 1: Create deposition ──
        dep_req = urllib.request.Request(
            f"{ZENODO_API}/deposit/depositions",
            data=json.dumps({"files": {"enabled": False}}).encode(),
            method="POST",
            headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
        )
        with urllib.request.urlopen(dep_req, timeout=30) as resp:
            deposition = json.loads(resp.read())
        dep_id = deposition["id"]
        
        # ── Step 2: Parse authors ──
        authors_raw = paper.get("authors", "") or ""
        try:
            authors_list = json.loads(authors_raw) if isinstance(authors_raw, str) else authors_raw
        except:
            authors_list = ["Rowan Quni-Gudzinas"]
        if not authors_list:
            authors_list = ["Rowan Quni-Gudzinas"]
        
        creators = []
        for author in (authors_list if isinstance(authors_list, list) else [str(authors_list)]):
            if isinstance(author, str):
                creators.append({"name": author.strip(), "affiliation": "QNFO Research"})
            elif isinstance(author, dict):
                creators.append({
                    "name": author.get("name", str(author)),
                    "affiliation": author.get("affiliation", "QNFO Research")
                })
        
        # ── Step 3: Keywords ──
        keywords = ["QNFO", "research"]
        title_lower = title.lower()
        for kw in ["quantum", "ultrametric", "p-adic", "physics", "mathematics",
                     "information", "philosophy", "autaxic", "trilemma", "reality",
                     "cosmology", "wave", "field", "particle", "dimension"]:
            if kw in title_lower and kw not in keywords:
                keywords.append(kw)
        
        # ── Step 4: Set metadata ──
        abstract = (paper.get("abstract") or f"Research paper: {title}")[:2000]
        metadata = {
            "metadata": {
                "title": title,
                "resource_type": {"type": "publication", "title": "Preprint"},
                "description": abstract,
                "creators": creators[:5],
                "access_right": "open",
                "license": "cc-by-4.0",
                "keywords": keywords[:10],
                "notes": f"QNFO auto-indexed paper. Paper ID: {paper_id}"
            }
        }
        
        meta_req = urllib.request.Request(
            f"{ZENODO_API}/deposit/depositions/{dep_id}",
            data=json.dumps(metadata).encode(),
            method="PUT",
            headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
        )
        with urllib.request.urlopen(meta_req, timeout=30) as resp:
            updated = json.loads(resp.read())
        
        # ── Step 5: PUBLISH (THIS IS THE FIX) ──
        pub_req = urllib.request.Request(
            f"{ZENODO_API}/deposit/depositions/{dep_id}/actions/publish",
            data=b"",
            method="POST",
            headers={"Authorization": f"Bearer {token}"}
        )
        with urllib.request.urlopen(pub_req, timeout=30) as resp:
            published = json.loads(resp.read())
        
        # ── Step 6: Extract DOI and zenodo_url ──
        doi = None
        zenodo_url = None
        
        # Try multiple locations for the DOI
        meta = published.get("metadata", {})
        prereserve = meta.get("prereserve_doi", {})
        if isinstance(prereserve, dict):
            doi = prereserve.get("doi")
        if not doi:
            doi = published.get("doi") or meta.get("doi")
        
        # Get Zenodo URL
        links = published.get("links", {})
        zenodo_url = links.get("html") or links.get("record_html") or f"https://zenodo.org/records/{dep_id}"
        
        if doi and zenodo_url:
            # ── Step 7: Update D1 ──
            update_body = json.dumps({
                "paper_id": paper_id,
                "doi": doi,
                "zenodo_url": zenodo_url
            }).encode()
            
            update_req = urllib.request.Request(
                f"{ASK_QWAV}/api/paper-publish",
                data=update_body,
                method="POST",
                headers={"Content-Type": "application/json", "User-Agent": UA}
            )
            try:
                with urllib.request.urlopen(update_req, timeout=15) as resp:
                    up_result = json.loads(resp.read())
                dois_created += 1
                status_icon = "✅" if up_result.get("success") else "⚠️"
                print(f"  [{idx+1}/{len(all_papers)}] {status_icon} {title[:50]}... → {doi}")
            except Exception as e:
                dois_created += 1
                print(f"  [{idx+1}/{len(all_papers)}] ⚠️ {title[:50]}... → {doi} (D1 update failed: {e})")
        else:
            errors.append(f"{paper_id}: DOI={doi} url={zenodo_url}")
            print(f"  [{idx+1}/{len(all_papers)}] ❌ {title[:50]}... missing DOI/URL")
        
        time.sleep(DELAY)
        
    except urllib.error.HTTPError as e:
        err_body = ""
        try:
            err_body = e.read().decode()[:300]
        except:
            pass
        errors.append(f"{paper_id}: HTTP {e.code} - {err_body}")
        print(f"  [{idx+1}/{len(all_papers)}] ❌ {paper_id}: HTTP {e.code} {err_body[:80]}")
        time.sleep(DELAY)
        
    except Exception as e:
        errors.append(f"{paper_id}: {str(e)[:150]}")
        print(f"  [{idx+1}/{len(all_papers)}] ❌ {paper_id}: {e}")
        time.sleep(DELAY)

# Summary
print("\n" + "=" * 60)
print(f"RESULTS: {dois_created} DOIs PUBLISHED, {len(errors)} errors")

if errors:
    print(f"\nFirst 5 errors:")
    for e in errors[:5]:
        print(f"  - {e}")

# Verify
try:
    req = urllib.request.Request(f"{ASK_QWAV}/api/stats", headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=10) as resp:
        stats = json.loads(resp.read())
    print(f"\nFinal stats: {stats.get('stats', {})}")
except Exception as e:
    print(f"\nCould not verify: {e}")

print("\n✅ DOI batch (PUBLISHED) complete!")
