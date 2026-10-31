// Renders SVGs to a PNG preview sheet so you can look at them (Read the PNG).
// Each SVG is shown on a light and a dark background at several sizes.
//   node render.js <file.svg|dir>... [--out preview.png] [--sizes 128,32,16] [--zoom x,y,w,h] [--big]
//   --zoom crops every SVG to that viewBox region (to inspect a detail)
//   --big renders one large image per SVG instead (600px, white background)
const fs = require('fs'), path = require('path');
const { Resvg } = require('@resvg/resvg-js');

const args = process.argv.slice(2);
const opt = (k, d) => { const i = args.indexOf(k); return i >= 0 ? args.splice(i, 2)[1] : d; };
const flag = k => { const i = args.indexOf(k); return i >= 0 ? (args.splice(i, 1), true) : false; };
const out = opt('--out', 'preview.png');
const sizes = opt('--sizes', '128,32,16').split(',').map(Number);
const zoom = opt('--zoom', null);
const big = flag('--big');

const files = args.flatMap(a => fs.statSync(a).isDirectory()
  ? fs.readdirSync(a).filter(f => f.endsWith('.svg')).sort().map(f => path.join(a, f)) : [a]);
if (!files.length) { console.error('no SVG files given'); process.exit(1); }

const load = f => {
  let s = fs.readFileSync(f, 'utf8');
  if (!/xmlns="http:\/\/www\.w3\.org\/2000\/svg"/.test(s)) s = s.replace('<svg', '<svg xmlns="http://www.w3.org/2000/svg"');
  if (zoom) s = s.replace(/viewBox="[^"]*"/, `viewBox="${zoom.split(',').join(' ')}"`);
  return s;
};
// Rasterise each SVG on its own and embed the PNG: nested SVG images aren't
// clipped to their viewBox, so zoomed shapes would spill out of their cells.
const png = (s, size) => 'data:image/png;base64,' + new Resvg(s, { fitTo: { mode: 'width', value: size } }).render().asPng().toString('base64');

if (big) {
  for (const f of files) {
    const o = files.length === 1 ? out : out.replace(/\.png$/, `-${path.basename(f, '.svg')}.png`);
    const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="600" height="600"><rect width="600" height="600" fill="#fff"/><image width="600" height="600" href="${png(load(f), 600)}"/></svg>`;
    fs.writeFileSync(o, new Resvg(svg).render().asPng());
    console.log(o);
  }
  process.exit(0);
}

const cell = Math.max(...sizes) + 12, pad = 8;
const panelW = sizes.reduce((a, s) => a + s + pad, pad);
let body = '', y = 10;
for (const f of files) {
  const src = load(f);
  body += `<text x="10" y="${y + 14}" font-family="sans-serif" font-size="13">${path.basename(f)}</text>`;
  [['#ffffff', 10], ['#0d1117', 20 + panelW]].forEach(([bg, x0]) => {
    body += `<rect x="${x0}" y="${y + 22}" width="${panelW}" height="${cell}" fill="${bg}" stroke="#ccc"/>`;
    let x = x0 + pad;
    for (const s of sizes) { body += `<image x="${x}" y="${y + 28}" width="${s}" height="${s}" href="${png(src, s)}"/>`; x += s + pad; }
  });
  y += cell + 34;
}
const W = 30 + 2 * panelW;
fs.writeFileSync(out, new Resvg(`<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${y}"><rect width="100%" height="100%" fill="#f4f4f4"/>${body}</svg>`, { font: { loadSystemFonts: true } }).render().asPng());
console.log(out);
