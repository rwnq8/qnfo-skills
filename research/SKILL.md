---
name: research
description: End-to-end research and publication pipeline -- GitHub + Zenodo + R2 + D1/KG core distribution stack (v2.8, deprecated proprietary IPFS/blockchain pinning). Project initialization, literature search, citation management, deep research, publication, deployment, and core distribution -- project initialization (Phase 0 scaffold, pre-flight checklist, WBS), literature search (Semantic Scholar, arXiv, web, Vectorize, KG), paper triage and classification, citation management and BibTeX verification, deep paradigm forecasting (9-stage Bayesian cascade with calibration register), research planning and hypothesis generation, publication formatting and PDF building (Pandoc+XeLaTeX ONLY), Zenodo DOI upload with robust retry and versioning, Cloudflare deployment (D1 + papers-server Worker), social media dissemination via Buffer, SEO optimization, core distribution stack (GitHub + Zenodo + R2 + D1/KG), and phase closeout protocol with version tagging. Use for ANY research, publication, project lifecycle, or dissemination task.
version: "2.9"
triggers: ["research", "paper", "literature", "preprint", "arXiv", "Semantic Scholar", "cite", "citation", "BibTeX", "bibliography", "deep dive", "paradigm forecast", "forecast", "Bayesian", "EV ranking", "publish", "Zenodo", "DOI", "manuscript", "LaTeX", "build PDF", "social media", "tweet", "post", "Buffer", "LinkedIn", "Bluesky", "SEO", "sitemap", "robots.txt", "discoverability", "llms.txt", "structured data", "meta tags", "IPFS", "filebase", "cid", "pinning", "Web3", "CAR", "DID", "Filecoin", "Arweave", "research plan", "methodology", "hypothesis", "publication", "dissemination", "write paper", "publish paper", "scientific", "academic", "LRAP", "QNFO publication", "QWAV publication"]
related: ["knowledge", "cloudflare", "git-github"]
priority: 1
platform: all
autonomous: true
self_sufficient: true
---

# RESEARCH -- v2.9 (Core Pipeline: GitHub + Zenodo + R2 + D1/KG)

> **v2.9 UPDATE (2026-07-21, Zenodo credential incident):** Added the
> **Zenodo Credential Protocol** section (in Phase 5, immediately before
> "Zenodo Upload") after a session diagnosed ~15 false "token dead /
> read-only scope" 403s that were actually caused by manually
> retyping/reconstructing a token from a truncated terminal display,
> introducing a one-character transcription error invisible by symptom.
> New scripts: `scripts/zenodo-token-check.py` (run FIRST on any Zenodo
> 403 -- distinguishes real scope problems from credential-transcription
> errors in one call), `scripts/zenodo-create-upload.py` and
> `scripts/zenodo-metadata-publish.py` (canonical create/upload/
> metadata/publish pipeline, replacing ad hoc inline scripts, with
> built-in live-DOI verification). Required token scopes documented:
> `deposit:write`, `deposit:actions`, `user:email`.

> **v2.7 UPDATE (2026-07-20, Pinata quota exceeded):** Pinata IPFS pinning
> REMOVED from all publication steps — the free-tier account hit its quota
> and is blocked. Replaced with **Filebase** (free 5GB S3-compatible bucket,
> auto-pins to IPFS, no request-volume limit) as the PRIMARY pinner, backed
> by **Lighthouse** (free Filecoin tier) as secondary pinner, **Cloudflare
> R2** as the canonical durable host, and **Cloudflare DNS** for DNSLink —
> all free, unlimited-request services. Every `api.pinata.cloud` reference,
> credential check, and gateway URL (`gateway.pinata.cloud`) has been
> removed or replaced. See `scripts/filebase-pin.js` (new) and the updated
> `cloudflare` skill's `scripts/filebase-upload.js` for the SigV4 upload
> helper. `scripts/pinata-pin.js` is retained on disk for historical
> reference only and MUST NOT be invoked — see its deprecation header.

> **v2.6 UPDATE (2026-07-20, kaizen audit):** Added `scripts/unicode-latex-preprocess.py` (fixes XeLaTeX Unicode-glyph and `keywords:`-field build failures -- A1/A2), `scripts/check-pdf.py` (PyMuPDF preflight + file-lock-safe replace -- B4/B5), `scripts/credential-scan.py` (pre-commit + pre-publish token leak scanner -- A4/C1/D2) wired into the Phase Closeout Protocol STEP 0.5 and the Publication Language Gate, `templates/gitignore-research-project-template.txt` for new project repos, a PROVENANCE-BUNDLE.zip hard gate before Zenodo upload (A3), `.zenodo_versions.json` version-chain tracking convention (C2), a Vectorize confirmation-bias disclosure requirement (C3), a multi-pinner IPFS fallback order Pinata→Filebase→Lighthouse (C4), documented Windows/PowerShell anti-patterns for inline `python -c`, `&&` chaining, and `curl` aliasing (B1/B2/B3), a YAML `---` delimiter conflict check (D3), an auto-discover related_identifiers KG query step (D4), a tag-backfill check in Phase Closeout (D1), and an Obsidian/external-path source material limitation note (C5/D5).

> **v2.5 UPDATE (2026-07-19): Added OSF Project Registration (Phase 5.5) for major research with falsifiable predictions. Added P11 (OSF GATE-CONDITIONAL) to Pre-Flight checklist. OSF policy: all resources public by default, API-only automation, external links (Zenodo/GitHub/IPFS) replace file uploads � NEVER require manual browser interaction.

> **v2.4 UPDATE's R2-Immediate-Write + Per-Turn Checkpoint Protocol (per-turn R2 sync, phase-end GitHub push + Zenodo version, session/project-conclusion IPFS pin + social promotion for FINAL deliverables only).

> **Merges 6:** research-pipeline + deep-research + publication-publisher + buffer-integration + seo-discoverability + ipfs-web3
> **v2.2 UPDATE (2026-07-18):** Merged in Phase 0 (Project Initialization), Pre-Flight Checklist (P1-P11), Cross-Skill Integration Checklist, Phase Closeout Protocol, Deliverable Registry / Risk Register templates, and Version Tagging Protocol (previously drafted as a separate, since-retired `research-v2` duplicate skill -- consolidated here as the single canonical research skill).
> **v2.3 UPDATE (2026-07-18):** Added mandatory REPO-TARGET GATE (`git remote -v` check) before every tag/commit/release in Phase 0 and the Phase Closeout Protocol, following ADR-026 Incident 3 (a prior session's Phase Closeout tags -- `v0.1-phase0`, `v1.0.0`, etc. -- plus a Zenodo-DOI GitHub Release were mistakenly created inside `qnfo-skills` instead of the project's own repo, requiring backup+delete remediation).
> **Related:** Always load `knowledge` for KG/D1 discovery. Load `cloudflare` for deployment to Pages/R2/D1/Workers. Load `git-github` for Phase 0 init and every phase closeout.
> **Cloudflare Full-Stack:** All publication artifacts live on R2 + D1 + Workers. Zenodo is external archival. Buffer is social dissemination.

## execute_plan

