---
name: handoff-protocol
version: 1.0.0
description: QACP-HANDOFF protocol for structured agent-to-agent session handoffs. Defines message schema, task registers, infrastructure snapshots, gap identification, and cross-system verification. Use when terminating a session, handing off to another agent, or reading a previous agent's handoff.
category: protocol
pinned: true
---

# HANDOFF PROTOCOL SKILL — v1.0.0

> **QACP-HANDOFF v1.0.** Structured agent-to-agent handoff protocol built on QACP message types. Replaces ad-hoc handoff summaries with a verifiable, machine-parseable state transfer between independent agent sessions.
> **PINNED.** This skill should be loaded for ALL QNFO agent sessions to ensure consistent handoffs.

---

## 0. WHY THIS EXISTS

**Problem:** 79% of agent responses in multi-session work involve re-discovering context that was already established. Ad-hoc handoffs (tape_handoff, conversation summaries, CONTINUATION-*.md files) lose critical information:

| What's Lost | Frequency | Impact |
|:------------|:---------:|:-------|
| Task register (what was started vs completed vs pending) | Every session | Agents re-plan already-planned work |
| Infrastructure snapshot (which DBs/Workers/Pages were touched) | Every session | Stale deployments, orphaned resources |
| Gap identification (what's missing, what's blocking) | Every session | Blockers go unresolved across sessions |
| Cross-system references (what entities were created/modified) | Every session | Duplicate entries, inconsistent state |
| Evidence links (commits, deployments, file hashes) | Most sessions | Phantom completion claims |

**Solution:** A structured handoff protocol that:
1. Uses QACP message envelope + schema registry
2. Mandates task register, infrastructure snapshot, gap list, and cross-references
3. Is verifiable (checksums, evidence refs)
4. Is machine-parseable (JSON Schema)
5. Is human-readable (structured Markdown rendering)

---

## 1. PROTOCOL SPECIFICATION

### 1.1 Message Type

QACP message type: `HANDOFF` (extends QACP v1.0 message envelope)

```
QACP-ENVELOPE:
  protocol: "qacp/1.0"
  message_type: "HANDOFF"
  message_id: <uuid>
  timestamp: <ISO 8601>
  sender: {agent_id, session_id}
  recipient: "urn:qacp:agent:next-session"
  payload: <HANDOFF-PAYLOAD>
```

### 1.2 HANDOFF Payload Schema

