---
name: local-to-r2-migration
description: Migrate local project files to Cloudflare R2 canonical storage — scan, classify, purge orphaned ephemeral files, upload project assets, update Discovery Index, and clean up local copies. Use when migrating local project clutter to R2 or when the user wants to enforce thin-client architecture.
version: "1.0"
---
> **INCLUDES AUTONOMOUS RED-TEAM SELF-AUDIT.** See RED-TEAM-PROTOCOL.md.


# Local-to-R2 Migration Skill (v1.0)

## 0. Purpose

**Problem:** The local filesystem has accumulated thousands of files that should live on Cloudflare R2. Agents pulled files from R2 and never cleaned them up. Orphaned `_*` ephemeral files, git objects, build artifacts, and entire project directories clutter `qnfo/projects/` and `qnfo/`.

**Solution:** This skill scans local directories, classifies every file, purges the junk (orphaned `_*` files, build artifacts, caches), uploads legitimate project files to R2, registers everything in the Discovery Index, and deletes the local copies after verified upload.

**Thin-Client Mandate:** The ONLY files that should persist locally are the DeepChat runtime (`qnfo/prompts/`). Everything else lives on R2. This skill is the enforcement mechanism.

## 1. When to Use

| Trigger | Action |
|:--------|:-------|
| User says "migrate local files to R2" | Full migration wizard |
| User says "clean up projects directory" | Scan + classify + ask before action |
| User says "enforce thin-client" | Full migration with auto-cleanup |
| Session closeout detects orphaned files | Trigger Phase 2 only (purge orphans) |
| New project needs R2 canonical storage | Phase 3 + 4 only (upload + index) |

## 2. Prerequisites

- `wrangler` v4.95+ authenticated: `npx wrangler whoami` must succeed
- Discovery Index accessible: `npx wrangler r2 object get qnfo/discovery/index.json --remote` must work
- Git available for import-surface management

## 3. File Classification System

Every file found in the scan is classified into one of these categories:

| Classification | Pattern | Action |
|:---------------|:--------|:-------|
| **ORPHANED-EPHEMERAL** | `_*` prefix (e.g., `_build.py`, `_data.json`) | DELETE immediately — these were ephemeral and abandoned |
| **GIT-OBJECTS** | Inside `.git/` directory | SKIP — managed by git |
| **WRANGLER-CACHE** | Inside `.wrangler/` directory | SKIP — managed by wrangler |
| **PYTHON-CACHE** | `__pycache__/` directory, `*.pyc` files | DELETE — regenerated on next Python run |
| **BUILD-ARTIFACT** | `*.o`, `*.rmeta`, `*.d`, `*.exe`, `*.dll`, `*.so` | DELETE — compiled objects, regenerated from source |
| **IMPORT-SURFACE** | Inside `qnfo/prompts/` | SKIP — this is the canonical local surface |
| **R2-MIGRATION-CANDIDATE** | Project files: `.md`, `.py`, `.json`, `.html`, `.css`, `.js`, `.tex`, `.pdf`, `.txt`, `.csv`, `.toml`, `.yaml`, `.lock`, `.rs`, `.ipynb`, images, data files | UPLOAD to R2 → verify → delete local |
| **UNKNOWN** | Everything else that doesn't match above | ASK USER — cannot determine destination |

## 4. Workflow — 5 Phases

### Phase 1: SCAN & CLASSIFY

**Goal:** Build a complete inventory of what's on disk and what should happen to each file.

```bash
# Step 1.1: Pull the migration scanner script (ephemeral)
npx wrangler r2 object get qnfo/tools/migration_scanner.py --remote --file=_migration_scanner.py

# If the script doesn't exist on R2 yet, create it inline (see §6 Embedded Scripts)

# Step 1.2: Run the scanner
python _migration_scanner.py --scan "qnfo/projects" --scan "qnfo/QWAV" --output _migration_report.json

# Step 1.3: Review the report
python _migration_scanner.py --report _migration_report.json
```

