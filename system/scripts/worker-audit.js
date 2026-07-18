#!/usr/bin/env node
// worker-audit.js — List all Workers + bindings + health check
// Usage: node worker-audit.js
// Requires: CLOUDFLARE_API_TOKEN, CLOUDFLARE_ACCOUNT_ID env vars

const T = process.env.CLOUDFLARE_API_TOKEN;
const ACCOUNT = process.env.CLOUDFLARE_ACCOUNT_ID;

async function runWorkerAudit() {
  if (!T) throw new Error('CLOUDFLARE_API_TOKEN not set');
  if (!ACCOUNT) throw new Error('CLOUDFLARE_ACCOUNT_ID not set');

  const w = await (await fetch(`https://api.cloudflare.com/client/v4/accounts/${ACCOUNT}/workers/scripts`, {
    headers: { Authorization: `Bearer ${T}` }
  })).json();

  const results = [];
  for (const wr of (w.result || [])) {
    const b = await (await fetch(`https://api.cloudflare.com/client/v4/accounts/${ACCOUNT}/workers/scripts/${wr.id}/bindings`, {
      headers: { Authorization: `Bearer ${T}` }
    })).json();
    let health = 'unknown';
    try {
      const hr = await fetch(`https://${wr.id}.${ACCOUNT.slice(0, 8)}.workers.dev/health`, { signal: AbortSignal.timeout(5000) });
      health = hr.status === 200 ? 'healthy' : `unhealthy (${hr.status})`;
    } catch (e) { health = 'unreachable'; }
    const bindings = (b.result || []).map(x => `${x.type}:${x.name}`).join(',');
    console.log(`${wr.id}: ${health} [${bindings}]`);
    results.push({ worker: wr.id, health, bindings: b.result || [] });
  }
  return results;
}

if (require.main === module) {
  runWorkerAudit().catch(e => { console.error('FATAL:', e.message); process.exitCode = 1; });
}

module.exports = { runWorkerAudit };
