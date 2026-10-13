#!/usr/bin/env node
// Audits the *published* GitHub Pages site, not a local stand-in.
// Keep Lighthouse versions fixed in .github/workflows/lighthouse-performance.yml.
'use strict';
const fs = require('node:fs');
const path = require('node:path');
const { spawnSync } = require('node:child_process');

const url = process.env.SITE_URL || 'https://eisatopon.github.io/national-olympiads-bank/';
const output = path.resolve('lighthouse-results');
fs.mkdirSync(output, { recursive: true });
const metrics = ['first-contentful-paint', 'largest-contentful-paint', 'total-blocking-time', 'cumulative-layout-shift', 'speed-index'];
const all = [];
let failures = 0;

for (const device of ['mobile', 'desktop']) {
  for (let n = 1; n <= 3; n++) {
    const name = `${device}-${n}`;
    const file = path.join(output, name + '.json');
    const args = [
      'lighthouse', url,
      '--output=json', '--output-path=' + file,
      '--chrome-flags=--headless --no-sandbox --disable-dev-shm-usage',
      '--throttling-method=simulate', '--quiet'
    ];
    if (device === 'desktop') args.push('--preset=desktop');
    process.stdout.write(`Running ${name} against ${url}\n`);
    const run = spawnSync('npx', args, { encoding: 'utf8', timeout: 150000 });
    if (run.status !== 0 || !fs.existsSync(file)) {
      failures++;
      console.error(`FAIL ${name}: ${run.error?.message || run.stderr || run.stdout || run.status}`);
      continue;
    }
    try {
      const report = JSON.parse(fs.readFileSync(file, 'utf8'));
      const row = { device, run: n, score: Math.round(report.categories.performance.score * 100) };
      for (const key of metrics) row[key] = report.audits[key]?.numericValue ?? null;
      row.lcp_element = report.audits['largest-contentful-paint-element']?.details?.items?.[0]?.node?.snippet || null;
      row.final_url = report.finalDisplayedUrl || report.finalUrl || url;
      all.push(row);
    } catch (err) {
      failures++;
      console.error(`Could not parse ${name}: ${err.message}`);
    }
  }
}
const median = vals => {
  const arr = vals.filter(v => typeof v === 'number' && Number.isFinite(v)).sort((a,b) => a-b);
  return arr.length ? arr[Math.floor(arr.length / 2)] : null;
};
const lines = [
  '## Lighthouse performance — published GitHub Pages',
  '',
  'Each value is the median of three runs (when all runs succeed). Scores are lab estimates, not field data.',
  '',
  '| Device | Runs | Performance | FCP (ms) | LCP (ms) | TBT (ms) | CLS | Speed Index (ms) |',
  '|---|---:|---:|---:|---:|---:|---:|---:|'
];
for (const device of ['mobile', 'desktop']) {
  const rows = all.filter(r => r.device === device);
  const val = key => median(rows.map(r => r[key]));
  lines.push(`| ${device} | ${rows.length}/3 | ${val('score') ?? '—'} | ${val('first-contentful-paint')?.toFixed(0) ?? '—'} | ${val('largest-contentful-paint')?.toFixed(0) ?? '—'} | ${val('total-blocking-time')?.toFixed(0) ?? '—'} | ${val('cumulative-layout-shift')?.toFixed(3) ?? '—'} | ${val('speed-index')?.toFixed(0) ?? '—'} |`);
  const snippets = [...new Set(rows.map(r => r.lcp_element).filter(Boolean))];
  if (snippets.length) lines.push('', `**${device} LCP element(s):** ${snippets.map(s => '\`'+s.replace(/\`/g, '')+'\`').join(', ')}`);
}
lines.push('', 'Full per-run Lighthouse JSON reports are available as workflow artifacts.');
fs.writeFileSync(path.join(output, 'summary.md'), lines.join('\n') + '\n');
fs.writeFileSync(path.join(output, 'runs.json'), JSON.stringify(all, null, 2) + '\n');
console.log(lines.join('\n'));
if (failures || all.length !== 6) {
  console.error(`Lighthouse completed with ${failures} failed runs; expected six reports, got ${all.length}.`);
  process.exitCode = 1;
}
