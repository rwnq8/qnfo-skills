---
name: skill-sync
description: Sync all DeepChat skills between local disk, GitHub, and Cloudflare R2. Monitors skill modifications and auto-syncs after changes. Updates Discovery Index with current versions. Use when skills are modified and need to be pushed to redundant backups, or to check sync status.
version: "1.1"
---

# SKILL SYNC SKILL — v1.1

> **On-demand skill.** Load via `skill_view('skill-sync')` to sync skills or check sync status.

---

## Purpose

Skills are modified locally but must be pushed to GitHub and R2 for redundancy. This skill automates the three-way sync and updates the Discovery Index with current versions.

## When to Use

| Trigger | Action |
|:--------|:-------|
| After any skill modification | "SYNC SKILLS" or use bootstrap_skills.py |
| "Are skills in sync?" | Check sync status report |
| "Push skills to GitHub/R2" | Selective sync |
| Before session closeout | Auto-sync check |

## Quick Sync (One Command)

```bash
python "%APPDATA%\.deepchat\skills\bootstrap_skills.py" --sync
```

This:
1. Commits and pushes all skill changes to GitHub (`rwnq8/qnfo-skills`)
2. Uploads all skills to R2 (`qnfo/prompts/skills/<name>/SKILL.md`)
3. Reports sync status

## Sync Status Check

```python
import os, urllib.request

TOKEN = os.environ.get('CLOUDFLARE_API_TOKEN', '')
ACCOUNT = 'edb167b78c9fb901ea5bca3ce58ccc4b'
SKILLS_DIR = os.path.expandvars(r'%USERPROFILE%\.deepchat\skills')

local_skills = []
for d in sorted(os.listdir(SKILLS_DIR)):
    p = os.path.join(SKILLS_DIR, d, 'SKILL.md')
    if os.path.isfile(p) and not d.startswith('.'):
        local_skills.append(d)

# Sample-check 5 skills against R2 for drift
drift = 0
for name in local_skills[:5]:
    local_size = os.path.getsize(os.path.join(SKILLS_DIR, name, 'SKILL.md'))
    url = f'https://api.cloudflare.com/client/v4/accounts/{ACCOUNT}/r2/buckets/qnfo/objects/qnfo/prompts/skills/{name}/SKILL.md'
    req = urllib.request.Request(url)
    req.add_header('Authorization', f'Bearer {TOKEN}')
    try:
        resp = urllib.request.urlopen(req, timeout=10)
        r2_size = len(resp.read())
        status = 'SYNCED' if r2_size == local_size else 'DRIFT'
        if status == 'DRIFT':
            drift += 1
        print(f'  {name}: {status} (local={local_size}, r2={r2_size})')
    except:
        print(f'  {name}: R2 MISSING')

status = 'DRIFT DETECTED — run bootstrap_skills.py --sync' if drift else 'IN SYNC'
print(f'\nSync Status: {status}')
```

## Bootstrap Tools

Must exist locally for this skill to work:
- `bootstrap_skills.py` — One-command sync tool
- Recoverable from R2: `qnfo/tools/bootstrap_skills.py`
- Recoverable from GitHub: `rwnq8/qnfo-skills/blob/master/bootstrap_skills.py`

---

## Mandatory Post-Sync Restart

**Rule:** After any successful skill sync (push to GitHub + R2), DeepChat MUST be restarted programmatically. Skills are loaded at application startup; changes made via sync do not take effect until DeepChat is killed and relaunched.

```powershell
powershell -ExecutionPolicy Bypass -File "$env:USERPROFILE\.deepchat\skills\skill-sync\scripts\restart_deepchat.ps1"
```

This kills all old DeepChat processes and launches a fresh instance. Execute this as the final step after confirming sync success. The current conversation will terminate.

---



## Embedded Scripts

Per DEFAULT.md §6.1, this skill's dependent scripts are documented below.
**Canonical source: Cloudflare R2 (`qnfo/tools/`). Tools execute as ephemeral `_<name>.py` files — pull from R2, execute, discard. Never persist locally.**

| Script | Canonical (R2) | Ephemeral Execution Cache | Purpose |
|:-------|:---------------|:--------------------------|:--------|
| `bootstrap_skills.py` | `qnfo/tools/bootstrap_skills.py` | `_bootstrap_skills.py` (ephemeral) | One-command skill sync tool |

### Execution Protocol (Ephemeral)
Tools execute locally (Python requires filesystem access) but do NOT persist:
1. **Pull:** `npx wrangler r2 object get qnfo/tools/<name>.py --remote --file=_<name>.py`
2. **Execute:** `python _<name>.py`
3. **Discard:** `Remove-Item _<name>.py`
4. If R2 copy missing: flag `[SKILL-GAP: script <name>.py missing from R2, cannot bootstrap]`

## VERSION HISTORY

| Version | Date | Changes |
|:--------|:-----|:--------|
| **v1.1** | 2026-06-26 | Skill audit — added version history. Current version. |


*skill-sync v1.1 — Monitors and syncs skills between local, GitHub, and R2. Keeps backups current. Includes mandatory post-sync restart.*
