/**
 * IPFS Toolkit — Pure Node.js (Zero External Dependencies)
 * =========================================================
 * Computes CIDs, builds DAGs, creates CAR archives, and verifies content
 * addressing — all without any npm packages. Designed for QNFO research
 * publication pipeline POC.
 *
 * Standards implemented:
 *   - CIDv1 (multicodec: raw=0x55, dag-pb=0x70, dag-json=0x0129)
 *   - Multihash (sha2-256=0x12, blake3=0x1e)
 *   - Multibase (base32 lowercase, base58btc)
 *   - CARv1 archive format
 *   - DAG-PB (UnixFS directory nodes)
 *   - DAG-JSON (structured metadata)
 *   - IPLD (InterPlanetary Linked Data)
 *
 * Usage:
 *   node ipfs-toolkit.js compute <file>           — Compute CID
 *   node ipfs-toolkit.js dag <directory>          — Build DAG + root CID
 *   node ipfs-toolkit.js car <directory>          — Create CAR archive
 *   node ipfs-toolkit.js verify <cid> <file>      — Verify content matches CID
 *   node ipfs-toolkit.js manifest <directory>     — Generate full manifest
 */

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

// ═══════════════════════════════════════════════════════════════
// 1. MULTIBASE — Base32 (RFC 4648 lowercase)
// ═══════════════════════════════════════════════════════════════

const BASE32 = 'abcdefghijklmnopqrstuvwxyz234567';

function base32Encode(buf) {
  let bits = 0, value = 0, out = '';
  for (let i = 0; i < buf.length; i++) {
    value = (value << 8) | buf[i];
    bits += 8;
    while (bits >= 5) {
      out += BASE32[(value >>> (bits - 5)) & 31];
      bits -= 5;
    }
  }
  if (bits > 0) out += BASE32[(value << (5 - bits)) & 31];
  return out;
}

