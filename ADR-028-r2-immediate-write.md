# ADR-028: R2-Immediate-Write & Per-Turn Checkpoint Protocol

**Status:** Active (2026-07-18)
**Complements:** ADR-026 (qnfo-skills scope), ADR-021/ADR-025 (thin-client cleanup, referenced in git-github/SKILL.md)
**Applies to:** All QNFO agent sessions creating or editing project artifacts (research projects, audits, documentation, notes — anywhere outside `qnfo-skills`)

## Decision

**Local disk is EPHEMERAL. No project file is durably "saved" until it exists
on R2 (project artifacts) or has been pushed to GitHub (skill files, or
project files additionally tracked in git).** A file that exists only on
local disk, even for the duration of a single chat turn, is at risk and does
not count as saved for durability purposes.

**Durability is a PER-TURN property, not a per-session or per-phase one.**
Any tool call that creates or edits a project deliverable MUST be followed,
in the SAME turn, by an R2 upload of that file (`wrangler r2 object put ...
--remote`, upload-only, never `rclone sync`/mirror). Deferring this to
"session closeout" or "phase closeout" is the exact anti-pattern this ADR
exists to eliminate.

## Root Cause (Incident Record)

**2026-07-18:** The `qnfo-photon-audit` project (its own GitHub repo, 5
commits, 14 files, ~145 KB spanning Phase 0-2 across multiple chat turns)
existed ONLY on local disk (`C:\Users\<user>\Projects\qnfo-photon-audit\`)
with **zero R2 presence** for an entire session. This was discovered only
when the user directly questioned why project files were being read from
local disk instead of R2. Verified via `rclone lsf` returning empty for
every plausible R2 path before remediation.

Separately, in the same audit window, a duplicate `research-v2` skill
(SKILL.md + templates + scripts) was drafted local-only and never committed
to git — it no longer exists anywhere, having been superseded by a proper
merge into the canonical `research` skill (see this repo's commit history,
2026-07-18).

**Both incidents share one root cause:** the prior protocol (§8.5 JIT
Thin-Client Protocol) treated R2/git sync as an END-OF-SESSION or
END-OF-PHASE action. This created a large window — an entire session, or an
entire skill-drafting session — where multi-turn work existed in exactly one
place: local disk. That is precisely the failure mode §8.5 was written to
prevent, but the "when" was wrong.

## Fix

### 1. R2-Immediate-Write Mandate (HARD)
Every project artifact (PROJECT-PLAN.md, docs/*, artifacts/*, notebooks/*,
any file referenced in an `update_plan` step) gets an R2 upload in the SAME
turn it is created/edited — not batched, not deferred.

### 2. Per-Turn Checkpoint Protocol (HARD)
At the end of any turn touching project files:
1. `wrangler r2 object put` each changed file (upload-only, `--remote`)
2. `git add` + `git commit` in the project's own repo (feature branch, IRON RULE)
3. Verify: local `Test-Path` AND one R2 round-trip spot-check
4. Only after 1-3 succeed may the response claim the artifact "exists"

### 3. Phase-End Checkpoint (in addition to per-turn)
1. Confirm per-turn checkpoints already cover all files (should be redundant)
2. `git push origin <branch> --tags` to GitHub
3. Zenodo: create (first phase) or **new-version** (subsequent phases) a
   deposit — see `research/SKILL.md` "Zenodo Versioning for Phase/Session
   Conclusions." Never a disconnected new deposit for what is really the
   next phase of an existing project.
4. Log DOI + R2 paths + git tag to D1/working memory

### 4. Session/Project-Conclusion Checkpoint (final deliverables only)
1. All of the above already satisfied (not a substitute)
2. Build final-form PDF (Pandoc+XeLaTeX), attach to Zenodo deposit
3. Pin PDF to IPFS, record CID
4. Promote via social media (Buffer) — **for FINAL public deliverables only**,
   not every internal WBS phase transition (that is noise, not signal)

### 5. R2 Write Rule: Upload-Only, Never Sync/Mirror (carried forward from a
separate 2026-07-17 incident where `rclone sync` deleted R2 files because
local had already been cleaned up — alpha-pi-helix project data loss)
- NEVER use `rclone sync`, `aws s3 sync`, or any delete-capable mirror command
- ALWAYS use additive `wrangler r2 object put <bucket>/<key> --file=<path> --remote`
- `--remote` is REQUIRED — omitting it silently no-ops against a local
  Miniflare simulation instead of the real bucket
- Deleting an R2 object requires the same Production Immutability Gate as
  any other destructive action

### 6. Skill Files Follow the Same Rule
A drafted skill (SKILL.md + supporting files) not committed to its git repo
by end-of-turn is treated as not durably existing — same standard as project
artifacts, applied to `qnfo-skills`.

## Remediation Performed (same day)

- `qnfo-photon-audit` (14 files) uploaded to
  `primary-r2:qnfo-projects/qnfo-photon-audit/` — verified via `rclone check`:
  **0 differences, 13/13 matching files** (`.gitignore` excluded from R2 mirror
  by convention, tracked in git only).
- `qnfo-agent/SKILL.md` bumped v3.33 -> v3.34 with this protocol written in
  (§8.5 revision — R2-Immediate-Write, Per-Turn/Phase-End/Conclusion
  Checkpoint tiers, Upload-Only rule, expanded File Categories table).
- `research/SKILL.md` bumped v2.3 -> v2.4 with Zenodo Versioning subsection
  cross-referencing this protocol.
- This ADR created to give the policy a durable, discoverable record separate
  from the skill body (skills can be edited/superseded; ADRs are the
  incident-and-decision record).

## Non-Goals / Scope Notes

- This ADR does NOT change ADR-026 (qnfo-skills remains skills-only; project
  artifacts still never belong in `qnfo-skills`, they go to R2 + the
  project's own repo/`qnfo-research`).
- This ADR does NOT mandate git commits for every single R2 upload in
  lockstep — R2 is the durability backstop; git commits happen at the same
  per-turn cadence but are verified independently (§8.5 Per-Turn Checkpoint
  step 2).
- Ephemeral/scratch files (`_*` prefix, one-off calculation scripts) are
  explicitly EXEMPT from R2-Immediate-Write — they produce no durable
  artifact themselves by definition. If their OUTPUT is durable, the output
  gets its own R2 write; the scratch script itself does not.
