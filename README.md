<p align="center">
    <a href="https://github.com/devicons/devicon/releases">
        <img alt="GitHub release (latest by semver)" src="https://img.shields.io/github/v/release/devicons/devicon?color=%2360be86&label=Latest%20release&style=for-the-badge&sort=semver">
    </a>
    <a href="/LICENSE">
        <img alt="GitHub" src="https://img.shields.io/github/license/devicons/devicon?color=%2360be86&style=for-the-badge">
    </a>
    <a href="https://github.com/devicons/devicon/graphs/contributors">
        <img alt="GitHub contributors" src="https://img.shields.io/github/contributors-anon/devicons/devicon?color=%2360be86&style=for-the-badge">
    </a>
    <a href="https://github.com/devicons/devicon/actions">
        <img alt="GitHub branch checks state" src="https://img.shields.io/github/checks-status/devicons/devicon/master?color=%2360be86&style=for-the-badge">
    </a>
    <a href="https://github.com/devicons/devicon/issues?q=is%3Aopen+is%3Aissue+label%3Arequest%3Aicon">
        <img alt="GitHub issues by-label" src="https://img.shields.io/github/issues/devicons/devicon/request:icon?color=%2360be86&label=icon%20requests&style=for-the-badge">
    </a>
    <a href="https://github.com/devicons/devicon/stargazers">
        <img alt="GitHub Repo stars" src="https://img.shields.io/github/stars/devicons/devicon?color=%2360be86&label=github%20stars&style=for-the-badge">
    </a>
</p>
<br />
<div align="center">
    <a href="https://github.com/devicons/devicon">
        <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/devicon/devicon-original-wordmark.svg" alt="Devicon Logo" height="140" />
    </a>
    <h5 align="center">
        devicon aims to gather all logos representing development languages and tools.
    </h5>
    <p align="center">
        <a target="_blank" href="https://devicon.dev">Demo</a>
        &middot;
        <a target="_blank" href="https://github.com/devicons/devicon/issues/new?assignees=&labels=request%3Aicon&template=icon-request.md&title=Icon+request%3A+%5BNAME%5D">Request Icon</a>
        &middot;
        <a href="#contribute">Contribute</a>
    </p>
</div>

<h2>TL;DR;</h2>

```html
<!-- in your header -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/devicon.min.css">

<!-- in your body -->
<i class="devicon-devicon-plain"></i>
```

<h2>Table of Contents</h2>
<ol>
    <li><a href="#about">About the project</a></li>
    <li><a href="#getting-started">Getting started</a></li>
    <li><a href="#request-icon">Requesting icon</a></li>
    <li><a href="#contribute">Contributing</a></li>
    <li><a href="#discord-server">Discord server</a></li>
    <li><a href="#develop-vs-master"><code>develop</code> vs <code>master</code></a></li>
    <li><a href="#stale-prs">Stale pull requests</a></li>
    <li><a href="#build-yourself">Go build yourself</a></li>
</ol>

<h2 id="about">About the project</h2>
<p>
    Devicon aims to gather all logos representing development languages and tools.
    Each icon comes in several versions: font/SVG, original/plain/line, colored/not colored, wordmark/no wordmark.
    Devicon has 150+ icons. And it's growing!<br />
</p>
<p>
    See the <a href="/devicon.json">devicon.json</a> or <a href="https://devicon.dev">our website</a> for complete and up to date reference of 
    all available icons.
</p>
<sub>
    All product names, logos, and brands are property of their respective owners. All company, product and service 
    names used in this website are for identification purposes only. Use of these names, logos, and brands does not 
    imply endorsement. Usage of these logos should be done according to the company/brand/service's brand policy.
</sub>
<p>
    Thank you to our contributors and the <a href="https://icomoon.io/#home">IcoMoon app</a>. Devicon would not be possible without you.
</p>


<h2 id="getting-started">Getting started</h2>
<p>
    For a super fast setup go check <a href="https://devicon.dev">devicon.dev</a>.<br />
    You can either <a href="#getting-started-svg">use the raw SVG</a> icons or our <a href="#getting-started-font">devicon font</a> (which is 
    also available via CDN).
</p>

<h4 id="getting-started-font">Use the <code>devicon</code> font (recommended)</h4>
<p>
    You can install devicon as a dependency to your project either with <code>npm</code> or <code>yarn</code>:
</p>

```bash
npm install --save devicon
yarn add devicon
```

<p>
    If you don't want to use a package manager you can also download
    and include <a href="/devicon.min.css">devicon.min.css</a> next to the <a href="/fonts">font files</a> to your project.
    See <a href="https://devicon.dev">devicon.dev</a> for details about how to add devicon to your project via
    a CDN.
</p>
<p>
    After setting up you just have to include the stylesheet in your header
    to get started:
</p>

```html
<link rel="stylesheet" href="devicon.min.css">
```

<p>Start using icons with <code>&lt;i&gt;</code>-tag</p>

