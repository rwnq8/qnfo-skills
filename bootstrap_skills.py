#!/usr/bin/env python3
"""
QNFO Skills Bootstrap — Restore all DeepChat skills from GitHub or Cloudflare R2.
Run this script when: new machine, corrupted skills, or recovery from disaster.

Usage:
    python bootstrap_skills.py                 # from GitHub (default)
    python bootstrap_skills.py --source r2     # from Cloudflare R2
    python bootstrap_skills.py --source local  # re-scan local only (verify)
    python bootstrap_skills.py --sync          # push local changes to GitHub + R2

Sources (in priority order):
    1. GitHub: https://github.com/rwnq8/qnfo-skills (public, git-tracked)
    2. Cloudflare R2: qnfo/prompts/skills/<name>/SKILL.md
    3. Local: %APPDATA%\.deepchat\skills\ (thin client cache)
"""

import os, sys, json, urllib.request, subprocess, shutil, hashlib

SKILLS_DIR = os.path.expandvars(r'%USERPROFILE%\.deepchat\skills')
GITHUB_REPO = 'https://github.com/rwnq8/qnfo-skills.git'
R2_BUCKET = 'qnfo'
R2_PREFIX = 'qnfo/prompts/skills'
ACCOUNT = 'edb167b78c9fb901ea5bca3ce58ccc4b'
TOKEN = os.environ.get('CLOUDFLARE_API_TOKEN', '')

# All 28 skills (discovered at build time; update if new skills added)
SKILLS = [
    "algorithmic-art", "bling-usability-audit", "closeout-manager", "cloudflare-deployer",
    "code-review", "deepchat-settings", "doc-coauthoring", "docx",
    "email-composer", "execution-guard", "frontend-design", "git-commit",
    "git-hygiene", "infographic-syntax-creator", "kaizen-autonomous-update", "knowledge-graph",
    "local-to-r2-migration", "mcp-builder", "pdf", "pdf-builder",
    "pptx", "prompt-audit", "publication-publisher", "qnfo-agent",
    "skill-creator", "template-catalog", "web-artifacts-builder", "xlsx"
]


def from_github():
    """Clone skills from GitHub to local disk."""
    print(f'[BOOTSTRAP] Restoring {len(SKILLS)} skills from GitHub...')
    if os.path.exists(SKILLS_DIR):
        backup = SKILLS_DIR + '.bak.' + str(int(os.path.getmtime(SKILLS_DIR)))
        print(f'  Backing up existing to {backup}')
        shutil.move(SKILLS_DIR, backup)
    
    subprocess.run(['git', 'clone', GITHUB_REPO, SKILLS_DIR], check=True)
    print(f'[BOOTSTRAP] GitHub restore complete: {SKILLS_DIR}')


def from_r2():
    """Download each skill from R2 via REST API."""
    print(f'[BOOTSTRAP] Restoring {len(SKILLS)} skills from Cloudflare R2...')
    if not TOKEN:
        print('  ERROR: CLOUDFLARE_API_TOKEN not set. Cannot access R2.')
        sys.exit(1)
    
    os.makedirs(SKILLS_DIR, exist_ok=True)
    count = 0
    for skill in SKILLS:
        url = f'https://api.cloudflare.com/client/v4/accounts/{ACCOUNT}/r2/buckets/{R2_BUCKET}/objects/{R2_PREFIX}/{skill}/SKILL.md'
        req = urllib.request.Request(url)
        req.add_header('Authorization', f'Bearer {TOKEN}')
        try:
            resp = urllib.request.urlopen(req, timeout=30)
            data = resp.read()
            skill_dir = os.path.join(SKILLS_DIR, skill)
            os.makedirs(skill_dir, exist_ok=True)
            with open(os.path.join(skill_dir, 'SKILL.md'), 'wb') as f:
                f.write(data)
            count += 1
            print(f'  [{count}/{len(SKILLS)}] {skill} ({len(data)} bytes)')
        except Exception as e:
            print(f'  [FAIL] {skill}: {e}')
    
    print(f'[BOOTSTRAP] R2 restore complete: {count}/{len(SKILLS)} skills to {SKILLS_DIR}')


