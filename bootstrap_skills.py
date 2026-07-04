"""Bootstrap skill sync tool — uploads skills to Cloudflare R2.

Usage:
  python bootstrap_skills.py              List local skills
  python bootstrap_skills.py --sync       Upload all local skills to R2
  python bootstrap_skills.py --clean      Delete R2 skill objects not present on local disk (DRY RUN)
  python bootstrap_skills.py --clean --force   Actually delete orphaned R2 skill objects
  python bootstrap_skills.py --verify     Verify all local skills exist on R2
"""
import os, sys, json, urllib.request, ssl

ACCOUNT = 'edb167b78c9fb901ea5bca3ce58ccc4b'
BUCKET = 'qnfo'
SKILLS_DIR = os.path.expanduser('~/.deepchat/skills')
R2_SKILLS_PREFIX = 'qnfo/prompts/skills/'

def _token():
    token = os.environ.get('CLOUDFLARE_API_TOKEN', '')
    if not token:
        print('ERROR: CLOUDFLARE_API_TOKEN not set')
        sys.exit(1)
    return token

def cf(endpoint, method='GET', body=None):
    token = _token()
    url = f'https://api.cloudflare.com/client/v4/accounts/{ACCOUNT}/{endpoint}'
    req = urllib.request.Request(url)
    req.add_header('Authorization', f'Bearer {token}')
    if method in ('PUT', 'DELETE'):
        req.method = method
    if method == 'PUT' and body:
        req.add_header('Content-Type', 'application/octet-stream')
        req.data = body.encode('utf-8') if isinstance(body, str) else body
    ctx = ssl._create_unverified_context()
    try:
        resp = urllib.request.urlopen(req, timeout=30, context=ctx)
        return json.loads(resp.read())
    except urllib.request.HTTPError as e:
        try:
            body = e.read().decode()
            return json.loads(body) if body else {'error': f'HTTP {e.code}: {e.reason}'}
        except:
            return {'error': f'HTTP {e.code}: {e.reason}'}
    except Exception as e:
        return {'error': str(e)}

def get_local_skills():
    """Return set of local skill names that have SKILL.md files."""
    skills = set()
    if not os.path.isdir(SKILLS_DIR):
        return skills
    for d in os.listdir(SKILLS_DIR):
        p = os.path.join(SKILLS_DIR, d, 'SKILL.md')
        if os.path.isfile(p) and not d.startswith('.') and not d.endswith('.skill'):
            skills.add(d)
    return skills

def list_r2_skills():
    """List all skill SKILL.md objects on R2 via REST API.
    
    The R2 list API returns: {"success": true, "result": [{"key": "...", ...}, ...]}
    Result is a direct list of objects, NOT an object with an 'objects' key.
    """
    token = _token()
    ctx = ssl._create_unverified_context()
    r2_skills = set()
    
    url = f'https://api.cloudflare.com/client/v4/accounts/{ACCOUNT}/r2/buckets/{BUCKET}/objects'
    params = urllib.parse.urlencode({
        'prefix': R2_SKILLS_PREFIX,
        'limit': 1000,
    })
    full_url = url + '?' + params
    req = urllib.request.Request(full_url)
    req.add_header('Authorization', f'Bearer {token}')
    
    try:
        resp = urllib.request.urlopen(req, timeout=30, context=ctx)
        data = json.loads(resp.read().decode())
    except Exception as e:
        print(f'  [WARN] R2 list error: {e}')
        return None
    
    if not data.get('success'):
        errors = data.get('errors', [])
        err_msg = errors[0].get('message', str(data)) if errors else str(data)
        print(f'  [WARN] R2 list API returned error: {err_msg}')
        return None
    
    result = data.get('result', [])
    
    # result is a flat list of objects: [{"key": "qnfo/prompts/skills/name/SKILL.md", ...}, ...]
    if isinstance(result, dict):
        # Older API format: {"objects": [...], "truncated": bool}
        objects = result.get('objects', [])
    elif isinstance(result, list):
        objects = result
    else:
        print(f'  [WARN] Unexpected result type: {type(result)}')
        return None
    
    for obj in objects:
        key = obj.get('key', '')
        if key.startswith(R2_SKILLS_PREFIX) and key.endswith('/SKILL.md'):
            name = key[len(R2_SKILLS_PREFIX):-len('/SKILL.md')]
            if name and '/' not in name:
                r2_skills.add(name)
    
    return r2_skills