**Output:** `_migration_report.json` containing:
```json
{
  "scan_time": "2026-06-04T12:00:00Z",
  "targets": ["qnfo/projects", "qnfo/QWAV"],
  "totals": {
    "files_found": 11072,
    "total_size_mb": 0.0
  },
  "by_classification": {
    "ORPHANED-EPHEMERAL": {"count": 1698, "size_mb": 0.0, "action": "DELETE"},
    "GIT-OBJECTS": {"count": 0, "action": "SKIP"},
    "PYTHON-CACHE": {"count": 0, "action": "DELETE"},
    "BUILD-ARTIFACT": {"count": 0, "action": "DELETE"},
    "R2-MIGRATION-CANDIDATE": {"count": 0, "size_mb": 0.0, "action": "UPLOAD"},
    "UNKNOWN": {"count": 0, "action": "ASK"}
  },
  "r2_destinations": {
    "projects/<project>/<path>": {"local_path": "...", "r2_path": "qnfo/projects/<project>/<path>", "size_bytes": 0}
  },
  "orphaned_files": ["list of _* files to delete"],
  "purgeable_artifacts": ["list of .o/.rmeta/__pycache__ to delete"]
}
```

**Safety Gate:** Display the classification summary to the user. Confirm before proceeding to Phase 2.

### Phase 2: PURGE ORPHANED & JUNK

**Goal:** Delete all files that are definitively junk — orphaned ephemeral files, build artifacts, Python caches. These are safe to delete because they're either regenerable or were explicitly marked for deletion (`_` prefix).

```bash
# Step 2.1: Delete orphaned _* files
Get-ChildItem -Recurse -File -Path "qnfo/projects", "qnfo/QWAV" |
    Where-Object { $_.Name -match '^_' -and $_.DirectoryName -notmatch '\\prompts\\' } |
    ForEach-Object {
        Write-Output "PURGING: $($_.FullName)"
        Remove-Item $_.FullName -Force
    }

# Step 2.2: Delete Python caches
Get-ChildItem -Recurse -Directory -Path "qnfo/projects", "qnfo/QWAV" |
    Where-Object { $_.Name -eq '__pycache__' } |
    ForEach-Object {
        Write-Output "PURGING: $($_.FullName)"
        Remove-Item $_.FullName -Recurse -Force
    }

# Step 2.3: Delete build artifacts (.o, .rmeta, .d files)
Get-ChildItem -Recurse -File -Path "qnfo/projects", "qnfo/QWAV" |
    Where-Object { $_.Extension -in '.o', '.d' -or $_.Name -match '\.rmeta$' } |
    ForEach-Object {
        Write-Output "PURGING: $($_.FullName)"
        Remove-Item $_.FullName -Force
    }

# Step 2.4: Verify purge
$remaining = Get-ChildItem -Recurse -File -Path "qnfo/projects", "qnfo/QWAV" |
    Where-Object { $_.Name -match '^_' }
if ($remaining) {
    Write-Output "WARNING: ${$remaining.Count} orphaned files could not be deleted"
} else {
    Write-Output "Phase 2 complete: All orphaned files purged."
}
```

**HARD RULE:** Never use `-ErrorAction SilentlyContinue` — verify every deletion with `Test-Path`. After deletion, re-scan to confirm the files are gone.

### Phase 3: UPLOAD TO R2

**Goal:** Upload each R2-MIGRATION-CANDIDATE to its appropriate R2 path, with verification.

**Step 3.1: Determine R2 destination mapping**

For each project directory, the R2 path follows this convention:
- `qnfo/projects/<project>/<file>` → `qnfo/projects/<project>/<file>`
- `qnfo/<path>` → `qnfo/qwav/<path>` (skip `.git/` directory)

For standalone files at the top level of projects/:
- `qnfo/projects/<file>` → `qnfo/projects/_top/<file>`

**Step 3.2: Batch upload with verification**

```bash
# For each migration candidate, upload and verify:
npx wrangler r2 object put qnfo/projects/<project>/<path> --file="qnfo/projects/<project>/<path>" --remote

# Verify the upload:
npx wrangler r2 object get qnfo/projects/<project>/<path> --remote
# Must return the file content, NOT "The specified key does not exist"
```

**Step 3.3: Handle conflicts**

