---
name: git-hygiene
description: "Git recovery and hygiene procedures -- branch recovery, detached HEAD, merge conflicts, and Iron Rule enforcement. Use when user says fix git, git is broken, git error, merge conflict, detached HEAD, branch recovery, or when git operations fail."
version: "1.1"
---



### DEC-034 Safe Push Protocol (v1.5 — 2026-07-10)

**CRITICAL:** Multiple LLM sessions can push to the same git branch simultaneously. Amended commits, force pushes, and tag updates can silently overwrite prior work. Use the InfraLockManager DO for git coordination.

**Safe Push Flow:** lock("git", "repo:branch", 300s) → verify HEAD matches origin → git push → unlock

**Lock Required For:** Amend (YES, 300s) | Force push (YES, 300s) | Tag overwrite (YES, 120s) | Merge conflict resolution (YES, 600s) | Normal fast-forward push (NO — git handles this natively)

**DO endpoint:** `https://infra-lock-manager.q08.workers.dev`
**Protocol:** DEC-034 Universal Multi-Session Write Collision Prevention


> **INCLUDES AUTONOMOUS RED-TEAM SELF-AUDIT.** Before claiming this skill complete, autonomously run: (1) Output Verification -- negative verification. (2) Assumption Challenge -- state and test every assumption. (3) Edge Case Check -- empty/null/max/boundary/desync. (4) DoD Integration -- run _dod_enforce.py if exists. (5) Iteration -- retry on failure, max 3. ANTI-PATTERN: User should NEVER ask about quality.

### Programmatic Loading & Execution
This skill is loaded and executed **programmatically by the LLM system** 
during response generation. Loading is triggered automatically via 
`skill_view('git-hygiene')` or `read()` with filesystem path.
**The user NEVER manually loads this skill.** The `skill-autoloader` 
detects task patterns and handles all skill loading. If this skill fails 
to load, the LLM system automatically retries via the fallback chain 
documented below.
**Pinning:** This skill is [On-demand — loads when triggered by task patterns].

### Skill Loading Retry Protocol
If `skill_view('name')` fails during programmatic loading, the LLM system 
MUST execute this fallback chain:
1. **Retry 1:** `read('%USERPROFILE%\.deepchat\skills\<name>\SKILL.md')`
2. **Retry 2:** Pull from Cloudflare R2: `npx wrangler r2 object get 
   qnfo/prompts/skills/<name>/SKILL.md --remote --file=_skill.md`
3. **Retry 3:** If R2 fails, search local filesystem for any cached copy
4. **Fallback:** If ALL retries fail, continue with `[SKILL-UNAVAILABLE: <name>]` 
   and best-effort knowledge
**NEVER silently proceed without a skill's critical instructions.** If a skill 
is required for the task and cannot be loaded after 3 retries, escalate to 
the user with the specific failure reason.

---

### DEC-034 Safe Push Protocol (v1.5 — 2026-07-10)

CRITICAL: Acquire DO lock before git amend/force-push to prevent multi-session collisions.
Lock required for: amend(300s), force-push(300s), tag-overwrite(120s), merge-conflict(600s).
Normal fast-forward push: NO lock needed (git handles this).
DO: https://infra-lock-manager.q08.workers.dev | Protocol: DEC-034


> **Related:** closeout-manager

---

## execute_plan (MANDATORY -- Before Any Execution)

**This skill involves execution-heavy workflows.** Before executing, use update_plan to populate a concrete, verifiable checklist. Every item must be short, specific, and testable with tool evidence.

### Execution Protocol

1. **Populate update_plan** with workflow phases as concrete checklist items
2. **Execute one item at a time** -- at most ONE in_progress
3. **Mark items completed ONLY with tool evidence** (Test-Path, exec output, git log)
4. **Never claim completion without execution evidence** -- Rule 14 enforcement
5. **If blocked:** Flag as [BLOCKED: reason] and move to the next item

### Example Plan

update_plan([
  {"step": "Diagnose the git error state", "status": "pending"},
  {"step": "Apply appropriate recovery procedure", "status": "pending"},
  {"step": "Verify branch is on feature/<name>", "status": "pending"},
  {"step": "Verify commit with git log -1 --oneline", "status": "pending"},
  {"step": "Verify no uncommitted changes", "status": "pending"}
])


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

## Commit Message Format (Merged from git-commit skill)

Follow the **Conventional Commits** specification:

```
<type>(<scope>): <subject>

[optional body]

[optional footer(s)]
```

### Types

| Type | Use For |
|:-----|:--------|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation changes |
| `style` | Formatting, whitespace (no code change) |
| `refactor` | Code restructuring (no feature/fix) |
| `perf` | Performance improvement |
| `test` | Adding or fixing tests |
| `build` | Build system, dependencies |
| `ci` | CI configuration |
| `chore` | Miscellaneous maintenance |

### Subject Rules
- Imperative mood: "add" not "added" / "fix" not "fixed"
- Lowercase first letter, no trailing period, max 50 characters

### Examples
- `fix(auth): handle null token in session refresh`
- `feat(api): add pagination to search endpoint`

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

> **Version:** (Kaizen-audited 2026-07-08)
