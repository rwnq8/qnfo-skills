---
name: web3-ipfs-deployer
description: 'Web3/IPFS development toolkit for research publication permanence — CID computation, DAG building, CAR archive creation, gateway verification, DID/ENS identity, multi-service pinning (Pinata, web3.storage, Lighthouse, Filecoin, Arweave), and end-to-end publication pipeline integration with QNFO infrastructure (Cloudflare R2, D1, Workers, Pages). Use when the user wants to — (1) compute IPFS CIDs or generate content-addressed manifests, (2) create CAR archives for publication preservation, (3) verify content availability across IPFS gateways, (4) generate DIDs and sign content attestations, (5) pin content to IPFS pinning services, (6) explore or deploy IPFS/Web3 permanence layers for research publications, (7) design or implement content-addressed storage architecture, or (8) run the full QNFO publication-to-IPFS pipeline.'
version: "1.1"
---

> **INCLUDES AUTONOMOUS RED-TEAM SELF-AUDIT.** Before claiming this skill complete, autonomously run: (1) Output Verification -- negative verification. (2) Assumption Challenge -- state and test every assumption. (3) Edge Case Check -- empty/null/max/boundary/desync. (4) DoD Integration -- verify all criteria met with tool evidence. (5) Iteration -- retry on failure, max 3. ANTI-PATTERN: User should NEVER ask about quality.

### Programmatic Loading & Execution
This skill is loaded and executed **programmatically by the LLM system** 
during response generation. Loading is triggered automatically via 
`skill_view('web3-ipfs-deployer')` or `read()` with filesystem path.
**The user NEVER manually loads this skill.** The `skill-autoloader` 
detects task patterns and handles all skill loading. If this skill fails 
to load, the LLM system automatically retries via the fallback chain 
documented below.
**Pinning:** This skill is [On-demand — loads when triggered by task patterns].

### Skill Loading Retry Protocol
If `skill_view('name')` fails during programmatic loading, the LLM system 
MUST execute this fallback chain:
1. **Retry 1:** `read('%USERPROFILE%\.deepchat\skills\<name>\SKILL.md')`
2. **Retry 2:** Pull from Cloudflare R2: `npx wrangler r2 object get 
   qnfo/prompts/skills/<name>/SKILL.md --remote --file=_skill.md`
3. **Retry 3:** If R2 fails, search local filesystem for any cached copy
4. **Fallback:** If ALL retries fail, continue with `[SKILL-UNAVAILABLE: <name>]` 
   and best-effort knowledge
**NEVER silently proceed without a skill's critical instructions.** If a skill 
is required for the task and cannot be loaded after 3 retries, escalate to 
the user with the specific failure reason.

---

> **Related:** cloudflare-deployer
# WEB3/IPFS DEPLOYER SKILL — v1.0

> **POC/Experimental.** Pure Node.js IPFS/Web3 toolkit for research publication permanence. Zero external dependencies for core CID/DAG/CAR operations.

---

## execute_plan (MANDATORY — Before Any Execution)

**This skill involves execution-heavy workflows.** Before executing, use update_plan to populate a concrete, verifiable checklist.

### Execution Protocol

1. **Populate update_plan** with workflow phases as concrete checklist items
2. **Execute one item at a time** — at most ONE in_progress
3. **Mark items completed ONLY with tool evidence** (Test-Path, exec output, git log)
4. **Never claim completion without execution evidence**
5. **If blocked:** Flag as [BLOCKED: reason] and move to the next item

### Example Plan

```json
[
  {"step": "Compute IPFS CIDs for publication files", "status": "pending"},
  {"step": "Generate DAG root CID and manifest", "status": "pending"},
  {"step": "Create CAR archive", "status": "pending"},
  {"step": "Generate author DID and sign attestation", "status": "pending"},
  {"step": "Pin to configured services", "status": "pending"},
  {"step": "Verify content across gateways", "status": "pending"},
  {"step": "Upload CAR to Cloudflare R2", "status": "pending"},
  {"step": "Update D1 papers table with IPFS CID", "status": "pending"}
]
```

---

## Purpose

