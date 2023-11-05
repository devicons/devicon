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
        <img alt="GitHub repository stars" src="https://img.shields.io/github/stars/devicons/devicon?color=%2360be86&label=github%20stars&style=for-the-badge">
    </a>
    <a href="https://devicon.dev/">
        <img alt="Registered logos" src="https://img.shields.io/github/directory-file-count/devicons/devicon/icons?color=%2360be86&label=registered%20logos&style=for-the-badge">
    </a>
</p>
<br />
<div align="center">
    <a href="https://github.com/devicons/devicon">
        <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/devicon/devicon-original-wordmark.svg" alt="Devicon Logo" height="140" />
    </a>
    <h5 align="center">
        Devicon aims to gather all logos representing development languages and tools.
    </h5>
    <p align="center">
        <a target="_blank" href="https://devicon.dev">Demo</a>
        &middot;
        <a target="_blank" href="https://github.com/devicons/devicon/issues/new?assignees=&labels=request%3Aicon&template=icon-request.md&title=Icon+request%3A+%5BNAME%5D">Request Icon</a>
        &middot;
        <a href="#contribute">Contribute</a>
    </p>
</div>

<h2>TL;DR</h2>

```html
<!-- in your header -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/devicon.min.css">

<!-- in your body -->
<i class="devicon-devicon-plain"></i>
```

<h2>Table of Contents</h2>
<ol>
    <li><a href="#about">About the Project</a></li>
    <li><a href="#getting-started">Getting Started</a></li>
    <li><a href="#request-icon">Requesting Icon</a></li>
    <li><a href="#contribute">Contributing</a></li>
    <li><a href="#discord-community">Discord Community</a></li>
    <li><a href="#develop-vs-master"><code>develop</code> vs <code>master</code></a></li>
    <li><a href="#stale-prs">Stale Pull Requests</a></li>
    <li><a href="#building-devicon">Building Devicon</a></li>
</ol>

<h2 id="about">About the Project</h2>
<p>
    Devicon aims to gather all logos representing development languages and tools.
    Each icon comes in several versions: font/SVG, original/plain/line, colored/not colored, wordmark/no wordmark.
    Devicon has 150+ icons. And it's growing!<br/>
</p>
<p>
    See the <a href="/devicon.json">devicon.json</a> or <a href="https://devicon.dev">our website</a> for complete and up to date reference of
    all available icons.
</p>

<p>
    Thanks to all our contributors and the <a href="https://icomoon.io/#home">IcoMoon app</a>. Devicon would not be possible without you.
</p>

<sub>
    All product names, logos, and brands are property of their respective owners. All company, product and service
    names used in this website are for identification purposes only. Use of these names, logos, and brands does not
    imply endorsement. Usage of these logos should be done according to the company/brand/service's brand policy.
</sub>

