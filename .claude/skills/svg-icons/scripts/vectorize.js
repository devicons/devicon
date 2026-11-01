// Turns a raster logo (PNG/JPG) into an SVG: finds the logo's few flat colours
// (or uses --palette), traces each colour with potrace, stacks the layers
// (biggest at the bottom, each grown slightly under the ones above so no seams
// show), drops the background, fits the result to 0 0 128 128 and optimizes it.
// The output is an ordinary multi-colour SVG for versions.js.
//   node vectorize.js <logo.png> --out logo.svg [--colors 6] [--palette '#hex,#hex'] [--size 1024] [--smooth 4]
// --colors: most colours to find (default 6). --palette: use these colours
// instead (snap to the brand's real values). --size: long side the image is
// resampled to before tracing (default 1024; smoother curves from small files).
// --smooth: blur radius in pixels at that size (default size/256 = 4) that
// irons out pixel stairs; lower it (1-2) to keep thin lines, at the cost of
// wobblier edges that plain/line versions may show as notches.
// Background: transparent pixels, or else the colour around the border, only
// where it's connected to the border (enclosed white parts stay white fills).
const fs = require('fs'), path = require('path');
const Jimp = require('jimp');
const B = require('./build');
const { traceBits } = require('./trace');
const { paper } = B;

const args = process.argv.slice(2);
const opt = (name, def) => { const i = args.indexOf(name); return i >= 0 ? args.splice(i, 2)[1] : def; };
const out = opt('--out'), maxColors = Number(opt('--colors', 6)), size = Number(opt('--size', 1024));
const palArg = opt('--palette');
const smoothR = Number(opt('--smooth', Math.max(1, Math.round(size / 256))));
const file = args[0];
if (!file || !out) { console.error('usage: node vectorize.js <logo.png> --out logo.svg [--colors 6] [--palette "#hex,..."] [--size 1024] [--smooth 4]'); process.exit(2); }

