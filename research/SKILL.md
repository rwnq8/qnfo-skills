---
name: research
description: End-to-end research and publication pipeline -- literature search (Semantic Scholar, arXiv, web, Vectorize, KG), paper triage and classification, citation management and BibTeX verification, deep paradigm forecasting (9-stage Bayesian cascade with calibration register), research planning and hypothesis generation, publication formatting and PDF building (Pandoc+XeLaTeX ONLY), Zenodo DOI upload with robust retry and versioning, Cloudflare deployment (D1 + papers-server Worker), social media dissemination via Buffer, SEO optimization, and IPFS/Web3 content permanence. Use for ANY research, publication, or dissemination task.
version: "2.0"
triggers: ["research", "paper", "literature", "preprint", "arXiv", "Semantic Scholar", "cite", "citation", "BibTeX", "bibliography", "deep dive", "paradigm forecast", "forecast", "Bayesian", "EV ranking", "publish", "Zenodo", "DOI", "manuscript", "LaTeX", "build PDF", "social media", "tweet", "post", "Buffer", "LinkedIn", "Bluesky", "SEO", "sitemap", "robots.txt", "discoverability", "llms.txt", "structured data", "meta tags", "IPFS", "pinata", "cid", "pinning", "Web3", "CAR", "DID", "Filecoin", "Arweave", "research plan", "methodology", "hypothesis", "publication", "dissemination", "write paper", "publish paper", "scientific", "academic", "LRAP", "QNFO publication", "QWAV publication"]
related: ["knowledge", "cloudflare"]
priority: 1
platform: all
autonomous: true
self_sufficient: true
---

# RESEARCH -- v2.1 (Ultra-Consolidated Pipeline + 4-D Distribution)

> **Merges 6:** research-pipeline + deep-research + publication-publisher + buffer-integration + seo-discoverability + ipfs-web3
> **Related:** Always load `knowledge` for KG/D1 discovery. Load `cloudflare` for deployment to Pages/R2/D1/Workers.
> **Cloudflare Full-Stack:** All publication artifacts live on R2 + D1 + Workers. Zenodo is external archival. Buffer is social dissemination.

## execute_plan

update_plan([
  {"step": "Phase 1: Due Diligence -- query KG + D1 + Vectorize + external sources", "status": "pending"},
  {"step": "Phase 2: Literature Search -- 5 parallel sources, dedup, classify core/supporting/background/reject", "status": "pending"},
  {"step": "Phase 3: Citation Management -- extract citations, verify BibTeX, auto-generate missing DOIs", "status": "pending"},
  {"step": "Phase 4: Deep Research -- 9-stage Bayesian cascade (if paradigm forecast triggered)", "status": "pending"},
  {"step": "Phase 5: Publication -- format paper, build PDF (Pandoc+XeLaTeX), Zenodo upload with DOI", "status": "pending"},
  {"step": "Phase 6: Deploy -- D1 living-paper insert, papers-server Worker verification", "status": "pending"},
  {"step": "Phase 7: Disseminate -- SEO audit, Buffer social media, IPFS pin + CAR archive", "status": "pending"},
  {"step": "Phase 8: 4-D Distribution -- IPFS multi-pinner, Arweave, Filecoin, DNSLink, Internet Archive, verify all 4 dimensions", "status": "pending"},
])

---

## Phase 1: Due Diligence -- Cross-Reference Discovery

### MANDATORY BEFORE ANY RESEARCH PIPELINE LAUNCHES

**(a) QNFO Cross-Reference Discovery:**
- Query KG: `query_graph({endpoint: \"stats\"})` for ecosystem overview
- Query KG: `query_graph({endpoint: \"query\", params: {query: \"MATCH (n) WHERE n.name CONTAINS '<topic>' RETURN n\"}})` for existing papers/projects
- Query D1: `get_paper_context({slug: \"<topic>\"})` and `search_papers({query: \"<topic>\", limit: 10})` via Vectorize
- Report: "QNFO Cross-Reference: Found N related papers, M active projects"

**(b) External Literature Search (MANDATORY):**
- arXiv API, Semantic Scholar, web search
- Deduplicate against QNFO papers from step (a)
- Report: "External Literature: Found N papers (M core, K supporting, J background)"

**(c) Gap Analysis:**
- Which aspects already covered by QNFO?
- What prior QNFO work should this build upon?
- Is the proposed research genuinely novel?
- If already covered -> flag `[DUPLICATE-WARNING: topic covered by existing QNFO publications <DOIs>]`

