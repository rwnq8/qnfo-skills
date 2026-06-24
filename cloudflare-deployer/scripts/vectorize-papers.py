#!/usr/bin/env python3
"""
vectorize-papers.py — Index publications in Cloudflare Vectorize for semantic search.
Uses Cloudflare Workers AI (bge-small-en-v1.5, 768d) for embeddings.
v1.0 — 2026-05-31

Usage:
  python vectorize-papers.py --dir "G:/My Drive/QWAV/papers" --index qwav-research
  python vectorize-papers.py --file paper.html --index qwav-research --title "Paper Title"
  python vectorize-papers.py --rebuild-index --index qwav-research  # Rebuild full index
"""

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

# Cloudflare config
CF_ACCOUNT_ID = "edb167b78c9fb901ea5bca3ce58ccc4b"
CF_API_BASE = f"https://api.cloudflare.com/client/v4/accounts/{CF_ACCOUNT_ID}"


def get_api_token():
    """Load Cloudflare API token."""
    token = os.environ.get("CLOUDFLARE_API_TOKEN")
    if token:
        return token
    token_path = os.path.expanduser(r"~\.cloudflare\api-token")
    if os.path.exists(token_path):
        with open(token_path) as f:
            return f.read().strip()
    print("[ERROR] No CLOUDFLARE_API_TOKEN found.")
    print("Expected at: %USERPROFILE%\\.cloudflare\\api-token")
    sys.exit(1)


def extract_text_from_html(filepath):
    """Extract clean text from HTML file for embedding."""
    text = Path(filepath).read_text(encoding='utf-8', errors='replace')
    # Remove scripts and styles
    text = re.sub(r'<script[^>]*>.*?</script>', '', text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL | re.IGNORECASE)
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', ' ', text)
    # Collapse whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def extract_title_from_html(filepath):
    """Extract title from HTML file."""
    text = Path(filepath).read_text(encoding='utf-8', errors='replace')
    m = re.search(r'<title[^>]*>(.+?)</title>', text, re.IGNORECASE)
    if m:
        return m.group(1).strip()
    m = re.search(r'<h1[^>]*>(.+?)</h1>', text, re.IGNORECASE)
    if m:
        return m.group(1).strip()
    return Path(filepath).stem.replace('-', ' ').title()


def generate_embedding(text, token):
    """Generate embedding via Cloudflare Workers AI."""
    import urllib.request
    import urllib.error
    
    url = f"{CF_API_BASE}/ai/run/@cf/baai/bge-small-en-v1.5"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    # Truncate to ~500 tokens for bge-small
    text_truncated = text[:2000]
    
    body = json.dumps({"text": [text_truncated]}).encode('utf-8')
    req = urllib.request.Request(url, data=body, headers=headers, method="POST")
    
    try:
        with urllib.request.urlopen(req) as resp:
            result = json.loads(resp.read().decode())
            if result.get("success") and result.get("result", {}).get("data"):
                return result["result"]["data"][0]
            else:
                print(f"  [WARN] Embedding API returned: {result}")
                return None
    except urllib.error.HTTPError as e:
        print(f"  [WARN] Embedding API error {e.code}: {e.read().decode()[:200]}")
        return None


def upsert_to_vectorize(index_name, vectors, token):
    """Upsert vectors to Vectorize index."""
    import urllib.request
    import urllib.error
    
    url = f"{CF_API_BASE}/vectorize/v2/indexes/{index_name}/upsert"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    
    body = json.dumps(vectors).encode('utf-8')
    req = urllib.request.Request(url, data=body, headers=headers, method="POST")
    
    try:
        with urllib.request.urlopen(req) as resp:
            result = json.loads(resp.read().decode())
            if result.get("success"):
                print(f"  [OK] Upserted {len(vectors)} vectors to {index_name}")
                return True
            else:
                print(f"  [WARN] Upsert returned: {result}")
                return False
    except urllib.error.HTTPError as e:
        print(f"  [WARN] Upsert API error {e.code}: {e.read().decode()[:200]}")
        return False


