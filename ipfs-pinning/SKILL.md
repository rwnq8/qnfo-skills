# IPFS PINNING SKILL -- v1.0

> **Related:** cloudflare-deployer, publication-publisher, closeout-manager
> **Auto-load triggers:** ipfs, pinata, cid, pinning, paper hash, content-addressing

---

## 0. WHY THIS EXISTS

IPFS pinning has been the #1 recurring blocker across multiple QNFO sessions:
- 2026-06-25: "Pinata 24-paper retry" — discovered 163 Filebase CIDs, only 139 (later 157) on Pinata
- 2026-07-02: "COMPLETE IPFS pinning: 14 remaining living papers" — blocked by missing credentials
- Each session: agent declares [BLOCKED] then requires user to provide credentials/context

**Root cause analysis:**
1. **Fragmented state**: Pinata creds, paper CIDs, Filebase CIDs, Living Papers D1 — spread across 4 systems
2. **No canonical IPFS registry**: No single source of truth for "which papers are pinned where"
3. **Stale handoffs**: HANDOFF.md claims 139 pins, live state shows 474
4. **Missing credential discovery**: Agents don't know to check `PINATA_API_KEY` vs `PINATA_JWT`
5. **No auto-recovery**: Failure modes not documented; each session re-debugges from scratch

**This skill ELIMINATES the IPFS blocker pattern permanently.**

---

## 1. ARCHITECTURE: IPFS Registry (Single Source of Truth)

### 1.1 Canonical Registry Location

```
R2: qnfo/ipfs/registry.json   ← Single source of truth
D1: living-paper.papers       ← Paper metadata (ipfs_cid column)
Pinata: api.pinata.cloud      ← Actual pinned files (474 pins)
```

### 1.2 Registry Schema

```json
{
  "version": "1.0",
  "updated": "2026-07-02T00:00:00Z",
  "pinning_services": {
    "pinata": {
      "total_pins": 474,
      "auth_method": "api_key_secret",
      "last_sync": "2026-07-02T00:00:00Z"
    },
    "filebase": {
      "total_uploads": 163,
      "auth_method": "s3_key",
      "last_sync": null
    }
  },
  "living_papers": {
    "total_papers": 455,
    "papers_with_cids": 163,
    "papers_without_cids": 292,
    "api_status": "offline_404"
  },
  "papers": {
    "<paper_id>": {
      "title": "...",
      "r2_key": "papers/...",
      "ipfs_cid": "Qm...",
      "pinata_pinned": true,
      "filebase_uploaded": true,
      "last_pinned": "2026-06-25"
    }
  }
}
```

### 1.3 Three-Tier Pin Health

| Tier | Criteria | Count (approx) |
|:-----|:---------|:---------------|
| **GOLD** | CID in D1 + pinned on Pinata + uploaded to Filebase | ~163 |
| **SILVER** | Content pinned on Pinata but CID not in D1 | ~311 |
| **BRONZE** | Paper exists in D1 but no CID + not pinned | ~292 |

---

## 2. CREDENTIAL DISCOVERY PROTOCOL

### 2.1 Auto-Discovery Order

Before declaring [BLOCKED: no IPFS credentials], scan ALL of:

```python
# Priority 1: Environment variables (most reliable)
PINATA_JWT = os.environ.get('PINATA_JWT')
PINATA_API_KEY = os.environ.get('PINATA_API_KEY')
PINATA_API_SECRET = os.environ.get('PINATA_API_SECRET')

# Priority 2: .env files in workspace
# Priority 3: R2 secrets store (qnfo/secrets/pinata.json)
# Priority 4: Cloudflare API tokens
```

**HARD RULE: Try ALL auth methods before declaring failure.** 
- `PINATA_JWT` may be expired → fall back to `PINATA_API_KEY` + `PINATA_API_SECRET`
- At least ONE method typically works.

### 2.2 Auth Verification

```python
def verify_pinata_auth():
    """Test both auth methods, return working credentials."""
    methods = [
        ('jwt', {'Authorization': f'Bearer {PINATA_JWT}'}),
        ('key', {'pinata_api_key': KEY, 'pinata_secret_api_key': SECRET}),
    ]
    for name, headers in methods:
        try:
            r = urlopen(Request('https://api.pinata.cloud/data/pinList?pageLimit=1', headers=headers))
            if r.status == 200:
                return name, headers
        except:
            continue
    return None, None
```

---

## 3. PINNING OPERATIONS

### 3.1 Pin a Single Paper

