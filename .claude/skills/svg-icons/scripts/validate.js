// Checks icon SVGs against common icon-set rules (devicon's by default):
// viewBox 0 0 128 128, content touching the box (no padding) and centred,
// no strokes/<image>/<text>/transforms, ids prefixed with the file name,
// newline at the end; *-plain*/*-line* files: exactly one path, one fill,
// no gradients/masks. Exit code 1 if anything fails.
//   node validate.js <file.svg|dir>...
const fs = require('fs'), path = require('path');
const B = require('./build');

const files = process.argv.slice(2).flatMap(a => fs.statSync(a).isDirectory()
  ? fs.readdirSync(a).filter(f => f.endsWith('.svg')).map(f => path.join(a, f)) : [a]);
let bad = 0;
for (const f of files) {
  const s = fs.readFileSync(f, 'utf8'), stem = path.basename(f, '.svg'), p = [];
  if (!/viewBox="0 0 128 128"/.test(s)) p.push('viewBox is not "0 0 128 128"');
  if (/\s(width|height)="/.test((s.match(/<svg\b[^>]*>/) || [''])[0])) p.push('root has width/height attributes');
  if (/(^|[\s;"])stroke\s*[=:]\s*"?(?!none|transparent)[#a-z]/i.test(s)) p.push('has strokes');
  if (/<image\b/.test(s)) p.push('embeds a raster <image>');
  if (/<text\b/.test(s)) p.push('has <text> (convert to paths)');
  if (/transform=/.test(s)) p.push('has transforms (bake them in)');
  if (!s.endsWith('\n')) p.push('no newline at the end');
  for (const m of s.matchAll(/\sid="([^"]+)"/g)) if (!m[1].startsWith(stem + '-')) p.push(`id "${m[1]}" not prefixed with "${stem}-"`);
  if (/-(plain|line)(-wordmark)?$/.test(stem)) {
    const n = (s.match(/<path\b/g) || []).length, fills = new Set(s.match(/fill="(?!none)[^"]+"/g) || []);
    if (n !== 1) p.push(`${n} paths (plain/line need exactly 1)`);
    if (fills.size > 1) p.push(`${fills.size} fill colours (plain/line need 1)`);
    if (/Gradient|<mask|<clipPath/.test(s)) p.push('gradient/mask/clip in a plain/line version');
  }
  try { // padding/centring from the rendered shapes
    const b = B.unionAll(B.leaves(s).map(l => l.path)).bounds;
    const big = Math.max(b.width, b.height);
    if (big < 127) p.push(`padding: content is ${big.toFixed(1)} wide/high, should fill 128`);
    if (Math.abs(b.center.x - 64) > 1 || Math.abs(b.center.y - 64) > 1) p.push(`not centred (centre ${b.center.x.toFixed(1)},${b.center.y.toFixed(1)})`);
  } catch (e) { p.push('could not parse shapes: ' + e.message.split('\n')[0]); }
  if (p.length) { bad++; console.log(`FAIL ${f}\n  - ${p.join('\n  - ')}`); } else console.log(`ok   ${f}`);
}
console.log(`${files.length} files, ${bad} failing`);
process.exit(bad ? 1 : 0);
