---
name: code
description: Code quality review, security audit, and MCP server building. Analyze code for quality/security/anti-patterns with specific line numbers. Build MCP servers in Python (FastMCP) or Node/TypeScript (MCP SDK) for integrating external APIs. Deploy MCP servers as Cloudflare Workers when possible.
version: "2.1"
triggers: ["code review", "security audit", "code quality", "best practices", "anti-pattern", "review this code", "audit this", "MCP", "Model Context Protocol", "FastMCP", "MCP server", "API integration", "tool building", "external API", "MCP SDK", "type safety", "SQL injection", "secrets", "race condition", "error handling", "code smell", "refactor"]
related: ["cloudflare"]
priority: 2
platform: all
autonomous: false
self_sufficient: true
---

# CODE -- v2.1 (Ultra-Consolidated Review + MCP)

> **v2.1 UPDATE (2026-07-21, phantom-claim audit):** Added the
> **Tool-Call Execution Mandate** section below. A code review finding or
> an MCP tool description is NOT verified until the code has actually been
> read/run/tested via a tool call in this turn — "this looks correct" is
> not a review, and "the tool should return X" is not a working MCP server.

> **Merges 2:** code-review + mcp-builder
> **Related:** Load `cloudflare` for deploying MCP servers as Workers with D1/R2/KV/Vectorize bindings.
> **Cloudflare Full-Stack:** All MCP servers deploy as Cloudflare Workers. Code reviews consider Workers/D1/R2 integration. No standalone servers.

## execute_plan

update_plan([
  {"step": "Identify operation: code review or MCP server build", "status": "pending"},
  {"step": "Read the target code files completely -- never review without reading", "status": "pending"},
  {"step": "Execute review or build with proper tooling", "status": "pending"},
  {"step": "Verify: all quality gates pass, tests run, MCP tools respond correctly", "status": "pending"},
])

---

## Tool-Call Execution Mandate (Anti-Phantom Gate — MANDATORY)

A finding, fix, or MCP tool claim without an invoked tool call showing
actual output is a PHANTOM CLAIM (`qnfo-agent` §9.11 Rule 14) — BLOCKED.

1. **Code review** — every file MUST be `read` in this turn before a finding is reported; never review "from memory" of an earlier turn or from the diff summary alone. If the language toolchain is available, actually run the linter/type-checker/build (`tsc --noEmit`, `eslint`, `pytest`, etc.) and show the exit code and output rather than asserting "this compiles" or "tests would pass".
2. **MCP server build** — after writing a tool, actually invoke it (via the MCP client/test harness or a direct function call) and show the real response. "The tool should return the papers list" is a phantom claim until a real call returns real JSON.
3. **Security/quality findings** — cite the exact line number from the `read` output, not a paraphrase; do not report a vulnerability class without pointing at the specific line that exhibits it.
4. If a build/test/lint tool is unavailable in this environment, the response MUST say `[NOT-VERIFIED: no toolchain available]` instead of "passes" or "verified".

---

## Code Review

### Severity Classification
| Severity | Definition | Action Required | Example |
|:---------|:-----------|:----------------|:--------|
| **CRITICAL** | Security vulnerability, data loss, production outage, token exposure | Fix immediately, block all deployment | Hardcoded API key, SQL injection, no auth on admin endpoint |
| **HIGH** | Functional bug, performance degradation, type safety violation | Fix before merge | Missing null check causing crash, N+1 query, `any` type on public API |
| **MEDIUM** | Code smell, missing error handling, inconsistent patterns | Fix this session | Empty catch block, missing input validation, no retry on transient failure |
| **LOW** | Style, formatting, documentation gaps | Note, fix when convenient | Missing JSDoc, inconsistent naming, dead code |

### Pre-Review Protocol
1. **Read every file** being reviewed -- NEVER review from memory or assumptions
2. **Understand the architecture** -- what does this code do? What are its dependencies?
3. **Run the code** if possible -- verify it compiles/executes before reviewing
4. **Check git history** -- what changed? Why?
5. **Review tests** -- do they exist? Do they pass? Do they cover edge cases?

### Review Checklist (6 domains)

