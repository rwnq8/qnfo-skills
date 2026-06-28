---
name: handoff-protocol
version: "1.1.0"
description: QACP-HANDOFF protocol for structured agent-to-agent session handoffs. Defines message schema, task registers, infrastructure snapshots, gap identification (with auto-detection and red-team testing), and cross-system verification. Use when terminating a session, handing off to another agent, or reading a previous agent's handoff.
category: protocol
pinned: true
---
> **INCLUDES AUTONOMOUS RED-TEAM SELF-AUDIT.** See RED-TEAM-PROTOCOL.md.


# HANDOFF PROTOCOL SKILL — v1.2.0

> **QACP-HANDOFF v1.2.** Structured agent-to-agent handoff protocol with auto-gap detection, red-team verification, AND mandatory copy-paste continuation prompts.
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

### 1.6 CONTINUATION PROMPT (REQUIRED — v1.2)

**Every handoff MUST include a verbatim copy-paste continuation prompt** that the user can paste directly into a new LLM session. This eliminates the #1 handoff failure mode: the next agent having to re-discover context.

#### 1.6.1 Format Requirements

The continuation prompt MUST be:

1. **In a code block** — triple-backtick fenced, no language tag, easily copyable
2. **Verbatim-executable** — copy/paste into a new session and the agent should know EXACTLY what to do
3. **Self-contained** — includes the HANDOFF file path to read, the DoD enforcement command, and the priority queue
4. **Specific** — names concrete files, commands, and URLs. No "fix the CMS" — must be "RUN _dod_enforce.py TO VERIFY, THEN..."
5. **Prioritized** — tasks listed in execution order with explicit dependencies

#### 1.6.2 Required Elements

```
REQUIRED in every continuation prompt:
  ☐ HANDOFF file path (e.g., "projects/cms/HANDOFF.md")
  ☐ DoD enforcement command (e.g., "RUN python _dod_enforce.py BEFORE CLOSEOUT")
  ☐ Priority queue (ranked list of next actions, most urgent first)
  ☐ Infrastructure verification step (what to check before executing)
  ☐ Critical blockers (what's currently broken and how to diagnose)
  ☐ Evidence requirement reminder (every claim needs tool output)

OPTIONAL elements:
  ☐ Specific commands to run (copy-paste executable)
  ☐ URLs to verify (live site checks)
  ☐ Version numbers to confirm (CMS v2.3, Ask QWAV v2.1, etc.)
  ☐ Expected state after completion (what success looks like)
```

#### 1.6.3 Example (from production handoff 2026-06-28)

```
LOAD ALL QNFO SKILLS. CONTINUE FROM HANDOFF IN projects/cms/HANDOFF.md. 

RUN python _dod_enforce.py TO VERIFY INFRASTRUCTURE STATE, THEN EXECUTE:

1. VERIFY all 7 Pages sites render correct content with CMS Client JS v2.7 and LP sections
2. PURGE Cloudflare CDN cache for laws.qnfo.org (stale content)
3. BATCH-IMPORT remaining Living Papers as CMS publications (72 done, ~383 pending)
4. SEED Vectorize paper-similarity index with Workers AI embeddings for all 455 papers
5. CREATE dedicated Pages projects for benchmark.qnfo.org, knowing.qnfo.org, solo.qnfo.org
6. ASSIGN DOIs to remaining 449 papers via Zenodo API
7. RUN python _dod_enforce.py before closeout — exit 0 required

CRITICAL: Every action must have verification evidence. No claim without tool output.
```

**Violation:** If a handoff is produced WITHOUT a continuation prompt in a copy-paste code block → the handoff is INCOMPLETE. Do not close the session until this is added.

The `gaps` array in the handoff payload is REQUIRED, but filling it has historically been ad-hoc — agents listed obvious blockers and missed subtle gaps. This section defines structured triggers that auto-populate the gaps list.

#### 1.5.1 Automatic Gap Detection (Run at Handoff Time)

Before writing the handoff, query these patterns and auto-populate gaps:

**A. CROSS-SYSTEM DESYNC DETECTION**
| Check | If this fails... | Gap ID | Severity |
|:------|:-----------------|:--------|:---------|
| GitHub HEAD == local HEAD | Commit not pushed | GAP-SYNC-001 | CRITICAL |
| R2 file count == expected count | R2 sync incomplete | GAP-SYNC-002 | HIGH |
| DI timestamp >= session start | DI not updated | GAP-SYNC-003 | HIGH |
| Bootstrap tools exist on R2 | No recovery path | GAP-SYNC-004 | HIGH |

**B. PATH DRIFT DETECTION**
- Scan ALL local scripts for references to wrong paths (e.g., `.deepchat\skills` instead of `DeepChat\skills`)
- If any found → GAP-DRIFT-001 (HIGH)
- Compare SKILL.md code examples against actual paths — mismatches → GAP-DRIFT-002 (MEDIUM)

**C. ORPHAN RESOURCE DETECTION**
- Orphaned `_*` files in working directory → GAP-ORPHAN-001 (LOW)
- `__pycache__` directories → GAP-ORPHAN-002 (LOW)
- Background processes still running → GAP-ORPHAN-003 (MEDIUM)

**D. RED-TEAM VERIFICATION PATTERNS (v1.1 — Actively try to break claims)**

Before writing the handoff, actively attempt to INVALIDATE the following claims:

| Claim | Red-Team Test | Gap if Fails |
|:------|:-------------|:-------------|
| "R2 sync is complete" | Pick 3 random files, GET them from R2 | GAP-RT-001 |
| "GitHub is pushed" | `git ls-remote origin` — verify hash | GAP-RT-002 |
| "Token is valid" | Run an actual PUT to R2 (not just whoami) | GAP-RT-003 |
| "All tasks executed" | For each [COMPLETED] task, verify evidence still exists | GAP-RT-004 |
| "No phantom claims" | Scan response history for "I will" / "Let me" without tool evidence | GAP-RT-005 |

**RED-TEAM RULE:** If ANY red-team test fails → the handoff is PREMATURE. Fix the gap BEFORE writing the handoff.

#### 1.5.2 Gap Auto-Population Protocol

When producing a handoff:

1. **Run the gap audit from closeout-manager §2.6** — this populates categories A-F
2. **Convert each finding to a gap entry** in the handoff's `gaps` array
3. **Run red-team tests** (§1.5.1 D) — convert each failure to a gap entry
4. **Classify severity** per closeout-manager §2.6.3
5. **If any CRITICAL gap exists** → BLOCK the handoff. Fix the gap first.

#### 1.5.3 Gap Entry Template

```json
{
  "id": "GAP-<CATEGORY>-<NNN>",
  "category": "sync|drift|orphan|red-team|infrastructure|test",
  "description": "<concrete, verifiable description of what's wrong>",
  "severity": "critical|high|medium|low",
  "impact": "<what breaks because of this gap>",
  "detection_method": "auto|red-team|user-reported",
  "suggested_approach": "<how a future agent could address this>",
  "blocked_by": ["<gap-id or external-dependency>"],
  "detected_at": "<ISO 8601>"
}
```

**New fields (v1.1):**
- `detection_method` — was this found automatically, via red-team testing, or because the user had to ask?
- `detected_at` — timestamp when the gap was identified

**USER-REPORTED gaps are a FAILURE of the auto-detection system.** If `detection_method` is `"user-reported"` → the gap audit protocol failed. Flag for Kaizen improvement.

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

*handoff-protocol skill v1.1.0 — QACP-HANDOFF v1.1. Auto-gap detection, red-team verification. Pinned. Load for all QNFO agent sessions.*

## RT: RED-TEAM SELF-AUDIT

Before claiming this skill complete, autonomously run:

1. Output Verification (negative verification)
2. Assumption Challenge (state and test every assumption)
3. Edge Case Check (empty/null/max/boundary/desync)
4. DoD Integration (run _dod_enforce.py if exists)
5. Iteration (retry on failure, max 3)

ANTI-PATTERN: User should NEVER ask about quality.
Refer to RED-TEAM-PROTOCOL.md for full protocol.