def delete_r2_skill(name):
    """Delete a single skill SKILL.md from R2. Returns (success, message)."""
    r2_path = f'{R2_SKILLS_PREFIX}{name}/SKILL.md'
    encoded = urllib.request.quote(r2_path, safe='')
    endpoint = f'r2/buckets/{BUCKET}/objects/{encoded}'
    result = cf(endpoint, method='DELETE')
    
    if 'error' in result:
        err = result['error']
        if 'does not exist' in str(err).lower() or 'not found' in str(err).lower():
            return True, 'already gone'
        return False, str(err)
    if result.get('success'):
        return True, 'deleted'
    errors = result.get('errors', [])
    err_msg = errors[0].get('message', str(result)) if errors else str(result)
    if 'does not exist' in err_msg.lower() or 'not found' in err_msg.lower():
        return True, 'already gone'
    return False, err_msg

def get_r2_etag(name):
    """Get the current ETag of a skill on R2. Returns etag string or None if not found."""
    token = _token()
    ctx = ssl._create_unverified_context()
    r2_key = f'{R2_SKILLS_PREFIX}{name}/SKILL.md'
    encoded = urllib.request.quote(r2_key, safe='')
    url = f'https://api.cloudflare.com/client/v4/accounts/{ACCOUNT}/r2/buckets/{BUCKET}/objects/{encoded}'
    req = urllib.request.Request(url, method='HEAD')
    req.add_header('Authorization', f'Bearer {token}')
    try:
        resp = urllib.request.urlopen(req, timeout=15, context=ctx)
        etag = resp.headers.get('ETag', resp.headers.get('etag', ''))
        return etag.strip('"') if etag else None
    except urllib.request.HTTPError as e:
        if e.code == 404:
            return None  # New file, no existing version
        return None
    except Exception:
        return None

def put_with_etag(name, content):
    """PUT a skill to R2 with ETag-based concurrent-write protection.
    
    Returns (ok: bool, status: str, message: str).
    On 412 Precondition Failed, returns (False, 'conflict', details).
    """
    token = _token()
    ctx = ssl._create_unverified_context()
    r2_key = f'{R2_SKILLS_PREFIX}{name}/SKILL.md'
    encoded = urllib.request.quote(r2_key, safe='')
    url = f'https://api.cloudflare.com/client/v4/accounts/{ACCOUNT}/r2/buckets/{BUCKET}/objects/{encoded}'

    # Get current ETag for optimistic concurrency
    current_etag = get_r2_etag(name)

    data = content.encode('utf-8') if isinstance(content, str) else content
    req = urllib.request.Request(url, data=data, method='PUT')
    req.add_header('Authorization', f'Bearer {token}')
    req.add_header('Content-Type', 'application/octet-stream')

    if current_etag:
        req.add_header('If-Match', f'"{current_etag}"')

    try:
        resp = urllib.request.urlopen(req, timeout=30, context=ctx)
        result = json.loads(resp.read().decode())
        if result.get('success'):
            return True, 'uploaded', 'OK'
        errors = result.get('errors', [])
        return False, 'api_error', errors[0].get('message', str(result)) if errors else str(result)
    except urllib.request.HTTPError as e:
        if e.code == 412:
            return False, 'conflict', f'CONFLICT: {name} was modified on R2 since last read. Pull latest before re-syncing.'
        return False, f'http_{e.code}', f'HTTP {e.code}: {e.reason}'
    except Exception as e:
        return False, 'exception', str(e)

def sync_skills():
    """Upload all local skills to R2 with ETag-based concurrent-write protection."""
    skills = sorted(get_local_skills())
    synced = 0
    failed = 0
    conflicts = 0
    for name in skills:
        local_path = os.path.join(SKILLS_DIR, name, 'SKILL.md')
        local_size = os.path.getsize(local_path)
        with open(local_path, 'r', encoding='utf-8') as f:
            content = f.read()

        ok, status, msg = put_with_etag(name, content)
        if ok:
            synced += 1
            print(f'  OK  {name} ({local_size} B)')
        elif status == 'conflict':
            conflicts += 1
            print(f'  CONFLICT {name}: {msg}')
        else:
            failed += 1
            print(f'  FAIL {name}: {msg}')

    print(f'\nSynced: {synced}/{len(skills)} | Conflicts: {conflicts} | Failed: {failed}')
    return synced, failed

