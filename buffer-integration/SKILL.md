---
name: buffer-integration
description: Buffer API integration for social media posting on QNFO/QWAV channels. Create, schedule, and manage social media posts across Twitter/X, LinkedIn, and Bluesky via Buffer. Use when user says "post this to social media," "schedule a tweet," "publish to LinkedIn," or when Phase 5 of LRAP requires social dissemination of a new publication.
---
> **INCLUDES AUTONOMOUS RED-TEAM SELF-AUDIT.** Before claiming this skill complete, autonomously run: (1) Output Verification -- negative verification. (2) Assumption Challenge -- state and test every assumption. (3) Edge Case Check -- empty/null/max/boundary/desync. (4) DoD Integration -- run _dod_enforce.py if exists. (5) Iteration -- retry on failure, max 3. ANTI-PATTERN: User should NEVER ask about quality.

> **Related:** publication-publisher


### Programmatic Loading & Execution
This skill is loaded and executed **programmatically by the LLM system** 
during response generation. Loading is triggered automatically via 
`skill_view('buffer-integration')` or `read()` with filesystem path.
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

# BUFFER INTEGRATION SKILL — v1.0 — v2.2

> **Version:** v1.0 (Kaizen-audited 2026-07-05)

> **Version:** v1.0 (Kaizen-audited 2026-07-05)


> **Phase 5 of LRAP.** Enables automated social media dissemination of QNFO/QWAV publications via Buffer **GraphQL API**.

---

## execute_plan (MANDATORY — Before Any Execution)

**This skill involves execution-heavy workflows.** Before executing, use update_plan to populate a concrete, verifiable checklist. Every item must be short, specific, and testable with tool evidence.

### Execution Protocol

1. **Populate update_plan** with workflow phases as concrete checklist items
2. **Execute one item at a time** — at most ONE in_progress
3. **Mark items completed ONLY with tool evidence** (Test-Path, exec output, git log)
4. **Never claim completion without execution evidence** — Rule 14 enforcement
5. **If blocked:** Flag as [BLOCKED: reason] and move to the next item

### Example Plan

update_plan([
  {"step": "Load Buffer access token", "status": "pending"},
  {"step": "List configured social profiles", "status": "pending"},
  {"step": "Generate channel-optimized post text", "status": "pending"},
  {"step": "Create posts with staggered schedule", "status": "pending"},
  {"step": "Verify posts in Buffer queue", "status": "pending"},
])

---

## Purpose

Integrate with the Buffer GraphQL API (api.buffer.com) to create, schedule, and manage social media posts across all configured QNFO/QWAV channels (Twitter/X, LinkedIn, Bluesky). Eliminates manual social media posting and enables scheduled, staggered dissemination of research publications.

## When to Use

| Trigger | Action |
|:--------|:-------|
| "Post this paper to social media" | Generate + schedule posts for all channels |
| "Schedule a tweet about the new publication" | Twitter/X specific post |
| "What are my Buffer profiles?" | List configured social profiles |
| "Check my scheduled posts" | List pending Buffer updates |
| Phase 5 of LRAP | Automatic trigger via `social-orchestrator` skill |

## Prerequisites

1. **Buffer Access Token** stored at `%USERPROFILE%\.buffer_token` (utf-8, no BOM)
2. **Buffer profiles configured** — Twitter/X, LinkedIn, Bluesky connected to your Buffer account
3. **Organization ID** — auto-discovered via GraphQL; requires at least one Buffer organization

### Token Setup

```bash
# Store Buffer token (one-time setup)
# Get token from: https://buffer.com/developers
# IMPORTANT: Save as UTF-8 without BOM
# Write setup script to file, execute, discard
echo "import os; token = input('Buffer Access Token: ').strip(); path = os.path.expandvars(r'%USERPROFILE%\\.buffer_token'); open(path, 'w', encoding='utf-8').write(token); print('[OK] Buffer token stored')" > _setup_buffer_token.py
python _setup_buffer_token.py
Remove-Item _setup_buffer_token.py
```

### Token Troubleshooting

