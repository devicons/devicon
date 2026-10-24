# CLAUDE.md — Devicon Project Guide

This file helps Claude Code understand the structure, conventions, and workflow of the Devicon project.

## Project Overview

Devicon is a collection of icons for programming languages, frameworks, and developer tools. Icons are distributed as a web font (icomoon-generated) and as SVG files.

- **Repo:** https://github.com/devicons/devicon (upstream) / Jørgen's fork
- **Wiki:** `D:\code\personal\devicon.wiki` (cloned locally)
- **Version:** See `package.json`

## Directory Structure

```
devicon/
├── icons/              # SVG source files, one folder per icon (e.g. icons/python/)
├── fonts/              # Generated font files (eot, svg, ttf, woff) — do not edit manually
├── .github/
│   ├── workflows/      # GitHub Actions workflows
│   ├── scripts/        # Python/JS automation scripts (icomoon_build.py etc.)
│   └── PULL_REQUEST_TEMPLATE/
├── devicon.json        # Master list of all icons + metadata
├── devicon-schema.json # JSON schema for devicon.json validation
├── icomoon.json        # Icomoon project config — updated by build scripts
├── devicon.min.css     # Generated CSS — do not edit manually
├── devicon-base.css    # CSS template
├── gulpfile.js         # Gulp tasks (CSS build, SVG optimization)
└── package.json
```

## Trunk-Based Development (current branch model)

- **Single branch:** `master` only. No `develop` branch.
- Contributors open PRs against `master`.
- Merging uses GitHub's native rules (ruleset on `master`): 1 approval required, squash merge only, squash commit title = PR title. No custom merge workflow.
- Font files are built weekly, not per PR.

## Workflow Architecture

### PR Flow
1. Contributor opens PR → `check_icon_pr.yml` validates the touched icons (found from changed files via `util.get_pr_icon_changes`, diffing the PR merge commit against `HEAD^1`) and the PR title → `post_check_icon_pr_comment.yml` comments any errors
2. `peek_icons.yml` runs Icomoon peek on the icon whose SVGs changed → `post_peek_screenshot.yml` posts screenshots as PR comment (nothing posted for PRs without SVG changes)
3. Maintainer approves → squash-merges (or GitHub auto-merge) to master, commit `<PR title> (#<n>)` — the `(#n)` is what the release job reads labels from (**no build step**)

### Repo setup the workflows depend on
- Ruleset on `master`: require PR + 1 approval, squash only, block force-push/deletion. Bypass: the bot GitHub App (always).
- No classic branch protection rule on `master` (Settings → Branches). A push must pass both, and a classic rule requiring PRs has its own bypass list, so it blocks the bot's `build:`/version pushes (GH013) even when the ruleset allows them. Delete it, or add the bot app to its "allow specified actors to bypass required pull requests" list.
- Bot GitHub App with `Contents: Read and write` (pushes to master) and `Pull requests: Read and write` (renames icon PRs), installed on the repo; `vars.BOT_APP_ID` + `secrets.BOT_APP_PRIVATE_KEY`.
- Environments: `production` (required reviewers, gates releases), `release` (holds `NPM_AUTOMATION_TOKEN`). Forks run `npm publish --dry-run`.
- Labels: `release: major`, `release: minor`.

### Weekly Build and Release (`build_weekly.yml`)
- Runs every Monday at 2 AM UTC
- `build` job: if `icons/` or `devicon.json` changed since the last `build:` commit, runs the Icomoon build + CSS and commits with `build:` prefix. On failure: creates a `build-failed` issue
  - An icon's glyphs are (re)built when its non-alias font versions in `devicon.json` don't match its glyphs in `icomoon.json` (new icon / versions changed), or one of its font SVGs changed since the last build (updated icon). Detection is by file diff, not PR titles.
  - Ends by deciding `should_release`: anything shipped (`icons`, `devicon.json`, CSS, `fonts`) changed since the last `v*` tag
