# Techniques and recipes

Contents
1. Using build.js directly
2. Plain versions from multi-colour logos
3. Detailed line-art and mascot logos
4. Line versions
5. Wordmarks and lockups
6. Logos on a tile or background
7. Raster-only logos
8. Fixing artifacts
9. Choosing the colour
10. Pitfalls the scripts already handle

## 1. Using build.js directly

`versions.js` covers the common case. For anything custom, write a small script:

```js
const B = require('<repo>/.claude/skills/svg-icons/scripts/build');  // use the absolute path
const { paper } = B; const { PaperOffset } = paper;
const ls = B.leaves(svgString);            // visible shapes in paint order: { path, color, raw, src }
const m = B.fitMatrix(B.unionAll(ls.map(l => l.path)).bounds);   // fit to 128, centred
const P = i => { const p = ls[i].path.clone({ insert: false }); p.transform(m); return p; };
let plain = B.unionAll([P(0), P(1)]).subtract(P(2), { insert: false });   // boolean ops
const ring = PaperOffset.offsetStroke(P(3), 1.2, { insert: false });      // outline band (stroke→path)
const inset = PaperOffset.offset(P(3), -1.5, { insert: false });          // grow (+) / shrink (−)
plain.transform(B.fitMatrix(plain.bounds));
fs.writeFileSync('x-plain.svg', B.prefixIds(B.optimize(B.pathSvg(plain, '#ff0000')), 'x-plain') + '\n');
```

Work in 128-unit space (transform first) so gap and line widths mean the same thing in every icon.

## 2. Plain versions from multi-colour logos

Goal: the same silhouette and the same recognisable inner structure, in one colour.

- **White or background-coloured parts → holes.** `plainPath()` does this by default (shapes that are ~white subtract). If a logo's "white" is meant as ink (rare), pass a custom `cutout`.
- **Colour boundaries → gaps.** With `--gap 2–3` (128 units), every shape drawn over a differently coloured shape first cuts a gap around itself. That's how overlapping flames, diamond facets or two slabs stay distinguishable. Without gaps, overlapping colours merge into a blob.
- **When adjacent same-coloured parts should stay separate**, union them; when a part is decorative shading (gradients, shadow wedges), drop it rather than let it distort the silhouette.
- **Shading in the original as separate shapes** (lighter/darker halves of a cylinder, highlights) should usually be unioned, with only the *structural* lines (bands, rims) kept as gaps. Hand-build these: union the body, subtract the bands, cut a thin ring along rims.
- If no plain version can be made that reads well, a **line** version can serve as the font version instead (devicon accepts original + line).

## 3. Detailed line-art and mascot logos

Cartoon logos (black outlines around coloured areas) are the hardest. Options, best first:

