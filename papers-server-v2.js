// papers-server v2.1 — minimal dynamic SEO test
// D1 binding: DB (papers table)

function escapeXml(s) {
  if (!s) return '';
  return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
}

async function serveSitemap(env) {
  try {
    const stmt = env.DB.prepare('SELECT id, title, published, created_at FROM papers WHERE id IS NOT NULL ORDER BY created_at DESC');
    const { results } = await stmt.all();
    let xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n';
    xml += '<url><loc>https://papers.qnfo.org/</loc><lastmod>2026-07-11</lastmod><changefreq>weekly</changefreq><priority>1.0</priority></url>\n';
    for (const r of results) {
      const sid = r.id;
      if (!sid) continue;
      xml += `<url><loc>https://papers.qnfo.org/papers/${escapeXml(sid)}/</loc><lastmod>${(r.published||r.created_at||'2026-07-11').toString().substring(0,10)}</lastmod><changefreq>monthly</changefreq><priority>0.8</priority></url>\n`;
    }
    xml += '</urlset>';
    return new Response(xml, { headers: {"Content-Type":"application/xml; charset=utf-8", "Cache-Control":"public, max-age=3600"} });
  } catch(e) {
    return new Response('Sitemap error: '+e.message, { status:500, headers:{"Content-Type":"text/plain"} });
  }
}

async function serveLlmsTxt(env) {
  try {
    const stmt = env.DB.prepare('SELECT id, title, doi, abstract FROM papers WHERE id IS NOT NULL ORDER BY created_at DESC');
    const { results } = await stmt.all();
    let txt = '# QNFO Research Papers\n# Updated: 2026-07-11\n# Total: '+results.length+'\n# URL: https://papers.qnfo.org/\n\n';
    for (const r of results) {
      txt += '## '+(r.title||'Untitled')+'\n';
      txt += '- Slug: '+(r.id||'')+'\n';
      if (r.doi) txt += '- DOI: '+r.doi+'\n';
      txt += '- URL: https://papers.qnfo.org/papers/'+(r.id||'')+'/\n';
      txt += '- Abstract: '+(r.abstract||'').substring(0,500)+'\n\n';
    }
    return new Response(txt, { headers: {"Content-Type":"text/plain; charset=utf-8", "Cache-Control":"public, max-age=3600"} });
  } catch(e) {
    return new Response('LLMs error: '+e.message, { status:500, headers:{"Content-Type":"text/plain"} });
  }
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const path = url.pathname;
    if (path === '/sitemap.xml') return serveSitemap(env);
    if (path === '/llms.txt') return serveLlmsTxt(env);
    if (path === '/robots.txt') return new Response('User-agent: *\nAllow: /\nSitemap: https://papers.qnfo.org/sitemap.xml\n', {headers:{"Content-Type":"text/plain"}});
    // Pass through to original Worker logic
    return new Response('OK - papers-server v2.1', {headers:{"Content-Type":"text/plain"}});
  }
};
