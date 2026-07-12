---
name: github-manager
description: DEPRECATED -- ARCHIVED (2026-06-01). GitHub fully deprecated per ADR-001. All PM is Cloudflare-native (R2, D1, Workers, Pages). This skill retained for historical reference only. Do NOT use for new operations.
---

# GITHUB MANAGER SKILL â v1.0



> **On-demand skill.** Load via `skill_view('github-manager')` for GitHub operations.

> **NOTE:** Cloudflare R2 is the PRIMARY platform for PM state. GitHub is FALLBACK for issue tracking when R2 is unavailable.



---



## Authentication



```bash

# Verify auth

gh auth status



# Required scopes: repo, workflow, read:org, gist

```



**Account:** rwnq8

**â ï¸ QNFO org is FLAGGED by GitHub.** Use rwnq8/qwav-program for tracking when qnfo is unavailable.



---







## Tools Required



This skill is designed for use with QNFO agent tools. When loaded by a DEFAULT.md agent, the full tool suite (read, write, edit, exec, process, brave_web_search, YoBrowser, subagent_orchestrator) is available.



## QNFO Custom Skill Note



This is a QNFO custom skill deployed via `_deploy.py` (pulled from R2: `qnfo/tools/deploy.py`). It is NOT accessible via `skill_view()` (which only indexes DeepChat's built-in registry). Load it with:



```

read('G:\My Drive\prompts\skills\github-manager\SKILL.md')

```







## 2.5.1 Embedded Scripts

Per DEFAULT.md §6.1, this skill's dependent scripts are documented below.
**Canonical source: Cloudflare R2 (qnfo/tools/). Tools execute as ephemeral _<name>.py files — pull from R2, execute, discard. Never persist locally.**

| Script | Canonical (R2) | Ephemeral Execution Cache | Purpose |
|:-------|:---------------|:----------------------|:--------|
| `deploy.py` | `qnfo/tools/deploy.py` | `_deploy.py (ephemeral)` | Deploys skill files to DeepChat runtime |

### Script Recovery Protocol
If a script is missing from local disk:
1. Pull canonical from R2: `npx wrangler r2 object get qnfo/tools --remote --file=<local_path>`
2. Verify integrity: `Test-Path <local_path>`
3. If R2 copy also missing: flag `[SKILL-GAP: script <name>.py missing from R2, cannot bootstrap]`
4. Do NOT attempt to use this skill if its canonical scripts cannot be recovered.


## Repository Management



```bash

# Create repo

gh repo create qnfo/<repo-name> --public --description "<desc>"



# View repo

gh repo view qnfo/<repo-name>



# List repos

gh repo list qnfo --limit 50

```



---



## Issues (FALLBACK ONLY)



```bash

# Create issue

gh issue create --repo qnfo/<repo> --title "<title>" --label "<label>" --body "<body>"



# List issues

gh issue list --repo qnfo/<repo> --label "project-state"



# Close issue

gh issue close <num> --repo qnfo/<repo> --reason completed



# Comment on issue

gh issue comment <num> --repo qnfo/<repo> --body "<comment>"

```



---



## Labels



```bash

# Create label

gh label create --repo qnfo/<repo> <label> --color <hex>



# List labels

gh label list --repo qnfo/<repo>



# Standard labels: project-state, handoff, task, bug, enhancement, blocked, documentation, research

```



---



## Projects



```bash

# List projects

gh project list --owner qnfo



# Create project

gh project create --owner qnfo --title "<name>"



# Add item

gh project item-create <board-num> --owner qnfo --title "<title>" --body "<body>"

```



---



## Releases



```bash

# Create release

gh release create v1.0 --repo qnfo/<repo> --title "v1.0" --notes "<notes>" <file.pdf>



# List releases

gh release list --repo qnfo/<repo>

```



---



## Wiki



```bash

# Clone wiki

git clone https://github.com/qnfo/<repo>.wiki.git



# Edit and push changes

cd <repo>.wiki

# Edit files

git add .

git commit -m "Update wiki"

git push

```



---



## Platform Failure Recovery



If QNFO org is flagged/blocked:

1. Use `rwnq8/` personal account as fallback

2. Annotate all files with `[GITHUB-FALLBACK: rwnq8/<repo>]`

3. Local files become the primary record

4. See DEFAULT.md Â§0.6.8.1 for full recovery protocol



---



## When NOT to Use GitHub



| Operation | Prefer Instead |

|:----------|:---------------|

| Project state tracking | R2 `qnfo/audit/state/<project>.json` |

| Backlog management | R2 `qnfo/audit/backlog/<project>.json` |

| Decision logging | R2 `qnfo/audit/decisions/DECISION-LOG.md` |

| Release artifacts | R2 `qnfo/releases/YYYY/MM/` |

| Deployment tracking | R2 `qnfo/deployments/` |



---



*github-manager skill v1.0 â Load on-demand via skill_view(). GitHub is FALLBACK for PM operations.*



---



*github-manager v1.0 â QNFO custom skill. Load via read('G:\\My Drive\\prompts\\skills\\github-manager\\SKILL.md'). Not accessible via skill_view().*