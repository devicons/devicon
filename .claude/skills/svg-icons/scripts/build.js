// Builds devicon versions (original, plain, line and their wordmarks) from an
// official logo SVG, following the wiki: viewBox 0 0 128 128, no padding,
// centred; plain/line = one united path in one colour, no strokes/gradients.
const paper = require('./paperenv');
const { PaperOffset } = paper;

const isPath = it => it instanceof paper.Path || it instanceof paper.CompoundPath;

function colorOf(c) {
  if (!c) return null;
  if (c.gradient) { // average of the stops
    const st = c.gradient.stops, n = st.length;
    return new paper.Color(st.reduce((a, s) => a + s.color.red, 0) / n, st.reduce((a, s) => a + s.color.green, 0) / n, st.reduce((a, s) => a + s.color.blue, 0) / n);
  }
  return c;
}

// Visible shapes in paint order, as global-coordinate paths with a colour.
function leaves(svg) {
  // paper ignores <style> rules: inline them as attributes first
  svg = require('svgo').optimize(svg, { plugins: [
    { name: 'inlineStyles', params: { onlyMatchedOnce: false } }, 'convertStyleToAttrs', 'removeTitle', 'removeDesc',
    'removeMetadata', 'removeEditorsNSData', 'removeXMLProcInst', 'removeComments', 'convertShapeToPath'] }).data;
  // paper can't parse compact arc flags ("a1 1 0 0130 4"): turn arcs into curves
  const svgpath = require('svgpath');
  svg = svg.replace(/(\sd=")([^"]*)"/g, (m, a, d) => a + svgpath(d).unarc().abs().toString() + '"');
  // a rect with only rx (or ry) has round corners per the spec; paper reads the
  // missing one as 0 and draws square corners
  svg = svg.replace(/<rect\b[^>]*>/g, t => {
    const rx = t.match(/\srx="([^"]*)"/), ry = t.match(/\sry="([^"]*)"/);
    return rx && !ry ? t.replace(/\s?\/?>$/, m => ` ry="${rx[1]}"${m}`) : ry && !rx ? t.replace(/\s?\/?>$/, m => ` rx="${ry[1]}"${m}`) : t;
  });
  // SVG's default fill is black, but paper leaves unfilled shapes empty
  svg = svg.replace(/<svg\b([^>]*)>/, (m, a) => /\sfill=/.test(a) ? m : `<svg${a} fill="#000">`);
  paper.project.clear();
  const root = paper.project.importSVG(svg, { expandShapes: true });
  const out = [];
  const walk = (item, clip) => {
    if (!item.visible || item.opacity === 0) return;
    if (item.className === 'Group' || item.className === 'Layer') {
      let mask = clip;
      const kids = item.children.slice();
      if (item.clipped && kids.length && isPath(kids[0])) {
        const m = kids[0].clone({ insert: false });
        m.transform(kids[0].parent.globalMatrix);
        mask = clip ? clip.intersect(m, { insert: false }) : m;
        kids.shift();
      }
      kids.forEach(k => walk(k, mask));
      return;
    }
    if (!isPath(item) || item.clipMask) return;
    const base = item.clone({ insert: false });
    base.transform(item.parent.globalMatrix);
    const add = (p, color) => {
      p.fillColor = color; p.strokeColor = null;
      if (clip) { const f = p.fillColor; p = p.intersect(clip, { insert: false }); p.fillColor = f; }
      if (!p.isEmpty() && Math.abs(p.area) > 0.01) out.push({ path: p, color, raw: color, src: item });
    };
    const fill = item.fillColor;
    if (fill && fill.alpha !== 0) add(base.clone({ insert: false }), fill);
    if (item.strokeColor && item.strokeWidth > 0 && item.strokeColor.alpha !== 0) {
      const w = item.strokeWidth * Math.sqrt(Math.abs(item.parent.globalMatrix.scaling.x * item.parent.globalMatrix.scaling.y));
      const s = PaperOffset.offsetStroke(base, w / 2, { cap: item.strokeCap || 'butt', join: item.strokeJoin || 'miter', insert: false });
      add(s, item.strokeColor);
    }
  };
  walk(root, null);
  return out;
}

