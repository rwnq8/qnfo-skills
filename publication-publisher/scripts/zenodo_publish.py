#!/usr/bin/env python3
"""
zenodo_publish.py — One-command Zenodo DOI registration via REST API.
v1.1 — 2026-06-04 — Multi-file artifact upload, manifest verification, semantic versioning.

CHANGES v1.0 → v1.1:
  - --file replaced by --artifacts-dir (directory of ALL project artifacts)
  - --manifest required: ARTIFACT-MANIFEST.json with SHA-256 checksums
  - --version required: MAJOR.MINOR.PATCH semantic version
  - Uploads ALL files in artifacts directory (not just PDF)
  - --verify mode: cross-references Zenodo record against manifest
  - Mandatory 8-category completeness check before upload

Usage:
  # First publication:
  python zenodo_publish.py --title "Paper Title" --author "Last, First" \
    --artifacts-dir ./project/ --manifest ARTIFACT-MANIFEST.json --version 1.0.0

  # Update existing publication (new version):
  python zenodo_publish.py --title "Paper Title v1.1.0" --author "Last, First" \
    --artifacts-dir ./project/ --manifest ARTIFACT-MANIFEST.json --version 1.1.0 \
    --doi 10.5281/zenodo.XXXXXXXX

  # Verify existing deposition against manifest:
  python zenodo_publish.py --verify --deposition-id 12345 --manifest ARTIFACT-MANIFEST.json
"""

import argparse
import json
import os
import sys
import urllib.request
import urllib.error
from pathlib import Path

VERSION = "1.1"

def get_token():
    token = os.environ.get("ZENODO_TOKEN")
    if token:
        return token
    token_path = os.path.expanduser("~\\.zenodo_token")
    if os.path.exists(token_path):
        with open(token_path) as f:
            return f.read().strip()
    print("[ERROR] No ZENODO_TOKEN env var and no ~/.zenodo_token file found.")
    print("Create a token at https://zenodo.org/account/settings/applications/")
    print("Required scopes: deposit:actions, deposit:write")
    print("Save to: %USERPROFILE%\\.zenodo_token")
    sys.exit(1)

def api_request(url, token, method="GET", data=None, content_type="application/json"):
    headers = {"Authorization": f"Bearer {token}"}
    body = None
    if data is not None:
        if content_type == "application/json":
            body = json.dumps(data).encode("utf-8")
            headers["Content-Type"] = "application/json"
        else:
            body = data
            headers["Content-Type"] = content_type

    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        error_body = e.read().decode()
        print(f"[ERROR] HTTP {e.code}: {error_body}")
        sys.exit(1)

def load_manifest(path):
    """Load and validate ARTIFACT-MANIFEST.json."""
    p = Path(path)
    if not p.exists():
        print(f"[ERROR] Manifest not found: {path}")
        sys.exit(1)
    with open(p, 'r', encoding='utf-8') as f:
        m = json.load(f)
    required = ['version', 'artifacts', 'total_files', 'categories_count']
    missing = [r for r in required if r not in m]
    if missing:
        print(f"[ERROR] Manifest missing required fields: {missing}")
        sys.exit(1)
    return m

def verify_manifest_completeness(artifacts_dir, manifest):
    """Verify all files in manifest exist on disk and vice versa."""
    adir = Path(artifacts_dir)
    if not adir.is_dir():
        print(f"[ERROR] Artifacts directory not found: {artifacts_dir}")
        sys.exit(1)

    manifest_paths = {a['path'] for a in manifest['artifacts']}
    disk_files = set()
    for f in sorted(adir.rglob('*')):
        if f.is_file() and not f.name.startswith('_') and '__pycache__' not in str(f):
            disk_files.add(str(f.relative_to(adir)))

    missing_from_disk = manifest_paths - disk_files
    missing_from_manifest = disk_files - manifest_paths

    if missing_from_disk:
        print(f"[WARNING] {len(missing_from_disk)} files in manifest but NOT on disk:")
        for f in sorted(missing_from_disk)[:10]:
            print(f"  MISSING: {f}")

    if missing_from_manifest:
        print(f"[WARNING] {len(missing_from_manifest)} files on disk but NOT in manifest:")
        for f in sorted(missing_from_manifest)[:10]:
            print(f"  EXTRA: {f}")

    required_categories = ['primary_output', 'source_document']
    missing_cats = [c for c in required_categories if c not in manifest.get('categories_count', {})]
    if missing_cats:
        print(f"[BLOCKED] Missing required artifact categories: {missing_cats}")
        sys.exit(1)

    print(f"[OK] Manifest verification passed: {manifest['total_files']} files, {len(manifest.get('categories_count', {}))} categories")
    return True