If you see `UnicodeEncodeError: 'latin-1' codec can't encode character '\ufeff'`:
```bash
# Write BOM removal script to file, execute, discard
echo "import os; p = os.path.expandvars(r'%USERPROFILE%\\.buffer_token'); raw = open(p, 'rb').read(); open(p, 'wb').write(raw[3:]) if raw[:3] == b'\xef\xbb\xbf' else None; print('[OK] BOM removed from token file')" > _fix_bom.py
python _fix_bom.py
Remove-Item _fix_bom.py
```

## Workflow — 4 Stages

### Stage 1: Load Configuration (GraphQL)

```python
import os

def load_buffer_token():
    token_path = os.path.expandvars(r'%USERPROFILE%\.buffer_token')
    if not os.path.exists(token_path):
        raise FileNotFoundError(
            "[BLOCKED] Buffer token not found. Get token from "
            "https://buffer.com/developers and store at %USERPROFILE%\\.buffer_token"
        )
    with open(token_path, 'r', encoding='utf-8-sig') as f:
        return f.read().strip()
```

### Stage 2: List Channels (GraphQL)

Discover social media channels via GraphQL:

```python
def list_channels(token: str) -> list[dict]:
    """Get all Buffer channels via GraphQL API."""
    import urllib.request, json
    
    def gql(query, variables=None):
        body = {"query": query}
        if variables:
            body["variables"] = variables
        data = json.dumps(body).encode("utf-8")
        req = urllib.request.Request(
            "https://api.buffer.com/1/graphql.json", data=data, method="POST"
        )
        req.add_header("Authorization", f"Bearer {token}")
        req.add_header("Content-Type", "application/json")
        resp = urllib.request.urlopen(req, timeout=15)
        return json.loads(resp.read().decode("utf-8"))
    
    # Get organization ID
    acct = gql("{ account { organizations { id } } }")
    org_id = acct["data"]["account"]["organizations"][0]["id"]
    
    # Get channels
    result = gql(
        '{ channels(input: { organizationId: "%s" }) { id service name displayName isDisconnected } }' % org_id
    )
    return result["data"]["channels"]
```

### Stage 3: Create Posts (GraphQL Mutation)

Create posts via the `createPost` mutation:

```python
def create_post(token: str, channel_id: str, text: str,
                link_url: str = None, schedule_at: str = None,
                now: bool = False, service: str = "") -> dict:
    """Create a Buffer post via GraphQL API."""
    # ... (same implementation as above) ...
    return {"success": True, "post_id": post_result["post"]["id"],
            "status": post_result["post"]["status"],
            "due_at": post_result["post"].get("dueAt")}
```

### Stage 3.5: Update Knowledge Graph with Social Media URLs (v3.0 — MANDATORY)

After successfully posting to ALL channels, update the publication's Knowledge Graph Paper node with the resolved social media post URLs. This enables one-query discovery of all external locations.

```python
def update_kg_social_urls(paper_slug: str, post_results: list) -> dict:
    """Update the Paper KG node with social media post URLs.
    
    Args:
        paper_slug: Publication slug (e.g., 'quantum-error-correction-ultrametric')
        post_results: List of {service, url} dicts from Buffer posting
    
    Contract: publication-publisher Stage 6.5d specifies the interface.
    The Paper node's social_urls property is initialized as '[]' and
    MUST be updated here after social dissemination.
    """
    import urllib.request, json
    
    PAPER_ID = f'paper-{paper_slug}'
    SOCIAL_URLS = json.dumps([r['url'] for r in post_results if r.get('url')])
    
    if not SOCIAL_URLS or SOCIAL_URLS == '[]':
        print('[KG] No social URLs to sync — nothing posted or URLs missing')
        return {"success": False, "error": "No URLs to sync"}
    
    payload = {
        'action': 'bulk',
        'nodes': [{
            'id': PAPER_ID,
            'label': 'Paper',
            'properties': {'social_urls': SOCIAL_URLS}
        }],
        'edges': []
    }
    
    body = json.dumps(payload).encode()
    req = urllib.request.Request(
        'https://graph-api.q08.workers.dev/sync',
        data=body, method='POST',
        headers={'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'}
    )
    result = json.loads(urllib.request.urlopen(req, timeout=15).read())
    
    print(f'[KG] Social URLs updated for {PAPER_ID}: nodes={result.get("upserted_nodes","?")}')
    
    # Verify
    verify_req = urllib.request.Request(
        f'https://graph-api.q08.workers.dev/neighbors/{PAPER_ID}',
        headers={'User-Agent': 'Mozilla/5.0'}
    )
    verify_data = json.loads(urllib.request.urlopen(verify_req, timeout=10).read())
    
    paper_node = None
    for n in verify_data.get('neighbors', []):
        if n.get('id') == PAPER_ID:
            paper_node = n
            break
    
    if paper_node and paper_node.get('properties', {}).get('social_urls', '[]') != '[]':
        print(f'[KG-VERIFIED] social_urls populated: {paper_node["properties"]["social_urls"]}')
        return {"success": True, "urls": SOCIAL_URLS}
    
    return {"success": False, "error": "social_urls verification failed — still empty"}
```

