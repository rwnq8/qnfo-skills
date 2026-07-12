// papers-server v3.0 — Full-Text Paper Pipeline (RED-TEAM AUDITED)
// Fixes: DOI hyperlinks, dynamic SEO, AI Query, Related Papers, category search, Zenodo links
// Deployed 2026-07-12 | QNFO Infrastructure | RED-TEAM AUDIT v3.0

// ============================================================
// DESIGN SYSTEM v3.0 (LOCKED — do not change)
// ============================================================
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
/* AI Query Box */
.ai-query-box { margin: 2rem 0; padding: 1.5rem; background: var(--blue-subtle); border-radius: var(--radius); border: 1px solid var(--blue-light); }
.ai-query-box h3 { font-size: 1rem; margin-bottom: .75rem; color: var(--blue-dark); }
.ai-query-box textarea { width: 100%; min-height: 80px; padding: .75rem; border: 1px solid var(--border); border-radius: var(--radius); font-family: 'Inter', sans-serif; font-size: .9rem; resize: vertical; }
.ai-query-box button { margin-top: .75rem; padding: .5rem 1.25rem; background: var(--blue); color: #fff; border: none; border-radius: var(--radius); font-family: 'Inter', sans-serif; font-size: .9rem; font-weight: 500; cursor: pointer; }
.ai-query-box button:hover { background: var(--blue-dark); }
.ai-query-box .spinner { display: none; margin-left: .5rem; }
/* Related Papers */
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
/* Search bar on index */
.search-bar { display: flex; gap: .5rem; margin-bottom: 1.5rem; }
.search-bar input { flex: 1; padding: .6rem .75rem; border: 1px solid var(--border); border-radius: var(--radius); font-family: 'Inter', sans-serif; font-size: .9rem; }
.search-bar button { padding: .6rem 1.25rem; background: var(--blue); color: #fff; border: none; border-radius: var(--radius); font-family: 'Inter', sans-serif; font-size: .9rem; font-weight: 500; cursor: pointer; }
.search-bar button:hover { background: var(--blue-dark); }
/* Pagination */
.pagination { display: flex; gap: .5rem; justify-content: center; margin: 1.5rem 0; }
.pagination a { padding: .4rem .8rem; background: var(--card-bg); border: 1px solid var(--border); border-radius: var(--radius); text-decoration: none; color: var(--blue); font-size: .85rem; font-family: 'Inter', sans-serif; }
.pagination a:hover { background: var(--blue-light); }
.pagination strong { padding: .4rem .8rem; background: var(--blue); color: #fff; border-radius: var(--radius); font-size: .85rem; }
</style>`;

var NAV = `
<nav><div class="inner">
<a href="https://qnfo.org"><strong>QNFO</strong></a>
<a href="https://papers.qnfo.org/">Papers</a>
<a href="https://deep.qwav.tech/">QWAV Deep</a>
<a href="https://legal.qnfo.org/">Legal</a>
</div></nav>`;

var MATHJAX = `
<script id="MathJax-config">
window.MathJax = {
  tex: { inlineMath: [["$","$"],["\\\\(\\","\\\\)"]], displayMath: [["$$","$$"],["\\\\[","\\\\]"]], macros: {} },
  options: { ignoreHtmlClass: "no-mathjax" }
};
<\/script>
<script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"><\/script>`;

// ============================================================
// UTILITY FUNCTIONS
// ============================================================
function escapeHtml(str) {
  if (!str) return "";
  return str.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
}

function escapeXml(s) {
  if (!s) return "";
  return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;").replace(/'/g, "&apos;");
}

function doiUrl(doi) {
  if (!doi) return "";
  return "https://doi.org/" + encodeURIComponent(doi);
}

function zenodoRecordUrl(doi) {
  // Extract Zenodo record ID from DOI: 10.5281/zenodo.12345678 → https://zenodo.org/records/12345678
  var m = doi.match(/zenodo\.(\d+)/);
  if (m) return "https://zenodo.org/records/" + m[1];
  return doiUrl(doi); // fallback
}

function formatDate(d) {
  if (!d) return "";
  try { return new Date(d).toLocaleDateString("en-US", { year: "numeric", month: "long", day: "numeric" }); }
  catch (e) { return String(d).substring(0, 10); }
}

// ============================================================
// SEO: Dynamic Sitemap + LLMs.txt (generated from D1, not R2)
// ============================================================
async function serveSitemap(env) {
  try {
    var stmt = env.DB.prepare("SELECT slug, published, created_at FROM papers WHERE slug IS NOT NULL AND slug != 'None' ORDER BY created_at DESC LIMIT 5000");
    var result = await stmt.all();
    var papers = result.results || [];
    var xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n';
    xml += '  <url><loc>https://papers.qnfo.org/</loc><lastmod>2026-07-12</lastmod><changefreq>daily</changefreq><priority>1.0</priority></url>\n';
    for (var i = 0; i < papers.length; i++) {
      var p = papers[i];
      var dateStr = (p.published || p.created_at || "2026-07-12").toString().substring(0, 10);
      xml += '  <url><loc>https://papers.qnfo.org/papers/' + escapeXml(p.slug) + '/</loc><lastmod>' + dateStr + '</lastmod><changefreq>monthly</changefreq><priority>0.8</priority></url>\n';
    }
    xml += '</urlset>';
    return new Response(xml, {
      headers: { "Content-Type": "application/xml; charset=utf-8", "Cache-Control": "public, max-age=3600" }
    });
  } catch (e) {
    console.error("Sitemap error:", e.message);
    return new Response('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"></urlset>', {
      status: 500,
      headers: { "Content-Type": "application/xml; charset=utf-8" }
    });
  }
}

async function serveLlmsTxt(env) {
  try {
    var stmt = env.DB.prepare("SELECT slug, title, doi, abstract FROM papers WHERE slug IS NOT NULL AND slug != 'None' ORDER BY created_at DESC LIMIT 5000");
    var result = await stmt.all();
    var papers = result.results || [];
    var txt = "# QNFO Research Papers\n";
    txt += "# Updated: 2026-07-12\n";
    txt += "# Total: " + papers.length + "\n";
    txt += "# URL: https://papers.qnfo.org/\n";
    txt += "# AI-accessible research paper index for LLM and AI crawler consumption\n\n";
    txt += "## Paper Index\n\n";
    for (var i = 0; i < papers.length; i++) {
      var p = papers[i];
      txt += "### " + (p.title || "Untitled") + "\n";
      txt += "- Slug: " + (p.slug || "") + "\n";
      if (p.doi) txt += "- DOI: " + p.doi + "\n";
      txt += "- URL: https://papers.qnfo.org/papers/" + (p.slug || "") + "/\n";
      if (p.abstract) txt += "- Abstract: " + (p.abstract || "").substring(0, 500) + "\n";
      txt += "\n";
    }
    return new Response(txt, {
      headers: { "Content-Type": "text/plain; charset=utf-8", "Cache-Control": "public, max-age=3600" }
    });
  } catch (e) {
    return new Response("# QNFO Research Papers\n# Error generating index: " + e.message + "\n", {
      status: 500,
      headers: { "Content-Type": "text/plain; charset=utf-8" }
    });
  }
}

function serveRobotsTxt() {
  var txt = "User-agent: *\nAllow: /\nSitemap: https://papers.qnfo.org/sitemap.xml\n\nUser-agent: GPTBot\nAllow: /\nUser-agent: anthropic-ai\nAllow: /\nUser-agent: Google-Extended\nAllow: /\nUser-agent: CCBot\nAllow: /\nUser-agent: PerplexityBot\nAllow: /\n";
  return new Response(txt, { headers: { "Content-Type": "text/plain; charset=utf-8" } });
}

// ============================================================
// RENDER FUNCTIONS
// ============================================================
function renderIndex(papers, pageInfo) {
  var total = pageInfo ? pageInfo.total : papers.length;
  var page = pageInfo ? pageInfo.page : 1;
  var perPage = pageInfo ? pageInfo.perPage : 100;
  var totalPages = Math.ceil(total / perPage);
  var searchVal = pageInfo ? pageInfo.search : "";

  var searchHtml = '<div class="search-bar"><input type="text" id="paper-search" placeholder="Search ' + total + ' papers..." value="' + escapeHtml(searchVal) + '"><button onclick="searchPapers()">🔍 Search</button></div>';

  var cards = "";
  if (papers.length === 0) {
    cards = '<p style="color:var(--text-muted);text-align:center;padding:2rem">No papers found. <a href="https://papers.qnfo.org/">Browse all papers</a>.</p>';
  } else {
    cards = papers.map(function (p) {
      var doiLink = p.doi ? '<a href="' + doiUrl(p.doi) + '" class="badge badge-doi" target="_blank" rel="noopener" title="Open on doi.org">DOI: ' + escapeHtml(p.doi) + '</a>' : "";
      return '<div class="card"><h3><a href="/papers/' + escapeHtml(p.slug) + '/">' + escapeHtml(p.title || "Untitled") + '</a></h3><p style="font-size:.9rem;color:var(--text-muted)">' + escapeHtml((p.abstract || "").slice(0, 250)) + ((p.abstract || "").length > 250 ? "..." : "") + '</p><div class="meta">' + doiLink + '</div></div>';
    }).join("\n");
  }

  // Pagination
  var pagination = "";
  if (totalPages > 1) {
    pagination = '<div class="pagination">';
    if (page > 1) pagination += '<a href="?page=' + (page - 1) + (searchVal ? '&search=' + encodeURIComponent(searchVal) : '') + '">← Previous</a>';
    for (var i = 1; i <= totalPages; i++) {
      if (i === page) pagination += '<strong>' + i + '</strong>';
      else if (Math.abs(i - page) <= 2 || i === 1 || i === totalPages) pagination += '<a href="?page=' + i + (searchVal ? '&search=' + encodeURIComponent(searchVal) : '') + '">' + i + '</a>';
      else if (Math.abs(i - page) === 3) pagination += '<span style="color:var(--text-muted);padding:.4rem">...</span>';
    }
    if (page < totalPages) pagination += '<a href="?page=' + (page + 1) + (searchVal ? '&search=' + encodeURIComponent(searchVal) : '') + '">Next →</a>';
    pagination += '</div>';
  }

  var jsonLd = '<script type="application/ld+json">{"@context":"https://schema.org","@type":"CollectionPage","name":"QNFO Research Papers","description":"' + total + ' research publications on ultrametric quantum computing, p-adic physics, and quantum foundations.","url":"https://papers.qnfo.org/","numberOfItems":' + total + '}</script>';

  return '<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"><title>QNFO Research Papers — ' + total + ' Publications</title><meta name="description" content="QNFO Research Papers — ' + total + ' publications on ultrametric quantum computing, p-adic physics, and quantum foundations. Browse, search, and explore full-text research papers with DOIs and AI-powered Q&A."><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600;1,8..60,400&display=swap" rel="stylesheet">' + DESIGN + jsonLd + '<script>function searchPapers(){var q=document.getElementById("paper-search").value;window.location="?search="+encodeURIComponent(q);}document.getElementById("paper-search").addEventListener("keydown",function(e){if(e.key==="Enter")searchPapers();});</script></head><body>' + NAV + '<main><h1>QNFO Research Papers</h1><p style="color:var(--text-muted);margin-bottom:1.5rem">' + total + ' publications</p>' + searchHtml + cards + pagination + '</main><footer><p>QNFO Research Hub — <a href="https://qnfo.org">qnfo.org</a> | <a href="/sitemap.xml">Sitemap</a> | <a href="/llms.txt">llms.txt</a></p></footer>' + MATHJAX + '</body></html>';
}

function renderPaper(paper, markdown, slug) {
  var title = paper.title || "Untitled";
  var doi = paper.doi || "";
  var abstract = paper.abstract || "";
  var published = paper.published || paper.created_at || "";
  var dateFormatted = formatDate(published);

  // Convert markdown to HTML (simple converter)
  var bodyHtml = "";
  if (markdown) {
    bodyHtml = markdown
      .replace(/^### (.+)$/gm, "<h3>$1</h3>")
      .replace(/^## (.+)$/gm, "<h2>$1</h2>")
      .replace(/^# (.+)$/gm, "<h1>$1</h1>")
      .replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>")
      .replace(/\*(.+?)\*/g, "<em>$1</em>")
      .replace(/`([^`]+)`/g, "<code>$1</code>")
      .replace(/\n\n/g, "</p><p>")
      .replace(/^(.+)$/gm, function (m, text) {
        if (text.startsWith("<h") || text.startsWith("</p>") || text.startsWith("<p>")) return m;
        if (text.trim() === "") return "";
        return "<p>" + text + "</p>";
      });
  }

  // DOI as CLICKABLE HYPERLINK (RED-TEAM FIX)
  var doiHtml = "";
  if (doi) {
    doiHtml = '<a href="' + doiUrl(doi) + '" class="badge badge-doi" target="_blank" rel="noopener" title="View on doi.org">📎 DOI: ' + escapeHtml(doi) + '</a>';
  }

  // Date badge
  var dateHtml = dateFormatted ? '<span class="badge" style="background:var(--blue-subtle);color:var(--text-muted)">📅 ' + escapeHtml(dateFormatted) + '</span>' : "";

  // Full-text or STUB with clickable Zenodo link (RED-TEAM FIX)
  var contentHtml = "";
  if (bodyHtml) {
    contentHtml = '<div class="paper-content">' + bodyHtml + '</div>';
  } else {
    var zenodoLink = doi ? zenodoRecordUrl(doi) : "";
    contentHtml = '<div class="stub-box"><p><strong>📄 Full paper content is being processed.</strong></p><p>The canonical Markdown source is being prepared for R2 archival. In the meantime, you can read the complete PDF on Zenodo:</p>' + (zenodoLink ? '<a href="' + zenodoLink + '" class="badge badge-zenodo" target="_blank" rel="noopener">📖 Read Full Paper on Zenodo →</a>' : '<p style="color:var(--text-muted)"><em>DOI: ' + escapeHtml(doi) + '</em></p>') + '</div>';
  }

  // AI Query Box (DESIGN SYSTEM v3.0 COMPONENT)
  var aiQueryHtml = '<div class="ai-query-box"><h3>🤖 Ask QWAV about this paper</h3><textarea id="ai-question" placeholder="e.g., What is the main result of this paper? How does it relate to p-adic quantum error correction?"></textarea><button onclick="askQWAV()">Ask QWAV</button><span class="spinner" id="ai-spinner">⏳</span><div id="ai-answer" style="margin-top:.75rem;font-size:.9rem;color:var(--text)"></div></div>';

  // AI Query JavaScript
  var aiQueryJs = '<script>function askQWAV(){var q=document.getElementById("ai-question").value;if(!q.trim())return;var btn=document.querySelector(".ai-query-box button");var spinner=document.getElementById("ai-spinner");var answer=document.getElementById("ai-answer");btn.disabled=true;spinner.style.display="inline";answer.innerHTML="";fetch("https://ask-qwav.q08.workers.dev/query",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({question:q,paper_slug:"' + escapeHtml(slug) + '"})}).then(function(r){return r.json();}).then(function(d){answer.innerHTML="<strong>QWAV:</strong> "+(d.answer||d.response||"No answer received. Try rephrasing your question.");}).catch(function(e){answer.innerHTML="<strong>Error:</strong> AI assistant is currently unavailable. Please try again later.";}).finally(function(){btn.disabled=false;spinner.style.display="none";});}</script>';

  // Citation metadata
  var citationMeta = doi ? '<meta name="citation_doi" content="' + escapeHtml(doi) + '">' : "";
  citationMeta += '<meta name="citation_title" content="' + escapeHtml(title) + '">';
  citationMeta += '<meta name="citation_publication_date" content="' + escapeXml(published.toString().substring(0, 10)) + '">';

  // Related Papers placeholder (will be filled by JS from KG API)
  var relatedHtml = '<div class="related-papers"><h3>📚 Related Papers</h3><div id="related-papers-list" style="color:var(--text-muted);font-size:.85rem">Loading related papers...</div></div>';
  var relatedJs = '<script>fetch("https://graph-api.q08.workers.dev/neighbors/paper-' + escapeHtml(slug) + '").then(function(r){return r.json();}).then(function(d){var neighbors=d.neighbors||[];var list=document.getElementById("related-papers-list");if(neighbors.length===0){list.innerHTML="No related papers found in Knowledge Graph.";return;}var html=neighbors.slice(0,5).map(function(n){var name=n.name||n.label||"Untitled";var slug2=(n.properties||{}).slug||"";return \'<a class="related-card" href="/papers/\'+slug2+\'/\"><strong>\'+name+\'</strong></a>\';}).join("");list.innerHTML=html||"No related papers found.";}).catch(function(){document.getElementById("related-papers-list").innerHTML="Knowledge Graph unavailable.";});</script>';

  var jsonLd = '<script type="application/ld+json">{"@context":"https://schema.org","@type":"ScholarlyArticle","headline":"' + escapeHtml(title) + '","description":"' + escapeHtml(abstract.slice(0, 300)) + '"' + (doi ? ',"identifier":"' + escapeHtml(doi) + '"' : "") + ',"author":[{"@type":"Person","name":"Rowan Brad Quni-Gudzinas"}],"publisher":{"@type":"Organization","name":"QNFO"},"url":"https://papers.qnfo.org/papers/' + escapeHtml(slug) + '/' + (doi ? '","sameAs":"' + doiUrl(doi) + '"' : "") + '}</script>';

  return '<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"><title>' + escapeHtml(title) + ' — QNFO</title><meta name="description" content="' + escapeHtml(abstract.slice(0, 160)) + '">' + citationMeta + '<meta name="robots" content="index, follow"><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600;1,8..60,400&display=swap" rel="stylesheet">' + DESIGN + jsonLd + '</head><body>' + NAV + '<main><h1>' + escapeHtml(title) + '</h1><div class="meta">' + doiHtml + ' ' + dateHtml + '</div>' + (abstract ? '<div class="abstract">' + escapeHtml(abstract) + '</div>' : "") + contentHtml + aiQueryHtml + relatedHtml + '</main><footer><p>QNFO Research Hub — <a href="https://qnfo.org">qnfo.org</a> | <a href="https://legal.qnfo.org/">QNFO-ULA License</a></p></footer>' + MATHJAX + aiQueryJs + relatedJs + '</body></html>';
}

function renderNotFound(path) {
  return '<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><title>404 — QNFO</title>' + DESIGN + '</head><body>' + NAV + '<main><h1>404 — Not Found</h1><p>The page <code>' + escapeHtml(path) + '</code> was not found.</p><p><a href="https://papers.qnfo.org/">Browse the paper catalog</a> or <a href="https://qnfo.org/">return to QNFO</a>.</p></main></body></html>';
}

function renderError(path, msg) {
  return '<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><title>Error — QNFO</title>' + DESIGN + '</head><body>' + NAV + '<main><h1>500 — Server Error</h1><p>An error occurred while processing <code>' + escapeHtml(path) + '</code>.</p><p style="color:var(--text-muted)">' + escapeHtml(msg) + '</p><p><a href="https://papers.qnfo.org/">Browse the paper catalog</a></p></main></body></html>';
}

// ============================================================
// MAIN FETCH HANDLER
// ============================================================
export default {
  async fetch(request, env) {
    var url = new URL(request.url);
    var path = url.pathname;
    var search = url.searchParams.get("search") || "";
    var category = url.searchParams.get("category") || "";
    var pageParam = parseInt(url.searchParams.get("page") || "1", 10) || 1;

    // SEO endpoints
    if (path === "/sitemap.xml") return serveSitemap(env);
    if (path === "/llms.txt") return serveLlmsTxt(env);
    if (path === "/robots.txt") return serveRobotsTxt();

    // Health check
    if (path === "/health") {
      return new Response(JSON.stringify({ status: "ok", worker: "papers-server", version: "3.0", bindings: { db: !!env.DB, r2: !!env.PAPERS_BUCKET } }), {
        headers: { "Content-Type": "application/json", "Access-Control-Allow-Origin": "*" }
      });
    }

    // Paper detail page
    var paperMatch = path.match(/^\/papers\/([^/]+)\/?$/);
    if (paperMatch) {
      var slug = paperMatch[1];
      try {
        var stmt = env.DB.prepare("SELECT * FROM papers WHERE slug = ? OR id = ?").bind(slug, slug);
        var result = await stmt.first();
        if (!result) {
          return new Response(renderNotFound(slug), { status: 404, headers: { "Content-Type": "text/html; charset=utf-8" } });
        }
        // Try R2 for markdown
        var markdown = null;
        var published = result.published || result.created_at || "";
        var ym = published.substring(0, 7).replace("-", "/");
        var y = published.substring(0, 4);
        var m = published.substring(5, 7);
        var r2Paths = [
          "qnfo/releases/" + ym + "/" + slug + "/paper.md",
          "qnfo/releases/" + y + "/" + m + "/" + slug + "/paper.md",
          "qnfo/papers/" + slug + "/paper.md",
          "qnfo/papers/" + (result.id || slug) + "/paper.md"
        ];
        for (var i = 0; i < r2Paths.length; i++) {
          try {
            var obj = await env.PAPERS_BUCKET.get(r2Paths[i]);
            if (obj) { markdown = await obj.text(); break; }
          } catch (e) {
            console.error("R2 markdown fetch failed:", r2Paths[i], e.message);
          }
        }
        return new Response(renderPaper(result, markdown, slug), { headers: { "Content-Type": "text/html; charset=utf-8" } });
      } catch (e) {
        return new Response(renderError(slug, e.message), { status: 500, headers: { "Content-Type": "text/html; charset=utf-8" } });
      }
    }

    // Index page
    if (path === "/" || path === "") {
      try {
        var perPage = 50;
        var offset = (pageParam - 1) * perPage;
        var whereClause = "slug IS NOT NULL AND slug != 'None'";
        var params = [];

        if (search) {
          whereClause += " AND (title LIKE ? OR abstract LIKE ?)";
          params.push("%" + search + "%", "%" + search + "%");
        }
        if (category) {
          whereClause += " AND (abstract LIKE ? OR title LIKE ?)";
          var catTerm = "%" + category.replace(/-/g, " ") + "%";
          params.push(catTerm, catTerm);
        }

        // Count total
        var countStmt = env.DB.prepare("SELECT COUNT(*) AS cnt FROM papers WHERE " + whereClause);
        for (var ci = 0; ci < params.length; ci++) countStmt = countStmt.bind(params[ci]);
        var countResult = await countStmt.first();
        var total = countResult ? countResult.cnt : 0;

        // Fetch page
        var fetchSql = "SELECT slug, title, doi, abstract, published, created_at FROM papers WHERE " + whereClause + " ORDER BY created_at DESC LIMIT ? OFFSET ?";
        var fetchStmt = env.DB.prepare(fetchSql);
        for (var fi = 0; fi < params.length; fi++) fetchStmt = fetchStmt.bind(params[fi]);
        fetchStmt = fetchStmt.bind(perPage, offset);
        var fetchResult = await fetchStmt.all();
        var papers = fetchResult.results || [];

        return new Response(renderIndex(papers, {
          total: total,
          page: pageParam,
          perPage: perPage,
          search: search
        }), { headers: { "Content-Type": "text/html; charset=utf-8" } });
      } catch (e) {
        return new Response(renderError("index", e.message), { status: 500, headers: { "Content-Type": "text/html; charset=utf-8" } });
      }
    }

    // CORS for API
    if (request.method === "OPTIONS") {
      return new Response(null, {
        headers: { "Access-Control-Allow-Origin": "*", "Access-Control-Allow-Methods": "GET, POST, OPTIONS", "Access-Control-Allow-Headers": "Content-Type" }
      });
    }

    return new Response(renderNotFound(path), { status: 404, headers: { "Content-Type": "text/html; charset=utf-8" } });
  }
};
