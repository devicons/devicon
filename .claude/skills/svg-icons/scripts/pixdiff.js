// Renders two SVGs (or two folders of same-named SVGs) and reports pixel
// differences, e.g. to prove an id rename or optimization changed nothing.
//   node pixdiff.js <a.svg|dirA> <b.svg|dirB> [--size 256]
const fs = require('fs'), path = require('path');
const { Resvg } = require('@resvg/resvg-js');
const args = process.argv.slice(2);
const i = args.indexOf('--size'); const size = i >= 0 ? Number(args.splice(i, 2)[1]) : 256;
const [A, Bp] = args;
const pairs = fs.statSync(A).isDirectory()
  ? fs.readdirSync(A).filter(f => f.endsWith('.svg') && fs.existsSync(path.join(Bp, f))).map(f => [path.join(A, f), path.join(Bp, f)])
  : [[A, Bp]];
const render = f => {
  let s = fs.readFileSync(f, 'utf8');
  if (!/xmlns="http:\/\/www\.w3\.org\/2000\/svg"/.test(s)) s = s.replace('<svg', '<svg xmlns="http://www.w3.org/2000/svg"');
  return new Resvg(s, { fitTo: { mode: 'width', value: size } }).render();
};
let same = 0;
for (const [a, b] of pairs) {
  try {
    const ra = render(a), rb = render(b);
    if (ra.width !== rb.width || ra.height !== rb.height) { console.log(`DIFF ${path.basename(a)}: size ${ra.width}x${ra.height} vs ${rb.width}x${rb.height}`); continue; }
    // .pixels makes a new buffer on every access: read it once
    const pa = ra.pixels, pb = rb.pixels;
    let n = 0;
    for (let k = 0; k < pa.length; k++) if (Math.abs(pa[k] - pb[k]) > 2) n++;
    if (n) console.log(`DIFF ${path.basename(a)}: ${n} channel values differ`); else same++;
  } catch (e) { console.log(`ERR  ${path.basename(a)}: ${e.message.split('\n')[0]}`); }
}
console.log(`identical: ${same}/${pairs.length}`);
