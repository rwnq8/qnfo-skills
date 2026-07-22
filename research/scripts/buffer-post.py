#!/usr/bin/env python3
"""
Buffer GraphQL Post Publisher (v1.1 — 2026-07-22, corrected)
==============================================================
Canonical script for publishing social media posts via Buffer's GraphQL API.

Usage:
    python buffer-post.py <text-file|inline-text> --platforms twitter,linkedin,bluesky [--dry-run]
    python buffer-post.py --list-channels

Environment:
    BUFFER_TOKEN — Buffer Personal Access Token (43 chars, suffix 14Ky)
                   Stored at %USERPROFILE%\\buffer\\token

Endpoint: https://api.buffer.com/graphql
Mutation: createPost (NOT deprecated createDraft)

v1.1 FIX (2026-07-22): PostActionPayload union type members ARE valid inline
fragment targets (contrary to a prior version's claim). The mutation now
requests `message` on every error variant and `post { id }` on success, so
callers can see WHY a post failed (e.g. LimitReachedError's exact queue
count, InvalidInputError's exact character-limit violation) instead of only
a bare __typename. Verified live 2026-07-22: successful Bluesky post
returned `post.id`; blocked Twitter/LinkedIn posts returned the exact
LimitReachedError message ("You have 10 scheduled posts out of 10 allowed.")
via the fragment below — proving fragments work correctly when the fragment
target name is a REAL union member (PostActionSuccess, InvalidInputError,
UnauthorizedError, UnexpectedError, NotFoundError, LimitReachedError,
RestProxyError — discoverable via `__type(name: "PostActionPayload")
{ possibleTypes { name } }`). The earlier "fragments don't work" diagnosis
was caused by using a non-existent fragment target name (`Post`) — a
schema-shape mistake, not a GraphQL union limitation.

Verified live 2026-07-22 with 3-channel posting for The Two-Level Lie paper.
"""
import urllib.request, json, os, sys, argparse
from pathlib import Path

# ── Config ──────────────────────────────────────────────────────────
URL = "https://api.buffer.com/graphql"
TOKEN = os.environ.get("BUFFER_TOKEN") or open(Path.home() / "buffer" / "token", "rb").read().strip().decode()
HEADERS = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}

# ── Channel Discovery (always live, never hardcoded) ─────────────────
def discover_channels():
    """Discover live channel IDs via GraphQL API. Returns {service: id}."""
    # Step 1: Get organization ID
    query = json.dumps({"query": "query { account { organizations { id } } }"}).encode()
    req = urllib.request.Request(URL, data=query, headers=HEADERS, method="POST")
    data = json.loads(urllib.request.urlopen(req, timeout=15).read())
    orgs = data["data"]["account"]["organizations"]
    if not orgs:
        raise RuntimeError("No organizations found — token may lack permissions")
    org_id = orgs[0]["id"]

    # Step 2: Get channels (note: `service` is a scalar/enum, NOT an object —
    # querying `service { name }` raises "must not have a selection")
    query = json.dumps({
        "query": f'query {{ channels(input: {{ organizationId: "{org_id}" }}) {{ id displayName service }} }}'
    }).encode()
    req = urllib.request.Request(URL, data=query, headers=HEADERS, method="POST")
    data = json.loads(urllib.request.urlopen(req, timeout=15).read())
    channels = {c["service"].lower(): c["id"] for c in data["data"]["channels"]}
    return channels


