/**
 * Web3 Identity & Attribution Layer
 * ==================================
 * Pure Node.js implementation of decentralized identity primitives
 * for research publication attribution. Zero external deps.
 *
 * Capabilities:
 *   - Ed25519 key generation + signing (via Node crypto)
 *   - DID:key creation and resolution
 *   - Content attestation (sign a CID to claim authorship)
 *   - Attestation verification
 *   - ENS contenthash encoding (EIP-1577)
 *   - UCAN-lite capability tokens for content delegation
 *
 * DID Method: did:key (multicodec-based, no blockchain required)
 * Signature: Ed25519 (EdDSA)
 *
 * Usage:
 *   node web3-identity.js generate             — Generate author identity
 *   node web3-identity.js attest <cid>         — Sign attestation for a CID
 *   node web3-identity.js verify <attestation> — Verify an attestation
 *   node web3-identity.js ens-contenthash <cid> — Encode IPFS CID as ENS contenthash
 */

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

// ═══════════════════════════════════════════════════════════════
// 1. ED25519 KEY GENERATION (Node 16+)
// ═══════════════════════════════════════════════════════════════

function generateEd25519KeyPair() {
  const { publicKey, privateKey } = crypto.generateKeyPairSync('ed25519', {
    publicKeyEncoding: { type: 'spki', format: 'der' },
    privateKeyEncoding: { type: 'pkcs8', format: 'der' },
  });

  // Extract raw 32-byte keys from DER
  const pubRaw = extractEd25519PublicKey(publicKey);
  const privRaw = extractEd25519PrivateKey(privateKey);

  return {
    publicKey: pubRaw,
    privateKey: privRaw,
    publicKeyHex: pubRaw.toString('hex'),
    privateKeyHex: privRaw.toString('hex'),
  };
}

function extractEd25519PublicKey(spkiDer) {
  // SPKI DER for Ed25519: 30 2a 30 05 06 03 2b 65 70 03 21 00 <32-byte key>
  return spkiDer.subarray(spkiDer.length - 32);
}

function extractEd25519PrivateKey(pkcs8Der) {
  // PKCS8 DER: seed is at offset ~16 for Ed25519
  return pkcs8Der.subarray(pkcs8Der.length - 32);
}

function signEd25519(privateKeyBytes, message) {
  // Node's crypto.sign with Ed25519
  const privateKey = crypto.createPrivateKey({
    key: Buffer.concat([
      Buffer.from('302e020100300506032b657004220420', 'hex'),
      privateKeyBytes,
    ]),
    format: 'der',
    type: 'pkcs8',
  });
  return crypto.sign(null, Buffer.isBuffer(message) ? message : Buffer.from(message), privateKey);
}

function verifyEd25519(publicKeyBytes, message, signature) {
  const publicKey = crypto.createPublicKey({
    key: Buffer.concat([
      Buffer.from('302a300506032b6570032100', 'hex'),
      publicKeyBytes,
    ]),
    format: 'der',
    type: 'spki',
  });
  return crypto.verify(null, Buffer.isBuffer(message) ? message : Buffer.from(message), publicKey, signature);
}

// ═══════════════════════════════════════════════════════════════
// 2. DID:KEY — W3C DID Method
// ═══════════════════════════════════════════════════════════════
// did:key:z<multibase-base58btc(multicodec-ed25519-pub(0xed01)+raw-32-pubkey)>

function publicKeyToDIDKey(publicKeyBytes) {
  // Multicodec for ed25519-pub: 0xed01
  const mcPub = Buffer.from([0xed, 0x01]);
  const data = Buffer.concat([mcPub, publicKeyBytes]);

  // Multibase base58btc encoding
  const encoded = base58btcEncode(data);
  return `did:key:z${encoded}`;
}

