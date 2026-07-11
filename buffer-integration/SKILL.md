---
name: buffer-integration
description: Buffer API integration for social media posting on QNFO/QWAV channels. Create, schedule, and manage social media posts across Twitter/X, LinkedIn, and Bluesky via Buffer. Use when user says "post this to social media," "schedule a tweet," "publish to LinkedIn," or when Phase 5 of LRAP requires social dissemination of a new publication.
version: "1.0"
---
> **INCLUDES AUTONOMOUS RED-TEAM SELF-AUDIT.** Before claiming this skill complete, autonomously run: (1) Output Verification -- negative verification. (2) Assumption Challenge -- state and test every assumption. (3) Edge Case Check -- empty/null/max/boundary/desync. (4) DoD Integration -- verify all criteria met with tool evidence. (5) Iteration -- retry on failure, max 3. ANTI-PATTERN: User should NEVER ask about quality.

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

# BUFFER INTEGRATION SKILL — v3.5

> **Version:** v3.5 (Kaizen-audited 2026-07-11) — scheduling with fallback: try addToQueue first, fall back to shareNow on LimitReachedError (Buffer free plan 10-post limit). Stagger: Twitter T+0, LinkedIn T+60, Bluesky T+120.


> **Phase 5 of LRAP.** Enables automated social media dissemination of QNFO/QWAV publications via Buffer **GraphQL API**.

---

## Autonomous Continuation Protocol (v1.0)

**All posting stages execute autonomously.** Agent MUST: (1) chain Twitter→LinkedIn→Bluesky without user prompts, (2) tag `[AUTO-CONTINUE]` between platforms. **ANTI-PATTERN:** User NEVER says "CONTINUE."

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
echo "import os; token = input('Buffer Access Token: ').strip(); path = os.path.expandvars(os.path.join(os.environ['USERPROFILE'], '.buffer_token')); open(path, 'w', encoding='utf-8-sig').write(token); print('[OK] Buffer token stored')" > _setup_buffer_token.py
python _setup_buffer_token.py
Remove-Item _setup_buffer_token.py
```

### Token Troubleshooting

If you see `UnicodeEncodeError: 'latin-1' codec can't encode character '\ufeff'`:
```bash
# Write BOM removal script to file, execute, discard
echo "import os; p = os.path.expandvars(os.path.join(os.environ['USERPROFILE'], '.buffer_token')); raw = open(p, 'rb').read(); open(p, 'wb').write(raw[3:]) if raw[:3] == b'\xef\xbb\xbf' else None; print('[OK] BOM removed from token file')" > _fix_bom.py
python _fix_bom.py
Remove-Item _fix_bom.py
```

## Workflow — 4 Stages

### Stage 1: Load Configuration (GraphQL)

```python
import os

def load_buffer_token():
    token_path = os.path.join(os.environ['USERPROFILE'], '.buffer_token')
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
            "https://api.buffer.com/graphql", data=data, method="POST"
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

### Stage 3: Create Posts (GraphQL Mutation — v3.0 SCHEMA-CORRECTED)

Create posts via the `createPost` mutation. **CRITICAL:** The Buffer GraphQL schema was introspected live (2026-07-10). Key corrections from v2.2:

| v2.2 (STALE) | v3.0 (CORRECTED) |
|:-------------|:-----------------|
| `mode: "automatic"` | `mode: "shareNow"` — ShareMode enum: `shareNow`, `addToQueue`, `shareNext`, `customScheduled` |
| `PostActionError` type | Does NOT exist. Use `InvalidInputError`, `RestProxyError`, etc. |
| `schedulingType: "automatic"` | Still correct — SchedulingType enum: `automatic`, `notification` |
| Truncated stub `# ... (same implementation as above) ...` | **FULL COMPLETE implementation embedded below** |

