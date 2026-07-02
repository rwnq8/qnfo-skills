# Shared Loading Protocol

> **Loaded once per session by skill-autoloader Rule 0. All QNFO skills reference this instead of duplicating.**

---

## Programmatic Loading & Execution

This skill is loaded and executed **programmatically by the LLM system** during response generation. Loading is triggered automatically via `skill_view('<name>')` or `read()` with filesystem path. **The user NEVER manually loads this skill.** The `skill-autoloader` detects task patterns and handles all skill loading.

## Skill Loading Retry Protocol

If `skill_view('name')` fails during programmatic loading, the LLM system MUST execute this fallback chain:

1. **Retry 1:** `read('%USERPROFILE%\.deepchat\skills\<name>\SKILL.md')`
2. **Retry 2:** Pull from Cloudflare R2: `npx wrangler r2 object get qnfo/prompts/skills/<name>/SKILL.md --remote --file=_skill.md`
3. **Retry 3:** If R2 fails, search local filesystem for any cached copy
4. **Fallback:** If ALL retries fail, continue with `[SKILL-UNAVAILABLE: <name>]` and best-effort knowledge

**NEVER silently proceed without a skill's critical instructions.** If a skill is required for the task and cannot be loaded after 3 retries, escalate to the user with the specific failure reason.

## execute_plan (MANDATORY — Before Any Execution)

**This skill involves execution-heavy workflows.** Before executing, use update_plan to populate a concrete, verifiable checklist. Every item must be short, specific, and testable with tool evidence.

### Execution Protocol

1. **Populate update_plan** with workflow phases as concrete checklist items
2. **Execute one item at a time** — at most ONE in_progress
3. **Mark items completed ONLY with tool evidence** (Test-Path, exec output, git log)
4. **Never claim completion without execution evidence** — Rule 14 enforcement
5. **If blocked:** Flag as [BLOCKED: reason] and move to the next item
