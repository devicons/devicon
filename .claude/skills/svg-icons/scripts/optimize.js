// Optimizes SVGs with SVGO (svgo.config.js), prefixes ids with the file name
// ("name-version-a") and ends the file with a newline.
//   node optimize.js <file.svg>... [--out dir]   (in place without --out)
//   node optimize.js --check <file.svg>...       (review: change nothing)
// --check reports files that optimizing would shrink by more than 20% (and
// 500 bytes) or 4 KB, and exits 1 if there are any. Smaller differences are
// noise: an icon optimized with another SVGO version or SVGOMG still shrinks
// a little.
const fs = require('fs'), path = require('path');
const B = require('./build');

const args = process.argv.slice(2);
const i = args.indexOf('--out');
const outDir = i >= 0 ? args.splice(i, 2)[1] : null;
const c = args.indexOf('--check');
const check = c >= 0 && !!args.splice(c, 1);
let unoptimized = 0;
for (const f of args) {
  const before = fs.readFileSync(f, 'utf8');
  const stem = path.basename(f, '.svg');
  const after = B.prefixIds(B.optimize(before, { generic: true }), stem).trim() + '\n';
  const saved = before.length - after.length, pct = Math.round(100 * saved / before.length);
  if (check) {
    const bad = (pct > 20 && saved > 500) || saved > 4096;
    if (bad) unoptimized++;
    console.log(`${bad ? 'UNOPTIMIZED' : 'ok'} ${f}: optimizing would save ${saved} bytes (${pct}%)`);
    continue;
  }
  const o = outDir ? path.join(outDir, path.basename(f)) : f;
  if (outDir) fs.mkdirSync(outDir, { recursive: true });
  fs.writeFileSync(o, after);
  console.log(`${o}: ${before.length} -> ${after.length} bytes`);
}
if (unoptimized) process.exit(1);
