# ADR-026: qnfo-skills Repository Scope — Skills Only

**Status:** Active (hardened 2026-07-18 following remediation of commingling incident)
**Applies to:** `QNFO/qnfo-skills` GitHub repository

## Decision

The `qnfo-skills` repository is **strictly and exclusively** for skill files and
directories consumed by the DeepChat skill system. No other content — research
papers, WBS plans, project scaffolding, session artifacts, scripts unrelated to
a skill's own tooling, or any JIT/ephemeral output — may be committed here.

## Permitted Content

```
<skill-name>/
├── SKILL.md          (required — the skill definition)
├── scripts/           (optional — skill-owned utility scripts, e.g. cloudflare/scripts/d1-query.js)
├── references/        (optional — supporting reference docs the skill loads)
├── templates/         (optional — file templates the skill instantiates)
└── assets/            (optional — static assets the skill ships)
```

Plus repo-root policy files: `.gitignore`, `README.md`, `ADR-026-skills-only.md`,
`ADR-027-research-separation.md`.

## Prohibited Content

- Research papers (`.md`, `.pdf`, `.docx` manuscripts)
- WBS / project plans, distribution manifests, closeout reports
- Session audit trails, handoff documents
- JIT ephemeral scripts (`_*` prefix files, one-off `check_*.py`, `verify_*.py`)
- Data dumps (`.json` snapshots, `.csv` exports, `.sql` dumps)
- Any file belonging to a specific research project (e.g. alpha-pi-helix,
  Core Pillars distribution, CFPE forecasts)

## Where Research/Project Files Belong

- **Shared research repo:** `QNFO/qnfo-research` — general research artifacts,
  papers, distribution scripts, WBS documents shared across projects.
- **Dedicated project repo:** `QNFO/<project-name>` — for large, long-lived
  research programs (e.g. a dedicated `QNFO/alpha-pi-helix` repo) where scale
  justifies isolation from the shared research repo.

Either pattern is acceptable; the invariant is **research and skills never
share a repository.**

## Enforcement

1. `.gitignore` in this repo uses a **default-deny allowlist** — only
   `SKILL.md`, `scripts/`, `references/`, `templates/`, `assets/`, and the
   root policy files are un-ignored. Everything else is blocked by pattern,
   including common research file extensions/names as a defense-in-depth
   backstop even if `git add -f` is used carelessly.
2. Before any commit to this repo, run:
   ```bash
   git status --short   # must show ONLY skill-scoped paths
   ```
3. Any PR/commit introducing a non-skill top-level file or a non-skill file
   inside a skill directory (e.g. `research/some-paper.pdf`) must be rejected
   and the content redirected to `qnfo-research` or a dedicated project repo.

## Incident History

- **2026-07-18 (initial violation):** 26 non-skill files (WBS plans, Core
  Pillar releases, red-team audits, alpha-pi-helix project files) were
  committed to `feature/skills-9-consolidated` across 3 commits
  (`1f9cb74`, `fb0b5ec`, `18886f9`), commingled with the 9 skill directories.
- **2026-07-18 (remediation attempt 1 — INCOMPLETE):** Research files migrated
  to new `QNFO/qnfo-research` repo. Skills repo force-pushed with a "clean"
  commit, but the recovery process only restored `SKILL.md` from each skill —
  it missed the `scripts/` subdirectories (16 script files across 6 skills:
  cloudflare ×7, documents ×1, knowledge ×1, research ×4, system ×3).
- **2026-07-18 (remediation attempt 2 — COMPLETE):** Full skill directories
  (`SKILL.md` + `scripts/`) re-copied from the canonical DeepChat skill store
  (`~/.deepchat/skills/`) verified file-by-file (25 files total: 9 SKILL.md +
  16 scripts), committed, and force-pushed. `.gitignore` hardened from a
  denylist to a default-deny allowlist to prevent recurrence structurally
  rather than relying on discipline alone.
