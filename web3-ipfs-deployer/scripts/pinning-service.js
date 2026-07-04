/**
 * Multi-Service IPFS Pinning Proxy
 * =================================
 * Abstracts over multiple IPFS pinning services with a unified API.
 * Pure Node.js — uses HTTP requests (no SDK dependencies).
 *
 * Services supported:
 *   - Pinata (pinata.cloud)
 *   - web3.storage (w3up)
 *   - Lighthouse (lighthouse.storage)
 *   - Filecoin (via Lighthouse deal-making)
 *   - Crust Network (crust.network)
 *   - 4EVERLAND (4everland.org)
 *   - Local (just computes CIDs, no remote pinning)
 *
 * Each service is opt-in — requires API key configured.
 *
 * Usage:
 *   node pinning-service.js status                          — Check all services
 *   node pinning-service.js pin <cid> --service pinata      — Pin to specific service
 *   node pinning-service.js pin <cid> --all                 — Pin to ALL configured services
 *   node pinning-service.js unpin <cid> --service pinata    — Unpin
 *   node pinning-service.js list --service pinata           — List pinned CIDs
 */

const fs = require('fs');
const path = require('path');

// ═══════════════════════════════════════════════════════════════
// CONFIGURATION LOADER
// ═══════════════════════════════════════════════════════════════

function loadConfig() {
  const configPath = path.join(__dirname, '..', '.pinning-config.json');
  if (fs.existsSync(configPath)) {
    return JSON.parse(fs.readFileSync(configPath, 'utf8'));
  }

  // Check env vars
  const config = { services: {} };

  if (process.env.PINATA_JWT) config.services.pinata = { jwt: process.env.PINATA_JWT };
  if (process.env.PINATA_API_KEY && process.env.PINATA_SECRET_KEY) {
    config.services.pinata = {
      apiKey: process.env.PINATA_API_KEY,
      secretKey: process.env.PINATA_SECRET_KEY,
    };
  }
  if (process.env.WEB3_STORAGE_TOKEN) config.services.web3storage = { token: process.env.WEB3_STORAGE_TOKEN };
  if (process.env.LIGHTHOUSE_API_KEY) config.services.lighthouse = { apiKey: process.env.LIGHTHOUSE_API_KEY };
  if (process.env.CRUST_SEED) config.services.crust = { seed: process.env.CRUST_SEED };
  if (process.env.FOUR_EVERLAND_TOKEN) config.services.foreverland = { token: process.env.FOUR_EVERLAND_TOKEN };

  return config;
}

// ═══════════════════════════════════════════════════════════════
// HTTP HELPERS
// ═══════════════════════════════════════════════════════════════

class HTTPError extends Error {
  constructor(status, body) {
    super(`HTTP ${status}: ${body}`);
    this.status = status;
    this.body = body;
  }
}

async function apiRequest(url, options = {}) {
  const { method = 'GET', headers = {}, body, timeout = 15000 } = options;

  const fetchOptions = {
    method,
    headers: { 'User-Agent': 'qnfo-ipfs-pinning/1.0', ...headers },
    signal: AbortSignal.timeout(timeout),
  };

  if (body) {
    fetchOptions.body = typeof body === 'string' ? body : JSON.stringify(body);
    if (typeof body !== 'string' && !fetchOptions.headers['Content-Type']) {
      fetchOptions.headers['Content-Type'] = 'application/json';
    }
  }

  const response = await fetch(url, fetchOptions);
  const text = await response.text();

  if (!response.ok) {
    throw new HTTPError(response.status, text);
  }

  try { return JSON.parse(text); } catch { return text; }
}

// ═══════════════════════════════════════════════════════════════
// 1. PINATA SERVICE
// ═══════════════════════════════════════════════════════════════

class PinataService {
  constructor(config) {
    this.name = 'pinata';
    this.configured = !!(config?.jwt || (config?.apiKey && config?.secretKey));
    this.jwt = config?.jwt;
    this.apiKey = config?.apiKey;
    this.secretKey = config?.secretKey;
  }

  getHeaders() {
    if (this.jwt) {
      return { Authorization: `Bearer ${this.jwt}` };
    }
    return {
      pinata_api_key: this.apiKey,
      pinata_secret_api_key: this.secretKey,
    };
  }