<h2 id="getting-started">Getting Started</h2>
<p>
    For a super fast setup, go check <a href="https://devicon.dev">devicon.dev</a>.<br />
    You can either use the <a href="#getting-started-svg">raw SVG</a> icons, our <a href="#getting-started-font">Devicon font</a> (which is
    also available via <a href=https://www.jsdelivr.com/package/npm/devicon>CDN</a>), or by <a href=#building-devicon>building Devicon</a> yourself.
</p>

<h3 id="getting-started-font">Use the <code>devicon</code> font (recommended)</h3>
<p>
    You can install devicon as a dependency to your project either with <code>npm</code> or <code>yarn</code>:
</p>

```bash
npm install --save devicon
yarn add devicon
```

<p>
    If you don't want to use a package manager, you can also download
    and include <a href="/devicon.min.css">devicon.min.css</a> next to the <a href="/fonts">font files</a> to your project.
    See <a href="https://devicon.dev">devicon.dev</a> for details about how to add Devicon to your project via
    a CDN.
</p>
<p>
    After setting up you just have to include the stylesheet in your header
    to get started:
</p>

```html
<link rel="stylesheet" href="devicon.min.css">
```

<p>Start using icons with <code>&lt;i&gt;</code>-tag:</p>

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
    An alternate way to use <code>devicon</code> is by copy/pasting the raw SVG code
    to your project.
</p>
<h3 id="getting-started-svg">Copy/paste SVG code (from the <a href="https://github.com/devicons/devicon/tree/master/icons">SVG folder</a> or the <a href="https://devicon.dev">project page</a>):</h3>

```html
<!--  for devicon plain version -->
<svg id="Devicon" class='devicon-devicon-plain' xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128"><path id="plain" fill="#60be86" d="M64,7.83H4.77L14.95,95.13l49,25,.06,0,49.07-25L123.23,7.83Zm42.77,54.86c0,.88,0,1.67-.77,2L73.25,80.44l-2.42,1.13-.27-3.15V72.23l.24-1.57,1.09-.47L95.07,59.81l-21.54-9.6L64.35,68.34,58.9,78.87l-1.22,2.27-2.05-.9L22,64.71a2.42,2.42,0,0,1-1.45-2V56.91a2.39,2.39,0,0,1,1.42-2l34-15.73,3.21-1.44v9.66l.24,1.34-1.56.7L34.45,59.79,56.3,69.42l8.05-16,6.21-12.65,1.13-2.28,1.81.91L106,54.89c.73.35.76,1.14.76,2Z"/></svg>
```

Add the following CSS rules in your stylesheet:

```css
.devicon-devicon-plain {
  max-width: 2em;
}

/* if you want to change the original color */
.devicon-devicon-plain path {
  fill: #4691f6;
}
```

<h4>You can also use the <code>img</code> tag and reference an SVG directly from the repository:</h4>

```html
<img src='https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/devicon/devicon-original.svg'>
```

<h2 id="request-icon">Requesting an icon</h2>
<p>
    When you want to request an icon please feel free to create an issue. Check out our <a href="https://github.com/devicons/devicon/wiki/Requesting-an-Icon">Wiki</a> for more information.
</p>

<h2 id="contribute">Contributing</h2>
<p>
    We are happy with every contribution, whether it's new icons, features, or maintainers. Please have a look at our <a href="https://github.com/devicons/devicon/wiki">Wiki</a> to see how you can contribute to this project.
</p>

<h2 id="discord-community">Discord community</h2>
<p>
We have a Discord community for Devicons. You can easily request icons, discuss, and have a good time talking with the community members! Join the official Discord Server <a href="https://discord.gg/hScy8KWACQ">here!</a>
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
        No icons for the latest SVGs. These will be built at every release.<br>
        Can be built manually. See <a href="#building-devicon"><i>Building Devicon</i></a>.
    </li>
    <li>
        Experimental changes.
    </li>
</ul>
<b><code>master</code> contains:</b>
<ul>
    <li>
        Latest official release, which contains all the SVGs and icons.
    </li>
    <li>
        Official, tested changes.
    </li>
</ul>

<h2 id="stale-prs">Stale Pull Requests</h2>
<p>
After a pull request has been open for over 30 days with no activity or response from the author, it'll be automatically marked as stale. We might fork your changes and merge the changes ourselves. Since GitHub tracks contributions by commits, you will be credited.
</p>

<h2 id="building-devicon">Building Devicon</h2>
<p>
Follow these steps to build the website and icons either locally or using <a href=https://www.gitpod.io>Gitpod.io</a>.
</p>

<h3>Table of contents</h3>
<ol>
    <li><a href="#using-gitpod">Using Gitpod to build</a></li>
    <li><a href="#local-installation">Local Installation</a></li>
    <ol>
      <li><a href="#install-dependencies">Install dependencies</a></li>
      <li><a href="#building-icons">Build the icons</a></li>
      <li><a href="#build-css">Build the CSS stylesheet</a></li>
      <li><a href="#web-server">Setting up the web server</a></li>
    </ol>
</ol>

<h2 id="using-gitpod">Using Gitpod.io</h2>
<p>By using <a href=https://www.gitpod.io)>Gitpod.io</a>, you can easily build the icons and install the<br>required dependencies in one single click. No extra setup is required.</p>

<a href=https://gitpod.io/#https://github.com/devicons/devicon/tree/develop><img src=https://gitpod.io/button/open-in-gitpod.svg alt="Open in Gitpod"></img></a>

> **Note**
> In case some of the commands are not properly ran, you can\
> follow the steps below and run the same commands on Gitpod.io

<h2 id="local-installation">Local Installation</h3>

<h3 id="install-dependencies">Install dependencies</h3>

<p><a href=https://github.com/devicons/devicon/fork>Fork</a> the repository and clone the forked repository.</p>

```bash
git clone https://github.com/<your-github-username>/devicon.git
```

> **Note**
> In case you don't have Git installed, check the <a href="https://git-scm.com/book/en/v2/Getting-Started-Installing-Git">official guide</a> to install Git on your operating system.

<h3>Install all the necessary NPM dependencies</h3>

```bash
npm install
```

> **Note**
> In case you don't have NPM installed, check this <a href=https://kinsta.com/blog/how-to-install-node-js/><b>ultimate guide</b></a> on installing Node.js and NPM. These tools are required in order to build Devicon properly.

<h3>Install Firefox</h3>
https://www.mozilla.org/en-US/firefox/new/

<h3>Install Python 3.8</h3>
https://www.python.org/downloads/

> **Note**
> Make sure your Python install includes [pip](https://pypi.org/project/pip/)

<h3>Install Selenium</h3>
```bash
python3 -m pip install --upgrade pip && pip install selenium==4.1.0 requests==2.25.1
```

<h3 id="building-icons">Build the new icons</h3>

<p>Once all the dependencies are installed, you can proceed to build the newest icons.<br>
Usually, this is done on each release, but you can have a sneak peek before a release.</p>

```bash
# Linux/Unix
npm run build-icons

# Windows
python3 ./.github/scripts/icomoon_build_githubless.py ./.github/scripts/build_assets/geckodriver-v0.32.2-win64/geckodriver.exe ./icomoon.json ./devicon.json ./icons ./ --headless
```

<i>The process might take a while, depending on your operating system's speed and the amount of icons.</i>
<p>If there are any errors shown, please let us know by <a href=https://github.com/devicons/devicon/issues/new/choose>creating an issue</a> or contacting us on our <a href=https://discord.gg/hScy8KWACQ>Discord community</a>.</p>

<h3 id="build-css">Build the CSS stylesheet</h3>

<p>Run the following command to build the new CSS stylesheet.<br>
This file is used to show all the new icons previously built.</p>

```bash
npm run build-css
```

<h3 id="web-server">Setting up the web server</h3>

<p>Run the following command to start the web server with Python.</p>

```bash
npm run dev # Will run on port 8000
```

<p>Or this command, which does exactly the same, but the port can be customized.</p>

```bash
python3 -m http.server <port>
```

<p>You're done now! :tada: Your build of Devicons should be available at <code>https://localhost:8000</code> (or the desired port).</p>

<br/>
<div align="center">
    <img src="https://forthebadge.com/images/badges/built-with-love.svg" />
    <img src="https://forthebadge.com/images/badges/built-by-developers.svg" />
</div>
