#!/usr/bin/env python3
"""
QNFO Skills Deploy — Copy all skills from canonical path to DeepChat's expected path.

CRITICAL: DeepChat's skill_view() expects skills at:
    %APPDATA%\DeepChat\skills\<name>\SKILL.md
But the canonical source (and skill_list() discovery) is at:
    %USERPROFILE%\.deepchat\skills\<name>\SKILL.md

This script bridges the gap. Run it after any skill change to ensure skill_view()
can find all skills.

Usage:
    python _deploy.py              # Deploy all skills to AppData path
    python _deploy.py --verify     # Check both paths match
    python _deploy.py --source     # Pull from AppData back to .deepchat
"""

import os, sys, shutil, hashlib

CANONICAL = os.path.expandvars(r'%USERPROFILE%\.deepchat\skills')
DEEPCHAT  = os.path.expandvars(r'%APPDATA%\DeepChat\skills')


def hash_file(path):
    """SHA-256 hash of a file."""
    if not os.path.exists(path):
        return None
    with open(path, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()


def discover_skills(skills_dir):
    """Find all skill directories with SKILL.md."""
    skills = {}
    if os.path.isdir(skills_dir):
        for d in sorted(os.listdir(skills_dir)):
            p = os.path.join(skills_dir, d, 'SKILL.md')
            if os.path.isfile(p) and not d.startswith('.'):
                skills[d] = p
    return skills


def deploy():
    """Copy skills from canonical source to DeepChat's expected path."""
    source_skills = discover_skills(CANONICAL)
    
    if not source_skills:
        print(f"[ERROR] No skills found at {CANONICAL}")
        return False
    
    os.makedirs(DEEPCHAT, exist_ok=True)
    
    deployed = 0
    skipped = 0
    
    for name, src_path in source_skills.items():
        dst_dir = os.path.join(DEEPCHAT, name)
        dst_path = os.path.join(dst_dir, 'SKILL.md')
        
        src_hash = hash_file(src_path)
        dst_hash = hash_file(dst_path)
        
        if src_hash == dst_hash:
            skipped += 1
            continue
        
        os.makedirs(dst_dir, exist_ok=True)
        shutil.copy2(src_path, dst_path)
        deployed += 1
        
        verification = hash_file(dst_path)
        if verification != src_hash:
            print(f"  [FAIL] {name}: copy failed checksum verification")
            return False
    
    total = len(source_skills)
    print(f"[DEPLOY] {CANONICAL} -> {DEEPCHAT}")
    print(f"  {deployed} deployed, {skipped} already synced, {total} total")
    return True


def verify():
    """Check both paths have identical skills."""
    canonical = discover_skills(CANONICAL)
    deepchat  = discover_skills(DEEPCHAT)
    
    canonical_names = set(canonical.keys())
    deepchat_names  = set(deepchat.keys())
    
    only_canonical = canonical_names - deepchat_names
    only_deepchat  = deepchat_names - canonical_names
    in_both        = canonical_names & deepchat_names
    
    print(f"[VERIFY] Canonical: {len(canonical)} skills at {CANONICAL}")
    print(f"[VERIFY] DeepChat:  {len(deepchat)} skills at {DEEPCHAT}")
    
    if only_canonical:
        print(f"  [GAP] Only canonical (not in DeepChat): {sorted(only_canonical)}")
    if only_deepchat:
        print(f"  [GAP] Only DeepChat (not canonical): {sorted(only_deepchat)}")
    
    mismatched = 0
    for name in sorted(in_both):
        ch = hash_file(canonical[name])
        dh = hash_file(deepchat[name])
        if ch != dh:
            print(f"  [DRIFT] {name}: content differs")
            mismatched += 1
    
    synced = len(in_both) - mismatched
    print(f"  Synced: {synced}, Drifted: {mismatched}")
    
    if only_canonical or only_deepchat or mismatched > 0:
        print(f"\n[ACTION] Run: python _deploy.py")
        return False
    else:
        print(f"\n[OK] Both paths identical. No action needed.")
        return True


def reverse_deploy():
    """Copy from DeepChat path back to canonical (recovery)."""
    source_skills = discover_skills(DEEPCHAT)
    
    if not source_skills:
        print(f"[ERROR] No skills found at {DEEPCHAT}")
        return False
    
    os.makedirs(CANONICAL, exist_ok=True)
    deployed = 0
    for name, src_path in source_skills.items():
        dst_dir = os.path.join(CANONICAL, name)
        dst_path = os.path.join(dst_dir, 'SKILL.md')
        os.makedirs(dst_dir, exist_ok=True)
        shutil.copy2(src_path, dst_path)
        deployed += 1
    
    print(f"[REVERSE] {DEEPCHAT} -> {CANONICAL}")
    print(f"  {deployed} skills restored to canonical")
    return True


if __name__ == '__main__':
    if '--verify' in sys.argv:
        sys.exit(0 if verify() else 1)
    elif '--source' in sys.argv:
        sys.exit(0 if reverse_deploy() else 1)
    else:
        sys.exit(0 if deploy() else 1)