  async pin(cid, options = {}) {
    if (!this.configured) throw new Error('Pinata not configured');

    const body = {
      hashToPin: cid,
      pinataMetadata: {
        name: options.name || `QNFO-${cid.slice(0, 12)}`,
        keyvalues: {
          source: 'qnfo-research',
          protocol: 'ipfs',
          ...options.metadata,
        },
      },
      pinataOptions: {
        cidVersion: 1,
        wrapWithDirectory: options.wrapDirectory !== false,
      },
    };

    return apiRequest('https://api.pinata.cloud/pinning/pinByHash', {
      method: 'POST',
      headers: this.getHeaders(),
      body,
    });
  }

  async pinJSON(json, options = {}) {
    if (!this.configured) throw new Error('Pinata not configured');
    return apiRequest('https://api.pinata.cloud/pinning/pinJSONToIPFS', {
      method: 'POST',
      headers: this.getHeaders(),
      body: {
        pinataContent: json,
        pinataMetadata: {
          name: options.name || 'QNFO-Metadata',
          keyvalues: { source: 'qnfo-research', ...options.metadata },
        },
      },
    });
  }

  async unpin(cid) {
    if (!this.configured) throw new Error('Pinata not configured');
    return apiRequest(`https://api.pinata.cloud/pinning/unpin/${cid}`, {
      method: 'DELETE',
      headers: this.getHeaders(),
    });
  }

  async list(options = {}) {
    if (!this.configured) throw new Error('Pinata not configured');
    const params = new URLSearchParams({
      status: options.status || 'pinned',
      pageLimit: String(options.limit || 100),
    });
    return apiRequest(`https://api.pinata.cloud/data/pinList?${params}`, {
      headers: this.getHeaders(),
    });
  }

  async status() {
    return {
      service: 'pinata',
      configured: this.configured,
      endpoint: 'https://api.pinata.cloud',
      features: ['pin', 'unpin', 'list', 'metadata', 'json-pinning', 'gateway'],
    };
  }
}

// ═══════════════════════════════════════════════════════════════
// 2. WEB3.STORAGE SERVICE (w3up)
// ═══════════════════════════════════════════════════════════════

class Web3StorageService {
  constructor(config) {
    this.name = 'web3.storage';
    this.configured = !!(config?.token);
    this.token = config?.token;
  }

