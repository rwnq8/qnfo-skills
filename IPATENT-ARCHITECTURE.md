# ipatent.me — System Architecture v1.0
## 2026-07-12 — Rowan Quni-Gudzinas

---

## Overview

**ipatent.me** is a standalone US Provisional Patent Disclosure platform with its own D1 database, Vectorize index, and R2 bucket — completely separate from QNFO assets but within the Cloudflare quniverse account.

Every query and submission is stored **verbatim in D1** and **embedded in Vectorize**, enabling:
1. Full reconstruction of any user session or submission
2. Semantic search across all disclosures
3. Synthesis of new inventive disclosures from collective prior art patterns

---

## Architecture

```
┌──────────────────────────────────────────────────────┐
│                  PRESENTATION LAYER                   │
│                                                       │
│   ipatent.me (Cloudflare Pages: ipatent-me)          │
│   ┌─────────────┬──────────┬────────┬───────────┐   │
│   │  Generate    │  Browse  │ Search │  Stats    │   │
│   │  (Form)      │  (List)  │ (Sem)  │  (Dash)   │   │
│   └──────┬───────┴────┬─────┴───┬────┴─────┬─────┘   │
│          │            │         │          │          │
│          └────────────┼─────────┼──────────┘          │
│                       │         │                      │
└───────────────────────┼─────────┼──────────────────────┘
                        │         │
                  /api/*         │
                        │         │
┌───────────────────────▼─────────▼──────────────────────┐
│                  WORKER LAYER                           │
│                                                         │
│   ipatent-api (Cloudflare Worker)                      │
│   ┌─────────────────────────────────────────────────┐  │
│   │  POST /api/submit     → D1 + Vectorize + R2     │  │
│   │  GET  /api/submissions → D1 query                │  │
│   │  GET  /api/submissions/:id → D1 lookup           │  │
│   │  POST /api/search      → AI embed → Vectorize   │  │
│   │  POST /api/analytics    → D1 analytics           │  │
│   │  GET  /api/stats        → D1 aggregation         │  │
│   │  GET  /api/health       → Binding check          │  │
│   └─────────────────────────────────────────────────┘  │
│                                                         │
│   Bindings:                                             │
│   • DB (ipatent-db)         — D1 Database               │
│   • VECTORIZE (ipatent-disclosures) — Vectorize Index   │
│   • BUCKET (ipatent)        — R2 Bucket                 │
│   • AI                      — Workers AI (embeddings)   │
└─────────────────────────────────────────────────────────┘
                        │
          ┌─────────────┼─────────────┐
          ▼             ▼             ▼
┌──────────────┐ ┌────────────┐ ┌──────────┐
│  D1: ipatent │ │ Vectorize: │ │  R2:     │
│  -db         │ │ ipatent-   │ │  ipatent │
│              │ │ disclosures│ │          │
│ submissions  │ │            │ │  /disclo-│
│ analytics    │ │ 1024-dim   │ │  sures/  │
│ sessions     │ │ cosine     │ │  *.html  │
└──────────────┘ └────────────┘ └──────────┘
```

---

## D1 Schema (ipatent-db)

### `submissions` — Verbatim disclosure storage
| Column | Type | Description |
|:-------|:-----|:------------|
| id | INTEGER PK | Auto-increment |
| submission_id | TEXT UNIQUE | USP-XXXXXXXX-XXXXXXXX format |
| inventor_name | TEXT | Submitter name |
| inventor_email | TEXT | Contact email |
| title | TEXT NOT NULL | Invention title |
| disclosure_text | TEXT NOT NULL | Full verbatim disclosure |
| document_html | TEXT | Generated HTML document |
| r2_key | TEXT | R2 object key |
| status | TEXT | draft/generated/filed |
| ip_address | TEXT | CF-Connecting-IP |
| user_agent | TEXT | User-Agent |
| country | TEXT | CF-IPCountry |
| session_id | TEXT | Browser session |
| created_at | TEXT | ISO datetime |
| updated_at | TEXT | ISO datetime |

### `analytics` — Full event stream
| Column | Type | Description |
|:-------|:-----|:------------|
| id | INTEGER PK | Auto-increment |
| event_type | TEXT NOT NULL | pageview, form_focus, submission, search, page_exit |
| page_url | TEXT | URL path |
| referrer | TEXT | HTTP Referer |
| ip_address | TEXT | CF-Connecting-IP |
| user_agent | TEXT | User-Agent |
| country | TEXT | CF-IPCountry |
| session_id | TEXT | Browser session UUID |
| metadata | TEXT | JSON blob |
| created_at | TEXT | ISO datetime |