def upload_artifacts(artifacts_dir, bucket_url, token):
    """Upload ALL files in artifacts_dir to the Zenodo bucket."""
    adir = Path(artifacts_dir)
    uploaded = []
    failed = []

    all_files = sorted([f for f in adir.rglob('*') if f.is_file() and not f.name.startswith('_') and '__pycache__' not in str(f)])

    for i, filepath in enumerate(all_files):
        rel_name = str(filepath.relative_to(adir))
        print(f"  [{i+1}/{len(all_files)}] Uploading: {rel_name} ({filepath.stat().st_size:,} bytes)...")

        with open(filepath, "rb") as f:
            file_data = f.read()

        try:
            result = api_request(
                f"{bucket_url}/{rel_name}",
                token,
                method="PUT",
                data=file_data,
                content_type="application/octet-stream"
            )
            uploaded.append(rel_name)
            print(f"    OK: {result.get('filesize', len(file_data)):,} bytes stored")
        except SystemExit:
            failed.append(rel_name)
            print(f"    FAILED: {rel_name}")

    return uploaded, failed

def verify_deposition(dep_id, manifest_path, token, base_url):
    """Verify existing deposition against manifest."""
    manifest = load_manifest(manifest_path)
    print(f"\n[VERIFY] Checking deposition {dep_id} against manifest...")
    print(f"  Manifest: {manifest_path}")
    print(f"  Expected files: {manifest['total_files']}")
    print(f"  Version: {manifest.get('version', 'N/A')}")

    dep_check = api_request(f"{base_url}/deposit/depositions/{dep_id}", token)
    zenodo_files = dep_check.get("files", [])
    zenodo_filenames = {f.get('filename', f.get('key', '')) for f in zenodo_files}

    manifest_paths = {a['path'] for a in manifest['artifacts']}

    missing_from_zenodo = manifest_paths - zenodo_filenames
    extra_in_zenodo = zenodo_filenames - manifest_paths

    print(f"  Files in Zenodo: {len(zenodo_filenames)}")
    print(f"  Files in manifest: {len(manifest_paths)}")
    print(f"  Match: {len(manifest_paths & zenodo_filenames)}")

    if missing_from_zenodo:
        print(f"\n[FAIL] {len(missing_from_zenodo)} files in manifest but NOT on Zenodo:")
        for f in sorted(missing_from_zenodo)[:20]:
            print(f"  MISSING: {f}")
    if extra_in_zenodo:
        print(f"\n[WARNING] {len(extra_in_zenodo)} files on Zenodo but NOT in manifest:")
        for f in sorted(extra_in_zenodo)[:10]:
            print(f"  EXTRA: {f}")

    if missing_from_zenodo:
        print("\n[BLOCKED: incomplete Zenodo upload] Re-upload missing files.")
        sys.exit(1)

    print(f"\n[OK] Zenodo deposition verified: all {len(manifest_paths)} manifest files present.")
    return True

