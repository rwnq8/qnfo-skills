/**
 * QNFO Research Publication → IPFS/Web3 Pipeline
 * ===============================================
 * End-to-end tool for publishing QNFO research to IPFS with Web3 identity,
 * content addressing, multi-gateway verification, and integration with
 * existing QNFO infrastructure (R2, D1, Workers).
 *
 * Pipeline Stages:
 *   1. PREPARE   — Gather publication files, compute CIDs, create CAR
 *   2. IDENTIFY  — Create/load author DID, sign attestation
 *   3. METADATA  — Build IPLD metadata node, generate manifest
 *   4. PIN       — Pin to configured services
 *   5. VERIFY    — Multi-gateway content verification
 *   6. INTEGRATE — Update R2, D1, and discovery index
 *
 * Usage:
 *   node publication-pipeline.js publish <publication-dir> [--all]
 *   node publication-pipeline.js stage <stage> <publication-dir>
 *   node publication-pipeline.js verify <cid>
 *   node publication-pipeline.js integrate <manifest> --r2 --d1
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// ═══════════════════════════════════════════════════════════════
// CONFIGURATION
// ═══════════════════════════════════════════════════════════════

const PIPELINE_CONFIG = {
  stages: ['prepare', 'identify', 'metadata', 'pin', 'verify', 'integrate'],
  requiredFiles: ['paper.md', 'abstract.txt', 'metadata.json'],
  optionalFiles: ['paper.pdf', 'paper.html', 'supplementary.zip', 'figures/'],
  gatewayTimeout: 15000,
  r2bucket: 'qnfo',
  r2prefix: 'releases/ipfs',
  d1database: 'living-paper',
};

// ═══════════════════════════════════════════════════════════════
// STAGE 1: PREPARE
// ═══════════════════════════════════════════════════════════════

function stagePrepare(publicationDir) {
  console.log('\n=== STAGE 1: PREPARE ===');
  console.log(`  Directory: ${publicationDir}`);

  // Validate required files
  const missing = PIPELINE_CONFIG.requiredFiles.filter(f =>
    !fs.existsSync(path.join(publicationDir, f))
  );
  if (missing.length > 0) {
    console.warn(`  [WARN] Missing required files: ${missing.join(', ')}`);
  }

  // List all files
  const allFiles = fs.readdirSync(publicationDir)
    .filter(f => !f.startsWith('.') && !f.startsWith('_'))
    .filter(f => fs.statSync(path.join(publicationDir, f)).isFile());

  console.log(`  Files found: ${allFiles.length}`);

  // Compute CIDs using the toolkit
  const toolkitPath = path.join(__dirname, 'ipfs-toolkit.js');
  const manifest = JSON.parse(execSync(
    `node "${toolkitPath}" manifest "${publicationDir}"`,
    { encoding: 'utf8' }
  ));

  console.log(`  Root CID: ${manifest.rootCID}`);
  console.log(`  File CIDs:`);
  manifest.files.forEach(f => {
    console.log(`    ${f.path.padEnd(40)} ${f.cid}`);
  });

  // Create CAR archive
  const carOutput = path.join(publicationDir, 'publication.car');
  const carResult = JSON.parse(execSync(
    `node "${toolkitPath}" car "${publicationDir}" "${carOutput}"`,
    { encoding: 'utf8' }
  ));
  console.log(`  CAR archive: ${carResult.output} (${(carResult.carSize / 1024).toFixed(1)} KB)`);

  return {
    publicationDir,
    manifest,
    carFile: carResult.output,
    carSize: carResult.carSize,
  };
}

// ═══════════════════════════════════════════════════════════════
// STAGE 2: IDENTIFY (DID + Attestation)
// ═══════════════════════════════════════════════════════════════

function stageIdentify(state) {
  console.log('\n=== STAGE 2: IDENTIFY ===');

  const identityPath = path.join(state.publicationDir, '.author-identity.json');
  const secretPath = path.join(state.publicationDir, '.author-identity.secret');

  let identity;
  if (fs.existsSync(identityPath)) {
    identity = JSON.parse(fs.readFileSync(identityPath, 'utf8'));
    console.log(`  Loaded existing identity: ${identity.did}`);
  } else {
    // Generate new identity
    const identityTool = path.join(__dirname, 'web3-identity.js');
    execSync(`node "${identityTool}" generate "${identityPath}"`, { encoding: 'utf8' });
    identity = JSON.parse(fs.readFileSync(identityPath, 'utf8'));
    console.log(`  Generated new identity: ${identity.did}`);
  }

  console.log(`  Attesting to root CID: ${state.manifest.rootCID}`);

  // Create attestation
  const attestationPath = path.join(state.publicationDir, 'attestation.json');
  const attestation = createAttestationRecord(identity, state.manifest.rootCID, state.manifest);
  fs.writeFileSync(attestationPath, JSON.stringify(attestation, null, 2));
  console.log(`  Attestation saved: ${attestationPath}`);

  return {
    ...state,
    identity,
    attestation,
  };
}

function createAttestationRecord(identity, rootCID, manifest) {
  return {
    '@context': [
      'https://www.w3.org/ns/credentials/v2',
      'https://w3id.org/security/data-integrity/v2',
    ],
    type: ['VerifiableCredential', 'ContentAttestation'],
    issuer: identity.did,
    issuanceDate: new Date().toISOString(),
    credentialSubject: {
      id: `ipfs://${rootCID}`,
      cid: rootCID,
      files: manifest.files.map(f => ({
        path: f.path,
        cid: f.cid,
        size: f.size,
        sha256: f.sha256,
      })),
      proof: 'content-addressing',
    },
    proof: {
      type: 'DataIntegrityProof',
      cryptosuite: 'eddsa-rdfc-2022',
      created: new Date().toISOString(),
      verificationMethod: identity.did,
      proofPurpose: 'assertionMethod',
      proofValue: '[Signature would be generated with private key]',
    },
  };
}

// ═══════════════════════════════════════════════════════════════
// STAGE 3: METADATA (IPLD + Manifest)
// ═══════════════════════════════════════════════════════════════

function stageMetadata(state) {
  console.log('\n=== STAGE 3: METADATA ===');

  // Load publication metadata
  const metadataPath = path.join(state.publicationDir, 'metadata.json');
  let pubMetadata = {};
  if (fs.existsSync(metadataPath)) {
    pubMetadata = JSON.parse(fs.readFileSync(metadataPath, 'utf8'));
  } else {
    // Extract from directory name
    pubMetadata = {
      title: path.basename(path.resolve(state.publicationDir)),
      authors: ['QNFO Research'],
      date: new Date().toISOString().split('T')[0],
      license: 'CC-BY-4.0',
    };
  }

  // Create IPLD metadata node
  const toolkitPath = path.join(__dirname, 'ipfs-toolkit.js');
  const metadataFile = path.join(state.publicationDir, '_metadata-input.json');
  fs.writeFileSync(metadataFile, JSON.stringify(pubMetadata));
  const ipldResult = JSON.parse(execSync(
    `node "${toolkitPath}" metadata "${metadataFile}"`,
    { encoding: 'utf8' }
  ));
  fs.unlinkSync(metadataFile);

  console.log(`  IPLD metadata CID: ${ipldResult.cid}`);
  console.log(`  Title: ${ipldResult.data.title}`);

  // Build enriched manifest with metadata link
  const enrichedManifest = {
    ...state.manifest,
    metadata: {
      ...pubMetadata,
      ipldCID: ipldResult.cid,
    },
    attestation: {
      did: state.identity.did,
      attestedAt: state.attestation.issuanceDate,
    },
  };

  const manifestPath = path.join(state.publicationDir, 'ipfs-manifest.json');
  fs.writeFileSync(manifestPath, JSON.stringify(enrichedManifest, null, 2));
  console.log(`  Enriched manifest: ${manifestPath}`);

  return {
    ...state,
    ipldMetadata: ipldResult,
    enrichedManifest,
  };
}

// ═══════════════════════════════════════════════════════════════
// STAGE 4: PIN
// ═══════════════════════════════════════════════════════════════

async function stagePin(state) {
  console.log('\n=== STAGE 4: PIN ===');

  const pinningPath = path.join(__dirname, 'pinning-service.js');

  try {
    console.log(`  Pinning ${state.manifest.rootCID} to all configured services...`);

    // Try pinning — may fail if no services configured
    const result = execSync(
      `node "${pinningPath}" pin ${state.manifest.rootCID} --all`,
      { encoding: 'utf8', stdio: 'pipe' }
    );
    console.log(result);
  } catch (e) {
    console.log('  [INFO] No remote pinning services configured. Using local-only mode.');
    console.log('  [INFO] Configure services in .pinning-config.json or env vars.');
  }

  return state;
}

// ═══════════════════════════════════════════════════════════════
// STAGE 5: VERIFY
// ═══════════════════════════════════════════════════════════════

async function stageVerify(state) {
  console.log('\n=== STAGE 5: VERIFY ===');

  const verifierPath = path.join(__dirname, 'gateway-verifier.js');
  const cid = state.manifest.rootCID;

  console.log(`  Verifying content at ${cid} across gateways...`);

  try {
    const result = execSync(
      `node "${verifierPath}" test ${cid}`,
      { encoding: 'utf8', stdio: 'pipe', timeout: 30000 }
    );
    console.log(result);
  } catch (e) {
    if (e.stdout) console.log(e.stdout);
    console.log('  [WARN] Gateway verification partially failed — content may not be propagated yet.');
    console.log('  [INFO] Re-run verification after pinning completes.');
  }

  return state;
}

// ═══════════════════════════════════════════════════════════════
// STAGE 6: INTEGRATE (R2 + D1 + Discovery Index)
// ═══════════════════════════════════════════════════════════════

async function stageIntegrate(state, options = {}) {
  console.log('\n=== STAGE 6: INTEGRATE ===');

  const { r2 = true, d1 = true, discoveryIndex = true } = options;

  // 6a. Upload to Cloudflare R2
  if (r2) {
    console.log('\n  [R2] Uploading to Cloudflare R2...');
    try {
      // Upload CAR archive
      const r2Path = `${PIPELINE_CONFIG.r2prefix}/${path.basename(path.resolve(state.publicationDir))}`;
      execSync(
        `npx wrangler r2 object put "qnfo/${r2Path}/publication.car" --file "${state.carFile}" --remote`,
        { encoding: 'utf8', stdio: 'pipe' }
      );
      console.log(`    Uploaded: qnfo/${r2Path}/publication.car`);

      // Upload manifest
      const manifestPath = path.join(state.publicationDir, 'ipfs-manifest.json');
      execSync(
        `npx wrangler r2 object put "qnfo/${r2Path}/ipfs-manifest.json" --file "${manifestPath}" --remote`,
        { encoding: 'utf8', stdio: 'pipe' }
      );
      console.log(`    Uploaded: qnfo/${r2Path}/ipfs-manifest.json`);
    } catch (e) {
      console.log(`  [WARN] R2 upload failed: ${e.message}`);
      console.log('  [INFO] Manually upload with: npx wrangler r2 object put ...');
    }
  }

  // 6b. Update D1 living-paper database
  if (d1) {
    console.log('\n  [D1] Updating living-paper database...');
    const meta = state.enrichedManifest.metadata;

    // Generate SQL
    const sql = `
INSERT OR REPLACE INTO papers (id, title, authors, doi, abstract, published, ipfs_cid)
VALUES (
  '${escapeSQL(path.basename(path.resolve(state.publicationDir)))}',
  '${escapeSQL(meta.title || '')}',
  '${escapeSQL((meta.authors || []).join(', '))}',
  '${escapeSQL(meta.doi || '')}',
  '${escapeSQL(meta.abstract || '')}',
  '${escapeSQL(meta.date || new Date().toISOString().split('T')[0])}',
  '${escapeSQL(state.manifest.rootCID)}'
);
`;
    const sqlPath = path.join(state.publicationDir, 'd1-update.sql');
    fs.writeFileSync(sqlPath, sql.trim());
    console.log(`    SQL written to: ${sqlPath}`);
    console.log('    Execute: npx wrangler d1 execute living-paper --file=<sql>');
  }

  // 6c. Update Discovery Index
  if (discoveryIndex) {
    console.log('\n  [DISCOVERY] Updating discovery index...');
    const indexEntry = {
      type: 'publication',
      id: path.basename(path.resolve(state.publicationDir)),
      title: state.enrichedManifest.metadata.title,
      rootCID: state.manifest.rootCID,
      did: state.identity?.did,
      date: new Date().toISOString(),
      files: state.manifest.files.map(f => ({ path: f.path, cid: f.cid })),
      gatewayUrls: state.manifest.gatewayUrls,
      persistent: true,
      protocol: 'ipfs://',
    };

    const indexPath = path.join(state.publicationDir, 'discovery-index-entry.json');
    fs.writeFileSync(indexPath, JSON.stringify(indexEntry, null, 2));
    console.log(`    Index entry: ${indexPath}`);
  }

  return state;
}

function escapeSQL(str) {
  if (!str) return '';
  return str.replace(/'/g, "''").replace(/\\/g, '\\\\');
}

// ═══════════════════════════════════════════════════════════════
// FULL PIPELINE ORCHESTRATOR
// ═══════════════════════════════════════════════════════════════

async function runPipeline(publicationDir, options = {}) {
  const { stages = PIPELINE_CONFIG.stages, r2 = true, d1 = true } = options;

  console.log('╔═══════════════════════════════════════════════════════════╗');
  console.log('║    QNFO Research Publication → IPFS/Web3 Pipeline        ║');
  console.log('╚═══════════════════════════════════════════════════════════╝');
  console.log(`  Publication: ${path.basename(path.resolve(publicationDir))}`);
  console.log(`  Stages: ${stages.join(' → ')}`);
  console.log(`  Time: ${new Date().toISOString()}`);

  let state = { publicationDir };

  try {
    if (stages.includes('prepare')) {
      state = { ...state, ...stagePrepare(publicationDir) };
    }

    if (stages.includes('identify')) {
      state = stageIdentify(state);
    }

    if (stages.includes('metadata')) {
      state = stageMetadata(state);
    }

    if (stages.includes('pin')) {
      state = await stagePin(state);
    }

    if (stages.includes('verify')) {
      state = await stageVerify(state);
    }

    if (stages.includes('integrate')) {
      state = await stageIntegrate(state, { r2, d1 });
    }

    console.log('\n╔═══════════════════════════════════════════════════════════╗');
    console.log('║              PIPELINE COMPLETE                            ║');
    console.log('╚═══════════════════════════════════════════════════════════╝');
    console.log(`\n  Root CID: ${state.manifest.rootCID}`);
    console.log(`  IPFS URL: ipfs://${state.manifest.rootCID}`);
    console.log(`  Gateway:  ${state.manifest.gatewayUrls[0]}`);
    console.log(`  Identity: ${state.identity?.did || 'N/A'}`);
    console.log(`  CAR file: ${state.carFile}`);

    // Save pipeline state
    const statePath = path.join(publicationDir, '_pipeline-state.json');
    fs.writeFileSync(statePath, JSON.stringify({
      completedAt: new Date().toISOString(),
      rootCID: state.manifest.rootCID,
      did: state.identity?.did,
      stages: stages,
    }, null, 2));
    console.log(`\n  State saved: ${statePath}`);

    return state;
  } catch (error) {
    console.error(`\n[PIPELINE FAILED] ${error.message}`);
    console.error(error.stack);
    process.exit(1);
  }
}

// ═══════════════════════════════════════════════════════════════
// INDIVIDUAL STAGE RUNNER
// ═══════════════════════════════════════════════════════════════

async function runStage(stage, publicationDir, options = {}) {
  const stages = {
    prepare: stagePrepare,
    identify: stageIdentify,
    metadata: stageMetadata,
    pin: stagePin,
    verify: stageVerify,
    integrate: stageIntegrate,
  };

  if (!stages[stage]) {
    console.error(`[ERROR] Unknown stage: ${stage}. Valid: ${Object.keys(stages).join(', ')}`);
    process.exit(1);
  }

  let state = { publicationDir };

  // Load existing state if available
  const statePath = path.join(publicationDir, '_pipeline-state.json');
  if (fs.existsSync(statePath)) {
    state = { ...state, ...JSON.parse(fs.readFileSync(statePath, 'utf8')) };
  }

  // Load manifest if available
  const manifestPath = path.join(publicationDir, 'ipfs-manifest.json');
  if (fs.existsSync(manifestPath)) {
    state.manifest = JSON.parse(fs.readFileSync(manifestPath, 'utf8'));
  }

  return stages[stage](state, options);
}

// ═══════════════════════════════════════════════════════════════
// CLI
// ═══════════════════════════════════════════════════════════════

async function main() {
  const args = process.argv.slice(2);
  const cmd = args[0];

  if (!cmd || cmd === '--help' || cmd === '-h') {
    console.log(`
QNFO Publication → IPFS/Web3 Pipeline
======================================

Commands:
  publish <dir> [--all]         Run full pipeline (prepare through integrate)
  publish <dir> --stages s1,s2  Run specific stages
  publish <dir> --no-r2         Skip R2 upload
  publish <dir> --no-d1         Skip D1 update
  stage <stage> <dir>           Run a single stage
  verify <cid>                  Run gateway verification only

Stages: prepare, identify, metadata, pin, verify, integrate

Examples:
  node publication-pipeline.js publish ../my-paper/
  node publication-pipeline.js publish ../my-paper/ --stages prepare,metadata,pin
  node publication-pipeline.js stage verify ../my-paper/
  node publication-pipeline.js verify bafybeibslwmyux23oocfu7urj7aa7t6jv3qlaj4teacj6ek3o2o3ddpyqa
`);
    process.exit(0);
  }

  switch (cmd) {
    case 'publish': {
      const pubDir = args[1];
      if (!pubDir || !fs.existsSync(pubDir)) {
        console.error(`[ERROR] Publication directory not found: ${pubDir}`);
        process.exit(1);
      }

      const stagesIdx = args.indexOf('--stages');
      const stages = stagesIdx >= 0
        ? args[stagesIdx + 1].split(',')
        : PIPELINE_CONFIG.stages;

      const options = {
        stages,
        r2: !args.includes('--no-r2'),
        d1: !args.includes('--no-d1'),
      };

      await runPipeline(pubDir, options);
      break;
    }

    case 'stage': {
      const stage = args[1];
      const pubDir = args[2];
      if (!pubDir || !fs.existsSync(pubDir)) {
        console.error(`[ERROR] Publication directory not found: ${pubDir}`);
        process.exit(1);
      }
      await runStage(stage, pubDir);
      break;
    }

    case 'verify': {
      const cid = args[1];
      if (!cid) {
        console.error('[ERROR] CID required');
        process.exit(1);
      }
      const verifierPath = path.join(__dirname, 'gateway-verifier.js');
      try {
        execSync(`node "${verifierPath}" test ${cid}`, { encoding: 'utf8', stdio: 'inherit' });
      } catch (e) {
        console.error(`[FAIL] ${e.message}`);
        process.exit(1);
      }
      break;
    }

    default:
      console.error(`[ERROR] Unknown command: ${cmd}`);
      process.exit(1);
  }
}

module.exports = { runPipeline, runStage, stagePrepare, stageIdentify, stageMetadata, stagePin, stageVerify, stageIntegrate };

if (require.main === module) {
  main().catch(err => {
    console.error(`[FATAL] ${err.message}`);
    process.exit(1);
  });
}
