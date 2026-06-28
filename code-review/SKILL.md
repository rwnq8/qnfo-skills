---
name: code-review
description: Comprehensive code review assistant that analyzes code quality, security, and best practices. Use when user asks for code review, security audit, implementation feedback, or wants code quality assessment.
version: "2.0"
allowedTools:
  - read
  - exec
  - write
  - edit
---
> **INCLUDES AUTONOMOUS RED-TEAM SELF-AUDIT.** See RED-TEAM-PROTOCOL.md.


# CODE REVIEW SKILL — v2.0

> **On-demand skill.** Load via `skill_view('code-review')` for comprehensive code analysis.

---

## When to Use

| Trigger | Action |
|:--------|:-------|
| "Review this code" | Full review with all focus areas |
| "Security audit" | Focused on §2.3 (Security) + §2.5 (Dependencies) |
| "Performance review" | Focused on §2.4 (Performance) |
| "Is this good code?" | Lightweight review, §2.1 + §2.2 only |
| User submits a PR or diff | Full review against changed files |

---

## Workflow — 4 Phases

### Phase 1: Discovery

```bash
# Discover what's being reviewed
git diff --name-only          # Changed files in current branch
git log --oneline -5          # Recent commits for context
```
Use `exec` to discover project structure, dependencies, and test coverage.

### Phase 2: Analysis

For each file under review, analyze across ALL four focus areas:

### 2.1 Code Quality
- Readability: clear variable names, consistent style, logical flow
- Maintainability: DRY principle, modular functions, low coupling
- Naming: descriptive, consistent with project conventions
- Structure: logical file organization, appropriate abstraction level
- Comments: explain WHY, not WHAT; no stale/outdated comments

### 2.2 Best Practices
- Language idioms: uses the language's recommended patterns
- Design patterns: appropriate use (not over-engineered)
- Error handling: all error paths handled, no silent failures
- Logging: appropriate levels (DEBUG/INFO/WARN/ERROR), structured where needed
- Testing: edge cases covered, tests are readable and maintainable

### 2.3 Security
- Input validation: all external inputs validated and sanitized
- Injection prevention: SQL, command, path injection vectors closed
- Authentication: proper auth checks on all protected operations
- Data exposure: no secrets in code, logs, or error messages
- OWASP Top 10: check against current OWASP vulnerabilities
- Dependency audit: `pip audit` / `npm audit` for known CVEs

### 2.4 Performance
- Algorithm complexity: Big-O analysis for critical paths
- Memory: no leaks, appropriate data structure choices
- I/O: batching, connection pooling, lazy loading where appropriate
- Caching: appropriate use, cache invalidation strategy
- N+1 queries: no inefficient database access patterns

### Phase 3: Output Generation

Structure the review output as follows:

```markdown
# CODE REVIEW: [file/project name]
**Reviewer:** QNFO Agent | **Date:** YYYY-MM-DD | **Scope:** [files reviewed]

## Summary (2-3 sentences)
[What the code does, overall quality assessment, key risks]

## Issues Found

| # | Severity | File:Line | Issue | Recommendation |
|:--|:---------|:----------|:------|:---------------|
| 1 | CRITICAL | ... | ... | ... |
| 2 | MAJOR | ... | ... | ... |
| 3 | MINOR | ... | ... | ... |

### CRITICAL Issues
[Detailed analysis for each CRITICAL issue — must include specific code reference]

### MAJOR Issues
[Detailed analysis for each MAJOR issue]

### MINOR Issues
[Detailed analysis for each MINOR issue with suggested fixes]

## Positive Aspects
[3-5 things the code does well]

## Recommendations (Prioritized)
1. [Highest-priority fix with rationale]
2. [Next-priority fix]
...

## Dependency Health (if applicable)
[Audit results, known vulnerabilities, upgrade recommendations]
```

### Phase 4: Verification (Before Delivering Review)

1. **Evidence check:** Every CRITICAL/MAJOR issue cites a specific line or pattern
2. **False positive check:** Did I verify the issue actually exists by reading the code?
3. **Completeness:** Did I cover all four focus areas?
4. **Actionability:** Can the developer act on every recommendation without additional research?

---

## Severity Classification

| Severity | Definition | Examples |
|:---------|:-----------|:---------|
| **CRITICAL** | Security vulnerability, data loss risk, production outage risk | SQL injection, hardcoded secrets, infinite loop |
| **MAJOR** | Bug, significant performance issue, maintainability blocker | Memory leak, wrong algorithm, missing error handling |
| **MINOR** | Style inconsistency, minor optimization, documentation gap | Naming convention violation, missing comment |

---

## Anti-Patterns (Flag Immediately)

| Anti-Pattern | Signal |
|:-------------|:-------|
| **Hardcoded secrets** | API keys, tokens, passwords in source |
| **Bare except** | `except:` or `except Exception:` without specific types |
| **eval()/exec()** | Dynamic code execution on user input |
| **Unvalidated input** | No sanitization before SQL/filesystem/command use |
| **Silent error swallowing** | `except: pass` or `try: ... except: None` |
| **God function** | Function >200 lines with multiple responsibilities |

---

## Usage Examples

```python
# Trigger via: "Review the code in src/auth.py"
# Or: "Do a security audit of the API endpoints"
# Or: "Is this implementation good?" (lightweight review)
```

---

*code-review v2.0 — Comprehensive code quality, security, and best practices analysis. All output labeled [LLM-INFERRED] unless verified against execution evidence.*

## RT: RED-TEAM SELF-AUDIT

Before claiming this skill complete, autonomously run:

1. Output Verification (negative verification)
2. Assumption Challenge (state and test every assumption)
3. Edge Case Check (empty/null/max/boundary/desync)
4. DoD Integration (run _dod_enforce.py if exists)
5. Iteration (retry on failure, max 3)

ANTI-PATTERN: User should NEVER ask about quality.
Refer to RED-TEAM-PROTOCOL.md for full protocol.