update_plan([
  {"step": "Phase 0: Project Initialization -- repo, scaffold, WBS, core claim lock", "status": "pending"},
  {"step": "Pre-Flight: Run P1-P11 checklist -- HARD gates must pass before Phase 1", "status": "pending"},
  {"step": "Phase 1: Due Diligence -- query KG + D1 + Vectorize + external sources", "status": "pending"},
  {"step": "Phase 2: Literature Search -- 5 parallel sources, dedup, classify core/supporting/background/reject", "status": "pending"},
  {"step": "Phase 3: Citation Management -- extract citations, verify BibTeX, auto-generate missing DOIs", "status": "pending"},
  {"step": "Phase 4: Deep Research -- 9-stage Bayesian cascade (if paradigm forecast triggered)", "status": "pending"},
  {"step": "Phase 5: Publication -- format paper, build PDF (Pandoc+XeLaTeX), Zenodo upload with DOI", "status": "pending"},
  {"step": "Phase 6: Deploy -- D1 living-paper insert, papers-server Worker verification", "status": "pending"},
  {"step": "Phase 7: Disseminate -- SEO audit, Buffer social media, papers.qnfo.org verification", "status": "pending"},
  {"step": "Phase 8: Core Distribution -- GitHub push + tag, Zenodo new-version, R2 archive sync, D1/KG records, DNSLink (optional)", "status": "pending"},
])

**Note:** Phase 0 and the Pre-Flight checklist apply to net-new, long-lived research projects (new repo, new WBS). For a single paper/update within an existing project, skip directly to Phase 1.

---

## Tool-Call Execution Mandate (Anti-Phantom Gate — MANDATORY, 2026-07-21)

This skill already carries extensive per-phase verification gates (BibTeX
audit, PDF rendering check, DOI resolution, papers-server HTTP 200, etc.).
This section is the umbrella rule they all serve: **no remote publication
action — Zenodo deposit, GitHub push/tag/release, R2 upload, D1
living-paper insert, OSF registration, Buffer post — may be reported as
successful without an INDEPENDENT re-query of the live state in the SAME
turn.** An API's immediate `"success": true`/`201 Created` response is the
FIRST signal, not the LAST — it confirms the request was accepted, not
that the artifact is durably live and correct.

1. **Zenodo** — never report "published" from the create/publish API response alone. Wait for indexing, then verify via `curl -sI https://doi.org/10.5281/zenodo.<id>` returning HTTP 200 (not the Zenodo API's own state field).
2. **Git push** — verify via an independent GitHub API query (`GET /repos/{owner}/{repo}/commits/{sha}`) or `git ls-remote origin <branch>`, not the local push exit code alone.
3. **R2 upload** — download the file back (`wrangler r2 object get ... --remote`) and compare size/hash to the source.
4. **D1 living-paper / KG inserts** — re-run a `SELECT`/`/neighbors` query and show the row/edge actually present.
5. **OSF registrations** — confirm via `GET /v2/registrations/{id}/` showing the real `date_registered`/`pending_registration_approval` state, never assert "registered" from the POST response body alone.
6. **Any claim this session already reported success on** — if closing out or continuing a prior session's claim, re-verify live state before repeating the claim; a prior turn's phantom claim propagates if not re-checked (see memory: never trust a remote action as successful without confirming actual server-side state).
7. If live re-verification cannot be run in this turn, the response MUST read `[NOT-VERIFIED: reason]` instead of "published"/"deployed"/"live"/"confirmed".

---

## Phase 0: Project Initialization (BLOCKING GATE for new projects)

> **HARD GATE:** Phase 1 MUST NOT begin until all Phase 0 deliverables are committed.

### 0.1 Repository and Infrastructure

Standard directory scaffold:
```
<project-slug>/
├── README.md
├── PROJECT-PLAN.md
├── .gitignore
├── docs/            # Source documents, prior work
├── artifacts/       # Literature reviews, gate memos, test results
├── notebooks/       # Working notes, calculation notebooks
└── releases/        # Versioned Zenodo-ready bundles
```

Git init on feature branch (NEVER main/master). Create GitHub repo via `gh repo create`.

**`.gitignore` (kaizen fix A4):** copy `templates/gitignore-research-project-template.txt`
into the new project's `.gitignore`. It excludes `_*.py`/`_*.js` (ephemeral
scripts frequently contain hardcoded tokens during development), `.env`,
`*.token`, `keys.json`, and standard build/OS noise. A project repo is NOT
the qnfo-skills allowlist repo -- it needs its own permissive `.gitignore`,
not the skills repo's default-deny one.

**REPO-TARGET GATE (HARD, MANDATORY — check before `git init`/`git tag`/`gh repo create`):**
```
git remote -v   # or: git -C <target-dir> remote -v
```
Verify the remote/working directory is the project's OWN repo
(`QNFO/<project-name>` or `QNFO/qnfo-research`) — **NEVER `QNFO/qnfo-skills`.**
`qnfo-skills` is a skills-only repo (ADR-026) and its tags/releases are
reserved for skill versioning, never research project phases. This check
applies to every step in this skill that creates a git tag, commit, or
GitHub Release — not just Phase 0. Verify the repo target FRESH each time;
do not assume a prior verification still holds after switching directories,
subagent delegation, or a long session. **A single misdirected `git tag` or
`gh release create` inside qnfo-skills is a policy violation that requires
full remediation (backup + delete + audit) — see ADR-026 Incident 3.**

### 0.2 Project Plan and WBS

Write `PROJECT-PLAN.md` with: Charter, Phases with WBS, Milestones with gate criteria, Deliverable Registry (see `templates/deliverable-registry-template.md`), Risk Register (see `templates/risk-register-template.md`), Success Criteria, Version History.

### 0.3 Core Claim Lock

If project audits/evaluates a claim: restate in logically valid, falsifiable terms. Document original AND reformulation if original had errors. Lock in `PROJECT-PLAN.md §1.2`.

### 0.4 Knowledge Graph / Memory Seed

Query KG for existing related papers/projects. Log novel project to working memory.

### 0.5 Closeout

Execute Phase Closeout Protocol (below). Tag: `v0.1-phase0`.

**Source material path limitation (kaizen fix C5):** if source materials
(e.g. Obsidian vault notes) live outside the workspace/allowed directories
(e.g. `D:\Obsidian`), `glob`/`read` cannot access them directly. This is a
platform limitation, not a bug to work around silently -- document it and
ask the user to either (a) copy the specific files into the project
workspace, or (b) run an `exec` command with an explicit `cwd` pointing at
the external path if the environment permits Full Access mode. Do not
assume such files don't exist just because a glob search returns empty.

---

## Pre-Flight Checklist (BLOCKING -- runs before Phase 1)

**HARD GATE:** Every item marked HARD must pass before Phase 1 begins.