If the R2 path already exists:
1. Compare file sizes: `npx wrangler r2 object get qnfo/projects/<project>/<path> --remote | Measure-Object`
2. If identical → skip upload, proceed to delete local
3. If different → flag `[CONFLICT]`, keep both, ask user
4. If R2 version is newer → skip upload, delete local (R2 is canonical)

**Step 3.4: Generate upload manifest**

Create `_upload_manifest.json` tracking every uploaded file:
```json
{
  "uploaded": [
    {"local": "qnfo/projects/x/file.md", "r2": "qnfo/projects/x/file.md", "verified": true}
  ],
  "skipped_conflicts": [],
  "failed": []
}
```

### Phase 4: UPDATE DISCOVERY INDEX

**Goal:** Register all migrated project assets in the Discovery Index so they're discoverable.

**IMPORTANT:** Follow the Discovery Index Edit Protocol (§4.5 of META-PROMPT):
1. **Re-pull latest from R2** before editing
2. **Verify all referenced R2 paths** exist before upload
3. **Create timestamped backup** before upload
4. **Verify upload** by re-pulling and diffing

```bash
# Step 4.1: Pull current index
npx wrangler r2 object get qnfo/discovery/index.json --remote --file=_discovery_index.json

# Step 4.2: Update index entries (use Python for JSON manipulation)
python -c "
import json, sys
from datetime import datetime

with open('_discovery_index.json', 'r') as f:
    index = json.load(f)

with open('_upload_manifest.json', 'r') as f:
    manifest = json.load(f)

# For each uploaded project, add/update the projects section
if 'projects' not in index:
    index['projects'] = {}

# Extract unique project names from uploaded paths
projects_updated = set()
for entry in manifest['uploaded']:
    r2_path = entry['r2']
    if r2_path.startswith('qnfo/projects/'):
        project_name = r2_path.split('/')[2]
        if project_name == '_top':
            continue  # Skip the top-level catchall
        projects_updated.add(project_name)
        if project_name not in index['projects']:
            index['projects'][project_name] = {
                'name': project_name,
                'r2_path': f'qnfo/projects/{project_name}/',
                'migrated_from_local': True,
                'migration_date': datetime.utcnow().isoformat() + 'Z',
                'status': 'migrated'
            }

# Update metadata
index['metadata']['last_modified'] = datetime.utcnow().isoformat() + 'Z'
index['metadata']['last_action'] = 'local-to-r2-migration'
index['metadata']['projects_migrated'] = list(projects_updated)

# Also update the asset_registry if it exists
if 'asset_registry' not in index:
    index['asset_registry'] = {}
for project in projects_updated:
    key = f'projects/{project}'
    index['asset_registry'][key] = {
        'type': 'project',
        'r2_bucket': 'qnfo',
        'r2_prefix': f'projects/{project}/',
        'migrated': True
    }

with open('_discovery_index.json', 'w') as f:
    json.dump(index, f, indent=2)

print(f'Updated Discovery Index: {len(projects_updated)} projects added/updated')
for p in sorted(projects_updated):
    print(f'  + {p}')
" via script file

# Step 4.3: Create backup
$timestamp = Get-Date -Format 'yyyy-MM-ddTHHmmss'
npx wrangler r2 object put "qnfo/discovery/index-backup-${timestamp}.json" --file=_discovery_index.json --remote

# Step 4.4: Upload updated index
npx wrangler r2 object put qnfo/discovery/index.json --file=_discovery_index.json --remote

# Step 4.5: Verify upload
npx wrangler r2 object get qnfo/discovery/index.json --remote --file=_discovery_index_verify.json
# Diff: python -c "import json; a=json.load(open('_discovery_index.json')); b=json.load(open('_discovery_index_verify.json')); assert a==b, 'VERIFICATION FAILED'; print('Index upload verified')"
```

### Phase 5: CLEAN UP & REPORT

**Goal:** Delete local copies after verified upload, generate final report, clean up ephemeral tools.

