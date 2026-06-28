---
name: buffer-integration
description: Buffer API integration for social media posting on QNFO/QWAV channels. Create, schedule, and manage social media posts across Twitter/X, LinkedIn, and Bluesky via Buffer. Use when user says "post this to social media," "schedule a tweet," "publish to LinkedIn," or when Phase 5 of LRAP requires social dissemination of a new publication.
---
> **INCLUDES AUTONOMOUS RED-TEAM SELF-AUDIT.** See RED-TEAM-PROTOCOL.md.


# BUFFER INTEGRATION SKILL — v2.0

> **Phase 5 of LRAP.** Enables automated social media dissemination of QNFO/QWAV publications via Buffer **GraphQL API**.

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
python -c "
token = input('Buffer Access Token: ').strip()
with open(r'%USERPROFILE%\\.buffer_token', 'w', encoding='utf-8') as f:
    f.write(token)
print('[OK] Buffer token stored')
"
```

### Token Troubleshooting

If you see `UnicodeEncodeError: 'latin-1' codec can't encode character '\ufeff'`:
```bash
python -c "
import os
p = os.path.expandvars(r'%USERPROFILE%\\.buffer_token')
raw = open(p, 'rb').read()
if raw[:3] == b'\xef\xbb\xbf':
    open(p, 'wb').write(raw[3:])
    print('[OK] BOM removed from token file')
"
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
    """Create a Buffer post via GraphQL API.
    
    Args:
        token: Buffer access token
        channel_id: Buffer channel ID (from list_channels)
        text: Post text
        link_url: URL to attach
        schedule_at: ISO 8601 datetime for custom scheduling
        now: Post immediately (shareNow mode)
        service: Channel service name for metadata (twitter/linkedin/bluesky)
    """
    import urllib.request, json
    
    if now:
        mode = "shareNow"
    elif schedule_at:
        mode = "customScheduled"
    else:
        mode = "addToQueue"
    
    post_input = {
        "channelId": channel_id,
        "text": text,
        "schedulingType": "automatic",  # Required: only "automatic" works for all channels
        "mode": mode,
        "assets": [],
    }
    
    if schedule_at:
        post_input["dueAt"] = schedule_at
    
    if link_url and service:
        post_input["metadata"] = {
            service: {"linkAttachment": {"url": link_url}}
        }
    
    mutation = """
    mutation($input: CreatePostInput!) {
      createPost(input: $input) {
        ... on PostActionSuccess {
          post { id status text dueAt }
        }
        ... on InvalidInputError { message }
        ... on LimitReachedError { message }
      }
    }
    """
    
    body = json.dumps({"query": mutation, "variables": {"input": post_input}}).encode()
    req = urllib.request.Request(
        "https://api.buffer.com/1/graphql.json", data=body, method="POST"
    )
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Content-Type", "application/json")
    
    resp = urllib.request.urlopen(req, timeout=15)
    result = json.loads(resp.read().decode("utf-8"))
    post_result = result["data"]["createPost"]
    
    if "post" in post_result:
        return {"success": True, "post_id": post_result["post"]["id"],
                "status": post_result["post"]["status"],
                "due_at": post_result["post"].get("dueAt")}
    return {"success": False, "error": post_result.get("message", "Unknown")}
```

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

## Embedded Script

### `scripts/buffer_post.py`