#### 1. Security (CRITICAL if any hit)
```
SEC-01: Hardcoded secrets / API keys / tokens in source code
SEC-02: SQL injection -- string concatenation in queries instead of parameterized
SEC-03: XSS -- unsanitized user input rendered in HTML
SEC-04: Path traversal -- user input used in file paths without sanitization
SEC-05: Missing authentication on sensitive endpoints
SEC-06: Missing authorization checks (any user can access any resource)
SEC-07: CORS misconfiguration (wildcard origin with credentials)
SEC-08: Sensitive data in logs or error messages
SEC-09: Insecure deserialization (pickle, eval, JSON.parse on untrusted input)
SEC-10: Missing CSRF protection on state-changing operations
```

#### 2. Type Safety
```
TYP-01: `any` type without documented justification
TYP-02: Missing type annotations on public function signatures
TYP-03: Type assertion (`as Type`) without runtime validation
TYP-04: Union types not narrowed before use
TYP-05: Optional chaining without fallback handling
TYP-06: Array/object destructuring without default values for optional fields
```

#### 3. Error Handling
```
ERR-01: Empty catch block `catch(e){}` -- silent error swallowing
ERR-02: Catching `Exception` or `any` without re-throwing or logging
ERR-03: No retry logic for transient failures (network, rate limit, timeout)
ERR-04: Error messages expose internal state (stack traces, DB queries, file paths)
ERR-05: No timeout on external API calls -- potential hang
ERR-06: Async function without try/catch or .catch() handler
```

#### 4. Concurrency & State
```
CON-01: Race condition -- read-modify-write without lock or transaction
CON-02: Durable Objects -- assuming single-instance without idempotency
CON-03: KV -- assuming strong consistency (KV is eventually consistent)
CON-04: D1 -- missing transaction for multi-statement writes
CON-05: Queue -- message not idempotent (duplicate delivery causes double-processing)
CON-06: Shared mutable state without synchronization
```

#### 5. Cloudflare-Native
```
CF-01: Workers -- no cold start awareness (heavy init in global scope)
CF-02: D1 -- missing indexes on frequently queried columns
CF-03: R2 -- `qnfo/` prefix inside `qnfo` bucket (creates `qnfo/qnfo/...` paths)
CF-04: KV -- listing keys (>1000) without pagination
CF-05: Vectorize -- dimension mismatch between embedding model and index
CF-06: Pages -- per-publication Pages project (use Workers + D1 instead)
CF-07: Wrangler.jsonc -- missing bindings for used services
CF-08: Workers -- exceeding 128MB memory limit
CF-09: Workers -- CPU time > 30s (default limit) without planning
```

#### 6. Performance
```
PRF-01: N+1 queries -- querying inside a loop instead of batching
PRF-02: Unbounded loop without exit condition or timeout
PRF-03: Large response bodies without streaming or pagination
PRF-04: Synchronous blocking operation in async context
PRF-05: Excessive logging in production (costs compute + storage)
PRF-06: No caching for frequently accessed/static data
```

### Output Format (MANDATORY)
Every finding MUST use this exact format:
```
[SEVERITY] <filepath>:<line_number> -- <one-line description>
  Root cause: <why this is a problem>
  Fix: <specific remediation>
  Example: <code showing the fix>
```

Example:
```
[CRITICAL] src/auth.ts:42 -- Hardcoded API token in source code
  Root cause: Plain-text Cloudflare API token embedded in source. If committed to git, token is permanently exposed in git history.
  Fix: Move to environment variable. Use `env.CLOUDFLARE_API_TOKEN` from wrangler.jsonc binding.
  Example:
    // BEFORE (vulnerable):
    const token = "cfat_abc123def456";
    // AFTER (secure):
    const token = env.CLOUDFLARE_API_TOKEN;
```

```
[HIGH] src/api.ts:87 -- N+1 query pattern in paper listing endpoint
  Root cause: For each paper, a separate D1 query fetches the author. With 100 papers, this is 101 queries.
  Fix: Batch the author fetch. Use a single D1 query with JOIN or WHERE id IN (...).
  Example:
    // BEFORE:
    for (const paper of papers) {
      paper.author = await db.prepare("SELECT name FROM authors WHERE id = ?").bind(paper.authorId).first();
    }
    // AFTER:
    const authorIds = papers.map(p => p.authorId);
    const authors = await db.prepare("SELECT id, name FROM authors WHERE id IN (" + authorIds.map(() => '?').join(',') + ")").bind(...authorIds).all();
    const authorMap = Object.fromEntries(authors.map(a => [a.id, a.name]));
    papers.forEach(p => p.author = authorMap[p.authorId]);
```

