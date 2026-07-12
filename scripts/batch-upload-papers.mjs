#!/usr/bin/env node
/**
 * Batch Upload Papers to R2
 * 
 * Reads paper-export.json (from `wrangler d1 execute`),
 * generates paper.md files, and uploads them to R2 at the 
 * paths the papers-server Worker expects.
 * 
 * Usage: node scripts/batch-upload-papers.mjs [--dry-run] [--limit N] [--offset N]
 */

import { readFileSync, writeFileSync, mkdirSync, existsSync } from 'fs';
import { execSync } from 'child_process';
import { resolve, join } from 'path';
import { fileURLToPath } from 'url';

const __dirname = fileURLToPath(new URL('.', import.meta.url));
const ROOT = resolve(__dirname, '..');

const DRY_RUN = process.argv.includes('--dry-run');
const LIMIT = parseInt(process.argv[process.argv.indexOf('--limit') + 1] || '9999', 10);
const OFFSET = parseInt(process.argv[process.argv.indexOf('--offset') + 1] || '0', 10);

// R2 bucket name and prefix
const BUCKET = 'qnfo';
const R2_PREFIX = 'qnfo';  // The papers-server expects paths starting with "qnfo/"

// Stats
let stats = {
  total: 0,
  withBodyMd: 0,
  generatedFromAbstract: 0,
  uploaded: 0,
  skipped: 0,
  errors: 0
};

function slugify(text) {
  return (text || '')
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-|-$/g, '');
}

function formatDate(dateStr) {
  if (!dateStr) return '';
  try {
    const d = new Date(dateStr);
    if (isNaN(d.getTime())) return dateStr.substring(0, 10);
    return d.toISOString().substring(0, 10);
  } catch {
    return String(dateStr).substring(0, 10);
  }
}

function extractYearMonth(dateStr) {
  if (!dateStr) return { year: '2025', month: '01' };
  const d = formatDate(dateStr);
  const parts = d.split('-');
  return {
    year: parts[0] || '2025',
    month: parts[1] || '01'
  };
}

function generatePaperMd(paper) {
  const title = paper.title || 'Untitled';
  const authors = paper.authors || 'Rowan Brad Quni-Gudzinas';
  const abstract = paper.abstract || '';
  const doi = paper.doi || '';
  const published = formatDate(paper.published || '');
  
  let md = `# ${title}\n\n`;
  
  if (authors) {
    md += `**Authors:** ${authors}\n\n`;
  }
  
  if (published) {
    md += `**Published:** ${published}\n\n`;
  }
  
  if (doi && doi !== 'CHAPTER-FRAGMENT' && !doi.startsWith('10.5281/zenodo.null')) {
    md += `**DOI:** [${doi}](https://doi.org/${encodeURIComponent(doi)})\n\n`;
  }
  
  if (abstract) {
    md += `## Abstract\n\n${abstract}\n\n`;
  }
  
  md += `---\n\n`;
  md += `*This paper is part of the QNFO research corpus. For the canonical typeset PDF, visit [Zenodo](https://zenodo.org/).*\n`;
  
  return md;
}

function getR2Path(paper) {
  const slug = paper.slug;
  const { year, month } = extractYearMonth(paper.published);
  // Primary path the papers-server expects: qnfo/releases/{year}/{month}/{slug}/paper.md
  return `${R2_PREFIX}/releases/${year}/${month}/${slug}/paper.md`;
}

async function uploadToR2(localPath, r2Path) {
  if (DRY_RUN) {
    console.log(`  [DRY RUN] Would upload: ${localPath} → ${r2Path}`);
    return true;
  }
  
  try {
    const cmd = `npx wrangler r2 object put "${BUCKET}/${r2Path}" --file="${localPath}" --content-type "text/markdown"`;
    execSync(cmd, { 
      cwd: ROOT, 
      stdio: 'pipe',
      timeout: 30000 
    });
    return true;
  } catch (err) {
    console.error(`  Upload error for ${r2Path}: ${err.message}`);
    return false;
  }
}

