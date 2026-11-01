# CLAUDE.md

Devicon is a set of icons for programming languages, frameworks and developer tools, shipped as SVG files and an icon font (built with icomoon.io).

The [wiki](https://github.com/devicons/devicon/wiki) is the source of truth for contributing. Link to it rather than copying its rules here, so there's one place to keep up to date.

## Where things are

- `icons/<name>/<name>-<version>.svg`: the icons. One folder per icon.
- `devicon.json`: every icon's versions, aliases, colour and tags. Kept sorted by `name`.
- Generated, don't edit by hand: `fonts/`, `devicon.min.css`, `icomoon.json` (all from the build).
- `.github/workflows/` and `.github/scripts/`: the bots (check, peek, build). Overview: [Our automated tasks and bots](https://github.com/devicons/devicon/wiki/Our-automated-tasks-and-bots).
- `docs/`: the website, devicon.dev (`npm run dev` serves it at http://localhost:8000/docs).

## Icons

- Process: [Overview on Submitting Icons](https://github.com/devicons/devicon/wiki/Overview-on-Submitting-Icons), [Updating an Icon](https://github.com/devicons/devicon/wiki/Updating-an-Icon).
- Rules: [What Icons Do We Accept?](https://github.com/devicons/devicon/wiki/What-Icons-Do-We-Accept%3F), [SVG Versions](https://github.com/devicons/devicon/wiki/SVG-Versions), [SVG Standards](https://github.com/devicons/devicon/wiki/SVG-Standards), [Naming Conventions](https://github.com/devicons/devicon/wiki/Naming-Conventions), [Updating devicon.json](https://github.com/devicons/devicon/wiki/Updating-%60devicon.json%60).
- One icon per PR. Titles: `new icon: <name> (<versions>)` or `update icon: <name> (<versions>)`. Other PRs use conventional-commit titles (`fix: …`, `docs: …`); `pr_title.yml` checks them.
- Skills in `.claude/skills/`:
  - `svg-icons`: build, fix, render and validate icon SVGs. Run `npm install` in `.claude/skills/svg-icons/scripts` first.
  - `devicon-icon-review`: review icon PRs against the wiki and maintainers' review practice.
- Always render an icon and look at it (light and dark background, small sizes) before calling it done.

## Branches and releases

See [Release strategy](https://github.com/devicons/devicon/wiki/Release-strategy,-conventions,-preparation-and-execution) for which branch PRs target and how releases are built. Fonts are built by the release workflow, not in PRs.

## Posting on GitHub

Only post (comments, reviews, PRs) when asked. Posts made through someone's account should say they were prepared by Claude. Never approve or merge on your own.
