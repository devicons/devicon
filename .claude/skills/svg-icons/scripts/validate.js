// Checks icon SVGs against common icon-set rules (devicon's by default):
// viewBox 0 0 128 128, content touching the box (no padding) and centred,
// no strokes/<image>/<text>/transforms, ids prefixed with the file name,
// newline at the end; *-plain*/*-line* files: only <svg xmlns viewBox> and
// one <path d fill>. Exit code 1 if anything fails.
//   node validate.js <file.svg|dir>...
const fs = require('fs'), path = require('path');
const B = require('./build');

// Font versions may only contain <svg xmlns viewBox> with one <path d fill>:
// everything else (groups, other shapes, defs/use, styles, opacity, fill-rule,
// transforms, ...) is lost or misread by the font build. Returns the problems.
function fontMarkupProblems(s) {
  const tags = [...s.matchAll(/<([a-zA-Z][\w:-]*)\b([^>]*?)\/?>/g)].map(m => ({ name: m[1], attrs: [...m[2].matchAll(/([\w:-]+)\s*=/g)].map(a => a[1]) }));
  const p = [];
  const extra = tags.filter(t => t.name !== 'svg' && t.name !== 'path').map(t => `<${t.name}>`);
  const paths = tags.filter(t => t.name === 'path');
  if (paths.length !== 1) p.push(`${paths.length} <path> elements (exactly 1 allowed)`);
  if (extra.length) p.push(`other elements: ${[...new Set(extra)].join(', ')}`);
  const bad = (t, ok) => t.attrs.filter(a => !ok.includes(a));
  const svgExtra = tags.filter(t => t.name === 'svg').flatMap(t => bad(t, ['xmlns', 'viewBox']));
  const pathExtra = paths.flatMap(t => bad(t, ['d', 'fill']));
  if (svgExtra.length) p.push(`<svg> attributes besides xmlns/viewBox: ${svgExtra.join(', ')}`);
  if (pathExtra.length) p.push(`<path> attributes besides d/fill: ${pathExtra.join(', ')}`);
  if (/<(?!\/?(svg|path)\b)[!?]/.test(s)) p.push('comments, doctype or XML declaration');
  const fill = (s.match(/<path\b[^>]*\sfill="([^"]*)"/) || [])[1];
  if (fill !== undefined && !/^#[0-9a-fA-F]{3}([0-9a-fA-F]{3})?$/.test(fill)) p.push(`fill="${fill}" (needs a #hex colour)`);
  return p;
}

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
    // allowlist: only <svg xmlns viewBox> and one <path d fill>
    for (const m of fontMarkupProblems(s)) p.push(`plain/line may only have <svg xmlns viewBox> and one <path d fill>; found ${m}`);
  }
  try { // padding/centring from the rendered shapes
    const b = B.unionAll(B.leaves(s).map(l => l.path)).bounds;
    const big = Math.max(b.width, b.height);
    if (b.left < -0.5 || b.top < -0.5 || b.right > 128.5 || b.bottom > 128.5) p.push(`outside the box (${b.left.toFixed(1)},${b.top.toFixed(1)} to ${b.right.toFixed(1)},${b.bottom.toFixed(1)})`);
    if (big < 127) p.push(`padding: content is ${big.toFixed(1)} wide/high, should fill 128`);
    if (Math.abs(b.center.x - 64) > 1 || Math.abs(b.center.y - 64) > 1) p.push(`not centred (centre ${b.center.x.toFixed(1)},${b.center.y.toFixed(1)})`);
  } catch (e) { p.push('could not parse shapes: ' + e.message.split('\n')[0]); }
  if (p.length) { bad++; console.log(`FAIL ${f}\n  - ${p.join('\n  - ')}`); } else console.log(`ok   ${f}`);
}
console.log(`${files.length} files, ${bad} failing`);
process.exit(bad ? 1 : 0);
