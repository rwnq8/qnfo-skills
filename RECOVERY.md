# QNFO Skills Recovery Guide

## Bootstrapping from Scratch

Any agent or user can restore ALL 28 skills from either backup with ONE command.

### Option 1: From GitHub (recommended)

```bash
git clone https://github.com/rwnq8/qnfo-skills.git "%APPDATA%\.deepchat\skills"
```

### Option 2: From Cloudflare R2

```bash
# Requires CLOUDFLARE_API_TOKEN in environment
python bootstrap_skills.py --source r2
```

### Option 3: Verify existing installation

```bash
python "%APPDATA%\.deepchat\skills\bootstrap_skills.py" --verify
```

## Backup Locations

| Location | Path | Access |
|:---------|:-----|:-------|
| **GitHub** | https://github.com/rwnq8/qnfo-skills | Public read, write via gh CLI |
| **Cloudflare R2** | `qnfo/prompts/skills/<name>/SKILL.md` | Full access via CLOUDFLARE_API_TOKEN |
| **Local Disk** | `%APPDATA%\.deepchat\skills\` | Always available (thin client) |

## Keeping Skills Synced

After ANY skill modification, run:
```bash
python "%APPDATA%\.deepchat\skills\bootstrap_skills.py" --sync
```
This pushes to GitHub AND uploads to R2 simultaneously.

## Skills Inventory (28 total)

All QNFO custom skills: algorithmic-art, bling-usability-audit, closeout-manager (v2.3), cloudflare-deployer (v1.3), code-review, deepchat-settings, doc-coauthoring, docx, email-composer, execution-guard, frontend-design, git-commit, git-hygiene, infographic-syntax-creator, kaizen-autonomous-update, knowledge-graph, local-to-r2-migration (v1.0), mcp-builder, pdf, pdf-builder (v1.4), pptx, prompt-audit, publication-publisher (v1.5), qnfo-agent (v3.28), skill-creator, template-catalog, web-artifacts-builder, xlsx.