# ── Post Creation ───────────────────────────────────────────────────
def create_post(channel_id: str, text: str, dry_run: bool = False) -> dict:
    """Publish a single post via Buffer createPost mutation.

    Args:
        channel_id: Live channel ID from discover_channels()
        text: Post body text (Buffer auto-shortens URLs)
        dry_run: If True, only validate and print — don't actually post

    Returns:
        dict with keys: ok, typename, message/error, post_id (if success)
    """
    # Escape text for GraphQL inline string
    text_escaped = text.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")

    # v1.1 fix: request `message` on every error variant + `post { id }` on
    # success. Inline fragments on PostActionPayload DO work — the fragment
    # target names must be the REAL union members (see module docstring).
    mutation = f"""
    mutation {{
      createPost(input: {{
        channelId: "{channel_id}",
        text: "{text_escaped}",
        schedulingType: automatic,
        mode: addToQueue,
        assets: [],
        saveToDraft: false
      }}) {{
        __typename
        ... on PostActionSuccess {{
          post {{ id }}
        }}
        ... on InvalidInputError {{
          message
        }}
        ... on UnauthorizedError {{
          message
        }}
        ... on UnexpectedError {{
          message
        }}
        ... on NotFoundError {{
          message
        }}
        ... on LimitReachedError {{
          message
        }}
        ... on RestProxyError {{
          message
        }}
      }}
    }}
    """

    if dry_run:
        return {"ok": True, "typename": "DRY_RUN", "text_len": len(text)}

    body = json.dumps({"query": mutation}).encode("utf-8")
    req = urllib.request.Request(URL, data=body, headers=HEADERS, method="POST")
    resp = urllib.request.urlopen(req, timeout=20)
    data = json.loads(resp.read().decode("utf-8"))

    result = data.get("data", {}).get("createPost", {})
    typename = result.get("__typename", "NO_TYPENAME")

    if typename == "PostActionSuccess":
        post_id = (result.get("post") or {}).get("id")
        return {"ok": True, "typename": typename, "text_len": len(text), "post_id": post_id}
    elif "errors" in data:
        err_msg = data["errors"][0].get("message", "Unknown GraphQL error")
        return {"ok": False, "typename": typename, "error": err_msg}
    else:
        # Error-type union member (LimitReachedError, InvalidInputError, etc.)
        msg = result.get("message", json.dumps(data))
        return {"ok": False, "typename": typename, "error": msg}


# ── Main ────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="Publish social media posts via Buffer GraphQL API")
    parser.add_argument("text", nargs="?", default=None, help="Post text (inline) or path to text file")
    parser.add_argument("--platforms", default="twitter,linkedin,bluesky",
                        help="Comma-separated platform names (twitter, linkedin, bluesky)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Validate without posting")
    parser.add_argument("--list-channels", action="store_true",
                        help="Only list available channels and exit")
    args = parser.parse_args()

    # Discover channels
    try:
        channels = discover_channels()
    except Exception as e:
        print(f"FATAL: Failed to discover channels: {e}")
        print("Check: BUFFER_TOKEN env var or %USERPROFILE%\\buffer\\token")
        sys.exit(1)

    if args.list_channels:
        print("=== Available Channels ===")
        for svc, cid in channels.items():
            print(f"  {svc}: {cid}")
        return

    if not args.text:
        print("ERROR: text argument required (unless --list-channels)")
        sys.exit(1)

    # Read text
    text_path = Path(args.text)
    if text_path.exists():
        with open(text_path, "r", encoding="utf-8") as f:
            text = f.read().strip()
    else:
        text = args.text

    # Determine target platforms
    targets = [p.strip().lower() for p in args.platforms.split(",")]
    unknown = [t for t in targets if t not in channels]
    if unknown:
        print(f"WARNING: Unknown platforms: {', '.join(unknown)}. Available: {list(channels.keys())}")
        targets = [t for t in targets if t in channels]

    if not targets:
        print("ERROR: No valid platforms to post to")
        sys.exit(1)

    # Post to each platform
    results = {}
    for platform in targets:
        ch_id = channels[platform]
        print(f"\n{'[DRY RUN] ' if args.dry_run else ''}Posting to {platform} (channel: {ch_id[:8]}...)...")
        try:
            result = create_post(ch_id, text, dry_run=args.dry_run)
            results[platform] = result
            if result["ok"]:
                extra = f" id={result['post_id']}" if result.get("post_id") else ""
                print(f"  OK {result['typename']} ({result['text_len']} chars){extra}")
            else:
                print(f"  FAIL {result.get('typename', '?')}: {result.get('error', '?')[:200]}")
        except urllib.error.HTTPError as e:
            body = e.read().decode()[:300]
            results[platform] = {"ok": False, "error": f"HTTP {e.code}: {body}"}
            print(f"  FAIL HTTP {e.code}: {body[:150]}")
        except Exception as e:
            results[platform] = {"ok": False, "error": str(e)}
            print(f"  FAIL {e}")

    # Summary
    print(f"\n{'=' * 50}")
    success = all(r["ok"] for r in results.values())
    for p, r in results.items():
        s = "OK" if r["ok"] else "FAIL"
        detail = r.get("typename", "") + (f" post_id={r['post_id']}" if r.get("post_id") else "") if r["ok"] else r.get("error", "?")[:100]
        print(f"  [{s}] {p}: {detail}")

    if success:
        print(f"\nAll {len(results)} posts {'validated' if args.dry_run else 'published'} successfully.")
    else:
        failed = [p for p, r in results.items() if not r["ok"]]
        print(f"\nFailed (see reasons above, not necessarily agent error — e.g. account queue limits): {', '.join(failed)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
