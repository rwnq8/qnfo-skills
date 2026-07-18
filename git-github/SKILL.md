---
name: git-github
description: Git workflow operations and GitHub project management -- conventional commits, branch recovery, merge conflicts, detached HEAD, stash recovery, GitHub Issues, PRs, Wikis, Releases, Milestones, project boards, and GitHub-D1 sync. GitHub is CANONICAL for skills repository and project files/archives.
version: "2.0"
triggers: ["git", "commit", "merge", "rebase", "branch", "push", "pull", "detached HEAD", "conflict", "stash", "reflog", "GitHub", "Issues", "PRs", "pull request", "wiki", "releases", "Milestones", "project board", "GitHub sync", "D1 sync", "repo", "repository", "fork", "clone", "remote", "origin", "main", "master", "feature branch"]
related: []
priority: 2
platform: all
autonomous: false
self_sufficient: true
---

# GIT-GITHUB -- v2.0 (Ultra-Consolidated VC + PM)

> **Merges 2:** git-operations + github-manager
> **Cloudflare Full-Stack:** Git is version control for the import surface ONLY. R2 + D1 are canonical for project artifacts. GitHub is secondary to D1 for project state. Skills repo (`qnfo-skills`) is for skills exclusively -- NEVER place project data there (ADR-026).

## execute_plan

update_plan([
  {"step": "Verify current branch: git branch --show-current (IRON RULE: NEVER main/master)", "status": "pending"},
  {"step": "Execute git or GitHub operation", "status": "pending"},
  {"step": "Verify: git log -1 --oneline, git status --short (must be clean)", "status": "pending"},
])

---

## Git Operations

### Conventional Commits (MANDATORY)
Format: `ACTION:[CREATE|EDIT|DELETE] FILE: <path> RATIONALE: <reason>`

Valid ACTION values:
- `CREATE` -- new file
- `EDIT` -- modified existing file
- `DELETE` -- removed file

Examples:
```
ACTION:CREATE FILE: prompts/DEFAULT.md RATIONALE: Added execution gate
ACTION:EDIT FILE: skills/cloudflare/SKILL.md RATIONALE: Added Email section
ACTION:DELETE FILE: deprecated/old-script.py RATIONALE: Replaced by new version
```

### Branch Discipline (IRON RULE)
- **NEVER commit to main/master.** This is a HARD GATE.
- Always use feature branches: `feature/<kebab-case-description>`
- Branch naming: lowercase, hyphens, descriptive (no underscores, no CamelCase)
- Verify before commit: `git branch --show-current`
- Examples: `feature/kaizen-update-2026-07-17`, `feature/cfpe-stage-4-red-team`

### Standard Workflow
```bash
# 1. Check state
git status

# 2. Verify on feature branch
git branch --show-current
# MUST show: feature/<name>, NOT main/master

# 3. Stage changes
git add <files>

# 4. Commit with conventional format
git commit -m "ACTION:TYPE FILE: path RATIONALE: reason"

# 5. Verify commit
git log -1 --oneline

# 6. Verify branch
git branch --show-current

# 7. Push if needed
git push origin <branch>
```

### Verification Protocol (POST-WRITE MANDATORY)
After EVERY git operation:
1. `git log -1 --oneline` -- commit exists in log
2. `git branch --show-current` -- on correct feature branch
3. `git status --short` -- clean working tree (empty output)

**Tool success messages are NOT verification.** Show the actual git output.

---

## Git Recovery Procedures

### Detached HEAD
```bash
# Scenario: you see "HEAD detached at <hash>"
git checkout -b feature/recovery-branch
# Verify: git branch --show-current
```

### Merge Conflicts
```bash
# 1. Identify conflicted files
git status

# 2. Open each conflicted file
# Conflict markers: <<<<<<< HEAD, =======, >>>>>>> other-branch

# 3. Resolve conflicts in each file
# Remove conflict markers, keep desired changes

# 4. Stage resolved files
git add <resolved-file>

# 5. Complete merge
git commit

# 6. Verify
git log --oneline -3
```

### Lost Commits (Reflog Recovery)
```bash
# 1. Find lost commit in reflog
git reflog
# Example: abc1234 HEAD@{2}: commit: ACTION:CREATE FILE: ...

# 2. Checkout the lost commit
git checkout abc1234

# 3. Create branch from it
git checkout -b feature/recovered

# 4. Verify
git log --oneline -3
```

### Stash Recovery
```bash
# 1. List saved stashes
git stash list
# stash@{0}: WIP on feature/branch: abc1234 Commit message
# stash@{1}: WIP on main: def5678 Older work

# 2. Apply most recent stash
git stash pop

# Or apply specific stash
git stash apply stash@{1}

# 3. Clear if needed
git stash clear
```

### Fixing Wrong Branch Commits
```bash
# Committed to main by mistake
git log -1 --oneline  # Note the hash
git checkout -b feature/correct-branch
git checkout main
git reset --hard origin/main  # Undo wrong commit on main
```

### Undoing Last Commit (not pushed)
```bash
# Undo commit, keep changes staged
git reset --soft HEAD~1

# Undo commit, keep changes unstaged
git reset HEAD~1

# Undo commit, discard changes (DANGEROUS)
git reset --hard HEAD~1
```

---

## GitHub Management

### Repository Operations
- **Create repo:** Via GitHub API or web UI
- **Clone:** `git clone <url>`
- **Push:** `git push origin <branch>`
- **Pull:** `git pull origin <branch>`

### Issues
Create, update, close Issues. Template: title (actionable, specific), body (description, steps, expected behavior, environment).

### Pull Requests
Create PRs with: title, description, linked issues, reviewers. Merge strategies: squash (clean history), merge (preserve commits), rebase (linear history).

### Wikis
Create/edit documentation pages. Structure: Home (overview), Getting Started (setup), Architecture (design), Operations (deploy/maintain).

### Releases
Create semantic versioned releases with release notes. Attach build artifacts (binaries, PDFs, archives).

### Milestones & Projects
Group issues into milestones with due dates. Track via project boards (To Do -> In Progress -> Done).

### GitHub-D1 Sync
GitHub is SECONDARY to D1 for project state. Sync direction: D1 -> GitHub (D1 is canonical). Sync on: project state changes, publication events, session closeouts.

---

## Protected Repositories

### qnfo-skills (ADR-026)
- **Git repo is for SKILLS ONLY.** NEVER place project data, publications, research artifacts, or governance documents.
- Git-tracked files in the skills repo are PROTECTED. They survive thin-client cleanups (ADR-021/ADR-025).
- Violating this rule is a fabrication-level offense (Rule 14).

### Import Surface
- `qnfo/prompts/` -- system prompts, templates, skills, configs
- This is the ONLY content that should be in the Local disk import surface
- Everything else: R2 + D1 (Cloudflare-native)

---

## Anti-Patterns
| Anti-Pattern | Fix |
|:-------------|:----|
| Committing to main/master | HARD GATE: `git branch --show-current` before commit |
| `git push --force` on shared branches | NEVER force-push to branches others use |
| Amending pushed commits | Only amend unpushed commits |
| Claiming commit without git log evidence | ALWAYS verify: `git log -1 --oneline` |
| Using skills repo as project workspace | ADR-026: skills repo = skills ONLY |
| `git add .` (adds everything blindly) | Stage specific files: `git add <file>` |
| Losing work by `git reset --hard` | Check `git stash` or `git reflog` first |
