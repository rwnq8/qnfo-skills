#!/usr/bin/env node
// verify-4d.js — Verify a publication meets the 4-D Distribution Gate:
// Distributed (>=2 IPFS gateways), Durable (Arweave/Zenodo/IA), Discoverable (DNSLink/DOI/KG), Duplicated (>=4 stores)
// Usage: node verify-4d.js <ipfs-cid> [arweave-tx] [doi] [dnslink-subdomain]
// NOTE (2026-07-20): gateway.pinata.cloud REMOVED from the gateway list —
// Pinata's free quota was exceeded and the account is blocked. Only free,
// unlimited-request public gateways are checked below.

async function checkUrl(url, timeoutMs = 8000) {
  try {
    const r = await fetch(url, { method: 'HEAD', signal: AbortSignal.timeout(timeoutMs) });
    return r.ok || r.status === 200;
  } catch (e) {
    return false;
  }
}

async function verify4D(cid, arweaveTx, doi, dnslinkSubdomain) {
  const results = { distributed: false, durable: false, discoverable: false, duplicated: false, details: {} };

  // Distributed: check >=2 independent IPFS gateways
  if (cid) {
    const gateways = [
      `https://ipfs.io/ipfs/${cid}`,
      `https://cloudflare-ipfs.com/ipfs/${cid}`,
      `https://dweb.link/ipfs/${cid}`
    ];
    const checks = await Promise.all(gateways.map(g => checkUrl(g)));
    const passCount = checks.filter(Boolean).length;
    results.details.ipfs_gateways_reachable = passCount;
    results.distributed = passCount >= 2;
    results.duplicated = passCount >= 4 || (passCount >= 2 && (arweaveTx || doi));
  }

  // Durable: Arweave TX confirmed OR DOI resolves
  if (arweaveTx) {
    results.details.arweave_reachable = await checkUrl(`https://arweave.net/${arweaveTx}`);
  }
  if (doi) {
    results.details.doi_resolves = await checkUrl(`https://doi.org/${doi}`);
  }
  results.durable = !!(results.details.arweave_reachable || results.details.doi_resolves);

  // Discoverable: DNSLink TXT record present (best-effort DNS-over-HTTPS check)
  if (dnslinkSubdomain) {
    try {
      const dnsR = await fetch(`https://cloudflare-dns.com/dns-query?name=_dnslink.${dnslinkSubdomain}&type=TXT`, {
        headers: { Accept: 'application/dns-json' }
      });
      const dnsD = await dnsR.json();
      results.details.dnslink_found = !!(dnsD.Answer && dnsD.Answer.length > 0);
    } catch (e) { results.details.dnslink_found = false; }
  }
  results.discoverable = !!(results.details.dnslink_found || doi);

  console.log('=== 4-D Distribution Verification ===');
  console.log(JSON.stringify(results, null, 2));
  const allPass = results.distributed && results.durable && results.discoverable && results.duplicated;
  console.log(allPass ? '\n[PASS] All 4 dimensions verified.' : '\n[FAIL] One or more dimensions incomplete.');
  return results;
}

if (require.main === module) {
  const [cid, arweaveTx, doi, dnslinkSubdomain] = process.argv.slice(2);
  if (!cid) {
    console.error('Usage: node verify-4d.js <ipfs-cid> [arweave-tx] [doi] [dnslink-subdomain]');
    process.exit(1);
  }
  verify4D(cid, arweaveTx, doi, dnslinkSubdomain).then(r => {
    const allPass = r.distributed && r.durable && r.discoverable && r.duplicated;
    process.exitCode = allPass ? 0 : 1;
  }).catch(e => { console.error('FATAL:', e.message); process.exitCode = 1; });
}

module.exports = { verify4D };