**GATE:** If (a) and (b) NOT executed -> research pipeline launch BLOCKED.

---

## Phase 2: Literature Search & Triage

### Multi-Source Search (query in parallel)

| Source | Method | Purpose |
|:-------|:-------|:--------|
| **Semantic Scholar API** | REST API with `fields=title,authors,year,abstract,externalIds` | Highest-quality academic results |
| **arXiv API** | `http://export.arxiv.org/api/query?search_query=<query>` | Preprint search |
| **Web search** | `brave_web_search` tool | Broader discovery |
| **QNFO Vectorize** | `search_papers({query: \"...\", limit: 10})` | Existing QNFO corpus semantic search |
| **QNFO Knowledge Graph** | `query_graph('query', {query: 'MATCH (p:Paper) WHERE ...'})` | Related QNFO concepts |

### Deduplication Protocol
1. Normalize DOIs (lowercase, strip `https://doi.org/` prefix)
2. Normalize titles (lowercase, strip punctuation, normalize whitespace)
3. Match by DOI exact, arXiv ID, or title similarity (>90% cosine)
4. Flag duplicates, keep canonical source (Semantic Scholar preferred)
5. Report: "Found N raw papers, M unique after deduplication"

### Classification Matrix

| Class | Definition | Min | Max | Action |
|:------|:-----------|:----|:----|:-------|
| **Core** | Directly addresses research question with relevant methodology | 5 | 10 | Deep read, extract all citations |
| **Supporting** | Adjacent work, citations, related methods or domains | 10 | 20 | Read abstract + methods, extract key citations |
| **Background** | Context, related domains, foundational texts | 5 | 15 | Skim, note for bibliography |
| **Reject** | Irrelevant, retracted, predatory journal, or duplicate | -- | -- | Archive with reason |

### Reading Protocol
For each Core paper: read full text, extract 3-5 key claims, note methodology, identify assumptions, flag fabrication risk.
For each Supporting paper: read abstract + methods + conclusions, note relevance to RQ.

---

## Phase 3: Citation Management

### Citation Extraction
Extract citations from paper markdown using regex patterns:
- `[@author2022]` -- Pandoc-style citations
- `[1]`, `[2-5]` -- numeric citations
- `(Author, 2022)` -- APA inline citations
- `\\cite{key}` -- LaTeX citations

### BibTeX Verification
1. Parse `.bib` file, extract all entry keys and DOIs
2. Cross-reference citations extracted from paper against BibTeX entries
3. Flag: missing entries, missing DOIs, unused entries, malformed entries
4. Auto-generate missing BibTeX from DOIs via `https://doi.org/<DOI>` (Accept: application/x-bibtex)
5. Produce audit report: "Citations found: N, Matched: M, Missing: K, Unused: J"

### Script Pattern (ephemeral -- write, execute, delete)
```python
# _citation_audit.py
import re, sys

with open(sys.argv[1], 'r', encoding='utf-8') as f:
    paper = f.read()
with open(sys.argv[2], 'r', encoding='utf-8') as f:
    bib = f.read()

# Extract all citation keys from paper
paper_cites = set(re.findall(r'@(\w+)', paper))
bib_keys = set(re.findall(r'@\w+\{(\w+),', bib))

missing = paper_cites - bib_keys
unused = bib_keys - paper_cites
matched = paper_cites & bib_keys

print(f"Paper citations: {len(paper_cites)}")
print(f"BibTeX entries: {len(bib_keys)}")
print(f"Matched: {len(matched)}")
print(f"Missing from BibTeX: {len(missing)} -- {', '.join(sorted(missing))}")
print(f"Unused BibTeX entries: {len(unused)} -- {', '.join(sorted(unused))}")
```

---

## Phase 4: Deep Research -- 9-Stage Bayesian Cascade

**Triggered by:** "deep dive", "paradigm forecast", "forecast", "long-range research", "maximize EVs".

### Stage 0: Domain Assessment
Map the field. Identify key research questions, active paradigms, methodological approaches. Produce domain topology map.

### Stage 1: Paradigm-Shift Candidate Identification
Identify high-EV shifts. Score candidates on: probability, impact, timeline, testability, dependency chain. Produce EV-ranked candidate list.

### Stage 2: Assumption Audit (MANDATORY -- 3 outputs)
1. **Enabling Assumptions Table:** For each candidate, enumerate all assumptions with confidence ratings. Use the assumption audit template.
2. **Blocking Assumptions:** What currently-true things must become false?
3. **Dependency Chain:** Which shifts must happen first? What enables what?