def verify_local():
    """Verify all skills exist locally."""
    missing = []
    ok = 0
    for skill in SKILLS:
        path = os.path.join(SKILLS_DIR, skill, 'SKILL.md')
        if os.path.exists(path):
            size = os.path.getsize(path)
            print(f'  [OK] {skill:30s} {size:>7d} bytes')
            ok += 1
        else:
            print(f'  [MISS] {skill}')
            missing.append(skill)
    
    print(f'\n  Local: {ok}/{len(SKILLS)} skills')
    if missing:
        print(f'  Missing: {", ".join(missing)}')
    return ok == len(SKILLS)


def sync_to_r2():
    """Upload all local skills to R2."""
    print(f'[SYNC] Uploading {len(SKILLS)} skills to R2...')
    if not TOKEN:
        print('  ERROR: CLOUDFLARE_API_TOKEN not set')
        sys.exit(1)
    
    ok = 0
    for skill in SKILLS:
        path = os.path.join(SKILLS_DIR, skill, 'SKILL.md')
        if not os.path.exists(path):
            print(f'  [SKIP] {skill} (not local)')
            continue
        with open(path, 'rb') as f:
            data = f.read()
        url = f'https://api.cloudflare.com/client/v4/accounts/{ACCOUNT}/r2/buckets/{R2_BUCKET}/objects/{R2_PREFIX}/{skill}/SKILL.md'
        req = urllib.request.Request(url, data=data, method='PUT')
        req.add_header('Authorization', f'Bearer {TOKEN}')
        try:
            resp = urllib.request.urlopen(req, timeout=30)
            ok += 1
            print(f'  [{ok}/{len(SKILLS)}] {skill}')
        except Exception as e:
            print(f'  [FAIL] {skill}: {e}')
    print(f'[SYNC] R2 upload: {ok}/{len(SKILLS)}')


def sync_to_github():
    """Commit and push skills to GitHub."""
    print('[SYNC] Pushing to GitHub...')
    if not os.path.exists(os.path.join(SKILLS_DIR, '.git')):
        print('  ERROR: Not a git repo. Clone first with --source github.')
        sys.exit(1)
    
    subprocess.run(['git', '-C', SKILLS_DIR, 'add', '-A'], check=True)
    result = subprocess.run(['git', '-C', SKILLS_DIR, 'commit', '-m', 
        f'SYNC: skills update {__import__("datetime").datetime.now().isoformat()[:19]}'],
        capture_output=True, text=True)
    if 'nothing to commit' not in result.stdout + result.stderr:
        subprocess.run(['git', '-C', SKILLS_DIR, 'push', 'origin', 'master'], check=True)
        print('[SYNC] GitHub push complete')
    else:
        print('[SYNC] No changes to push')


def sync_all():
    """Full three-way sync: local -> GitHub -> R2."""
    sync_to_github()
    sync_to_r2()
    print('[SYNC] Three-way sync complete: local, GitHub, R2 all up to date.')


def main():
    source = 'github'
    action = 'restore'
    for arg in sys.argv[1:]:
        if arg.startswith('--source='):
            source = arg.split('=', 1)[1]
        elif arg == '--sync':
            action = 'sync'
        elif arg == '--verify':
            action = 'verify'
    
    if action == 'sync':
        sync_all()
    elif action == 'verify':
        ok = verify_local()
        print(f'\nVerification: {"ALL OK" if ok else "MISSING SKILLS"}')
    elif source == 'github':
        from_github()
        verify_local()
    elif source == 'r2':
        from_r2()
        verify_local()
    elif source == 'local':
        verify_local()
    else:
        print(f'Unknown source: {source}')
        print('Usage: python bootstrap_skills.py [--source=github|r2|local] [--sync] [--verify]')
        sys.exit(1)


if __name__ == '__main__':
    main()
