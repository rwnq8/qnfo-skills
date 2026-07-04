/**
 * IPFS Gateway Verifier
 * =====================
 * Tests content availability across multiple IPFS gateways.
 * Used to verify that pinned content is actually retrievable.
 *
 * Tests:
 *   - HTTP 200 from each gateway
 *   - Content hash matches expected SHA-256
 *   - Response time benchmarking
 *   - Gateway health dashboard
 *
 * Usage:
 *   node gateway-verifier.js test <cid>                — Test all gateways
 *   node gateway-verifier.js test <cid> --gateways <n> — Test specific gateways
 *   node gateway-verifier.js dashboard                 — Show gateway health dashboard
 *   node gateway-verifier.js best <cid>                — Find fastest gateway
 */

// ═══════════════════════════════════════════════════════════════
// GATEWAY REGISTRY
// ═══════════════════════════════════════════════════════════════

const GATEWAYS = {
  ipfs_io: {
    name: 'IPFS.io',
    url: 'https://ipfs.io/ipfs/{cid}',
    type: 'public',
    owner: 'Protocol Labs',
    rateLimit: 'Moderate',
    reliability: 'High',
  },
  cloudflare: {
    name: 'Cloudflare IPFS',
    url: 'https://cloudflare-ipfs.com/ipfs/{cid}',
    type: 'public',
    owner: 'Cloudflare',
    rateLimit: 'High',
    reliability: 'Very High',
  },
  dweb_link: {
    name: 'dweb.link',
    url: 'https://dweb.link/ipfs/{cid}',
    type: 'public',
    owner: 'Protocol Labs',
    rateLimit: 'Moderate',
    reliability: 'High',
  },
  pinata: {
    name: 'Pinata',
    url: 'https://gateway.pinata.cloud/ipfs/{cid}',
    type: 'public',
    owner: 'Pinata',
    rateLimit: 'High',
    reliability: 'High',
  },
  foreverland: {
    name: '4EVERLAND',
    url: 'https://4everland.io/ipfs/{cid}',
    type: 'public',
    owner: '4EVERLAND',
    rateLimit: 'Moderate',
    reliability: 'Medium',
  },
  crust: {
    name: 'Crust Network',
    url: 'https://crustwebsites.net/ipfs/{cid}',
    type: 'public',
    owner: 'Crust Network',
    rateLimit: 'Low',
    reliability: 'Medium',
  },
  fleek: {
    name: 'Fleek',
    url: 'https://{cid}.ipfs.fleek.co',
    type: 'public',
    owner: 'Fleek',
    rateLimit: 'High',
    reliability: 'High',
  },
  ipfs_eth_co: {
    name: 'ipfs.eth.co',
    url: 'https://ipfs.eth.co/ipfs/{cid}',
    type: 'public',
    owner: 'ETH.co (deprecated)',
    rateLimit: 'Low',
    reliability: 'Low',
  },
  infura: {
    name: 'Infura IPFS',
    url: 'https://ipfs.infura.io/ipfs/{cid}',
    type: 'public',
    owner: 'Infura',
    rateLimit: 'Moderate',
    reliability: 'High',
  },
  w3s_link: {
    name: 'w3s.link',
    url: 'https://{cid}.ipfs.w3s.link',
    type: 'public',
    owner: 'web3.storage',
    rateLimit: 'High',
    reliability: 'High',
  },
  nftstorage_link: {
    name: 'nftstorage.link',
    url: 'https://{cid}.ipfs.nftstorage.link',
    type: 'public',
    owner: 'NFT.Storage',
    rateLimit: 'High',
    reliability: 'High',
  },
  // Localhost (if IPFS daemon is running)
  localhost: {
    name: 'Local IPFS Daemon',
    url: 'http://127.0.0.1:8080/ipfs/{cid}',
    type: 'local',
    owner: 'Self-hosted',
    rateLimit: 'None',
    reliability: 'Self-managed',
  },
};