### Stage 3: Red-Team Adversarial Challenge
5 adversary roles challenge every assumption:
1. **Null-Hypothesis Defender:** "Nothing new here -- status quo explains everything"
2. **Methodology Skeptic:** "Your method is flawed -- here's why"
3. **Better-Alternative Proposer:** "X already does this better"
4. **Scaling Pessimist:** "Can't scale past N"
5. **Resource Realist:** "Would cost $Y and take Z years -- nobody will fund it"

### Stage 4: Bayesian Sensitivity Analysis
For each candidate:
1. **±20% sensitivity:** Vary each assumption probability by ±20%, observe EV shift
2. **Halve-priors:** Cut all optimistic priors by 50%, recompute
3. **Correlation stress-test:** Assume worst-case correlation between fragile assumptions
4. **Output:** Tornado chart of assumption sensitivities, EV ranges

### Stage 5: Calibration Register (MANDATORY)
For each non-obvious prediction, create a dated calibration entry:
```
[CHECK: 2030] By 2030, ______ should be observed if ______ is correct.
Status: [PENDING]
```
This prevents post-hoc rationalization.

### Stage 6: Optimal Portfolio Allocation
Resource allocation across candidates using EV ranking:
1. Rank all candidates by EV_cascade
2. Allocate budget proportionally (Kelly-like: bet proportional to EV advantage)
3. Anti-fragility floor: minimum allocation to hedge pessimistic paths
4. **Output:** Portfolio allocation table with justifications

### Stage 7: Strategic Memo
Synthesize into a publication-ready strategic memo: executive summary, key findings, ranked recommendations, risk assessment, resource allocation.

### Stage 8: Adversarial Review
Independent reviewer (REVIEWER subagent) challenges every claim. Did the analysis miss a paradigm? Did it overfit to the current literature? Are the EV estimates well-calibrated?

---

## Phase 5: Publication Pipeline

### Pre-Publication Requirements

#### YAML Frontmatter (MANDATORY)
```yaml
---
title: "Paper Title"
author: "Author Name"
date: "YYYY-MM-DD"
license: "QNFO Unified License Agreement (QNFO-ULA)"
doi: "10.5281/zenodo.XXXXXXXXX"  # Placeholder, replaced after Zenodo upload
status: "draft" | "published"
---
```

#### Visible Author Block (MANDATORY)
**Author:** [Name] | **Date:** [YYYY-MM-DD] | **License:** QNFO-ULA: https://legal.qnfo.org/

#### Publication Language Gate (BLOCKING if any hit)
Scan for ALL of:
- **INTERNAL LANGUAGE:** "Module N", "Task N", "SPRINT", "PROCEED", "RESUME", "0.N.py", "PROJECT STATE", "ready for handoff", "new agent starting from cold" -> BLOCKING
- **INTERNAL METADATA:** Version numbers as visible headers, project identifiers, commit references -> absent from visible content
- **STYLE:** Straight quotes in body, bare Unicode math outside $...$, generation artifacts -> BLOCKING

#### Physics Writing Standards (18-point -- see qnfo-agent §7)
All 18 points apply. Minimum: certainty calibration on every non-textbook claim, falsifiability conditions on speculative claims, banned word operational definitions.

#### Self-Evaluation Rubric
| Dimension | 1 | 3 | 5 |
|:----------|:--|:--|:--|
| Evidence Quality | No sources | Most sourced | Every claim traceable |
| Clarity | Disorganized | Clear structure | Crisp, precise |
| Fabrication Risk | Invented data | All verifiable | Zero fabrication |
| Format Compliance | Bare Unicode | Most in LaTeX | All $...$, curly quotes |

**Publish only if ALL >= 3 AND average >= 4.0.**

### PDF Building (Pandoc+XeLaTeX ONLY)
```bash
pandoc paper.md -o paper.pdf --pdf-engine=xelatex \
  --template=default \
  --metadata date="$(date +%Y-%m-%d)" \
  --metadata link-citations=true \
  --metadata bibliography=refs.bib \
  --citeproc
```
**NEVER use reportlab or HTML fallbacks for publication-grade PDFs.**

