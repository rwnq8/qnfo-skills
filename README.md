# qnfo-skills

Skill definitions and skill-owned tooling for the DeepChat agent skill system.

**This repository is strictly scoped to skill files.** See
[ADR-026](./ADR-026-skills-only.md) for the full policy and
[ADR-027](./ADR-027-research-separation.md) for where research/project files
belong instead (`QNFO/qnfo-research` or a dedicated project repo).

## Skills in this repository

| Skill | Scripts |
|---|---|
| `cloudflare` | d1-query, dnslink-create, filebase-upload, infra-audit, r2-hygiene, r2-upload, worker-route |
| `code` | — |
| `documents` | r2-archive |
| `frontend-design` | — |
| `git-github` | — |
| `knowledge` | kg-seed-4d |
| `qnfo-agent` | — |
| `research` | arweave-upload, internet-archive-submit, pinata-pin, verify-4d |
| `system` | infra-audit, skill-sync, worker-audit |

## Contributing

Before committing, verify `git status --short` shows only skill-scoped paths
(`<skill>/SKILL.md`, `<skill>/scripts/*`, `<skill>/references/*`,
`<skill>/templates/*`, `<skill>/assets/*`). The `.gitignore` in this repo is a
default-deny allowlist — non-skill files will not stage even with `git add -A`,
though `git add -f` can still bypass it, so manual review remains required.
