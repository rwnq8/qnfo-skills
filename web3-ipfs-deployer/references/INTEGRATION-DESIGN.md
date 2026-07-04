# QNFO Research Publications — IPFS/Web3 Integration Design

> **Architecture Decision Document**
> Date: 2026-07-03 | Status: POC/Experimental | Author: QNFO Web3 Working Group

---

## Executive Summary

This document maps the IPFS/Web3 pipeline to existing QNFO infrastructure, defining how content-addressed storage integrates with Cloudflare R2, D1, Workers, Pages, and the Discovery Index. The goal is a three-layer permanence model: **IPFS (availability) → Filecoin (guaranteed persistence) → Arweave (centuries-scale backup)**.

---

## 1. Architecture Overview

```
┌──────────────────────────────────────────────────────────────────┐
│                    QNFO Publication Pipeline                      │
│                                                                   │
│  Author ──► Markdown ──► IPFS Toolkit ──► CID Computation         │
│                │              │                │                  │
│                ▼              ▼                ▼                  │
│           Abstract.md    DAG Builder     CAR Archive              │
│           Metadata.json  IPLD Metadata   Manifest.json            │
│                │              │                │                  │
│                └──────────────┴────────────────┘                  │
│                               │                                   │
│                    ┌──────────┴──────────┐                        │
│                    ▼                     ▼                        │
│           ┌───────────────┐    ┌─────────────────┐               │
│           │  IPFS NETWORK  │    │ QNFO INFRASTRUCTURE │            │
│           │                │    │                     │            │
│           │  Pinata         │──►│ R2: CAR archive     │            │
│           │  web3.storage   │──►│ D1: papers table    │            │
│           │  Lighthouse     │──►│ Workers: papers-    │            │
│           │  Filecoin       │    │   server (gateway   │            │
│           │  Arweave        │    │   fallback)         │            │
│           │                 │    │ Pages: Cached CDN   │            │
│           └───────────────┘    └─────────────────┘               │
└──────────────────────────────────────────────────────────────────┘
```

---

## 2. Component Integration Matrix

| QNFO Component | IPFS Role | Integration Method | Status |
|:---------------|:----------|:-------------------|:-------|
| **R2** (`qnfo` bucket) | CAR archive cold storage + backup pinning | `wrangler r2 object put qnfo/releases/ipfs/<slug>/publication.car` | ✅ Ready |
| **D1** (`living-paper`) | Publication metadata index with IPFS CID column | `INSERT INTO papers ... ipfs_cid = '<cid>'` | ✅ Ready |
| **Workers** (`papers-server`) | Dynamic gateway — serve from IPFS when R2 unavailable | Worker fetches from `cloudflare-ipfs.com/ipfs/<cid>` as fallback | 🔄 POC |
| **Pages** (`papers.qnfo.org`) | CDN-cached render of IPFS-backed content | Pages serves from R2; R2 backed by IPFS CAR | ✅ Ready |
| **Vectorize** (`qwav-research-v2`) | Semantic search across IPFS-indexed papers | Embeddings computed from markdown; CID stored as metadata | 🔄 POC |
| **Discovery Index** | IPFS-native content discovery | `discovery-index-entry.json` per publication with `protocol: "ipfs://"` | ✅ Ready |
| **Knowledge Graph** | IPLD-linked publication graph | DAG-JSON nodes with cross-references via `/` links | 🔄 Future |

---

## 3. Data Flow: Publication to IPFS + QNFO

```
Stage 1: Author creates publication (Markdown)
    └─► metadata.json, paper.md, abstract.txt, paper.pdf

Stage 2: IPFS Toolkit computes CIDs
    ├─► paper.md      → bafkreid2l...
    ├─► metadata.json → bafkreicqq...
    ├─► abstract.txt   → bafkreicbl...
    └─► ROOT DAG       → bafybeien5...  (directory node)

Stage 3: CAR Archive created
    └─► publication.car (8930 bytes, 5 blocks, self-contained)

Stage 4: R2 Cold Storage
    └─► qnfo/releases/ipfs/<slug>/publication.car
    └─► qnfo/releases/ipfs/<slug>/ipfs-manifest.json

Stage 5: D1 Metadata Index
    └─► INSERT INTO living-paper.papers (id, ipfs_cid, ...)

Stage 6: Pinning Services (optional, configured)
    ├─► Pinata: pinByHash
    ├─► web3.storage: CAR upload + Filecoin deal
    └─► Lighthouse: pin + Filecoin deal

Stage 7: Web3 Identity (optional)
    ├─► DID:key generated for author
    ├─► Attestation signed for root CID
    └─► ENS contenthash computed (EIP-1577)

Stage 8: Gateway Verification
    └─► Test 10+ gateways for content availability
```

---

## 4. Papers-Server Worker: IPFS Fallback

The `papers-server` Worker currently fetches papers from R2 (markdown) + D1 (metadata). With IPFS integration, add an IPFS fallback path:

```javascript
// In papers-server Worker (pseudocode)
async function servePaper(slug) {
  // 1. Try D1 + R2 (primary path)
  const paper = await env.DB.prepare('SELECT * FROM papers WHERE id = ?').bind(slug).first();
  if (paper) {
    const md = await env.PAPERS_BUCKET.get(`releases/${paper.release_path}/paper.md`);
    if (md) return render(md, paper);
  }

  // 2. Fallback: Fetch from IPFS gateway
  if (paper?.ipfs_cid) {
    const ipfsResp = await fetch(`https://cloudflare-ipfs.com/ipfs/${paper.ipfs_cid}`);
    if (ipfsResp.ok) return renderFromIPFS(await ipfsResp.text(), paper);
  }

  // 3. Return metadata-only page
  return renderMetadataOnly(paper);
}
```

---

## 5. Persistence Tier Model

| Tier | Technology | Duration | Cost | Redundancy | How It Works |
|:-----|:-----------|:---------|:-----|:-----------|:-------------|
| **Tier 0: Active** | R2 + Pages CDN | Immediate | $0 (free tier) | Cloudflare global edge | Primary serving layer |
| **Tier 1: Available** | IPFS Public Gateways | As accessed | $0 | 10+ gateways worldwide | Anyone who accesses becomes a provider |
| **Tier 2: Pinned** | Pinata + web3.storage | Years | ~$5-20/mo | Dual service redundancy | Pinning services maintain copies |
| **Tier 3: Guaranteed** | Filecoin Storage Deals | 1.5-10 years | ~$0.01/GB/deal | 3-5 miners | Economic incentive for storage |
| **Tier 4: Permanent** | Arweave | Centuries | ~$5/GB one-time | 100+ miners | Proof-of-access consensus |
| **Tier ∞: Self-Sovereign** | Local CAR file | Forever | $0 | Your hard drive | You always have a copy |

### Recommended QNFO Configuration

- **All papers:** Tier 0 (R2) + Tier 1 (IPFS, automatic via content addressing)
- **Published papers:** Tier 2 (Pinata + web3.storage dual pinning)
- **Landmark papers:** Tier 3 (Filecoin deals for guaranteed persistence)
- **Archive/legacy:** Tier 4 (Arweave for centuries-scale permanence)

---

## 6. Security & Identity Model

### DID:key for Author Attribution

Every author generates a `did:key` (Ed25519-based, no blockchain required):
```
did:key:z6MkqpPLqUHAQKDPTm4ChWaxVXSRP2GWJ5xqjAso8EagSm43
```

### Content Attestation Flow

```
1. Author generates DID:key (once, offline)
2. Author creates publication → computes root CID
3. Author signs attestation: { did, cid, timestamp, signature }
4. Anyone can verify: did:key → pubkey → verify(signature, payload)
5. Attestation stored alongside publication in R2 + IPFS
```

### ENS Contenthash (EIP-1577)

Maps human-readable ENS names to IPFS CIDs:
```
qnfo.eth → contenthash: 0xe301701220... → bafybeien5...
```

---

## 7. Cost Analysis

| Component | Free Tier | Production Estimate |
|:----------|:----------|:--------------------|
| R2 (CAR storage) | 10 GB free | $0.015/GB/mo |
| IPFS Pinning (Pinata) | 1 GB free | $20/mo (100 GB) |
| web3.storage | 5 GB free | $10/mo (100 GB) |
| Filecoin Deals | N/A | ~$0.01/GB/deal |
| Arweave | N/A | ~$5/GB (one-time) |
| Cloudflare Pages | Unlimited bandwidth | $0 |
| **Total (Minimal)** | **$0/mo** | **$0/mo** |
| **Total (Robust)** | **$0/mo for small scale** | **~$30-50/mo** |

**Key insight:** For QNFO's current scale (~170 papers, ~50 MB total), the entire pipeline runs at zero cost under all free tiers. The IPFS layer adds cost-free permanent addressing.

---

## 8. Implementation Roadmap

| Phase | Deliverable | Timeline | Dependencies |
|:------|:------------|:---------|:-------------|
| **Phase 0 (Done)** | IPFS Toolkit (CID, DAG, CAR) | Complete | Pure Node.js |
| **Phase 1 (Done)** | Web3 Identity + Gateway Verifier | Complete | None |
| **Phase 2 (This POC)** | Publication Pipeline + Integration Design | Complete | Phase 0-1 |
| **Phase 3** | R2 CAR archive pipeline for existing papers | 1-2 days | Cloudflare token |
| **Phase 4** | D1 ipfs_cid column migration + Worker fallback | 2-3 days | Phase 3 |
| **Phase 5** | Pinata + web3.storage auto-pinning in pipeline | 1 day | Service API keys |
| **Phase 6** | Filecoin deal automation for landmark papers | 2-3 days | Lighthouse integration |
| **Phase 7** | ENS contenthash resolution + qnfo.eth | 1-2 days | ENS domain |
| **Phase 8** | Arweave one-time archival of complete corpus | 1 day | AR wallet |

---

## 9. Risk Assessment

| Risk | Severity | Mitigation |
|:-----|:---------|:-----------|
| IPFS gateway censorship | Medium | Multi-gateway redundancy (10+ gateways) + R2 fallback |
| Pinata/web3.storage shutdown | Low | Multi-service pinning + CAR files always on R2 |
| Filecoin deal expiry | Low | Auto-renewal; Arweave as permanent backup |
| DID key loss | Medium | Keys stored in QNFO secrets; attestations are public record |
| Content hash collision (SHA-256) | Negligible | 2^256 space is astronomically large |
| CAR format obsolescence | Low | Open standard; multiple implementations exist |

---

## 10. Conclusion

IPFS/Web3 integration provides QNFO research publications with:

1. **Permanent, verifiable content addressing** — every paper has a CID that proves its integrity forever
2. **Decentralized availability** — content survives any single platform's failure
3. **Zero additional cost at current scale** — all free tiers cover QNFO's corpus
4. **Cryptographic author attribution** — DID:key + content attestations without blockchain dependency
5. **Incremental adoption** — each tier can be added independently; the pipeline works at any level

**Recommendation:** Proceed to Phase 3 (R2 CAR pipeline for existing papers) and Phase 4 (D1 migration + Worker fallback) to make IPFS a native layer of the QNFO publication infrastructure.

---

*This document is itself content-addressed. Root CID available in the accompanying manifest.*
