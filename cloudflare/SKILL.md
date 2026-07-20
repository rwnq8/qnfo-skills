---
name: cloudflare
description: ULTRA-CONSOLIDATED Cloudflare Full-Stack -- Workers, Pages, D1, R2, KV, Vectorize, Queues, Durable Objects, AI, DNS, Zero Trust, Email, WAF, CDN, Turnstile, Infrastructure Audit. The ONLY infrastructure skill. NEVER treat Cloudflare components in isolation -- ALL code, outputs, and deliverables must evaluate the full Cloudflare stack end-to-end.
version: "3.1"
triggers: ["cloudflare-deployer", "deploy", "wrangler", "Pages", "Workers", "R2", "D1", "DNS", "KV", "Vectorize", "Queues", "AI", "Durable Objects", "Zero Trust", "Access", "Gateway", "WARP", "Tunnel", "WAF", "CDN", "Turnstile", "email", "SPF", "DKIM", "DMARC", "infrastructure", "audit", "health check", "orphan", "lifecycle", "worker route", "route conflict", "522", "CNAME", "Cloudflare", "upload", "migrate", "Pages Functions", "Workers for Platforms", "Cron Triggers", "Tail Workers", "Smart Placement", "Hyperdrive", "Secrets Store", "Pipelines", "Browser Rendering", "Zaraz", "Argo", "Spectrum", "TURN", "Network Interconnect", "Cache Reserve", "Bot Management", "API Shield", "DDoS", "Analytics Engine", "Web Analytics", "GraphQL API", "Observability", "Miniflare", "Sandbox", "Workerd", "Terraform", "Pulumi", "Snippets", "Containers", "Workflows", "Artifacts", "R2 Data Catalog", "R2 SQL", "Static Assets", "Bindings", "Image", "Stream", "RealtimeKit", "Flagship", "feature flags", "Agents SDK", "AI Gateway", "AI Search", "Workers AI", "do", "durable", "sandbox", "turnstile", "web-perf", "thin client", "IaC", "consolidation", "4-D", "IPFS bridge", "DNSLink", "Arweave", "Filecoin", "distributed", "durable", "discoverable", "duplicated"]
related: ["qnfo-agent", "research"]
priority: 1
platform: cloudflare
autonomous: true
self_sufficient: true
---

# CLOUDFLARE -- v3.1 (Full-Stack + 4-D + Consolidation)

> **v3.1 UPDATE (2026-07-20, Pinata quota exceeded):** Removed Pinata from
> the R2→IPFS Bridge. Filebase (free 5GB S3-compatible, no request-volume
> limit, auto-pins on write) is now the PRIMARY pinner; Lighthouse (free
> Filecoin tier) is SECONDARY. See `scripts/filebase-upload.js` for the
> SigV4 helper — this same helper is reused by the `research` skill's
> `scripts/filebase-pin.js`. Do not add `PINATA_API_KEY`/`PINATA_API_SECRET`
> back to any Worker env or wrangler secret.

> **Merges 9:** cloudflare + cloudflare-deployer + cloudflare-one + cloudflare-email-service + email + infrastructure-audit + web-perf + workers-best-practices + wrangler
> **Added v3.0:** Worker Consolidation Pattern, R2→IPFS Bridge, DNSLink Deployment, 4-D Architecture
> **Related:** Always load with `qnfo-agent` for production immutability gates + due diligence. Load `research` for 4-D distribution pipeline.
> **Full-Stack Mandate:** Evaluate Workers, D1, R2, KV, DO, AI, Vectorize, Queues, Pages, DNS, Zero Trust, Email, WAF, CDN as ONE integrated platform. NEVER isolate components.

## execute_plan

update_plan([
  {"step": "Identify service via decision trees below", "status": "pending"},
  {"step": "Check full-stack cross-service implications", "status": "pending"},
  {"step": "Execute with Cloudflare-native tools (wrangler CLI, REST API, Dashboard)", "status": "pending"},
  {"step": "Verify deployment health + DNS integrity + lifecycle state", "status": "pending"},
  {"step": "Audit: check for orphans, 522-RISK, CNAME chains, resource drift", "status": "pending"},
  {"step": "4-D Gate: Verify Distributed, Durable, Discoverable, Duplicated storage", "status": "pending"},
])

---

## Worker Consolidation Pattern (MANDATORY)

