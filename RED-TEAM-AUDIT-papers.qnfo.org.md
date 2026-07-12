# RED-TEAM AUDIT: papers.qnfo.org — Full-Text Paper Pipeline
## QNFO Infrastructure Audit · 2026-07-12 · Severity: **CRITICAL**

---

## Executive Summary

**papers.qnfo.org is BROKEN.** The intent was to provide access to 616 full-text research papers indexed in D1 with DOIs linking to Zenodo. Instead, users see either:

1. **Broken query links from qnfo.org** — `/papers.qnfo.org/?category=quantum-error-correction` returns a STATIC page with ZERO paper cards
2. **A static landing page** — the `qnfo-publications.pages.dev` static site is served instead of the dynamic `papers-server` Worker
3. **404s for 8/9 paper slugs** — only `quantum-laws-of-form` returns 200, and it's a STUB with no full-text
4. **503s for sitemap.xml and llms.txt** — SEO is dead
5. **DOIs are NOT hyperlinked** — displayed as plain badge text, users cannot navigate to Zenodo

**616 papers exist in D1 with complete metadata** (title, DOI, abstract, date). **Zero full-text paper.md files exist on R2.** The entire pipeline from Zenodo deposition → R2 archival → dynamic rendering is disconnected.

---

## Root Cause Analysis

### CRITICAL-1: Edge-Router Misdirects papers.qnfo.org to Static Pages

