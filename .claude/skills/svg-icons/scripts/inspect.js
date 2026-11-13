// Describes an SVG: root attributes, element counts, ids, strokes/gradients,
// and every visible shape in paint order (index, colour, bounds). The shape
// indexes are what versions.js --logo/--text take.
//   node inspect.js <file.svg>...
const fs = require('fs');
const B = require('./build');

for (const f of process.argv.slice(2)) {
  const src = fs.readFileSync(f, 'utf8');
  const root = (src.match(/<svg\b[^>]*>/) || [''])[0];
  const count = re => (src.match(re) || []).length;
  console.log(`== ${f}`);
  console.log(`  root: ${root.slice(0, 200)}`);
  console.log(`  bytes=${src.length} paths=${count(/<path\b/g)} groups=${count(/<g\b/g)} gradients=${count(/<(linear|radial)Gradient\b/g)} clip/mask=${count(/<(clipPath|mask)\b/g)} strokes=${count(/(^|[\s;"])stroke\s*[=:]\s*"?(?!none|transparent)[#a-z]/gi)} transforms=${count(/transform=/g)} <style>=${count(/<style\b/g)} <image>=${count(/<image\b/g)} <text>=${count(/<text\b/g)}`);
  const ids = [...src.matchAll(/\sid="([^"]+)"/g)].map(m => m[1]);
  if (ids.length) console.log(`  ids: ${ids.slice(0, 20).join(', ')}${ids.length > 20 ? ` (+${ids.length - 20})` : ''}`);
  const ls = B.leaves(src);
  console.log(`  ${ls.length} visible shapes (paint order):`);
  ls.forEach((l, i) => {
    const r = l.path.bounds;
    console.log(`    ${i} ${l.color.gradient ? 'gradient~' : ''}${B.hex(l.color)} x=${r.x.toFixed(1)} y=${r.y.toFixed(1)} w=${r.width.toFixed(1)} h=${r.height.toFixed(1)} area=${Math.abs(l.path.area).toFixed(0)}`);
  });
}