const isWhite = c => { const k = colorOf(c); return k && k.red > 0.94 && k.green > 0.94 && k.blue > 0.94; };
const hex = c => colorOf(c).toCSS(true);

function unionAll(paths) {
  let r = null;
  for (const p of paths) r = r ? r.unite(p, { insert: false }) : p.clone({ insert: false });
  return r;
}

// Matrix that fits `bounds` into the 128x128 box, centred, largest side = 128.
function fitMatrix(b) {
  const s = 128 / Math.max(b.width, b.height);
  return new paper.Matrix().translate(64, 64).scale(s).translate(-b.center.x, -b.center.y);
}

// opts: select(leaf, i) -> keep?, cutout(leaf, i) -> is a hole?, gap (in 128 units), color
function plainPath(ls, opts = {}) {
  let res = null, below = [];
  ls.forEach((l, i) => {
    const hole = opts.cutout ? opts.cutout(l, i) : isWhite(l.color);
    if (hole) { if (res) res = res.subtract(l.path, { insert: false }); return; }
    if (res && opts.gap) {
      // keep a gap where this shape covers a shape of another colour
      const differs = below.some(b => hex(b.color) !== hex(l.color) && b.path.intersects(l.path) || b.path.bounds.intersects(l.path.bounds) && hex(b.color) !== hex(l.color));
      if (differs) {
        const grown = PaperOffset.offset(l.path, opts.gap, { join: 'round', insert: false });
        res = res.subtract(grown, { insert: false });
      }
    }
    res = res ? res.unite(l.path, { insert: false }) : l.path.clone({ insert: false });
    below.push(l);
  });
  // cutting gaps at an angle leaves thin slivers and sharp spikes; shrink then
  // grow back with round joins to remove them (corners get a ~1 unit radius)
  if (opts.gap) {
    const inner = PaperOffset.offset(res, -1, { join: 'round', insert: false });
    res = PaperOffset.offset(inner, 1, { join: 'round', insert: false });
  }
  return res;
}

function prominent(ls) {
  const area = {};
  for (const l of ls) if (!isWhite(l.color)) { const h = hex(l.color); area[h] = (area[h] || 0) + Math.abs(l.path.area); }
  return Object.entries(area).sort((a, b) => b[1] - a[1])[0][0];
}

// Split a (compound) path into islands: each outer contour with the holes inside it.
function islands(p) {
  // winding in source files is unreliable: reorient from the actual nesting
  // (outer contours clockwise, holes counter-clockwise) before splitting
  p = p.clone({ insert: false });
  p.reorient(true, true);
  const kids = p instanceof paper.CompoundPath ? p.children.map(c => c.clone({ insert: false })) : [p.clone({ insert: false })];
  const outers = kids.filter(k => k.clockwise);
  const holes = kids.filter(k => !k.clockwise);
  return outers.map(o => {
    const mine = holes.filter(h => o.contains(h.interiorPoint));
    return mine.length ? new paper.CompoundPath({ children: [o, ...mine], insert: false }) : o;
  });
}

// Outline of a plain shape, `width` wide, inside the shape. Parts too thin to
// have an inside (thin bars, small dots) stay solid instead of disappearing.
function linePath(plain, width) {
  let out = null;
  for (const isl of islands(plain)) {
    const inner = PaperOffset.offset(isl, -width, { join: 'miter', insert: false });
    const thin = !inner || inner.isEmpty() || Math.abs(inner.area) < width * width || !isl.bounds.contains(inner.bounds);
    const part = thin ? isl : isl.subtract(inner, { insert: false });
    out = out ? out.unite(part, { insert: false }) : part;
  }
  return out || plain;
}

const svgDoc = body => `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128">${body}</svg>`;
function pathSvg(p, color) {
  p = p.clone({ insert: false });
  p.reorient(true, true);
  const d = p.pathData;
  return svgDoc(`<path fill="${color}" d="${d}"/>`);
}

