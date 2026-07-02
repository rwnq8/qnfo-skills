---
name: skill-sync
description: Sync all DeepChat skills between local disk, GitHub, and Cloudflare R2. Monitors skill modifications and auto-syncs after changes. Updates Discovery Index with current versions. Use when skills are modified and need to be pushed to redundant backups, or to check sync status.
version: "1.3"
---


---

# SKILL SYNC SKILL — v1.3

> **On-demand skill. AUTO-GAP-AUDIT INTEGRATION.** Load via `skill_view('skill-sync')` to sync skills or check sync status. Automatically triggers gap audit (closeout-manager §2.6) after sync completion.

---

## Purpose

Skills are modified locally but must be pushed to GitHub and R2 for redundancy. This skill automates the three-way sync, updates the Discovery Index with current versions, and **triggers the POST-PHASE GAP AUDIT** to verify no desync or drift remains.

## When to Use

| Trigger | Action |
|:--------|:-------|
| After any skill modification | "SYNC SKILLS" or use bootstrap_skills.py → auto-triggers gap audit |
| "Are skills in sync?" | Check sync status report → auto-triggers gap audit if desync found |
| "Push skills to GitHub/R2" | Selective sync → auto-verifies R2 + DI |
| Before session closeout | Auto-sync check → feeds into closeout gap audit |

## Quick Sync (One Command)

```bash
python "%USERPROFILE%\.deepchat\skills\bootstrap_skills.py" --sync
```

This:
1. Commits and pushes all skill changes to GitHub (`rwnq8/qnfo-skills`)
2. Uploads all skills to R2 (`qnfo/prompts/skills/<name>/SKILL.md`)
3. Reports sync status
4. **AUTO-TRIGGERS gap audit** (closeout-manager §2.6) — verifies R2, GitHub, and DI consistency

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
- `bootstrap_skills.py` — One-command sync tool (located at `%USERPROFILE%\.deepchat\skills\bootstrap_skills.py`)
- Recoverable from R2: `qnfo/tools/bootstrap_skills.py`
- Recoverable from GitHub: `rwnq8/qnfo-skills/blob/master/bootstrap_skills.py`

---

## Auto-Gap-Audit Integration (v1.3)

After sync completes (GitHub + R2), this skill automatically triggers the POST-PHASE GAP AUDIT (closeout-manager §2.6):
1. Verify R2 sync count matches local count
2. Verify GitHub HEAD matches local commit
3. Verify Discovery Index is updated with current versions
4. Report any desync or drift as gaps

## Mandatory Post-Sync Restart

**Rule:** After any successful skill sync (push to GitHub + R2), DeepChat MUST be restarted programmatically. Skills are loaded at application startup; changes made via sync do not take effect until DeepChat is killed and relaunched.

```powershell
powershell -ExecutionPolicy Bypass -File "$env:USERPROFILE\.deepchat\skills\skill-sync\scripts\restart_deepchat.ps1"
```

This kills all old DeepChat processes and launches a fresh instance. Execute this as the final step after confirming sync success. The current conversation will terminate.

---

*skill-sync v1.3 — Monitors and syncs skills between local, GitHub, and R2. Auto-gap-audit integration. Paths corrected (%USERPROFILE%\.deepchat\skills). Includes mandatory post-sync restart.*