**GATE:** After posting, `social_urls` on the Paper KG node MUST be non-empty (not `"[]"`). If verification fails → `[BLOCKED: social URLs not synced to KG]`. Retry with KG mutex: POST `https://qnfo-agent-session.q08.workers.dev/kg-mutex/acquire` → graph-api `/sync` → POST `/kg-mutex/release`.

### Stage 4: Channel-Specific Formatting

Each social platform has different character limits, formatting rules, and audience expectations:

```python
def format_for_channel(service: str, paper_title: str, paper_doi: str, 
                        key_finding: str = "", paper_url: str = "") -> str:
    """Generate channel-optimized post text."""
    
    templates = {
        "twitter": {
            "max_chars": 280,
            "format": (
                "🚀 {hook}\n"
                "Key finding: {finding}\n"
                "📄 Full paper: {link}\n"
                "{hashtags}"
            ),
            "hashtags": "#research #QNFO #QWAV",
        },
        "linkedin": {
            "max_chars": 3000,
            "format": (
                "📄 New Research Publication\n\n"
                "{title}\n\n"
                "{finding}\n\n"
                "Read the full paper: {link}\n\n"
                "{hashtags}"
            ),
            "hashtags": "#Research #AcademicPublishing #OpenScience",
        },
        "bluesky": {
            "max_chars": 300,
            "format": (
                "📄 {title}\n\n"
                "{finding}\n\n"
                "Read: {link}"
            ),
            "hashtags": "",
        },
    }
    
    tmpl = templates.get(service, templates["twitter"])
    
    # Truncate title for short platforms
    short_title = paper_title[:100] + "..." if len(paper_title) > 100 else paper_title
    
    # Use DOI if no custom paper URL provided
    link = paper_url or f"https://doi.org/{paper_doi}"
    
    # Format finding (keep concise for Twitter)
    finding = key_finding[:120] + "..." if len(key_finding) > 120 and service == "twitter" else key_finding
    
    return tmpl["format"].format(
        hook=f"New research: {short_title}",
        title=paper_title,
        finding=finding or "Published on QNFO/QWAV",
        link=link,
        hashtags=tmpl["hashtags"],
    )[:tmpl["max_chars"]]
```

---

## ⚠️ REST API PERMANENTLY REMOVED (v2.1)

The legacy REST API at `api.bufferapp.com` is **permanently shut down** and returns HTTP 401 for all requests. The `scripts/buffer_post.py` has been removed from this skill. **All posting MUST use the GraphQL API** (Section "Workflow — 4 Stages" above).

---

## 🔑 CRITICAL: ChannelId Must Be Exact 24-Char Hex

> **THE #1 CAUSE OF FAILURE:** Truncated or wrong ChannelIds.

The Buffer GraphQL channels query returns `id` fields that are **exactly 24 hexadecimal characters**. Copy them verbatim — do NOT truncate, do NOT change case, do NOT add prefixes. Example:

```json
{"id": "679f024fd7abca001fddb4c2"}
```

A truncated ID like `679f024fd7abca` (12 chars) will NOT work. Verify your channel IDs have 24 characters before calling `create_post()`.