### Common Anti-Patterns by Language

#### TypeScript
```typescript
// ❌ BAD: any type
function process(data: any): any { return data.value; }

// ✅ GOOD: proper types
interface DataShape { value: string; count: number; }
function process(data: DataShape): string { return data.value; }

// ❌ BAD: unsafe optional chaining without fallback
const name = user?.profile?.name; // name is string | undefined

// ✅ GOOD: with fallback
const name = user?.profile?.name ?? "Unknown User";

// ❌ BAD: type assertion without validation
const data = response as ApiResponse;
// ✅ GOOD: runtime validation
if (!isApiResponse(response)) throw new Error("Invalid response");
const data = response;
```

#### Python
```python
# ❌ BAD: bare except
try:
    result = api_call()
except:
    pass

# ✅ GOOD: specific exception with logging
try:
    result = api_call()
except RequestException as e:
    logger.error(f"API call failed: {e}")

# ❌ BAD: mutable default argument
def append_to(value, items=[]):
    items.append(value)
    return items

# ✅ GOOD: None default
def append_to(value, items=None):
    if items is None:
        items = []
    items.append(value)
    return items

# ❌ BAD: f-string with user input in SQL
cursor.execute(f"SELECT * FROM users WHERE id = '{user_input}'")

# ✅ GOOD: parameterized query
cursor.execute("SELECT * FROM users WHERE id = ?", (user_input,))
```

---

## MCP Server Building

### Architecture Decision (HARD RULE)
ALL MCP servers deploy as Cloudflare Workers. No standalone servers, no Docker containers, no VPS. Rationale:
- Edge latency (<50ms cold start at 250+ locations)
- D1/R2/KV/Vectorize native bindings -- no separate database infrastructure
- Automatic HTTPS, WAF, DDoS protection
- Zero server maintenance -- no patching, no uptime monitoring
- Observability via Workers Analytics Engine
- 100K requests/day free tier, $0.30/million after

### Python (FastMCP) Complete Example