// Subdomain gateways (faster, better origin isolation)
const SUBDOMAIN_GATEWAYS = {
  ipfs_io_sub: 'https://{cid}.ipfs.ipfs.io',
  dweb_sub: 'https://{cid}.ipfs.dweb.link',
  cf_sub: 'https://{cid}.ipfs.cloudflare-ipfs.com',
};

// ═══════════════════════════════════════════════════════════════
// VERIFICATION ENGINE
// ═══════════════════════════════════════════════════════════════

async function testGateway(gateway, cid, expectedSha256 = null, timeout = 10000) {
  const url = gateway.url.replace('{cid}', cid);
  const start = Date.now();

  try {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), timeout);

    const response = await fetch(url, {
      signal: controller.signal,
      headers: { 'User-Agent': 'QNFO-Gateway-Verifier/1.0' },
    });
    clearTimeout(timeoutId);

    const buffer = await response.arrayBuffer();
    const elapsed = Date.now() - start;

    // Compute SHA-256 of response body
    const hashBuffer = await crypto.subtle.digest('SHA-256', buffer);
    const sha256 = Array.from(new Uint8Array(hashBuffer))
      .map(b => b.toString(16).padStart(2, '0'))
      .join('');

    const result = {
      gateway: gateway.name,
      url,
      status: response.status,
      size: buffer.byteLength,
      elapsedMs: elapsed,
      sha256,
      hashMatch: expectedSha256 ? sha256 === expectedSha256 : null,
      ok: response.status === 200 && (!expectedSha256 || sha256 === expectedSha256),
    };

    return result;
  } catch (error) {
    const elapsed = Date.now() - start;
    return {
      gateway: gateway.name,
      url,
      status: 0,
      size: 0,
      elapsedMs: elapsed,
      sha256: null,
      hashMatch: false,
      ok: false,
      error: error.name === 'AbortError' ? 'Timeout' : error.message,
    };
  }
}

async function testSubdomainGateway(name, urlTemplate, cid, timeout = 10000) {
  const url = urlTemplate.replace('{cid}', cid);
  const start = Date.now();

  try {
    const controller = new AbortController();
    setTimeout(() => controller.abort(), timeout);

    const response = await fetch(url, {
      signal: controller.signal,
      headers: { 'User-Agent': 'QNFO-Gateway-Verifier/1.0' },
    });

    const buffer = await response.arrayBuffer();
    const elapsed = Date.now() - start;

    const hashBuffer = await crypto.subtle.digest('SHA-256', buffer);
    const sha256 = Array.from(new Uint8Array(hashBuffer))
      .map(b => b.toString(16).padStart(2, '0'))
      .join('');

    return {
      gateway: `${name} (subdomain)`,
      url,
      status: response.status,
      size: buffer.byteLength,
      elapsedMs: elapsed,
      sha256,
      ok: response.status === 200,
    };
  } catch (error) {
    return {
      gateway: `${name} (subdomain)`,
      url,
      status: 0,
      size: 0,
      elapsedMs: Date.now() - start,
      sha256: null,
      ok: false,
      error: error.message,
    };
  }
}

/**
 * Full verification sweep across all gateways.
 */