- `release` job (only if `should_release`, gated by `production` environment approval): derives semver bump from labels of PRs merged since the last `v*` tag → `npm version` → pushes tag → creates GitHub release
- `publish` job: calls `npm_publish.yml` as a reusable workflow (releases made with `GITHUB_TOKEN` don't trigger `release:` events)
- Only one run at a time (`concurrency: build-and-release`)

### Version Bump Labels
| PR Label         | Bump    |
|------------------|---------|
| `release: major` | major   |
| `release: minor` | minor   |
| (none)           | patch   |

### Manual Build / Release
Run `build_weekly.yml` via workflow_dispatch — it does exactly what the weekly run does (build if needed, release if anything changed). To build without releasing, reject the `production` approval. The `bump` input (`auto`/`patch`/`minor`/`major`) overrides the label-derived bump.

### PR titles
Not used to find icons anywhere (bots, build, release all use changed files). Enforced by `check_icon_pr.yml` for icon PRs (any change in `icons/`):
- one icon per PR; only `icons/<name>/` and that icon's `devicon.json` entry may change — any other added/modified/deleted file or other `devicon.json` entry fails the check with a comment
- title `new icon: <name> (<versions>)` (icon not in target branch's `devicon.json`) or `update icon: <name> (<versions>)`; versions = the SVGs the PR adds/changes; case and version order don't matter
- wrong title on an otherwise clean-scoped PR → check fails, writes `expected_title.txt`, and `post_check_icon_pr_comment.yml` renames the PR with the bot app token (which re-runs the check) and comments old → new title. Without the bot app it comments the expected title instead
- wrong title on a PR with scope problems → no rename; the title issue is part of the error comment
- `devicon.json`-only PRs (aliases, tags…) have no title or scope requirement
- `post_check_icon_pr_comment.yml` only acts on a PR whose head SHA matches the checked commit (fork runs' artifacts are untrusted) and only accepts titles matching the icon-title format

The title becomes the squash commit and the release-notes line.

## TODO
- Replace icomoon.io (Selenium) with a local Node font build: keep existing glyphs from `icomoon.json`, normalize new SVGs to the 1024 grid, assign next codepoint, generate fonts with `svgicons2svgfont` → `svg2ttf` → `ttf2woff`/`ttf2eot`. Prototype first and diff glyph output against current fonts. Would also allow real-font PR previews instead of peek-bot.
- Update wiki pages still describing the `develop` flow (Release-strategy, Creating-Pull-Request-for-New-Icon, Overview-on-Submitting-Icons, Requesting-an-Icon, About-the-Maintainers, Our-automated-tasks-and-bots) — on a wiki branch, publish together with the migration.

## Common Tasks

### Run the build locally (Windows)
```powershell
npm run build-icons
```

### Build CSS only
```powershell
npm run build-css
```

### Run local dev server
```powershell
npm run dev
# Opens http://localhost:8000/docs
```

### Add a new icon
1. Create folder `icons/<name>/` with SVG variants
2. Add entry to `devicon.json` in alphabetical order (validate against `devicon-schema.json`)
3. Open PR against `master` with title format: `new icon: <name> (<variants>)`

## devicon.json Format
Each entry looks like:
```json
{
  "name": "python",
  "tags": ["scripting", "data science", ...],
  "versions": {
    "svg": ["original", "original-wordmark", "plain", "plain-wordmark"],
    "font": ["original", "plain", ...]
  },
  "color": "#3572A5",
  "aliases": [...]
}
```

## Important Notes
- Font files (`fonts/`, `devicon.eot`, `devicon.ttf`, etc.) are **generated artifacts** — don't edit them directly.
- `icomoon.json` is updated by the build script — don't edit manually.
- `devicon.min.css` is generated by `npm run build-css` — don't edit manually.
- The `build:` commit prefix is used by the weekly build to detect the last successful build.
- All building, versioning and releasing goes through `build_weekly.yml` (the old `build_icons.yml` and `version_and_release.yml` were removed).
