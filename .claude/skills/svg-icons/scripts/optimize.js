// Optimizes SVGs with SVGO (multipass, 2-decimal precision), prefixes ids with
// the file name ("name-version-a") and ends the file with a newline.
//   node optimize.js <file.svg>... [--out dir]   (in place without --out)
const fs = require('fs'), path = require('path');
const B = require('./build');

const args = process.argv.slice(2);
const i = args.indexOf('--out');
const outDir = i >= 0 ? args.splice(i, 2)[1] : null;
for (const f of args) {
  const before = fs.readFileSync(f, 'utf8');
  const stem = path.basename(f, '.svg');
  const after = B.prefixIds(B.optimize(before), stem).trim() + '\n';
  const o = outDir ? path.join(outDir, path.basename(f)) : f;
  if (outDir) fs.mkdirSync(outDir, { recursive: true });
  fs.writeFileSync(o, after);
  console.log(`${o}: ${before.length} -> ${after.length} bytes`);
}