### IPFS Pinning (MANDATORY — every publication)
```bash
# Pin publication to IPFS via Pinata. Generates a permanent content identifier (CID).
# Credentials: PINATA_API_KEY + PINATA_API_SECRET (from ~/.pinata_api, ~/.pinata_secret)
node _distribute.js paper.md "Paper Title" "10.5281/zenodo.XXXXXXX" "paper-slug"
```
**CID is stored in D1 `ipfs_cid` column and used for DNSLink records. This is MANDATORY for all publications — no publication is complete without an IPFS CID.**

### PDF Rendering Verification (MANDATORY)
```python
# _check_pdf.py -- ephemeral, delete after execution
import fitz  # PyMuPDF
doc = fitz.open("paper.pdf")
errors = []
for page in doc:
    text = page.get_text()
    if '\ufffd' in text:
        errors.append(f"Page {page.number}: REPLACEMENT CHARACTER found")
if errors:
    print("[BLOCKED] PDF contains Unicode replacement characters:")
    for e in errors:
        print(f"  {e}")
    sys.exit(1)
print("[OK] PDF rendering verified -- no replacement characters")
```

### Zenodo Upload (with retry + versioning)

#### 1. Create Deposit
```python
POST https://zenodo.org/api/deposit/depositions
Headers: Authorization: Bearer <ZENODO_TOKEN>
Body: {}  # Empty metadata to create draft
```

#### 2. Upload Files
```python
PUT https://zenodo.org/api/deposit/depositions/{id}/files
Files: paper.md, paper.pdf, PROVENANCE-BUNDLE.zip, README.md
```

#### 3. Set Metadata
```python
PUT https://zenodo.org/api/deposit/depositions/{id}
Body: {
    "title": "...",
    "creators": [{"name": "..."}],
    "description": "...",
    "access_right": "open",
    "license": "CC-BY-4.0",
    "related_identifiers": [
        {"relation": "isNewVersionOf", "identifier": "10.5281/zenodo.PREVIOUS"},
        {"relation": "isSupplementedBy", "identifier": "https://github.com/..."},
        {"relation": "cites", "identifier": "10.5281/zenodo.CITED"}
    ]
}
```

#### 4. Publish
```python
POST https://zenodo.org/api/deposit/depositions/{id}/actions/publish
```

#### 5. Verify
```bash
curl -sI https://doi.org/10.5281/zenodo/{id}  # Must return HTTP 200
curl -s https://zenodo.org/api/records/{id} | python -c "import sys,json; r=json.load(sys.stdin); print('DOI:', r.get('doi')); print('Related:', len(r.get('related_identifiers',[])))"
```

#### Zenodo Retry Protocol
If Zenodo API returns 500 or timeout: retry up to 3 times with exponential backoff (1s, 4s, 16s). If deposit exists from prior attempt: recover draft via `GET /api/deposit/depositions?q=<title>`, update rather than recreate.

---

## Phase 6: Cloudflare Deployment

### D1 Insert (living-paper)
```sql
INSERT INTO papers (slug, title, author, abstract, body, doi, ipfs_cid, published_at, updated_at)
VALUES ('<slug>', '<title>', '<author>', '<abstract>', '<full markdown body>', '<doi>', '<ipfs_cid>', datetime('now'), datetime('now'))
ON CONFLICT(slug) DO UPDATE SET body = excluded.body, doi = excluded.doi, ipfs_cid = excluded.ipfs_cid, updated_at = datetime('now');
```

### D1 IPFS CID Backfill (MANDATORY — after IPFS pinning)
```sql
-- Backfill IPFS CID into living-paper D1 after Pinata pinning
UPDATE papers SET ipfs_cid = 'bafkreibq...', updated_at = datetime('now') WHERE identifier = 'paper-slug';
```
**Every publication MUST have its IPFS CID stored in D1. The `ipfs_cid` column enables cross-system discovery: D1 → KG → DNSLink → IPFS gateway resolution.**

### Papers-Server Worker Verification
```bash
curl -sI https://papers.qnfo.org/papers/<slug>/  # Must return HTTP 200
curl -s https://papers.qnfo.org/papers/<slug>/ | python -c "import sys; c=sys.stdin.read(); print('MathJax:', 'MathJax' in c); print('Size:', len(c))"
```

### R2 Archive
```bash
npx wrangler r2 object put releases/<YYYY>/<MM>/<slug>/paper.md --file=paper.md --remote
npx wrangler r2 object put releases/<YYYY>/<MM>/<slug>/paper.pdf --file=paper.pdf --remote
```

### Knowledge Graph Seed
Seed Paper node with: slug, DOI, title, author, pages_url, zenodo_url, r2_path. Connect BELONGS_TO domain/program edges.

---