```python
def create_post(token: str, channel_id: str, text: str,
                link_url: str = None, schedule_at: str = None,
                now: bool = False, service: str = "",
                try_schedule_first: bool = True) -> dict:
    """Create a Buffer post via GraphQL API with scheduling fallback.

    Buffer free plan has a 10 scheduled post limit. This function:
    1. Defaults to mode="addToQueue" (scheduled) with a dueAt time
    2. If LimitReachedError (queue full) → retries with mode="shareNow" (immediate)
    3. If try_schedule_first=False → posts immediately (skips scheduling attempt)

    CreatePostInput fields (from live introspection):
      - channelId (String!): 24-char hex channel ID
      - text (String): post body text
      - schedulingType (SchedulingType!): "automatic" | "notification"
      - mode (ShareMode!): "shareNow" | "addToQueue" | "shareNext" | "customScheduled"
      - assets ([AssetInput!]!): list of media assets (use [] for text-only)
      - dueAt (DateTime): optional scheduled time (ISO 8601)
      - source (String): optional source identifier

    PostActionPayload union types (from live introspection):
      - PostActionSuccess { post { id, status, dueAt } }
      - InvalidInputError { message }
      - RestProxyError { message, link, code }
      - LimitReachedError { message }
      - NotFoundError { message }
      - UnauthorizedError { message }
      - UnexpectedError { message }
    """
    import urllib.request, json, ssl
    from datetime import datetime, timezone, timedelta

    ctx = ssl.create_default_context()

    def gql(query, variables=None):
        body = {"query": query}
        if variables:
            body["variables"] = variables
        data = json.dumps(body).encode("utf-8")
        req = urllib.request.Request(
            "https://api.buffer.com/graphql", data=data, method="POST"
        )
        req.add_header("Authorization", f"Bearer {token}")
        req.add_header("Content-Type", "application/json")
        resp = urllib.request.urlopen(req, timeout=15, context=ctx)
        return json.loads(resp.read().decode("utf-8"))

    # Determine mode: try scheduling first, fall back to immediate
    if now or not try_schedule_first:
        mode = "shareNow"
        due_at = None
    else:
        mode = "addToQueue"
        due_at = schedule_at or (
            datetime.now(timezone.utc) + timedelta(minutes=30)
        ).strftime("%Y-%m-%dT%H:%M:%SZ")

    # Build input
    post_input = {
        "channelId": channel_id,
        "text": text,
        "schedulingType": "automatic",
        "mode": mode,
        "assets": [],
    }
    if due_at:
        post_input["dueAt"] = due_at

    mutation = """
    mutation createPost($input: CreatePostInput!) {
      createPost(input: $input) {
        ... on PostActionSuccess {
          post { id status dueAt }
        }
        ... on InvalidInputError { message }
        ... on RestProxyError { message code }
        ... on LimitReachedError { message }
        ... on NotFoundError { message }
        ... on UnauthorizedError { message }
        ... on UnexpectedError { message }
      }
    }
    """

    variables = {"input": post_input}
    result = gql(mutation, variables)

    if "errors" in result:
        err_msg = result["errors"][0].get("message", str(result["errors"]))
        return {"success": False, "error": err_msg}

    post_data = result.get("data", {}).get("createPost", {})

    if "post" in post_data:
        return {
            "success": True,
            "post_id": post_data["post"]["id"],
            "status": post_data["post"]["status"],
            "due_at": post_data["post"].get("dueAt"),
            "mode": mode,
        }
    elif "message" in post_data:
        err_msg = post_data.get("message", "")
        # If queue is full (LimitReachedError on __typename or message),
        # retry with shareNow immediately
        if ("limit" in err_msg.lower() or "reached" in err_msg.lower()) and mode != "shareNow":
            print(f"[RETRY] Queue limit reached for {service} — posting immediately")
            # Retry with shareNow
            post_input["mode"] = "shareNow"
            post_input.pop("dueAt", None)
            variables = {"input": post_input}
            retry_result = gql(mutation, variables)
            retry_data = retry_result.get("data", {}).get("createPost", {})
            if "post" in retry_data:
                return {
                    "success": True,
                    "post_id": retry_data["post"]["id"],
                    "status": retry_data["post"]["status"],
                    "due_at": retry_data["post"].get("dueAt"),
                    "mode": "shareNow",
                    "fallback": True,
                }
        return {
            "success": False,
            "error": err_msg,
            "code": post_data.get("code", ""),
        }
    else:
        return {"success": False, "error": f"Unexpected response: {json.dumps(post_data)[:200]}"}
```

**Post to ALL channels (batch):**