Provides a complete, zero-dependency IPFS/Web3 toolkit for QNFO research publication permanence. Enables content-addressed storage, decentralized identity, multi-service pinning, gateway verification, and integration with existing QNFO infrastructure (Cloudflare R2, D1, Workers, Pages).

## When to Use

| Trigger | Action |
|:--------|:-------|
| "Compute IPFS CIDs for my publication" | Run `ipfs-toolkit.js manifest <dir>` |
| "Create a CAR archive" | Run `ipfs-toolkit.js car <dir> <output>` |
| "Verify this CID against my file" | Run `ipfs-toolkit.js verify <cid> <file>` |
| "Generate a DID for author attribution" | Run `web3-identity.js generate <output>` |
| "Sign an attestation for this CID" | Run `web3-identity.js` attest workflow |
| "Pin this to Pinata/web3.storage" | Run `pinning-service.js pin <cid> --all` |
| "Check gateway availability for a CID" | Run `gateway-verifier.js test <cid>` |
| "Run the full publication pipeline" | Run `publication-pipeline.js publish <dir>` |
| "What's the IPFS/Web3 landscape?" | Read `references/LANDSCAPE-SURVEY.md` |
| "How to integrate IPFS with our infra?" | Read `references/INTEGRATION-DESIGN.md` |

---

## Prerequisites

1. **Node.js 18+** — required for all scripts. Verify: `node --version`
2. **No npm dependencies** — all core CID/DAG/CAR operations use Node built-in `crypto`
3. **Pinning service API keys** (optional, for remote pinning):
   - Pinata: JWT or API Key + Secret at `%USERPROFILE%\.pinning-config.json` or env vars `PINATA_JWT` / `PINATA_API_KEY` + `PINATA_SECRET_KEY`
   - web3.storage: token at `WEB3_STORAGE_TOKEN`
   - Lighthouse: API key at `LIGHTHOUSE_API_KEY`
4. **Cloudflare API token** (optional, for R2 uploads): `$env:CLOUDFLARE_API_TOKEN`

---

## Skill Structure

```
web3-ipfs-deployer/
├── SKILL.md                              ← This file
├── scripts/
│   ├── ipfs-toolkit.js                   ← CID/DAG/CAR/IPLD engine (zero deps)
│   ├── web3-identity.js                  ← DID:key + attestations + ENS
│   ├── pinning-service.js                ← Multi-service pinning (Pinata, w3s, Lighthouse)
│   ├── gateway-verifier.js               ← 11-gateway content verification
│   └── publication-pipeline.js           ← E2E QNFO → IPFS orchestration
├── references/
│   ├── LANDSCAPE-SURVEY.md               ← Comprehensive IPFS/Web3 ecosystem survey
│   └── INTEGRATION-DESIGN.md             ← Architecture + QNFO infra mapping
└── assets/
    └── sample-publication/               ← Template: paper.md + abstract.txt + metadata.json
```

---

## Embedded Scripts

> **SELF-CONTAINED:** This skill bundles 5 executable scripts. Before executing any script, verify it exists at its canonical path under this skill root.

| Script | Purpose | Key Commands |
|:-------|:--------|:-------------|
| `scripts/ipfs-toolkit.js` | CID computation, DAG building, CAR creation, IPLD metadata | `compute`, `dag`, `car`, `verify`, `manifest`, `metadata` |
| `scripts/web3-identity.js` | DID:key generation, content attestation, ENS contenthash | `generate`, `attest`, `verify`, `ens-contenthash`, `did-resolve` |
| `scripts/pinning-service.js` | Multi-service pinning abstraction | `status`, `pin`, `unpin`, `strategies` |
| `scripts/gateway-verifier.js` | 11-gateway content verification | `test`, `dashboard`, `best`, `practices` |
| `scripts/publication-pipeline.js` | End-to-end QNFO → IPFS pipeline | `publish`, `stage`, `verify` |

### Bootstrap Protocol

All scripts are self-contained under this skill's `scripts/` directory. No pulling from R2 needed.

**Script execution:**
```bash
node "%USERPROFILE%\.deepchat\skills\web3-ipfs-deployer\scripts\<script>.js" <command>
```