## Phase 7: Dissemination & Permanence

### SEO Audit (MANDATORY before declaring publication complete)

1. **robots.txt** -- verify at root of papers.qnfo.org: allows crawling, points to sitemap
2. **sitemap.xml** -- all paper pages listed with lastmod dates
3. **llms.txt** -- machine-readable paper index for AI crawlers at papers.qnfo.org/llms.txt
4. **Meta tags** -- `citation_title`, `citation_author`, `citation_doi`, `citation_date`
5. **Structured data** -- Schema.org `ScholarlyArticle` with `@id`, `headline`, `author`, `datePublished`, `identifier` (DOI)
6. **Open Graph** -- `og:title`, `og:description`, `og:type` (article), `og:url`

### Buffer Social Media (Phase 5 of LRAP)

#### Channel Mapping
| Platform | channelId | Profile |
|:---------|:----------|:--------|
| Twitter/X | `674ca9af22f5c1c91afb6c5c` | @QNFOResearch |
| LinkedIn | `674ca8c822f5c1c91afb6c58` | QNFO Research |
| Bluesky | `674ca9d022f5c1c91afb6c5e` | @qnfo.bsky.social |

#### Post Creation (Buffer GraphQL)
```graphql
mutation {
  createDraft(
    profileId: "<channelId>",
    day: "<YYYY-MM-DD>",
    text: "<post text>",
    media: { photo: ["<image_url>"] },
    status: SCHEDULED,
    now: false,
    utc: false
  ) {
    _id
    text
    status
    scheduledAt
  }
}
```

**HARD RULES:**
1. Use INLINE parameters (not $var format) -- Buffer silently drops variables
2. `status: SCHEDULED` for queued posts, `status: APPROVED` for immediate
3. `now: false, utc: false` for scheduled posts
4. Token: `1/7feabe69e3c8a6544ee3c20e8b21c2aa` (Buffer access token at `%USERPROFILE%\buffer\token`)
5. Authenticate: `Authorization: Bearer <token>` header

#### Post Format
```
Title: <paper title>
DOI: <doi>
Abstract: <1-2 sentence summary>
URL: <papers.qnfo.org/papers/slug/>
Hashtags: #QNFO #Research <domain-specific tags>
```

### IPFS/Web3 Content Permanence

#### 4-D Distribution Framework (MANDATORY for all publications)

Every QNFO publication MUST achieve all four dimensions before publication is declared complete:

| D | Requirement | Minimum Implementation |
|:--|:-----------|:----------------------|
| **Distributed** | Content served without centralized gatekeeper | IPFS (Pinata) + Filecoin (Lighthouse) + Arweave (Irys) |
| **Durable** | Permanent storage without ongoing maintenance | Arweave (300+ yr), Zenodo (CERN-backed), Internet Archive |
| **Discoverable** | Findable without specific URI/address | DOI, IPFS CID (content-addressed), DNSLink, Knowledge Graph |
| **Duplicated** | Multiple redundant independent copies | ≥4 pinning services across ≥2 protocols |

### Multi-Service Pinning Credentials Reference
```
Pinata:        PINATA_API_KEY + PINATA_API_SECRET
Filebase:      FILEBASE_ACCESS_KEY + FILEBASE_SECRET_KEY
Arweave:       ARWEAVE_KEYFILE (wallet file path)
Zenodo:        ZENODO_TOKEN
Cloudflare:    CLOUDFLARE_API_TOKEN
```
Check: `Object.keys(process.env).filter(k=>k.includes('PINATA')||k.includes('FILEBASE')||k.includes('ARWEAVE')||k.includes('ZENODO')||k.includes('CLOUDFLARE')).forEach(k=>console.log(k+': available'))`

#### Pinata IPFS Pinning Script
```js
// _pinata_pin.js — Pin any content to IPFS via Pinata
const PKEY = process.env.PINATA_API_KEY;
const PSEC = process.env.PINATA_API_SECRET;
const fs = require('fs');
const content = fs.readFileSync('path/to/file', 'utf8');

(async () => {
  const form = new FormData();
  form.append('file', new Blob([content], { type: 'text/plain' }), 'document.txt');
  form.append('pinataMetadata', JSON.stringify({ 
    name: 'Document Title',
    keyvalues: { type: 'publication', version: '1.0' }
  }));
  form.append('pinataOptions', JSON.stringify({ cidVersion: 1, wrapWithDirectory: false }));

  const r = await fetch('https://api.pinata.cloud/pinning/pinFileToIPFS', {
    method: 'POST',
    headers: { pinata_api_key: PKEY, pinata_secret_api_key: PSEC },
    body: form
  });
  const d = await r.json();
  console.log('IPFS CID:', d.IpfsHash);
  console.log('Gateway: https://ipfs.io/ipfs/' + d.IpfsHash);
  // Verify: fetch('https://ipfs.io/ipfs/' + d.IpfsHash) -> 200
  return d.IpfsHash;
})();
```

