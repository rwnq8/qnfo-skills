---
name: seo-discoverability
description: Automated SEO and AI crawler discoverability optimization for Cloudflare Pages sites. Audits robots.txt, sitemaps, meta tags, structured data, llms.txt, and topic taxonomies. Use when deploying new publications, auditing discoverability, or improving organic + AI traffic.
version: "1.1"
---

> **INCLUDES AUTONOMOUS RED-TEAM SELF-AUDIT.** Before claiming this skill complete, autonomously run: (1) Output Verification -- negative verification. (2) Assumption Challenge -- state and test every assumption. (3) Edge Case Check -- empty/null/max/boundary/desync. (4) DoD Integration -- run _dod_enforce.py if exists. (5) Iteration -- retry on failure, max 3. ANTI-PATTERN: User should NEVER ask about quality.

### Programmatic Loading & Execution
This skill is loaded and executed **programmatically by the LLM system** 
during response generation. Loading is triggered automatically via 
`skill_view('seo-discoverability')` or `read()` with filesystem path.
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

---

## Autonomous Continuation Protocol (v1.0)

**All audit stages execute autonomously.** Agent MUST: (1) chain robots→sitemap→meta→llms→taxonomy without user prompts, (2) tag `[AUTO-CONTINUE]` between stages. **ANTI-PATTERN:** User NEVER says "CONTINUE."

---

## execute_plan (MANDATORY -- Before Any Execution)

**This skill involves execution-heavy workflows.** Before executing, use update_plan to populate a concrete, verifiable checklist. Every item must be short, specific, and testable with tool evidence.

### Execution Protocol

1. **Populate update_plan** with workflow phases as concrete checklist items
2. **Execute one item at a time** -- at most ONE in_progress
3. **Mark items completed ONLY with tool evidence** (Test-Path, exec output, git log)
4. **Never claim completion without execution evidence** -- Rule 14 enforcement
5. **If blocked:** Flag as [BLOCKED: reason] and move to the next item

### Example Plan

update_plan([
  {"step": "Audit robots.txt presence and correctness", "status": "pending"},
  {"step": "Audit sitemap.xml presence and completeness", "status": "pending"},
  {"step": "Audit meta tags, structured data, llms.txt", "status": "pending"},
  {"step": "Generate missing SEO artifacts", "status": "pending"},
  {"step": "Deploy SEO artifacts to Cloudflare Pages", "status": "pending"}
])


# SEO DISCOVERABILITY SKILL — v1.0

> **On-demand skill.** Load via `skill_view('seo-discoverability')` for automated SEO and AI crawler optimization of QNFO/QWAV Cloudflare Pages sites.

---
---

## Purpose

Ensures all QNFO/QWAV sites are maximally discoverable by both traditional search engines (Google, Bing) and AI crawlers (ChatGPT, Claude, Perplexity, Google AI). Automates the full SEO injection pipeline from audit through deployment.

## When to Use

| Trigger | Action |
|:--------|:-------|
| New publication deployed | Run full SEO injection for that site |
| "Check SEO" / "Audit SEO" | Run comprehensive audit |
| "Improve discoverability" | Run Phase 1 + Phase 2 pipeline |
| "Update SEO for all sites" | Full rebuild + redeploy |
| Session startup | Quick health check |

## Architecture

Two Python toolkits provide the core functionality:

| Script | R2 Path | Purpose |
|:-------|:--------|:--------|
| `seo_toolkit.py` | `qnfo/tools/seo_toolkit.py` | Phase 1: robots.txt, sitemap.xml, meta tags, OG, Twitter, JSON-LD, canonical |
| `seo_phase2.py` | `qnfo/tools/seo_phase2.py` | Phase 2: llms.txt, llms-full.txt, ai.txt, topic taxonomy, enhanced structured data |

## Quick Reference

### Phase 1 — Traditional SEO
```bash
# Build SEO artifacts for all sites
python seo_toolkit.py --build

# Build + deploy Tier 1 only (hub sites)
python seo_toolkit.py --tier=1 --deploy

# Build + deploy single site
python seo_toolkit.py --site=quantum-laws-of-form --deploy
```

### Phase 2 — AI Crawler Discoverability
```bash
# Build AI crawler layer for all sites
python seo_phase2.py --build

# Deploy everything
python seo_phase2.py --deploy

# Generate only master taxonomy + master llms.txt
python seo_phase2.py --master-only
```

### Verification
```bash
python final_phase2_verify.py  # Comprehensive audit of all 33 sites
```

## What Gets Generated Per Site

