#!/usr/bin/env node
// convert.js — CSV to JSON converter for Independent Journalism Atlas
// Usage: node convert.js
// Input:  assets/data/creators-master.csv  (source of truth)
// Output: assets/data/creators-data.json

const fs = require('fs');
const path = require('path');

const INPUT  = path.join(__dirname, 'assets', 'data', 'creators-master.csv');
const OUTPUT = path.join(__dirname, 'assets', 'data', 'creators-data.json');

// Parse a CSV line respecting double-quoted fields that may contain commas.
function parseLine(line) {
  const fields = [];
  let current = '';
  let inQuotes = false;

  for (let i = 0; i < line.length; i++) {
    const ch = line[i];
    if (ch === '"') {
      if (inQuotes && line[i + 1] === '"') {
        // Escaped quote inside a quoted field
        current += '"';
        i++;
      } else {
        inQuotes = !inQuotes;
      }
    } else if (ch === ',' && !inQuotes) {
      fields.push(current);
      current = '';
    } else {
      current += ch;
    }
  }
  fields.push(current);
  return fields;
}

const raw = fs.readFileSync(INPUT, 'utf8');
const lines = raw.split(/\r?\n/);

// First line is the header
const headers = parseLine(lines[0]);

const creators = [];

for (let i = 1; i < lines.length; i++) {
  const line = lines[i].trim();
  if (!line) continue;

  const values = parseLine(line);

  // Map by header name
  const row = {};
  headers.forEach((h, idx) => {
    row[h] = (values[idx] || '').trim();
  });

  // Skip rows with no creator name
  if (!row['Creator Name']) continue;

  // Groups field: use the full value as parsed (CSV quoting already handled).
  // Treat spreadsheet formula errors as empty.
  // index.html filters on a single `group` string match.
  const groupRaw = row['Groups'] || '';
  const group = groupRaw.startsWith('#') ? '' : groupRaw;

  creators.push({
    name:      row['Creator Name'],
    channel:   row['Creator Channel'],
    link:      row['Link Primary'],
    platform:  row['Platform Primary'],
    topic:     row['Topic/Category'],
    geography: row['Geography'],
    group:     group,
  });
}

fs.writeFileSync(OUTPUT, JSON.stringify(creators, null, 2), 'utf8');
console.log(`Done — wrote ${creators.length} creators to ${OUTPUT}`);
