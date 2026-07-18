#!/usr/bin/env node
// dnslink-create.js — Map a subdomain to an IPFS CID via DNSLink TXT record
// Usage: node dnslink-create.js <zone_id> <subdomain> <cid>
// Requires: CLOUDFLARE_API_TOKEN env var

const T = process.env.CLOUDFLARE_API_TOKEN;

async function createDnsLink(zoneId, subdomain, cid) {
  if (!T) throw new Error('CLOUDFLARE_API_TOKEN not set');
  const r = await fetch(`https://api.cloudflare.com/client/v4/zones/${zoneId}/dns_records`, {
    method: 'POST',
    headers: { Authorization: `Bearer ${T}`, 'Content-Type': 'application/json' },
    body: JSON.stringify({
      type: 'TXT',
      name: `_dnslink.${subdomain}`,
      content: `dnslink=/ipfs/${cid}`,
      ttl: 1
    })
  });
  const d = await r.json();
  if (!d.success) {
    console.error('DNSLink creation failed:', JSON.stringify(d.errors));
    process.exitCode = 1;
    return null;
  }
  console.log(`DNSLink created: _dnslink.${subdomain} -> dnslink=/ipfs/${cid}`);
  console.log(`Verify: nslookup -type=TXT _dnslink.${subdomain}`);
  console.log(`Gateway: https://cloudflare-ipfs.com/ipns/${subdomain}`);
  return d.result;
}

if (require.main === module) {
  const [zoneId, subdomain, cid] = process.argv.slice(2);
  if (!zoneId || !subdomain || !cid) {
    console.error('Usage: node dnslink-create.js <zone_id> <subdomain> <cid>');
    process.exit(1);
  }
  createDnsLink(zoneId, subdomain, cid).catch(e => { console.error('FATAL:', e.message); process.exitCode = 1; });
}

module.exports = { createDnsLink };