```python
# server.py -- Deploy as Cloudflare Worker
from fastmcp import FastMCP
from typing import Optional, List, Dict, Any
import json
import os

# Initialize with name and description
mcp = FastMCP(
    name="qno-research-mcp",
    description="QNFO Research MCP Server -- search papers, query knowledge graph, manage memories"
)

# ---------------------------------------------------------------------------
# Tool: search_papers
# ---------------------------------------------------------------------------
@mcp.tool()
def search_papers(
    query: str,
    limit: Optional[int] = 10,
    source: Optional[str] = "all"
) -> str:
    """Semantic search across QWAV research papers using Vectorize.

    This tool searches the QNFO paper corpus using 768-dimensional vector embeddings
    for meaning-based similarity (not keyword matching). Supports filtering by source.

    Args:
        query: Natural language search query describing what you want to find.
               Example: "room temperature quantum coherence in biological systems"
        limit: Maximum number of results to return (1-50, default 10).
               Higher values return more results but may include less relevant papers.
        source: Filter by paper source. Options: "all" (default), "arxiv", "zenodo", "manual".
                Use "all" to search across the entire corpus.

    Returns:
        JSON array of paper objects, each containing:
        - slug: Paper identifier (e.g., "quantum-laws-of-form-v2")
        - title: Paper title
        - score: Similarity score (0-1, higher = more relevant)
        - snippet: Relevant excerpt from the paper body
        - doi: Digital Object Identifier (if published)
        - published_at: ISO 8601 publication date

    Error Handling:
        - Returns {"error": "message", "results": []} if query is empty or invalid
        - Returns {"error": "message", "results": []} if search service is unavailable
        - Returns empty results array if no papers match the query

    Examples:
        search_papers(query="quantum error correction topological", limit=5)
        search_papers(query="adelic physics", limit=10, source="zenodo")
    """
    # Validate inputs FIRST -- before any business logic
    if not query or len(query.strip()) == 0:
        return json.dumps({
            "error": "query parameter is required and must be non-empty",
            "results": []
        })

    if limit is not None and (limit < 1 or limit > 50):
        return json.dumps({
            "error": f"limit must be between 1 and 50, got {limit}",
            "results": []
        })

    valid_sources = ["all", "arxiv", "zenodo", "manual"]
    if source and source not in valid_sources:
        return json.dumps({
            "error": f"source must be one of {valid_sources}, got '{source}'",
            "results": []
        })

    # Execute search
    try:
        results = perform_vector_search(
            query=query.strip(),
            limit=min(limit or 10, 50),
            source_filter=source
        )
        return json.dumps({
            "results": results,
            "count": len(results),
            "query": query.strip()
        })
    except Exception as e:
        return json.dumps({
            "error": f"Search failed: {str(e)}",
            "results": []
        })


# ---------------------------------------------------------------------------
# Tool: get_paper
# ---------------------------------------------------------------------------
@mcp.tool()
def get_paper(slug: str, include_body: Optional[bool] = True) -> str:
    """Get full paper details including body content from D1 living-paper database.

    Retrieves complete paper metadata and optionally the full markdown body.
    Use this after search_papers to read a specific paper in detail.

    Args:
        slug: Paper identifier (e.g., "quantum-laws-of-form-v2").
              Must be an exact match -- use search_papers first to find the slug.
        include_body: Whether to include the full markdown body in the response.
                      Set to False for metadata-only queries (faster, smaller response).

    Returns:
        JSON object with paper details:
        - slug: Paper identifier
        - title: Full paper title
        - author: Author name
        - abstract: Paper abstract (first 500 chars of body if no explicit abstract)
        - body: Full markdown body (only if include_body=True)
        - doi: Digital Object Identifier
        - published_at: ISO 8601 publication date
        - updated_at: ISO 8601 last update date
        - pages_url: Live URL on papers.qnfo.org
        - zenodo_url: Zenodo record URL

    Error Handling:
        - Returns {"error": "Paper not found: <slug>"} if slug doesn't exist
        - Returns {"error": "slug parameter is required"} if slug is empty

    Examples:
        get_paper(slug="quantum-laws-of-form-v2")
        get_paper(slug="cfpe-forecast-stages3-5", include_body=False)
    """
    if not slug or len(slug.strip()) == 0:
        return json.dumps({"error": "slug parameter is required"})

    try:
        paper = fetch_paper_from_d1(slug.strip())
        if not paper:
            return json.dumps({"error": f"Paper not found: {slug}"})

        result = {
            "slug": paper["slug"],
            "title": paper["title"],
            "author": paper.get("author", "Unknown"),
            "abstract": paper.get("abstract", paper.get("body", "")[:500]),
            "doi": paper.get("doi"),
            "published_at": paper.get("published_at"),
            "updated_at": paper.get("updated_at"),
            "pages_url": f"https://papers.qnfo.org/papers/{paper['slug']}/",
            "zenodo_url": f"https://doi.org/{paper['doi']}" if paper.get("doi") else None
        }

        if include_body:
            result["body"] = paper.get("body", "")

        return json.dumps(result)
    except Exception as e:
        return json.dumps({"error": f"Failed to fetch paper: {str(e)}"})


# ---------------------------------------------------------------------------
# Tool: query_graph
# ---------------------------------------------------------------------------
@mcp.tool()
def query_graph(
    endpoint: str,
    params: Optional[Dict[str, Any]] = None
) -> str:
    """Query the QNFO Knowledge Graph for ecosystem discovery and impact analysis.

    The Knowledge Graph contains 3,242+ nodes and 4,697+ edges mapping all QNFO
    papers, projects, concepts, decisions, and infrastructure assets.

    Args:
        endpoint: Graph API endpoint to query. Options:
                 - "stats": Ecosystem overview (node/edge counts, label distribution)
                 - "nodes": Query nodes by label and optional search
                 - "neighbors": Get connected nodes and edges for a specific entity
                 - "impact": Analyze downstream dependencies and impact
                 - "query": Run a raw graph query
        params: Endpoint-specific parameters as a key-value dictionary.
                For "nodes": {"label": "Paper", "search": "quantum"}
                For "neighbors": {"id": "paper-cfpe-forecast"}
                For "impact": {"id": "project-qnfo-gov"}
                For "query": {"query": "MATCH (p:Paper)-[:BELONGS_TO]->(c:Concept) RETURN p,c"}

    Returns:
        JSON response from the graph API. Structure varies by endpoint.
        "stats" returns: {totalNodes, totalEdges, nodeLabels, relationshipTypes}

    Error Handling:
        - Returns {"error": "message"} if endpoint is invalid
        - Returns {"error": "message"} if graph API is unreachable

    Examples:
        query_graph(endpoint="stats")
        query_graph(endpoint="nodes", params={"label": "Paper", "search": "quantum"})
        query_graph(endpoint="neighbors", params={"id": "project-cfpe-forecast"})
    """
    valid_endpoints = ["stats", "nodes", "neighbors", "impact", "query"]
    if endpoint not in valid_endpoints:
        return json.dumps({
            "error": f"Invalid endpoint '{endpoint}'. Must be one of: {valid_endpoints}"
        })

    try:
        result = call_graph_api(endpoint, params or {})
        return json.dumps(result)
    except Exception as e:
        return json.dumps({"error": f"Graph API error: {str(e)}"})


# ---------------------------------------------------------------------------
# Resource: Static paper listing
# ---------------------------------------------------------------------------
@mcp.resource("papers://recent/{count}")
def list_recent_papers(count: int = 10) -> str:
    """List the most recently published papers.

    Args:
        count: Number of papers to return (1-50, default 10)
    """
    count = max(1, min(count or 10, 50))
    papers = fetch_recent_papers(count)
    return json.dumps({"papers": papers, "count": len(papers)})
```

