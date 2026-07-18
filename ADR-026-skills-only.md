# ADR-026: qnfo-skills Repository Scope — Skills Only

**Status:** Active (hardened 2026-07-18 following remediation of THREE commingling incidents)
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

## Prohibited Git Metadata: Tags, Releases, Branches (ADDED 2026-07-18, Incident 3)

**This repo's ban on research content applies to git metadata, not just files.**
A commit can be "clean" (only skill-scoped files) while the *tag* or *GitHub
Release* wrapped around it still leaks research content into this repo's
history, tag list, and Releases page. This happened concretely — see Incident
3 below — where the research skill's own Phase Closeout Protocol (which
creates a git tag per phase, e.g. `v0.1-phase0`, `v1.0.0`, plus an eventual
GitHub Release for the Zenodo DOI) was executed with the working directory
pointed at `qnfo-skills` instead of the dedicated research project repo.

**Hard rules:**
1. **Tags in this repo are RESERVED for skill versioning only** (if ever
   used) — e.g. `skills-v1.0.0` for a skill-ecosystem-wide milestone. Any tag
   matching research/project patterns (`v0.1-phase0`, `v0.2-phase1-dd`,
   `v1.0.0` unqualified, `archive/<project-name>`, etc.) is a **violation**
   and must be deleted.
2. **GitHub Releases in this repo are PROHIBITED entirely.** Publications,
   Zenodo DOI announcements, and paradigm-forecast releases belong on the
   project's own repo (`qnfo-research` or a dedicated `QNFO/<project>` repo)
   or on Zenodo directly — never as a `qnfo-skills` GitHub Release.
3. **Before creating ANY git tag or GitHub Release, verify the current
   working directory / `git remote -v` points at the correct project repo —
   NOT `qnfo-skills`.** This is a mandatory pre-flight check for the research
   skill's Phase Closeout Protocol (see `research/SKILL.md`).
4. **Routine sync verification (see README.md) must include a tag/release
   audit**, not just a file-tree diff — a clean working tree does not imply
   a clean repo if stale tags/releases exist from before a remediation.

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
- **2026-07-18 (Incident 3 — stale tags/release from PRE-remediation history,
  found during a follow-up user-reported audit, REMEDIATED same day):**
  Attempts 1-2 above fixed the *branch tip* (working tree at `master`/
  `feature/skills-9-consolidated`) but never audited **tags** or **GitHub
  Releases**, which are independent refs that survive a branch force-push.
  6 stale tags survived from the pre-remediation commit graph, each pointing
  at commits containing research/project content that was never in this
  repo's clean history:
  - `v1.0.0` (+ matching GitHub Release "QNFO 100-Year Paradigm Forecast
    v1.0.0", linking Zenodo DOI 10.5281/zenodo.21366522) — commit contained
    ~85 files: the OLD 59-skill pre-consolidation tree plus 18 root-level
    paradigm-forecast research documents (`QNFO_PARADIGM_FORECAST.md`,
    `AUTX_Master_Plan_v3.0_Overview.md`, `CFPE_METHODOLOGY.md`, etc.)
  - `v1.0.0-dec034`, `v0.1-phase0`, `v0.5-phase4-deep` — Phase 0 / Phase 4
    closeout tags from the research skill's OWN Version Tagging Protocol,
    created while working directory was mistakenly `qnfo-skills` instead of
    a project repo. Contained `PROJECT-PLAN.md`, `WBS-v2.0.md`,
    `silent-radix-cryptanalysis.md`, `review/red-team-audit-v2.md`,
    Core Pillar release PDFs, and alpha-pi-helix project files.
  - `archive/zitterbewegung-cosmology-research`, `archive/ultrametric-
    foundation-thesis` — pre-dated even ADR-026's existence; the latter
    contained an entire unrelated legacy website/CMS project (25 files:
    `hub.html`, `unified-api-gateway.js`, `qnfo-cms-client.js`, a thesis PDF).
  **Root cause:** git tags and GitHub Releases are independent of branch
  history — a force-push "clean" branch does not remove them, and neither
  remediation attempt checked `git tag -l` / `gh release list` against the
  new allowlist policy.
  **Fix:** All 6 tags verified as non-ancestors of clean `master` (confirmible
  via `git merge-base --is-ancestor <tag> origin/master`, exit 1 = not an
  ancestor = safe to delete). Full `git bundle` backup of all 6 tag refs
  created and uploaded to R2 (`qnfo-backups/qnfo-skills/orphaned-tags-2026-07-18.bundle`,
  MD5-verified) before deletion — zero data loss. GitHub Release "v1.0.0"
  deleted (Zenodo DOI, the actual durable publication record, is unaffected
  and still resolves at `doi.org/10.5281/zenodo.21366522`). All 6 tags deleted
  from origin via `git push --delete`. Stray fully-merged branch
  `feature/skills-9-consolidated` also deleted (verified ancestor of master
  first). Added the "Prohibited Git Metadata" section above plus an explicit
  pre-flight check in `research/SKILL.md`'s Phase Closeout Protocol to
  prevent recurrence.
