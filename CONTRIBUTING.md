# Contributing to Devicon

First of all, thanks for taking the time to contribute!

These are not rules, just guidelines that you can follow in order to keep the repository as clean as possible. But if you don't have time to follow all of it, no worries, just create a pull request and I'll make the modifications myself if needed.

And if you think there is a better way to organize this repo, please do not hesitate to share your point of view.

## Submitting icon(s)

Each icon comes in different "versions":
- original
- original-wordmark
- plain
- plain-wordmark
- line
- line-wordmark

This is not mandatory, an icon can only have 1 or 2 versions available. Just keep in mind that the minimum is 1 and the maximum 6 (for now).

The plain and line versions (with or without wordmark) are designed to be available in the final icon font. So they need to stay as simple as possible (one color and ensure that the paths are united before to export to svg). You can use a service like [compressor](https://compressor.io/) or [SVG Editor](https://petercollingridge.appspot.com/svg-editor) in order to optimize the svg file.
The original versions are only available in svg format, so they do not need to be as simple and they can contain numerous colors.
Some icons are really simple (like the apple one), so the original version can be used for the icon font. In this case, I'll add an alias so they can be found with the "original" or "plain" naming convention.

##### Organizational guidelines:
- Each icon has his own folder located in the "icons" folder.
- Each icon folder contains one .eps file and as many .svg files as versions available.
- The .eps file contains all available versions of an icon. Each version is contained in a 128px by 128px artboard.
- Each .svg file contains one version of an icon in a "0 0 128 128" viewbox
- The naming convention for the svg file is the following: (icon name)-(original/plain/line)-(wordmark)