### Verify Channel IDs

```python
def verify_channel_ids(channels):
    """Check all channel IDs are valid 24-char hex strings."""
    for ch in channels:
        cid = ch.get("id", "")
        if len(cid) != 24:
            print(f"  WARN: Bad ChannelId for {ch['service']}: {cid} ({len(cid)} chars, needs 24)")
        else:
            print(f"  OK   {ch['service']}: {cid}")
```

---

## ✅ Verified Working (v2.1 — 2026-06-30)

The GraphQL API was **proven working** for 6 posts across 3 channels:

| Paper | DOI | Twitter | Bluesky | LinkedIn |
|:------|:----|:--------|:--------|:---------|
| Silent Radix | 10.5281/zenodo.21067593 | `6a43d23a1ec479235021c836` | `6a43d23c1e42905afea3b54c` | `6a43d23d9c6ee994bd422862` |
| Cyclic Measurement | 10.5281/zenodo.21047527 | `6a43d2519c6ee994bd422947` | `6a43d2533a82910a41251a3c` | `6a43d254032afd2413bd5075` |

**Key corrections in v2.1:**
1. `schedulingType` and `mode` are **separate top-level fields** in CreatePostInput (not nested)
2. `isQueuePaused` is the correct field name (not `isPaused`)
3. ChannelId must be the **exact 24-char hex** from the channels query — never truncated
4. GraphQL endpoint: `https://api.buffer.com/1/graphql.json` — REST API `api.bufferapp.com` is dead



---

## Integration Points

| Upstream Skill | How It Feeds Buffer Integration |
|:---------------|:-------------------------------|
| `social-orchestrator` | Generates channel-optimized text → calls this skill to post |
| `publication-publisher` | After Zenodo + Cloudflare deploy → triggers social dissemination |
| `research-orchestrator` | Calls as Phase 5 of the pipeline |

## Channel Format Reference

| Platform | Max Length | Hashtag Strategy | Link Behavior | Best Time |
|:---------|:----------|:-----------------|:--------------|:----------|
| **Twitter/X** | 280 chars | 3-5 specific hashtags | Auto-card from DOI | Tue-Thu 9-11am |
| **LinkedIn** | 3000 chars | 3-5 professional hashtags | Rich preview | Tue-Thu 8-10am |
| **Bluesky** | 300 chars | Optional, community-driven | Plain text link | Tue-Thu 10am-12pm |

## Failure Handling

| Scenario | Response |
|:---------|:---------|
| Buffer token missing | `[BLOCKED: no token]` — guide user to get token from buffer.com/developers |
| Token file has BOM | Auto-handled via `encoding='utf-8-sig'` in load_token() |
| Profile not found for channel | `[NO-PROFILE: twitter]` — list available channels, suggest connecting |
| Organization not found | `[BLOCKED] No Buffer organization` — create one at buffer.com |
| Post text exceeds platform limit | Truncated automatically (280 for Twitter, 300 for Bluesky) |
| Channel disconnected | `[WARN] Channel {service} is disconnected — skipping.` |
| HTTP 401 Unauthorized | Token expired — regenerate at buffer.com/developers |
| Network error / timeout | Auto-retry via urllib (graceful error message shown) |
| Bluesky/Twitter/LinkedIn notification mode | Not supported — script always uses `automatic` schedulingType |
| Rate limit (100 req/15min) | Buffer API enforces; back off and retry |

---

*buffer-integration v2.2 — Phase 5 of LRAP. Buffer GraphQL API integration for automated social media dissemination. v2.2 adds Stage 3.5: KG auto-update with social media URLs after posting (publication-publisher v3.0 contract).*

## RT: RED-TEAM SELF-AUDIT

Before claiming this skill complete, autonomously run:

1. Output Verification (negative verification)
2. Assumption Challenge (state and test every assumption)
3. Edge Case Check (empty/null/max/boundary/desync)
4. DoD Integration (run _dod_enforce.py if exists)
5. Iteration (retry on failure, max 3)

ANTI-PATTERN: User should NEVER ask about quality.
Refer to RED-TEAM-PROTOCOL.md for full protocol.