| ID | Check | Gate | How to Verify |
|---|---|---|---|
| **P1** | Git repo initialized on feature branch? | HARD | `git branch --show-current` != main/master |
| **P2** | GitHub remote configured and pushed? | HARD | `git remote -v` shows origin; `gh repo view` succeeds |
| **P3** | Directory structure created? (`docs/`, `artifacts/`, `notebooks/`, `releases/`) | HARD | Directory listing shows all 4 dirs |
| **P4** | `PROJECT-PLAN.md` written with charter, WBS, milestones, deliverables, risks? | HARD | All 6 sections populated; no placeholder text |
| **P5** | `README.md` written with project overview? | SOFT | File exists with name, status, quick start |
| **P6** | Core claim reformulated and locked (if applicable)? | HARD | `PROJECT-PLAN.md §1.2` contains locked, logically valid formulation |
| **P7** | `.gitignore` present? | SOFT | File exists covering IDE, OS, build artifacts |
| **P8** | Phase 0 committed, tagged, and pushed? | HARD | `git tag -l 'v0.1*'` returns tag; `git log -1 --oneline` shows Phase 0 commit |
| **P9** | Project logged to Knowledge Graph / working memory? | SOFT | Memory recall returns project entry |
| **P10** | Cross-skill integration checklist reviewed? | SOFT | All relevant skills loaded per integration table |
| **P11** | OSF project created for qualifying research? (MAJOR projects ONLY — skip for exploratory studies, single papers, or minor updates) | SOFT-CONDITIONAL | OSF API: project public, components linked to Zenodo/GitHub, registration drafts created. File upload via API NOT supported — use external links (Zenodo DOI, GitHub raw) instead. NEVER require manual browser interaction. ALL OSF resources must be public. |

**If any HARD gate fails:** BLOCK research launch. Fix the gap and re-run.

---

## Cross-Skill Integration Checklist

| Skill | Load at Phase | Purpose |
|---|---|---|
| `git-github` | **0** (init), every closeout | Branch discipline, conventional commits, repo creation |
| `knowledge` | **0** (KG seed), **1** (DD), every closeout | KG queries, D1 cross-reference, project state logging |
| `cloudflare` | **6** (deployment) | R2 archive, D1 insert, Worker verification |
| `research` | **All phases** | This skill -- the master pipeline |
| `memory-management` | **0**, every closeout | Durable memory logging |
| `documents` / `pdf` | **5** (publication) | PDF building, document formatting |
| `system` | **0** (if Desktop automation needed) | App configuration |
| `git-github` (OSF addendum) | **2-5** (qualifying projects only) | OSF project creation, components, registration drafts, external file links |

---

## Phase Closeout Protocol (MANDATORY -- every phase, for net-new projects with a dedicated repo)

**STEP 0 (HARD GATE, run FIRST, every single time -- no exceptions):**
```
git remote -v
```
Confirm the remote URL is the PROJECT's own repo (`QNFO/<project-name>` or
`QNFO/qnfo-research`). If it shows `QNFO/qnfo-skills` -- STOP. Do not commit,
tag, or create a release. `cd` to the correct project directory first. This
single check prevents the exact failure mode documented in ADR-026 Incident 3
(research phase tags `v0.1-phase0`, `v1.0.0`, etc. and a Zenodo-DOI GitHub
Release were mistakenly created inside `qnfo-skills`, requiring a full
backup+delete remediation).

**STEP 0.5 (HARD GATE, kaizen fix A4/C1/D2 -- credential pre-commit scan):**
```bash
python <research-skill-path>/scripts/credential-scan.py --staged
```
Run this AFTER `git add` and BEFORE `git commit`. If it exits non-zero,
BLOCK the commit, remove the hardcoded secret (move to env var or a
`~/.{service}_token` file), re-stage, and re-scan. GitHub push protection
will otherwise reject the push after the fact -- catching it pre-commit
avoids a rewritten-history remediation.

```
1. COMMIT:  git add <phase-artifacts> ; python <research-skill-path>/scripts/credential-scan.py --staged ; git commit -m "ACTION:CREATE FILE: <files> RATIONALE: Phase N complete"
2. TAG:     git tag v<major>.<minor>-<phase-slug> -m "Phase N: <description>"
3. PUSH:    git push origin <feature-branch> --tags
4. VERIFY:  git log -1 --oneline && git branch --show-current && git status --short
5. LOG:     memory_remember(content="Phase N completed. Deliverables: <list>.")
6. TAG-BACKFILL-CHECK (kaizen fix D1): git tag -l 'v*'  # confirm ALL prior
   phase tags exist -- a missing tag from an earlier phase (e.g. Phase 0's
   v0.1-phase0 never created) should be discovered and backfilled NOW, not
   discovered later during an audit.
```
*(Windows PowerShell note -- kaizen fix B2: use `;` to chain commands, not
`&&`. `cmd /c "cmd1 && cmd2"` also works but breaks on inner quoting; prefer
`;` or separate sequential tool calls.)*

### Version Tagging Protocol

| Phase | Tag Pattern | Example |
|---|---|---|
| 0 -- Init | `v0.1-phase0` | `v0.1-phase0` |
| 1 -- Due Diligence | `v0.2-phase1-dd` | `v0.2-phase1-dd` |
| 2 -- Literature | `v0.3-phase2-lit` | `v0.3-phase2-lit` |
| 3 -- Citations | `v0.4-phase3-cite` | `v0.4-phase3-cite` |
| 4 -- Deep Research | `v0.5-phase4-deep` | `v0.5-phase4-deep` |
| 5 -- Publication | `v1.0` | `v1.0` (major version bump) |
| 6 -- Deployment | `v1.1-deploy` | `v1.1-deploy` |
| 7 -- Dissemination | `v1.2-disseminate` | `v1.2-disseminate` |
| 8 -- Core Distribution | `v1.3-distribute` | `v1.3-distribute` |

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

**Vectorize Confirmation-Bias Disclosure (kaizen fix C3, HARD when triggered):**
QNFO's Vectorize index currently contains ONLY QNFO-internal papers. If a
`search_papers` call returns results and ALL of them are QNFO-authored, this
is NOT external corroboration -- it is the corpus searching itself. Any
report claiming "confirmed by literature search" MUST distinguish:
`[QNFO-INTERNAL: N hits, self-referential]` vs `[EXTERNAL: M hits from arXiv/
Semantic Scholar/web]`. If external search step (b) was skipped or returned
zero results while internal search (a) returned nonzero, explicitly flag
`[CONFIRMATION-BIAS-RISK: only internal corpus searched]` in the due
diligence report -- do not silently present internal-only hits as validation.

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

**YAML delimiter conflict check (kaizen fix D3):** a markdown table
separator row (`|---|---|`) or a horizontal rule elsewhere in the body can
contain the bare string `---`, which some naive frontmatter parsers
misinterpret as a second frontmatter block. Before building, count `---`
occurrences on their own line at column 0:
```bash
python -c "import sys; t=open('paper.md',encoding='utf-8').read(); print(sum(1 for l in t.split(chr(10)) if l.strip()=='---'))"
```
Only the FIRST TWO such lines (opening and closing the YAML block) are valid
frontmatter delimiters. `scripts/unicode-latex-preprocess.py` already
handles this correctly (it anchors the frontmatter regex to the START of the
file with `^---\n...\n---\n`), but any custom tooling touching `paper.md`
must apply the same anchoring rule -- never a naive "split on ---".

#### Visible Author Block (MANDATORY)
**Author:** [Name] | **Date:** [YYYY-MM-DD] | **License:** QNFO-ULA: https://legal.qnfo.org/

