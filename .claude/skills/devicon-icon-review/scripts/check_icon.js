// Checks one devicon icon (its devicon.json entry and icons/<name>/ files)
// against the standards in references/devicon-standards.md. No dependencies.
//   node check_icon.js <name> [--repo path-to-devicon-checkout]
// Prints ERROR / WARN / NOTE lines; exit code 1 if there are errors.
// Geometry (padding, centring, outside the box) needs the svg-icons skill:
//   node .claude/skills/svg-icons/scripts/validate.js <repo>/icons/<name>
const fs = require('fs'), path = require('path');

const args = process.argv.slice(2);
const ri = args.indexOf('--repo');
const repo = ri >= 0 ? args.splice(ri, 2)[1] : process.cwd();
const name = args[0];
if (!name) { console.error('usage: node check_icon.js <name> [--repo path]'); process.exit(2); }

const out = { ERROR: [], WARN: [], NOTE: [] };
const err = m => out.ERROR.push(m), warn = m => out.WARN.push(m), note = m => out.NOTE.push(m);
const ORDER = ['original', 'original-wordmark', 'plain', 'plain-wordmark', 'line', 'line-wordmark'];
const hex6 = c => { c = c.toLowerCase(); return /^#[0-9a-f]{3}$/.test(c) ? '#' + [...c.slice(1)].map(x => x + x).join('') : c; };

// --- devicon.json ---
let all;
try { all = JSON.parse(fs.readFileSync(path.join(repo, 'devicon.json'), 'utf8')); }
catch (e) { console.log(`ERROR devicon.json does not parse: ${e.message}`); process.exit(1); }
const names = all.map(x => x.name);
const i = names.indexOf(name);
const entry = all[i];
if (!entry) { console.log(`ERROR no devicon.json entry named "${name}"`); process.exit(1); }
if (!(i === 0 || names[i - 1] < name) || !(i === names.length - 1 || name < names[i + 1]))
  err(`devicon.json: "${name}" is not in alphabetical order (between "${names[i - 1]}" and "${names[i + 1]}")`);
const unsorted = names.findIndex((n, k) => k && names[k - 1] > n);
if (unsorted > 0 && names[unsorted] !== name && names[unsorted - 1] !== name)
  note(`devicon.json is unsorted elsewhere ("${names[unsorted - 1]}" before "${names[unsorted]}"); the check-bot will fail every PR until that's fixed`);

for (const k of ['name', 'altnames', 'tags', 'versions', 'color', 'aliases']) if (!(k in entry)) err(`devicon.json: missing "${k}"`);
const extra = Object.keys(entry).filter(k => !['name', 'altnames', 'tags', 'versions', 'color', 'aliases'].includes(k));
if (extra.length) err(`devicon.json: unknown keys ${extra.join(', ')}`);
if (!/^[a-z0-9]+$/.test(name)) warn(`name "${name}" should be lowercase letters/digits only (see Naming Conventions)`);
if ((entry.altnames || []).includes(name)) err('altnames repeats the name');
if (!Array.isArray(entry.tags) || !entry.tags.length) warn('tags should be a non-empty array of strings');
const svgV = entry.versions?.svg || [], fontV = entry.versions?.font || [];
for (const v of [...svgV, ...fontV]) if (!ORDER.includes(v)) err(`invalid version name "${v}" (allowed: ${ORDER.join(', ')})`);
const inOrder = list => list.every((v, k) => !k || ORDER.indexOf(list[k - 1]) < ORDER.indexOf(v));
if (!inOrder(svgV)) warn(`versions.svg is not in the usual order (${ORDER.join(', ')})`);
if (!inOrder(fontV)) warn('versions.font is not in the usual order');
if (new Set(svgV).size !== svgV.length || new Set(fontV).size !== fontV.length) err('duplicate entries in versions');
for (const v of fontV) if (!svgV.includes(v)) err(`versions.font has "${v}" but versions.svg doesn't (font versions must be existing SVG files)`);
if (!svgV.includes('original')) err('there is no original version: every icon needs one (a one-colour logo is "original" plus an alias to "plain")');
if (!fontV.length) err('versions.font is empty: at least one font-ready version (plain, line, or a qualifying original) is required');
if (fontV.includes('original') && fontV.includes('plain')) warn('both original and plain are font versions: if plain is just the original in one colour, remove it and alias instead');
if (!/^#[0-9a-fA-F]{3}([0-9a-fA-F]{3})?$/.test(entry.color || '')) err(`color "${entry.color}" must be "#rgb" or "#rrggbb"`);
else if (/^#fff(fff)?$/i.test(entry.color)) warn('color is white: invisible on light backgrounds; use the logo\'s main non-white colour');
const short = c => c.replace(/^#([0-9a-f])\1([0-9a-f])\2([0-9a-f])\3$/i, '#$1$2$3');
if (entry.color && short(entry.color) !== entry.color) warn(`color "${entry.color}" can be shortened to "${short(entry.color)}"`);

const validAlias = a => a !== null && typeof a === 'object' && !Array.isArray(a) && typeof a.base === 'string' && typeof a.alias === 'string';
const aliases = (entry.aliases || []).filter(a => { if (validAlias(a)) return true; err(`alias ${JSON.stringify(a)} must be an object {"base": "...", "alias": "..."}`); return false; });
const aliasNames = new Set();
for (const a of aliases) {
  if (!ORDER.includes(a.base) || !ORDER.includes(a.alias)) err(`alias ${a.base} -> ${a.alias}: invalid version name`);
  if (a.base === a.alias) err(`alias ${a.base} -> ${a.alias}: base and alias are the same`);
  if (!svgV.includes(a.base)) err(`alias base "${a.base}" is not an existing SVG version`);
  else if (!fontV.includes(a.base)) err(`alias base "${a.base}" is not a font version: aliases only work for font versions`);
  // an SVG file may share the alias name (e.g. a multi-colour original aliased
  // to plain for the font); only a font version of that name would clash
  if (fontV.includes(a.alias)) err(`alias "${a.alias}" is also a font version: the font would get that class twice`);
  if (aliasNames.has(a.alias)) err(`alias "${a.alias}" defined twice`);
  aliasNames.add(a.alias);
  const style = v => v.split('-')[0];
  if (style(a.base) === 'line' && style(a.alias) !== 'line' || style(a.base) !== 'line' && style(a.alias) === 'line' && style(a.base) !== 'original')
    warn(`alias ${a.base} -> ${a.alias} crosses styles (plain and line look different)`);
  if (!a.base.endsWith('wordmark') && a.alias.endsWith('wordmark')) note(`alias ${a.base} -> ${a.alias}: only valid if the ${a.base} logo contains the technology's name`);
}

// Font versions may only contain <svg xmlns viewBox> with one <path d fill>:
// everything else (groups, other shapes, defs/use, styles, opacity, fill-rule,
// transforms, ...) is lost or misread by the font build. Returns the problems.
function fontMarkupProblems(s) {
  const tags = [...s.matchAll(/<([a-zA-Z][\w:-]*)\b([^>]*?)\/?>/g)].map(m => ({ name: m[1], attrs: [...m[2].matchAll(/([\w:-]+)\s*=/g)].map(a => a[1]) }));
  const p = [];
  const extra = tags.filter(t => t.name !== 'svg' && t.name !== 'path').map(t => `<${t.name}>`);
  const paths = tags.filter(t => t.name === 'path');
  if (paths.length !== 1) p.push(`${paths.length} <path> elements (exactly 1 allowed)`);
  else if (!/<path\b[^>]*\sd="[^"]*[0-9][^"]*"/.test(s)) p.push('a <path> without path data (renders nothing)');
  if (extra.length) p.push(`other elements: ${[...new Set(extra)].join(', ')}`);
  const bad = (t, ok) => t.attrs.filter(a => !ok.includes(a));
  const svgExtra = tags.filter(t => t.name === 'svg').flatMap(t => bad(t, ['xmlns', 'viewBox']));
  const pathExtra = paths.flatMap(t => bad(t, ['d', 'fill']));
  if (svgExtra.length) p.push(`<svg> attributes besides xmlns/viewBox: ${svgExtra.join(', ')}`);
  if (pathExtra.length) p.push(`<path> attributes besides d/fill: ${pathExtra.join(', ')}`);
  if (/<(?!\/?(svg|path)\b)[!?]/.test(s)) p.push('comments, doctype or XML declaration');
  const fill = (s.match(/<path\b[^>]*\sfill="([^"]*)"/) || [])[1];
  if (fill !== undefined && !/^#[0-9a-fA-F]{3}([0-9a-fA-F]{3})?$/.test(fill)) p.push(`fill="${fill}" (needs a #hex colour)`);
  return p;
}

// --- files ---
const dir = path.join(repo, 'icons', name);
const files = fs.existsSync(dir) ? fs.readdirSync(dir) : [];
if (!files.length) err(`icons/${name}/ is missing or empty`);
for (const f of files) {
  if (f.endsWith('.eps')) continue;
  const m = f.match(new RegExp(`^${name}-(.+)\\.svg$`));
  if (!m || !ORDER.includes(m[1])) err(`icons/${name}/${f}: file name must be ${name}-<version>.svg`);
  else if (!svgV.includes(m[1])) err(`icons/${name}/${f} is not listed in versions.svg`);
}
for (const v of svgV) if (!files.includes(`${name}-${v}.svg`)) err(`versions.svg lists "${v}" but icons/${name}/${name}-${v}.svg doesn't exist`);

const colour = hex6(entry.color || '');
let colourSeen = false;
for (const v of svgV) {
  const f = path.join(dir, `${name}-${v}.svg`);
  if (!fs.existsSync(f)) continue;
  const s = fs.readFileSync(f, 'utf8'), rel = `${name}-${v}.svg`, root = (s.match(/<svg\b[^>]*>/) || [''])[0];
  const isFont = fontV.includes(v) || aliases.some(a => a.base === v);
  if (!/viewBox="0 0 128 128"/.test(root)) err(`${rel}: viewBox must be exactly "0 0 128 128" (found ${(root.match(/viewBox="[^"]*"/) || ['none'])[0]})`);
  if (/\s(width|height)="/.test(root)) err(`${rel}: remove width/height from <svg>`);
  if (!/xmlns="http:\/\/www\.w3\.org\/2000\/svg"/.test(root)) err(`${rel}: missing xmlns (the SVG won't display as an image)`);
  if (/<image\b/i.test(s)) err(`${rel}: contains <image> (raster images aren't allowed; use real vector paths)`);
  if (/<text\b/i.test(s)) err(`${rel}: contains <text>; convert text to paths`);
  const stroke = /(^|[\s;"])stroke\s*[=:]\s*"?(?!none|transparent)[#a-z]/i.test(s);
  if (stroke) (isFont ? err : warn)(`${rel}: uses strokes${isFont ? ' (icomoon ignores strokes: convert stroke to path)' : '; convert to paths if possible'}`);
  if (/<style\b|\sclass="/.test(s)) warn(`${rel}: has <style>/classes; inline them as fill attributes`);
  if (/\sstyle="/.test(s)) warn(`${rel}: has style="..." attributes; use plain attributes`);
  if (/transform=/.test(s)) warn(`${rel}: has transforms; bake them into the paths (SVGO does most)`);
  if (/(sodipodi|inkscape):|xml:space|<metadata|data-name=/.test(s)) warn(`${rel}: editor leftovers (sodipodi/inkscape/xml:space/metadata/data-name); optimize with SVGO`);
  const longHex = [...new Set([...s.matchAll(/#[0-9a-f]{6}\b/gi)].map(m => m[0]).filter(c => short(c) !== c))];
  if (longHex.length) warn(`${rel}: shorten ${longHex.join(', ')} to ${longHex.map(short).join(', ')} (SVGO does this)`);
  if (/opacity="(0?\.\d+|0)"/.test(s)) warn(`${rel}: uses opacity; faded paths render wrongly in the font and are usually a tracing leftover`);
  if (s.trimEnd().split('\n').length > 1) warn(`${rel}: should be optimized onto a single line`);
  if (!s.endsWith('\n')) warn(`${rel}: add an empty line at the end of the file`);
  const kb = Buffer.byteLength(s) / 1024;
  if (kb > 40) warn(`${rel}: ${kb.toFixed(0)} KB is very large (99% of devicon SVGs are under ~42 KB); reduce nodes`);
  for (const id of [...s.matchAll(/\sid="([^"]+)"/g)].map(m => m[1])) if (!id.startsWith(`${name}-${v}-`)) { note(`${rel}: id "${id}" isn't prefixed with "${name}-${v}-" (the build prefixes it after merge)`); break; }
  const fills = [...new Set([...s.matchAll(/fill="(#[0-9a-fA-F]{3,6})"/g)].map(m => hex6(m[1])))];
  if (fills.includes(colour)) colourSeen = true;
  const light = c => { const n = parseInt(c.slice(1), 16); return ((n >> 16) & 255) > 225 && ((n >> 8) & 255) > 225 && (n & 255) > 225; };
  if (fills.length && fills.every(light) && !/fill="url\(/.test(s)) warn(`${rel}: only white/near-white fills (${fills.join(', ')}): looks like the logo's variant for dark backgrounds; use the primary (light-background) version`);
  if (isFont) {
    // allowlist: only <svg xmlns viewBox> and one <path d fill>
    for (const m of fontMarkupProblems(s)) err(`${rel}: font versions may only have <svg xmlns viewBox> and one <path d fill>; found ${m}`);
    if (fills.includes('#ffffff')) err(`${rel}: white fill in a font version turns into ink; cut white parts out as holes`);
    if (!fills.length && colour !== '#000000') warn(`${rel}: no fill; expected fill="${entry.color}" (the entry's color)`);
    else if (fills.length === 1 && fills[0] !== colour) warn(`${rel}: fill ${fills[0]} differs from the entry's color ${entry.color}`);
  }
}
if (!colourSeen && colour && colour !== '#000000') warn(`color ${entry.color} doesn't appear in any of the SVGs: use a colour from the logo`);

for (const level of ['ERROR', 'WARN', 'NOTE']) for (const m of out[level]) console.log(`${level.padEnd(5)} ${m}`);
console.log(`${name}: ${out.ERROR.length} errors, ${out.WARN.length} warnings, ${out.NOTE.length} notes`);
process.exit(out.ERROR.length ? 1 : 0);
