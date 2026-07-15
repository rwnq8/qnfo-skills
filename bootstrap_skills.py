#!/usr/bin/env python3
"""
bootstrap_skills.py — Skills Sync Tool v2.0

Syncs DeepChat skills between local disk, GitHub, and Cloudflare R2.
Supports: --sync, --status, --validate, --health, --dry-run

Canonical locations:
  R2:  qnfo/tools/bootstrap_skills.py
  GitHub: rwnq8/qnfo-skills/blob/master/bootstrap_skills.py
  Local: %USERPROFILE%\\.deepchat\\skills\\bootstrap_skills.py
"""

import os, sys, json, argparse, urllib.request, hashlib, re
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple

SKILLS_DIR = os.path.expandvars(r'%USERPROFILE%\\.deepchat\\skills')
R2_ACCOUNT = 'edb167b78c9fb901ea5bca3ce58ccc4b'
R2_BUCKET = 'qnfo'
R2_PREFIX = 'qnfo/prompts/skills'
D1_DB = 'qnfo-audit'

def get_token() -> str:
    token = os.environ.get('CLOUDFLARE_API_TOKEN', '')
    if not token:
        secrets_path = os.path.expandvars(r'%USERPROFILE%\\.cloudflare\\api-token')
        if os.path.exists(secrets_path):
            with open(secrets_path, 'r') as f:
                token = f.read().strip()
    return token

def r2_put(key: str, data: bytes, token: str) -> bool:
    url = f'https://api.cloudflare.com/client/v4/accounts/{R2_ACCOUNT}/r2/buckets/{R2_BUCKET}/objects/{key}'
    req = urllib.request.Request(url, data=data, method='PUT')
    req.add_header('Authorization', f'Bearer {token}')
    req.add_header('Content-Type', 'application/octet-stream')
    try:
        urllib.request.urlopen(req, timeout=15)
        return True
    except Exception as e:
        print(f'  R2 PUT FAILED for {key}: {e}', file=sys.stderr)
        return False

def r2_get_size(key: str, token: str) -> Optional[int]:
    url = f'https://api.cloudflare.com/client/v4/accounts/{R2_ACCOUNT}/r2/buckets/{R2_BUCKET}/objects/{key}'
    req = urllib.request.Request(url, method='HEAD')
    req.add_header('Authorization', f'Bearer {token}')
    try:
        resp = urllib.request.urlopen(req, timeout=10)
        return int(dict(resp.headers).get('Content-Length', 0))
    except Exception:
        return None

def scan_skills() -> List[dict]:
    skills = []
    for d in sorted(os.listdir(SKILLS_DIR)):
        path = os.path.join(SKILLS_DIR, d, 'SKILL.md')
        if not os.path.isfile(path) or d.startswith('.'):
            continue
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        fm_match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
        if not fm_match:
            skills.append({'directory': d, 'name': d, 'version': '?', 'path': path,
                          'size': os.path.getsize(path), 'sha256': hashlib.sha256(content.encode()).hexdigest(),
                          'frontmatter_valid': False, 'has_related': False, 'has_integration_table': False,
                          'warnings': ['No YAML frontmatter delimiters']})
            continue
        name_match = re.search(r'name:\s*(.+)', fm_match.group(1))
        ver_match = re.search(r'version:\s*"?(.+?)"?\s*$', fm_match.group(1), re.MULTILINE)
        has_related = bool(re.search(r'> \*\*Related:\*\*', content))
        has_int = bool(re.search(r'(Integration|Downstream).{0,80}\n\|', content))
        warnings = []
        fm = fm_match.group(1)
        for line in fm.split('\n'):
            if 'description:' in line and '"' in line:
                desc = line.split(':', 1)[1].strip()
                if desc.startswith('"') and "'" in desc and "\\'" not in desc:
                    warnings.append('Unescaped single quote in double-quoted description (js-yaml may reject)')
        skills.append({'directory': d, 'name': name_match.group(1).strip() if name_match else d,
                      'version': ver_match.group(1) if ver_match else '?', 'path': path,
                      'size': os.path.getsize(path), 'sha256': hashlib.sha256(content.encode()).hexdigest(),
                      'frontmatter_valid': True, 'has_related': has_related, 'has_integration_table': has_int,
                      'warnings': warnings})
    return skills

def compute_health_score(skill: dict) -> Tuple[int, int, str]:
    score = 0; max_score = 5; issues = []
    if skill['frontmatter_valid']: score += 1
    else: issues.append('frontmatter')
    if skill['has_related']: score += 1
    else: issues.append('no Related header')
    if not skill['warnings']: score += 1
    else: issues.append('js-yaml warnings')
    if skill['version'] and skill['version'] != '?': score += 1
    else: issues.append('no version tag')
    has_refs = os.path.isdir(os.path.join(SKILLS_DIR, skill['directory'], 'references'))
    has_scripts = os.path.isdir(os.path.join(SKILLS_DIR, skill['directory'], 'scripts'))
    if has_refs or has_scripts: score += 1
    else: issues.append('no refs or scripts')
    status = 'HEALTHY' if score >= 4 else 'DEGRADED' if score >= 2 else 'CRITICAL'
    return score, max_score, status, issues

