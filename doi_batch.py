"""Batch DOI generation via Zenodo API for QNFO papers without DOIs."""
import json, urllib.request, urllib.error, time, sys
from pathlib import Path

ZENODO_API = "https://zenodo.org/api"
ASK_QWAV = "https://ask-qwav.q08.workers.dev"
UA = "QNFO-DOI-Batch/1.0"
BATCH_SIZE = 5  # Papers per batch
DELAY = 2  # Seconds between API calls (rate limit)

# ── Load Zenodo token ──
token_path = Path.home() / ".zenodo_token"
if not token_path.exists():
    print("❌ No Zenodo token found at ~/.zenodo_token")
    sys.exit(1)
token = token_path.read_text().strip()
print(f"✅ Zenodo token loaded ({len(token)} chars)")

# ── Get papers without DOIs ──
print("Fetching papers...")
req = urllib.request.Request(f"{ASK_QWAV}/api/papers?limit=200", headers={"User-Agent": UA})
with urllib.request.urlopen(req, timeout=30) as resp:
    papers = json.loads(resp.read())["data"]

no_doi = [p for p in papers if not (p.get("doi") or "").strip()]
print(f"Papers without DOI: {len(no_doi)} / {len(papers)}")

if not no_doi:
    print("All papers have DOIs already!")
    sys.exit(0)

# ── Get the paper that already has a DOI to see its format ──
with_doi = [p for p in papers if (p.get("doi") or "").strip()]
if with_doi:
    print(f"Existing DOI example: {with_doi[0]['doi']} (paper: {with_doi[0].get('title','?')[:60]})")

# ── Batch process ──
dois_created = 0
errors = []
total = len(no_doi)

print(f"\nProcessing {total} papers (batch size: {BATCH_SIZE}, delay: {DELAY}s)...")
print("="*60)

for idx, paper in enumerate(no_doi):
    paper_id = paper["id"]
    title = (paper.get("title") or "Untitled")[:250]
    
    try:
        # Step 1: Create deposition
        dep_req = urllib.request.Request(
            f"{ZENODO_API}/deposit/depositions",
            data=json.dumps({}).encode(),
            method="POST",
            headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
        )
        with urllib.request.urlopen(dep_req, timeout=30) as resp:
            deposition = json.loads(resp.read())
        dep_id = deposition["id"]
        
        # Step 2: Parse authors
        authors_raw = paper.get("authors", "") or ""
        try:
            authors_list = json.loads(authors_raw)
        except:
            authors_list = ["QNFO Research Collective"]
        
        if not authors_list:
            authors_list = ["Rowan Quni-Gudzinas"]
        
        creators = []
        for author in authors_list:
            if isinstance(author, str):
                creators.append({"name": author.strip(), "affiliation": "QNFO Research"})
            elif isinstance(author, dict):
                creators.append({
                    "name": author.get("name", str(author)),
                    "affiliation": author.get("affiliation", "QNFO Research")
                })
        
        # Step 3: Build metadata
        abstract = (paper.get("abstract") or f"Research paper: {title}")[:2000]
        
        # Extract keywords from title
        keywords = ["QNFO", "research"]
        title_lower = title.lower()
        if "quantum" in title_lower: keywords.append("quantum")
        if "ultrametric" in title_lower: keywords.append("ultrametric")
        if "p-adic" in title_lower: keywords.append("p-adic")
        if "physics" in title_lower: keywords.append("physics")
        if "mathematics" in title_lower: keywords.append("mathematics")
        if "information" in title_lower: keywords.append("information theory")
        if "philosoph" in title_lower: keywords.append("philosophy")
        keywords = keywords[:10]
        
        metadata = {
            "metadata": {
                "title": title,
                "upload_type": "publication",
                "publication_type": "preprint",
                "description": abstract,
                "creators": creators[:5],
                "access_right": "open",
                "license": "cc-by-4.0",
                "keywords": keywords,
                "notes": f"QNFO auto-indexed paper. Paper ID: {paper_id}"
            }
        }
        
        # Step 4: Update deposition metadata
        meta_req = urllib.request.Request(
            f"{ZENODO_API}/deposit/depositions/{dep_id}",
            data=json.dumps(metadata).encode(),
            method="PUT",
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
        )
        with urllib.request.urlopen(meta_req, timeout=30) as resp:
            updated = json.loads(resp.read())
        
        # Step 5: Get DOI
        doi = None
        prereserve = updated.get("metadata", {}).get("prereserve_doi", {})
        if isinstance(prereserve, dict):
            doi = prereserve.get("doi")
        if not doi:
            doi = updated.get("doi")
        if not doi:
            # Try to construct DOI URL
            conceptdoi = updated.get("conceptdoi")
            if conceptdoi and isinstance(conceptdoi, str):
                doi = conceptdoi
        
        if doi:
            # Step 6: Update D1 with DOI
            update_body = json.dumps({"paper_id": paper_id, "doi": doi}).encode()
            update_req = urllib.request.Request(
                f"{ASK_QWAV}/api/paper-doi",
                data=update_body,
                method="POST",
                headers={"Content-Type": "application/json", "User-Agent": UA}
            )
            try:
                with urllib.request.urlopen(update_req, timeout=15) as resp:
                    up_result = json.loads(resp.read())
                if up_result.get("success"):
                    dois_created += 1
                    print(f"  [{idx+1}/{total}] ✅ {title[:55]}... → {doi}")
                else:
                    dois_created += 1
                    print(f"  [{idx+1}/{total}] ⚠️ {title[:55]}... → {doi} (D1 update failed: {up_result.get('error','?')})")
            except Exception as e:
                dois_created += 1
                print(f"  [{idx+1}/{total}] ⚠️ {title[:55]}... → {doi} (D1 update error: {e})")
        else:
            errors.append(f"{paper_id}: No DOI in response (dep_id={dep_id})")
            print(f"  [{idx+1}/{total}] ❌ {title[:55]}... — no DOI returned")
        
        time.sleep(DELAY)
        
    except urllib.error.HTTPError as e:
        err_body = ""
        try:
            err_body = e.read().decode()[:300]
        except:
            pass
        error_msg = f"{paper_id}: HTTP {e.code} - {err_body}"
        errors.append(error_msg)
        print(f"  [{idx+1}/{total}] ❌ {paper_id}: HTTP {e.code} {err_body[:80]}")
        time.sleep(DELAY * 2)
        
    except Exception as e:
        error_msg = f"{paper_id}: {str(e)[:150]}"
        errors.append(error_msg)
        print(f"  [{idx+1}/{total}] ❌ {paper_id}: {e}")
        time.sleep(DELAY)

# ── Summary ──
print("\n" + "="*60)
print(f"RESULTS: {dois_created} DOIs created, {len(errors)} errors")
print(f"Progress: {dois_created}/{total} ({100*dois_created//total if total else 0}%)")

if errors:
    print(f"\nFirst 5 errors:")
    for e in errors[:5]:
        print(f"  - {e}")

# Verify final count
try:
    req = urllib.request.Request(f"{ASK_QWAV}/api/stats", headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=10) as resp:
        stats = json.loads(resp.read())
    print(f"\nFinal ask-qwav stats: {stats.get('stats', {})}")
except Exception as e:
    print(f"\nCould not verify stats: {e}")

print("\n✅ DOI batch complete!")