function base32Decode(str) {
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

// Base58btc for legacy CIDv0
const BASE58 = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz';

function base58Encode(buf) {
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
  for (let i = digits.length - 1; i >= 0; i--) out += BASE58[digits[i]];
  return out;
}

// ═══════════════════════════════════════════════════════════════
// 2. MULTIHASH — sha2-256 (0x12), blake3 (0x1e placeholder)
// ═══════════════════════════════════════════════════════════════

function multihashSHA256(data) {
  const hash = crypto.createHash('sha256').update(data).digest();
  return Buffer.concat([Buffer.from([0x12, 0x20]), hash]);
}

function multihashSHA256Hex(data) {
  return crypto.createHash('sha256').update(data).digest('hex');
}

function multihashBLAKE3(data) {
  // BLAKE3 support via Node's crypto if available (Node 20.12+)
  // fallback: SHA-512 truncated for demonstration
  try {
    const hash = crypto.createHash('blake3').update(data).digest();
    return Buffer.concat([Buffer.from([0x1e, 0x20]), hash.slice(0, 32)]);
  } catch {
    const hash = crypto.createHash('sha512').update(data).digest().subarray(0, 32);
    console.warn('[WARN] BLAKE3 not available, using SHA-512 truncated (non-standard)');
    return Buffer.concat([Buffer.from([0x1e, 0x20]), hash]);
  }
}

// ═══════════════════════════════════════════════════════════════
// 3. CID COMPUTATION
// ═══════════════════════════════════════════════════════════════

// Multicodec codes
const RAW = 0x55;        // raw binary
const DAG_PB = 0x70;     // protobuf (UnixFS)
const DAG_JSON = 0x0129;  // dag-json
const DAG_CBOR = 0x71;   // dag-cbor

/**
 * Compute CIDv1 for raw content (single file).
 * Format: <cid-version><multicodec><multihash>
 */
function computeCIDv1(data, multicodec = RAW) {
  const mh = multihashSHA256(data);
  const prefix = [0x01]; // CIDv1
  // Encode multicodec as varint
  if (multicodec < 0x80) {
    prefix.push(multicodec);
  } else {
    prefix.push((multicodec & 0x7f) | 0x80);
    prefix.push(multicodec >>> 7);
  }
  const cidBytes = Buffer.concat([Buffer.from(prefix), mh]);
  return 'b' + base32Encode(cidBytes);
}

/**
 * Compute CIDv0 (legacy, base58btc) for backward compatibility.
 */
function computeCIDv0(data) {
  const mh = multihashSHA256(data);
  // CIDv0: <cid-version=0x12><multicodec=dag-pb=0x20><multihash>
  const cidBytes = Buffer.concat([
    Buffer.from([0x12, 0x20]),
    mh.subarray(2) // skip multihash prefix
  ]);
  return base58Encode(cidBytes);
}

// ═══════════════════════════════════════════════════════════════
// 4. VARINT ENCODING (for protobuf fields)
// ═══════════════════════════════════════════════════════════════

function encodeVarint(num) {
  const bytes = [];
  while (num > 0x7f) {
    bytes.push((num & 0x7f) | 0x80);
    num >>>= 7;
  }
  bytes.push(num & 0x7f);
  return Buffer.from(bytes);
}

// ═══════════════════════════════════════════════════════════════
// 5. DAG-PB — Directory Nodes (UnixFS)
// ═══════════════════════════════════════════════════════════════

/**
 * Encode a single PBLink for DAG-PB.
 * PBLink { Hash, Name, Tsize }
 *   field 1: Hash (bytes)
 *   field 2: Name (string)
 *   field 3: Tsize (varint)
 */
function encodeDAGPBLink(name, cidStr, cumulativeSize) {
  const cidBytes = base32Decode(cidStr.slice(1));
  const nameBytes = Buffer.from(name, 'utf8');
  const pieces = [];

  // Hash (field 1)
  const hash = Buffer.concat([Buffer.from([0x0a]), encodeVarint(cidBytes.length), cidBytes]);
  pieces.push(hash);

  // Name (field 2)
  const nameField = Buffer.concat([Buffer.from([0x12]), encodeVarint(nameBytes.length), nameBytes]);
  pieces.push(nameField);

  // Tsize (field 3)
  const tsize = Buffer.concat([Buffer.from([0x18]), encodeVarint(cumulativeSize)]);
  pieces.push(tsize);

  return Buffer.concat(pieces);
}

/**
 * Build a DAG-PB directory node from links.
 * PBNode { Links (repeated PBLink), Data (bytes) }
 */
function encodeDAGPBNode(links) {
  // Sort links alphabetically by name (deterministic ordering)
  const sorted = [...links].sort((a, b) => a.name.localeCompare(b.name));

  const linkFields = [];
  for (const link of sorted) {
    const lb = encodeDAGPBLink(link.name, link.cid, link.size);
    linkFields.push(Buffer.concat([Buffer.from([0x12]), encodeVarint(lb.length), lb]));
  }

  // PBNode: Data = empty bytes (field 1), Links (field 2)
  const data = Buffer.from([0x0a, 0x00]); // empty Data field
  return Buffer.concat([data, ...linkFields]);
}

/**
 * Compute root CID for a directory.
 */
function computeDirCID(links) {
  const dagBytes = encodeDAGPBNode(links);
  return computeCIDv1(dagBytes, DAG_PB);
}

// ═══════════════════════════════════════════════════════════════
// 6. DAG-JSON — Structured Metadata
// ═══════════════════════════════════════════════════════════════

/**
 * Encode a value as a DAG-JSON-compatible CID link.
 * Format: { "/": "bafy..." }
 */
function dagJSONLink(cid) {
  return { '/': cid };
}

/**
 * Create a DAG-JSON metadata node (self-describing).
 */
function createDAGJSON(data) {
  const jsonBytes = Buffer.from(JSON.stringify(data), 'utf8');
  const cid = computeCIDv1(jsonBytes, DAG_JSON);
  return { cid, data, bytes: jsonBytes };
}

// ═══════════════════════════════════════════════════════════════
// 7. CARv1 ARCHIVE FORMAT
// ═══════════════════════════════════════════════════════════════

/**
 * Create a CARv1 archive header.
 * CARv1 format: <header><block><block>...
 * Header is a DAG-CBOR encoded { version: 1, roots: [CID] }
 */
function createCARHeader(rootCID) {
  const rootBytes = base32Decode(rootCID.slice(1));
  const rootsField = Buffer.concat([
    Buffer.from([0x81]), // array of 1 element
    Buffer.from([0xd8, 0x2a]), // tag 42 (CID)
    Buffer.from([0x58]), rootBytes.length < 256 ?
      Buffer.from([rootBytes.length]) :
      Buffer.concat([Buffer.from([0x19]), encodeVarint(rootBytes.length)]),
    rootBytes
  ]);
  const header = Buffer.concat([
    Buffer.from([0xa2]), // map of 2 pairs
    Buffer.from([0x67, 0x76, 0x65, 0x72, 0x73, 0x69, 0x6f, 0x6e]), // "version"
    Buffer.from([0x01]), // 1
    Buffer.from([0x65, 0x72, 0x6f, 0x6f, 0x74, 0x73]), // "roots"
    rootsField
  ]);
  return header;
}

/**
 * Encode a CARv1 block (CID + data).
 */
function encodeCARBlock(cid, data) {
  const cidBytes = base32Decode(cid.slice(1));
  const cidField = Buffer.concat([
    Buffer.from([0xd8, 0x2a]), // tag 42 (CID)
    Buffer.from([0x58]), cidBytes.length < 256 ?
      Buffer.from([cidBytes.length]) :
      Buffer.concat([Buffer.from([0x19]), encodeVarint(cidBytes.length)]),
    cidBytes
  ]);
  return Buffer.concat([cidField, data]);
}

/**
 * Create a complete CARv1 archive from files.
 */
function createCARv1(files, rootCID) {
  const header = createCARHeader(rootCID);
  const blocks = [];

  for (const file of files) {
    const block = encodeCARBlock(file.cid, file.data);
    blocks.push(block);
  }

  // Also add the root DAG node
  if (files.length > 1) {
    const rootLinks = files.map(f => ({ name: f.name, cid: f.cid, size: f.data.length }));
    const rootDAGData = encodeDAGPBNode(rootLinks);
    const rootDAGBlock = encodeCARBlock(rootCID, rootDAGData);
    blocks.push(rootDAGBlock);
  }

  const headerLen = encodeVarint(header.length);
  const carBuffer = Buffer.concat([headerLen, header, ...blocks]);
  return carBuffer;
}

// ═══════════════════════════════════════════════════════════════
// 8. IPLD — Linked Data Nodes
// ═══════════════════════════════════════════════════════════════

/**
 * Create an IPLD Collection node (array of links to child nodes).
 * Useful for: paper series, multi-part publications, datasets.
 */
function createIPLDCollection(items) {
  const collection = items.map((item, i) => ({
    index: i,
    ...item
  }));
  return createDAGJSON(collection);
}

/**
 * Create an IPLD Metadata node for a QNFO publication.
 */
function createPublicationMetadata({ title, authors, doi, abstract, date, license, keywords, version }) {
  const meta = {
    '@type': 'scholarly:Publication',
    title,
    authors: authors.map(a => ({ '@type': 'Person', name: a })),
    doi,
    abstract,
    datePublished: date,
    license: license || 'CC-BY-4.0',
    keywords: keywords || [],
    version: version || '1.0.0',
    publisher: 'QNFO Research',
    contentAddressed: true,
    protocol: 'ipfs://',
  };
  return createDAGJSON(meta);
}

// ═══════════════════════════════════════════════════════════════
// 9. CONTENT VERIFICATION
// ═══════════════════════════════════════════════════════════════

/**
 * Verify that file content matches a given CID.
 */
function verifyCID(cid, data) {
  const computedCID = computeCIDv1(data);
  return {
    match: computedCID === cid,
    expected: cid,
    computed: computedCID,
    multihash: multihashSHA256Hex(data),
  };
}

// ═══════════════════════════════════════════════════════════════
// 10. DISCOVERY MANIFEST
// ═══════════════════════════════════════════════════════════════

/**
 * Generate a complete discovery manifest for a publication directory.
 */
function generateManifest(dirPath, { name, description, version, license } = {}) {
  const files = fs.readdirSync(dirPath).filter(f =>
    !f.startsWith('.') && !f.startsWith('_') && fs.statSync(path.join(dirPath, f)).isFile()
  );

  const fileResults = [];
  const allFiles = [];

  for (const file of files.sort()) {
    const filePath = path.join(dirPath, file);
    const data = fs.readFileSync(filePath);
    const cid = computeCIDv1(data);
    const sha256 = multihashSHA256Hex(data);

    fileResults.push({
      path: file,
      cid,
      size: data.length,
      sha256,
      mimetype: guessMimeType(file),
    });

    allFiles.push({ name: file, cid, data });
  }

  const rootCID = allFiles.length === 1
    ? allFiles[0].cid
    : computeDirCID(allFiles.map(f => ({ name: f.name, cid: f.cid, size: f.data.length })));

  const metadata = createPublicationMetadata({
    title: name || path.basename(dirPath),
    authors: ['QNFO Research'],
    abstract: description || '',
    date: new Date().toISOString().split('T')[0],
    license: license || 'CC-BY-4.0',
    keywords: ['qnfo', 'research', 'ipfs', 'content-addressed'],
    version: version || '1.0.0',
  });

  const gatewayUrls = [
    `https://ipfs.io/ipfs/${rootCID}`,
    `https://cloudflare-ipfs.com/ipfs/${rootCID}`,
    `https://dweb.link/ipfs/${rootCID}`,
    `https://gateway.pinata.cloud/ipfs/${rootCID}`,
    `https://${rootCID}.ipfs.dweb.link`,
    `ipfs://${rootCID}`,
  ];

  const manifest = {
    manifest: 'qnfo-ipfs-manifest/1.0',
    generated: new Date().toISOString(),
    publication: metadata.data,
    publicationCID: metadata.cid,
    rootCID,
    files: fileResults,
    gatewayUrls,
    stats: {
      totalFiles: fileResults.length,
      totalBytes: fileResults.reduce((sum, f) => sum + f.size, 0),
      avgFileSize: Math.round(fileResults.reduce((sum, f) => sum + f.size, 0) / fileResults.length),
    },
    verification: {
      method: 'CIDv1 + sha2-256',
      reproducible: true,
      tool: 'ipfs-toolkit.js (pure Node.js, zero deps)',
    },
  };

  return manifest;
}

function guessMimeType(filename) {
  const ext = path.extname(filename).toLowerCase();
  const map = {
    '.md': 'text/markdown',
    '.txt': 'text/plain',
    '.html': 'text/html',
    '.json': 'application/json',
    '.pdf': 'application/pdf',
    '.png': 'image/png',
    '.jpg': 'image/jpeg',
    '.svg': 'image/svg+xml',
    '.csv': 'text/csv',
    '.bib': 'application/x-bibtex',
    '.tex': 'application/x-latex',
    '.ipynb': 'application/x-ipynb+json',
    '.py': 'text/x-python',
    '.js': 'text/javascript',
  };
  return map[ext] || 'application/octet-stream';
}

// ═══════════════════════════════════════════════════════════════
// 11. CLI INTERFACE
// ═══════════════════════════════════════════════════════════════

function printUsage() {
  console.log(`
IPFS Toolkit — Pure Node.js CID/DAG/CAR/Verification
=====================================================

Commands:
  compute <file>              Compute CIDv1 for a single file
  compute --cidv0 <file>      Compute legacy CIDv0 (base58btc)
  dag <directory>             Build DAG + compute root CID for directory
  car <directory> [output]    Create CARv1 archive
  verify <cid> <file>         Verify file content matches CID
  manifest <directory>        Generate full discovery manifest
  metadata <json-file>        Create IPLD metadata node

Examples:
  node ipfs-toolkit.js compute paper.pdf
  node ipfs-toolkit.js dag ./publication/
  node ipfs-toolkit.js car ./publication/ publication.car
  node ipfs-toolkit.js verify bafy...abc paper.pdf
  node ipfs-toolkit.js manifest ./publication/
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
    case 'compute': {
      if (args[1] === '--cidv0') {
        const file = args[2];
        if (!file) { console.error('[ERROR] File required'); process.exit(1); }
        const data = fs.readFileSync(file);
        const cid = computeCIDv0(data);
        console.log(JSON.stringify({ file, cid, cidVersion: 0, size: data.length }));
        break;
      }
      const file = args[1];
      if (!file) { console.error('[ERROR] File required'); process.exit(1); }
      const data = fs.readFileSync(file);
      const cid = computeCIDv1(data);
      const sha256 = multihashSHA256Hex(data);
      console.log(JSON.stringify({ file, cid, cidVersion: 1, size: data.length, sha256 }));
      break;
    }

    case 'dag': {
      const dir = args[1] || '.';
      const manifest = generateManifest(dir);
      console.log(JSON.stringify({
        rootCID: manifest.rootCID,
        files: manifest.files.map(f => ({ path: f.path, cid: f.cid, size: f.size })),
      }, null, 2));
      break;
    }

    case 'car': {
      const dir = args[1] || '.';
      const output = args[2] || `${path.basename(path.resolve(dir))}.car`;
      const manifest = generateManifest(dir);

      const allFiles = manifest.files.map(f => ({
        name: f.path,
        cid: f.cid,
        data: fs.readFileSync(path.join(dir, f.path)),
      }));

      const carBuffer = createCARv1(allFiles, manifest.rootCID);
      fs.writeFileSync(output, carBuffer);
      console.log(JSON.stringify({
        output,
        rootCID: manifest.rootCID,
        carSize: carBuffer.length,
        blocks: allFiles.length + (allFiles.length > 1 ? 1 : 0),
      }, null, 2));
      break;
    }

    case 'verify': {
      const cid = args[1];
      const file = args[2];
      if (!cid || !file) { console.error('[ERROR] CID and file required'); process.exit(1); }
      const data = fs.readFileSync(file);
      const result = verifyCID(cid, data);
      console.log(JSON.stringify(result, null, 2));
      if (!result.match) process.exit(1);
      break;
    }

    case 'manifest': {
      const dir = args[1] || '.';
      const name = args[2] || path.basename(path.resolve(dir));
      const manifest = generateManifest(dir, { name });
      console.log(JSON.stringify(manifest, null, 2));
      const outPath = path.join(dir, 'ipfs-manifest.json');
      fs.writeFileSync(outPath, JSON.stringify(manifest, null, 2));
      console.log(`\n[SAVED] ${outPath}`);
      break;
    }

    case 'metadata': {
      const file = args[1];
      if (!file) { console.error('[ERROR] JSON metadata file required'); process.exit(1); }
      const meta = JSON.parse(fs.readFileSync(file, 'utf8'));
      const result = createPublicationMetadata(meta);
      console.log(JSON.stringify({
        cid: result.cid,
        size: result.bytes.length,
        data: result.data,
      }, null, 2));
      break;
    }

    default:
      console.error(`[ERROR] Unknown command: ${cmd}`);
      printUsage();
      process.exit(1);
  }
}

// ═══════════════════════════════════════════════════════════════
// EXPORTS (for programmatic use)
// ═══════════════════════════════════════════════════════════════

module.exports = {
  computeCIDv1,
  computeCIDv0,
  computeDirCID,
  createCARv1,
  createDAGJSON,
  createIPLDCollection,
  createPublicationMetadata,
  generateManifest,
  verifyCID,
  multihashSHA256Hex,
  base32Encode,
  base32Decode,
};

// Run if invoked directly
if (require.main === module) {
  main();
}