// paper.js wraps exports in one <g> holding inherited attributes (fill-rule,
// fill="none", font-*="none"). Move them onto the children and drop the group:
// reviewers ask for ungrouped paths, and SVGO only collapses attribute-free groups.
function ungroup(svg) {
  // exports with gradients come as <svg><svg><defs/><g>...</g></svg></svg>
  svg = svg.trim().replace(/^(<svg\b[^>]*>)<svg>([\s\S]*)<\/svg><\/svg>$/, '$1$2</svg>')
    .replace(/\sfill-rule="none"/g, ''); // not a valid value
  const m = svg.match(/^(<svg\b[^>]*>(?:<defs>[\s\S]*?<\/defs>)?)<g\b([^>]*)>([\s\S]*)<\/g><\/svg>$/);
  if (!m || /<g\b/.test(m[3])) return svg;
  const attrs = [...m[2].matchAll(/\s([\w:-]+)="([^"]*)"/g)];
  const body = m[3].replace(/<(\w+)\b((?:[^>"]|"[^"]*")*?)(\/?)>/g, (t, tag, a, close) => {
    for (const [, k, v] of attrs) if (!new RegExp(`\\s${k}="`).test(a)) a += ` ${k}="${v}"`;
    return `<${tag}${a}${close}>`;
  });
  return `${m[1]}${body}</svg>`;
}

// SVGO (as the wiki asks), keeping ids readable for the file-name prefix
function optimize(svg) {
  // paper.js export leftovers that SVGO keeps: no-op styles and zero-width strokes
  svg = svg.replace(/\sstyle="mix-blend-mode:\s*normal;?"/g, '')
    .replace(/\s(font-family|font-size|font-weight|text-anchor)="none"/g, '')
    .replace(/\s(stroke-width="0"|stroke-miterlimit="[^"]*"|stroke="none"|fill-rule="nonzero"|stroke-dasharray="none")/g, '');
  svg = ungroup(svg);
  return require('svgo').optimize(svg, { multipass: true, floatPrecision: 2,
    plugins: [{ name: 'preset-default', params: { overrides: { cleanupIds: { minify: true } } } }] }).data;
}

// Prefix ids with the file name (same rule as the check-bot/build)
function prefixIds(svg, prefix) {
  const ids = [...new Set([...svg.matchAll(/\sid="([^"]+)"/g)].map(m => m[1]))].filter(i => !i.startsWith(prefix + '-'));
  for (const id of ids) {
    const to = `${prefix}-${id}`;
    svg = svg.split(` id="${id}"`).join(` id="${to}"`)
      .split(`url(#${id})`).join(`url(#${to})`)
      .split(`href="#${id}"`).join(`href="#${to}"`);
  }
  return svg;
}

// opts.select(leaf, i): which shapes belong to this version (for lockups that
// hold both the logo and the wordmark). Returns { original, plain, line, color }.
function build(svg, opts = {}) {
  const ls = leaves(svg).filter((l, i) => !opts.select || opts.select(l, i));
  if (opts.recolor) ls.forEach((l, i) => { const c = opts.recolor(l, i); if (c) l.path.fillColor = l.color = new paper.Color(c); });
  const m0 = fitMatrix(unionAll(ls.map(l => l.path)).bounds);
  const ls128 = ls.map(l => { const p = l.path.clone({ insert: false }); p.transform(m0); return { ...l, path: p }; });
  const color = opts.color || prominent(ls128);
  const res = { color, count: ls.length };

  // original: every shape with its own fill (gradients included)
  paper.project.clear();
  const g = new paper.Group(ls128.map(l => l.path.clone()));
  res.original = optimize(svgDoc(g.exportSVG({ asString: true, precision: 3 }).replace(/ xmlns="[^"]*"/g, '')));

  // plain: one path, one colour; line: inner outline of plain
  let plain = plainPath(ls128, opts);
  plain.transform(fitMatrix(plain.bounds));
  res.plain = optimize(pathSvg(plain, color));
  if (opts.line !== false) res.line = optimize(pathSvg(linePath(plain, opts.lineWidth || 4), color));
  return res;
}

module.exports = { paper, leaves, build, plainPath, linePath, pathSvg, optimize, ungroup, prefixIds, fitMatrix, unionAll, isWhite, hex, svgDoc };