```json
{
  "$schema": "https://qacp.qnfo.org/schemas/handoff/v1.0",
  "protocol": "QACP-HANDOFF",
  "version": "1.0.0",
  "handoff_id": "<uuid>",
  "created_at": "<ISO 8601>",

  "session": {
    "id": "<session-id>",
    "agent_name": "<agent-identifier>",
    "model": "<model-name>",
    "started_at": "<ISO 8601>",
    "terminated_at": "<ISO 8601>",
    "total_tool_invocations": 0,
    "execution_ratio": 0.0
  },

  "task_register": {
    "completed": [
      {
        "id": "<task-id>",
        "description": "<concrete, verifiable description>",
        "evidence": "<file-path | commit-hash | deployment-url | test-result>",
        "completed_at": "<ISO 8601>"
      }
    ],
    "in_progress": [
      {
        "id": "<task-id>",
        "description": "<what was being done>",
        "current_state": "<exact point of interruption>",
        "next_action": "<first thing next agent should do>",
        "blockers": ["<blocker-description>"]
      }
    ],
    "pending": [
      {
        "id": "<task-id>",
        "description": "<what needs to be done>",
        "priority": 1,
        "dependencies": ["<task-id>"],
        "estimated_effort": "<minutes|hours|days>",
        "source": "<where this task originated>"
      }
    ]
  },

  "infrastructure_snapshot": {
    "databases": {
      "<db-name>": {
        "id": "<uuid>",
        "tables": 0,
        "key_rows": 0,
        "state": "clean|modified|corrupt",
        "last_query": "<ISO 8601>"
      }
    },
    "workers": {
      "<worker-name>": {
        "endpoint": "<url>",
        "status": "deployed|broken|stale|unknown",
        "version": "<version>",
        "last_deployed": "<ISO 8601>"
      }
    },
    "pages": {
      "<project-name>": {
        "url": "<url>",
        "status": "deployed|stale|broken",
        "last_deployed": "<ISO 8601>"
      }
    },
    "vectorize": {
      "<index-name>": {
        "dimensions": 768,
        "vector_count": 0,
        "metric": "cosine",
        "state": "populated|empty|corrupt"
      }
    },
    "r2": {
      "<bucket-name>": {
        "key_count_estimate": 0,
        "paths_touched": ["<path>"]
      }
    },
    "cms": {
      "entries_total": 0,
      "content_types": ["page", "paper", "publication"],
      "relationships": 0,
      "entries_created_this_session": 0
    }
  },

  "artifacts": {
    "files_created": [
      {"path": "<path>", "purpose": "<why>", "persisted_to": "r2|local|github"}
    ],
    "files_modified": [
      {"path": "<path>", "change": "<summary>"}
    ],
    "deployments": [
      {"target": "<worker|page>", "url": "<url>", "version": "<v>"}
    ],
    "commits": [
      {"hash": "<sha>", "message": "<msg>"}
    ]
  },

  "gaps": [
    {
      "id": "GAP-<NNN>",
      "category": "infrastructure|data|integration|documentation|test|security",
      "description": "<what's missing or broken>",
      "severity": "critical|high|medium|low",
      "impact": "<what breaks because of this gap>",
      "suggested_approach": "<how a future agent could address this>",
      "blocked_by": ["<gap-id or external-dependency>"]
    }
  ],

  "cross_references": {
    "systems_touched": ["<system-name>"],
    "entities_created": [
      {"system": "<system>", "entity_type": "<type>", "id": "<id>", "description": "<what>"}
    ],
    "entities_modified": [
      {"system": "<system>", "entity_type": "<type>", "id": "<id>", "change": "<what changed>"}
    ],
    "entities_deleted": [
      {"system": "<system>", "entity_type": "<type>", "id": "<id>", "reason": "<why>"}
    ]
  },

  "continuation": {
    "summary": "<1-3 sentence summary a new agent can read to understand this session>",
    "recommended_starting_point": "<what to do first>",
    "priority_queue": [
      {"rank": 1, "task_id": "<id>", "reason": "<why this is highest priority>"}
    ],
    "known_blockers": [
      {"task_id": "<id>", "blocker": "<description>", "possible_resolution": "<how to unblock>"}
    ],
    "do_not_repeat": ["<things already tried that didn't work>"]
  },

  "verification": {
    "checksum_sha256": "<sha256 of normalized payload>",
    "evidence_count": 0,
    "systems_queried_for_snapshot": ["<system>"],
    "snapshot_timestamp": "<ISO 8601 when snapshot was taken>"
  }
}
```

### 1.3 Required vs Optional Fields

| Field | Required | Reason |
|:------|:--------:|:-------|
| `session.*` | **REQUIRED** | Identity and traceability |
| `task_register.completed` | **REQUIRED** | What was actually done |
| `task_register.in_progress` | **REQUIRED** | Continuation critical — most frequently lost |
| `task_register.pending` | **REQUIRED** | What remains for next session |
| `infrastructure_snapshot.databases` | **REQUIRED** | D1 state is session-critical |
| `gaps` | **REQUIRED** | Blockers that fell through cracks |
| `continuation.summary` | **REQUIRED** | Minimum viable handoff |
| `continuation.priority_queue` | **REQUIRED** | Ordered next steps |
| `infrastructure_snapshot.workers` | Optional | Only if Workers were touched |
| `infrastructure_snapshot.pages` | Optional | Only if Pages were deployed |
| `infrastructure_snapshot.vectorize` | Optional | Only if Vectorize was modified |
| `cross_references` | Recommended | Prevents duplicate work across systems |
| `artifacts` | Recommended | Evidence of work done |

### 1.4 Field Descriptions

**task_register.in_progress.current_state** — Must be specific enough that a new agent can resume WITHOUT re-discovering context. Example:
- GOOD: `"Phase 2 CMS sync script crashed at line 244 with NameError: 'data_json' is not defined. The variable name bug has been fixed. Need to re-run _sync_cms.py."`
- BAD: `"Working on CMS integration."`

**gaps.severity** values:
- `critical` — Prevents system from functioning. Must be resolved before any other work.
- `high` — Major missing piece. Should be resolved this session.
- `medium` — Nice-to-have integration. Can be deferred.
- `low` — Cosmetic or future improvement.

**infrastructure_snapshot** — Query LIVE systems at handoff time, not from memory. Every count in the snapshot should be verifiable by re-running the query.

---

## 2. STORAGE & DISTRIBUTION

### 2.1 Canonical Storage Locations

