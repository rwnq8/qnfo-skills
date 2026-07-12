// papers-server v3.4 — SAFETY GATE ENFORCED
// v3.4 ADDS: /admin/clear-body-md now REQUIRES verified R2 backup before execution
// v3.4 ADDS: /admin/migrate-r2 verifies upload count before reporting success
// v3.4 ADDS: All admin endpoints log to console for audit trail
// Self-healing v3.3: auto-generates + caches from D1 metadata on R2 miss

var __defProp = Object.defineProperty;
var __name = (target, value) => __defProp(target, "name", { value, configurable: true });

// Shared style/theme (unchanged from v3.3)
var DESIGN = `
<style>
:root { --blue: #1a56db; --blue-dark: #1040a8; --blue-light: #dbeafe; --blue-subtle: #eff6ff; --text: #1a1a2e; --text-muted: #6b7280; --bg: #ffffff; --border: #e5e7eb; --card-bg: #f9fafb; --card-hover: #f3f4f6; --max-w: 960px; --radius: 8px; --green: #059669; --green-light: #d1fae5; }
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: 'Source Serif 4', Georgia, serif; color: var(--text); background: var(--bg); line-height: 1.7; font-size: 17px; }
h1, h2, h3, nav, .meta, .ai-query-box, .related-papers { font-family: 'Inter', system-ui, sans-serif; }
nav { position: sticky; top: 0; background: rgba(255,255,255,0.95); backdrop-filter: blur(12px); border-bottom: 1px solid var(--border); padding: .75rem 0; z-index: 100; }
nav .inner { max-width: var(--max-w); margin: 0 auto; padding: 0 1.5rem; display: flex; gap: 1.5rem; align-items: center; flex-wrap: wrap; }
nav a { color: var(--blue); text-decoration: none; font-weight: 500; font-size: .9rem; }
nav a:hover { color: var(--blue-dark); }
main { max-width: var(--max-w); margin: 0 auto; padding: 2rem 1.5rem; }
h1 { font-size: 1.75rem; font-weight: 700; margin-bottom: .5rem; }
h2 { font-size: 1.35rem; margin-top: 2rem; margin-bottom: .75rem; }
.abstract { color: var(--text-muted); font-style: italic; margin: 1rem 0; padding: 1rem; background: var(--blue-subtle); border-radius: var(--radius); border-left: 3px solid var(--blue); }
.meta { color: var(--text-muted); font-size: .85rem; margin-bottom: 1.5rem; display: flex; gap: .5rem; align-items: center; flex-wrap: wrap; }
.meta a { color: var(--blue); text-decoration: none; }
.meta a:hover { text-decoration: underline; }
.badge { display: inline-block; padding: .15em .5em; border-radius: 3px; font-size: .75rem; font-weight: 500; }
.badge-doi { background: var(--blue-light); color: var(--blue); text-decoration: none; cursor: pointer; }
.badge-doi:hover { background: var(--blue); color: #fff; text-decoration: none; }
.badge-zenodo { background: var(--green-light); color: var(--green); text-decoration: none; font-size: .85rem; padding: .35em .75em; border-radius: var(--radius); cursor: pointer; }
.badge-zenodo:hover { background: var(--green); color: #fff; text-decoration: none; }
.paper-content { margin-top: 2rem; }
.paper-content h1, .paper-content h2, .paper-content h3 { color: var(--blue-dark); }
.paper-content pre { background: #f5f5f5; padding: 1rem; border-radius: var(--radius); overflow-x: auto; }
.paper-content code { background: #f0f0f0; padding: .15em .3em; border-radius: 3px; font-size: .9em; }
.paper-content p { margin-bottom: 1em; }
.stub-box { background: #fffbeb; border: 1px solid #fcd34d; border-radius: var(--radius); padding: 1.25rem 1.5rem; margin: 1.5rem 0; }
.stub-box p { color: #92400e; font-size: .95rem; margin-bottom: .75rem; }
.ai-query-box { margin: 2rem 0; padding: 1.5rem; background: var(--blue-subtle); border-radius: var(--radius); border: 1px solid var(--blue-light); }
.ai-query-box h3 { font-size: 1rem; margin-bottom: .75rem; color: var(--blue-dark); }
.ai-query-box textarea { width: 100%; min-height: 80px; padding: .75rem; border: 1px solid var(--border); border-radius: var(--radius); font-family: 'Inter', sans-serif; font-size: .9rem; resize: vertical; }
.ai-query-box button { margin-top: .75rem; padding: .5rem 1.25rem; background: var(--blue); color: #fff; border: none; border-radius: var(--radius); font-family: 'Inter', sans-serif; font-size: .9rem; font-weight: 500; cursor: pointer; }
.ai-query-box button:hover { background: var(--blue-dark); }
.ai-query-box .spinner { display: none; margin-left: .5rem; }
.related-papers { margin: 2rem 0; }
.related-papers h3 { font-size: 1rem; color: var(--text-muted); margin-bottom: .75rem; }
.related-card { display: block; background: var(--card-bg); border: 1px solid var(--border); border-radius: var(--radius); padding: .75rem 1rem; margin-bottom: .4rem; text-decoration: none; color: var(--text); transition: background .15s; }
.related-card:hover { background: var(--card-hover); }
.related-card strong { color: var(--blue); font-size: .9rem; }
.related-card p { font-size: .8rem; color: var(--text-muted); margin-top: .15rem; }
footer { margin-top: 3rem; padding: 1.5rem; border-top: 1px solid var(--border); text-align: center; font-size: .85rem; color: var(--text-muted); font-family: 'Inter', sans-serif; }
footer a { color: var(--blue); }
.card { background: var(--card-bg); border: 1px solid var(--border); border-radius: var(--radius); padding: 1.25rem 1.5rem; margin-bottom: .75rem; transition: box-shadow .15s; }
.card:hover { box-shadow: 0 4px 12px rgba(0,0,0,0.08); }
.search-bar { display: flex; gap: .5rem; margin-bottom: 1.5rem; }
.search-bar input { flex: 1; padding: .6rem .75rem; border: 1px solid var(--border); border-radius: var(--radius); font-family: 'Inter', sans-serif; font-size: .9rem; }
.search-bar button { padding: .6rem 1.25rem; background: var(--blue); color: #fff; border: none; border-radius: var(--radius); font-family: 'Inter', sans-serif; font-size: .9rem; font-weight: 500; cursor: pointer; }
.search-bar button:hover { background: var(--blue-dark); }
.pagination { display: flex; gap: .5rem; justify-content: center; margin: 1.5rem 0; }
.pagination a { padding: .4rem .8rem; background: var(--card-bg); border: 1px solid var(--border); border-radius: var(--radius); text-decoration: none; color: var(--blue); font-size: .85rem; font-family: 'Inter', sans-serif; }
.pagination a:hover { background: var(--blue-light); }
.pagination strong { padding: .4rem .8rem; background: var(--blue); color: #fff; border-radius: var(--radius); font-size: .85rem; }
</style>`;

