---
name: devicon-icon-review
description: Review devicon "new icon" / "update icon" pull requests (and icon proposals or icon files before a PR) the way devicon's maintainers do — whether the technology is accepted, whether the logo is official and current, version naming and aliases, SVG standards (128×128 viewBox, no padding, centred, optimized single-line files), font-readiness of plain/line versions (one path, one colour, no strokes, white cut out), devicon.json correctness, the peek-bot font previews, and PR scope/title. Use this whenever the user asks to review, check, approve, or give feedback on a devicon icon PR or icon SVGs, mentions a PR number in devicons/devicon with an icon title, or asks whether an icon "is ready" — even if they only paste a PR link.
---

# Reviewing devicon icon PRs

The goal is the review a careful devicon maintainer would write: correct, specific, kind, and actionable — every problem comes with the fix (often a ready-to-commit suggestion). Contributors are frequently first-timers; maintainers here link the wiki, explain *why*, and offer help.

Standards live in `references/devicon-standards.md` (with links to the maintainer comments they come from). Read it before your first review in a session; it's the source of truth for the checklist below.

## Tools

- `scripts/check_icon.js <name> --repo <devicon checkout>` — checks the icon's `devicon.json` entry and its files: required keys, versions vs files, font versions (one path, one fill, fill = `color`, no white/groups/gradients/strokes), aliases, viewBox/width/height/xmlns, raster `<image>`, `<text>`, `<style>`/editor leftovers, single line + trailing newline, size, id prefixes, sort order. No dependencies.
- The **svg-icons** skill (`.claude/skills/svg-icons/`) for the visual side: `render.js` (light/dark, 128/32/16 px), `validate.js` (padding, centring, outside-the-box), `pixdiff.js`, `inspect.js`. If its dependencies aren't installed (`npm install` in its `scripts` folder), render the SVGs some other way — don't skip looking at them.
- `gh` for the PR, its files, comments (peek-bot screenshots, check-bot output) and the linked issue.

## Workflow

1. **Get the PR.**
   ```bash
   gh pr view <n> -R devicons/devicon --json title,body,baseRefName,headRefName,headRepositoryOwner,files,labels,comments,statusCheckRollup
   gh pr checkout <n> -R devicons/devicon   # in a scratch worktree, never in the user's working copy
   ```
   Note the title, the base branch the repo expects (see `.github/workflows/check_icon_pr.yml`), the changed files, the linked issue and the source link in the PR body.
2. **Scope and process** (standards §7): one icon, only `icons/<name>/` and that entry changed, title `new|update icon: <name> (<versions>)` matching the files, correct base, no duplicate open PR. Renames/removals are breaking and belong in their own PR.
3. **Acceptance** (§1): technology not company, dev-related, well-known, official logo exists, brand guidelines allow it, logo is current. If acceptance is unclear, say so and leave the decision to a maintainer instead of guessing.
4. **Source and fidelity** (§2): open the official source (brand kit, repo, website) and compare with `original` side by side — colours (hex), details, proportions. Flag rasters, outdated logos, invented colours, missing shadows/details.
5. **Run the checks.**
   ```bash
   node .claude/skills/devicon-icon-review/scripts/check_icon.js <name> --repo .
   node .claude/skills/svg-icons/scripts/validate.js icons/<name>
   node .claude/skills/svg-icons/scripts/render.js icons/<name> --out /tmp/<name>-preview.png
   ```
   Then **look at the preview**: blobs (white not cut out), slivers, uneven line widths, things outside the box, off-centre, squished, unreadable at 16px.
6. **Versions and devicon.json** (§3, §6): original exists; at least one font version; priority original > plain > line; duplicates replaced by aliases; aliases only for versions without files; `color` = main logo colour and present in the SVGs; order and formatting of the entry.
7. **Font preview** (§5): read the peek-bot comment's screenshots (download the images and look). Glyph count must equal the number of font versions; check each glyph for spikes, filled holes, missing parts. If peek hasn't run or failed, say so — the maintainer adds `bot:peek`.
8. **Write the review** (format below). Offer fixed SVGs or `devicon.json` suggestions when the fix is mechanical; you can usually produce them with the svg-icons scripts.

## Review format

Use this structure (in chat, or as a PR review when the user asks you to post it):

```markdown
**Verdict:** Approve | Request changes | Needs a maintainer decision (why)

Thanks for the PR! Here's what I found:

### Must fix
- `<file>`: <problem> — <fix>. (<wiki link>)

### Should fix
- …

### Optional / nice to have
- …

<previews: rendered PNGs, peek screenshots, side-by-side with the official logo>

<suggestion blocks for devicon.json, or fixed SVG code in <details>>
```

- **Must fix** = blocks merging (standards violations, wrong logo, broken font glyph, missing original/font version, devicon.json errors). **Should fix** = expected but minor (fill ≠ color, missing trailing newline, unoptimized). **Optional** = improvements (line-wordmark hollow text, extra versions).
- Every item: what, where, why, how to fix — and a link to the relevant wiki page: [SVG-Standards](https://github.com/devicons/devicon/wiki/SVG-Standards), [SVG-Versions](https://github.com/devicons/devicon/wiki/SVG-Versions), [Updating devicon.json](https://github.com/devicons/devicon/wiki/Updating-%60devicon.json%60), [Creating original](https://github.com/devicons/devicon/wiki/Creating-original-Icons) / [plain](https://github.com/devicons/devicon/wiki/Creating-plain-Icons) / [line](https://github.com/devicons/devicon/wiki/Creating-line-Icons) icons, [Optimizing icons](https://github.com/devicons/devicon/wiki/Optimizing-icons), [What Icons Do We Accept?](https://github.com/devicons/devicon/wiki/What-Icons-Do-We-Accept%3F).
- For `devicon.json` fixes use GitHub suggestion blocks (```` ```suggestion ````) on the right lines, so the contributor can commit them with one click.
- Show, don't just tell: attach renders for visual problems (`render.js --zoom` for details). GitHub can't show images by local or relative path: tell the user which PNGs to drag into the comment, or host them (e.g. a branch on their fork, linked via `raw.githubusercontent.com` pinned to a commit).
- If the logo itself is the technology's name (a lettermark such as "Nx"), wordmark aliases (`original` → `original-wordmark`, …) are a cheap, useful suggestion.
- Don't pile on: if the logo itself is wrong or not accepted, say that first; nitpicks about a file that will be replaced are noise.
- Separate facts from judgement calls (colour choice, how much to simplify a plain version); for judgement calls, propose and ask.

## Posting

Only post to GitHub when the user asks. Reviews and comments posted through `gh` appear under the user's account, so start them with a line saying they were prepared by Claude on the user's behalf (unless the user has set up a separate bot identity). Prefer `gh pr review <n> --comment|--request-changes|--approve --body-file …`; approving is the user's call — never approve on your own initiative. Link issues and PRs with full `https://github.com/devicons/devicon/...` URLs in chat (bare `#123` can resolve to a fork).
