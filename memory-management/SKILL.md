---
name: memory-management
description: Guide the agent to recall, remember, and route durable learning into Memory, Skills, Scheduled Tasks, or Tape.
---

> **INCLUDES AUTONOMOUS RED-TEAM SELF-AUDIT.** Before claiming this skill complete, autonomously run: (1) Output Verification -- negative verification. (2) Assumption Challenge -- state and test every assumption. (3) Edge Case Check -- empty/null/max/boundary/desync. (4) DoD Integration -- run _dod_enforce.py if exists. (5) Iteration -- retry on failure, max 3. ANTI-PATTERN: User should NEVER ask about quality.

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
