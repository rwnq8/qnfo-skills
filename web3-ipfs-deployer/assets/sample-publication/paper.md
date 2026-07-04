# Content-Addressed Research: IPFS as a Permanent Layer for Scientific Publication

**QNFO Research & Web3 Working Group**
*July 3, 2026*

## Abstract

This paper explores the use of IPFS and content-addressed storage as a permanent, verifiable layer for scientific research publications. We demonstrate a pure Node.js pipeline for computing CIDs, building DAG archives, creating CAR files, and verifying content across multiple IPFS gateways. The approach leverages cryptographic content addressing to ensure immutability, reproducibility, and censorship resistance for research outputs.

## 1. Introduction

Scientific publishing faces a fundamental tension: the need for permanent, immutable records versus the reality of link rot, platform dependence, and centralized gatekeeping. Over the past two decades, the web has lost millions of research artifacts to expired domains, restructured university websites, and discontinued publishing platforms.

Content-addressed storage — where a file's address is a cryptographic hash of its contents — offers a compelling alternative. The InterPlanetary File System (IPFS) implements this paradigm at web scale, providing a decentralized network where content is addressed by what it is, not where it lives.

## 2. The Content Addressing Advantage

### 2.1 Immutability by Construction

In a content-addressed system, modifying a single byte of content produces an entirely different address. This means:

- **Verifiability:** Anyone can verify that the content they received exactly matches the content that was published
- **Tamper-evidence:** Any modification to published content is immediately detectable
- **Reproducibility:** The same CID always points to the same content, forever

### 2.2 Decentralized Persistence

Rather than relying on a single server or organization, content on IPFS is distributed across the network. Anyone who accesses content becomes a temporary provider, creating a resilient distribution mesh.

## 3. Implementation

### 3.1 Pure Node.js CID Computation

Our implementation requires zero external dependencies. CIDs are computed from first principles using Node.js built-in cryptography:

```javascript
const crypto = require('crypto');

function computeCIDv1(data) {
  const hash = crypto.createHash('sha256').update(data).digest();
  // Multihash prefix: sha2-256 (0x12) + length (0x20)
  const mh = Buffer.concat([Buffer.from([0x12, 0x20]), hash]);
  // CIDv1: version (0x01) + raw codec (0x55) + multihash
  const cidBytes = Buffer.concat([Buffer.from([0x01, 0x55]), mh]);
  return 'b' + base32Encode(cidBytes); // base32 lowercase
}
```

### 3.2 CAR Archive Format

Content Addressable aRchives (CAR) provide a portable, self-contained format for IPFS data. A CAR file contains all blocks needed to reconstruct a DAG, enabling:

- Offline content distribution
- Archival backup
- Cross-system content migration

### 3.3 Multi-Gateway Verification

We verify content availability across 10+ public IPFS gateways, ensuring global accessibility regardless of network conditions or regional restrictions.

## 4. Integration with QNFO Infrastructure

The IPFS pipeline integrates with existing QNFO infrastructure:

| Layer | Component | Role |
|:------|:----------|:-----|
| **IPFS** | Content addressing | Permanent, verifiable content identity |
| **R2** | CAR archive storage | Cloudflare-based backup and gateway |
| **D1** | Metadata database | Searchable publication index with IPFS CIDs |
| **Workers** | papers-server | Dynamic paper rendering with IPFS fallback |
| **Pages** | Gateway caching | CDN-accelerated content delivery |

## 5. Future Directions

- **Filecoin integration:** Automated storage deals for guaranteed persistence
- **ENS resolution:** Human-readable domains resolving to IPFS CIDs
- **Verifiable credentials:** DID-based author attestation with cryptographic proof
- **Arweave backup:** Permanent, one-time-payment storage as final backup layer
- **zk-SNARK proofs:** Zero-knowledge verification of content without revealing it

## 6. Conclusion

Content-addressed storage represents the natural evolution of scientific publishing infrastructure. By making content verifiable by construction and persistent by protocol, we can build a research commons that outlasts any single institution, platform, or funding cycle.

---

*This paper itself is published on IPFS. Its root CID is recorded in the accompanying manifest. Verify it: `node ipfs-toolkit.js verify <CID> paper.md`*