---

## Workflow — 5 Stages

### Stage 1: Compute CIDs & Generate Manifest

```bash
# Compute manifest for a publication directory
node scripts/ipfs-toolkit.js manifest <publication-dir> "Publication Title"

# Output: ipfs-manifest.json with root CID, file CIDs, gateway URLs, stats
```

**What this produces:**
- CIDv1 for every file (base32, sha2-256)
- Root CID (DAG-PB directory node if multiple files)
- IPLD metadata node (DAG-JSON)
- Gateway URLs for 6+ public gateways
- SHA-256 hashes for independent verification

### Stage 2: Create CAR Archive

```bash
# Create self-contained CARv1 archive
node scripts/ipfs-toolkit.js car <publication-dir> <output>.car

# Output: <output>.car — portable, self-verifiable IPFS archive
```

### Stage 3: Generate Author Identity & Attestation

```bash
# Generate Ed25519 keypair + DID:key (once per author)
node scripts/web3-identity.js generate .author-identity.json

# DID is stored in .author-identity.json
# Private key is stored in .author-identity.secret — MOVE TO SECURE LOCATION

# Resolve a DID to public key (verification)
node scripts/web3-identity.js did-resolve did:key:z6Mk...

# Compute ENS contenthash (EIP-1577) for a CID
node scripts/web3-identity.js ens-contenthash bafy...
```

### Stage 4: Pin & Persist

```bash
# Check service configuration status
node scripts/pinning-service.js status

# Show pinning strategy recommendations
node scripts/pinning-service.js strategies

# Pin to all configured services
node scripts/pinning-service.js pin <cid> --all

# Pin to specific service
node scripts/pinning-service.js pin <cid> --service pinata

# Pin with Filecoin storage deal (via Lighthouse)
node scripts/pinning-service.js pin <cid> --with-filecoin
```

### Stage 5: Verify & Monitor

```bash
# Test content availability across all gateways
node scripts/gateway-verifier.js test <cid>

# Test specific gateways only
node scripts/gateway-verifier.js test <cid> --gateways cloudflare,pinata,dweb_link

# Find fastest responding gateway
node scripts/gateway-verifier.js best <cid>

# Show regional gateway best practices
node scripts/gateway-verifier.js practices
```

---

## End-to-End Pipeline (Orchestration)

```bash
# Run complete pipeline: prepare → identify → metadata → pin → verify → integrate
node scripts/publication-pipeline.js publish <publication-dir>

# Run specific stages only
node scripts/publication-pipeline.js publish <publication-dir> --stages prepare,metadata,pin

# Skip R2 upload or D1 update
node scripts/publication-pipeline.js publish <publication-dir> --no-r2 --no-d1

# Run a single stage
node scripts/publication-pipeline.js stage verify <publication-dir>
```

**Pipeline stages:**
1. **PREPARE**: Gather files, compute CIDs, create CAR archive
2. **IDENTIFY**: Generate/load author DID, create content attestation
3. **METADATA**: Build IPLD metadata node, generate enriched manifest
4. **PIN**: Submit to configured pinning services
5. **VERIFY**: Check content availability across gateways
6. **INTEGRATE**: Upload to R2, update D1, update Discovery Index

---

## Persistence Tier Model

| Tier | Technology | Duration | Cost | Use For |
|:-----|:-----------|:---------|:-----|:--------|
| Tier 0: Active | R2 + Pages CDN | Immediate | $0 | Primary serving |
| Tier 1: Available | IPFS Gateways | As accessed | $0 | Global availability |
| Tier 2: Pinned | Pinata + web3.storage | Years | ~$5-20/mo | Guaranteed availability |
| Tier 3: Guaranteed | Filecoin Deals | 1.5-10 years | <$0.01/GB | Economic persistence |
| Tier 4: Permanent | Arweave | Centuries | ~$5/GB one-time | Forever archive |
| Tier ∞: Sovereign | Local CAR file | Forever | $0 | You always have a copy |

**Recommendation:** At QNFO's current scale (~170 papers, ~50 MB), Tiers 0-2 run at **zero cost** under all free tiers. Add Tier 3 for landmark papers. Consider Tier 4 only for archival corpus.