def cmd_health(token: str = None):
    skills = scan_skills()
    results = []
    for s in skills:
        score, mx, status, issues = compute_health_score(s)
        r2_key = f'{R2_PREFIX}/{s["directory"]}/SKILL.md'
        r2_size = r2_get_size(r2_key, token) if token else None
        r2_status = 'SYNCED' if r2_size and r2_size == s['size'] else 'DRIFT' if r2_size else 'NO-R2'
        results.append({'skill': s['directory'], 'version': s['version'], 'health': f'{score}/{mx}',
                       'status': status, 'issues': issues, 'r2': r2_status, 'size_kb': round(s['size']/1024, 1)})
    print(f'\n{"="*80}')
    print(f'SKILL HEALTH DASHBOARD — {datetime.now(timezone.utc).isoformat()}')
    print(f'{"="*80}')
    healthy = sum(1 for r in results if r['status'] == 'HEALTHY')
    degraded = sum(1 for r in results if r['status'] == 'DEGRADED')
    critical = sum(1 for r in results if r['status'] == 'CRITICAL')
    print(f'Total: {len(results)} | HEALTHY: {healthy} | DEGRADED: {degraded} | CRITICAL: {critical}')
    print(f'\n{"Skill":<32} {"Ver":<6} {"Health":<8} {"R2":<10} {"Size":<6} {"Issues"}')
    print('-' * 80)
    for r in sorted(results, key=lambda x: (0 if x['status'] == 'CRITICAL' else 1 if x['status'] == 'DEGRADED' else 2, x['skill'])):
        issues_str = '; '.join(r['issues']) if r['issues'] else '—'
        print(f'{r["skill"]:<32} {r["version"]:<6} {r["health"]:<8} {r["r2"]:<10} {r["size_kb"]:<5}KB {issues_str}')
    print(f'\n{"="*80}')
    print(f'SUMMARY: {healthy} healthy, {degraded} need attention, {critical} critical')
    if critical > 0:
        print(f'  [ACTION-REQUIRED] {critical} skills have critical issues')
        for r in results:
            if r['status'] == 'CRITICAL':
                print(f'    - {r["skill"]}: {"; ".join(r["issues"])}')

    # Stale skill detection — Phase 2.3
    try:
        import sqlite3
        db_path = os.path.expandvars(r'%APPDATA%\\DeepChat\\app_db\\agent.db')
        if os.path.exists(db_path):
            conn = sqlite3.connect(db_path)
            cur = conn.cursor()
            cur.execute("""
                SELECT ss.skill_name, MAX(s.created_at) as last_seen
                FROM new_session_active_skills ss
                JOIN new_sessions s ON ss.session_id = s.id
                GROUP BY ss.skill_name
                ORDER BY last_seen ASC
            """)
            usage = {row[0]: row[1] for row in cur.fetchall()}
            stale_days = 60
            stale = []
            for s in skills:
                last_seen = usage.get(s['directory'])
                if last_seen and (datetime.now().timestamp() - last_seen) > stale_days * 86400:
                    stale.append(s['directory'])
                elif not last_seen:
                    stale.append(s['directory'])  # Never loaded
            conn.close()
            if stale:
                print(f'\n  SKILL RETIREMENT CANDIDATES (unused > {stale_days}d or never loaded):')
                for name in sorted(stale):
                    print(f'    - {name}')
                print(f'  [AUTO-RETIRE] {len(stale)} skills flagged for retirement review')
    except Exception:
        pass
    return results

def cmd_sync(token: str, dry_run: bool = False):
    skills = scan_skills()
    result = {'total': len(skills), 'uploaded': 0, 'failed': 0, 'skipped': 0}
    for s in skills:
        r2_key = f'{R2_PREFIX}/{s["directory"]}/SKILL.md'
        r2_size = r2_get_size(r2_key, token)
        if r2_size == s['size']:
            result['skipped'] += 1; continue
        if dry_run:
            print(f'  [DRY-RUN] {s["directory"]} ({s["size"]} bytes)')
            result['uploaded'] += 1; continue
        with open(s['path'], 'rb') as f:
            data = f.read()
        if r2_put(r2_key, data, token):
            print(f'  [OK] {s["directory"]} ({s["size"]} bytes)')
            result['uploaded'] += 1
        else:
            result['failed'] += 1
    print(f'\nSync: {result["total"]} total | {result["uploaded"]} uploaded | {result["failed"]} failed | {result["skipped"]} skipped')
    return result

def cmd_validate():
    skills = scan_skills()
    broken = [s for s in skills if not s['frontmatter_valid']]
    warnings = [s for s in skills if s['warnings']]
    print(f'Validate: {len(skills)} skills — {len(skills)-len(broken)-len(warnings)} clean, {len(warnings)} warnings, {len(broken)} broken')
    for s in broken:
        print(f'  [BROKEN] {s["directory"]}: {"; ".join(s["warnings"])}')
    for s in warnings:
        print(f'  [WARN]  {s["directory"]}: {"; ".join(s["warnings"])}')

def main():
    parser = argparse.ArgumentParser(description='Skills Sync Tool v2.0')
    parser.add_argument('--health', action='store_true', help='Show skill health dashboard')
    parser.add_argument('--sync', action='store_true', help='Sync all skills to R2')
    parser.add_argument('--validate', action='store_true', help='Validate frontmatter')
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    if not any([args.health, args.sync, args.validate]):
        parser.print_help(); return
    token = get_token()
    if args.health:
        cmd_health(token if token else None)
    elif args.sync:
        cmd_sync(token, args.dry_run)
    elif args.validate:
        cmd_validate()

if __name__ == '__main__':
    main()