### Rule
Workers sharing the same D1/R2 bindings MUST be consolidated into a single unified gateway Worker. Queue/cron Workers stay separate (they require dedicated bindings).

### Consolidation Decision Matrix
| Worker Type | Consolidatable? | Reason |
|:------------|:---------------|:-------|
| HTTP API (same bindings) | **Yes** | Routes merge into gateway, domains point to same Worker |
| Queue consumer | **No** | Requires queue binding — dedicated Worker per queue |
| Cron trigger | **No** | Requires cron binding — dedicated Worker per schedule |
| MCP protocol | **Maybe** | If D1/R2 overlap with gateway, merge; else separate |
| AI/LLM inference | **Maybe** | If Workers AI binding shared, merge; else separate |

### Consolidation Workflow
1. Audit all Workers: list bindings, routes, domains
2. Identify sharing groups (same D1/R2 bindings)
3. Merge HTTP routes into gateway Worker
4. Add all D1 bindings to gateway metadata
5. Deploy consolidated gateway
6. Migrate domains from old Workers → gateway
7. Delete old Workers
8. Verify all routes respond

### Example: 2026-07-18 Consolidation (9→7)
```
qnfo-api     ─┐
graph-api    ─┼──► qnfo-gateway v2.0 (17 routes, 7 domains)
qnfo-legal   ─┘
```

---

## Reusable Scripts (Copy-Paste into any execution context)

### Filebase S3 SigV4 Upload (IPFS Auto-Pin)
```js
// _filebase_upload.js — Upload to Filebase → auto IPFS pin
const crypto = require('crypto');
const AK = process.env.FILEBASE_ACCESS_KEY;
const SK = process.env.FILEBASE_SECRET_KEY;
const HOST = 's3.filebase.com';
const BUCKET = 'qnfo-archive'; // Use existing bucket or create in dashboard

function hmac(k, d) { return crypto.createHmac('sha256', k).update(d).digest(); }

async function s3Put(key, body, contentType) {
  const payloadHash = crypto.createHash('sha256').update(body).digest('hex');
  const amzDate = new Date().toISOString().replace(/[:-]|\.\d{3}/g, '');
  const dateStamp = amzDate.substring(0, 8);
  const path = '/' + BUCKET + '/' + key;
  
  // AWS SigV4 canonical request
  const canonicalReq = [
    'PUT', path, '',
    'content-type:' + (contentType || 'text/plain'),
    'host:' + HOST,
    'x-amz-content-sha256:' + payloadHash,
    'x-amz-date:' + amzDate + '\n',
    'content-type;host;x-amz-content-sha256;x-amz-date',
    payloadHash
  ].join('\n');
  
  // String to sign
  const credentialScope = dateStamp + '/us-east-1/s3/aws4_request';
  const stringToSign = [
    'AWS4-HMAC-SHA256', amzDate, credentialScope,
    crypto.createHash('sha256').update(canonicalReq).digest('hex')
  ].join('\n');
  
  // Derive signing key
  const kDate = hmac('AWS4' + SK, dateStamp);
  const kRegion = hmac(kDate, 'us-east-1');
  const kService = hmac(kRegion, 's3');
  const kSigning = hmac(kService, 'aws4_request');
  const signature = hmac(kSigning, stringToSign).toString('hex');
  
  const auth = 'AWS4-HMAC-SHA256 Credential=' + AK + '/' + credentialScope +
    ',SignedHeaders=content-type;host;x-amz-content-sha256;x-amz-date,Signature=' + signature;
  
  const r = await fetch('https://' + HOST + path, {
    method: 'PUT',
    headers: { Authorization: auth, 'Content-Type': contentType,
      Host: HOST, 'x-amz-content-sha256': payloadHash, 'x-amz-date': amzDate },
    body: body
  });
  // Filebase auto-pins all S3 objects to IPFS
  return { status: r.status, ok: r.ok, ipfsCid: r.headers.get('x-ipfs-cid') };
}
```

