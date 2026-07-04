# IPFS/Web3 Landscape for Research Publication — Comprehensive Survey

> **QNFO Web3 Working Group | July 2026 | POC/Experimental**

---

## Executive Summary

This document surveys the IPFS/Web3 landscape as it pertains to scientific research publication and permanent content dissemination. We evaluate protocols, services, and tools across the stack — from content addressing and storage permanence to identity, discovery, and monetization — and assess their maturity, cost, and fit for QNFO's research pipeline.

**Key finding:** The IPFS/Web3 ecosystem has matured significantly since 2022. Content addressing, multi-service pinning, Filecoin storage deals, and gateway infrastructure are production-ready. The cost curve is favorable for research publication: at QNFO's scale (~170 papers, ~50 MB), the entire stack runs at zero cost under current free tiers.

---

## 1. Content Addressing Layer

### 1.1 IPFS (InterPlanetary File System)

**Status:** Production, stable (v0.32+)

IPFS is the foundational layer. Content is addressed by cryptographic hash (CID), not location. This provides:

- **Immutability:** Changing one byte changes the entire CID
- **Deduplication:** Identical content has the same CID, stored once
- **Verifiability:** Anyone can verify content matches its CID
- **Location independence:** Content can be served from any node

**CID Versions:**
| Version | Encoding | Multicodec | Example |
|:--------|:---------|:-----------|:--------|
| CIDv0 | Base58btc | dag-pb only | `Qm...` (46 chars) |
| CIDv1 | Base32 | Any codec | `bafy...` (59+ chars) |

### 1.2 Multihash

Standardized hash identification. QNFO primarily uses `sha2-256` (0x12):
```
[0x12, 0x20] + <32-byte SHA-256 hash>
```

### 1.3 CAR (Content Addressable aRchives)

**Status:** CARv1 format is stable, widely supported.

CAR files provide: self-contained IPFS data packages, offline distribution, archival backup, direct upload to pinning services. QNFO pipeline produces CARv1 archives: 5 blocks for a typical 3-file publication, ~8.9 KB overhead.

---

## 2. Pinning & Persistence Services

### 2.1 Pinata ⭐ Primary
**Status:** Production | **Free tier:** 1 GB, 500 pins | **Paid:** $20/mo (100 GB)
Most widely used IPFS pinning service. REST API + SDK, JSON pinning, dedicated gateway, Submarine for private files.

### 2.2 web3.storage ⭐ Recommended for Persistence
**Status:** Production, w3up v17+ | **Free tier:** 5 GB
Built by Protocol Labs. Automatic Filecoin deals for every upload. 10+ year persistence.

### 2.3 Lighthouse
**Status:** Production | **Free tier:** 1 GB
Explicit Filecoin deal management + encryption. Perpetual storage with auto-renewing deals.

### 2.4 Crust Network
**Status:** Production (Polkadot parachain)
Decentralized pinning with CRU token incentives. Truly decentralized alternative.

### 2.5 4EVERLAND
**Status:** Production
Asian infrastructure, Great Firewall-compatible. IPFS pinning + Web3 hosting.

### 2.6 NFT.Storage
**Status:** Production — free for public data
Free forever for public content. Ideal for open-access research papers.

### 2.7 Arweave (Permaweb)
**Status:** Production | **Model:** Pay once, store forever | **Cost:** ~$5/GB one-time
Not IPFS, but complementary. Permanent storage via proof-of-access consensus. 200+ year theoretical persistence.

---

## 3. IPFS Gateways

| Gateway | URL Pattern | Owner | Reliability | Rate Limit |
|:--------|:------------|:------|:------------|:-----------|
| **IPFS.io** | `ipfs.io/ipfs/{cid}` | Protocol Labs | High | Moderate |
| **Cloudflare** | `cloudflare-ipfs.com/ipfs/{cid}` | Cloudflare | Very High | High |
| **dweb.link** | `dweb.link/ipfs/{cid}` | Protocol Labs | High | Moderate |
| **Pinata** | `gateway.pinata.cloud/ipfs/{cid}` | Pinata | High | High |
| **w3s.link** | `{cid}.ipfs.w3s.link` | web3.storage | High | High |
| **nftstorage.link** | `{cid}.ipfs.nftstorage.link` | NFT.Storage | High | High |
| **4EVERLAND** | `4everland.io/ipfs/{cid}` | 4EVERLAND | Medium | Moderate |
| **Fleek** | `{cid}.ipfs.fleek.co` | Fleek | High | High |
| **Infura** | `ipfs.infura.io/ipfs/{cid}` | Infura | High | Moderate |

**QNFO Gateway Strategy:** Cloudflare primary → dweb.link → ipfs.io → pinata → w3s.link → self-hosted papers-server Worker.

---

## 4. Web3 Identity & Attribution

### 4.1 DID (Decentralized Identifiers)
**Standard:** W3C DID Core v1.0

