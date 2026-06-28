---
name: git-commit
description: Generate well-formatted git commit messages following conventional commit standards. Use when user wants to generate a commit message, needs guidance on commit format, or asks to commit code changes.
version: "2.0"
allowedTools:
  - exec
---
> **INCLUDES AUTONOMOUS RED-TEAM SELF-AUDIT.** See RED-TEAM-PROTOCOL.md.


# GIT COMMIT SKILL — v2.0

> **On-demand skill.** Load via `skill_view('git-commit')` for conventional commit message generation.

---

## When to Use

| Trigger | Action |
|:--------|:-------|
| "Generate a commit message" | Full workflow below |
| "Commit these changes" | Stage → generate message → commit with verification |
| "What should my commit look like?" | Format guide only |

---

## Workflow — 3 Steps

### Step 1: Discover Changes

```bash
git status
git diff --staged
# Or for unstaged:
git diff
```

Analyze what changed: new files, modified files, deleted files.

### Step 2: Generate Commit Message

Follow the **Conventional Commits** specification:

```
<type>(<scope>): <subject>

[optional body]

[optional footer(s)]
```

#### Types

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

#### Subject Rules

- Imperative mood: "add" not "added" / "fix" not "fixed"
- Lowercase first letter
- No trailing period
- Max 50 characters

#### Body (Optional)

- Explain **what** and **why**, not how
- Wrap at 72 characters
- Blank line between subject and body

#### Footer (Optional)

- `Fixes #123` or `Closes #456`
- `BREAKING CHANGE: description`

### Step 3: Commit with Verification

```bash
# If using generated message:
git commit -m "<message>"

# Verify
git log -1 --oneline
```

**MANDATORY:** After every commit, run `git log -1 --oneline` to verify.

---

## Examples

### Simple fix
```
fix(auth): handle null token in session refresh
```

### Feature with body
```
feat(api): add pagination to search endpoint

Add cursor-based pagination to improve performance for large
result sets. Default page size is 20 items.

Closes #142
```

### Breaking change
```
feat(core): switch config format from JSON to YAML

BREAKING CHANGE: All existing config.json files must be migrated
to config.yaml. Use the migration script in scripts/migrate-config.js.
```

---

## Anti-Patterns

| Anti-Pattern | Fix |
|:-------------|:----|
| "I committed" without `git log -1` | Always verify with git log |
| Vague subject: "updates" | Be specific: "fix(payment): correct tax calculation" |
| Period at end of subject | Remove trailing period |
| Capitalized first letter | Use lowercase |
| Mixing unrelated changes in one commit | Split into separate commits |

---

*git-commit v2.0 — Conventional commit message generation with verification.*

## RT: RED-TEAM SELF-AUDIT

Before claiming this skill complete, autonomously run:

1. Output Verification (negative verification)
2. Assumption Challenge (state and test every assumption)
3. Edge Case Check (empty/null/max/boundary/desync)
4. DoD Integration (run _dod_enforce.py if exists)
5. Iteration (retry on failure, max 3)

ANTI-PATTERN: User should NEVER ask about quality.
Refer to RED-TEAM-PROTOCOL.md for full protocol.

