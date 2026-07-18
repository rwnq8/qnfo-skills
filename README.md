# qnfo-skills

Skill definitions and skill-owned tooling for the DeepChat agent skill system.

**This repository is strictly scoped to skill files.** See
[ADR-026](./ADR-026-skills-only.md) for the full policy and
[ADR-027](./ADR-027-research-separation.md) for where research/project files
belong instead (`QNFO/qnfo-research` or a dedicated project repo).

## Skills in this repository

| Skill | Scripts | Templates |
|---|---|---|
| `cloudflare` | d1-query, dnslink-create, filebase-upload, infra-audit, r2-hygiene, r2-upload, worker-route | — |
| `code` | — | — |
| `documents` | r2-archive | — |
| `frontend-design` | — | — |
| `git-github` | — | — |
| `knowledge` | kg-seed-4d | — |
| `qnfo-agent` | — | — |
| `research` | arweave-upload, internet-archive-submit, pinata-pin, verify-4d | deliverable-registry-template, risk-register-template |
| `system` | infra-audit, skill-sync, worker-audit | — |

## The Three Sources of Truth (Keep in Sync)

Every QNFO custom skill must exist **identically** in all three of these
locations. They are peers, not a primary + replicas — drift in any one
direction (local ahead of GitHub, GitHub ahead of R2, etc.) is a bug.

| Source | Path | Role |
|---|---|---|
| **Local (canonical for editing)** | `~/.deepchat/skills/<skill>/` | Where the DeepChat agent actually loads skills from at runtime |
| **GitHub** | `QNFO/qnfo-skills` (this repo) | Version-controlled history, PR review, rollback |
| **R2** | `qnfo-skills` bucket, `prompts/skills/<skill>/` | Cross-machine / cross-agent distribution surface |

### One Skill, One Directory (Anti-Duplication Rule)

**Never create a second local skill directory for an updated version of an
existing skill** (e.g. `research-v2` alongside `research`). This causes:
- Ambiguous autoloader matching (which one does the trigger table point to?)
- Silent local/GitHub/R2 drift (the "v2" almost never gets pushed anywhere)
- Orphaned content when only one of the two directories is edited going forward

**Instead:** edit the existing skill's `SKILL.md` in place and bump its
`version:` field in the YAML frontmatter (e.g. `"2.1"` -> `"2.2"`). Use the
body's version heading (`# SKILL-NAME -- vX.Y`) and the YAML `version:` field
consistently — a mismatch between the two is itself a sync-drift symptom to
watch for.

## Sync Verification (Best Practice — run before AND after any skill edit)

Because there is no automated CI sync check yet, an LLM agent (or human)
performing skill maintenance MUST manually verify all three sources agree
before declaring a skill "in sync." Content should be compared **after
normalizing line endings** (`\r\n` vs `\n`), since CRLF/LF differences are
cosmetic, not real drift:

```powershell
# 1. Local vs GitHub (after `git pull` or clone to a temp dir)
$local = [System.IO.File]::ReadAllText("$env:USERPROFILE\.deepchat\skills\<skill>\SKILL.md")
$gh    = [System.IO.File]::ReadAllText("<path-to-cloned-repo>\<skill>\SKILL.md")
$crlf = [string]([char]13) + [string]([char]10); $lf = [string]([char]10)
($local.Replace($crlf,$lf)) -eq ($gh.Replace($crlf,$lf))   # must be True

# 2. GitHub vs R2 (after sync)
rclone check <local-repo-path> primary-r2:qnfo-skills/prompts/skills/<skill>

# 3. Directory-level duplicate check (catches "research" + "research-v2" cases)
Get-ChildItem "$env:USERPROFILE\.deepchat\skills" -Directory |
  Group-Object { $_.Name -replace '-v\d+$','' } |
  Where-Object Count -gt 1
```

## Sync Workflow (LLM-Orchestrated)

1. **Edit locally first** — `~/.deepchat/skills/<skill>/SKILL.md` is the
   working copy. Bump `version:` in frontmatter + the `# ... -- vX.Y` heading
   together.
2. **Clone/pull this repo to a scratch dir** — never edit a live checkout that
   also has uncommitted unrelated changes.
3. **Copy only the changed skill directory** (`SKILL.md` + `scripts/` +
   `templates/` etc.) into the scratch clone.
4. **Verify `git status --short` shows only skill-scoped paths** before
   staging (see Contributing below).
5. **Commit on a feature branch** (`fix/...` or `feat/...`, never `main`),
   using format: `ACTION:EDIT FILE: <path> RATIONALE: <reason>`.
6. **Push and open/merge PR** (or fast-forward merge for solo maintenance).
7. **Run `system/scripts/skill-sync.js`** (or equivalent R2 PUT) to push the
   same files to the `qnfo-skills` R2 bucket under `prompts/skills/<skill>/`.
8. **Re-verify all three sources** using the Sync Verification steps above.
9. **Never leave an orphan.** If a skill was renamed or superseded, delete the
   old local directory (after backing it up) in the same maintenance pass —
   do not let both versions coexist across a session boundary.

## Contributing

Before committing, verify `git status --short` shows only skill-scoped paths
(`<skill>/SKILL.md`, `<skill>/scripts/*`, `<skill>/references/*`,
`<skill>/templates/*`, `<skill>/assets/*`). The `.gitignore` in this repo is a
default-deny allowlist — non-skill files will not stage even with `git add -A`,
though `git add -f` can still bypass it, so manual review remains required.

## Incident Log (Cross-Reference)

See `ADR-026-skills-only.md` §"Incident History" for the 2026-07-18
commingling incident and its two-attempt remediation. See this repo's commit
history for the 2026-07-18 `research`/`research-v2` local-only duplication
fix (merged into `research` v2.2; `research-v2` never existed on GitHub/R2 and
was removed locally after a full content diff confirmed nothing was lost).