async function fullVerification(cid, expectedSha256 = null, options = {}) {
  const {
    timeout = 10000,
    concurrency = 5,
    includeSubdomains = true,
    gateways: selectedGateways = null,
  } = options;

  const gatewayList = selectedGateways
    ? Object.fromEntries(selectedGateways.map(k => [k, GATEWAYS[k]]).filter(([, v]) => v))
    : GATEWAYS;

  const subdomainList = includeSubdomains ? SUBDOMAIN_GATEWAYS : {};

  const results = {};

  // Test main gateways in batches
  const gatewayEntries = Object.entries(gatewayList);
  for (let i = 0; i < gatewayEntries.length; i += concurrency) {
    const batch = gatewayEntries.slice(i, i + concurrency);
    const batchResults = await Promise.all(
      batch.map(([key, gw]) => testGateway(gw, cid, expectedSha256, timeout))
    );
    batchResults.forEach((result, idx) => {
      results[batch[idx][0]] = result;
    });
  }

  // Test subdomain gateways
  if (includeSubdomains) {
    const subEntries = Object.entries(subdomainList);
    for (let i = 0; i < subEntries.length; i += concurrency) {
      const batch = subEntries.slice(i, i + concurrency);
      const batchResults = await Promise.all(
        batch.map(([key, url]) => testSubdomainGateway(key, url, cid, timeout))
      );
      batchResults.forEach((result, idx) => {
        results[`${batch[idx][0]}_sub`] = result;
      });
    }
  }

  // Summary stats
  const allResults = Object.values(results);
  const successful = allResults.filter(r => r.ok);
  const failed = allResults.filter(r => !r.ok);
  const avgLatency = successful.length > 0
    ? Math.round(successful.reduce((sum, r) => sum + r.elapsedMs, 0) / successful.length)
    : 0;

  return {
    cid,
    timestamp: new Date().toISOString(),
    summary: {
      total: allResults.length,
      successful: successful.length,
      failed: failed.length,
      successRate: allResults.length > 0
        ? `${Math.round((successful.length / allResults.length) * 100)}%`
        : '0%',
      avgLatencyMs: avgLatency,
      fastest: successful.length > 0
        ? successful.reduce((best, r) => r.elapsedMs < best.elapsedMs ? r : best).gateway
        : null,
      slowest: successful.length > 0
        ? successful.reduce((worst, r) => r.elapsedMs > worst.elapsedMs ? r : worst).gateway
        : null,
    },
    results,
    sha256Consensus: successful.length > 1
      ? checkSHA256Consensus(successful)
      : null,
  };
}

function checkSHA256Consensus(results) {
  const hashes = results.filter(r => r.sha256).map(r => r.sha256);
  const unique = new Set(hashes);
  return {
    consensus: unique.size === 1,
    uniqueHashes: unique.size,
    hash: unique.size === 1 ? hashes[0] : null,
    disagreeCount: hashes.filter(h => h !== hashes[0]).length,
  };
}

// ═══════════════════════════════════════════════════════════════
// GATEWAY DASHBOARD
// ═══════════════════════════════════════════════════════════════

function generateDashboard(verificationResults) {
  console.log(`
╔══════════════════════════════════════════════════════════════════╗
║              IPFS GATEWAY VERIFICATION DASHBOARD                  ║
╠══════════════════════════════════════════════════════════════════╣
║ CID: ${verificationResults.cid.padEnd(54)}║
║ Time: ${verificationResults.timestamp.padEnd(54)}║
╠══════════════════════════════════════════════════════════════════╣
║ Success: ${String(verificationResults.summary.successful).padEnd(4)} / ${String(verificationResults.summary.total).padEnd(4)}  (${verificationResults.summary.successRate.padEnd(4)})                     ║
║ Avg Latency: ${String(verificationResults.summary.avgLatencyMs + 'ms').padEnd(48)}║
╠══════════════════════════════════════════════════════════════════╣`);

  for (const [key, result] of Object.entries(verificationResults.results)) {
    const icon = result.ok ? '✅' : '❌';
    const status = result.ok ? `HTTP ${result.status}` : (result.error || 'FAILED');
    const latency = result.elapsedMs ? `${result.elapsedMs}ms` : '---';
    console.log(`║ ${icon} ${key.padEnd(24)} ${status.padEnd(12)} ${latency.padEnd(8)} ${String(result.size || 0).padEnd(10)}║`);
  }

  console.log(`╚══════════════════════════════════════════════════════════════════╝`);
}

// ═══════════════════════════════════════════════════════════════════
// GATEWAY BEST-PRACTICE GUIDANCE
// ═══════════════════════════════════════════════════════════════════

