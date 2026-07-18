#!/usr/bin/env node
// kg-seed-4d.js — Seed/update a Knowledge Graph node with 4-D distribution properties
// Usage: node kg-seed-4d.js <memory-mcp-base-url> <node-id> <properties-json>
// Example: node kg-seed-4d.js https://qnfo-memory-mcp.q08.workers.dev paper-my-slug '{"ipfs_cid":"bafy...","dns_link":"_dnslink.my-slug.qnfo.org","zenodo_doi":"10.5281/zenodo.X","distribution_status":"complete"}'

async function seedKG4D(baseUrl, nodeId, properties) {
  const sql = `UPDATE nodes SET properties = json_patch(properties, ?) WHERE id = ?`;
  const r = await fetch(`${baseUrl}/mcp`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      jsonrpc: '2.0', id: 1, method: 'tools/call',
      params: { name: 'query_graph', arguments: { endpoint: 'query', params: { query: sql, params: [JSON.stringify(properties), nodeId] } } }
    })
  });
  const d = await r.json();
  console.log('KG 4-D seed result:', JSON.stringify(d, null, 2));
  return d;
}

if (require.main === module) {
  const [baseUrl, nodeId, propsJson] = process.argv.slice(2);
  if (!baseUrl || !nodeId || !propsJson) {
    console.error('Usage: node kg-seed-4d.js <memory-mcp-base-url> <node-id> <properties-json>');
    process.exit(1);
  }
  let properties;
  try { properties = JSON.parse(propsJson); } catch (e) {
    console.error('Invalid JSON for properties:', e.message);
    process.exit(1);
  }
  seedKG4D(baseUrl, nodeId, properties).catch(e => { console.error('FATAL:', e.message); process.exitCode = 1; });
}

module.exports = { seedKG4D };