```python
#!/usr/bin/env python3
"""
Buffer Integration — Create and schedule social media posts.
Usage: python buffer_post.py --title "Paper Title" --doi "10.5281/zenodo.XXXXX"

Environment:
  BUFFER_ACCESS_TOKEN (or stored at %USERPROFILE%\.buffer_token)
"""

import argparse
import json
import os
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone


def load_token() -> str:
    """Load Buffer token from environment or token file."""
    token = os.environ.get("BUFFER_ACCESS_TOKEN", "")
    if token:
        return token
    
    token_path = os.path.expandvars(r"%USERPROFILE%\.buffer_token")
    if os.path.exists(token_path):
        with open(token_path, "r") as f:
            return f.read().strip()
    
    raise FileNotFoundError(
        "[BLOCKED] Buffer token not found.\n"
        "Set BUFFER_ACCESS_TOKEN env var or store at %USERPROFILE%\\.buffer_token\n"
        "Get token from: https://bufferapp.com/developers/apps"
    )


def list_profiles(token: str) -> list[dict]:
    """List all Buffer social media profiles."""
    url = "https://api.bufferapp.com/1/profiles.json"
    req = urllib.request.Request(url)
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("User-Agent", "QNFO-BufferIntegration/1.0")

    response = urllib.request.urlopen(req, timeout=15)
    profiles = json.loads(response.read().decode("utf-8"))

    return [
        {
            "id": p["id"],
            "service": p["service"],
            "name": p.get("formatted_username", p["service"]),
            "timezone": p.get("timezone", "UTC"),
        }
        for p in profiles
    ]


def create_update(token: str, profile_id: str, text: str, 
                  link_url: str = None, schedule_at: str = None, 
                  now: bool = False) -> dict:
    """Create a Buffer post/update."""
    params = {
        "profile_ids[]": profile_id,
        "text": text,
    }
    
    if link_url:
        params["media[link]"] = link_url
    
    if now:
        params["now"] = "true"
    elif schedule_at:
        params["scheduled_at"] = schedule_at
    else:
        # Default: notification mode (manual approval)
        params["schedulingType"] = "notification"
    
    data = urllib.parse.urlencode(params).encode("utf-8")
    
    url = "https://api.bufferapp.com/1/updates/create.json"
    req = urllib.request.Request(url, data=data, method="POST")
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Content-Type", "application/x-www-form-urlencoded")
    req.add_header("User-Agent", "QNFO-BufferIntegration/1.0")

    response = urllib.request.urlopen(req, timeout=15)
    result = json.loads(response.read().decode("utf-8"))
    
    success = result.get("success", False)
    return {
        "success": success,
        "post_id": result.get("buffer_count") or result.get("id", ""),
        "error": result.get("message", "") if not success else "",
    }


def format_for_channel(service: str, paper_title: str, paper_doi: str = "",
                       key_finding: str = "", paper_url: str = "",
                       custom_text: str = "") -> str:
    """Generate channel-optimized post text."""
    if custom_text:
        return custom_text
    
    templates = {
        "twitter": (
            "🚀 New research: {title}\n"
            "Key finding: {finding}\n"
            "📄 Full paper: {link}"
        ),
        "linkedin": (
            "📄 New Research Publication: {title}\n\n"
            "{finding}\n\n"
            "Read the full paper: {link}"
        ),
        "bluesky": (
            "📄 New QNFO/QWAV research: {title}\n\n"
            "{finding}\n\n"
            "Read: {link}"
        ),
    }
    
    tmpl = templates.get(service, templates["twitter"])
    short_title = paper_title[:100] + "..." if len(paper_title) > 100 else paper_title
    link = paper_url or (f"https://doi.org/{paper_doi}" if paper_doi else "[link pending]")
    finding = key_finding or "Published on QNFO/QWAV via Zenodo."
    
    return tmpl.format(title=short_title, finding=finding, link=link)


def stagger_schedule(base_time: datetime, channel_index: int) -> str:
    """Stagger posts by 2-4 hours between channels to avoid bot-like behavior."""
    stagger_hours = 2 + channel_index * 2  # 2h, 4h, 6h gaps
    scheduled = base_time + timedelta(hours=stagger_hours)
    return scheduled.isoformat()


def main():
    parser = argparse.ArgumentParser(description="Create and schedule Buffer social media posts")
    parser.add_argument("--title", "-t", required=True, help="Publication title")
    parser.add_argument("--doi", "-d", default="", help="Zenodo DOI")
    parser.add_argument("--url", "-u", default="", help="Publication page URL")
    parser.add_argument("--finding", "-f", default="", help="Key finding (one sentence)")
    parser.add_argument("--text", default="", help="Custom text (overrides auto-format)")
    parser.add_argument("--channels", default="twitter,linkedin,bluesky",
                        help="Comma-separated channels to post to")
    parser.add_argument("--now", action="store_true", help="Post immediately (no scheduling)")
    parser.add_argument("--schedule-for", default="",
                        help="Schedule for specific ISO datetime")
    parser.add_argument("--list", action="store_true", help="List profiles only, don't post")
    parser.add_argument("--dry-run", action="store_true", help="Preview posts without creating")
    args = parser.parse_args()

    token = load_token()
    profiles = list_profiles(token)
    
    if args.list:
        print(f"Buffer Profiles ({len(profiles)}):")
        for p in profiles:
            print(f"  [{p['service']}] {p['name']} (ID: {p['id']})")
        return 0

    # Find profiles for requested channels
    channels = [c.strip().lower() for c in args.channels.split(",")]
    target_profiles = [p for p in profiles if p["service"] in channels]
    
    if not target_profiles:
        available = [p["service"] for p in profiles]
        print(f"[BLOCKED] No profiles found for channels: {channels}")
        print(f"Available services: {available}")
        return 1

    # Determine schedule time
    if args.now:
        schedule_at = None
        now_mode = True
    elif args.schedule_for:
        schedule_at = args.schedule_for
        now_mode = False
    else:
        schedule_at = stagger_schedule(datetime.now(timezone.utc), 0)
        now_mode = False

    results = []
    for i, profile in enumerate(target_profiles):
        text = format_for_channel(
            service=profile["service"],
            paper_title=args.title,
            paper_doi=args.doi,
            paper_url=args.url,
            key_finding=args.finding,
            custom_text=args.text,
        )
        
        channel_schedule = stagger_schedule(
            datetime.now(timezone.utc), i
        ) if not args.now and not args.schedule_for else (args.schedule_for or None)
        
        if args.dry_run:
            print(f"\n[Dry Run] {profile['service']} ({profile['name']}):")
            print(f"  Text: {text[:100]}...")
            print(f"  Schedule: {channel_schedule or 'now'}")
            continue
        
        result = create_update(
            token=token,
            profile_id=profile["id"],
            text=text,
            link_url=args.url or f"https://doi.org/{args.doi}" if args.doi else None,
            schedule_at=channel_schedule,
            now=now_mode,
        )
        
        status = "✅ Created" if result["success"] else f"❌ Failed: {result['error']}"
        results.append({
            "channel": profile["service"],
            "profile": profile["name"],
            "status": status,
            "post_id": result.get("post_id", ""),
            "scheduled_at": channel_schedule,
        })
        print(f"  [{profile['service']}] {status} (ID: {result.get('post_id', 'N/A')})")

    # Summary
    successes = sum(1 for r in results if "✅" in r["status"])
    print(f"\n[SUMMARY] {successes}/{len(results)} posts created")
    
    if not args.now and not args.dry_run:
        print(f"[SCHEDULED] First post at: {results[0]['scheduled_at'] if results else 'N/A'}")

    return 0 if successes == len(results) else 1


if __name__ == "__main__":
    sys.exit(main())
```