#### Publication Language Gate (BLOCKING if any hit)
Scan for ALL of:
- **INTERNAL LANGUAGE:** "Module N", "Task N", "SPRINT", "PROCEED", "RESUME", "0.N.py", "PROJECT STATE", "ready for handoff", "new agent starting from cold" -> BLOCKING
- **INTERNAL METADATA:** Version numbers as visible headers, project identifiers, commit references -> absent from visible content
- **STYLE:** Straight quotes in body, bare Unicode math outside $...$, generation artifacts -> BLOCKING
- **CREDENTIAL LEAKS (kaizen fix D2):** `cfat_[a-zA-Z0-9_]{20,}`, `ghp_[a-zA-Z0-9]{36}`, `sk-[a-zA-Z0-9]{20,}`, `AKIA[0-9A-Z]{16}`, `Bearer [A-Za-z0-9._-]{20,}` -> BLOCKING. Run `scripts/credential-scan.py paper.md` as part of this gate, not just at git-commit time -- a token could be pasted into the paper body itself, which is a worse leak than a script file since it gets published to Zenodo/IPFS permanently.

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

**STEP 0 (MANDATORY, run BEFORE pandoc -- kaizen fix A1/A2):** XeLaTeX's
default font (Latin Modern) lacks glyphs for many Unicode Greek/math/
subscript/superscript/bra-ket characters used in physics prose outside
`$...$`, and Pandoc's `keywords:` YAML field crashes some XeLaTeX templates
with an undefined `\xmpquote` macro. Run the preprocessor first:
```bash
python scripts/unicode-latex-preprocess.py paper.md --out paper.build.md
```
This converts Unicode math characters to LaTeX math (wrapped in `$...$`,
never double-converting characters already inside math spans) and strips
the `keywords:` field. Build FROM `paper.build.md`, not the original.

```bash
pandoc paper.build.md -o paper.pdf --pdf-engine=xelatex \
  --template=default \
  --metadata date="$(date +%Y-%m-%d)" \
  --metadata link-citations=true \
  --metadata bibliography=refs.bib \
  --citeproc
```
**NEVER use reportlab or HTML fallbacks for publication-grade PDFs.**

**If the build still fails with a LaTeX error mentioning a specific missing
character or macro:** check whether the character is inside `$$...$$` and
was written directly in LaTeX already (not Unicode) -- some math symbols
(e.g. `\ket{}`, `\langle`) require the `physics` or `braket` LaTeX package;
add `--metadata header-includes="\usepackage{braket}"` if bra-ket macros are
used directly in the source rather than relying on the preprocessor's
`\langle`/`\rangle` fallback.

### R2 Archive (MANDATORY -- every publication)

Every publication's source (paper.md), rendered PDF (paper.pdf), and provenance bundle
(PROVENANCE-BUNDLE.zip) MUST be uploaded to Cloudflare R2 immediately after Zenodo publishing.

```bash
npx wrangler r2 object put qnfo-releases/releases/<YYYY>/<MM>/<slug>/paper.md --file=paper.md --remote
npx wrangler r2 object put qnfo-releases/releases/<YYYY>/<MM>/<slug>/paper.pdf --file=paper.pdf --remote
```

### DNSLink (OPTIONAL -- read-only IPFS resolution)

```bash
node ../cloudflare/scripts/dnslink-create.js <zone_id> <subdomain>.qnfo.org <ipfs_cid>
```

### PDF Rendering Verification (MANDATORY)

**Preflight (kaizen fix B4):** verify PyMuPDF is installed before relying on
it -- `pip show PyMuPDF`. If missing: `pip install PyMuPDF`.

```bash
python scripts/check-pdf.py paper.pdf
```
This checks: PDF opens without error (corrupt-file detection), zero pages
contain `\ufffd` (Unicode replacement character -- glyph miss), zero
completely empty pages, page count > 0, and prints a per-page character
count for a quick sanity skim. Exit code 0 = pass, 1 = BLOCKED.

**File-lock handling (kaizen fix B5):** if the build script needs to replace
an existing `paper.pdf` that a PDF viewer currently has open, `os.replace()`
raises `PermissionError` on Windows. Use `replace_with_retry()` from
`scripts/check-pdf.py` (retries with backoff, falls back to a timestamped
sibling file rather than silently failing) instead of calling
`os.replace()` directly in build scripts.

### OSF Project Registration (MANDATORY for qualifying projects)

**GATE:** ONLY for major research programs with significant predictions and falsifiable claims. Do NOT register exploratory projects, single papers within existing programs, or minor updates. If the project doesn't make testable, falsifiable predictions with calibration registers, skip this section.

**POLICY:** ALL OSF resources MUST be public. NEVER expect or request manual browser interaction. Registration drafts, full form completion (all ~30 schema fields), subject taxonomy assignment, and final registration submission are ALL 100% achievable via the OSF v2 API (verified live 2026-07-20, registration `kj6ar` created via pure API calls, HTTP 201). Only file uploads specifically require Waterbutler (cookie-based sessions) — for those, link to external canonical sources (Zenodo DOI, GitHub tree, IPFS gateway) instead. Do not conflate the file-upload limitation with the registration/form-completion capability — they are different OSF subsystems with different constraints. See "OSF Registration — Full API Automation Protocol" below.

**HARD GATE: LLM-Executable Research** — OSF registration is ONLY valid for research that can be fully executed by this LLM agent within ONE chat thread, with NO human subjects, NO external resources (lab equipment, personnel, institutional partnerships), and NO IRB requirement. All data must be publicly available or computable from first principles. If the research involves human participants, lab equipment, funding applications, or any resource not immediately available in the current session, do NOT create OSF registrations — link to Zenodo/GitHub instead.

**Qualifying research types:**
- Automated data analysis of publicly available datasets
- Synthesis and meta-analysis of published literature
- Mathematical/computational models and simulations
- Algorithm development and validation on benchmark datasets
- Formal verification of claims against existing evidence
- Framework validation using existing published data
- Re-analysis of open-access data with pre-registered methods

**Non-qualifying research (link to Zenodo/GitHub only):**
- Any RCT, survey, interview, or behavioral experiment with human participants
- Any research requiring physical lab equipment or facilities
- Any research requiring new data collection from human subjects
- Any research requiring IRB/ethics committee approval
- Any research requiring hiring or contracting personnel
- Any research requiring institutional partnerships or funding applications
- NUMERATA Phase 2 experiments (N=324 human subjects, N=60 child participants, IRB required)

**BONA FIDE REGISTRATION REQUIREMENTS (MANDATORY — never create incomplete stubs):**

Every OSF registration MUST:
1. **Populate ALL ~30 structured fields** — the OSF Preregistration template includes hypothesis, design plan, sampling plan, variables, analysis plan, and falsification criteria. ALL must be populated via `registration_responses` as a JSON object with values for every required question. Empty `registration_responses = {}` is a STUB — NEVER submit a stub. Never submit what you cannot fully populate.
2. **Require explicit user approval** — use `deepchat_question` to present the complete registration text (all populated fields) and ask: "Submit this as an OSF Preregistration? This is a permanent, timestamped, immutable record. Once submitted, it cannot be edited or deleted." Only submit if user explicitly confirms.
3. **Track followup** — after submission, store the registration ID, DOI, and submission timestamp in D1/KG with status "registered." Set a reminder for the declared data collection/completion target date. This is a COMMITMENT — failing to close out is a negative reputational signal.
4. **Close out registration** — when research completes: (a) return to the OSF registration URL, (b) add a comment or results section, (c) formally complete or withdraw the registration, (d) update D1/KG status to "completed" or "withdrawn." A registration that is submitted and never closed out is an abandoned commitment — a detectable pattern of abandoned registrations on an OSF account undermines credibility.

