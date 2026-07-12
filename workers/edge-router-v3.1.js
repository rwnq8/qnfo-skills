var __defProp = Object.defineProperty;
var __name = (target, value) => __defProp(target, "name", { value, configurable: true });

// edge-router.js — v3.1 RED-TEAM FIX
// FIX: papers.qnfo.org now routes to PAPERS_SERVER Worker (not static Pages)
// FIX: papers-server does dynamic D1+R2 rendering with DOI hyperlinks, AI Query, Related Papers
// ADDED: PAPERS_SERVER service binding

var edge_router_default = {
  async fetch(request, env, ctx) {
    var url = new URL(request.url);
    var host = url.hostname;
    var path = url.pathname;

    // API routing
    if (path.startsWith("/api/ai/query") && env.AI_WORKER) {
      var aiUrl = new URL(request.url);
      aiUrl.pathname = path.replace("/api/ai", "");
      var aiReq = new Request(aiUrl, request);
      return env.AI_WORKER.fetch(aiReq);
    }
    if (path.startsWith("/api/graph/") && env.GRAPH_API) {
      var gUrl = new URL(request.url);
      gUrl.pathname = path.replace("/api/graph", "");
      var gReq = new Request(gUrl, request);
      return env.GRAPH_API.fetch(gReq);
    }
    if (path.startsWith("/api/paper/") && env.PAPER_CATALOG) {
      var pUrl = new URL(request.url);
      pUrl.pathname = path.replace("/api/paper", "");
      var pReq = new Request(pUrl, request);
      return env.PAPER_CATALOG.fetch(pReq);
    }

    // Health endpoint
    if (path === "/health") {
      return new Response(JSON.stringify({
        status: "ok",
        worker: "qnfo-edge-router",
        version: "3.1",
        bindings: {
          ai_worker: !!env.AI_WORKER,
          graph_api: !!env.GRAPH_API,
          paper_catalog: !!env.PAPER_CATALOG,
          papers_server: !!env.PAPERS_SERVER
        },
        routes: ["archive", "papers", "legal", "qwav", "hub"]
      }), {
        headers: { "Content-Type": "application/json", "Access-Control-Allow-Origin": "*" }
      });
    }

    // CORS
    if (request.method === "OPTIONS") {
      return new Response(null, {
        headers: {
          "Access-Control-Allow-Origin": "*",
          "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
          "Access-Control-Allow-Headers": "Content-Type"
        }
      });
    }

    // === FIX: papers.qnfo.org → PAPERS_SERVER (dynamic Worker with D1+R2) ===
    if (host === "papers.qnfo.org" || path.startsWith("/papers/")) {
      if (env.PAPERS_SERVER) {
        return env.PAPERS_SERVER.fetch(request);
      }
      // Fallback: if PAPERS_SERVER binding is missing, proxy to static Pages
      return fetch("https://qnfo-publications.pages.dev" + path + url.search, request);
    }

    // Archive
    if (host === "archive.qnfo.org") {
      return archiveResponse();
    }

    // Legal
    if (host === "legal.qnfo.org" || path.startsWith("/legal/")) {
      return fetch("https://qnfo-legal.pages.dev" + path + url.search, request);
    }

    // QWAV
    if (host.includes("qwav") || host.includes("qwave")) {
      return fetch("https://qwav.pages.dev" + path + url.search, request);
    }

    // Default: QNFO Hub
    return fetch("https://qnfo-hub.pages.dev" + path + url.search, request);
  }
};

function archiveResponse() {
  return new Response('<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="UTF-8">\n<meta name="viewport" content="width=device-width, initial-scale=1.0">\n<title>QNFO Research Archive</title>\n<style>\n:root{--blue:#1a56db;--text:#1a1a2e;--bg:#fff;--border:#e5e7eb}\nbody{font-family:"Source Serif 4",Georgia,serif;color:var(--text);background:var(--bg);max-width:960px;margin:0 auto;padding:2rem;line-height:1.7}\nh1{font-family:Inter,system-ui,sans-serif;font-size:2rem}\na{color:var(--blue);text-decoration:none}\n.nav{display:flex;gap:1.5rem;margin:1.5rem 0 2rem;font-family:Inter,system-ui,sans-serif}\n.card{background:#f9fafb;border:1px solid #e5e7eb;border-radius:8px;padding:1.5rem;margin:1rem 0}\n.card h3{margin-bottom:.5rem}\n</style>\n</head>\n<body>\n<h1>🔬 QNFO Research Archive</h1>\n<div class="nav">\n  <a href="https://papers.qnfo.org">📄 Papers Catalog</a>\n  <a href="https://qnfo.org">🏠 QNFO Hub</a>\n  <a href="https://legal.qnfo.org">⚖ License</a>\n</div>\n<p>The QNFO Research Archive contains <strong>658 publications</strong> across quantum error correction, p-adic mathematics, ultrametric theory, condensed mathematics, and related fields — now with AI-powered Q&A and Knowledge Graph integration.</p>\n<div class="card"><h3>📚 Browse</h3><p>All papers at <a href="https://papers.qnfo.org">papers.qnfo.org</a> with full-text search, AI-powered discussion, and Knowledge Graph-powered related papers.</p></div>\n<div class="card"><h3>⚡ Infrastructure</h3><p>Powered by <strong>25 Cloudflare Workers</strong>, <strong>10 Pages projects</strong>, <strong>5 D1 databases</strong>, and <strong>4 service bindings</strong> (AI, KG, Catalog, Papers Server).</p></div>\n<div class="card"><h3>🤖 AI Integration</h3><p>API endpoints: <code>/api/ai/query</code> (paper Q&A), <code>/api/graph/neighbors/:slug</code> (related papers), <code>/api/paper/:slug</code> (metadata). All proxied via edge router.</p></div>\n<p style="margin-top:2rem;color:#6b7280;font-size:.85rem">© QNFO · Licensed under <a href="https://legal.qnfo.org">QNFO-ULA</a></p>\n</body></html>', {
    headers: { "Content-Type": "text/html; charset=utf-8" }
  });
}

__name(archiveResponse, "archiveResponse");

export {
  edge_router_default as default
};
//# sourceMappingURL=edge-router.js.map