| File | Content-Type | Purpose |
|:-----|:-------------|:--------|
| `robots.txt` | text/plain | Crawler permissions, AI bot allowlisting, sitemap ref |
| `sitemap.xml` | application/xml | URL discovery for all search engines |
| `llms.txt` | text/plain | AI crawler content manifest (llmstxt.org standard) |
| `llms-full.txt` | text/plain | Full content extract optimized for LLM ingestion |
| `ai.txt` | text/plain | AI agent permissions manifest |
| `_headers` | N/A | Content-Type rules, X-Robots-Tag, security headers |
| `topic-taxonomy.md` | text/markdown | 12-domain cross-discipline taxonomy (hub only) |
| `index.html` | text/html | Injected with: OG, Twitter, JSON-LD, canonical, keywords, AI topic hints |

## Topic Taxonomy

A 12-domain interconnected taxonomy bridges all QNFO/QWAV content:
quantum-computing → p-adic-mathematics → mathematics → physics → cosmology → philosophy → self-help → spirituality → cognition → computer-science → number-theory → research-methodology

Each site is mapped to its primary topics, and AI crawlers receive cross-discipline bridge information via llms.txt and enhanced JSON-LD.

## Custom Domain Propagation

After deployment, Cloudflare Pages custom domains may take 5-15 minutes to propagate. The `.pages.dev` deployment URL updates immediately. Verify with:
```bash
# Check llms.txt exists and returns 200 — write check script, execute, discard
echo "import urllib.request; r = urllib.request.urlopen('https://<domain>/llms.txt'); print(r.status)" > _check_llms.py
python _check_llms.py
Remove-Item _check_llms.py
```

## ✅ Fix Deployed: SEO Metadata Injector Worker (2026-06-21)

**Status:** ALL 16 affected sites now at 7/7 + robots ✅

The fix was deployed via Option C — a Cloudflare Worker (`seo-metadata-injector`) that injects OG, Twitter, JSON-LD, canonical, meta description, keywords, ai-topics, and robots tags into HTML responses.

### Worker Details
- **Worker name:** `seo-metadata-injector`
- **Routes:**
  - `papers.qnfo.org/papers/*` — 15 publication sub-pages
  - `primer.qwav.tech/*` — standalone qlof-primer site
- **Worker code:** R2 `qnfo/tools/seo-injector-worker.js`

### Sites Fixed (all now 7/7 + robots)
solo.qnfo.org, paradigm.qnfo.org, quantum.qnfo.org, hierarchy.qnfo.org, unity.qnfo.org, different.qnfo.org, measure.qnfo.org, knowing.qnfo.org, adelic.qnfo.org, cocyle.qnfo.org, lexicon.qnfo.org, ai-poc.qnfo.org, archive.qnfo.org, primer.qwav.tech, laws.qnfo.org, living-paper.qnfo.org

### Additional fix
- **archive.qnfo.org:** DNS was CNAME→qnfo.org (wrong), fixed to CNAME→qnfo-archive.pages.dev + custom domain reactivated

### Note
`final_phase2_verify.py` does NOT follow redirects. For redirect-only sites, verify by fetching the custom domain directly (Python follows redirects by default, unlike the script).

### Fallback (if Worker needs redeployment)
```bash
# Pull worker code from R2
npx wrangler r2 object get qnfo/tools/seo-injector-worker.js --remote --file=worker.js
# Deploy
npx wrangler deploy --name seo-metadata-injector
```

## Build Output

All build artifacts are stored at: `%TEMP%\qnfo-seo-build\<project-name>\`

---

*seo-discoverability v1.0 — Automated SEO + AI crawler optimization for QNFO/QWAV*

> **Version:** (Kaizen-audited 2026-07-08)
## Handoff Protocol (MANDATORY at Closeout)

1. **Verify** ALL execute_plan items marked [EXECUTED] with tool evidence (Test-Path, exec output, git log)
2. **Archive** session artifacts to R2 canonical storage: `npx wrangler r2 object put qnfo/audit/... --remote --file=<artifact>`
3. **Generate** continuation prompt documenting pending work and current state for the next session
4. **Clean up** ephemeral _* files and __pycache__ directories: `Remove-Item _* -Recurse -Force`

### Continuation Prompt Template
```
TASK: [description of pending work from execute_plan]
STATE: [current state — what's executed, what's blocked, why]
NEXT: [first executable action for the next session]
R2: [canonical path for session artifacts]
```


## Closeout Protocol (MANDATORY)

Before declaring this skill workflow complete:
1. **Task Execution Verification:** Compare planned tasks ([PENDING] in execute_plan) vs executed tasks ([EXECUTED] with evidence)
2. **Filesystem Verification:** `Test-Path <file>` for every file claimed as created/modified. Never claim from memory.
3. **Git Verification:** `git log -1 --oneline` for every commit claimed. Verify commit hash exists.
4. **R2 State Upload:** Upload session audit trail to `qnfo/audit/` — conversations, decisions, state files.
5. **Discovery Index Update:** Update `qnfo/discovery/index.json` with any new resources created, projects modified, or publications generated.
6. **Ephemeral Cleanup:** Delete ALL _* prefixed files and __pycache__ directories. Session is not complete until `Get-ChildItem -File -Name | Where-Object { $_ -match '^_' }` returns zero results.