**Registration Closeout Protocol:**
```python
# 1. Verify the registered research is complete (all analysis run, paper published with Zenodo DOI)
# 2. Navigate to OSF registration URL and add results/outcome comment
# 3. Update D1: UPDATE papers SET registration_status = 'completed', completed_at = datetime('now') WHERE registration_id = '{id}'
# 4. Update KG: json_set(properties, '$.registration_status', 'completed', '$.completed_at', '{date}')
# 5. Log to durable memory: "OSF registration {reg_id} closed out {date}. Results: {zenodo_doi}."
# 6. If research was NOT completed, mark as "withdrawn" with a brief explanation. Never abandon.
```

**STUB AUDIT PROTOCOL:** Periodically audit all draft registrations via `GET /v2/users/me/draft_registrations/`. If `registration_responses` is empty `{}` (no form content) AND the research does not qualify under the LLM-Executable Research Gate, DELETE the draft immediately. Empty stubs are a reputational risk. If `registration_responses` is PARTIALLY filled but the research will not be completed, DELETE. Only retain drafts that (a) pass the LLM-Executable Research Gate AND (b) have fully populated `registration_responses` AND (c) will be completed within the declared timeframe.

#### OSF Workflow (API-only, fully automated)

```python
# 1. Authenticate
TOKEN = "<OSF_PERSONAL_ACCESS_TOKEN>"  # Stored in .osf_token, OSF_TOKEN env var, keys.json, Windows CM
HEADERS = {"Authorization": "Bearer " + TOKEN, "Content-Type": "application/vnd.api+json"}

# 2. Create project (ALWAYS public)
POST https://api.osf.io/v2/nodes/
Body: {"data": {"type": "nodes", "attributes": {"title": "...", "category": "project", "public": true, "description": "..."}}}

# 3. Create components (one per experiment/task)
POST https://api.osf.io/v2/nodes/{project_id}/children/
Body: {"data": {"type": "nodes", "attributes": {"title": "Experiment N...", "category": "data", "public": true, "description": "📦 Canonical files: [Zenodo DOI] | [GitHub tree URL] | [IPFS gateway]"}}}

# 4. Add external links to descriptions (REQUIRED — replaces file uploads)
PATCH https://api.osf.io/v2/nodes/{node_id}/
Body: {"data": {"type": "nodes", "id": "{node_id}", "attributes": {"description": "..." + String.fromCodePoint(0x1F4E6) + " Files: " + zenodo_doi + " | " + github_tree_url + " | " + ipfs_gateway}}}

# 5. Create draft registrations (one per experiment)
GET https://api.osf.io/v2/schemas/registrations/  # Find schema ID for "OSF Preregistration"
POST https://api.osf.io/v2/nodes/{component_id}/draft_registrations/
Body: {"data": {"type": "draft_registrations", "attributes": {}, "relationships": {"branched_from": {"data": {"type": "nodes", "id": "{cid}"}}, "registration_schema": {"data": {"type": "schemas", "id": "697b72f611a8e98484c6139b"}}}}}

# 6. Document all IDs, URLs, and registration draft links in project README/PROJECT-PLAN.md
# 7. Verify: all nodes public, all descriptions contain external links, registration drafts created
```

#### OSF File Upload — NOT SUPPORTED via API

**Waterbutler requires cookie-based browser sessions.** Do NOT attempt file upload via API — it will fail. Do NOT request manual browser interaction. Instead:

- Link to Zenodo DOI (canonical published version with all files)
- Link to GitHub tree URL (source code, analysis scripts, protocols)
- Link to IPFS gateway (permanent content-addressed copy)

The OSF project becomes a **discovery hub** pointing to canonical storage, not a file host.

#### OSF Registration — Full API Automation Protocol (CORRECTED 2026-07-20)

**Prior guidance in this section was WRONG and has been retracted.** The entire registration workflow — schema discovery, field population, subject taxonomy, final submission — is achievable via API with ZERO browser interaction. Verified live: registration `kj6ar` created 2026-07-20T12:48:47Z via pure API calls, HTTP 201.

**Step 1 — Discover real schema keys (NEVER assume `q1`/`q2` format):**
```python
r = requests.get(f'https://api.osf.io/v2/schemas/registrations/{SCHEMA_ID}/schema_blocks/?page[size]=100', headers=H)
# Real keys look like '344-2', '344-47', etc. Walk blocks tracking the preceding
# question-label to build a {key: label} map. Only required=True keys are mandatory.
```

**Step 2 — For select-type fields, get EXACT verbatim option text:**
```python
# API rejects any option text that doesn't match the schema's display_text VERBATIM.
# Walk schema_blocks from the select-input key forward, collecting select-input-option
# blocks until the next non-option block type.
```

**Step 3 — Populate ALL fields in one PATCH:**
```python
patch = {'data': {'id': draft_id, 'type': 'draft_registrations',
                   'attributes': {'registration_responses': responses}}}
r = requests.patch(f'https://api.osf.io/v2/draft_registrations/{draft_id}/', headers=H, json=patch)
# 200 = success. 400 "must be one of the provided options" = re-check Step 2 exact text.
```

**Step 4 — MANDATORY subject taxonomy (registration 400s without this):**
```python
# Subjects require a root->leaf chain, set on the DRAFT (flat list), not the node
# (which uses list-of-lists). These are SEPARATE relationships.
chain = []  # build via GET /v2/subjects/{id}/ walking .relationships.parent.data.id to null
patch = {'data': {'id': draft_id, 'type': 'draft_registrations', 'attributes': {'subjects': chain}}}
requests.patch(f'https://api.osf.io/v2/draft_registrations/{draft_id}/', headers=H, json=patch)
```

**Step 5 — Submit:**
```python
reg_data = {'data': {'type': 'registrations', 'attributes': {
    'draft_registration': draft_id, 'registration_choice': 'immediate'}}}
r = requests.post(f'https://api.osf.io/v2/nodes/{NODE_ID}/registrations/', headers=H, json=reg_data)
# HTTP 201 = SUCCESS, fully immutable, date_registered timestamp set.
```

**Understanding `pending_registration_approval: true` after success:** This is NOT a manual-review queue — OSF confirmed via API error "OSF Registries is an unmoderated provider." It is OSF's mandatory email-confirmation anti-hijacking gate (like 2FA), applied uniformly to ALL registrations regardless of creation method, resolved only by the account holder clicking the emailed confirmation link. Report this precisely: "Registration submitted (HTTP 201, ID `{id}`). Pending only the account holder's email confirmation — OSF's standard anti-hijacking safeguard, not a data-entry step."

**Never again claim** "requires browser interaction" for registration/form completion. That was false. Only file uploads (Waterbutler) have this limitation.

#### OSF Cleanup

```python
# Delete a node (components, test projects, etc.)
DELETE https://api.osf.io/v2/nodes/{node_id}/

# List all nodes (check for orphans)
GET https://api.osf.io/v2/users/me/nodes/
```

