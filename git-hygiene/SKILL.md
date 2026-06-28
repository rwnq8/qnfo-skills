---
name: git-hygiene
description: Git recovery and hygiene procedures — branch recovery, detached HEAD, merge conflicts, and Iron Rule enforcement. Use when git operations fail or the workspace is in an unexpected state.
version: "1.0"
---
> **INCLUDES AUTONOMOUS RED-TEAM SELF-AUDIT.** See RED-TEAM-PROTOCOL.md.


# GIT HYGIENE SKILL — v1.0

> **On-demand skill.** Load via `skill_view('git-hygiene')` when git operations fail.
> Source: DEFAULT.md §9 + QWAV-AGENT.md §7

---

## IRON RULE: NEVER Commit to main/master

**Feature branches only.** Always verify before work:
```bash
git branch --show-current
# Must return: feature/<kebab-case-description>
```

---
## Common Recovery Scenarios

### Detached HEAD
```bash
# Create rescue branch from current state
git checkout -b feature/recovery-<timestamp>

# Verify state
git log -1 --oneline
git branch --show-current
```

### Merge Conflicts
```bash
# Abort and retry
git merge --abort
git pull --rebase
# Resolve conflicts manually, then:
git add .
git rebase --continue
```

### Branch Renamed by Another Process (CPL L19)
```bash
# Verify current branch name
git branch --show-current

# If different from expected, update recorded name — do NOT create another branch
# Continue work on current branch
```

### Push Rejected
```bash
# Pull remote changes first
git pull --rebase
# Resolve any conflicts
git push
```

### Wrong Branch — Uncommitted Changes
```bash
# Stash changes
git stash
# Switch to correct branch
git checkout feature/<correct-branch>
# Apply stash
git stash pop
```

---

## Git Protocol (Pre-Work)

```bash
# 1. Verify branch
git branch --show-current
# Must be feature/<name>

# 2. Verify branch name hasn't changed (CPL L19)
# Compare against expected name

# 3. Pull latest
git pull --rebase
```

## Git Protocol (Post-Work)

```bash
# 1. Filesystem verify
Test-Path <file>
Get-Content <file> -First 5

# 2. Stage
git add <files>

# 3. Commit with format
git commit -m "ACTION:[CREATE|EDIT|DELETE] FILE: <path> RATIONALE:<reason>"

# 4. Verify commit
git log -1 --oneline

# 5. Verify branch
git branch --show-current
```

---

## Commit Format

```
ACTION:[CREATE|EDIT|DELETE] FILE: <path> RATIONALE:<reason>
```

Examples:
- `ACTION:CREATE FILE: papers/quantum-error-v1.md RATIONALE:Initial draft`
- `ACTION:EDIT FILE: README.md RATIONALE:Update project state`

---

## Anti-Patterns

| Anti-Pattern | Fix |
|:-------------|:----|
| "I committed" without `git log -1` verification | Always verify with git log |
| Direct commits to main/master | Feature branches only — IRON RULE |
| Creating new branch when branch renamed | Update recorded name (CPL L19) |
| `-ErrorAction SilentlyContinue` in git commands | Use `$LASTEXITCODE`, `try/catch` |

---

## Verification Rules

| After Every... | Verify With... |
|:---------------|:---------------|
| Commit | `git log -1 --oneline` |
| Branch switch | `git branch --show-current` |
| Push | `git log -1 --oneline` (confirm remote) |

**Never claim "committed" without git log verification (CPL L13).**

---

*git-hygiene skill v1.0 — Load on-demand via skill_view() for git recovery*

---

*git-hygiene v1.0 — QNFO custom skill. Load via read('R2 `qnfo/prompts/skills/git-hygiene\\SKILL.md'). Not accessible via skill_view().*

## RT: RED-TEAM SELF-AUDIT

Before claiming this skill complete, autonomously run:

1. Output Verification (negative verification)
2. Assumption Challenge (state and test every assumption)
3. Edge Case Check (empty/null/max/boundary/desync)
4. DoD Integration (run _dod_enforce.py if exists)
5. Iteration (retry on failure, max 3)

ANTI-PATTERN: User should NEVER ask about quality.
Refer to RED-TEAM-PROTOCOL.md for full protocol.

