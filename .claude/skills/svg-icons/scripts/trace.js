// Traces colour masks of a raster logo with potrace; returns path data per mask.
const Jimp = require('jimp'), potrace = require('potrace');
async function traceMask(file, keep, box) {
  const im = await Jimp.read(file);
  const { width: W, height: H } = im.bitmap;
  const m = new Jimp(W, H, 0xffffffff);
  im.scan(0, 0, W, H, function (x, y, i) {
    const d = this.bitmap.data;
    if (box && (x < box[0] || y < box[1] || x > box[2] || y > box[3])) return;
    if (d[i + 3] > 128 && keep(d[i], d[i + 1], d[i + 2])) m.setPixelColor(0x000000ff, x, y);
  });
  const buf = await m.getBufferAsync(Jimp.MIME_PNG);
  const svg = await new Promise((res, rej) => potrace.trace(buf, { turdSize: 20, optTolerance: 0.4, threshold: 128 }, (e, s) => e ? rej(e) : res(s)));
  return (svg.match(/ d="([^"]+)"/) || [])[1];
}
module.exports = { traceMask };
