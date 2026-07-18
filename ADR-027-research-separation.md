# ADR-027: Research Project File Separation

**Status:** Active (2026-07-18)
**Complements:** ADR-026 (qnfo-skills scope)

## Decision

All research project files — papers, WBS/project plans, distribution
artifacts, audit reports, data exports, and project-specific scripts — MUST
live in a repository separate from `QNFO/qnfo-skills`.

## Two Approved Patterns

| Pattern | When to use | Example |
|---|---|---|
| **Shared repo** `QNFO/qnfo-research` | Small/medium research outputs, cross-project scripts, papers not tied to one long-lived program | Core Pillar papers, distribution scripts, one-off whitepapers |
| **Dedicated repo** `QNFO/<project-name>` | Large, long-lived research programs with many files/versions | A hypothetical `QNFO/alpha-pi-helix` if that project's file count grows large enough to warrant isolation |

Both patterns are permitted. Projects MAY start in `qnfo-research` and graduate
to a dedicated repo later; this is a normal, expected evolution and does not
require an ADR update — only a note in the project's own README pointing to
its new location.

## Non-Negotiable Invariant

**Research and skills never share a repository, branch, or commit.** This is
enforced structurally in `qnfo-skills/.gitignore` (default-deny allowlist,
see ADR-026) in addition to being a written policy.

## Rationale

The 2026-07-18 incident showed that documentation-only policy (a sentence in
a skill's SKILL.md) is insufficient — commits still slipped through across
3 separate sessions/commits before being caught. Structural enforcement
(allowlist `.gitignore`) plus a documented ADR closes both the human-process
gap and the tooling gap.
