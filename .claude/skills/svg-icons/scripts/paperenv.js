// Loads paper.js in a jsdom window with a stub canvas: boolean ops, offsets and
// SVG import/export don't need real drawing.
const { JSDOM } = require('jsdom');
const dom = new JSDOM('<!doctype html><html><body></body></html>', { pretendToBeVisual: true });
const w = dom.window;
w.HTMLCanvasElement.prototype.getContext = function () {
  const canvas = this;
  return new Proxy({}, { get: (t, p) => p === 'canvas' ? canvas : (p in t ? t[p] : () => ({ width: 0, data: [] })), set: (t, p, v) => (t[p] = v, true) });
};
for (const k of ['window', 'document', 'navigator', 'self', 'HTMLCanvasElement', 'Image', 'DOMParser', 'XMLSerializer', 'Node'])
  if (!(k in global) || k === 'window' || k === 'self') global[k] = k === 'window' || k === 'self' ? w : w[k];
const paper = require('paper/dist/paper-core.js');
paper.setup(new paper.Size(128, 128));
module.exports = paper;
// paperjs-offset requires 'paper' itself; make that our instance
const Module = require('module');
const key = require.resolve('paper');
const m = new Module(key); m.filename = key; m.loaded = true; m.exports = paper;
require.cache[key] = m;
paper.PaperOffset = require('paperjs-offset').PaperOffset;