### Dependencies
- Python 3.8+ (standard library only)
- Buffer Access Token (free tier supports 3 social channels)

### Usage

```bash
# Post a new publication to all channels
python buffer_post.py --title "Ultrametric Emergence in Quantum Cognition" \
  --doi "10.5281/zenodo.XXXXX" \
  --finding "p-Adic ultrametric hierarchies provide a formal framework for emergent cognitive structures in quantum decision theory."

# Post to Twitter only, immediately
python buffer_post.py --title "..." --finding "..." --channels twitter --now

# Preview posts without creating them
python buffer_post.py --title "..." --finding "..." --dry-run

# List configured Buffer profiles
python buffer_post.py --list

# Schedule for a specific time
python buffer_post.py --title "..." --finding "..." --schedule-for "2026-06-25T09:00:00Z"
```

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

*buffer-integration v2.0 — Phase 5 of LRAP. Buffer GraphQL API integration for automated social media dissemination.*

## RT: RED-TEAM SELF-AUDIT

Before claiming this skill complete, autonomously run:

1. Output Verification (negative verification)
2. Assumption Challenge (state and test every assumption)
3. Edge Case Check (empty/null/max/boundary/desync)
4. DoD Integration (run _dod_enforce.py if exists)
5. Iteration (retry on failure, max 3)

ANTI-PATTERN: User should NEVER ask about quality.
Refer to RED-TEAM-PROTOCOL.md for full protocol.