### Worker Deployment (via REST API)
```js
// _deploy_worker.js — Deploy/update a Cloudflare Worker
const T = process.env.CLOUDFLARE_API_TOKEN;
const ACCOUNT = '...'; // Cloudflare account ID
const WORKER = 'worker-name';

(async () => {
  const form = new FormData();
  form.append('worker.js', new Blob([workerCode], { type: 'application/javascript+module' }), 'worker.js');
  form.append('metadata', JSON.stringify({
    main_module: 'worker.js',
    bindings: [
      { type: 'r2_bucket', name: 'MY_BUCKET', bucket_name: 'bucket-name' },
      { type: 'd1', name: 'MY_DB', database_id: 'database-uuid' }
    ]
  }));
  const r = await fetch('https://api.cloudflare.com/client/v4/accounts/' + ACCOUNT + '/workers/scripts/' + WORKER, {
    method: 'PUT', headers: { 'Authorization': 'Bearer ' + T }, body: form
  });
  const d = await r.json();
  console.log('Deploy:', d.success ? 'OK' : 'FAIL: ' + (d.errors ? d.errors.map(e=>e.message).join(', ') : ''));
})();
```

### R2 Object Upload Script
```js
// _r2_upload.js — Upload any file to R2 bucket
const T = process.env.CLOUDFLARE_API_TOKEN;
await fetch('https://api.cloudflare.com/client/v4/accounts/' + ACCOUNT + '/r2/buckets/' + BUCKET + '/objects/' + encodeURIComponent(KEY), {
  method: 'PUT', headers: { 'Authorization': 'Bearer ' + T }, body: content
});
// Alt: npx wrangler r2 object put {BUCKET}/{KEY} --file path --remote
```

### D1 Query Script
```js
// _d1_query.js — Execute D1 SQL via REST API
const T = process.env.CLOUDFLARE_API_TOKEN;
await fetch('https://api.cloudflare.com/client/v4/accounts/' + ACCOUNT + '/d1/database/' + DB + '/query', {
  method: 'POST',
  headers: { 'Authorization': 'Bearer ' + T, 'Content-Type': 'application/json' },
  body: JSON.stringify({ sql: 'SELECT * FROM t LIMIT 10' })
});
```

### DNSLink Creation Script
```js
// _dnslink_create.js — Map domain to IPFS CID
await fetch('https://api.cloudflare.com/client/v4/zones/' + ZONE + '/dns_records', {
  method: 'POST',
  headers: { 'Authorization': 'Bearer ' + process.env.CLOUDFLARE_API_TOKEN, 'Content-Type': 'application/json' },
  body: JSON.stringify({ type: 'TXT', name: '_dnslink.' + SUB, content: 'dnslink=/ipfs/' + CID, ttl: 1 })
});
```

### Worker Route Creation Script
```js
// _worker_route.js — Route domain to Worker
await fetch('https://api.cloudflare.com/client/v4/zones/' + ZONE + '/workers/routes', {
  method: 'POST',
  headers: { 'Authorization': 'Bearer ' + process.env.CLOUDFLARE_API_TOKEN, 'Content-Type': 'application/json' },
  body: JSON.stringify({ pattern: DOMAIN + '/*', script: WORKER })
});
```

### R2 Hygiene Check
```js
// _r2_hygiene.js — Check for qnfo/qnfo/ double-prefix
const r = await fetch('https://api.cloudflare.com/client/v4/accounts/' + A + '/r2/buckets/qnfo/objects?prefix=qnfo/&limit=5', {
  headers: { 'Authorization': 'Bearer ' + T }
});
const d = await r.json();
const bad = (d.result?.objects||[]).filter(o => o.key.startsWith('qnfo/'));
if (bad.length > 0) bad.forEach(o => console.log('FIX: ' + o.key));
```



### "I need to run code"
```
Serverless functions at edge -> Workers
Full-stack web app with Git -> Pages
Stateful coordination/real-time -> Durable Objects
Long-running multi-step jobs -> Workflows
Run Docker containers -> Containers
Multi-tenant platform -> Workers for Platforms
Scheduled tasks (cron) -> Cron Triggers
Lightweight edge logic -> Snippets
Process Worker execution events -> Tail Workers
Optimize latency to backend -> Smart Placement
```

### "I need to store data"
```
Key-value (config/sessions/cache) -> KV
Relational SQL -> D1 (SQLite) or Hyperdrive (existing Postgres/MySQL)
Object/file storage (S3-compatible) -> R2
Versioned file trees -> Artifacts
Message queue (async processing) -> Queues
Vector embeddings (AI/semantic search) -> Vectorize
Strongly-consistent per-entity state -> Durable Objects (DO Storage)
Secrets management -> Secrets Store
Streaming ETL to R2 -> Pipelines
Managed Apache Iceberg catalog on R2 -> R2 Data Catalog
Serverless SQL analytics over Iceberg -> R2 SQL
Persistent cache -> Cache Reserve
```