async function main() {
  console.log('=== QNFO Paper Batch Upload to R2 ===');
  console.log(`Mode: ${DRY_RUN ? 'DRY RUN' : 'LIVE UPLOAD'}`);
  console.log(`Limit: ${LIMIT}, Offset: ${OFFSET}`);
  console.log('');
  
  // Read the export
  const exportPath = join(ROOT, 'paper-export.json');
  console.log(`Reading ${exportPath}...`);
  
  const raw = readFileSync(exportPath, 'utf-8');
  const jsonData = JSON.parse(raw);
  
  // The wrangler output is an array of batches
  let papers = [];
  if (Array.isArray(jsonData)) {
    for (const batch of jsonData) {
      if (batch.results && Array.isArray(batch.results)) {
        papers.push(...batch.results);
      }
    }
  }
  
  console.log(`Found ${papers.length} papers total.`);
  
  // Apply offset/limit
  papers = papers.slice(OFFSET, OFFSET + LIMIT);
  stats.total = papers.length;
  console.log(`Processing ${papers.length} papers (offset=${OFFSET}, limit=${LIMIT})...\n`);
  
  // Create temp directory for markdown files
  const tmpDir = join(ROOT, 'tmp-papers');
  if (!existsSync(tmpDir) && !DRY_RUN) {
    mkdirSync(tmpDir, { recursive: true });
  }
  
  let batchNum = 0;
  const BATCH_SIZE = 50;
  const batches = [];
  
  for (let i = 0; i < papers.length; i += BATCH_SIZE) {
    batches.push(papers.slice(i, i + BATCH_SIZE));
  }
  
  console.log(`Split into ${batches.length} batches of up to ${BATCH_SIZE} papers each.\n`);
  
  for (const batch of batches) {
    batchNum++;
    console.log(`--- Batch ${batchNum}/${batches.length} (${batch.length} papers) ---`);
    
    for (const paper of batch) {
      const slug = paper.slug;
      
      if (!slug || slug === 'None') {
        stats.skipped++;
        continue;
      }
      
      // Use body_md if available, otherwise generate from metadata
      let markdown = '';
      if (paper.body_md && paper.body_md !== 'None' && paper.body_md.length > 50) {
        markdown = paper.body_md;
        stats.withBodyMd++;
      } else {
        markdown = generatePaperMd(paper);
        stats.generatedFromAbstract++;
      }
      
      const r2Path = getR2Path(paper);
      const localPath = join(tmpDir, `${slug.replace(/[^a-zA-Z0-9_-]/g, '_')}.md`);
      
      if (!DRY_RUN) {
        writeFileSync(localPath, markdown, 'utf-8');
      }
      
      const success = await uploadToR2(localPath, r2Path);
      if (success) {
        stats.uploaded++;
        if (stats.uploaded % 50 === 0) {
          console.log(`  Progress: ${stats.uploaded}/${stats.total} uploaded...`);
        }
      } else {
        stats.errors++;
      }
    }
    
    console.log(`  Batch ${batchNum} complete. Pausing 2s...`);
    if (!DRY_RUN) {
      await new Promise(r => setTimeout(r, 2000));
    }
  }
  
  // Cleanup
  if (!DRY_RUN && existsSync(tmpDir)) {
    try {
      execSync(`Remove-Item -Recurse -Force "${tmpDir}"`, { shell: 'powershell.exe', stdio: 'pipe' });
    } catch {}
  }
  
  console.log('\n=== UPLOAD COMPLETE ===');
  console.log(`Total papers:       ${stats.total}`);
  console.log(`With body_md:       ${stats.withBodyMd}`);
  console.log(`Generated from abs: ${stats.generatedFromAbstract}`);
  console.log(`Uploaded to R2:     ${stats.uploaded}`);
  console.log(`Skipped:             ${stats.skipped}`);
  console.log(`Errors:              ${stats.errors}`);
}

main().catch(err => {
  console.error('Fatal error:', err);
  process.exit(1);
});