def list_indexes(token):
    """List available Vectorize indexes."""
    import urllib.request
    import urllib.error
    
    url = f"{CF_API_BASE}/vectorize/v2/indexes"
    headers = {"Authorization": f"Bearer {token}"}
    req = urllib.request.Request(url, headers=headers)
    
    try:
        with urllib.request.urlopen(req) as resp:
            result = json.loads(resp.read().decode())
            if result.get("success"):
                return result.get("result", [])
    except urllib.error.HTTPError as e:
        print(f"[WARN] List indexes error {e.code}")
    return []


def discover_html_files(root_dir):
    """Recursively find HTML files."""
    html_files = []
    for f in Path(root_dir).rglob('*.html'):
        if any(part.startswith('.') or part.startswith('_') or part == 'node_modules'
               for part in f.parts):
            continue
        html_files.append(f)
    return sorted(html_files)


def paper_id_from_file(filepath):
    """Generate stable ID from file content."""
    text = filepath.read_text(encoding='utf-8', errors='replace')
    return hashlib.sha256(text.encode()).hexdigest()[:16]


def main():
    parser = argparse.ArgumentParser(description="Index papers in Cloudflare Vectorize")
    parser.add_argument('--dir', help='Directory containing HTML paper files')
    parser.add_argument('--file', help='Single HTML file to index')
    parser.add_argument('--title', help='Title for single-file indexing')
    parser.add_argument('--index', default='qwav-research', help='Vectorize index name')
    parser.add_argument('--rebuild-index', action='store_true', help='Rebuild full index')
    parser.add_argument('--dry-run', action='store_true', help='Preview without upserting')
    parser.add_argument('--list-indexes', action='store_true', help='List available Vectorize indexes')
    args = parser.parse_args()
    
    token = get_api_token()
    
    if args.list_indexes:
        indexes = list_indexes(token)
        print(f"\nAvailable Vectorize indexes ({len(indexes)}):")
        for idx in indexes:
            print(f"  - {idx.get('name', 'unknown')} ({idx.get('config', {}).get('dimensions', '?')}d)")
        return
    
    # Collect files to index
    if args.rebuild_index:
        print("[REBUILD] Rebuilding full index...")
        # Try QWAV papers directory
        papers_dir = Path(r"G:\My Drive\QWAV\papers")
        if not papers_dir.exists():
            print("[ERROR] Papers directory not found. Use --dir to specify.")
            sys.exit(1)
        html_files = discover_html_files(papers_dir)
    elif args.file:
        filepath = Path(args.file)
        if not filepath.exists():
            print(f"[ERROR] File not found: {args.file}")
            sys.exit(1)
        html_files = [filepath]
    elif args.dir:
        html_files = discover_html_files(Path(args.dir))
    else:
        print("[ERROR] Must specify --dir, --file, or --rebuild-index")
        sys.exit(1)
    
    if not html_files:
        print("[WARN] No HTML files found.")
        return
    
    print(f"\nVectorize — Indexing {len(html_files)} files to '{args.index}':")
    print(f"{'='*60}")
    
    vectors = []
    for i, filepath in enumerate(html_files):
        title = args.title if args.file else extract_title_from_html(filepath)
        text = extract_text_from_html(filepath)
        pid = paper_id_from_file(filepath)
        
        print(f"\n[{i+1}/{len(html_files)}] {title[:80]}")
        print(f"  File: {filepath.name} ({len(text):,} chars)")
        print(f"  ID:   {pid}")
        
        if args.dry_run:
            print(f"  [DRY RUN] Would embed and upsert")
            continue
        
        print(f"  Generating embedding...")
        embedding = generate_embedding(text, token)
        if embedding is None:
            print(f"  [SKIP] Embedding generation failed")
            continue
        
        vectors.append({
            "id": pid,
            "values": embedding,
            "metadata": {
                "title": title,
                "file": filepath.name,
                "source": str(filepath),
                "chars": len(text),
            }
        })
        
        # Batch upsert every 10 papers or on last
        if len(vectors) >= 10 or i == len(html_files) - 1:
            upsert_to_vectorize(args.index, vectors, token)
            vectors = []
            time.sleep(0.5)  # Rate limit avoidance
    
    print(f"\n[OK] Vectorize indexing complete for {len(html_files)} files.")


if __name__ == '__main__':
    main()