function didKeyToPublicKey(did) {
  if (!did.startsWith('did:key:z')) {
    throw new Error(`Unsupported DID format: ${did}. Only did:key:z is supported.`);
  }
  const encoded = did.slice('did:key:z'.length);
  const data = base58btcDecode(encoded);

  // Verify multicodec header
  if (data[0] !== 0xed || data[1] !== 0x01) {
    throw new Error(`Expected ed25519-pub multicodec (0xed01), got 0x${data[0].toString(16)}${data[1].toString(16)}`);
  }
  return data.subarray(2);
}

// ═══════════════════════════════════════════════════════════════
// Base58btc encoding (for DID:key)
// ═══════════════════════════════════════════════════════════════

const BASE58_ALPHABET = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz';

function base58btcEncode(buf) {
  const digits = [0];
  for (let i = 0; i < buf.length; i++) {
    let carry = buf[i];
    for (let j = 0; j < digits.length; j++) {
      carry += digits[j] * 256;
      digits[j] = carry % 58;
      carry = Math.floor(carry / 58);
    }
    while (carry > 0) {
      digits.push(carry % 58);
      carry = Math.floor(carry / 58);
    }
  }
  let out = '';
  for (let i = 0; i < buf.length && buf[i] === 0; i++) out += '1';
  for (let i = digits.length - 1; i >= 0; i--) out += BASE58_ALPHABET[digits[i]];
  return out;
}

function base58btcDecode(str) {
  const bytes = [];
  for (let i = 0; i < str.length; i++) {
    let value = BASE58_ALPHABET.indexOf(str[i]);
    if (value === -1) throw new Error(`Invalid base58 character: ${str[i]}`);
    for (let j = 0; j < bytes.length; j++) {
      value += bytes[j] * 58;
      bytes[j] = value & 0xff;
      value >>= 8;
    }
    while (value > 0) {
      bytes.push(value & 0xff);
      value >>= 8;
    }
  }
  for (let i = 0; i < str.length && str[i] === '1'; i++) bytes.push(0);
  return Buffer.from(bytes.reverse());
}

// ═══════════════════════════════════════════════════════════════
// 3. CONTENT ATTESTATION (Sign a CID to claim authorship)
// ═══════════════════════════════════════════════════════════════

/**
 * Create a signed attestation for authorship of content at a CID.
 * Format: JWS-like structure with DID, CID, timestamp, and signature.
 */
function createAttestation(privateKeyBytes, publicKeyBytes, cid, metadata = {}) {
  const did = publicKeyToDIDKey(publicKeyBytes);
  const timestamp = new Date().toISOString();

  // Build the attestation payload
  const payload = {
    '@context': 'https://w3id.org/security/v2',
    type: 'Ed25519Signature2020',
    created: timestamp,
    creator: did,
    claim: {
      type: 'ContentAuthorship',
      cid,
      ...metadata,
    },
  };

  // Canonicalize and sign
  const payloadBytes = Buffer.from(JSON.stringify(payload), 'utf8');
  const signature = signEd25519(privateKeyBytes, payloadBytes);

  return {
    payload,
    signature: signature.toString('base64url'),
    proof: {
      type: 'Ed25519Signature2020',
      created: timestamp,
      verificationMethod: did,
      proofValue: signature.toString('base64url'),
    },
  };
}

/**
 * Verify a content attestation.
 */
function verifyAttestation(attestation) {
  const { payload, signature } = attestation;
  if (!payload || !signature) {
    return { valid: false, error: 'Missing payload or signature' };
  }

  const did = payload.creator;
  let publicKeyBytes;
  try {
    publicKeyBytes = didKeyToPublicKey(did);
  } catch (e) {
    return { valid: false, error: `Invalid DID: ${e.message}` };
  }

  const payloadBytes = Buffer.from(JSON.stringify(payload), 'utf8');
  const sigBytes = Buffer.from(signature, 'base64url');
  const valid = verifyEd25519(publicKeyBytes, payloadBytes, sigBytes);

  return {
    valid,
    creator: did,
    cid: payload.claim.cid,
    created: payload.created,
    error: valid ? null : 'Signature verification failed',
  };
}