### Zenodo Credential Protocol (MANDATORY — read before ANY Zenodo API call)

**Incident record (2026-07-20/21):** A session spent an entire multi-hour
block diagnosing repeated `{"status":403,"message":"Permission denied."}`
errors as "the token has read-only scope" / "the token is dead" across
~15 different curl/PowerShell/Python attempts, tried sandbox endpoints,
query-param auth, multipart uploads, and different Content-Type headers —
none of which was the actual problem. The real root cause: the token had
been read from a **truncated terminal display** (`Get-ChildItem env:`
showing `ZENODO_TOKEN = BkLOVH2EDBcc...` with only the prefix visible) and
then **manually retyped/reconstructed** by guessing the suffix from a
separate truncated output, producing a 59-character string that was
subtly wrong versus the real 60-character token. Zenodo returns the exact
same generic 403 for "wrong token" as for "right token, wrong scope" —
the two failure modes are **indistinguishable by symptom alone**.

**THE RULE:** Never hardcode, retype, or reconstruct a Zenodo (or any)
API token from a truncated/partial display. Always reference the live
environment variable directly in code:

```python
import os
TOKEN = os.environ.get('ZENODO_TOKEN')   # Python — correct
```
```powershell
$env:ZENODO_TOKEN                         # PowerShell — correct, pass through directly
```

**NEVER do this:**
```python
TOKEN = 'BkLOVH2EDBccmqRMEYz0vJrmbph0Bb9wDqy19RHyxMpJE0eZKZMJoqjw72g'  # WRONG — hand-copied from truncated output
```

If a token must be inspected for debugging, print ONLY its length
(`len(token)`) and confirm that length matches expectations — never print
the full value (credential-leak risk per `qnfo-agent` §Publication
Language Gate) and never re-derive the value from a partial print.

**Diagnostic script (run FIRST on any Zenodo 403):**
```bash
python <research-skill-path>/scripts/zenodo-token-check.py
```
This tests read (`GET /deposit/depositions`), write (`POST` a probe
deposit), and metadata-write (`PUT` on that probe), then cleans up the
probe deposit. It distinguishes "token has no write scope — generate a
new one with `deposit:write` + `deposit:actions` scopes" from "token
works fine, the problem is elsewhere in this call" — collapsing what was
previously ~15 exploratory tool calls into one.

**Required token scopes** (generate at
https://zenodo.org/account/settings/applications/):

| Scope | Purpose |
|---|---|
| `deposit:write` | Allow upload (but not publishing) |
| `deposit:actions` | Allow publishing of uploads |
| `user:email` | Allow access to email address (read-only) |

**Publish pipeline scripts** (replace ad hoc inline `python -c` snippets
or hand-written one-off scripts — see kaizen fix B1 on why inline
multi-line Python via `-c` is itself an anti-pattern on Windows):
```bash
python <research-skill-path>/scripts/zenodo-create-upload.py <bundle.zip> [--newversion <deposit_id>]
python <research-skill-path>/scripts/zenodo-metadata-publish.py --metadata-file <metadata.json> [--dry-run]
```
`zenodo-create-upload.py` handles both "brand-new deposit" and
"new version of an existing concept" (via `--newversion`, using the same
GET-verify-before-`actions/newversion` pattern as the C2 version-chain fix
below). `zenodo-metadata-publish.py` sets metadata, publishes, and
verifies the DOI resolves live via `doi.org` + `zenodo.org/api/records`
before declaring success — never trust the tool's immediate return value
alone (see the "General principle" memory: verify server-side state
independently for every remote publish action).

**Metadata gotcha:** Zenodo's REST API requires an `upload_type` (or
`resource_type`) field in metadata — omitting it produces
`HTTP 400 {"errors":[{"field":"metadata.resource_type","messages":["Missing data for required field."]}]}`
on the `actions/publish` call specifically (metadata PUT itself succeeds
with 200, making this easy to miss until the publish step). Common
values: `publication`, `dataset`, `software`, `poster`, `presentation`.

---

### Zenodo Upload (with retry + versioning)

**HARD GATE (kaizen fix A3):** `PROVENANCE-BUNDLE.zip` MUST be built and
verified BEFORE any Zenodo upload begins -- not added ad hoc during the
upload step. The bundle MUST contain: `paper.md`, `paper.pdf`,
`PROJECT-PLAN.md`, `README.md`, all `artifacts/*.md`, all `docs/*.md`.
Verify before upload:
```bash
python -c "import zipfile,sys; z=zipfile.ZipFile('PROVENANCE-BUNDLE.zip'); names=z.namelist(); required=['paper.md','paper.pdf']; missing=[r for r in required if not any(r in n for n in names)]; print('Bundle contents:', names); sys.exit(1 if missing else 0)"
```
If this check is not run and passed, the Zenodo deposit is INCOMPLETE even
if `actions/publish` succeeds -- missing provenance is a silent failure, not
a hard error, so it must be caught here.

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
**GATE:** Do not proceed to Step 3 until all 4 files are confirmed present in
the deposit's file list (`GET /api/deposit/depositions/{id}/files`).

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
**Auto-discover related QNFO papers (kaizen fix D4):** before hand-writing
`related_identifiers`, query the KG for prior QNFO publications on the same
topic/program so cross-references aren't missed:
```
query_graph({endpoint: "query", params: {query: "MATCH (p:Paper)-[:BELONGS_TO]->(d) WHERE d.name CONTAINS '<domain>' RETURN p.title, p.doi"}})
```
Add a `{"relation": "cites", "identifier": "<doi>"}` entry for each relevant
result found this way, in addition to any DOIs the author already knows to cite.

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

#### Version Chain Tracking (kaizen fix C2 -- `.zenodo_versions.json`)
Zenodo's concept-DOI/version-DOI split is easy to get wrong: calling
`actions/newversion` on a STALE deposit ID (not the latest version) returns
HTTP 403. Maintain a tracking file at the project root:
```json
{
  "concept_doi": "10.5281/zenodo.XXXXXXX",
  "latest_deposit_id": "YYYYYYY",
  "versions": [
    {"doi": "10.5281/zenodo.XXXXXXX", "deposit_id": "YYYYYYY", "tag": "v1.0", "published_at": "2026-07-20"}
  ]
}
```
Before calling `actions/newversion`, ALWAYS verify with a GET first:
```bash
curl -s -H "Authorization: Bearer $ZENODO_TOKEN" https://zenodo.org/api/deposit/depositions/<latest_deposit_id>
```
If the GET fails or the record's `state` shows it is not the latest, look up
the current latest via the concept DOI's `GET /api/records/?q=conceptdoi:"<concept_doi>"`
before proceeding. Update `.zenodo_versions.json` immediately after every
successful publish -- this file is the single source of truth for "what is
the latest deposit ID", preventing the fragmented-citation-record failure
mode where a disconnected new deposit gets created because the correct ID
was lost or misremembered.

#### Zenodo Versioning for Phase/Session Conclusions (MANDATORY -- see qnfo-agent §8.5 JIT Thin-Client Protocol, Phase-End and Session/Project-Conclusion Checkpoint subsections)

