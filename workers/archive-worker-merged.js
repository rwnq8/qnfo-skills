// archive-worker — MERGED (Session 14)
// Combines: archive-worker (archive.qnfo.org HTML pages) + qnfo-archive-worker (queue consumer)
// Bindings needed: DB (D1), QNFO_BUCKET (R2)
// Queue: qnfo-lifecycle-queue (consumer)

// ============================================================
// CSS DESIGN (from original archive-worker)
// ============================================================
const DESIGN = `
:root{--blue:#1a56db;--blue-dark:#1040a8;--blue-light:#dbeafe;--blue-subtle:#eff6ff;--text:#1a1a2e;--text-muted:#6b7280;--bg:#fff;--border:#e5e7eb;--card-bg:#f9fafb;--max-w:960px;--radius:8px}
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'Source Serif 4',Georgia,serif;color:var(--text);background:var(--bg);line-height:1.7;font-size:17px;-webkit-font-smoothing:antialiased}
h1,h2,h3,nav{font-family:'Inter',system-ui,sans-serif}
nav{position:sticky;top:0;background:rgba(255,255,255,.95);backdrop-filter:blur(12px);border-bottom:1px solid var(--border);padding:.75rem 0;z-index:100}
nav .inner{max-width:var(--max-w);margin:0 auto;padding:0 1.5rem;display:flex;gap:1.5rem;align-items:center}
nav a{color:var(--blue);text-decoration:none;font-weight:500;font-size:.9rem}
nav a:hover{color:var(--blue-dark)}
main{max-width:var(--max-w);margin:0 auto;padding:2rem 1.5rem}
h1{font-size:2rem;font-weight:700;margin-bottom:.5rem;letter-spacing:-.02em}
.subtitle{color:var(--text-muted);margin-bottom:2rem}
.card{background:var(--card-bg);border:1px solid var(--border);border-radius:var(--radius);padding:1.25rem 1.5rem;margin-bottom:.75rem;transition:box-shadow .15s}
.card:hover{box-shadow:0 4px 12px rgba(0,0,0,.08)}
.card h3{font-size:1.1rem}
.card h3 a{color:var(--blue);text-decoration:none}
.card h3 a:hover{color:var(--blue-dark)}
.card p{color:var(--text-muted);font-size:.9rem;margin-top:.25rem}
.badge{display:inline-block;padding:.15em .5em;border-radius:3px;font-size:.75rem;font-weight:500;margin-right:.5rem}
.badge-doi{background:var(--blue-light);color:var(--blue)}
.badge-type{background:#f3e8ff;color:#7c3aed}
.links{margin-top:2rem;padding-top:1.5rem;border-top:1px solid var(--border)}
.links a{color:var(--blue)}
footer{margin-top:3rem;padding:1.5rem;border-top:1px solid var(--border);text-align:center;font-family:'Inter',sans-serif;font-size:.85rem;color:var(--text-muted)}
footer a{color:var(--blue)}
`;

const ROBOTS_TXT = `User-agent: *
Allow: /
Sitemap: https://archive.qnfo.org/sitemap.xml

User-agent: GPTBot
Allow: /
User-agent: anthropic-ai
Allow: /
User-agent: Google-Extended
Allow: /
User-agent: CCBot
Allow: /
User-agent: PerplexityBot
Allow: /
`;

const LLMS_TXT = `# archive.qnfo.org

> QNFO Research Archive — 658 publications across quantum error correction, p-adic mathematics, ultrametric theory, and related fields.

## Core Resources
- [Papers Catalog](https://papers.qnfo.org): Full-text searchable paper repository
- [QNFO Hub](https://qnfo.org): Main research hub
- [License](https://legal.qnfo.org): QNFO-ULA license details

## API
- /api/ai/query: Paper Q&A endpoint
- /api/graph/neighbors/:slug: Knowledge Graph related papers
- /api/paper/:slug: Paper metadata
`;

const SITEMAP_XML = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n  <url><loc>https://archive.qnfo.org/</loc><changefreq>weekly</changefreq><priority>0.8</priority></url>\n</urlset>';

// ============================================================
// ARCHIVAL QUEUE CONSUMER (from qnfo-archive-worker)
// ============================================================
async function listR2Objects(env, prefix) {
  try {
    const result = await env.QNFO_BUCKET.list({ prefix });
    return result.objects || [];
  } catch (err) {
    console.error(`[ARCHIVE] Error listing R2 objects: ${err.message}`);
    return [];
  }
}