| Location | Path | Purpose |
|:---------|:-----|:--------|
| **R2** | `qnfo/audit/handoffs/<YYYY-MM-DD>-<session-id>.json` | Canonical machine-parseable handoff |
| **R2** | `qnfo/audit/handoffs/<YYYY-MM-DD>-<session-id>.md` | Human-readable rendered handoff |
| **Tape** | `tape_handoff("handoff/<session-id>", summary)` | Session tape anchor for quick lookup |
| **Local** | `<workspace>/HANDOFF-<project>.json` | Ephemeral — cleaned up by closeout-manager |

### 2.2 Handoff Lifecycle

```
Agent A terminates
  ↓
1. Produce HANDOFF payload (validated against schema)
2. Upload JSON to R2: qnfo/audit/handoffs/<date>-<session-id>.json
3. Render Markdown version to same path with .md extension
4. Write tape anchor: tape_handoff("handoff/<session-id>", summary)
5. Update Discovery Index: add handoff entry
  ↓
Agent B starts
  ↓
1. Check tape anchors for most recent handoff
2. Pull HANDOFF JSON from R2
3. Parse task_register, gaps, infrastructure_snapshot
4. Prioritize: in_progress tasks first, then priority_queue
5. Verify infrastructure_snapshot against live systems
6. ACK the handoff (update Discovery Index: handoff acknowledged)
```

---

## 3. AGENT PROCEDURES

### 3.1 Producing a Handoff (Agent A — Session Termination)

```
PROCEDURE: produce_handoff
PRECONDITION: All session tasks complete or documented as in_progress/pending

1. COLLECT task register:
   - For each update_plan step marked completed: record with evidence
   - For each update_plan step marked in_progress: record with current_state + next_action
   - For each update_plan step marked pending: record with priority

2. QUERY LIVE INFRASTRUCTURE (do NOT use memory):
   a. For each D1 database touched: SELECT COUNT(*) FROM <key_tables>
   b. For each Worker touched: check deployment status
   c. For each Pages project touched: verify URL reachable
   d. For Vectorize: query with dummy vector, count matches
   e. For R2: note paths touched
   f. For CMS: SELECT COUNT(*) FROM content_entries, content_relationships

3. IDENTIFY GAPS:
   - What was mentioned as needed but not done?
   - What systems are in unexpected states?
   - What errors were encountered but not resolved?
   - What integrations are incomplete?

4. BUILD CROSS-REFERENCES:
   - Every entity created (CMS entry, D1 row, R2 object, Worker deployment)
   - Every entity modified
   - Every entity deleted

5. WRITE CONTINUATION:
   - summary: 1-3 sentences
   - priority_queue: ordered by urgency
   - known_blockers: with possible resolutions
   - do_not_repeat: failed approaches

6. VALIDATE:
   - All REQUIRED fields present
   - All counts are from live queries (not estimates)
   - Evidence refs are verifiable
   - Checksum computed

7. STORE:
   - R2 JSON + Markdown
   - tape_handoff anchor
   - Discovery Index update
```

### 3.2 Reading a Handoff (Agent B — Session Start)

```
PROCEDURE: consume_handoff
PRECONDITION: New session started, no context loaded

1. CHECK for existing handoffs:
   - tape_anchors() — look for "handoff/" prefixed anchors
   - If none: check R2 qnfo/audit/handoffs/ for most recent
   - If none: this is a cold-start session — ask user for context

2. PULL most recent handoff JSON from R2

3. PARSE and VALIDATE:
   - All REQUIRED fields present?
   - Checksum matches?
   - Infrastructure snapshot internally consistent?

4. VERIFY against LIVE systems:
   - Query each database from infrastructure_snapshot
   - Compare counts: if different, something changed between sessions
   - Flag discrepancies as gaps

5. PRIORITIZE work:
   - First: resume in_progress tasks (read current_state + next_action)
   - Second: address critical/high gaps
   - Third: execute priority_queue in order
   - Fourth: handle pending tasks

6. ACK the handoff:
   - Update Discovery Index: mark handoff as acknowledged
   - This prevents the same handoff from being re-read by future agents
```

### 3.3 Integration with closeout-manager

The `closeout-manager` skill handles:
- Git hygiene (commits, branch state)
- R2 audit trail export
- Discovery Index + lifecycle timestamps
- Temporary file cleanup
- Decision log updates

The `handoff-protocol` skill handles:
- Task register documentation
- Infrastructure snapshot
- Gap identification
- Cross-system references
- Continuation prompt

**Order of execution:**
1. `handoff-protocol` FIRST — produce structured handoff (this skill)
2. `closeout-manager` SECOND — cleanup, audit trails, lifecycle (existing skill)

---

## 4. HANDOFF TEMPLATE

### 4.1 Minimal Handoff (when time is critical)