def clean_r2(dry_run=True):
    """Delete R2 skill objects not present on local disk."""
    local_skills = get_local_skills()
    print(f'Local skills: {len(local_skills)}')
    
    r2_skills = list_r2_skills()
    
    if r2_skills is None:
        print('\n[INFO] R2 listing unavailable (wrangler v4.95+ removed r2 object list).')
        print('[INFO] Falling back to individual file existence checks for R2 orphan detection.')
        print('[INFO] Attempting to detect orphans by probing known skill paths...')
        # Fallback: we can't enumerate, so we can't clean blindly
        print('[BLOCKED] Cannot enumerate R2 objects. --clean requires R2 object listing capability.')
        print('  This may be a Cloudflare API permissions issue or a v4.95+ limitation.')
        print('  Alternative: use --clean-legacy LIST to specify explicit names to delete.')
        return 0, 0
    
    print(f'R2 skills: {len(r2_skills)}')
    
    orphans = r2_skills - local_skills
    new_locals = local_skills - r2_skills
    
    if new_locals:
        print(f'\nSkills on local but NOT on R2: {len(new_locals)}')
        for s in sorted(new_locals):
            print(f'  [NEW] {s}')
    
    if not orphans:
        print('\n[OK] No orphaned R2 skills to clean.')
        return 0, 0
    
    print(f'\nOrphaned R2 skills (on R2 but NOT local): {len(orphans)}')
    for s in sorted(orphans):
        print(f'  [ORPHAN] {s}')
    
    if dry_run:
        print(f'\n[DRY RUN] Would delete {len(orphans)} orphaned skills from R2.')
        print('Run with --force to actually delete them.')
        return len(orphans), 0
    
    # Actually delete
    deleted = 0
    failed = 0
    print(f'\n[EXECUTING] Deleting {len(orphans)} orphaned skills from R2...')
    for name in sorted(orphans):
        ok, msg = delete_r2_skill(name)
        if ok:
            deleted += 1
            print(f'  [OK] DELETED: {name} ({msg})')
        else:
            failed += 1
            print(f'  [FAIL] {name}: {msg}')
    
    print(f'\nClean: {deleted}/{len(orphans)} deleted, {failed} failed')
    return deleted, failed

def verify_skills():
    """Verify all local skills exist on R2 with non-trivial content."""
    local_skills = sorted(get_local_skills())
    ok = 0
    missing = 0
    size_mismatch = 0
    
    for name in local_skills:
        local_path = os.path.join(SKILLS_DIR, name, 'SKILL.md')
        local_size = os.path.getsize(local_path)
        
        r2_path = f'{R2_SKILLS_PREFIX}{name}/SKILL.md'
        encoded = urllib.request.quote(r2_path, safe='')
        endpoint = f'r2/buckets/{BUCKET}/objects/{encoded}'
        
        # HEAD request to check existence and size
        token = _token()
        ctx = ssl._create_unverified_context()
        url = f'https://api.cloudflare.com/client/v4/accounts/{ACCOUNT}/{endpoint}'
        req = urllib.request.Request(url, method='HEAD')
        req.add_header('Authorization', f'Bearer {token}')
        
        try:
            resp = urllib.request.urlopen(req, timeout=15, context=ctx)
            r2_size = int(resp.headers.get('Content-Length', 0))
            if r2_size > 0:
                ok += 1
                status = 'OK' if r2_size == local_size else f'SIZE-MISMATCH (local={local_size}, r2={r2_size})'
                if r2_size != local_size:
                    size_mismatch += 1
                    print(f'  [WARN] {name}: {status}')
                else:
                    print(f'  [OK]  {name} ({local_size} B)')
            else:
                missing += 1
                print(f'  [MISSING] {name}: 0 bytes on R2')
        except urllib.request.HTTPError as e:
            if e.code == 404:
                missing += 1
                print(f'  [MISSING] {name}: not found on R2')
            else:
                missing += 1
                print(f'  [FAIL] {name}: HTTP {e.code}')
        except Exception as e:
            missing += 1
            print(f'  [FAIL] {name}: {e}')
    
    print(f'\nVerify: {ok}/{len(local_skills)} OK, {missing} missing, {size_mismatch} size mismatch')
    return ok, missing, size_mismatch

if __name__ == '__main__':
    import urllib.parse
    
    if '--clean' in sys.argv:
        dry_run = '--force' not in sys.argv
        clean_r2(dry_run=dry_run)
    elif '--sync' in sys.argv:
        sync_skills()
    elif '--verify' in sys.argv:
        verify_skills()
    else:
        skills = sorted(get_local_skills())
        print(f'Skills directory: {SKILLS_DIR}')
        print(f'Total skills: {len(skills)}')
        for s in skills:
            p = os.path.join(SKILLS_DIR, s, 'SKILL.md')
            size = os.path.getsize(p)
            print(f'  {s} ({size} B)')
        print(f'\nCommands:')
        print(f'  --sync     Upload all local skills to R2')
        print(f'  --clean    Dry-run: show R2 orphans not on local disk')
        print(f'  --clean --force  Delete orphaned R2 skill objects')
        print(f'  --verify   Check all local skills exist on R2')