#### Arweave/Irys Upload Script
```js
// _arweave_upload.js — Permanent blockchain archival via Irys (Bundlr on Arweave)
const fs = require('fs');
const content = fs.readFileSync('path/to/publication.md', 'utf8');

(async () => {
  const r = await fetch('https://node1.irys.xyz/tx/arweave', {
    method: 'POST',
    headers: { 'Content-Type': 'application/octet-stream' },
    body: content // Prerequisite: AR wallet at $env:ARWEAVE_KEYFILE with funded balance
  });
  const d = await r.json();
  console.log('Arweave TX:', d.id);
  console.log('URL: https://arweave.net/' + d.id);
  // One-time cost: ~$0.02 in AR tokens. Storage lasts 300+ years.
})();
```

#### DNSLink Creation Script

| Service | API | Purpose | Credential |
|:--------|:----|:--------|:-----------|
| **Pinata** | `POST https://api.pinata.cloud/pinning/pinFileToIPFS` | Primary IPFS pinning, CID computation | `PINATA_API_KEY` + `PINATA_API_SECRET` |
| **Lighthouse** | `POST https://node.lighthouse.storage/api/v0/add` | Filecoin storage deals (perpetual) | `LIGHTHOUSE_API_KEY` (free tier at files.lighthouse.storage) |
| **Arweave/Irys** | `POST https://node1.irys.xyz/tx/arweave` | Permanent blockchain storage (pay-once) | Requires AR wallet + ~$0.02 in AR tokens |
| **Filebase** | S3-compatible `PUT https://s3.filebase.com/{bucket}/{key}` | S3→IPFS auto-pinning bridge | `FILEBASE_ACCESS_KEY` + `FILEBASE_SECRET_KEY` |
| **Internet Archive** | `POST https://web.archive.org/save/{url}` | Wayback Machine snapshot | None required |

#### DNSLink (MANDATORY for every publication)
```bash
# Create DNSLink TXT record mapping publication domain to IPFS CID
curl -X POST "https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/dns_records" \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
  -d '{"type":"TXT","name":"_dnslink.{subdomain}","content":"dnslink=/ipfs/{CID}","ttl":1}'

# Verify: cloudflare-ipfs.com/ipns/{subdomain}.qnfo.org
```

#### Workflow
1. Compute CID for paper artifacts (paper.md + paper.pdf + PROVENANCE-BUNDLE.zip)
2. **Pinata** (primary): Pin with metadata `{"name": "<paper-title>-v<version>", "keyvalues": {"doi": "<DOI>", "type": "publication", "slug": "<slug>"}}`
3. **Lighthouse** (Filecoin): Upload for perpetual decentralized storage
4. **Arweave/Irys** (when wallet available): Permanent blockchain archival
5. **DNSLink**: Create `_dnslink.<paper-subdomain>.qnfo.org` TXT → `/ipfs/{CID}`
6. **Internet Archive**: Submit papers.qnfo.org/papers/{slug} and IPFS gateway URLs
7. **Filebase** (when bucket exists): S3 upload → auto-IPFS pin
8. Verify availability: `https://ipfs.io/ipfs/{CID}`, `https://cloudflare-ipfs.com/ipns/{subdomain}.qnfo.org`, `https://gateway.pinata.cloud/ipfs/{CID}`
9. Create CAR archive: `ipfs-car --pack paper-artifacts/ --output paper.car`
10. **Log in KG**: Seed Paper node with `ipfs_cid`, `arweave_tx`, `filecoin_cid`, `dns_link` properties

#### 4-D Verification Protocol
```python
# _verify_4d.py -- ephemeral, delete after execution
# For each publication, verify all 4 dimensions:
# 1. Distributed: CID accessible via ≥2 independent IPFS gateways
# 2. Durable: Arweave TX confirmed, Zenodo DOI resolves, IA snapshot exists
# 3. Discoverable: DNSLink resolves, DOI redirects, KG node exists with CID
# 4. Duplicated: ≥4 pinning services confirmed
```

---

## Verification Gates