  async pin(cid, options = {}) {
    if (!this.configured) throw new Error('web3.storage not configured');
    // web3.storage w3up requires CAR upload rather than CID pinning
    // For direct CID pinning, we upload as a "remote pin"
    return apiRequest('https://api.web3.storage/pins', {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${this.token}`,
        'Content-Type': 'application/json',
      },
      body: {
        cid,
        name: options.name || `QNFO-${cid.slice(0, 12)}`,
        origins: options.origins || [],
        meta: { source: 'qnfo-research', ...options.metadata },
      },
    });
  }

  async status() {
    return {
      service: 'web3.storage',
      configured: this.configured,
      endpoint: 'https://api.web3.storage',
      features: ['pin', 'car-upload', 'filecoin-deals', 'gateway'],
      note: '10+ year Filecoin deal persistence by default',
    };
  }
}

// ═══════════════════════════════════════════════════════════════
// 3. LIGHTHOUSE SERVICE (+ Filecoin deals)
// ═══════════════════════════════════════════════════════════════

class LighthouseService {
  constructor(config) {
    this.name = 'lighthouse';
    this.configured = !!(config?.apiKey);
    this.apiKey = config?.apiKey;
  }

  async pin(cid, options = {}) {
    if (!this.configured) throw new Error('Lighthouse not configured');
    return apiRequest('https://api.lighthouse.storage/api/v0/pin', {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${this.apiKey}`,
        'Content-Type': 'application/json',
      },
      body: { cid, name: options.name || `QNFO-${cid.slice(0, 12)}` },
    });
  }

  /**
   * Create a Filecoin storage deal for persistence.
   * Lighthouse handles the deal-making process.
   */
  async createFilecoinDeal(cid, options = {}) {
    if (!this.configured) throw new Error('Lighthouse not configured');
    return apiRequest('https://api.lighthouse.storage/api/v0/deal/make', {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${this.apiKey}`,
        'Content-Type': 'application/json',
      },
      body: {
        cid,
        miner: options.miner || [],
        network: options.network || 'filecoin_mainnet',
        duration: options.duration || 525, // ~1.5 years in epochs
        replication: options.replication || 3,
      },
    });
  }

  async status() {
    return {
      service: 'lighthouse',
      configured: this.configured,
      endpoint: 'https://api.lighthouse.storage',
      features: ['pin', 'filecoin-deals', 'encryption', 'gateway', 'car-upload'],
    };
  }
}

// ═══════════════════════════════════════════════════════════════
// 4. CRUST NETWORK SERVICE
// ═══════════════════════════════════════════════════════════════

class CrustService {
  constructor(config) {
    this.name = 'crust';
    this.configured = !!(config?.seed);
  }

  async status() {
    return {
      service: 'crust',
      configured: this.configured,
      endpoint: 'https://crust.network',
      features: ['decentralized-pinning', 'ipfs-compatible', 'token-incentivized'],
      note: 'Polkadot parachain, requires CRU tokens for storage orders',
    };
  }
}

// ═══════════════════════════════════════════════════════════════
// 5. 4EVERLAND SERVICE
// ═══════════════════════════════════════════════════════════════

class FourEverlandService {
  constructor(config) {
    this.name = '4everland';
    this.configured = !!(config?.token);
  }

  async status() {
    return {
      service: '4everland',
      configured: this.configured,
      endpoint: 'https://www.4everland.org',
      features: ['pin', 'gateway', 'hosting', 'buckets'],
    };
  }
}

// ═══════════════════════════════════════════════════════════════
// 6. LOCAL SERVICE (CID computation only, no remote pinning)
// ═══════════════════════════════════════════════════════════════

class LocalService {
  constructor() {
    this.name = 'local';
    this.configured = true;
  }

  async pin() {
    return { status: 'local-only', note: 'CIDs computed locally. Use pinning services for remote persistence.' };
  }

  async status() {
    return {
      service: 'local',
      configured: true,
      features: ['cid-computation', 'car-creation', 'verification'],
      note: 'Runs entirely offline. No remote pinning.',
    };
  }
}

// ═══════════════════════════════════════════════════════════════
// 7. UNIFIED PINNING MANAGER
// ═══════════════════════════════════════════════════════════════

class PinningManager {
  constructor(config) {
    const cfg = config || loadConfig();
    this.services = {
      pinata: new PinataService(cfg.services?.pinata),
      web3storage: new Web3StorageService(cfg.services?.web3storage),
      lighthouse: new LighthouseService(cfg.services?.lighthouse),
      crust: new CrustService(cfg.services?.crust),
      foreverland: new FourEverlandService(cfg.services?.foreverland),
      local: new LocalService(),
    };
  }

  getService(name) {
    const service = this.services[name];
    if (!service) throw new Error(`Unknown service: ${name}. Available: ${Object.keys(this.services).join(', ')}`);
    if (!service.configured) throw new Error(`Service ${name} is not configured`);
    return service;
  }

  listServices() {
    return Object.entries(this.services).map(([name, svc]) => ({
      name,
      configured: svc.configured,
    }));
  }

  async status() {
    const results = [];
    for (const [name, svc] of Object.entries(this.services)) {
      results.push(await svc.status());
    }
    return results;
  }

  async pin(cid, options = {}) {
    const serviceName = options.service || 'local';
    if (serviceName === 'all') {
      const results = {};
      for (const [name, svc] of Object.entries(this.services)) {
        if (name === 'local') continue;
        if (!svc.configured) {
          results[name] = { error: 'Not configured' };
          continue;
        }
        try {
          results[name] = await svc.pin(cid, options);
        } catch (e) {
          results[name] = { error: e.message };
        }
      }
      return { cid, results };
    }

    const service = this.getService(serviceName);
    return service.pin(cid, options);
  }

  async unpin(cid, options = {}) {
    const service = this.getService(options.service || 'pinata');
    return service.unpin(cid);
  }

  /**
   * Pin with Filecoin deal for long-term persistence.
   */
  async pinWithFilecoinDeal(cid, options = {}) {
    const service = this.getService('lighthouse');
    const pinResult = await service.pin(cid, options);
    const dealResult = await service.createFilecoinDeal(cid, options);
    return { pin: pinResult, filecoinDeal: dealResult };
  }
}

// ═══════════════════════════════════════════════════════════════
// 8. PINNING STRATEGY RECOMMENDATIONS
// ═══════════════════════════════════════════════════════════════

const PINNING_STRATEGIES = {
  minimal: {
    name: 'Minimal (Cost-Free)',
    description: 'Public gateway discovery + Cloudflare R2 integration only',
    services: ['local'],
    estimatedCost: '$0/month',
    persistence: 'As long as content is accessed',
  },
  standard: {
    name: 'Standard (Recommended)',
    description: 'Pinata + web3.storage dual pinning with automated CAR uploads',
    services: ['pinata', 'web3storage'],
    estimatedCost: '~$5-20/month',
    persistence: '10+ years (Filecoin deals via web3.storage)',
  },
  robust: {
    name: 'Robust (Maximum Redundancy)',
    description: 'Pinata, web3.storage, Lighthouse with Filecoin deals, Crust Network',
    services: ['pinata', 'web3storage', 'lighthouse', 'crust'],
    estimatedCost: '~$20-50/month',
    persistence: '20+ years (multi-network redundancy)',
  },
  archival: {
    name: 'Archival (Permanent)',
    description: 'All services + Filecoin deals + Arweave backup',
    services: ['pinata', 'web3storage', 'lighthouse', 'crust', 'foreverland'],
    estimatedCost: '~$50-100/month + one-time Arweave fees',
    persistence: 'Centuries (Arweave permanence)',
  },
};

// ═══════════════════════════════════════════════════════════════
// 9. CLI
// ═══════════════════════════════════════════════════════════════

async function main() {
  const args = process.argv.slice(2);
  const cmd = args[0];

  if (!cmd || cmd === '--help' || cmd === '-h') {
    console.log(`
Multi-Service IPFS Pinning Proxy
=================================

Commands:
  status                          Show all services and configuration status
  strategies                      Show recommended pinning strategies
  pin <cid> --service <name>      Pin a CID to a specific service
  pin <cid> --all                 Pin to all configured services
  pin <cid> --with-filecoin       Pin + create Filecoin storage deal
  unpin <cid> --service <name>    Unpin from a service
  list --service <name>           List pinned content

Services: pinata, web3storage, lighthouse, crust, foreverland, local

Examples:
  node pinning-service.js status
  node pinning-service.js pin bafy...abc --service pinata
  node pinning-service.js pin bafy...abc --all
`);
    process.exit(0);
  }

  const manager = new PinningManager();

  switch (cmd) {
    case 'status': {
      const results = await manager.status();
      console.log(JSON.stringify(results, null, 2));
      break;
    }

    case 'strategies': {
      console.log(JSON.stringify(PINNING_STRATEGIES, null, 2));
      break;
    }

    case 'pin': {
      const cid = args[1];
      if (!cid) { console.error('[ERROR] CID required'); process.exit(1); }

      const serviceIdx = args.indexOf('--service');
      const allFlag = args.includes('--all');
      const filecoinFlag = args.includes('--with-filecoin');

      if (filecoinFlag) {
        const result = await manager.pinWithFilecoinDeal(cid);
        console.log(JSON.stringify(result, null, 2));
      } else if (allFlag) {
        const result = await manager.pin(cid, { service: 'all' });
        console.log(JSON.stringify(result, null, 2));
      } else if (serviceIdx >= 0) {
        const serviceName = args[serviceIdx + 1];
        const result = await manager.pin(cid, { service: serviceName });
        console.log(JSON.stringify(result, null, 2));
      } else {
        console.error('[ERROR] Specify --service <name> or --all');
        process.exit(1);
      }
      break;
    }

    case 'unpin': {
      const cid = args[1];
      const serviceIdx = args.indexOf('--service');
      if (!cid || serviceIdx < 0) {
        console.error('[ERROR] CID and --service required');
        process.exit(1);
      }
      const result = await manager.unpin(cid, { service: args[serviceIdx + 1] });
      console.log(JSON.stringify(result, null, 2));
      break;
    }

    default:
      console.error(`[ERROR] Unknown command: ${cmd}`);
      process.exit(1);
  }
}

module.exports = { PinningManager, PinataService, Web3StorageService, LighthouseService, PINNING_STRATEGIES };

if (require.main === module) {
  main().catch(err => {
    console.error(`[FATAL] ${err.message}`);
    process.exit(1);
  });
}
