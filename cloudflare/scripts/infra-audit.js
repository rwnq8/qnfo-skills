#!/usr/bin/env node
// infra-audit.js — Full Cloudflare fleet audit: Workers, D1, R2, Vectorize, Queues, KV, Pages, DNS
// Usage: node infra-audit.js
// Requires: CLOUDFLARE_API_TOKEN, CLOUDFLARE_ACCOUNT_ID env vars

const T = process.env.CLOUDFLARE_API_TOKEN;
const ACCOUNT = process.env.CLOUDFLARE_ACCOUNT_ID;

async function cf(path) {
  const r = await fetch(`https://api.cloudflare.com/client/v4${path}`, { headers: { Authorization: `Bearer ${T}` } });
  return r.json();
}

async function runInfraAudit() {
  if (!T) throw new Error('CLOUDFLARE_API_TOKEN not set');
  if (!ACCOUNT) throw new Error('CLOUDFLARE_ACCOUNT_ID not set');

  const [workers, d1, r2, vectorize, queues, kv, pages, zones] = await Promise.all([
    cf(`/accounts/${ACCOUNT}/workers/scripts`),
    cf(`/accounts/${ACCOUNT}/d1/database`),
    cf(`/accounts/${ACCOUNT}/r2/buckets`),
    cf(`/accounts/${ACCOUNT}/vectorize/v2/indexes`),
    cf(`/accounts/${ACCOUNT}/queues`),
    cf(`/accounts/${ACCOUNT}/storage/kv/namespaces`),
    cf(`/accounts/${ACCOUNT}/pages/projects`),
    cf(`/zones?per_page=50`)
  ]);

  const summary = {
    workers: (workers.result || []).length,
    d1_databases: (d1.result || []).length,
    r2_buckets: (r2.result?.buckets || r2.result || []).length,
    vectorize_indexes: (vectorize.result || []).length,
    queues: (queues.result || []).length,
    kv_namespaces: (kv.result || []).length,
    pages_projects: (pages.result || []).length,
    dns_zones: (zones.result || []).filter(z => z.status === 'active').length
  };

  console.log('=== Cloudflare Infrastructure Audit ===');
  console.log(JSON.stringify(summary, null, 2));
  console.log('\nWorkers:', (workers.result || []).map(w => w.id).join(', '));
  console.log('D1 Databases:', (d1.result || []).map(d => d.name).join(', '));
  console.log('Pages Projects:', (pages.result || []).map(p => p.name).join(', '));
  console.log('DNS Zones:', (zones.result || []).map(z => z.name).join(', '));

  return summary;
}

if (require.main === module) {
  runInfraAudit().catch(e => { console.error('FATAL:', e.message); process.exitCode = 1; });
}

module.exports = { runInfraAudit };