const hex = c => '#' + c.map(v => Math.round(v).toString(16).padStart(2, '0')).join('');
const parseHex = h => { h = h.trim().replace('#', ''); if (h.length === 3) h = [...h].map(x => x + x).join(''); return [0, 2, 4].map(i => parseInt(h.slice(i, i + 2), 16)); };
const dist2 = (a, b) => (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2 + (a[2] - b[2]) ** 2;

// Smooths a mask's pixel stairs (box blur twice, threshold at half): potrace
// follows stairs faithfully, and plain/line offsets turn them into notches.
function smooth(bits, W, H, r) {
  let a = Float32Array.from(bits);
  const pass = (src, horizontal) => {
    const dst = new Float32Array(W * H), n = horizontal ? W : H, m = horizontal ? H : W;
    for (let j = 0; j < m; j++) {
      const at = i => horizontal ? j * W + i : i * W + j;
      let sum = 0;
      for (let i = -r; i <= r; i++) sum += src[at(Math.min(n - 1, Math.max(0, i)))];
      for (let i = 0; i < n; i++) {
        dst[at(i)] = sum / (2 * r + 1);
        sum += src[at(Math.min(n - 1, i + r + 1))] - src[at(Math.max(0, i - r))];
      }
    }
    return dst;
  };
  for (let t = 0; t < 2; t++) a = pass(pass(a, true), false);
  return Uint8Array.from(a, v => v >= 0.5 ? 1 : 0);
}

(async () => {
  const im = await Jimp.read(file);
  const s = size / Math.max(im.bitmap.width, im.bitmap.height);
  im.resize(Math.round(im.bitmap.width * s), Math.round(im.bitmap.height * s), Jimp.RESIZE_BICUBIC);
  const { width: W, height: H, data } = im.bitmap, N = W * H;
  const rgb = k => [data[4 * k], data[4 * k + 1], data[4 * k + 2]];
  const border = [];
  for (let x = 0; x < W; x++) border.push(x, (H - 1) * W + x);
  for (let y = 0; y < H; y++) border.push(y * W, y * W + W - 1);

  // background: transparent pixels, or the most common border colour
  const transparent = border.filter(k => data[4 * k + 3] < 128).length > border.length / 4;
  let bg = null;
  if (!transparent) {
    const bins = new Map();
    for (const k of border) { const c = rgb(k), key = c.map(v => v >> 4).join(); const b = bins.get(key) || { n: 0, s: [0, 0, 0] }; b.n++; c.forEach((v, j) => b.s[j] += v); bins.set(key, b); }
    const top = [...bins.values()].sort((a, b) => b.n - a.n)[0];
    bg = top.s.map(v => v / top.n);
  }
  const opaque = k => data[4 * k + 3] >= 128;
  const isBgColour = k => bg && dist2(rgb(k), bg) < 40 ** 2;

  // palette: the given colours, or the most common distinct colours
  let pal;
  if (palArg) pal = palArg.split(',').map(parseHex);
  else {
    const bins = new Map(); let fg = 0;
    for (let k = 0; k < N; k++) {
      if (!opaque(k)) continue;
      const c = rgb(k), key = c.map(v => v >> 3).join();
      const b = bins.get(key) || { n: 0, s: [0, 0, 0] }; b.n++; c.forEach((v, j) => b.s[j] += v); bins.set(key, b); fg++;
    }
    pal = [];
    for (const b of [...bins.values()].sort((a, b) => b.n - a.n)) {
      if (pal.length >= maxColors + (bg ? 1 : 0) || b.n < fg * 0.003) break;
      const c = b.s.map(v => v / b.n);
      if (pal.every(p => dist2(p, c) >= 48 ** 2)) pal.push(c);
    }
    // refine each colour to the mean of the pixels close to it (anti-aliasing excluded)
    const acc = pal.map(() => ({ n: 0, s: [0, 0, 0] }));
    for (let k = 0; k < N; k++) {
      if (!opaque(k)) continue;
      const c = rgb(k);
      pal.forEach((p, j) => { if (dist2(p, c) < 24 ** 2) { acc[j].n++; c.forEach((v, t) => acc[j].s[t] += v); } });
    }
    pal = pal.map((p, j) => acc[j].n ? acc[j].s.map(v => v / acc[j].n) : p);
  }
  if (bg && !pal.some(p => dist2(p, bg) < 40 ** 2)) pal.push(bg);

  // label every pixel with its palette colour (0 = background). Anti-aliased
  // edge pixels sit between two colours (and can be nearest to a third one, as
  // red-on-white is to orange): they take the label of the nearest clear pixel
  // of one of their two nearest colours (so a gradient never turns background).
  const label = new Int16Array(N).fill(-1), cand1 = new Int16Array(N), cand2 = new Int16Array(N);
  const queue = [];
  for (let k = 0; k < N; k++) {
    if (!opaque(k)) { label[k] = 0; queue.push(k); continue; }
    const c = rgb(k); let b1 = 0, b2 = 0, d1 = Infinity, d2 = Infinity;
    pal.forEach((p, j) => { const d = dist2(p, c); if (d < d1) { d2 = d1; b2 = b1; d1 = d; b1 = j; } else if (d < d2) { d2 = d; b2 = j; } });
    cand1[k] = b1 + 1; cand2[k] = b2 + 1;
    if (d1 < 12 ** 2 || d1 < d2 / 4) { label[k] = b1 + 1; queue.push(k); } // within a third of the way
  }
  // second pass: pixels none of whose colours reached them take any neighbour's
  for (const strict of [true, false]) for (let q = 0; q < queue.length; q++) {
    const k = queue[q], x = k % W, l = label[k];
    for (const n of [x > 0 ? k - 1 : -1, x < W - 1 ? k + 1 : -1, k - W, k + W])
      if (n >= 0 && n < N && label[n] === -1 && (!strict || l === cand1[n] || l === cand2[n])) { label[n] = l; queue.push(n); }
  }
  if (bg) { // flood the background colour in from the border
    const bgIdx = pal.findIndex(p => dist2(p, bg) < 40 ** 2) + 1;
    const stack = border.filter(k => label[k] === bgIdx);
    for (const k of stack) label[k] = 0;
    while (stack.length) {
      const k = stack.pop(), x = k % W;
      for (const n of [x > 0 ? k - 1 : -1, x < W - 1 ? k + 1 : -1, k - W, k + W])
        if (n >= 0 && n < N && label[n] === bgIdx) { label[n] = 0; stack.push(n); }
    }
  }

  // layers: colours that are present, biggest bounding box at the bottom
  const layers = pal.map((c, j) => ({ c, j: j + 1, n: 0, x0: W, y0: H, x1: -1, y1: -1 }));
  for (let k = 0; k < N; k++) {
    const l = label[k]; if (l <= 0) continue;
    const L = layers[l - 1], x = k % W, y = (k / W) | 0;
    L.n++; L.x0 = Math.min(L.x0, x); L.y0 = Math.min(L.y0, y); L.x1 = Math.max(L.x1, x); L.y1 = Math.max(L.y1, y);
  }
  const minArea = N * 0.0005;
  const stack = layers.filter(L => L.n > minArea).sort((a, b) => (b.x1 - b.x0) * (b.y1 - b.y0) - (a.x1 - a.x0) * (a.y1 - a.y0));
  if (!stack.length) { console.error('nothing to trace (is the whole image background?)'); process.exit(1); }

  // each layer: its own pixels, grown a few pixels into the layers above it
  // (only there), so neighbouring colours overlap instead of leaving seams
  // (not near the background: there the jagged hidden edge would stick out of
  // the outline, and plain/line versions show it)
  const grow = Math.max(1, Math.round(size / 256));
  const turdSize = Math.round(20 * (size / 1024) ** 2);
  let nearBg = new Uint8Array(N);
  for (let k = 0; k < N; k++) if (label[k] === 0) nearBg[k] = 1;
  for (let g = 0; g <= grow; g++) {
    const next = nearBg.slice();
    for (let k = 0; k < N; k++) {
      if (nearBg[k]) continue;
      const x = k % W;
      if ((x > 0 && nearBg[k - 1]) || (x < W - 1 && nearBg[k + 1]) || (k >= W && nearBg[k - W]) || (k + W < N && nearBg[k + W])) next[k] = 1;
    }
    nearBg = next;
  }
  const paths = [];
  for (let i = 0; i < stack.length; i++) {
    const above = new Set(stack.slice(i + 1).map(L => L.j));
    let bits = new Uint8Array(N);
    for (let k = 0; k < N; k++) if (label[k] === stack[i].j) bits[k] = 1;
    for (let g = 0; g < grow; g++) {
      const next = bits.slice();
      for (let k = 0; k < N; k++) {
        if (bits[k] || nearBg[k] || !above.has(label[k])) continue;
        const x = k % W;
        if ((x > 0 && bits[k - 1]) || (x < W - 1 && bits[k + 1]) || (k >= W && bits[k - W]) || (k + W < N && bits[k + W])) next[k] = 1;
      }
      bits = next;
    }
    const d = await traceBits(smooth(bits, W, H, smoothR), W, H, { turdSize });
    if (!d) continue;
    const p = new paper.CompoundPath({ pathData: d, insert: false });
    p.fillRule = 'evenodd';
    p.reorient(true, true); // nonzero-safe holes for icon fonts
    paths.push({ p, c: stack[i].c, share: stack[i].n / N });
  }

  // bounds of all layers (a boolean union isn't needed and can fail on traced paths)
  const m = B.fitMatrix(paths.map(x => x.p.bounds).reduce((a, b) => a.unite(b)));
  const body = paths.map(({ p, c }) => { p.transform(m); return `<path fill="${hex(c)}" d="${p.pathData}"/>`; }).join('');
  const stem = path.basename(out, '.svg');
  fs.writeFileSync(out, B.prefixIds(B.optimize(B.svgDoc(body)), stem).trim() + '\n');
  console.log(`${out}: ${paths.length} colour layers, bottom to top:`);
  for (const { c, share } of paths) console.log(`  ${hex(c)}  ${(100 * share).toFixed(1)}% of the image`);
  console.log(`background: ${transparent ? 'transparent' : hex(bg) + ' (removed where it touches the border)'}`);
  console.log('Next: render it and compare with the PNG; snap the colours to the brand\'s real values with --palette.');
})().catch(e => { console.error(e); process.exit(1); });
