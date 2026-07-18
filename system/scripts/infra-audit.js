#!/usr/bin/env node
// infra-audit.js (system skill copy) — see cloudflare/scripts/infra-audit.js for the canonical version
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

  const [workers, d1, r2, pages, zones] = await Promise.all([
    cf(`/accounts/${ACCOUNT}/workers/scripts`),
    cf(`/accounts/${ACCOUNT}/d1/database`),
    cf(`/accounts/${ACCOUNT}/r2/buckets`),
    cf(`/accounts/${ACCOUNT}/pages/projects`),
    cf(`/zones?per_page=50`)
  ]);

  const summary = {
    workers: (workers.result || []).length,
    d1_databases: (d1.result || []).length,
    r2_buckets: (r2.result?.buckets || r2.result || []).length,
    pages_projects: (pages.result || []).length,
    dns_zones: (zones.result || []).filter(z => z.status === 'active').length
  };
  console.log('=== Infra Audit Summary ===');
  console.log(JSON.stringify(summary, null, 2));
  return summary;
}

if (require.main === module) {
  runInfraAudit().catch(e => { console.error('FATAL:', e.message); process.exitCode = 1; });
}

module.exports = { runInfraAudit };
