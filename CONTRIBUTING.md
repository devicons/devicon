<h1>Contributing to Devicon</h1>
<p>
First of all, thanks for taking the time to contribute! This project can only grow and live by your countless contributions. To keep this project maintable we developed some guidelines for contributions. 
</p>

<h2>Table of Content</h2>
<ul>
  <li><a href="#overview">Overview on Submitting Icon</a></li>
  <li><a href="#versionNaming">Naming Conventions</a></li>
  <li><a href="#svgStandards">SVG Standards</a></li>
  <li><a href="#orgGuidelines">Organizational Guidelines</a></li>
  <li><a href="#updateDevicon">Updating the <code>devicon.json</code></a></li>
  <li><a href="#example">Example</a></li>
  <li><a href="#requestingIcon">Requesting An Icon</a></li>
  <li><a href="#buildScript">Regarding the Build Script</a></li>
</ul>

<hr>
<h2 id="overview">Overview on Submitting Icon</h2>
<p>Here is an overview of what you have to do to submit your icons to the repo.</p>
<ol>
  <li>Create the svgs for each logo versions that you have </li>
  <li>Put the svgs for each logo into its own folders in <code>/fonts</code> </li>
  <li><a href="#updateDevicon">Update the <code>devicon.json</code> to include the new icon</a> </li>
  <li>Create a separated pull request (PR) for each icon (no matter how many versions). </li>
  <li>Include the name of the icon in the pull request title. Follow this format: <code>new icon: {{logoName}} ({{versions}})</code> </li>
  <li><i>Optional</i>: Add images of the new icon(s) to the description of the pull request. This would help speed up the review process </li>
  <li><i>Optional</i>: Reference the issues regarding the new icon. </li>
  <li>Wait for a repo maintainer to review your changes. Once they are satisfied, they will <a href="#buildScript">build your repo </a>. This will create a PR into your branch.</li>
  <li>Review the PR. It should contain the icon versions of your svgs. Accept the changes if you are satisfied</li>
  <li>Once you accept the changes, a maintainer will accept your PR into the repo.</li>
</ol>

<hr>
<h2 id='versionNaming'>Versions and Naming Conventions</h2>
<p>Each icon can come in different versions. So far, we have:</p>
<ul>
  <li><b>original</b>: the original logo. Can contains multiple colors. <a href="https://github.com/devicons/devicon/blob/master/icons/amazonwebservices/amazonwebservices-original.svg"> Example </a> </li>
  <li><b>original-wordmark</b>: similar to the above but must contain the name of the technology.<a href="https://github.com/devicons/devicon/blob/master/icons/amazonwebservices/amazonwebservices-original-wordmark.svg"> Example </a></li>
  <li><b>plain</b>: a one-color version of the original logo.<a href="https://github.com/devicons/devicon/blob/master/icons/android/android-plain.svg"> Example </a></li>
  <li><b>plain-wordmark</b>: a one-color version of the original logo but with wordmark.<a href="https://github.com/devicons/devicon/blob/master/icons/android/android-plain-wordmark.svg"> Example </a></li>
  <li><b>line</b>: a one-color, line version of the original logo.<a href="https://github.com/devicons/devicon/blob/master/icons/apache/apache-line.svg"> Example </a></li>
  <li><b>line-wordmark</b>: a one-color, line version of the original logo but with wordmark.<a href="https://github.com/devicons/devicon/blob/master/icons/apache/apache-line-wordmark.svg"> Example </a></li>
</ul>
<p>
It is not mandatory to have 6 versions for each icon. An icon can only have one or two versions available. Just keep in mind that the minimum is 1 and the maximum 6 (for now). You must also have at least one version that can be make into an icon.
</p>
<p>
The <b>plain</b> and <b>line</b> versions (with or without wordmark) are designed to be available in the final icon font.
</p>
<p>
The <b>original</b> version are only available in svg format, so they do not need to be as simple and can contain numerous colors.
</p>
<p>
Some icons are really simple (like the Apple one), so the original version can be used as the plain version and as the icon font. In this case, you'll only need to make only one of the version (either "original" or "plain"). You can then add an alias in the <code>devicon.json</code> so they can be found with either the "original" or "plain" naming convention.
</p>

<hr>
<h2 id='svgStandards'>SVG Standards</h2>
<p>Before you submit your logos/svgs, please ensure that they meet the following standard:</p>
<ul>
  <li>The background must be transparent.</li>
  <li>The <b>plain</b> and <b>line</b> versions (with or without wordmark) need to stay as simple as possible. They must have only one color and the paths are united before exporting to svg. 
  </li>
  <li>Optimize/compress your SVGs. You can use a service like <a href="https://compressor.io/">compressor</a> or <a href="https://petercollingridge.appspot.com/svg-editor">SVG Editor</a>.</li>
  <li>
</ul>

<hr>
<h2 id='orgGuidelines'>Organizational Guidelines</h2>
<ul>
  <li>Each icon has its own folder located in the <code>icons</code> folder</li>
  <li>Each icon folder contains one <code>.eps</code> file and as many <code>.svg</code> files as versions available</li>
  <li>The <code>.eps</code> file contains all available versions of an icon. Each version is contained in a 128px by 128px artboard</li>
  <li>Each <code>.svg</code> file contains one version of an icon in a <code>0 0 128 128</code> viewbox</li>
  <li>The naming convention for the svg file is the following: <code>(icon name)-(original|plain|line)-(wordmark)</code></li>
</ul>

<hr>
<h2 id='updateDevicon'> Updating the <code>devicon.json</code> </h2>
<p>
  Before you open a PR into Devicon, you'd have to update the <code>devicon.json</code>. This is essential for our build script to work and to document your work.
</p>
<p>
  Here is the object that each of your logo must have:
</p>

<pre>
  <code>
    {
        "name": string, // the official name of the technology. Must be lower case, no space or use the dash '-' character.
        "tags": string[], // list of tags relating to the technology for search purpose
        "versions": {
            "svg": VersionString[], // list the svgs that you have 
            "font": VersionString[] // list the fonts acceptable versions that you have
        },
        "color": string, // the main color of the logo. Only track 1 color
        "aliases": AliasObj[] // keeps track of the aliases
    }
  </code>
</pre>

<p>
  Here is the AliasObj interface:
</p>
<pre>
  <code>   
    {
        "base": VersionString, // the base version
        "alias": VersionString // the alias version that's similar to the base version
    }
  </code>
</pre>

<p>
  Here is what VersionString means:
</p>
<ol>
  <li> If you have "html5-original", the version string would be "original" </li>
  <li> If you have "react-line-wordmark", the version string would be "line-wordmark" </li>
  <li> See <a href="#iconFormat">Icon Formats and Naming Conventions</a> for more details </li>
</ol>

<hr>
<h2 id='example'>Example </h2>
<p>
As an example, let's assume you have created the svgs for Amazon Web Services and Redhat logos.
</p>
<p>For the Amazon Web Services svgs, you have the following versions: "original", "original-wordmark", "plain-wordmark". However, the "original" version is simple enough to be a "plain" version as well. Note that we are not using the acronym AWS.</p>
<p>For the Redhat svg, you have the "original", "original-wordmark", "plain", "plain-wordmark" versions. </p>
<ol>
  <li>
    Put the svgs for each logo that you have into its own folders in <code>/fonts</code>
    <ul>
      <li>This means you would create two folders: one for <code>amazonwebservices</code> and one for <code>redhat</code></li>
      <li><b>Note</b>: don't do this in the same commits. We want to have each logo in its own PR so don't create these two folders in the same commit</li>
    </ul>
  </li>
  <li>
    <a href="#updateDevicon">Update the <code>devicon.json</code> to include the icon (or variations)</a>
    <ul>
      <li>For the <code>amazonwebservices</code>, you would do this 
        <pre>
          <code>
            {
              "name": "amazonwebservices", 
              "tags": [
                "cloud",
                "hosting",
                "server"
              ],
              "versions": {
                "svg": [ // here are the versions that are available in svgs
                  "original",
                  "original-wordmark",
                  "plain-wordmark"
                ],
                "font": [ // here are the versions that are available as font icons
                  "original", // original is simple enough to be used as plain
                  "plain-wordmark"
                ]
              },
              "color": "#F7A80D", // note the '#' character
              "aliases": [
                {
                    "base": "original", // here is the base version aka the one that we will upload to Icomoon
                    "alias": "plain" // this is its alias. Our script will create a reference so we can search using "original" or "plain"
                }
              ]
            }
          </code>
        </pre>
      </li>
      <li>For the <code>redhat</code>, you would do this 
        <pre>
          <code>
            {
              "name": "redhat",
              "tags": [
                "server",
                "linux"
              ],
              "versions": {
                "svg": [
                  "original",
                  "original-wordmark",
                  "plain",
                  "plain-wordmark"
                ],
                "font": [
                  "plain",
                  "plain-wordmark"
                ]
              },
              "color": "#e93442",
              "aliases": [] // no aliases
            },
          </code>
        </pre>
      </li>
      <li><b>Note</b>: again, don't do this in the same commits. We want to have each logo in its own PR so don't create two folders in the same commit</li>
    </ul>
  </li>
  <li>Create a separated pull request (PR) for each icon (no matter how many variations).
    <ul>
      <li>This means you would have to create two PRs</li>
      <li>For Amazon Web Services, the branch name would be icons/amazonwebservices. </li>
      <li>For Redhat, the branch name would be icons/redhat. </li>
      <li> </li>
    </ul>
  </li>
  <li>
    Include the name of the icon in the pull request. Follow this format: "new icon: {{logoName}} ({{versions}})"
    <ul>
      <li>For Amazon Web Services, your PR title should be "new icon: amazonwebservices (original, original-wordmark, plain-wordmark)"</li>
      <li>For Redhat, your PR title should be "new icon: redhat (original, original-wordmark, plain, plain-wordmark)"</li>
    </ul>
  </li>
  <li>For the rest of the steps, you can follow <a href="#overview">Overview on Submitting Icon</a></li>
</ol>

<hr>
<h2 id='requestingIcon'>Requesting an Icon</h2>
<p>When you want to request a new icon please feel free to create a issue following some simple guidelines:</p>
<ul>
  <li>Search for other issues already requesting the icon</li>
  <li>If an issue doesn't exist, create an issue naming it "Icon request: <i>name-of-the-icon</i>". </li>
  <li>Please create separated issues for each icon</li>
  <li>optional: Include links where the icon can be found</li>
</ul>

<hr>
<h2 id='buildScript'>Regarding The Build Script</h2>
<p>To make adding icons easier for repo maintainers, we rely on GitHub Actions, Python, Selenium, and Gulp to automate our tasks.</p>
<p>So far, the tasks that we have automated are:</p>
<ul>
  <li>Upload svgs to <a href="https://icomoon.io/app/#/select">icomoon.io</a> and get the icons back. For details, see <a href="https://github.com/devicons/devicon/issues/252"> the original disscussion</a>, <a href="https://github.com/devicons/devicon/pull/268">this PR that introduce the feature</a> and <a href="https://github.com/devicons/devicon/issues/300">the final changes to it.</a></li>
  <li>Build, combine, and minify CSS files. For details, see <a href="https://github.com/devicons/devicon/pull/290">this</a></li>
  <li>Ensure code quality is up to standard</li>
</ul>