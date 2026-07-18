#!/usr/bin/env node
// worker-route.js — Bind a domain route to a Cloudflare Worker
// Usage: node worker-route.js <zone_id> <domain-pattern> <worker-name>
// Requires: CLOUDFLARE_API_TOKEN env var

const T = process.env.CLOUDFLARE_API_TOKEN;

async function createWorkerRoute(zoneId, pattern, workerName) {
  if (!T) throw new Error('CLOUDFLARE_API_TOKEN not set');
  const r = await fetch(`https://api.cloudflare.com/client/v4/zones/${zoneId}/workers/routes`, {
    method: 'POST',
    headers: { Authorization: `Bearer ${T}`, 'Content-Type': 'application/json' },
    body: JSON.stringify({ pattern, script: workerName })
  });
  const d = await r.json();
  if (!d.success) {
    console.error('Route creation failed:', JSON.stringify(d.errors));
    process.exitCode = 1;
    return null;
  }
  console.log(`Route created: ${pattern} -> ${workerName}`);
  return d.result;
}

if (require.main === module) {
  const [zoneId, pattern, workerName] = process.argv.slice(2);
  if (!zoneId || !pattern || !workerName) {
    console.error('Usage: node worker-route.js <zone_id> <domain-pattern> <worker-name>');
    process.exit(1);
  }
  createWorkerRoute(zoneId, pattern, workerName).catch(e => { console.error('FATAL:', e.message); process.exitCode = 1; });
}

module.exports = { createWorkerRoute };