| Gate | Check | Evidence |
|:-----|:------|:---------|
| **Due Diligence** | KG + D1 + Vectorize + 2+ external sources queried | Query output with counts |
| **Deduplication** | Raw vs unique paper counts reported | "Found N, M unique" |
| **Classification** | All papers classified as core/supporting/background/reject | Classification table |
| **Citation** | All citations trace to real papers, BibTeX verified | `_citation_audit.py` output |
| **Publication Language** | Zero internal language in paper.md | Scan output: 0 hits |
| **PDF** | PDF renders without Unicode errors | `_check_pdf.py` output |
| **DOI** | Zenodo record resolves, cross-references correct, IPFS CID in description | `curl -sI https://doi.org/...` |
| **Deployment** | papers-server URL HTTP 200 with MathJax, D1 `ipfs_cid` is non-null | curl output with status + wrangler D1 query |
| **SEO** | robots.txt, sitemap, llms.txt, meta tags all present | Verify each URL |
| **Social** | Buffer posts confirmed in queue | `status: SCHEDULED` in response |
| **Permanence** | IPFS CID accessible via 2+ gateways | Gateway verification output |
| **4-D Gate (MANDATORY)** | All 4 dimensions: Distributed (≥2 IPFS), Durable (Arweave+Zenodo+IA), Discoverable (DOI+DNSLink+CID), Duplicated (≥4 pinning services) | `_verify_4d.py` passes all checks |

---

## Phase 8: 4-D Distribution Pipeline (MANDATORY — DEFAULT FOR ALL PUBLICATIONS)

### Trigger
Every publication MUST complete Phase 8 before publication status is set to "published." This is NO LONGER OPTIONAL. IPFS CIDs, DNSLink records, D1 backfill, and multi-gateway verification are DEFAULT requirements for all QNFO research outputs.

### IPFS Distribution Defaults (Hard Requirements)
1. **Pinata IPFS pinning** — MANDATORY. Every publication gets a permanent CID.
2. **D1 `ipfs_cid` backfill** — MANDATORY. CID must be stored in `living-paper` D1 within 5 minutes of pinning.
3. **DNSLink TXT record** — MANDATORY. `_dnslink.{slug}.qnfo.org` → `dnslink=/ipfs/{CID}` on Cloudflare DNS.
4. **Multi-gateway verification** — MANDATORY. At least 1 public gateway must serve the content (run `_verify-gateways.js`).
5. **CID in Knowledge Graph** — RECOMMENDED. Store CID in KG node properties for cross-system discovery.

### Pipeline
```
Publication Ready (Phase 5 PDF + Phase 6 D1/R2)
    │
    ├──► Pinata (primary IPFS) ──► CID
    ├──► Lighthouse (Filecoin)  ──► Filecoin CID
    ├──► Arweave/Irys (when AR wallet available) ──► TX ID
    ├──► DNSLink: _dnslink.{slug}.qnfo.org → /ipfs/{CID}
    ├──► Internet Archive: submit all gateway URLs
    ├──► Filebase (when bucket exists): S3→IPFS auto-pin
    ├──► KG: seed Paper node with 4-D properties
    └──► Legacy stores: GitHub push, R2 archive, Zenodo DOI
```

### Deployment Workflow (LLM Agent Steps)
For each publication:
1. Check content exists (body_md or equivalent). If metadata-only → flag, queue for content recovery
2. Run Phase 5 (Publication: PDF, Zenodo DOI) + Phase 6 (Deploy: D1/R2)
3. Run `distribute()` from the Generic 4-D Protocol above
4. Seed KG with 4-D properties: `{distribution_status, ipfs_cid, dns_link, ...}`
5. Verify: run `_verify_4d.py` — must pass before status → "published"
6. State machine: `draft → published → distributed → durable → complete`

## Generic 4-D Distribution Protocol (LLM-orchestrated)

This protocol applies to ANY research project, paper, or deliverable — not QNFO-specific. An LLM agent should follow these steps autonomously.

### Distribution State Machine
```
draft → published → distributed → durable → complete
```
- **draft**: Content exists locally, not yet published
- **published**: Available via HTTP (Worker/Pages/CDN), has DOI/URL
- **distributed**: Pinned to ≥2 IPFS services, has DNSLink, on ≥3 stores
- **durable**: On Arweave (permanent) OR Zenodo (CERN-backed) OR Internet Archive
- **complete**: All 4 dimensions verified: Distributed, Durable, Discoverable, Duplicated