```javascript
// qnfo-edge-router — BROKEN LINE:
if (host === "papers.qnfo.org" || path.startsWith("/papers/")) {
  return fetch(`https://qnfo-publications.pages.dev${path}${url.search}`, request);
}
```

The edge-router proxies papers.qnfo.org to `qnfo-publications.pages.dev` — a STATIC Pages project with NO database, no paper catalog, no dynamic rendering. The static project renders a single hardcoded HTML page. **The `papers-server` Worker (which has D1 + R2 bindings) is NEVER reached.**

**Impact:** Every request to papers.qnfo.org hits a static site. D1 is never queried. 616 papers are invisible.

**Root cause:** The edge-router lacks a `PAPERS_SERVER` service binding. When it was built, the papers-server didn't exist yet, so `qnfo-publications.pages.dev` was the only thing available.

**Fix:** Either add `PAPERS_SERVER` service binding to edge-router, or set up a worker route for papers-server on `papers.qnfo.org/*`.

---

### CRITICAL-2: Zero Full-Text Markdown Files on R2

R2 inventory check (confirmed via both wrangler CLI and REST API):

```
qnfo/releases/  — ZERO paper.md files at any path
qnfo/papers/    — ZERO paper.md files at any path
```

**Every paper rendered by papers-server falls into the STUB path:**

```javascript
// papers-server v2.1 renderPaper() — STUB PATH:
${bodyHtml ? '<div class="paper-content">'+bodyHtml+'</div>'
  : '<p style="color:var(--text-muted)">Full paper content is being processed.
     DOI links to Zenodo for the complete PDF.</p>'}
```

The papers-server loops through 4 R2 paths per paper slug — all 4 are empty. All 616 papers render as "Full paper content is being processed."

**Impact:** Zero papers show full-text. The STUB message is inaccurate ("DOI links to Zenodo" — but the DOI is NOT a link).

**Root cause:** The `publication-publisher` skill uploads paper.md to R2 as Stage 6 of a 7-stage pipeline. This step was not executed for most papers. Alternatively, the papers were published to Zenodo but never uploaded to R2.

**Fix:** Implement a batch upload pipeline from Zenodo → R2 for all 616 papers. Short-term: make the STUB message useful — show a clickable DOI link to Zenodo.

---

### CRITICAL-3: DOIs Are Not Hyperlinks

```javascript
// papers-server v2.1 — BROKEN DOI RENDERING:
${doi ? '<span class="badge badge-doi">DOI: '+escapeHtml(doi)+'</span>' : ""}
```

DOI is rendered as a `<span>` — NOT an `<a>` tag. Users see a blue badge with "DOI: 10.5281/zenodo.12345678" but **cannot click it.**

**Impact:** The STUB message says "DOI links to Zenodo for the complete PDF" — but the DOI is not a link. The UX is deceptive.

**Fix:** Replace `<span class="badge badge-doi">DOI: ...</span>` with `<a href="https://doi.org/${doi}" class="badge badge-doi" target="_blank" rel="noopener">DOI: ${doi}</a>`

Also add a prominent "📄 Read Full Paper on Zenodo" link when full-text is unavailable.

---

### HIGH-4: SEO Endpoints Return 503

```
/sitemap.xml → 503 (tries R2 seo/sitemap.xml — doesn't exist)
/llms.txt    → 503 (tries R2 seo/llms.txt — doesn't exist)
```

Papers are invisible to search engines AND AI crawlers. The `papers-server` tries to fetch SEO files from R2, but R2 has no `seo/` prefix.

**Fix:** Generate sitemap.xml and llms.txt dynamically from D1 queries (already implemented in the OLD `papers-server-v2.js` which was overwritten by v2.1).

---

### HIGH-5: Missing Design System v3.0 Components

Per `cloudflare-deployer` Skill Design Compliance Matrix, every paper page MUST have:

| Component | Required | Current |
|:----------|:--------:|:-------:|
| AI Query box | ✅ | ❌ Missing |
| Related Papers section | ✅ | ❌ Missing |
| Sticky topbar with blur | ✅ | ✅ Present |
| Paper cards with hover | ✅ | ✅ Present |
| DOI badge (clickable) | ❌ | ❌ Broken |

**Fix:** Add AI Query textarea + "Ask QWAV" button. Add "Related Papers" section querying Knowledge Graph.

---

### HIGH-6: qnfo.org Links Expect Category Filtering

The qnfo.org homepage links to `papers.qnfo.org/?category=quantum-error-correction` and similar URLs. The papers-server has NO category filtering logic. These query parameters are silently ignored.

**Fix:** Add `?category=` and `?search=` parameter handling to the papers index route.

---

## Severity Matrix

| Finding | Severity | Users Affected | Reputation Risk |
|:--------|:--------:|:-------------:|:--------------:|
| Edge-router misdirection | **CRITICAL** | ALL | HIGH — broken for months |
| Zero full-text on R2 | **CRITICAL** | ALL | HIGH — STUB everywhere |
| DOI not hyperlinked | **CRITICAL** | ALL | MEDIUM — deceptive UX |
| SEO 503 | **HIGH** | ALL crawlers | HIGH — invisible |
| Missing AI Query | **HIGH** | ALL | MEDIUM |
| Missing Related Papers | **HIGH** | ALL | MEDIUM |
| No category filtering | **MEDIUM** | qnfo.org visitors | LOW |

---

## Strategy: Three-Phase Fix

### Phase 1: IMMEDIATE (today) — Make It Work

1. **Fix edge-router** — route papers.qnfo.org → papers-server Worker
2. **Fix DOI hyperlinks** — DOIs become clickable `https://doi.org/` links
3. **Fix SEO** — dynamic sitemap.xml + llms.txt from D1
4. **Fix STUB message** — "📄 Read Full Paper on Zenodo →" with clickable DOI
5. **Deploy papers-server v3.0**

### Phase 2: SHORT-TERM (this week) — Make It Complete

1. **Batch upload paper.md files to R2** — pull from Zenodo, PDFs, or regenerate
2. **Add AI Query box** — textarea → ask-qwav Worker
3. **Add Related Papers** — query graph-api for neighbors
4. **Add category filtering** — parse `?category=` and `?search=`
5. **Register papers.qnfo.org with Google Search Console**

### Phase 3: LONG-TERM — Make It Robust

1. **Automate R2 upload in publication-publisher** — Stage 6 must be MANDATORY
2. **R2 Event Notification → Queue → Auto-KG sync** — papers auto-discoverable
3. **R2 Event Notification → Queue → Auto-R2-archive** — paper.md auto-archived
4. **Vectorize re-index** — re-embed all 616 papers for semantic search
5. **Full analytics dashboard** — views, DOIs clicked, AI queries

---

*Generated by QNFO Red-Team Protocol · 2026-07-12*