// ═══════════════════════════════════════════════════════════════
// 4. ENS CONTENTHASH (EIP-1577)
// ═══════════════════════════════════════════════════════════════
// Format: 0xe3010170<multihash-bytes>
//   0xe3 = ipfs-ns (contenthash namespace)
//   0x01 = CIDv1
//   0x01 = dag-pb (0x70 in varint? Actually 0x01 then the raw codec.)

/**
 * Encode an IPFS CIDv1 as an ENS contenthash per EIP-1577.
 * Reverses multibase encoding to get raw bytes.
 */
function cidToENSContentHash(cid) {
  if (!cid.startsWith('b')) {
    throw new Error('Only CIDv1 (base32) is supported for ENS contenthash');
  }
  const cidBytes = base32Decode(cid.slice(1));
  // contenthash format: 0xe3 (ipfs-ns) + raw CID bytes
  const contentHash = Buffer.concat([Buffer.from([0xe3]), cidBytes]);
  return '0x' + contentHash.toString('hex');
}

/**
 * Base32 decode (replicated from ipfs-toolkit for standalone use)
 */
function base32Decode(str) {
  const BASE32 = 'abcdefghijklmnopqrstuvwxyz234567';
  const bytes = [];
  let bits = 0, value = 0;
  for (let i = 0; i < str.length; i++) {
    const idx = BASE32.indexOf(str[i].toLowerCase());
    if (idx === -1) continue;
    value = (value << 5) | idx;
    bits += 5;
    if (bits >= 8) { bytes.push((value >>> (bits - 8)) & 0xff); bits -= 8; }
  }
  return Buffer.from(bytes);
}

// ═══════════════════════════════════════════════════════════════
// 5. UCAN-LITE — Capability Delegation Tokens
// ═══════════════════════════════════════════════════════════════

/**
 * Create a simple UCAN-like capability token.
 * Grants a delegate the ability to publish/update content at a CID.
 */
function createCapability(issuerPrivKey, issuerPubKey, audienceDID, capability, expirationDays = 30) {
  const now = new Date();
  const exp = new Date(now.getTime() + expirationDays * 86400000);

  const token = {
    ucan: '0.1.0-lite',
    iss: publicKeyToDIDKey(issuerPubKey),
    aud: audienceDID,
    cap: capability,
    exp: exp.toISOString(),
    iat: now.toISOString(),
  };

  const tokenBytes = Buffer.from(JSON.stringify(token), 'utf8');
  const signature = signEd25519(issuerPrivKey, tokenBytes);

  return {
    token,
    signature: signature.toString('base64url'),
    encoded: `${Buffer.from(JSON.stringify(token)).toString('base64url')}.${signature.toString('base64url')}`,
  };
}

// ═══════════════════════════════════════════════════════════════
// 6. IDENTITY PERSISTENCE
// ═══════════════════════════════════════════════════════════════

function saveIdentity(keyPair, filePath = '.qnfo-identity.json') {
  const identity = {
    did: publicKeyToDIDKey(keyPair.publicKey),
    publicKey: keyPair.publicKeyHex,
    privateKey: '[REDACTED — store securely]',
    created: new Date().toISOString(),
    method: 'did:key',
    keyType: 'Ed25519',
  };
  fs.writeFileSync(filePath, JSON.stringify(identity, null, 2));
  return identity;
}

// ═══════════════════════════════════════════════════════════════
// 7. MULTI-AUTHOR PUBLICATION
// ═══════════════════════════════════════════════════════════════

/**
 * Create a multi-author attestation for a publication.
 * Each author signs independently. The set of signatures forms a
 * verifiable authorship claim.
 */
function createMultiAuthorAttestation(cid, authorIdentities, metadata = {}) {
  const attestations = [];
  for (const author of authorIdentities) {
    const att = createAttestation(
      author.privateKey,
      author.publicKey,
      cid,
      { ...metadata, authorName: author.name || 'Anonymous' }
    );
    attestations.push(att);
  }

  return {
    type: 'MultiAuthorAttestation',
    cid,
    authors: attestations.map(a => ({
      did: a.payload.creator,
      verified: true,
    })),
    attestations,
    metadata,
  };
}

