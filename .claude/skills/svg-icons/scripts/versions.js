// Builds icon versions from a logo SVG: original, plain, line and (with --text)
// their wordmarks, each fitted to viewBox 0 0 128 128 (centred, no padding),
// optimized with SVGO, ids prefixed with the file name.
//   plain = one path, one colour: shapes united, white shapes become holes,
//           optional gaps where differently coloured shapes overlap
//   line  = inner outline of plain (stroke converted to a filled path)
//
//   node versions.js <logo.svg> --name foo --out dir/
//     [--logo 6-9,11]      shape indexes of the logo (default: all; see inspect.js)
//     [--text 0-5]         shape indexes of the wordmark text -> *-wordmark versions
//     [--gap 2.5]          gap (in 128 units) between overlapping colours in plain
//     [--color '#hex']     plain/line colour (default: colour with the largest area)
//     [--wordmark-color '#hex']
//     [--line-width 4]     outline width of line versions (128 units)
//     [--plain-only '#000000']  build plain/line from shapes of this colour only
//     [--skip line,plain-wordmark]
// Writes <name>-<version>.svg files and preview.png into --out.
const fs = require('fs'), path = require('path');
const B = require('./build');
const { paper } = B;

const args = process.argv.slice(2);
const opt = (k, d) => { const i = args.indexOf(k); return i >= 0 ? args.splice(i, 2)[1] : d; };
const range = s => s ? s.split(',').flatMap(p => { const [a, b] = p.split('-').map(Number); return b === undefined ? [a] : Array.from({ length: b - a + 1 }, (_, i) => a + i); }) : null;
const name = opt('--name'), outDir = opt('--out', '.');
const logoIdx = range(opt('--logo')), textIdx = range(opt('--text'));
const gap = Number(opt('--gap', 0)), color = opt('--color'), wordmarkColor = opt('--wordmark-color');
const lineWidth = Number(opt('--line-width', 4)), plainOnly = opt('--plain-only');
const skip = (opt('--skip', '') || '').split(',');
const src = args[0];
if (!src || !name) { console.error('usage: node versions.js <logo.svg> --name foo --out dir [options]'); process.exit(1); }

const all = B.leaves(fs.readFileSync(src, 'utf8'));
const logo = all.filter((l, i) => logoIdx ? logoIdx.includes(i) : !(textIdx || []).includes(i));
const text = textIdx ? all.filter((l, i) => textIdx.includes(i)) : [];
const clone = (p, m) => { const c = p.clone({ insert: false }); if (m) c.transform(m); return c; };
const plainOf = (ls, m, g = gap) => B.plainPath(ls.filter(l => !plainOnly || B.hex(l.color) === plainOnly).map(l => ({ ...l, path: clone(l.path, m) })), { gap: g });
const one = (p, c) => B.optimize(B.pathSvg(p, c));
const prominent = ls => {
  const area = {};
  for (const l of ls) if (!B.isWhite(l.color)) { const h = B.hex(l.color); area[h] = (area[h] || 0) + Math.abs(l.path.area); }
  return Object.entries(area).sort((a, b) => b[1] - a[1])[0][0];
};
const originalOf = ls => {
  const m = B.fitMatrix(B.unionAll(ls.map(l => l.path)).bounds);
  paper.project.clear();
  const g = new paper.Group(ls.map(l => { const p = clone(l.path, m); p.fillColor = l.path.fillColor; return p; }));
  return B.optimize(B.svgDoc(g.exportSVG({ asString: true, precision: 3 }).replace(/ xmlns="[^"]*"/g, '')));
};

const files = {};
const col = color || prominent(logo);
// A logo in one solid colour is already font-ready: its original is a single
// path (holes wound for the nonzero rule) and plain becomes an alias of it.
const oneColour = ls => !ls.some(l => l.color.gradient) && new Set(ls.filter(l => !B.isWhite(l.color)).map(l => B.hex(l.color))).size === 1;
const solo = oneColour(logo), soloW = text.length && oneColour([...logo, ...text]);
const lp = plainOf(logo, B.fitMatrix(B.unionAll(logo.map(l => l.path)).bounds));
lp.transform(B.fitMatrix(lp.bounds));
if (!skip.includes('original')) files.original = solo ? one(lp, prominent(logo)) : originalOf(logo);
if (!skip.includes('plain') && !solo) files.plain = one(lp, col);
if (!skip.includes('line')) files.line = one(B.linePath(lp, lineWidth), col);
if (solo) console.log('note: one-colour logo, so original is font-ready: add "original" to versions.font and alias original -> plain');

if (text.length) {
  const both = [...logo, ...text];
  const mw = B.fitMatrix(B.unionAll(both.map(l => l.path)).bounds);
  const lpW = plainOf(logo, mw), tpW = plainOf(text, mw, 0);
  const plainW = lpW.unite(tpW, { insert: false });
  const s = B.fitMatrix(plainW.bounds);
  [plainW, lpW, tpW].forEach(p => p.transform(s));
  const wc = wordmarkColor || col;
  if (!skip.includes('original-wordmark')) files['original-wordmark'] = soloW ? one(plainW, prominent(both)) : originalOf(both);
  if (!skip.includes('plain-wordmark') && !soloW) files['plain-wordmark'] = one(plainW, wc);
  if (soloW) console.log('note: one-colour wordmark: add "original-wordmark" to versions.font and alias original-wordmark -> plain-wordmark');
  if (!skip.includes('line-wordmark')) {
    // outline the logo; letters stay solid (outlined letters get too thin)
    const w = Math.max(1.5, lineWidth * Math.max(lpW.bounds.width, lpW.bounds.height) / 128);
    files['line-wordmark'] = one(B.linePath(lpW, w).unite(tpW, { insert: false }), wc);
  }
}

fs.mkdirSync(outDir, { recursive: true });
for (const [v, svg] of Object.entries(files)) {
  const f = path.join(outDir, `${name}-${v}.svg`);
  fs.writeFileSync(f, B.prefixIds(svg, `${name}-${v}`).trim() + '\n');
  console.log(f);
}
require('child_process').execFileSync(process.execPath, [path.join(__dirname, 'render.js'), outDir, '--out', path.join(outDir, 'preview.png')], { stdio: 'inherit' });
