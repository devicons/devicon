// Traces colour masks of a raster logo with potrace; returns path data per mask.
const Jimp = require('jimp'), potrace = require('potrace');

// Path data (potrace, even-odd holes) for a bitmap: bits[y * W + x] = 1 is ink.
async function traceBits(bits, W, H, opts = {}) {
  const m = new Jimp(W, H, 0xffffffff), d = m.bitmap.data;
  for (let k = 0; k < W * H; k++) if (bits[k]) d[4 * k] = d[4 * k + 1] = d[4 * k + 2] = 0;
  const buf = await m.getBufferAsync(Jimp.MIME_PNG);
  const svg = await new Promise((res, rej) => potrace.trace(buf, { turdSize: 20, optTolerance: 0.4, threshold: 128, ...opts }, (e, s) => e ? rej(e) : res(s)));
  return (svg.match(/ d="([^"]+)"/) || [])[1];
}

// One colour of a raster file: keep(r, g, b) picks the pixels, box = [x0, y0, x1, y1]
async function traceMask(file, keep, box) {
  const im = await Jimp.read(file);
  const { width: W, height: H, data } = im.bitmap;
  const bits = new Uint8Array(W * H);
  for (let y = 0; y < H; y++) for (let x = 0; x < W; x++) {
    if (box && (x < box[0] || y < box[1] || x > box[2] || y > box[3])) continue;
    const i = 4 * (y * W + x);
    if (data[i + 3] > 128 && keep(data[i], data[i + 1], data[i + 2])) bits[y * W + x] = 1;
  }
  return traceBits(bits, W, H);
}
module.exports = { traceMask, traceBits };
