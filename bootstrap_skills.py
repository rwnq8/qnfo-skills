"""Bootstrap skill sync tool — uploads skills to Cloudflare R2."""
import os, sys, json, urllib.request

ACCOUNT = 'edb167b78c9fb901ea5bca3ce58ccc4b'
BUCKET = 'qnfo'
SKILLS_DIR = os.path.expanduser('~/.deepchat/skills')

def cf(endpoint, method='GET', body=None):
    token = os.environ.get('CLOUDFLARE_API_TOKEN', '')
    if not token:
        print('ERROR: CLOUDFLARE_API_TOKEN not set')
        sys.exit(1)
    url = f'https://api.cloudflare.com/client/v4/accounts/{ACCOUNT}/{endpoint}'
    req = urllib.request.Request(url)
    req.add_header('Authorization', f'Bearer {token}')
    if method == 'PUT' and body:
        req.method = 'PUT'
        req.add_header('Content-Type', 'application/octet-stream')
        req.data = body.encode('utf-8') if isinstance(body, str) else body
    try:
        resp = urllib.request.urlopen(req, timeout=15)
        return json.loads(resp.read())
    except Exception as e:
        return {'error': str(e)}

def sync_skills():
    skills = []
    for d in sorted(os.listdir(SKILLS_DIR)):
        p = os.path.join(SKILLS_DIR, d, 'SKILL.md')
        if os.path.isfile(p) and not d.startswith('.') and not d.endswith('.skill'):
            skills.append(d)

    synced = 0
    failed = 0
    for name in skills:
        local_path = os.path.join(SKILLS_DIR, name, 'SKILL.md')
        local_size = os.path.getsize(local_path)
        with open(local_path, 'r', encoding='utf-8') as f:
            content = f.read()

        r2_path = f'r2/buckets/{BUCKET}/objects/qnfo/prompts/skills/{name}/SKILL.md'
        result = cf(r2_path, 'PUT', content)
        if 'result' in result:
            synced += 1
            print(f'  OK  {name} ({local_size} B)')
        else:
            failed += 1
            print(f'  FAIL {name}: {result.get("error", result)}')

    print(f'\nSynced: {synced}/{len(skills)} | Failed: {failed}')
    return synced, failed

if __name__ == '__main__':
    if '--sync' in sys.argv:
        sync_skills()
    else:
        skills = []
        for d in sorted(os.listdir(SKILLS_DIR)):
            p = os.path.join(SKILLS_DIR, d, 'SKILL.md')
            if os.path.isfile(p) and not d.startswith('.') and not d.endswith('.skill'):
                skills.append(d)
        print(f'Skills directory: {SKILLS_DIR}')
        print(f'Total skills: {len(skills)}')
        for s in skills[:5]:
            print(f'  {s}')
        if len(skills) > 5:
            print(f'  ... and {len(skills)-5} more')
        print('\nRun with --sync to upload all skills to R2')