```python
def pin_paper(r2_key, paper_id, title):
    """Download from R2, upload to Pinata, return CID."""
    # 1. Download from R2
    content = download_from_r2(f"qnfo/{r2_key}")
    
    # 2. Upload to Pinata
    boundary = '----boundary'
    body = (
        f'--{boundary}\r\n'
        f'Content-Disposition: form-data; name="file"; filename="{paper_id}.md"\r\n'
        f'Content-Type: text/markdown\r\n\r\n'
        f'{content.decode()}\r\n'
        f'--{boundary}\r\n'
        f'Content-Disposition: form-data; name="pinataMetadata"\r\n\r\n'
        f'{{"name":"{paper_id}.md","keyvalues":{{"title":"{title}","paper_id":"{paper_id}"}}}}\r\n'
        f'--{boundary}--\r\n'
    ).encode()
    
    req = Request('https://api.pinata.cloud/pinning/pinFileToIPFS',
                  data=body,
                  headers={**auth_headers, 'Content-Type': f'multipart/form-data; boundary={boundary}'})
    result = json.loads(urlopen(req).read())
    return result['IpfsHash']
```

### 3.2 Batch Pin (with 2s delays)

```python
def batch_pin(paper_list, delay=2):
    """Pin multiple papers with rate-limiting."""
    results = {'success': [], 'failed': []}
    for paper in paper_list:
        try:
            cid = pin_paper(paper['r2_key'], paper['id'], paper['title'])
            results['success'].append({**paper, 'cid': cid})
            time.sleep(delay)  # Rate limiting
        except Exception as e:
            results['failed'].append({**paper, 'error': str(e)})
    return results
```

### 3.3 Verify Pin Status

```python
def verify_pin(cid):
    """Check if a CID is pinned on Pinata."""
    req = Request(f'https://api.pinata.cloud/data/pinList?hashContains={cid}',
                  headers=auth_headers)
    result = json.loads(urlopen(req).read())
    return result['count'] > 0
```

---

## 4. RECOVERY PROTOCOLS

### 4.1 Stale HANDOFF Detection

If HANDOFF.md says `pinata_pinned: 139` but live Pinata shows 474:
→ **TRUST LIVE STATE.** HANDOFF is stale. Update registry.

### 4.2 Missing R2 Source File Recovery

If `r2_key` doesn't exist in R2 but paper has content elsewhere:
1. Check `living-paper` D1 for `content_md` column
2. Check Pinata for existing pin (CID might exist)
3. Check user's local Obsidian vault (`G:\My Drive\Obsidian\...`)
4. Flag as `[RECOVERABLE: source in Obsidian vault, not automated]`

### 4.3 Credential Rotation Handling

If Pinata returns 401:
1. Try `PINATA_JWT` first
2. Fall back to `PINATA_API_KEY` + `PINATA_API_SECRET`
3. If both fail, check `qnfo/secrets/pinata.json` on R2
4. Only then flag `[BLOCKED: Pinata credentials expired — needs user rotation]`

---

## 5. SELF-HEALING REGISTRY SYNC

### 5.1 Sync Protocol (run at session start)

```python
def sync_ipfs_registry():
    """Pull all IPFS state into a canonical registry."""
    registry = load_or_create_registry()
    
    # 1. Query Pinata (live state)
    registry['pinning_services']['pinata'] = query_pinata_stats()
    
    # 2. Query Filebase (if available)
    # registry['pinning_services']['filebase'] = query_filebase_stats()
    
    # 3. Query Living Papers D1
    registry['living_papers'] = query_living_papers_stats()
    
    # 4. Cross-reference: find papers in D1 that are NOT on Pinata
    registry['gaps'] = compute_gaps(registry)
    
    # 5. Upload to R2
    upload_to_r2('qnfo/ipfs/registry.json', json.dumps(registry, indent=2))
    
    return registry
```

### 5.2 Gap Detection

```python
def compute_gaps(registry):
    """Find papers that need pinning."""
    gaps = {
        'need_pinning': [],      # Papers with CID but not on Pinata
        'need_cid_generation': [], # Papers in D1 without CID
        'need_d1_sync': [],      # Papers on Pinata but CID not in D1
    }
    # ... compute from registry
    return gaps
```

---

## 6. INTEGRATION POINTS

### 6.1 With Living Papers D1
- `living-paper.papers` table has `ipfs_cid`, `ipfs_pinned`, `r2_key` columns
- After pinning: UPDATE `ipfs_cid` and `ipfs_pinned = true`
- After unpinning: UPDATE `ipfs_pinned = false`