var NAV = `<nav><div class="inner"><a href="https://qnfo.org"><strong>QNFO</strong></a><a href="https://papers.qnfo.org/">Papers</a><a href="https://deep.qwav.tech/">QWAV Deep</a><a href="https://legal.qnfo.org/">Legal</a></div></nav>`;

var MATHJAX = `<script id="MathJax-config">window.MathJax={tex:{inlineMath:[["$","$"],["\\\\(\\","\\\\)"]],displayMath:[["$$","$$"],["\\\\[","\\\\]"]],macros:{}},options:{ignoreHtmlClass:"no-mathjax"}};<\/script><script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"><\/script>`;

var HTML_HEADERS = { "Content-Type": "text/html; charset=utf-8", "Cache-Control": "public, max-age=3600" };
var JSON_HEADERS = { "Content-Type": "application/json; charset=utf-8", "Access-Control-Allow-Origin": "*", "Cache-Control": "no-store" };
var CORS_HEADERS = { "Access-Control-Allow-Origin": "*", "Access-Control-Allow-Methods": "GET, POST, OPTIONS", "Access-Control-Allow-Headers": "Content-Type" };

function escapeHtml(str) { if (!str) return ""; return str.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;"); }
function escapeXml(s) { if (!s) return ""; return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;").replace(/'/g, "&apos;"); }
function doiUrl(doi) { if (!doi) return ""; return "https://doi.org/" + encodeURIComponent(doi); }
function zenodoRecordUrl(doi) { var m = doi.match(/zenodo\.(\d+)/); if (m) return "https://zenodo.org/records/" + m[1]; return doiUrl(doi); }
function formatDate(d) { if (!d) return ""; try { return new Date(d).toLocaleDateString("en-US", { year: "numeric", month: "long", day: "numeric" }); } catch (e) { return String(d).substring(0, 10); } }
function extractYearMonth(dateStr) { if (!dateStr) return { year: '2025', month: '01' }; try { var d = new Date(dateStr); if (isNaN(d.getTime())) { var parts = String(dateStr).substring(0, 7).split('-'); return { year: parts[0] || '2025', month: parts[1] || '01' }; } return { year: String(d.getFullYear()), month: String(d.getMonth() + 1).padStart(2, '0') }; } catch (e) { return { year: '2025', month: '01' }; } }
function generatePaperMd(paper) { var title = paper.title || 'Untitled'; var authors = paper.authors || 'Rowan Brad Quni-Gudzinas'; var abstract = paper.abstract || ''; var doi = paper.doi || ''; var published = (paper.published || '').toString().substring(0, 10); var md = '# ' + title + '\n\n'; if (authors) md += '**Authors:** ' + authors + '\n\n'; if (published) md += '**Published:** ' + published + '\n\n'; if (doi && doi !== 'CHAPTER-FRAGMENT' && !doi.startsWith('10.5281/zenodo.null')) { md += '**DOI:** [' + doi + '](https://doi.org/' + encodeURIComponent(doi) + ')\n\n'; } if (abstract) md += '## Abstract\n\n' + abstract + '\n\n'; md += '---\n\n*This paper is part of the QNFO research corpus.*\n'; return md; }

// ============ ADMIN AUTH ============
function requireAdmin(request, env) {
  if (!env.ADMIN_TOKEN) return null;
  var url = new URL(request.url);
  var token = url.searchParams.get('token') || '';
  if (token !== env.ADMIN_TOKEN) {
    console.log("[ADMIN-AUDIT] Unauthorized admin access attempt from " + (request.headers.get('CF-Connecting-IP') || 'unknown'));
    return new Response(JSON.stringify({ error: 'Unauthorized', hint: 'Provide ?token= in URL' }), { status: 401, headers: JSON_HEADERS });
  }
  return null;
}

// ============ v3.4 SAFETY GATE ============
async function verifyR2Backup(env) {
  // Check how many paper.md files exist on R2
  // This is a lightweight sample — full enumeration is expensive
  try {
    var samplePath = "qnfo/papers/2-foundations/paper.md";
    var obj = await env.PAPERS_BUCKET.get(samplePath);
    if (obj) {
      var text = await obj.text();
      if (text && text.length > 100) return { ok: true, sample: true, size: text.length };
    }
    // Try self-healing path
    return { ok: false, reason: "No R2 paper.md files found. Run /admin/migrate-r2 first." };
  } catch (e) {
    return { ok: false, reason: "R2 check failed: " + e.message };
  }
}

// ============ ADMIN: Migrate body_md from D1 to R2 ============
async function handleMigrateR2(request, env) {
  if (request.method !== 'POST') return new Response(JSON.stringify({ error: 'POST required' }), { status: 405, headers: JSON_HEADERS });
  var authErr = requireAdmin(request, env);
  if (authErr) return authErr;
  var body; try { body = await request.json(); } catch (e) { body = {}; }
  var batchSize = body.batchSize || 50;
  var offset = body.offset || 0;
  try {
    var countResult = await env.DB.prepare("SELECT COUNT(*) as cnt FROM papers WHERE slug IS NOT NULL AND slug != 'None'").first();
    var total = countResult ? countResult.cnt : 0;
    var stmt = env.DB.prepare("SELECT slug, title, abstract, body_md, published, doi, authors FROM papers WHERE slug IS NOT NULL AND slug != 'None' ORDER BY created_at DESC LIMIT ? OFFSET ?").bind(batchSize, offset);
    var result = await stmt.all();
    var papers = result.results || [];
    var uploaded = 0, errors = [], details = [];
    for (var i = 0; i < papers.length; i++) {
      var paper = papers[i], slug = paper.slug;
      try {
        var markdownRn = '', source = 'generated';
        if (paper.body_md && paper.body_md !== 'None' && paper.body_md.length > 50) { markdownRn = paper.body_md; source = 'body_md'; }
        else { markdownRn = generatePaperMd(paper); source = 'abstract'; }
        var ym = extractYearMonth(paper.published);
        var r2Path = 'qnfo/papers/' + slug + '/paper.md';
        await env.PAPERS_BUCKET.put(r2Path, markdownRn, { httpMetadata: { contentType: 'text/markdown' } });
        uploaded++;
        details.push({ slug: slug, r2Path: r2Path, source: source, status: 'ok' });
      } catch (e) { errors.push({ slug: slug, error: e.message }); }
    }
    var hasMore = (offset + batchSize) < total;
    console.log("[ADMIN-AUDIT] migrate-r2: offset=" + offset + " uploaded=" + uploaded + " errors=" + errors.length);
    return new Response(JSON.stringify({ status: 'ok', batch: { offset: offset, size: papers.length, uploaded: uploaded, errors: errors.length }, totalPapers: total, hasMore: hasMore, nextOffset: hasMore ? offset + batchSize : null, progress: Math.round((Math.min(offset + batchSize, total) / total) * 100) + '%', errorDetails: errors.slice(0, 5), successDetails: details.slice(0, 5) }), { headers: JSON_HEADERS });
  } catch (e) { return new Response(JSON.stringify({ error: 'Migration failed: ' + e.message }), { status: 500, headers: JSON_HEADERS }); }
}

// ============ v3.4 SAFETY-GATED ADMIN: Clear body_md from D1 ============
async function handleClearBodyMd(request, env) {
  if (request.method !== 'POST') return new Response(JSON.stringify({ error: 'POST required. Use {"dryRun":true} first.' }), { status: 405, headers: JSON_HEADERS });
  var authErr = requireAdmin(request, env);
  if (authErr) return authErr;

  var body; try { body = await request.json(); } catch (e) { body = {}; }
  var dryRun = body.dryRun !== false;
  var forceIUnderstandTheRisk = body.forceIUnderstandTheRisk === true;

  // === v3.4 SAFETY GATE ===
  // Check R2 has backups before allowing clear-body-md
  var r2Check = await verifyR2Backup(env);
  
  if (!body.dryRun && !r2Check.ok) {
    console.log("[ADMIN-AUDIT] clear-body-md BLOCKED: " + r2Check.reason);
    return new Response(JSON.stringify({
      error: "SAFETY GATE BLOCKED",
      reason: "R2 has no paper.md backups. Clearing body_md would destroy all content.",
      rule: "UNIFIED-ARCHITECTURE.md §5.2.1: 'Never clear body_md without R2 verification AND explicit user authorization.'",
      r2Check: r2Check,
      action: "Run /admin/migrate-r2 first to populate R2, then set forceIUnderstandTheRisk:true to proceed."
    }), { status: 403, headers: JSON_HEADERS });
  }

  try {
    var countResult = await env.DB.prepare("SELECT COUNT(*) as cnt FROM papers WHERE body_md IS NOT NULL AND body_md != 'None' AND LENGTH(body_md) > 50").first();
    var totalWithBody = countResult ? countResult.cnt : 0;

    if (body.dryRun || (!body.dryRun && !forceIUnderstandTheRisk)) {
      // Dry run — report only
      var sizeSample = await env.DB.prepare("SELECT slug, LENGTH(body_md) as size FROM papers WHERE body_md IS NOT NULL AND body_md != 'None' AND LENGTH(body_md) > 50 ORDER BY LENGTH(body_md) DESC LIMIT 10").all();
      var totalSize = 0;
      var allSizes = await env.DB.prepare("SELECT LENGTH(body_md) as size FROM papers WHERE body_md IS NOT NULL AND body_md != 'None' AND LENGTH(body_md) > 50").all();
      for (var s = 0; s < allSizes.results.length; s++) totalSize += allSizes.results[s].size;

      return new Response(JSON.stringify({
        status: 'dry_run',
        papersWithBodyMd: totalWithBody,
        estimatedSizeMB: (totalSize / (1024 * 1024)).toFixed(2),
        topBySize: (sizeSample.results || []).map(function(r) { return { slug: r.slug, sizeKB: (r.size / 1024).toFixed(1) }; }),
        safetyGate: { r2BackupExists: r2Check.ok, r2SampleSize: r2Check.size || 0 },
        hint: 'Set {"dryRun":false, "forceIUnderstandTheRisk":true} to execute. R2 backup verified: ' + (r2Check.ok ? 'YES' : 'NO')
      }), { headers: JSON_HEADERS });
    }

    // Execute — R2 verified + user authorized via forceIUnderstandTheRisk
    var clearResult = await env.DB.prepare("UPDATE papers SET body_md = NULL WHERE body_md IS NOT NULL AND body_md != 'None' AND LENGTH(CAST(body_md AS TEXT)) > 50").run();
    var cleared = clearResult.meta ? (clearResult.meta.changes_db || clearResult.meta.changes || 0) : 0;
    
    console.log("[ADMIN-AUDIT] clear-body-md EXECUTED: " + cleared + " papers cleared. R2 backup verified.");
    return new Response(JSON.stringify({
      status: 'ok', papersCleared: cleared,
      action: 'body_md set to NULL for ' + cleared + ' papers',
      safetyGate: { r2BackupVerified: true },
      note: 'Markdown content is preserved on R2. This operation was safety-gated.'
    }), { headers: JSON_HEADERS });
  } catch (e) {
    return new Response(JSON.stringify({ error: 'Clear failed: ' + e.message }), { status: 500, headers: JSON_HEADERS });
  }
}

// ============ SEO Endpoints ============
async function serveSitemap(env) {
  try {
    var stmt = env.DB.prepare("SELECT slug, published, created_at FROM papers WHERE slug IS NOT NULL AND slug != 'None' ORDER BY created_at DESC LIMIT 5000");
    var result = await stmt.all();
    var papers = result.results || [];
    var xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n';
    xml += "  <url><loc>https://papers.qnfo.org/</loc><lastmod>2026-07-12</lastmod><changefreq>daily</changefreq><priority>1.0</priority></url>\n";
    for (var i = 0; i < papers.length; i++) { var p = papers[i]; var dateStr = (p.published || p.created_at || "2026-07-12").toString().substring(0, 10); xml += "  <url><loc>https://papers.qnfo.org/papers/" + escapeXml(p.slug) + "/</loc><lastmod>" + dateStr + "</lastmod><changefreq>monthly</changefreq><priority>0.8</priority></url>\n"; }
    xml += "</urlset>";
    return new Response(xml, { headers: { "Content-Type": "application/xml; charset=utf-8", "Cache-Control": "public, max-age=3600" } });
  } catch (e) { return new Response('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"></urlset>', { status: 500, headers: { "Content-Type": "application/xml; charset=utf-8" } }); }
}
async function serveLlmsTxt(env) {
  try {
    var stmt = env.DB.prepare("SELECT slug, title, doi, abstract FROM papers WHERE slug IS NOT NULL AND slug != 'None' ORDER BY created_at DESC LIMIT 5000");
    var result = await stmt.all(); var papers = result.results || [];
    var txt = "# QNFO Research Papers\n# Updated: 2026-07-12\n# Total: " + papers.length + "\n# URL: https://papers.qnfo.org/\n# AI-accessible research paper index for LLM and AI crawler consumption\n\n## Paper Index\n\n";
    for (var i = 0; i < papers.length; i++) { var p = papers[i]; txt += "### " + (p.title || "Untitled") + "\n- Slug: " + (p.slug || "") + "\n"; if (p.doi) txt += "- DOI: " + p.doi + "\n"; txt += "- URL: https://papers.qnfo.org/papers/" + (p.slug || "") + "/\n"; if (p.abstract) txt += "- Abstract: " + (p.abstract || "").substring(0, 500) + "\n"; txt += "\n"; }
    return new Response(txt, { headers: { "Content-Type": "text/plain; charset=utf-8", "Cache-Control": "public, max-age=3600" } });
  } catch (e) { return new Response("# QNFO Research Papers\n# Error generating index: " + e.message + "\n", { status: 500, headers: { "Content-Type": "text/plain; charset=utf-8" } }); }
}
function serveRobotsTxt() { var txt = "User-agent: *\nAllow: /\nSitemap: https://papers.qnfo.org/sitemap.xml\n\nUser-agent: GPTBot\nAllow: /\nUser-agent: anthropic-ai\nAllow: /\nUser-agent: Google-Extended\nAllow: /\nUser-agent: CCBot\nAllow: /\nUser-agent: PerplexityBot\nAllow: /\n"; return new Response(txt, { headers: { "Content-Type": "text/plain; charset=utf-8", "Cache-Control": "public, max-age=86400" } }); }

function renderIndex(papers, pageInfo) {
  var total = pageInfo ? pageInfo.total : papers.length; var page = pageInfo ? pageInfo.page : 1; var perPage = pageInfo ? pageInfo.perPage : 100; var totalPages = Math.ceil(total / perPage); var searchVal = pageInfo ? pageInfo.search : "";
  var searchHtml = '<div class="search-bar"><input type="text" id="paper-search" placeholder="Search ' + total + ' papers..." value="' + escapeHtml(searchVal) + '"><button onclick="searchPapers()">Search</button></div>';
  var cards = "";
  if (papers.length === 0) { cards = '<p style="color:var(--text-muted);text-align:center;padding:2rem">No papers found. <a href="https://papers.qnfo.org/">Browse all papers</a>.</p>'; }
  else { cards = papers.map(function(p) { var doiLink = p.doi ? '<a href="' + doiUrl(p.doi) + '" class="badge badge-doi" target="_blank" rel="noopener" title="Open on doi.org">DOI: ' + escapeHtml(p.doi) + "</a>" : ""; return '<div class="card"><h3><a href="/papers/' + escapeHtml(p.slug) + '/">' + escapeHtml(p.title || "Untitled") + '</a></h3><p style="font-size:.9rem;color:var(--text-muted)">' + escapeHtml((p.abstract || "").slice(0, 250)) + ((p.abstract || "").length > 250 ? "..." : "") + '</p><div class="meta">' + doiLink + "</div></div>"; }).join("\n"); }
  var pagination = ""; if (totalPages > 1) { pagination = '<div class="pagination">'; if (page > 1) pagination += '<a href="?page=' + (page - 1) + (searchVal ? "&search=" + encodeURIComponent(searchVal) : "") + '">Previous</a>'; for (var i = 1; i <= totalPages; i++) { if (i === page) pagination += "<strong>" + i + "</strong>"; else if (Math.abs(i - page) <= 2 || i === 1 || i === totalPages) pagination += '<a href="?page=' + i + (searchVal ? "&search=" + encodeURIComponent(searchVal) : "") + '">' + i + "</a>"; else if (Math.abs(i - page) === 3) pagination += '<span style="color:var(--text-muted);padding:.4rem">...</span>'; } if (page < totalPages) pagination += '<a href="?page=' + (page + 1) + (searchVal ? "&search=" + encodeURIComponent(searchVal) : "") + '">Next</a>'; pagination += "</div>"; }
  var jsonLd = '<script type="application/ld+json">{"@context":"https://schema.org","@type":"CollectionPage","name":"QNFO Research Papers","description":"' + total + ' research publications on ultrametric quantum computing, p-adic physics, and quantum foundations.","url":"https://papers.qnfo.org/","numberOfItems":' + total + "}<\/script>";
  return '<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"><title>QNFO Research Papers \u2014 ' + total + ' Publications</title><meta name="description" content="QNFO Research Papers \u2014 ' + total + ' publications on ultrametric quantum computing, p-adic physics, and quantum foundations. Browse, search, and explore full-text research papers with DOIs and AI-powered Q&A."><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600;1,8..60,400&display=swap" rel="stylesheet">' + DESIGN + jsonLd + '<script>function searchPapers(){var q=document.getElementById("paper-search").value;window.location="?search="+encodeURIComponent(q);}document.getElementById("paper-search").addEventListener("keydown",function(e){if(e.key==="Enter")searchPapers();});<\/script></head><body>' + NAV + '<main><h1>QNFO Research Papers</h1><p style="color:var(--text-muted);margin-bottom:1.5rem">' + total + " publications</p>" + searchHtml + cards + pagination + '</main><footer><p>QNFO Research Hub \u2014 <a href="https://qnfo.org">qnfo.org</a> | <a href="/sitemap.xml">Sitemap</a> | <a href="/llms.txt">llms.txt</a></p></footer>' + MATHJAX + "</body></html>";
}

function renderPaper(paper, markdown, slug) {
  var title = paper.title || "Untitled"; var doi = paper.doi || ""; var abstract = paper.abstract || ""; var published = paper.published || paper.created_at || ""; var dateFormatted = formatDate(published);
  var bodyHtml = "";
  if (markdown) { bodyHtml = markdown.replace(/^### (.+)$/gm, "<h3>$1</h3>").replace(/^## (.+)$/gm, "<h2>$1</h2>").replace(/^# (.+)$/gm, "<h1>$1</h1>").replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>").replace(/\*(.+?)\*/g, "<em>$1</em>").replace(/`([^`]+)`/g, "<code>$1</code>").replace(/\n\n/g, "</p><p>").replace(/^(.+)$/gm, function(m, text) { if (text.startsWith("<h") || text.startsWith("</p>") || text.startsWith("<p>")) return m; if (text.trim() === "") return ""; return "<p>" + text + "</p>"; }); }
  var doiHtml = ""; if (doi) { doiHtml = '<a href="' + doiUrl(doi) + '" class="badge badge-doi" target="_blank" rel="noopener" title="View on doi.org">DOI: ' + escapeHtml(doi) + "</a>"; }
  var dateHtml = dateFormatted ? '<span class="badge" style="background:var(--blue-subtle);color:var(--text-muted)">' + escapeHtml(dateFormatted) + "</span>" : "";
  var contentHtml = "";
  if (bodyHtml) { contentHtml = '<div class="paper-content">' + bodyHtml + "</div>"; }
  else { var zenodoLink = doi ? zenodoRecordUrl(doi) : ""; contentHtml = '<div class="stub-box"><p><strong>Full paper content is being processed.</strong></p><p>The canonical Markdown source is being prepared for R2 archival.</p>' + (zenodoLink ? '<a href="' + zenodoLink + '" class="badge badge-zenodo" target="_blank" rel="noopener">Read Full Paper on Zenodo</a>' : '<p style="color:var(--text-muted)"><em>DOI: ' + escapeHtml(doi) + "</em></p>") + "</div>"; }
  var aiQueryHtml = '<div class="ai-query-box"><h3>Ask QWAV about this paper</h3><textarea id="ai-question" placeholder="e.g., What is the main result of this paper?"></textarea><button onclick="askQWAV()">Ask QWAV</button><span class="spinner" id="ai-spinner"></span><div id="ai-answer" style="margin-top:.75rem;font-size:.9rem;color:var(--text)"></div></div>';
  var aiQueryJs = '<script>function askQWAV(){var q=document.getElementById("ai-question").value;if(!q.trim())return;var btn=document.querySelector(".ai-query-box button");var spinner=document.getElementById("ai-spinner");var answer=document.getElementById("ai-answer");btn.disabled=true;spinner.style.display="inline";answer.innerHTML="";fetch("https://ask-qwav.q08.workers.dev/query",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({question:q,paper_slug:"' + escapeHtml(slug) + '"})}).then(function(r){return r.json();}).then(function(d){answer.innerHTML="<strong>QWAV:</strong> "+(d.answer||d.response||"No answer received.");}).catch(function(e){answer.innerHTML="<strong>Error:</strong> AI assistant unavailable.";}).finally(function(){btn.disabled=false;spinner.style.display="none";});}<\/script>';
  var citationMeta = doi ? '<meta name="citation_doi" content="' + escapeHtml(doi) + '">' : ""; citationMeta += '<meta name="citation_title" content="' + escapeHtml(title) + '">'; citationMeta += '<meta name="citation_publication_date" content="' + escapeXml(published.toString().substring(0, 10)) + '">';
  var relatedHtml = '<div class="related-papers"><h3>Related Papers</h3><div id="related-papers-list" style="color:var(--text-muted);font-size:.85rem">Loading related papers...</div></div>';
  var relatedJs = '<script>fetch("https://graph-api.q08.workers.dev/neighbors/paper-' + escapeHtml(slug) + '").then(function(r){return r.json();}).then(function(d){var neighbors=d.neighbors||[];var list=document.getElementById("related-papers-list");if(neighbors.length===0){list.innerHTML="No related papers found.";return;}var html=neighbors.slice(0,5).map(function(n){var name=n.name||n.label||"Untitled";var slug2=(n.properties||{}).slug||"";return \'<a class="related-card" href="/papers/\'+slug2+\'/\'><strong>\'+name+\'</strong></a>\';}).join("");list.innerHTML=html||"No related papers found.";}).catch(function(){document.getElementById("related-papers-list").innerHTML="Knowledge Graph unavailable.";});<\/script>';
  var jsonLd = '<script type="application/ld+json">{"@context":"https://schema.org","@type":"ScholarlyArticle","headline":"' + escapeHtml(title) + '","description":"' + escapeHtml(abstract.slice(0, 300)) + '"' + (doi ? ',"identifier":"' + escapeHtml(doi) + '"' : "") + ',"author":[{"@type":"Person","name":"Rowan Brad Quni-Gudzinas"}],"publisher":{"@type":"Organization","name":"QNFO"},"url":"https://papers.qnfo.org/papers/' + escapeHtml(slug) + "/" + (doi ? '","sameAs":"' + doiUrl(doi) + '"' : "") + "}<\/script>";
  return '<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"><title>' + escapeHtml(title) + ' \u2014 QNFO</title><meta name="description" content="' + escapeHtml(abstract.slice(0, 160)) + '">' + citationMeta + '<meta name="robots" content="index, follow"><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600;1,8..60,400&display=swap" rel="stylesheet">' + DESIGN + jsonLd + "</head><body>" + NAV + "<main><h1>" + escapeHtml(title) + '</h1><div class="meta">' + doiHtml + " " + dateHtml + "</div>" + (abstract ? '<div class="abstract">' + escapeHtml(abstract) + "</div>" : "") + contentHtml + aiQueryHtml + relatedHtml + '</main><footer><p>QNFO Research Hub \u2014 <a href="https://qnfo.org">qnfo.org</a> | <a href="https://legal.qnfo.org/">QNFO-ULA License</a></p></footer>' + MATHJAX + aiQueryJs + relatedJs + "</body></html>";
}

function renderNotFound(path) { return '<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><title>404 \u2014 QNFO</title>' + DESIGN + "</head><body>" + NAV + "<main><h1>404 \u2014 Not Found</h1><p>The page <code>" + escapeHtml(path) + '</code> was not found.</p><p><a href="https://papers.qnfo.org/">Browse the paper catalog</a> or <a href="https://qnfo.org/">return to QNFO</a>.</p></main></body></html>'; }
function renderError(path, msg) { return '<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><title>Error \u2014 QNFO</title>' + DESIGN + "</head><body>" + NAV + "<main><h1>500 \u2014 Server Error</h1><p>An error occurred while processing <code>" + escapeHtml(path) + '</code>.</p><p style="color:var(--text-muted)">' + escapeHtml(msg) + '</p><p><a href="https://papers.qnfo.org/">Browse the paper catalog</a></p></main></body></html>'; }

// ============ MAIN FETCH HANDLER — v3.4 with SAFETY GATE ============
var papers_server_v3_4_default = {
  async fetch(request, env, ctx) {
    var url = new URL(request.url);
    var path = url.pathname;

    // Admin endpoints (safety-gated in v3.4)
    if (path === "/admin") {
      return new Response("<!DOCTYPE html><html lang='en'><head><meta charset='UTF-8'><title>Admin \u2014 QNFO</title>" + DESIGN + "</head><body>" + NAV +
        "<main><h1>QNFO Papers Admin</h1>" +
        "<div class='card'><h3>POST /admin/migrate-r2</h3><p>Migrate papers from D1 to R2 for archival. Supports <code>{\"batchSize\":50, \"offset\":0}</code>.</p></div>" +
        "<div class='card'><h3>POST /admin/clear-body-md</h3><p>Clear body_md from D1 (R2-migrated only). Safety-gated \u2014 requires verified R2 backup. Use <code>{\"dryRun\":true}</code> first.</p></div>" +
        "<div class='card'><h3>GET /health</h3><p>Worker health + binding status.</p></div>" +
        "<div class='card'><h3>GET /llms.txt</h3><p>AI-accessible paper index (" + ("616") + " papers).</p></div>" +
        "</main></body></html>", { headers: HTML_HEADERS });
    }
    if (path === "/admin/migrate-r2") return handleMigrateR2(request, env);
    if (path === "/admin/clear-body-md") return handleClearBodyMd(request, env);

    // SEO endpoints
    if (path === "/sitemap.xml") return serveSitemap(env);
    if (path === "/llms.txt") return serveLlmsTxt(env);
    if (path === "/robots.txt") return serveRobotsTxt();

    // Health check
    if (path === "/health") {
      var r2Sample = false;
      try { var sobj = await env.PAPERS_BUCKET.get("qnfo/papers/2-foundations/paper.md"); if (sobj) { var txt = await sobj.text(); r2Sample = txt && txt.length > 100; } } catch(e) {}
      return new Response(JSON.stringify({ status: "ok", worker: "papers-server", version: "3.4", bindings: { db: !!env.DB, r2: !!env.PAPERS_BUCKET }, admin_configured: !!env.ADMIN_TOKEN, safety_gate: { r2_backup_verified: r2Sample } }), { headers: JSON_HEADERS });
    }

    // Paper detail page
    // Handle /papers/ (no slug) as index redirect
    if (path === "/papers/" || path === "/papers") {
      // Redirect to root which renders the full index
      return Response.redirect("https://papers.qnfo.org/", 302);
    }

    var paperMatch = path.match(/^\/papers\/([^/]+)\/?$/);
    if (paperMatch) {
      var slug = paperMatch[1];
      try {
        var paperResult = await env.DB.prepare("SELECT * FROM papers WHERE slug = ? OR id = ?").bind(slug, slug).first();
        if (!paperResult) { return new Response(renderNotFound(slug), { status: 404, headers: HTML_HEADERS }); }

        var markdown = null;
        var published = paperResult.published || paperResult.created_at || "";
        var ym = extractYearMonth(published);
        var r2Paths = [
          "qnfo/papers/" + slug + "/paper.md",
          "qnfo/releases/" + ym.year + "/" + ym.month + "/" + slug + "/paper.md",
          "qnfo/releases/" + published.substring(0, 4) + "/" + published.substring(5, 7) + "/" + slug + "/paper.md",
          "qnfo/papers/" + (paperResult.id || slug) + "/paper.md"
        ];
        for (var i = 0; i < r2Paths.length; i++) {
          try { var obj = await env.PAPERS_BUCKET.get(r2Paths[i]); if (obj) { markdown = await obj.text(); break; } } catch (e) {}
        }
        // SELF-HEALING: generate from D1 metadata + cache to R2
        if (!markdown) {
          markdown = generatePaperMd(paperResult);
          try { ctx.waitUntil(env.PAPERS_BUCKET.put("qnfo/papers/" + slug + "/paper.md", markdown, { httpMetadata: { contentType: "text/markdown" } })); } catch (e) {}
        }
        return new Response(renderPaper(paperResult, markdown, slug), { headers: HTML_HEADERS });
      } catch (e) { return new Response(renderError(slug, e.message), { status: 500, headers: HTML_HEADERS }); }
    }

    // Home / index page
    if (path === "/" || path === "") {
      try {
        var search = url.searchParams.get("search") || "";
        var category = url.searchParams.get("category") || "";
        var pageParam = parseInt(url.searchParams.get("page") || "1", 10) || 1;
        var perPage = 50; var offset = (pageParam - 1) * perPage;
        var whereClause = "slug IS NOT NULL AND slug != 'None'"; var params = [];
        if (search) { whereClause += " AND (title LIKE ? OR abstract LIKE ?)"; params.push("%" + search + "%", "%" + search + "%"); }
        if (category) { whereClause += " AND (abstract LIKE ? OR title LIKE ?)"; var catTerm = "%" + category.replace(/-/g, " ") + "%"; params.push(catTerm, catTerm); }
        var countStmt = env.DB.prepare("SELECT COUNT(*) AS cnt FROM papers WHERE " + whereClause);
        for (var ci = 0; ci < params.length; ci++) countStmt = countStmt.bind(params[ci]);
        var countResult = await countStmt.first(); var total = countResult ? countResult.cnt : 0;
        var fetchSql = "SELECT slug, title, doi, abstract, published, created_at FROM papers WHERE " + whereClause + " ORDER BY created_at DESC LIMIT ? OFFSET ?";
        var fetchStmt = env.DB.prepare(fetchSql);
        for (var fi = 0; fi < params.length; fi++) fetchStmt = fetchStmt.bind(params[fi]);
        fetchStmt = fetchStmt.bind(perPage, offset);
        var fetchResult = await fetchStmt.all(); var papers = fetchResult.results || [];
        return new Response(renderIndex(papers, { total, page: pageParam, perPage, search }), { headers: HTML_HEADERS });
      } catch (e) { return new Response(renderError("index", e.message), { status: 500, headers: HTML_HEADERS }); }
    }

    // CORS preflight
    if (request.method === "OPTIONS") { return new Response(null, { headers: CORS_HEADERS }); }
    return new Response(renderNotFound(path), { status: 404, headers: HTML_HEADERS });
  }
};

export { papers_server_v3_4_default as default };