### "I need AI/ML"
```
Run inference (LLMs/embeddings/images) -> Workers AI
Vector database for RAG/search -> Vectorize
Build stateful AI agents -> Agents SDK
Gateway for any AI provider -> AI Gateway
AI-powered search widget -> AI Search
Browser automation/screenshots -> Browser Rendering
```

### "I need networking"
```
Expose local service to internet -> Tunnel (cloudflared)
TCP/UDP proxy (non-HTTP) -> Spectrum
WebRTC TURN server -> TURN
Private network connectivity -> Network Interconnect
Optimize routing -> Argo Smart Routing
Workers private network -> Workers VPC
Real-time video/audio -> RealtimeKit or Realtime SFU
```

### "I need security"
```
Web Application Firewall -> WAF
DDoS protection -> DDoS
Bot detection/management -> Bot Management
API protection -> API Shield
CAPTCHA alternative -> Turnstile
Credential leak detection -> WAF Managed Ruleset
```

### "I need media/content"
```
Image optimization/transformation -> Images
Video streaming/encoding -> Stream
Third-party script management -> Zaraz
```

### "I need analytics/data"
```
Query across all Cloudflare products -> GraphQL Analytics API
Custom high-cardinality metrics -> Analytics Engine
Client-side (RUM) performance data -> Web Analytics
Workers Logs and real-time debugging -> Observability
SQL over Iceberg data lake -> R2 SQL (+ Pipelines + R2 Data Catalog)
Raw logs (Logpush to external) -> Cloudflare docs
```

### "I need infrastructure-as-code"
```
Pulumi -> Pulumi provider
Terraform -> Terraform provider
REST API -> Cloudflare API
```

---

## R2→IPFS Bridge (4-D Integration)

**PINATA REMOVED (2026-07-20, free quota exceeded, account blocked).** The
R2→IPFS bridge now routes through **Filebase** (free 5GB S3-compatible
bucket, no request-volume limit, auto-pins every object on write) as the
PRIMARY pinner. This eliminates the extra `pinByHash` API hop entirely —
writing to Filebase via S3 `PUT` auto-pins in one step.

### Architecture
```
R2 Write Event ──► qnfo-archive Worker (queue) ──► Filebase S3 PUT ──► IPFS Network (auto-pin)
                         │                              │
                         │                        (fallback: Lighthouse free Filecoin tier)
  Cloudflare IPFS Gateway ◄── DNSLink ◄── _dnslink TXT
  (CDN-accelerated edge delivery, free/unlimited)
```

### qnfo-archive Worker Extension (Filebase, replaces Pinata pinByHash)
```js
// On R2 archival event, auto-pin to IPFS via Filebase S3-compatible PUT.
// Filebase pins on write — no separate "pin" API call needed.
// Requires: FILEBASE_ACCESS_KEY, FILEBASE_SECRET_KEY (AWS SigV4 auth against s3.filebase.com)
// See scripts/filebase-upload.js in this skill for the full SigV4 helper (s3Put).
async function pinToIPFSViaFilebase(env, key, body, contentType, metadata) {
  const result = await s3Put(env.FILEBASE_BUCKET || 'qnfo-archive', key, body, contentType);
  if (!result.ok) {
    throw new Error('Filebase PUT failed: HTTP ' + result.status + ' — do NOT fall back to Pinata (quota exceeded, blocked). Try Lighthouse instead.');
  }
  return result.ipfsCid; // returned via x-ipfs-cid response header
}
```

### Multi-Service Pinning Credentials
| Service | Credential | Purpose |
|:--------|:-----------|:--------|
| Filebase (PRIMARY) | `FILEBASE_ACCESS_KEY` + `FILEBASE_SECRET_KEY` | Free 5GB, no request-volume limit, S3→IPFS auto-pinning |
| Lighthouse (SECONDARY) | `LIGHTHOUSE_API_KEY` | Free-tier Filecoin storage deals, no CC required |
| ~~Pinata~~ | ~~`PINATA_API_KEY` + `PINATA_API_SECRET`~~ | **REMOVED 2026-07-20 — free quota exceeded, account blocked. Do not use, do not add credentials back.** |