---

## Pinning Service Configuration

### Pinata (Recommended Primary)

```bash
# Store Pinata JWT
echo "PINATA_JWT=your-jwt-here" > $env:USERPROFILE\.pinning-config.json
# OR use env vars:
# $env:PINATA_API_KEY = "..."
# $env:PINATA_SECRET_KEY = "..."
```

### web3.storage (Recommended for Persistence)

```bash
$env:WEB3_STORAGE_TOKEN = "your-token-here"
```

### Lighthouse (for Filecoin Deals)

```bash
$env:LIGHTHOUSE_API_KEY = "your-key-here"
```

### Pinning Strategies

| Strategy | Services | Cost | Persistence |
|:---------|:---------|:-----|:------------|
| **Minimal** | Local (CID only) | $0/mo | As long as content is accessed |
| **Standard (Recommended)** | Pinata + web3.storage | ~$5-20/mo | 10+ years (Filecoin auto-deals) |
| **Robust** | Pinata + web3 + Lighthouse + Crust | ~$20-50/mo | 20+ years (multi-network) |
| **Archival** | All services + Arweave | ~$50-100/mo + one-time | Centuries (Arweave permanence) |

View all strategies: `node scripts/pinning-service.js strategies`

---

## Identity & Attribution

### DID:key (No Blockchain Required)

```bash
# Generate identity (Ed25519)
node scripts/web3-identity.js generate .qnfo-author.json

# Output:
# {
#   "did": "did:key:z6MkqpPLqUHAQKDPTm4ChWaxVXSRP2GWJ5xqjAso8EagSm43",
#   "publicKey": "a8da0119...",
#   "method": "did:key",
#   "keyType": "Ed25519"
# }
```

### Content Attestation

After generating DID + computing CID, sign an attestation:

```python
# Attestation format:
{
  "payload": {
    "creator": "did:key:z6Mk...",
    "claim": { "type": "ContentAuthorship", "cid": "bafy..." },
    "created": "2026-07-03T..."
  },
  "signature": "base64url-ed25519-signature"
}
```

### ENS Contenthash (EIP-1577)

```bash
node scripts/web3-identity.js ens-contenthash bafybeien574xc2zby...
# → { cid: "bafy...", ensContentHash: "0xe3017012208def...", standard: "EIP-1577" }
```

---

## Gateway Verification

| Gateway | URL Pattern | Reliability |
|:--------|:------------|:------------|
| Cloudflare | `cloudflare-ipfs.com/ipfs/{cid}` | Very High |
| IPFS.io | `ipfs.io/ipfs/{cid}` | High |
| dweb.link | `dweb.link/ipfs/{cid}` | High |
| Pinata | `gateway.pinata.cloud/ipfs/{cid}` | High |
| w3s.link | `{cid}.ipfs.w3s.link` | High |
| 4EVERLAND | `4everland.io/ipfs/{cid}` | Medium |
| Fleek | `{cid}.ipfs.fleek.co` | High |
| Infura | `ipfs.infura.io/ipfs/{cid}` | High |

**Regional best practices:**
- **Production:** Cloudflare primary → dweb.link → ipfs.io
- **China/Asia:** 4EVERLAND primary
- **Archival:** dweb.link + ipfs.io (Protocol Labs uptime guarantees)
- **Research:** Multi-gateway redundancy (Cloudflare + ipfs.io + dweb.link + pinata)

---

## Integration with QNFO Infrastructure

| Component | Integration | Method |
|:----------|:------------|:-------|
| **R2** | CAR archive cold storage | `wrangler r2 object put qnfo/releases/ipfs/<slug>/publication.car --remote` |
| **D1** | Metadata with IPFS CID | `INSERT INTO papers ... ipfs_cid = '<cid>'` |
| **Workers** | IPFS fallback gateway | Worker fetches from `cloudflare-ipfs.com/ipfs/<cid>` |
| **Pages** | CDN-cached rendering | Pages serves from R2; R2 backed by IPFS CAR |
| **Discovery Index** | IPFS-native discovery | `discovery-index-entry.json` with `protocol: "ipfs://"` |

