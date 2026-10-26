#!/usr/bin/env node
// check-rejections.js — fail if a slug in the private rejections.csv is live in creators-master.csv
// without a re-admit note. Run automatically by convert.js; also runnable alone.
//
// A rejected slug may stay in the master only if journalism-atlas-private/data/readmits.csv
// has a row for it (slug,date,decided_by,note) dated after the rejection.
// Reads the private repo from ../journalism-atlas-private (sibling checkout). Fails closed
// when it is missing; pass --skip-rejection-check to bypass on purpose.

const fs = require('fs');
const path = require('path');

const ROOT = path.join(__dirname, '..');
const PRIVATE = process.env.ATLAS_PRIVATE_DIR || path.join(ROOT, '..', 'journalism-atlas-private');

function parseCSV(text) {
  const rows = []; let f = [], cur = '', q = false;
  for (let i = 0; i < text.length; i++) {
    const ch = text[i], nx = text[i + 1];
    if (ch === '"') { if (q && nx === '"') { cur += '"'; i++; } else q = !q; }
    else if (ch === ',' && !q) { f.push(cur); cur = ''; }
    else if ((ch === '\n' || (ch === '\r' && nx === '\n')) && !q) {
      if (ch === '\r') i++;
      f.push(cur); cur = '';
      if (f.some(x => x !== '')) rows.push(f);
      f = [];
    } else cur += ch;
  }
  if (cur !== '' || f.length) { f.push(cur); if (f.some(x => x !== '')) rows.push(f); }
  return rows;
}

function readTable(file) {
  const rows = parseCSV(fs.readFileSync(file, 'utf8').replace(/^﻿/, ''));
  const head = rows.shift();
  return rows.map(r => Object.fromEntries(head.map((h, i) => [h, r[i] || ''])));
}

function checkRejections() {
  const rejFile = path.join(PRIVATE, 'data', 'rejections.csv');
  const readmitFile = path.join(PRIVATE, 'data', 'readmits.csv');
  if (!fs.existsSync(rejFile)) {
    console.error(`FATAL: ${rejFile} not found. The rejected-slug check cannot run. ` +
                  `Check out journalism-atlas-private next to this repo, set ATLAS_PRIVATE_DIR, or pass --skip-rejection-check.`);
    process.exit(1);
  }
  const master = readTable(path.join(ROOT, 'assets', 'data', 'creators-master.csv'));
  const live = new Set(master.map(r => r.slug));
  const readmits = new Map();
  if (fs.existsSync(readmitFile)) readTable(readmitFile).forEach(r => readmits.set(r.slug, r));
  const bad = [];
  readTable(rejFile).forEach(r => {
    if (r.status && r.status !== 'rejected') return;
    if (!live.has(r.slug)) return;
    const re = readmits.get(r.slug);
    if (!re || !re.date || !re.decided_by || !re.note || re.date < r.date) bad.push(r);
  });
  if (bad.length) {
    console.error(`FATAL: ${bad.length} rejected slug(s) are live in creators-master.csv with no valid re-admit note:`);
    bad.forEach(r => console.error(`  ${r.slug}  rejected ${r.date} by ${r.decided_by} (${r.reason_code})`));
    console.error('Remove them from the master (move to the hold list) or add a row to journalism-atlas-private/data/readmits.csv (slug,date,decided_by,note) dated after the rejection.');
    process.exit(1);
  }
  console.log('Rejection check OK: no rejected slug is live without a re-admit note.');
}

module.exports = { checkRejections };
if (require.main === module) checkRejections();
