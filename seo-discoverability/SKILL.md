---
name: seo-discoverability
description: Automated SEO and AI crawler discoverability optimization for Cloudflare Pages sites. Audits robots.txt, sitemaps, meta tags, structured data, llms.txt, and topic taxonomies. Use when deploying new publications, auditing discoverability, or improving organic + AI traffic.
version: 1.0
---
> **INCLUDES AUTONOMOUS RED-TEAM SELF-AUDIT.** See RED-TEAM-PROTOCOL.md.


# SEO DISCOVERABILITY SKILL — v1.0

> **On-demand skill.** Load via `skill_view('seo-discoverability')` for automated SEO and AI crawler optimization of QNFO/QWAV Cloudflare Pages sites.

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
python -c "import urllib.request; r = urllib.request.urlopen('https://<domain>/llms.txt'); print(r.status)"
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

*seo-discoverability v1.1 — Automated SEO + AI crawler optimization for QNFO/QWAV*

## RT: RED-TEAM SELF-AUDIT

Before claiming this skill complete, autonomously run:

1. Output Verification (negative verification)
2. Assumption Challenge (state and test every assumption)
3. Edge Case Check (empty/null/max/boundary/desync)
4. DoD Integration (run _dod_enforce.py if exists)
5. Iteration (retry on failure, max 3)

ANTI-PATTERN: User should NEVER ask about quality.
Refer to RED-TEAM-PROTOCOL.md for full protocol.

