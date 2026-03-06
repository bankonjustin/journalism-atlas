#!/usr/bin/env node
// convert.js — CSV to JSON converter for Independent Journalism Atlas
// Usage: node convert.js
// Input:  assets/data/creators-master.csv  (source of truth)
// Output: assets/data/creators-data.json
//
// Schema notes:
//   - `group` and `topic` are stored as comma-separated strings representing
//     multiple values (e.g. "Culture & Media, Power & Politics").
//     Consumers must split on ',' and trim to get individual values.
//   - `group` values starting with '#' (spreadsheet errors like #N/A) are
//     treated as empty.

const fs = require('fs');
const path = require('path');

const INPUT  = path.join(__dirname, 'assets', 'data', 'creators-master.csv');
const OUTPUT = path.join(__dirname, 'assets', 'data', 'creators-data.json');

// Parse an entire CSV file, correctly handling quoted fields that contain
// commas, escaped quotes (""), and embedded newlines.
// Returns an array of rows; each row is an array of string field values.
function parseCSV(text) {
  const rows = [];
  let fields = [];
  let current = '';
  let inQuotes = false;

  for (let i = 0; i < text.length; i++) {
    const ch   = text[i];
    const next = text[i + 1];

    if (ch === '"') {
      if (inQuotes && next === '"') {
        // Escaped quote inside a quoted field
        current += '"';
        i++;
      } else {
        inQuotes = !inQuotes;
      }
    } else if (ch === ',' && !inQuotes) {
      fields.push(current);
      current = '';
    } else if ((ch === '\n' || (ch === '\r' && next === '\n')) && !inQuotes) {
      // End of record (newline outside a quoted field)
      if (ch === '\r') i++; // consume \r of \r\n
      fields.push(current);
      current = '';
      // Skip entirely blank lines
      if (fields.some(f => f !== '')) rows.push(fields);
      fields = [];
    } else {
      current += ch;
    }
  }

  // Flush last record (file may not end with a newline)
  if (current || fields.length) {
    fields.push(current);
    if (fields.some(f => f !== '')) rows.push(fields);
  }

  return rows;
}

const raw  = fs.readFileSync(INPUT, 'utf8');
const rows = parseCSV(raw);

// First row is the header
const headers = rows[0];

const creators = [];

for (let i = 1; i < rows.length; i++) {
  const values = rows[i];

  // Map by header name
  const row = {};
  headers.forEach((h, idx) => {
    row[h] = (values[idx] || '').trim();
  });

  // Skip rows with no creator name
  if (!row['Creator Name']) continue;

  // Groups field: use the full value as parsed (CSV quoting already handled).
  // Treat spreadsheet formula errors (e.g. #N/A) as empty.
  // Consumers split on ',' to get individual group names.
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
