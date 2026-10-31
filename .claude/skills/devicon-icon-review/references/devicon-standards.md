# Devicon icon standards

What maintainers and experienced contributors expect from new and updated icons. Distilled from the wiki and from review comments by lunatic-fox, canaleal, Thomas-Boi, amacado, Panquesito7, BenSouchet and weh, plus contributors Finii (Nerd Fonts), cyberalien (Iconify), kilianpaquier, ConX and gewaleelek. Links point to examples. When the wiki and this file disagree, the newer, more specific rule wins; say so in the review.

Contents
1. Is the icon accepted?
2. Source and fidelity
3. Versions and naming
4. SVG file standards
5. Font versions (plain/line, or original used as font)
6. devicon.json
7. Process and PR scope
8. Known disagreements

## 1. Is the icon accepted?

- **A technology, not a company.** Tools, languages, frameworks, services, OSes, servers. Company logos are out of scope (OpenAI, Perforce-the-company, Twilio-as-company); old company icons stay for backward compatibility. A product of a company is fine (AWS yes, Amazon no). See [What Icons Do We Accept?](https://github.com/devicons/devicon/wiki/What-Icons-Do-We-Accept%3F).
- **It helps you work with code**: write, check/transform, test, store/share, build/deploy, or run/host code and services. General-public tools (Word, Discord) aren't accepted; well-known tools of the tech industry are judged case by case.
- **Well-known**, not brand new.
- **It has an official logo.** No official logo → not accepted (REST API, accessibility, Scrum, EJS). Fan-made or meme logos don't count ([#2192](https://github.com/devicons/devicon/pull/2192#issuecomment-2308632887), [#2081](https://github.com/devicons/devicon/issues/2081#issuecomment-2595015572)).
- **Not a component already covered** by an existing icon that uses the same logo (Alertmanager = Prometheus).
- **Brand guidelines allow it.** Some brands forbid the symbol without the wordmark, or a one-colour version (GameMaker, Vaadin plain-wordmark, Elastic). Check and link the guidelines when relevant.
- **Current logo.** If the brand has changed its logo, the PR should use the new one ([VirtualBox closed](https://github.com/devicons/devicon/pull/2279#issuecomment-2525332984)).

## 2. Source and fidelity

- **Use the official vector.** Brand/press kit, the project's GitHub repo, the website's header SVG, official favicons (`safari-pinned-tab.svg` is often a ready one-colour version). Wikimedia copies and icon sites are fallbacks, not sources. Ask for the source link — the PR template requires "Link to prove your SVG is correct and up-to-date".
- **Never a raster**: no `<image>` with base64 PNG/JPG or linked images. A PNG in an SVG wrapper is rejected outright. If only a raster logo exists, trace it carefully (Inkscape Trace Bitmap, vectorizer.ai with paths grouped by colour), snap the palette to the logo's real colours, remove stray outlines/backgrounds ([guide](https://github.com/devicons/devicon/pull/1961#issuecomment-1788123861)).
- **`original` is the exact logo**: official colours (compare hex values with the source), all details (shadows, highlights — [Jenkins](https://github.com/devicons/devicon/pull/1590#discussion_r1091102802), [Power Pages](https://github.com/devicons/devicon/pull/1935#discussion_r1378967391)), inner white fills kept ([CLion](https://github.com/devicons/devicon/pull/1291#discussion_r936652146)), transparent background, nothing added. Don't redesign a logo ([djangorest discussion](https://github.com/devicons/devicon/pull/1407#discussion_r986192431)).
- **Acceptable edits**: crop off the wordmark to get the symbol, remove a background tile, remove ®/™ marks too small to render ([#1298](https://github.com/devicons/devicon/pull/1298#discussion_r929301091), [#1697](https://github.com/devicons/devicon/pull/1697#discussion_r1127683172)), and simplify *plain/line* versions so they read at small sizes.

## 3. Versions and naming

- Versions: `original`, `plain`, `line`, each optionally `-wordmark`. Nothing else (no `-dark`, `-white`, `-horizontal`). Colour variants are never added — users recolour plain icons ([#2239](https://github.com/devicons/devicon/issues/2239), [#973](https://github.com/devicons/devicon/issues/973#issuecomment-997299959)).
- **`original` must always exist** ([#2150](https://github.com/devicons/devicon/pull/2150#discussion_r1498680301), [#2270](https://github.com/devicons/devicon/pull/2270#issuecomment-2351546375)).
- **At least one font-ready version** must exist (plain or line, or an original that qualifies).
- **Priority `original > plain > line`, and non-wordmark over wordmark.** One file that fits several versions takes the highest name and the others become aliases: a one-colour, one-path logo is `x-original` + alias `plain`; a logo that is just letters is `x-original` (+ aliases to wordmark names if wanted) ([SVG-Versions note](https://github.com/devicons/devicon/wiki/SVG-Versions), [#1757](https://github.com/devicons/devicon/pull/1757#discussion_r1199843913), [#1871](https://github.com/devicons/devicon/pull/1871#discussion_r1367742567)).
- **Wordmark = logo with the technology's name.** A styled letter ("V") isn't a word. A non-wordmark file can't alias a wordmark name unless it contains the name ([#2163](https://github.com/devicons/devicon/pull/2163#discussion_r1554836910)).
- **`plain`** = one colour + transparency, one united path. Typically the original in one colour with paths unified, white parts cut out, and thin gaps where colours met so it doesn't become a blob ([#1860](https://github.com/devicons/devicon/pull/1860#issuecomment-1789424696)).
- **`line`** = an outline version: roughly the inverse of plain — where plain has gaps there are lines ([#1488](https://github.com/devicons/devicon/pull/1488#discussion_r1019289384)). Even line thickness, thick enough to read small ([#2264](https://github.com/devicons/devicon/pull/2264#issuecomment-2943588270)); outlined (hollow) letters in `line-wordmark` are optional.
- **Duplicates are removed**: if `plain` is just `original` without colour, delete it and alias instead ([#1456](https://github.com/devicons/devicon/pull/1456#discussion_r996286096), lunatic-fox's [duplicate sweep](https://github.com/devicons/devicon/pull/1998#issuecomment-1807542194)).
- **File names**: `icons/<name>/<name>-<version>.svg`, name lowercase and concatenated (`amazonwebservices`, `threedsmax` for "3ds Max"). Use the name the project uses most; other names go in `altnames` ([#1372](https://github.com/devicons/devicon/pull/1372#discussion_r967808514), [#1552](https://github.com/devicons/devicon/issues/1552#issuecomment-1556399185)).

## 4. SVG file standards

- **`viewBox="0 0 128 128"`** exactly — no offsets (`663 37 128 128` is wrong, [#2556](https://github.com/devicons/devicon/pull/2556#issuecomment-3376536384)), no `width`/`height`.
- **No padding**: scaled proportionally until the longer side is 128 (top–bottom or left–right touches the edges, [#2343](https://github.com/devicons/devicon/pull/2343#issuecomment-2641737246)); nothing outside the box (128.005 gets flagged, [#2090](https://github.com/devicons/devicon/pull/2090#issuecomment-1960301828)); **centred** on both axes; **aspect ratio kept** (squished logos get rejected, [#1926](https://github.com/devicons/devicon/pull/1926#discussion_r1370458696)). Zero padding was adopted on cyberalien's (Iconify) advice so icons scale crisply ([#1537](https://github.com/devicons/devicon/pull/1537#issuecomment-1322651792)).
- **Optimized**: SVGO/SVGOMG with multipass and every option except "Remove xmlns", "Round/rewrite number lists" and "Replace duplicate elements with links" ([guide](https://github.com/devicons/devicon/issues/1279#issuecomment-1195433256), [wiki](https://github.com/devicons/devicon/wiki/Optimizing-icons)). Then **one line, plus an empty line at the end** ([#2221](https://github.com/devicons/devicon/pull/2221#discussion_r1693924712), [#2404](https://github.com/devicons/devicon/pull/2404#discussion_r2109620969)).
- **Minimal markup**: needed are `xmlns`, `viewBox` and fills ([#2264](https://github.com/devicons/devicon/pull/2264#discussion_r2135248195)). Remove `<style>` (inline as `fill` attributes), classes, ids that aren't referenced, `style="…"`, `xml:space`, editor metadata, `version`, `fill="none"` leftovers, `currentColor`, unused groups.
- **No strokes** (convert stroke to path — icomoon ignores strokes and renders them empty, [#2246](https://github.com/devicons/devicon/pull/2246#discussion_r1718161755)); **no `<text>`** (convert to paths); **no opacity tricks** (faded paths, [#1557](https://github.com/devicons/devicon/pull/1557#discussion_r1038740182)). The check-bot only enforces strokes on font versions, but clean originals are preferred.
- **IDs prefixed with the file name** (`kotlin-original-a`) so inline SVGs on one page don't clash ([#2608](https://github.com/devicons/devicon/issues/2608)). The planned build step prefixes them after merge, so a missing prefix is a notice, not a blocker.
- **Reasonable size and node count.** Median icon ≈ 2.7 KB, 90% under ≈ 11 KB, 99% under ≈ 42 KB. Huge paths break the font build (nano at 126–181 KB, [#1619](https://github.com/devicons/devicon/pull/1619#issuecomment-1376496982); Delphi at 1.2 M characters). Excess or misplaced nodes (curve nodes inside straight segments) cause spikes in the font ([#1527](https://github.com/devicons/devicon/pull/1527#issuecomment-1321879664), [#1472](https://github.com/devicons/devicon/pull/1472#issuecomment-1333637693)). Finii's tips: simplify selected nodes, 4 nodes for a circle, ~4 decimal digits, remove stray smudges ([#2290](https://github.com/devicons/devicon/pull/2290#issuecomment-2647523553), [#2264](https://github.com/devicons/devicon/pull/2264#issuecomment-2938914267)).

## 5. Font versions

Every version listed in `versions.font` becomes a glyph in an icon font, where **all colour is discarded**:

- **Exactly one `<path>`, one fill colour, no groups**, no gradients, clip-paths, masks or filters ([wiki](https://github.com/devicons/devicon/wiki/SVG-Versions), canaleal [#2301](https://github.com/devicons/devicon/pull/2301#issuecomment-2525311988)).
- **White is not transparent.** White parts turn into ink and the icon becomes a blob; they must be cut out as holes (Thomas-Boi [#892](https://github.com/devicons/devicon/pull/892#issuecomment-948889487), [#1097](https://github.com/devicons/devicon/pull/1097#issuecomment-1077051443); Finii [#2427](https://github.com/devicons/devicon/pull/2427#issuecomment-2930982922)).
- **Fill = the entry's `color`.** canaleal's validation report flags missing or different fills ([#2436](https://github.com/devicons/devicon/pull/2436#issuecomment-2975459914)); `#000000` may be omitted (SVG default black) but explicit is preferred.
- **Holes must work with the nonzero fill rule** that fonts use: holes wound opposite to their outer contour. Even-odd-only holes may fill in the font (Finii [#2290](https://github.com/devicons/devicon/pull/2290#issuecomment-2647523553)).
- **Check the font glyph, not just the SVG.** Peek-bot screenshots (or importing into icomoon) show artifacts: spikes, filled gaps, slivers, wrong shapes ([#1527](https://github.com/devicons/devicon/pull/1527#issuecomment-1321271036), [#1977](https://github.com/devicons/devicon/pull/1977#issuecomment-1806839218)). Artifacts often appear only after optimization: too-low precision (weh [#2380](https://github.com/devicons/devicon/pull/2380#issuecomment-2913470372)) or compressed path data icomoon misreads (cyberalien [#1527](https://github.com/devicons/devicon/pull/1527#issuecomment-1321773090)). Glyph count must equal the number of font versions.
- **Readable at small sizes.** Too intricate → simplify (Finii [#2264](https://github.com/devicons/devicon/pull/2264#issuecomment-2346134953)). For outlined mascots: inner outlines become gaps, outer outlines merge into the silhouette (Finii [#2264](https://github.com/devicons/devicon/pull/2264#issuecomment-2933483100)).

## 6. devicon.json

```json
{
    "name": "example",
    "altnames": [],
    "tags": ["language"],
    "versions": {
        "svg": ["original", "original-wordmark", "plain", "plain-wordmark", "line", "line-wordmark"],
        "font": ["plain", "plain-wordmark", "line", "line-wordmark"]
    },
    "color": "#123456",
    "aliases": []
}
```

- All six keys present; `altnames` and `aliases` may be empty arrays. `altnames` must not repeat `name`.
- **Sorted by `name`**; the file's formatting kept (4-space indentation, arrays one item per line, no trailing commas — don't let a formatter rewrite the file, [#1465](https://github.com/devicons/devicon/pull/1465#issuecomment-1287950577), [#2726](https://github.com/devicons/devicon/pull/2726#discussion_r4241951876)).
- **`versions.svg`** lists exactly the SVG files in the folder; **`versions.font`** only those that are font-ready; order `original, original-wordmark, plain, plain-wordmark, line, line-wordmark` ([#2488](https://github.com/devicons/devicon/pull/2488#issuecomment-3066715324)).
- **`aliases`** only for versions that don't exist as files; `base` must be an existing font version; one object per alias (no arrays); never alias across style (plain → line) or from non-wordmark to wordmark without the name; base ≠ alias. Flowchart (lunatic-fox [#1788](https://github.com/devicons/devicon/pull/1788#discussion_r1225886328)): `original → plain`, `original → line`, `original → original-wordmark → plain-wordmark / line-wordmark`.
- **`color`**: the logo's main colour, or the primary colour from the brand guidelines; must appear in the icon; for gradients the dominant/middle colour; not GitHub Linguist's colour; avoid pure white ([#1393](https://github.com/devicons/devicon/pull/1393#issuecomment-1261984651), [#1450](https://github.com/devicons/devicon/pull/1450#discussion_r995986304), [#1457](https://github.com/devicons/devicon/pull/1457#discussion_r996288194), [#2021](https://github.com/devicons/devicon/pull/2021#discussion_r1398515635)).
- **`tags`**: reuse existing tags; avoid catch-alls like "utility".

## 7. Process and PR scope

- One icon per PR, changing only `icons/<name>/` and that icon's `devicon.json` entry.
- Title `new icon: <name> (<versions>)` or `update icon: <name> (<versions>)` listing the versions in the PR.
- Base branch: whatever the repo currently uses (check `.github/workflows/check_icon_pr.yml` and the PR template) — `develop` before the trunk-based migration, `master` after.
- Renames and removals are breaking changes: separate PR, major release.
- Merges preferred over rebases while reviewing (easier to see what changed); don't force-push away review history without reason.
- Check for an open PR or issue for the same icon first; link the issue (`This PR closes #…`).

## 8. Known disagreements

- **Single path vs editability**: BenSouchet argued multiple paths are easier to edit and sometimes smaller ([#1323](https://github.com/devicons/devicon/pull/1323#discussion_r932554197)); the standard (enforced since) is one path for font versions. Originals may keep several paths.
- **Simplifying a logo**: BenSouchet/lunatic-fox accept dropping tiny details in plain versions for readability; others prefer not altering logos. Consensus: original stays exact; plain/line may simplify.
- **Fill on plain SVGs**: once removed ("colour comes from devicon.json"), later re-added for third-party tools; current expectation: fill = `color`.