- **Inner lines become transparent gaps, outer outline merges with the shape** (Finii's rule): a black line with filled area on *both* sides becomes a gap; a line with area on one side and nothing on the other becomes part of the silhouette. Result: a solid silhouette with the drawing's inner structure cut into it.
- **Silhouette only** (union everything non-white): readable at 16px but loses features.
- **The black linework alone** as a `line` version: faithful, but often too thin for small sizes.

Simplify: remove tiny details that vanish at 32px, merge near-duplicate lines, and keep the node count down. Compare with how the project itself shows the logo small (favicon, app icon) — that's often the best guide to an acceptable simplification.

## 4. Line versions

- `linePath(plain, w)` = plain minus plain inset by `w`: an inner outline that keeps the outer size exact. Use `w` ≈ 3.5–4.5 at 128 for icons; for wordmark lockups scale `w` with the logo's size so it matches the icon version.
- Keep one stroke width everywhere. Very different widths (thin outside, fat inside) read as two styles.
- Holes in the plain shape get outlined too (letters cut out of a badge become outlined letters) — check that this still reads.
- Alternative for organic shapes: render the plain shape large, centre-line trace it, stroke the centre lines with round caps/joins, and convert stroke to path.
- Letters in `line-wordmark` usually stay solid; outlined (hollow) text is optional and only works when letters are large.

## 5. Wordmarks and lockups

- A wordmark version is the logo **with the technology's name**. A logo that is only letters (e.g. "Nx", "p5*") is just the original; create aliases for the wordmark names if the icon set wants them.
- Lockup files often contain icon + text (and sometimes a tagline like "from Salesforce"): select shapes by index (`inspect.js` bounds tell you which is which) and leave out taglines unless the official wordmark includes them.
- Keep the official spacing between icon and text; don't rearrange a horizontal lockup into a stacked one unless the brand provides one.

## 6. Logos on a tile or background

If the logo is a symbol on a coloured tile (app-icon style), the original keeps the tile. For plain, keep the tile and cut the symbol out of it (the plain icon then looks like the original on a dark background) — or, if the brand uses the bare symbol, use that. Don't fill a transparent area with a background colour; users choose their own background.

## 7. Raster-only logos

1. Look harder for a vector first: the project's repo (`docs/`, `assets/`, `branding/`), site header (inline SVG/`<symbol>`), favicon SVGs, press kits, older releases.
2. **Simple geometry** (circles, bars, rounded rectangles): rebuild it exactly. Measure from the image — fit circles to edge pixels, take bounding boxes of symbols, sample flat colours away from edges — and draw clean shapes. Far better than tracing.
3. **Organic shapes or letters**: trace per colour with `trace.js` (`traceMask(png, (r,g,b) => <colour test>, [x0,y0,x1,y1])`), use `fill-rule="evenodd"` on traced paths (potrace holes), then snap colours to the logo's real values. Online tracers (vectorizer.ai, "group paths by colour") work well too; afterwards remove stray outlines/backgrounds and snap the palette.
4. Say clearly that the result is traced/rebuilt and from which file.

## 8. Fixing artifacts

- **Slivers and spikes** after cutting gaps at an angle: morphological opening — shrink by ~1 unit and grow back with round joins (`plainPath` does this whenever `gap` is set). Look at zoomed renders (`render.js --zoom`) of every acute corner.
- **Filled gaps / missing holes in the font** but not in the SVG: winding direction. `pathSvg()` reorients (outer clockwise, holes counter-clockwise); for hand-made paths, reorient before export.
- **Artifacts only after optimization**: precision too low or path compression the font tool misreads. Re-optimize from the unoptimized file with more precision (3–4 decimals) or without `convertPathData`, then re-check the font preview.
- **Stray "smudges"**: tiny paths or 3-node blobs left from tracing/merging. Inspect shapes by area (`inspect.js`) and delete the tiny ones.
- **Duplicate nodes at the same coordinates**: usually harmless; breaking apart and recombining paths removes most.
- **Something outside the box**: re-fit with `fitMatrix` on the true bounds; check that no shape (including invisible ones) extends the bounds.

## 9. Choosing the colour

The main colour of the logo, unless the brand guidelines name a primary colour. For gradients take the dominant/middle colour of the gradient; for multi-colour logos the colour with the largest area or the one the brand uses most on its site. Avoid white (invisible on light backgrounds) for one-colour versions; a black logo is `#000000`. The colour must actually appear in the logo.

## 10. Pitfalls the scripts already handle

Know these when working outside the scripts:

- paper.js ignores `<style>` rules → inline styles first (SVGO `inlineStyles` + `convertStyleToAttrs`).
- Compact arc flags (`a1 1 0 0130 4`) break paper's parser → normalise paths with `svgpath(d).unarc().abs()`.
- SVG's default fill is black, but paper leaves unfilled shapes empty → set `fill="#000"` on the root when missing.
- Paper's `exportSVG` of a shape that still has a gradient returns a group → use `path.pathData` for single paths.
- Reading text files on Windows with Node keeps CRLF, Python's `read_text` translates it → open with `newline=""` when preserving line endings matters.
- Inkscape-exported SVGs carry metadata, `sodipodi:*` attributes and `xml:space` → SVGO removes them.