async function processArchivalJob(env, job) {
  const { project, sourcePath, targetPath } = job;
  console.log(`[ARCHIVE] Archiving ${project}: ${sourcePath} → ${targetPath}`);

  const objects = await listR2Objects(env, sourcePath);
  if (objects.length === 0) {
    console.log(`[ARCHIVE] No objects found at ${sourcePath} — project has no R2 files`);
  }

  let copied = 0;
  let failed = 0;

  for (const obj of objects) {
    try {
      const original = await env.QNFO_BUCKET.get(obj.key);
      if (!original) continue;

      const relativePath = obj.key.replace(sourcePath, "");
      const targetKey = `${targetPath}${relativePath}`.replace(/\/\//g, "/");

      await env.QNFO_BUCKET.put(targetKey, original.body, {
        httpMetadata: original.httpMetadata || {},
        customMetadata: {
          ...(original.customMetadata || {}),
          archived_at: new Date().toISOString(),
          archived_from: obj.key
        }
      });

      await env.QNFO_BUCKET.delete(obj.key);
      copied++;
      console.log(`[ARCHIVE] Copied: ${obj.key} → ${targetKey}`);
    } catch (err) {
      console.error(`[ARCHIVE] Failed to copy ${obj.key}: ${err.message}`);
      failed++;
    }
  }

  console.log(`[ARCHIVE] Complete for ${project}: ${copied} copied, ${failed} failed, ${objects.length} total`);

  return { project, sourcePath, targetPath, copied, failed, total: objects.length };
}

// ============================================================
// HTML HELPERS (from original archive-worker)
// ============================================================
function escapeHtml(str) {
  if (!str) return "";
  return str.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
}

// ============================================================
// MAIN HANDLER
// ============================================================
export default {
  // Queue consumer — processes R2 archival migration jobs
  async queue(batch, env, ctx) {
    console.log(`[ARCHIVE] Processing batch of ${batch.messages.length} messages`);
    for (const message of batch.messages) {
      try {
        const job = message.body;
        await processArchivalJob(env, job);
        message.ack();
      } catch (err) {
        console.error(`[ARCHIVE] Error processing job: ${err.message}`);
        message.retry({ delaySeconds: 60 });
      }
    }
  },

  // HTTP handler — serves archive.qnfo.org pages + API endpoints
  async fetch(request, env) {
    const url = new URL(request.url);
    const path = url.pathname;

    // SEO endpoints
    if (path === "/robots.txt") {
      return new Response(ROBOTS_TXT, { headers: { "Content-Type": "text/plain; charset=utf-8" } });
    }
    if (path === "/llms.txt") {
      return new Response(LLMS_TXT, { headers: { "Content-Type": "text/plain; charset=utf-8" } });
    }
    if (path === "/sitemap.xml") {
      return new Response(SITEMAP_XML, { headers: { "Content-Type": "application/xml; charset=utf-8" } });
    }

    // Health check (merged)
    if (path === "/health") {
      return new Response(JSON.stringify({
        status: "ok",
        worker: "archive-worker-merged",
        capabilities: ["queue-consumer", "html-render", "archival"],
        version: "v2.0-merged"
      }), {
        headers: { "Content-Type": "application/json", "Access-Control-Allow-Origin": "*" }
      });
    }

    // Manual archival trigger (from qnfo-archive-worker)
    if (path === "/archive" && request.method === "POST") {
      try {
        const body = await request.json();
        const result = await processArchivalJob(env, body);
        return new Response(JSON.stringify({ status: "archived", ...result }), {
          headers: { "Content-Type": "application/json", "Access-Control-Allow-Origin": "*" }
        });
      } catch (e) {
        return new Response(JSON.stringify({ error: e.message }), {
          status: 500,
          headers: { "Content-Type": "application/json", "Access-Control-Allow-Origin": "*" }
        });
      }
    }

    // Main archive page (HTML)
    try {
      const stmt = env.DB.prepare(
        "SELECT slug, title, doi, abstract, published, created_at FROM papers WHERE slug IS NOT NULL AND slug != ? ORDER BY created_at DESC LIMIT 50"
      ).bind("None");
      const { results } = await stmt.all();

      const cards = results.map((p) => `
<div class="card">
  <h3><a href="https://papers.qnfo.org/papers/${p.slug}/">${escapeHtml(p.title || "Untitled")}</a></h3>
  <p>${escapeHtml((p.abstract || "").slice(0, 200))}${(p.abstract || "").length > 200 ? "..." : ""}</p>
  <p style="margin-top:.5rem">${p.doi ? `<span class="badge badge-doi">DOI: ${escapeHtml(p.doi.slice(0, 50))}</span>` : ""}${p.published ? `<span class="badge badge-type">${p.published.slice(0, 10)}</span>` : ""}</p>
</div>`).join("\n");

      return new Response(`<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"><title>QNFO Research Archive</title><meta name="description" content="QNFO Research Archive — ${results.length} archived publications on ultrametric quantum computing and p-adic physics."><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600;1,8..60,400&display=swap" rel="stylesheet"><style>${DESIGN}</style></head><body><nav><div class="inner"><a href="https://qnfo.org"><strong>QNFO</strong></a><a href="https://papers.qnfo.org/">Papers</a><a href="https://archive.qnfo.org/">Archive</a><a href="https://deep.qwav.tech/">QWAV Deep</a><a href="https://legal.qnfo.org/">Legal</a></div></nav><main><h1>QNFO Research Archive</h1><p class="subtitle">${results.length} archived publications — sorted by date</p><p style="color:var(--text-muted);margin-bottom:1.5rem">Browse archived research papers. For active research, visit <a href="https://papers.qnfo.org/">the Papers catalog</a> or <a href="https://deep.qwav.tech/">QWAV Deep</a>.</p>${cards}<div class="links"><p><a href="https://papers.qnfo.org/">Browse all papers →</a> | <a href="https://deep.qwav.tech/">QWAV Research Feed →</a></p></div></main><footer><p>QNFO Research Hub — <a href="https://qnfo.org">qnfo.org</a> | <a href="https://legal.qnfo.org/">QNFO-ULA License</a></p></footer></body></html>`, {
        headers: { "Content-Type": "text/html; charset=utf-8" }
      });
    } catch (e) {
      console.error(`[ARCHIVE] DB query error: ${e.message}`);
      return new Response(`<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"><title>QNFO Research Archive</title><style>${DESIGN}</style></head><body><nav><div class="inner"><a href="https://qnfo.org"><strong>QNFO</strong></a><a href="https://papers.qnfo.org/">Papers</a><a href="https://deep.qwav.tech/">QWAV Deep</a></div></nav><main><h1>QNFO Research Archive</h1><p style="color:var(--text-muted)">The archive is initializing. Please check back shortly.</p><p><a href="https://papers.qnfo.org/">Browse the paper catalog →</a></p></main></body></html>`, {
        headers: { "Content-Type": "text/html; charset=utf-8" }
      });
    }
  }
};