```bash
# Step 5.1: Delete local copies (only for files verified in manifest)
python -c "
import json, os

with open('_upload_manifest.json', 'r') as f:
    manifest = json.load(f)

deleted = 0
failed = 0
for entry in manifest['uploaded']:
    if entry.get('verified'):
        local = entry['local']
        if os.path.exists(local):
            os.remove(local)
            deleted += 1
            print(f'DELETED: {local}')
        else:
            print(f'ALREADY-GONE: {local}')
    else:
        print(f'SKIPPED (unverified): {entry[\"local\"]}')
        failed += 1

# Also clean empty directories
for root, dirs, files in os.walk('qnfo/projects', topdown=False):
    if root != 'qnfo/projects' and not files and not dirs:
        try:
            os.rmdir(root)
            print(f'REMOVED-EMPTY-DIR: {root}')
        except:
            pass

print(f'\\nCleanup: {deleted} files deleted, {failed} skipped (unverified)')
" via script file

# Step 5.2: Verify cleanup
Write-Output "=== Post-migration file counts ==="
Write-Output "projects/: $((Get-ChildItem -Recurse -File -Path 'qnfo/projects' | Where-Object { $_.DirectoryName -notmatch '\\.wrangler|__pycache__|\\.git' }).Count) files remain"
Write-Output "QWAV/: $((Get-ChildItem -Recurse -File -Path 'qnfo/QWAV' | Where-Object { $_.DirectoryName -notmatch '\\.wrangler|__pycache__|\\.git' }).Count) files remain"

# Step 5.3: Clean up ephemeral tools
Remove-Item _migration_scanner.py -ErrorAction Stop
Remove-Item _migration_report.json -ErrorAction Stop
Remove-Item _upload_manifest.json -ErrorAction Stop
Remove-Item _discovery_index.json -ErrorAction Stop
Remove-Item _discovery_index_verify.json -ErrorAction Stop
# VERIFY:
$orphans = Get-ChildItem -File | Where-Object { $_.Name -match '^_' }
if ($orphans) { Write-Output "FAILED SELF-CLEANUP: $orphans" }
```

## 5. Safety Gates

| Gate | Location | Check |
|:-----|:---------|:------|
| **User confirmation before Phase 2** | After scan | Display classification summary. Wait for explicit "proceed" before deleting anything |
| **User confirmation before Phase 3** | After purge | Display upload plan (N files, M MB, destinations). Wait for "proceed" |
| **Upload verification** | Per-file in Phase 3 | Every upload verified with `r2 object get` before deleting local |
| **Conflict detection** | Phase 3 Step 3.3 | Never overwrite R2 without explicit user approval |
| **Index backup** | Phase 4 Step 4.3 | Timestamped backup created before index modification |
| **Post-deletion scan** | Phase 5 Step 5.2 | Verify file counts dropped after cleanup |
| **Self-cleanup** | Phase 5 Step 5.3 | All ephemeral `_*` files created by this skill are deleted |

## 6. Embedded Scripts

> **SELF-CONTAINED:** Before executing any script, verify it exists at its canonical path. If missing, the bootstrap protocol below recreates it.

| Script | Canonical Path | Purpose |
|:-------|:---------------|:--------|
| `migration_scanner.py` | `qnfo/prompts/tools\migration_scanner.py` | File classification, report generation |

### Bootstrap Protocol

```bash
Test-Path "qnfo/prompts/tools\migration_scanner.py"
# If MISSING: create from embedded source below
# After creation: upload to R2 for future use
# npx wrangler r2 object put qnfo/tools/migration_scanner.py --file="qnfo/prompts/tools\migration_scanner.py" --remote
```

### Embedded Source: `migration_scanner.py`