### `sessions` — Session aggregate
| Column | Type | Description |
|:-------|:-----|:------------|
| session_id | TEXT PK | Browser session UUID |
| ip_address | TEXT | Last known IP |
| user_agent | TEXT | Last known UA |
| country | TEXT | Last known country |
| first_seen | TEXT | First event time |
| last_seen | TEXT | Last event time |
| page_views | INTEGER | Total pageviews |
| total_events | INTEGER | Total events |
| metadata | TEXT | JSON blob |

---

## Vectorize: ipatent-disclosures

| Property | Value |
|:---------|:------|
| Dimensions | 1024 |
| Metric | cosine |
| Model | @cf/baai/bge-large-en-v1.5 |
| Embedding source | `${title}\n\n${disclosure_text}` (first 8000 chars) |
| Metadata per vector | submission_id, title, inventor, country, created_at |

---

## R2 Bucket: ipatent

| Path Pattern | Content |
|:-------------|:--------|
| `disclosures/{submission_id}.html` | Generated disclosure HTML |
| Cache-Control | public, max-age=86400 |
| Custom metadata | submission_id, title, inventor |

---

## Data Flow: Submission

```
1. User fills form → POST /api/submit
2. Worker validates title + disclosure_text
3. Generates submission ID (USP-XXXXXXXX-XXXXXXXX)
4. Generates disclosure HTML document
5. Stores HTML in R2: disclosures/{id}.html
6. INSERTS verbatim into D1 submissions table
7. Calls Workers AI: embed(title + "\n\n" + disclosure_text)
8. UPSERTS vector into Vectorize: ipatent-disclosures
9. Tracks analytics event: submission
10. Returns HTML document with X-Submission-ID header
```

## Data Flow: Search

```
1. User enters query → POST /api/search
2. Worker calls Workers AI: embed(query)
3. Queries Vectorize: ipatent-disclosures (topK=limit, cosine)
4. Enriches results from D1: title, inventor, status
5. Tracks analytics event: search
6. Returns ranked results with similarity scores
```

---

## Separation from QNFO

All ipatent.me assets are completely independent:

| Asset Type | QNFO | ipatent.me |
|:-----------|:-----|:-----------|
| D1 Database | qnfo-audit (35e2e573) | ipatent-db (19cc87d6) |
| Vectorize | qwav-research-v2 (1024d) | ipatent-disclosures (1024d) |
| R2 Bucket | qnfo | ipatent |
| Worker | Multiple | ipatent-api |
| Pages | qnfo-hub, qnfo-publications, etc. | ipatent-me |
| Domain | qnfo.org | ipatent.me |
| Account | quniverse (shared) | quniverse (shared) |

---

## Deployments

| Component | URL |
|:----------|:----|
| Pages (production) | https://ipatent-me.pages.dev |
| Pages (custom domain) | https://ipatent.me (SSL provisioning) |
| Worker (workers.dev) | https://ipatent-api.q08.workers.dev |
| Worker route | ipatent.me/api/* |

---

## Future Capabilities

1. **Synthesis Engine**: Query Vectorize with a partial idea → get semantically related disclosures → generate novel combination
2. **Citation Graph**: Track which disclosures reference which prior art → D1 graph
3. **PDF Generation**: Browser-based or server-side PDF via Workers
4. **Email Delivery**: Send generated disclosure to inventor's email
5. **USPTO Integration**: Direct SB/16 form generation
6. **Rate Limiting**: Per-session and per-IP limits on submissions
7. **Auth**: Optional account creation for saving disclosures

---

## Session 14 — ipatent.me Initialization

| Step | Status |
|:-----|:------|
| Create ipatent-db D1 database | ✅ |
| Create ipatent-disclosures Vectorize index (1024d, cosine) | ✅ |
| Create ipatent R2 bucket | ✅ |
| Create submissions, analytics, sessions tables | ✅ |
| Build ipatent-api Worker (D1+R2+Vectorize+AI) | ✅ |
| Build Pages frontend (Generate/Browse/Search/Stats) | ✅ |
| Deploy Worker with all bindings | ✅ |
| Deploy Pages site | ✅ |
| E2E test: submit → D1 → Vectorize → R2 | ✅ (3/4 vectors) |
| Semantic search verification | ✅ |
| Wire ipatent.me custom domain | ✅ (SSL pending) |
| Wire zombie domains | ✅ (5 domains → 301 redirects) |
| 17/17 domains verified | ✅ |
