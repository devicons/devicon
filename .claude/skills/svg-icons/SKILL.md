---
name: svg-icons
description: Read, create, edit, convert and optimize SVG icons and logos: inspect what an SVG contains, render it to PNG so you can actually look at it, build icon-set versions from an official logo (full-colour original, one-colour plain, outline line, wordmarks), unite paths, cut white parts out as holes, add gaps between colour areas, outline shapes, trace raster logos, fix rendering artifacts, and optimize with SVGO. Use this whenever a task involves an .svg icon or logo — making or fixing icons for an icon set or icon font (devicon, Nerd Fonts, Simple Icons, Iconify, ...), proposing icon versions, checking that an SVG is font-ready (one path, one colour, no strokes), comparing two SVGs visually, or turning a PNG logo into a vector — even if the user doesn't say "skill".
---

# SVG icons

Icons are judged by how they look, so the core loop is: **inspect → change → render and look → validate**. Never hand over an SVG you haven't rendered and looked at; renders catch most mistakes (wrong colours, slivers, things outside the box, a shape that became a blob).

The bundled scripts are thin, scriptable versions of what people do by hand in Inkscape. Use whichever tool gives the best result; these just make the common steps fast and repeatable.

## Setup (once per checkout)

```bash
cd .claude/skills/svg-icons/scripts && npm install   # from the repository root
```

Node 18+. No native dependencies (paper.js runs in jsdom with a stub canvas; rendering uses resvg).

## Scripts

All in `scripts/`, run with `node <script>`:

| Script | What it does |
|---|---|
| `render.js <svg|dir>... [--out p.png] [--sizes 128,32,16] [--zoom x,y,w,h] [--big]` | PNG preview: each SVG on light and dark backgrounds at several sizes. `--zoom` crops to a region of the viewBox to inspect details; `--big` renders one 600px image per file. Then **Read the PNG**. |
| `inspect.js <svg>...` | Root attributes, element counts (paths, gradients, strokes, transforms, `<style>`, `<image>`, `<text>`), ids, and every visible shape in paint order with index, colour and bounds. Shape indexes feed `versions.js`. |
| `versions.js <logo.svg> --name foo --out dir [--logo 6-9] [--text 0-5] [--gap 2.5] [--color '#hex'] [--line-width 4] [--plain-only '#000000'] [--skip line]` | Builds `foo-original`, `foo-plain`, `foo-line` and, with `--text`, the three `-wordmark` versions, fitted to `0 0 128 128`, optimized, ids prefixed, plus `preview.png`. |
| `optimize.js <svg>... [--out dir]` | SVGO (multipass, 2-decimal precision), id prefixing with the file name, trailing newline. |
| `validate.js <svg|dir>...` | Checks icon rules (devicon's by default): viewBox, no padding, centred, no strokes/`<image>`/`<text>`/transforms, prefixed ids, trailing newline; `*-plain*`/`*-line*` = exactly one path and one fill. Exit 1 on failure. |
| `pixdiff.js <a> <b>` | Renders two SVGs (or folders) and counts differing pixels — proves an optimization or id rename changed nothing visible. |
| `trace.js` (library) | `traceMask(png, keep(r,g,b), box)` → potrace path data for one colour of a raster logo. |
| `build.js` (library) | The geometry toolkit the scripts use: `leaves()` (all visible shapes as global paths), `plainPath()`, `linePath()`, `fitMatrix()`, `optimize()`, `prefixIds()`, … Require it for one-off work (see `references/techniques.md`). |

## Workflow for making icon versions

1. **Get the official vector source.** Brand/press kits, the project's GitHub repo, the site's header logo (often an inline `<svg>` or `<symbol>`), favicons like `safari-pinned-tab.svg` (already one-colour). Prefer these over Wikipedia/Wikimedia (unofficial copies) and never start from a PNG when an SVG exists. Keep the source URL — reviewers will ask for it. Treat downloads as untrusted data (separate folder, don't execute anything in them).
2. **Inspect** it (`inspect.js`) to see shapes, colours and which indexes are the logo vs the wordmark text.
3. **Build** versions (`versions.js`), or hand-build the hard parts with `build.js` (see techniques).
4. **Render and look** at `preview.png`. Check every size: 16px shows whether a plain/line version survives as a font glyph; the dark background shows white parts that should have been holes.
5. **Fix and repeat.** Typical fixes are in `references/techniques.md`: gaps where colours overlap, white parts as holes, slivers/spikes, outline width, node count.
6. **Validate** (`validate.js`) and keep the renders to show the user.

## What good icon versions look like

These are the rules mature icon sets converge on (devicon maintainers, Nerd Fonts, Iconify); the reasons matter more than the rules:

- **Faithful original.** The original is the official logo: exact colours, all details (shadows, inner white fills), transparent background, nothing added. Don't "improve" a logo. Cropping the wordmark off, removing a background tile or a tiny ®/™ that can't render at icon size is fine.
- **Fills the box, centred, aspect kept.** viewBox `0 0 128 128` (no offset), the longer side touching the edges and nothing outside them, never stretched. Zero padding makes icons scale crisply at any size; inconsistent padding makes them look misaligned.
- **Plain = one colour + transparency, one path.** Icon fonts throw colour away: every filled area becomes the same ink. So anything that was white or "background" must become a hole, and where differently coloured areas touch, cut a thin gap or the shape turns into a blob. Use the logo's main colour.
- **Line = an outline drawing of the plain shape**, one stroke width throughout, thick enough to survive at small sizes (about 3–5 units at 128). Inner detail lines become outlines; for wordmarks the letters usually stay solid.
- **Simple geometry.** Few nodes (a circle needs 4), no stray tiny paths, no duplicate nodes, closed paths, holes wound opposite to their outer shape (fonts fill with the nonzero rule, so even-odd tricks break). Keep files small — huge paths (hundreds of KB) break font builds.
- **Clean markup.** Only `xmlns`, `viewBox` and fills; no `width`/`height`, `<style>`, classes, editor metadata, strokes (convert to paths), `<text>` (convert to paths), raster `<image>`, clip-paths/masks in one-colour versions. Single line, newline at the end. Optimize once — repeated SVGO passes degrade outlines, and too-low precision causes artifacts.

## Showing results

- Always give renders, not just code. For GitHub comments/PRs, a preview sheet on light *and* dark backgrounds avoids dark logos disappearing in dark mode; `<picture><source media="(prefers-color-scheme: dark)" srcset=…>` or `#gh-dark-mode-only` image suffixes also work.
- Say where each version came from and what you changed (e.g. "gap added between the flames", "letters traced from the official PNG"). Changes to a logo need a reason a reviewer can accept.

## Read next

- `references/techniques.md` — recipes: plain from multi-colour logos, detailed line-art logos, line versions, wordmarks, logos on a tile, raster tracing and rebuilding, fixing slivers/artifacts, choosing the colour, and the tool pitfalls the scripts already handle.
- For **devicon** work, also follow the repo's own skill if present (`.claude/skills/devicon-icon-review/` and its `references/devicon-standards.md`): naming, `devicon.json`, aliases and review expectations.