At every session or phase conclusion for a project with an existing Zenodo
deposit, create a NEW VERSION rather than a disconnected upload:
```python
# 1. Create a new version draft of the existing concept
POST https://zenodo.org/api/deposit/depositions/{existing_id}/actions/newversion
# Response includes a "latest_draft" link -> extract new draft deposit ID

# 2. Upload the updated files to the NEW draft (remove stale files first if replacing)
DELETE https://zenodo.org/api/deposit/depositions/{new_id}/files/{stale_file_id}
PUT https://zenodo.org/api/deposit/depositions/{new_id}/files

# 3. Update metadata (bump version string, e.g. "1.0" -> "1.1")
PUT https://zenodo.org/api/deposit/depositions/{new_id}
Body: {"metadata": {"version": "1.1", ...}}

# 4. Publish the new version
POST https://zenodo.org/api/deposit/depositions/{new_id}/actions/publish
```
This keeps ALL phase-by-phase snapshots under one **concept DOI** (stable,
never changes) with each phase getting its own **version DOI** (changes per
version). Never create a brand-new unrelated Zenodo deposit for what is
really the next phase/version of an existing project -- that fragments the
citation record and breaks `isNewVersionOf`/`isPreviousVersionOf` relations.
Only use a genuinely NEW deposit for a genuinely NEW, unrelated publication.

---

## Phase 6: Cloudflare Deployment

### D1 Insert (living-paper)
```sql
INSERT INTO papers (slug, title, author, abstract, body, doi, published_at, updated_at)
VALUES ('<slug>', '<title>', '<author>', '<abstract>', '<full markdown body>', '<doi>', '<ipfs_cid>', datetime('now'), datetime('now'))
ON CONFLICT(slug) DO UPDATE SET body = excluded.body, doi = excluded.doi, updated_at = datetime('now');
```

### D1 Record Update (MANDATORY — after IPFS pinning)
```sql
-- Update D1 living-paper record after Zenodo publishing
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

1. **robots.txt** — verify at root of papers.qnfo.org: allows crawling, points to sitemap
2. **sitemap.xml** — all paper pages listed with lastmod dates
3. **llms.txt** — machine-readable paper index for AI crawlers at papers.qnfo.org/llms.txt
4. **Meta tags** — `citation_title`, `citation_author`, `citation_doi`, `citation_date`
5. **Structured data** — Schema.org `ScholarlyArticle` with `@id`, `headline`, `author`, `datePublished`, `identifier` (DOI)
6. **Open Graph** — `og:title`, `og:description`, `og:type` (article), `og:url`

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

### DNSLink (OPTIONAL v2.8 — read-only IPFS gateway resolution)

```bash
# Create DNSLink TXT record mapping publication subdomain to IPFS CID
# Cloudflare DNS: free, unlimited records. Verified via dweb.link.
node ../cloudflare/scripts/dnslink-create.js <ZONE_ID> <subdomain>.qnfo.org <CID>
# Verify: nslookup -type=TXT _dnslink.<subdomain>.qnfo.org
# Gateway: https://dweb.link/ipns/<subdomain>.qnfo.org
```

### Internet Archive (MANDATORY)

```
GET https://web.archive.org/save/https://papers.qnfo.org/papers/<slug>
```

### Publication URL Verification
```bash
curl -sI https://papers.qnfo.org/papers/<slug>/  # Must return HTTP 200
```

## Phase 8: Core Distribution Stack (MANDATORY)

### Trigger
Every publication MUST complete Phase 8 before publication status is set to "published."

### Core Distribution Stack (v2.8)

All distribution dimensions are satisfied by the core QNFO infrastructure:

| Layer | Implementation | Verification |
|:------|:--------------|:-------------|
| **GitHub** | Public repo with tags, releases, version history | `git tag -l`, `gh release view` |
| **Zenodo** | DOI with versioned deposits (concept DOI + version DOIs) | `curl -sI https://doi.org/<doi>` |
| **R2** | Canonical file archive (md, pdf, provenance bundle) | `npx wrangler r2 object get qnfo-releases/releases/<YYYY>/<MM>/<slug>/paper.md --remote --pipe` |
| **D1/KG** | Living-paper DB entry + Knowledge Graph node | `get_paper_context({slug})`, `query_graph({endpoint:"nodes"})` |

### Pipeline
```
Publication Ready (Phase 5 PDF + Phase 6 D1/R2)
    |
    |-- GitHub:  git add, git commit, git push --tags (public repo)
    |-- Zenodo:  create new version deposit, upload PDF+md+bundle, publish
    |-- R2:      npx wrangler r2 object put qnfo-releases/releases/<YYYY>/<MM>/<slug>/ --remote
    |-- D1/KG:   INSERT/UPDATE living-paper + sync Knowledge Graph
    |-- DNSLink (OPTIONAL): _dnslink.<slug>.qnfo.org -> /ipfs/<CID>
    |-- Internet Archive: submit papers.qnfo.org URL
```

### DNSLink (OPTIONAL -- convenience layer)
```bash
curl -X POST "https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/dns_records"   -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN"   -d '{"type":"TXT","name":"_dnslink.{subdomain}","content":"dnslink=/ipfs/{CID}","ttl":1}'
```

### Deployment Workflow
1. Confirm content exists (body_md in D1 or paper.md in R2)
2. Run Phase 5 (Publication: PDF, Zenodo DOI) + Phase 6 (Deploy: D1/R2)
3. Push to GitHub with version tag, create GitHub Release with DOI link
4. Upload all artifacts to R2 (canonical durable host)
5. Seed/update D1 living-paper and Knowledge Graph records
6. (OPTIONAL) Create DNSLink TXT record if an IPFS CID is available
7. Submit Internet Archive snapshot
8. Verify: papers.qnfo.org returns HTTP 200, DOI resolves, R2 content round-trips

## Verification Gates