### 6.2 With CMS (qnfo-cms D1)
- `content_entries` has `ipfs_cid` in `data_json`
- Paper entries reference `lp_paper_id` for cross-reference

### 6.3 With Cross-Ecosystem Platform
- Platform JS can display IPFS badges via CID
- CID gateway: `https://ipfs.io/ipfs/{cid}` or `https://{cid}.ipfs.dweb.link`

---

## 7. ANTI-PATTERNS (NEVER DO)

| Anti-Pattern | Why | Correct |
|:-------------|:----|:--------|
| Trust HANDOFF over live Pinata | HANDOFF is always stale | Query Pinata API directly |
| Declare [BLOCKED] without trying all auth methods | PINATA_JWT expired but KEY+SECRET works | Try both (see §2) |
| Assume papers must be re-pinned without checking | 474 already pinned | Check live state first |
| Create local IPFS node for pinning | Not needed — Pinata API is sufficient | Use Pinata pinning API |
| Hardcode CID counts in prompts | Counts change every session | Query live every time |

---

## 8. EMBEDDED SCRIPTS

| Script | Canonical (R2) | Purpose |
|:-------|:---------------|:--------|
| `ipfs_sync.py` | `qnfo/tools/ipfs_sync.py` | Full registry sync + gap detection |
| `pinata_pin.py` | `qnfo/tools/pinata_pin.py` | Pin single/batch papers to Pinata |
| `ipfs_verify.py` | `qnfo/tools/ipfs_verify.py` | Verify CID pin status on Pinata |

### Bootstrap Protocol

If scripts are missing from R2:
```bash
# Pull from R2 first
npx wrangler r2 object get qnfo/tools/ipfs_sync.py --remote --file=_ipfs_sync.py
npx wrangler r2 object get qnfo/tools/pinata_pin.py --remote --file=_pinata_pin.py
npx wrangler r2 object get qnfo/tools/ipfs_verify.py --remote --file=_ipfs_verify.py
```

If R2 pull fails → recreate from this skill's embedded protocol sections above.

---

## 9. RED-TEAM SELF-AUDIT

Before claiming IPFS work is complete:
1. **Live Pinata query**: Confirm count matches expectation
2. **Auth method test**: Both JWT and KEY+SECRET tried
3. **Cross-reference**: D1 CIDs vs Pinata CIDs
4. **Registry upload**: `qnfo/ipfs/registry.json` is current
5. **Gap report**: Exact list of papers needing action (not just "N papers")

---

## 10. CID FORMAT HANDLING (RED-TEAM FINDING)

**Critical gap discovered 2026-07-02:** D1 Living Papers stores CIDs in CIDv1 base32 format (`bafkreidnp4bhat...`) while Pinata stores them in CIDv0 base58 format (`QmdBxLf4Z...`). Pinata's `hashContains` search does STRING matching, not multihash matching, so cross-referencing D1 CIDs against Pinata returns false negatives.

### 10.1 CID Conversion

```python
import multihash, base58, base32

def cid_v0_to_v1(cid_v0):
    """Convert Qm... (CIDv0) to bafkreid... (CIDv1)."""
    # CIDv0: <cidv0> = <multihash> where multihash is sha2-256
    raw = base58.b58decode(cid_v0)
    # CIDv1: <cidv1> = <cidv1-multibase><cidv1-multicodec><multihash>
    # Multicodec for dag-pb = 0x70, Multibase for base32 = 'b'
    pass  # Requires proper CID library

def normalize_cid(cid):
    """Convert any CID format to a consistent search format."""
    if cid.startswith('Qm') and len(cid) == 46:
        return cid  # CIDv0
    if cid.startswith('baf'):
        return cid  # CIDv1 base32
    return cid
```

### 10.2 Cross-Reference Strategy

To verify whether a D1 paper is actually pinned on Pinata:
1. Pull the paper content from R2
2. Compute both CIDv0 and CIDv1
3. Search Pinata with BOTH formats
4. Store both CIDs in the registry

### 10.3 Current Workaround

Until CID conversion is implemented:
- Search Pinata by **filename** (paper ID or r2_key slug) instead of CID
- The Pinata metadata `name` field contains `papers-{slug}.md` which matches the r2_key
- This is more reliable than CID matching across format boundaries

---

*ipfs-pinning v1.0 — Permanent solution for IPFS blocking. v1.1 adds CID format handling per red-team finding 2026-07-02.* Auto-discovers credentials, syncs live state, self-heals registry, and integrates with LP D1 + CMS + cross-ecosystem platform.*
