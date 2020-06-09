<h1>Contributing to Devicon</h1>
<p>
First of all, thanks for taking the time to contribute! This project can only grow and live by your countless contributions. To keep this project maintable we developed some guidelines for contributions. 
</p>
<h2>Submitting icon</h2>
<ul>
  <li>Create a separated pull request for each icon (no matter how many variations)</li>
  <li>Include the name of the icon in the pull request f.e. "new icon: html5 (original, plain, line)"</li>
  <li>At least the plain or line version of the icon is required (since those are required for the icon font)</li>
  <li>Modify <a href="https://github.com/konpa/devicon/blob/master/devicon.json">devicon.json</a> to include the icon (or variations)</li>
  <li>Modify <a href="https://github.com/konpa/devicon/blob/master/devicon-colors.css">devicon-colors.css</a> to include the colored version of the icon</li>
  <li>optional: Add a image of the new icon(s) to the description of the pull request</li>
  <li>optional: Reference the issues regarding the new icon</li>
</ul>
<h3>Icon formats and naming conventions</h3>
<p>Each icon comes in different variations:</p>
<ul>
  <li>original</li>
  <li>original-wordmark</li>
  <li>plain</li>
  <li>plain-wordmark</li>
  <li>line</li>
  <li>line-wordmark</li>
</ul>
<p>
This is not mandatory, an icon can only have one or two variations available. Just keep in mind that the minimum is 1 and the maximum 6 (for now).
</p>
<p>
The plain and line variations (with or without wordmark) are designed to be available in the final icon font. So they need to stay as simple as possible (one color and ensure that the paths are united before to export to svg). You can use a service like <a href="https://compressor.io/">compressor</a> or <a href="https://petercollingridge.appspot.com/svg-editor">SVG Editor</a> in order to optimize the svg file.
</p>
<p>
The original versions are only available in svg format, so they do not need to be as simple and they can contain numerous colors.
</p>
<p>
Some icons are really simple (like the apple one), so the original version can be used for the icon font. In this case, I'll add an alias so they can be found with the "original" or "plain" naming convention.
</p>
<h3>Organizational guidelines</h3>
<ul>
  <li>Each icon has his own folder located in the "icons" folder</li>
  <li>Each icon folder contains one .eps file and as many .svg files as versions available</li>
  <li>The .eps file contains all available versions of an icon. Each version is contained in a 128px by 128px artboard</li>
  <li>Each .svg file contains one version of an icon in a "0 0 128 128" viewbox</li>
  <li>The naming convention for the svg file is the following: (icon name)-(original/plain/line)-(wordmark)</li>
</ul>
<h2>Requesting a icon</h2>
<p>When you want to request a new icon please feel free to create a issue following some simple guidelines:</p>
<ul>
  <li>Search for other issues already requesting the icon</li>
  <li>Create an issue naming it "Icon request: <i>name-of-the-icon</i>"; please create separated issues for each icon</li>
  <li>optional: Include links where the icon can be found</li>
</ul>