```python
#!/usr/bin/env python3
"""Migration Scanner — scan, classify, and report on local files for R2 migration.

Usage:
    python _migration_scanner.py --scan <dir> [--scan <dir2> ...] --output <report.json>
    python _migration_scanner.py --report <report.json>
"""

import os
import json
import argparse
from datetime import datetime, timezone


# Classification rules
SKIP_DIRS = {'.git', '.wrangler', '__pycache__', 'node_modules', 'target', '.venv', 'venv'}
SKIP_EXTENSIONS = {'.exe', '.dll', '.so', '.dylib', '.wasm', '.bin'}
ORPHAN_PATTERN = lambda name: name.startswith('_')
BUILD_EXTENSIONS = {'.o', '.d', '.rmeta', '.rlib', '.a', '.lib', '.class', '.pyc', '.pyo'}
SOURCE_EXTENSIONS = {
    '.md', '.py', '.json', '.html', '.css', '.js', '.jsx', '.ts', '.tsx',
    '.tex', '.pdf', '.txt', '.csv', '.toml', '.yaml', '.yml', '.lock',
    '.rs', '.ipynb', '.xml', '.svg', '.png', '.jpg', '.jpeg', '.gif',
    '.webp', '.ico', '.woff', '.woff2', '.ttf', '.eot', '.mp4', '.webm',
    '.mp3', '.wav', '.zip', '.tar', '.gz', '.bz2', '.xz', '.cfg', '.ini',
    '.env', '.sample', '.template', '.nix', '.sh', '.bash', '.ps1', '.bat',
    '.tf', '.hcl', '.proto', '.graphql', '.sql', '.r', '.jl', '.go', '.c',
    '.h', '.cpp', '.hpp', '.java', '.kt', '.swift', '.scala', '.rb', '.php',
    '.wasm', '.wat', '.css.map', '.js.map',
}
IMPORT_SURFACE_PREFIX = os.path.normpath('qnfo/prompts')


def classify_file(filepath, size_bytes):
    """Classify a single file."""
    name = os.path.basename(filepath)
    ext = os.path.splitext(name)[1].lower()
    dirpath = os.path.dirname(filepath)
    norm = os.path.normpath(filepath)

    # DeepChat runtime — never touch
    if norm.startswith(IMPORT_SURFACE_PREFIX):
        return 'IMPORT-SURFACE'

    # Check parent directories for skip patterns
    parts = norm.replace('\\', '/').split('/')
    for part in parts:
        if part in SKIP_DIRS:
            if part == '.git':
                return 'GIT-OBJECTS'
            elif part == '.wrangler':
                return 'WRANGLER-CACHE'
            elif part == '__pycache__':
                return 'PYTHON-CACHE'
            elif part in ('node_modules', 'target', '.venv', 'venv'):
                return 'BUILD-ARTIFACT'

    # Orphaned ephemeral files
    if ORPHAN_PATTERN(name):
        return 'ORPHANED-EPHEMERAL'

    # Build artifacts by extension
    if ext in BUILD_EXTENSIONS:
        return 'BUILD-ARTIFACT'

    # Binary/skip extensions
    if ext in SKIP_EXTENSIONS:
        return 'BUILD-ARTIFACT'

    # Known source files — migration candidates
    if ext in SOURCE_EXTENSIONS or ext == '':
        return 'R2-MIGRATION-CANDIDATE'

    # Unknown
    return 'UNKNOWN'


def determine_r2_path(filepath, classification):
    """Determine the R2 destination path for a file."""
    norm = os.path.normpath(filepath).replace('\\', '/')

    if norm.startswith('qnfo/projects/'):
        rel = norm[len('qnfo/projects/'):]
        return f'qnfo/projects/{rel}'
    elif norm.startswith('qnfo/'):
        rel = norm[len('qnfo/'):]
        return f'qnfo/qwav/{rel}'
    elif norm.startswith('qnfo/archive/'):
        rel = norm[len('qnfo/archive/'):]
        return f'qnfo/archive/{rel}'
    else:
        return f'qnfo/migrated/{os.path.basename(filepath)}'


def scan_directory(target_dir):
    """Scan a directory and classify all files."""
    results = {
        'ORPHANED-EPHEMERAL': [],
        'GIT-OBJECTS': [],
        'WRANGLER-CACHE': [],
        'PYTHON-CACHE': [],
        'BUILD-ARTIFACT': [],
        'IMPORT-SURFACE': [],
        'R2-MIGRATION-CANDIDATE': [],
        'UNKNOWN': [],
    }

    for root, dirs, files in os.walk(target_dir):
        for f in files:
            filepath = os.path.join(root, f)
            try:
                size = os.path.getsize(filepath)
            except OSError:
                size = 0

            classification = classify_file(filepath, size)
            entry = {
                'local_path': filepath.replace('\\', '/'),
                'size_bytes': size,
                'classification': classification,
            }

            if classification == 'R2-MIGRATION-CANDIDATE':
                entry['r2_path'] = determine_r2_path(filepath, classification)

            if classification in results:
                results[classification].append(entry)

    return results


def run_scan(targets, output_path):
    """Full scan of all targets."""
    combined = {
        'scan_time': datetime.now(timezone.utc).isoformat(),
        'targets': targets,
        'by_classification': {},
    }

    # Accumulate results
    for category in ['ORPHANED-EPHEMERAL', 'GIT-OBJECTS', 'WRANGLER-CACHE',
                     'PYTHON-CACHE', 'BUILD-ARTIFACT', 'IMPORT-SURFACE',
                     'R2-MIGRATION-CANDIDATE', 'UNKNOWN']:
        combined[category] = []

    total_size = 0
    total_files = 0

    for target in targets:
        if not os.path.isdir(target):
            print(f'WARNING: {target} does not exist, skipping')
            continue
        print(f'Scanning {target}...')
        results = scan_directory(target)
        for category, entries in results.items():
            combined[category].extend(entries)
            total_files += len(entries)
            for e in entries:
                total_size += e.get('size_bytes', 0)

    # Build summary
    combined['totals'] = {
        'files_found': total_files,
        'total_size_bytes': total_size,
        'total_size_mb': round(total_size / (1024 * 1024), 2),
    }

    combined['by_classification'] = {}
    for category in ['ORPHANED-EPHEMERAL', 'GIT-OBJECTS', 'WRANGLER-CACHE',
                     'PYTHON-CACHE', 'BUILD-ARTIFACT', 'IMPORT-SURFACE',
                     'R2-MIGRATION-CANDIDATE', 'UNKNOWN']:
        entries = combined[category]
        cat_size = sum(e.get('size_bytes', 0) for e in entries)
        combined['by_classification'][category] = {
            'count': len(entries),
            'size_mb': round(cat_size / (1024 * 1024), 2),
        }

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(combined, f, indent=2, ensure_ascii=False)

    print(f'\nScan complete: {total_files} files ({combined["totals"]["total_size_mb"]} MB)')
    print(f'Report written to {output_path}')
    return combined


def print_report(report_path):
    """Print a human-readable summary of the scan report."""
    with open(report_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    totals = data.get('totals', {})
    by_class = data.get('by_classification', {})

    print('=' * 60)
    print('MIGRATION SCAN REPORT')
    print('=' * 60)
    print(f'Scan time: {data.get("scan_time", "unknown")}')
    print(f'Targets: {", ".join(data.get("targets", []))}')
    print(f'Total files: {totals.get("files_found", 0)}')
    print(f'Total size: {totals.get("total_size_mb", 0)} MB')
    print()

    action_map = {
        'ORPHANED-EPHEMERAL': '🗑️  DELETE (abandoned ephemeral)',
        'GIT-OBJECTS': '⏭️  SKIP (git-managed)',
        'WRANGLER-CACHE': '⏭️  SKIP (wrangler-managed)',
        'PYTHON-CACHE': '🗑️  DELETE (regenerated)',
        'BUILD-ARTIFACT': '🗑️  DELETE (regenerated from source)',
        'IMPORT-SURFACE': '🔒 SKIP (DeepChat runtime — NEVER delete)',
        'R2-MIGRATION-CANDIDATE': '☁️  UPLOAD to R2',
        'UNKNOWN': '❓ ASK USER',
    }

    for cat in ['ORPHANED-EPHEMERAL', 'PYTHON-CACHE', 'BUILD-ARTIFACT',
                'R2-MIGRATION-CANDIDATE', 'GIT-OBJECTS', 'WRANGLER-CACHE',
                'IMPORT-SURFACE', 'UNKNOWN']:
        info = by_class.get(cat, {})
        count = info.get('count', 0)
        size = info.get('size_mb', 0)
        action = action_map.get(cat, '?')
        if count > 0:
            print(f'  {action:50s} | {count:>6d} files | {size:>8.2f} MB')

    print()
    print('=' * 60)

    # Show R2 destinations summary
    candidates = data.get('R2-MIGRATION-CANDIDATE', [])
    if candidates:
        # Group by R2 prefix
        prefixes = {}
        for c in candidates:
            r2 = c.get('r2_path', 'unknown')
            prefix = '/'.join(r2.split('/')[:3])  # qnfo/projects/<name>
            if prefix not in prefixes:
                prefixes[prefix] = {'count': 0, 'size': 0}
            prefixes[prefix]['count'] += 1
            prefixes[prefix]['size'] += c.get('size_bytes', 0)

        print('\nR2 UPLOAD DESTINATIONS:')
        for prefix, info in sorted(prefixes.items()):
            print(f'  {prefix}/  ({info["count"]} files, {info["size"] / (1024*1024):.2f} MB)')

    print()


def main():
    parser = argparse.ArgumentParser(description='Migration Scanner')
    parser.add_argument('--scan', action='append', dest='targets', help='Directory to scan')
    parser.add_argument('--output', help='Output JSON report path')
    parser.add_argument('--report', help='Print summary of an existing report')
    args = parser.parse_args()

    if args.report:
        print_report(args.report)
    elif args.targets and args.output:
        run_scan(args.targets, args.output)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
```