const GATEWAY_BEST_PRACTICES = {
  production: {
    primary: 'cloudflare-ipfs.com',
    fallback: ['ipfs.io', 'dweb.link'],
    subdomain: true,
    caching: 'CDN-level (Cloudflare)',
    note: 'Cloudflare serves from their global CDN — fastest for most regions.',
  },
  china: {
    primary: '4everland.io',
    fallback: ['crustwebsites.net'],
    subdomain: false,
    note: 'Great Firewall blocks most IPFS gateways. 4EVERLAND has nodes in Asia.',
  },
  archival: {
    primary: 'dweb.link',
    fallback: ['ipfs.io', 'w3s.link'],
    subdomain: true,
    note: 'Protocol Labs gateways have longest uptime guarantees.',
  },
  research: {
    primary: 'cloudflare-ipfs.com',
    fallback: ['ipfs.io', 'dweb.link', 'gateway.pinata.cloud'],
    subdomain: true,
    note: 'Multi-gateway redundancy ensures research content is always available.',
  },
};

// ═══════════════════════════════════════════════════════════════════
// CLI
// ═══════════════════════════════════════════════════════════════════

async function main() {
  const args = process.argv.slice(2);
  const cmd = args[0];

  if (!cmd || cmd === '--help' || cmd === '-h') {
    console.log(`
IPFS Gateway Verifier
======================

Commands:
  test <cid> [sha256]            Test all gateways for a CID
  test <cid> --gateways gw1,gw2  Test specific gateways
  dashboard <result-json>        Display dashboard from saved results
  best <cid>                     Find fastest responding gateway
  practices                      Show gateway best practices by region

Examples:
  node gateway-verifier.js test bafy...abc
  node gateway-verifier.js test bafy...abc --gateways cloudflare,pinata
  node gateway-verifier.js best bafy...abc
`);
    process.exit(0);
  }

  switch (cmd) {
    case 'test': {
      const cid = args[1];
      let expectedSha256 = null;
      let selectedGateways = null;

      // Parse options
      if (args.includes('--sha256')) {
        expectedSha256 = args[args.indexOf('--sha256') + 1];
      }
      if (args.includes('--gateways')) {
        selectedGateways = args[args.indexOf('--gateways') + 1].split(',');
      }

      if (!cid) {
        console.error('[ERROR] CID required');
        process.exit(1);
      }

      console.log(`\nTesting gateways for CID: ${cid}...\n`);
      const results = await fullVerification(cid, expectedSha256, {
        gateways: selectedGateways,
      });

      generateDashboard(results);

      // Save results
      const outPath = `gateway-verification-${cid.slice(0, 12)}.json`;
      const fs = require('fs');
      fs.writeFileSync(outPath, JSON.stringify(results, null, 2));
      console.log(`\n[SAVED] Full results: ${outPath}`);
      break;
    }

    case 'dashboard': {
      const file = args[1];
      if (!file) {
        console.error('[ERROR] Results JSON file required');
        process.exit(1);
      }
      const fs = require('fs');
      const results = JSON.parse(fs.readFileSync(file, 'utf8'));
      generateDashboard(results);
      break;
    }

    case 'best': {
      const cid = args[1];
      if (!cid) {
        console.error('[ERROR] CID required');
        process.exit(1);
      }
      console.log(`\nFinding fastest gateway for: ${cid}...\n`);
      const results = await fullVerification(cid, null, { includeSubdomains: false });
      const successful = Object.values(results.results).filter(r => r.ok);
      if (successful.length === 0) {
        console.log('[FAIL] No gateways returned content successfully.');
      } else {
        successful.sort((a, b) => a.elapsedMs - b.elapsedMs);
        console.log('Top gateways by speed:');
        successful.slice(0, 5).forEach((r, i) => {
          console.log(`  ${i + 1}. ${r.gateway} — ${r.elapsedMs}ms (${r.size}B)`);
        });
      }
      break;
    }

    case 'practices': {
      console.log(JSON.stringify(GATEWAY_BEST_PRACTICES, null, 2));
      break;
    }

    default:
      console.error(`[ERROR] Unknown command: ${cmd}`);
      process.exit(1);
  }
}

module.exports = {
  fullVerification,
  testGateway,
  generateDashboard,
  GATEWAYS,
  SUBDOMAIN_GATEWAYS,
  GATEWAY_BEST_PRACTICES,
};

if (require.main === module) {
  main().catch(err => {
    console.error(`[FATAL] ${err.message}`);
    process.exit(1);
  });
}