---

## Filecoin & Arweave

### Filecoin Storage Deals (via Lighthouse)

```bash
# Pin + create Filecoin deal in one command
node scripts/pinning-service.js pin <cid> --with-filecoin

# Deals in production:
#   Duration: 525 epochs (~1.5 years), extendable
#   Replication: 3 miners
#   Cost: fractions of a cent per deal
```

### Arweave Permanent Archive

```bash
# Not yet automated in scripts — manual via ardrive.io or arkb CLI
# Cost: ~$5/GB one-time (QNFO corpus: ~$0.25 total)
```

---

## IPLD (InterPlanetary Linked Data)

The toolkit supports DAG-JSON metadata nodes with CID links:

```json
{
  "title": "Paper A",
  "references": [
    { "/": "bafy...cid-of-paper-b" },
    { "/": "bafy...cid-of-paper-c" }
  ]
}
```

This enables citation graphs and cross-publication linking via content addressing. See `references/INTEGRATION-DESIGN.md` §5 for full IPLD design.

---

## Protocol Maturity

| Protocol | Maturity | Recommendation |
|:---------|:---------|:---------------|
| IPFS (core) | Production | ✅ Use immediately |
| CIDv1 | Stable | ✅ Canonical format |
| CARv1 | Stable | ✅ Archive format |
| did:key | Stable | ✅ Identity (no blockchain) |
| Filecoin deals | Production | ✅ Persistence layer |
| Arweave | Production | ⚠️ Archive tier only |
| ENS (EIP-1577) | Stable | ⚠️ Optional, cost + complexity |
| Verifiable Credentials v2 | W3C CR | ⚠️ Use v2 data model |

---

## Failure Handling

| Scenario | Response |
|:---------|:---------|
| `node --version` < 18 | [BLOCKED] Upgrade Node.js to 18+ |
| Script not found | Verify `%USERPROFILE%\.deepchat\skills\web3-ipfs-deployer\scripts\` exists |
| Pinata returns 401 | Token expired — regenerate at pinata.cloud |
| web3.storage returns 401 | Token expired — regenerate at web3.storage |
| Gateway returns timeout | Gateway may be rate-limited — try another gateway |
| R2 upload fails | Verify `$env:CLOUDFLARE_API_TOKEN` — run `npx wrangler whoami` |
| CAR creation fails on large files | Split into smaller publication directories |
| CID mismatch on verification | Content has been modified — file changed since CID was computed |
| DID persistence lost | Keys are stored locally — back up `.author-identity.secret` file |

---

## Reference Files

- **Comprehensive landscape survey:** `references/LANDSCAPE-SURVEY.md` — 13-section survey covering content addressing, 7 pinning services, 11 gateways, Web3 identity, IPLD, Filecoin/Arweave, JS ecosystem (20+ packages), protocol maturity, regulatory analysis
- **Integration design document:** `references/INTEGRATION-DESIGN.md` — Architecture decision document: 6-tier persistence model, data flow mapping to QNFO infra (R2/D1/Workers/Pages/Vectorize), cost analysis, 8-phase roadmap, risk assessment

---

## Quick Reference

```bash
# Most common workflows:

# 1. Compute CIDs for a publication
node scripts/ipfs-toolkit.js manifest ./my-paper/ "My Paper Title"

# 2. Create portable archive
node scripts/ipfs-toolkit.js car ./my-paper/ my-paper.car

# 3. Verify content integrity
node scripts/ipfs-toolkit.js verify bafy...abc paper.md

# 4. Generate author identity
node scripts/web3-identity.js generate .author.json

# 5. Check pinning service status
node scripts/pinning-service.js status

# 6. Pin to all configured services
node scripts/pinning-service.js pin bafy...abc --all

# 7. Test gateway availability
node scripts/gateway-verifier.js test bafy...abc

# 8. Run full pipeline
node scripts/publication-pipeline.js publish ./my-paper/
```

---

*web3-ipfs-deployer v1.0 — POC/Experimental. Zero-dependency IPFS toolkit for QNFO research publication permanence.*

> **Version:** (Kaizen-audited 2026-07-08)
