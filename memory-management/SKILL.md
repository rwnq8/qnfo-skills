---
name: memory-management
description: Guide the agent to recall, remember, and route durable learning into Memory, Skills, Scheduled Tasks, or Tape. Use when user says "remember this," "recall previous work," "save this for later," "what do you know about," "continue where we left off," "memory," or when a task produces knowledge that should persist across sessions.
version: "1.2"
---

> **INCLUDES AUTONOMOUS RED-TEAM SELF-AUDIT.** Before claiming this skill complete, autonomously run: (1) Output Verification -- negative verification. (2) Assumption Challenge -- state and test every assumption. (3) Edge Case Check -- empty/null/max/boundary/desync. (4) DoD Integration -- verify all criteria met with tool evidence. (5) Iteration -- retry on failure, max 3. ANTI-PATTERN: User should NEVER ask about quality.

### Programmatic Loading & Execution
This skill is loaded and executed **programmatically by the LLM system** 
during response generation. Loading is triggered automatically via 
`skill_view('memory-management')` or `read()` with filesystem path.
**The user NEVER manually loads this skill.** The `skill-autoloader` 
detects task patterns and handles all skill loading. If this skill fails 
to load, the LLM system automatically retries via the fallback chain 
documented below.
**Pinning:** This skill is [On-demand — loads when triggered by task patterns].

### Skill Loading Retry Protocol
If `skill_view('name')` fails during programmatic loading, the LLM system 
MUST execute this fallback chain:
1. **Retry 1:** `read('%USERPROFILE%\.deepchat\skills\<name>\SKILL.md')`
2. **Retry 2:** Pull from Cloudflare R2: `npx wrangler r2 object get 
   qnfo/prompts/skills/<name>/SKILL.md --remote --file=_skill.md`
3. **Retry 3:** If R2 fails, search local filesystem for any cached copy
4. **Fallback:** If ALL retries fail, continue with `[SKILL-UNAVAILABLE: <name>]` 
   and best-effort knowledge
**NEVER silently proceed without a skill's critical instructions.** If a skill 
is required for the task and cannot be loaded after 3 retries, escalate to 
the user with the specific failure reason.

---

> **Related:** qnfo-agent
## execute_plan (MANDATORY -- Before Any Execution)

**This skill involves execution-heavy workflows.** Before executing, use update_plan to populate a concrete, verifiable checklist. Every item must be short, specific, and testable with tool evidence.

### Execution Protocol

1. **Populate update_plan** with workflow phases as concrete checklist items
2. **Execute one item at a time** -- at most ONE in_progress
3. **Mark items completed ONLY with tool evidence** (Test-Path, exec output, git log)
4. **Never claim completion without execution evidence** -- Rule 14 enforcement
5. **If blocked:** Flag as [BLOCKED: reason] and move to the next item

### Example Plan

update_plan([
  {"step": "Identify what to remember from current session", "status": "pending"},
  {"step": "Route to appropriate store (Memory, Skill, Scheduled Task, Tape)", "status": "pending"},
  {"step": "Create durable learning artifact", "status": "pending"},
  {"step": "Verify storage and retrieval", "status": "pending"}
])


# Memory Management

> **Version:** v1.0 (Kaizen-audited 2026-07-05)

> **Version:** v1.0 (Kaizen-audited 2026-07-05)


Use this skill when a task may produce durable learning or when the user asks you to recall, remember, continue earlier work, preserve an exact statement, capture a reusable procedure, or handle a recurring need.

## Recall

Rely on automatic memory injection for ordinary context. Use `memory_recall` when the user refers to previous work with cues such as again, last time, before, continue, same project, remember, or asks what you already know.

Use `tape_search` and then `tape_context` when the user needs source evidence, exact wording, logs, command output, file snippets, or why a prior decision was made. Memory is a durable conclusion layer, not the raw transcript.

## Remember

Use `memory_remember` only for durable conclusions that should change future behavior. Choose the most specific category:

- `user_preference`: stable user preferences, constraints, communication style, environment choices.
- `project_fact`: durable project conventions, architecture entry points, commands, dependencies, paths, or operational constraints.
- `task_outcome`: completed, blocked, or deliberately deferred task results. Include status, outcome, and blocker in prose when relevant.
- `heuristic`: reusable troubleshooting strategy, workflow, decision rule, or engineering lesson.
- `anti_pattern`: repeated mistake, unsafe approach, brittle pattern, stale assumption, or thing to avoid.

Do not remember raw tool results, bash output, grep output, file contents, transient mechanics, one-off failures, secrets, credentials, hidden reasoning, or anything only useful for the current turn.

## Verbatim Scope

Store exact wording only when the user explicitly asks you to remember a sentence or phrase verbatim. In that case, keep the requested text intact and make the surrounding content minimal.

Automatic extraction is different: it should normalize durable facts into concise memory content, deduplicate related entries, and avoid preserving raw transcript text.

## Procedures -> Skill

When the useful learning is a reusable multi-step procedure, prefer drafting a skill with `skill_manage` instead of stuffing the full procedure into Memory. Memory may keep a short pointer or heuristic, but the repeatable workflow belongs in a Skill.

Use `skill_manage` for draft skills only. Do not modify installed skills unless the user explicitly asks through the supported review flow.

## Recurring -> Scheduled Task

When the user asks for a periodic, low-frequency, or future recurring action, suggest creating a Scheduled Task in settings. Memory does not wake the agent, schedule future work, or create automation side effects.

## End-of-task Learning Check

Before finishing a non-trivial task, check whether there is one durable lesson to save:

1. Did the user reveal a stable preference or constraint?
2. Did you learn a durable project fact?
3. Is there a task outcome, blocker, or explicit deferral worth preserving?
4. Did a reusable heuristic work?
5. Did an anti-pattern or stale assumption become clear?
6. Is this actually a reusable procedure for `skill_manage` or a recurring need for Scheduled Tasks rather than Memory?

Remember only the smallest durable conclusion. Leave raw process in Tape.
## Handoff Protocol (MANDATORY at Closeout)

1. **Verify** ALL execute_plan items marked [EXECUTED] with tool evidence (Test-Path, exec output, git log)
2. **Archive** session artifacts to R2 canonical storage: `npx wrangler r2 object put qnfo/audit/... --remote --file=<artifact>`
3. **Generate** continuation prompt documenting pending work and current state for the next session
4. **Clean up** ephemeral _* files and __pycache__ directories: `Remove-Item _* -Recurse -Force`

### Continuation Prompt Template
```
TASK: [description of pending work from execute_plan]
STATE: [current state — what's executed, what's blocked, why]
NEXT: [first executable action for the next session]
R2: [canonical path for session artifacts]
```


## Closeout Protocol (MANDATORY)

Before declaring this skill workflow complete:
1. **Task Execution Verification:** Compare planned tasks ([PENDING] in execute_plan) vs executed tasks ([EXECUTED] with evidence)
2. **Filesystem Verification:** `Test-Path <file>` for every file claimed as created/modified. Never claim from memory.
3. **Git Verification:** `git log -1 --oneline` for every commit claimed. Verify commit hash exists.
4. **R2 State Upload:** Upload session audit trail to `qnfo/audit/` — conversations, decisions, state files.
5. **Discovery Index Update:** Update `qnfo/discovery/index.json` with any new resources created, projects modified, or publications generated.
6. **Ephemeral Cleanup:** Delete ALL _* prefixed files and __pycache__ directories. Session is not complete until `Get-ChildItem -File -Name | Where-Object { $_ -match '^_' }` returns zero results.


### Additional Execute Plan (Expanded)

```python
update_plan([
  {"step": "Identify what to remember from current session", "status": "pending"},
  {"step": "Route to appropriate store (Memory, Skill, Scheduled Task, Tape)", "status": "pending"},
  {"step": "Create durable learning artifact with proper category", "status": "pending"},
  {"step": "Verify storage and retrieval — Test-Path or API query", "status": "pending"},
  {"step": "Generate session handoff documenting pending learnings", "status": "pending"},
])
```