## 7. Integration with Knowledge Graph

After migration completes, query the Knowledge Graph for cross-project impact:

```bash
# Load the knowledge-graph skill
read('%APPDATA%\DeepChat\skills\knowledge-graph\SKILL.md')

# Query: what depends on migrated projects?
# The Knowledge Graph API can identify broken references and stale dependencies
```

## 8. Example Run

```
User: migrate all local files to R2

Agent:
  1. [Phase 1] Scans qnfo/projects/ and qnfo/
     → 11,072 files found (1,245 MB)
     → 1,698 orphaned _* files → DELETE
     → 890 build artifacts → DELETE
     → 4,285 migration candidates → UPLOAD to R2
     → 4,199 git/wrangler objects → SKIP

  2. [GATE] Displays summary, asks: "Proceed with purging 2,588 junk files?"

  User: yes

  3. [Phase 2] Purges 2,588 files. Verified.

  4. [GATE] Displays: "Upload 4,285 files (890 MB) to R2 across 32 project paths?"

  User: yes

  5. [Phase 3] Uploads to R2 with per-file verification.
     → 4,280 uploaded, 5 conflicts (identical), 0 failed

  6. [Phase 4] Updates Discovery Index with 32 project entries.
     → Backup created, index uploaded, verified

  7. [Phase 5] Deletes 4,285 local files. Cleans up ephemeral scripts.
     → 0 files remain in projects/ (outside .git/.wrangler)
     → 0 _* files in working directory

  Final state: Thin-client enforced. Everything canonical on R2.
```