---

## DNSLink Deployment

### Pattern
Every QNFO publication subdomain gets a DNSLink TXT record:
```bash
curl -X POST "https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/dns_records" \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
  -d '{"type":"TXT","name":"_dnslink.{subdomain}","content":"dnslink=/ipfs/{CID}","ttl":1}'
```

### Verification
- `https://cloudflare-ipfs.com/ipns/{subdomain}.qnfo.org` → serves content from IPFS
- `nslookup -type=TXT _dnslink.{subdomain}.qnfo.org` → returns `dnslink=/ipfs/{CID}`

---

## Cloudflare One (Zero Trust & SASE)

### Product Suite
- **Access:** Zero Trust application access. Replace VPN with identity-aware proxy.
- **Gateway:** DNS filtering, HTTP filtering, SWG (Secure Web Gateway)
- **WARP:** Device client that routes traffic through Cloudflare network
- **Tunnel:** `cloudflared` -- expose local services to Cloudflare edge without public IPs
- **DLP:** Data Loss Prevention -- scan data in transit for sensitive content
- **CASB:** Cloud Access Security Broker -- API-based SaaS security
- **Device Posture:** Check device health before granting access
- **Browser Isolation:** Remote browser session for risky sites

### Migrations (from Zscaler, VPN, etc.)
1. Deploy WARP client to endpoints
2. Configure Gateway DNS + HTTP policies equivalent to legacy
3. Set up Tunnel for internal applications (replacing VPN)
4. Migrate access policies to Access
5. Phase out legacy infrastructure

---

## Email (Workers Binding + Email Routing)

### Sending Email (Workers Binding)
```javascript
// wrangler.jsonc
{
  "send_email": [{
    "name": "SEND_EMAIL",
    "destination_address": "me@example.com"
  }]
}

// In Worker
await env.SEND_EMAIL.send(
  new EmailMessage(
    "from@example.com",
    "to@example.com",
    "Subject line",
    "Plain text body",
    "<p>HTML body</p>"
  )
);
```

### Email Routing (Inbound Processing)
```jsonc
// wrangler.jsonc
{
  "email_routing": [{
    "name": "INBOUND",
    "destination_address": "catchall@example.com"
  }]
}

// In Worker -- handle incoming emails
export default {
  async email(message, env, ctx) {
    const { to, from, subject, raw } = message;
    await message.forward("forwarded@example.com");
  }
};
```

### SPF/DKIM/DMARC Setup
```
SPF:  TXT @ "v=spf1 include:_spf.mx.cloudflare.net ~all"
DKIM: CNAME <selector>._domainkey <selector>._domainkey.<zone>.onmicrosoft.com
DMARC: TXT _dmarc "v=DMARC1; p=quarantine; rua=mailto:dmarc@example.com"
```

---

## Infrastructure Audit (Full Ecosystem)

### D1 Databases
Baseline: 6. Database IDs: `ipatent-db`, `qnfo-cms`, `living-paper`, `portfolio-state`, `qnfo-graph`, `qnfo-audit`

### R2 Buckets
Baseline: 14 buckets (added `releases` 2026-07-15, distinct from `qnfo-releases`).

### Workers
Baseline: 7 (post-consolidation 2026-07-18).
**Fleet:** `qnfo-gateway` (unified API+graph+legal+papers, 17 routes), `qnfo-archive`, `qnfo-lifecycle` (v1.1 — 7 cron handlers with real logic, `/status` fixed), `qnfo-ai`, `qnfo-ipatent`, `qnfo-memory-mcp` (v1.0.1 — debug endpoints removed), `qnfo-qwav`

### Pages
Baseline: 5 projects (post-consolidation 2026-07-17: `qnfo-publications`, `qwav`, `qnfo-hub`, `ipatent-me`, `ask-qwav`).

### Vectorize
Baseline: 4 indexes.

### DNS Integrity Checks

#### 522-RISK Detection (MANDATORY)
For every CNAME record pointing to `.pages.dev`, verify the domain is registered on the target Pages project.

#### CNAME Chain Detection
Detect CNAME chains: A -> B -> C.pages.dev

#### Dead Worker Detection
CNAME pointing to non-existent Worker.

