/**
 * QNFO Unified API Gateway v2.4 — Phase 3 catch-all proxy architecture.
 * All routes proxy to backend workers with path-prefix stripping + safe header forwarding.
 * Single entry point per MASTER-PLAN: api-gateway.q08.workers.dev
 */
export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    const p = url.pathname;
    const q = url.search;
    const h = { 'Access-Control-Allow-Origin': '*', 'Content-Type': 'application/json' };
    if (request.method === 'OPTIONS') return new Response(null, { status: 204, headers: h });

    // Helper: build safe headers for proxy forwarding (strip CF connection headers)
    const proxyHeaders = () => {
      const fwd = new Headers();
      for (const [k, v] of request.headers) {
        const kl = k.toLowerCase();
        if (!['host','cf-connecting-ip','cf-ipcountry','cf-ray','cf-visitor','cdn-loop','cf-ew-via'].includes(kl)) {
          fwd.set(k, v);
        }
      }
      fwd.set('X-Forwarded-By', 'api-gateway-v2.4');
      return fwd;
    };

    // Helper: proxy to target worker with safe headers
    const proxy = async (targetUrl) => {
      try {
        const r = await fetch(targetUrl, { method: request.method, headers: proxyHeaders() });
        return new Response(r.body, { status: r.status, statusText: r.statusText,
          headers: { ...h, 'Content-Type': r.headers.get('Content-Type') || 'application/json' } });
      } catch(e) {
        return new Response(JSON.stringify({ error: 'Proxy failed', detail: e.message }), { status: 502, headers: h });
      }
    };

    // ── Root / API index ──
    if (p === '/' || p === '/api') {
      return new Response(JSON.stringify({
        service: 'QNFO Unified API Gateway v2.4',
        base: url.origin,
        health: url.origin + '/health',
        routes: {
          '/cms/*':    '→ cms-api.q08.workers.dev',
          '/papers/*': '→ ask-qwav.q08.workers.dev v2.8',
          '/search/*': '→ ask-qwav.q08.workers.dev v2.8 (vectorize + AI)',
          '/graph/*':  '→ graph-api.q08.workers.dev (432n/1123e)',
          '/data/*':   '→ qnfo-data-api.q08.workers.dev',
        }
      }), { status: 200, headers: h });
    }

    // ── Health aggregation ──
    if (p === '/health') {
      try {
        const [papers, graph] = await Promise.all([
          fetch('https://ask-qwav.q08.workers.dev/health').then(r=>r.ok?r.json():null).catch(()=>null),
          fetch('https://graph-api.q08.workers.dev/stats').then(r=>r.ok?r.json():null).catch(()=>null),
        ]);
        return new Response(JSON.stringify({ gateway: 'v2.4', papers, graph }), { status: 200, headers: h });
      } catch(e) {
        return new Response(JSON.stringify({ gateway: 'v2.4', error: e.message }), { status: 500, headers: h });
      }
    }

    // ── PATH-PREFIX PROXY ROUTING (strip prefix before forwarding) ──

    if (p.startsWith('/cms'))   return proxy('https://cms-api.q08.workers.dev'         + p.replace(/^\/cms/,   '') + q);
    if (p.startsWith('/papers')) return proxy('https://ask-qwav.q08.workers.dev'      + p.replace(/^\/papers/,'') + q);
    if (p.startsWith('/search')) return proxy('https://ask-qwav.q08.workers.dev'      + p.replace(/^\/search/,'') + q);
    if (p.startsWith('/graph'))  return proxy('https://graph-api.q08.workers.dev'      + p.replace(/^\/graph/, '') + q);
    if (p.startsWith('/data'))   return proxy('https://qnfo-data-api.q08.workers.dev'  + p.replace(/^\/data/,  '') + q);

    return new Response(JSON.stringify({ error: 'Not found', path: p, routes: url.origin + '/' }), { status: 404, headers: h });
  }
};