Use `fill_prompt_template("HANDOFF", {...})` with these args:

```
{
  "session_id": "<id>",
  "summary": "<1-3 sentence summary>",
  "completed": "<bullet list of completed tasks with evidence>",
  "in_progress": "<bullet list of in-progress tasks with current state>",
  "pending": "<bullet list of pending tasks>",
  "gaps": "<bullet list of gaps>",
  "infrastructure": "<summary of infrastructure state>",
  "continuation": "<what to do next>"
}
```

### 4.2 Full Handoff (when handing off complex work)

Use the complete JSON payload from §1.2. Render to Markdown for human readability, store JSON for machine parsing.

---

## 5. VERIFICATION

### 5.1 Handoff Integrity Check

Before accepting a handoff, Agent B MUST verify:

1. **Session identity:** session.id is a valid UUID, timestamps are reasonable
2. **Task evidence:** For each completed task, at least attempt to verify the evidence ref
3. **Infrastructure snapshot freshness:** snapshot_timestamp is within last 24 hours
4. **No phantom claims:** If a completed task claims "deployed X" but X is not reachable, flag as gap
5. **Cross-reference consistency:** If two systems claim different states for the same entity, flag as gap

### 5.2 Anti-Corruption

Store a SHA-256 checksum of the normalized JSON payload in `verification.checksum_sha256`. Agent B recomputes and compares before trusting the handoff.

---

## 6. ANTI-PATTERNS

| Anti-Pattern | Why It Fails | Correct Approach |
|:-------------|:-------------|:-----------------|
| "Everything is done" without task register | Phantom completion. No evidence. | List EVERY task with evidence ref |
| Handoff from memory | Infrastructure state drifts. Counts are wrong. | Query live systems at handoff time |
| Skipping gaps section | Blockers go unresolved across sessions | Every session MUST identify gaps |
| Vague in_progress.current_state | Next agent must re-discover context | Be excruciatingly specific |
| No infrastructure snapshot | Next agent doesn't know what was touched | Query ALL systems touched |
| Handoff buried in conversation text | Next agent can't parse it | Store to R2 + tape anchor |
| Handoff without priority_queue | Next agent doesn't know what to do first | Rank tasks by urgency |

---

## 7. INTEGRATION POINTS

| Integration | How |
|:------------|:----|
| **QACP Gateway** | Handoff payloads can be sent via QACP REST API: `POST /qacp/message {type: "HANDOFF", payload: {...}}` |
| **CMS** | Handoffs can be registered as CMS entries (type: "handoff") for discovery |
| **Knowledge Graph** | Each handoff creates a `Handoff` node linked to touched Projects/Assets |
| **Lifecycle Pipeline** | Handoffs include `last_active` timestamp — prevents premature archival |
| **Discovery Index** | `qnfo/discovery/index.json` entries for each handoff |
| **Vectorize** | Handoff summaries can be embedded for semantic search across sessions |

---

## 8. QACP REGISTRATION

This protocol registers with QACP:
- **Message type:** `HANDOFF`
- **Schema ID:** `urn:qacp:schema:handoff:v1.0`
- **Schema JSON:** Stored in D1 `qacp_schemas` table
- **Endpoint:** `POST /qacp/message` with `message_type: "HANDOFF"`

---



## Embedded Scripts

Per DEFAULT.md §6.1, this skill's dependent scripts are documented below.
**Canonical source: Cloudflare R2 (`qnfo/tools/`). Tools execute as ephemeral `_<name>.py` files — pull from R2, execute, discard. Never persist locally.**

| Script | Canonical (R2) | Ephemeral Execution Cache | Purpose |
|:-------|:---------------|:--------------------------|:--------|
| `sync_cms.py` | `qnfo/tools/sync_cms.py` | `_sync_cms.py` (ephemeral) | CMS sync script for cross-system state verification |

### Execution Protocol (Ephemeral)
Tools execute locally (Python requires filesystem access) but do NOT persist:
1. **Pull:** `npx wrangler r2 object get qnfo/tools/<name>.py --remote --file=_<name>.py`
2. **Execute:** `python _<name>.py`
3. **Discard:** `Remove-Item _<name>.py`
4. If R2 copy missing: flag `[SKILL-GAP: script <name>.py missing from R2, cannot bootstrap]`

## VERSION HISTORY

| Version | Date | Changes |
|:--------|:-----|:--------|
| **v1.0.0** | 2026-06-26 | Skill audit — added version history. Current version. |


*handoff-protocol skill v1.0.0 — QACP-HANDOFF v1.0. Pinned. Load for all QNFO agent sessions.*