### Node/TypeScript (MCP SDK) Example

```typescript
// server.ts
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

// Initialize
const server = new McpServer({
  name: "qno-research-mcp",
  version: "1.0.0",
  description: "QNFO Research MCP Server"
});

// ---------------------------------------------------------------------------
// Tool: search_papers
// ---------------------------------------------------------------------------
server.tool(
  "search_papers",
  "Semantic search across QWAV research papers using Vectorize embeddings. Returns papers ranked by meaning similarity (not keywords). Supports filtering by source.",
  {
    query: z.string()
      .min(1, "Query must be non-empty")
      .max(500, "Query too long")
      .describe("Natural language search query"),
    limit: z.number()
      .int()
      .min(1)
      .max(50)
      .default(10)
      .describe("Maximum results (1-50)"),
    source: z.enum(["all", "arxiv", "zenodo", "manual"])
      .default("all")
      .describe("Paper source filter"),
  },
  async ({ query, limit, source }) => {
    // Input validation is handled by Zod schemas above
    try {
      const results = await env.PAPER_VZ.query(query, {
        topK: limit,
        filter: source !== "all" ? { source } : undefined,
        returnMetadata: true,
      });

      return {
        content: [{
          type: "text",
          text: JSON.stringify({
            results: results.matches.map(m => ({
              slug: m.id,
              title: m.metadata?.title,
              score: m.score,
              snippet: m.metadata?.body?.slice(0, 300),
              doi: m.metadata?.doi,
            })),
            count: results.matches.length,
            query,
          }),
        }],
      };
    } catch (error) {
      return {
        content: [{
          type: "text",
          text: JSON.stringify({
            error: `Search failed: ${error instanceof Error ? error.message : "Unknown error"}`,
            results: [],
          }),
        }],
        isError: true,
      };
    }
  }
);

// ---------------------------------------------------------------------------
// Tool: get_paper
// ---------------------------------------------------------------------------
server.tool(
  "get_paper",
  "Get full paper details including body content from D1 living-paper database.",
  {
    slug: z.string()
      .min(1, "Slug is required")
      .describe("Paper identifier"),
    include_body: z.boolean()
      .default(true)
      .describe("Include full markdown body"),
  },
  async ({ slug, include_body }) => {
    try {
      const paper = await env.DB.prepare(
        "SELECT slug, title, author, abstract, body, doi, published_at FROM papers WHERE slug = ?"
      ).bind(slug).first();

      if (!paper) {
        return {
          content: [{ type: "text", text: JSON.stringify({ error: `Paper not found: ${slug}` }) }],
          isError: true,
        };
      }

      const result: Record<string, unknown> = {
        slug: paper.slug,
        title: paper.title,
        author: paper.author,
        doi: paper.doi,
        published_at: paper.published_at,
        pages_url: `https://papers.qnfo.org/papers/${paper.slug}/`,
        zenodo_url: paper.doi ? `https://doi.org/${paper.doi}` : null,
      };

      if (include_body) {
        result.body = paper.body;
      }

      return {
        content: [{ type: "text", text: JSON.stringify(result) }],
      };
    } catch (error) {
      return {
        content: [{ type: "text", text: JSON.stringify({ error: `Database error: ${error}` }) }],
        isError: true,
      };
    }
  }
);