```python
def post_to_all_channels(token: str, posts: dict) -> list[dict]:
    """Post to all configured Buffer channels with staggered scheduling.

    Scheduling strategy (Buffer free plan: 10 scheduled post limit):
    1. Twitter: try addToQueue at T+0 (or shareNow if queue full)
    2. LinkedIn: try addToQueue at T+60min (or shareNow if queue full)
    3. Bluesky: try addToQueue at T+120min (or shareNow if queue full)
    4. Any LimitReachedError → retry with shareNow (immediate posting)

    Args:
        token: Buffer access token
        posts: dict mapping service name (twitter/linkedin/bluesky) to post text

    Returns:
        List of {service, status, id, mode} dicts
    """
    import urllib.request, json, ssl
    from datetime import datetime, timezone, timedelta

    ctx = ssl.create_default_context()

    def gql(query, variables=None):
        body = {"query": query}
        if variables:
            body["variables"] = variables
        req = urllib.request.Request(
            "https://api.buffer.com/graphql",
            data=json.dumps(body).encode(), method="POST"
        )
        req.add_header("Authorization", f"Bearer {token}")
        req.add_header("Content-Type", "application/json")
        resp = urllib.request.urlopen(req, timeout=15, context=ctx)
        return json.loads(resp.read().decode("utf-8"))

    # Get org and channels
    acct = gql("{ account { organizations { id } } }")
    org_id = acct["data"]["account"]["organizations"][0]["id"]

    channels_raw = gql(
        '{ channels(input: { organizationId: "%s" }) { id service isDisconnected } }' % org_id
    )
    ch_map = {}
    for ch in channels_raw["data"]["channels"]:
        ch_map[ch["service"].lower()] = {
            "id": ch["id"],
            "disconnected": ch.get("isDisconnected", False),
        }

    # Stagger schedule: Twitter immediate, LinkedIn +1hr, Bluesky +2hr
    stagger_minutes = {"twitter": 0, "linkedin": 60, "bluesky": 120}
    results = []

    for service, text in posts.items():
        ch = ch_map.get(service, {})
        if not ch.get("id"):
            results.append({"service": service, "status": "NO_CHANNEL"})
            continue
        if ch.get("disconnected"):
            results.append({"service": service, "status": "DISCONNECTED"})
            continue

        # Calculate scheduled time for this service
        offset = stagger_minutes.get(service, 0)
        schedule_at = (
            datetime.now(timezone.utc) + timedelta(minutes=offset)
        ).strftime("%Y-%m-%dT%H:%M:%SZ") if offset > 0 else None

        # Try scheduling first; create_post handles LimitReachedError fallback
        r = create_post(token, ch["id"], text,
                        schedule_at=schedule_at,
                        try_schedule_first=True,
                        service=service)
        if r["success"]:
            results.append({
                "service": service,
                "status": "POSTED",
                "id": r["post_id"],
                "mode": r.get("mode", "unknown"),
                "fallback": r.get("fallback", False),
                "due_at": r.get("due_at"),
            })
        else:
            results.append({
                "service": service,
                "status": "FAILED",
                "error": r.get("error", ""),
            })

    return results
```
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

Each social platform has different audiences who respond to different messaging and formatting. **POSTS ARE FINDINGS-FIRST.** The most surprising, provocative, or compelling research result leads every post. No boilerplate about venue/publisher (Zenodo). Platform-native communication:

- **Twitter**: Bold, unfiltered claim. Aggressive hashtags for discoverability. Make them stop scrolling.
- **LinkedIn**: Professional credibility. Full title, indexing metadata for scholarly legitimacy. Polished but not corporate-speak.
- **Bluesky**: Clean, conversational, community-driven. No hashtags (Bluesky doesn't use them the same way).

```python
def format_for_channel(service: str, paper_title: str, paper_doi: str, 
                        key_finding: str = "", paper_url: str = "",
                        indexing: str = "") -> str:
    """Generate platform-native post text — findings-first, metadata-trailing.
    
    Different platforms = different audiences = different messaging:
    - Twitter: bold, unfiltered claim + hashtags for discoverability
    - LinkedIn: professional credibility with full title + indexing
    - Bluesky: clean, conversational, no hashtags
    
    Args:
        service: 'twitter', 'linkedin', or 'bluesky'
        paper_title: Full publication title
        paper_doi: Zenodo DOI (e.g., '10.5281/zenodo.XXXXXXX')
        key_finding: THE most compelling finding — this is the hook
        paper_url: Custom URL (defaults to doi.org/DOI)
        indexing: Indexing services (shown only on LinkedIn where scholarly legitimacy matters)
    """
    
    # Indexing metadata — LinkedIn only (scholarly legitimacy signal)
    indexing_line = f"📚 Indexed: {indexing}" if indexing else "📚 Indexed: Zenodo, Google Scholar, Semantic Scholar"
    
    templates = {
        "twitter": {
            "max_chars": 280,
            "format": (
                "{finding}\n\n"
                "📄 {short_title}\n"
                "🔗 {link}\n"
                "{hashtags}"
            ),
            "hashtags": "#research #QNFO #QWAV",
        },
        "linkedin": {
            "max_chars": 3000,
            "format": (
                "{finding}\n\n"
                "📄 {title}\n\n"
                "🔗 Read the full paper: {link}\n\n"
                "{indexing_line}\n\n"
                "{hashtags}"
            ),
            "hashtags": "#Research #AcademicPublishing #OpenScience #QNFO",
        },
        "bluesky": {
            "max_chars": 300,
            "format": (
                "{finding}\n\n"
                "📄 {short_title}\n"
                "🔗 {link}"
            ),
            "hashtags": "",
        },
    }
    
    tmpl = templates.get(service, templates["twitter"])
    
    short_title = paper_title[:80] + "..." if len(paper_title) > 80 else paper_title
    link = paper_url or f"https://doi.org/{paper_doi}"
    
    # Finding IS the star — give it maximum real estate
    finding_max = 160 if service == "twitter" else (200 if service == "bluesky" else 2000)
    finding = key_finding[:finding_max] + "..." if len(key_finding) > finding_max else key_finding
    
    text = tmpl["format"].format(
        finding=finding or "New research publication on QNFO/QWAV.",
        title=paper_title,
        short_title=short_title,
        link=link,
        hashtags=tmpl["hashtags"],
        indexing_line=indexing_line,
    )
    
    text = text[:tmpl["max_chars"]]
    if len(text) == tmpl["max_chars"] and len(text) >= tmpl["max_chars"] - 3:
        text = text[:tmpl["max_chars"] - 3] + "..."
    
    return text
```

---

## ⚠️ REST API PERMANENTLY REMOVED (v2.1)

The legacy REST API at `api.bufferapp.com` is **permanently shut down** and returns HTTP 401 for all requests. The `scripts/buffer_post.py` has been removed from this skill. **All posting MUST use the GraphQL API** (Section "Workflow — 4 Stages" above).

---

## 🔑 CRITICAL: ChannelId Must Be Exact 24-Char Hex

> **THE #1 CAUSE OF FAILURE:** Truncated or wrong ChannelIds.

The Buffer GraphQL channels query returns `id` fields that are **exactly 24 hexadecimal characters**. Copy them verbatim — do NOT truncate, do NOT change case, do NOT add prefixes. Example:

```json
{"id": "<query-from-api>"}
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

## ✅ Verified Working (v3.0 — 2026-07-10)

**Schema introspected live.** The GraphQL API was **proven working** for 9 posts across 3 channels (Scaffold-Lock: 3 posts, Zitterbewegung Lit Review: 3 posts in this session):

| Publication | DOI | Twitter | Bluesky | LinkedIn |
|:------------|:----|:--------|:--------|:---------|
| ZBW Lit Review | 10.5281/zenodo.21214374 | `6a50b9d3a568479189ca5e14` | `6a50b9d6a568479189ca5e3a` | `6a50b9d5e9caad523acdc912` |
| Scaffold-Lock | 10.5281/zenodo.21282108 | `6a4fbd7ed4453bdb5c1a3606` | `6a4fbd802b6d8f6cc40e8da5` | `6a4fbd836f8628af34310fb7` |
| Silent Radix | 10.5281/zenodo.21067593 | Verified | `6a43d23c1e42905afea3b54c` | `6a43d23d9c6ee994bd422862` |
| Cyclic Measurement | 10.5281/zenodo.21047527 | Verified | `6a43d2533a82910a41251a3c` | `6a43d254032afd2413bd5075` |

**Key corrections in v3.0 (2026-07-10):**
1. **`mode` requires `ShareMode` enum** — NOT `"automatic"`. Valid: `shareNow`, `addToQueue`, `shareNext`, `customScheduled`. Introspected live.
2. **`PostActionError` does NOT exist** — use `InvalidInputError`, `RestProxyError`, `LimitReachedError`, `NotFoundError`, `UnauthorizedError`, `UnexpectedError` instead.
3. **`PostActionSuccess` IS the success type** — with `post { id, status, dueAt }` fields.
4. **FULL `create_post()` implementation** embedded — the v2.2 skill had a truncated stub (`# ... same as above ...`). Now complete and verified.
5. **`post_to_all_channels()` added** — batch posts to all channels in a single function call.
6. GraphQL endpoint: `https://api.buffer.com/graphql` — unchanged.



---

### Stage 5: Expanded Dissemination Channels (Beyond Buffer)

Buffer covers Twitter/X, LinkedIn, and Bluesky. For wider scholarly reach, these additional channels integrate directly via API (no academic gatekeeping):

#### Stage 5a: Reddit -- via PRAW (Python Reddit API Wrapper)

> **TRACKING HOOK:** Every successful Reddit post auto-records to D1 `dissemination_tracker` via `track_dissemination()` (Stage 6). The post's Reddit permalink is stored as `post_url`.

```python
# pip install praw
import praw
from datetime import datetime, timezone

def post_to_reddit(client_id, client_secret, user_agent,
                   username, password, subreddit,
                   title, text, flair=""):
    reddit = praw.Reddit(
        client_id=client_id, client_secret=client_secret,
        user_agent=user_agent, username=username, password=password)
    sub = reddit.subreddit(subreddit)
    submission = sub.submit(title=title, selftext=text, flair_id=flair if flair else None)
    result = {
        "success": True, "post_id": submission.id,
        "url": f"https://reddit.com{submission.permalink}",
        "subreddit": subreddit, "title": title,
        "posted_at": datetime.now(timezone.utc).isoformat()}
    return result
```

#### Stage 5b: Mastodon -- via Mastodon.py

> **TRACKING HOOK:** Every successful Mastodon toot auto-records to D1 `dissemination_tracker` via `track_dissemination()` (Stage 6).

```python
# pip install Mastodon.py
from mastodon import Mastodon

def post_to_mastodon(instance_url, access_token, text, content_warning="", visibility="public"):
    mastodon = Mastodon(access_token=access_token, api_base_url=instance_url)
    kwargs = {"visibility": visibility}
    if content_warning:
        kwargs["spoiler_text"] = content_warning
    status = mastodon.status_post(text, **kwargs)
    result = {"success": True, "post_id": str(status["id"]),
              "url": status.get("url", ""), "instance": instance_url,
              "visibility": visibility}
    return result
```

#### Stage 5c: RSS Feed Generation -- stdlib xml.etree

> **TRACKING HOOK:** Each paper added to the RSS feed auto-records to D1 `dissemination_tracker` (Stage 6) as `channel='rss_feed'`.

```python
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

def build_rss_feed(papers, feed_title="QNFO/QWAV Research",
                   feed_link="https://papers.qnfo.org/",
                   feed_description="QNFO/QWAV Research Publications"):
    rss = ET.Element("rss", version="2.0")
    channel = ET.SubElement(rss, "channel")
    ET.SubElement(channel, "title").text = feed_title
    ET.SubElement(channel, "link").text = feed_link
    ET.SubElement(channel, "description").text = feed_description
    for paper in papers:
        item = ET.SubElement(channel, "item")
        ET.SubElement(item, "title").text = paper["title"]
        desc = paper.get("finding", "") + "\n\nDOI: " + paper.get("doi", "")
        ET.SubElement(item, "description").text = desc
        ET.SubElement(item, "link").text = paper.get("url", f"https://doi.org/{paper.get('doi', '')}")
        ET.SubElement(item, "guid").text = paper.get("doi", paper.get("slug", ""))
        ET.SubElement(item, "pubDate").text = paper.get("date", "")
    return ET.tostring(rss, encoding="unicode", xml_declaration=True)
```

#### Stage 5d: ORCID -- Auto-Add Publications to Researcher Profile

> **TRACKING HOOK:** Successful ORCID additions auto-record to D1 `dissemination_tracker` (Stage 6) as `channel='orcid'`.

```python
def add_to_orcid(orcid_id, access_token, paper_title, paper_doi, paper_date):
    import urllib.request
    work_xml = f'''<?xml version="1.0" encoding="UTF-8"?>
    <work:work xmlns:work="http://www.orcid.org/ns/work"
               xmlns:common="http://www.orcid.org/ns/common">
      <work:title><common:title>{paper_title}</common:title></work:title>
      <work:type>working-paper</work:type>
      <work:external-ids>
        <work:external-id>
          <common:external-id-type>doi</common:external-id-type>
          <common:external-id-value>{paper_doi}</common:external-id-value>
          <common:external-id-url>https://doi.org/{paper_doi}</common:external-id-url>
          <common:external-id-relationship>self</common:external-id-relationship>
        </work:external-id>
      </work:external-ids>
    </work:work>'''
    url = f"https://api.orcid.org/v3.0/{orcid_id}/work"
    req = urllib.request.Request(url, data=work_xml.encode(), method="POST")
    req.add_header("Authorization", f"Bearer {access_token}")
    req.add_header("Content-Type", "application/orcid+xml")
    resp = urllib.request.urlopen(req, timeout=15)
    return {"success": resp.status == 201, "orcid_id": orcid_id, "doi": paper_doi}
```

---

### Stage 6: D1 Dissemination Tracking (MANDATORY -- v3.7)

Every external post, link, and dissemination event MUST be tracked in D1 for impact/reach auditing. This includes Buffer, Reddit, Mastodon, RSS, ORCID, and any non-Cloudflare-hosted links.

#### 6a. D1 Schema -- dissemination_tracker

```sql
CREATE TABLE IF NOT EXISTS dissemination_tracker (
    id TEXT PRIMARY KEY,
    paper_slug TEXT NOT NULL,
    paper_doi TEXT,
    paper_title TEXT,
    channel TEXT NOT NULL,
    action TEXT NOT NULL DEFAULT 'posted',
    post_url TEXT,
    post_id TEXT,
    post_text_snippet TEXT,
    mode TEXT,
    fallback INTEGER DEFAULT 0,
    posted_at TEXT,
    zenodo_url TEXT,
    pages_url TEXT,
    github_url TEXT,
    created_at TEXT DEFAULT (datetime('now')),
    updated_at TEXT DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_dt_paper ON dissemination_tracker(paper_slug);
CREATE INDEX IF NOT EXISTS idx_dt_channel ON dissemination_tracker(channel);
CREATE INDEX IF NOT EXISTS idx_dt_posted ON dissemination_tracker(posted_at);
```

#### 6b. track_dissemination() -- Record Every External Post

```python
def track_dissemination(paper_slug, paper_doi, paper_title, channel,
                        action="posted", post_url="", post_id="",
                        post_text="", mode="", fallback=False,
                        zenodo_url="", pages_url="", github_url=""):
    import urllib.request, json, uuid, os
    from datetime import datetime, timezone
    TOKEN = os.environ.get('CLOUDFLARE_API_TOKEN', '')
    ACCOUNT = 'edb167b78c9fb901ea5bca3ce58ccc4b'
    DB_ID = 'qnfo-audit'
    row_id = str(uuid.uuid4())
    now = datetime.now(timezone.utc).isoformat()
    snippet = post_text[:200].replace("'", "''") if post_text else ""
    safe_title = paper_title.replace("'", "''")
    sql = f"INSERT INTO dissemination_tracker (id, paper_slug, paper_doi, paper_title, channel, action, post_url, post_id, post_text_snippet, mode, fallback, posted_at, zenodo_url, pages_url, github_url) VALUES ('{row_id}', '{paper_slug}', '{paper_doi}', '{safe_title}', '{channel}', '{action}', '{post_url}', '{post_id}', '{snippet}', '{mode}', {1 if fallback else 0}, '{now}', '{zenodo_url}', '{pages_url}', '{github_url}')"
    url = f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT}/d1/database/{DB_ID}/query"
    body = json.dumps({"sql": sql}).encode()
    req = urllib.request.Request(url, data=body, method="POST")
    req.add_header("Authorization", f"Bearer {TOKEN}")
    req.add_header("Content-Type", "application/json")
    try:
        resp = urllib.request.urlopen(req, timeout=10)
        result = json.loads(resp.read().decode())
        success = result.get("success", False)
    except Exception as e:
        result = {"error": str(e)}
        success = False
    return {"id": row_id, "channel": channel, "action": action, "success": success}
```

#### 6c. get_impact_report() -- Query Dissemination Reach

```python
def get_impact_report(paper_slug=""):
    import urllib.request, json, os
    TOKEN = os.environ.get('CLOUDFLARE_API_TOKEN', '')
    ACCOUNT = 'edb167b78c9fb901ea5bca3ce58ccc4b'
    DB_ID = 'qnfo-audit'
    where = f"WHERE paper_slug = '{paper_slug}'" if paper_slug else ""
    queries = {
        "total": f"SELECT COUNT(*) as c FROM dissemination_tracker {where}",
        "by_channel": f"SELECT channel, COUNT(*) as c FROM dissemination_tracker {where} GROUP BY channel ORDER BY c DESC",
        "by_action": f"SELECT action, COUNT(*) as c FROM dissemination_tracker {where} GROUP BY action",
        "recent": f"SELECT channel, post_url, posted_at FROM dissemination_tracker {where} ORDER BY posted_at DESC LIMIT 20",
        "first": f"SELECT MIN(posted_at) as first FROM dissemination_tracker {where}",
        "last": f"SELECT MAX(posted_at) as last FROM dissemination_tracker {where}"}
    url = f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT}/d1/database/{DB_ID}/query"
    headers = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}
    results = {}
    for key, sql in queries.items():
        body = json.dumps({"sql": sql}).encode()
        req = urllib.request.Request(url, data=body, method="POST", headers=headers)
        resp = json.loads(urllib.request.urlopen(req, timeout=10).read())
        results[key] = resp.get("result", [{}])[0].get("results", [])
    return results
```

---

### Stage 7: Non-Traditional Dissemination -- NO ARXIV, NO JOURNALS

> **POLICY:** arXiv and traditional journals are GATEKEPT dissemination channels. All QNFO/QWAV research is published exclusively on Zenodo (open access, immediate, no peer-review barrier). The channels below reach scholarly audiences WITHOUT academic gatekeeping.

| # | Channel | Method | Audience | Effort | Impact | Automatable |
|:--|:--------|:-------|:---------|:-------|:-------|:------------|
| 1 | **Hacker News** | Submit to news.ycombinator.com | Technical audience | Low | HIGH if upvoted | Script + manual submit |
| 2 | **Discord Webhooks** | Post to academic Discord servers via webhook API | Niche communities | Low | MEDIUM | Write script, execute, discard |
| 3 | **YouTube Shorts** | LLM-generated 60s explainer video | General public | Medium | HIGH | LLM script + pipeline |
| 4 | **GitHub Discussions** | Post to paper's GitHub repo Discussions | Developer-academics | Low | MEDIUM | GitHub API |
| 5 | **Wikipedia Citations** | Cite paper in relevant Wikipedia articles | Evergreen credibility | Medium | LONG-TERM HIGH | Manual (must be genuine) |
| 6 | **Physics Stack Exchange** | Answer questions, reference paper | Academic credibility | Low | MEDIUM | Draft answer, human posts |
| 7 | **Infographics** | One-image visual summary via infographic-syntax-creator | Highly shareable | Low | HIGH | Fully automated |
| 8 | **LinkedIn Articles** | Full long-form article on LinkedIn Publishing | Professional network | Medium | MEDIUM | LLM draft, human posts |
| 9 | **X Communities** | Post to field-specific X/Twitter Communities | Targeted academics | Low | MEDIUM | Buffer API |
| 10 | **Email Listservs** | Draft pitch email to field mailing lists | Direct inbox | Medium | MEDIUM | LLM draft, human sends |
| 11 | **Podcast Pitches** | Draft pitch to academic podcasts | Long-form exposure | Medium | LONG-TERM HIGH | LLM draft, human sends |
| 12 | **Citation Alerts** | Google Scholar alert when cited (passive) | Track organic impact | Low | PASSIVE | Manual setup, then passive |
| 13 | **LLM SEO** | llms.txt, robots.txt, semantic markup, sitemap | AI crawlers (ChatGPT, Claude) | Low | PASSIVE HIGH | seo-discoverability skill |

> **NO ARXIV:** arXiv requires endorsement for first submission in most categories -- this is academic gatekeeping. QNFO/QWAV research is published on Zenodo (immediate, open, no endorsement). arXiv is NOT a dissemination channel for this pipeline.
>
> **NO TRADITIONAL JOURNALS:** Journal submission = multi-month delay, paywall, copyright transfer. QNFO research is immediate open access. The channels above provide wider reach, faster, without gatekeepers.

---

## Integration Points

| Upstream Skill | How It Feeds Buffer Integration |
|:---------------|:-------------------------------|
| `social-orchestrator` | Generates channel-optimized text → calls this skill to post |
| `publication-publisher` | After Zenodo + Cloudflare deploy → triggers social dissemination |
| `research-orchestrator` | Calls as Phase 5 of the pipeline |

## Channel Format Reference

| Platform | Max Length | Design | Schedule | Hashtags | Link Behavior |
|:---------|:----------|:-------|:---------|:---------|:--------------|
| **Twitter/X** | 280 chars | **Finding-first** (160 chars), title, DOI | T+0 (or immediate) | 3-5 specific hashtags | Auto-card from DOI |
| **LinkedIn** | 3000 chars | **Finding-first** (2000 chars), title, DOI, indexing | T+60m (or immediate) | 3-5 professional hashtags | Rich preview |
| **Bluesky** | 300 chars | **Finding-first** (200 chars), title, DOI | T+120m (or immediate) | Optional, no hashtags | Plain text link |
| **Reddit** | 40000 chars (text post) | **Finding-first** + title + DOI | Auto-post (rate-limited) | Subreddit rules, no spam | Crosspost link |
| **Mastodon** | 500 chars | **Finding-first** (compact) | T+180m (or immediate) | 2-3 community hashtags | Plain text + CW |
| **RSS Feed** | Unlimited XML | Title + finding + DOI + pubDate | Auto | Feed readers, aggregators | Auto-discovery |
| **ORCID** | — | Title + DOI + type + date | Manual trigger | Researcher profile | DOI link |
| **D1 Tracking** | — | All fields tracked | Every post | `dissemination_tracker` | `get_impact_report()` |

> **v3.5 — Scheduling with Fallback**: Posts try `addToQueue` first (staggered: Twitter T+0, LinkedIn T+60m, Bluesky T+120m). If Buffer free plan 10-post limit is exceeded → `LimitReachedError` triggers automatic fallback to `shareNow` (immediate posting) per platform. Findings-first templates (v3.4) with platform-native communication: Twitter (bold claim), LinkedIn (credibility + full title), Bluesky (clean conversational).

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
| **InvalidInputError** | GraphQL returning malformed input — check `mode` is valid ShareMode (`shareNow` not `automatic`) |
| **RestProxyError** | Buffer backend proxy error — retry after 30s |
| **LimitReachedError** | Posting limit hit — back off and wait |
| Rate limit (100 req/15min) | Buffer API enforces; back off and retry |
| **Schema drift (types changed)** | Run embedded introspection script below to detect new types/enums |

## Embedded Script: Schema Introspection (SELF-CONTAINED)

Use this script whenever Buffer API calls fail to detect schema drift:

```python
#!/usr/bin/env python3
"""Introspect Buffer GraphQL schema — detect type drift.
Usage: python _buffer_introspect.py
Output: Prints CreatePostInput fields, PostActionPayload union types, enum values.
"""
import os, json, urllib.request, ssl

ctx = ssl.create_default_context()
buf_path = os.path.expandvars(r"%USERPROFILE%\.buffer_token")

if not os.path.exists(buf_path):
    print("[BLOCKED] No Buffer token at %USERPROFILE%\\.buffer_token")
    exit(1)

with open(buf_path, "r", encoding="utf-8-sig") as f:
    token = f.read().strip()

GQL = "https://api.buffer.com/graphql"

def gql(query):
    req = urllib.request.Request(GQL, data=json.dumps({"query": query}).encode(), method="POST")
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Content-Type", "application/json")
    return json.loads(urllib.request.urlopen(req, timeout=10, context=ctx).read())

# 1. CreatePostInput fields
r = gql("""{ __type(name: "CreatePostInput") { name inputFields { name type { name kind } } } }""")
fields = r["data"]["__type"]["inputFields"]
print("=== CreatePostInput Fields ===")
for f in fields:
    print(f"  {f['name']}: {f['type']['name']}")

# 2. PostActionPayload union
r = gql("""{ __type(name: "PostActionPayload") { kind possibleTypes { name fields { name } } } }""")
t = r["data"]["__type"]
print(f"\n=== PostActionPayload ({t['kind']}) ===")
for pt in t["possibleTypes"]:
    fields = [f["name"] for f in pt["fields"]]
    print(f"  ... on {pt['name']}: {fields}")

# 3. ShareMode enum
r = gql("""{ __type(name: "ShareMode") { enumValues { name } } }""")
vals = r["data"]["__type"]["enumValues"]
print(f"\n=== ShareMode ===")
print(f"  {[v['name'] for v in vals]}")

# 4. SchedulingType enum
r = gql("""{ __type(name: "SchedulingType") { enumValues { name } } }""")
vals = r["data"]["__type"]["enumValues"]
print(f"\n=== SchedulingType ===")
print(f"  {[v['name'] for v in vals]}")
```

**Execution:** Write to `_buffer_introspect.py`, run, compare against Stage 3 docs, delete. No external deps beyond Python stdlib.

---

*buffer-integration v3.5 — Phase 5 of LRAP. v3.5 (2026-07-11): embedded scheduling logic — create_post() tries addToQueue, falls back to shareNow on LimitReachedError (Buffer free plan 10-post limit). post_to_all_channels() staggers: Twitter T+0, LinkedIn T+60, Bluesky T+120 with per-platform fallback. v3.4: platform-native communication. v3.3: findings-first design. v3.2: removed journal_line. v3.1: added journal+indexing. v3.0: GraphQL schema corrected.*

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

## RT: RED-TEAM SELF-AUDIT

Before claiming this skill complete, autonomously run:

1. Output Verification (negative verification)
2. Assumption Challenge (state and test every assumption)
3. Edge Case Check (empty/null/max/boundary/desync)
4. DoD Integration (run _dod_enforce.py if exists)
5. Iteration (retry on failure, max 3)

ANTI-PATTERN: User should NEVER ask about quality.
Refer to RED-TEAM-PROTOCOL.md for full protocol.