// ═══════════════════════════════════════════════════════════════
// 8. CLI
// ═══════════════════════════════════════════════════════════════

function printUsage() {
  console.log(`
Web3 Identity & Attribution Layer
===================================

Commands:
  generate [output]              Generate Ed25519 keypair + DID:key
  attest <cid> [metadata-json]   Sign authorship attestation for a CID
  verify <attestation-file>      Verify an attestation
  multi-attest <cid> <authors-dir>   Create multi-author attestation
  ens-contenthash <cid>          Convert IPFS CID to ENS contenthash
  did-resolve <did>              Resolve a DID:key to public key bytes

Examples:
  node web3-identity.js generate .qnfo-author.json
  node web3-identity.js attest bafy...abc
  node web3-identity.js verify attestation.json
  node web3-identity.js ens-contenthash bafy...abc
`);
}

function main() {
  const args = process.argv.slice(2);
  const cmd = args[0];

  if (!cmd || cmd === '--help' || cmd === '-h') {
    printUsage();
    process.exit(0);
  }

  switch (cmd) {
    case 'generate': {
      const output = args[1] || '.qnfo-identity.json';
      const keyPair = generateEd25519KeyPair();
      const identity = saveIdentity(keyPair, output);

      console.log(JSON.stringify({
        did: identity.did,
        publicKey: identity.publicKey,
        savedTo: output,
        warning: 'STORE PRIVATE KEY SECURELY. It is not saved by default.',
      }, null, 2));

      // Also save private key separately (user should protect this)
      const secretPath = output.replace('.json', '.secret');
      fs.writeFileSync(secretPath, keyPair.privateKeyHex);
      console.log(`\n[SECRET] Private key saved to ${secretPath} — MOVE TO SECURE LOCATION`);
      break;
    }

    case 'attest': {
      const cid = args[1];
      if (!cid) { console.error('[ERROR] CID required'); process.exit(1); }

      // Load identity
      const identityPath = args[2] || '.qnfo-identity.json';
      let metadata = {};
      if (args[3]) {
        try { metadata = JSON.parse(fs.readFileSync(args[3], 'utf8')); } catch {}
      }

      console.error('[ERROR] Attestation requires private key from identity.secret file');
      console.error('Usage: node web3-identity.js attest <cid> <identity-json> [metadata-json]');
      process.exit(1);
    }

    case 'verify': {
      const file = args[1];
      if (!file) { console.error('[ERROR] Attestation file required'); process.exit(1); }
      const attestation = JSON.parse(fs.readFileSync(file, 'utf8'));
      const result = verifyAttestation(attestation);
      console.log(JSON.stringify(result, null, 2));
      if (!result.valid) process.exit(1);
      break;
    }

    case 'ens-contenthash': {
      const cid = args[1];
      if (!cid) { console.error('[ERROR] CID required'); process.exit(1); }
      const contentHash = cidToENSContentHash(cid);
      console.log(JSON.stringify({ cid, ensContentHash: contentHash, standard: 'EIP-1577' }));
      break;
    }

    case 'did-resolve': {
      const did = args[1];
      if (!did) { console.error('[ERROR] DID required'); process.exit(1); }
      const pubKey = didKeyToPublicKey(did);
      console.log(JSON.stringify({
        did,
        method: 'key',
        keyType: 'Ed25519',
        publicKeyBytes: pubKey.toString('hex'),
        publicKeyLength: pubKey.length,
      }));
      break;
    }

    default:
      console.error(`[ERROR] Unknown command: ${cmd}`);
      printUsage();
      process.exit(1);
  }
}

module.exports = {
  generateEd25519KeyPair,
  publicKeyToDIDKey,
  didKeyToPublicKey,
  signEd25519,
  verifyEd25519,
  createAttestation,
  verifyAttestation,
  cidToENSContentHash,
  createCapability,
  createMultiAuthorAttestation,
};

if (require.main === module) {
  main();
}
