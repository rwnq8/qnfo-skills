# Deliverable Registry Template

> Used in `PROJECT-PLAN.md` Phase 0 (Project Initialization). Track every deliverable across all 8 phases with its archival target and status.

| ID | Deliverable | Phase | Format | Local Path | Archival Target(s) | Status | Notes |
|---|---|---|---|---|---|---|---|
| D-0.1 | PROJECT-PLAN.md | 0 | Markdown | `PROJECT-PLAN.md` | GitHub | draft | Charter, WBS, milestones |
| D-0.2 | README.md | 0 | Markdown | `README.md` | GitHub | draft | Project overview |
| D-1.1 | Due Diligence report | 1 | Markdown | `artifacts/due-diligence.md` | GitHub | pending | KG + D1 + external cross-reference |
| D-2.1 | Literature classification | 2 | Markdown | `artifacts/lit-review.md` | GitHub | pending | Core/Supporting/Background/Reject |
| D-3.1 | Citation audit report | 3 | Markdown + BibTeX | `artifacts/citation-audit.md`, `references.bib` | GitHub | pending | |
| D-4.1 | Strategic memo (if triggered) | 4 | Markdown | `artifacts/strategic-memo.md` | GitHub | pending | 9-stage Bayesian cascade output |
| D-5.1 | Paper (markdown source) | 5 | Markdown | `<slug>.md` | GitHub, Zenodo, IPFS | pending | |
| D-5.2 | Paper (PDF) | 5 | PDF | `<slug>.pdf` | GitHub, Zenodo, IPFS | pending | Pandoc+XeLaTeX only |
| D-5.3 | Provenance bundle | 5 | ZIP | `PROVENANCE-BUNDLE.zip` | Zenodo | pending | |
| D-6.1 | D1 living-paper record | 6 | SQL row | `living-paper.papers` | Cloudflare D1 | pending | |
| D-6.2 | R2 archive copy | 6 | Files | `releases/<YYYY>/<MM>/<slug>/` | Cloudflare R2 | pending | |
| D-7.1 | SEO artifacts | 7 | Various | `robots.txt`, `sitemap.xml`, `llms.txt` | papers.qnfo.org | pending | |
| D-7.2 | Social media posts | 7 | Buffer drafts | -- | Buffer (Twitter/LinkedIn/Bluesky) | pending | |
| D-8.1 | IPFS CID | 8 | CID string | `ipfs-cids.json` | Pinata, D1, KG | pending | |
| D-8.2 | DNSLink record | 8 | DNS TXT | -- | Cloudflare DNS | pending | |
| D-8.3 | Arweave TX (optional) | 8 | TX ID | -- | Arweave | pending | Requires funded AR wallet |

**Status values:** `draft` -> `in-progress` -> `pending-review` -> `archived` -> `verified`

**Instructions:** Add one row per concrete deliverable at Phase 0 time (even if paths are provisional). Update `Status` at each phase closeout. A deliverable is not "verified" until its archival target has been independently confirmed (HTTP 200, DOI resolves, hash matches, etc.) -- see the skill's Verification Gates table.