### Lifecycle Pipeline

| Worker | Purpose | Cron | Health Check |
|:-------|:--------|:-----|:-------------|
| `qnfo-lifecycle` | Scans `last_active`, transitions ACTIVE->STALE->ARCHIVED | Daily 06:00 UTC | `curl https://qnfo-lifecycle.q08.workers.dev/status` |
| `qnfo-archive` | Consumes queue, migrates R2 files | On queue trigger | `curl https://qnfo-archive.q08.workers.dev/health` |

### Lifecycle Timeline
| Days Inactive | Status | Action |
|:-------------:|:-------|:-------|
| 0-90 | ACTIVE | Normal operation |
| 90-180 | STALE | Flagged by Lifecycle Worker. Project intact. |
| 180+ | ARCHIVED | R2 files auto-migrated to `qnfo/archive/projects/<name>/` |

### Resource Baselines (post-consolidation)

| Resource | Expected | Warning | Critical |
|:---------|:--------|:--------|:---------|
| D1 Databases | 6 | +/- 1 | +/- 2+ |
| Workers | 7 | 8-9 | 10+ |
| Pages Projects | 5 | 6-7 | 8+ |
| Vectorize Indexes | 4 | +/- 1 | +/- 2+ |
| R2 Buckets | 14 | +/- 1 | +/- 3+ |
| Queues | 1 | +/- 1 | +/- 2+ |
| KV Namespaces | 1 | +/- 1 | +/- 2+ |
| DNS Zones | 12 active | +/- 1 | +/- 3+ |
| 522-RISK | 0 | 1+ | -- |
| CNAME Chains | 0 | 1+ | -- |
| DEAD-WORKER | 0 | 1+ | -- |

### DNS Zones (verified 2026-07-18)
12 active zones: `empoweringchange.today`, `ipatent.me`, `q08.org`, `qnfo.net`, `qnfo.org`, `qnfo.uk`, `q-wave.tech`, `qwave.tech`, `qwav.net`, `qwav.org`, `qwav.tech`, `qwav.uk`. Growth from prior baseline (7) reflects legitimate qwav/ipatent product domain expansion, not drift.

### OPEN ITEM — I-05: Unexplained Pages Project Deletions (2026-07-18)
`audit_pages` D1 table lists 10 projects with `status='active'` as of the last sync, but only 5 exist live. `qnfo-legal` deletion is **explained** (consolidated into `qnfo-gateway` Worker v2.0). The following 4 are **UNEXPLAINED** — no matching `deployment_history` or `audit_trail` row, and Pages project deletion has no soft-delete/undo via API:
- `quantum-advantage-audit` (last deployed 2026-07-13)
- `ultrametric-ai-poc` (last deployed 2026-07-12)
- `two-ways-of-measuring` (last deployed 2026-07-12)
- `qnfo-design-system` (last deployed 2026-07-13)
- `hensel-code` (last deployed 2026-07-13)

**Action needed:** Investigate whether these were manually deleted, hit a Pages project quota/cleanup automation, or another undocumented process. If content is needed, check R2 `qnfo-backups`/`qnfo-releases` for build artifacts predating deletion. Until root-caused, treat any future Pages project disappearance as CRITICAL and halt automated cleanup scripts touching Pages.

### D1 Backup Coverage (MANDATORY — added 2026-07-18)
`qnfo-lifecycle` runs a daily 05:00 UTC cron (`runBackup`) that exports `portfolio-state.resources` and `qnfo-audit.audit_sessions` to `qnfo-backups/{db}/{table}-{date}.json`. **Before this fix, `qnfo-backups` was 0 objects for the database's entire lifetime** — a silent single-point-of-failure that turned a 3-row data-loss incident (C-01, 2026-07-18) into an unrecoverable event without D1 Time Travel. Extend `runBackup`'s `tables` array whenever a new production-critical D1 table is added (e.g., `living-paper.papers` once schema stabilizes).

**C-01 RESOLVED (2026-07-18):** `living-paper.papers` fully restored to 616 rows via `wrangler d1 time-travel restore --bookmark=00000b67-...`. KG-D1 reconciled to 616=616 (26 missing KG Paper nodes seeded via `qnfo-gateway` `/sync`). Zero data loss confirmed — a concurrent session's 189-row write (13 orphan chapter files) was verified already contained within the restored 616-row set.