| Gate | Check | Evidence |
|:-----|:------|:---------|
| **Due Diligence** | KG + D1 + 2+ external sources queried | Query output with counts |
| **Classification** | All papers classified as core/supporting/background/reject | Classification table |
| **Citation** | All citations trace to real papers, BibTeX verified | `_citation_audit.py` output |
| **Publication Language** | Zero internal language in paper.md | Scan output: 0 hits |
| **PDF** | PDF renders without Unicode errors | `_check_pdf.py` output |
| **DOI** | Zenodo record resolves, cross-references correct | `curl -sI https://doi.org/...` |
| **Deployment** | papers-server URL HTTP 200, D1 entry exists with slug/doi | curl output + wrangler D1 query |
| **SEO** | robots.txt, sitemap, llms.txt, meta tags all present | Verify each URL |
| **Social** | Buffer posts confirmed in queue | `status: SCHEDULED` in response |
| **DNSLink (OPTIONAL)** | TXT record resolves, dweb.link gateway serves content | `nslookup -type=TXT` + `curl dweb.link/ipns/...` |
| **Core Distribution Gate (MANDATORY)** | All core layers: GitHub (public repo), Zenodo (DOI), R2 (archive), D1/KG (discoverability) | All 4 layers verified |

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
| Single-store publishing | Core stack REQUIRED: GitHub+Zenodo+R2+D1/KG. DNSLink optional. |
| No DNSLink for publications | Every paper must have `_dnslink.{slug}.qnfo.org` TXT record |
| Publishing without D1/KG records | Log `doi`, `r2_path` in D1 living-paper + Knowledge Graph Paper node |
| Skipping 4-D verification | `_verify_4d.py` must pass before status → "published" |
| Relying on single IPFS pinner | Use ≥3 independent pinning services per publication |
| Skipping Phase 0 for a net-new long-lived project | HARD GATE -- scaffold repo, WBS, PROJECT-PLAN.md before Phase 1 |
| No pre-flight checklist before due diligence | Run P1-P11 before Phase 1 begins |
| No phase closeout (commit/tag/push/verify/log) | 5-step Phase Closeout Protocol at every phase end |
| No risk register at project init | ≥5 risks logged at Phase 0 using the risk register template |
| No deliverable registry | All deliverables tracked with paths and archival targets from Phase 0 |
| Creating a research phase tag/release inside `qnfo-skills` | `git remote -v` REPO-TARGET GATE before every tag/commit/release (ADR-026 Incident 3) |
| Assuming a "clean branch" audit is sufficient | Tags and GitHub Releases are independent refs -- audit `git tag -l` and `gh release list` separately, they survive a branch force-push |
| Project files existing ONLY on local disk across a turn boundary | R2-Immediate-Write mandate (ADR-028) -- upload every project artifact to R2 in the SAME turn it's created/edited, never deferred to closeout |
| Creating a disconnected new Zenodo deposit for each phase | Use Zenodo's `actions/newversion` API to keep phase snapshots under one concept DOI (ADR-028) |
| Social-promoting every internal WBS phase transition | Reserve Buffer/social posts for FINAL public deliverables only, not interim phase closeouts |
| OSF registration for minor/exploratory projects | GATE-CONDITIONAL: OSF ONLY for major research with significant predictions and falsifiable claims. Skip for single papers, exploratory studies, or minor updates. |
| Waiting until after publication to create OSF project | Create OSF project during Phase 2 (experimental design) or Phase 4 (deep research) — not after. The registrations timestamp the pre-data-collection hypotheses. |
| Attempting OSF file upload via API | Waterbutler requires cookie sessions — Bearer tokens cannot upload. Use external links to Zenodo DOI + GitHub tree + IPFS instead. (Registration/form completion has NO such limitation — that is 100% API-automatable; only file uploads need Waterbutler.) |
| Claiming OSF registration form completion "requires browser interaction" | FALSE — corrected 2026-07-20. Discover real schema keys via `/schema_blocks/` (format `344-N`, not `q1`/`q2`), populate via PATCH, set subject taxonomy chain, submit via POST — all API, HTTP 201 confirmed live (registration `kj6ar`). |
| OSF tokens in only one location | Store OSF tokens redundantly: %USERPROFILE%\\.osf_token, OSF_TOKEN env var, keys.json, Windows Credential Manager, GitHub secrets. Follow the pattern used by Cloudflare/Zenodo/Buffer tokens. |
| OSF nodes set to private | ALL OSF nodes MUST be public by default. Verify with `GET /v2/nodes/{id}/` → `attributes.public === true`. |
| Not documenting OSF ID mappings | Maintain a mapping of project/component/draft IDs in PROJECT-PLAN.md. These IDs are needed for API updates and cross-referencing. |
| OSF descriptions without external links | Every node description MUST contain links to the canonical file locations (Zenodo DOI, GitHub tree, IPFS). OSF is the discovery hub, not the file host. |
| Creating OSF project without Zenodo DOI backlink | Every OSF project description MUST include the Zenodo DOI. This is the primary discoverability bridge between platforms.
| Submitting OSF registration with empty registration_responses | **HARD GATE:** Empty registration_responses is a STUB. NEVER submit. All ~30 template fields must be populated. |
| Submitting OSF registration without explicit user approval | Use deepchat_question to present the full registration content before submission. OSF registrations are permanent and immutable. |
| Creating OSF registrations then never closing them out | Every submitted registration must eventually be completed or withdrawn. Abandoned registrations are visible on the account and undermine credibility. Run periodic closeout audits. |
| Creating OSF registrations for non-executable research | LLM-Executable Research Gate: no human subjects, no external resources, no IRB. If the protocol cannot be executed in this chat thread, link to Zenodo/GitHub only. |
| Leaving draft registrations with partial registration_responses | If the research will not be completed and submitted, DELETE the draft. Partial stubs are a reputational risk. |
| Not storing OSF registration tracking in D1/KG | Store registration_id, doi, status, and dates in D1 + KG for lifecycle tracking and closeout audit. |
| Submitting OSF registration with empty registration_responses | **HARD GATE:** `registration_responses = {}` is a STUB. NEVER submit. All ~30 template fields must be populated. |
| Submitting OSF registration without explicit user approval | Use `deepchat_question` to present the full registration content before submission. OSF registrations are permanent and immutable. |
| Creating OSF registrations then never closing them out | Every submitted registration must eventually be completed or withdrawn. Abandoned registrations are visible on the account and undermine credibility. Run periodic closeout audits. |
| Creating OSF registrations for non-executable research | LLM-Executable Research Gate: no human subjects, no external resources, no IRB. If the protocol cannot be executed in this chat thread, link to Zenodo/GitHub only. |
| Leaving draft registrations with partial registration_responses | If the research will not be completed and submitted, DELETE the draft. Partial stubs are a reputational risk. |
| Not storing OSF registration tracking in D1/KG | Store registration_id, doi, status, and dates in D1 + KG for lifecycle tracking and closeout audit. |
| `python -c "..."` inline scripts on Windows (kaizen fix B1) | Nested double-quotes in f-strings collide with `python -c "..."` outer quotes; Windows escaping of `\n`, dict literals, and Unicode breaks silently. `write` the script to a `_*.py` file first, `exec` it, then delete -- never inline for anything beyond a one-liner with zero quotes/dicts/regex. |
| `curl` on Windows PowerShell (kaizen fix B3) | PowerShell aliases `curl` to `Invoke-WebRequest`, which has different flags (`-s` is not recognized) and fails. Use `python -c 'import urllib.request; ...'` (single-line, no nested quotes) or invoke `curl.exe` explicitly (the real binary, bypassing the alias). |
| Unicode math left unconverted for XeLaTeX (kaizen fix A1) | Run `scripts/unicode-latex-preprocess.py` before every Pandoc+XeLaTeX build -- see PDF Building section above. |
| `keywords:` YAML field in Pandoc frontmatter (kaizen fix A2) | Strip it -- `scripts/unicode-latex-preprocess.py` does this automatically. It crashes some XeLaTeX templates via an undefined `\xmpquote` macro. |
| Ephemeral scripts with hardcoded API tokens reaching `git add` (kaizen fix A4) | Run `scripts/credential-scan.py --staged` before every commit (Phase Closeout Protocol STEP 0.5). Add `_*.py`/`.env`/`*.token` to `.gitignore` from Phase 0. |
| Obsidian/external-drive source notes assumed inaccessible or silently skipped (kaizen fix C5/D5) | Document the path limitation and ask the user to copy files in, or use `exec` with explicit `cwd` in Full Access mode. If imported notes mix internal monologue with delivered content and lack YAML frontmatter, load `doc-coauthoring` to help the user separate meta-planning from publishable content before it enters the research pipeline. |