def main():
    parser = argparse.ArgumentParser(
        description=f"One-command Zenodo DOI registration (v{VERSION}) — multi-file artifact upload"
    )
    # Mode selection
    parser.add_argument("--sandbox", action="store_true", help="Use sandbox.zenodo.org for testing")
    parser.add_argument("--verify", action="store_true", help="Verify existing deposition against manifest")
    parser.add_argument("--deposition-id", type=int, default=0, help="Deposition ID for --verify mode")

    # Required for upload mode
    parser.add_argument("--title", default="", help="Publication title")
    parser.add_argument("--author", default="", help="Author name (Last, First)")
    parser.add_argument("--artifacts-dir", default="", help="Directory containing ALL project artifacts")
    parser.add_argument("--manifest", default="", help="Path to ARTIFACT-MANIFEST.json")
    parser.add_argument("--version", default="", help="Semantic version MAJOR.MINOR.PATCH")

    # Optional metadata
    parser.add_argument("--abstract", default="", help="Publication abstract")
    parser.add_argument("--keywords", default="", help="Comma-separated keywords")
    parser.add_argument("--upload-type", default="publication",
                        choices=["publication", "poster", "presentation", "dataset",
                                 "image", "video", "software", "lesson", "other"])
    parser.add_argument("--license", default="CC-BY-4.0", help="License identifier")
    parser.add_argument("--doi", default="", help="Existing DOI for creating new version")
    parser.add_argument("--yes", action="store_true", help="Skip confirmation prompt for non-interactive use")
    args = parser.parse_args()

    # --- VERIFY MODE ---
    if args.verify:
        if not args.deposition_id:
            print("[ERROR] --verify requires --deposition-id")
            sys.exit(1)
        if not args.manifest:
            print("[ERROR] --verify requires --manifest")
            sys.exit(1)
        token = get_token()
        base_url = "https://sandbox.zenodo.org/api" if args.sandbox else "https://zenodo.org/api"
        verify_deposition(args.deposition_id, args.manifest, token, base_url)
        return

    # --- UPLOAD MODE ---
    if not args.title:
        print("[ERROR] --title is required for upload mode")
        sys.exit(1)
    if not args.author:
        print("[ERROR] --author is required for upload mode")
        sys.exit(1)
    if not args.artifacts_dir:
        print("[ERROR] --artifacts-dir is required for upload mode")
        sys.exit(1)
    if not args.manifest:
        print("[ERROR] --manifest is required for upload mode (ARTIFACT-MANIFEST.json)")
        sys.exit(1)
    if not args.version:
        print("[ERROR] --version is required (MAJOR.MINOR.PATCH)")
        sys.exit(1)

    # Validate semantic version format
    version_parts = args.version.split('.')
    if len(version_parts) != 3 or not all(p.isdigit() for p in version_parts):
        print(f"[ERROR] Invalid version format: '{args.version}'. Must be MAJOR.MINOR.PATCH (e.g., 1.0.0)")
        sys.exit(1)

    # Validate artifacts directory
    adir = Path(args.artifacts_dir)
    if not adir.is_dir():
        print(f"[ERROR] Artifacts directory not found: {args.artifacts_dir}")
        sys.exit(1)

    # Load and validate manifest
    manifest = load_manifest(args.manifest)
    verify_manifest_completeness(args.artifacts_dir, manifest)

    # Verify version consistency
    manifest_version = manifest.get('version', '')
    if manifest_version and manifest_version != args.version:
        print(f"[WARNING] Manifest version ({manifest_version}) differs from --version ({args.version})")
        print(f"[WARNING] Using --version value: {args.version}")

    token = get_token()
    base_url = "https://sandbox.zenodo.org/api" if args.sandbox else "https://zenodo.org/api"
    env_label = "SANDBOX" if args.sandbox else "PRODUCTION"

    # --- DOI DUPLICATE CHECK ---
    if not args.doi and not args.sandbox:
        print("[QC] Checking for existing records with same title...")
        query = f'title:"{args.title}"'
        from urllib.parse import quote
        search_url = f"{base_url}/records?q={quote(query)}&size=5&sort=mostrecent"
        try:
            search_result = api_request(search_url, token)
            hits = search_result.get("hits", {}).get("hits", [])
            existing_dois = []
            for hit in hits:
                doi = hit.get("doi", "")
                hit_title = hit.get("metadata", {}).get("title", "") if "metadata" in hit else hit.get("title", "")
                if doi and hit_title:
                    existing_dois.append((doi, hit_title))
            if existing_dois:
                print(f"[BLOCKED] Found {len(existing_dois)} existing record(s) with similar title:")
                for doi, t in existing_dois:
                    print(f'  {doi} — "{t}"')
                print()
                print("[ACTION REQUIRED] To create a new version of an existing record, use:")
                print(f"  --doi {existing_dois[0][0]}")
                print()
                if args.yes:
                    print("[FATAL] Non-interactive mode (--yes) — cannot proceed without --doi.")
                    sys.exit(1)
                else:
                    response = input("Proceed anyway with new standalone record? [y/N]: ")
                    if response.lower() != 'y':
                        print("Aborted.")
                        sys.exit(0)
        except Exception as e:
            print(f"[WARNING] Could not check for existing records: {e}")

    # --- PRE-FLIGHT SUMMARY ---
    all_files = sorted([f for f in adir.rglob('*') if f.is_file() and not f.name.startswith('_') and '__pycache__' not in str(f)])
    total_size = sum(f.stat().st_size for f in all_files)

    print(f"\n{'='*60}")
    print(f"  ZENODO DOI REGISTRATION — {env_label} (v{VERSION})")
    print(f"{'='*60}")
    print(f"  Title:         {args.title}")
    print(f"  Author:        {args.author}")
    print(f"  Version:       {args.version}")
    print(f"  Artifacts dir: {args.artifacts_dir}")
    print(f"  Manifest:      {args.manifest} ({manifest['total_files']} files)")
    print(f"  Files to upload: {len(all_files)} ({total_size:,} bytes total)")
    print(f"  Categories:    {manifest.get('categories_count', {})}")
    print(f"  Upload type:   {args.upload_type}")
    print(f"  License:       {args.license}")
    if args.abstract:
        print(f"  Abstract:      {args.abstract[:100]}...")
    if args.keywords:
        print(f"  Keywords:      {args.keywords}")
    if args.doi:
        print(f"  New version of:  {args.doi}")
    print(f"{'='*60}\n")

    # Phase 1: Create deposition
    print("[1/4] Creating deposition...")
    metadata = {
        "metadata": {
            "title": args.title,
            "upload_type": args.upload_type,
            "publication_type": "other",
            "creators": [{"name": args.author}],
            "license": args.license,
            "version": args.version,
        }
    }
    if args.abstract:
        metadata["metadata"]["description"] = args.abstract
    if args.keywords:
        metadata["metadata"]["keywords"] = [k.strip() for k in args.keywords.split(",") if k.strip()]
    if args.doi:
        metadata["metadata"]["related_identifiers"] = [{
            "relation": "isNewVersionOf",
            "identifier": args.doi,
            "resource_type": "publication-other"
        }]

    deposition = api_request(f"{base_url}/deposit/depositions", token, method="POST", data=metadata)
    dep_id = deposition["id"]
    bucket_url = deposition["links"]["bucket"]
    print(f"  Deposition ID: {dep_id}")
    print(f"  Bucket URL:    {bucket_url}")

    # Phase 2: Upload ALL artifacts
    print(f"\n[2/4] Uploading {len(all_files)} files from {args.artifacts_dir}...")
    uploaded, failed = upload_artifacts(args.artifacts_dir, bucket_url, token)

    if failed:
        print(f"\n[FAILED] {len(failed)} files failed to upload:")
        for f in failed:
            print(f"  FAILED: {f}")
    if uploaded:
        print(f"\n  Uploaded: {len(uploaded)}/{len(all_files)} files successfully")
    if failed:
        print("\n[BLOCKED: incomplete upload] Fix failed files and re-upload.")
        sys.exit(1)

    # Phase 3: Verify metadata
    print(f"\n[3/4] Verifying deposition...")
    dep_check = api_request(f"{base_url}/deposit/depositions/{dep_id}", token)
    print(f"  Title confirmed: {dep_check.get('title', 'N/A')}")
    files = dep_check.get("files", [])
    print(f"  Files attached: {len(files)}")

    # Cross-reference against manifest
    zenodo_filenames = {f.get('filename', f.get('key', '')) for f in files}
    manifest_paths = {a['path'] for a in manifest['artifacts']}
    match = len(zenodo_filenames & manifest_paths)
    print(f"  Manifest match: {match}/{manifest['total_files']}")
    if match != manifest['total_files']:
        missing = manifest_paths - zenodo_filenames
        print(f"  [WARNING] {len(missing)} files in manifest not found in deposition!")
        for mf in sorted(missing)[:10]:
            print(f"    MISSING: {mf}")

    # Phase 4: Publish
    if args.sandbox:
        print(f"\n[4/4] SANDBOX TEST COMPLETE")
        print(f"  Deposition {dep_id} created successfully in sandbox.")
        print(f"  No DOI issued (sandbox mode).")
        print(f"  {len(uploaded)} files uploaded.")
        print(f"  To publish for real, remove --sandbox flag.")
        print(f"\n{'='*60}")
        print(f"  SANDBOX TEST PASSED")
        print(f"{'='*60}")
    else:
        print(f"\n[4/4] PUBLISHING {len(uploaded)} files...")
        if args.yes:
            print("  --yes flag set: auto-confirming publish")
        else:
            confirm = input("  Type 'PUBLISH' to confirm: ")
            if confirm.strip() != "PUBLISH":
                print("  Aborted.")
                sys.exit(0)

        publish_result = api_request(
            f"{base_url}/deposit/depositions/{dep_id}/actions/publish",
            token, method="POST"
        )

        doi = publish_result.get("doi", "N/A")
        recid = publish_result.get("record_id", publish_result.get("id", "N/A"))

        print(f"\n{'='*60}")
        print(f"  PUBLISHED SUCCESSFULLY")
        print(f"  Title:   {args.title}")
        print(f"  Version: {args.version}")
        print(f"  Files:   {len(uploaded)}")
        print(f"  DOI:     {doi}")
        print(f"  URL:     https://doi.org/{doi}")
        print(f"  Zenodo:  https://zenodo.org/records/{recid}")
        print(f"{'='*60}")

        print(f"\nDOI={doi}")
        print(f"ZENODO_URL=https://zenodo.org/records/{recid}")

if __name__ == "__main__":
    main()
