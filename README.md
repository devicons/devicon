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
    <li><a href="#build-yourself">Go build yourself</a></li>
</ol>

<h2 id="about">About the project</h2>
<p>
    Devicon aims to gather all logos representing development languages and tools.
    Each icon comes in several versions: font/svg, original/plain/line, colored/not colored, wordmark/no wordmark.
    Devicon has 150+ icons. And it's growing!<br />
</p>
<p>
    See the <a href="/devicon.json">devicon.json</a> or <a href="https://devicon.dev">our website</a> for complete and up to date reference of 
    all available icons.
</p>
<sub>
    All product names, logos, and brands are property of their respective owners. All company, product and service 
    names used in this website are for identification purposes only. Use of these names, logos, and brands does not 
    imply endorsement.
</sub>


<h2 id="getting-started">Getting started</h2>
<p>
    For a super fast setup go check <a href="https://devicon.dev">devicon.dev</a>.<br />
    You can either <a href="#getting-started-svg">use the raw svg</a> icons or our <a href="#getting-started-font">devicon font</a> (which is 
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
<!--  for git plain version -->
<i class="devicon-git-plain"></i>

<!--  for git plain version with wordmark -->
<i class="devicon-git-plain-wordmark"></i>

<!--  for git plain version colored with git main color (devicon-color.css or devicon.min.css required) -->
<i class="devicon-git-plain colored"></i>

<!--  for git plain version with wordmark colored with git main color (devicon-color.css or devicon.min.css required) -->
<i class="devicon-git-plain-wordmark colored"></i>
```

<p>
    An alternate way to use <code>devicon</code> is by copy/paste the raw svg code
    to your project.
</p>
<h4 id="getting-started-svg">Copy/paste svg code (from the <a href="https://github.com/devicons/devicon/tree/master/icons">svg folder</a> or the <a href="https://devicon.dev">project page</a></h4>

```html
<!--  for git plain version -->
<svg class="devicon-git-plain" viewBox="0 0 128 128">
  <path fill="#F34F29" d="M124.742,58.378L69.625,3.264c-3.172-3.174-8.32-3.174-11.497,0L46.685,14.71l14.518,14.518c3.375-1.139,7.243-0.375,9.932,2.314c2.703,2.706,3.462,6.607,2.293,9.993L87.42,55.529c3.385-1.167,7.292-0.413,9.994,2.295c3.78,3.777,3.78,9.9,0,13.679c-3.78,3.78-9.901,3.78-13.683,0c-2.842-2.844-3.545-7.019-2.105-10.521L68.578,47.933l-0.002,34.341c0.922,0.455,1.791,1.063,2.559,1.828c3.779,3.777,3.779,9.898,0,13.683c-3.779,3.777-9.904,3.777-13.679,0c-3.778-3.784-4.088-9.905-0.311-13.683C58.079,83.169,59,82.464,60,81.992V47.333c-1-0.472-1.92-1.172-2.856-2.111c-2.861-2.86-3.396-7.06-1.928-10.576L40.983,20.333L3.229,58.123c-3.175,3.177-3.155,8.325,0.02,11.5l55.126,55.114c3.173,3.174,8.325,3.174,11.503,0l54.86-54.858C127.913,66.703,127.916,61.552,124.742,58.378z"/>
</svg>
```

Add css rules in your stylesheet
```css
.devicon-git-plain {
  max-width: 2em;
}

/* if you want to change the original color */
.devicon-git-plain path {
  fill: #4691f6;
}
```

<h2 id="request-icon">Requesting icon</h2>
<p>
    When you want to request a icon please feel feel to create a issue. See our <a href="/CONTRIBUTING.md#requestingIcon">contribution guidelines</a> for more information.
</p>

<h2 id="contribute">Contributing</h2>
<p>
    We are happy for every contribution. Please have a look at our <a href="CONTRIBUTING.md">contribution guidelines</a>
    to see how you can contribute to this project.
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
Open <a href="https://icomoon.io/app/#/select">icomoon.io</a> and import <a href="/icomoon.json">icomoon.json</a>. Choose <i>yes</i> when beeing asked
if you like to restore the settings stored in the configuration file.

The next step is to click on <b>Generate font</b> and download the resulting archive. Extract it
contents and you will find a <a href="/fonts">fonts</a> directory next to a <code>style.css</code>. Replace the content of the <code>fonts</code> folder,
rename the <code>style.css</code> to <a href="/devicon.css">devicon.css</a> and follow the next step to build the final stylesheet.

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
