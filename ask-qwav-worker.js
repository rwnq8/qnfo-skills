/**
 * QNFO Ask QWAV v2.6 + SEED + VECTOR-PURGE + PAPER-DOI endpoint
 * /api/seed — batch-seeds Vectorize with paper embeddings
 * /api/vector-purge — deletes vectors by ID from Vectorize
 * /api/paper-doi — updates paper DOI in D1 (POST {paper_id, doi})
 */
export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const p = url.pathname;
    const h = { 'Access-Control-Allow-Origin': '*', 'Content-Type': 'application/json' };
    if (request.method === 'OPTIONS') return new Response(null, { status: 204, headers: h });

    try {
      if (p === '/' || p === '/api') {
        return J({ service: 'QNFO Ask QWAV v2.6', models: { embedding: '@cf/baai/bge-m3 (1024-dim)', textgen: '@cf/deepseek-ai/deepseek-r1-distill-qwen-32b' }, endpoints: ['/health','/api/search?q=X','/api/papers','/api/ask?q=X','/api/stats','/api/seed','/api/cleanup','/api/vector-purge','/api/vector-list','/api/paper-doi'] }, 200, h);
      }

      if (p === '/health' || p === '/api/health') {
        let n = 0, vs = '?', aiOk = 'unknown', embTest = 'not-tested';
        try { const r = await env.PAPERS_DB.prepare('SELECT count(*) as c FROM papers').all(); n = r.results?.[0]?.c || 0; } catch(e) {}
        try { const idx = await env.VECTORIZE_INDEX.describe(); vs = 'dim='+(idx.dimensions||'?')+' vectors='+(idx.vectorCount||'?'); } catch(e) {}
        try { const emb = await env.AI.run('@cf/baai/bge-m3', { text: ['test'] }); aiOk = emb?.data ? 'ok' : 'no-data'; embTest = emb?.data ? `shape=[${emb.data.length},${emb.data[0]?.length||'?'}]` : 'no-embedding'; } catch(e) { aiOk = 'error'; embTest = e.message.substring(0,80); }
        return J({ status: 'ok', version: '2.6', papers: n, vectorize: vs, ai: aiOk, embedding_test: embTest }, 200, h);
      }

      if (p === '/api/papers') {
        const lim = Math.min(parseInt(url.searchParams.get('limit')||'20'),100);
        const off = parseInt(url.searchParams.get('offset')||'0');
        const { results } = await env.PAPERS_DB.prepare('SELECT id, title, authors, doi, abstract, published, ipfs_cid FROM papers ORDER BY updated_at DESC LIMIT ? OFFSET ?').bind(lim, off).all();
        const { results: c } = await env.PAPERS_DB.prepare('SELECT count(*) as c FROM papers').all();
        return J({ success: true, total: c[0]?.c||0, limit: lim, offset: off, data: results }, 200, h);
      }

      if (p === '/api/search') {
        const q = url.searchParams.get('q');
        const lim = Math.min(parseInt(url.searchParams.get('limit')||'10'),50);
        if (!q) return J({ success: false, error: 'Missing ?q=' }, 400, h);
        let results = [], method = 'vectorize';
        try {
          const emb = await env.AI.run('@cf/baai/bge-m3', { text: [q] });
          if (emb?.data?.[0]) {
            const vr = await env.VECTORIZE_INDEX.query(emb.data[0], { topK: Math.min(lim*3, 50) });
            if (vr?.matches?.length) {
              const ids = vr.matches.map(m=>m.id);
              const pl = ids.map(()=>'?').join(',');
              const { results: pr } = await env.PAPERS_DB.prepare(`SELECT id, title, authors, doi, abstract FROM papers WHERE id IN (${pl}) AND abstract IS NOT NULL AND abstract != '' LIMIT ?`).bind(...ids, lim).all();
              results = pr || [];
            }
          }
        } catch(e) {}
        if (!results.length) {
          const lq = `%${q}%`;
          const { results: lr } = await env.PAPERS_DB.prepare('SELECT id, title, authors, doi, abstract FROM papers WHERE (title LIKE ? OR abstract LIKE ?) AND abstract IS NOT NULL AND abstract != \'\' LIMIT ?').bind(lq, lq, lim).all();
          results = lr || [];
          if (results.length) method = 'like';
        }
        return J({ success: true, query: q, total: results.length, method, data: results }, 200, h);
      }

      if (p === '/api/ask') {
        const q = url.searchParams.get('q');
        if (!q) return J({ success: false, error: 'Missing ?q=' }, 400, h);
        let ctx = '';
        try {
          const emb = await env.AI.run('@cf/baai/bge-m3', { text: [q] });
          if (emb?.data?.[0]) {
            const vr = await env.VECTORIZE_INDEX.query(emb.data[0], { topK: 5 });
            if (vr?.matches?.length) {
              const ids = vr.matches.map(m=>m.id);
              const pl = ids.map(()=>'?').join(',');
              const { results: pr } = await env.PAPERS_DB.prepare(`SELECT title, abstract FROM papers WHERE id IN (${pl}) AND abstract IS NOT NULL AND abstract != '' LIMIT 5`).bind(...ids).all();
              ctx = (pr||[]).map(x=>'TITLE: '+x.title+'\nABSTRACT: '+(x.abstract||'').substring(0,500)).join('\n\n');
            }
          }
        } catch(e) {}
        if (!ctx) {
          const lq = `%${q}%`;
          const { results: pr } = await env.PAPERS_DB.prepare("SELECT title, abstract FROM papers WHERE (title LIKE ? OR abstract LIKE ?) AND abstract IS NOT NULL AND abstract != '' LIMIT 5").bind(lq,lq).all();
          ctx = (pr||[]).map(x=>'TITLE: '+x.title+'\nABSTRACT: '+(x.abstract||'').substring(0,500)).join('\n\n');
        }
        try {
          const ai = await env.AI.run('@cf/deepseek-ai/deepseek-r1-distill-qwen-32b', {
            messages: [{role:'system',content:'You are QNFO research assistant. Answer based on papers. Be factual. Under 500 words.'}, {role:'user',content:'Question: '+q+'\n\nRelevant papers:\n'+ctx+'\n\nAnswer:'}],
            max_tokens: 600, temperature: 0.3
          });
          return J({ success: true, question: q, answer: ai.response || ai, papers: ctx?ctx.split('TITLE:').length-1:0 }, 200, h);
        } catch(e) {
          const lq = `%${q}%`;
          const { results: pr } = await env.PAPERS_DB.prepare('SELECT id, title, authors, doi FROM papers WHERE title LIKE ? LIMIT 3').bind(lq).all();
          return J({ success: true, question: q, answer: 'AI model loading. Showing relevant papers.', papers: pr||[] }, 200, h);
        }
      }

      // ═══ NEW: /api/seed — Seed Vectorize with paper embeddings ═══
      if (p === '/api/seed') {
        const limit = Math.min(parseInt(url.searchParams.get('limit')||'10'), 50);
        const offset = parseInt(url.searchParams.get('offset')||'0');
        const { results: papers } = await env.PAPERS_DB.prepare('SELECT id, title, abstract FROM papers ORDER BY updated_at DESC LIMIT ? OFFSET ?').bind(limit, offset).all();
        
        let seeded = 0, errors = [];
        const vectors = [];
        
        for (const paper of papers) {
          try {
            const text = (paper.abstract || paper.title || "untitled").substring(0, 2000);
            const emb = await env.AI.run('@cf/baai/bge-m3', { text: [text] });
            if (emb?.data?.[0]) {
              vectors.push({ id: paper.id, values: emb.data[0], metadata: { title: paper.title?.substring(0,100) || '' } });
              seeded++;
            }
          } catch(e) {
            errors.push(`${paper.id}: ${e.message?.substring(0,50)}`);
          }
        }
        
        // Batch upsert
        if (vectors.length > 0) {
          try {
            await env.VECTORIZE_INDEX.upsert(vectors);
          } catch(e) {
            errors.push(`upsert: ${e.message?.substring(0,50)}`);
          }
        }
        
        // Check vector count after seed
        let vc = 0;
        try { const idx = await env.VECTORIZE_INDEX.describe(); vc = idx.vectorCount || 0; } catch(e) {}
        
        return J({ success: true, seeded, total_in_index: vc, errors: errors.slice(0,5), offset, limit }, 200, h);
      }

      if (p === '/api/stats') {
        const { results: t } = await env.PAPERS_DB.prepare('SELECT count(*) as c FROM papers').all();
        const { results: d } = await env.PAPERS_DB.prepare("SELECT count(*) as c FROM papers WHERE doi IS NOT NULL AND doi != ''").all();
        const { results: c } = await env.PAPERS_DB.prepare("SELECT count(*) as c FROM papers WHERE ipfs_cid IS NOT NULL AND ipfs_cid != ''").all();
        return J({ success: true, stats: { total_papers: t[0]?.c||0, with_doi: d[0]?.c||0, with_ipfs: c[0]?.c||0 } }, 200, h);
      }

      // /api/cleanup — Delete papers from D1 (legacy, for stub removal)
      if (p === '/api/cleanup' && request.method === 'POST') {
        const body = await request.json();
        const ids = body.ids || [];
        if (!ids.length) return J({ success: false, error: 'Missing ids array' }, 400, h);
        let deleted = 0, errors = [];
        for (const id of ids) {
          try {
            await env.PAPERS_DB.prepare('DELETE FROM papers WHERE id = ?').bind(id).run();
            deleted++;
          } catch(e) { errors.push(`${id}: ${e.message?.substring(0,50)}`); }
        }
        return J({ success: true, deleted, total: ids.length, errors: errors.slice(0,10) }, 200, h);
      }

      // ═══ v2.5: /api/vector-purge — Delete vectors from Vectorize index ═══
      if (p === '/api/vector-purge' && request.method === 'POST') {
        const body = await request.json();
        const ids = body.ids || [];
        if (!ids.length) return J({ success: false, error: 'Missing ids array' }, 400, h);
        
        let deleted = 0, errors = [];
        // Delete in batches of 50 (Vectorize limit)
        const batchSize = 50;
        for (let i = 0; i < ids.length; i += batchSize) {
          const batch = ids.slice(i, i + batchSize);
          try {
            await env.VECTORIZE_INDEX.deleteByIds(batch);
            deleted += batch.length;
          } catch(e) {
            errors.push(`batch ${i}: ${e.message?.substring(0,80)}`);
          }
        }
        
        // Check vector count after purge
        let vc = 0;
        try { const idx = await env.VECTORIZE_INDEX.describe(); vc = idx.vectorCount || 0; } catch(e) {}
        
        return J({ success: true, deleted, total: ids.length, remaining: vc, errors: errors.slice(0,5) }, 200, h);
      }

      // ═══ v2.6: /api/paper-doi — Update paper DOI in D1 ═══
      if (p === '/api/paper-doi' && request.method === 'POST') {
        const body = await request.json();
        const paper_id = body.paper_id;
        const doi = body.doi;
        if (!paper_id || !doi) return J({ success: false, error: 'Missing paper_id or doi' }, 400, h);
        try {
          await env.PAPERS_DB.prepare('UPDATE papers SET doi = ?, updated_at = datetime(\'now\') WHERE id = ?').bind(doi, paper_id).run();
          return J({ success: true, paper_id, doi, updated: true }, 200, h);
        } catch(e) {
          return J({ success: false, error: e.message?.substring(0,100) }, 500, h);
        }
      }

      // ═══ v2.5: /api/vector-list — List paper IDs that SHOULD be in Vectorize ═══
      if (p === '/api/vector-list') {
        const { results } = await env.PAPERS_DB.prepare('SELECT id FROM papers WHERE abstract IS NOT NULL AND abstract != \'\' ORDER BY id').all();
        const ids = (results||[]).map(r=>r.id);
        let vc = 0;
        try { const idx = await env.VECTORIZE_INDEX.describe(); vc = idx.vectorCount || 0; } catch(e) {}
        return J({ success: true, paper_count: ids.length, vector_count: vc, paper_ids: ids }, 200, h);
      }

      return J({ error: 'Not found', path: p }, 404, h);
    } catch(e) { return J({ error: e.message }, 500, h); }
  }
};
function J(d,s,h){return new Response(JSON.stringify(d),{status:s||200,headers:h||{}})}