```html
<!--  for devicon plain version -->
<i class="devicon-devicon-plain"></i>

<!--  for devicon plain version with wordmark -->
<i class="devicon-devicon-plain-wordmark"></i>

<!--  for devicon plain version colored with devicon main color -->
<i class="devicon-devicon-plain colored"></i>

<!--  for devicon plain version with wordmark colored with devicon main color -->
<i class="devicon-devicon-plain-wordmark colored"></i>
```

<p>
    An alternate way to use <code>devicon</code> is by copy/paste the raw SVG code
    to your project.
</p>
<h4 id="getting-started-svg">Copy/paste SVG code (from the <a href="https://github.com/devicons/devicon/tree/master/icons">svg folder</a> or the <a href="https://devicon.dev">project page</a>)</h4>

```html
<!--  for devicon plain version -->
<svg id="Devicon" class='devicon-devicon-plain' xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128"><path id="plain" fill="#60be86" d="M64,7.83H4.77L14.95,95.13l49,25,.06,0,49.07-25L123.23,7.83Zm42.77,54.86c0,.88,0,1.67-.77,2L73.25,80.44l-2.42,1.13-.27-3.15V72.23l.24-1.57,1.09-.47L95.07,59.81l-21.54-9.6L64.35,68.34,58.9,78.87l-1.22,2.27-2.05-.9L22,64.71a2.42,2.42,0,0,1-1.45-2V56.91a2.39,2.39,0,0,1,1.42-2l34-15.73,3.21-1.44v9.66l.24,1.34-1.56.7L34.45,59.79,56.3,69.42l8.05-16,6.21-12.65,1.13-2.28,1.81.91L106,54.89c.73.35.76,1.14.76,2Z"/></svg>
```

Add css rules in your stylesheet
```css
.devicon-devicon-plain {
  max-width: 2em;
}

/* if you want to change the original color */
.devicon-devicon-plain path {
  fill: #4691f6;
}
```

<h4>You can also use the <code>img</code> tag and referencing an svg directly from the repo.</h4>

```html
<img src='https://cdn.jsdelivr.net/gh/devicons/devicon/icons/devicon/devicon-original.svg'>
```

<h2 id="request-icon">Requesting icon</h2>
<p>
    When you want to request an icon please feel free to create an issue. See our <a href="https://github.com/devicons/devicon/wiki/Requesting-an-Icon">Wiki</a> for more information.
</p>

<h2 id="contribute">Contributing</h2>
<p>
    We are happy with every contribution, whether it's new icons, features, or maintainers. Please have a look at our <a href="https://github.com/devicons/devicon/wiki">Wiki</a> to see how you can contribute to this project.
</p>

<h2 id="discord-server">Discord server</h2>
<p>
We are running a Discord server. You can go here to talk, discuss, and more with the maintainers and other people, too. Here's the invitation: https://discord.gg/hScy8KWACQ.
<b>Note that the Discord server is unofficial, and Devicons is still being maintained via GitHub.</b>
</p>

<h2 id="develop-vs-master"><code>develop</code> vs <code>master</code></h2>
<p>
All official releases shall be in <code>master</code>. Any updates in between (icons, features, etc.) will be kept in <code>develop</code>. 
</p>
<b><code>develop</code> contains:</b>
<ul>
    <li>
        Latest SVGs (non-optimized).
    </li>
    <li>
        No icons for the latest SVGs. These will be build at every release.
    </li>
    <li>
        Experimental changes.
    </li>
</ul>
<b><code>master</code> contains:</b>
<ul>
    <li>
        Latest official release, which contains the SVGs and icons.
    </li>
    <li>
        Official tested changes.
    </li>
</ul>

<h2 id="stale-prs">Stale pull requests</h2>
<p>
After a pull request has been open for over 30 days with no activity or response from the author, it'll be automatically marked as stale. We might fork your changes and merge the changes ourselves. Since GitHub tracks contributions by commits, you will be credited.
</p>

<h2 id="build-yourself">Go build yourself</h2>
<p>
    Feel free to follow those steps when you want to build the font
    by yourself.
</p>
<h5>Prerequisites</h5>
<p>Install gulp (and gulp plugins)</p>

```bash
npm install
```

<h5>Build the font and export stylesheet</h5>
Open <a href="https://icomoon.io/app/#/select">icomoon.io</a> and import <a href="/icomoon.json">icomoon.json</a>. Choose <i>yes</i> when being asked
if you would like to restore the settings stored in the configuration file.

The next step is to click on <b>Generate font</b> and download the resulting archive. Extract the contents and you will find a <a href="/fonts">fonts</a> directory next to a <code>style.css</code>. Replace the contents of the <code>fonts</code> folder, rename <code>style.css</code> as <a href="/devicon.css">devicon.css</a> and follow the next step to build the final stylesheet.

<h5>Build and minify stylesheet</h5>
<p>
    Run the following command to build the resulting file <code>devicon.min.css</code>
</p>

```bash
npm run build-css
```

<br />
<div align="center">
    <img src="https://forthebadge.com/images/badges/built-with-love.svg" />
    <img src="https://forthebadge.com/images/badges/built-by-developers.svg" />
</div>