### R2 Path Hygiene
**CRITICAL RULE:** Bucket name IS the namespace. NEVER prefix keys with `qnfo/` inside the `qnfo` bucket.

---

## Retrieval Sources (Prefer over pre-training)

| Source | Method | Use for |
|:-------|:-------|:--------|
| Cloudflare docs | `search_cloudflare_documentation({query})` | Limits, pricing, API reference |
| Workers types | `npm pack @cloudflare/workers-types` | Type signatures, binding shapes |
| Wrangler config schema | `node_modules/wrangler/config-schema.json` | Config fields, binding shapes |

---

## Anti-Patterns

| Anti-Pattern | Fix |
|:-------------|:----|
| Treating Cloudflare services in isolation | Evaluate full-stack: Workers + D1 + R2 + KV + DNS + WAF as ONE system |
| Deploying without infrastructure audit | Audit resource baselines BEFORE and AFTER deployment |
| Skipping DNS integrity on Pages deploy | Verify CNAME->.pages.dev domain registration (522-RISK check) |
| Using `qnfo/` prefix in R2 keys on `qnfo` bucket | Bucket IS the namespace. Use `category/subpath` convention. |
| Trusting local files over R2 | R2 is canonical. Local files are ephemeral caches. |
| `wrangler deploy` without verifying `wrangler whoami` | Always verify authentication first |
| Pages-per-publication | Use single Pages project or Workers + D1 for dynamic serving |
| Non-Cloudflare infrastructure | Architecture Compliance Gate: D1/R2/Workers ONLY |
| Duplicated Workers with same bindings | Consolidate into gateway Worker per Consolidation Pattern |
| Publishing without DNSLink | Every publication subdomain must have `_dnslink` TXT record |
| Single copy of critical assets | 4-D: Distributed, Durable, Discoverable, Duplicated |
| Skipping Arweave/Filecoin for permanence | Permanent blockchain storage for critical deliverables |
| Unauthenticated `/debug/*` routes bound to production D1 (DROP/CREATE/INSERT) | NEVER ship debug/init/seed endpoints to production Workers. Root cause of 2026-07-18 living-paper 616→3 row data loss (`qnfo-memory-mcp /debug/init`). Gate: any route containing DROP/CREATE TABLE/schema-reset logic requires auth header + non-production-only compatibility flag, or must not exist post-deploy. |
| Empty backup bucket with no verification | Add a scheduled backup Worker cron (`runBackup`) writing to R2 on day 1 of any new production D1 database. Verify object count > 0 within first 24h, not just bucket existence. |
| Assuming infra-audit narrative (handoff notes) over live D1 row counts | ALWAYS query live D1 `SELECT COUNT(*)` before trusting audit_sessions.notes — narrative logs can be stale or describe a different table than what actually shipped. |
| Vectorize binding declared in wrangler config but never called in fetch handler (dead binding masked by LIKE/stub fallback) | Read full Worker source and cross-reference every declared binding name against actual usage in handler code. Found 2026-07-18 in both `qnfo-ipatent` (`/api/search` literal stub despite populated 1024-dim `DISCLOSURES_VZ` index) and `qnfo-qwav` (`/ask` used SQL `LIKE` despite unused `QWAV_VZ` binding to 768-dim `qwav-research-v2` index). Fix: embed query via Workers AI (matching the index's original embedding model), `.query()` the Vectorize index, keep LIKE only as a fallback when AI/Vectorize is unavailable. |
| Restoring a production D1 database via Time Travel without first exporting a full row/table snapshot of ANY concurrent writes to R2 | Before any Time Travel restore, run `SELECT *` (explicit column list, avoid FTS5 tables which break `d1 export`) and upload the JSON to R2 as a safety net. Verified 2026-07-18: C-01 living-paper restore preceded by snapshot to `qnfo-backups/living-paper/pre-restore-snapshot-*.json`; post-restore diff confirmed zero data loss. |
| Using Pinata for R2→IPFS pinning (REMOVED 2026-07-20) | Pinata's free quota was exceeded and the account is blocked. Use Filebase (PRIMARY, free 5GB, auto-pins on S3 PUT) → Lighthouse (SECONDARY, free Filecoin tier). Never add `PINATA_API_KEY`/`PINATA_API_SECRET` back to Worker env vars or wrangler secrets. |
