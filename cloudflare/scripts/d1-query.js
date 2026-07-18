#!/usr/bin/env node
// d1-query.js — Execute D1 SQL via REST API
// Usage: node d1-query.js <database_id> "<SQL>"
// Requires: CLOUDFLARE_API_TOKEN, CLOUDFLARE_ACCOUNT_ID env vars

const T = process.env.CLOUDFLARE_API_TOKEN;
const ACCOUNT = process.env.CLOUDFLARE_ACCOUNT_ID;

async function d1Query(databaseId, sql, params = []) {
  if (!T) throw new Error('CLOUDFLARE_API_TOKEN not set');
  if (!ACCOUNT) throw new Error('CLOUDFLARE_ACCOUNT_ID not set');
  const r = await fetch(`https://api.cloudflare.com/client/v4/accounts/${ACCOUNT}/d1/database/${databaseId}/query`, {
    method: 'POST',
    headers: { Authorization: `Bearer ${T}`, 'Content-Type': 'application/json' },
    body: JSON.stringify({ sql, params })
  });
  const d = await r.json();
  if (!d.success) {
    console.error('D1 query failed:', JSON.stringify(d.errors));
    process.exitCode = 1;
    return null;
  }
  return d.result;
}

if (require.main === module) {
  const [databaseId, sql] = process.argv.slice(2);
  if (!databaseId || !sql) {
    console.error('Usage: node d1-query.js <database_id> "<SQL>"');
    process.exit(1);
  }
  d1Query(databaseId, sql).then(result => {
    if (result) console.log(JSON.stringify(result, null, 2));
  }).catch(e => { console.error('FATAL:', e.message); process.exitCode = 1; });
}

module.exports = { d1Query };