| DID Method | Blockchain Required | Key Type | QNFO Suitability |
|:-----------|:--------------------|:---------|:-----------------|
| **did:key** | No | Ed25519 | ⭐ Best — simple, offline, verifiable |
| did:ethr | Ethereum | secp256k1 | Overkill for simple attribution |
| did:web | No (DNS) | Any | Good for institutional identity |

**QNFO uses did:key** — purely cryptographic, no blockchain dependency.

### 4.2 Verifiable Credentials
**Standard:** W3C VC Data Model v2.0
Content attestations link a DID to a CID with Ed25519 signature. Anyone can verify: extract pubkey from DID → verify signature.

### 4.3 ENS (Ethereum Name Service)
**Standard:** EIP-1577 (contenthash)
Maps `qnfo.eth` → IPFS CID via contenthash record. Optional but useful for human-readable resolution.

---

## 5. JavaScript/Node.js Tooling Ecosystem

| Library | Version | Purpose | Dependencies |
|:--------|:--------|:--------|:-------------|
| **helia** | 7.0+ | Full IPFS node in JS | 50+ transitive |
| **@helia/unixfs** | 8.0+ | UnixFS file operations | ~20 |
| **@helia/car** | 6.0+ | CAR import/export | ~15 |
| **@helia/verified-fetch** | 8.0+ | Trustless IPFS fetching | ~30 |
| **multiformats** | 14.0+ | CID, multibase, multihash | 0 |
| **@ipld/dag-json** | 11.0+ | DAG-JSON codec | ~10 |
| **@ipld/dag-pb** | 4.1+ | DAG-PB codec | ~10 |
| **@web3-storage/w3up-client** | 17.0+ | web3.storage client | ~40 |
| **@pinata/sdk** | 2.1+ | Pinata API client | ~5 |

### QNFO Approach: Zero-Dependency Toolkit

Rather than pulling in Helia (50+ deps), `ipfs-toolkit.js` implements CID computation, DAG building, and CAR creation from first principles using Node.js built-in `crypto`. **Zero npm dependencies.** When IPFS networking features are needed (DHT announce, bitswap), upgrade to `helia` + `@helia/car`.

---

## 6. Protocol Maturity Assessment

| Protocol/Standard | Maturity | Risk | Recommendation |
|:------------------|:---------|:-----|:---------------|
| IPFS (core) | Production | Low | ✅ Use immediately |
| CIDv1 | Stable | None | ✅ Canonical format |
| CARv1 | Stable | Low | ✅ Archive format |
| Multihash (sha2-256) | Stable | None | ✅ Primary hash |
| DAG-JSON | Stable | Low | ✅ Metadata |
| did:key | Stable | None | ✅ Identity |
| ENS (EIP-1577) | Stable | Low | ⚠️ Optional |
| Filecoin deals | Production | Low | ✅ Persistence |
| Arweave | Production | Low | ⚠️ Archive only |

---

## 7. Key Findings

1. **IPFS is production-ready for research publication.** CID computation, CAR creation, and multi-gateway retrieval work reliably.
2. **Zero-cost at QNFO scale.** ~170 papers, ~50 MB fit within all free tiers.
3. **Multi-service pinning is achievable.** Pinata + web3.storage provide dual redundancy.
4. **Filecoin deals are trivially cheap.** Multi-year storage costs fractions of a cent.
5. **DID-based attribution works without blockchain.** did:key is purely cryptographic.
6. **The JavaScript Helia ecosystem is mature.** Available when networking features are needed.
7. **CAR files are the universal archive format.** Self-contained, portable, auto-verifiable.

---

## 8. Recommendations

| Priority | Action | Timeline | Cost |
|:---------|:-------|:---------|:-----|
| **P0** | Add `ipfs_cid` column to D1 `papers` table | Immediate | $0 |
| **P0** | Upload CAR archives for all papers to R2 | 1-2 days | $0 |
| **P1** | Add IPFS fallback to papers-server Worker | 2-3 days | $0 |
| **P1** | Configure Pinata + web3.storage auto-pinning | 1 day | $0 (free tier) |
| **P2** | Filecoin deals for landmark papers | 2-3 days | <$0.01 |
| **P3** | Arweave archive of complete corpus | 1 day | ~$0.25 one-time |

---

## 9. References

- IPFS Spec: https://specs.ipfs.dev/
- CID Spec: https://github.com/multiformats/cid
- CAR Spec: https://ipld.io/specs/transport/car/carv1/
- IPLD: https://ipld.io/
- DID Core: https://www.w3.org/TR/did-core/
- VC Data Model: https://www.w3.org/TR/vc-data-model-2.0/
- ENS EIP-1577: https://eips.ethereum.org/EIPS/eip-1577
- Filecoin Docs: https://docs.filecoin.io/
- Arweave: https://www.arweave.org/
- Helia: https://github.com/ipfs/helia
- Pinata: https://docs.pinata.cloud/
- web3.storage: https://web3.storage/docs/

---

*This landscape survey is part of the QNFO IPFS/Web3 POC. v1.0 — July 3, 2026.*