## 9. Error Recovery

| Scenario | Recovery |
|:---------|:---------|
| `wrangler whoami` fails | Stop. Report: "wrangler not authenticated. Run `npx wrangler login` first." |
| R2 upload fails for a file | Log failure in manifest. Skip deletion. Retry batch at end. After 3 failures: mark `[FAILED]` and continue. |
| Discovery Index pull fails | Attempt rebuild from R2 enumeration. If that fails: report `[BLOCKED: Cannot access Discovery Index]` |
| User aborts mid-migration | Save state in `_migration_state.json`. Can resume with `--resume` flag. |
| Local file locked (in use) | Skip, log `[LOCKED]`, continue. Manual cleanup later. |
| R2 path collision with different content | Flag `[CONFLICT]`, preserve both, report to user for manual resolution. |

---

*Local-to-R2 Migration Skill v1.0 — Scan, classify, purge, upload, index, clean. Thin-client enforcement tool.*

## RT: RED-TEAM SELF-AUDIT

Before claiming this skill complete, autonomously run:

1. Output Verification (negative verification)
2. Assumption Challenge (state and test every assumption)
3. Edge Case Check (empty/null/max/boundary/desync)
4. DoD Integration (run _dod_enforce.py if exists)
5. Iteration (retry on failure, max 3)

ANTI-PATTERN: User should NEVER ask about quality.
Refer to RED-TEAM-PROTOCOL.md for full protocol.