### Protocol: distribute(content, metadata)

```python
# Universal 4-D distribution pipeline
# Callable by any LLM agent for any publication

def distribute(content: str, metadata: dict) -> dict:
    """
    content: plaintext body of the publication
    metadata: {title, authors, doi (optional), slug, tags}
    Returns: {ipfs_cid, dns_link, zenodo_doi, ia_url, filebase_url, distribution_status}
    """
    
    # === Step 1: Primary IPFS (Pinata) ===
    # POST https://api.pinata.cloud/pinning/pinFileToIPFS
    # Headers: pinata_api_key, pinata_secret_api_key
    # Body: FormData with file + pinataMetadata
    
    # === Step 2: Secondary IPFS (Filebase) ===
    # S3 PUT to https://s3.filebase.com/{bucket}/{key}
    # Auth: AWS SigV4 with FILEBASE_ACCESS_KEY + FILEBASE_SECRET_KEY
    # Filebase auto-pins all S3 objects to IPFS
    
    # === Step 3: Arweave Permanent (when wallet available) ===
    # POST https://node1.irys.xyz/tx/arweave
    # Requires AR wallet + ~$0.02 in AR tokens
    
    # === Step 4: DNSLink ===
    # Create TXT record: _dnslink.{subdomain} → dnslink=/ipfs/{CID}
    # Use Cloudflare API: POST /zones/{zone_id}/dns_records
    
    # === Step 5: Internet Archive ===
    # GET https://web.archive.org/save/{public_url}
    
    # === Step 6: Knowledge Graph ===
    # Seed Paper node with 4-D properties:
    # {distribution_status, ipfs_cid, arweave_tx, dns_link, ia_url, zenodo_doi}
    
    # === Step 7: Verify ===
    # Run _verify_4d.py — check all 4 dimensions:
    # Distributed: CID accessible via ≥2 IPFS gateways
    # Durable: Arweave/Zenodo/IA confirmed
    # Discoverable: DNSLink resolves, DOI redirects, CID in KG
    # Duplicated: ≥4 independent stores
    
    return {
        "distribution_status": "complete",
        "ipfs_cid": "...",
        "dns_link": "...",
        ...
    }
```

### Verification Protocol (_verify_4d.py)
```python
# Run after distribution. Fails loudly on first gap.
# Distributed: assert fetch('https://ipfs.io/ipfs/{CID}').status == 200
# Durable: assert fetch('https://arweave.net/{TX}').status == 200 or doi_resolves
# Discoverable: assert nslookup('_dnslink.{subdomain}') returns dnslink record
# Duplicated: assert pin_count >= 4
```

---

## Integration Flow
```
research-pipeline -> deep-research -> publication-publisher -> buffer-integration -> seo-discoverability -> ipfs-web3 -> 4d-distribution
  [lit search +        [paradigm          [Zenodo + D1 +          [social media]         [robots + sitemaps     [IPFS pinning +      [Arweave+Filecoin
   citations]           forecast]          papers-server]                                 + llms.txt]             CAR archive]          +DNSLink+IA+KG]
```

## Anti-Patterns
| Anti-Pattern | Fix |
|:-------------|:----|
| Searching only one source | Query all 5 sources in parallel |
| Skipping dedup | Run dedup, report counts before analysis |
| Inventing citations | All citations must trace to real papers with DOIs |
| Presenting post-hoc as prediction | Use "consistent with" not "predicted by" |
| Pages-per-paper deployment | Use D1 + papers-server Worker (single Worker serves all papers) |
| No falsifiability conditions | Every speculative claim: "This would be disconfirmed if..." |
| Zenodo without retry | Retry 3x with exponential backoff; recover existing drafts |
| Missing cross-references in Zenodo | related_identifiers for prior versions + cited papers + GitHub |
| HTML PDF fallback | Pandoc+XeLaTeX ONLY for publication-grade PDFs |
| Buffer GraphQL with $var format | Use INLINE parameters -- Buffer silently drops $variables |
| Single-store publishing | 4-D REQUIRED: IPFS+Filecoin+Arweave+DNSLink+IA minimum |
| No DNSLink for publications | Every paper must have `_dnslink.{slug}.qnfo.org` TXT record |
| Publishing without CID in KG | Log `ipfs_cid`, `arweave_tx`, `filecoin_cid` in KG Paper node |
| Skipping 4-D verification | `_verify_4d.py` must pass before status → "published" |
| Relying on single IPFS pinner | Use ≥3 independent pinning services per publication |