// Export as Worker
export default {
  async fetch(request: Request, env: Env, ctx: ExecutionContext): Promise<Response> {
    // MCP endpoint
    const url = new URL(request.url);
    if (url.pathname === "/mcp") {
      return server.handleRequest(request, env, ctx);
    }

    // Health check
    if (url.pathname === "/health") {
      return new Response(JSON.stringify({ status: "ok", uptime: Date.now() }), {
        headers: { "Content-Type": "application/json" },
      });
    }

    return new Response("Not Found", { status: 404 });
  },
};
```

### Deployment (wrangler.jsonc)
```jsonc
{
  "$schema": "node_modules/wrangler/config-schema.json",
  "name": "qno-research-mcp",
  "main": "server.ts",
  "compatibility_date": "2025-07-17",
  "compatibility_flags": ["nodejs_compat"],
  "d1_databases": [
    {
      "binding": "DB",
      "database_name": "living-paper",
      "database_id": "35e2e573-92f3-46ac-83c6-22f6429fc5e5"
    }
  ],
  "vectorize": [
    {
      "binding": "PAPER_VZ",
      "index_name": "qwav-research-v2"
    }
  ],
  "r2_buckets": [
    {
      "binding": "BUCKET",
      "bucket_name": "qnfo"
    }
  ],
  "observability": {
    "enabled": true,
    "head_sampling_rate": 1
  }
}
```

### Deploy & Verify
```bash
# Deploy
npx wrangler deploy

# Verify endpoint
curl -s https://qno-research-mcp.q08.workers.dev/health
# {"status":"ok","uptime":1721200000000}

# Test MCP tool
curl -s -X POST https://qno-research-mcp.q08.workers.dev/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tools/call",
    "params": {
      "name": "search_papers",
      "arguments": {"query": "quantum error correction", "limit": 3}
    },
    "id": 1
  }'
```

### MCP Tool Design Rules (HARD)
1. **Input validation FIRST:** Every tool validates ALL inputs before any business logic. Return structured error immediately on invalid input.
2. **Descriptive docstrings:** Every tool must have a comprehensive docstring covering: purpose, all parameters with types and defaults, return format, error conditions, usage examples.
3. **Structured errors:** Always `{"error": "message", "details": {...}}` -- never raw strings, never stack traces.
4. **Default values:** All optional parameters have sensible defaults.
5. **Range limits:** Numeric parameters have explicit min/max (enforced in schema, NOT just in docs).
6. **Idempotent operations:** If the same inputs produce different outputs, document why.
7. **Timeouts:** All external API calls have explicit timeouts (default 10s).
8. **Retry with backoff:** Transient failures (429, 503) retry up to 3 times with exponential backoff.

### Testing Checklist
- [ ] All tools respond to valid inputs with correct output format
- [ ] All tools return structured errors for invalid inputs (empty, null, wrong type, out of range)
- [ ] Server returns 200 on `/health` endpoint
- [ ] Server returns 200 on `/mcp` endpoint with correct MCP protocol
- [ ] D1 binding works (test get_paper with known slug)
- [ ] Vectorize binding works (test search_papers with known query)
- [ ] R2 binding works (if applicable)
- [ ] Error responses don't leak internal state (no stack traces, no DB queries, no file paths)
- [ ] Rate limiting works (if applicable)
- [ ] Cold start time < 500ms

---

## Anti-Patterns
| Anti-Pattern | Fix |
|:-------------|:----|
| Reviewing code without reading it | `read` every file before reviewing |
| "Improve error handling" without specifics | Cite exact line, show fix with code example |
| MCP server without input validation | Zod schemas (TS) or manual validation (Python) on every input |
| MCP server returning raw exceptions | Always return structured `{"error": "..."}` |
| Non-Cloudflare MCP deployment | Deploy as Cloudflare Worker |
| `any` type without justification | Document WHY `any` is necessary |
| Silent error swallowing | Log all errors with context; never empty catch |
